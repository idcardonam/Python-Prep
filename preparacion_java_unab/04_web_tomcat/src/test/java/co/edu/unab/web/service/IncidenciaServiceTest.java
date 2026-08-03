package co.edu.unab.web.service;

import co.edu.unab.web.model.Prioridad;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class IncidenciaServiceTest {
    private final IncidenciaService service = new IncidenciaService();

    @Test
    void rechazaDatosInvalidos() {
        var errores = service.validar(
                "abc",
                "corta",
                "correo-invalido",
                "URGENTE");

        assertTrue(errores.containsKey("titulo"));
        assertTrue(errores.containsKey("descripcion"));
        assertTrue(errores.containsKey("correo"));
        assertTrue(errores.containsKey("prioridad"));
    }

    @Test
    void creaIncidenciaAbierta() {
        var errores = service.validar(
                "Error en matrícula",
                "El estudiante no puede confirmar la asignatura",
                "estudiante@unab.test",
                "ALTA");
        assertTrue(errores.isEmpty());

        var incidencia = service.crear(
                "Error en matrícula",
                "El estudiante no puede confirmar la asignatura",
                "estudiante@unab.test",
                Prioridad.ALTA);

        assertEquals(1, incidencia.id());
        assertEquals("ABIERTA", incidencia.estado().name());
        assertFalse(service.listar().isEmpty());
    }
}
