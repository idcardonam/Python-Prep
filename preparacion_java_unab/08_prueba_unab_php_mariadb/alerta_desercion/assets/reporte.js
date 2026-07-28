/* reporte.js */
(function ($) {
    'use strict';

    let tabla;

    function badgeNivel(nivel) {
        const n = (nivel || 'PENDIENTE').toUpperCase();
        const map = {
            BAJO: 'badge-bajo',
            MEDIO: 'badge-medio',
            ALTO: 'badge-alto',
            PENDIENTE: 'badge-pendiente'
        };
        const cls = map[n] || 'badge-pendiente';
        // Texto + clase: el color no es el único indicador
        return `<span class="badge badge-nivel ${cls}">${n}</span> <span class="visually-hidden">${n}</span>`;
    }

    function pintarResumen(r) {
        $('#rTotal').text(r.TOTAL || 0);
        $('#rBajo').text(r.BAJO || 0);
        $('#rMedio').text(r.MEDIO || 0);
        $('#rAlto').text(r.ALTO || 0);
        $('#rPend').text(r.PENDIENTE || 0);
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
                alert(resp.mensaje + (resp.detalle ? ('\n' + resp.detalle) : ''));
                return;
            }
            pintarResumen(resp.resumen || {});
            cargarFiltros(resp.filtros || {});
            const data = resp.data || [];
            if (tabla) {
                tabla.clear().rows.add(data).draw();
                return;
            }
            tabla = $('#tablaReporte').DataTable({
                data: data,
                pageLength: 10,
                order: [[2, 'asc']],
                columns: [
                    { data: 'periodo' },
                    { data: 'codigo' },
                    { data: 'estudiante' },
                    { data: 'programa' },
                    { data: 'nivel' },
                    { data: 'campus' },
                    {
                        data: 'puntaje',
                        render: function (v) { return v === null || v === undefined ? '-' : v; }
                    },
                    {
                        data: 'nivel_riesgo',
                        render: badgeNivel
                    },
                    { data: 'variables', defaultContent: '-' },
                    { data: 'fecha_calculo', defaultContent: '-' },
                    { data: 'usuario_calculo', defaultContent: '-' }
                ]
            });
        });
    }

    $('#btnFiltrar').on('click', cargar);
    cargar();
})(jQuery);
