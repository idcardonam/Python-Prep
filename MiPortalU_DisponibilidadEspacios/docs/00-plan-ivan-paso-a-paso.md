# Plan de Iván — qué hacer ahora (paso a paso)

Conversación con Manuel García + encargo original. Esto es lo que haces, en este orden. Nada más.

## Recomendación en una frase

**No arregles Reservitas. No lo pases a PHP nuevo. No copies el sancocho.**  
Saca un mapa de qué hay ahí, **separa las tres cosas**, y de cero en MiPortalU montas **solo** la consulta informativa de aulas (programación académica de Banner).

## Qué es Reservitas (lo que Manuel te aclaró)

No es un solo sistema. Hay **varias configuraciones**. Prestaba (al menos) tres cosas distintas:

| # | Qué es | Qué hace | Dónde se “reserva” de verdad | ¿Es tu proyecto ahora? |
| --- | --- | --- | --- | --- |
| 1 | Aulas / salones / auditorios | **Solo muestra** si el espacio está ocupado por programación académica | En **Banner**, no en Reservitas | **SÍ** |
| 2 | Préstamo de implementos (cámaras, equipos de facultades) | Presta elementos; cada tipo tiene su configuración | En Reservitas hoy; jefatura + Krystel evalúan **KOHA** u otra app productiva | **NO** |
| 3 | Otros préstamos (Bienestar: elementos deportivos, y lo que esté hablando Alexis) | Reservas de elementos, no de aulas | Otro frente | **NO** |

Tu módulo en MiPortalU es **solo la fila 1**. Informativo. El estudiante mira disponibilidad. No reserva.

Por eso no tiene sentido “actualizar Reservitas a la última PHP”: te estarías casando con un PHP viejo que mezcla tres productos. Lo correcto es **ingeniería inversa → requerimientos de aulas → construir de cero en MiPortalU**.

Comparar lo viejo con lo actual **no** es para copiar pantallas. Es para no inventar reglas y para demostrarle al equipo: “esto está conectado a Banner, hace X, y de aquí solo migraremos Y”.

---

## Qué me tienes que enviar (no accesos)

Tienes todo en local. Envíame archivos. **Borra o tacha contraseñas** (usuario/clave de Oracle, tokens, `password=`). Con el código me basta.

### Envío 1 — MiPortalU (hoy, aunque Reservitas aún no esté)

Carpeta completa:

`modulos/disponibilidadAulas/`

Todo lo que haya: `.php`, `.js`, `.css`, includes. Si el PHP llama otra clase, mándala también.

### Envío 2 — Foto del menú de Reservitas (hoy)

Capturas (o fotos del celular, da igual):

1. Menú principal de Reservitas.
2. Pantalla de disponibilidad de aulas (filtros + resultado).
3. Cualquier menú de **préstamo de equipos / cámaras / implementos**.
4. Cualquier menú de **Bienestar / deportes**, si aparece.

Así separo las tres cosas sin adivinar.

### Envío 3 — Reservitas (en cuanto la tengas)

1. Lista de carpetas de la raíz (nombres). En Windows, en la carpeta del proyecto:

```bat
tree /F /A | more
```

Si es enorme, basta el primer nivel + la carpeta de PHP de aulas.

2. Archivos de **configuración** (`config.php`, `conexion.php`, `.ini`, `.env`) **sin claves**.
3. El PHP que arma la **consulta de aulas** (en la reunión se habló de algo tipo `day.php`; manda el que sea).
4. El PHP o tabla/config que define **`id_tipo`** (1 salones, 2 informática, 3 auditorios).
5. Si ves carpetas tipo `prestamo`, `equipos`, `implementos`, `bienestar`: manda solo los nombres. No las migres.

No me mandes el zip entero si pesa mucho. Primero árbol + configs tapadas + PHP de aulas.

---

## Qué haces tú, en este orden

### Paso 1 — No toques código de Reservitas

Cero cambios. Cero “mejoras”. Cero PHP 8.  
Si lo tocas, se pierde la comparación con lo que ya está.

### Paso 2 — Abre el módulo del portal (30–45 min)

Ruta:

`modulos/disponibilidadAulas/disponibilidad.php`

Anota en un bloc (o en `docs/08-entregable-lunes.md`):

1. ¿Es solo una página de enlaces o ya consulta base de datos?
2. Los tres tipos y a qué URL de Reservitas mandan.
3. El query string completo (`id_tipo=`, sede, etc.).
4. Nombres de archivos JS/CSS que carga.

Eso es el Envío 1. Me lo pasas y lo mapeo.

### Paso 3 — Armar el mapa (esto es el entregable, no la pantalla bonita)

Cuando tengas Reservitas, para **cada menú** anota una línea:

