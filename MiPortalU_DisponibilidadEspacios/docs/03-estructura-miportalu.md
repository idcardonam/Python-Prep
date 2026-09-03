# Cómo está armado MiPortalU (para este proyecto)

Notas de la capacitación con Julián Ojeda (2 sep 2026). Sirven para no pelear con las convenciones del portal al crear el módulo.

## Estructura de carpetas

| Ruta | Qué va ahí |
| --- | --- |
| `assets/` | CSS, JavaScript y procesos compartidos |
| `modulos/` | Funcionalidad para estudiante o administrativo. **Aquí vive este proyecto.** Un proyecto nuevo = un módulo, salvo que sea mejora de uno existente. |
| `gestion de contenidos/` | Clases/funciones reutilizables y pantallas de gestión (pestaña administrativa). No mezclar módulos de estudiante aquí. |

El módulo actual a revisar es:

`modulos/disponibilidadAulas/disponibilidad.php`

La consulta nueva (clase PHP) debería ir donde el portal guarda las clases de negocio (gestión de contenidos / clases), no embebida en el HTML del módulo. Julián lo dijo explícitamente: a partir de las consultas de Reservitas se crea **el módulo y la clase** en el portal.

## Stack local

- PHP **5.6** en el Instant Client/XAMPP local. El portal en servidor está en 7.x y hay plan de migración; mientras tanto no usar sintaxis posterior a 5.6.
- Front del portal: **jQuery**. No hay otra librería global. Si el módulo necesita algo extra, se carga **dentro del módulo**.
- Iconos: Awesome. Alertas: SweetAlert (no `alert()` del navegador).
- Oracle Instant Client: en la sesión se corrigió una instalación de 64 bits; el entorno local del portal usa **32 bits**.
- Apache desde el panel (XAMPP/SAM). URL local: `localhost`.
- Imágenes de CDN interno no se ven en local; estilos y scripts sí.

## Bases de datos

| Base | Quién la gestiona | Implicación para este proyecto |
| --- | --- | --- |
| Esquema del portal (Oracle) | El equipo TIC puede crear tablas, vistas, procedimientos y funciones | Útil si hay que persistir algo propio del módulo. Esta consulta **no debería** duplicar el catálogo de espacios. |
| Banner TEST y PPRD | Se puede apuntar el entorno de desarrollo. En **producción** los scripts van a la DBA por INATE | Fuente de espacios y ocupación. Solo lectura. |
| Banner productivo | No autogestión | Esta iniciativa no escribe en Banner. |

Confirmar con Manuel García el usuario de solo lectura, el SID/servicio de TEST y los esquemas referenciados en el código de Reservitas.

## Git y despliegue (crítico)

- Repositorio interno en **GitLab** (no público). Requiere red interna o VPN si se está fuera del campus.
- Rama principal del portal a cargo de Julián. Cada ingeniero trabaja en rama propia.
- Rama de Iván creada en la sesión: **PPRD-IC** (PPR + IC).
- **Antes de hacer push**, avisar a Julián. El script de despliegue **cifra los PHP**. Si dos personas suben a la vez, se han corrompido archivos en el servidor.
- Probar primero en **MiPortalU PPRD** (contraseñas genéricas de prueba) y después pasar al funcional.

Localmente, en la capacitación, el login usaba la contraseña del correo / portal productivo. Las genéricas aún no estaban habilitadas en local.

## Estructura mínima de una página interna

Julián dejó el esqueleto en el chat de la reunión. Replicarlo al tocar el módulo:

1. Includes del menú lateral (aunque el menú vaya a desaparecer, se sigue cargando).
2. Clase PHP nueva del módulo (consultas, no lógica en la vista).
3. Librerías opcionales: Awesome + SweetAlert.
4. Footer.
5. A partir de ahí, el HTML/JS del módulo.

## Qué hacer Iván en el código (orden)

1. Confirmar que el clone local abre `localhost` y entra al portal.
2. Abrir `modulos/disponibilidadAulas/` completo: PHP, includes, JS, CSS.
3. No reescribir la UI todavía. Primero documentar enlaces y parámetros.
4. Cuando exista Reservitas, ubicar el PHP de consulta (en la reunión se mencionó algo tipo `day.php`; hay que confirmarlo en el código real).
5. Extraer conexión, query/vista/procedimiento y reglas de tipo/sede/horario.
6. Recién ahí proponer si la clase nueva del portal llama la misma vista o arma una capa equivalente.
