/* reporte.js — Tablero operativo de alerta temprana */
(function ($) {
    'use strict';

    let tabla;
    let ultimoData = [];

    function pct(parte, total) {
        if (!total) return '0%';
        return ((parte * 100) / total).toFixed(1) + '%';
    }

    function badgeNivel(nivel) {
        const n = (nivel || 'PENDIENTE').toUpperCase();
        const map = {
            BAJO: 'badge-bajo',
            MEDIO: 'badge-medio',
            ALTO: 'badge-alto',
            PENDIENTE: 'badge-pendiente'
        };
        const cls = map[n] || 'badge-pendiente';
        // Texto visible + etiqueta accesible (color no es el único indicador)
        return `<span class="badge badge-nivel ${cls}" title="Nivel ${n}">${n}</span>`;
    }

    function ordenRiesgo(nivel) {
        const n = (nivel || 'PENDIENTE').toUpperCase();
        if (n === 'ALTO') return 1;
        if (n === 'MEDIO') return 2;
        if (n === 'BAJO') return 3;
        return 4; // PENDIENTE al final o según necesidad operativa
    }

    function alertar(tipo, msg) {
        $('#alertBox').removeClass('d-none alert-success alert-danger alert-warning alert-info')
            .addClass('alert-' + tipo).text(msg);
    }

    function pintarResumen(r) {
        const total = r.TOTAL || 0;
        $('#rTotal').text(total);
        $('#rBajo').text(r.BAJO || 0);
        $('#rMedio').text(r.MEDIO || 0);
        $('#rAlto').text(r.ALTO || 0);
        $('#rPend').text(r.PENDIENTE || 0);
        $('#pBajo').text(pct(r.BAJO || 0, total));
        $('#pMedio').text(pct(r.MEDIO || 0, total));
        $('#pAlto').text(pct(r.ALTO || 0, total));
        $('#pPend').text(pct(r.PENDIENTE || 0, total));
        $('#rTotalHint').text(total === 80 ? 'OK: 80 matriculados (meta del enunciado)' : 'Matriculados visibles con filtros actuales');

        // Alertas operativas
        const $a = $('#alertaOperativa');
        const $p = $('#alertaPendientes');
        if ((r.ALTO || 0) > 0) {
            $a.removeClass('d-none').html(
                `<strong>Atención:</strong> hay <strong>${r.ALTO}</strong> estudiante(s) en nivel <strong>ALTO</strong>. ` +
                `Priorice acompañamiento académico/bienestar y revise las variables disparadoras.`
            );
        } else {
            $a.addClass('d-none').empty();
        }
        if ((r.PENDIENTE || 0) > 0) {
            $p.removeClass('d-none').html(
                `<strong>Cálculo incompleto:</strong> ${r.PENDIENTE} matriculado(s) aún en <strong>PENDIENTE</strong>. ` +
                `Use “Recalcular período” para alimentar <code>GWRPIRR</code>.`
            );
        } else {
            $p.addClass('d-none').empty();
        }
    }

    function pintarPrioritarios(data) {
        const altos = (data || [])
            .filter(function (r) { return (r.nivel_riesgo || '').toUpperCase() === 'ALTO'; })
            .sort(function (a, b) { return (parseFloat(b.puntaje) || 0) - (parseFloat(a.puntaje) || 0); });

        $('#badgeAltoLista').text(altos.length);
        const $tb = $('#tablaPrioritarios tbody');
        $tb.empty();
        if (!altos.length) {
            $tb.append('<tr><td colspan="4" class="text-muted text-center py-3">Sin estudiantes en nivel ALTO</td></tr>');
            return;
        }
        altos.slice(0, 15).forEach(function (r) {
            $tb.append(
                `<tr>
                    <td>${escapeHtml(r.estudiante || '')}<div class="small text-muted">${escapeHtml(r.codigo || '')}</div></td>
                    <td>${escapeHtml(r.programa || '')}</td>
                    <td><strong>${r.puntaje ?? '-'}</strong></td>
                    <td class="small">${escapeHtml(r.variables || '-')}</td>
                </tr>`
            );
        });
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function cargarFiltros(filtros) {
        const $p = $('#fPeriodo');
        const $pr = $('#fPrograma');
        const periodoActual = $p.val();
        const programaActual = $pr.val();
        $p.find('option:not([value=""])').remove();
        $pr.find('option:not([value=""])').remove();
        (filtros.periodos || []).forEach(function (v) {
            if (v) $p.append(`<option value="${v}">${v}</option>`);
        });
        (filtros.programas || []).forEach(function (v) {
            if (v) $pr.append(`<option value="${v}">${v}</option>`);
        });
        $p.val(periodoActual || '');
        $pr.val(programaActual || '');
    }

    function cargar() {
        const params = {
            periodo: $('#fPeriodo').val(),
            programa: $('#fPrograma').val(),
            nivel_riesgo: $('#fNivel').val()
        };
        return $.getJSON('api/reporte.php', params).then(function (resp) {
            if (!resp.ok) {
                alertar('danger', (resp.mensaje || 'Error') + (resp.detalle ? (' — ' + resp.detalle) : ''));
                return;
            }
            ultimoData = resp.data || [];
            pintarResumen(resp.resumen || {});
            pintarPrioritarios(ultimoData);
            cargarFiltros(resp.filtros || {});

            // Orden operativo: ALTO → MEDIO → BAJO → PENDIENTE, luego nombre
            const dataOrdenada = ultimoData.slice().sort(function (a, b) {
                const d = ordenRiesgo(a.nivel_riesgo) - ordenRiesgo(b.nivel_riesgo);
                if (d !== 0) return d;
                return String(a.estudiante || '').localeCompare(String(b.estudiante || ''), 'es');
            });

            if (tabla) {
                tabla.clear().rows.add(dataOrdenada).draw();
                return;
            }

            tabla = $('#tablaReporte').DataTable({
                data: dataOrdenada,
                pageLength: 10,
                lengthMenu: [10, 25, 50, 80, 100],
                order: [], // ya viene ordenado por prioridad
                columns: [
                    { data: 'periodo', defaultContent: '-' },
                    { data: 'codigo', defaultContent: '-' },
                    { data: 'estudiante', defaultContent: '-' },
                    { data: 'programa', defaultContent: '-' },
                    { data: 'nivel', defaultContent: '-' },
                    { data: 'campus', defaultContent: '-' },
                    {
                        data: 'puntaje',
                        render: function (v) { return (v === null || v === undefined || v === '') ? '-' : v; }
                    },
                    {
                        data: 'nivel_riesgo',
                        render: badgeNivel
                    },
                    {
                        data: 'variables',
                        defaultContent: '0',
                        render: function (v) {
                            // En el modelo real es cantidad (smallint), no lista de códigos
                            if (v === null || v === undefined || v === '') return '0';
                            return String(v);
                        }
                    },
                    { data: 'fecha_calculo', defaultContent: '-' },
                    { data: 'usuario_calculo', defaultContent: '-' }
                ],
                language: {
                    search: 'Buscar:',
                    lengthMenu: 'Mostrar _MENU_',
                    info: 'Mostrando _START_ a _END_ de _TOTAL_',
                    paginate: { previous: 'Anterior', next: 'Siguiente' },
                    zeroRecords: 'Sin registros con los filtros actuales'
                }
            });
        }).catch(function (xhr) {
            const msg = (xhr.responseJSON && (xhr.responseJSON.mensaje || xhr.responseJSON.detalle)) || 'No se pudo cargar el reporte';
            alertar('danger', msg);
        });
    }

    function recalcularPeriodo() {
        const periodo = $('#fPeriodo').val() || prompt('Período a recalcular (ej. 202601):', '');
        if (!periodo) return;
        if (!confirm('¿Recalcular TODOS los matriculados del período ' + periodo + '?')) return;

        $.post('api/calcular.php', {
            accion: 'calcular',
            periodo: periodo,
            id_estudiante: '%'
        }).done(function (resp) {
            alertar(resp.ok ? 'success' : 'danger', resp.mensaje || 'Sin mensaje');
            if (resp.ok) {
                $('#fPeriodo').val(periodo);
                cargar();
            }
        }).fail(function (xhr) {
            const msg = (xhr.responseJSON && (xhr.responseJSON.mensaje || xhr.responseJSON.detalle)) || 'Error al recalcular';
            alertar('danger', msg);
        });
    }

    $('#btnFiltrar').on('click', cargar);
    $('#btnActualizar').on('click', cargar);
    $('#btnLimpiar').on('click', function () {
        $('#fPeriodo').val('');
        $('#fPrograma').val('');
        $('#fNivel').val('');
        cargar();
    });
    $('#btnRecalc').on('click', recalcularPeriodo);
    $('#btnImprimir').on('click', function () { window.print(); });

    $('[data-quick]').on('click', function () {
        $('#fNivel').val($(this).data('quick'));
        cargar();
    });

    cargar();
})(jQuery);
