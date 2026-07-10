#!/usr/bin/env python3
"""Genera hoja de vida en PDF replicando el diseño original."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "cv_output"

# Colores del diseño original
SIDEBAR_COLOR = colors.HexColor("#8FA3AD")
SIDEBAR_TEXT = colors.white
MAIN_TEXT = colors.HexColor("#2B2B2B")
MUTED_TEXT = colors.HexColor("#4A4A4A")
ACCENT_LINE = colors.HexColor("#8FA3AD")

PAGE_W, PAGE_H = A4
SIDEBAR_W = 62 * mm
MARGIN_TOP = 18 * mm
MARGIN_RIGHT = 14 * mm
CONTENT_LEFT = SIDEBAR_W + 10 * mm
CONTENT_W = PAGE_W - CONTENT_LEFT - MARGIN_RIGHT


def load_profile(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def draw_sidebar_section_title(c: canvas.Canvas, y: float, title: str) -> float:
    c.setFillColor(SIDEBAR_TEXT)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(8 * mm, y, title.upper())
    return y - 5 * mm


def draw_sidebar_bullets(c: canvas.Canvas, y: float, items: list[str], font_size: float = 8) -> float:
    c.setFillColor(SIDEBAR_TEXT)
    c.setFont("Helvetica", font_size)
    x = 10 * mm
    line_h = font_size + 3
    max_w = SIDEBAR_W - 14 * mm

    for item in items:
        words = item.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if c.stringWidth(test, "Helvetica", font_size) <= max_w:
                line = test
            else:
                if line:
                    c.drawString(x, y, f"• {line}")
                    y -= line_h
                line = word
        if line:
            c.drawString(x, y, f"• {line}")
            y -= line_h
    return y - 2 * mm


def draw_sidebar_training(c: canvas.Canvas, y: float, items: list[dict]) -> float:
    c.setFillColor(SIDEBAR_TEXT)
    for item in items:
        c.setFont("Helvetica-Bold", 7.5)
        title = item["titulo"]
        wrapped = _wrap_text(c, title, "Helvetica-Bold", 7.5, SIDEBAR_W - 14 * mm)
        for line in wrapped:
            c.drawString(8 * mm, y, line)
            y -= 9
        c.setFont("Helvetica", 7.5)
        detail = f"{item['institucion']} | {item['periodo']}"
        c.drawString(8 * mm, y, detail)
        y -= 11
    return y


def _wrap_text(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if c.stringWidth(test, font, size) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(c: canvas.Canvas, text: str, x: float, y: float, width: float, style: ParagraphStyle) -> float:
    p = Paragraph(text.replace("\n", " ").strip(), style)
    w, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    return y - h


def generate_pdf(profile: dict, output_path: Path, photo_path: Path | None = None) -> None:
    c = canvas.Canvas(str(output_path), pagesize=A4)

    # Fondo sidebar
    c.setFillColor(SIDEBAR_COLOR)
    c.rect(0, 0, SIDEBAR_W, PAGE_H, fill=1, stroke=0)

    # Foto de perfil
    photo = photo_path or BASE_DIR / "img_0.jpeg"
    if photo.exists():
        photo_size = 42 * mm
        photo_x = (SIDEBAR_W - photo_size) / 2
        photo_y = PAGE_H - MARGIN_TOP - photo_size
        c.saveState()
        path = c.beginPath()
        r = 4 * mm
        x, y, w, h = photo_x, photo_y, photo_size, photo_size
        path.moveTo(x + r, y)
        path.lineTo(x + w - r, y)
        path.arcTo(x + w - 2 * r, y, x + w, y + 2 * r, startAng=270, extent=90)
        path.lineTo(x + w, y + h - r)
        path.arcTo(x + w - 2 * r, y + h - 2 * r, x + w, y + h, startAng=0, extent=90)
        path.lineTo(x + r, y + h)
        path.arcTo(x, y + h - 2 * r, x + 2 * r, y + h, startAng=90, extent=90)
        path.lineTo(x, y + r)
        path.arcTo(x, y, x + 2 * r, y + 2 * r, startAng=180, extent=90)
        path.close()
        c.clipPath(path, stroke=0)
        c.drawImage(str(photo), x, y, width=w, height=h, preserveAspectRatio=True, anchor="c")
        c.restoreState()

    y = PAGE_H - MARGIN_TOP - 48 * mm

    # Contacto
    y = draw_sidebar_section_title(c, y, "CONTACTO")
    y -= 2 * mm
    contact = profile["contacto"]
    for icon, value in [("☎", contact["telefono"]), ("✉", contact["email"]), ("in", contact["linkedin"])]:
        c.setFillColor(SIDEBAR_TEXT)
        c.circle(10 * mm, y + 1.5, 3.5, fill=1, stroke=0)
        c.setFillColor(SIDEBAR_COLOR)
        c.setFont("Helvetica-Bold", 5.5)
        c.drawCentredString(10 * mm, y, icon[:2])
        c.setFillColor(SIDEBAR_TEXT)
        c.setFont("Helvetica", 7.5)
        wrapped = _wrap_text(c, value, "Helvetica", 7.5, SIDEBAR_W - 18 * mm)
        for i, line in enumerate(wrapped):
            c.drawString(15 * mm, y - i * 9, line)
        y -= max(11, len(wrapped) * 9 + 2)

    y -= 4 * mm
    y = draw_sidebar_section_title(c, y, "CONOCIMIENTOS")
    y = draw_sidebar_bullets(c, y, profile["conocimientos"])

    y -= 2 * mm
    y = draw_sidebar_section_title(c, y, "FORMACIÓN COMPLEMENTARIA")
    y = draw_sidebar_training(c, y, profile["formacion_complementaria"])

    c.setFillColor(SIDEBAR_TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(8 * mm, 12 * mm, profile.get("referencias", "Referencias a solicitud"))

    # Contenido principal
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "Name",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=24,
        textColor=MAIN_TEXT,
        alignment=TA_LEFT,
    )
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=MUTED_TEXT,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13,
        textColor=MAIN_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=12,
        textColor=MUTED_TEXT,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        textColor=MAIN_TEXT,
        alignment=TA_LEFT,
        spaceBefore=6,
        spaceAfter=4,
    )
    job_title_style = ParagraphStyle(
        "JobTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=MAIN_TEXT,
    )
    job_meta_style = ParagraphStyle(
        "JobMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=MUTED_TEXT,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.3,
        leading=11.5,
        textColor=MAIN_TEXT,
        leftIndent=8,
        bulletIndent=0,
        bulletFontName="Helvetica",
        bulletFontSize=8.3,
        alignment=TA_JUSTIFY,
    )

    y_main = PAGE_H - MARGIN_TOP
    c.setFillColor(MAIN_TEXT)
    y_main = draw_paragraph(c, profile["nombre"], CONTENT_LEFT, y_main, CONTENT_W, name_style)
    y_main = draw_paragraph(c, profile["titulo"], CONTENT_LEFT, y_main - 2 * mm, CONTENT_W, title_style)
    if profile.get("subtitulo"):
        y_main = draw_paragraph(c, profile["subtitulo"], CONTENT_LEFT, y_main - 1 * mm, CONTENT_W, subtitle_style)

    c.setStrokeColor(ACCENT_LINE)
    c.setLineWidth(0.8)
    c.line(CONTENT_LEFT, y_main - 4 * mm, PAGE_W - MARGIN_RIGHT, y_main - 4 * mm)
    y_main -= 10 * mm

    y_main = draw_paragraph(c, profile["perfil"], CONTENT_LEFT, y_main, CONTENT_W, body_style)
    y_main -= 4 * mm

    y_main = draw_paragraph(c, "EXPERIENCIA LABORAL", CONTENT_LEFT, y_main, CONTENT_W, section_style)

    for exp in profile["experiencia"]:
        header = f"<b>{exp['cargo']}</b> | {exp['empresa']} | {exp['periodo']}"
        y_main = draw_paragraph(c, header, CONTENT_LEFT, y_main, CONTENT_W, job_meta_style)
        if exp.get("rol"):
            y_main = draw_paragraph(c, exp["rol"], CONTENT_LEFT, y_main, CONTENT_W, job_title_style)
        for bullet in exp["bullets"]:
            y_main = draw_paragraph(c, f"• {bullet}", CONTENT_LEFT, y_main, CONTENT_W, bullet_style)
        y_main -= 2 * mm

    y_main = draw_paragraph(c, "FORMACIÓN ACADÉMICA", CONTENT_LEFT, y_main, CONTENT_W, section_style)
    for edu in profile["formacion_academica"]:
        line = f"<b>{edu['titulo']}</b><br/>{edu['institucion']} | {edu['periodo']}"
        y_main = draw_paragraph(c, line, CONTENT_LEFT, y_main, CONTENT_W, job_meta_style)
        y_main -= 1 * mm

    c.showPage()
    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar hoja de vida PDF")
    parser.add_argument(
        "--perfil",
        type=Path,
        default=BASE_DIR / "perfil_base.yaml",
        help="Archivo YAML con el perfil (base o adaptado)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Ruta del PDF de salida",
    )
    args = parser.parse_args()

    profile = load_profile(args.perfil)
    output = args.output or OUTPUT_DIR / "HV_Ivan_David_Cardona.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_pdf(profile, output)
    print(f"PDF generado: {output}")


if __name__ == "__main__":
    main()
