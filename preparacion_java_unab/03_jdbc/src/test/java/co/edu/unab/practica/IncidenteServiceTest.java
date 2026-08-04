package co.edu.unab.practica;

import co.edu.unab.practica.dao.JdbcIncidenteDao;
import co.edu.unab.practica.db.ConexionFactory;
import co.edu.unab.practica.model.Estado;
import co.edu.unab.practica.model.Incidente;
import co.edu.unab.practica.model.Prioridad;
import co.edu.unab.practica.service.IncidenteService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIfEnvironmentVariable;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@EnabledIfEnvironmentVariable(named = "DB_URL", matches = ".+")
class IncidenteServiceTest {

    @Test
    void creaActualizaYRechazaVersionAntigua() throws Exception {
        IncidenteService service = new IncidenteService(
                ConexionFactory.desdeEntorno(),
                new JdbcIncidenteDao());

        Incidente creado = service.crear(
                "Prueba de integración",
                "Registro temporal para comprobar JDBC",
                Prioridad.BAJA,
                1);

        Incidente actualizado = service.cambiarEstado(
                creado.getId(),
                creado.getVersion(),
                Estado.EN_PROGRESO,
                2,
                2L,
                "Inicio de atención en prueba");

        assertEquals(Estado.EN_PROGRESO, actualizado.getEstado());
        assertEquals(creado.getVersion() + 1, actualizado.getVersion());

        assertThrows(
                IllegalStateException.class,
                () -> service.cambiarEstado(
                        actualizado.getId(),
                        creado.getVersion(),
                        Estado.CERRADO,
                        2,
                        2L,
                        "Versión antigua"));
    }
}
