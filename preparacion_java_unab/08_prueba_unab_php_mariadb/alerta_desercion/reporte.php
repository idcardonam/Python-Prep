<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tablero de alerta temprana — Reporte UNAB</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid px-4">
        <a class="navbar-brand fw-semibold" href="index.php">Alerta Temprana UNAB</a>
        <div class="navbar-nav">
            <a class="nav-link" href="variables.php">Variables</a>
            <a class="nav-link" href="calculo.php">Cálculo</a>
            <a class="nav-link active" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container-fluid px-4 py-4">
    <!-- Encabezado institucional -->
    <div class="reporte-hero mb-4 p-4 rounded-3 text-white shadow-sm">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <p class="small mb-1 text-white-50">Permanencia estudiantil · referencia SPADIES / SNIES</p>
                <h1 class="h3 mb-2">Tablero de alerta temprana de deserción</h1>
                <p class="mb-0 small">
                    Consulta directa de estudiantes matriculados (<code class="text-white">GWRPIEM_MATRICULADO = 'Y'</code>)
                    con resultado consolidado (<code class="text-white">GWRPIRR</code>).
                    Si aún no hay cálculo, el nivel se muestra como <strong>PENDIENTE</strong> (no se oculta el caso).
                </p>
            </div>
            <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                <button type="button" class="btn btn-light btn-sm me-1" id="btnActualizar">Actualizar tablero</button>
                <button type="button" class="btn btn-warning btn-sm me-1" id="btnRecalc">Recalcular período</button>
                <button type="button" class="btn btn-outline-light btn-sm" id="btnImprimir">Imprimir / PDF</button>
            </div>
        </div>
    </div>

    <!-- Alerta operativa (se llena por JS) -->
    <div id="alertaOperativa" class="alert alert-danger d-none shadow-sm" role="alert"></div>
    <div id="alertaPendientes" class="alert alert-warning d-none shadow-sm" role="alert"></div>
    <div id="alertBox" class="alert d-none" role="alert"></div>

    <!-- KPIs -->
    <div class="row g-3 mb-3" id="panelResumen">
        <div class="col-6 col-md">
            <div class="card kpi-card shadow-sm h-100">
                <div class="card-body">
                    <div class="text-muted small">Matriculados (Y)</div>
                    <div class="fs-3 fw-bold" id="rTotal">0</div>
                    <div class="small text-muted" id="rTotalHint">Base del reporte</div>
                </div>
            </div>
        </div>
        <div class="col-6 col-md">
            <div class="card kpi-card shadow-sm h-100 border-success">
                <div class="card-body">
                    <div class="text-muted small">BAJO <span class="text-success">(0–29.99)</span></div>
                    <div class="fs-3 fw-bold text-success" id="rBajo">0</div>
                    <div class="small" id="pBajo">0%</div>
                </div>
            </div>
        </div>
        <div class="col-6 col-md">
            <div class="card kpi-card shadow-sm h-100 border-warning">
                <div class="card-body">
                    <div class="text-muted small">MEDIO <span class="text-warning">(30–59.99)</span></div>
                    <div class="fs-3 fw-bold text-warning" id="rMedio">0</div>
                    <div class="small" id="pMedio">0%</div>
                </div>
            </div>
        </div>
        <div class="col-6 col-md">
            <div class="card kpi-card shadow-sm h-100 border-danger">
                <div class="card-body">
                    <div class="text-muted small">ALTO <span class="text-danger">(60–100)</span></div>
                    <div class="fs-3 fw-bold text-danger" id="rAlto">0</div>
                    <div class="small" id="pAlto">0%</div>
                </div>
            </div>
        </div>
        <div class="col-6 col-md">
            <div class="card kpi-card shadow-sm h-100">
                <div class="card-body">
                    <div class="text-muted small">PENDIENTE de cálculo</div>
                    <div class="fs-3 fw-bold text-secondary" id="rPend">0</div>
                    <div class="small" id="pPend">0%</div>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-3 mb-3">
        <!-- Prioritarios ALTO -->
        <div class="col-lg-5">
            <div class="card shadow-sm h-100">
                <div class="card-header bg-white d-flex justify-content-between align-items-center">
                    <strong>Prioridad de acompañamiento (ALTO)</strong>
                    <span class="badge text-bg-danger" id="badgeAltoLista">0</span>
                </div>
                <div class="card-body p-0">
                    <div class="table-responsive" style="max-height: 260px;">
                        <table class="table table-sm table-hover mb-0" id="tablaPrioritarios">
                            <thead class="table-light">
                            <tr>
                                <th>Estudiante</th>
                                <th>Programa</th>
                                <th>Puntaje</th>
                                <th>Variables</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr><td colspan="4" class="text-muted text-center py-3">Sin estudiantes en nivel ALTO</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer small text-muted bg-white">
                    Idea operativa: estos casos deberían entrar primero a tutoría / bienestar / seguimiento académico.
                </div>
            </div>
        </div>

        <!-- Leyenda + filtros -->
        <div class="col-lg-7">
            <div class="card shadow-sm mb-3">
                <div class="card-body">
                    <div class="row g-2 align-items-end">
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
                        <div class="col-md-3 d-grid gap-1">
                            <button class="btn btn-primary" id="btnFiltrar">Aplicar filtros</button>
                            <button class="btn btn-outline-secondary btn-sm" id="btnLimpiar">Limpiar</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-body small">
                    <strong>Leyenda de clasificación (enunciado)</strong>
                    <ul class="mb-2 mt-2">
                        <li><span class="badge badge-nivel badge-bajo">BAJO</span> puntaje 0 a 29.99</li>
                        <li><span class="badge badge-nivel badge-medio">MEDIO</span> puntaje 30 a 59.99</li>
                        <li><span class="badge badge-nivel badge-alto">ALTO</span> puntaje 60 a 100</li>
                        <li><span class="badge badge-nivel badge-pendiente">PENDIENTE</span> matriculado sin fila en GWRPIRR</li>
                    </ul>
                    <p class="mb-0 text-muted">
                        El color <em>no</em> es el único indicador: cada nivel incluye texto explícito en la columna “Nivel riesgo”.
                        Tras un recálculo masivo esperado: <strong>80 estudiantes matriculados</strong>.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabla principal DataTables -->
    <div class="card shadow-sm">
        <div class="card-header bg-white d-flex flex-wrap justify-content-between align-items-center gap-2">
            <div>
                <strong>Detalle de estudiantes matriculados</strong>
                <div class="small text-muted">Búsqueda global, ordenamiento y paginación con DataTables</div>
            </div>
            <div class="btn-group btn-group-sm" role="group" aria-label="Atajos de nivel">
                <button type="button" class="btn btn-outline-danger" data-quick="ALTO">Ver ALTO</button>
                <button type="button" class="btn btn-outline-warning" data-quick="MEDIO">Ver MEDIO</button>
                <button type="button" class="btn btn-outline-success" data-quick="BAJO">Ver BAJO</button>
                <button type="button" class="btn btn-outline-secondary" data-quick="PENDIENTE">Ver PENDIENTE</button>
            </div>
        </div>
        <div class="card-body">
            <table id="tablaReporte" class="table table-striped table-hover w-100 align-middle">
                <thead>
                <tr>
                    <th>Período</th>
                    <th>Código</th>
                    <th>Estudiante</th>
                    <th>Programa</th>
                    <th>Nivel acad.</th>
                    <th>Campus</th>
                    <th>Puntaje</th>
                    <th>Nivel riesgo</th>
                    <th>Variables de riesgo</th>
                    <th>Fecha cálculo</th>
                    <th>Usuario cálculo</th>
                </tr>
                </thead>
            </table>
        </div>
    </div>
</main>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/dataTables.bootstrap5.min.js"></script>
<script src="assets/reporte.js"></script>
</body>
</html>
