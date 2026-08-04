package co.edu.unab.practica;

import co.edu.unab.practica.dao.JdbcIncidenteDao;
import co.edu.unab.practica.db.ConexionFactory;
import co.edu.unab.practica.model.Estado;
import co.edu.unab.practica.model.Incidente;
import co.edu.unab.practica.model.Prioridad;
import co.edu.unab.practica.service.IncidenteService;

public final class App {
    private App() {
    }

    public static void main(String[] args) throws Exception {
        IncidenteService service = new IncidenteService(
                ConexionFactory.desdeEntorno(),
                new JdbcIncidenteDao());

        System.out.println("Incidentes actuales:");
        service.listar().forEach(System.out::println);

        Incidente creado = service.crear(
                "Práctica JDBC",
                "Incidente creado desde la aplicación Java",
                Prioridad.MEDIA,
                1);
        System.out.println("\nCreado: " + creado);

        Incidente actualizado = service.cambiarEstado(
                creado.getId(),
                creado.getVersion(),
                Estado.EN_PROGRESO,
                2,
                2L,
                "El técnico inicia la atención");
        System.out.println("Actualizado: " + actualizado);

        try {
            service.cambiarEstado(
                    actualizado.getId(),
                    creado.getVersion(),
                    Estado.CERRADO,
                    2,
                    2L,
                    "Intento con versión antigua");
        } catch (IllegalStateException e) {
            System.out.println("Conflicto esperado: " + e.getMessage());
        }
    }
}
