# -*- coding: utf-8 -*-
"""Genera MANUAL_OPERACION.pdf a partir del contenido institucional."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "MANUAL_OPERACION.pdf"
AZUL = HexColor("#1B3A5C")
DORADO = HexColor("#C4A035")
GRIS = HexColor("#4A5568")
FONDO = HexColor("#F4F1E8")
LINEA = HexColor("#D6D0C4")


def estilos():
    base = getSampleStyleSheet()
    s = {}
    s["marca"] = ParagraphStyle(
        "marca", parent=base["Normal"], fontName="Times-Bold", fontSize=9,
        textColor=DORADO, alignment=TA_CENTER, spaceAfter=4, tracking=1,
    )
    s["titulo"] = ParagraphStyle(
        "titulo", parent=base["Title"], fontName="Times-Bold", fontSize=22,
        textColor=AZUL, alignment=TA_CENTER, spaceAfter=8, leading=26,
    )
    s["sub"] = ParagraphStyle(
        "sub", parent=base["Normal"], fontName="Times-Italic", fontSize=11,
        textColor=GRIS, alignment=TA_CENTER, spaceAfter=6,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"], fontName="Times-Bold", fontSize=13,
        textColor=AZUL, spaceBefore=16, spaceAfter=8, borderPadding=3,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"], fontName="Times-Bold", fontSize=11,
        textColor=HexColor("#2C5282"), spaceBefore=10, spaceAfter=6,
    )
    s["p"] = ParagraphStyle(
        "p", parent=base["Normal"], fontName="Times-Roman", fontSize=10,
        textColor=HexColor("#1A202C"), alignment=TA_JUSTIFY, leading=14,
        spaceAfter=7,
    )
    s["li"] = ParagraphStyle(
        "li", parent=s["p"], alignment=TA_LEFT, leftIndent=4, spaceAfter=3,
    )
    s["cell"] = ParagraphStyle(
        "cell", parent=base["Normal"], fontName="Times-Roman", fontSize=8,
        leading=11, textColor=HexColor("#1A202C"),
    )
    s["cellh"] = ParagraphStyle(
        "cellh", parent=s["cell"], fontName="Times-Bold", textColor=white,
    )
    s["pie"] = ParagraphStyle(
        "pie", parent=base["Normal"], fontName="Times-Italic", fontSize=8,
        textColor=GRIS, alignment=TA_CENTER,
    )
    s["code"] = ParagraphStyle(
        "code", parent=base["Code"], fontName="Courier", fontSize=8,
        textColor=AZUL, leading=11, spaceAfter=6, leftIndent=8,
    )
    return s


def tabla(filas: list[list[str]], st, anchos=None):
    data = []
    for i, fila in enumerate(filas):
        sty = st["cellh"] if i == 0 else st["cell"]
        data.append([Paragraph(str(c).replace("\n", "<br/>"), sty) for c in fila])
    t = Table(data, colWidths=anchos, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), AZUL),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#F7FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINEA),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AZUL)
    canvas.rect(0, LETTER[1] - 28, LETTER[0], 28, fill=1, stroke=0)
    canvas.setFillColor(DORADO)
    canvas.rect(0, LETTER[1] - 32, LETTER[0], 4, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(2 * cm, LETTER[1] - 20, "UNAB  ·  Dirección de TIC  ·  Estadísticas TIC")
    canvas.drawRightString(LETTER[0] - 2 * cm, LETTER[1] - 20, "Portal de cuentas Gmail")
    canvas.setFillColor(AZUL)
    canvas.rect(0, 0, LETTER[0], 22, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(2 * cm, 8, "Uso interno del área  ·  No publicar CSV de origen")
    canvas.drawRightString(LETTER[0] - 2 * cm, 8, f"Página {doc.page}")
    canvas.restoreState()


def construir():
    st = estilos()
    story = []

    story.append(Spacer(1, 1.6 * cm))
    story.append(Paragraph("UNIVERSIDAD AUTÓNOMA DE BUCARAMANGA", st["marca"]))
    story.append(Paragraph("Dirección de Tecnologías de la Información y las Comunicaciones", st["sub"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Manual de operación", st["titulo"]))
    story.append(Paragraph("Portal de gestión de cuentas Gmail institucionales", st["sub"]))
    story.append(Paragraph("Depuración de cuentas · Campaña 2FA · Seguimiento en SharePoint", st["p"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Versión septiembre 2026  ·  Documento para uso general del área", st["pie"]))
    story.append(Spacer(1, 0.8 * cm))

    story.append(Paragraph("1. Propósito", st["h1"]))
    story.append(Paragraph(
        "Este portal concentra en un solo enlace el seguimiento de las cuentas Gmail institucionales: "
        "depuración (inventario, inactividad y bloqueos), campaña de autenticación en dos pasos (2FA) "
        "de estudiantes vigentes, y registro de la meta del proyecto y de las acciones realizadas. "
        "No se requiere saber programar para consultar el sitio ni para la actualización periódica de archivos.",
        st["p"],
    ))
    story.append(Paragraph(
        "<b>Dirección del portal</b><br/>"
        "https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/SitePages/CollabHome.aspx",
        st["p"],
    ))
    story.append(Paragraph(
        "El sitio se llama <b>Proyecto Depuración Gmail</b>. Es un grupo privado: solo ingresan las personas "
        "a las que se les haya concedido permiso.",
        st["p"],
    ))

    story.append(Paragraph("2. Qué contiene el portal", st["h1"]))
    story.append(tabla(
        [
            ["Pieza", "Qué se ve", "Cómo se mantiene"],
            [
                "Tablero Power BI",
                "Totales, estados de cuenta, avance",
                "Tres CSV en etl/output y listas. Refresco cada hora.",
            ],
            [
                "Resumen 2FA",
                "Cobertura por facultad y pendientes",
                "Informe HTML y un CSV de pendientes en etl/output.",
            ],
            [
                "Listas SharePoint",
                "Meta del proyecto y bitácora de acciones",
                "Se editan en el sitio, a mano. No las genera el actualizador.",
            ],
        ],
        st,
        [3.8 * cm, 5.8 * cm, 6.6 * cm],
    ))
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph(
        "Las listas no son archivos: no se «suben». Se abren en el menú izquierdo (MetaProyecto, Acciones) "
        "y se editan como una tabla. Los números de inventario del tablero salen de "
        "cuentas_powerbi.csv, dependencias_powerbi.csv y capacidad_powerbi.csv, no de las listas "
        "Cuentas, Dependencias o capacidad.",
        st["p"],
    ))

    story.append(Paragraph("3. Acceso: consulta y operación", st["h1"]))
    story.append(Paragraph(
        "Los permisos se dan en SharePoint. Hay dos perfiles.",
        st["p"],
    ))
    story.append(Paragraph("3.1 Consulta (revisar el portal)", st["h2"]))
    story.append(Paragraph(
        "Permite abrir el tablero, el Resumen 2FA y las listas. No reemplaza archivos en etl/output.",
        st["p"],
    ))
    story.append(Paragraph(
        "1. Entre al sitio Proyecto Depuración Gmail.<br/>"
        "2. Engranaje (arriba a la derecha) → Permisos del sitio (o Información del sitio → Permisos).<br/>"
        "3. Compartir sitio / Invitar a personas.<br/>"
        "4. Escriba el correo institucional.<br/>"
        "5. Nivel: <b>Lectura</b> (grupo Visitantes).<br/>"
        "6. Confirme. La persona recibirá aviso o verá el sitio en SharePoint.",
        st["li"],
    ))
    story.append(Paragraph(
        "También puede usar Compartir en la página de inicio y elegir «Puede ver».",
        st["p"],
    ))

    story.append(Paragraph("3.2 Operación (cargar archivos y editar listas)", st["h2"]))
    story.append(Paragraph(
        "Permite subir los seis archivos a etl/output, editar MetaProyecto y Acciones, y ejecutar "
        "actualizar.bat en el equipo del área.",
        st["p"],
    ))
    story.append(Paragraph(
        "Mismos pasos de invitación, con nivel <b>Edición</b> (grupo Miembros).",
        st["p"],
    ))
    story.append(Paragraph(
        "La carpeta etl/input guarda CSV de origen. En esa carpeta: menú … → Administrar acceso → "
        "dejar solo al personal de operación. El resto del sitio puede ser de consulta.",
        st["p"],
    ))

    story.append(Paragraph("3.3 Informe Power BI", st["h2"]))
    story.append(Paragraph(
        "Si el tablero pide licencia o indica que no hay permiso: en app.powerbi.com, área de trabajo "
        "del informe → Acceso. Agregue el mismo correo como Visor (consulta) o Colaborador (si debe "
        "pulsar «Actualizar ahora» sobre el conjunto de datos).",
        st["p"],
    ))

    story.append(Paragraph("4. Uso diario (consulta)", st["h1"]))
    story.append(Paragraph(
        "1. Abra el enlace del apartado 1 e inicie sesión con la cuenta institucional.<br/>"
        "2. En la portada verá el tablero de depuración.<br/>"
        "3. Resumen 2FA abre el informe de estudiantes vigentes sin 2FA. Use facultad y programa. "
        "«Descargar CSV pendientes» abre un archivo; en Excel filtre la columna facultad.<br/>"
        "4. MetaProyecto: consulte o ajuste la meta (requiere edición).<br/>"
        "5. Acciones: consulte o registre lo ejecutado.",
        st["li"],
    ))
    story.append(Paragraph(
        "Si el tablero parece desactualizado, espere el refresco horario o solicite «Actualizar ahora» "
        "a quien tenga rol de operación en Power BI.",
        st["p"],
    ))

    story.append(PageBreak())
    story.append(Paragraph("5. Actualización periódica de datos", st["h1"]))
    story.append(Paragraph(
        "Cada vez que exista un corte nuevo de Google Admin (en la práctica, mensual). Lo realiza "
        "quien tenga perfil de operación.",
        st["p"],
    ))

    story.append(Paragraph("5.1 Carpeta de entrada (insumos)", st["h2"]))
    story.append(Paragraph(
        "Reúna en una sola carpeta del PC únicamente lo que sale de los sistemas. No mezcle HTML ni CSV de Power BI.",
        st["p"],
    ))
    story.append(tabla(
        [
            ["Archivo", "¿Obligatorio?", "Origen"],
            [
                "User_Download_….csv",
                "Sí",
                "Google Admin Console, informe de usuarios (todas las cuentas del dominio).",
            ],
            [
                "CSV de inscritos o prematriculados (uno o varios)",
                "Sí (para 2FA)",
                "Extracto académico del periodo.",
            ],
            [
                "VISTA DE CURRICULO.xlsx",
                "No",
                "Catálogo de planes.",
            ],
        ],
        st,
        [5.2 * cm, 3.4 * cm, 7.6 * cm],
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "El mismo User_Download alimenta el tablero de depuración y el cruce 2FA.",
        st["p"],
    ))

    story.append(Paragraph("5.2 Ejecutar el actualizador", st["h2"]))
    story.append(Paragraph(
        "1. Doble clic en Python-Prep\\cruce_cuentas\\actualizar.bat.<br/>"
        "2. Cuando pida la ruta: en el Explorador abra la carpeta del 5.1, clic en la barra de dirección, "
        "copie (Ctrl+C) y pegue en la ventana. Enter.<br/>"
        "3. Espere uno a tres minutos hasta ver LISTO.<br/>"
        "4. Se abre en el escritorio Archivos_SharePoint_AAAA-MM-DD (la fecha evita mezclar cortes).",
        st["li"],
    ))

    story.append(Paragraph("5.3 Seis archivos a SharePoint (etl / output)", st["h2"]))
    story.append(tabla(
        [
            ["Archivo", "Función"],
            ["cuentas_powerbi.csv", "Tablero: detalle de cuentas"],
            ["dependencias_powerbi.csv", "Tablero: resumen por dependencia"],
            ["capacidad_powerbi.csv", "Tablero: licencias e inventario"],
            ["resumen.html", "Informe 2FA para consulta"],
            ["listado_sin_2fa.html", "Listado 2FA de trabajo"],
            ["02_estudiantes_sin_2fa.csv", "Descarga de pendientes (filtrar facultad en Excel)"],
        ],
        st,
        [7 * cm, 9.2 * cm],
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "No suba el archivo LEAME, ni los CSV por facultad (sin_2fa_…), ni 00_universo.csv. "
        "Esos quedan en el PC, en cruce_cuentas\\salida\\.",
        st["p"],
    ))

    story.append(Paragraph("5.4 Cómo cargar", st["h2"]))
    story.append(Paragraph(
        "1. Sitio → Documentos → etl → output.<br/>"
        "2. Seleccione los seis archivos de la carpeta del escritorio.<br/>"
        "3. Arrástrelos a output. Si pregunta Reemplazar, confirme.<br/>"
        "4. Abra el portal y verifique Resumen 2FA (fecha del corte).<br/>"
        "5. Power BI mostrará el corte en la siguiente hora, o use Actualizar ahora en el conjunto de datos.",
        st["li"],
    ))

    story.append(Paragraph("5.5 Programar Power BI cada hora (una sola vez)", st["h2"]))
    story.append(Paragraph(
        "1. https://app.powerbi.com con cuenta institucional.<br/>"
        "2. Área de trabajo → conjunto de datos (no el informe).<br/>"
        "3. … → Configuración → Actualización programada.<br/>"
        "4. Activar, frecuencia Cada hora, zona Bogotá. Guardar.",
        st["li"],
    ))
    story.append(Paragraph(
        "No es necesario republicar el archivo .pbix si las fuentes ya apuntan a SharePoint.",
        st["p"],
    ))

    story.append(Paragraph("6. Listas MetaProyecto y Acciones", st["h1"]))
    story.append(tabla(
        [
            ["Lista", "Para qué", "Cuándo se cambia"],
            ["MetaProyecto", "Meta de depuración, fechas, proyección", "Cuando se define o ajusta la meta del periodo"],
            ["Acciones", "Bitácora de lo ejecutado", "Cuando hay bloqueos, comunicados o cierre de lote"],
        ],
        st,
        [4 * cm, 6.5 * cm, 5.7 * cm],
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Menú izquierdo → nombre de la lista → Editar o + Nuevo. Si cambia la meta y el tablero no se mueve, "
        "no regenere CSV: edite la lista y refresque Power BI.",
        st["p"],
    ))

    story.append(Paragraph("7. Flujo resumido", st["h1"]))
    story.append(Paragraph(
        "Carpeta del corte (Google Admin + inscritos) → doble clic en actualizar.bat → "
        "carpeta del escritorio con seis archivos → arrastrar a etl/output → tablero (cada hora) "
        "y botón Resumen 2FA. Las listas se editan en el sitio y entran en el mismo refresco.",
        st["p"],
    ))

    story.append(Paragraph("8. Incidencias frecuentes", st["h1"]))
    story.append(tabla(
        [
            ["Qué ocurre", "Qué hacer"],
            ["No se encontró Python", "Instalar Python desde python.org y marcar Add Python to PATH."],
            ["No hallé export Google", "Debe estar User_Download… en la carpeta cuya ruta pegó."],
            ["No hallé CSV de inscritos", "Faltan los archivos académicos en esa misma carpeta."],
            ["El tablero no cambia", "Confirme los tres *_powerbi.csv reemplazados. Actualizar ahora."],
            ["La meta no cambia", "Edite MetaProyecto, no un CSV."],
            ["404 al descargar pendientes", "Suba 02_estudiantes_sin_2fa.csv junto al HTML."],
            ["No aparece la carpeta en el escritorio", "Busque Escritorio o Desktop. El actualizador la abre."],
            ["No tiene acceso al sitio", "Solicitar lectura o edición (apartado 3)."],
            ["El HTML 2FA se ve incompleto", "Abrir en pestaña nueva, no solo en la vista previa de SharePoint."],
        ],
        st,
        [5.8 * cm, 10.4 * cm],
    ))

    story.append(Paragraph("9. Protección de datos", st["h1"]))
    story.append(Paragraph(
        "Los CSV de origen y el universo de cuentas contienen información sensible. Trabaje en el equipo "
        "del área. No publique etl/input ni 00_universo.csv en el portal de consulta. No envíe listados "
        "de correos por canales no institucionales.",
        st["p"],
    ))

    story.append(Paragraph("10. Soporte", st["h1"]))
    story.append(Paragraph(
        "Estadísticas TIC — Dirección de TIC<br/>Universidad Autónoma de Bucaramanga",
        st["p"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=LETTER,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.4 * cm,
        title="Manual de operación — Portal cuentas Gmail UNAB",
        author="Estadísticas TIC — Dirección de TIC",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    construir()
