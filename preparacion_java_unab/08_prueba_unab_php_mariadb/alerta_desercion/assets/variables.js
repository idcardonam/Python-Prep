/* variables.js — CRUD GWRPIVR vía AJAX (UX amigable) */
(function ($) {
    'use strict';

    const modalEl = document.getElementById('modalVariable');
    const modal = new bootstrap.Modal(modalEl);
    let modo = 'crear';
    let tabla;

    const DT_ES = {
        search: 'Buscar en la lista:',
        searchPlaceholder: 'Escriba código, nombre o descripción…',
        lengthMenu: 'Mostrar _MENU_ variables por página',
        info: 'Mostrando _START_ a _END_ de _TOTAL_ variables',
        infoEmpty: 'No hay variables para mostrar',
        infoFiltered: '(filtrado de _MAX_ en total)',
        zeroRecords: 'No se encontró ninguna variable con ese texto. Pruebe otra palabra.',
        paginate: {
            previous: 'Anterior',
            next: 'Siguiente',
            first: 'Primera',
            last: 'Última'
        },
        emptyTable: 'Aún no hay variables registradas. Use “Agregar variable”.'
    };

    function showAlert(tipo, msg) {
        const box = $('#alertBox');
        box.removeClass('d-none alert-success alert-danger alert-warning alert-info')
            .addClass('alert-' + tipo)
            .text(msg);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showModalAlert(msg) {
        $('#modalAlert').removeClass('d-none').text(msg);
    }

    function clearModalErrors() {
        $('#modalAlert').addClass('d-none').text('');
        $('.field-error').removeClass('show').text('');
        $('#formVariable .is-invalid').removeClass('is-invalid');
    }

    function setFieldError(inputSel, errSel, msg) {
        $(inputSel).addClass('is-invalid');
        $(errSel).addClass('show').text(msg);
    }

    function badgeActivo(v) {
        if (v === 'Y') {
            return '<span class="badge badge-activa">Activa <small>(Y)</small></span>';
        }
        return '<span class="badge badge-inactiva">Inactiva <small>(N)</small></span>';
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
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, 'Todas']],
            // Buscador arriba; cantidad / info / páginas abajo
            dom: "<'row'<'col-12'f>>" +
                 "<'row'<'col-12'tr>>" +
                 "<'vars-dt-bottom'<'dt-len'l><'dt-info'i><'dt-pag'p>>",
            language: DT_ES,
            order: [[0, 'asc']],
            columns: [
                { data: 'id' },
                { data: 'codigo' },
                { data: 'nombre' },
                {
                    data: 'descripcion',
                    render: function (v) {
                        if (!v) return '<span class="text-muted">—</span>';
                        const t = String(v);
                        return t.length > 80 ? t.substring(0, 80) + '…' : t;
                    }
                },
                { data: 'peso' },
                { data: 'activo', render: badgeActivo },
                { data: 'user_ins', defaultContent: '—' },
                { data: 'date_ins', defaultContent: '—' },
                { data: 'user_upd', defaultContent: '—' },
                { data: 'date_upd', defaultContent: '—' },
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-nowrap',
                    render: function (row) {
                        const btnEdit =
                            `<button type="button" class="btn btn-sm btn-outline-primary btn-edit" data-id="${row.id}">Editar</button>`;
                        const btnToggle = row.activo === 'Y'
                            ? `<button type="button" class="btn btn-sm btn-outline-warning btn-toggle" data-id="${row.id}" data-activo="N">Inactivar</button>`
                            : `<button type="button" class="btn btn-sm btn-outline-success btn-toggle" data-id="${row.id}" data-activo="Y">Reactivar</button>`;
                        return `<div class="acciones-cell">${btnEdit}${btnToggle}</div>`;
                    }
                }
            ]
        });

        // Placeholder amigable (DataTables a veces no aplica searchPlaceholder solo)
        const $input = $('#tablaVariables_filter input');
        $input.attr('placeholder', DT_ES.searchPlaceholder);
        $input.attr('aria-label', 'Buscar variables por código, nombre o descripción');
    }

    function abrirCrear() {
        modo = 'crear';
        clearModalErrors();
        $('#modalTitulo').text('Nueva variable');
        $('#formVariable')[0].reset();
        $('#varId').val('');
        $('#wrapCodigo').show();
        $('#varCodigo').prop('disabled', false).prop('readonly', false);
        $('#varActivo').val('Y');
        modal.show();
        setTimeout(function () { $('#varCodigo').trigger('focus'); }, 300);
    }

    function abrirEditar(id) {
        clearModalErrors();
        $.getJSON('api/variables.php', { accion: 'obtener', id: id }).done(function (resp) {
            if (!resp.ok) {
                showAlert('danger', resp.mensaje);
                return;
            }
            const d = resp.data;
            modo = 'editar';
            $('#modalTitulo').text('Editar variable');
            $('#varId').val(d.id);
            $('#varCodigo').val(d.codigo);
            $('#wrapCodigo').hide();
            $('#varNombre').val(d.nombre);
            $('#varDescripcion').val(d.descripcion);
            $('#varPeso').val(d.peso);
            $('#varActivo').val(d.activo);
            modal.show();
            setTimeout(function () { $('#varNombre').trigger('focus'); }, 300);
        });
    }

    function validarFormularioCliente() {
        clearModalErrors();
        let ok = true;

        if (modo === 'crear') {
            const codigoRaw = ($('#varCodigo').val() || '');
            const codigo = codigoRaw.toUpperCase().trim();

            if (!codigo) {
                setFieldError('#varCodigo', '#errCodigo', 'Debe escribir un código. Ejemplo: BAJO_RENDIMIENTO');
                ok = false;
            } else if (/\s/.test(codigoRaw)) {
                setFieldError(
                    '#varCodigo',
                    '#errCodigo',
                    'El código no puede tener espacios. Use guion bajo: ejemplo BAJO_RENDIMIENTO (no “BAJO RENDIMIENTO”).'
                );
                ok = false;
            } else if (!/^[A-Z0-9_\-]+$/.test(codigo)) {
                setFieldError(
                    '#varCodigo',
                    '#errCodigo',
                    'Solo se permiten letras, números, guion (-) y guion bajo (_).'
                );
                ok = false;
            }
            $('#varCodigo').val(codigo);
        }

        const nombre = ($('#varNombre').val() || '').trim();
        if (!nombre) {
            setFieldError('#varNombre', '#errNombre', 'Escriba un nombre claro para esta variable.');
            ok = false;
        }

        const pesoRaw = $('#varPeso').val();
        if (pesoRaw === '' || pesoRaw === null) {
            setFieldError('#varPeso', '#errPeso', 'Indique el peso (número entre 0 y 100).');
            ok = false;
        } else {
            const peso = Number(pesoRaw);
            if (Number.isNaN(peso) || peso < 0 || peso > 100) {
                setFieldError('#varPeso', '#errPeso', 'El peso debe ser un número entre 0 y 100.');
                ok = false;
            }
        }

        if (!ok) {
            showModalAlert('Revise los campos marcados en rojo. Corrija el mensaje bajo cada casilla y vuelva a guardar.');
        }
        return ok;
    }

    // Normaliza código mientras escribe (feedback inmediato si pega espacios)
    $('#varCodigo').on('input', function () {
        const raw = $(this).val() || '';
        if (/\s/.test(raw)) {
            setFieldError(
                '#varCodigo',
                '#errCodigo',
                'Quitó el espacio: el código no admite espacios. Use guion bajo _'
            );
            showModalAlert('El código no puede contener espacios. Reemplácelos por guion bajo (_).');
        } else {
            $('#errCodigo').removeClass('show').text('');
            $(this).removeClass('is-invalid');
            if (!$('#errNombre').hasClass('show') && !$('#errPeso').hasClass('show')) {
                $('#modalAlert').addClass('d-none').text('');
            }
        }
    });

    $('#btnNueva').on('click', abrirCrear);

    $('#tablaVariables').on('click', '.btn-edit', function () {
        abrirEditar($(this).data('id'));
    });

    $('#tablaVariables').on('click', '.btn-toggle', function () {
        const id = $(this).data('id');
        const activo = $(this).data('activo');
        const texto = activo === 'Y'
            ? '¿Reactivar esta variable? Volverá a usarse en el cálculo de riesgo.'
            : '¿Inactivar esta variable? No se borra: solo deja de usarse en el cálculo (baja lógica).';
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
        if (!validarFormularioCliente()) {
            return;
        }

        const payload = {
            accion: modo === 'crear' ? 'crear' : 'actualizar',
            id: $('#varId').val(),
            codigo: ($('#varCodigo').val() || '').toUpperCase().trim(),
            nombre: ($('#varNombre').val() || '').trim(),
            descripcion: $('#varDescripcion').val(),
            peso: $('#varPeso').val(),
            activo: $('#varActivo').val()
        };

        $('#btnGuardar').prop('disabled', true).text('Guardando…');

        $.post('api/variables.php', payload)
            .done(function (resp) {
                if (resp.ok) {
                    modal.hide();
                    showAlert('success', resp.mensaje);
                    cargar().then(initTabla);
                } else {
                    // Error de negocio: se muestra DENTRO del modal
                    showModalAlert(resp.mensaje || 'No fue posible guardar. Revise los datos.');
                    if (resp.campo === 'codigo' || /código|codigo|espacio/i.test(resp.mensaje || '')) {
                        setFieldError('#varCodigo', '#errCodigo', resp.mensaje);
                    }
                }
            })
            .fail(function (xhr) {
                const msg = (xhr.responseJSON && xhr.responseJSON.mensaje) || 'Error al guardar. Intente de nuevo.';
                showModalAlert(msg);
                if (/código|codigo|espacio/i.test(msg)) {
                    setFieldError('#varCodigo', '#errCodigo', msg);
                }
            })
            .always(function () {
                $('#btnGuardar').prop('disabled', false).text('Guardar variable');
            });
    });

    // Al cerrar el modal, limpia errores (evita “basura” visual)
    modalEl.addEventListener('hidden.bs.modal', function () {
        clearModalErrors();
        $('#formVariable')[0].reset();
    });

    cargar().then(initTabla);
})(jQuery);
