<?php
/**
 * API — Detalle de variables que aportaron al puntaje de un estudiante
 * (GWRPICE + GWRPIVR) para el modal del reporte.
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

$periodo = trim((string)($_GET['periodo'] ?? ''));
$idEstudiante = trim((string)($_GET['id_estudiante'] ?? ''));

if ($periodo === '' || $idEstudiante === '') {
    json_response([
        'ok' => false,
        'mensaje' => 'Indique período e ID de estudiante.',
    ], 422);
}

try {
    $stEst = $pdo->prepare(
        "SELECT
            em.GWRPIEM_PERIODO AS periodo,
            em.GWRPIEM_ID_ESTUDIANTE AS id_estudiante,
            em.GWRPIEM_CODIGO_ESTUDIANTE AS codigo,
            em.GWRPIEM_NOMBRE_COMPLETO AS estudiante,
            em.GWRPIEM_PROGRAMA AS programa,
            em.GWRPIEM_NIVEL AS nivel,
            em.GWRPIEM_CAMPUS AS campus,
            rr.GWRPIRR_PUNTAJE_FINAL AS puntaje,
            COALESCE(rr.GWRPIRR_NIVEL_RIESGO, 'PENDIENTE') AS nivel_riesgo,
            rr.GWRPIRR_VARIABLES_RIESGO AS variables_count,
            rr.GWRPIRR_FECHA_CALCULO AS fecha_calculo,
            rr.GWRPIRR_USUARIO_CALCULO AS usuario_calculo
         FROM GWRPIEM em
         LEFT JOIN GWRPIRR rr
            ON rr.GWRPIRR_ID_ESTUDIANTE = em.GWRPIEM_ID_ESTUDIANTE
           AND rr.GWRPIRR_PERIODO = em.GWRPIEM_PERIODO
         WHERE em.GWRPIEM_PERIODO = ?
           AND em.GWRPIEM_ID_ESTUDIANTE = ?
         LIMIT 1"
    );
    $stEst->execute([$periodo, $idEstudiante]);
    $est = $stEst->fetch();
    if (!$est) {
        json_response(['ok' => false, 'mensaje' => 'Estudiante no encontrado en el período.'], 404);
    }

    // Variables que SÍ aportan al puntaje (misma regla del SP)
    $stVars = $pdo->prepare(
        "SELECT
            vr.GWRPIVR_CODIGO AS codigo,
            vr.GWRPIVR_NOMBRE AS nombre,
            vr.GWRPIVR_PESO AS peso,
            ce.GWRPICE_PRESENTA_RIESGO AS presenta_riesgo,
            ce.GWRPICE_OBSERVACION AS observacion,
            ce.GWRPICE_ACTIVO AS ce_activo,
            vr.GWRPIVR_ACTIVO AS vr_activo
         FROM GWRPICE ce
         INNER JOIN GWRPIVR vr ON vr.GWRPIVR_ID = ce.GWRPICE_ID_VARIABLE
         WHERE ce.GWRPICE_PERIODO = ?
           AND ce.GWRPICE_ID_ESTUDIANTE = ?
           AND ce.GWRPICE_PRESENTA_RIESGO = 'Y'
           AND ce.GWRPICE_ACTIVO = 'Y'
           AND vr.GWRPIVR_ACTIVO = 'Y'
         ORDER BY vr.GWRPIVR_PESO DESC, vr.GWRPIVR_CODIGO ASC"
    );
    $stVars->execute([$periodo, $idEstudiante]);
    $aportan = $stVars->fetchAll();

    $suma = 0.0;
    foreach ($aportan as $v) {
        $suma += (float)$v['peso'];
    }

    json_response([
        'ok' => true,
        'estudiante' => $est,
        'variables_aportan' => $aportan,
        'suma_pesos' => round($suma, 2),
        'puntaje_tope' => min(100, round($suma, 2)),
        'explicacion' => 'Se suman los pesos de variables con riesgo presente (Y), registro CE activo (Y) y variable activa (Y). El puntaje final no supera 100.',
    ]);
} catch (Throwable $e) {
    json_response([
        'ok' => false,
        'mensaje' => 'No se pudo cargar el detalle.',
        'detalle' => $e->getMessage(),
    ], 500);
}
