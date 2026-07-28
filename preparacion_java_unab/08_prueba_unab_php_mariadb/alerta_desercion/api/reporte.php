<?php
/**
 * API AJAX — Reporte estudiantes matriculados + resultado de riesgo
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

$periodo = trim((string)($_GET['periodo'] ?? ''));
$programa = trim((string)($_GET['programa'] ?? ''));
$nivel = trim((string)($_GET['nivel_riesgo'] ?? ''));

$sql = "SELECT
            em.GWRPIEM_PERIODO AS periodo,
            em.GWRPIEM_ID AS codigo,
            em.GWRPIEM_NOMBRE AS estudiante,
            em.GWRPIEM_PROGRAMA AS programa,
            em.GWRPIEM_NIVEL AS nivel,
            em.GWRPIEM_CAMPUS AS campus,
            rr.GWRPIRR_PUNTAJE AS puntaje,
            COALESCE(rr.GWRPIRR_NIVEL_RIESGO, 'PENDIENTE') AS nivel_riesgo,
            rr.GWRPIRR_VARIABLES AS variables,
            rr.GWRPIRR_DATE_CALC AS fecha_calculo,
            rr.GWRPIRR_USER_CALC AS usuario_calculo
        FROM GWRPIEM em
        LEFT JOIN GWRPIRR rr
            ON rr.GWRPIRR_ID_ESTUDIANTE = em.GWRPIEM_ID
           AND (rr.GWRPIRR_PERIODO = em.GWRPIEM_PERIODO OR rr.GWRPIRR_PERIODO = :periodo_join OR :periodo_join = '')
        WHERE em.GWRPIEM_MATRICULADO = 'Y'";

$params = [':periodo_join' => $periodo];

if ($periodo !== '') {
    $sql .= ' AND em.GWRPIEM_PERIODO = :periodo';
    $params[':periodo'] = $periodo;
}
if ($programa !== '') {
    $sql .= ' AND em.GWRPIEM_PROGRAMA = :programa';
    $params[':programa'] = $programa;
}
if ($nivel !== '') {
    if ($nivel === 'PENDIENTE') {
        $sql .= ' AND rr.GWRPIRR_NIVEL_RIESGO IS NULL';
    } else {
        $sql .= ' AND rr.GWRPIRR_NIVEL_RIESGO = :nivel';
        $params[':nivel'] = $nivel;
    }
}

// Orden base en SQL: luego el frontend prioriza ALTO→MEDIO→BAJO→PENDIENTE
$sql .= ' ORDER BY em.GWRPIEM_NOMBRE ASC';

try {
    $st = $pdo->prepare($sql);
    $st->execute($params);
    $rows = $st->fetchAll();

    // Resumen KPI + porcentajes (valor agregado para decisión institucional)
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

    $periodos = $pdo->query("SELECT DISTINCT GWRPIEM_PERIODO AS v FROM GWRPIEM WHERE GWRPIEM_MATRICULADO='Y' AND GWRPIEM_PERIODO IS NOT NULL AND GWRPIEM_PERIODO <> '' ORDER BY 1")->fetchAll(PDO::FETCH_COLUMN);
    $programas = $pdo->query("SELECT DISTINCT GWRPIEM_PROGRAMA AS v FROM GWRPIEM WHERE GWRPIEM_MATRICULADO='Y' AND GWRPIEM_PROGRAMA IS NOT NULL AND GWRPIEM_PROGRAMA <> '' ORDER BY 1")->fetchAll(PDO::FETCH_COLUMN);

    json_response([
        'ok' => true,
        'data' => $rows,
        'resumen' => $resumen,
        'prioritarios' => array_slice($prioritarios, 0, 20),
        'meta' => [
            'matriculados_esperados' => 80,
            'cumple_meta_matriculados' => count($rows) === 80,
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
        'mensaje' => 'No se pudo construir el reporte. Verifique nombres de columnas con herramientas/ver_estructura.php',
        'detalle' => $e->getMessage(),
    ], 500);
}
