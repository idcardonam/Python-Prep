# Simulacro 1 · Java + SQL

Duración: 90 minutos. Sin Internet, IA ni soluciones.

## Contexto

La universidad necesita analizar inscripciones de estudiantes a cursos.

## Parte A · Java (55 puntos)

Implementa:

```java
enum TipoEstudiante { GRADO, POSGRADO, INTERCAMBIO }
enum EstadoInscripcion { ACTIVA, CANCELADA, LISTA_ESPERA }
class Estudiante
class Curso
class Inscripcion
class GestorInscripciones
```

### Reglas

- `Estudiante`: id positivo, nombre, correo válido y tipo.
- `Curso`: código, nombre y cupo mayor que cero.
- `Inscripcion`: estudiante, curso, fecha y estado.
- No puede existir más de una inscripción `ACTIVA` para el mismo estudiante y curso.
- Los atributos deben ser privados.
- Usa constructores, getters, `toString()`, `equals()` y `hashCode()` donde corresponda.

### Métodos

```java
void agregar(Inscripcion inscripcion)
List<Inscripcion> activasPorCurso(String codigo)
Map<String, Long> contarActivasPorCurso()
Optional<Estudiante> buscarPorCorreo(String correo)
```

En `main`, crea tres estudiantes, dos cursos y cinco inscripciones. Demuestra el rechazo de un duplicado.

## Parte B · SQL (40 puntos)

Diseña:

```text
estudiante
curso
inscripcion
```

Incluye claves, foráneas, `NOT NULL`, `UNIQUE` y `CHECK`.

Escribe consultas para:

1. Cursos con cupos disponibles.
2. Total de inscripciones activas por curso, incluyendo cursos sin inscripciones.
3. Estudiantes sin inscripción activa.
4. Tres cursos con más inscripciones activas.
5. Cancelar las inscripciones de un estudiante dentro de una transacción.

## Parte C · Explicación (5 puntos)

En dos minutos explica:

- por qué usaste enums;
- qué protege la base de datos;
- una diferencia entre Oracle y PostgreSQL.

## Control de tiempo

- Minuto 0–10: modelo y reglas en papel.
- Minuto 10–50: Java.
- Minuto 50–80: SQL.
- Minuto 80–90: compilar, probar y explicar.

## Entrega

- Código que compile.
- Script SQL.
- Un archivo `NOTAS.txt` con decisiones y pendientes.
