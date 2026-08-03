package co.edu.unab.practica.dao;

import co.edu.unab.practica.model.Estado;
import co.edu.unab.practica.model.Incidente;
import co.edu.unab.practica.model.Prioridad;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public final class JdbcIncidenteDao implements IncidenteDao {

    @Override
    public Incidente crear(Connection connection, Incidente incidente) throws SQLException {
        String sql = """
                INSERT INTO incidente (
                    titulo, descripcion, prioridad, estado, solicitante_id
                ) VALUES (?, ?, ?, ?, ?)
                """;

        try (PreparedStatement statement =
                     connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, incidente.getTitulo());
            statement.setString(2, incidente.getDescripcion());
            statement.setString(3, incidente.getPrioridad().name());
            statement.setString(4, incidente.getEstado().name());
            statement.setLong(5, incidente.getSolicitanteId());

            int filas = statement.executeUpdate();
            if (filas != 1) {
                throw new SQLException("Se esperaba insertar una fila y se insertaron " + filas);
            }

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (!keys.next()) {
                    throw new SQLException("La base no devolvió el id generado");
                }
                return buscarPorId(connection, keys.getLong(1))
                        .orElseThrow(() -> new SQLException("No fue posible recuperar el incidente"));
            }
        }
    }

    @Override
    public Optional<Incidente> buscarPorId(Connection connection, long id) throws SQLException {
        String sql = """
                SELECT id, titulo, descripcion, prioridad, estado,
                       solicitante_id, tecnico_id, fecha_creacion, version
                FROM incidente
                WHERE id = ?
                """;

        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setLong(1, id);
            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next()
                        ? Optional.of(mapear(resultSet))
                        : Optional.empty();
            }
        }
    }

    @Override
    public List<Incidente> listar(Connection connection) throws SQLException {
        String sql = """
                SELECT id, titulo, descripcion, prioridad, estado,
                       solicitante_id, tecnico_id, fecha_creacion, version
                FROM incidente
                ORDER BY fecha_creacion DESC, id DESC
                """;

        List<Incidente> resultado = new ArrayList<>();
        try (PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            while (resultSet.next()) {
                resultado.add(mapear(resultSet));
            }
        }
        return List.copyOf(resultado);
    }

    @Override
    public boolean actualizarEstado(
            Connection connection,
            long id,
            int versionEsperada,
            Estado nuevoEstado,
            Long tecnicoId) throws SQLException {
        String sql = """
                UPDATE incidente
                SET estado = ?,
                    tecnico_id = ?,
                    fecha_actualizacion = CURRENT_TIMESTAMP,
                    version = version + 1
                WHERE id = ?
                  AND version = ?
                """;

        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, nuevoEstado.name());
            if (tecnicoId == null) {
                statement.setNull(2, java.sql.Types.BIGINT);
            } else {
                statement.setLong(2, tecnicoId);
            }
            statement.setLong(3, id);
            statement.setInt(4, versionEsperada);
            return statement.executeUpdate() == 1;
        }
    }

    private Incidente mapear(ResultSet resultSet) throws SQLException {
        long tecnico = resultSet.getLong("tecnico_id");
        Long tecnicoId = resultSet.wasNull() ? null : tecnico;
        Timestamp fecha = resultSet.getTimestamp("fecha_creacion");

        return new Incidente(
                resultSet.getLong("id"),
                resultSet.getString("titulo"),
                resultSet.getString("descripcion"),
                Prioridad.valueOf(resultSet.getString("prioridad")),
                Estado.valueOf(resultSet.getString("estado")),
                resultSet.getLong("solicitante_id"),
                tecnicoId,
                fecha.toLocalDateTime(),
                resultSet.getInt("version"));
    }
}
