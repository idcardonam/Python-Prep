package co.edu.unab.practica.service;

import co.edu.unab.practica.dao.IncidenteDao;
import co.edu.unab.practica.db.ConexionFactory;
import co.edu.unab.practica.model.Estado;
import co.edu.unab.practica.model.Incidente;
import co.edu.unab.practica.model.Prioridad;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;
import java.util.Optional;

public final class IncidenteService {
    private final ConexionFactory conexiones;
    private final IncidenteDao dao;

    public IncidenteService(ConexionFactory conexiones, IncidenteDao dao) {
        this.conexiones = conexiones;
        this.dao = dao;
    }

    public Incidente crear(
            String titulo,
            String descripcion,
            Prioridad prioridad,
            long solicitanteId) throws SQLException {
        validarTexto(titulo, 5, 120, "título");
        validarTexto(descripcion, 10, 2000, "descripción");
        if (prioridad == null) {
            throw new IllegalArgumentException("La prioridad es obligatoria");
        }
        if (solicitanteId <= 0) {
            throw new IllegalArgumentException("El solicitante es inválido");
        }

        try (Connection connection = conexiones.abrir()) {
            return dao.crear(
                    connection,
                    Incidente.nuevo(titulo.trim(), descripcion.trim(), prioridad, solicitanteId));
        }
    }

    public Optional<Incidente> buscar(long id) throws SQLException {
        try (Connection connection = conexiones.abrir()) {
            return dao.buscarPorId(connection, id);
        }
    }

    public List<Incidente> listar() throws SQLException {
        try (Connection connection = conexiones.abrir()) {
            return dao.listar(connection);
        }
    }

    public Incidente cambiarEstado(
            long incidenteId,
            int versionEsperada,
            Estado nuevoEstado,
            long usuarioResponsableId,
            Long tecnicoId,
            String comentario) throws SQLException {
        validarTexto(comentario, 3, 500, "comentario");

        try (Connection connection = conexiones.abrir()) {
            boolean autoCommitOriginal = connection.getAutoCommit();
            try {
                connection.setAutoCommit(false);

                Incidente actual = dao.buscarPorId(connection, incidenteId)
                        .orElseThrow(() -> new IllegalArgumentException("Incidente no encontrado"));

                validarTransicion(actual.getEstado(), nuevoEstado);

                boolean actualizado = dao.actualizarEstado(
                        connection,
                        incidenteId,
                        versionEsperada,
                        nuevoEstado,
                        tecnicoId);
                if (!actualizado) {
                    throw new IllegalStateException(
                            "Conflicto: el incidente fue modificado por otro usuario");
                }

                insertarHistorial(
                        connection,
                        incidenteId,
                        usuarioResponsableId,
                        actual.getEstado(),
                        nuevoEstado,
                        comentario);

                connection.commit();
                return dao.buscarPorId(connection, incidenteId)
                        .orElseThrow(() -> new SQLException("El incidente desapareció"));
            } catch (Exception error) {
                try {
                    connection.rollback();
                } catch (SQLException rollbackError) {
                    error.addSuppressed(rollbackError);
                }
                if (error instanceof SQLException sqlError) {
                    throw sqlError;
                }
                if (error instanceof RuntimeException runtimeError) {
                    throw runtimeError;
                }
                throw new SQLException("Error inesperado al cambiar estado", error);
            } finally {
                connection.setAutoCommit(autoCommitOriginal);
            }
        }
    }

    private void insertarHistorial(
            Connection connection,
            long incidenteId,
            long usuarioId,
            Estado anterior,
            Estado nuevo,
            String comentario) throws SQLException {
        String sql = """
                INSERT INTO historial_incidente (
                    incidente_id, usuario_id, estado_anterior,
                    estado_nuevo, comentario
                ) VALUES (?, ?, ?, ?, ?)
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setLong(1, incidenteId);
            statement.setLong(2, usuarioId);
            statement.setString(3, anterior.name());
            statement.setString(4, nuevo.name());
            statement.setString(5, comentario.trim());
            if (statement.executeUpdate() != 1) {
                throw new SQLException("No se insertó el historial");
            }
        }
    }

    private void validarTransicion(Estado actual, Estado nuevo) {
        if (nuevo == null) {
            throw new IllegalArgumentException("El nuevo estado es obligatorio");
        }
        boolean permitida = switch (actual) {
            case ABIERTO -> nuevo == Estado.EN_PROGRESO;
            case EN_PROGRESO -> nuevo == Estado.CERRADO;
            case CERRADO -> false;
        };
        if (!permitida) {
            throw new IllegalStateException("Transición no permitida: " + actual + " -> " + nuevo);
        }
    }

    private void validarTexto(String valor, int minimo, int maximo, String campo) {
        if (valor == null || valor.trim().length() < minimo || valor.trim().length() > maximo) {
            throw new IllegalArgumentException(
                    "El campo %s debe tener entre %d y %d caracteres"
                            .formatted(campo, minimo, maximo));
        }
    }
}
