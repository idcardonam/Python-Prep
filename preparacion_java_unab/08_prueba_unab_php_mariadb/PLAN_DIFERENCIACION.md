# Plan de diferenciación — Prueba UNAB (PHP + MariaDB)

## Objetivo
Entregar un módulo de alerta temprana de deserción que se vea de alguien con experiencia institucional
(no solo de alguien que “completó el enunciado”).

## Valor agregado (lo que te resalta)
1. Arquitectura clara (config / modulos / sql / docs)
2. Seguridad real: prepared statements + escape HTML + validaciones de negocio
3. Mensajes humanos al usuario (no errores técnicos crudos)
4. Bitácora de acciones en archivo (sin alterar el modelo de BD)
5. README de decisiones técnicas (como en producción)
6. Panel de resumen (totales por nivel de riesgo) encima del DataTable
7. Comentarios en código con intención de negocio, no ruido

## Orden de construcción
1. Extraer estructura real de tablas
2. Mapear tablas a negocio
3. Conexion + helpers
4. CRUD variables
5. Stored procedure
6. Integracion PHP del SP
7. Reporte DataTables + resumen
8. Hardening seguridad + README entrega
