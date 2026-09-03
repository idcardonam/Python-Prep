# Flujo actual vs. experiencia esperada

## Flujo actual

```text
Estudiante autenticado en MiPortalU
        │
        ▼
modulos/disponibilidadAulas/disponibilidad.php
        │
        │  elige tipo (informática / salones / auditorios)
        │  y sede/campus
        ▼
Redirección a Reservitas (id_tipo + parámetros de sede)
        │
        ▼
Reservitas consulta ocupación (Banner u origen por validar)
        │
        ▼
El estudiante ve disponibilidad fuera de MiPortalU
```

Lo que hay que extraer de `disponibilidad.php`:

- Includes, sesión y layout del portal.
- HTML de los tres tipos y de las sedes.
- URL de destino hacia Reservitas.
- Query string completo (`id_tipo`, sede, otros).
- JS/CSS propios del módulo, si existen.
- Si hay lógica PHP de negocio o es solo un menú de enlaces.

## Flujo esperado

```text
Estudiante autenticado en MiPortalU
        │
        ▼
Módulo Disponibilidad de espacios (misma familia de menú)
        │
        │  tipo + fecha + campus + edificio/área + franja
        ▼
Capa de consulta en MiPortalU (reutilizada o nueva)
        │
        ▼
Banner (fuente institucional: vista / query / procedimiento)
        │
        ▼
Resultados en el portal: tarjetas + agenda del día
        │
        X  no crea reservas
        X  no muestra responsable
```

## Pantalla objetivo (mockup)

El HTML en `mockup/disponibilidad-espacios.html` no es diseño cerrado. Sirve para alinear la experiencia:

1. Selector de tipo: informática, salones, auditorios.
2. Filtros: fecha (hoy por defecto), campus, edificio/área (dependiente), desde, hasta.
3. Accesos rápidos: solo disponibles, disponibles ahora, hoy.
4. Resultado en tarjetas: código, ubicación, estado, mini línea de tiempo del día.
5. “Ver horario del día”: matriz hora × espacio (disponible / ocupado).
6. Aviso visible: consulta informativa; reservas se gestionan en Banner.

Campus de ejemplo en el mockup (validar contra datos reales): Campus El Jardín, Campus El Bosque, CSU, Instituto Caldas, La Casona.

Códigos de ejemplo: `ED-ING-L51-AINF`, `ED-APP-CUB 10`, `ED-ING-AUD JARM`. El código institucional real sale de Banner/Reservitas, no del mockup.

## Privacidad

No mostrar responsable ni datos personales de una reserva si el estudiante no los necesita. Si la consulta legado trae nombre, omitirlo en la capa de presentación.

## Criterio de equivalencia

Antes de construir la UI definitiva, probar al menos tres escenarios contra Reservitas (misma fecha, tipo y campus) y confirmar el mismo conjunto de espacios disponibles/ocupados. Si no coincide, no se avanza a implementación amplia.
