@echo off
chcp 65001 >nul
title Evaluador fundamentos Java
cd /d "%~dp0"

echo ======================================================
echo   COMPILANDO TU RESPUESTA
echo ======================================================
echo.

where javac >nul 2>nul
if errorlevel 1 (
    echo [FALTA] No se encontro javac.
    echo Instala JDK 21 siguiendo ..\00_instalacion\INSTALACION_WINDOWS.md
    echo.
    pause
    exit /b 1
)

if exist build rmdir /s /q build
mkdir build

javac -encoding UTF-8 -d build PracticaFundamentos.java EvaluadorFundamentos.java

if errorlevel 1 (
    echo.
    echo ======================================================
    echo [ERROR DE COMPILACION]
    echo Lee el primer error mostrado arriba.
    echo Revisa la linea indicada, guarda y vuelve a ejecutar.
    echo ======================================================
    echo.
    pause
    exit /b 1
)

echo [OK] Compilacion correcta.
echo.
java -cp build EvaluadorFundamentos

echo.
pause
