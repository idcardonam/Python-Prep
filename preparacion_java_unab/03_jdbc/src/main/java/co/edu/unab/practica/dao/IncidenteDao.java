package co.edu.unab.practica.dao;

import co.edu.unab.practica.model.Estado;
import co.edu.unab.practica.model.Incidente;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Optional;

public interface IncidenteDao {
    Incidente crear(Connection connection, Incidente incidente) throws SQLException;

    Optional<Incidente> buscarPorId(Connection connection, long id) throws SQLException;

    List<Incidente> listar(Connection connection) throws SQLException;

    boolean actualizarEstado(
            Connection connection,
            long id,
            int versionEsperada,
            Estado nuevoEstado,
            Long tecnicoId) throws SQLException;
}
