#!/usr/bin/env python3
"""HV de 1 página — Coordinador/a de Operaciones (Comfenalco)."""

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT_DIR = Path(__file__).resolve().parent
PDF_OUT = OUT_DIR / "HV_Ivan_David_Cardona_Mendoza_Coordinador_Operaciones.pdf"

NAVY = HexColor("#1B3A4B")
TEAL = HexColor("#2A6F7F")
GOLD = HexColor("#C4A35A")
INK = HexColor("#1F2933")
MUTED = HexColor("#5B6770")
LINE = HexColor("#D7DEE3")
BG_SIDE = HexColor("#F4F7F8")


def wrap(c, text, font, size, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(c, text, x, y, font, size, max_w, leading, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap(c, text, font, size, max_w)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def section_title(c, text, x, y, w):
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 11)
    c.drawString(x, y, text.upper())
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(x, y - 3, x + w, y - 3)
    return y - 14


def bullet(c, text, x, y, max_w, size=8.4, leading=10.4):
    c.setFillColor(TEAL)
    c.circle(x + 2.2, y + 2.2, 1.5, fill=1, stroke=0)
    y = draw_wrapped(c, text, x + 10, y, "Times-Roman", size, max_w - 10, leading, INK)
    return y - 2.2


def job_header(c, role, company, dates, x, y, max_w):
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 9.4)
    c.drawString(x, y, role)
    c.setFillColor(TEAL)
    c.setFont("Times-Italic", 8.2)
    date_w = c.stringWidth(dates, "Times-Italic", 8.2)
    c.drawRightString(x + max_w, y, dates)
    y -= 12
    c.setFillColor(MUTED)
    c.setFont("Times-Roman", 8.3)
    c.drawString(x, y, company)
    return y - 12


