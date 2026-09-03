# Preguntas para el equipo

Llegar con el archivo abierto. 30 minutos. Sin tour general.

## Carlos Duarte — 30 min (consulta de aulas en Banner)

**Para qué:** ubicar la ocupación de **programación académica de aulas**. No préstamos de equipos.

**Frase de arranque:**

> No voy a migrar Reservitas completo. Solo la consulta informativa de aulas hacia MiPortalU. Necesito el objeto de Banner y si la vista actual sirve sin copiar el PHP viejo.

1. ¿Qué objeto trae espacios + ocupación de aulas? `owner.objeto`
2. ¿Es la misma vista pesada del proyecto de reservas, o es otra?
3. ¿Reservitas pega a Banner directo o hay esquema intermedio?
4. ¿`id_tipo` 1 / 2 / 3 cómo se traduce en Banner?
5. Aula nueva en Banner: ¿qué debe tener para aparecer?
6. ¿La consulta es solo lectura? ¿Hay insert/update de aula en Reservitas?
7. ¿MiPortalU llama esa vista, o armo consulta nueva sobre las mismas tablas?
8. ¿Tiempo en TEST de un día + un campus? ¿Se puede filtrar antes?

**Salida obligatoria (una frase):**  
La fuente de aulas es ______ y en MiPortalU vamos a ______ (reutilizar vista / recortar consulta).

## Manuel García — sesión 2 (datos, no enfoque)

El enfoque ya lo dio: mapa, de cero, no actualizar PHP de Reservitas, aulas aparte de préstamos.

Pídele ahora:

1. SQL Developer TEST, usuario **solo lectura** (no compartir claves por chat abierto).
2. Separar objetos: “esto es aulas” vs “esto es préstamo de implementos”.
3. Chat: aulas = programación Banner, **sin escritura**.
4. Si una vista mezcla aulas + equipos: marcarla para **no usarla tal cual**.
5. Dueño funcional: facultades (implementos) vs. Bienestar vs. Alexis — para no meterse.

No pedir diseño de UI ni upgrade de Reservitas.

## Julián Ojeda — solo si te trancas con el portal

1. ¿El módulo se queda en `disponibilidadAulas` o se renombra?
2. ¿Dónde va la clase PHP de la consulta?
3. ¿Patrón de módulo reciente (Oracle + jQuery) para copiar includes?
4. Local: ¿apunta a Banner TEST?
5. Avisar antes de push (cifrado de PHP).

## Jonathan Espinel — una pregunta

Confirmar en una línea que el alcance de Iván es **solo consulta informativa de aulas** y que préstamos de implementos / Bienestar / Alexis **no** entran en este módulo.
