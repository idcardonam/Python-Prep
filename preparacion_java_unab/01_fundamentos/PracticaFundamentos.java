import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Archivo inicial del laboratorio.
 *
 * Compilar:
 *   javac PracticaFundamentos.java
 *
 * Ejecutar:
 *   java PracticaFundamentos
 */
public class PracticaFundamentos {

    public static boolean correoValido(String correo) {
        // TODO: ejercicio 1
        return false;
    }

    public static double calcularTotalHoras(double horas, double valorHora) {
        // TODO: ejercicio 2
        return 0;
    }

    public static int horasMaximasRespuesta(Prioridad prioridad) {
        // TODO: ejercicio 3
        return 0;
    }

    public static void main(String[] args) {
        // TODO: ejercicio 10
        System.out.println("Completa los ejercicios de ENUNCIADOS.md");
    }
}

enum Prioridad {
    BAJA, MEDIA, ALTA
}

enum Estado {
    ABIERTO, EN_PROGRESO, CERRADO
}

class Incidente {
    // TODO: ejercicios 4 y 5
}

class GestorIncidentes {
    private final List<Incidente> incidentes = new ArrayList<>();

    public void agregar(Incidente incidente) {
        // TODO: ejercicio 6
    }

    public Optional<Incidente> buscarPorId(long id) {
        // TODO: ejercicio 6
        return Optional.empty();
    }

    public List<Incidente> buscarPorEstado(Estado estado) {
        // TODO: ejercicio 6
        return List.of();
    }

    public Map<Prioridad, Long> contarPorPrioridad() {
        // TODO: ejercicio 7
        return Map.of();
    }

    public Incidente obtenerObligatorio(long id) {
        // TODO: ejercicio 8
        throw new UnsupportedOperationException("Pendiente");
    }

    public List<Incidente> ordenarPorPrioridadEId() {
        // TODO: ejercicio 9
        return List.of();
    }
}

class IncidenteNoEncontradoException extends RuntimeException {
    public IncidenteNoEncontradoException(String mensaje) {
        super(mensaje);
    }
}