```text
Menú: ________
¿Aulas, implementos o Bienestar?
Archivo PHP: ________
¿Lee Banner? ¿Qué vista/tabla? (si se ve en el código)
¿Escribe algo? sí/no
¿Quién lo usa? (estudiante / facultad / bienestar)
```

Al final deben quedar **tres cajas**, no una.

### Paso 4 — De las tres cajas, trabaja solo “Aulas”

De esa caja saca:

- Fuente Banner (vista, tabla o procedimiento).
- Filtros: tipo, campus, edificio, fecha, hora.
- Qué significa “disponible” (libre en la franja vs. libre todo el día).
- Confirmación: **no inserta reserva**.

Eso son los requerimientos de **tu** proyecto.

### Paso 5 — Sesión con Carlos Duarte (30 min)

**Para qué es Carlos:** la consulta de **programación académica de aulas en Banner**. No para préstamos de cámaras.

Llega con `disponibilidad.php` abierto y, si ya está, el PHP de aulas de Reservitas.

Dile esto, textual:

> “No voy a migrar Reservitas completo. Solo la consulta informativa de aulas. Necesito que me confirmes dónde está la ocupación de programación académica y si la vista que ya existe sirve para MiPortalU sin copiar el PHP viejo.”

Preguntas, en este orden (si se acaba el tiempo, las 1–6 bastan):

1. ¿Qué objeto de Banner trae espacios + ocupación de **aulas**? Nombre: owner.vista o owner.paquete.
2. ¿Esa es la misma vista “pesada” del proyecto de reservas, o es otra?
3. ¿Reservitas le pega directo a Banner o hay un esquema en el medio?
4. ¿`id_tipo` 1, 2, 3 cómo se traduce en Banner? (salón / informática / auditorio)
5. Si mañana crean un aula nueva en Banner, ¿qué tiene que tener para aparecer?
6. ¿La consulta es solo lectura? ¿Hay algún insert/update de aula en Reservitas?
7. ¿Mejor: MiPortalU llama **esa misma vista**, o armo una consulta nueva sobre las mismas tablas?
8. ¿Cuánto se demora en TEST un día + un campus? Si es lenta, ¿hay forma de filtrar antes?

**Qué debes salir diciendo (una frase):**  
“La fuente de aulas es ______ y en MiPortalU vamos a ______ (reutilizar vista / recortar consulta).”

No le pidas que te explique préstamos de equipos. Eso no es de él en esta sesión.

### Paso 6 — Qué más hacer con Manuel García

Ya hablaste con él: te dijo el enfoque correcto (mapa + de cero + solo aulas). Ahora la sesión siguiente es **corta y de datos**, no de filosofía.

Dile esto:

> “Ya quedó: no actualizo Reservitas; hago mapa y construyo en MiPortalU solo la consulta de aulas. Para no mezclar con préstamos, necesito que me ayudes a identificar en TEST qué objetos son de aulas y cuáles son de implementos.”

Pídele solo esto:

1. En SQL Developer TEST: usuario de **solo lectura** (eso lo gestionan ustedes; a mí no me lo pases).
2. Que te confirme, cuando tengas nombres del código: “esta vista/tabla es aulas; esta otra es préstamos”.
3. Confirmación por escrito (chat): **aulas = programación Banner, sin escritura**.
4. Si un objeto mezcla aulas + equipos, que te lo marque: **no lo uses tal cual**.
5. Quién es dueño funcional de préstamos de facultades vs. Bienestar vs. Alexis — para no meterte.

No le pidas que te diseñe la UI. No le pidas PHP 8 para Reservitas.  
Si te insiste en “organizar el sancocho”, la respuesta es: **el mapa de las tres cajas es esa organización**; el código nuevo es solo la caja de aulas en MiPortalU.

### Paso 7 — Lunes (qué llevar)

No lleves una pantalla terminada. Lleva:

1. Mapa: tres productos dentro de Reservitas (aunque 2 y 3 estén solo nombrados).
2. Flujo de aulas: MiPortalU enlaza → Reservitas muestra → Banner programa.
3. Fuente de aulas (si Carlos ya contestó) o “bloqueado por X”.
4. Requerimientos **solo** de consulta de aulas (lista corta).
5. Frase: se construye de cero en MiPortalU; no se actualiza el PHP de Reservitas; no se migran préstamos.

---

## Qué no haces

- No subas Reservitas a PHP 8.
- No armes préstamo de cámaras, facultades ni Bienestar.
- No crees reservas de aula (eso es Banner).
- No copies el frontend viejo.
- No inventes un catálogo de aulas en el portal.
- No mezcles el proyecto de Marlon (Bienestar) ni lo de Alexis.

## Si solo puedes hacer una cosa hoy

Mándame el Envío 1 (`disponibilidadAulas/`) y 2–4 capturas de Reservitas. Con eso empiezo el mapa. El resto llega cuando tengas la carpeta.
