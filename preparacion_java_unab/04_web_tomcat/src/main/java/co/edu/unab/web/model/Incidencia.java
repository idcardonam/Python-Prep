package co.edu.unab.web.model;

import java.time.LocalDateTime;

public record Incidencia(
        long id,
        String titulo,
        String descripcion,
        String correo,
        Prioridad prioridad,
        Estado estado,
        LocalDateTime fechaCreacion) {
}
