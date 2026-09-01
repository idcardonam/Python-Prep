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
    "email": ["correo", "email", "correo institucional", "correo_institucional", "e-mail", "mail"],
    "estado": ["estado", "estado academico", "estado académico", "situacion", "situación", "status"],
    "facultad": ["facultad", "escuela", "unidad academica", "unidad académica"],
    "programa": ["programa", "carrera", "programa academico", "programa académico"],
    "seccion": ["seccion", "sección", "grupo", "curso", "paralelo"],
    "jornada": ["jornada", "modalidad jornada"],
    "codigo": ["codigo", "código", "codigo_estudiante", "codigo estudiante", "id estudiante"],
    "nivel": ["nivel", "tipo formacion", "tipo formación", "nivel formacion"],
    "nombres": ["nombres", "nombre", "primer nombre"],
    "apellidos": ["apellidos", "apellido"],
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
    mapped = {norm_header(h): h for h in headers}
    for a in aliases:
        if a in mapped:
            return mapped[a]
    for h in headers:
        nh = norm_header(h)
        for a in aliases:
            if a in nh or nh in a:
                return h
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
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(text.splitlines(), dialect=dialect)
    headers = reader.fieldnames or []
    rows = [{k: (v if v is not None else "").strip() for k, v in row.items()} for row in reader]
    return headers, rows


def parse_date(value: str) -> datetime | None:
    v = (value or "").strip()
    if not v or v in {"-", "Never", "Nunca", "—"}:
        return None
    v = v.replace("T", " ")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
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
    if i in {"not enrolled", "no", "off", "false", "never", "no inscrito", "not_enrolled"}:
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
    )}
    for k, v in extra.items():
        if not k or norm_header(k) in skip:
            continue
        out[f"a_{k}"] = v
    return out


def html_report(path: Path, resumen: dict[str, Any], por_facultad: list[dict[str, Any]]) -> None:
    rows = "".join(
        f"<tr><td>{r['facultad']}</td><td>{r['cuentas']}</td><td>{r['sin_2fa']}</td>"
        f"<td>{r['cobertura_2fa']}%</td></tr>"
        for r in por_facultad
    )
    perfiles = "".join(f"<li><strong>{k}:</strong> {v}</li>" for k, v in resumen["perfiles"].items())
    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"/>
<title>Cruce cuentas institucionales</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;margin:2rem;background:#f4f7fb;color:#1f2937}}
.card{{background:#fff;border-radius:12px;padding:1.2rem;margin-bottom:1rem;box-shadow:0 4px 16px rgba(0,0,0,.06)}}
h1{{color:#003B70}} table{{border-collapse:collapse;width:100%}}
th,td{{border-bottom:1px solid #d5deea;padding:.5rem;text-align:left}}
.kpi{{display:flex;gap:1rem;flex-wrap:wrap}}
.kpi div{{background:#e8eef5;padding:.8rem 1rem;border-radius:10px;min-width:140px}}
.bad{{color:#b42318;font-weight:700}}
</style></head><body>
<div class="card">
<h1>Cruce Google × académico</h1>
<p>Generado: {resumen['generado']}</p>
<div class="kpi">
  <div>Cuentas Google<br><strong>{resumen['n_google']}</strong></div>
  <div>Fichas académicas<br><strong>{resumen['n_academico']}</strong></div>
  <div>Match estudiantes<br><strong>{resumen['n_match_estudiante']}</strong></div>
  <div class="bad">Sin 2FA<br><strong>{resumen['n_sin_2fa']}</strong></div>
  <div>Cobertura 2FA<br><strong>{resumen['cobertura_2fa']}%</strong></div>
</div>
</div>
<div class="card"><h2>Perfiles</h2><ul>{perfiles}</ul></div>
<div class="card"><h2>2FA por facultad (solo match académico)</h2>
<table><thead><tr><th>Facultad</th><th>Cuentas</th><th>Sin 2FA</th><th>Cobertura</th></tr></thead>
<tbody>{rows or '<tr><td colspan="4">Sin match académico</td></tr>'}</tbody></table>
<p>Usa las hojas CSV de <code>salida/</code> para filtrar por prioridad y sección.</p>
</div>
</body></html>"""
    path.write_text(html, encoding="utf-8")


def cruzar(google_path: Path, academico_path: Path, personal_path: Path | None, salida: Path, cfg: dict[str, Any]) -> None:
    excluir = {norm_estado(x) for x in cfg.get("estados_excluir", EXCLUIR_DEFAULT)}
    ou_personal = [str(x).lower() for x in cfg.get("ou_personal", [])]
    dias_inactiva = int(cfg.get("dias_inactiva", 90))
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    g_headers, g_rows = read_csv(google_path)
    a_headers, a_rows = read_csv(academico_path)
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
        academico = {campo: get(row, a_map[campo]) for campo in a_map}
        academico.pop("email", None)
        # Toda columna académica original
        academico["_todas"] = dict(row)
        f["academico"] = academico

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

    n_google = sum(1 for r in planos if r["en_google"] == "SI")
    n_acad = sum(1 for r in planos if r["en_academico"] == "SI")
    n_match = sum(1 for r in planos if r["perfil"] == "ESTUDIANTE_VIGENTE")
    n_sin = sum(1 for r in planos if r["tiene_2fa"] == "NO")
    n_con = sum(1 for r in planos if r["tiene_2fa"] == "SI")
    cobertura = round(100 * n_con / n_google, 1) if n_google else 0
    perfiles = dict(Counter(r["perfil"] for r in planos))
    resumen = {
        "generado": datetime.now().isoformat(timespec="seconds"),
        "n_google": n_google,
        "n_academico": n_acad,
        "n_match_estudiante": n_match,
        "n_sin_2fa": n_sin,
        "cobertura_2fa": cobertura,
        "perfiles": perfiles,
        "graduados_filtrados_en_academico": skipped_grad,
        "mapeo_google": g_map,
        "mapeo_academico": a_map,
        "mapeo_personal": p_map,
    }
    (salida / "resumen.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8")
    html_report(salida / "resumen.html", resumen, fac)

    print("Listo →", salida.resolve())
    print(f"Google: {n_google} | Académico vigente: {n_acad} | Match estudiante: {n_match}")
    print(f"Sin 2FA: {n_sin} | Cobertura 2FA sobre Google: {cobertura}%")
    print(f"Graduados filtrados del CSV académico: {skipped_grad}")
    print("Columnas Google detectadas:", {k: v for k, v in g_map.items() if v})
    print("Columnas académico detectadas:", {k: v for k, v in a_map.items() if v})


def main() -> None:
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Cruce Google Admin × académico (2FA y ficha institucional)")
    ap.add_argument("--google", type=Path)
    ap.add_argument("--academico", type=Path)
    ap.add_argument("--personal", type=Path, help="CSV opcional de docentes/administrativos (GH/nómina)")
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--config", type=Path, default=root / "config.yaml")
    ap.add_argument("--ejemplo", action="store_true", help="Corre con CSV de entrada/_ejemplos")
    args = ap.parse_args()
    cfg = load_config(args.config if args.config.exists() else root / "config.example.yaml")

    if args.ejemplo:
        base = root / "entrada" / "_ejemplos"
        cruzar(
            base / "google_admin.csv",
            base / "academico.csv",
            base / "personal.csv",
            args.salida or root / "salida",
            cfg,
        )
        return
    if not args.google or not args.academico:
        ap.error("Indica --google y --academico, o usa --ejemplo")
    cruzar(
        args.google,
        args.academico,
        args.personal,
        args.salida or root / "salida",
        cfg,
    )


if __name__ == "__main__":
    main()
