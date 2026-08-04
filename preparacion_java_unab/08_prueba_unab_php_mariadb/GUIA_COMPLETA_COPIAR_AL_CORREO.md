# GUIA COMPLETA — Prueba UNAB TIC (PHP + MariaDB)
# Sistema de alerta temprana de deserción estudiantil
# Copia este archivo a tu correo y ve pegando bloque por bloque en la VM

IMPORTANTE
- NO modifiques el modelo de datos (no CREATE/ALTER TABLE de las tablas dadas).
- SI puedes crear el PROCEDURE (lo pide el enunciado).
- Antes de pegar codigo: abre phpMyAdmin → base prueba_ing → anota nombres REALES de tablas/columnas.
- Donde diga AJUSTAR: cambia al nombre real que veas.

================================================================
PASO 0 — RECONOCIMIENTO (10 minutos)
================================================================

1. Abre el navegador en la VM.
2. Entra a phpMyAdmin (normalmente http://localhost/phpmyadmin).
3. Selecciona la base: prueba_ing
4. Anota en papel:

TABLAS QUE VES:
- ________________________________
- ________________________________
- ________________________________

COLUMNAS de la tabla de VARIABLES DE RIESGO:
- ________________________________

COLUMNAS de ESTUDIANTES (o similar):
- ________________________________

5. Busca la carpeta del proyecto PHP. Rutas comunes:
   C:\xampp\htdocs\
   C:\wampp\www\
   C:\Apache24\htdocs\
6. Crea una carpeta de trabajo, ejemplo:
   C:\xampp\htdocs\alerta_desercion\

Estructura recomendada:

alerta_desercion/
  config/
    conexion.php
  variables/
    index.php
    crear.php
    guardar.php
    editar.php
    actualizar.php
    eliminar.php
  riesgo/
    calcular.php
  reporte/
    index.php
  index.php

================================================================
PASO 1 — CONFIGURACION DE CONEXION
================================================================

Archivo: config/conexion.php

```php
<?php
/**
 * Conexion a MariaDB - Prueba UNAB
 * Ajusta usuario/clave si en la VM son distintos.
 */
$host = "localhost";
$usuario = "root";
$clave = ""; // en XAMPP suele ir vacia; si pide clave, colocala
$baseDatos = "prueba_ing";

$mysqli = new mysqli($host, $usuario, $clave, $baseDatos);

if ($mysqli->connect_errno) {
    http_response_code(500);
    die("Error de conexion MySQL: " . $mysqli->connect_error);
}

// UTF-8 para tildes y ñ
$mysqli->set_charset("utf8mb4");

/**
 * Helper simple para escapar salida HTML (seguridad XSS)
 */
function e(?string $texto): string
{
    return htmlspecialchars((string)$texto, ENT_QUOTES, "UTF-8");
}
```

Prueba rapida: crea index.php en la raiz:

```php
<?php
require_once __DIR__ . "/config/conexion.php";
echo "Conexion OK a prueba_ing";
```

Abre: http://localhost/alerta_desercion/
Si sale "Conexion OK", sigue.

================================================================
PASO 2 — CRUD VARIABLES DE RIESGO
================================================================

NOTA DE AJUSTE DE TABLA
En los ejemplos uso:
  tabla: variables_riesgo
  campos: id, nombre, descripcion, peso, activo

Si en phpMyAdmin se llama distinto, reemplaza TODOS esos nombres.

------------------------------------------------
2.1 Archivo: variables/index.php  (LISTAR)
------------------------------------------------

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

$sql = "SELECT id, nombre, descripcion, peso, activo
        FROM variables_riesgo
        ORDER BY id ASC";
$resultado = $mysqli->query($sql);

if (!$resultado) {
    die("Error al listar: " . $mysqli->error);
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Variables de riesgo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 24px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f2f2f2; }
        .ok { color: green; }
        .err { color: #b00020; }
        a.btn { display: inline-block; padding: 6px 10px; background: #0b5fff; color: #fff; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Variables de riesgo</h1>

    <?php if (isset($_GET["msg"])): ?>
        <p class="ok"><?= e($_GET["msg"]) ?></p>
    <?php endif; ?>
    <?php if (isset($_GET["error"])): ?>
        <p class="err"><?= e($_GET["error"]) ?></p>
    <?php endif; ?>

    <p><a class="btn" href="crear.php">Nueva variable</a>
       <a class="btn" href="../reporte/index.php">Ver reporte</a>
       <a class="btn" href="../riesgo/calcular.php">Calcular riesgo</a></p>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Descripcion</th>
                <th>Peso</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
        <?php while ($fila = $resultado->fetch_assoc()): ?>
            <tr>
                <td><?= e($fila["id"]) ?></td>
                <td><?= e($fila["nombre"]) ?></td>
                <td><?= e($fila["descripcion"]) ?></td>
                <td><?= e($fila["peso"]) ?></td>
                <td><?= ((int)$fila["activo"] === 1) ? "Si" : "No" ?></td>
                <td>
                    <a href="editar.php?id=<?= (int)$fila["id"] ?>">Editar</a> |
                    <a href="eliminar.php?id=<?= (int)$fila["id"] ?>"
                       onclick="return confirm('¿Eliminar esta variable?');">Eliminar</a>
                </td>
            </tr>
        <?php endwhile; ?>
        </tbody>
    </table>
</body>
</html>
```

------------------------------------------------
2.2 Archivo: variables/crear.php  (FORMULARIO ALTA)
------------------------------------------------

```php
<?php require_once __DIR__ . "/../config/conexion.php"; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear variable de riesgo</title>
</head>
<body>
    <h1>Crear variable de riesgo</h1>
    <form method="post" action="guardar.php">
        <p>
            <label>Nombre *</label><br>
            <input type="text" name="nombre" maxlength="100" required>
        </p>
        <p>
            <label>Descripcion *</label><br>
            <textarea name="descripcion" rows="4" cols="50" required></textarea>
        </p>
        <p>
            <label>Peso (0 a 100) *</label><br>
            <input type="number" name="peso" step="0.01" min="0" max="100" required>
        </p>
        <p>
            <label>
                <input type="checkbox" name="activo" value="1" checked>
                Activo
            </label>
        </p>
        <button type="submit">Guardar</button>
        <a href="index.php">Cancelar</a>
    </form>
</body>
</html>
```

------------------------------------------------
2.3 Archivo: variables/guardar.php  (INSERT seguro)
------------------------------------------------

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: index.php");
    exit;
}

$nombre = trim($_POST["nombre"] ?? "");
$descripcion = trim($_POST["descripcion"] ?? "");
$peso = $_POST["peso"] ?? "";
$activo = isset($_POST["activo"]) ? 1 : 0;

// Validaciones de integridad
if ($nombre === "" || mb_strlen($nombre) < 3) {
    header("Location: index.php?error=" . urlencode("Nombre invalido (minimo 3 caracteres)"));
    exit;
}
if ($descripcion === "" || mb_strlen($descripcion) < 5) {
    header("Location: index.php?error=" . urlencode("Descripcion invalida"));
    exit;
}
if (!is_numeric($peso) || $peso < 0 || $peso > 100) {
    header("Location: index.php?error=" . urlencode("Peso debe estar entre 0 y 100"));
    exit;
}

$sql = "INSERT INTO variables_riesgo (nombre, descripcion, peso, activo)
        VALUES (?, ?, ?, ?)";
$stmt = $mysqli->prepare($sql);
if (!$stmt) {
    die("Error prepare: " . $mysqli->error);
}

$pesoFloat = (float)$peso;
$stmt->bind_param("ssdi", $nombre, $descripcion, $pesoFloat, $activo);

if (!$stmt->execute()) {
    header("Location: index.php?error=" . urlencode("No se pudo guardar: " . $stmt->error));
    exit;
}

$stmt->close();
header("Location: index.php?msg=" . urlencode("Variable creada correctamente"));
exit;
```

------------------------------------------------
2.4 Archivo: variables/editar.php  (FORMULARIO EDICION)
------------------------------------------------

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

$id = (int)($_GET["id"] ?? 0);
if ($id <= 0) {
    header("Location: index.php?error=" . urlencode("ID invalido"));
    exit;
}

$stmt = $mysqli->prepare("SELECT id, nombre, descripcion, peso, activo FROM variables_riesgo WHERE id = ?");
$stmt->bind_param("i", $id);
$stmt->execute();
$res = $stmt->get_result();
$variable = $res->fetch_assoc();
$stmt->close();

if (!$variable) {
    header("Location: index.php?error=" . urlencode("Variable no encontrada"));
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Editar variable</title>
</head>
<body>
    <h1>Editar variable #<?= e($variable["id"]) ?></h1>
    <form method="post" action="actualizar.php">
        <input type="hidden" name="id" value="<?= (int)$variable["id"] ?>">
        <p>
            <label>Nombre *</label><br>
            <input type="text" name="nombre" maxlength="100" required
                   value="<?= e($variable["nombre"]) ?>">
        </p>
        <p>
            <label>Descripcion *</label><br>
            <textarea name="descripcion" rows="4" cols="50" required><?= e($variable["descripcion"]) ?></textarea>
        </p>
        <p>
            <label>Peso (0 a 100) *</label><br>
            <input type="number" name="peso" step="0.01" min="0" max="100" required
                   value="<?= e($variable["peso"]) ?>">
        </p>
        <p>
            <label>
                <input type="checkbox" name="activo" value="1"
                    <?= ((int)$variable["activo"] === 1) ? "checked" : "" ?>>
                Activo
            </label>
        </p>
        <button type="submit">Actualizar</button>
        <a href="index.php">Cancelar</a>
    </form>
</body>
</html>
```

------------------------------------------------
2.5 Archivo: variables/actualizar.php  (UPDATE seguro)
------------------------------------------------

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    header("Location: index.php");
    exit;
}

$id = (int)($_POST["id"] ?? 0);
$nombre = trim($_POST["nombre"] ?? "");
$descripcion = trim($_POST["descripcion"] ?? "");
$peso = $_POST["peso"] ?? "";
$activo = isset($_POST["activo"]) ? 1 : 0;

if ($id <= 0) {
    header("Location: index.php?error=" . urlencode("ID invalido"));
    exit;
}
if ($nombre === "" || mb_strlen($nombre) < 3) {
    header("Location: index.php?error=" . urlencode("Nombre invalido"));
    exit;
}
if ($descripcion === "" || mb_strlen($descripcion) < 5) {
    header("Location: index.php?error=" . urlencode("Descripcion invalida"));
    exit;
}
if (!is_numeric($peso) || $peso < 0 || $peso > 100) {
    header("Location: index.php?error=" . urlencode("Peso invalido"));
    exit;
}

$sql = "UPDATE variables_riesgo
        SET nombre = ?, descripcion = ?, peso = ?, activo = ?
        WHERE id = ?";
$stmt = $mysqli->prepare($sql);
$pesoFloat = (float)$peso;
$stmt->bind_param("ssdii", $nombre, $descripcion, $pesoFloat, $activo, $id);

if (!$stmt->execute()) {
    header("Location: index.php?error=" . urlencode("No se pudo actualizar"));
    exit;
}

$stmt->close();
header("Location: index.php?msg=" . urlencode("Variable actualizada"));
exit;
```

------------------------------------------------
2.6 Archivo: variables/eliminar.php  (DELETE seguro)
------------------------------------------------

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

$id = (int)($_GET["id"] ?? 0);
if ($id <= 0) {
    header("Location: index.php?error=" . urlencode("ID invalido"));
    exit;
}

// Si la tabla tiene FK y no deja borrar, cambia a UPDATE activo=0
$stmt = $mysqli->prepare("DELETE FROM variables_riesgo WHERE id = ?");
$stmt->bind_param("i", $id);

if (!$stmt->execute()) {
    // Alternativa de integridad: desactivar en vez de borrar
    $stmt2 = $mysqli->prepare("UPDATE variables_riesgo SET activo = 0 WHERE id = ?");
    $stmt2->bind_param("i", $id);
    if ($stmt2->execute()) {
        header("Location: index.php?msg=" . urlencode("Variable desactivada (no se pudo eliminar por integridad)"));
        exit;
    }
    header("Location: index.php?error=" . urlencode("No se pudo eliminar"));
    exit;
}

$stmt->close();
header("Location: index.php?msg=" . urlencode("Variable eliminada"));
exit;
```

================================================================
PASO 3 — STORED PROCEDURE (calcular riesgo del estudiante)
================================================================

En phpMyAdmin → SQL, primero MIRA las tablas reales.
Este procedure es una plantilla tipica. AJUSTA nombres.

CASO A — Si tienes tablas tipo:
- estudiantes(id, nombre, ...)
- estudiante_variable(id_estudiante, id_variable, valor)
- variables_riesgo(id, nombre, peso, activo)

```sql
DELIMITER //

CREATE PROCEDURE sp_calcular_riesgo_estudiante(IN p_id_estudiante INT)
BEGIN
    DECLARE v_puntaje DECIMAL(10,2) DEFAULT 0;
    DECLARE v_nivel VARCHAR(20);

    -- Suma ponderada de variables activas del estudiante
    SELECT IFNULL(SUM(ev.valor * vr.peso) / NULLIF(SUM(vr.peso), 0), 0)
      INTO v_puntaje
      FROM estudiante_variable ev
      INNER JOIN variables_riesgo vr ON vr.id = ev.id_variable
     WHERE ev.id_estudiante = p_id_estudiante
       AND vr.activo = 1;

    -- Umbrales (ajustalos si el enunciado define otros)
    IF v_puntaje >= 70 THEN
        SET v_nivel = 'ALTO';
    ELSEIF v_puntaje >= 40 THEN
        SET v_nivel = 'MEDIO';
    ELSE
        SET v_nivel = 'BAJO';
    END IF;

    SELECT
        p_id_estudiante AS id_estudiante,
        ROUND(v_puntaje, 2) AS puntaje_riesgo,
        v_nivel AS nivel_riesgo;
END //

DELIMITER ;
```

Probar en phpMyAdmin:
```sql
CALL sp_calcular_riesgo_estudiante(1);
```

CASO B — Si el enunciado ya da la formula exacta:
Copia la formula del PDF/Word y solo cambia el cuerpo del procedure.
No inventes reglas distintas a las del examen.

Si dice que el procedure YA existe, no lo crees: solo usalo desde PHP.

================================================================
PASO 4 — INTEGRAR EL PROCEDURE EN PHP
================================================================

Archivo: riesgo/calcular.php

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

$idEstudiante = (int)($_GET["id_estudiante"] ?? $_POST["id_estudiante"] ?? 0);
$resultadoRiesgo = null;
$error = null;

// Lista de estudiantes para el select (AJUSTAR nombre de tabla/columnas)
$estudiantes = $mysqli->query("SELECT id, nombre FROM estudiantes ORDER BY nombre ASC");

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if ($idEstudiante <= 0) {
        $error = "Seleccione un estudiante valido";
    } else {
        $stmt = $mysqli->prepare("CALL sp_calcular_riesgo_estudiante(?)");
        if (!$stmt) {
            $error = "No se pudo preparar el procedimiento: " . $mysqli->error;
        } else {
            $stmt->bind_param("i", $idEstudiante);
            if ($stmt->execute()) {
                $res = $stmt->get_result();
                if ($res) {
                    $resultadoRiesgo = $res->fetch_assoc();
                    $res->free();
                }
                // limpiar resultados extra del CALL
                while ($mysqli->more_results() && $mysqli->next_result()) { /* noop */ }
            } else {
                $error = "Error al ejecutar SP: " . $stmt->error;
            }
            $stmt->close();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Calcular riesgo de deserción</title>
</head>
<body>
    <h1>Calcular nivel de riesgo</h1>
    <p><a href="../variables/index.php">Volver a variables</a></p>

    <?php if ($error): ?>
        <p style="color:#b00020;"><?= e($error) ?></p>
    <?php endif; ?>

    <form method="post">
        <label>Estudiante</label>
        <select name="id_estudiante" required>
            <option value="">-- Seleccione --</option>
            <?php if ($estudiantes): while ($e = $estudiantes->fetch_assoc()): ?>
                <option value="<?= (int)$e["id"] ?>" <?= $idEstudiante === (int)$e["id"] ? "selected" : "" ?>>
                    <?= e($e["nombre"]) ?>
                </option>
            <?php endwhile; endif; ?>
        </select>
        <button type="submit">Calcular riesgo</button>
    </form>

    <?php if ($resultadoRiesgo): ?>
        <h2>Resultado</h2>
        <ul>
            <li>ID estudiante: <?= e($resultadoRiesgo["id_estudiante"] ?? "") ?></li>
            <li>Puntaje: <?= e($resultadoRiesgo["puntaje_riesgo"] ?? "") ?></li>
            <li>Nivel: <strong><?= e($resultadoRiesgo["nivel_riesgo"] ?? "") ?></strong></li>
        </ul>
    <?php endif; ?>
</body>
</html>
```

================================================================
PASO 5 — REPORTE CON DATATABLES
================================================================

Archivo: reporte/index.php

Si la VM NO tiene internet, usa DataTables local (busca en htdocs si ya hay librerias).
Si hay internet, CDN funciona.

```php
<?php
require_once __DIR__ . "/../config/conexion.php";

/**
 * AJUSTAR este SQL al modelo real.
 * Idea: listar estudiantes con su info de riesgo / variables.
 * Ejemplo generico:
 */
$sql = "
    SELECT
        e.id,
        e.nombre,
        e.documento,
        e.programa,
        IFNULL(ROUND(SUM(ev.valor * vr.peso) / NULLIF(SUM(vr.peso), 0), 2), 0) AS puntaje
    FROM estudiantes e
    LEFT JOIN estudiante_variable ev ON ev.id_estudiante = e.id
    LEFT JOIN variables_riesgo vr ON vr.id = ev.id_variable AND vr.activo = 1
    GROUP BY e.id, e.nombre, e.documento, e.programa
    ORDER BY puntaje DESC
";

$resultado = $mysqli->query($sql);
if (!$resultado) {
    die("Error en reporte: " . $mysqli->error . " — Ajusta el SQL a las tablas reales.");
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de riesgo de deserción</title>

    <!-- DataTables + jQuery (CDN). Si no hay internet, cambia a archivos locales -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>

    <style>
        body { font-family: Arial, sans-serif; margin: 24px; }
        .alto { color: #b00020; font-weight: bold; }
        .medio { color: #b86b00; font-weight: bold; }
        .bajo { color: #0a7a2f; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Reporte de alerta temprana</h1>
    <p>
        <a href="../variables/index.php">CRUD Variables</a> |
        <a href="../riesgo/calcular.php">Calcular riesgo</a>
    </p>

    <table id="tablaRiesgo" class="display" style="width:100%">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Documento</th>
                <th>Programa</th>
                <th>Puntaje</th>
                <th>Nivel</th>
            </tr>
        </thead>
        <tbody>
        <?php while ($fila = $resultado->fetch_assoc()):
            $puntaje = (float)$fila["puntaje"];
            if ($puntaje >= 70) {
                $nivel = "ALTO";
                $clase = "alto";
            } elseif ($puntaje >= 40) {
                $nivel = "MEDIO";
                $clase = "medio";
            } else {
                $nivel = "BAJO";
                $clase = "bajo";
            }
        ?>
            <tr>
                <td><?= e($fila["id"]) ?></td>
                <td><?= e($fila["nombre"]) ?></td>
                <td><?= e($fila["documento"] ?? "") ?></td>
                <td><?= e($fila["programa"] ?? "") ?></td>
                <td><?= e(number_format($puntaje, 2)) ?></td>
                <td class="<?= $clase ?>"><?= e($nivel) ?></td>
            </tr>
        <?php endwhile; ?>
        </tbody>
    </table>

    <script>
        $(document).ready(function () {
            $('#tablaRiesgo').DataTable({
                pageLength: 10,
                language: {
                    url: "https://cdn.datatables.net/plug-ins/1.13.8/i18n/es-ES.json"
                }
            });
        });
    </script>
</body>
</html>
```

Si DataTables CDN falla (sin internet), deja la tabla HTML igual:
sigue siendo un reporte valido; agrega nota en README.

================================================================
PASO 6 — PORTADA SIMPLE
================================================================

Archivo: index.php

```php
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Alerta temprana de deserción - UNAB</title>
</head>
<body>
    <h1>Sistema de alerta temprana de deserción estudiantil</h1>
    <p>Prueba técnica - Ingeniero de Sistemas y Operación TIC</p>
    <ul>
        <li><a href="variables/index.php">1) CRUD Variables de riesgo</a></li>
        <li><a href="riesgo/calcular.php">2) Calcular riesgo (Stored Procedure)</a></li>
        <li><a href="reporte/index.php">3) Reporte DataTables</a></li>
    </ul>
</body>
</html>
```

================================================================
PASO 7 — CALIDAD, SEGURIDAD E INTEGRIDAD (checklist)
================================================================

Marca esto antes de entregar:

[ ] Toda consulta de escritura usa prepare + bind_param
[ ] No hay SQL concatenando $_POST directo
[ ] Salidas con htmlspecialchars / funcion e()
[ ] Validacion de vacios y rangos numericos
[ ] No alteraste tablas del modelo dado
[ ] El CALL al procedure funciona
[ ] CRUD crea / lista / edita / elimina (o desactiva)
[ ] DataTables muestra busqueda/paginacion
[ ] Nombres de archivos claros y ordenados

Archivo opcional: README.txt

```text
Proyecto: Alerta temprana de desercion estudiantil
Stack: PHP + Apache + MariaDB + phpMyAdmin
Base: prueba_ing

Modulos:
1. CRUD variables_riesgo
2. SP sp_calcular_riesgo_estudiante
3. Integracion PHP del SP
4. Reporte con DataTables
5. Validaciones y prepared statements

Pendientes / supuestos:
- Se ajustaron nombres de columnas al modelo real de prueba_ing
- Umbrales de riesgo: BAJO <40, MEDIO 40-69, ALTO >=70
  (reemplazar si el enunciado define otros)
```

================================================================
ORDEN EXACTO PARA IR PEGANDO EN LA VM
================================================================

1. Crear carpetas
2. Pegar config/conexion.php → probar index
3. Pegar CRUD variables (index, crear, guardar, editar, actualizar, eliminar)
4. Verificar nombres de tabla/columnas en phpMyAdmin y corregir
5. Crear/probar stored procedure
6. Pegar riesgo/calcular.php
7. Pegar reporte/index.php
8. Probar flujo completo
9. Revisar checklist de seguridad
10. Entregar carpeta + README

================================================================
SI ALGO FALLA — PREGUNTAS RAPIDAS AL ING. MANUEL GARCIA
================================================================

1. ¿Cual es el usuario/clave MySQL de la VM?
2. ¿Cuales son los nombres exactos de las tablas de variables y estudiantes?
3. ¿El procedimiento almacenado ya existe o debo crearlo?
4. ¿Hay formula/umbrales oficiales de riesgo en el enunciado?
5. ¿DataTables debe ir por CDN o hay libreria local?

================================================================
FIN DE LA GUIA
================================================================
