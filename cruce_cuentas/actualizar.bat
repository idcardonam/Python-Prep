@echo off
chcp 65001 >nul 2>&1
title Actualizador Portal Gmail — UNAB TIC
color 1F
cls

echo ╔══════════════════════════════════════════════════════════════╗
echo ║     ACTUALIZADOR PORTAL — Depuracion Gmail + 2FA           ║
echo ║                                                            ║
echo ║  Genera los CSV de Power BI y el informe 2FA.              ║
echo ║  Al terminar, deja una carpeta en el ESCRITORIO            ║
echo ║  lista para arrastrar a SharePoint (etl / output).         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

where py >nul 2>&1 && (set "PY=py -3") || (
  where python3 >nul 2>&1 && (set "PY=python3") || (
    where python >nul 2>&1 && (set "PY=python") || (
      echo [ERROR] No se encontro Python instalado.
      echo Instale Python desde https://www.python.org/downloads/
      echo Marque la casilla "Add Python to PATH".
      pause
      exit /b 1
    )
  )
)

cd /d "%~dp0"
echo [OK] Carpeta del script: %CD%
echo.

echo Instalando dependencias si faltan...
%PY% -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo [ERROR] No se pudieron instalar dependencias.
    pause
    exit /b 1
)

echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo  INSTRUCCIONES:
echo.
echo  Ponga en UNA carpeta:
echo     - User_Download_*.csv     (Google Admin — TODAS las cuentas)
echo     - CSV de inscritos        (para el informe 2FA)
echo     - VISTA DE CURRICULO.xlsx (si la tiene)
echo.
echo  Copie la ruta desde la barra del Explorador y peguela abajo.
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
    pause
    exit /b 1
)

echo.
echo [OK] Carpeta de datos: %CARPETA%
echo.
echo [1/3] Procesando Power BI (cuentas, dependencias, capacidad)...
echo.

%PY% procesar_powerbi.py --carpeta "%CARPETA%" --salida .\salida
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Fallo el procesamiento Power BI.
    pause
    exit /b 1
)

echo.
echo [2/3] Procesando cruce 2FA (HTML y CSV por facultad)...
echo.

%PY% cruzar.py --carpeta "%CARPETA%" --salida .\salida
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Fallo el cruce 2FA.
    pause
    exit /b 1
)

echo.
echo [3/3] Empaquetando entrega en el Escritorio...
echo.

%PY% empaquetar_entrega.py --origen .\salida > "%TEMP%\portal_entrega.txt"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] No se pudo crear la carpeta del Escritorio.
    type "%TEMP%\portal_entrega.txt"
    pause
    exit /b 1
)
type "%TEMP%\portal_entrega.txt"
set /p DEST=<"%TEMP%\portal_entrega.txt"

echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo  [LISTO]
echo.
echo  En el ESCRITORIO hay una carpeta con 6 archivos:
echo     Archivos_SharePoint_AAAA-MM-DD
echo.
echo  Suba esos 6 a SharePoint: Documentos ^> etl ^> output
echo  (Reemplazar si pregunta). No suba los CSV por facultad.
echo.
echo  Power BI se actualiza SOLO cada hora (programado).
echo  Si necesita verlo YA: app.powerbi.com ^> Actualizar ahora.
echo.
echo  Las LISTAS (MetaProyecto, Acciones) NO se cambian con este
echo  script. Se editan en el portal SharePoint cuando cambie
echo  la meta o registre una accion.
echo.
echo ══════════════════════════════════════════════════════════════
echo.

start "" "%DEST%"
start "" "https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/Documentos%%20compartidos/Forms/AllItems.aspx?id=%%2Fsites%%2FProyectoDepuracinGmail%%2FDocumentos%%20compartidos%%2Fetl%%2Foutput"

echo Cuando haya subido los archivos, puede cerrar esta ventana.
pause
