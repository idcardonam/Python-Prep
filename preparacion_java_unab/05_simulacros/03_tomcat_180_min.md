# Simulacro 3 · Aplicación web Java y Tomcat

Duración: 180 minutos. Sin Internet, IA ni soluciones.

## Contexto

Construye una aplicación web de incidencias TIC empaquetada como WAR.

## Modelo

Una incidencia tiene:

- id;
- título;
- descripción;
- correo;
- prioridad: `BAJA`, `MEDIA`, `ALTA`;
- estado: `ABIERTA`, `EN_PROGRESO`, `CERRADA`;
- fecha;
- versión.

## Parte A · Arquitectura (20 puntos)

Organiza:

```text
model/
dao/
service/
web/
filter/
WEB-INF/views/
```

Explica la responsabilidad de cada capa.

## Parte B · Casos de uso (30 puntos)

Implementa:

| Método | Ruta | Función |
|---|---|---|
| GET | `/incidencias` | listar |
| GET | `/incidencias/nueva` | formulario |
| POST | `/incidencias` | crear |
| GET | `/incidencias/ver?id=...` | detalle |
| POST | `/incidencias/estado` | cambiar estado |

Reglas:

- Título entre 5 y 120.
- Descripción entre 10 y 2000.
- Correo válido.
- Estado inicial `ABIERTA`.
- No pasar directamente de `ABIERTA` a `CERRADA`.
- Usar Post/Redirect/Get.

## Parte C · Persistencia (20 puntos)

- JDBC con `PreparedStatement`.
- Recursos cerrados.
- Filtro por estado y prioridad.
- Cambio de estado transaccional.
- Control optimista:

```sql
UPDATE incidencia
SET estado = ?, version = version + 1
WHERE id = ? AND version = ?;
```

Si actualiza cero filas, informa conflicto.

## Parte D · Seguridad (15 puntos)

- Escapar salida con `<c:out>`.
- Validar en servidor.
- Proteger POST con sesión y token CSRF.
- Cabecera `X-Content-Type-Options`.
- No mostrar SQL ni trazas.
- No registrar secretos.

## Parte E · Pruebas y despliegue (15 puntos)

Prueba:

- título corto;
- correo inválido;
- transición válida e inválida;
- entrada de inyección SQL;
- título con `<script>`;
- conflicto de versión.

Genera:

```bash
mvn clean test package
```

Explica:

- ubicación del WAR;
- cómo desplegar en Tomcat;
- diagnóstico de 404;
- diagnóstico de 500;
- diferencia entre `javax.servlet` y `jakarta.servlet`.

## Control de tiempo

- Minuto 0–20: modelo, rutas y capas.
- Minuto 20–60: base y DAO.
- Minuto 60–120: service, servlet y JSP.
- Minuto 120–145: seguridad.
- Minuto 145–165: pruebas.
- Minuto 165–180: empaquetar y explicar.

## Estrategia si no terminas

Prioriza:

1. proyecto que compile;
2. listar y crear;
3. validación en servidor;
4. `PreparedStatement`;
5. estructura por capas;
6. README con lo pendiente y cómo lo completarías.
