<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cálculo de riesgo — UNAB</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark navbar-unab">
    <div class="container">
        <a class="navbar-brand navbar-brand-wrap" href="index.php">
            <img class="logo-unab" src="assets/img/logo-unab.svg" alt="UNAB"
                 onerror="this.onerror=null;this.src='assets/img/logo-unab.png';">
            <span>Alerta Temprana UNAB</span>
        </a>
        <div class="navbar-nav ms-auto">
            <a class="nav-link" href="variables.php">Variables</a>
            <a class="nav-link active" href="calculo.php">Cálculo</a>
            <a class="nav-link" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <h1 class="h3 page-vars-title">Ejecutar cálculo de riesgo</h1>
    <p class="text-muted">
        Invoca <code>P_CALCULAR_RIESGO_ESTUDIANTE</code>.
        La transacción se confirma en PHP solo si <code>P_CODIGO = 0</code>.
    </p>

    <div id="alertBox" class="alert d-none" role="alert"></div>

    <div class="row g-3">
        <div class="col-md-6">
            <div class="card shadow-sm h-100 card-vars">
                <div class="card-body">
                    <h2 class="h5">Calcular un estudiante</h2>
                    <div class="mb-3">
                        <label class="form-label" for="periodoUno">Período</label>
                        <input type="text" class="form-control" id="periodoUno" value="<?= e(periodo_default()) ?>" maxlength="6">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="idEstudiante">ID estudiante</label>
                        <input type="text" class="form-control" id="idEstudiante" placeholder="Ej: U0000001" maxlength="20">
                    </div>
                    <button type="button" class="btn btn-unab" id="btnUno">Calcular estudiante</button>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card shadow-sm h-100 card-vars">
                <div class="card-body">
                    <h2 class="h5">Recalcular todo el período</h2>
                    <div class="mb-3">
                        <label class="form-label" for="periodoTodos">Período</label>
                        <input type="text" class="form-control" id="periodoTodos" value="<?= e(periodo_default()) ?>" maxlength="6">
                    </div>
                    <p class="small text-muted">
                        Procesa uno a uno los matriculados (<code>MATRICULADO = 'Y'</code>)
                        y muestra el avance en la barra de progreso.
                    </p>
                    <button type="button" class="btn btn-unab-gold" id="btnTodos">Recalcular período</button>

                    <div class="progress-panel" id="panelProgreso" aria-live="polite">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <strong id="progresoTitulo">Procesando estudiantes…</strong>
                            <span id="progresoPct">0%</span>
                        </div>
                        <div class="progress progress-unab">
                            <div class="progress-bar progress-bar-striped progress-bar-animated"
                                 id="barraProgreso" role="progressbar"
                                 style="width:0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">0%</div>
                        </div>
                        <div class="progress-meta">
                            <span id="progresoDetalle">0 / 0</span>
                            <span id="progresoActual">—</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="alert alert-info mt-4">
        <strong>Nota operativa:</strong> si cambia pesos en GWRPIVR, debe volver a ejecutar este cálculo;
        GWRPIRR no se actualiza solo.
    </div>
</main>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="assets/calculo.js"></script>
</body>
</html>
