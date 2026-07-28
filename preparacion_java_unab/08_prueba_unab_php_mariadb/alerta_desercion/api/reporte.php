<?php
/**
 * API AJAX — Reporte + export CSV
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

$periodo = trim((string)($_GET['periodo'] ?? ''));
$programa = trim((string)($_GET['programa'] ?? ''));
$nivel = trim((string)($_GET['nivel_riesgo'] ?? ''));
$export = strtolower(trim((string)($_GET['export'] ?? '')));

$sql = "SELECT
            em.GWRPIEM_PERIODO AS periodo,
            em.GWRPIEM_CODIGO_ESTUDIANTE AS codigo,
            em.GWRPIEM_ID_ESTUDIANTE AS id_estudiante,
            em.GWRPIEM_NOMBRE_COMPLETO AS estudiante,
            em.GWRPIEM_PROGRAMA AS programa,
            em.GWRPIEM_NIVEL AS nivel,
            em.GWRPIEM_CAMPUS AS campus,
            rr.GWRPIRR_PUNTAJE_FINAL AS puntaje,
            COALESCE(rr.GWRPIRR_NIVEL_RIESGO, 'PENDIENTE') AS nivel_riesgo,
            rr.GWRPIRR_VARIABLES_RIESGO AS variables,
            rr.GWRPIRR_FECHA_CALCULO AS fecha_calculo,
            rr.GWRPIRR_USUARIO_CALCULO AS usuario_calculo
        FROM GWRPIEM em
        LEFT JOIN GWRPIRR rr
            ON rr.GWRPIRR_ID_ESTUDIANTE = em.GWRPIEM_ID_ESTUDIANTE
           AND rr.GWRPIRR_PERIODO = em.GWRPIEM_PERIODO
        WHERE em.GWRPIEM_MATRICULADO = 'Y'";

$params = [];

if ($periodo !== '') {
    $sql .= ' AND em.GWRPIEM_PERIODO = :periodo';
    $params[':periodo'] = $periodo;
}
if ($programa !== '') {
    $sql .= ' AND em.GWRPIEM_PROGRAMA = :programa';
    $params[':programa'] = $programa;
}
if ($nivel !== '') {
    if (strtoupper($nivel) === 'PENDIENTE') {
        $sql .= ' AND rr.GWRPIRR_ID IS NULL';
    } else {
        $sql .= ' AND rr.GWRPIRR_NIVEL_RIESGO = :nivel';
        $params[':nivel'] = strtoupper($nivel);
    }
}

$sql .= ' ORDER BY em.GWRPIEM_NOMBRE_COMPLETO ASC';

try {
    $st = $pdo->prepare($sql);
    $st->execute($params);
    $rows = $st->fetchAll();

    if ($export === 'csv') {
        $filename = 'reporte_riesgo_' . ($periodo !== '' ? $periodo : 'todos') . '_' . date('Ymd_His') . '.csv';
        header('Content-Type: text/csv; charset=UTF-8');
        header('Content-Disposition: attachment; filename="' . $filename . '"');
        header('Pragma: no-cache');
        header('Expires: 0');
        echo "\xEF\xBB\xBF"; // BOM Excel UTF-8
        $out = fopen('php://output', 'w');
        fputcsv($out, [
            'Periodo', 'Codigo', 'ID_Estudiante', 'Estudiante', 'Programa', 'Nivel_acad',
            'Campus', 'Puntaje', 'Nivel_riesgo', 'Vars_riesgo', 'Fecha_calculo', 'Usuario_calculo',
        ], ';');
        foreach ($rows as $r) {
            fputcsv($out, [
                $r['periodo'], $r['codigo'], $r['id_estudiante'], $r['estudiante'],
                $r['programa'], $r['nivel'], $r['campus'], $r['puntaje'],
                $r['nivel_riesgo'], $r['variables'], $r['fecha_calculo'], $r['usuario_calculo'],
            ], ';');
        }
        fclose($out);
        auditar('EXPORT_REPORTE_CSV', ['periodo' => $periodo, 'filas' => count($rows)]);
        exit;
    }

    $resumen = ['BAJO' => 0, 'MEDIO' => 0, 'ALTO' => 0, 'PENDIENTE' => 0, 'TOTAL' => count($rows)];
    foreach ($rows as $r) {
        $nr = strtoupper((string)($r['nivel_riesgo'] ?? 'PENDIENTE'));
        if (!isset($resumen[$nr])) {
            $resumen[$nr] = 0;
        }
        $resumen[$nr]++;
    }

    $prioritarios = array_values(array_filter($rows, static function (array $r): bool {
        return strtoupper((string)($r['nivel_riesgo'] ?? '')) === 'ALTO';
    }));
    usort($prioritarios, static function (array $a, array $b): int {
        return (float)($b['puntaje'] ?? 0) <=> (float)($a['puntaje'] ?? 0);
    });

    $periodos = $pdo->query("SELECT DISTINCT GWRPIEM_PERIODO AS v FROM GWRPIEM WHERE GWRPIEM_MATRICULADO='Y' ORDER BY 1")->fetchAll(PDO::FETCH_COLUMN);
    $programas = $pdo->query("SELECT DISTINCT GWRPIEM_PROGRAMA AS v FROM GWRPIEM WHERE GWRPIEM_MATRICULADO='Y' ORDER BY 1")->fetchAll(PDO::FETCH_COLUMN);

    json_response([
        'ok' => true,
        'data' => $rows,
        'resumen' => $resumen,
        'prioritarios' => array_slice($prioritarios, 0, 20),
        'meta' => [
            'matriculados_esperados' => 80,
            'cumple_meta_matriculados' => count($rows) === 80,
            'periodo_sugerido' => '202630',
            'clasificacion' => [
                'BAJO' => '0 a 29.99',
                'MEDIO' => '30 a 59.99',
                'ALTO' => '60 a 100',
                'PENDIENTE' => 'Sin fila en GWRPIRR',
            ],
        ],
        'filtros' => [
            'periodos' => $periodos,
            'programas' => $programas,
        ],
    ]);
} catch (Throwable $e) {
    json_response([
        'ok' => false,
        'mensaje' => 'No se pudo construir el reporte.',
        'detalle' => $e->getMessage(),
    ], 500);
}
