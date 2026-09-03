# Hallazgo confirmado — dos módulos, un solo destino Reservitas

Fecha: 3 sep 2026. Fuentes: PHP de Iván, capturas Reservitas + menú MiPortalU, conversación con Manuel García.

## Corte claro

En MiPortalU hay **dos menús distintos**. En Reservitas es el **mismo** `day.php`, pero con **parámetros distintos**.

| En MiPortalU | Menú | Qué es | ¿Proyecto de Iván? |
| --- | --- | --- | --- |
| Reserva de Espacios → **Disponibilidad de Aulas** | `disponibilidad.php` | Consulta de aulas / salones / auditorios | **SÍ** |
| **Reserva de Equipos** (Jardín, Bosque, CSU, Caldas, Estación 42, La Casona) | Otro enlace | Préstamo de cámaras, kits, Zoom salas, etc. | **NO** |

Manuel lo dijo bien: son dos módulos. No los mezcles.

## Qué hace hoy `disponibilidad.php`

Confirmado con el código: **solo tabs + enlaces**. No hay SQL. No hay clase. No consulta Banner.

Includes: `headerInt.inc`, `lateralIzqInt.inc`, `footerInt.inc`.

### Mapa de enlaces (validado)

| Tab | Etiqueta sede | URL Reservitas |
| --- | --- | --- |
| Aulas de informática | Unab | `day.php?area=201&id_sede=1&id_tipo=2` |
| Aulas de informática | Instituto Caldas | `day.php?area=204&id_sede=4&id_tipo=2` |
| Salones | Campus Central | `day.php?id_sede=1&id_tipo=1` |
| Salones | CSU | `day.php?id_sede=2&id_tipo=1` |
| Salones | Campus el Bosque | `day.php?id_sede=3&id_tipo=1` |
| Salones | La Casona | `day.php?id_sede=5&id_tipo=1` |
| Auditorios | Campus Central | `day.php?id_sede=1&id_tipo=3` |

### Parámetros Reservitas

| Parámetro | Significado | Valores vistos |
| --- | --- | --- |
| `id_tipo` | Tipo de recurso | `1` salones · `2` informática · `3` auditorios · **`12` equipos (fuera de alcance)** |
| `id_sede` | Campus / sede | `1` Central/Jardín · `2` CSU · `3` Bosque · `4` Caldas · `5` La Casona |
| `area` | Subconjunto / edificio-área | `201` informática Jardín · `204` informática Caldas · `413` equipos (ejemplo captura) |
| `day` `month` `year` | Fecha (opcional en el enlace del portal) | En captura aulas no venía; Reservitas usa el día actual |

Host: `https://aulas.unab.edu.co/reservitas/day.php`

## Evidencia en pantallas

### Módulo AULAS (sí)

URL: `day.php?area=201&id_sede=1&id_tipo=2`

- Título: Sistema de Préstamos y Reservas.
- Campus: Jardín.
- Columnas: códigos tipo `ED-BLA-A11-AINF`, `ED-ING-L51-AINF`.
- Filas: 06:00 → ~21:00 / 22:00, cada 30 minutos.
- Celdas ocupadas: nombres de **materias** (Estadística, Cálculo, Fundamentos de Programación…) = programación académica.
- Celdas libres: `+` (en Reservitas permite intentar reserva; **en MiPortalU no se replica**).

### Módulo EQUIPOS (no)

URL: `day.php?area=413&id_sede=1&id_tipo=12&...`

- Dropdown **Equipos**: cámara web, kit simulación, telepresencia, micrófono, router, etc.
- Columnas: `ZOOM SALA(01)` … `(20)`.
- Reservas con Id (ej. 822645) y títulos de reuniones/comités.
- También tiene `+` para crear préstamo.

Misma pantalla `day.php`. Distinto `id_tipo` / `area`. Distinto negocio.

### Menú MiPortalU

Servicios Electrónicos ya separa:

- **Reserva de Equipos** → sedes.
- **Reserva de Espacios** → Disponibilidad de Aulas (+ Actualización Aulas Virtuales, Espacios UNAB Nuevo).

Tu reemplazo es solo **Disponibilidad de Aulas**.

## Conclusión técnica de esta etapa

1. MiPortalU no tiene lógica de disponibilidad: hay que **crearla**.
2. La lógica vive en Reservitas `day.php` + lo que ese PHP lea (Banner / vista / tablas).
3. `id_tipo` 1, 2, 3 = tu alcance. `id_tipo` 12 = otro proyecto.
4. En aulas lo que se muestra son **clases/eventos programados**, no un “préstamo de aula” hecho en Reservitas.
5. El `+` de Reservitas **no** se lleva a MiPortalU (consulta informativa).

## Qué falta (siguiente bloque)

1. Código fuente de Reservitas: `day.php` y dónde arma el SQL / llama la vista.
2. Con Carlos: nombre del objeto Banner de **aulas** (no equipos).
3. Con Manuel: en TEST, marcar objetos de `id_tipo` 1–3 vs. 12.
4. Tres pruebas de equivalencia (informática, salones, auditorios) misma fecha.
