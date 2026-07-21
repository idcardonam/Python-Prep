# Instalación del entorno para practicar

Instala únicamente desde sitios oficiales. Este orden evita problemas con variables y versiones.

## 1. Git

Descarga:

https://git-scm.com/download/win

Durante la instalación puedes conservar las opciones predeterminadas.

Verifica en PowerShell:

```powershell
git --version
```

## 2. Java JDK 21

Descarga Eclipse Temurin JDK 21:

https://adoptium.net/temurin/releases/?version=21

Selecciona:

- Operating System: Windows
- Architecture: x64
- Package Type: JDK
- Installer: `.msi`

En el instalador activa:

- `Set JAVA_HOME variable`
- `Add to PATH`

Verifica:

```powershell
java -version
javac -version
echo $env:JAVA_HOME
```

Si ambos comandos muestran versión 21, continúa.

## 3. IntelliJ IDEA Community

Descarga:

https://www.jetbrains.com/idea/download/

Selecciona **Community Edition**, que es gratuita.

Al crear un proyecto:

1. `New Project`
2. `Java`
3. JDK: 21
4. Build system: Maven cuando corresponda

No dependas completamente del autocompletado. También practica compilando desde terminal.

## 4. Maven

Descarga el archivo binario `.zip`:

https://maven.apache.org/download.cgi

Pasos:

1. Descomprime en:

   ```text
   C:\herramientas\apache-maven
   ```

2. Crea variable:

   ```text
   MAVEN_HOME=C:\herramientas\apache-maven
   ```

3. Añade al `Path`:

   ```text
   %MAVEN_HOME%\bin
   ```

4. Cierra y abre PowerShell.

Verifica:

```powershell
mvn -version
```

Debe mostrar Maven y Java 21.

## 5. PostgreSQL 16

Descarga:

https://www.postgresql.org/download/windows/

Instala:

- PostgreSQL Server
- Command Line Tools
- pgAdmin

Durante la instalación:

- conserva el puerto `5432`;
- define una contraseña local que puedas recordar;
- no uses una contraseña real de trabajo.

Verifica:

```powershell
psql --version
```

Si PowerShell no encuentra `psql`, añade al `Path` una ruta parecida a:

```text
C:\Program Files\PostgreSQL\16\bin
```

## 6. DBeaver Community (recomendado)

Descarga:

https://dbeaver.io/download/

Sirve para consultar PostgreSQL y familiarizarte con una interfaz que también puede conectarse a Oracle.

Datos locales sugeridos:

```text
Host: localhost
Port: 5432
Database: unab_practica
User: unab_practica
Password: practica_local
```

## 7. Apache Tomcat 11

Descarga el archivo `.zip`:

https://tomcat.apache.org/download-11.cgi

Descomprime en:

```text
C:\herramientas\apache-tomcat-11
```

Crea:

```text
CATALINA_HOME=C:\herramientas\apache-tomcat-11
```

Iniciar:

```powershell
& "$env:CATALINA_HOME\bin\startup.bat"
```

Abrir:

```text
http://localhost:8080
```

Detener:

```powershell
& "$env:CATALINA_HOME\bin\shutdown.bat"
```

## 8. Postman (opcional)

Descarga:

https://www.postman.com/downloads/

Úsalo para practicar GET, POST, parámetros, cuerpos JSON y códigos HTTP.

También puedes usar `curl`; no es obligatorio instalar Postman.

## 9. Oracle

No instales Oracle Database local al comienzo: consume más recursos y puede distraerte.

Practica:

- SQL relacional en PostgreSQL.
- Diferencias de Oracle en `02_sql/03_oracle_equivalencias.sql`.
- Sintaxis Oracle en Oracle Live SQL:

  https://livesql.oracle.com/

Si después confirmas que la prueba exige una base Oracle local, se puede preparar Oracle Database Free y SQL Developer.

## 10. Descargar los materiales

Opción A, Git:

```powershell
git clone https://github.com/idcardonam/Python-Prep.git
cd Python-Prep
git switch cursor/cv-generator-35e8
cd preparacion_java_unab
```

Opción B:

1. Abre el repositorio en GitHub.
2. Selecciona la rama `cursor/cv-generator-35e8`.
3. Pulsa `Code`.
4. `Download ZIP`.
5. Descomprime.

## Verificación final

Ejecuta:

```powershell
git --version
java -version
javac -version
mvn -version
psql --version
```

Luego:

```powershell
cd preparacion_java_unab\04_web_tomcat
mvn clean test package
```

Debe generarse:

```text
target\incidentes.war
```

## No instales todavía

- Oracle Database completo.
- Docker.
- Spring Boot CLI.
- Plugins de IA.

Primero domina Java, SQL, JDBC, Maven y Tomcat. Spring Boot se añadirá después de entender esas bases.
