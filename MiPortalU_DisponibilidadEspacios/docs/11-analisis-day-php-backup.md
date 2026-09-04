# Análisis del backup de `day.php` (Manuel García)

**Estado:** referencia de trabajo. **No** es el `day.php` productivo final. Manuel lo ha modificado. Servirá para mapear arquitectura; la equivalencia final se valida contra la versión real o la URL viva.

## Hallazgo principal (una frase)

Para **aulas** (`id_tipo` 1–3) la ocupación viene de **Oracle Banner** (`BANINST1.V_RESERVAS_SALON`). Para **equipos y otros** (`id_tipo` > 3, p. ej. 12) la ocupación viene de **MySQL local** (tablas MRBS de Reservitas). Por eso no se mezclan en MiPortalU.

## Cómo arranca el archivo

1. Exige `id_tipo` numérico.
2. Carga **una config por tipo**: `config{N}.inc.php`  
   Ejemplo: `config2.inc.php` = aulas de informática, `config12.inc.php` = equipos.  
   Esto es lo que Manuel decía: “por cada cosa que prestaban hay una configuración”.
3. Conecta **dos bases**:
   - MySQL → `conec.php` → `Conectarse()`
   - Oracle → `conecora.php` → `Conec_ora()`
4. Lee metadatos en MySQL:
   - `mrbs_tipo` → `area_tipo`, `dias`, `reservar` (si el tipo permite reservar)
   - `mrbs_sede` → nombre de sede

## Bifurcación aulas vs resto

| Condición | Fuente de ocupación | Fuente de columnas (espacios) |
| --- | --- | --- |
| `$id_tipo <= 3` (aulas / salones / auditorios) | **Oracle** `BANINST1.V_RESERVAS_SALON` (+ `V_UNAB_CSARA2`) | Oracle + lista de rooms desde MySQL `$tbl_room` por `area` |
| `$id_tipo > 3` (equipos, CPA, etc.) | **MySQL** `$tbl_entry` + `$tbl_room` | MySQL `$tbl_room` |

En la UI: si `$id_tipo < 11` muestra “Campus/Áreas”; si no, “Equipos”.

## Consulta Oracle de aulas (el corazón de tu módulo)

Para `$id_tipo == 2` o `3` (en este backup; salones `1` entra al bloque `<=3` pero la query grande de ocupación está escrita para 2 y 3 — **validar en la versión real / con Carlos**):

Objeto principal:

```text
BANINST1.V_RESERVAS_SALON
BANINST1.V_UNAB_CSARA2          (outer join por período/NRC)
BANINST1.F_UNAB_DOCENTE_PIDM_PARM(...)
BANINST1.F_UNAB_NAME_PIDM_PARM(..., 'APNOM')   → DOCENTE
BANINST1.F_UNAB_SSBSECT_PARM(..., 'DEPT_NAME') → DEPT_NAME
```

Campos útiles:

| Campo | Uso |
| --- | --- |
| `ROOM` | Código del espacio (columna) |
| `EDIF` / `EDIF_NAME` | Edificio |
| `FI` / `FF` | Vigencia de la programación |
| `HI` / `HF` | Hora inicio / fin (HHMM) |
| `DS` | Días de la semana (código Banner U/M/T/W/R/F/S) |
| `TERM` / `NRC` / `TITULO` / `EVENTO` | Qué ocupa (materia o evento) |
| `DOCENTE` / `DEPT_NAME` | Responsable — **no mostrar al estudiante en MiPortalU** |

Filtros: fecha del día entre `FI`–`FF`, día de semana en `DS`, `EDIF IN (...)`, `ROOM IN (...)`.

Encabezado de columnas (también Oracle):

```text
SELECT EDIF, EDIF_NAME, ROOM ROOM_NAME
FROM BANINST1.V_RESERVAS_SALON
WHERE ROOM IN (...) AND EDIF IN (...)
GROUP BY EDIF, EDIF_NAME, ROOM
ORDER BY ROOM
```

## Cómo arma edificios / salones (MySQL + hardcodes)

Para informática (`id_tipo == 2`), el `area` del portal decide el set de edificios:

