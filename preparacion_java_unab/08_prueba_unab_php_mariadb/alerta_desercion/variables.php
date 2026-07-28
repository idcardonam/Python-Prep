<?php require_once __DIR__ . '/config/conexion.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Variables de riesgo — GWRPIVR</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.8/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href="assets/app.css" rel="stylesheet">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="index.php">Alerta Temprana UNAB</a>
        <div class="navbar-nav">
            <a class="nav-link active" href="variables.php">Variables</a>
            <a class="nav-link" href="calculo.php">Cálculo</a>
            <a class="nav-link" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
            <h1 class="h3 mb-1">Catálogo de variables de riesgo</h1>
            <p class="text-muted small mb-0">CRUD sobre <code>GWRPIVR</code>. Baja lógica (Y/N). Código único en mayúsculas sin espacios.</p>
        </div>
        <button class="btn btn-success" id="btnNueva">Nueva variable</button>
    </div>

    <div id="alertBox" class="alert d-none" role="alert"></div>

    <div class="card shadow-sm">
        <div class="card-body">
            <table id="tablaVariables" class="table table-striped table-hover w-100">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Descripción</th>
                    <th>Peso</th>
                    <th>Estado</th>
                    <th>User crea</th>
                    <th>Fecha crea</th>
                    <th>User mod</th>
                    <th>Fecha mod</th>
                    <th>Acciones</th>
                </tr>
                </thead>
            </table>
        </div>
    </div>
</main>

<!-- Modal crear/editar -->
<div class="modal fade" id="modalVariable" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <form class="modal-content" id="formVariable">
            <div class="modal-header">
                <h2 class="modal-title h5" id="modalTitulo">Nueva variable</h2>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <input type="hidden" name="id" id="varId">
                <div class="mb-3" id="wrapCodigo">
                    <label class="form-label">Código *</label>
                    <input type="text" class="form-control" name="codigo" id="varCodigo" maxlength="30" placeholder="Ej: ACADEMICO_BAJO">
                    <div class="form-text">Se normaliza a MAYÚSCULAS. Sin espacios.</div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Nombre *</label>
                    <input type="text" class="form-control" name="nombre" id="varNombre" required maxlength="120">
                </div>
                <div class="mb-3">
                    <label class="form-label">Descripción</label>
                    <textarea class="form-control" name="descripcion" id="varDescripcion" rows="3"></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label">Peso (0 a 100) *</label>
                    <input type="number" class="form-control" name="peso" id="varPeso" min="0" max="100" step="0.01" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Estado *</label>
                    <select class="form-select" name="activo" id="varActivo">
                        <option value="Y">Y — Activa</option>
                        <option value="N">N — Inactiva</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-primary">Guardar</button>
            </div>
        </form>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.13.8/js/dataTables.bootstrap5.min.js"></script>
<script src="assets/variables.js"></script>
</body>
</html>
