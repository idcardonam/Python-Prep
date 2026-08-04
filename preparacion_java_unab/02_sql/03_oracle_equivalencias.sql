/*
DIFERENCIAS ESENCIALES: POSTGRESQL Y ORACLE

No memorices todas las particularidades. Aprende a reconocer qué cambia
y a consultar la documentación del motor disponible.
*/

-- 1. IDENTIDAD

-- PostgreSQL
CREATE TABLE ejemplo_pg (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- Oracle 12c+
CREATE TABLE ejemplo_oracle (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- Oracle tradicional
-- CREATE SEQUENCE ejemplo_seq START WITH 1 INCREMENT BY 1;
-- INSERT INTO ejemplo (id) VALUES (ejemplo_seq.NEXTVAL);


-- 2. TIPOS FRECUENTES

-- PostgreSQL              Oracle
-- BIGINT                  NUMBER(19)
-- INTEGER                 NUMBER(10)
-- BOOLEAN                 NUMBER(1) o CHAR(1) en tablas
-- VARCHAR(n)              VARCHAR2(n)
-- TEXT                    CLOB
-- TIMESTAMP               TIMESTAMP
-- BYTEA                   BLOB


-- 3. FECHA ACTUAL

-- PostgreSQL
SELECT CURRENT_TIMESTAMP;

-- Oracle
-- SELECT SYSTIMESTAMP FROM dual;


-- 4. CONCATENACIÓN

-- Ambos admiten:
SELECT 'Java' || ' y SQL';


-- 5. LÍMITE DE FILAS

-- PostgreSQL y Oracle moderno
SELECT *
FROM incidente
ORDER BY fecha_creacion DESC
FETCH FIRST 5 ROWS ONLY;

-- PostgreSQL también admite LIMIT 5.
-- Oracle antiguo utiliza ROWNUM o una subconsulta.


-- 6. CADENAS VACÍAS

-- PostgreSQL diferencia '' de NULL.
-- Oracle trata la cadena vacía como NULL.


-- 7. INSENSIBILIDAD A MAYÚSCULAS

-- PostgreSQL ofrece ILIKE:
SELECT *
FROM incidente
WHERE titulo ILIKE '%reporte%';

-- Portabilidad:
SELECT *
FROM incidente
WHERE LOWER(titulo) LIKE LOWER('%reporte%');


-- 8. UPSERT

-- PostgreSQL:
-- INSERT ... ON CONFLICT (...) DO UPDATE

-- Oracle:
-- MERGE INTO ... USING ... WHEN MATCHED ... WHEN NOT MATCHED ...


-- 9. BLOQUEO

-- Ambos soportan:
SELECT *
FROM incidente
WHERE id = 1
FOR UPDATE;


-- 10. PROCEDIMIENTOS

-- PostgreSQL usa PL/pgSQL como lenguaje habitual.
-- Oracle usa PL/SQL.


-- 11. JDBC

-- PostgreSQL:
-- jdbc:postgresql://localhost:5432/unab_practica
-- driver: org.postgresql.Driver

-- Oracle:
-- jdbc:oracle:thin:@//host:1521/servicio
-- driver: oracle.jdbc.OracleDriver


-- 12. PLAN DE EJECUCIÓN

-- PostgreSQL:
EXPLAIN SELECT * FROM incidente WHERE estado = 'ABIERTO';

-- Oracle:
-- EXPLAIN PLAN FOR SELECT ...;
-- SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);


/*
RESPUESTA SEGURA EN UNA PRUEBA:

"Mi experiencia práctica principal es SQL sobre PostgreSQL. Los
fundamentos de modelo relacional, joins, transacciones, índices,
restricciones y PreparedStatement son transferibles. En Oracle
revisaría tipos NUMBER/VARCHAR2, secuencias o identity, manejo de
cadena vacía, PL/SQL y plan de ejecución antes de llevar un cambio
a producción."
*/
