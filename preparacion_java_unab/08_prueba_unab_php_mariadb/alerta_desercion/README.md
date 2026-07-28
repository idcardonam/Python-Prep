# Alerta temprana de deserción estudiantil — Entrega UNAB TIC

## Candidato
**Iván David Cardona Mendoza**  
Prueba: Ingeniero de Sistemas y Operación TIC / Desarrollador  
Stack: PHP + MariaDB + Bootstrap + jQuery + DataTables

---

## Qué resuelve
Módulo de alerta temprana sobre la base `prueba_ing` (sin alterar el modelo de datos):

1. **CRUD AJAX** de variables de riesgo (`GWRPIVR`) con baja lógica Y/N.
2. **Cálculo** vía `P_CALCULAR_RIESGO_ESTUDIANTE` con transacciones en PHP.
3. **Reporte** de matriculados (`GWRPIEM` LEFT JOIN `GWRPIRR`) con priorización operativa.

---

## Capturas sugeridas (adjuntar al ZIP / informe)
Coloque capturas en una carpeta `capturas/` o péguelas en el PDF de entrega:

| # | Pantalla | Qué demostrar |
|---|----------|----------------|
| 1 | `index.php` | Portada institucional UNAB |
| 2 | `variables.php` | Listado + botón Agregar + interruptor auditoría |
| 3 | Modal nueva variable | Validación de código con espacios (error dentro del modal) |
| 4 | `calculo.php` | Barra de progreso en recálculo masivo |
| 5 | `reporte.php` | KPIs 80 matriculados + cola ALTO |
| 6 | Modal “Ver detalle” | Variables que aportaron al puntaje |
| 7 | Export CSV | Archivo abierto en Excel |
| 8 | phpMyAdmin | Fila en `GWRPIRR` tras el cálculo |

---

## Checklist de entrega (antes del mediodía)
- [ ] Carpeta del proyecto completa (PHP, `sql/`, `assets/`, `config/`, `README.md`)
- [ ] `config/config.ejemplo.php` incluido (sin contraseñas reales)
- [ ] `config/config.local.php` **NO** subir con claves sensibles si el ZIP es público; documentar cómo crearlo
- [ ] Script `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql` ejecutable en phpMyAdmin
- [ ] CRUD Variables funciona (crear / editar / inactivar / reactivar)
- [ ] Cálculo individual OK (`P_CODIGO = 0`)
- [ ] Cálculo masivo ~80 matriculados con barra de progreso
- [ ] Reporte con LEFT JOIN y niveles BAJO/MEDIO/ALTO/PENDIENTE
- [ ] Detalle por estudiante (variables aportantes)
- [ ] Export CSV del reporte
- [ ] Bitácora `logs/acciones.log` generada al operar
- [ ] README leído y rutas de la VM verificadas
- [ ] ZIP nombrado claramente (ej. `Cardona_Ivan_AlertaDesercion.zip`)

---

## Instalación en la VM (XAMPP)
1. Encender **Apache** y **MySQL**.
2. Proyecto en DocumentRoot (en esta prueba: `C:\xampp\htdocs\pruebaIng`).
3. Copiar `config/config.ejemplo.php` → `config/config.local.php` y ajustar usuario/clave/periodo.
4. En phpMyAdmin → base `prueba_ing` → SQL: ejecutar `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql`.
5. Abrir `http://localhost/` (o la ruta que apunte al DocumentRoot).
6. Flujo: **Variables → Cálculo → Reporte**.

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

## Decisiones técnicas (valor agregado)
1. **PDO + transacciones en PHP**: el SP no hace COMMIT/ROLLBACK; PHP confirma solo si `P_CODIGO = 0`.
2. **Baja lógica** en variables (`Y/N`), sin borrado físico.
3. **Normalización de código**: mayúsculas, sin espacios, unicidad.
4. **Auditoría**: columnas USER/DATE + interruptor “Mostrar auditoría” + `logs/acciones.log`.
5. **Reporte LEFT JOIN**: PENDIENTE cuando aún no hay cálculo.
6. **Detalle aportantes**: mismas reglas del SP (CE riesgo Y + CE activo Y + VR activo Y).
7. **Export CSV** UTF-8 con BOM para Excel.
8. **Progreso masivo**: lista matriculados y calcula uno a uno con barra visual.
9. **UX no técnica**: mensajes claros dentro del modal; buscador guiado en español.

## Clasificación de riesgo
- BAJO: 0 – 29.99  
- MEDIO: 30 – 59.99  
- ALTO: 60 – 100  
- Puntaje = suma de pesos aplicables, tope 100 (`LEAST`)

## Pruebas sugeridas
1. Listar variables; ocultar/mostrar auditoría.
2. Crear variable con espacios en código → error **dentro** del modal.
3. Código duplicado → mensaje de unicidad.
4. Editar peso; inactivar / reactivar.
5. Calcular un estudiante → fila en `GWRPIRR`.
6. Recalcular período con barra de progreso → ~80 matriculados.
7. Reporte: filtrar ALTO; **Ver detalle**; exportar CSV.

## Estructura
```
pruebaIng/   (o alerta_desercion/)
  api/                  endpoints AJAX
  assets/               js / css / img
  config/               conexion y config
  herramientas/         inspección de modelo
  logs/                 bitácora local
  sql/                  procedimiento
  index.php             portada
  variables.php         CRUD
  calculo.php           cálculo + progreso
  reporte.php           tablero + detalle + CSV
  README.md             este documento
```

## Nota
El código asume los nombres reales de columnas (`GWRPIVR_*`, `GWRPIEM_*`, `GWRPICE_*`, `GWRPIRR_*`).
Si el entorno difiere, use `herramientas/ver_estructura.php` y ajuste solo alias/columnas, manteniendo las reglas del enunciado.
