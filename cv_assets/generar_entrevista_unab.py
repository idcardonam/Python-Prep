#!/usr/bin/env python3
"""Genera el portafolio y el plan de preparación para la entrevista UNAB."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.utils import ImageReader


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "portfolio_unab"
OUTPUT_DIR = BASE_DIR.parent / "entregables"
FONT_DIR = BASE_DIR / "fonts"

PAGE_W, PAGE_H = letter

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#276FBF")
SKY = colors.HexColor("#EAF3FB")
GOLD = colors.HexColor("#F4C95D")
TEAL = colors.HexColor("#2A9D8F")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#526273")
LIGHT = colors.HexColor("#F5F7FA")
BORDER = colors.HexColor("#D9E1E8")
WHITE = colors.white
RED = colors.HexColor("#B44646")

pdfmetrics.registerFont(TTFont("Raleway", str(FONT_DIR / "Raleway-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Raleway-Bold", str(FONT_DIR / "Raleway-Bold.ttf")))


def pstyle(
    name: str,
    *,
    size: float = 10,
    leading: float | None = None,
    font: str = "Raleway",
    color=INK,
    align=TA_LEFT,
    space_after: float = 0,
) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment=align,
        spaceAfter=space_after,
    )


def draw_paragraph(
    c: canvas.Canvas,
    text: str,
    x: float,
    top_y: float,
    width: float,
    *,
    size: float = 10,
    leading: float | None = None,
    font: str = "Raleway",
    color=INK,
    align=TA_LEFT,
    max_height: float | None = None,
) -> float:
    style = pstyle(
        f"draw-{x}-{top_y}-{size}",
        size=size,
        leading=leading,
        font=font,
        color=color,
        align=align,
    )
    para = Paragraph(text, style)
    _, height = para.wrap(width, max_height or PAGE_H)
    if max_height is not None and height > max_height + 0.5:
        raise ValueError(f"Texto desbordado: requiere {height:.1f}, disponible {max_height:.1f}: {text[:70]}")
    para.drawOn(c, x, top_y - height)
    return top_y - height


def rounded_card(
    c: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    body: str,
    *,
    accent=BLUE,
    fill=WHITE,
    title_size: float = 11,
    body_size: float = 9.2,
) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y, width, height, 9, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + height - 8, width, 8, 9, fill=1, stroke=0)
    top = y + height - 20
    top = draw_paragraph(
        c,
        title,
        x + 14,
        top,
        width - 28,
        size=title_size,
        leading=title_size * 1.12,
        font="Raleway-Bold",
        color=NAVY,
        max_height=32,
    )
    draw_paragraph(
        c,
        body,
        x + 14,
        top - 7,
        width - 28,
        size=body_size,
        leading=body_size * 1.27,
        color=INK,
        max_height=height - 58,
    )


def draw_footer(c: canvas.Canvas, page_num: int, label: str = "Portafolio profesional") -> None:
    c.setStrokeColor(BORDER)
    c.line(36, 30, PAGE_W - 36, 30)
    c.setFillColor(MUTED)
    c.setFont("Raleway", 7.5)
    c.drawString(36, 18, f"{label} · Iván David Cardona Mendoza")
    c.drawRightString(PAGE_W - 36, 18, str(page_num))


def draw_page_header(c: canvas.Canvas, kicker: str, title: str, page_num: int) -> None:
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 78, PAGE_W, 78, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 78, 10, 78, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Raleway-Bold", 8.5)
    c.drawString(36, PAGE_H - 28, kicker.upper())
    c.setFillColor(WHITE)
    c.setFont("Raleway-Bold", 19)
    c.drawString(36, PAGE_H - 54, title)
    draw_footer(c, page_num)


def draw_tag(c: canvas.Canvas, text: str, x: float, y: float, width: float) -> None:
    c.setFillColor(SKY)
    c.setStrokeColor(colors.HexColor("#C8DDF1"))
    c.roundRect(x, y, width, 22, 11, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Raleway-Bold", 7.5)
    c.drawCentredString(x + width / 2, y + 7, text)


def fit_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    reader = ImageReader(str(path))
    iw, ih = reader.getSize()
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(reader, x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, preserveAspectRatio=True)


def draw_cover(c: canvas.Canvas) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.circle(PAGE_W + 10, PAGE_H - 40, 175, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(-20, 65, 130, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(42, PAGE_H - 200, 72, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Raleway-Bold", 13)
    c.drawString(42, PAGE_H - 105, "PORTAFOLIO DE DESARROLLO")
    c.setFont("Raleway-Bold", 31)
    c.drawString(42, PAGE_H - 155, "SOLUCIONES QUE")
    c.drawString(42, PAGE_H - 190, "CONVIERTEN PROCESOS")
    c.drawString(42, PAGE_H - 225, "EN CAPACIDAD DIGITAL")
    draw_paragraph(
        c,
        "Aplicaciones institucionales · Automatización · Integración · Analítica · Seguridad",
        42,
        PAGE_H - 262,
        450,
        size=12,
        leading=16,
        font="Raleway-Bold",
        color=GOLD,
    )
    photo = BASE_DIR / "img_0.jpeg"
    if photo.exists():
        c.saveState()
        c.setFillColor(WHITE)
        c.roundRect(42, 165, 156, 190, 16, fill=1, stroke=0)
        c.drawImage(str(photo), 50, 173, 140, 174, preserveAspectRatio=True, anchor="c")
        c.restoreState()
    draw_paragraph(
        c,
        "<b>IVÁN DAVID CARDONA MENDOZA</b><br/>Ingeniero de Sistemas · Especialista en Seguridad Informática",
        224,
        330,
        320,
        size=14,
        leading=20,
        color=WHITE,
    )
    draw_paragraph(
        c,
        "Selección de proyectos desarrollados en Organización Servicios y Asesorías (OSYA), "
        "presentados desde el problema, la solución, la arquitectura y el valor generado.",
        224,
        250,
        315,
        size=10.5,
        leading=15,
        color=WHITE,
    )
    c.setFillColor(GOLD)
    c.roundRect(224, 145, 278, 42, 8, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Raleway-Bold", 10)
    c.drawCentredString(363, 160, "ENTREVISTA · DESARROLLADOR TIC · UNAB")
    c.setFillColor(colors.HexColor("#B8C9D9"))
    c.setFont("Raleway", 8)
    c.drawString(42, 34, "Documento de conversación técnica · Julio de 2026")


def draw_profile_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "Propuesta profesional", "No desarrollo por desarrollar: resuelvo procesos", page_num)
    draw_paragraph(
        c,
        "Mi trabajo comienza entendiendo dónde se detiene la operación, quién necesita actuar y qué "
        "evidencia debe quedar. A partir de ahí diseño soluciones mantenibles, integradas y seguras.",
        44,
        688,
        515,
        size=13,
        leading=18,
        font="Raleway-Bold",
        color=NAVY,
    )
    cards = [
        ("01 · Entender", "Levanto el proceso con el usuario, identifico reglas, excepciones, responsables y criterios de aceptación."),
        ("02 · Diseñar", "Traduzco la necesidad en flujos, datos, roles, integraciones y controles antes de construir."),
        ("03 · Construir", "Desarrollo aplicaciones, automatizaciones y reportes con tecnologías apropiadas para la operación."),
        ("04 · Asegurar", "Incorporo autenticación, autorizaciones, logs, trazabilidad, reversión y documentación."),
        ("05 · Integrar", "Conecto áreas y sistemas evitando duplicidad, reproceso y pérdida de contexto entre solicitudes."),
        ("06 · Medir", "Convierto datos operativos en tableros para seguimiento, control y toma de decisiones."),
    ]
    positions = [(44, 500), (306, 500), (44, 335), (306, 335), (44, 170), (306, 170)]
    accents = [BLUE, TEAL, GOLD, BLUE, TEAL, GOLD]
    for (title, body), (x, y), accent in zip(cards, positions, accents):
        rounded_card(c, x, y, 250, 135, title, body, accent=accent, body_size=9.5)
    draw_paragraph(
        c,
        "<b>Principio de trabajo:</b> una solución útil no termina cuando compila; termina cuando el "
        "usuario puede operar, el equipo puede mantenerla y la organización puede auditarla.",
        44,
        146,
        512,
        size=10,
        leading=14,
        color=MUTED,
        align=TA_CENTER,
    )


def draw_ecosystem_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "Mapa de soluciones", "Ecosistema digital construido para OSYA", page_num)
    draw_paragraph(
        c,
        "Las soluciones no fueron iniciativas aisladas: conectaron operación, tecnología, datos y control "
        "para atender procesos críticos de nómina, tesorería, selección, contratación y soporte.",
        44,
        688,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    center_x, center_y = 306, 400
    c.setFillColor(NAVY)
    c.circle(center_x, center_y, 72, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Raleway-Bold", 18)
    c.drawCentredString(center_x, center_y + 8, "OSYA")
    c.setFont("Raleway", 8)
    c.drawCentredString(center_x, center_y - 10, "OPERACIÓN INTEGRADA")
    nodes = [
        ("OSYA PORTAL", 70, 540, BLUE),
        ("NEXUS", 386, 540, TEAL),
        ("TALENTFLOW", 55, 370, GOLD),
        ("NOVASOFT TI", 402, 370, BLUE),
        ("INCAPACIDADES", 75, 205, TEAL),
        ("HORAS EXTRA", 385, 205, GOLD),
        ("ANALÍTICA", 226, 115, BLUE),
    ]
    for title, x, y, accent in nodes:
        w, h = 155, 58
        nx, ny = x + w / 2, y + h / 2
        c.setStrokeColor(colors.HexColor("#A9B8C6"))
        c.setLineWidth(1.2)
        c.line(center_x, center_y, nx, ny)
        c.setFillColor(WHITE)
        c.setStrokeColor(accent)
        c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
        c.setFillColor(accent)
        c.rect(x, y, 7, h, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Raleway-Bold", 9)
        c.drawCentredString(x + w / 2 + 3, y + 32, title)
        sub = {
            "OSYA PORTAL": "Solicitudes y autorizaciones",
            "NEXUS": "Tesorería y caja menor",
            "TALENTFLOW": "Selección y contratación",
            "NOVASOFT TI": "Incidentes y automatización",
            "INCAPACIDADES": "Registro, validación y cobro",
            "HORAS EXTRA": "Estandarización y cálculo",
            "ANALÍTICA": "Power BI y Looker Studio",
        }[title]
        c.setFont("Raleway", 7.3)
        c.setFillColor(MUTED)
        c.drawCentredString(x + w / 2 + 3, y + 17, sub)
    draw_paragraph(
        c,
        "Patrón común: <b>requerimiento real · flujo controlado · integración · evidencia · información para decidir.</b>",
        44,
        96,
        520,
        size=10.5,
        leading=14,
        color=NAVY,
        align=TA_CENTER,
    )


def draw_project_page(
    c: canvas.Canvas,
    page_num: int,
    *,
    code: str,
    title: str,
    subtitle: str,
    challenge: str,
    solution: str,
    flow: list[str],
    technologies: str,
    controls: str,
    value: str,
    interview_line: str,
) -> None:
    draw_page_header(c, code, title, page_num)
    draw_paragraph(c, subtitle, 44, 690, 520, size=10.5, leading=14, color=MUTED)
    rounded_card(c, 44, 526, 250, 125, "El reto operativo", challenge, accent=GOLD, body_size=9.3)
    rounded_card(c, 318, 526, 250, 125, "La solución construida", solution, accent=TEAL, body_size=9.3)

    c.setFillColor(LIGHT)
    c.setStrokeColor(BORDER)
    c.roundRect(44, 395, 524, 105, 10, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Raleway-Bold", 10)
    c.drawString(58, 476, "FLUJO FUNCIONAL")
    step_w = 88
    start_x = 58
    for i, step in enumerate(flow):
        x = start_x + i * 101
        c.setFillColor(WHITE)
        c.setStrokeColor(BLUE)
        c.roundRect(x, 420, step_w, 38, 8, fill=1, stroke=1)
        draw_paragraph(c, step, x + 6, 448, step_w - 12, size=7.3, leading=9, font="Raleway-Bold", color=NAVY, align=TA_CENTER, max_height=29)
        if i < len(flow) - 1:
            c.setStrokeColor(BLUE)
            c.line(x + step_w + 3, 439, x + step_w + 11, 439)
            c.line(x + step_w + 8, 442, x + step_w + 11, 439)
            c.line(x + step_w + 8, 436, x + step_w + 11, 439)

    rounded_card(c, 44, 195, 250, 175, "Arquitectura y tecnología", technologies, accent=BLUE, body_size=9.1)
    rounded_card(c, 318, 195, 250, 175, "Controles y valor", f"<b>Controles:</b> {controls}<br/><br/><b>Valor:</b> {value}", accent=TEAL, body_size=8.8)

    c.setFillColor(NAVY)
    c.roundRect(44, 80, 524, 88, 10, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Raleway-Bold", 8)
    c.drawString(60, 146, "CÓMO LO CONTARÉ EN LA ENTREVISTA")
    draw_paragraph(c, f"“{interview_line}”", 60, 128, 492, size=10, leading=14, color=WHITE, max_height=48)


def draw_automation_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "06 · Automatización", "Dos procesos manuales convertidos en flujos controlados", page_num)
    rounded_card(
        c,
        44,
        410,
        524,
        260,
        "Gestión integral de incapacidades",
        "<b>Contexto:</b> el registro y seguimiento de incapacidades involucraba trabajadores, nómina y "
        "posterior gestión de cobro ante ARL o entidad de salud.<br/><br/>"
        "<b>Intervención:</b> diseñé un formulario web con Google Forms, campos y validaciones alineados "
        "con el ERP. La información verificada alimentaba un aplicativo para controlar estado, responsable, "
        "entidad de cobro y trazabilidad del caso.<br/><br/>"
        "<b>Valor:</b> unificación del dato desde el origen, reducción de reprocesos y visibilidad del ciclo "
        "completo desde el reporte hasta la gestión de recuperación.",
        accent=TEAL,
        body_size=9.8,
    )
    rounded_card(
        c,
        44,
        115,
        524,
        260,
        "Automatización del cálculo de horas extra",
        "<b>Contexto:</b> los reportes de clientes llegaban en formatos distintos y el cálculo para nómina "
        "se realizaba manualmente.<br/><br/>"
        "<b>Intervención:</b> estandaricé el formato de reporte y construí macros para validar, consolidar y "
        "calcular automáticamente la información antes de su procesamiento en nómina.<br/><br/>"
        "<b>Valor:</b> proceso repetible, menor exposición a errores de digitación, criterios homogéneos y "
        "mejor preparación de la información para revisión.",
        accent=GOLD,
        body_size=9.8,
    )


def draw_analytics_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "07 · Analítica", "Del registro operativo a una conversación con datos", page_num)
    draw_paragraph(
        c,
        "Construí tableros para tesorería, ventas, cartera, selección y flujo de caja. El objetivo no era "
        "“hacer gráficos”, sino convertir transacciones en señales útiles para responsables y directivos.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    image_path = ASSETS_DIR / "sanitized_flujo_tesoreria.jpg"
    c.setFillColor(WHITE)
    c.setStrokeColor(BORDER)
    c.roundRect(44, 352, 524, 285, 10, fill=1, stroke=1)
    fit_image(c, image_path, 55, 367, 502, 252)
    rounded_card(
        c,
        44,
        170,
        250,
        155,
        "Decisiones habilitadas",
        "Seguimiento de ingresos y egresos, posición acumulada, exposición financiera y comportamiento por periodo. "
        "El acceso móvil permitió llevar el análisis a espacios de decisión gerencial.",
        accent=BLUE,
        body_size=9.2,
    )
    rounded_card(
        c,
        318,
        170,
        250,
        155,
        "Principios aplicados",
        "Modelo de datos entendible, filtros relevantes, indicadores con contexto, navegación simple y separación "
        "entre detalle operativo y lectura ejecutiva.",
        accent=TEAL,
        body_size=9.2,
    )
    draw_paragraph(
        c,
        "Las capturas se presentan anonimizadas para proteger información operativa y de terceros.",
        44,
        145,
        520,
        size=8.5,
        color=MUTED,
        align=TA_CENTER,
    )


def draw_gallery_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "08 · Evidencia visual", "Tableros diseñados para distintas preguntas de negocio", page_num)
    images = [
        ("Ventas 2024", "sanitized_ventas_2024.jpg"),
        ("Comparativo 2024–2025", "sanitized_comparativo_ventas.jpg"),
        ("Ventas 2025", "sanitized_ventas_2025.jpg"),
        ("Cartera OSYA", "sanitized_cartera_osya.jpg"),
    ]
    positions = [(44, 422), (314, 422), (44, 125), (314, 125)]
    for (label, filename), (x, y) in zip(images, positions):
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER)
        c.roundRect(x, y, 254, 260, 9, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Raleway-Bold", 10)
        c.drawString(x + 12, y + 236, label)
        fit_image(c, ASSETS_DIR / filename, x + 12, y + 78, 230, 145)
        descriptions = {
            "Ventas 2024": "Tendencia, clientes, vendedores y composición de ingresos.",
            "Comparativo 2024–2025": "Variaciones interanuales y servicios con cambios relevantes.",
            "Ventas 2025": "Lectura mensual y seguimiento dinámico del desempeño comercial.",
            "Cartera OSYA": "Antigüedad, concentración y priorización de gestión de cobro.",
        }
        draw_paragraph(c, descriptions[label], x + 12, y + 66, 230, size=8.3, leading=11, color=MUTED, max_height=45)
    draw_paragraph(
        c,
        "Capturas protegidas: el portafolio demuestra estructura analítica sin revelar datos de clientes, cuentas o transacciones.",
        44,
        102,
        520,
        size=8.4,
        color=MUTED,
        align=TA_CENTER,
    )


def draw_engineering_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "09 · Ingeniería", "Estándares incorporados en las soluciones", page_num)
    items = [
        ("Requerimientos", "Proceso, actores, reglas, excepciones y criterios de aceptación antes de construir."),
        ("Integración", "Conexiones controladas con ERP y áreas responsables, evitando duplicidad y pérdida de trazabilidad."),
        ("Seguridad", "2FA, gestión de usuarios, mínimo privilegio, autorizaciones y protección del cambio sensible."),
        ("Trazabilidad", "Logs de auditoría, historial de actividades, responsables, estados y evidencia de cada intervención."),
        ("Calidad", "Validaciones, revisión con usuarios, control de cambios, posibilidad de reversión y documentación."),
        ("Operación", "Despliegue local, soporte, monitoreo y diseño pensando en continuidad y mantenibilidad."),
    ]
    y = 540
    for i, (title, body) in enumerate(items):
        x = 44 if i % 2 == 0 else 314
        if i % 2 == 0 and i > 0:
            y -= 165
        rounded_card(c, x, y, 254, 145, title, body, accent=[BLUE, TEAL, GOLD][i % 3], body_size=9.3)
    c.setFillColor(NAVY)
    c.roundRect(44, 70, 524, 76, 10, fill=1, stroke=0)
    draw_paragraph(
        c,
        "Mi diferencial no es solo programar: es combinar desarrollo, comprensión del proceso y seguridad "
        "para entregar aplicaciones que puedan operar, mantenerse y auditarse.",
        64,
        128,
        484,
        size=11,
        leading=15,
        font="Raleway-Bold",
        color=WHITE,
        align=TA_CENTER,
        max_height=48,
    )


def draw_unab_fit_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "10 · Conversación UNAB", "Cómo conecto mi experiencia con el reto institucional", page_num)
    rows = [
        ("Requerimiento UNAB", "Evidencia en mi experiencia"),
        ("Analizar requerimientos", "OSYA Portal, NEXUS y TalentFlow nacieron del levantamiento directo con áreas usuarias."),
        ("Desarrollar y mantener", "Aplicaciones Python, React y Streamlit desplegadas para procesos institucionales."),
        ("Integrar sistemas y datos", "Conexiones controladas con ERP, SQL, formularios, reportes y flujos entre áreas."),
        ("Pruebas y liberaciones", "Validaciones funcionales, autorización de cambios, reversión y acompañamiento a operación."),
        ("Seguridad y trazabilidad", "2FA, roles, logs, historial, doble autorización y experiencia en ISO 27001/COBIT."),
        ("Documentación y servicio", "Procedimientos auditables, atención de incidentes y contacto directo con usuarios."),
    ]
    table = Table(
        [[Paragraph(f"<b>{a}</b>" if i == 0 else a, pstyle(f"tf{i}a", size=8.8, leading=11, color=WHITE if i == 0 else INK)),
          Paragraph(f"<b>{b}</b>" if i == 0 else b, pstyle(f"tf{i}b", size=8.8, leading=11, color=WHITE if i == 0 else INK))]
         for i, (a, b) in enumerate(rows)],
        colWidths=[170, 350],
        rowHeights=[30, 52, 52, 52, 52, 52, 52],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.6, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
            ]
        )
    )
    table.wrapOn(c, 520, 400)
    table.drawOn(c, 44, 318)
    rounded_card(
        c,
        44,
        92,
        524,
        190,
        "Mi enfoque inicial si me vinculo",
        "<b>Escuchar y mapear:</b> comprender arquitectura, aplicaciones asignadas, backlog, usuarios y lineamientos TIC.<br/><br/>"
        "<b>Estabilizar y entregar:</b> atender prioridades, documentar dependencias y buscar una mejora de bajo riesgo que demuestre valor temprano.<br/><br/>"
        "<b>Fortalecer:</b> dejar pruebas, trazabilidad, documentación y conocimiento transferible para que la solución no dependa de una sola persona.",
        accent=GOLD,
        body_size=9.4,
    )


def draw_closing_page(c: canvas.Canvas, page_num: int) -> None:
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0, 16, PAGE_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Raleway-Bold", 11)
    c.drawString(52, PAGE_H - 90, "CIERRE")
    c.setFont("Raleway-Bold", 31)
    c.drawString(52, PAGE_H - 150, "NO VENGO SOLO A")
    c.drawString(52, PAGE_H - 187, "OCUPAR UN CARGO.")
    c.setFillColor(GOLD)
    c.drawString(52, PAGE_H - 240, "VENGO A ENTENDER,")
    c.drawString(52, PAGE_H - 277, "CONSTRUIR Y DEJAR")
    c.drawString(52, PAGE_H - 314, "CAPACIDAD INSTALADA.")
    draw_paragraph(
        c,
        "Mi experiencia combina desarrollo, automatización, integración, analítica y seguridad. "
        "Quiero poner esa combinación al servicio de procesos académicos y administrativos que necesitan "
        "soluciones estables, documentadas y sostenibles.",
        52,
        PAGE_H - 365,
        470,
        size=12,
        leading=18,
        color=WHITE,
    )
    c.setFillColor(TEAL)
    c.roundRect(52, 150, 465, 104, 12, fill=1, stroke=0)
    draw_paragraph(
        c,
        "<b>IVÁN DAVID CARDONA MENDOZA</b><br/>Ingeniero de Sistemas · Especialista en Seguridad Informática<br/>"
        "304 558 7767 · idcm@hotmail.es · https://n9.cl/lajpr",
        72,
        228,
        425,
        size=11,
        leading=16,
        color=WHITE,
        align=TA_CENTER,
        max_height=70,
    )
    c.setFillColor(colors.HexColor("#B8C9D9"))
    c.setFont("Raleway", 7.5)
    c.drawString(52, 35, f"Portafolio profesional · Página {page_num}")


def draw_osya_method_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(
        c,
        "01 · Método demostrado",
        "Del requerimiento a una solución segura: OSYA Portal",
        page_num,
    )
    draw_paragraph(
        c,
        "Este proyecto resume mi forma de desarrollar: entender el proceso y sus riesgos antes de elegir "
        "tecnología, construir por etapas y llevar la seguridad hasta la operación.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    phases = [
        (
            "1. Alcance y riesgo",
            "Contabilidad, nómina y tesorería dependían de TI para solicitudes frecuentes. Identifiqué actores, "
            "reglas, datos afectados, autorizadores y riesgos de cambio directo sobre la operación.",
            GOLD,
        ),
        (
            "2. Flujo y arquitectura",
            "Diseñé solicitud, validación, aprobación del responsable, ejecución controlada por TI y "
            "evidencia. Separé interfaz React, lógica Django, PostgreSQL e integración con ERP.",
            BLUE,
        ),
        (
            "3. Implementación",
            "Construí entregas progresivas con Git para controlar versiones y cambios sobre un sitio ya en "
            "producción, preservando una ruta clara de actualización.",
            TEAL,
        ),
        (
            "4. Pruebas con usuarios",
            "Validé manualmente sobre base de pruebas y posteriormente con usuarios finales, revisando reglas, "
            "perfiles, resultados y excepciones antes de consolidar el cambio.",
            BLUE,
        ),
        (
            "5. Seguridad y afinamiento",
            "Apliqué permisos diferenciados de consulta y escritura, 2FA, aprobación del responsable, logs, "
            "historial y reversión controlada. El control fue parte del flujo, no un agregado final.",
            TEAL,
        ),
    ]
    y_positions = [545, 420, 295, 170, 45]
    for (title, body, accent), y in zip(phases, y_positions):
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER)
        c.roundRect(44, y, 524, 104, 10, fill=1, stroke=1)
        c.setFillColor(accent)
        c.roundRect(44, y, 8, 104, 8, fill=1, stroke=0)
        draw_paragraph(
            c,
            title,
            66,
            y + 82,
            150,
            size=10.5,
            leading=13,
            font="Raleway-Bold",
            color=NAVY,
            max_height=28,
        )
        draw_paragraph(
            c,
            body,
            220,
            y + 86,
            328,
            size=8.8,
            leading=11.5,
            color=INK,
            max_height=76,
        )


def draw_macro_architecture_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "02 · Automatización", "Macro de horas extra: estandarizar antes de automatizar", page_num)
    draw_paragraph(
        c,
        "Más de 30 clientes reportaban novedades en archivos Excel. La variedad de formatos y el cálculo "
        "manual generaban errores en valores que impactaban directamente el pago de nómina.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    rounded_card(
        c,
        44,
        520,
        250,
        125,
        "Alcance y riesgos",
        "<b>Alcance:</b> recepción, validación, consolidación y cálculo de horas extra.<br/><br/>"
        "<b>Riesgos:</b> formato incorrecto, dato incompleto, duplicidad, fórmula inconsistente y pago errado.",
        accent=GOLD,
        body_size=9.1,
    )
    rounded_card(
        c,
        318,
        520,
        250,
        125,
        "Decisión de diseño",
        "Definí una plantilla Excel estándar para clientes y una macro que aplicaba las mismas reglas de "
        "validación y cálculo antes de preparar la información para nómina.",
        accent=TEAL,
        body_size=9.1,
    )

    c.setFillColor(LIGHT)
    c.setStrokeColor(BORDER)
    c.roundRect(44, 340, 524, 150, 10, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Raleway-Bold", 10)
    c.drawString(58, 466, "ARQUITECTURA DEL FLUJO")
    steps = [
        ("Archivo Excel", "Entrada estándar"),
        ("Validación", "Campos y formato"),
        ("Consolidación", "+30 clientes"),
        ("Cálculo", "Reglas homogéneas"),
        ("Salida", "Revisión nómina"),
    ]
    for i, (title, subtitle) in enumerate(steps):
        x = 58 + i * 101
        c.setFillColor(WHITE)
        c.setStrokeColor(BLUE)
        c.roundRect(x, 382, 88, 58, 8, fill=1, stroke=1)
        draw_paragraph(c, title, x + 5, 426, 78, size=7.4, leading=9, font="Raleway-Bold", color=NAVY, align=TA_CENTER, max_height=19)
        draw_paragraph(c, subtitle, x + 5, 402, 78, size=6.8, leading=8, color=MUTED, align=TA_CENTER, max_height=17)
        if i < 4:
            c.setStrokeColor(BLUE)
            c.line(x + 91, 411, x + 99, 411)
            c.line(x + 96, 414, x + 99, 411)
            c.line(x + 96, 408, x + 99, 411)

    rounded_card(
        c,
        44,
        130,
        250,
        180,
        "Controles aplicados",
        "• Plantilla única de entrada.<br/>"
        "• Validación previa al cálculo.<br/>"
        "• Reglas homogéneas para todos los clientes.<br/>"
        "• Separación entre procesamiento y revisión.<br/>"
        "• Archivo de salida preparado para control de nómina.",
        accent=BLUE,
        body_size=9,
    )
    rounded_card(
        c,
        318,
        130,
        250,
        180,
        "Valor demostrado",
        "No presento una cifra que no fue medida formalmente. El valor verificable fue reducir la exposición "
        "a errores de cálculo, convertir un proceso variable en uno repetible y facilitar la revisión antes "
        "de afectar pagos.",
        accent=TEAL,
        body_size=9.1,
    )
    c.setFillColor(NAVY)
    c.roundRect(44, 62, 524, 48, 9, fill=1, stroke=0)
    draw_paragraph(
        c,
        "“La automatización empezó por controlar el dato de entrada; no por escribir una macro sobre un proceso desordenado.”",
        60,
        94,
        492,
        size=9.5,
        leading=13,
        font="Raleway-Bold",
        color=WHITE,
        align=TA_CENTER,
        max_height=30,
    )


def draw_integrated_projects_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "04 · Visión integral", "Proyectos conectados con procesos, datos y decisiones", page_num)
    draw_paragraph(
        c,
        "El valor no está en contar aplicaciones. Está en demostrar que cada una resolvió una parte del flujo "
        "y que los datos producidos podían convertirse en seguimiento y control.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    projects = [
        ("OSYA PORTAL", "Contabilidad · Nómina · Tesorería", "Django · React · PostgreSQL · ERP", BLUE),
        ("NEXUS", "Cobros · Egresos · Caja menor", "Aplicación · datos · Power BI", TEAL),
        ("TALENTFLOW", "Selección · RQ · Contratación", "IA asistida · correos · analítica", GOLD),
        ("NOVASOFT TI", "Incidentes · consultas repetitivas", "Python · Streamlit · ERP", BLUE),
        ("INCAPACIDADES", "Registro · validación · cobro", "Google Forms · ERP · gestión", TEAL),
        ("HORAS EXTRA", "Reportes de más de 30 clientes", "Excel · validación · nómina", GOLD),
    ]
    positions = [(44, 510), (306, 510), (44, 350), (306, 350), (44, 190), (306, 190)]
    for (title, process, architecture, accent), (x, y) in zip(projects, positions):
        c.setFillColor(WHITE)
        c.setStrokeColor(BORDER)
        c.roundRect(x, y, 250, 130, 10, fill=1, stroke=1)
        c.setFillColor(accent)
        c.roundRect(x, y + 121, 250, 9, 9, fill=1, stroke=0)
        draw_paragraph(c, title, x + 14, y + 105, 222, size=10.5, leading=12, font="Raleway-Bold", color=NAVY, max_height=20)
        draw_paragraph(c, process, x + 14, y + 78, 222, size=8.5, leading=10.5, color=INK, max_height=24)
        c.setStrokeColor(BORDER)
        c.line(x + 14, y + 57, x + 236, y + 57)
        draw_paragraph(c, architecture, x + 14, y + 43, 222, size=8, leading=10, font="Raleway-Bold", color=MUTED, max_height=32)
    c.setFillColor(NAVY)
    c.roundRect(44, 75, 512, 82, 10, fill=1, stroke=0)
    draw_paragraph(
        c,
        "<b>Patrón transversal:</b> proceso entendido · datos controlados · integración · evidencia · decisión. "
        "Ese patrón es transferible a aplicaciones académicas y administrativas.",
        64,
        137,
        472,
        size=10,
        leading=14,
        color=WHITE,
        align=TA_CENTER,
        max_height=48,
    )


def draw_connected_analytics_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "05 · Analítica conectada", "NEXUS: de la operación a la decisión", page_num)
    draw_paragraph(
        c,
        "Los tableros no fueron ejercicios aislados. Partieron de datos generados por aplicaciones y procesos "
        "para responder preguntas de tesorería, cartera, ventas, selección y flujo de caja.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    c.setFillColor(LIGHT)
    c.setStrokeColor(BORDER)
    c.roundRect(44, 570, 524, 84, 10, fill=1, stroke=1)
    chain = ["NEXUS", "PostgreSQL", "Modelo de datos", "Power BI", "Dirección"]
    for i, label in enumerate(chain):
        x = 58 + i * 101
        draw_tag(c, label, x, 601, 84)
        if i < 4:
            c.setStrokeColor(BLUE)
            c.line(x + 86, 612, x + 99, 612)

    fit_image(c, ASSETS_DIR / "sanitized_flujo_tesoreria.jpg", 44, 305, 330, 235)
    rounded_card(
        c,
        394,
        305,
        174,
        235,
        "Lectura ejecutiva",
        "• Ingresos y egresos.<br/>"
        "• Flujo acumulado.<br/>"
        "• Riesgo financiero.<br/>"
        "• Seguimiento por periodo.<br/>"
        "• Consulta móvil para directivos.<br/><br/>"
        "La captura está anonimizada para proteger información operativa.",
        accent=TEAL,
        body_size=8.5,
        title_size=10.5,
    )
    rounded_card(
        c,
        44,
        105,
        250,
        165,
        "Otros tableros",
        "TalentFlow y selección; salidas de dinero; cartera; ventas; comparativos; control contable en Looker Studio "
        "y flujo de caja consultable desde dispositivos móviles.",
        accent=BLUE,
        body_size=9.1,
    )
    rounded_card(
        c,
        318,
        105,
        250,
        165,
        "Mi criterio analítico",
        "Defino primero la pregunta, el responsable y la decisión. Después modelo, valido y presento el indicador. "
        "Un tablero sin proceso de uso es solo una pantalla.",
        accent=GOLD,
        body_size=9.1,
    )


def draw_unab_education_page(c: canvas.Canvas, page_num: int) -> None:
    draw_page_header(c, "06 · Ajuste institucional", "Cómo llevaría este enfoque al contexto UNAB", page_num)
    draw_paragraph(
        c,
        "En educación superior, una aplicación puede afectar matrículas, notas, pagos, acceso a servicios, "
        "reportes regulatorios y continuidad académica. Por eso el desarrollo exige rigor técnico y comprensión social.",
        44,
        690,
        520,
        size=11,
        leading=15,
        color=MUTED,
    )
    rows = [
        ("Necesidad UNAB", "Cómo respondo"),
        ("Requerimientos de usuarios", "Levanto proceso, reglas, excepciones, responsables y criterios de aceptación."),
        ("Aplicaciones e integración", "Diseño capas, datos y contratos; desarrollo con versionamiento y cambios controlados."),
        ("Pruebas y liberación", "Base de pruebas, validación manual, usuarios finales, respaldo y posibilidad de reversión."),
        ("Seguridad y trazabilidad", "Perfiles, mínimo privilegio, aprobación, 2FA, logs, historial y documentación."),
    ]
    table = Table(
        [[Paragraph(f"<b>{a}</b>" if i == 0 else a, pstyle(f"ue{i}a", size=8.4, leading=10.5, color=WHITE if i == 0 else INK)),
          Paragraph(f"<b>{b}</b>" if i == 0 else b, pstyle(f"ue{i}b", size=8.4, leading=10.5, color=WHITE if i == 0 else INK))]
         for i, (a, b) in enumerate(rows)],
        colWidths=[172, 348],
        rowHeights=[30, 54, 54, 54, 54],
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.6, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
    ]))
    table.wrapOn(c, 520, 300)
    table.drawOn(c, 44, 370)

    rounded_card(
        c,
        44,
        180,
        250,
        155,
        "Responsabilidad sectorial",
        "<b>Ley 30 y SNIES:</b> información completa, veraz, actualizada, disponible y protegida para planeación, "
        "calidad, inspección y vigilancia.<br/><br/><b>CNA:</b> evidencia histórica y sistemas que soporten autoevaluación.",
        accent=GOLD,
        body_size=8.6,
    )
    rounded_card(
        c,
        318,
        180,
        250,
        155,
        "Protección e impacto",
        "<b>Ley 1581:</b> seguridad, acceso autorizado, finalidad y confidencialidad de datos personales.<br/><br/>"
        "<b>Impacto social:</b> cambios estables para no interrumpir servicios de estudiantes, docentes y administrativos.",
        accent=TEAL,
        body_size=8.6,
    )
    c.setFillColor(NAVY)
    c.roundRect(44, 65, 524, 88, 10, fill=1, stroke=0)
    draw_paragraph(
        c,
        "“Mi plus como especialista es identificar alcance y riesgo desde el inicio, diseñar el flujo, "
        "implementar con control y afinar la seguridad hasta que la solución quede estable y auditable.”",
        62,
        132,
        488,
        size=10,
        leading=14,
        font="Raleway-Bold",
        color=WHITE,
        align=TA_CENTER,
        max_height=56,
    )


def generate_portfolio(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output), pagesize=letter)
    c.setTitle("Portafolio de Desarrollo - Ivan David Cardona - UNAB")
    draw_cover(c)
    c.showPage()
    draw_osya_method_page(c, 2)
    c.showPage()
    draw_macro_architecture_page(c, 3)
    c.showPage()
    draw_project_page(
        c,
        4,
        code="03 · Operación TIC",
        title="NOVASOFT TI",
        subtitle="Aplicación para gestionar incidentes y automatizar respuestas repetitivas del área de tecnología.",
        challenge="El equipo invertía tiempo en incidentes recurrentes y consultas operativas que podían resolverse con un flujo controlado y acceso oportuno a información del ERP.",
        solution="Desarrollé una aplicación en Streamlit para registrar, consultar y automatizar incidentes frecuentes, apoyada en una conexión controlada con la base de datos del ERP.",
        flow=["Incidente", "Clasificación", "Consulta ERP", "Resolución", "Registro"],
        technologies="<b>Stack:</b> Python, Streamlit, base de datos del ERP y servidor local.<br/><br/>"
        "<b>Operación:</b> interfaz simple para facilitar adopción, consulta y gestión por parte del equipo TIC.",
        controls="2FA con Google, usuarios y roles, logs de auditoría, registro de actividades y evidencia apta para procesos de calidad.",
        value="Menos esfuerzo en tareas repetitivas, atención más consistente y conocimiento operativo convertido en una herramienta reutilizable.",
        interview_line="NOVASOFT TI resume mi forma de trabajar: observar patrones de incidentes, convertirlos en lógica y dejar trazabilidad de la atención.",
    )
    c.showPage()
    draw_integrated_projects_page(c, 5)
    c.showPage()
    draw_connected_analytics_page(c, 6)
    c.showPage()
    draw_unab_education_page(c, 7)
    c.showPage()
    c.save()


def study_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    return {
        "title": pstyle("study-title", size=28, leading=33, font="Raleway-Bold", color=NAVY),
        "subtitle": pstyle("study-subtitle", size=13, leading=18, font="Raleway-Bold", color=BLUE),
        "h1": pstyle("study-h1", size=19, leading=24, font="Raleway-Bold", color=NAVY, space_after=8),
        "h2": pstyle("study-h2", size=13, leading=17, font="Raleway-Bold", color=BLUE, space_after=5),
        "body": pstyle("study-body", size=9.4, leading=13.2, color=INK, align=TA_JUSTIFY, space_after=7),
        "bullet": ParagraphStyle(
            "study-bullet",
            fontName="Raleway",
            fontSize=9.2,
            leading=12.7,
            textColor=INK,
            leftIndent=14,
            firstLineIndent=-9,
            bulletIndent=0,
            spaceAfter=4,
        ),
        "small": pstyle("study-small", size=7.5, leading=10, color=MUTED),
        "quote": pstyle("study-quote", size=11, leading=16, font="Raleway-Bold", color=NAVY, align=TA_CENTER),
        "table": pstyle("study-table", size=7.9, leading=10.4, color=INK),
        "table_head": pstyle("study-table-head", size=8, leading=10, font="Raleway-Bold", color=WHITE),
    }


def study_page(canvas_obj: canvas.Canvas, doc) -> None:
    page = canvas_obj.getPageNumber()
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, PAGE_H - 26, PAGE_W, 26, fill=1, stroke=0)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.rect(0, PAGE_H - 26, 9, 26, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Raleway-Bold", 7.5)
    canvas_obj.drawString(34, PAGE_H - 17, "PREPARACIÓN ENTREVISTA UNAB · DESARROLLADOR TIC")
    canvas_obj.setStrokeColor(BORDER)
    canvas_obj.line(34, 28, PAGE_W - 34, 28)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.setFont("Raleway", 7.2)
    canvas_obj.drawString(34, 17, "Iván David Cardona Mendoza · 21 de julio de 2026 · 9:35 a. m.")
    canvas_obj.drawRightString(PAGE_W - 34, 17, str(page))
    canvas_obj.restoreState()


def bullet(text: str, styles: dict) -> Paragraph:
    return Paragraph(f"• {text}", styles["bullet"])


def callout(text: str, styles: dict, *, color=SKY, border=BLUE) -> Table:
    table = Table([[Paragraph(text, styles["body"])]], colWidths=[520])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def section_title(text: str, styles: dict) -> list:
    return [Paragraph(text, styles["h1"]), Spacer(1, 4)]


def table_from_rows(rows: list[list[str]], widths: list[float], styles: dict, header: bool = True) -> Table:
    data = []
    for i, row in enumerate(rows):
        style = styles["table_head"] if header and i == 0 else styles["table"]
        data.append([Paragraph(f"<b>{cell}</b>" if header and i == 0 else cell, style) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.55, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [WHITE, LIGHT]),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    table.setStyle(TableStyle(commands))
    return table


def add_qa(story: list, question: str, answer: str, styles: dict) -> None:
    story.append(KeepTogether([
        Paragraph(question, styles["h2"]),
        Paragraph(answer, styles["body"]),
        Spacer(1, 4),
    ]))


def generate_study_plan(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = study_styles()
    doc = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=43,
        bottomMargin=40,
        title="Plan de preparación entrevista UNAB - Ivan David Cardona",
        author="Ivan David Cardona Mendoza",
    )
    story: list = []

    story += [
        Spacer(1, 68),
        Paragraph("ENTREVISTA UNAB", styles["subtitle"]),
        Spacer(1, 10),
        Paragraph("PLAN COMPLETO DE PREPARACIÓN", styles["title"]),
        Spacer(1, 12),
        Paragraph("Desarrollador(a) para el Departamento de Tecnologías de Información y Comunicaciones", styles["subtitle"]),
        Spacer(1, 38),
        callout(
            "<b>Objetivo:</b> llegar a la entrevista sin pedir que “te den una oportunidad”. Llegar con evidencia, "
            "criterio y una lectura concreta del reto: entender procesos académicos y administrativos, construir "
            "soluciones integradas y dejarlas estables, seguras, probadas y documentadas.",
            styles,
            color=colors.HexColor("#FFF8E5"),
            border=GOLD,
        ),
        Spacer(1, 42),
        Paragraph("ENTREVISTA PRESENCIAL", styles["h2"]),
        Paragraph(
            "<b>Fecha:</b> martes, 21 de julio de 2026<br/>"
            "<b>Hora:</b> 9:35 a. m. · duración anunciada: 20 minutos<br/>"
            "<b>Lugar:</b> Campus El Jardín · Oficina de Infraestructura, primer piso de Biblioteca<br/>"
            "<b>Entrevistadora:</b> Ing. Vicky Lozano Sierra · Directora de Tecnologías de la Información",
            styles["body"],
        ),
        Spacer(1, 35),
        Paragraph("IVÁN DAVID CARDONA MENDOZA", styles["h1"]),
        Paragraph("Ingeniero de Sistemas · Especialista en Seguridad Informática", styles["body"]),
        PageBreak(),
    ]

    story += section_title("1. Qué está buscando realmente la UNAB", styles)
    story.append(Paragraph(
        "La misión publicada para el cargo es diseñar, desarrollar, mantener y mejorar sistemas de información y "
        "aplicaciones institucionales, garantizando soluciones estables, seguras, documentadas e integradas, alineadas "
        "con necesidades académicas, administrativas y estratégicas. No están buscando únicamente velocidad para "
        "programar: buscan alguien que entienda el contexto institucional y pueda responder por el ciclo de vida.",
        styles["body"],
    ))
    vacancy_rows = [
        ["Lo que exige la convocatoria", "Lo que debes demostrar en 20 minutos"],
        ["Análisis de requerimientos", "Que conversas con usuarios, entiendes reglas y traduces necesidades en una solución viable."],
        ["Desarrollo y mantenimiento", "Que has construido aplicaciones y también sabes atender cambios, incidentes y evolución."],
        ["Bases de datos e integración", "Que manejas SQL, conexiones con ERP, servicios y flujos entre áreas sin perder control."],
        ["Pruebas y liberaciones", "Que validas antes de producción, defines aceptación, controlas cambios y contemplas reversión."],
        ["Seguridad y trazabilidad", "Que incorporas roles, 2FA, logs, mínimo privilegio, historial y protección del dato."],
        ["Documentación y servicio", "Que dejas conocimiento transferible y acompañas al usuario hasta estabilizar la solución."],
    ]
    story.append(table_from_rows(vacancy_rows, [190, 330], styles))
    story.append(Spacer(1, 12))
    story.append(callout(
        "<b>Tu frase guía:</b> “Mi fortaleza es conectar tres conversaciones que normalmente se separan: lo que el "
        "usuario necesita, lo que técnicamente es sostenible y lo que seguridad y auditoría exigen.”",
        styles,
    ))
    story.append(PageBreak())

    story += section_title("2. Lo esencial sobre la UNAB y su área TIC", styles)
    story.append(Paragraph(
        "Esta sección ya contiene la investigación relevante. No necesitas llegar recitando nombres de sistemas; debes "
        "usar estos datos para demostrar que entendiste el entorno y formular mejores preguntas.",
        styles["body"],
    ))
    for text in [
        "<b>Propósito institucional:</b> formar personas autónomas, éticas y creativas capaces de transformar su entorno. "
        "En entrevista, conecta tecnología con estudiantes, docentes y personal administrativo; no hables solo de código.",
        "<b>Dirección TIC:</b> una publicación institucional de 2023 reportó que el área, liderada por Vicky Lozano Sierra, "
        "gestionaba cerca de 75 proyectos estratégicos de mantenimiento y mejora de procesos.",
        "<b>Ecosistema:</b> la misma publicación registró más de 51 aplicaciones, entre ellas Banner académico y financiero, "
        "Sara, Mi Portal U, Guido, Simplicity, CRM, Apolo PURE y Suite Vision Empresarial.",
        "<b>Plataforma tecnológica pública:</b> la UNAB ha informado uso de bases de datos Oracle y MySQL, servidores Unix/GNU/Linux, "
        "redes LAN y wifi, además de arquitectura de software e integraciones institucionales.",
        "<b>Trabajo conjunto:</b> Infraestructura Tecnológica y Sistemas de Información tienen responsabilidades distintas, "
        "pero colaboran para continuidad, rendimiento, actualizaciones y mejora de servicios.",
        "<b>Estrategia 2025–2032:</b> incluye el PETIC 2032 y la proyección de infraestructura física y tecnológica. La "
        "transformación digital institucional prioriza servicios digitales, procesos automatizados, analítica y experiencia de usuario.",
        "<b>Seguridad:</b> la política institucional de gestión de incidentes publicada en 2025 enfatiza respuesta inmediata "
        "para proteger confidencialidad, integridad, disponibilidad y continuidad de datos, aplicaciones, activos y redes.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "<b>Lectura correcta del reto:</b> entrarías a un ecosistema heterogéneo, con aplicaciones críticas y usuarios muy "
        "distintos. Tu valor está en integrarte al equipo, aprender sus estándares y mejorar sin romper la operación.",
        styles,
        color=colors.HexColor("#EAF7F4"),
        border=TEAL,
    ))
    story.append(PageBreak())

    story += section_title("2A. Desarrollo en educación superior: regulación e impacto social", styles)
    story.append(Paragraph(
        "Este conocimiento sí puede diferenciarte, siempre que lo traduzcas a decisiones de ingeniería. La directora no "
        "necesita una exposición jurídica; necesita comprobar que entiendes por qué una aplicación universitaria exige "
        "integridad, continuidad, privacidad, evidencia y cambios controlados.",
        styles["body"],
    ))
    education_rows = [
        ["Marco", "Exigencia relevante", "Implicación para desarrollo"],
        ["Ley 30 de 1992", "El Estado inspecciona y vigila la educación superior y vela por la calidad del servicio.", "Los sistemas deben sostener procesos institucionales verificables y confiables."],
        ["SNIES / Decreto 1767 de 2006", "Las IES responden por información completa, veraz, actualizada, disponible, segura y confidencial; el reporte debe apoyarse en procesos automatizados.", "Validaciones, calidad de datos, trazabilidad, responsables, calendarios, evidencia y controles sobre cargues."],
        ["CNA y acreditación", "La autoevaluación y los Cuadros Maestros requieren información histórica; el CNA usa SNIES como fuente primaria.", "Conservar historia, evitar alteraciones, documentar reglas y facilitar reportes reproducibles."],
        ["Ley 1581 de 2012", "Finalidad, acceso autorizado, seguridad y confidencialidad de datos personales.", "Mínimo privilegio, autenticación, protección de secretos, logs prudentes y datos de prueba anonimizados."],
        ["Políticas UNAB", "Gobierno TIC, cuentas y contraseñas, auditoría y respuesta a incidentes para preservar continuidad.", "Alinear arquitectura, cambios, accesos y operación con estándares internos antes de desplegar."],
    ]
    story.append(table_from_rows(education_rows, [92, 208, 220], styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph("El impacto social que debes nombrar", styles["h2"]))
    for text in [
        "Un error en una integración puede afectar matrícula, calificaciones, pagos, inscripción o acceso a servicios.",
        "Una indisponibilidad no impacta solo un indicador técnico: interrumpe actividades de estudiantes, docentes y administrativos.",
        "Un dato inconsistente puede propagarse hacia reportes de calidad, planeación, acreditación o autoridades del sector.",
        "Una autorización excesiva puede exponer información académica, financiera o personal de la comunidad universitaria.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 8))
    story.append(callout(
        "<b>Cómo decirlo en 45 segundos:</b> “Entiendo que en una universidad un desarrollo no solo debe cumplir una "
        "función. Debe proteger datos personales y académicos, preservar historia y trazabilidad, soportar reportes confiables "
        "y evitar que un cambio interrumpa servicios con impacto directo en la comunidad. Por eso mi método empieza por alcance "
        "y riesgo, continúa con flujo y arquitectura, y termina con pruebas, control de cambios y seguridad en operación.”",
        styles,
        color=colors.HexColor("#FFF8E5"),
        border=GOLD,
    ))
    story.append(PageBreak())

    story += section_title("3. Tu mapa de valor frente a la vacante", styles)
    fit_rows = [
        ["Necesidad probable", "Evidencia tuya", "Mensaje"],
        ["Levantamiento con áreas", "OSYA Portal, NEXUS, incapacidades", "“Primero ordeno proceso, reglas y responsables.”"],
        ["Aplicaciones institucionales", "OSYA Portal, NEXUS, TalentFlow", "“He construido soluciones para procesos críticos.”"],
        ["Gestión de incidentes", "NOVASOFT TI y GLPI", "“Convierto incidentes repetitivos en conocimiento reutilizable.”"],
        ["Integración", "ERP, formularios, áreas de nómina/tesorería/contratación", "“Integro con control y trazabilidad.”"],
        ["Datos", "SQL, Power BI, Looker Studio", "“Diseño la aplicación y también la capacidad de medirla.”"],
        ["Seguridad", "2FA, roles, logs, doble autorización", "“La seguridad nace con la solución, no al final.”"],
        ["Auditoría y gobierno", "Comultrasan, COBIT, ISO 27001", "“Entiendo qué evidencia necesita un control.”"],
    ]
    story.append(table_from_rows(fit_rows, [138, 190, 192], styles))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Tus tres proyectos principales para la entrevista", styles["h2"]))
    story.append(bullet("<b>OSYA Portal:</b> el mejor caso para requerimientos, integración, autorización, seguridad y trazabilidad.", styles))
    story.append(bullet("<b>NOVASOFT TI:</b> el mejor caso para soporte, automatización, ERP y orientación al servicio.", styles))
    story.append(bullet("<b>TalentFlow:</b> el mejor caso para flujo de negocio, integración entre áreas y uso responsable de IA.", styles))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "NEXUS, incapacidades, horas extra y Power BI quedan como evidencia complementaria. No intentes contar los siete "
        "proyectos en 20 minutos; demuestra profundidad en dos y usa los demás cuando una pregunta los haga relevantes.",
        styles["body"],
    ))
    story.append(PageBreak())

    story += section_title("4. Apertura de 90 segundos", styles)
    story.append(callout(
        "“Ingeniera Vicky, gracias por la oportunidad. Soy Ingeniero de Sistemas y Especialista en Seguridad Informática. "
        "Mi experiencia combina desarrollo de aplicaciones, automatización, bases de datos y control. En OSYA trabajé "
        "directamente con áreas como nómina, tesorería, selección, contratación y TI para convertir necesidades operativas "
        "en soluciones como OSYA Portal, NEXUS, TalentFlow y NOVASOFT TI.<br/><br/>"
        "Mi forma de trabajar es entender primero el proceso y sus riesgos; después diseño el flujo, la integración y los "
        "controles. Por eso mis desarrollos incorporan elementos como roles, doble factor, autorizaciones, logs y trazabilidad. "
        "Además, mi experiencia auditando TI en Comultrasan me enseñó a pensar en continuidad, evidencia y mantenibilidad, no "
        "solo en que una funcionalidad opere.<br/><br/>"
        "Al conocer que TIC de la UNAB administra un ecosistema amplio de aplicaciones académicas y administrativas, veo que "
        "el reto del cargo es aprender ese entorno, trabajar cerca de los usuarios y entregar cambios seguros y documentados. "
        "Esa combinación entre desarrollo, servicio y seguridad es precisamente el valor que puedo aportar.”",
        styles,
        color=colors.HexColor("#FFF8E5"),
        border=GOLD,
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Cómo decirlo", styles["h2"]))
    for text in [
        "No lo memorices palabra por palabra. Memoriza cuatro ideas: <b>quién soy, qué construí, cómo trabajo y por qué encajo.</b>",
        "Habla a ritmo tranquilo, con pausas después de cada proyecto o concepto importante.",
        "Mira a la entrevistadora; el portafolio es apoyo, no libreto.",
        "No empieces enumerando tecnologías. Empieza por el problema y termina con el valor.",
    ]:
        story.append(bullet(text, styles))
    story.append(PageBreak())

    story += section_title("5. Historia principal: OSYA Portal", styles)
    star_rows = [
        ["Momento", "Qué decir"],
        ["Situación", "“Contabilidad, nómina y tesorería dependían de TI para solicitudes frecuentes. La alta demanda generaba esperas y afectaba su operación.”"],
        ["Tarea", "“Necesitaba centralizar las solicitudes, definir responsables y permitir cambios sin perder control ni evidencia.”"],
        ["Acción", "“Levanté los flujos con cada área, organicé un catálogo, incorporé autorización del jefe responsable y control de ejecución por TI. Desarrollé con Python, React y PostgREST; añadí 2FA, roles, logs, doble autorización y reversión.”"],
        ["Resultado", "“La organización obtuvo un canal único, trazabilidad por solicitud y mejor control de cambios. El conocimiento dejó de depender de conversaciones dispersas.”"],
        ["Aprendizaje", "“Automatizar antes de ordenar el proceso solo acelera el desorden. Primero se aclaran reglas y responsables.”"],
    ]
    story.append(table_from_rows(star_rows, [85, 435], styles))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Preguntas de seguimiento que pueden hacerte", styles["h2"]))
    story.append(bullet("<b>¿Cómo levantaste requerimientos?</b> Entrevistas con responsables, recorrido del proceso, casos frecuentes, excepciones y validación del flujo propuesto.", styles))
    story.append(bullet("<b>¿Cómo controlaste cambios sensibles?</b> Roles, aprobación previa, doble autorización, registro de actividad y reversión controlada por TI.", styles))
    story.append(bullet("<b>¿Qué mejorarías hoy?</b> Fortalecer pruebas automatizadas, versionamiento formal, métricas de uso y desacoplar integraciones mediante APIs cuando la arquitectura lo permita.", styles))
    story.append(Spacer(1, 9))
    story.append(callout(
        "<b>No inventes métricas.</b> Si te preguntan cuánto redujiste el tiempo y no tienes medición, responde: "
        "“No quiero darle una cifra que no medí formalmente. Sí puedo demostrar que centralizamos el flujo, eliminamos "
        "pasos manuales y dejamos trazabilidad; hoy establecería línea base y KPI desde el inicio.”",
        styles,
        color=colors.HexColor("#FCEEEE"),
        border=RED,
    ))
    story.append(PageBreak())

    story += section_title("6. Segunda historia: NOVASOFT TI", styles)
    story.append(Paragraph(
        "<b>Versión de 75 segundos:</b> “En TI identificamos incidentes repetitivos y consultas que consumían capacidad. "
        "Analicé los patrones, definí qué casos podían automatizarse y desarrollé NOVASOFT TI con Python y Streamlit, "
        "con conexión controlada a información del ERP. La aplicación facilitó registrar, consultar y resolver casos "
        "frecuentes. Incorporé 2FA, usuarios, logs y registro de actividades para que la automatización no sacrificara "
        "control. El resultado fue una atención más consistente y conocimiento operativo convertido en herramienta.”",
        styles["body"],
    ))
    story.append(Paragraph("Lo que esta historia demuestra", styles["h2"]))
    for text in [
        "Orientación al servicio: el desarrollo parte del incidente y de la experiencia del usuario.",
        "Análisis: identificas patrones antes de automatizar.",
        "Integración: trabajas con información del ERP de manera controlada.",
        "Mantenibilidad: eliges una interfaz sencilla para facilitar adopción y soporte.",
        "Seguridad: autenticación, roles, logs y trazabilidad desde el diseño.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Tercera historia de respaldo: TalentFlow", styles["h2"]))
    story.append(Paragraph(
        "Úsala si preguntan por IA, experiencia de usuario o integración entre áreas. Explica que la IA apoyaba la asociación "
        "entre candidatos y requerimientos, pero no reemplazaba la decisión humana. Destaca el historial, los estados, los "
        "correos y la continuidad hacia exámenes, contratos y contratación.",
        styles["body"],
    ))
    story.append(callout(
        "<b>Frase fuerte:</b> “No presento la IA como una caja negra que decide. La utilizo para asistir una tarea, mantener "
        "criterios verificables y dejar a la persona responsable la decisión final.”",
        styles,
    ))
    story.append(PageBreak())

    story += section_title("7. Fundamentos técnicos que debes dominar", styles)
    technical_rows = [
        ["Tema", "Respuesta esencial"],
        ["API REST", "Recurso y contrato claro; GET consulta, POST crea, PUT/PATCH actualiza, DELETE elimina; códigos HTTP, autenticación, validación, versionado e idempotencia."],
        ["SQL", "Joins, agregaciones, índices, transacciones, integridad referencial, consultas parametrizadas, plan de ejecución y mínimo privilegio."],
        ["Pruebas", "Unitarias para lógica, integración para componentes, funcionales contra requerimiento, regresión antes de liberar y aceptación con usuario."],
        ["Liberación", "Cambio aprobado, respaldo, versión identificada, pruebas previas, ventana, monitoreo, plan de reversión y evidencia."],
        ["Seguridad", "Validar entrada, evitar inyección, proteger secretos, 2FA, RBAC, mínimo privilegio, logs sin datos sensibles y gestión de vulnerabilidades."],
        ["Logs", "Evento, fecha, usuario/correlación, acción y resultado; niveles adecuados; no registrar contraseñas, tokens ni datos innecesarios."],
        ["Integración ERP", "Preferir APIs o capa controlada; credenciales de servicio restringidas; transacciones, validaciones, trazabilidad y evitar escrituras directas no gobernadas."],
        ["Agilidad", "Backlog priorizado, historia de usuario, criterio de aceptación, entregas pequeñas, demostración, retroalimentación y retrospectiva."],
    ]
    story.append(table_from_rows(technical_rows, [95, 425], styles))
    story.append(Spacer(1, 12))
    story.append(callout(
        "<b>Regla para responder:</b> definición breve, ejemplo propio y riesgo o control. Así demuestras conocimiento aplicado, no teoría memorizada.",
        styles,
    ))
    story.append(PageBreak())

    story += section_title("8. Oracle, MySQL, Java y .NET: cómo manejar las brechas", styles)
    story.append(Paragraph(
        "La convocatoria menciona estas tecnologías como deseables. Tu base más fuerte es Python, React, SQL y aplicaciones "
        "sobre bases relacionales. No afirmes experiencia que no tienes; demuestra fundamentos transferibles y capacidad de aprendizaje.",
        styles["body"],
    ))
    add_qa(
        story,
        "¿Ha trabajado con Oracle?",
        "“Mi experiencia práctica más fuerte está en SQL y bases relacionales usadas en mis desarrollos. No presentaría Oracle "
        "como mi tecnología principal todavía. Sí manejo modelado, joins, transacciones, integridad, permisos y optimización de "
        "consultas, que son fundamentos transferibles. Ya estoy reforzando particularidades de Oracle como esquemas, secuencias, "
        "PL/SQL y planes de ejecución.”",
        styles,
    )
    add_qa(
        story,
        "¿Domina Java o .NET?",
        "“Mi stack principal ha sido Python, React y Streamlit. Puedo leer una arquitectura, entender contratos, datos e integraciones "
        "y aprender el framework definido por el equipo. Prefiero ser transparente sobre la curva de aprendizaje y compensarla con "
        "fundamentos de ingeniería, documentación y entregas controladas.”",
        styles,
    )
    story.append(Paragraph("Conceptos mínimos para repasar", styles["h2"]))
    for text in [
        "<b>Oracle:</b> esquema/usuario, secuencia, PL/SQL, tablespace, EXPLAIN PLAN, COMMIT/ROLLBACK.",
        "<b>MySQL:</b> InnoDB, AUTO_INCREMENT, índices, EXPLAIN, transacciones y procedimientos.",
        "<b>Java/.NET:</b> capas controlador–servicio–repositorio, inyección de dependencias, ORM, configuración por ambiente y manejo de excepciones.",
        "<b>Git:</b> rama por cambio, commits pequeños, pull request, revisión, resolución de conflictos y etiquetas de versión.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 10))
    story.append(callout(
        "La respuesta madura no es “aprendo rápido”. Es explicar <b>qué fundamento ya posees, qué brecha reconoces y cómo la cerrarías sin poner en riesgo una aplicación crítica.</b>",
        styles,
        color=colors.HexColor("#FFF8E5"),
        border=GOLD,
    ))
    story.append(PageBreak())

    story += section_title("9. Preguntas técnicas probables y respuestas", styles)
    add_qa(
        story,
        "¿Cómo aborda un requerimiento nuevo?",
        "Aclaro objetivo, usuario, proceso actual, reglas, excepciones, datos, integraciones y restricciones. Documento alcance y "
        "criterios de aceptación, propongo una solución viable, la valido con el usuario y divido la entrega en cambios pequeños.",
        styles,
    )
    add_qa(
        story,
        "¿Qué hace antes de llevar un cambio a producción?",
        "Revisión de código y configuración, pruebas unitarias/funcionales/integración según el cambio, validación con usuario, "
        "respaldo, aprobación, plan de despliegue y reversión. Después monitoreo logs, comportamiento y confirmo con el usuario.",
        styles,
    )
    add_qa(
        story,
        "¿Cómo diagnostica un incidente?",
        "Confirmo impacto y prioridad, reproduzco cuando es seguro, reviso cambios recientes y logs, aíslo capa de interfaz, servicio, "
        "integración o datos; mitigo primero si la operación está afectada, corrijo, valido y documento causa raíz y prevención.",
        styles,
    )
    add_qa(
        story,
        "¿Cómo diseña una integración segura?",
        "Contrato claro, autenticación, autorización mínima, validación de entrada y salida, manejo de errores, timeout y reintentos "
        "controlados, idempotencia cuando aplica, trazabilidad por correlación y protección de secretos.",
        styles,
    )
    add_qa(
        story,
        "¿Cómo decide si automatizar?",
        "Busco volumen, repetición, reglas estables, costo del error y disponibilidad de datos. Primero estandarizo el proceso; después "
        "automatizo. Si hay decisiones ambiguas o excepciones frecuentes, mantengo intervención humana.",
        styles,
    )
    story.append(PageBreak())

    story += section_title("10. Preguntas de comportamiento", styles)
    add_qa(
        story,
        "Hábleme de un desacuerdo con un usuario.",
        "Explica que separas la necesidad de la solución solicitada: escuchas, confirmas impacto, presentas restricciones y alternativas, "
        "acuerdas criterio de aceptación y documentas la decisión. Usa OSYA Portal como ejemplo de negociación entre áreas y TI.",
        styles,
    )
    add_qa(
        story,
        "¿Qué error ha cometido?",
        "Elige un error real y controlable, no una falsa virtud. Ejemplo: comenzar una solución con requisitos insuficientes, detectar "
        "reproceso y aprender a validar flujo y excepciones antes de desarrollar. Explica el cambio concreto en tu método.",
        styles,
    )
    add_qa(
        story,
        "¿Cómo prioriza varias solicitudes?",
        "Impacto en operación y usuarios, urgencia, riesgo, dependencia, esfuerzo y compromisos. Comunicas prioridad, responsable y "
        "estado; atiendes incidentes críticos sin perder visibilidad del backlog.",
        styles,
    )
    add_qa(
        story,
        "¿Por qué quiere trabajar en la UNAB?",
        "No respondas solo “por estabilidad”. Habla del reto: ecosistema institucional amplio, impacto en estudiantes/docentes, "
        "transformación digital, trabajo entre infraestructura y sistemas de información y posibilidad de construir capacidad sostenible.",
        styles,
    )
    add_qa(
        story,
        "¿Cuál es su principal fortaleza?",
        "“Puedo conversar con el usuario, construir la solución y cuestionarla desde seguridad y auditoría. Esa visión reduce vacíos "
        "entre requerimiento, código y control.”",
        styles,
    )
    story.append(PageBreak())

    story += section_title("11. Tu lectura del reto: “vi lo que necesitan”", styles)
    story.append(callout(
        "“Por la información pública de la UNAB, entiendo que TIC no administra una sola aplicación: sostiene un ecosistema académico "
        "y administrativo con plataformas críticas, bases Oracle y MySQL, servicios sobre Linux e integraciones entre áreas. En un "
        "entorno así, desarrollar bien significa comprender dependencias, proteger continuidad y dejar pruebas y documentación.<br/><br/>"
        "Mi experiencia puede aportar especialmente en tres frentes: convertir requerimientos recurrentes en flujos controlados; "
        "construir soluciones e integraciones con trazabilidad; y sumar una mirada de seguridad desde el diseño. Antes de proponer una "
        "tecnología, mi primer paso sería conocer sus estándares, arquitectura, backlog y usuarios prioritarios.”",
        styles,
        color=colors.HexColor("#EAF7F4"),
        border=TEAL,
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Tres hipótesis para conversar, no para presentar como diagnóstico", styles["h2"]))
    for text in [
        "<b>Demanda:</b> con decenas de aplicaciones y proyectos, probablemente el reto no sea solo construir, sino priorizar y mantener.",
        "<b>Integración:</b> Banner, portales y aplicaciones especializadas requieren contratos, datos y cambios bien gobernados.",
        "<b>Conocimiento:</b> documentación y trazabilidad son esenciales para evitar dependencia de personas y facilitar soporte.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Usa expresiones como “por lo que pude investigar”, “mi hipótesis sería” y “quisiera entender cómo lo manejan actualmente”. "
        "Eso demuestra preparación sin pretender conocer problemas internos que aún no has visto.",
        styles["body"],
    ))
    story.append(PageBreak())

    story += section_title("12. Preguntas inteligentes para la directora", styles)
    questions = [
        "¿Cuáles son las aplicaciones o procesos que concentrarían las prioridades iniciales de esta posición?",
        "¿Cómo se distribuye hoy el trabajo entre Sistemas de Información, Infraestructura y las áreas usuarias?",
        "¿Cuál es el stack principal para desarrollos internos y qué lineamientos de arquitectura, pruebas y control de cambios utilizan?",
        "¿Qué tipo de integraciones son más frecuentes alrededor de Banner y las demás aplicaciones institucionales?",
        "¿Cómo se gestiona el backlog: incidentes, mantenimiento, deuda técnica y nuevos requerimientos?",
        "¿Qué resultado le permitiría decir, después de los primeros meses, que la persona seleccionada está generando valor?",
    ]
    for i, text in enumerate(questions, 1):
        story.append(KeepTogether([
            Paragraph(f"{i:02d}", pstyle(f"qnum{i}", size=16, leading=18, font="Raleway-Bold", color=GOLD)),
            Paragraph(text, styles["body"]),
            Spacer(1, 5),
        ]))
    story.append(Spacer(1, 10))
    story.append(callout(
        "<b>Elige solo dos o tres.</b> Para una entrevista de 20 minutos, prioriza la primera y la última. Si ya respondieron "
        "alguna durante la conversación, no la repitas.",
        styles,
    ))
    story.append(PageBreak())

    story += section_title("13. Guion exacto para 20 minutos", styles)
    time_rows = [
        ["Tiempo", "Objetivo", "Qué haces"],
        ["0:00–1:30", "Abrir", "Agradecimiento y presentación de 90 segundos."],
        ["1:30–5:30", "Demostrar encaje", "OSYA Portal: problema, decisión técnica, controles y valor."],
        ["5:30–9:00", "Demostrar operación", "NOVASOFT TI o NEXUS según la pregunta."],
        ["9:00–14:00", "Responder", "Preguntas técnicas y de comportamiento; respuestas de 45–75 segundos."],
        ["14:00–16:30", "Leer el reto", "Conecta investigación UNAB con tu forma de trabajo."],
        ["16:30–18:30", "Preguntar", "Dos preguntas inteligentes a la directora."],
        ["18:30–20:00", "Cerrar", "Síntesis de valor, agradecimiento y entrega del portafolio."],
    ]
    story.append(table_from_rows(time_rows, [75, 110, 335], styles))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Cierre de 30 segundos", styles["h2"]))
    story.append(callout(
        "“Gracias por la conversación. Me interesa el reto porque combina precisamente lo que he venido construyendo: "
        "aplicaciones para procesos reales, integración con datos y una mirada fuerte de seguridad y trazabilidad. Sé que "
        "debo aprender la arquitectura y los estándares propios de la UNAB, y llegaría con disposición para hacerlo de forma "
        "ordenada, colaborar con el equipo y generar valor desde las primeras prioridades que ustedes definan.”",
        styles,
        color=colors.HexColor("#FFF8E5"),
        border=GOLD,
    ))
    story.append(PageBreak())

    story += section_title("14. Cómo usar el portafolio físico", styles)
    for text in [
        "<b>Imprime una copia a color</b>, tamaño carta, una cara por hoja, papel de 90–120 g. Utiliza una carpeta blanca limpia.",
        "Lleva además <b>dos copias de la HV</b>, libreta pequeña y bolígrafo. No vuelvas a imprimir certificados salvo que te los soliciten.",
        "No abras el portafolio al empezar. Cuando pregunten por experiencia, di: “Traje un resumen visual; si le parece, puedo mostrarle el flujo de uno de los proyectos”.",
        "En 20 minutos muestra máximo tres páginas: mapa del ecosistema, OSYA Portal y ajuste a UNAB. Deja el documento completo al final.",
        "No entregues capturas con información sensible. Las incluidas están protegidas y se concentran en estructura visual.",
        "No leas las páginas. Señala el problema, la decisión y el control. La entrevistadora debe mirarte a ti, no quedarse descifrando el documento.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Frase para ofrecerlo", styles["h2"]))
    story.append(callout(
        "“Preparé un portafolio breve con los problemas que abordé, la arquitectura general y los controles aplicados. "
        "No contiene datos sensibles. ¿Le parece si uso una página para explicar el proyecto más relacionado con el cargo?”",
        styles,
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph("La respuesta sincera", styles["h2"]))
    story.append(Paragraph(
        "Sí, llevar el portafolio es una buena decisión, pero no porque el documento consiga el cargo. Funciona si te ayuda a "
        "explicar con claridad, demuestra preparación y deja evidencia después de una entrevista corta. Si intentas presentarlo "
        "completo o lo usas para exagerar, juega en contra.",
        styles["body"],
    ))
    story.append(PageBreak())

    story += section_title("15. Plan de estudio: 16 al 21 de julio", styles)
    schedule_rows = [
        ["Fecha", "Bloque", "Resultado verificable"],
        ["Jue. 16", "Leer secciones 1–3 y 7. Revisar portafolio completo. Escribir tres datos reales que puedas cuantificar.", "Mapa cargo–experiencia y lista de métricas honestas."],
        ["Vie. 17", "Practicar apertura, OSYA Portal y NOVASOFT. Estudiar API, SQL, pruebas, liberación y seguridad.", "Tres audios: 90 s, 2 min y 5 min; sin leer."],
        ["Sáb. 18", "Leer secciones 2, 8 y 9. Repasar Oracle/MySQL, Git y arquitectura por capas. Dibujar OSYA Portal.", "Explicar arquitectura en una hoja y responder 10 preguntas técnicas."],
        ["Dom. 19", "Simulación completa de 20 minutos con cronómetro. Revisar lenguaje corporal y respuestas largas.", "Una grabación completa y lista de cinco correcciones."],
        ["Lun. 20", "Dos simulaciones: técnica y ejecutiva. Imprimir, ordenar carpeta y verificar ruta/documentos.", "Respuestas menores a 75 s y carpeta lista."],
        ["Mar. 21", "Repaso de una página, respiración, desayuno y llegada anticipada. No estudiar temas nuevos.", "Llegar al campus entre 9:00 y 9:05 a. m."],
    ]
    story.append(table_from_rows(schedule_rows, [58, 282, 180], styles))
    story.append(Spacer(1, 14))
    story.append(callout(
        "<b>Método diario:</b> 25 minutos de lectura; 20 minutos hablando en voz alta; 15 minutos corrigiendo. "
        "Prepararse para entrevista exige producir respuestas, no solo consumir información.",
        styles,
    ))
    story.append(PageBreak())

    story += section_title("16. Simulacro de evaluación", styles)
    prompts = [
        "Preséntese en 90 segundos.",
        "Cuénteme un desarrollo del que se sienta orgulloso.",
        "¿Cómo levanta y documenta requerimientos?",
        "¿Cómo garantiza calidad antes de producción?",
        "¿Cómo integraría una aplicación nueva con un sistema institucional?",
        "¿Cómo maneja seguridad, roles y trazabilidad?",
        "Hábleme de un incidente difícil y cómo lo resolvió.",
        "¿Qué experiencia tiene con Oracle, MySQL, Java o .NET?",
        "¿Qué haría durante sus primeras semanas?",
        "¿Por qué la UNAB y qué pregunta tiene para mí?",
    ]
    for i, prompt in enumerate(prompts, 1):
        story.append(Paragraph(f"<b>{i}. {prompt}</b>", styles["body"]))
        story.append(Paragraph("Notas: ____________________________________________________________________________________", styles["small"]))
        story.append(Spacer(1, 5))
    story.append(Spacer(1, 8))
    score_rows = [
        ["Criterio", "1", "3", "5"],
        ["Claridad", "Divaga", "Se entiende", "Idea directa y memorable"],
        ["Evidencia", "Generaliza", "Da ejemplo", "Explica decisión y resultado"],
        ["Técnica", "Enumera herramientas", "Describe uso", "Explica controles y trade-offs"],
        ["Tiempo", "> 2 min", "75–120 s", "45–75 s"],
        ["Naturalidad", "Recita", "Conversacional", "Escucha y adapta"],
    ]
    story.append(table_from_rows(score_rows, [150, 110, 120, 140], styles))
    story.append(PageBreak())

    story += section_title("17. Recomendaciones de comunicación y presencia", styles)
    for text in [
        "<b>Vestuario:</b> formal sobrio; camisa clara, pantalón oscuro, zapatos limpios. Evita accesorios o fragancias que distraigan.",
        "<b>Llegada:</b> apunta a estar en el campus 30–35 minutos antes. La oficina está en el primer piso de Biblioteca.",
        "<b>Postura:</b> espalda recta, manos visibles, movimientos tranquilos. Saluda por nombre y agradece el tiempo.",
        "<b>Escucha:</b> deja terminar la pregunta. Si es amplia, confirma: “¿Quiere que lo aborde desde arquitectura o desde el proceso?”",
        "<b>Respuesta:</b> empieza por la conclusión, continúa con evidencia y cierra con aprendizaje o valor.",
        "<b>Desconocimiento:</b> “No lo he implementado directamente; esto es lo que sí conozco y así abordaría la brecha”.",
        "<b>Confidencialidad:</b> no reveles nombres, cuentas, valores ni datos de trabajadores o clientes.",
        "<b>Actitud:</b> evita “yo hice todo solo”. Reconoce usuarios, responsables y equipos; enfatiza tu contribución concreta.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 14))
    story.append(callout(
        "La seguridad que necesitas no viene de parecer que sabes todo. Viene de poder explicar con precisión lo que hiciste, "
        "por qué lo hiciste y qué aprendiste.",
        styles,
        color=colors.HexColor("#EAF7F4"),
        border=TEAL,
    ))
    story.append(PageBreak())

    story += section_title("18. Hoja de repaso para la mañana de la entrevista", styles)
    story.append(Paragraph("CUATRO IDEAS QUE DEBEN RECORDAR DE MÍ", styles["h2"]))
    for text in [
        "Construyo soluciones a partir de procesos reales y contacto con usuarios.",
        "Tengo experiencia en Python, React, Streamlit, SQL, automatización e integración.",
        "Incorporo seguridad, roles, 2FA, logs, trazabilidad y documentación.",
        "Mi experiencia de auditoría me permite pensar en riesgo, continuidad y evidencia.",
    ]:
        story.append(bullet(text, styles))
    story.append(Spacer(1, 9))
    story.append(Paragraph("TRES HISTORIAS", styles["h2"]))
    story.append(bullet("OSYA Portal: solicitudes, autorización, ERP, 2FA, logs y reversión.", styles))
    story.append(bullet("NOVASOFT TI: incidentes repetitivos, Streamlit, ERP y trazabilidad.", styles))
    story.append(bullet("TalentFlow: selección, RQ, IA asistida y continuidad hacia contratación.", styles))
    story.append(Spacer(1, 9))
    story.append(Paragraph("DOS PREGUNTAS", styles["h2"]))
    story.append(bullet("¿Cuáles serían las aplicaciones o prioridades iniciales del cargo?", styles))
    story.append(bullet("¿Qué resultado definiría un buen desempeño durante los primeros meses?", styles))
    story.append(Spacer(1, 9))
    story.append(Paragraph("UNA FRASE DE CIERRE", styles["h2"]))
    story.append(callout(
        "“Puedo aportar una combinación de desarrollo, comprensión del proceso y seguridad. Llegaría a aprender su "
        "arquitectura, colaborar con el equipo y convertir prioridades en soluciones mantenibles y documentadas.”",
        styles,
    ))
    story.append(Spacer(1, 18))
    story.append(Paragraph("LISTA DE SALIDA", styles["h2"]))
    for text in [
        "[ ] Documento de identidad",
        "[ ] Dos hojas de vida",
        "[ ] Portafolio impreso",
        "[ ] Libreta y bolígrafo",
        "[ ] Celular en silencio",
        "[ ] Ruta y hora confirmadas",
    ]:
        story.append(bullet(text, styles))
    story.append(PageBreak())

    story += section_title("19. Fuentes consultadas", styles)
    sources = [
        "[1] Convocatoria Ingeniero(a) de Sistemas y Operación TIC / Desarrollador(a), reproducida por Colombia Jobs Expertini a partir de la publicación UNAB.",
        "[2] UNAB. “Conoce más sobre las tareas que realiza el área de TIC”. Publicación institucional, 13 de junio de 2023.",
        "[3] UNAB. “Infraestructura Tecnológica y Sistemas de Información: un solo equipo que apoya la operación de toda la UNAB”. 20 de junio de 2023.",
        "[4] UNAB. Estrategia Institucional 2025–2032 resumida. Incluye referencia al PETIC 2032.",
        "[5] UNAB. Plan de Desarrollo: transformación digital, automatización, analítica y experiencia digital del usuario.",
        "[6] Repositorio UNAB. Política Gestión de Incidentes de Seguridad de la Información, 2025.",
        "[7] UNAB. “Conoce todo sobre la actualización de Banner 9 a un clic”.",
        "[8] Repositorio UNAB. Política para creación y manejo de cuentas y contraseñas para usuarios.",
        "[9] Congreso de Colombia. Ley 30 de 1992, artículos 3, 31, 32 y 56: inspección, vigilancia, calidad y creación del SNIES.",
        "[10] Ministerio de Educación Nacional. Decreto 1767 de 2006: disponibilidad, automatización, veracidad, seguridad y confidencialidad de la información SNIES.",
        "[11] Superintendencia de Industria y Comercio. Ley 1581 de 2012: principios de finalidad, seguridad y confidencialidad en datos personales.",
        "[12] Consejo Nacional de Acreditación. Cuadros Maestros 2025 y orientaciones de autoevaluación: información histórica, evidencia y articulación con SNIES.",
    ]
    for source in sources:
        story.append(bullet(source, styles))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Enlaces", styles["h2"]))
    links = [
        "https://unab.edu.co/conoce-mas-sobre-las-tareas-que-realiza-el-area-de-tic/",
        "https://unab.edu.co/infraestructura-tecnologica-y-sistemas-de-informacion-un-solo-equipo-que-apoya-la-operacion-de-toda-la-unab/",
        "https://unab.edu.co/plan_desarrollo/",
        "https://unab.edu.co/NewFolder/Estrategia%20Institucional%202025-2032%20Resumida.pdf",
        "https://repository.unab.edu.co/handle/20.500.12749/32318",
        "https://unab.edu.co/publicacion414/",
        "https://www.mineducacion.gov.co/1621/articles-85860_archivo_pdf.pdf",
        "https://snies.mineducacion.gov.co/1778/articles-391237_Decreto_1767.pdf",
        "https://sedeelectronica.sic.gov.co/sites/default/files/normatividad/Ley_1581_2012.pdf",
        "https://www.cna.gov.co/portal/427106:Cuadros-Maestros-Acreditacion-CNA-Actualizados-2025",
    ]
    for link in links:
        story.append(Paragraph(link, styles["small"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 18))
    story.append(callout(
        "<b>Nota de rigor:</b> los datos de 75 proyectos y más de 51 aplicaciones corresponden a una publicación institucional "
        "de 2023. Úsalos como contexto histórico público, no como cifras actuales garantizadas.",
        styles,
        color=colors.HexColor("#FFF8E5"),
        border=GOLD,
    ))

    doc.build(story, onFirstPage=study_page, onLaterPages=study_page)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    portfolio_path = OUTPUT_DIR / "Portafolio_Desarrollo_Ivan_Cardona_UNAB.pdf"
    study_path = OUTPUT_DIR / "Plan_Preparacion_Entrevista_UNAB_Ivan_Cardona.pdf"
    generate_portfolio(portfolio_path)
    generate_study_plan(study_path)
    print(f"Portafolio generado: {portfolio_path}")
    print(f"Plan generado: {study_path}")


if __name__ == "__main__":
    main()
