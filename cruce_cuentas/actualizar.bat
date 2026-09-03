@echo off
chcp 65001 >nul 2>&1
title Actualizador Cruce 2FA — UNAB TIC
color 1F
cls

echo ╔══════════════════════════════════════════════════════════════╗
echo ║          ACTUALIZADOR CRUCE 2FA — UNAB TIC                 ║
echo ║                                                            ║
echo ║  Este script genera los informes HTML y CSV actualizados.  ║
echo ║  Al terminar, suba la carpeta "salida" a SharePoint.       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM ── Detectar Python ──
where py >nul 2>&1 && (set "PY=py -3") || (
  where python3 >nul 2>&1 && (set "PY=python3") || (
    where python >nul 2>&1 && (set "PY=python") || (
      echo [ERROR] No se encontro Python instalado.
      echo Instale Python desde https://www.python.org/downloads/
      echo Marque la casilla "Add Python to PATH" durante la instalacion.
      pause
      exit /b 1
    )
  )
)

REM ── Ubicar este script (cruce_cuentas/) ──
cd /d "%~dp0"
echo [OK] Carpeta del script: %CD%
echo.

REM ── Verificar dependencias ──
%PY% -c "import yaml" >nul 2>&1 || (
  echo Instalando dependencias...
  %PY% -m pip install -r requirements.txt --quiet
)

REM ── Preguntar ruta de datos ──
echo ══════════════════════════════════════════════════════════════
echo.
echo  INSTRUCCIONES:
echo.
echo  1. Abra el Explorador de Windows
echo  2. Navegue a la carpeta donde estan los archivos:
echo       - User_Download_*.csv  (Google Admin)
echo       - CSV de inscritos
echo       - VISTA DE CURRICULO.xlsx (si la tiene)
echo  3. Haga clic en la barra de direccion (arriba)
echo  4. Copie la ruta (Ctrl+C)
echo  5. Vuelva aqui y pegue la ruta (clic derecho o Ctrl+V)
echo.
echo ══════════════════════════════════════════════════════════════
echo.

if not "%~1"=="" (
    set "CARPETA=%~1"
    echo Usando carpeta recibida: %~1
) else (
    set /p "CARPETA=Pegue la ruta de la carpeta de datos: "
)

if not exist "%CARPETA%" (
    echo.
    echo [ERROR] La carpeta no existe: %CARPETA%
    echo Verifique la ruta y vuelva a intentar.
    pause
    exit /b 1
)

echo.
echo [OK] Carpeta de datos: %CARPETA%
echo.
echo Ejecutando cruce...
echo ──────────────────────────────────────────────────────────────
echo.

%PY% cruzar.py --carpeta "%CARPETA%" --salida .\salida

if %ERRORLEVEL% neq 0 (
    echo.
    echo ══════════════════════════════════════════════════════════════
    echo [ERROR] El cruce fallo. Revise los mensajes de arriba.
    echo ══════════════════════════════════════════════════════════════
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo  [LISTO] Informes generados en la carpeta "salida":
echo.
echo    salida\resumen.html           — Informe para jefatura
echo    salida\listado_sin_2fa.html   — Listado operativo
echo    salida\02_estudiantes_sin_2fa.csv
echo    salida\06_cobertura_2fa_facultad.csv
echo    (y otros archivos de detalle)
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo  SIGUIENTE PASO:
echo.
echo    1. Abra SharePoint:
echo       Documentos ^> etl ^> output
echo.
echo    2. Seleccione TODOS los archivos de la carpeta "salida"
echo       y arrastrelos a SharePoint (reemplazar si pregunta)
echo.
echo    3. Verifique en el portal que los datos estan actualizados
echo.
echo ══════════════════════════════════════════════════════════════
echo.

REM ── Abrir la carpeta de salida ──
start "" "%~dp0salida"

REM ── Abrir SharePoint ──
echo Presione cualquier tecla para abrir SharePoint...
pause >nul
start "" "https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/Documentos%%20compartidos/Forms/AllItems.aspx?id=%%2Fsites%%2FProyectoDepuracinGmail%%2FDocumentos%%20compartidos%%2Fetl%%2Foutput"

echo.
echo Cuando haya subido los archivos, puede cerrar esta ventana.
pause
