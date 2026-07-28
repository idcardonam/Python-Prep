<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cálculo de riesgo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="index.php">Alerta Temprana UNAB</a>
        <div class="navbar-nav">
            <a class="nav-link" href="variables.php">Variables</a>
            <a class="nav-link active" href="calculo.php">Cálculo</a>
            <a class="nav-link" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <h1 class="h3">Ejecutar cálculo de riesgo</h1>
    <p class="text-muted">Invoca <code>P_CALCULAR_RIESGO_ESTUDIANTE</code>. La transacción se confirma en PHP solo si <code>P_CODIGO = 0</code>.</p>

    <div id="alertBox" class="alert d-none" role="alert"></div>

    <div class="row g-3">
        <div class="col-md-6">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h2 class="h5">Calcular un estudiante</h2>
                    <div class="mb-3">
                        <label class="form-label">Período</label>
                        <input type="text" class="form-control" id="periodoUno" value="<?= e(periodo_default()) ?>" maxlength="6">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">ID estudiante</label>
                        <input type="text" class="form-control" id="idEstudiante" placeholder="Ej: 10001" maxlength="20">
                    </div>
                    <button class="btn btn-primary" id="btnUno">Calcular estudiante</button>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h2 class="h5">Recalcular todo el período</h2>
                    <div class="mb-3">
                        <label class="form-label">Período</label>
                        <input type="text" class="form-control" id="periodoTodos" value="<?= e(periodo_default()) ?>" maxlength="6">
                    </div>
                    <p class="small text-muted">Usa <code>P_ID_ESTUDIANTE = '%'</code> para procesar matriculados (Y).</p>
                    <button class="btn btn-warning" id="btnTodos">Recalcular período</button>
                </div>
            </div>
        </div>
    </div>

    <div class="alert alert-info mt-4">
        <strong>Nota operativa:</strong> si cambias pesos en GWRPIVR, debes volver a ejecutar este cálculo;
        GWRPIRR no se actualiza solo.
    </div>
</main>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="assets/calculo.js"></script>
</body>
</html>
