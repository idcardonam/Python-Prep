<?php
/**
 * API AJAX — CRUD GWRPIVR (columnas REALES)
 * USER_ADD / DATE_ADD / USER_UPD / DATE_UPD
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

$accion = $_GET['accion'] ?? $_POST['accion'] ?? '';

try {
    switch ($accion) {
        case 'listar':
            listarVariables($pdo);
            break;
        case 'obtener':
            obtenerVariable($pdo);
            break;
        case 'crear':
            crearVariable($pdo);
            break;
        case 'actualizar':
            actualizarVariable($pdo);
            break;
        case 'toggle_activo':
            toggleActivo($pdo);
            break;
        default:
            json_response(['ok' => false, 'mensaje' => 'Acción no reconocida'], 400);
    }
} catch (Throwable $e) {
    auditar('ERROR_API_VARIABLES', ['error' => $e->getMessage(), 'accion' => $accion]);
    json_response([
        'ok' => false,
        'mensaje' => 'Ocurrió un error controlado al procesar la solicitud.',
        'detalle' => $e->getMessage(),
    ], 500);
}

function listarVariables(PDO $pdo): void
{
    $sql = "SELECT
                GWRPIVR_ID AS id,
                GWRPIVR_CODIGO AS codigo,
                GWRPIVR_NOMBRE AS nombre,
                GWRPIVR_DESCRIPCION AS descripcion,
                GWRPIVR_PESO AS peso,
                GWRPIVR_ACTIVO AS activo,
                GWRPIVR_USER_ADD AS user_ins,
                GWRPIVR_DATE_ADD AS date_ins,
                GWRPIVR_USER_UPD AS user_upd,
                GWRPIVR_DATE_UPD AS date_upd
            FROM GWRPIVR
            ORDER BY GWRPIVR_ID ASC";
    $rows = $pdo->query($sql)->fetchAll();
    json_response(['ok' => true, 'data' => $rows]);
}

function obtenerVariable(PDO $pdo): void
{
    $id = (int)($_GET['id'] ?? 0);
    if ($id <= 0) {
        json_response(['ok' => false, 'mensaje' => 'ID inválido'], 422);
    }
    $st = $pdo->prepare("SELECT
            GWRPIVR_ID AS id,
            GWRPIVR_CODIGO AS codigo,
            GWRPIVR_NOMBRE AS nombre,
            GWRPIVR_DESCRIPCION AS descripcion,
            GWRPIVR_PESO AS peso,
            GWRPIVR_ACTIVO AS activo
        FROM GWRPIVR WHERE GWRPIVR_ID = ?");
    $st->execute([$id]);
    $row = $st->fetch();
    if (!$row) {
        json_response(['ok' => false, 'mensaje' => 'Variable no encontrada'], 404);
    }
    json_response(['ok' => true, 'data' => $row]);
}

function normalizarCodigo(string $codigo): array
{
    // Detectar espacios ANTES del trim/normalización para mensaje claro al usuario
    if (preg_match('/\s/', $codigo)) {
        return [false, 'El código no puede tener espacios. Escriba por ejemplo BAJO_RENDIMIENTO (con guion bajo), no “BAJO RENDIMIENTO”.', 'codigo'];
    }
    $codigo = strtoupper(trim($codigo));
    if ($codigo === '') {
        return [false, 'Debe escribir un código. Ejemplo: BAJO_RENDIMIENTO', 'codigo'];
    }
    if (!preg_match('/^[A-Z0-9_\-]+$/', $codigo)) {
        return [false, 'El código solo admite letras, números, guion (-) y guion bajo (_).', 'codigo'];
    }
    return [true, $codigo, null];
}

function validarPayload(array $in, bool $esCreacion): array
{
    $errores = [];
    $codigo = '';

    $campo = null;

    if ($esCreacion) {
        [$okCod, $codigoOMsg, $campoCod] = normalizarCodigo((string)($in['codigo'] ?? ''));
        if (!$okCod) {
            $errores[] = $codigoOMsg;
            $campo = $campoCod;
        } else {
            $codigo = $codigoOMsg;
        }
    }

    $nombre = trim((string)($in['nombre'] ?? ''));
    if ($nombre === '') {
        $errores[] = 'Escriba un nombre claro para esta variable.';
        $campo = $campo ?? 'nombre';
    }

    $descripcion = trim((string)($in['descripcion'] ?? ''));
    $pesoRaw = $in['peso'] ?? '';
    if ($pesoRaw === '' || !is_numeric($pesoRaw)) {
        $errores[] = 'Indique el peso: debe ser un número entre 0 y 100.';
        $peso = null;
        $campo = $campo ?? 'peso';
    } else {
        $peso = (float)$pesoRaw;
        if ($peso < 0 || $peso > 100) {
            $errores[] = 'El peso debe estar entre 0 y 100.';
            $campo = $campo ?? 'peso';
        }
    }

    $activo = strtoupper(trim((string)($in['activo'] ?? 'Y')));
    if (!in_array($activo, ['Y', 'N'], true)) {
        $errores[] = 'El estado solo admite Activa (Y) o Inactiva (N).';
    }

    return [$errores, $codigo, $nombre, $descripcion, $peso, $activo, $campo];
}

function crearVariable(PDO $pdo): void
{
    [$errores, $codigo, $nombre, $descripcion, $peso, $activo, $campo] = validarPayload($_POST, true);
    if ($errores) {
        json_response([
            'ok' => false,
            'mensaje' => implode(' ', $errores),
            'campo' => $campo,
        ], 422);
    }

    $sql = "INSERT INTO GWRPIVR (
                GWRPIVR_CODIGO, GWRPIVR_NOMBRE, GWRPIVR_DESCRIPCION, GWRPIVR_PESO, GWRPIVR_ACTIVO,
                GWRPIVR_USER_ADD, GWRPIVR_DATE_ADD
            ) VALUES (?, ?, ?, ?, ?, ?, NOW())";
    try {
        $st = $pdo->prepare($sql);
        $st->execute([$codigo, $nombre, $descripcion, $peso, $activo, app_user()]);
    } catch (PDOException $e) {
        if ($e->getCode() === '23000') {
            json_response(['ok' => false, 'mensaje' => 'Ya existe una variable con ese código. Debe ser único.'], 409);
        }
        throw $e;
    }

    auditar('CREAR_VARIABLE', ['codigo' => $codigo, 'peso' => $peso, 'activo' => $activo]);
    json_response(['ok' => true, 'mensaje' => 'Variable de riesgo creada correctamente.']);
}

function actualizarVariable(PDO $pdo): void
{
    $id = (int)($_POST['id'] ?? 0);
    if ($id <= 0) {
        json_response(['ok' => false, 'mensaje' => 'ID inválido'], 422);
    }

    [$errores, , $nombre, $descripcion, $peso, $activo, $campo] = validarPayload($_POST, false);
    if ($errores) {
        json_response([
            'ok' => false,
            'mensaje' => implode(' ', $errores),
            'campo' => $campo,
        ], 422);
    }

    $sql = "UPDATE GWRPIVR
            SET GWRPIVR_NOMBRE = ?,
                GWRPIVR_DESCRIPCION = ?,
                GWRPIVR_PESO = ?,
                GWRPIVR_ACTIVO = ?,
                GWRPIVR_USER_UPD = ?,
                GWRPIVR_DATE_UPD = NOW()
            WHERE GWRPIVR_ID = ?";
    $st = $pdo->prepare($sql);
    $st->execute([$nombre, $descripcion, $peso, $activo, app_user(), $id]);

    if ($st->rowCount() === 0) {
        $check = $pdo->prepare('SELECT 1 FROM GWRPIVR WHERE GWRPIVR_ID = ?');
        $check->execute([$id]);
        if (!$check->fetchColumn()) {
            json_response(['ok' => false, 'mensaje' => 'Variable no encontrada'], 404);
        }
    }

    auditar('ACTUALIZAR_VARIABLE', ['id' => $id, 'peso' => $peso, 'activo' => $activo]);
    json_response(['ok' => true, 'mensaje' => 'Variable actualizada. Si cambió el peso, ejecute nuevamente el cálculo para refrescar GWRPIRR.']);
}

function toggleActivo(PDO $pdo): void
{
    $id = (int)($_POST['id'] ?? 0);
    $nuevo = strtoupper(trim((string)($_POST['activo'] ?? '')));
    if ($id <= 0 || !in_array($nuevo, ['Y', 'N'], true)) {
        json_response(['ok' => false, 'mensaje' => 'Parámetros inválidos para activar/inactivar.'], 422);
    }

    $st = $pdo->prepare("UPDATE GWRPIVR
                         SET GWRPIVR_ACTIVO = ?, GWRPIVR_USER_UPD = ?, GWRPIVR_DATE_UPD = NOW()
                         WHERE GWRPIVR_ID = ?");
    $st->execute([$nuevo, app_user(), $id]);

    auditar('TOGGLE_VARIABLE', ['id' => $id, 'activo' => $nuevo]);
    $msg = $nuevo === 'Y' ? 'Variable reactivada.' : 'Variable inactivada (baja lógica).';
    json_response(['ok' => true, 'mensaje' => $msg]);
}