| `area` | Campus (comentario en código) | `edificios2` |
| --- | --- | --- |
| 201 | Jardín | `ED-APP`, `ED-BLN`, `ED-ING`, `ED-BIB`, `ED-BLA`, `ED-CSU`, `ED-BLD` |
| 202 | CSU | `ED-CSU` |
| 203 | Bosque | `ED-SET`, `ED-PET` |
| 812 | Casona | `ED-BLC` |
| 204 / 205 | Caldas | `ED-PRI`, `ED-SEC` (resolución 30 min) |

Los **rooms** de esa área salen de MySQL:

```text
SELECT room_name FROM $tbl_room WHERE area_id = {area}
```

Auditorios (`id_tipo == 3`): fuerza `area = 211`, edificios `ED-APP`, `ED-ING`, `ED-BLN`, `ED-BLC`.

Salones (`id_tipo == 1`): en el portal el enlace **no** manda `area`; aquí hay lógica incompleta/mezclada en el backup. **Prioridad con Carlos / versión real.**

## Qué NO llevar a MiPortalU (aunque esté en este PHP)

- Todo el bloque del `+` / `edit_entry.php` / `edit_entry_email.php` (crear reserva).
- Reglas de viernes, 6pm CSU, Bosque sábado, exclusiones de nivel LDAP, etc. (son del **préstamo**, no de la consulta informativa).
- `id_tipo` 6, 7, 11, 12 (Gesell, iPad, CPA, Multimedios/equipos).
- Mostrar docente / departamento en el tooltip al estudiante.
- Debug del backup: `print_r($salones2)`, echos, fecha hardcode comentada, mezcla `mysql_*` / `mysqli` / `$mysqli` sin definir claro.

## Qué SÍ reutilizar como idea (no copiar el archivo)

1. Misma fuente: `BANINST1.V_RESERVAS_SALON` (+ joins/funciones necesarias).
2. Filtros: fecha, día semana, edificio, room, tipo vía catálogo MySQL de areas/rooms **o** equivalente limpio.
3. Resultado: lista de espacios + bloques HI–HF + título (materia/evento).
4. UI nueva en MiPortalU: disponible / ocupado, sin `+`.

## Archivos que faltan pedir (backup / carpeta)

Sin estos no se cierra el mapa local:

| Archivo | Para qué |
| --- | --- |
| `config1.inc.php` `config2.inc.php` `config3.inc.php` | Horarios, resolution, nombres de tablas `$tbl_*` |
| `conecora.php` / `conec.php` | Solo estructura (sin claves) — confirmar SID TEST |
| Función `get_default_area($id_sede, $id_tipo)` | Cómo nace el `area` cuando el portal no la manda (salones) |
| Definición / comentario de `BANINST1.V_RESERVAS_SALON` | Carlos / Manuel en SQL Developer |

## Pregunta lista para Carlos (con este backup)

> En el `day.php` (backup) para `id_tipo` 2 y 3 la ocupación sale de `BANINST1.V_RESERVAS_SALON` filtrada por `EDIF` y `ROOM`. ¿Esa es la vista vigente? ¿Salones (`id_tipo=1`) usan la misma? ¿Podemos leerla en TEST solo lectura desde MiPortalU sin pasar por MySQL de Reservitas?

## Pregunta lista para Manuel

> Este backup carga `config{id_tipo}.inc.php` y parte Oracle vs MySQL en `id_tipo <= 3`. ¿En producción sigue igual? ¿Me pasas `config1`, `config2`, `config3` (sin claves) y confirmas si salones también pegan a `V_RESERVAS_SALON`?

## Implicación para el lunes

Ya no es “¿Banner o no?”. Para aulas es **sí, Banner vía `V_RESERVAS_SALON`**.  
La decisión A/B queda así:

- **Reutilizar la vista** `V_RESERVAS_SALON` (y lo mínimo de catálogo room/area).
- **No reutilizar** el PHP de Reservitas ni la rama MySQL de equipos.
- Construir la capa y UI **de cero** en MiPortalU, solo `id_tipo` 1–3.
