# -*- coding: utf-8 -*-
"""Copia a Escritorio/Archivos_SharePoint_AAAA-MM-DD solo lo que se sube a etl/output."""
from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Solo estos nombres van a SharePoint (etl/output). El resto queda en salida/ local.
EXACTOS = [
    "cuentas_powerbi.csv",
    "dependencias_powerbi.csv",
    "capacidad_powerbi.csv",
    "resumen.html",
    "listado_sin_2fa.html",
    "02_estudiantes_sin_2fa.csv",
    "06_cobertura_2fa_facultad.csv",
]

INSTRUCCIONES = """ARCHIVOS PARA SHAREPOINT — {fecha}

Qué hacer (5 minutos):

1. Abra el sitio:
   Documentos → etl → output

2. Seleccione TODOS los archivos de ESTA carpeta
   (no suba la carpeta entera: abra esta carpeta y arrastre los archivos)

3. Arrástrelos a etl/output
   Si pregunta "¿Reemplazar?": Reemplazar

4. En Power BI (app.powerbi.com): el tablero se actualiza solo
   cada hora. Si necesita ver el corte YA: Actualizar ahora.

NO suba a SharePoint los archivos de la carpeta "salida" del proyecto
(00_universo.csv y similares: son técnicos y tienen más datos).

Listas (MetaProyecto, Acciones): NO se tocan con este proceso.
Se editan en el portal SharePoint cuando cambie la meta o registre una acción.
"""


def carpeta_escritorio(fecha: str | None = None) -> Path:
    dia = fecha or date.today().isoformat()
    escritorio = Path.home() / "Desktop"
    if not escritorio.is_dir():
        escritorio = Path.home() / "Escritorio"
    if not escritorio.is_dir():
        escritorio = Path.home()
    dest = escritorio / f"Archivos_SharePoint_{dia}"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def empaquetar(origen: Path, dest: Path) -> list[str]:
    copiados: list[str] = []
    for nombre in EXACTOS:
        src = origen / nombre
        if src.is_file():
            shutil.copy2(src, dest / nombre)
            copiados.append(nombre)
    for src in sorted(origen.glob("sin_2fa_*.csv")):
        shutil.copy2(src, dest / src.name)
        copiados.append(src.name)
    (dest / "LEAME_SUBIR_A_SHAREPOINT.txt").write_text(
        INSTRUCCIONES.format(fecha=date.today().isoformat()), encoding="utf-8"
    )
    return copiados


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--origen", type=Path, default=ROOT / "salida")
    ap.add_argument("--dest", type=Path)
    args = ap.parse_args()
    dest = args.dest or carpeta_escritorio()
    dest.mkdir(parents=True, exist_ok=True)
    copiados = empaquetar(args.origen, dest)
    print(dest.resolve())
    print(f"Copiados {len(copiados)} archivos:")
    for n in copiados:
        print(f"  - {n}")


if __name__ == "__main__":
    main()
