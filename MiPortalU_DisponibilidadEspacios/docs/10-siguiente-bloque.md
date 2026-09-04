# Siguiente bloque de trabajo (después del PHP y las capturas)

## Ya quedó cerrado

1. En MiPortalU hay **dos módulos**: Disponibilidad de Aulas vs Reserva de Equipos.
2. `disponibilidad.php` **solo enlaza**; no consulta BD.
3. Reservitas usa el mismo `day.php` para ambos; se separan por `id_tipo` (`1/2/3` aulas · `12` equipos).
4. Tu alcance = **solo aulas** (lo de los archivos / enlaces de `disponibilidad.php`).
5. **Equipos:** el jefe + Krystel revisan alternativas productivas (KOHA). No entra en este desarrollo.
6. Backup de `day.php` (Manuel): aulas leen **Oracle** `BANINST1.V_RESERVAS_SALON`; equipos leen **MySQL**. No es la versión final de prod, pero sí la arquitectura.

## Qué sigue — en este orden

### Ahora (tú, local)

1. Captura de **Salones** (`id_tipo=1`) y **Auditorios** (`id_tipo=3`).
2. Pídele a Manuel: `config1.inc.php`, `config2.inc.php`, `config3.inc.php` (sin claves).
3. Si aparece el `day.php` productivo, lo cruzamos con el backup (diff mental: misma vista o no).

### Con Carlos Duarte (30 min)

Lleva: captura de aulas + este hallazgo del backup.

Pregunta de cierre:

> En el `day.php` (backup) para `id_tipo` 2 y 3 la ocupación sale de `BANINST1.V_RESERVAS_SALON` filtrada por `EDIF` y `ROOM`. ¿Esa es la vista vigente? ¿Salones (`id_tipo=1`) usan la misma? ¿Podemos leerla en TEST solo lectura desde MiPortalU sin pasar por el MySQL de Reservitas?

### Con Manuel García (sesión 2, datos)

> Este backup carga `config{id_tipo}.inc.php` y parte Oracle (aulas) vs MySQL (equipos) en `id_tipo <= 3`. ¿En producción sigue igual? Pásame `config1`, `config2`, `config3` sin claves. En TEST, confirma que `V_RESERVAS_SALON` es aulas y que `id_tipo=12` no la usa.

### Cuando tengas los config1/2/3

Mándamelos. Con eso cerramos horarios (`resolution`, morning/evening) y nombres de tablas `$tbl_*` para el diseño de la clase en MiPortalU.

## Qué no haces todavía

- No armes UI de equipos.
- No copies la grilla beige de Reservitas tal cual.
- No pidas PHP 8 para Reservitas.
- No implementes el botón `+` de reserva.
- No tomes el backup de Manuel como el PHP final de producción.
