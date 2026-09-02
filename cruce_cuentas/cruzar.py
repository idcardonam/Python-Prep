#!/usr/bin/env python3
"""
Cruce reutilizable: Google Workspace + información académica (+ personal opcional).

Uso:
  python3 cruzar.py --ejemplo
  python3 cruzar.py --google entrada/google_admin.csv --academico entrada/academico.csv
  python3 cruzar.py --google g.csv --academico a.csv --personal p.csv --salida salida/

No subas CSV reales a Git. Solo corre en tu PC.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


# --- Detección de columnas (exportes Admin Console EN/ES) ---

GOOGLE_ALIASES = {
    "email": [
        "email address [required]",
        "email address",
        "email",
        "correo electrónico",
        "correo",
        "primary email",
    ],
    "nombre": ["first name [required]", "first name", "nombre", "given name"],
    "apellido": ["last name [required]", "last name", "apellidos", "apellido", "family name"],
    "estado_google": ["status [read only]", "status", "estado", "account status"],
    "ou": ["org unit path [required]", "org unit path", "org unit", "unidad organizacional", "ou"],
    "ultimo_ingreso": [
        "last sign in [read only]",
        "last sign in",
        "last login",
        "último inicio de sesión",
        "ultimo inicio de sesion",
    ],
    "2fa_inscrito": [
        "2sv enrolled [read only]",
        "2sv enrolled",
        "2-step verification enrollment status",
        "2sv enrollment",
        "enrollment status",
        "verificación en 2 pasos",
        "2-step verification enrolled",
    ],
    "2fa_forzado": [
        "2-step verification enforcement",
        "2sv enforcement",
        "enforcement",
        "aplicación de verificación en 2 pasos",
    ],
}

ACADEMICO_ALIASES = {
    "email": [
        "correo_unab",
        "correo institucional",
        "correo_institucional",
        "email institucional",
        "correo unab",
        "mail_institucional",
        "correo",
        "email",
        "e-mail",
        "mail",
        "usuario",
        "userprincipalname",
        "cuenta",
        "e_mail",
    ],
    "estado": [
        "est_acad",
        "estado academico",
        "estado académico",
        "estado",
        "situacion",
        "situación",
    ],
    "facultad": ["escuela", "facultad", "unidad academica", "unidad académica"],
    "programa": ["programa", "carrera", "programa academico", "programa académico"],
    "seccion": ["seccion", "sección", "paralelo"],
    "jornada": ["jornada", "modalidad jornada"],
    "codigo": ["codigo", "código", "codigo_estudiante", "codigo estudiante", "id estudiante", "id"],
    "nivel": ["nivel", "tipo formacion", "tipo formación", "nivel formacion"],
    "nombres": ["nombres", "nombre", "primer nombre"],
    "apellidos": ["apellidos", "apellido"],
    "cod_prog": ["cod_prog"],
    "cod_majr": ["cod_majr"],
    "cod_esc": ["cod_esc"],
    "periodo": ["periodo"],
}

PERSONAL_ALIASES = {
    "email": ["correo", "email", "correo institucional"],
    "tipo": ["tipo", "vinculacion", "vinculación", "rol", "categoria"],
    "area": ["area", "área", "dependencia", "facultad", "unidad"],
    "seccion": ["seccion", "sección", "oficina", "grupo"],
    "cargo": ["cargo", "puesto"],
    "nombres": ["nombres", "nombre"],
    "apellidos": ["apellidos", "apellido"],
}

CURRICULO_ALIASES = {
    "periodo": ["periodo", "term", "periodo_plan", "effective term"],
    "escuela": ["escuela", "facultad", "college"],
    "cod_esc": ["cod_esc", "codigo_escuela"],
    "programa": ["programa", "carrera", "program"],
    "cod_prog": ["cod_prog", "codigo_programa"],
    "major": ["cod_majr", "major", "cod_major"],
    "nivel": ["nivel"],
    "plan": ["plan", "plan_estudios", "plan estudios", "curriculo", "currículum", "cod_plan", "codigo_plan"],
    "tipo": ["tipo", "formal", "tipo_formacion", "tipo formación", "modalidad"],
    "campus": ["campus"],
}

EXCLUIR_DEFAULT = {
    "GRADUADO",
    "GRADUADA",
    "EGRESADO",
    "EGRESADA",
    "TITULADO",
    "TITULADA",
    "GRADUATE",
    "ALUMNI",
}


def norm_header(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return re.sub(r"\s+", " ", s)


def norm_email(s: str) -> str:
    return (s or "").strip().lower()


def norm_estado(s: str) -> str:
    s = (s or "").strip().upper()
    s = s.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
    return re.sub(r"\s+", " ", s)


def pick_col(headers: list[str], aliases: list[str]) -> str | None:
    """Coincidencia exacta del encabezado normalizado. Evita CANT_CURSOS / INSCRIP_STATUS."""
    mapped = {norm_header(h): h for h in headers}
    for a in aliases:
        hit = mapped.get(norm_header(a))
        if hit:
            return hit
    return None


def map_columns(headers: list[str], alias_map: dict[str, list[str]]) -> dict[str, str | None]:
    return {k: pick_col(headers, v) for k, v in alias_map.items()}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    n_comma, n_semi = first.count(","), first.count(";")
    if n_semi > n_comma:
        delimiter = ";"
    elif n_comma > n_semi:
        delimiter = ","
    else:
        try:
            delimiter = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|").delimiter
        except csv.Error:
            delimiter = ","
    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    headers = reader.fieldnames or []
    rows = [{k: (v if v is not None else "").strip() for k, v in row.items() if k is not None} for row in reader]
    headers = [h for h in headers if h is not None]
    if len(headers) <= 1 and n_semi > 1:
        reader = csv.DictReader(text.splitlines(), delimiter=";")
        headers = [h for h in (reader.fieldnames or []) if h is not None]
        rows = [{k: (v if v is not None else "").strip() for k, v in row.items() if k is not None} for row in reader]
    return headers, rows


def periodo_desde_nombre(nombre: str) -> str:
    m = re.search(r"(20\d{4})", nombre)
    if m:
        return m.group(1)
    m = re.search(r"IC\s*20\d{2}", nombre, re.I)
    return re.sub(r"\s+", " ", m.group(0)).upper() if m else Path(nombre).stem


def parece_export_google(headers: list[str]) -> bool:
    blob = " ".join(norm_header(h) for h in headers)
    return "2sv" in blob or "2-step verification" in blob or "email address [required]" in blob


def nombre_parece_curriculo(path: Path) -> bool:
    nom = norm_header(path.stem.replace("-", " ").replace("_", " "))
    return "curricul" in nom or "vista de curriculo" in nom


def es_archivo_curriculo(path: Path, headers: list[str] | None = None) -> bool:
    if nombre_parece_curriculo(path):
        return True
    h = headers if headers is not None else peek_headers(path)
    nh = {norm_header(x) for x in h}
    if "correo_unab" in nh or "correo institucional" in nh:
        return False
    if parece_export_google(h):
        return False
    return "periodo" in nh and bool(nh & {"programa", "escuela", "cod_prog", "cod_majr"})


def peek_headers(path: Path) -> list[str]:
    raw = path.read_bytes()[:16384]
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    delim = ";" if first.count(";") > first.count(",") else ","
    return next(csv.reader([first], delimiter=delim), [])


def listar_csv(carpeta: Path) -> list[Path]:
    return sorted(p for p in carpeta.glob("*.csv") if p.is_file())


def listar_csv_academico(carpeta: Path) -> list[Path]:
    out: list[Path] = []
    for p in listar_csv(carpeta):
        if p.name.lower().startswith("user_download"):
            continue
        headers = peek_headers(p)
        if parece_export_google(headers) or es_archivo_curriculo(p, headers):
            continue
        nh = {norm_header(x) for x in headers}
        if {"tipo", "cargo"} <= nh and "escuela" not in nh and "est_acad" not in nh:
            continue
        out.append(p)
    return out


def listar_csv_curriculo(carpeta: Path) -> list[Path]:
    return [p for p in listar_csv(carpeta) if es_archivo_curriculo(p)]


def inspeccionar_academico(carpeta: Path) -> None:
    """Solo metadatos: no imprime correos ni celdas."""
    todos = listar_csv(carpeta)
    google = [p for p in todos if p.name.lower().startswith("user_download") or parece_export_google(peek_headers(p))]
    curric = listar_csv_curriculo(carpeta)
    files = listar_csv_academico(carpeta)
    print(f"Carpeta: {carpeta}")
    if google:
        print(f"Google Admin omitido del académico: {len(google)}")
        for p in google:
            print(f"  - {p.name}")
    if curric:
        print(f"Vista de currículo (catálogo de planes, no estudiantes): {len(curric)}")
        for p in curric:
            headers, rows = read_csv(p)
            mapped = map_columns(headers, CURRICULO_ALIASES)
            print(f"  {p.name}  filas={len(rows)}  cols={len(headers)}")
            print(f"    periodo: {mapped.get('periodo') or 'NO'}  escuela: {mapped.get('escuela') or 'NO'}  programa: {mapped.get('programa') or 'NO'}")
            print(f"    cod_prog: {mapped.get('cod_prog') or 'NO'}  major: {mapped.get('major') or 'NO'}  plan: {mapped.get('plan') or 'NO'}")
            print(f"    columnas: {headers}")
    if not files:
        raise SystemExit(f"No hay CSV académicos de inscritos en {carpeta}")
    print(f"Archivos CSV de inscritos: {len(files)}")
    print("-" * 72)
    all_headers: dict[str, set[str]] = {}
    total = 0
    for p in files:
        headers, rows = read_csv(p)
        total += len(rows)
        mapped = map_columns(headers, ACADEMICO_ALIASES)
        print(f"{p.name}")
        print(f"  filas={len(rows):>8}  cols={len(headers):>3}  periodo={periodo_desde_nombre(p.name)}  bytes={p.stat().st_size}")
        print(f"  correo detectado: {mapped.get('email') or 'NO'}")
        print(f"  estado detectado: {mapped.get('estado') or 'NO'}")
        print(f"  facultad: {mapped.get('facultad') or 'NO'}  programa: {mapped.get('programa') or 'NO'}  seccion: {mapped.get('seccion') or 'NO'}")
        print(f"  columnas: {headers}")
        print()
        all_headers.setdefault("union", set()).update(headers)
    print("-" * 72)
    print(f"Filas totales inscritos (suma bruta, puede haber duplicados entre archivos): {total}")
    print(f"Columnas distintas en inscritos: {len(all_headers['union'])}")
    print("Regla de currículo: si hay varias filas del mismo programa/major, el ÚLTIMO periodo es el plan vigente.")


def cargar_academico_carpeta(carpeta: Path) -> tuple[list[str], list[dict[str, str]]]:
    files = listar_csv_academico(carpeta)
    if not files:
        raise SystemExit(f"No hay CSV en {carpeta}")
    union: list[str] = []
    seen_h: set[str] = set()
    rows_out: list[dict[str, str]] = []
    for p in files:
        headers, rows = read_csv(p)
        for h in headers:
            if h not in seen_h:
                seen_h.add(h)
                union.append(h)
        periodo = periodo_desde_nombre(p.name)
        for row in rows:
            row["_fuente_archivo"] = p.name
            row["_periodo"] = periodo
            rows_out.append(row)
    extra = ["_fuente_archivo", "_periodo"]
    headers_final = union + [x for x in extra if x not in seen_h]
    return headers_final, rows_out


def merge_texto(prev: str, nuevo: str) -> str:
    prev = (prev or "").strip()
    nuevo = (nuevo or "").strip()
    if not nuevo:
        return prev
    if not prev:
        return nuevo
    parts = [x.strip() for x in prev.split(" | ") if x.strip()]
    if nuevo not in parts:
        parts.append(nuevo)
    return " | ".join(parts)


def split_multi(s: str) -> list[str]:
    return [x.strip() for x in (s or "").replace(";", "|").split("|") if x.strip()]


def periodo_orden(valor: str) -> tuple[int, int]:
    """Mayor tupla = periodo más reciente (plan vigente)."""
    s = (valor or "").strip().upper()
    m = re.search(r"(20\d{4})", s)
    if m:
        return (2, int(m.group(1)))
    m = re.search(r"IC\s*(20\d{2})", s)
    if m:
        return (1, int(m.group(1)))
    m = re.search(r"(\d{5,6})", s)
    if m:
        return (2, int(m.group(1)))
    return (0, 0)


def clave_txt(s: str) -> str:
    return norm_header(s).upper()


def indice_curriculo(cod_prog: str, major: str, programa: str, escuela: str) -> list[tuple]:
    keys: list[tuple] = []
    cp, cm = clave_txt(cod_prog), clave_txt(major)
    pr, es = clave_txt(programa), clave_txt(escuela)
    if cp and cm:
        keys.append(("pm", cp, cm))
    if cp:
        keys.append(("p", cp))
    if pr:
        keys.append(("n", pr, es))
    return keys


def cargar_catalogo_curriculo(paths: list[Path]) -> tuple[dict[tuple, dict[str, str]], dict[str, str | None], int]:
    """Una fila vigente por programa/major: gana el último PERIODO."""
    vigentes: dict[tuple, dict[str, str]] = {}
    c_map: dict[str, str | None] = {}
    n_hist = 0
    for path in paths:
        headers, rows = read_csv(path)
        c_map = map_columns(headers, CURRICULO_ALIASES)
        for row in rows:
            n_hist += 1
            pieza = {campo: (row.get(c_map[campo], "") if c_map.get(campo) else "") for campo in c_map}
            pieza["_fuente"] = path.name
            pieza["_todas"] = dict(row)
            per = pieza.get("periodo") or ""
            orden = periodo_orden(per)
            for key in indice_curriculo(pieza.get("cod_prog") or "", pieza.get("major") or "", pieza.get("programa") or "", pieza.get("escuela") or ""):
                prev = vigentes.get(key)
                if prev is None or orden >= periodo_orden(prev.get("periodo") or ""):
                    vigentes[key] = pieza
    return vigentes, c_map, n_hist


def buscar_plan(catalogo: dict[tuple, dict[str, str]], cod_prog: str, major: str, programa: str, escuela: str) -> dict[str, str]:
    for key in indice_curriculo(cod_prog, major, programa, escuela):
        hit = catalogo.get(key)
        if hit:
            return hit
    cps, cms, prs, ess = split_multi(cod_prog), split_multi(major), split_multi(programa), split_multi(escuela)
    n = max(len(cps), len(cms), len(prs), len(ess), 1)
    for i in range(n):
        hit = buscar_plan_simple(
            catalogo,
            cps[i] if i < len(cps) else (cps[-1] if cps else ""),
            cms[i] if i < len(cms) else (cms[-1] if cms else ""),
            prs[i] if i < len(prs) else (prs[-1] if prs else ""),
            ess[i] if i < len(ess) else (ess[-1] if ess else ""),
        )
        if hit:
            return hit
    return {}


def buscar_plan_simple(catalogo: dict[tuple, dict[str, str]], cod_prog: str, major: str, programa: str, escuela: str) -> dict[str, str]:
    for key in indice_curriculo(cod_prog, major, programa, escuela):
        hit = catalogo.get(key)
        if hit:
            return hit
    return {}


def adjuntar_curriculo(ficha: dict[str, Any], plan: dict[str, str]) -> None:
    if not plan:
        return
    dest = ficha.setdefault("curriculo", {})
    for campo in ("periodo", "escuela", "cod_esc", "programa", "cod_prog", "major", "nivel", "plan", "tipo", "campus"):
        dest[campo] = merge_texto(dest.get(campo, ""), plan.get(campo, ""))
    dest["match"] = "SI"


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v in {"-", "Never", "Nunca", "—", "Never logged in"}:
        return None
    v = v.replace("T", " ")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
    ):
        try:
            return datetime.strptime(v[:19], fmt)
        except ValueError:
            continue
    return None


def is_2fa_on(inscrito: str, forzado: str) -> bool:
    """True solo si el usuario tiene 2FA inscrito. Enforcement Off/On es otra cosa."""
    i = (inscrito or "").strip().lower()
    if not i:
        return False
    if i in {"not enrolled", "no", "off", "false", "0", "never", "no inscrito", "not_enrolled"}:
        return False
    if "not enrolled" in i or i.startswith("not "):
        return False
    if i in {"enrolled", "yes", "si", "sí", "true", "on", "inscrito"}:
        return True
    if "enrolled" in i or "inscrit" in i:
        return True
    return False


def load_config(path: Path | None) -> dict[str, Any]:
    cfg: dict[str, Any] = {
        "dominio": "unab.edu.co",
        "estados_excluir": sorted(EXCLUIR_DEFAULT),
        "ou_personal": ["docente", "profesor", "administrativo", "gestion", "tic", "staff", "planta"],
        "dias_inactiva": 90,
    }
    if path and path.exists() and yaml:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cfg.update({k: v for k, v in data.items() if v is not None})
    return cfg


def proyecto_a_ficha(email: str) -> dict[str, Any]:
    return {
        "correo": email,
        "perfil": "SIN_CLASIFICAR",
        "prioridad_2fa": "N/A",
        "tiene_2fa": None,
        "en_google": False,
        "en_academico": False,
        "en_personal": False,
        "google": {},
        "academico": {},
        "personal": {},
        "curriculo": {},
        "alertas": [],
    }


def clasificar(ficha: dict[str, Any], ou_personal: list[str], excluir: set[str]) -> None:
    ou = (ficha["google"].get("ou") or "").lower()
    estado = norm_estado(ficha["academico"].get("estado") or "")
    if estado in excluir:
        ficha["perfil"] = "EGRESADO_EN_EXTRACTO"
        ficha["alertas"].append("Aparece en académico con estado de egreso (debería filtrarse).")
        return
    if ficha["en_academico"] and ficha["en_google"]:
        ficha["perfil"] = "ESTUDIANTE_VIGENTE"
        return
    if ficha["en_academico"] and not ficha["en_google"]:
        ficha["perfil"] = "ACADEMICO_SIN_CUENTA_GOOGLE"
        ficha["alertas"].append("Tiene registro académico vigente y no aparece en Admin Google.")
        return
    if ficha["en_personal"]:
        tipo = (ficha["personal"].get("tipo") or "").upper()
        ficha["perfil"] = "PERSONAL_" + (tipo if tipo else "INSTITUCIONAL")
        return
    if any(p in ou for p in ou_personal):
        ficha["perfil"] = "POSIBLE_PERSONAL_POR_OU"
        return
    if "egresad" in ou or "gradua" in ou or "alumni" in ou:
        ficha["perfil"] = "POSIBLE_EGRESADO_CON_CUENTA"
        ficha["alertas"].append("Está en Google y no en académico vigente: posible egresado con cuenta activa.")
        return
    if ficha["en_google"]:
        ficha["perfil"] = "GOOGLE_SIN_MATCH_ACADEMICO"
        ficha["alertas"].append(
            "Cuenta institucional sin ficha académica vigente: personal, egresado u órfana. Completar con CSV de GH."
        )
        return
    ficha["perfil"] = "SIN_CLASIFICAR"


def prioridad_2fa(ficha: dict[str, Any], dias_inactiva: int, now: datetime) -> str:
    if ficha["tiene_2fa"] is True:
        return "OK"
    if ficha["tiene_2fa"] is None:
        return "SIN_DATO_GOOGLE"
    ultimo = parse_date(ficha["google"].get("ultimo_ingreso") or "")
    inactiva = False
    if ultimo is None:
        inactiva = True
    else:
        inactiva = (now - ultimo).days >= dias_inactiva
    perfil = ficha["perfil"]
    if perfil.startswith("PERSONAL") or perfil == "POSIBLE_PERSONAL_POR_OU":
        return "ALTA_PERSONAL_SIN_2FA"
    if perfil == "ESTUDIANTE_VIGENTE" and not inactiva:
        return "ALTA_ESTUDIANTE_ACTIVO_SIN_2FA"
    if perfil == "ESTUDIANTE_VIGENTE" and inactiva:
        return "MEDIA_ESTUDIANTE_INACTIVO_SIN_2FA"
    if perfil == "POSIBLE_EGRESADO_CON_CUENTA":
        return "REVISAR_EGRESO_Y_2FA"
    if inactiva:
        return "MEDIA_CUENTA_INACTIVA_SIN_2FA"
    return "ALTA_SIN_2FA"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def flatten(ficha: dict[str, Any]) -> dict[str, Any]:
    g, a, p = ficha["google"], ficha["academico"], ficha["personal"]
    c = ficha.get("curriculo") or {}
    out = {
        "correo": ficha["correo"],
        "perfil": ficha["perfil"],
        "prioridad_2fa": ficha["prioridad_2fa"],
        "tiene_2fa": "" if ficha["tiene_2fa"] is None else ("SI" if ficha["tiene_2fa"] else "NO"),
        "en_google": "SI" if ficha["en_google"] else "NO",
        "en_academico": "SI" if ficha["en_academico"] else "NO",
        "en_personal": "SI" if ficha["en_personal"] else "NO",
        "g_nombre": g.get("nombre", ""),
        "g_apellido": g.get("apellido", ""),
        "g_estado": g.get("estado_google", ""),
        "g_ou": g.get("ou", ""),
        "g_ultimo_ingreso": g.get("ultimo_ingreso", ""),
        "g_2fa_inscrito": g.get("2fa_inscrito", ""),
        "g_2fa_forzado": g.get("2fa_forzado", ""),
        "a_nombres": a.get("nombres", ""),
        "a_apellidos": a.get("apellidos", ""),
        "a_estado": a.get("estado", ""),
        "a_facultad": a.get("facultad", ""),
        "a_programa": a.get("programa", ""),
        "a_seccion": a.get("seccion", ""),
        "a_jornada": a.get("jornada", ""),
        "a_codigo": a.get("codigo", ""),
        "a_nivel": a.get("nivel", ""),
        "a_cod_prog": a.get("cod_prog", ""),
        "a_cod_majr": a.get("cod_majr", ""),
        "c_match": c.get("match", "NO") if c else "NO",
        "c_periodo_vigente": c.get("periodo", ""),
        "c_escuela": c.get("escuela", ""),
        "c_programa": c.get("programa", ""),
        "c_cod_prog": c.get("cod_prog", ""),
        "c_major": c.get("major", ""),
        "c_plan": c.get("plan", ""),
        "c_nivel": c.get("nivel", ""),
        "c_tipo": c.get("tipo", ""),
        "c_campus": c.get("campus", ""),
        "p_tipo": p.get("tipo", ""),
        "p_area": p.get("area", ""),
        "p_seccion": p.get("seccion", ""),
        "p_cargo": p.get("cargo", ""),
        "alertas": " | ".join(ficha["alertas"]),
    }
    extra = a.get("_todas") or {}
    skip = {norm_header(x) for x in (
        "correo", "email", "correo institucional", "e-mail", "mail",
        "nombres", "nombre", "apellidos", "apellido", "estado",
        "facultad", "programa", "seccion", "sección", "jornada",
        "codigo", "código", "codigo_estudiante", "nivel",
        "cod_prog", "cod_majr", "cod_esc", "periodo",
    )}
    for k, v in extra.items():
        if not k or norm_header(k) in skip:
            continue
        out[f"a_{k}"] = v
    return out


def html_report(
    path: Path,
    resumen: dict[str, Any],
    por_facultad: list[dict[str, Any]],
    por_plan: list[dict[str, Any]] | None = None,
) -> None:
    def tabla(filas: list[dict[str, Any]], cols: list[tuple[str, str]]) -> str:
        body = "".join(
            "<tr>" + "".join(f"<td>{html.escape(str(r.get(k, '')))}</td>" for k, _ in cols) + "</tr>"
            for r in filas
        )
        head = "".join(f"<th>{html.escape(t)}</th>" for _, t in cols)
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body or '<tr><td colspan=\"%d\">Sin datos</td></tr>' % len(cols)}</tbody></table>"

    perfiles = "".join(
        f"<li><strong>{html.escape(str(k))}:</strong> {v}</li>" for k, v in resumen["perfiles"].items()
    )
    fac_html = tabla(por_facultad, [("facultad", "Escuela / facultad"), ("cuentas", "Cuentas"), ("sin_2fa", "Sin 2FA"), ("cobertura_2fa", "Cobertura %")])
    plan_html = tabla(
        por_plan or [],
        [
            ("escuela", "Escuela"),
            ("programa", "Programa (plan vigente)"),
            ("periodo_vigente", "Periodo plan"),
            ("cuentas", "Cuentas"),
            ("sin_2fa", "Sin 2FA"),
            ("cobertura_2fa", "Cobertura %"),
        ],
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<title>Cruce cuentas institucionales</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:2rem;background:#f4f7fb;color:#1f2937}}
.card{{background:#fff;border-radius:12px;padding:1.2rem;margin-bottom:1rem;box-shadow:0 4px 16px rgba(0,0,0,.06)}}
h1,h2{{color:#003B70}} table{{border-collapse:collapse;width:100%}}
th,td{{border-bottom:1px solid #d5deea;padding:.5rem;text-align:left}}
.kpi{{display:flex;gap:1rem;flex-wrap:wrap}}
.kpi div{{background:#e8eef5;padding:.8rem 1rem;border-radius:10px;min-width:140px}}
.bad{{color:#b42318;font-weight:700}}
.note{{font-size:.95rem;color:#4b5563}}
</style></head><body>
<div class="card">
<h1>Cruce Google × académico × currículo</h1>
<p>Generado: {html.escape(str(resumen['generado']))}</p>
<p class="note">Reutilizable por periodo: mismos CSV de entrada, nueva carpeta de salida. Egresados no cuentan como vigentes; sí quedan en el radar de Google sin match.</p>
<h2>Acción 2FA (estudiantes vigentes)</h2>
<div class="kpi">
  <div>Match estudiantes<br><strong>{resumen['n_match_estudiante']}</strong></div>
  <div class="bad">Estudiantes sin 2FA<br><strong>{resumen.get('n_estudiantes_sin_2fa', 0)}</strong></div>
  <div>Cobertura 2FA estudiantes<br><strong>{resumen.get('cobertura_2fa_estudiantes', 0)}%</strong></div>
  <div>Planes vigentes (catálogo)<br><strong>{resumen.get('n_planes_vigentes', 0)}</strong></div>
  <div>Fichas con plan vigente<br><strong>{resumen.get('n_match_curriculo', 0)}</strong></div>
</div>
<h2>Universo Google (radar)</h2>
<div class="kpi">
  <div>Cuentas Google<br><strong>{resumen['n_google']}</strong></div>
  <div>Fichas académicas vigentes<br><strong>{resumen['n_academico']}</strong></div>
  <div class="bad">Sin 2FA en el dominio<br><strong>{resumen['n_sin_2fa']}</strong></div>
  <div>Cobertura 2FA dominio<br><strong>{resumen['cobertura_2fa']}%</strong></div>
  <div>Google sin ficha vigente<br><strong>{resumen.get('n_google_sin_match', 0)}</strong></div>
</div>
</div>
<div class="card"><h2>Perfiles</h2><ul>{perfiles}</ul>
<p class="note">GOOGLE_SIN_MATCH_ACADEMICO = personal + egresados con cuenta + huérfanas. No son la campaña de facultades. Ver <code>03_google_sin_match_academico.csv</code>.</p>
</div>
<div class="card"><h2>2FA por escuela (match académico)</h2>
{fac_html}
</div>
<div class="card"><h2>2FA por programa con plan vigente (último periodo del currículo)</h2>
{plan_html}
<p class="note">Si un programa cambió de plan ante el MEN, se usa el periodo más reciente. Histórico del catálogo: {resumen.get('n_filas_curriculo', 0)} filas.</p>
</div>
</body></html>"""
    path.write_text(html_doc, encoding="utf-8")


