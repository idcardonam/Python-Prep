# Disponibilidad de espacios en MiPortalU

**Universidad Autónoma de Bucaramanga (UNAB) · TIC**  
**Responsable de exploración e implementación:** Iván Cardona  
**Revisión de hallazgos:** lunes (próxima sesión con el equipo)

Empieza por [docs/00-plan-ivan-paso-a-paso.md](docs/00-plan-ivan-paso-a-paso.md): qué hacer, qué enviar, qué pedirle a Carlos y a Manuel.

## Qué vamos a hacer

Traer a **MiPortalU** la consulta **informativa** de aulas, salones y auditorios. Banner es la fuente (programación académica). Las reservas de aula **no** se hacen en Reservitas ni en el portal: se hacen en Banner.

Reservitas es un PHP viejo que mezcla **varias cosas** (aulas + préstamo de implementos + otros). No se actualiza Reservitas a PHP nuevo. No se copia el sancocho. Se hace mapa, se recorta solo aulas, y se construye de cero en el portal.

Hoy MiPortalU solo redirige a Reservitas.

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

- Crear, editar o cancelar reservas de aula (eso es Banner).
- Actualizar Reservitas a PHP nuevo o reescribir el sancocho completo.
- **Reserva / préstamo de equipos** (cámaras, kits, Zoom salas, `id_tipo=12`). El jefe indicó revisar alternativas ya productivas (p. ej. **KOHA**) con Krystel; **no** se implementa en este módulo.
- Reservas de Bienestar / elementos deportivos (Marlon / Alexis).
- Catálogo paralelo de espacios en MiPortalU.

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
| [docs/00-plan-ivan-paso-a-paso.md](docs/00-plan-ivan-paso-a-paso.md) | Plan de Iván: pasos, envíos, Carlos y Manuel |
| [docs/01-analisis-reunion.md](docs/01-analisis-reunion.md) | Qué se acordó en la capacitación y el correo |
| [docs/02-flujo-actual-vs-esperado.md](docs/02-flujo-actual-vs-esperado.md) | Cómo funciona hoy vs. la experiencia objetivo |
| [docs/03-estructura-miportalu.md](docs/03-estructura-miportalu.md) | Cómo trabajar en el portal (módulos, Git, PHP, BD) |
| [docs/04-mapeo-datos.md](docs/04-mapeo-datos.md) | Campos que hay que encontrar en Banner/Reservitas |
| [docs/05-alternativa-tecnica.md](docs/05-alternativa-tecnica.md) | Opción A (reutilizar) vs. B (reconstruir) |
| [docs/06-preguntas-equipo.md](docs/06-preguntas-equipo.md) | Preguntas para Carlos, Manuel y Julián |
| [docs/07-checklist-exploracion.md](docs/07-checklist-exploracion.md) | Orden de trabajo día a día |
| [docs/08-entregable-lunes.md](docs/08-entregable-lunes.md) | Entregable del lunes (actualizado con PHP real) |
| [docs/09-hallazgo-dos-modulos.md](docs/09-hallazgo-dos-modulos.md) | Aulas vs equipos: parámetros y evidencias |
| [docs/10-siguiente-bloque.md](docs/10-siguiente-bloque.md) | Qué hacer justo ahora |
| [docs/11-analisis-day-php-backup.md](docs/11-analisis-day-php-backup.md) | Análisis del backup de day.php (Manuel) |
| [docs/12-vamos-bien-guia-punto4.md](docs/12-vamos-bien-guia-punto4.md) | Cruce guía punto 4 + correo del jefe |
| [docs/13-configs-y-test-solo-lectura.md](docs/13-configs-y-test-solo-lectura.md) | Configs 1/2/3, alerta seguridad, TEST solo lectura |
| [codigo/disponibilidad.php](codigo/disponibilidad.php) | Copia del PHP actual del portal |
| [evidencia/](evidencia/) | Capturas Reservitas + menú MiPortalU |
| [mockup/disponibilidad-espacios.html](mockup/disponibilidad-espacios.html) | Mockup interactivo de la experiencia |

Abrir el mockup en el navegador: no requiere servidor.

## Principio de diseño

Si mañana se crea un espacio nuevo en Banner y cumple las reglas actuales, la vista de MiPortalU debe mostrarlo **sin** mantener un catálogo propio.

## Resultado esperado del lunes

Salir de la revisión con:

1. Fuente de datos identificada (tabla, vista, procedimiento o query).
2. Alternativa técnica definida (A o B).
3. Primer plan de implementación sobre MiPortalU y estimación preliminar.
