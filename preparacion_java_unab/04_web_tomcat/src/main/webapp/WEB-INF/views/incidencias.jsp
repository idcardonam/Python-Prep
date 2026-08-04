<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Incidencias TIC</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; color: #17212b; }
        main { max-width: 960px; margin: auto; }
        form { display: grid; gap: .7rem; padding: 1rem; background: #f4f7fa; }
        label { font-weight: bold; }
        input, textarea, select, button { padding: .6rem; font: inherit; }
        button { background: #17324d; color: white; border: 0; cursor: pointer; }
        .error { color: #a12626; font-size: .9rem; }
        table { width: 100%; border-collapse: collapse; margin-top: 2rem; }
        th, td { border: 1px solid #d9e1e8; padding: .6rem; text-align: left; }
        th { background: #17324d; color: white; }
    </style>
</head>
<body>
<main>
    <h1>Gestión de incidencias TIC</h1>

    <form method="post" action="${pageContext.request.contextPath}/incidencias">
        <label for="titulo">Título</label>
        <input id="titulo" name="titulo" maxlength="120"
               value="<c:out value='${titulo}'/>" required>
        <c:if test="${not empty errores.titulo}">
            <span class="error"><c:out value="${errores.titulo}"/></span>
        </c:if>

        <label for="descripcion">Descripción</label>
        <textarea id="descripcion" name="descripcion" maxlength="2000"
                  rows="4" required><c:out value="${descripcion}"/></textarea>
        <c:if test="${not empty errores.descripcion}">
            <span class="error"><c:out value="${errores.descripcion}"/></span>
        </c:if>

        <label for="correo">Correo</label>
        <input id="correo" name="correo" type="email"
               value="<c:out value='${correo}'/>" required>
        <c:if test="${not empty errores.correo}">
            <span class="error"><c:out value="${errores.correo}"/></span>
        </c:if>

        <label for="prioridad">Prioridad</label>
        <select id="prioridad" name="prioridad" required>
            <option value="">Seleccione</option>
            <c:forEach items="${prioridades}" var="prioridad">
                <option value="${prioridad}"
                    ${prioridadSeleccionada == prioridad.toString() ? 'selected' : ''}>
                    <c:out value="${prioridad}"/>
                </option>
            </c:forEach>
        </select>
        <c:if test="${not empty errores.prioridad}">
            <span class="error"><c:out value="${errores.prioridad}"/></span>
        </c:if>

        <button type="submit">Registrar incidencia</button>
    </form>

    <table>
        <thead>
        <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Correo</th>
            <th>Prioridad</th>
            <th>Estado</th>
        </tr>
        </thead>
        <tbody>
        <c:forEach items="${incidencias}" var="incidencia">
            <tr>
                <td><c:out value="${incidencia.id}"/></td>
                <td><c:out value="${incidencia.titulo}"/></td>
                <td><c:out value="${incidencia.correo}"/></td>
                <td><c:out value="${incidencia.prioridad}"/></td>
                <td><c:out value="${incidencia.estado}"/></td>
            </tr>
        </c:forEach>
        <c:if test="${empty incidencias}">
            <tr><td colspan="5">No hay incidencias registradas.</td></tr>
        </c:if>
        </tbody>
    </table>
</main>
</body>
</html>
