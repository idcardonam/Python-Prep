/* variables.js — CRUD GWRPIVR vía AJAX */
(function ($) {
    'use strict';

    const modalEl = document.getElementById('modalVariable');
    const modal = new bootstrap.Modal(modalEl);
    let modo = 'crear';
    let tabla;

    function showAlert(tipo, msg) {
        const box = $('#alertBox');
        box.removeClass('d-none alert-success alert-danger alert-warning')
            .addClass('alert-' + tipo)
            .text(msg);
    }

    function badgeActivo(v) {
        if (v === 'Y') return '<span class="badge text-bg-success">Y — Activa</span>';
        return '<span class="badge text-bg-secondary">N — Inactiva</span>';
    }

    function cargar() {
        return $.getJSON('api/variables.php', { accion: 'listar' }).then(function (resp) {
            if (!resp.ok) {
                showAlert('danger', resp.mensaje || 'No se pudo listar');
                return [];
            }
            return resp.data || [];
        }).catch(function (xhr) {
            const msg = (xhr.responseJSON && xhr.responseJSON.detalle) ? xhr.responseJSON.detalle : 'Error de red/API';
            showAlert('danger', msg);
            return [];
        });
    }

    function initTabla(data) {
        if (tabla) {
            tabla.clear().rows.add(data).draw();
            return;
        }
        tabla = $('#tablaVariables').DataTable({
            data: data,
            pageLength: 10,
            columns: [
                { data: 'id' },
                { data: 'codigo' },
                { data: 'nombre' },
                { data: 'descripcion' },
                { data: 'peso' },
                {
                    data: 'activo',
                    render: badgeActivo
                },
                { data: 'user_ins' },
                { data: 'date_ins' },
                { data: 'user_upd' },
                { data: 'date_upd' },
                {
                    data: null,
                    orderable: false,
                    render: function (row) {
                        const btnEdit = `<button class="btn btn-sm btn-outline-primary btn-edit" data-id="${row.id}">Editar</button>`;
                        const btnToggle = row.activo === 'Y'
                            ? `<button class="btn btn-sm btn-outline-warning btn-toggle" data-id="${row.id}" data-activo="N">Inactivar</button>`
                            : `<button class="btn btn-sm btn-outline-success btn-toggle" data-id="${row.id}" data-activo="Y">Reactivar</button>`;
                        return btnEdit + ' ' + btnToggle;
                    }
                }
            ]
        });
    }

    function abrirCrear() {
        modo = 'crear';
        $('#modalTitulo').text('Nueva variable');
        $('#formVariable')[0].reset();
        $('#varId').val('');
        $('#wrapCodigo').show();
        $('#varCodigo').prop('disabled', false);
        modal.show();
    }

    function abrirEditar(id) {
        $.getJSON('api/variables.php', { accion: 'obtener', id: id }).done(function (resp) {
            if (!resp.ok) {
                showAlert('danger', resp.mensaje);
                return;
            }
            const d = resp.data;
            modo = 'editar';
            $('#modalTitulo').text('Editar variable #' + d.id);
            $('#varId').val(d.id);
            $('#varCodigo').val(d.codigo);
            $('#wrapCodigo').hide();
            $('#varNombre').val(d.nombre);
            $('#varDescripcion').val(d.descripcion);
            $('#varPeso').val(d.peso);
            $('#varActivo').val(d.activo);
            modal.show();
        });
    }

    $('#btnNueva').on('click', abrirCrear);

    $('#tablaVariables').on('click', '.btn-edit', function () {
        abrirEditar($(this).data('id'));
    });

    $('#tablaVariables').on('click', '.btn-toggle', function () {
        const id = $(this).data('id');
        const activo = $(this).data('activo');
        const texto = activo === 'Y' ? '¿Reactivar esta variable?' : '¿Inactivar esta variable? (baja lógica, no borra)';
        if (!confirm(texto)) return;

        $.post('api/variables.php', { accion: 'toggle_activo', id: id, activo: activo })
            .done(function (resp) {
                if (resp.ok) {
                    showAlert('success', resp.mensaje);
                    cargar().then(initTabla);
                } else {
                    showAlert('danger', resp.mensaje || 'No se pudo cambiar estado');
                }
            })
            .fail(function (xhr) {
                const msg = (xhr.responseJSON && xhr.responseJSON.mensaje) || 'Error al cambiar estado';
                showAlert('danger', msg);
            });
    });

    $('#formVariable').on('submit', function (e) {
        e.preventDefault();
        const payload = {
            accion: modo === 'crear' ? 'crear' : 'actualizar',
            id: $('#varId').val(),
            codigo: ($('#varCodigo').val() || '').toUpperCase().trim(),
            nombre: $('#varNombre').val(),
            descripcion: $('#varDescripcion').val(),
            peso: $('#varPeso').val(),
            activo: $('#varActivo').val()
        };

        $.post('api/variables.php', payload)
            .done(function (resp) {
                if (resp.ok) {
                    modal.hide();
                    showAlert('success', resp.mensaje);
                    cargar().then(initTabla);
                } else {
                    showAlert('warning', resp.mensaje || 'Validación');
                }
            })
            .fail(function (xhr) {
                const msg = (xhr.responseJSON && xhr.responseJSON.mensaje) || 'Error al guardar';
                showAlert('danger', msg);
            });
    });

    cargar().then(initTabla);
})(jQuery);
