DROP TABLE IF EXISTS historial_incidente;
DROP TABLE IF EXISTS incidente;
DROP TABLE IF EXISTS usuario_tic;

CREATE TABLE usuario_tic (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR(120) NOT NULL,
    correo          VARCHAR(254) NOT NULL UNIQUE,
    rol             VARCHAR(20) NOT NULL,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_usuario_rol
        CHECK (rol IN ('SOLICITANTE', 'TECNICO', 'ADMINISTRADOR'))
);

CREATE TABLE incidente (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo              VARCHAR(120) NOT NULL,
    descripcion         VARCHAR(2000) NOT NULL,
    prioridad           VARCHAR(10) NOT NULL,
    estado              VARCHAR(20) NOT NULL DEFAULT 'ABIERTO',
    solicitante_id      BIGINT NOT NULL,
    tecnico_id          BIGINT NULL,
    fecha_creacion      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version             INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT fk_incidente_solicitante
        FOREIGN KEY (solicitante_id) REFERENCES usuario_tic(id),
    CONSTRAINT fk_incidente_tecnico
        FOREIGN KEY (tecnico_id) REFERENCES usuario_tic(id),
    CONSTRAINT ck_incidente_prioridad
        CHECK (prioridad IN ('BAJA', 'MEDIA', 'ALTA')),
    CONSTRAINT ck_incidente_estado
        CHECK (estado IN ('ABIERTO', 'EN_PROGRESO', 'CERRADO')),
    CONSTRAINT ck_incidente_titulo
        CHECK (CHAR_LENGTH(TRIM(titulo)) >= 5),
    CONSTRAINT ck_incidente_descripcion
        CHECK (CHAR_LENGTH(TRIM(descripcion)) >= 10)
);

CREATE TABLE historial_incidente (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    incidente_id    BIGINT NOT NULL,
    usuario_id      BIGINT NOT NULL,
    estado_anterior VARCHAR(20) NULL,
    estado_nuevo    VARCHAR(20) NOT NULL,
    comentario      VARCHAR(500) NOT NULL,
    fecha           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historial_incidente
        FOREIGN KEY (incidente_id) REFERENCES incidente(id) ON DELETE CASCADE,
    CONSTRAINT fk_historial_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario_tic(id)
);

CREATE INDEX ix_incidente_estado_prioridad
    ON incidente (estado, prioridad);

CREATE INDEX ix_incidente_solicitante
    ON incidente (solicitante_id);

CREATE INDEX ix_historial_incidente_fecha
    ON historial_incidente (incidente_id, fecha);

INSERT INTO usuario_tic (nombre, correo, rol) VALUES
    ('Ana Solicitante', 'ana@unab.test', 'SOLICITANTE'),
    ('Carlos Técnico', 'carlos@unab.test', 'TECNICO'),
    ('Laura Técnica', 'laura@unab.test', 'TECNICO'),
    ('Mario Administrador', 'mario@unab.test', 'ADMINISTRADOR');

INSERT INTO incidente (
    titulo, descripcion, prioridad, estado,
    solicitante_id, tecnico_id, fecha_creacion
) VALUES
    ('Error en matrícula', 'El estudiante no puede confirmar una asignatura', 'ALTA', 'ABIERTO', 1, NULL, CURRENT_TIMESTAMP - INTERVAL '3 hours'),
    ('Reporte financiero', 'El reporte presenta una diferencia en el consolidado', 'MEDIA', 'EN_PROGRESO', 1, 2, CURRENT_TIMESTAMP - INTERVAL '2 days'),
    ('Cambio de contraseña', 'El usuario necesita restablecer sus credenciales', 'BAJA', 'CERRADO', 1, 3, CURRENT_TIMESTAMP - INTERVAL '5 days'),
    ('Fallo de integración', 'La aplicación no recibe respuesta del servicio académico', 'ALTA', 'EN_PROGRESO', 1, 2, CURRENT_TIMESTAMP - INTERVAL '1 day'),
    ('Consulta de calificación', 'El docente solicita validar la nota registrada', 'MEDIA', 'ABIERTO', 1, NULL, CURRENT_TIMESTAMP - INTERVAL '4 hours');

INSERT INTO historial_incidente (
    incidente_id, usuario_id, estado_anterior, estado_nuevo, comentario
) VALUES
    (2, 2, 'ABIERTO', 'EN_PROGRESO', 'Se inicia revisión del reporte'),
    (3, 3, 'ABIERTO', 'EN_PROGRESO', 'Se valida identidad del usuario'),
    (3, 3, 'EN_PROGRESO', 'CERRADO', 'Credencial restablecida'),
    (4, 2, 'ABIERTO', 'EN_PROGRESO', 'Se revisan logs de integración');
