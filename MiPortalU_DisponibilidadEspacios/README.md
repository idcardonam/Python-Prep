# Disponibilidad de espacios en MiPortalU

**Universidad Autónoma de Bucaramanga (UNAB) · TIC**  
**Responsable de exploración e implementación:** Iván Cardona  
**Revisión de hallazgos:** lunes (próxima sesión con el equipo)

Este paquete consolida la capacitación de MiPortalU (2 sep 2026), el correo de arranque, la guía de ingeniería y el mockup. El objetivo es que Iván llegue al lunes con el flujo claro, la alternativa técnica recomendada y el siguiente paso de construcción.

## Qué vamos a hacer

Traer a **MiPortalU** la consulta de disponibilidad de aulas, salones y auditorios que hoy se abre en **Reservitas**. El estudiante consulta sin salir del portal. **Banner sigue siendo la fuente.** Las reservas **no** se crean ni se editan desde MiPortalU.

Hoy el portal solo redirige a Reservitas. El servidor de Reservitas está obsoleto, con problemas de seguridad y PHP antiguo; esta migración es la meta del año para esa consulta.

## Alcance de esta etapa (hasta el lunes)

1. Revisar `modulos/disponibilidadAulas/disponibilidad.php` en MiPortalU.
2. Documentar los enlaces actuales a Reservitas (tipos, campus, parámetros).
3. Cuando llegue la carpeta de Reservitas, ubicar la consulta a Banner (espacios y ocupación).
4. Micro sesión con **Carlos Duarte**: reutilizar la consulta actual o reconstruirla en MiPortalU.
5. Micro sesión con **Manuel García**: accesos de solo lectura en TEST (SQL Developer).
6. Si hace falta, sesiones cortas con **Julián Ojeda** sobre estructura del portal.
7. Llevar al lunes: hallazgos, alternativa recomendada y siguiente actividad.

La carpeta de desarrollo de Reservitas ya fue solicitada. Sin ella no se cierra la fuente de datos.

## Fuera de alcance

- Crear, editar o cancelar reservas.
- Replicar la lógica de programación de Banner.
- Catálogo paralelo de espacios en MiPortalU.
- Reserva de equipos (otro frente; se evalúa Percoa).
- Proyecto de Bienestar (asignado a Marlon).

## Equipo

| Persona | Rol en este proyecto |
| --- | --- |
| Iván Cardona | Exploración, propuesta técnica e implementación en MiPortalU |
| Jonathan Espinel | Encargo del proyecto, contexto funcional y gestión de la carpeta Reservitas |
| Julián Ojeda | Estructura de MiPortalU, GitLab, ambiente local, convenciones de módulos |
| Carlos Duarte | Validar si se reutiliza la vista/consulta actual de espacios |
| Manuel García | Accesos y permisos de solo lectura en TEST vía SQL Developer |

## Documentos de este paquete

| Archivo | Para qué |
| --- | --- |
| [docs/01-analisis-reunion.md](docs/01-analisis-reunion.md) | Qué se acordó en la capacitación y el correo |
| [docs/02-flujo-actual-vs-esperado.md](docs/02-flujo-actual-vs-esperado.md) | Cómo funciona hoy vs. la experiencia objetivo |
| [docs/03-estructura-miportalu.md](docs/03-estructura-miportalu.md) | Cómo trabajar en el portal (módulos, Git, PHP, BD) |
| [docs/04-mapeo-datos.md](docs/04-mapeo-datos.md) | Campos que hay que encontrar en Banner/Reservitas |
| [docs/05-alternativa-tecnica.md](docs/05-alternativa-tecnica.md) | Opción A (reutilizar) vs. B (reconstruir) |
| [docs/06-preguntas-equipo.md](docs/06-preguntas-equipo.md) | Preguntas para Carlos, Manuel y Julián |
| [docs/07-checklist-exploracion.md](docs/07-checklist-exploracion.md) | Orden de trabajo día a día |
| [docs/08-entregable-lunes.md](docs/08-entregable-lunes.md) | Plantilla para la revisión del lunes |
| [mockup/disponibilidad-espacios.html](mockup/disponibilidad-espacios.html) | Mockup interactivo de la experiencia |

Abrir el mockup en el navegador: no requiere servidor.

## Principio de diseño

Si mañana se crea un espacio nuevo en Banner y cumple las reglas actuales, la vista de MiPortalU debe mostrarlo **sin** mantener un catálogo propio.

## Resultado esperado del lunes

Salir de la revisión con:

1. Fuente de datos identificada (tabla, vista, procedimiento o query).
2. Alternativa técnica definida (A o B).
3. Primer plan de implementación sobre MiPortalU y estimación preliminar.
