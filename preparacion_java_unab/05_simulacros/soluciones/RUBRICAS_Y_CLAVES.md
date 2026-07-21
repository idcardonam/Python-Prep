# Rúbricas y claves

Abre este archivo únicamente después de terminar cada simulacro.

## Simulacro 1

| Área | Puntos |
|---|---:|
| Modelo POO y encapsulación | 15 |
| Validaciones, enums, equals/hashCode | 15 |
| Colecciones y métodos | 20 |
| Demostración y manejo de error | 5 |
| DDL y restricciones | 15 |
| Consultas SQL | 25 |
| Explicación | 5 |

Claves:

- Cadenas con `equals`, no `==`.
- Lista interna protegida mediante copia.
- `LEFT JOIN` para incluir cursos sin inscripciones.
- `NOT EXISTS` para estudiantes sin inscripción activa.
- En PostgreSQL puede usarse índice único parcial para una inscripción activa.
- Oracle puede requerir índice basado en función o lógica transaccional.

## Simulacro 2

| Área | Puntos |
|---|---:|
| Esquema e integridad | 20 |
| Configuración y recursos | 15 |
| CRUD parametrizado | 25 |
| Transacción de préstamo | 20 |
| Transacción de devolución | 10 |
| Pruebas y explicación | 10 |

Claves:

- `SELECT ... FOR UPDATE` evita que dos operaciones presten el mismo equipo.
- Todos los pasos usan la misma conexión.
- `autoCommit` se desactiva, se hace `commit` o `rollback` y se restaura.
- El DAO no debe cerrar una conexión entregada por el servicio.
- La base también debe proteger la unicidad de préstamo abierto.

Esqueleto transaccional:

```java
try (Connection connection = factory.abrir()) {
    boolean original = connection.getAutoCommit();
    try {
        connection.setAutoCommit(false);
        // leer y bloquear
        // validar
        // insertar
        // actualizar
        connection.commit();
    } catch (Exception error) {
        connection.rollback();
        throw error;
    } finally {
        connection.setAutoCommit(original);
    }
}
```

## Simulacro 3

| Área | Puntos |
|---|---:|
| Maven, WAR y capas | 20 |
| Casos de uso y HTTP | 25 |
| JDBC y transacción | 20 |
| Validación y PRG | 10 |
| Seguridad | 15 |
| Pruebas y diagnóstico | 10 |

Claves:

- Tomcat 9 usa `javax`; Tomcat 10/11 usa `jakarta`.
- Servlet lee HTTP y delega; no contiene SQL.
- Service aplica reglas y transacciones.
- DAO contiene SQL parametrizado.
- JSP presenta y escapa con JSTL; no contiene scriptlets.
- POST correcto termina en redirect.
- POST inválido hace forward conservando errores.
- La versión evita sobrescribir cambios concurrentes.

## Interpretación

| Puntaje | Lectura |
|---|---|
| Menos de 50 | Repetir fundamentos |
| 50–64 | Base parcial con riesgos |
| 65–79 | Nivel funcional supervisado |
| 80–89 | Buen nivel práctico |
| 90–100 | Solución sólida y explicable |

No consideres superado un simulacro si seguridad, SQL/JDBC o transacciones están por debajo del 50 %, aunque el total sea alto.
