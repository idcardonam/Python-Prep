package co.edu.unab.web;

import co.edu.unab.web.model.Prioridad;
import co.edu.unab.web.service.IncidenciaService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.Map;

@WebServlet("/incidencias")
public final class IncidenciaServlet extends HttpServlet {
    private final IncidenciaService service = new IncidenciaService();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        mostrarPagina(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String titulo = request.getParameter("titulo");
        String descripcion = request.getParameter("descripcion");
        String correo = request.getParameter("correo");
        String prioridad = request.getParameter("prioridad");

        Map<String, String> errores = service.validar(
                titulo,
                descripcion,
                correo,
                prioridad);

        if (!errores.isEmpty()) {
            request.setAttribute("errores", errores);
            request.setAttribute("titulo", titulo);
            request.setAttribute("descripcion", descripcion);
            request.setAttribute("correo", correo);
            request.setAttribute("prioridadSeleccionada", prioridad);
            mostrarPagina(request, response);
            return;
        }

        service.crear(
                titulo,
                descripcion,
                correo,
                Prioridad.valueOf(prioridad));

        // Post/Redirect/Get evita duplicar el registro al recargar.
        response.sendRedirect(request.getContextPath() + "/incidencias");
    }

    private void mostrarPagina(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setAttribute("incidencias", service.listar());
        request.setAttribute("prioridades", Prioridad.values());
        request.getRequestDispatcher("/WEB-INF/views/incidencias.jsp")
                .forward(request, response);
    }
}
