# -*- coding: utf-8 -*-
"""Copia a Escritorio/Archivos_SharePoint_AAAA-MM-DD solo lo que se sube a etl/output."""
from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Mínimo para actualizar el portal. El resto queda en salida/ del PC.
EXACTOS = [
    "cuentas_powerbi.csv",
    "dependencias_powerbi.csv",
    "capacidad_powerbi.csv",
    "resumen.html",
    "listado_sin_2fa.html",
    "02_estudiantes_sin_2fa.csv",
]

INSTRUCCIONES = """ARCHIVOS PARA SHAREPOINT — {fecha}

Suba SOLO estos 6 archivos a Documentos → etl → output:

  Power BI (tablero):
    1. cuentas_powerbi.csv
    2. dependencias_powerbi.csv
    3. capacidad_powerbi.csv

  Informe 2FA (botón Resumen 2FA):
    4. resumen.html
    5. listado_sin_2fa.html
    6. 02_estudiantes_sin_2fa.csv
       (pendientes; en Excel filtre la columna facultad)

NO suba:
  - este archivo LEAME
  - los CSV por facultad (sin_2fa_*.csv)
  - 00_universo.csv ni el resto de "salida" del PC

Pasos:
1. Seleccione los 6 archivos (no el LEAME)
2. Arrastre a etl/output → Reemplazar
3. Power BI se refresca cada hora (o Actualizar ahora)

Listas MetaProyecto y Acciones: se editan en el portal, no con estos archivos.
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
