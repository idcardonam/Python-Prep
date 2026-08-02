#!/usr/bin/env python3
"""Genera PDF carta (8.5x11) con 8 stickers circulares - Batalla de Boyacá."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sticker-7-agosto-batalla-boyaca.png"
CIRCLE = ROOT / "sticker-7-agosto-circular.png"
PDF_OUT = ROOT / "hoja_8_stickers_batalla_boyaca_carta.pdf"
PREVIEW_OUT = ROOT / "preview_hoja_8_stickers.png"


def make_circular_sticker(src: Path, dst: Path, size: int = 1600) -> Path:
    """Recorta el sticker a un círculo limpio con fondo transparente."""
    img = Image.open(src).convert("RGBA")

    # Recortar márgenes blancos alrededor del círculo
    alpha_proxy = img.convert("RGB")
    bg = alpha_proxy.getpixel((0, 0))
    mask_bg = Image.new("RGB", img.size, bg)
    diff = ImageChops_difference(alpha_proxy, mask_bg)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)

    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Máscara circular anti-alias
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((1, 1, size - 2, size - 2), fill=255)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0))
    out.putalpha(mask)
    out.save(dst, "PNG")
    return dst


def ImageChops_difference(a: Image.Image, b: Image.Image) -> Image.Image:
    from PIL import ImageChops

    return ImageChops.difference(a, b)


def build_pdf(circle_png: Path, pdf_path: Path) -> None:
    page_w, page_h = letter  # 612 x 792 pt

    cols, rows = 2, 4
    margin_x = 0.45 * inch
    margin_y = 0.35 * inch
    gutter_x = 0.30 * inch
    gutter_y = 0.22 * inch

    usable_w = page_w - (2 * margin_x) - gutter_x
    usable_h = page_h - (2 * margin_y) - ((rows - 1) * gutter_y)
    diameter = min(usable_w / cols, usable_h / rows)

    # Centrar la grilla en la página
    grid_w = cols * diameter + gutter_x
    grid_h = rows * diameter + (rows - 1) * gutter_y
    origin_x = (page_w - grid_w) / 2
    origin_y = (page_h - grid_h) / 2

    sticker = ImageReader(str(circle_png))

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setTitle("Stickers 7 de Agosto - Batalla de Boyacá")
    c.setAuthor("Batalla de Boyacá Stickers")
    c.setSubject("Hoja imprimible carta - 8 stickers")
    c.setCreator("generar_hoja_stickers.py")

    # Permisos: imprimir sí; modificar/anotar no (PDF "tipo seguridad")
    encrypt = StandardEncryption(
        userPassword="",
        ownerPassword="batalla-boyaca-print-lock",
        canPrint=1,
        canModify=0,
        canCopy=1,
        canAnnotate=0,
        strength=128,
    )
    c.setEncrypt(encrypt)

    # Fondo blanco de impresión
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    for row in range(rows):
        for col in range(cols):
            x = origin_x + col * (diameter + gutter_x)
            # Filas de arriba hacia abajo
            y = origin_y + (rows - 1 - row) * (diameter + gutter_y)

            # Guía de corte sutil (círculo punteado gris claro)
            c.setStrokeColorRGB(0.82, 0.82, 0.82)
            c.setDash(2, 3)
            c.setLineWidth(0.6)
            c.circle(x + diameter / 2, y + diameter / 2, diameter / 2 + 3, stroke=1, fill=0)
            c.setDash()

            c.drawImage(
                sticker,
                x,
                y,
                width=diameter,
                height=diameter,
                mask="auto",
                preserveAspectRatio=True,
                anchor="c",
            )

    c.showPage()
    c.save()

    print(f"PDF: {pdf_path}")
    print(f"Página: {page_w / inch:.2f}\" x {page_h / inch:.2f}\" (carta)")
    print(f"Stickers: {cols}x{rows} | diámetro: {diameter / inch:.3f}\"")
    print(f"Gutter X: {gutter_x / inch:.2f}\" | Gutter Y: {gutter_y / inch:.2f}\"")


def build_preview_png(circle_png: Path, preview_path: Path, dpi: int = 150) -> None:
    """Vista previa raster de la hoja carta para revisión visual."""
    page_w_in, page_h_in = 8.5, 11.0
    page_w = int(page_w_in * dpi)
    page_h = int(page_h_in * dpi)

    cols, rows = 2, 4
    margin_x = int(0.45 * dpi)
    margin_y = int(0.35 * dpi)
    gutter_x = int(0.30 * dpi)
    gutter_y = int(0.22 * dpi)

    usable_w = page_w - (2 * margin_x) - gutter_x
    usable_h = page_h - (2 * margin_y) - ((rows - 1) * gutter_y)
    diameter = min(usable_w // cols, usable_h // rows)

    grid_w = cols * diameter + gutter_x
    grid_h = rows * diameter + (rows - 1) * gutter_y
    origin_x = (page_w - grid_w) // 2
    origin_y = (page_h - grid_h) // 2

    sheet = Image.new("RGB", (page_w, page_h), (255, 255, 255))
    sticker = Image.open(circle_png).convert("RGBA").resize(
        (diameter, diameter), Image.Resampling.LANCZOS
    )

    draw = ImageDraw.Draw(sheet)
    for row in range(rows):
        for col in range(cols):
            x = origin_x + col * (diameter + gutter_x)
            y = origin_y + row * (diameter + gutter_y)
            cx, cy = x + diameter / 2, y + diameter / 2
            r = diameter / 2 + 3
            # Guía de corte
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(210, 210, 210), width=1)
            sheet.paste(sticker, (x, y), sticker)

    sheet.save(preview_path, "PNG")
    print(f"Preview: {preview_path}")


def main() -> None:
    make_circular_sticker(SRC, CIRCLE)
    build_pdf(CIRCLE, PDF_OUT)
    build_preview_png(CIRCLE, PREVIEW_OUT)
    # Copia a artifacts para descarga rápida
    artifacts = Path("/opt/cursor/artifacts")
    artifacts.mkdir(parents=True, exist_ok=True)
    for f in (PDF_OUT, PREVIEW_OUT, CIRCLE):
        target = artifacts / f.name
        target.write_bytes(f.read_bytes())
        print(f"Artifact: {target}")


if __name__ == "__main__":
    main()
