-- 1
SELECT id, titulo, prioridad, estado
FROM incidente
ORDER BY CASE prioridad
    WHEN 'ALTA' THEN 1
    WHEN 'MEDIA' THEN 2
    WHEN 'BAJA' THEN 3
END, id;

-- 2
SELECT i.id, i.titulo, u.nombre, u.correo
FROM incidente i
JOIN usuario_tic u ON u.id = i.solicitante_id
WHERE i.estado = 'ABIERTO'
ORDER BY i.fecha_creacion;

-- 3
SELECT u.id, u.nombre, COUNT(i.id) AS total_asignados
FROM usuario_tic u
LEFT JOIN incidente i ON i.tecnico_id = u.id
WHERE u.rol = 'TECNICO'
GROUP BY u.id, u.nombre
ORDER BY u.nombre;

-- 4
SELECT estado, prioridad, COUNT(*) AS total
FROM incidente
GROUP BY estado, prioridad
ORDER BY estado, prioridad;

-- 5
SELECT u.*
FROM usuario_tic u
WHERE u.rol = 'TECNICO'
  AND NOT EXISTS (
      SELECT 1
      FROM incidente i
      WHERE i.tecnico_id = u.id
  );

-- 6
SELECT i.*
FROM incidente i
WHERE NOT EXISTS (
    SELECT 1
    FROM historial_incidente h
    WHERE h.incidente_id = i.id
);

-- 7
SELECT i.id, i.titulo, h.estado_nuevo, h.comentario, h.fecha
FROM incidente i
LEFT JOIN LATERAL (
    SELECT estado_nuevo, comentario, fecha
    FROM historial_incidente
    WHERE incidente_id = i.id
    ORDER BY fecha DESC, id DESC
    FETCH FIRST 1 ROW ONLY
) h ON TRUE
ORDER BY i.id;

-- En Oracle moderno puede resolverse con ROW_NUMBER() OVER
-- (PARTITION BY incidente_id ORDER BY fecha DESC, id DESC).

-- 8
SELECT *
FROM incidente
WHERE LOWER(titulo) LIKE LOWER('%reporte%');

-- Desde Java se debe usar:
-- WHERE LOWER(titulo) LIKE LOWER(?)
-- y statement.setString(1, "%reporte%");

-- 9
BEGIN;

UPDATE incidente
SET tecnico_id = 2,
    estado = 'EN_PROGRESO',
    fecha_actualizacion = CURRENT_TIMESTAMP,
    version = version + 1
WHERE id = 1
  AND estado = 'ABIERTO';

INSERT INTO historial_incidente (
    incidente_id, usuario_id, estado_anterior, estado_nuevo, comentario
) VALUES (
    1, 2, 'ABIERTO', 'EN_PROGRESO', 'Incidente asignado al técnico'
);

COMMIT;

-- 10
BEGIN;
UPDATE incidente SET titulo = 'Cambio temporal' WHERE id = 1;
ROLLBACK;
SELECT titulo FROM incidente WHERE id = 1;

-- 11
UPDATE incidente
SET estado = 'CERRADO',
    fecha_actualizacion = CURRENT_TIMESTAMP,
    version = version + 1
WHERE id = 2
  AND version = 0
  AND estado = 'EN_PROGRESO';

-- La aplicación debe comprobar que se actualizó exactamente una fila.

-- 12
CREATE OR REPLACE VIEW vw_incidentes_activos AS
SELECT
    i.id,
    i.titulo,
    i.prioridad,
    i.estado,
    solicitante.nombre AS solicitante,
    tecnico.nombre AS tecnico
FROM incidente i
JOIN usuario_tic solicitante ON solicitante.id = i.solicitante_id
LEFT JOIN usuario_tic tecnico ON tecnico.id = i.tecnico_id
WHERE i.estado IN ('ABIERTO', 'EN_PROGRESO');

-- 13
EXPLAIN
SELECT *
FROM incidente
WHERE estado = 'ABIERTO'
  AND prioridad = 'ALTA';

-- 14
-- Una alternativa estable para PreparedStatement:
SELECT *
FROM incidente
WHERE (? IS NULL OR estado = ?);

-- En Java se establece el mismo valor en ambos parámetros.

-- 15
-- PRIMARY KEY: identificadores únicos y no nulos.
-- FOREIGN KEY: usuarios existentes.
-- NOT NULL: campos obligatorios.
-- UNIQUE: correos sin duplicar.
-- CHECK: roles, prioridad, estado y longitudes válidas.
