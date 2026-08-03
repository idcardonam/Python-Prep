# Laboratorio 4 · Servlet, JSP y Tomcat

## Qué demuestra

- Aplicación web Java empaquetada como WAR.
- Arquitectura `web → service → model`.
- Manejo de GET y POST.
- Validación en servidor.
- Patrón Post/Redirect/Get.
- JSP bajo `WEB-INF`.
- Salida escapada con JSTL.
- Codificación UTF-8 y cabeceras de seguridad.

Esta versión usa almacenamiento en memoria para concentrarse en HTTP y Tomcat. El ejercicio consiste en sustituirlo después por el DAO JDBC del laboratorio anterior.

## Compatibilidad importante

| Servidor | Paquetes |
|---|---|
| Tomcat 9 | `javax.servlet.*` |
| Tomcat 10/11 | `jakarta.servlet.*` |

Este proyecto usa `jakarta.servlet` y está preparado para Tomcat 11.

No mezcles ambos espacios de nombres.

## Compilar

```bash
mvn clean test package
```

Resultado:

```text
target/incidentes.war
```

## Desplegar

1. Copia `target/incidentes.war` a `$CATALINA_HOME/webapps/`.
2. Inicia Tomcat:

   ```bash
   $CATALINA_HOME/bin/startup.sh
   ```

3. Abre:

   ```text
   http://localhost:8080/incidentes/incidencias
   ```

4. Revisa logs:

   ```bash
   tail -f $CATALINA_HOME/logs/catalina.out
   ```

## Flujo

```text
Navegador
   │ HTTP
   ▼
Utf8SecurityHeadersFilter
   ▼
IncidenciaServlet
   ▼
IncidenciaService
   ▼
Repositorio en memoria
```

## Ejercicios

1. Añade filtro por estado.
2. Añade página de detalle.
3. Implementa cambio `ABIERTA → EN_PROGRESO → CERRADA`.
4. Impide el cambio mediante GET; utiliza POST.
5. Añade token CSRF de sesión.
6. Sustituye la memoria por JDBC y `PreparedStatement`.
7. Añade página de error 404.
8. Añade autenticación de práctica con sesión.
9. Prueba un título:

   ```html
   <script>alert('xss')</script>
   ```

   Verifica que se muestre como texto y no se ejecute.
10. Explica cómo desplegarías una nueva versión con respaldo y reversión.

## Diagnóstico

### 404

- Confirma que el WAR fue desplegado.
- Revisa el contexto `/incidentes`.
- Revisa `@WebServlet("/incidencias")`.
- Busca errores durante el arranque.

### 500

- Lee la primera excepción y el primer `Caused by`.
- Revisa parámetros nulos y conversión de enums.
- No muestres la traza al usuario final.

### `ClassNotFoundException: jakarta.servlet...`

- Versión de Tomcat incompatible.
- Dependencia incorrecta.
- Mezcla entre `javax` y `jakarta`.

### Caracteres dañados

- Ejecutar `request.setCharacterEncoding("UTF-8")` antes de leer parámetros.
- Definir UTF-8 en respuesta y JSP.

### Conexiones agotadas

- Usar `try-with-resources`.
- No guardar una `Connection` como atributo de Servlet.
- Revisar transacciones abiertas y tamaño del pool.
