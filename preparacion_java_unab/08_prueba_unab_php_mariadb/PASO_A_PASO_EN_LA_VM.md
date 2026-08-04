# PASO A PASO EN LA VM (sin GitHub)

## Minuto 0–5 · XAMPP
1. Apache = Start
2. MySQL = ya running (OK)

## Minuto 5–10 · Estructura real (OBLIGATORIO)
En phpMyAdmin → SQL:

```sql
DESCRIBE GWRPIVR;
DESCRIBE GWRPIEM;
DESCRIBE GWRPICE;
DESCRIBE GWRPIRR;
```

Copia el resultado al chat (o foto). Con eso se ajustan nombres exactos.

También mira 1 fila:
```sql
SELECT * FROM GWRPIVR LIMIT 1;
SELECT * FROM GWRPIEM LIMIT 1;
SELECT * FROM GWRPICE LIMIT 1;
```

## Minuto 10–15 · Carpeta del proyecto
Crear en `C:\xampp\htdocs\alerta_desercion\` las carpetas:
- config
- api
- assets
- sql
- herramientas
- logs

## Orden de pegado de archivos
1. config/config.ejemplo.php
2. config/config.local.php
3. config/config.php
4. config/conexion.php
5. index.php (probar http://localhost/alerta_desercion/)
6. api/variables.php + variables.php + assets/variables.js + assets/app.css
7. sql/P_CALCULAR_RIESGO_ESTUDIANTE.sql (en phpMyAdmin, ajustado)
8. api/calcular.php + calculo.php + assets/calculo.js
9. api/reporte.php + reporte.php + assets/reporte.js
10. README.md
11. ZIP de entrega

## Pruebas mínimas antes del ZIP
- Listar 10 variables
- Crear / editar / inactivar
- CALL procedimiento (uno y masivo %)
- Reporte con 80 matriculados tras cálculo masivo
