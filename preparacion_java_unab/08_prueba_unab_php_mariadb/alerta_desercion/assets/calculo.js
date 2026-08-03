/* calculo.js — individual + masivo con barra de progreso */
(function ($) {
    'use strict';

    function alertar(tipo, msg) {
        $('#alertBox')
            .removeClass('d-none alert-success alert-danger alert-warning alert-info')
            .addClass('alert-' + tipo)
            .text(msg);
    }

    function calcular(periodo, idEstudiante) {
        return $.post('api/calcular.php', {
            accion: 'calcular',
            periodo: periodo,
            id_estudiante: idEstudiante
        });
    }

    function setProgreso(hechos, total, nombre) {
        const pct = total ? Math.round((hechos * 100) / total) : 0;
        $('#panelProgreso').addClass('active');
        $('#barraProgreso')
            .css('width', pct + '%')
            .attr('aria-valuenow', pct)
            .text(pct + '%');
        $('#progresoPct').text(pct + '%');
        $('#progresoDetalle').text(hechos + ' / ' + total);
        $('#progresoActual').text(nombre || '—');
    }

    $('#btnUno').on('click', function () {
        const periodo = $('#periodoUno').val().trim();
        const id = $('#idEstudiante').val().trim();
        if (!id) {
            alertar('warning', 'Indique el ID del estudiante (ejemplo: U0000001).');
            return;
        }
        const $btn = $(this).prop('disabled', true).text('Calculando…');
        calcular(periodo, id).done(function (resp) {
            alertar(resp.ok ? 'success' : 'danger', resp.mensaje || 'Sin mensaje');
        }).fail(function (xhr) {
            const msg = (xhr.responseJSON && (xhr.responseJSON.mensaje || xhr.responseJSON.detalle)) || 'Error de cálculo';
            alertar('danger', msg);
        }).always(function () {
            $btn.prop('disabled', false).text('Calcular estudiante');
        });
    });

    $('#btnTodos').on('click', async function () {
        const periodo = $('#periodoTodos').val().trim();
        if (!periodo) {
            alertar('warning', 'Indique el período a recalcular.');
            return;
        }
        if (!confirm('¿Recalcular TODOS los estudiantes matriculados del período ' + periodo + '?\nSe mostrará una barra de progreso.')) {
            return;
        }

        const $btn = $(this).prop('disabled', true).text('Procesando…');
        $('#btnUno').prop('disabled', true);
        $('#barraProgreso').addClass('progress-bar-animated');
        $('#progresoTitulo').text('Preparando listado de matriculados…');
        setProgreso(0, 1, 'Consultando…');

        try {
            const respLista = await $.getJSON('api/calcular.php', {
                accion: 'listar_matriculados',
                periodo: periodo
            });
            if (!respLista.ok) {
                alertar('danger', respLista.mensaje || 'No se pudo listar matriculados');
                return;
            }
            const lista = respLista.data || [];
            if (!lista.length) {
                alertar('warning', 'No hay estudiantes matriculados (Y) en el período ' + periodo + '.');
                $('#panelProgreso').removeClass('active');
                return;
            }

            $('#progresoTitulo').text('Recalculando período ' + periodo);
            setProgreso(0, lista.length, 'Iniciando…');

            let ok = 0;
            let fail = 0;
            const errores = [];

            for (let i = 0; i < lista.length; i++) {
                const est = lista[i];
                const label = (est.codigo || est.id_estudiante) + ' · ' + (est.nombre || '');
                setProgreso(i, lista.length, label);
                try {
                    const resp = await calcular(periodo, est.id_estudiante);
                    if (resp && resp.ok) {
                        ok++;
                    } else {
                        fail++;
                        if (errores.length < 5) {
                            errores.push((est.id_estudiante || '') + ': ' + ((resp && resp.mensaje) || 'error'));
                        }
                    }
                } catch (e) {
                    fail++;
                    if (errores.length < 5) {
                        errores.push((est.id_estudiante || '') + ': error de red');
                    }
                }
                setProgreso(i + 1, lista.length, label);
            }

            $('#barraProgreso').removeClass('progress-bar-animated');
            $('#progresoTitulo').text('Cálculo masivo finalizado');

            let msg = 'Cálculo exitoso. Estudiantes procesados: ' + ok + ' de ' + lista.length + '.';
            if (fail) {
                msg = 'Proceso terminado con observaciones. OK: ' + ok + ' · Con error: ' + fail + '.';
                if (errores.length) {
                    msg += ' Ejemplos: ' + errores.join(' | ');
                }
                alertar(fail === lista.length ? 'danger' : 'warning', msg);
            } else {
                alertar('success', msg);
            }
        } catch (err) {
            alertar('danger', 'No se pudo completar el recálculo masivo.');
            $('#panelProgreso').removeClass('active');
        } finally {
            $btn.prop('disabled', false).text('Recalcular período');
            $('#btnUno').prop('disabled', false);
        }
    });
})(jQuery);
