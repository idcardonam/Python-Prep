#!/usr/bin/env python3
"""Genera carta de presentación en PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "entregables"

MARGIN_LEFT = 25 * mm
MARGIN_RIGHT = 25 * mm
MARGIN_TOP = 20 * mm
MARGIN_BOTTOM = 20 * mm


def build_styles():
    styles = getSampleStyleSheet()
    return {
        "header": ParagraphStyle(
            "Header",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#2B2B2B"),
            alignment=TA_LEFT,
        ),
        "subject": ParagraphStyle(
            "Subject",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#2B2B2B"),
            alignment=TA_LEFT,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#2B2B2B"),
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "closing": ParagraphStyle(
            "Closing",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#2B2B2B"),
            alignment=TA_LEFT,
            spaceBefore=6,
        ),
        "signature": ParagraphStyle(
            "Signature",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#2B2B2B"),
            alignment=TA_LEFT,
            spaceBefore=16,
        ),
    }


def generate_letter_pdf(content: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )
    styles = build_styles()
    story = []

    for line in content["encabezado"]:
        story.append(Paragraph(line, styles["header"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(content["destinatario"], styles["header"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(content["asunto"], styles["subject"]))

    for paragraph in content["cuerpo"]:
        story.append(Paragraph(paragraph, styles["body"]))

    for line in content["cierre"]:
        story.append(Paragraph(line, styles["closing"]))

    story.append(Paragraph(content["firma"], styles["signature"]))

    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generar carta de presentación PDF")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    content = {
        "encabezado": [
            "Bucaramanga, 10 de julio de 2026",
            "Ivan David Cardona Mendoza",
            "Ingeniero de Sistemas",
            "Celular: 304 558 7767",
            "Correo: idcm@hotmail.es",
        ],
        "destinatario": (
            "Señores<br/>"
            "Universidad Autónoma de Bucaramanga – UNAB<br/>"
            "Departamento de Selección de Personal<br/>"
            "Ciudad"
        ),
        "asunto": (
            "<b>Asunto:</b> Postulación al cargo de Auxiliar administrativo TIC – "
            "Convocatoria Departamento de Tecnologías de Información y la Comunicación"
        ),
        "cuerpo": [
            (
                "Reciban un cordial saludo. Me dirijo a ustedes con el interés de participar "
                "en la convocatoria para el cargo de Auxiliar administrativo TIC, convencido "
                "de que mi experiencia en soporte a usuarios, seguimiento de incidentes y "
                "acompañamiento de la infraestructura tecnológica puede aportar valor al "
                "trabajo que realiza el Departamento de Tecnologías de Información y la "
                "Comunicación de la Universidad."
            ),
            (
                "Conozco el peso que tiene este rol dentro de una institución educativa. "
                "Cuando un docente, un estudiante o un funcionario administrativo tiene un "
                "fallo de conectividad, un equipo que no responde o una plataforma que no "
                "carga, no se trata solo de un ticket: se trata de interrumpir una clase, "
                "retrasar un trámite o frenar una labor que debía salir a tiempo. Por eso "
                "he cultivado una forma de trabajar centrada en la escucha, la respuesta "
                "oportuna y el registro claro de cada caso. No me conformo con “reiniciar y "
                "ver si pasa”; me quedo hasta entender qué ocurrió, qué se hizo y qué debe "
                "quedar documentado para la siguiente vez."
            ),
            (
                "Soy Ingeniero de Sistemas, con Tarjeta Profesional vigente, y Especialista "
                "en Seguridad Informática. Además, cuento con formación técnica previa en "
                "Análisis y Desarrollo de Sistemas, lo que me da una base sólida para "
                "comprender tanto el lado del usuario como el funcionamiento de la "
                "infraestructura que soporta los servicios. En los últimos años he trabajado "
                "en funciones de soporte y seguridad informática, atención de incidentes, "
                "documentación de solicitudes, aplicación de políticas de seguridad y apoyo "
                "en tareas de mantenimiento tecnológico. En Financiera Comultrasan participé "
                "en auditorías internas de TI, seguimiento de hallazgos, evaluación de "
                "disponibilidad de servicios y reporte de anomalías, actividades que "
                "fortalecieron mi criterio para identificar cuándo un caso puede resolverse "
                "en primer nivel y cuándo debe escalarse con la información adecuada. "
                "Anteriormente, en Constructodo de la Guajira S.A.S, apoyé la estructuración "
                "de procesos del área de sistemas y el diseño de políticas de seguridad "
                "alineadas a la operación diaria."
            ),
            (
                "Entre las competencias que puedo poner al servicio de la UNAB se encuentran: "
                "soporte técnico de primer nivel, diagnóstico inicial de incidentes, "
                "acompañamiento en tareas de mantenimiento preventivo, actualización de "
                "inventarios, monitoreo básico de servicios, documentación de cambios y "
                "cumplimiento de lineamientos de seguridad de la información. Manejo entornos "
                "Windows y Linux, bases de datos, herramientas de seguimiento y ofimática "
                "avanzada. También tengo certificación como Auditor Interno ISO/IEC 27001:2022, "
                "lo que refuerza mi compromiso con el tratamiento responsable de la información "
                "y con las buenas prácticas exigidas en un entorno institucional."
            ),
            (
                "Me motiva especialmente la posibilidad de vincularme a una universidad con "
                "la trayectoria de la UNAB, donde el trabajo de TIC no se limita a mantener "
                "equipos encendidos, sino a sostener el ecosistema que permite enseñar, "
                "investigar y prestar servicios con calidad. Valoro el trabajo en equipo, la "
                "comunicación respetuosa con el usuario y la disposición para aprender de "
                "quienes conocen la operación de redes e infraestructura desde adentro. "
                "Tengo disponibilidad para desempeñar la labor en modalidad presencial en "
                "Bucaramanga, Campus El Jardín, y para cumplir con las etapas y requisitos "
                "del proceso de selección."
            ),
            (
                "Adjunto mi hoja de vida y quedo atento a cualquier información adicional "
                "que la Universidad requiera. Agradezco de antemano el tiempo dedicado a "
                "revisar mi postulación y expreso mi genuino interés en aportar, con "
                "responsabilidad y vocación de servicio, al fortalecimiento del soporte "
                "tecnológico de la comunidad universitaria."
            ),
        ],
        "cierre": ["Atentamente,"],
        "firma": "Ivan David Cardona Mendoza<br/>Ingeniero de Sistemas<br/>304 558 7767 | idcm@hotmail.es",
    }

    generate_letter_pdf(content, args.output)
    word_count = sum(len(p.split()) for p in content["cuerpo"])
    print(f"Carta generada: {args.output}")
    print(f"Palabras aproximadas en el cuerpo: {word_count}")


if __name__ == "__main__":
    main()
