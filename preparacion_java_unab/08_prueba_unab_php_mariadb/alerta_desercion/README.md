# Alerta temprana de deserción estudiantil — Entrega UNAB TIC

## Candidato
**Iván David Cardona Mendoza**  
Prueba técnica: Ingeniero de Sistemas y Operación TIC / Desarrollador  
Stack: **PHP + MariaDB + Bootstrap + jQuery + DataTables**  
Base de datos: `prueba_ing` (modelo **sin alteraciones**)

---

## 1. Cumplimiento del enunciado (checklist evaluador)

### 1.1 Actividades obligatorias del candidato

| # | Actividad | Estado | Evidencia en el sistema |
|---|-----------|--------|-------------------------|
| 1 | CRUD sobre `GWRPIVR` (AJAX, Bootstrap modal, DataTables, baja lógica Y/N) | Cumple | `variables.php` + `api/variables.php` + `assets/variables.js` |
| 2 | Procedimiento `P_CALCULAR_RIESGO_ESTUDIANTE` | Cumple | `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql` |
| 3 | PHP `CALL` con transacciones (commit solo si `P_CODIGO = 0`) | Cumple | `api/calcular.php` |
| 4 | Reporte DataTables `GWRPIEM` LEFT JOIN `GWRPIRR` | Cumple | `reporte.php` + `api/reporte.php` |
| 5 | Seguridad / integridad / auditoría / calidad | Cumple | PDO prepared statements, validaciones, USER/DATE, `logs/acciones.log`, XSS con `e()` |

### 1.2 Reglas de negocio

| Regla | Cumple | Cómo |
|-------|--------|------|
| Solo estudiantes `GWRPIEM_MATRICULADO = 'Y'` | Sí | SP + reporte + listado masivo |
| Puntaje = suma de pesos donde CE riesgo Y + CE activo Y + VR activo Y | Sí | JOINs del SP |
| Tope `LEAST(..., 100)` | Sí | SP |
| BAJO 0–29.99 / MEDIO 30–59.99 / ALTO 60–100 | Sí | SP + tablero |
| `GWRPIRR_VARIABLES_RIESGO` = **cantidad** (no lista de códigos) | Sí | `COUNT`/suma de flags en SP |
| Una fila por (periodo, estudiante): UPDATE si existe, INSERT si no | Sí | SP |
| SP **no** hace COMMIT/ROLLBACK (lo controla PHP) | Sí | SP sin commit; PHP `beginTransaction` / `commit` / `rollBack` |
| Cambio de pesos en GWRPIVR **no** refresca solo GWRPIRR | Sí | Hay que volver a calcular |
| No rediseñar / alterar el modelo de datos | Sí | Solo lectura/escritura sobre tablas existentes |

### 1.3 Procedimiento almacenado

- Nombre: `P_CALCULAR_RIESGO_ESTUDIANTE`
- Parámetros: `P_PERIODO`, `P_ID_ESTUDIANTE` (`%` = masivo), `P_USUARIO`, `OUT P_CODIGO`, `OUT P_MENSAJE`
- Archivo fuente: `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql`
- Instalación: phpMyAdmin → base `prueba_ing` → pestaña SQL → ejecutar el script

### 1.4 Entregables

| Entregable | Incluido |
|------------|----------|
| Código fuente PHP | Sí (`*.php`, `api/`, `assets/`, `config/`) |
| Script SP SQL | Sí (`sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql`) |
| README | Sí (este archivo) |
| Config de ejemplo | Sí (`config/config.ejemplo.php`) |
| ZIP antes del mediodía | Responsabilidad del candidato (ver §7) |

---

## 2. Qué resuelve el sistema
1. Administrar el catálogo de variables de riesgo (`GWRPIVR`).
2. Calcular el riesgo consolidado por estudiante/periodo.
3. Priorizar acompañamiento con tablero BAJO / MEDIO / ALTO / PENDIENTE.
4. Extras de valor: detalle de variables aportantes, export CSV, barra de progreso, auditoría visible bajo interruptor, bitácora en archivo.

---

## 3. Instalación en la VM (XAMPP)
1. Encender **Apache** y **MySQL**.
2. Proyecto en DocumentRoot de la prueba: `C:\xampp\htdocs\pruebaIng` (URL `http://localhost/`).
3. Copiar `config/config.ejemplo.php` → `config/config.local.php` y ajustar usuario/clave/periodo.
4. En phpMyAdmin → `prueba_ing` → SQL: ejecutar `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql`.
5. Abrir `http://localhost/` → flujo **Variables → Cálculo → Reporte**.

