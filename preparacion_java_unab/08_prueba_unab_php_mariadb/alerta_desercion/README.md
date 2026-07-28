# Alerta temprana de deserción estudiantil — Entrega UNAB TIC

## Candidato
Iván David Cardona Mendoza  
Prueba: Ingeniero de Sistemas y Operación TIC / Desarrollador

## Qué resuelve
Módulo de alerta temprana sobre `prueba_ing` para:
1. Administrar variables de riesgo (`GWRPIVR`) con CRUD AJAX.
2. Calcular riesgo consolidado mediante `P_CALCULAR_RIESGO_ESTUDIANTE`.
3. Reportar estudiantes matriculados (`GWRPIEM_MATRICULADO = 'Y'`) con resultado en `GWRPIRR`.

## Stack
- PHP 8+ (PDO MySQL)
- MariaDB / MySQL (XAMPP)
- Bootstrap 5, jQuery, DataTables

## Instalación en la VM
1. Encender **Apache** y **MySQL** en XAMPP.
2. Copiar carpeta `alerta_desercion` a `C:\xampp\htdocs\`.
3. Ajustar `config/config.local.php` (usuario/clave/periodo).
4. Abrir `http://localhost/alerta_desercion/herramientas/ver_estructura.php` y validar columnas.
5. En phpMyAdmin → SQL: ejecutar `sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql` (ajustando nombres de columnas si difieren).
6. Abrir `http://localhost/alerta_desercion/`.

## Decisiones técnicas (valor agregado)
1. **PDO + transacciones en PHP**: el SP no hace COMMIT/ROLLBACK; PHP confirma solo si `P_CODIGO = 0`.
2. **Baja lógica** en variables (`Y/N`), evitando borrado físico cuando hay referencias en `GWRPICE`.
3. **Normalización de código**: mayúsculas, sin espacios, control de llave única.
4. **Auditoría**: `GWRPIVR_USER_UPD/DATE_UPD` + bitácora `logs/acciones.log` sin alterar el modelo.
5. **Reporte con LEFT JOIN**: muestra PENDIENTE cuando aún no hay cálculo.
6. **Panel resumen** BAJO/MEDIO/ALTO/PENDIENTE encima del DataTable (priorización operativa).
7. **Insignias con texto**: el color no es el único indicador de nivel.

## Clasificación de riesgo
- BAJO: 0 – 29.99
- MEDIO: 30 – 59.99
- ALTO: 60 – 100
- Puntaje = suma de pesos aplicables, tope 100 (`LEAST`)

## Pruebas sugeridas
1. Listar variables (deben verse las 10 iniciales).
2. Crear variable con código inválido (espacios) → rechazo.
3. Crear variable con código duplicado → mensaje de unicidad.
4. Editar peso y estado; verificar user/fecha de modificación.
5. Inactivar / reactivar.
6. Calcular un estudiante y verificar fila en `GWRPIRR`.
7. Recalcular con `%` y verificar ~80 matriculados en reporte.
8. Filtrar reporte por nivel ALTO / PENDIENTE.

## Estructura
```
alerta_desercion/
  api/           endpoints AJAX
  assets/        js/css
  config/        conexion y config
  herramientas/  inspección de modelo
  logs/          bitácora local
  sql/           procedimiento
  *.php          pantallas
```

## Nota sobre nombres de columnas
El SQL/PHP asume el prefijo de campos del enunciado (`GWRPIVR_*`, `GWRPIEM_*`, etc.).
Si `ver_estructura.php` muestra nombres distintos, ajustar únicamente alias/columnas
manteniendo las reglas de negocio del PDF.
