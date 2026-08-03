<?php
/**
 * Herramienta de inspección — ejecutar UNA vez en la VM
 * URL: http://localhost/alerta_desercion/herramientas/ver_estructura.php
 *
 * Copia el JSON/HTML resultante si necesitas ajustar nombres de columnas.
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/config/conexion.php';

$tablas = ['GWRPIEM', 'GWRPIVR', 'GWRPICE', 'GWRPIRR'];
$salida = [];

foreach ($tablas as $tabla) {
    try {
        $cols = $pdo->query("DESCRIBE `$tabla`")->fetchAll(PDO::FETCH_ASSOC);
        $sample = $pdo->query("SELECT * FROM `$tabla` LIMIT 2")->fetchAll(PDO::FETCH_ASSOC);
        $count = (int)$pdo->query("SELECT COUNT(*) FROM `$tabla`")->fetchColumn();
        $salida[$tabla] = [
            'total_filas' => $count,
            'columnas' => $cols,
            'muestra' => $sample,
        ];
    } catch (Throwable $e) {
        $salida[$tabla] = ['error' => $e->getMessage()];
    }
}

header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Inspección modelo prueba_ing</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="h3 mb-3">Inspección de estructura — prueba_ing</h1>
    <p class="text-muted">Úsala para validar columnas reales antes de entregar. No modifica datos.</p>
    <?php foreach ($salida as $tabla => $info): ?>
        <div class="card mb-4 shadow-sm">
            <div class="card-header fw-semibold"><?= htmlspecialchars($tabla) ?></div>
            <div class="card-body">
                <?php if (isset($info['error'])): ?>
                    <div class="alert alert-danger"><?= htmlspecialchars($info['error']) ?></div>
                <?php else: ?>
                    <p>Filas: <strong><?= (int)$info['total_filas'] ?></strong></p>
                    <pre class="bg-dark text-white p-3 rounded small"><?= htmlspecialchars(json_encode($info, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) ?></pre>
                <?php endif; ?>
            </div>
        </div>
    <?php endforeach; ?>
</div>
</body>
</html>
