-- =============================================================================
-- P_CALCULAR_RIESGO_ESTUDIANTE  (nombres REALES de prueba_ing)
-- =============================================================================
-- Reglas del enunciado:
-- - Solo GWRPIEM_MATRICULADO = 'Y'
-- - Suma GWRPIVR_PESO donde:
--     GWRPICE_PRESENTA_RIESGO = 'Y'
--     GWRPICE_ACTIVO = 'Y'
--     GWRPIVR_ACTIVO = 'Y'
-- - Puntaje = LEAST(suma, 100)
-- - BAJO 0-29.99 | MEDIO 30-59.99 | ALTO 60-100
-- - GWRPIRR_VARIABLES_RIESGO = cantidad de variables que aportaron
-- - Una fila por (periodo, estudiante): UPDATE si existe, INSERT si no
-- - NO COMMIT/ROLLBACK aquí (lo controla PHP)
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
    DECLARE v_done INT DEFAULT 0;

    DECLARE v_id_est VARCHAR(20);
    DECLARE v_puntaje DECIMAL(5,2);
    DECLARE v_nivel VARCHAR(10);
    DECLARE v_vars INT;
    DECLARE v_existe INT;

    DECLARE cur_calc CURSOR FOR
        SELECT id_estudiante, puntaje, nivel_riesgo, variables_riesgo
        FROM tmp_riesgo_calc;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1 v_msg = MESSAGE_TEXT;
        SET v_error = 1;
    END;

    SET P_CODIGO = 0;
    SET P_MENSAJE = 'OK';

    IF P_PERIODO IS NULL OR TRIM(P_PERIODO) = '' THEN
        SET P_CODIGO = 100;
        SET P_MENSAJE = 'El período es obligatorio.';
        LEAVE proc_body;
    END IF;

    IF P_USUARIO IS NULL OR TRIM(P_USUARIO) = '' THEN
        SET P_CODIGO = 101;
        SET P_MENSAJE = 'El usuario de cálculo es obligatorio.';
        LEAVE proc_body;
    END IF;

    IF P_ID_ESTUDIANTE IS NULL OR TRIM(P_ID_ESTUDIANTE) = '' THEN
        SET P_CODIGO = 102;
        SET P_MENSAJE = 'Indique un ID de estudiante o % para recálculo masivo.';
        LEAVE proc_body;
    END IF;

    DROP TEMPORARY TABLE IF EXISTS tmp_riesgo_calc;
    CREATE TEMPORARY TABLE tmp_riesgo_calc (
        id_estudiante VARCHAR(20) NOT NULL PRIMARY KEY,
        puntaje DECIMAL(5,2) NOT NULL,
        nivel_riesgo VARCHAR(10) NOT NULL,
        variables_riesgo SMALLINT UNSIGNED NOT NULL
    );

    INSERT INTO tmp_riesgo_calc (id_estudiante, puntaje, nivel_riesgo, variables_riesgo)
    SELECT
        em.GWRPIEM_ID_ESTUDIANTE,
        LEAST(IFNULL(SUM(CASE
            WHEN ce.GWRPICE_ID IS NOT NULL THEN vr.GWRPIVR_PESO
            ELSE 0
        END), 0), 100) AS puntaje,
        CASE
            WHEN LEAST(IFNULL(SUM(CASE WHEN ce.GWRPICE_ID IS NOT NULL THEN vr.GWRPIVR_PESO ELSE 0 END), 0), 100) >= 60 THEN 'ALTO'
            WHEN LEAST(IFNULL(SUM(CASE WHEN ce.GWRPICE_ID IS NOT NULL THEN vr.GWRPIVR_PESO ELSE 0 END), 0), 100) >= 30 THEN 'MEDIO'
            ELSE 'BAJO'
        END AS nivel_riesgo,
        IFNULL(SUM(CASE WHEN ce.GWRPICE_ID IS NOT NULL THEN 1 ELSE 0 END), 0) AS variables_riesgo
    FROM GWRPIEM em
    LEFT JOIN GWRPICE ce
        ON ce.GWRPICE_ID_ESTUDIANTE = em.GWRPIEM_ID_ESTUDIANTE
       AND ce.GWRPICE_PERIODO = em.GWRPIEM_PERIODO
       AND ce.GWRPICE_PRESENTA_RIESGO = 'Y'
       AND ce.GWRPICE_ACTIVO = 'Y'
    LEFT JOIN GWRPIVR vr
        ON vr.GWRPIVR_ID = ce.GWRPICE_ID_VARIABLE
       AND vr.GWRPIVR_ACTIVO = 'Y'
    WHERE em.GWRPIEM_MATRICULADO = 'Y'
      AND em.GWRPIEM_PERIODO = P_PERIODO
      AND (P_ID_ESTUDIANTE = '%' OR em.GWRPIEM_ID_ESTUDIANTE = P_ID_ESTUDIANTE)
    GROUP BY em.GWRPIEM_ID_ESTUDIANTE;

    IF v_error = 1 THEN
        SET P_CODIGO = 200;
        SET P_MENSAJE = CONCAT('Error preparando cálculo: ', v_msg);
        LEAVE proc_body;
    END IF;

    SELECT COUNT(*) INTO v_procesados FROM tmp_riesgo_calc;
    IF v_procesados = 0 THEN
        SET P_CODIGO = 201;
        SET P_MENSAJE = 'No hay estudiantes matriculados para calcular con esos parámetros.';
        LEAVE proc_body;
    END IF;

    SET v_done = 0;
    OPEN cur_calc;

    read_loop: LOOP
        FETCH cur_calc INTO v_id_est, v_puntaje, v_nivel, v_vars;
        IF v_done = 1 OR v_error = 1 THEN
            LEAVE read_loop;
        END IF;

        SELECT COUNT(*) INTO v_existe
        FROM GWRPIRR
        WHERE GWRPIRR_PERIODO = P_PERIODO
          AND GWRPIRR_ID_ESTUDIANTE = v_id_est;

        IF v_existe > 0 THEN
            UPDATE GWRPIRR
               SET GWRPIRR_PUNTAJE_FINAL = v_puntaje,
                   GWRPIRR_NIVEL_RIESGO = v_nivel,
                   GWRPIRR_VARIABLES_RIESGO = v_vars,
                   GWRPIRR_FECHA_CALCULO = NOW(),
                   GWRPIRR_USUARIO_CALCULO = P_USUARIO
             WHERE GWRPIRR_PERIODO = P_PERIODO
               AND GWRPIRR_ID_ESTUDIANTE = v_id_est;
        ELSE
            INSERT INTO GWRPIRR (
                GWRPIRR_PERIODO,
                GWRPIRR_ID_ESTUDIANTE,
                GWRPIRR_PUNTAJE_FINAL,
                GWRPIRR_NIVEL_RIESGO,
                GWRPIRR_VARIABLES_RIESGO,
                GWRPIRR_FECHA_CALCULO,
                GWRPIRR_USUARIO_CALCULO
            ) VALUES (
                P_PERIODO,
                v_id_est,
                v_puntaje,
                v_nivel,
                v_vars,
                NOW(),
                P_USUARIO
            );
        END IF;
    END LOOP;

    CLOSE cur_calc;

    IF v_error = 1 THEN
        SET P_CODIGO = 202;
        SET P_MENSAJE = CONCAT('Error guardando GWRPIRR: ', v_msg);
        LEAVE proc_body;
    END IF;

    SET P_CODIGO = 0;
    SET P_MENSAJE = CONCAT('Cálculo exitoso. Estudiantes procesados: ', v_procesados, '.');
END //

DELIMITER ;
