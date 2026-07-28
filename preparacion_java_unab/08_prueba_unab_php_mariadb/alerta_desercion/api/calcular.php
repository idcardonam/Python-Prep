<?php
/**
 * API AJAX — Cálculo de riesgo vía P_CALCULAR_RIESGO_ESTUDIANTE
 * La transacción vive en PHP (commit solo si P_CODIGO = 0).
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

if (($_POST['accion'] ?? '') !== 'calcular') {
    json_response(['ok' => false, 'mensaje' => 'Acción no válida'], 400);
}

$periodo = trim((string)($_POST['periodo'] ?? periodo_default()));
$idEstudiante = trim((string)($_POST['id_estudiante'] ?? ''));
$usuario = app_user();

if ($periodo === '') {
    json_response(['ok' => false, 'mensaje' => 'El período es obligatorio.'], 422);
}
if ($idEstudiante === '') {
    json_response(['ok' => false, 'mensaje' => 'Indique un estudiante o % para recálculo masivo.'], 422);
}

try {
    $pdo->beginTransaction();

    // OUT params vía variables de usuario
    $sql = "CALL P_CALCULAR_RIESGO_ESTUDIANTE(:periodo, :id_est, :usuario, @p_codigo, @p_mensaje)";
    $st = $pdo->prepare($sql);
    $st->bindValue(':periodo', $periodo);
    $st->bindValue(':id_est', $idEstudiante);
    $st->bindValue(':usuario', $usuario);
    $st->execute();
    // limpiar posibles resultsets del CALL
    while ($st->nextRowset()) { /* noop */ }
    $st->closeCursor();

    $out = $pdo->query('SELECT @p_codigo AS codigo, @p_mensaje AS mensaje')->fetch();
    $codigo = (int)($out['codigo'] ?? -1);
    $mensaje = (string)($out['mensaje'] ?? 'Sin mensaje del procedimiento');

    if ($codigo === 0) {
        $pdo->commit();
        auditar('CALCULAR_RIESGO_OK', [
            'periodo' => $periodo,
            'id_estudiante' => $idEstudiante,
            'mensaje' => $mensaje,
        ]);
        json_response([
            'ok' => true,
            'codigo' => $codigo,
            'mensaje' => $mensaje,
        ]);
    }

    $pdo->rollBack();
    auditar('CALCULAR_RIESGO_ERROR', [
        'periodo' => $periodo,
        'id_estudiante' => $idEstudiante,
        'codigo' => $codigo,
        'mensaje' => $mensaje,
    ]);
    json_response([
        'ok' => false,
        'codigo' => $codigo,
        'mensaje' => $mensaje,
    ], 422);
} catch (Throwable $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    auditar('CALCULAR_RIESGO_EXCEPTION', ['error' => $e->getMessage()]);
    json_response([
        'ok' => false,
        'mensaje' => 'Error al ejecutar el cálculo. Verifique que el procedimiento exista y que los nombres de columnas coincidan.',
        'detalle' => $e->getMessage(),
    ], 500);
}
