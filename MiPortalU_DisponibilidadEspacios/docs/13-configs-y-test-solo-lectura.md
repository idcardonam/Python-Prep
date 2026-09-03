# Configs 1/2/3 + respuesta Carlos + qué es TEST solo lectura

Fecha: 3 sep 2026.

## ALERTA DE SEGURIDAD (urgente)

Los archivos `config1.inc.php` y `config2.inc.php` que pegaste **no empiezan limpios**. Antes del comentario `# $Id: config.inc.php...` hay un bloque PHP ofuscado (`$wfbipzfo`, `kzjtwco`, `error_reporting(0)`, decodificación y ejecución dinámica).

Eso **no es configuración MRBS**. Es patrón típico de **webshell / backdoor**.

Qué hacer ya:

1. **No ejecutes** esos archivos en local ni los subas a Git.
2. Avisa ya a **Manuel García** y a quien lleve seguridad / el servidor de Reservitas: “config1 y config2 del backup traen PHP ofuscado al inicio”.
3. Pide una copia **limpia** (o confirma si en producción también está infectado; encaja con lo que Jonathan dijo del servidor obsoleto y problemas de seguridad).
4. `config3.inc.php` en tu pegado **sí** arranca limpio (`ini_set('default_charset'...)`). Aun así, no copies claves.
5. Había un `db_password` comentado en config3: **no lo reenvíes** por chat; pide que lo roten si ese backup circuló.

Este repo **no** guarda esos PHP infectados. Solo el resumen funcional abajo.

---

## Respuesta de Carlos (la anotaste)

> ¿`V_RESERVAS_SALON` es la vigente? ¿También salones (`id_tipo=1`)?  
> **Sí — son salones** (también aplica a salones).

Queda: ocupación de **salones + informática + auditorios** = misma fuente Banner `BANINST1.V_RESERVAS_SALON` (a confirmar matices de filtro, pero ya no es “solo tipo 2/3”).

---

## Qué es “TEST solo lectura”

Significa:

1. Conectar con **SQL Developer** al ambiente **TEST** de Banner (no producción).
2. Con un usuario que **solo pueda consultar** (`SELECT`).  
   No puede insertar, actualizar ni borrar.
3. Para que tú (o Manuel) abras `BANINST1.V_RESERVAS_SALON`, veas columnas y pruebes un día/campus **sin riesgo** de dañar Banner.

No es una app. Es el permiso de base de datos para explorar. Manuel te ayuda a conseguir ese usuario/conexión. **No me pases usuario ni clave**; solo confirma “ya entré a TEST y vi la vista”.

---

## Lo útil de config1 / config2 / config3 (sin secretos)

Base común (los tres):

| Parámetro | Valor |
| --- | --- |
| Día | 06:00 → 22:00 |
| Vista default | `day` |
| Idioma | `es` |
| Auth | LDAP (Reservitas; MiPortalU usa la del portal) |
| Tablas MySQL | `area`, `entry`, `room`, `users`, `programa`, `repeat` |
| Tipos de ocupación (colores) | A Pregrado, B Posgrado, C Ed. No Formal, E Externa, F Administrativa, G Docente, J Otra |

Diferencias que importan para **tu** UI:

| Archivo | Tipo | `$resolution` | Bloque de grilla | Admins (solo contexto, no UI estudiante) |
| --- | --- | --- | --- | --- |
| `config1.inc.php` | Salones | **3600** (1 hora) | 06–22 cada 1 h | Comentario “Administrador AULAS BANNER” |
| `config2.inc.php` | Informática | **1800** (30 min) | 06–22 cada 30 min | Admins informática / sedes |
| `config3.inc.php` | Auditorios | **3600** (1 hora) | 06–22 cada 1 h | Admin auditorios; charset UTF-8 explícito |

Eso cuadra con la captura de informática (bloques de 30 min). Para salones/auditorios el mockup puede usar **1 hora** o unificar a 30 min en MiPortalU (decisión de UX; la fuente Banner trae `HI`/`HF` reales).

Credenciales DB / LDAP host: **no documentar ni versionar**. Pídelas por el canal interno de Manuel si hacen falta en TEST.

---

## Cómo queda el rumbo (aún más firme)

1. Solo aulas: `id_tipo` 1, 2, 3.  
2. Ocupación: `BANINST1.V_RESERVAS_SALON` (Carlos: también salones).  
3. Catálogo rooms/areas: hoy en MySQL de Reservitas; en MiPortalU hay que decidir si se lee Banner puro o un recorte del catálogo (Carlos/Manuel).  
4. Grilla: 06–22; resolución 30 min (tipo 2) o 60 min (tipos 1 y 3).  
5. Sin reserva, sin equipos, sin copiar el PHP infectado/legado.

## Para el lunes puedes decir

- Guía punto 4: avance OK.  
- Fuente candidata confirmada con Carlos: `V_RESERVAS_SALON` también para salones.  
- Configs: horarios y resolución por tipo.  
- Riesgo: backup de configs 1 y 2 con posible webshell → reportado / por limpiar.  
- Siguiente: acceso TEST solo lectura + `day.php` oficial limpio + armar clase en MiPortalU.
