# Entregable para la revisión del lunes

Actualizado con el PHP real de `disponibilidad.php` y capturas del 3 sep 2026.

## 1. Flujo actual

**Qué hace MiPortalU**

`modulos/disponibilidadAulas/disponibilidad.php` es **solo tabs + enlaces** a Reservitas. Includes: header, lateral, footer. **No hay SQL.**

**Qué hace Reservitas**

`https://aulas.unab.edu.co/reservitas/day.php` pinta la grilla del día (06:00–22:00, bloques 30 min). Misma pantalla sirve para aulas y para equipos; se separa por `id_tipo` / `area` / `id_sede`.

**Enlaces reales del portal**

| Tipo | Sede | URL |
| --- | --- | --- |
| Informática `id_tipo=2` | Unab `id_sede=1` `area=201` | `day.php?area=201&id_sede=1&id_tipo=2` |
| Informática `id_tipo=2` | Caldas `id_sede=4` `area=204` | `day.php?area=204&id_sede=4&id_tipo=2` |
| Salones `id_tipo=1` | Central `id_sede=1` | `day.php?id_sede=1&id_tipo=1` |
| Salones `id_tipo=1` | CSU `id_sede=2` | `day.php?id_sede=2&id_tipo=1` |
| Salones `id_tipo=1` | Bosque `id_sede=3` | `day.php?id_sede=3&id_tipo=1` |
| Salones `id_tipo=1` | La Casona `id_sede=5` | `day.php?id_sede=5&id_tipo=1` |
| Auditorios `id_tipo=3` | Central `id_sede=1` | `day.php?id_sede=1&id_tipo=3` |

**Fuera de este módulo:** Reserva de Equipos en el menú → Reservitas con `id_tipo=12` (ejemplo captura `area=413`).

**¿Hay query en el PHP del portal?** No.

## 2. Fuente

| Ítem | Valor |
| --- | --- |
| Sistema que ejecuta la consulta hoy | Reservitas `day.php` |
| ¿Banner directo? | PENDIENTE — abrir `day.php` en la carpeta |
| Owner.objeto | PENDIENTE — sesión Carlos Duarte |
| Archivo PHP de Reservitas | `day.php` (confirmado en URL) |
| Escritura en Banner | No para este módulo (consulta informativa) |
| Qué se ve en celdas de aulas | Nombres de materias / eventos = programación académica |

## 3. Alternativa recomendada

- [x] **B orientado a construir de cero en MiPortalU la UI**, reutilizando la **fuente de datos** de aulas cuando Carlos la confirme (vista/tablas). No copiar el frontend de Reservitas. No migrar equipos.
- [ ] A puro (embeber/reusar PHP de Reservitas) — descartado: es el sancocho y el servidor viejo.
- [ ] Aún no se cierra el objeto SQL porque falta el código de `day.php`.

**Por qué:** el portal hoy no consulta nada. Reservitas mezcla aulas (`id_tipo` 1–3) y equipos (`12`) en el mismo `day.php`. Manuel: mapa + construir solo disponibilidad de aulas. Jonathan: consulta informativa, sin reserva.

## 4. Mapeo

| UI | ¿Existe? | Campo / evidencia | Hueco |
| --- | --- | --- | --- |
| Tipo | Sí | `id_tipo` 1, 2, 3 | Validar en BD/Carlos |
| Campus | Sí | `id_sede` 1–5 | Etiquetas exactas Banner |
| Área / edificio | Parcial | `area` 201, 204 (solo informática en el portal) | Cómo se arma para salones/auditorios |
| Código espacio | Sí | `ED-…-AINF` en grilla | Origen Banner |
| Fecha | Sí | day/month/year en Reservitas | Default hoy |
| Franja | Sí | bloques 30 min 06:00–22:00 | Confirmar si Banner usa el mismo corte |
| Ocupación | Sí | celda con nombre de materia | Query exacta |
| Agenda del día | Sí | grilla completa | Cómo devolverla al portal |
| Crear reserva (`+`) | Existe en Reservitas | No llevar a MiPortalU | — |
| Equipos | Existe | `id_tipo=12` | Fuera de alcance |

## 5. Prueba de equivalencia

| Escenario | Resultado Reservitas | Resultado propuesto | ¿Igual? |
| --- | --- | --- | --- |
| Informática Jardín `area=201` | Captura 3 sep 2026 (materias en AINF) | PENDIENTE | |
| Salones `id_sede=1&id_tipo=1` | PENDIENTE | PENDIENTE | |
| Auditorios `id_tipo=3` | PENDIENTE | PENDIENTE | |

## 6. Bloqueos

| Bloqueo | Impacto | Dueño | Estado |
| --- | --- | --- | --- |
| Carpeta / `day.php` de Reservitas | No se ve el SQL | Jonathan | Solicitada |
| Objeto Banner aulas | No se cierra la clase del portal | Carlos Duarte | Por agendar |
| Separar objetos aulas vs equipos en TEST | Evitar vista mezclada | Manuel García | Sesión 2 |
| Código solo en equipo local UNAB | Este repo documenta, no despliega al portal | Iván | OK |

## 7. Siguiente paso

1. Conseguir `day.php` (+ includes de conexión) y marcar la query de **aulas**.
2. 30 min Carlos: `owner.objeto` de programación de aulas.
3. 30 min Manuel: en TEST, aulas ≠ equipos.
4. Empezar clase + UI en MiPortalU **solo** para `id_tipo` 1, 2, 3.
5. Equipos (`12`) queda en el mapa como “otro módulo / otro proyecto”.