### Config mínima (`config.local.php`)
```php
<?php
return [
    'db' => [
        'host' => '127.0.0.1',
        'port' => '3306',
        'name' => 'prueba_ing',
        'user' => 'root',
        'pass' => '',
        'charset' => 'utf8mb4',
    ],
    'app_user' => 'IVAN.CARDONA',
    'periodo_default' => '202630',
];
```

---

## 4. Bitácora `logs/acciones.log` (verificar)
La función `auditar()` en `config/conexion.php` escribe una línea JSON por acción.

**Cómo comprobarlo en la VM:**
1. En Variables: crear o editar una variable, o inactivar una.
2. En Cálculo: calcular un estudiante.
3. Abrir el archivo:
   - `C:\xampp\htdocs\pruebaIng\logs\acciones.log`
4. Debe existir y contener líneas como:
```json
{"fecha":"2026-07-28T...","usuario":"IVAN.CARDONA","accion":"CREAR_VARIABLE","detalle":{...},"ip":"::1"}
```

Si la carpeta `logs` no existe, el sistema la crea al primer evento. Si no aparece el archivo: revise permisos de escritura de Apache sobre esa carpeta.

Acciones registradas (entre otras): `CREAR_VARIABLE`, `ACTUALIZAR_VARIABLE`, `TOGGLE_VARIABLE`, `CALCULAR_RIESGO_OK`, `CALCULAR_RIESGO_ERROR`, `EXPORT_REPORTE_CSV`.

---

## 5. Capturas sugeridas (adjuntar al ZIP / informe)

| # | Pantalla | Qué demostrar |
|---|----------|----------------|
| 1 | `index.php` | Portada institucional |
| 2 | `variables.php` | CRUD + DataTables + interruptor auditoría |
| 3 | Modal nueva variable | Error de espacios **dentro** del modal |
| 4 | `calculo.php` | Barra de progreso masivo |
| 5 | `reporte.php` | KPIs (~80) + cola ALTO |
| 6 | Modal “Ver detalle” | Variables que aportaron al puntaje |
| 7 | CSV en Excel | Exportación del reporte |
| 8 | phpMyAdmin `GWRPIRR` | Fila tras cálculo |
| 9 | `logs/acciones.log` | Bitácora generada |

---

## 6. Decisiones técnicas (valor agregado)
1. PDO + transacciones en PHP; SP sin COMMIT/ROLLBACK.
2. Baja lógica Y/N (sin borrado físico).
3. Código normalizado: mayúsculas, sin espacios, único.
4. Auditoría de columnas + interruptor “Mostrar auditoría” + log en archivo.
5. Reporte LEFT JOIN → PENDIENTE si no hay cálculo.
6. Detalle aportantes con la misma regla del SP.
7. CSV UTF-8 con BOM para Excel.
8. Recálculo masivo con progreso visual (uno a uno).
9. UX clara para usuarios no técnicos (mensajes en español dentro del modal).

---

## 7. Checklist de empaquetado ZIP
- [ ] Carpeta completa del proyecto
- [ ] `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql`
- [ ] `README.md` (este archivo)
- [ ] `config/config.ejemplo.php`
- [ ] `config.local.php` con contraseñas reales **fuera** del ZIP si aplica
- [ ] Capturas (opcional pero recomendado)
- [ ] Probar Variables / Cálculo / Reporte / Detalle / CSV / log
- [ ] Nombre: `Cardona_Ivan_AlertaDesercion.zip`

---

## 8. Estructura
```
pruebaIng/
  api/                  endpoints AJAX
  assets/               js / css / img
  config/               conexion y config
  herramientas/         inspección de modelo
  logs/                 bitácora local (acciones.log)
  sql/                  procedimiento almacenado
  index.php             portada
  variables.php         CRUD GWRPIVR
  calculo.php           cálculo + progreso
  reporte.php           tablero + detalle + CSV
  README.md
```

## 9. Nota
No se modificó el modelo de `prueba_ing`. Los nombres de columnas usados son los reales (`GWRPIVR_*`, `GWRPIEM_*`, `GWRPICE_*`, `GWRPIRR_*`).
