# Siguiente bloque de trabajo (después del PHP y las capturas)

## Ya quedó cerrado

1. En MiPortalU hay **dos módulos**: Disponibilidad de Aulas vs Reserva de Equipos.
2. `disponibilidad.php` **solo enlaza**; no consulta BD.
3. Reservitas usa el mismo `day.php` para ambos; se separan por `id_tipo` (`1/2/3` aulas · `12` equipos).
4. Tu alcance = **solo aulas** (lo de los archivos / enlaces de `disponibilidad.php`).
5. **Equipos:** el jefe + Krystel revisan alternativas productivas (KOHA). No entra en este desarrollo.

## Qué sigue — en este orden

### Ahora (tú, local)

1. Entra a Reservitas y abre **Salones** (`id_tipo=1`) y **Auditorios** (`id_tipo=3`). Guarda 1 captura de cada uno (misma idea que la de informática).
2. En el menú **Reserva de Equipos** del portal, anota a qué URL manda Jardín (solo para el mapa; no lo construyas).
3. Pídele a Jonathan, otra vez y por escrito: la carpeta de Reservitas o al menos `day.php` + el archivo de conexión.

### Con Carlos Duarte (30 min)

Lleva: este mapa + captura de aulas + el PHP de enlaces.

Pregunta única de cierre:

> En `day.php` con `id_tipo=2` se ven materias en columnas `ED-…-AINF`. ¿Qué vista o tablas de Banner alimentan eso? ¿Sirve para MiPortalU en solo lectura?

### Con Manuel García (sesión 2, datos)

> Este backup carga `config{id_tipo}.inc.php` y parte Oracle (aulas) vs MySQL (equipos) en `id_tipo <= 3`. ¿En producción sigue igual? Pásame `config1`, `config2`, `config3` sin claves. En TEST, confirma que `V_RESERVAS_SALON` es aulas y que `id_tipo=12` no la usa.

### Cuando tengas `day.php`

Mándamelo (sin claves). Yo te marco:

- dónde está el SQL,
- qué parámetros usa,
- qué campos salen,
- qué clase PHP 5.6 armarías en el portal.

## Qué no haces todavía

- No armes UI de equipos.
- No copies la grilla beige de Reservitas tal cual.
- No pidas PHP 8 para Reservitas.
- No implementes el botón `+` de reserva.
