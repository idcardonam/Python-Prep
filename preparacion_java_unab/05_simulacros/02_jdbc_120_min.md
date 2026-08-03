# Simulacro 2 · CRUD JDBC

Duración: 120 minutos. Sin Internet, IA ni soluciones.

## Contexto

Construye una aplicación Java de consola para préstamos de equipos.

```text
equipo:
  id, codigo, descripcion, disponible

prestamo:
  id, equipo_id, usuario, fecha_prestamo, fecha_devolucion
```

## Parte A · Base de datos (20 puntos)

1. Crea ambas tablas.
2. Añade claves, foráneas y restricciones.
3. Impide dos préstamos abiertos para el mismo equipo.
4. Inserta tres equipos.

## Parte B · Modelo y DAO (35 puntos)

Implementa:

```java
record Equipo(Long id, String codigo, String descripcion, boolean disponible)

interface EquipoDao {
    Equipo crear(Equipo equipo) throws SQLException;
    Optional<Equipo> buscarPorId(long id) throws SQLException;
    List<Equipo> listar() throws SQLException;
    boolean actualizar(Equipo equipo) throws SQLException;
}
```

Reglas:

- Configuración por variables de entorno.
- `PreparedStatement`.
- `try-with-resources`.
- Recuperar id generado.
- Comprobar filas afectadas.

## Parte C · Transacción (35 puntos)

Implementa:

```java
Prestamo prestar(long equipoId, String usuario)
void devolver(long prestamoId)
```

`prestar` debe:

1. iniciar transacción;
2. bloquear el equipo con `FOR UPDATE`;
3. comprobar disponibilidad;
4. insertar préstamo;
5. marcar equipo no disponible;
6. ejecutar `commit`;
7. ejecutar `rollback` si falla.

`devolver` debe actualizar préstamo y equipo en la misma transacción.

## Parte D · Pruebas y explicación (10 puntos)

Demuestra:

- alta y consulta;
- rechazo de préstamo duplicado;
- rollback;
- devolución;
- una entrada como `' OR '1'='1`.

Explica por qué el servicio debe compartir la misma conexión entre los DAO que participan en la transacción.

## Control de tiempo

- Minuto 0–15: esquema.
- Minuto 15–35: modelo y configuración.
- Minuto 35–70: CRUD.
- Minuto 70–105: transacción.
- Minuto 105–120: pruebas y explicación.

## Penalizaciones importantes

- SQL concatenado con entradas: -20.
- Sin rollback: -15.
- Recursos no cerrados: -10.
- Contraseña en código: -10.