def build():
    page_w, page_h = letter
    c = canvas.Canvas(str(PDF_OUT), pagesize=letter)
    c.setTitle("Hoja de vida — Iván David Cardona Mendoza")
    c.setAuthor("Iván David Cardona Mendoza")
    c.setSubject("Coordinador de Operaciones")

    # Header bar
    c.setFillColor(NAVY)
    c.rect(0, page_h - 78, page_w, 78, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, page_h - 82, page_w, 4, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Times-Bold", 20)
    c.drawString(0.55 * inch, page_h - 36, "IVÁN DAVID CARDONA MENDOZA")
    c.setFont("Times-Roman", 10.5)
    c.setFillColor(HexColor("#E8EEF0"))
    c.drawString(
        0.55 * inch,
        page_h - 54,
        "Ingeniero de Sistemas  ·  Coordinación de operaciones, proyectos y procesos",
    )
    c.setFont("Times-Roman", 8.3)
    c.drawString(
        0.55 * inch,
        page_h - 70,
        "304 558 7767   ·   idcm@hotmail.es   ·   TP vigente   ·   https://n9.cl/lajpr",
    )

    left_x = 0.52 * inch
    right_x = 5.55 * inch
    y = page_h - 102
    col_w = 4.85 * inch
    side_w = 2.35 * inch

    # PERFIL
    y = section_title(c, "Perfil profesional", left_x, y, col_w)
    perfil = (
        "Ingeniero de Sistemas y Especialista en Seguridad Informática con más de 6 años "
        "articulando planeación operativa, estructuración de procesos internos, gestión de "
        "riesgos y seguimiento de controles para el cumplimiento de metas institucionales. "
        "Experiencia coordinando trabajo con distintas áreas, implementando políticas de "
        "seguridad y mejorando el desempeño diario mediante indicadores, documentación y "
        "sostenibilidad de procesos. Orientado a la gestión de proyectos en curso, la "
        "operación confiable y la toma de decisiones con información."
    )
    y = draw_wrapped(c, perfil, left_x, y, "Times-Roman", 8.6, col_w, 11.2, INK)
    y -= 10

    # EXPERIENCIA
    y = section_title(c, "Experiencia laboral", left_x, y, col_w)

    y = job_header(
        c,
        "Analista de soporte y seguridad informática",
        "Organización Servicios y Asesorías",
        "Mar. 2025 – Jun. 2026",
        left_x,
        y,
        col_w,
    )
    for t in [
        "Coordiné el soporte operativo de aplicaciones y usuarios, dando seguimiento a incidentes y asegurando continuidad de la operación diaria.",
        "Implementé políticas de seguridad y controles en los desarrollos TIC, alineando el trabajo técnico con las reglas internas de la organización.",
        "Optimicé procesos de nómina y contabilidad con automatizaciones y macros, reduciendo retrabajo y mejorando el desempeño de áreas de apoyo.",
        "Integré información entre sistemas para respaldar la toma de decisiones de coordinación y el seguimiento de resultados.",
    ]:
        y = bullet(c, t, left_x, y, col_w)
    y -= 6

    y = job_header(
        c,
        "Profesional de auditorías de tecnología de la información",
        "Financiera Comultrasan",
        "Sep. 2023 – Ene. 2025",
        left_x,
        y,
        col_w,
    )
    for t in [
        "Planifiqué y ejecuté auditorías internas de TI, con cronograma, alcance, evidencias y reportes de seguimiento hasta el cierre de hallazgos.",
        "Hice gestión de riesgos y evaluación de controles internos, proponiendo acciones correctivas para que los procesos se mantuvieran sostenibles.",
        "Hice seguimiento a indicadores de control, ciberseguridad y cumplimiento normativo, articulando resultados con las áreas auditadas.",
        "Analicé bases de datos y construí macros de información para soportar decisiones operativas y de control.",
    ]:
        y = bullet(c, t, left_x, y, col_w)
    y -= 6

    y = job_header(
        c,
        "Ingeniero de sistemas / Auditor interno",
        "Constructodo de la Guajira S.A.S.",
        "Nov. 2019 – May. 2023",
        left_x,
        y,
        col_w,
    )
    for t in [
        "Participé en la planeación estratégica y en la estructuración de procesos internos para ordenar la operación y sostener el cumplimiento de objetivos.",
        "Elaboré políticas de seguridad y análisis de riesgos, con enfoque de prevención y mejora del desempeño cotidiano.",
        "Definí métricas e informes de seguimiento para estrategias comerciales y toma de decisiones de coordinación.",
        "Articulé trabajo técnico, control interno y áreas de la empresa para que los procesos operaran de forma documentada y medible.",
    ]:
        y = bullet(c, t, left_x, y, col_w)

    # SIDEBAR
    side_top = page_h - 88
    c.setFillColor(BG_SIDE)
    c.rect(right_x - 10, 0.42 * inch, side_w + 28, side_top - 0.42 * inch, fill=1, stroke=0)

    sx = right_x
    sy = page_h - 108
    sw = 2.28 * inch

    sy = section_title(c, "Formación", sx, sy, sw)
    blocks = [
        ("Especialista en Seguridad Informática", "Corporación Universitaria Minuto de Dios  ·  2023"),
        ("Ingeniero de Sistemas  ·  TP vigente", "Universidad Popular del César  ·  2022"),
        ("Técnico en Análisis y Desarrollo de Sistemas", "Uparsistem  ·  2014"),
    ]
    for title, sub in blocks:
        c.setFillColor(NAVY)
        c.setFont("Times-Bold", 8.1)
        for line in wrap(c, title, "Times-Bold", 8.1, sw):
            c.drawString(sx, sy, line)
            sy -= 10
        c.setFillColor(MUTED)
        c.setFont("Times-Roman", 7.5)
        for line in wrap(c, sub, "Times-Roman", 7.5, sw):
            c.drawString(sx, sy, line)
            sy -= 9.5
        sy -= 6

    sy -= 4
    sy = section_title(c, "Complementaria", sx, sy, sw)
    comps = [
        "Auditor interno ISO/IEC 27001:2022 — SGS Academy, 2023 (32 h)",
        "Auditor interno en sistemas integrados — Eidec, 2022 (32 h)",
        "Sistemas integrados de gestión — Eidec, 2022 (120 h)",
    ]
    for t in comps:
        c.setFillColor(TEAL)
        c.circle(sx + 2, sy + 2, 1.4, fill=1, stroke=0)
        sy = draw_wrapped(c, t, sx + 9, sy, "Times-Roman", 7.5, sw - 9, 9.4, INK)
        sy -= 4

    sy -= 6
    sy = section_title(c, "Competencias del cargo", sx, sy, sw)
    skills = [
        "Coordinación operativa y seguimiento de metas",
        "Gestión de proyectos y cronogramas",
        "Estructuración y sostenibilidad de procesos",
        "Políticas de seguridad y gestión de riesgos",
        "Articulación con áreas / comités",
        "Indicadores, reportes y documentación",
        "Soporte a usuarios e incidentes (ITIL)",
        "Scrum  ·  ISO 27001  ·  COBIT  ·  NIST",
        "SQL  ·  Excel  ·  Power BI  ·  bases de datos",
    ]
    for t in skills:
        c.setFillColor(TEAL)
        c.circle(sx + 2, sy + 2, 1.4, fill=1, stroke=0)
        sy = draw_wrapped(c, t, sx + 9, sy, "Times-Roman", 7.6, sw - 9, 9.6, INK)
        sy -= 3.2

    sy -= 8
    sy = section_title(c, "Idiomas y disponibilidad", sx, sy, sw)
    c.setFillColor(INK)
    c.setFont("Times-Roman", 8)
    c.drawString(sx, sy, "Español: nativo")
    sy -= 12
    c.drawString(sx, sy, "Inglés: lectura técnica")
    sy -= 14
    sy = draw_wrapped(
        c,
        "Disponible para vinculación en Bucaramanga.",
        sx,
        sy,
        "Times-Roman",
        7.6,
        sw,
        9.6,
        INK,
    )

    c.setFillColor(MUTED)
    c.setFont("Times-Roman", 7)
    c.drawCentredString(page_w / 2, 0.28 * inch, "Referencias a solicitud")

    c.showPage()
    c.save()
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    build()
