-- Resuelve debajo de cada enunciado sin abrir soluciones.

-- 1. Listar id, título, prioridad y estado de todos los incidentes,
--    ordenados primero por ALTA, luego MEDIA y luego BAJA.


-- 2. Mostrar los incidentes abiertos junto al nombre y correo
--    del solicitante.


-- 3. Mostrar todos los técnicos y el número de incidentes que tienen
--    asignados, incluyendo técnicos sin incidentes.


-- 4. Contar incidentes por estado y prioridad.


-- 5. Mostrar usuarios que nunca han sido asignados como técnicos.


-- 6. Obtener incidentes que no tienen ningún registro de historial.


-- 7. Mostrar el último evento de historial de cada incidente.


-- 8. Buscar títulos que contengan la palabra "reporte",
--    sin distinguir mayúsculas y minúsculas.


-- 9. Asignar el incidente 1 al técnico 2 y cambiarlo a EN_PROGRESO.
--    Ambas modificaciones (incidente + historial) deben estar
--    en una sola transacción.


-- 10. Intentar una modificación y ejecutar ROLLBACK para demostrar
--     que el cambio no queda persistido.


-- 11. Actualizar el incidente 2 a CERRADO usando control optimista:
--     solo debe actualizar si version = 0. Incrementar version.


-- 12. Crear una vista llamada vw_incidentes_activos con incidentes
--     ABIERTO o EN_PROGRESO, solicitante y técnico.


-- 13. Explicar con EXPLAIN la consulta que filtra por estado y prioridad.


-- 14. Crear una consulta parametrizable para filtrar opcionalmente
--     por estado. No construyas SQL concatenando entradas de usuario
--     desde Java.


-- 15. ¿Qué restricciones de la base evitan datos inválidos aunque
--     la aplicación Java tenga un error? Escríbelas como comentarios.

