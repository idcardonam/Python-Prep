# -*- coding: utf-8 -*-
"""Procesa el CSV de Google Admin y genera los 3 archivos que alimentan Power BI.

Misma lógica que el pipeline anterior (cuentas / dependencias / capacidad).
Se invoca desde actualizar.bat junto con el cruce 2FA.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
LICENCIAS_DEFAULT = 433


def cargar_csv(archivo: Path) -> pd.DataFrame:
    """Google Admin suele exportar UTF-16 con tabuladores. Probamos varias opciones."""
    intentos = [
        {"encoding": "utf-16", "sep": "\t"},
        {"encoding": "utf-16-le", "sep": "\t"},
        {"encoding": "utf-8-sig", "sep": ","},
        {"encoding": "utf-8-sig", "sep": ";"},
        {"encoding": "latin-1", "sep": ","},
        {"encoding": "latin-1", "sep": ";"},
        {"encoding": "cp1252", "sep": ","},
        {"encoding": "cp1252", "sep": ";"},
    ]
    for opts in intentos:
        try:
            df = pd.read_csv(archivo, **opts)
            if len(df) > 0 and len(df.columns) > 1:
                print(f"  Formato detectado: encoding={opts['encoding']}, sep={repr(opts['sep'])}")
                print(f"  Filas leidas: {len(df)} | Columnas: {len(df.columns)}")
                return df
        except Exception:
            continue
    df = pd.read_csv(archivo, encoding="utf-8-sig", sep=None, engine="python")
    print(f"  Autodetectado: {len(df)} filas")
    return df


def buscar_columna(df: pd.DataFrame, *palabras_clave: str):
    for col in df.columns:
        nombre = str(col).lower()
        if all(palabra in nombre for palabra in palabras_clave):
            return df[col]
    return None


def columna(df: pd.DataFrame, *palabras_clave: str, default=""):
    col = buscar_columna(df, *palabras_clave)
    if col is not None:
        return col
    return pd.Series([default] * len(df), index=df.index)


def resolver_google(args: argparse.Namespace) -> Path:
    if args.google:
        p = Path(args.google)
        if not p.is_file():
            raise SystemExit(f"No existe el archivo Google Admin: {p}")
        return p
    if args.carpeta:
        sys.path.insert(0, str(ROOT))
        import cruzar

        fuentes = cruzar.descubrir_fuentes(Path(args.carpeta))
        if not fuentes["google"]:
            raise SystemExit(
                f"No hallé User_Download*.csv (Google Admin) en {args.carpeta}"
            )
        return fuentes["google"][0]
    data = ROOT / "data"
    csvs = sorted(data.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True) if data.exists() else []
    if not csvs:
        raise SystemExit("Indique --google o --carpeta, o ponga un CSV en cruce_cuentas/data/")
    return csvs[0]


def procesar(google_path: Path, salida: Path, licencias: int) -> dict:
    salida.mkdir(parents=True, exist_ok=True)
    print(f"Leyendo: {google_path.name}")
    df = cargar_csv(google_path)
    if len(df) == 0:
        raise SystemExit("ERROR: El archivo se leyó vacío.")

    print(f"  Columnas encontradas: {list(df.columns)[:5]}...")

    out = pd.DataFrame()
    email_col = buscar_columna(df, "email")
    out["email"] = email_col if email_col is not None else (df.iloc[:, 2] if df.shape[1] > 2 else df.iloc[:, 0])

    first = buscar_columna(df, "first", "name")
    last = buscar_columna(df, "last", "name")
    if first is not None and last is not None:
        out["nombre"] = first.fillna("").astype(str).str.strip() + " " + last.fillna("").astype(str).str.strip()
    else:
        out["nombre"] = columna(df, "name", default="")
        if out["nombre"].eq("").all():
            out["nombre"] = columna(df, "nombre", default="")

    out["dependencia"] = columna(df, "org", "unit", default="Sin asignar")
    out["estado_google"] = columna(df, "status", default="")
    if out["estado_google"].eq("").all():
        out["estado_google"] = columna(df, "estado", default="")
    out["ultimo_acceso"] = columna(df, "last", "sign", default="")
    if out["ultimo_acceso"].eq("").all():
        out["ultimo_acceso"] = columna(df, "login", default="")
    out["licencia"] = columna(df, "licen", default="")

    out["email"] = out["email"].astype(str).str.strip().str.lower()
    out["nombre"] = out["nombre"].fillna("").astype(str).str.strip()
    out["dependencia"] = out["dependencia"].fillna("Sin asignar").astype(str).str.strip()
    out["dependencia"] = out["dependencia"].str.replace(r"^/+", "", regex=True).str.split("/").str[-1]

    def dias_sin_acceso(val):
        texto = str(val).strip().lower()
        if texto in ("", "nan", "never", "nunca", "never logged in", "no data"):
            return None
        fecha = pd.to_datetime(val, dayfirst=True, errors="coerce", utc=True)
        if pd.isna(fecha):
            fecha = pd.to_datetime(val, errors="coerce", utc=True)
        if pd.isna(fecha):
            return None
        return (datetime.now() - fecha.to_pydatetime().replace(tzinfo=None)).days

    out["dias_sin_acceso"] = out["ultimo_acceso"].apply(dias_sin_acceso)

    def clasificar_variante(row):
        estado = str(row.get("estado_google", "")).lower()
        if "suspend" in estado:
            return "Suspendida"
        dias = row["dias_sin_acceso"]
        if dias is None:
            return "Inactiva cronica"
        if dias >= 180:
            return "Inactiva cronica"
        if dias >= 90:
            return "Ultima vez"
        return "Activa"

    out["variante"] = out.apply(clasificar_variante, axis=1)
    prefijos = out["email"].str.split("@").str[0]
    out.loc[prefijos.duplicated(keep=False), "variante"] = "Doble"
    acciones = {
        "Inactiva cronica": "Bloquear",
        "Ultima vez": "Revisar con dependencia",
        "Suspendida": "Ya bloqueada",
        "Doble": "Revisar duplicado",
        "Activa": "Mantener",
    }
    out["accion_recomendada"] = out["variante"].map(acciones)

    out.to_csv(salida / "cuentas_powerbi.csv", index=False, encoding="utf-8-sig")

    dep = (
        out.groupby("dependencia", dropna=False)
        .agg(
            total=("email", "count"),
            inactiva_cronica=("variante", lambda s: (s == "Inactiva cronica").sum()),
            ultima_vez=("variante", lambda s: (s == "Ultima vez").sum()),
            activas=("variante", lambda s: (s == "Activa").sum()),
            suspendidas=("variante", lambda s: (s == "Suspendida").sum()),
            dobles=("variante", lambda s: (s == "Doble").sum()),
            a_bloquear=("accion_recomendada", lambda s: (s == "Bloquear").sum()),
        )
        .reset_index()
    )
    dep.to_csv(salida / "dependencias_powerbi.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame(
        [
            {
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "licencias_totales": licencias,
                "cuentas_inventario": len(out),
                "disponibles": licencias - len(out),
            }
        ]
    ).to_csv(salida / "capacidad_powerbi.csv", index=False, encoding="utf-8-sig")

    resumen = {
        "total": len(out),
        "por_variante": out["variante"].value_counts().to_dict(),
        "por_estado_google": out["estado_google"].astype(str).value_counts().to_dict(),
        "a_bloquear": int((out["accion_recomendada"] == "Bloquear").sum()),
        "suspendidas": int((out["variante"] == "Suspendida").sum()),
        "activas": int((out["variante"] == "Activa").sum()),
    }
    (salida / "resumen_analisis.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\n=== POWER BI LISTO ===")
    print(f"Total cuentas: {resumen['total']}")
    print(f"Por variante: {resumen['por_variante']}")
    print(f"A bloquear: {resumen['a_bloquear']}")
    print(f"Archivos: cuentas_powerbi.csv, dependencias_powerbi.csv, capacidad_powerbi.csv")
    return resumen


def main() -> None:
    ap = argparse.ArgumentParser(description="Google Admin → CSV para Power BI")
    ap.add_argument("--google", type=Path, help="Ruta al User_Download CSV")
    ap.add_argument("--carpeta", type=Path, help="Carpeta que contiene User_Download (se detecta solo)")
    ap.add_argument("--salida", type=Path, default=ROOT / "salida")
    ap.add_argument("--licencias", type=int, default=LICENCIAS_DEFAULT)
    args = ap.parse_args()
    google = resolver_google(args)
    procesar(google, args.salida, args.licencias)


if __name__ == "__main__":
    main()
