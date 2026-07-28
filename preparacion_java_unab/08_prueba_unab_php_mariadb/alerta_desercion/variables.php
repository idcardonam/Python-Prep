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
<body>
<nav class="navbar navbar-expand-lg navbar-dark navbar-unab">
    <div class="container">
        <a class="navbar-brand navbar-brand-wrap" href="index.php">
            <img class="logo-unab" src="assets/img/logo-unab.svg" alt="UNAB"
                 onerror="this.onerror=null;this.src='assets/img/logo-unab.png';">
            <span>Alerta Temprana UNAB</span>
        </a>
        <div class="navbar-nav ms-auto">
            <a class="nav-link active" href="variables.php">Variables</a>
            <a class="nav-link" href="calculo.php">Cálculo</a>
            <a class="nav-link" href="reporte.php">Reporte</a>
        </div>
    </div>
</nav>

<main class="container py-4">
    <div class="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-3">
        <div>
            <h1 class="h3 page-vars-title mb-1">Catálogo de variables de riesgo</h1>
            <p class="text-muted small mb-0">
                Administra el catálogo <code>GWRPIVR</code>. La baja es lógica (Activa/Inactiva).
                El código debe ir en mayúsculas y <strong>sin espacios</strong>.
            </p>
        </div>
        <button type="button" class="btn btn-unab-gold" id="btnNueva">Agregar variable</button>
    </div>

    <div id="alertBox" class="alert d-none" role="alert"></div>

    <div class="card card-vars shadow-sm">
        <div class="card-body">
            <div class="vars-search-help">
                <strong>¿Cómo buscar?</strong>
                Escriba en el cuadro de búsqueda cualquier parte del
                <em>código</em>, <em>nombre</em> o <em>descripción</em>.
                Ejemplo: <code>INASISTENCIA</code> o <code>rendimiento</code>.
            </div>

            <div class="table-responsive">
                <table id="tablaVariables" class="table table-hover w-100 align-middle">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Código</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Peso</th>
                        <th>Estado</th>
                        <th>Creado por</th>
                        <th>Fecha creación</th>
                        <th>Modificado por</th>
                        <th>Fecha modificación</th>
                        <th>Acciones</th>
                    </tr>
                    </thead>
                </table>
            </div>
        </div>
    </div>
</main>

<!-- Modal crear/editar: solo título + cerrar en el encabezado -->
<div class="modal fade" id="modalVariable" tabindex="-1" aria-labelledby="modalTitulo" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <form class="modal-content" id="formVariable" novalidate>
            <div class="modal-header">
                <h2 class="modal-title h5 mb-0" id="modalTitulo">Nueva variable</h2>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
            </div>
            <div class="modal-body">
                <div id="modalAlert" class="alert alert-danger d-none" role="alert"></div>

                <input type="hidden" name="id" id="varId">

                <div class="mb-3" id="wrapCodigo">
                    <label class="form-label" for="varCodigo">Código *</label>
                    <input type="text" class="form-control" name="codigo" id="varCodigo"
                           maxlength="30" placeholder="Ejemplo: BAJO_RENDIMIENTO"
                           autocomplete="off">
                    <div class="form-text">
                        Use MAYÚSCULAS. Separar palabras con guion bajo (_).
                        <strong>No use espacios</strong>.
                    </div>
                    <div class="field-error" id="errCodigo"></div>
                </div>

                <div class="mb-3">
                    <label class="form-label" for="varNombre">Nombre *</label>
                    <input type="text" class="form-control" name="nombre" id="varNombre"
                           required maxlength="120" placeholder="Nombre claro para el equipo académico">
                    <div class="field-error" id="errNombre"></div>
                </div>

                <div class="mb-3">
                    <label class="form-label" for="varDescripcion">Descripción</label>
                    <textarea class="form-control" name="descripcion" id="varDescripcion" rows="3"
                              placeholder="Explique en qué casos aplica esta variable"></textarea>
                </div>

                <div class="mb-3">
                    <label class="form-label" for="varPeso">Peso (0 a 100) *</label>
                    <input type="number" class="form-control" name="peso" id="varPeso"
                           min="0" max="100" step="0.01" required placeholder="Ejemplo: 25">
                    <div class="form-text">Entre mayor el peso, más impacta el puntaje de riesgo.</div>
                    <div class="field-error" id="errPeso"></div>
                </div>

                <div class="mb-1">
                    <label class="form-label" for="varActivo">Estado *</label>
                    <select class="form-select" name="activo" id="varActivo">
                        <option value="Y">Activa (Y) — se usa en el cálculo</option>
                        <option value="N">Inactiva (N) — no se usa en el cálculo</option>
                    </select>
                </div>
            </div>
            <div class="modal-footer bg-light">
                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" class="btn btn-unab" id="btnGuardar">Guardar variable</button>
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
