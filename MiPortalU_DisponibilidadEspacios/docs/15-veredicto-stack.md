# Veredicto de stack — encaje con la plantilla de Julián

Fecha: 3 sep 2026.

## Decisión

**No React SPA.**  
**Sí: plantilla Julián (PHP módulo + clase) + UI moderna en CSS/JS del módulo (jQuery/Vanilla + SweetAlert + Font Awesome).**

Eso es lo que mejor compagina con MiPortalU, las 4 capas y el deploy actual.

| Opción | ¿Encaja con Julián? | Veredicto |
| --- | --- | --- |
| React app aparte (Vite/CRA, otro puerto) | No — otra sesión, otro menú, otro deploy | Descartada para este proyecto |
| React embebido (build → un `.js` en assets) | Forzado — PHP 5.6, curva, OK de Julián/Jonathan | Fase 2 solo si lo piden |
| **Módulo PHP + clase + CSS/JS moderno** | **Sí — es la ley** | **Elegida** |

“De cero” y “bonito” = **nueva experiencia dentro del portal**, no nuevo framework.

## Qué era el `test_conexion.php` que enviaste

No prueba Banner/Oracle. Prueba (comentado) un **INSERT** a MySQL `mrbs_room` vía `conec.php` → `$link` (mysqli).

Eso es el catálogo **local de Reservitas** (áreas/salones en MRBS), no la ocupación académica.

| Pieza | Tecnología | ¿La usamos en MiPortalU aulas? |
| --- | --- | --- |
| Ocupación del día (materias) | Oracle `BANINST1.V_RESERVAS_SALON` | **Sí — núcleo** |
| Catálogo `mrbs_room` / `conec.php` | MySQL Reservitas | **No ideal** — acopla al legado; preferir rooms desde Banner o catálogo propio del portal |
| Insert de prueba en `test_conexion` | Escritura MySQL | **No** — nuestro módulo es solo lectura |

Conclusión: ese archivo confirma el mundo MySQL de Reservitas. **Para aulas necesitamos el patrón de conexión Oracle del portal** (otra clase o include de MiPortalU), no este insert.

## Arquitectura elegida (detalle)

```text
modulos/disponibilidadAulas/disponibilidad.php   ← plantilla Julián (capa vista)
        │
        ▼
gestionContenidos/clases/DisponibilidadAulas.php ← nueva clase (capa negocio)
        │
        ▼
Conexión Oracle TEST (solo SELECT)               ← capa datos Banner
        │
        ▼
BANINST1.V_RESERVAS_SALON
```

Assets: CSS/JS bajo el módulo o `/assets/...` solo para esta pantalla (grilla, tabs, estados disponible/ocupado).

## Qué pedir ahora (sustituye el test MySQL)

1. **A Manuel / Julián:**  
   > ¿Cómo se conecta MiPortalU a Banner Oracle en TEST? ¿Hay clase o `conec` del portal (no el `conec.php` de Reservitas)? Necesito un ejemplo de `oci_connect` / PDO OCI de solo lectura.

2. Si existe en el portal algo tipo `test_conexion` **Oracle**, ese sí; el de `mrbs_room` no.

3. Sin ejemplo de clase aún: la primera clase del proyecto será `DisponibilidadAulas.php` siguiendo `nuevaClase.php` vacío/plantilla.

## UI “interesante” sin React

- Tabs tipo / sede / fecha (mockup mejorado).
- Tarjetas o grilla clara: libre = verde suave, ocupado = bloque con nombre de materia (sin docente).
- Transiciones CSS, iconos FA, SweetAlert en “sin resultados” / error de conexión.
- Aviso fijo: consulta informativa, fuente Banner.
- Responsive.

Todo dentro de `#conten_central`.
