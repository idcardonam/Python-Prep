package co.edu.unab.web.service;

import co.edu.unab.web.model.Estado;
import co.edu.unab.web.model.Incidencia;
import co.edu.unab.web.model.Prioridad;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public final class IncidenciaService {
    private final AtomicLong secuencia = new AtomicLong();
    private final Map<Long, Incidencia> incidencias = new ConcurrentHashMap<>();

    public Map<String, String> validar(
            String titulo,
            String descripcion,
            String correo,
            String prioridadTexto) {
        Map<String, String> errores = new LinkedHashMap<>();
        if (titulo == null || titulo.trim().length() < 5 || titulo.trim().length() > 120) {
            errores.put("titulo", "El título debe tener entre 5 y 120 caracteres");
        }
        if (descripcion == null
                || descripcion.trim().length() < 10
                || descripcion.trim().length() > 2000) {
            errores.put("descripcion", "La descripción debe tener entre 10 y 2000 caracteres");
        }
        if (correo == null || !correo.matches("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$")) {
            errores.put("correo", "El correo no tiene un formato válido");
        }
        try {
            Prioridad.valueOf(prioridadTexto);
        } catch (IllegalArgumentException | NullPointerException e) {
            errores.put("prioridad", "Seleccione una prioridad válida");
        }
        return Map.copyOf(errores);
    }

    public Incidencia crear(
            String titulo,
            String descripcion,
            String correo,
            Prioridad prioridad) {
        long id = secuencia.incrementAndGet();
        Incidencia incidencia = new Incidencia(
                id,
                titulo.trim(),
                descripcion.trim(),
                correo.trim().toLowerCase(),
                prioridad,
                Estado.ABIERTA,
                LocalDateTime.now());
        incidencias.put(id, incidencia);
        return incidencia;
    }

    public List<Incidencia> listar() {
        List<Incidencia> resultado = new ArrayList<>(incidencias.values());
        resultado.sort(Comparator.comparing(Incidencia::fechaCreacion).reversed());
        return List.copyOf(resultado);
    }
}
