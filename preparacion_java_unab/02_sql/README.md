# Laboratorio 2 · SQL PostgreSQL y Oracle

## Objetivo

Practicar modelado, integridad, consultas, transacciones y diferencias de sintaxis.

## Preparación

```bash
PGPASSWORD=practica_local psql \
  -h localhost -U unab_practica -d unab_practica \
  -f 01_esquema_postgresql.sql
```

Entrar a la consola:

```bash
PGPASSWORD=practica_local psql \
  -h localhost -U unab_practica -d unab_practica
```

Comandos útiles de `psql`:

```text
\dt                 listar tablas
\d incidente        describir tabla
\i archivo.sql      ejecutar archivo
\x                  vista expandida
\q                  salir
```

## Orden

1. Lee `01_esquema_postgresql.sql`.
2. Explica las claves, restricciones e índices.
3. Resuelve `02_ejercicios.sql`.
4. Prueba cada consulta.
5. Compara con `soluciones/02_soluciones.sql`.
6. Estudia `03_oracle_equivalencias.sql`.

## Preguntas que debes poder responder

- ¿Por qué una clave foránea protege la integridad?
- ¿Cuándo usar `INNER JOIN` y cuándo `LEFT JOIN`?
- ¿Por qué un índice acelera lecturas pero tiene costo en escrituras?
- ¿Qué diferencia existe entre `WHERE` y `HAVING`?
- ¿Qué hacen `COMMIT` y `ROLLBACK`?
- ¿Cómo evita `PreparedStatement` la inyección SQL?
- ¿Qué cambia entre `GENERATED AS IDENTITY` en PostgreSQL y Oracle?