def cruzar(
    google_path: Path,
    academico_path: Path | None,
    personal_path: Path | None,
    salida: Path,
    cfg: dict[str, Any],
    academico_dir: Path | None = None,
    curriculo_path: Path | None = None,
) -> None:
    excluir = {norm_estado(x) for x in cfg.get("estados_excluir", EXCLUIR_DEFAULT)}
    ou_personal = [str(x).lower() for x in cfg.get("ou_personal", [])]
    dias_inactiva = int(cfg.get("dias_inactiva", 90))
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    g_headers, g_rows = read_csv(google_path)
    if academico_dir:
        a_headers, a_rows = cargar_academico_carpeta(academico_dir)
    elif academico_path:
        a_headers, a_rows = read_csv(academico_path)
        for row in a_rows:
            row.setdefault("_fuente_archivo", academico_path.name)
            row.setdefault("_periodo", periodo_desde_nombre(academico_path.name))
        if "_fuente_archivo" not in a_headers:
            a_headers = list(a_headers) + ["_fuente_archivo", "_periodo"]
    else:
        raise SystemExit("Falta --academico o --academico-dir")
    curric_files: list[Path] = []
    if curriculo_path and curriculo_path.exists():
        curric_files = [curriculo_path]
    elif academico_dir:
        curric_files = listar_csv_curriculo(academico_dir)
    catalogo, c_map, n_filas_curriculo = cargar_catalogo_curriculo(curric_files) if curric_files else ({}, {}, 0)
    g_map = map_columns(g_headers, GOOGLE_ALIASES)
    a_map = map_columns(a_headers, ACADEMICO_ALIASES)
    if not g_map["email"]:
        raise SystemExit(f"No hallé columna de correo en Google. Encabezados: {g_headers}")
    if not a_map["email"]:
        raise SystemExit(f"No hallé columna de correo en académico. Encabezados: {a_headers}")

    fichas: dict[str, dict[str, Any]] = {}

    def get(row: dict[str, str], col: str | None) -> str:
        return row.get(col, "") if col else ""

    for row in g_rows:
        email = norm_email(get(row, g_map["email"]))
        if not email:
            continue
        f = fichas.setdefault(email, proyecto_a_ficha(email))
        f["en_google"] = True
        f["google"] = {
            "nombre": get(row, g_map["nombre"]),
            "apellido": get(row, g_map["apellido"]),
            "estado_google": get(row, g_map["estado_google"]),
            "ou": get(row, g_map["ou"]),
            "ultimo_ingreso": get(row, g_map["ultimo_ingreso"]),
            "2fa_inscrito": get(row, g_map["2fa_inscrito"]),
            "2fa_forzado": get(row, g_map["2fa_forzado"]),
        }
        f["tiene_2fa"] = is_2fa_on(f["google"]["2fa_inscrito"], f["google"]["2fa_forzado"])
        # Conserva columnas extra del Admin por si sirven después
        f["google"]["_extra"] = {k: v for k, v in row.items() if k not in set(g_map.values()) and v}

    skipped_grad = 0
    detalle_acad: list[dict[str, Any]] = []
    for row in a_rows:
        email = norm_email(get(row, a_map["email"]))
        if not email:
            continue
        estado = norm_estado(get(row, a_map["estado"]))
        if estado in excluir:
            skipped_grad += 1
            continue
        f = fichas.setdefault(email, proyecto_a_ficha(email))
        f["en_academico"] = True
        pieza = {campo: get(row, a_map[campo]) for campo in a_map}
        pieza.pop("email", None)
        if not f.get("academico"):
            f["academico"] = {**pieza, "_todas": dict(row)}
        else:
            acc = f["academico"]
            for campo, val in pieza.items():
                acc[campo] = merge_texto(acc.get(campo, ""), val)
            todas = acc.setdefault("_todas", {})
            for k, v in row.items():
                todas[k] = merge_texto(todas.get(k, ""), v)
        det = {"correo": email, "_periodo": row.get("_periodo", ""), "_fuente_archivo": row.get("_fuente_archivo", "")}
        det.update(row)
        plan = buscar_plan(
            catalogo,
            get(row, a_map.get("cod_prog")),
            get(row, a_map.get("cod_majr")),
            get(row, a_map.get("programa")),
            get(row, a_map.get("facultad")),
        )
        if plan:
            adjuntar_curriculo(f, plan)
            det["c_periodo_vigente"] = plan.get("periodo", "")
            det["c_plan"] = plan.get("plan", "")
            det["c_programa"] = plan.get("programa", "")
        detalle_acad.append(det)

    p_map = {}
    if personal_path and personal_path.exists():
        p_headers, p_rows = read_csv(personal_path)
        p_map = map_columns(p_headers, PERSONAL_ALIASES)
        if not p_map["email"]:
            print("AVISO: CSV personal sin columna de correo; se ignora.")
        else:
            for row in p_rows:
                email = norm_email(get(row, p_map["email"]))
                if not email:
                    continue
                f = fichas.setdefault(email, proyecto_a_ficha(email))
                f["en_personal"] = True
                f["personal"] = {campo: get(row, p_map[campo]) for campo in p_map if campo != "email"}
                f["personal"]["_todas"] = dict(row)

    for f in fichas.values():
        clasificar(f, ou_personal, excluir)
        f["prioridad_2fa"] = prioridad_2fa(f, dias_inactiva, now)

    salida.mkdir(parents=True, exist_ok=True)
    planos = [flatten(f) for f in sorted(fichas.values(), key=lambda x: x["correo"])]
    fields: list[str] = []
    seen: set[str] = set()
    for r in planos:
        for k in r:
            if k not in seen:
                seen.add(k)
                fields.append(k)
    if not fields:
        fields = ["correo"]

    write_csv(salida / "00_universo.csv", planos, fields)
    write_csv(
        salida / "01_sin_2fa.csv",
        [r for r in planos if r["tiene_2fa"] == "NO"],
        fields,
    )
    write_csv(
        salida / "02_estudiantes_sin_2fa.csv",
        [r for r in planos if r["perfil"] == "ESTUDIANTE_VIGENTE" and r["tiene_2fa"] == "NO"],
        fields,
    )
    write_csv(
        salida / "03_google_sin_match_academico.csv",
        [r for r in planos if r["en_google"] == "SI" and r["en_academico"] == "NO"],
        fields,
    )
    write_csv(
        salida / "04_academico_sin_cuenta_google.csv",
        [r for r in planos if r["perfil"] == "ACADEMICO_SIN_CUENTA_GOOGLE"],
        fields,
    )
    write_csv(
        salida / "05_prioridad_alta_2fa.csv",
        [r for r in planos if r["prioridad_2fa"].startswith("ALTA")],
        fields,
    )

    fac = []
    gstats = defaultdict(Counter)
    for r in planos:
        if r["en_academico"] != "SI" or r["en_google"] != "SI":
            continue
        k = r.get("a_facultad") or "(sin dato)"
        gstats[k]["cuentas"] += 1
        if r["tiene_2fa"] == "NO":
            gstats[k]["sin_2fa"] += 1
        if r["tiene_2fa"] == "SI":
            gstats[k]["con_2fa"] += 1
    for k, c in sorted(gstats.items()):
        tot = c["cuentas"]
        fac.append(
            {
                "facultad": k,
                "cuentas": tot,
                "sin_2fa": c["sin_2fa"],
                "cobertura_2fa": round(100 * c["con_2fa"] / tot, 1) if tot else 0,
            }
        )
    write_csv(
        salida / "06_cobertura_2fa_facultad.csv",
        fac,
        ["facultad", "cuentas", "sin_2fa", "cobertura_2fa"],
    )

    prog = defaultdict(Counter)
    for r in planos:
        if r["en_academico"] != "SI" or r["en_google"] != "SI":
            continue
        k = f"{r.get('a_facultad') or '-'} | {r.get('a_programa') or '-'} | seccion {r.get('a_seccion') or '-'}"
        prog[k]["cuentas"] += 1
        if r["tiene_2fa"] == "NO":
            prog[k]["sin_2fa"] += 1
        if r["tiene_2fa"] == "SI":
            prog[k]["con_2fa"] += 1
    prog_rows = []
    for k, c in sorted(prog.items()):
        tot = c["cuentas"]
        prog_rows.append(
            {
                "facultad_programa_seccion": k,
                "cuentas": tot,
                "sin_2fa": c["sin_2fa"],
                "cobertura_2fa": round(100 * c["con_2fa"] / tot, 1) if tot else 0,
            }
        )
    write_csv(
        salida / "07_cobertura_2fa_programa_seccion.csv",
        prog_rows,
        ["facultad_programa_seccion", "cuentas", "sin_2fa", "cobertura_2fa"],
    )
    det_fields: list[str] = []
    det_seen: set[str] = set()
    for r in detalle_acad:
        for k in r:
            if k not in det_seen:
                det_seen.add(k)
                det_fields.append(k)
    if det_fields:
        write_csv(salida / "08_academico_filas.csv", detalle_acad, det_fields)

    planes_vigentes: list[dict[str, Any]] = []
    seen_plan: set[tuple] = set()
    for pieza in catalogo.values():
        ident = (
            pieza.get("periodo", ""),
            pieza.get("cod_prog", ""),
            pieza.get("major", ""),
            pieza.get("programa", ""),
        )
        if ident in seen_plan:
            continue
        seen_plan.add(ident)
        row_out = {
            "periodo_vigente": pieza.get("periodo", ""),
            "cod_esc": pieza.get("cod_esc", ""),
            "escuela": pieza.get("escuela", ""),
            "cod_prog": pieza.get("cod_prog", ""),
            "programa": pieza.get("programa", ""),
            "major": pieza.get("major", ""),
            "plan": pieza.get("plan", ""),
            "nivel": pieza.get("nivel", ""),
            "tipo": pieza.get("tipo", ""),
            "campus": pieza.get("campus", ""),
            "_fuente": pieza.get("_fuente", ""),
        }
        extra = pieza.get("_todas") or {}
        for k, v in extra.items():
            if k and f"{k}" not in row_out:
                row_out[k] = v
        planes_vigentes.append(row_out)
    planes_vigentes.sort(key=lambda r: (str(r.get("escuela", "")), str(r.get("programa", ""))))
    if planes_vigentes:
        plan_fields: list[str] = []
        seen_pf: set[str] = set()
        for r in planes_vigentes:
            for k in r:
                if k not in seen_pf:
                    seen_pf.add(k)
                    plan_fields.append(k)
        write_csv(salida / "09_catalogo_planes_vigentes.csv", planes_vigentes, plan_fields)

    plan_stats = defaultdict(Counter)
    for r in planos:
        if r["en_academico"] != "SI" or r["en_google"] != "SI":
            continue
        k = (
            r.get("c_escuela") or r.get("a_facultad") or "-",
            r.get("c_programa") or r.get("a_programa") or "-",
            r.get("c_periodo_vigente") or "-",
        )
        plan_stats[k]["cuentas"] += 1
        if r["tiene_2fa"] == "NO":
            plan_stats[k]["sin_2fa"] += 1
        if r["tiene_2fa"] == "SI":
            plan_stats[k]["con_2fa"] += 1
    plan_rows = []
    for (esc, prog, per), c in sorted(plan_stats.items()):
        tot = c["cuentas"]
        plan_rows.append(
            {
                "escuela": esc,
                "programa": prog,
                "periodo_vigente": per,
                "cuentas": tot,
                "sin_2fa": c["sin_2fa"],
                "cobertura_2fa": round(100 * c["con_2fa"] / tot, 1) if tot else 0,
            }
        )
    write_csv(
        salida / "10_cobertura_2fa_plan_vigente.csv",
        plan_rows,
        ["escuela", "programa", "periodo_vigente", "cuentas", "sin_2fa", "cobertura_2fa"],
    )

    n_google = sum(1 for r in planos if r["en_google"] == "SI")
    n_acad = sum(1 for r in planos if r["en_academico"] == "SI")
    n_match = sum(1 for r in planos if r["perfil"] == "ESTUDIANTE_VIGENTE")
    n_sin = sum(1 for r in planos if r["tiene_2fa"] == "NO")
    n_con = sum(1 for r in planos if r["tiene_2fa"] == "SI")
    n_est_sin = sum(1 for r in planos if r["perfil"] == "ESTUDIANTE_VIGENTE" and r["tiene_2fa"] == "NO")
    n_est_con = sum(1 for r in planos if r["perfil"] == "ESTUDIANTE_VIGENTE" and r["tiene_2fa"] == "SI")
    n_google_sin_match = sum(1 for r in planos if r["en_google"] == "SI" and r["en_academico"] == "NO")
    n_match_curr = sum(1 for r in planos if r.get("c_match") == "SI")
    cob_est = round(100 * n_est_con / n_match, 1) if n_match else 0
    cobertura = round(100 * n_con / n_google, 1) if n_google else 0
    perfiles = dict(Counter(r["perfil"] for r in planos))
    resumen = {
        "generado": datetime.now().isoformat(timespec="seconds"),
        "n_google": n_google,
        "n_academico": n_acad,
        "n_match_estudiante": n_match,
        "n_estudiantes_sin_2fa": n_est_sin,
        "cobertura_2fa_estudiantes": cob_est,
        "n_sin_2fa": n_sin,
        "cobertura_2fa": cobertura,
        "n_google_sin_match": n_google_sin_match,
        "n_planes_vigentes": len(planes_vigentes),
        "n_filas_curriculo": n_filas_curriculo,
        "n_match_curriculo": n_match_curr,
        "perfiles": perfiles,
        "graduados_filtrados_en_academico": skipped_grad,
        "mapeo_google": g_map,
        "mapeo_academico": a_map,
        "mapeo_personal": p_map,
        "mapeo_curriculo": c_map,
    }
    (salida / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    html_report(salida / "resumen.html", resumen, fac, plan_rows)

    print("Listo ->", salida.resolve())
    print(f"Google: {n_google} | Académico vigente: {n_acad} | Match estudiante: {n_match}")
    print(f"Estudiantes sin 2FA: {n_est_sin} | Cobertura 2FA estudiantes: {cob_est}%")
    print(f"Sin 2FA dominio: {n_sin} | Cobertura 2FA dominio: {cobertura}%")
    print(f"Radar Google sin ficha vigente: {n_google_sin_match} | Egresados filtrados del académico: {skipped_grad}")
    print(f"Currículo: {n_filas_curriculo} filas históricas -> {len(planes_vigentes)} planes vigentes | match plan: {n_match_curr}")
    print("Columnas Google detectadas:", {k: v for k, v in g_map.items() if v})
    print("Columnas académico detectadas:", {k: v for k, v in a_map.items() if v})
    if c_map:
        print("Columnas currículo detectadas:", {k: v for k, v in c_map.items() if v})


def main() -> None:
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Cruce Google Admin × académico (2FA y ficha institucional)")
    ap.add_argument("--google", type=Path)
    ap.add_argument("--academico", type=Path)
    ap.add_argument("--academico-dir", type=Path, help="Carpeta con varios CSV de inscritos (se unen)")
    ap.add_argument("--personal", type=Path, help="CSV opcional de docentes/administrativos (GH/nómina)")
    ap.add_argument("--curriculo", type=Path, help="CSV Vista de currículo (si está en --academico-dir se detecta solo)")
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--config", type=Path, default=root / "config.yaml")
    ap.add_argument("--ejemplo", action="store_true", help="Corre con CSV de entrada/_ejemplos")
    ap.add_argument("--inspeccionar", type=Path, help="Solo analiza encabezados de una carpeta de CSV (sin cruce)")
    args = ap.parse_args()
    cfg = load_config(args.config if args.config.exists() else root / "config.example.yaml")

    if args.inspeccionar:
        inspeccionar_academico(args.inspeccionar)
        return
    if args.ejemplo:
        base = root / "entrada" / "_ejemplos"
        cruzar(
            base / "google_admin.csv",
            base / "academico.csv",
            base / "personal.csv",
            args.salida or root / "salida",
            cfg,
            curriculo_path=base / "curriculo.csv" if (base / "curriculo.csv").exists() else None,
        )
        return
    if not args.google or not (args.academico or args.academico_dir):
        ap.error("Indica --google y --academico o --academico-dir, o usa --ejemplo / --inspeccionar")
    cruzar(
        args.google,
        args.academico,
        args.personal,
        args.salida or root / "salida",
        cfg,
        academico_dir=args.academico_dir,
        curriculo_path=args.curriculo,
    )


if __name__ == "__main__":
    main()
