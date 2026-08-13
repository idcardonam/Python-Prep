#!/usr/bin/env python3
"""HV A4 en el estilo original (barra lateral + foto redondeada)."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
PHOTO = ROOT / "foto_ivan.png"
PDF_OUT = ROOT / "HV_Ivan_David_Cardona_Mendoza.pdf"

pdfmetrics.registerFont(TTFont("Inter", "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Med", "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Semi", "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))

SLATE = HexColor("#A3B1B4")
INK = HexColor("#545454")
HEAD = HexColor("#3D3D3D")
NAME = HexColor("#5A5A5A")
MUTED = HexColor("#6A6A6A")
ICON_BG = HexColor("#545454")


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


def draw_text(c, text, x, y, font, size, max_w, leading, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(c, text, font, size, max_w):
        c.drawString(x, y, line)
        y -= leading
    return y


def section(c, title, x, y, color=HEAD, max_w=None):
    c.setFillColor(color)
    c.setFont("Inter-Bold", 10)
    label = title.upper()
    if max_w:
        return draw_text(c, label, x, y, "Inter-Bold", 10, max_w, 12.4, color) - 4
    c.drawString(x, y, label)
    return y - 16


def icon_circle(c, x, y, r=6.2):
    c.setFillColor(ICON_BG)
    c.circle(x, y, r, fill=1, stroke=0)
    return r


def icon_phone(c, cx, cy):
    r = icon_circle(c, cx, cy)
    c.setStrokeColor(white)
    c.setLineWidth(0.9)
    c.setLineCap(1)
    # simple handset
    c.arc(cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2, 200, 140)
    c.setFillColor(white)
    c.circle(cx - 2.1, cy - 1.6, 0.7, fill=1, stroke=0)
    c.circle(cx + 2.1, cy + 1.6, 0.7, fill=1, stroke=0)


def icon_mail(c, cx, cy):
    icon_circle(c, cx, cy)
    c.setStrokeColor(white)
    c.setFillColor(white)
    c.setLineWidth(0.8)
    w, h = 7.2, 5.0
    x, y = cx - w / 2, cy - h / 2
    c.rect(x, y, w, h, fill=0, stroke=1)
    c.line(x, y + h, cx, cy - 0.2)
    c.line(cx, cy - 0.2, x + w, y + h)


def icon_in(c, cx, cy):
    icon_circle(c, cx, cy)
    c.setFillColor(white)
    c.setFont("Inter-Bold", 6.2)
    c.drawCentredString(cx, cy - 2.2, "in")


def contact_row(c, icon_fn, text, x, y, max_w):
    icon_fn(c, x + 6.4, y + 2.4)
    return draw_text(c, text, x + 18, y, "Inter", 7.6, max_w - 18, 10, INK) - 6


def bullet(c, text, x, y, max_w, size=8.0, leading=10.4):
    c.setFillColor(INK)
    c.circle(x + 2.0, y + 2.4, 1.35, fill=1, stroke=0)
    return draw_text(c, text, x + 10, y, "Inter", size, max_w - 10, leading, INK) - 1.6


def build():
    page_w, page_h = A4
    c = canvas.Canvas(str(PDF_OUT), pagesize=A4)
    c.setTitle("Hoja de vida — Iván David Cardona Mendoza")
    c.setAuthor("Iván David Cardona Mendoza")

    # left margin + sidebar
    left_m = 14
    side_w = 188
    side_x = left_m
    c.setFillColor(SLATE)
    c.rect(side_x, 0, side_w, page_h, fill=1, stroke=0)

    # photo
    photo_pad = 16
    photo_w = side_w - 2 * photo_pad
    photo_h = photo_w * (734 / 644)
    photo_y = page_h - 18 - photo_h
    c.drawImage(
        ImageReader(str(PHOTO)),
        side_x + photo_pad,
        photo_y,
        width=photo_w,
        height=photo_h,
        mask="auto",
        preserveAspectRatio=True,
        anchor="c",
    )

    sx = side_x + 16
    sw = side_w - 32
    y = photo_y - 22

    y = section(c, "Contacto", sx, y, max_w=sw)
    y = contact_row(c, icon_phone, "304 558 7767", sx, y, sw)
    y = contact_row(c, icon_mail, "idcm@hotmail.es", sx, y, sw)
    y = contact_row(c, icon_in, "https://n9.cl/lajpr", sx, y, sw)
    y -= 8

    y = section(c, "Conocimientos", sx, y, max_w=sw)
    skills = [
        "Coordinación operativa",
        "Gestión de proyectos",
        "Procesos internos",
        "Políticas de seguridad",
        "Gestión de riesgos",
        "ITIL  ·  Scrum",
        "ISO 27001  ·  COBIT",
        "NIST  ·  GDPR",
        "SQL  ·  bases de datos",
        "Excel  ·  Power BI",
        "Python  ·  PHP",
    ]
    for s in skills:
        c.setFillColor(INK)
        c.circle(sx + 2.2, y + 2.6, 1.4, fill=1, stroke=0)
        c.setFont("Inter", 8.0)
        c.drawString(sx + 10, y, s)
        y -= 13.2
    y -= 8

    y = section(c, "Formación complementaria", sx, y, max_w=sw)
    comps = [
        ("Auditor interno ISO/IEC 27001:2022 (32 h)", "SGS Academy  |  2023"),
        ("Auditor interno en sistemas integrados (32 h)", "Eidec  |  2022"),
        ("Sistemas integrados de gestión (120 h)", "Eidec  |  2022"),
    ]
    for title, sub in comps:
        y = draw_text(c, title, sx, y, "Inter-Semi", 7.5, sw, 9.6, HEAD)
        y = draw_text(c, sub, sx, y + 1, "Inter", 7.1, sw, 9.2, MUTED)
        y -= 8

    y -= 6
    y = section(c, "Idiomas", sx, y, max_w=sw)
    y = draw_text(c, "Español: nativo", sx, y, "Inter", 8.0, sw, 11, INK)
    y = draw_text(c, "Inglés: lectura técnica", sx, y, "Inter", 8.0, sw, 11, INK)
    y -= 10
    y = draw_text(c, "Disponible para Bucaramanga", sx, y, "Inter-Med", 7.6, sw, 10, HEAD)

    c.setFillColor(HEAD)
    c.setFont("Inter-Med", 7.4)
    c.drawString(sx, 18, "Referencias a solicitud")

    # MAIN COLUMN
    mx = side_x + side_w + 22
    mw = page_w - mx - 22
    y = page_h - 42

    c.setFillColor(NAME)
    c.setFont("Inter-Bold", 22)
    c.drawString(mx, y, "IVAN DAVID CARDONA")
    y -= 18
    c.setFont("Inter-Bold", 11)
    c.setFillColor(HEAD)
    c.drawString(mx, y, "INGENIERO DE SISTEMAS")
    y -= 13
    c.setFont("Inter-Med", 8.4)
    c.setFillColor(MUTED)
    c.drawString(mx, y, "Coordinación de operaciones, proyectos y procesos")
    y -= 22

    perfil = (
        "Ingeniero de Sistemas y Especialista en Seguridad Informática con más de 6 años "
        "articulando planeación operativa, estructuración de procesos internos, gestión de "
        "riesgos y seguimiento de controles para el cumplimiento de metas institucionales. "
        "Experiencia coordinando trabajo con distintas áreas, implementando políticas de "
        "seguridad y mejorando el desempeño diario mediante indicadores, documentación y "
        "sostenibilidad de procesos. Orientado a la gestión de proyectos en curso, la "
        "operación confiable y la toma de decisiones con información."
    )
    y = draw_text(c, perfil, mx, y, "Inter", 8.35, mw, 11.2, INK)
    y -= 16

    y = section(c, "Experiencia laboral", mx, y)

    jobs = [
        (
            "ANALISTA TIC",
            "Organización Servicios y Asesorías  |  Marzo 2025 - Junio 2026",
            [
                "Analista de soporte y seguridad informática: coordinación del soporte operativo a usuarios y seguimiento de incidentes para continuidad de la operación diaria.",
                "Implementación de políticas de seguridad y controles en desarrollos TIC, alineando el trabajo técnico con las reglas internas.",
                "Optimización de procesos de nómina y contabilidad con automatizaciones (Python, React) y macros avanzadas.",
                "Análisis de datos e integración de sistemas para respaldar la toma de decisiones de coordinación.",
            ],
        ),
        (
            "Profesional Auditorías Tecnología de la Información",
            "Financiera Comultrasan  |  Sep 2023 - Ene 2025",
            [
                "Planeación y ejecución de auditorías internas de TI, con cronograma, alcance, evidencias y seguimiento hasta el cierre de hallazgos.",
                "Gestión de riesgos de TI y evaluación de controles internos para sostener procesos y cumplimiento normativo.",
                "Análisis y gestión de bases de datos; elaboración de macros e indicadores de seguimiento.",
                "Ciberseguridad, pruebas de rendimiento y articulación de resultados con las áreas auditadas.",
            ],
        ),
        (
            "Ingeniero de Sistemas / Auditor Interno",
            "Constructodo de la Guajira S.A.S  |  Nov 2019 - May 2023",
            [
                "Planeación estratégica y estructuración de procesos internos para ordenar la operación y el cumplimiento de objetivos.",
                "Análisis de riesgos y creación de políticas de seguridad, con enfoque de prevención y mejora del desempeño cotidiano.",
                "Elaboración de métricas e informes de seguimiento para estrategias comerciales y toma de decisiones de coordinación.",
            ],
        ),
    ]
    for title, org, bullets in jobs:
        c.setFillColor(HEAD)
        c.setFont("Inter-Bold", 9.2)
        c.drawString(mx, y, title)
        y -= 12
        c.setFillColor(MUTED)
        c.setFont("Inter", 7.8)
        c.drawString(mx, y, org)
        y -= 13
        for b in bullets:
            y = bullet(c, b, mx, y, mw, size=8.05, leading=10.5)
        y -= 8

    y -= 2
    y = section(c, "Formación académica", mx, y)
    edu = [
        ("Especialista en Seguridad Informática", "Corporación Universitaria Minuto de Dios  |  2023"),
        ("Ingeniero de Sistemas  ·  TP vigente", "Universidad Popular del César  |  2022"),
        ("Técnico en Análisis y Desarrollo de Sistemas", "Uparsistem  |  2014"),
    ]
    for title, sub in edu:
        c.setFillColor(HEAD)
        c.setFont("Inter-Bold", 8.8)
        c.drawString(mx, y, title)
        y -= 11.5
        c.setFillColor(MUTED)
        c.setFont("Inter", 7.7)
        c.drawString(mx, y, sub)
        y -= 16

    c.showPage()
    c.save()
    print(f"PDF: {PDF_OUT}")


if __name__ == "__main__":
    build()
