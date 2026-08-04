package co.edu.unab.practica.model;

import java.time.LocalDateTime;
import java.util.Objects;

public final class Incidente {
    private final Long id;
    private final String titulo;
    private final String descripcion;
    private final Prioridad prioridad;
    private final Estado estado;
    private final long solicitanteId;
    private final Long tecnicoId;
    private final LocalDateTime fechaCreacion;
    private final int version;

    public Incidente(
            Long id,
            String titulo,
            String descripcion,
            Prioridad prioridad,
            Estado estado,
            long solicitanteId,
            Long tecnicoId,
            LocalDateTime fechaCreacion,
            int version) {
        this.id = id;
        this.titulo = Objects.requireNonNull(titulo);
        this.descripcion = Objects.requireNonNull(descripcion);
        this.prioridad = Objects.requireNonNull(prioridad);
        this.estado = Objects.requireNonNull(estado);
        this.solicitanteId = solicitanteId;
        this.tecnicoId = tecnicoId;
        this.fechaCreacion = fechaCreacion;
        this.version = version;
    }

    public static Incidente nuevo(
            String titulo,
            String descripcion,
            Prioridad prioridad,
            long solicitanteId) {
        return new Incidente(
                null,
                titulo,
                descripcion,
                prioridad,
                Estado.ABIERTO,
                solicitanteId,
                null,
                null,
                0);
    }

    public Long getId() {
        return id;
    }

    public String getTitulo() {
        return titulo;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public Prioridad getPrioridad() {
        return prioridad;
    }

    public Estado getEstado() {
        return estado;
    }

    public long getSolicitanteId() {
        return solicitanteId;
    }

    public Long getTecnicoId() {
        return tecnicoId;
    }

    public LocalDateTime getFechaCreacion() {
        return fechaCreacion;
    }

    public int getVersion() {
        return version;
    }

    @Override
    public String toString() {
        return "Incidente{id=%s, titulo='%s', prioridad=%s, estado=%s, version=%d}"
                .formatted(id, titulo, prioridad, estado, version);
    }
}
