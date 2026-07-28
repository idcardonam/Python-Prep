<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Reporte de riesgo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="index.php">Alerta Temprana UNAB</a>
        <div class="navbar-nav">
            <a class="nav-link" href="variables.php">Variables</a>
            <a class="nav-link" href="calculo.php">Cálculo</a>
            <a class="nav-link active" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <h1 class="h3 mb-1">Reporte operativo de riesgo</h1>
    <p class="text-muted">Fuente: <code>GWRPIEM</code> (matriculado = Y) + <code>LEFT JOIN GWRPIRR</code>. Los pendientes aparecen como <strong>PENDIENTE</strong>.</p>

    <div class="row g-3 mb-3" id="panelResumen">
        <div class="col"><div class="card text-center shadow-sm"><div class="card-body"><div class="text-muted small">Total</div><div class="fs-4 fw-bold" id="rTotal">0</div></div></div></div>
        <div class="col"><div class="card text-center shadow-sm"><div class="card-body"><div class="text-muted small">BAJO</div><div class="fs-4 fw-bold text-success" id="rBajo">0</div></div></div></div>
        <div class="col"><div class="card text-center shadow-sm"><div class="card-body"><div class="text-muted small">MEDIO</div><div class="fs-4 fw-bold text-warning" id="rMedio">0</div></div></div></div>
        <div class="col"><div class="card text-center shadow-sm"><div class="card-body"><div class="text-muted small">ALTO</div><div class="fs-4 fw-bold text-danger" id="rAlto">0</div></div></div></div>
        <div class="col"><div class="card text-center shadow-sm"><div class="card-body"><div class="text-muted small">PENDIENTE</div><div class="fs-4 fw-bold text-secondary" id="rPend">0</div></div></div></div>
    </div>

    <div class="card shadow-sm mb-3">
        <div class="card-body row g-2 align-items-end">
            <div class="col-md-3">
                <label class="form-label">Período</label>
                <select id="fPeriodo" class="form-select"><option value="">Todos</option></select>
            </div>
            <div class="col-md-3">
                <label class="form-label">Programa</label>
                <select id="fPrograma" class="form-select"><option value="">Todos</option></select>
            </div>
            <div class="col-md-3">
                <label class="form-label">Nivel de riesgo</label>
                <select id="fNivel" class="form-select">
                    <option value="">Todos</option>
                    <option value="BAJO">BAJO</option>
                    <option value="MEDIO">MEDIO</option>
                    <option value="ALTO">ALTO</option>
                    <option value="PENDIENTE">PENDIENTE</option>
                </select>
            </div>
            <div class="col-md-3">
                <button class="btn btn-primary w-100" id="btnFiltrar">Aplicar filtros</button>
            </div>
        </div>
    </div>

    <div class="card shadow-sm">
        <div class="card-body">
            <table id="tablaReporte" class="table table-striped table-hover w-100">
                <thead>
                <tr>
                    <th>Período</th>
                    <th>Código</th>
                    <th>Estudiante</th>
                    <th>Programa</th>
                    <th>Nivel</th>
                    <th>Campus</th>
                    <th>Puntaje</th>
                    <th>Nivel riesgo</th>
                    <th>Variables</th>
                    <th>Fecha cálculo</th>
                    <th>Usuario cálculo</th>
                </tr>
                </thead>
            </table>
        </div>
    </div>
</main>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/dataTables.bootstrap5.min.js"></script>
<script src="assets/reporte.js"></script>
</body>
</html>
