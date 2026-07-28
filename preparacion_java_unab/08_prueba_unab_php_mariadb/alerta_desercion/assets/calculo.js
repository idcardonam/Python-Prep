/* calculo.js */
(function ($) {
    'use strict';

    function alertar(tipo, msg) {
        $('#alertBox').removeClass('d-none alert-success alert-danger alert-warning')
            .addClass('alert-' + tipo).text(msg);
    }

    function calcular(periodo, idEstudiante) {
        return $.post('api/calcular.php', {
            accion: 'calcular',
            periodo: periodo,
            id_estudiante: idEstudiante
        });
    }

    $('#btnUno').on('click', function () {
        const periodo = $('#periodoUno').val().trim();
        const id = $('#idEstudiante').val().trim();
        if (!id) {
            alertar('warning', 'Indique el ID del estudiante');
            return;
        }
        calcular(periodo, id).done(function (resp) {
            alertar(resp.ok ? 'success' : 'danger', resp.mensaje || 'Sin mensaje');
        }).fail(function (xhr) {
            const msg = (xhr.responseJSON && (xhr.responseJSON.mensaje || xhr.responseJSON.detalle)) || 'Error de cálculo';
            alertar('danger', msg);
        });
    });

    $('#btnTodos').on('click', function () {
        if (!confirm('¿Recalcular TODOS los estudiantes matriculados del período?')) return;
        const periodo = $('#periodoTodos').val().trim();
        calcular(periodo, '%').done(function (resp) {
            alertar(resp.ok ? 'success' : 'danger', resp.mensaje || 'Sin mensaje');
        }).fail(function (xhr) {
            const msg = (xhr.responseJSON && (xhr.responseJSON.mensaje || xhr.responseJSON.detalle)) || 'Error de cálculo masivo';
            alertar('danger', msg);
        });
    });
})(jQuery);
