# Análisis de la reunión y del correo de arranque

Fuentes: capacitación MiPortalU (2 sep 2026, ~62 min) y correo de asignación a Iván Cardona.

## Qué se decidió para Iván

No es un proyecto de “reservas”. Es una **migración de consulta**.

Jonathan lo formuló así en la reunión: migrar a MiPortalU **solo** la consulta de disponibilidad de salones, aulas de informática y auditorios. Nueva interfaz en el portal. Misma información que Reservitas. Sin reservar equipos ni crear reservas.

El correo posterior lo confirma y fija el orden de trabajo:

1. Revisar mockup, guía y documentación técnica (este paquete).
2. Empezar por `modulos/disponibilidadAulas/disponibilidad.php`.
3. Cuando esté la carpeta de Reservitas, ver cómo se consultan espacios y ocupación en Banner.
4. Validar con Carlos Duarte si se reutiliza la consulta o se reconstruye.
5. Pedir a Manuel García accesos de TEST en SQL Developer.
6. Usar a Julián Ojeda solo para dudas puntuales de estructura del portal.
7. El lunes revisar hallazgos, alternativa recomendada y siguiente paso.

## Por qué se hace ahora

Reservitas vive en un servidor obsoleto, con problemas de seguridad y PHP muy antiguo. El equipo lleva 3–4 años postergando la migración. Este año la meta es empezar esos cambios. La consulta de espacios es el primer recorte viable: no toca el flujo de reserva, solo la lectura.

La reserva de **equipos** es otro frente (Jonathan está explorando Percoa). No forma parte de este trabajo.

## Qué hay hoy en MiPortalU

Ruta en producción:

`https://miportalu.unab.edu.co/modulos/disponibilidadAulas/disponibilidad.php`

El portal **no** pinta la agenda. Agrupa accesos por tipo y redirige a Reservitas:

| Tipo en el portal | Sedes que se ven en el HTML actual | Parámetro observado |
| --- | --- | --- |
| Aulas de informática | UNAB / Instituto Caldas | `id_tipo=2` |
| Salones | Campus Central / CSU / Campus El Bosque / La Casona | `id_tipo=1` |
| Auditorios | Campus Central | `id_tipo=3` |

Esos `id_tipo` salen del HTML actual. Hay que validarlos en código antes de tratarlos como regla.

En la reunión, Jonathan mostró el menú: Servicios electrónicos → Reserva de equipos (otro tema) y Reserva de espacios → Disponibilidad de aulas. Julián confirmó que esa opción **solo enlaza** a Reservitas.

## Experiencia que hay que construir

1. Entrar a MiPortalU → Disponibilidad de espacios.
2. Elegir Aulas de informática, Salones o Auditorios.
3. Filtrar fecha, campus, edificio/área y franja (desde / hasta).
4. Ver primero los espacios **disponibles**.
5. Poder abrir el horario del día (bloques disponible / ocupado).
6. Sin botones de reserva y sin datos personales del responsable.

Consulta informativa. La disponibilidad refleja la programación de Banner. Las reservas siguen en Banner.

## Hipótesis técnica que hay que validar con Carlos

Jonathan cree que ya existe una **vista** (asociada a Carlos Duarte) usada hace poco en el proyecto de reservas. Julián no la conoce de memoria y recuerda una vista pesada que se intentó usar en otro proceso. Hasta no ver el código de Reservitas y la vista en TEST, no se cierra si:

- Reservitas consulta Banner directo, o
- pasa por esa vista / procedimiento / esquema intermedio.

Esa es la decisión A vs. B del lunes.

## Lo que no es este proyecto

Durante la misma reunión se asignó a **Marlon** el frente de Bienestar (eventos, horas, registro de estudiantes; hoy en Google Forms + cargue MDU a Banner). Eso no es trabajo de Iván.

Iván tenía además un tablero/cruce de datos de “la ingi”, con cierre previsto ese mismo día. El proyecto de disponibilidad arranca **después** de esa actividad y de que Jonathan gestione la carpeta de Reservitas.

## Dependencias que bloquean el cierre técnico

| Dependencia | Quién | Estado al asignar |
| --- | --- | --- |
| Carpeta / código de Reservitas | Jonathan con el equipo dueño | Solicitada, no disponible aún |
| Acceso SQL Developer a TEST (solo lectura) | Manuel García | Pendiente de micro sesión |
| Validación de la vista/consulta | Carlos Duarte | Pendiente de micro sesión |
| Ambiente local de MiPortalU | Julián + equipo de Iván | En configuración en la capacitación |
| Usuarios Delta / SARA | Jonathan | Demora típica 3–4 días |

Sin Reservitas o sin acceso a TEST, el lunes se puede llevar el flujo del portal, el mockup y las preguntas; no se puede afirmar aún la fuente exacta ni comparar resultados.

## Lectura para Iván

El trabajo de esta semana no es “armar ya la pantalla”. Es **cerrar la fuente y la alternativa**. Si llega al lunes con `disponibilidad.php` documentado, el mapa de parámetros a Reservitas, y una recomendación A/B fundada (aunque la carpeta aún no haya llegado, con bloqueos explícitos), cumple el encargo.
