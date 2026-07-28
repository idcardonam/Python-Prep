<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Alerta Temprana UNAB — Permanencia estudiantil</title>
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
            <a class="nav-link" href="calculo.php">Cálculo</a>
            <a class="nav-link" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <section class="home-hero mb-4">
        <p class="small text-white-50 mb-2" style="position:relative;z-index:1">
            Universidad Autónoma de Bucaramanga · Permanencia estudiantil · referencia SPADIES / SNIES
        </p>
        <h1>Sistema de alerta temprana de deserción</h1>
        <p>
            Identifique variables de riesgo, calcule el puntaje consolidado de cada estudiante
            matriculado y priorice el acompañamiento académico y de bienestar.
            Periodo activo: <strong><?= e(periodo_default()) ?></strong>
            · Operador: <strong><?= e(app_user()) ?></strong>
        </p>
        <div class="home-cta d-flex flex-wrap gap-2 mt-3" style="position:relative;z-index:1">
            <a class="btn btn-unab-gold" href="variables.php">1. Variables de riesgo</a>
            <a class="btn btn-light" href="calculo.php">2. Calcular riesgo</a>
            <a class="btn btn-outline-light" href="reporte.php">3. Ver reporte</a>
        </div>
    </section>

    <div class="row g-3 mb-4">
        <div class="col-md-4">
            <div class="home-step">
                <div class="step-num">1</div>
                <h2 class="h5">Catálogo GWRPIVR</h2>
                <p class="small text-muted mb-3">
                    Cree, edite e inactive variables. Baja lógica (Y/N), código único y auditoría opcional.
                </p>
                <a href="variables.php" class="btn btn-sm btn-unab">Abrir variables</a>
            </div>
        </div>
        <div class="col-md-4">
            <div class="home-step">
                <div class="step-num">2</div>
                <h2 class="h5">Cálculo P_CALCULAR…</h2>
                <p class="small text-muted mb-3">
                    Ejecute el procedimiento por estudiante o por período, con transacción PHP
                    (commit solo si P_CODIGO = 0) y barra de progreso.
                </p>
                <a href="calculo.php" class="btn btn-sm btn-unab">Abrir cálculo</a>
            </div>
        </div>
        <div class="col-md-4">
            <div class="home-step">
                <div class="step-num">3</div>
                <h2 class="h5">Reporte operativo</h2>
                <p class="small text-muted mb-3">
                    Tablero BAJO / MEDIO / ALTO, detalle de variables aportantes y exportación CSV.
                </p>
                <a href="reporte.php" class="btn btn-sm btn-unab">Abrir reporte</a>
            </div>
        </div>
    </div>

    <div class="card card-vars shadow-sm">
        <div class="card-body">
            <h2 class="h6 text-uppercase text-muted mb-2" style="letter-spacing:.06em">Clasificación</h2>
            <div class="d-flex flex-wrap gap-3 small">
                <span><span class="badge text-bg-success">BAJO</span> 0 – 29.99</span>
                <span><span class="badge text-bg-warning text-dark">MEDIO</span> 30 – 59.99</span>
                <span><span class="badge text-bg-danger">ALTO</span> 60 – 100</span>
                <span><span class="badge text-bg-secondary">PENDIENTE</span> sin cálculo en GWRPIRR</span>
            </div>
            <hr>
            <p class="small text-muted mb-0">
                Base de datos <code>prueba_ing</code> · PHP + MariaDB + Bootstrap + jQuery + DataTables.
                Si cambia pesos en variables, vuelva a ejecutar el cálculo: GWRPIRR no se refresca solo.
            </p>
        </div>
    </div>
</main>
</body>
</html>
