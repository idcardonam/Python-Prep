@echo off
chcp 65001 >nul
title Verificar entorno Java UNAB

echo ======================================================
echo   VERIFICACION DEL ENTORNO DE PRACTICA JAVA
echo ======================================================
echo.

where java >nul 2>nul
if errorlevel 1 (
    echo [FALTA] Java no esta instalado o no esta en PATH.
) else (
    echo [OK] Java encontrado.
    java -version
)

echo.
where javac >nul 2>nul
if errorlevel 1 (
    echo [FALTA] El compilador javac no esta disponible.
    echo         Debes instalar un JDK, no solamente un JRE.
) else (
    echo [OK] Compilador Java encontrado.
    javac -version
)

echo.
where git >nul 2>nul
if errorlevel 1 (
    echo [PENDIENTE] Git no esta instalado.
) else (
    echo [OK] Git encontrado.
    git --version
)

echo.
where mvn >nul 2>nul
if errorlevel 1 (
    echo [PENDIENTE] Maven no esta instalado.
    echo             No es necesario para el primer ejercicio.
) else (
    echo [OK] Maven encontrado.
    call mvn -version
)

echo.
where psql >nul 2>nul
if errorlevel 1 (
    echo [PENDIENTE] PostgreSQL no esta instalado.
    echo             No es necesario para el primer ejercicio.
) else (
    echo [OK] PostgreSQL encontrado.
    psql --version
)

echo.
echo ======================================================
echo Para iniciar solo necesitas [OK] en Java y javac.
echo Si faltan, abre 00_instalacion\INSTALACION_WINDOWS.md
echo ======================================================
echo.
pause
