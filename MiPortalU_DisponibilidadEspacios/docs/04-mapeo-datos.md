# Mapeo de datos

Objetivo: cada control del mockup debe nacer de Banner/Reservitas, no de una lista mantenida a mano en MiPortalU.

## Campos a identificar

| Dato funcional | Para qué | Qué hay que encontrar en código o BD | Estado |
| --- | --- | --- | --- |
| Tipo de espacio | Separar informática / salón / auditorio | Campo o regla real. En el portal se observa `id_tipo` 1, 2, 3 | Pendiente de validar en PHP |
| Sede / campus | Filtro de ubicación | ID técnico + etiqueta visible | Pendiente |
| Edificio / área | Acotar búsqueda; depende de campus y tipo | Relación campus ↔ edificio ↔ espacio | Pendiente |
| Código del espacio | Identificar el recurso en tarjetas | Código institucional Banner/Reservitas | Pendiente |
| Fecha | Consultar un día | Formato y condición (`DATE`, string, rango) | Pendiente |
| Hora inicio / fin | Franja y bloques | Intervalos o grilla de ocupación | Pendiente |
| Ocupación | Disponible vs. ocupado | Query/regla de reserva o programación | Pendiente |
| Detalle de ocupación | Agenda del día | Bloques por hora **sin** responsable | Pendiente |

## Relación mockup → origen (a completar)

| UI (mockup) | Origen esperado | Campo real (llenar) | Notas |
| --- | --- | --- | --- |
| Botón Aulas de informática | Tipo | | ¿`id_tipo=2`? |
| Botón Salones | Tipo | | ¿`id_tipo=1`? |
| Botón Auditorios | Tipo | | ¿`id_tipo=3`? |
| Fecha | Parámetro de consulta | | Default: hoy |
| Campus | Dimensión de ubicación | | El Jardín, El Bosque, CSU, Caldas, La Casona son nombres de mockup |
| Edificio / área | Dimensión de ubicación | | Debe filtrar según tipo + campus |
| Desde / Hasta | Franja | | Definir si es hora exacta o bloque institucional |
| Estado DISPONIBLE | Sin cruce de ocupación en la franja | | |
| Estado OCUPACIÓN PARCIAL | Hay cruce en parte de la franja | | El mockup distingue parcial vs. libre; Reservitas puede ser binario |
| Mini timeline 06:00–18:00 | Agenda del día | | Si la fuente no trae bloques, hay que derivarlos |
| Matriz horario del día | Mismos bloques | | |

## Preguntas de mapeo (llevar a Carlos)

1. ¿Un espacio nuevo en Banner aparece solo por tipo/categoría, por atributo de edificio, o por una tabla de parametrización?
2. ¿La ocupación es SSRMEET / programación académica, reservas ad-hoc, o ambas?
3. ¿El “disponible” de Reservitas es “libre todo el día” o “libre en la franja pedida”?
4. ¿Campus y edificio son códigos Banner (`STVCAMP`, edificios SLB) o catálogo propio de Reservitas?
5. ¿La vista pesada de reservas ya entrega tipo + campus + edificio + franjas, o solo ocupación cruda?

## Comparación mínima contra Reservitas

Cuando exista acceso, llenar esta tabla con la misma fecha y tipo:

| # | Fecha | Tipo | Campus | Espacio (código) | Reservitas | Propuesta | ¿Coincide? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | Informática | | | | | |
| 2 | | Salones | | | | | |
| 3 | | Auditorios | | | | | |

Tres escenarios no son suficientes para certificar producción, pero sí para la revisión del lunes.
