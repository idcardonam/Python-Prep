<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Alerta temprana de deserción — UNAB TIC</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body class="bg-light">
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
    <div class="p-4 mb-4 bg-white rounded shadow-sm border">
        <h1 class="h3">Sistema de alertas tempranas para riesgo de deserción estudiantil</h1>
        <p class="mb-2 text-secondary">
            Módulo operativo alineado a la lógica de prevención (referencia SPADIES/SNIES):
            administrar variables, calcular riesgo consolidado y priorizar acompañamiento.
        </p>
        <p class="mb-0 small text-muted">
            Enfoque de entrega: integridad de datos, auditoría de cambios y control transaccional.
            Base: <code>prueba_ing</code> · Stack: PHP + MariaDB + Bootstrap + jQuery + DataTables
        </p>
    </div>

    <div class="row g-3">
        <div class="col-md-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h2 class="h5">1. CRUD GWRPIVR</h2>
                    <p class="small">Administra el catálogo de variables de riesgo con validaciones, baja lógica y AJAX.</p>
                    <a class="btn btn-primary btn-sm" href="variables.php">Abrir módulo</a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h2 class="h5">2. Cálculo P_CALCULAR...</h2>
                    <p class="small">Ejecuta el procedimiento por estudiante o masivo (`%`) con commit/rollback en PHP.</p>
                    <a class="btn btn-primary btn-sm" href="calculo.php">Ejecutar cálculo</a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h2 class="h5">3. Reporte operativo</h2>
                    <p class="small">DataTables sobre matriculados (Y) + LEFT JOIN a resultados, con filtros y resumen.</p>
                    <a class="btn btn-primary btn-sm" href="reporte.php">Ver reporte</a>
                </div>
            </div>
        </div>
    </div>
</main>
</body>
</html>
