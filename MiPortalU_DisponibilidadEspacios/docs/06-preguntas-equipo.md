# Preguntas para el equipo

Llegar a cada micro sesión con el archivo ya abierto. Máximo ~30 minutos. No pedir un tour general.

## Carlos Duarte (consulta / lógica)

Antes: haber leído `disponibilidad.php` y, si ya llegó, el PHP de consulta de Reservitas.

1. ¿Dónde está exactamente la consulta que trae espacios y ocupación? ¿Archivo, vista, procedimiento?
2. ¿Reservitas consulta Banner directo u otro esquema/vista/procedimiento?
3. ¿La vista que se usó en el proyecto reciente de reservas es la misma de disponibilidad de aulas?
4. ¿Qué regla hace que un espacio nuevo parametrizado en Banner aparezca en la consulta?
5. ¿Cómo se diferencian aulas de informática, salones y auditorios en datos (no en el HTML)?
6. ¿Cómo se resuelven sede/campus, edificio/área, fecha y bloques de horario?
7. ¿Qué parte podemos reutilizar sin traernos el frontend legado?
8. ¿Hay dependencias de compatibilidad (`id_tipo`, nombres de sede, rangos horarios)?
9. ¿La vista es pesada para un estudiante que consulta un campus y un día? ¿Hay índices o recorte posible?
10. Decisión: **A reutilizar** o **B reconstruir capa en MiPortalU**, y por qué.

## Manuel García (accesos TEST)

Solo permisos y conexión. No diseño funcional.

1. Conexión SQL Developer al TEST que corresponde a esta consulta (host, puerto, servicio/SID, si se puede compartir por el canal interno).
2. Usuario de **solo lectura** para revisar fuentes.
3. Confirmación de esquemas/vistas/procedimientos que aparezcan en el código.
4. Confirmación explícita: esta iniciativa **no requiere escrituras** en Banner.
5. Si TEST y PPRD difieren para objetos de espacios/ocupación, cuál usar para la equivalencia con Reservitas.

## Julián Ojeda (estructura MiPortalU)

Solo si algo del portal no se entiende con el código.

1. ¿El módulo nuevo se queda en `modulos/disponibilidadAulas/` o se crea otro nombre (`disponibilidadEspacios`)?
2. ¿La clase de consulta va en gestión de contenidos / clases con qué convención de nombre?
3. ¿El menú “Disponibilidad de aulas” se reetiqueta o se crea ítem nuevo?
4. ¿Hay un patrón de módulo reciente (consulta Oracle + jQuery) para copiar includes?
5. ¿En local el módulo debe apuntar a Banner TEST o al esquema del portal?
6. Recordatorio: avisar antes de cualquier push por el cifrado de PHP.

## Jonathan Espinel (gestión, no técnica profunda)

1. ¿Ya hay fecha de entrega de la carpeta de Reservitas?
2. ¿Quién es el contacto dueño de ese servidor si el zip no llega antes del lunes?
3. ¿El funcional que valida equivalencia es el mismo de reservas de espacios?
4. Confirmar que reserva de equipos queda fuera (Percoa) y no se mezcla en el módulo.
