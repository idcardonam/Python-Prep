#!/usr/bin/env python3
"""Genera hoja de vida replicando el diseño original de Ivan Cardona."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "fonts"
OUTPUT_DIR = BASE_DIR.parent / "cv_output"

PAGE_W, PAGE_H = letter
SIDEBAR_X = 8.5
SIDEBAR_W = 194
SIDEBAR_COLOR = colors.Color(0.639, 0.694, 0.706)
MAIN_X = 229.5
MAIN_W = PAGE_W - MAIN_X - 18
SIDEBAR_TEXT_X = 41.5

pdfmetrics.registerFont(TTFont("Raleway", str(FONTS_DIR / "Raleway-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Raleway-Bold", str(FONTS_DIR / "Raleway-Bold.ttf")))


def load_profile(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def wrap_text(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
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


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_w: float,
    font: str = "Raleway",
    size: float = 11,
    leading: float = 14.5,
    bold_prefix: str | None = None,
) -> float:
    lines = wrap_text(c, text, font, size, max_w)
    for line in lines:
        if bold_prefix and line.startswith(bold_prefix):
            c.setFont("Raleway-Bold", size)
            c.drawString(x, y, bold_prefix)
            rest_x = x + c.stringWidth(bold_prefix, "Raleway-Bold", size)
            c.setFont(font, size)
            c.drawString(rest_x, y, line[len(bold_prefix) :])
        else:
            c.setFont(font, size)
            c.drawString(x, y, line)
        y -= leading
    return y


def draw_centered(c: canvas.Canvas, text: str, y: float, font: str, size: float) -> float:
    c.setFont(font, size)
    text_w = c.stringWidth(text, font, size)
    x = MAIN_X + (MAIN_W - text_w) / 2
    c.drawString(x, y, text)
    return y - size - 4


def draw_spaced_title(c: canvas.Canvas, text: str, y: float, size: float = 17) -> float:
    spaced = " ".join(text.upper())
    c.setFont("Raleway-Bold", size)
    text_w = c.stringWidth(spaced, "Raleway-Bold", size)
    x = MAIN_X + (MAIN_W - text_w) / 2
    c.drawString(x, y, spaced)
    return y - size - 8


def draw_sidebar_title(c: canvas.Canvas, title: str, y: float) -> float:
    c.setFillColor(colors.white)
    size = 14
    max_width = SIDEBAR_W - (SIDEBAR_TEXT_X - SIDEBAR_X) - 8
    while c.stringWidth(title.upper(), "Raleway-Bold", size) > max_width and size > 9:
        size -= 0.5
    c.setFont("Raleway-Bold", size)
    c.drawString(SIDEBAR_TEXT_X, y, title.upper())
    return y - 18


def draw_sidebar_skills(c: canvas.Canvas, items: list[str], y: float) -> float:
    c.setFont("Raleway", 10.5)
    for item in items:
        c.drawString(SIDEBAR_TEXT_X + 2, y, item)
        y -= 16.5
    return y


def draw_sidebar_training(c: canvas.Canvas, items: list[dict], y: float) -> float:
    for item in items:
        c.setFont("Raleway-Bold", 10.5)
        for line in wrap_text(c, item["titulo"], "Raleway-Bold", 10.5, SIDEBAR_W - 55):
            c.drawString(SIDEBAR_TEXT_X, y, line)
            y -= 13
        c.setFont("Raleway", 9.5)
        c.drawString(SIDEBAR_TEXT_X, y, f"{item['institucion']} | {item['periodo']}")
        y -= 15
    return y


def draw_contact_icon(c: canvas.Canvas, cx: float, cy: float, label: str) -> None:
    c.setFillColor(colors.Color(0.33, 0.33, 0.33))
    c.circle(cx, cy, 8.5, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Raleway-Bold", 6)
    c.drawCentredString(cx, cy - 2, label)


def generate_pdf(profile: dict, output_path: Path, photo_path: Path | None = None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=letter)

    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(SIDEBAR_COLOR)
    c.roundRect(SIDEBAR_X, 8.5, SIDEBAR_W, PAGE_H - 17, 6, fill=1, stroke=0)

    photo = photo_path or BASE_DIR / "img_0.jpeg"
    if photo.exists():
        photo_size = 118
        photo_x = SIDEBAR_X + (SIDEBAR_W - photo_size) / 2
        photo_y = PAGE_H - 145
        c.saveState()
        path = c.beginPath()
        r = 10
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

    c.setFillColor(colors.HexColor("#2B2B2B"))

    y = PAGE_H - 18
    y = draw_centered(c, profile["nombre"], y, "Raleway-Bold", 28)
    y_title = draw_spaced_title(c, profile["titulo"], y - 2, 16)

    c.setStrokeColor(SIDEBAR_COLOR)
    c.setLineWidth(1)
    c.line(MAIN_X, y_title - 6, PAGE_W - 18, y_title - 6)

    y_profile = y_title - 18
    profile_text = " ".join(profile["perfil"].split())
    y_profile = draw_wrapped(c, profile_text, MAIN_X, y_profile, MAIN_W, "Raleway", 10.3, 12.7)

    y_exp_title = y_profile - 5
    c.setFont("Raleway-Bold", 15)
    c.drawString(MAIN_X, y_exp_title, "EXPERIENCIA LABORAL")

    y_job = y_exp_title - 17
    for exp in profile["experiencia"]:
        c.setFont("Raleway-Bold", 12)
        c.drawString(MAIN_X + 0.4, y_job, exp["cargo"])
        y_job -= 12.5
        c.setFont("Raleway-Bold", 11)
        c.drawString(MAIN_X, y_job, f"{exp['empresa']} | {exp['periodo']}")
        y_job -= 12.5
        if exp.get("rol"):
            c.setFont("Raleway", 11)
            c.drawString(MAIN_X, y_job, exp["rol"])
            y_job -= 12.5
        c.setFont("Raleway", 10.5)
        for bullet in exp["bullets"]:
            for line in wrap_text(c, bullet, "Raleway", 10.5, MAIN_W):
                c.drawString(MAIN_X, y_job, line)
                y_job -= 11.7
        y_job -= 1.5

    y_edu = y_job - 1
    c.setFont("Raleway-Bold", 14)
    c.drawString(MAIN_X, y_edu, "FORMACIÓN ACADÉMICA")
    y_edu -= 15
    for edu in profile["formacion_academica"]:
        c.setFont("Raleway-Bold", 11.5)
        c.drawString(MAIN_X, y_edu, edu["titulo"])
        y_edu -= 12.5
        c.setFont("Raleway", 10.5)
        c.drawString(MAIN_X, y_edu, f"{edu['institucion']} | {edu['periodo']}")
        y_edu -= 12.5

    y_contact = PAGE_H - 238
    y_contact = draw_sidebar_title(c, "CONTACTO", y_contact)
    contact = profile["contacto"]
    draw_contact_icon(c, 50, y_contact - 2, "T")
    c.setFont("Raleway", 11)
    c.drawString(66, y_contact - 5, contact["telefono"])
    y_contact -= 24
    draw_contact_icon(c, 50, y_contact - 2, "@")
    c.drawString(66, y_contact - 5, contact["email"])
    y_contact -= 24
    draw_contact_icon(c, 50, y_contact - 2, "in")
    for line in wrap_text(c, contact["linkedin"], "Raleway", 11, SIDEBAR_W - 55):
        c.drawString(66, y_contact - 5, line)
        y_contact -= 14
    y_contact -= 10

    y_contact = draw_sidebar_title(c, "CONOCIMIENTOS", PAGE_H - 395)
    y_contact = draw_sidebar_skills(c, profile["conocimientos"], y_contact - 3)

    y_contact = draw_sidebar_title(c, "FORMACIÓN COMPLEMENTARIA", PAGE_H - 592)
    draw_sidebar_training(c, profile["formacion_complementaria"], y_contact)

    c.setFont("Raleway-Bold", 13.5)
    c.drawString(SIDEBAR_TEXT_X, 20, profile.get("referencias", "Referencias a solicitud"))

    c.showPage()
    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar hoja de vida PDF")
    parser.add_argument("--perfil", type=Path, default=BASE_DIR / "perfil_base.yaml")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    profile = load_profile(args.perfil)
    output = args.output or OUTPUT_DIR / "HV_Ivan_David_Cardona.pdf"
    generate_pdf(profile, output)
    print(f"PDF generado: {output}")


if __name__ == "__main__":
    main()
