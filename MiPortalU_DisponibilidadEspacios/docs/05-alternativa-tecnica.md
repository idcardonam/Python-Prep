# Alternativa técnica (A vs. B)

Decisión que hay que llevar el lunes, validada con Carlos Duarte. Hasta no ver Reservitas y TEST, esto es un marco — no un veredicto.

## Opción A — Reutilizar la consulta y las reglas actuales

MiPortalU llama la **misma** vista, procedimiento o query que ya usa Reservitas (la vista que Jonathan asocia a Carlos Duarte). El portal solo cambia la presentación.

**Conviene si:**

- La vista ya distingue tipos, campus, edificio, fecha y ocupación.
- El rendimiento es aceptable para una consulta de estudiante (Julián recuerda una vista “pesada”).
- Las reglas de “espacio nuevo aparece solo” ya están en esa capa.
- No hay escrituras ni efectos laterales al consultarla.

**Riesgo:** arrastrar complejidad o costo de la vista al portal; acoplarse a un contrato que Reservitas puede seguir cambiando.

## Opción B — Reconstruir una capa limpia en MiPortalU

Nueva clase/consulta en el portal, equivalente en resultado, leyendo Banner (o un recorte más simple de las mismas tablas). No se porta el frontend de Reservitas.

**Conviene si:**

- La vista actual mezcla reserva de equipos, permisos o campos que el estudiante no debe ver.
- Es demasiado pesada o difícil de filtrar por franja.
- Reservitas calcula disponibilidad en PHP y no en BD.
- Hay reglas muertas o de UI legado que no queremos copiar.

**Riesgo:** divergencia silenciosa con Reservitas; hay que sostener pruebas de equivalencia.

## Recomendación provisional (para discutir, no para cerrar)

Partir de **A si la vista cubre tipo + ubicación + ocupación en lectura**. Si Carlos confirma que la vista es la de reservas “pesada” y no filtra bien por franja, pasar a **B** usando las **mismas tablas fuente**, no un catálogo nuevo.

En ambos casos:

- Banner es la única fuente de espacios.
- MiPortalU no escribe en Banner.
- La UI es nueva (mockup), no un iframe de Reservitas.
- La clase PHP del portal encapsula la consulta; `disponibilidad.php` solo orquesta filtros y render.

## Qué necesita el lunes para elegir

1. Nombre de objeto: vista / paquete / query (owner.objeto).
2. Si Reservitas pega a Banner directo o a un esquema intermedio.
3. Costo aproximado (tiempo de la consulta en TEST con un campus y un día).
4. Si el PHP de Reservitas aplica filtros extra después de la BD.
5. Dependencias que hay que conservar por compatibilidad (parámetros `id_tipo`, etc.).

## Siguiente paso de construcción (cuando esté la decisión)

Independiente de A o B:

1. Clase de consulta en el portal (PHP 5.6, Oracle).
2. Endpoint o postback del módulo: tipo, fecha, campus, edificio, desde, hasta.
3. Vista según mockup (jQuery, CSS del módulo, SweetAlert para errores).
4. Pruebas de equivalencia con Reservitas.
5. Paso a PPRD con Julián coordinando el push.
