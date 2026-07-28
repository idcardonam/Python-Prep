-- =============================================================================
-- P_CALCULAR_RIESGO_ESTUDIANTE
-- Prueba técnica UNAB — Alerta temprana de deserción
-- =============================================================================
-- Reglas:
-- 1) Solo estudiantes GWRPIEM_MATRICULADO = 'Y'
-- 2) Suma pesos de variables con:
--      GWRPICE_PRESENTA_RIESGO = 'Y'
--      GWRPICE_ACTIVO = 'Y'
--      GWRPIVR_ACTIVO = 'Y'
-- 3) Puntaje = LEAST(suma, 100)
-- 4) BAJO 0-29.99 | MEDIO 30-59.99 | ALTO 60-100
-- 5) Una fila por estudiante+periodo en GWRPIRR (upsert)
-- 6) NO hacer COMMIT/ROLLBACK aquí (lo controla PHP)
--
-- IMPORTANTE: si ver_estructura.php muestra nombres distintos de columnas,
-- ajusta SOLO los nombres de campo; no cambies la lógica de negocio.
-- =============================================================================

DROP PROCEDURE IF EXISTS P_CALCULAR_RIESGO_ESTUDIANTE;

DELIMITER //

CREATE PROCEDURE P_CALCULAR_RIESGO_ESTUDIANTE(
    IN  P_PERIODO       VARCHAR(6),
    IN  P_ID_ESTUDIANTE VARCHAR(20),
    IN  P_USUARIO       VARCHAR(50),
    OUT P_CODIGO        INT,
    OUT P_MENSAJE       VARCHAR(500)
)
proc_body: BEGIN
    DECLARE v_error INT DEFAULT 0;
    DECLARE v_msg   VARCHAR(500) DEFAULT '';
    DECLARE v_procesados INT DEFAULT 0;

    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1 v_msg = MESSAGE_TEXT;
        SET v_error = 1;
    END;

    SET P_CODIGO = 0;
    SET P_MENSAJE = 'OK';

    IF P_PERIODO IS NULL OR TRIM(P_PERIODO) = '' THEN
        SET P_CODIGO = 100;
        SET P_MENSAJE = 'El período es obligatorio (formato sugerido AAAAPP).';
        LEAVE proc_body;
    END IF;

    IF P_USUARIO IS NULL OR TRIM(P_USUARIO) = '' THEN
        SET P_CODIGO = 101;
        SET P_MENSAJE = 'El usuario de cálculo es obligatorio para auditoría.';
        LEAVE proc_body;
    END IF;

    IF P_ID_ESTUDIANTE IS NULL OR TRIM(P_ID_ESTUDIANTE) = '' THEN
        SET P_CODIGO = 102;
        SET P_MENSAJE = 'Debe indicar un ID de estudiante o % para recálculo masivo.';
        LEAVE proc_body;
    END IF;

    /*
      Cursor lógico vía INSERT...SELECT / UPDATE.
      Se procesa:
        - un estudiante si P_ID_ESTUDIANTE <> '%'
        - todos los matriculados del período si P_ID_ESTUDIANTE = '%'
    */

    -- Temporary result set of scores to upsert
    DROP TEMPORARY TABLE IF EXISTS tmp_riesgo_calc;
    CREATE TEMPORARY TABLE tmp_riesgo_calc (
        id_estudiante VARCHAR(20) NOT NULL,
        periodo       VARCHAR(6)  NOT NULL,
        puntaje       DECIMAL(10,2) NOT NULL,
        nivel_riesgo  VARCHAR(10) NOT NULL,
        variables     VARCHAR(1000) NULL,
        PRIMARY KEY (id_estudiante, periodo)
    );

    INSERT INTO tmp_riesgo_calc (id_estudiante, periodo, puntaje, nivel_riesgo, variables)
    SELECT
        em.GWRPIEM_ID AS id_estudiante,
        P_PERIODO AS periodo,
        LEAST(IFNULL(SUM(vr.GWRPIVR_PESO), 0), 100) AS puntaje,
        CASE
            WHEN LEAST(IFNULL(SUM(vr.GWRPIVR_PESO), 0), 100) >= 60 THEN 'ALTO'
            WHEN LEAST(IFNULL(SUM(vr.GWRPIVR_PESO), 0), 100) >= 30 THEN 'MEDIO'
            ELSE 'BAJO'
        END AS nivel_riesgo,
        GROUP_CONCAT(DISTINCT vr.GWRPIVR_CODIGO ORDER BY vr.GWRPIVR_CODIGO SEPARATOR ',') AS variables
    FROM GWRPIEM em
    LEFT JOIN GWRPICE ce
        ON ce.GWRPICE_ID_ESTUDIANTE = em.GWRPIEM_ID
       AND ce.GWRPICE_PRESENTA_RIESGO = 'Y'
       AND ce.GWRPICE_ACTIVO = 'Y'
    LEFT JOIN GWRPIVR vr
        ON vr.GWRPIVR_CODIGO = ce.GWRPICE_COD_VARIABLE
       AND vr.GWRPIVR_ACTIVO = 'Y'
    WHERE em.GWRPIEM_MATRICULADO = 'Y'
      AND (P_ID_ESTUDIANTE = '%' OR em.GWRPIEM_ID = P_ID_ESTUDIANTE)
      AND (em.GWRPIEM_PERIODO = P_PERIODO OR em.GWRPIEM_PERIODO IS NULL OR em.GWRPIEM_PERIODO = '')
      /*
        Nota: si GWRPIEM no tiene columna de período, elimina la línea de período
        y filtra solo por matriculado. Ajusta tras ver_estructura.php
      */
    GROUP BY em.GWRPIEM_ID;

    IF v_error = 1 THEN
        SET P_CODIGO = 200;
        SET P_MENSAJE = CONCAT('Error preparando cálculo: ', v_msg);
        LEAVE proc_body;
    END IF;

    SELECT COUNT(*) INTO v_procesados FROM tmp_riesgo_calc;

    IF v_procesados = 0 THEN
        SET P_CODIGO = 201;
        SET P_MENSAJE = 'No se encontraron estudiantes matriculados para calcular con los criterios indicados.';
        LEAVE proc_body;
    END IF;

    -- Upsert a GWRPIRR (una fila por estudiante+período)
    INSERT INTO GWRPIRR (
        GWRPIRR_ID_ESTUDIANTE,
        GWRPIRR_PERIODO,
        GWRPIRR_PUNTAJE,
        GWRPIRR_NIVEL_RIESGO,
        GWRPIRR_VARIABLES,
        GWRPIRR_USER_CALC,
        GWRPIRR_DATE_CALC
    )
    SELECT
        t.id_estudiante,
        t.periodo,
        t.puntaje,
        t.nivel_riesgo,
        t.variables,
        P_USUARIO,
        NOW()
    FROM tmp_riesgo_calc t
    ON DUPLICATE KEY UPDATE
        GWRPIRR_PUNTAJE = VALUES(GWRPIRR_PUNTAJE),
        GWRPIRR_NIVEL_RIESGO = VALUES(GWRPIRR_NIVEL_RIESGO),
        GWRPIRR_VARIABLES = VALUES(GWRPIRR_VARIABLES),
        GWRPIRR_USER_CALC = VALUES(GWRPIRR_USER_CALC),
        GWRPIRR_DATE_CALC = VALUES(GWRPIRR_DATE_CALC);

    IF v_error = 1 THEN
        SET P_CODIGO = 202;
        SET P_MENSAJE = CONCAT('Error guardando resultados en GWRPIRR: ', v_msg,
                               '. Verifique llave única (estudiante, período) y nombres de columnas.');
        LEAVE proc_body;
    END IF;

    SET P_CODIGO = 0;
    SET P_MENSAJE = CONCAT('Cálculo exitoso. Estudiantes procesados: ', v_procesados, '.');
END //

DELIMITER ;
