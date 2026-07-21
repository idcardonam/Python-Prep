# Laboratorio 3 · JDBC

## Objetivo

Conectar Java con PostgreSQL de forma segura y entender:

- `Connection`
- `PreparedStatement`
- `ResultSet`
- `try-with-resources`
- transacciones
- control optimista
- separación modelo / DAO / servicio

## Antes de ejecutar

Carga el esquema:

```bash
PGPASSWORD=practica_local psql \
  -h localhost -U unab_practica -d unab_practica \
  -f ../02_sql/01_esquema_postgresql.sql
```

Configura:

```bash
export DB_URL='jdbc:postgresql://localhost:5432/unab_practica'
export DB_USER='unab_practica'
export DB_PASSWORD='practica_local'
```

## Compilar y ejecutar

```bash
mvn clean test
mvn exec:java -Dexec.mainClass=co.edu.unab.practica.App
```

## Lee el proyecto en este orden

1. `model/Estado.java`
2. `model/Prioridad.java`
3. `model/Incidente.java`
4. `db/ConexionFactory.java`
5. `dao/IncidenteDao.java`
6. `dao/JdbcIncidenteDao.java`
7. `service/IncidenteService.java`
8. `App.java`

## Ejercicios

1. Añade `buscarPorPrioridad(Prioridad prioridad)`.
2. Añade filtro por texto en título usando `LOWER(titulo) LIKE LOWER(?)`.
3. Añade un método para asignar técnico y registrar historial en una transacción.
4. Provoca una excepción después del primer `UPDATE` y demuestra el `ROLLBACK`.
5. Intenta buscar con:

   ```text
   ' OR '1'='1
   ```

   Verifica que se trata como texto y no altera la consulta.
6. Cambia dos veces el mismo incidente usando una versión antigua y demuestra el conflicto optimista.
7. Registra tiempos de consulta sin imprimir URL completa, usuario ni contraseña.

## Preguntas de entrevista

- ¿Por qué no compartir una sola `Connection` global?
- ¿Por qué el servicio controla la transacción?
- ¿Por qué el DAO recibe la conexión durante una operación transaccional?
- ¿Qué ocurre si no se restaura `autoCommit`?
- ¿Por qué comprobar el número de filas de `executeUpdate()`?
- ¿Qué diferencia hay entre error funcional y `SQLException`?
