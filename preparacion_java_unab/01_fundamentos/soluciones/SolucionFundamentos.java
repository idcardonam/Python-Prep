import java.util.ArrayList;
import java.util.Comparator;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

public class SolucionFundamentos {

    public static boolean correoValido(String correo) {
        if (correo == null || correo.isBlank()) {
            return false;
        }
        int arroba = correo.indexOf('@');
        int punto = correo.lastIndexOf('.');
        return arroba > 0 && punto > arroba + 1 && punto < correo.length() - 1;
    }

    public static double calcularTotalHoras(double horas, double valorHora) {
        if (horas < 0 || valorHora < 0) {
            throw new IllegalArgumentException("Horas y valor deben ser positivos");
        }
        double normales = Math.min(horas, 8);
        double extras = Math.max(horas - 8, 0);
        return normales * valorHora + extras * valorHora * 1.25;
    }

    public static int horasMaximasRespuesta(SolucionPrioridad prioridad) {
        Objects.requireNonNull(prioridad, "La prioridad es obligatoria");
        return switch (prioridad) {
            case ALTA -> 2;
            case MEDIA -> 8;
            case BAJA -> 24;
        };
    }

    public static void main(String[] args) {
        SolucionGestorIncidentes gestor = new SolucionGestorIncidentes();
        gestor.agregar(new SolucionIncidente(1, "Fallo en portal", "El portal no permite ingresar", SolucionPrioridad.ALTA));
        gestor.agregar(new SolucionIncidente(2, "Reporte errado", "El consolidado presenta diferencias", SolucionPrioridad.MEDIA));
        gestor.agregar(new SolucionIncidente(3, "Cambio de clave", "El usuario requiere nueva contraseña", SolucionPrioridad.BAJA));
        gestor.agregar(new SolucionIncidente(4, "Error de matrícula", "No aparece una asignatura inscrita", SolucionPrioridad.ALTA));
        gestor.agregar(new SolucionIncidente(5, "Consulta de nota", "El estudiante solicita una validación", SolucionPrioridad.MEDIA));

        gestor.obtenerObligatorio(1).cambiarEstado(SolucionEstado.EN_PROGRESO);
        gestor.obtenerObligatorio(2).cambiarEstado(SolucionEstado.EN_PROGRESO);
        gestor.obtenerObligatorio(2).cambiarEstado(SolucionEstado.CERRADO);

        System.out.println(gestor.contarPorPrioridad());
        System.out.println(gestor.buscarPorEstado(SolucionEstado.EN_PROGRESO));
        System.out.println(gestor.ordenarPorPrioridadEId());

        try {
            gestor.obtenerObligatorio(3).cambiarEstado(SolucionEstado.CERRADO);
        } catch (IllegalStateException e) {
            System.out.println("Transición rechazada correctamente: " + e.getMessage());
        }
    }
}

enum SolucionPrioridad {
    BAJA, MEDIA, ALTA
}

enum SolucionEstado {
    ABIERTO, EN_PROGRESO, CERRADO
}

final class SolucionIncidente {
    private final long id;
    private final String titulo;
    private final String descripcion;
    private final SolucionPrioridad prioridad;
    private SolucionEstado estado;

    SolucionIncidente(long id, String titulo, String descripcion, SolucionPrioridad prioridad) {
        if (id <= 0) {
            throw new IllegalArgumentException("El id debe ser positivo");
        }
        if (titulo == null || titulo.trim().length() < 5) {
            throw new IllegalArgumentException("El título debe tener mínimo 5 caracteres");
        }
        if (descripcion == null || descripcion.trim().length() < 10) {
            throw new IllegalArgumentException("La descripción debe tener mínimo 10 caracteres");
        }
        this.id = id;
        this.titulo = titulo.trim();
        this.descripcion = descripcion.trim();
        this.prioridad = Objects.requireNonNull(prioridad, "La prioridad es obligatoria");
        this.estado = SolucionEstado.ABIERTO;
    }

    long getId() {
        return id;
    }

    String getTitulo() {
        return titulo;
    }

    String getDescripcion() {
        return descripcion;
    }

    SolucionPrioridad getPrioridad() {
        return prioridad;
    }

    SolucionEstado getEstado() {
        return estado;
    }

    void cambiarEstado(SolucionEstado nuevoEstado) {
        Objects.requireNonNull(nuevoEstado, "El estado es obligatorio");
        boolean permitida = switch (estado) {
            case ABIERTO -> nuevoEstado == SolucionEstado.EN_PROGRESO;
            case EN_PROGRESO -> nuevoEstado == SolucionEstado.CERRADO;
            case CERRADO -> false;
        };
        if (!permitida) {
            throw new IllegalStateException("Transición no permitida: " + estado + " -> " + nuevoEstado);
        }
        estado = nuevoEstado;
    }

    @Override
    public String toString() {
        return "Incidente{id=%d, titulo='%s', prioridad=%s, estado=%s}"
                .formatted(id, titulo, prioridad, estado);
    }
}

final class SolucionGestorIncidentes {
    private final List<SolucionIncidente> incidentes = new ArrayList<>();

    void agregar(SolucionIncidente incidente) {
        Objects.requireNonNull(incidente, "El incidente es obligatorio");
        if (buscarPorId(incidente.getId()).isPresent()) {
            throw new IllegalArgumentException("Ya existe el id " + incidente.getId());
        }
        incidentes.add(incidente);
    }

    Optional<SolucionIncidente> buscarPorId(long id) {
        return incidentes.stream()
                .filter(incidente -> incidente.getId() == id)
                .findFirst();
    }

    List<SolucionIncidente> buscarPorEstado(SolucionEstado estado) {
        return incidentes.stream()
                .filter(incidente -> incidente.getEstado() == estado)
                .toList();
    }

    Map<SolucionPrioridad, Long> contarPorPrioridad() {
        Map<SolucionPrioridad, Long> conteo = new EnumMap<>(SolucionPrioridad.class);
        for (SolucionPrioridad prioridad : SolucionPrioridad.values()) {
            conteo.put(prioridad, 0L);
        }
        for (SolucionIncidente incidente : incidentes) {
            conteo.compute(incidente.getPrioridad(), (clave, total) -> total + 1);
        }
        return Map.copyOf(conteo);
    }

    SolucionIncidente obtenerObligatorio(long id) {
        return buscarPorId(id)
                .orElseThrow(() -> new SolucionIncidenteNoEncontradoException("No existe el incidente " + id));
    }

    List<SolucionIncidente> ordenarPorPrioridadEId() {
        Comparator<SolucionIncidente> comparador = Comparator
                .comparingInt((SolucionIncidente incidente) -> orden(incidente.getPrioridad()))
                .thenComparingLong(SolucionIncidente::getId);
        return incidentes.stream().sorted(comparador).toList();
    }

    private int orden(SolucionPrioridad prioridad) {
        return switch (prioridad) {
            case ALTA -> 1;
            case MEDIA -> 2;
            case BAJA -> 3;
        };
    }
}

class SolucionIncidenteNoEncontradoException extends RuntimeException {
    SolucionIncidenteNoEncontradoException(String mensaje) {
        super(mensaje);
    }
}
