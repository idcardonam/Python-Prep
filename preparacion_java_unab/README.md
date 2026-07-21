# Preparación práctica Java · UNAB

Ruta diseñada para practicar sin IA una prueba presencial con énfasis en:

- Java y programación orientada a objetos.
- SQL en PostgreSQL y diferencias esenciales con Oracle.
- JDBC, `PreparedStatement`, transacciones y manejo de recursos.
- Arquitectura de tres capas.
- JSP/Servlet y despliegue WAR en Tomcat.
- Pruebas, validación, seguridad y diagnóstico.

## Orden de trabajo

No abras las soluciones antes de terminar cada ejercicio.

1. `01_fundamentos/ENUNCIADOS.md`
2. `02_sql/README.md`
3. `03_jdbc/README.md`
4. `04_web_tomcat/README.md`
5. `05_simulacros/`
6. `entregables/Guia_Practica_Java_UNAB_Ivan_Cardona.pdf`

## Método de práctica sin IA

Para cada ejercicio:

1. Lee el enunciado una sola vez.
2. Escribe en papel entradas, salidas, reglas y errores posibles.
3. Programa sin copiar la solución.
4. Compila con frecuencia.
5. Cuando falle, lee el primer error y su línea antes de cambiar código.
6. Prueba casos válidos, inválidos y límites.
7. Explica en voz alta qué hiciste y por qué.
8. Solo entonces compara con `soluciones/`.

## Comandos esenciales

```bash
java -version
javac -version
mvn -version
psql --version
```

Compilar un archivo Java:

```bash
javac NombreArchivo.java
java NombreArchivo
```

Compilar un proyecto Maven:

```bash
mvn clean test
mvn clean package
```

## Configuración de PostgreSQL

```bash
sudo service postgresql start
sudo -u postgres psql
```

Dentro de `psql`:

```sql
CREATE USER unab_practica WITH PASSWORD 'practica_local';
CREATE DATABASE unab_practica OWNER unab_practica;
\q
```

Cargar el esquema:

```bash
PGPASSWORD=practica_local psql \
  -h localhost -U unab_practica -d unab_practica \
  -f 02_sql/01_esquema_postgresql.sql
```

Nunca reutilices esta contraseña en otro entorno. Es únicamente para práctica local.

## Variables para el laboratorio JDBC

```bash
export DB_URL='jdbc:postgresql://localhost:5432/unab_practica'
export DB_USER='unab_practica'
export DB_PASSWORD='practica_local'
```

## Qué debes poder hacer sin consultar

- Crear una clase con atributos privados, constructor, getters y validaciones.
- Explicar herencia, interfaz, encapsulación y polimorfismo.
- Usar `List`, `Map`, `Set`, `Optional` y excepciones.
- Escribir `SELECT`, `JOIN`, `GROUP BY`, subconsulta, `INSERT`, `UPDATE` y transacción.
- Evitar inyección SQL con `PreparedStatement`.
- Abrir y cerrar recursos con `try-with-resources`.
- Explicar `commit`, `rollback` y `autoCommit`.
- Separar Servlet, Service, DAO y base de datos.
- Empaquetar una aplicación como WAR y explicar su despliegue en Tomcat.
- Diagnosticar un 404, un 500 y un error JDBC leyendo logs.

## Regla para la prueba

Si no recuerdas una API exacta:

1. escribe primero la estructura y la intención;
2. resuelve la parte que sí conoces;
3. deja un comentario preciso en vez de inventar;
4. explica el riesgo y cómo lo validarías.

Una solución pequeña que compila, valida y está bien organizada vale más que una solución grande incompleta.
