#!/usr/bin/env python3
"""Genera la guía de preparación práctica Java para la prueba UNAB."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUTPUT = REPO / "entregables" / "Guia_Practica_Java_UNAB_Ivan_Cardona.pdf"
FONTS = REPO / "cv_assets" / "fonts"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#276FBF")
GOLD = colors.HexColor("#F4C95D")
TEAL = colors.HexColor("#2A9D8F")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#526273")
LIGHT = colors.HexColor("#F5F7FA")
BORDER = colors.HexColor("#D9E1E8")
WHITE = colors.white

pdfmetrics.registerFont(TTFont("Raleway", str(FONTS / "Raleway-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Raleway-Bold", str(FONTS / "Raleway-Bold.ttf")))


def style(name, size=9.5, leading=None, font="Raleway", color=INK, align=0, after=6):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.32,
        textColor=color,
        alignment=align,
        spaceAfter=after,
    )


S = {
    "title": style("title", 28, 34, "Raleway-Bold", NAVY),
    "subtitle": style("subtitle", 13, 18, "Raleway-Bold", BLUE),
    "h1": style("h1", 19, 24, "Raleway-Bold", NAVY, after=9),
    "h2": style("h2", 13, 17, "Raleway-Bold", BLUE, after=6),
    "body": style("body", 9.5, 13.4, "Raleway", INK, TA_JUSTIFY, 7),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Raleway",
        fontSize=9.2,
        leading=12.8,
        textColor=INK,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=4,
    ),
    "small": style("small", 7.5, 10, "Raleway", MUTED),
    "table": style("table", 8, 10.5, "Raleway", INK),
    "table_head": style("table_head", 8, 10.5, "Raleway-Bold", WHITE),
    "code": ParagraphStyle(
        "code",
        fontName="Courier",
        fontSize=7.7,
        leading=10.2,
        textColor=INK,
        leftIndent=8,
        rightIndent=8,
        backColor=colors.HexColor("#EEF2F5"),
        borderColor=BORDER,
        borderWidth=0.5,
        borderPadding=8,
        spaceBefore=4,
        spaceAfter=9,
    ),
}


def bullet(text):
    return Paragraph(f"• {text}", S["bullet"])


def code(text):
    return Preformatted(text.strip(), S["code"])


def callout(text, color=colors.HexColor("#EAF3FB"), border=BLUE):
    table = Table([[Paragraph(text, S["body"])]], colWidths=[520])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.8, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def table(rows, widths):
    data = []
    for index, row in enumerate(rows):
        current = S["table_head"] if index == 0 else S["table"]
        data.append([
            Paragraph(f"<b>{cell}</b>" if index == 0 else cell, current)
            for cell in row
        ])
    result = Table(data, colWidths=widths, repeatRows=1)
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.55, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return result


def page_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 766, 612, 26, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 766, 9, 26, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Raleway-Bold", 7.5)
    canvas.drawString(34, 775, "PRÁCTICA JAVA · ORACLE · POSTGRESQL · TOMCAT")
    canvas.setStrokeColor(BORDER)
    canvas.line(34, 28, 578, 28)
    canvas.setFillColor(MUTED)
    canvas.setFont("Raleway", 7.2)
    canvas.drawString(34, 17, "Preparación presencial sin IA · Iván David Cardona Mendoza")
    canvas.drawRightString(578, 17, str(canvas.getPageNumber()))
    canvas.restoreState()


def start_page(story, number, title):
    story.append(Paragraph(f"{number}. {title}", S["h1"]))


def end_page(story):
    story.append(PageBreak())


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=43,
        bottomMargin=40,
        title="Guía práctica Java UNAB - Ivan David Cardona",
        author="Ivan David Cardona Mendoza",
    )
    story = []

    story += [
        Spacer(1, 65),
        Paragraph("PRUEBA PRÁCTICA UNAB", S["subtitle"]),
        Spacer(1, 8),
        Paragraph("JAVA DESDE CERO<br/>HASTA TOMCAT Y JDBC", S["title"]),
        Spacer(1, 14),
        Paragraph("Java · POO · SQL · PostgreSQL · Oracle · JDBC · JSP/Servlet · Tomcat", S["subtitle"]),
        Spacer(1, 35),
        callout(
            "<b>Propósito:</b> desarrollar una base suficiente para resolver una prueba presencial sin depender "
            "de IA. La prioridad es escribir código pequeño que compile, proteger datos, explicar decisiones y "
            "diagnosticar errores.",
            colors.HexColor("#FFF8E5"),
            GOLD,
        ),
        Spacer(1, 35),
        Paragraph("Material incluido", S["h2"]),
        bullet("Fundamentos explicados paso a paso."),
        bullet("Laboratorios con archivos iniciales y soluciones separadas."),
        bullet("Proyecto JDBC real contra PostgreSQL."),
        bullet("Aplicación WAR con JSP/Servlet para Tomcat."),
        bullet("Tres simulacros progresivos y rúbricas."),
        Spacer(1, 45),
        Paragraph("IVÁN DAVID CARDONA MENDOZA", S["h1"]),
        Paragraph("Ingeniero de Sistemas · Especialista en Seguridad Informática", S["body"]),
        PageBreak(),
    ]

    start_page(story, 1, "Qué puede evaluar la prueba")
    story.append(Paragraph(
        "Por la vacante y el stack mencionado por la directora, la prueba probablemente combinará lectura de "
        "requerimientos, Java, SQL, mantenimiento de una aplicación existente y explicación de controles. No "
        "asumas que pedirán construir un sistema completo.",
        S["body"],
    ))
    story.append(table([
        ["Bloque", "Qué podrían pedir", "Qué demostrar"],
        ["Java", "Clase, método, colección, validación o corrección de error.", "Sintaxis, POO, claridad y casos límite."],
        ["SQL", "Consulta, join, agrupación, actualización o modelo.", "Integridad, filtros correctos y seguridad."],
        ["JDBC", "CRUD o transacción.", "PreparedStatement, recursos, commit y rollback."],
        ["Web", "Servlet/JSP, endpoint o mantenimiento.", "HTTP, capas, validación y PRG."],
        ["Tomcat", "WAR, ruta que falla o log.", "Despliegue y diagnóstico."],
        ["Seguridad", "Entrada maliciosa, perfiles o auditoría.", "Mínimo privilegio, trazabilidad y manejo de errores."],
    ], [75, 230, 215]))
    story.append(Spacer(1, 12))
    story.append(callout(
        "<b>Estrategia:</b> primero identifica entrada, salida, reglas y errores. Después crea la estructura mínima, "
        "compila y agrega comportamiento por partes. No escribas cien líneas sin compilar.",
    ))
    end_page(story)

    start_page(story, 2, "Cómo funciona Java")
    story.append(Paragraph(
        "El archivo `.java` contiene código fuente. `javac` lo convierte en bytecode `.class`, y la JVM ejecuta "
        "ese bytecode. Java verifica tipos antes de ejecutar; por eso muchos errores aparecen al compilar.",
        S["body"],
    ))
    story.append(code("""
// Archivo Hola.java
public class Hola {
    public static void main(String[] args) {
        System.out.println("Hola UNAB");
    }
}
    """))
    story.append(code("""
javac Hola.java
java Hola
    """))
    story.append(Paragraph("Reglas que debes recordar", S["h2"]))
    for text in [
        "El nombre del archivo coincide con la clase pública.",
        "Cada sentencia termina normalmente con punto y coma.",
        "Java diferencia mayúsculas y minúsculas.",
        "`String` es un objeto; se compara con `equals()`.",
        "`null` significa ausencia de referencia y debe validarse.",
        "Un mensaje de compilación indica archivo, línea y tipo de problema.",
    ]:
        story.append(bullet(text))
    story.append(callout(
        "<b>Lectura de error:</b> empieza por el primer error. Los siguientes pueden ser consecuencias. Corrige uno, recompila y vuelve a leer.",
        colors.HexColor("#EAF7F4"),
        TEAL,
    ))
    end_page(story)

    start_page(story, 3, "Variables, condiciones y ciclos")
    story.append(code("""
int cantidad = 30;
double valor = 12500.50;
boolean activo = true;
String nombre = "Iván";

if (activo && cantidad > 0) {
    System.out.println(nombre + ": " + cantidad);
}

for (int i = 0; i < cantidad; i++) {
    System.out.println(i);
}
    """))
    story.append(table([
        ["Tipo", "Ejemplo", "Uso"],
        ["int / long", "int total = 3;", "Enteros; long para ids grandes."],
        ["double", "double valor = 2.5;", "Decimales generales. Dinero real suele usar BigDecimal."],
        ["boolean", "boolean activo = true;", "Condición verdadera o falsa."],
        ["char", "char letra = 'A';", "Un carácter."],
        ["String", "String texto = \"hola\";", "Cadena de caracteres."],
    ], [95, 170, 255]))
    story.append(Paragraph("Errores frecuentes", S["h2"]))
    story.append(code("""
// Incorrecto
if (estado == "ABIERTO") { }

// Correcto y seguro ante null constante
if ("ABIERTO".equals(estado)) { }
    """))
    story.append(bullet("Usar `=` para asignar y `==` para comparar primitivos."))
    story.append(bullet("Olvidar que un índice de lista comienza en cero."))
    story.append(bullet("Crear un ciclo que nunca modifica su condición."))
    end_page(story)

    start_page(story, 4, "Métodos y validación")
    story.append(Paragraph(
        "Un método recibe parámetros, ejecuta una responsabilidad y puede devolver un resultado. Los nombres deben "
        "expresar una acción. Valida condiciones inválidas al inicio para evitar lógica anidada.",
        S["body"],
    ))
    story.append(code("""
public static double calcularPago(double horas, double valorHora) {
    if (horas < 0 || valorHora < 0) {
        throw new IllegalArgumentException("Valores negativos");
    }

    double normales = Math.min(horas, 8);
    double extras = Math.max(horas - 8, 0);
    return normales * valorHora
            + extras * valorHora * 1.25;
}
    """))
    story.append(Paragraph("Preguntas antes de programar", S["h2"]))
    for text in [
        "¿Qué recibe el método?",
        "¿Qué devuelve?",
        "¿Qué valores son inválidos?",
        "¿Qué ocurre en cero, mínimo y máximo?",
        "¿Puede retornar ausencia? Considera `Optional`.",
        "¿La responsabilidad cabe en una frase?",
    ]:
        story.append(bullet(text))
    story.append(callout(
        "En una prueba, primero escribe la firma y tres ejemplos de entrada/salida. Eso reduce cambios improvisados.",
    ))
    end_page(story)

    start_page(story, 5, "Programación orientada a objetos")
    story.append(Paragraph(
        "Una clase agrupa estado y comportamiento. La encapsulación protege invariantes: el objeto no debería poder "
        "quedar en un estado inválido por una modificación externa.",
        S["body"],
    ))
    story.append(code("""
public final class Incidente {
    private final long id;
    private final String titulo;
    private Estado estado;

    public Incidente(long id, String titulo) {
        if (id <= 0) throw new IllegalArgumentException("Id");
        if (titulo == null || titulo.isBlank()) {
            throw new IllegalArgumentException("Título");
        }
        this.id = id;
        this.titulo = titulo.trim();
        this.estado = Estado.ABIERTO;
    }

    public Estado getEstado() {
        return estado;
    }
}
    """))
    story.append(table([
        ["Concepto", "Significado práctico"],
        ["Encapsulación", "Atributos privados y cambios controlados por métodos."],
        ["Abstracción", "Exponer lo necesario y ocultar detalles."],
        ["Herencia", "Una clase especializa otra; úsala solo si existe relación real “es un”."],
        ["Polimorfismo", "Trabajar contra interfaz y cambiar implementación."],
        ["Composición", "Un objeto contiene otros; suele ser más flexible que herencia."],
    ], [120, 400]))
    end_page(story)

    start_page(story, 6, "Interfaces, enums y records")
    story.append(code("""
public interface IncidenteDao {
    Optional<Incidente> buscarPorId(long id);
    List<Incidente> listar();
}

public enum Estado {
    ABIERTO, EN_PROGRESO, CERRADO
}

public record CrearIncidente(
        String titulo,
        String descripcion,
        Prioridad prioridad) {
}
    """))
    story.append(Paragraph(
        "La interfaz define un contrato sin acoplar al consumidor a JDBC o memoria. El enum limita valores válidos. "
        "El record es útil para datos inmutables y genera constructor, accesores, `equals`, `hashCode` y `toString`.",
        S["body"],
    ))
    story.append(Paragraph("Cuándo no usar record", S["h2"]))
    story.append(bullet("Cuando el objeto tiene identidad y estado mutable complejo."))
    story.append(bullet("Cuando necesitas ocultar o transformar accesores."))
    story.append(bullet("Cuando representa una entidad JPA con requisitos específicos."))
    story.append(callout(
        "<b>Respuesta de entrevista:</b> “Uso interfaces en límites que pueden cambiar, enums para estados cerrados "
        "y records para comandos o respuestas inmutables.”",
    ))
    end_page(story)

    start_page(story, 7, "Colecciones y Optional")
    story.append(table([
        ["Tipo", "Propiedad", "Ejemplo de uso"],
        ["List", "Ordenada, admite repetidos.", "Incidentes de una consulta."],
        ["Set", "No admite duplicados.", "Permisos o códigos únicos."],
        ["Map", "Clave asociada a valor.", "Conteo por prioridad."],
        ["Optional", "Resultado que puede no existir.", "Buscar por id."],
    ], [90, 180, 250]))
    story.append(code("""
List<Incidente> abiertos = incidentes.stream()
        .filter(i -> i.getEstado() == Estado.ABIERTO)
        .toList();

Map<Prioridad, Long> conteo = incidentes.stream()
        .collect(Collectors.groupingBy(
                Incidente::getPrioridad,
                Collectors.counting()));

Incidente incidente = buscarPorId(id)
        .orElseThrow(() -> new NoEncontradoException(id));
    """))
    story.append(Paragraph("Reglas", S["h2"]))
    story.append(bullet("No expongas una lista interna mutable; devuelve copia."))
    story.append(bullet("Usa `Set` cuando la unicidad sea parte del problema."))
    story.append(bullet("No uses `Optional` como sustituto universal de validación."))
    story.append(bullet("Puedes resolver con bucles si aún no dominas Streams; claridad primero."))
    end_page(story)

    start_page(story, 8, "Excepciones y diagnóstico")
    story.append(code("""
try {
    service.crear(comando);
} catch (IllegalArgumentException e) {
    System.out.println("Dato inválido: " + e.getMessage());
} catch (SQLException e) {
    System.err.println("Error de persistencia");
    throw e;
}
    """))
    story.append(Paragraph(
        "Las excepciones de validación representan errores esperables del usuario. `SQLException` representa un "
        "problema técnico que debe registrarse con contexto y causa, sin mostrar SQL ni credenciales al usuario.",
        S["body"],
    ))
    story.append(Paragraph("Cómo leer una traza", S["h2"]))
    for text in [
        "Identifica tipo y mensaje.",
        "Busca el primer `Caused by` relevante.",
        "Encuentra la primera línea de tu código.",
        "Revisa datos de entrada y cambio reciente.",
        "Corrige la causa, no ocultes el síntoma.",
    ]:
        story.append(bullet(text))
    story.append(callout(
        "Nunca uses `catch (Exception e) { }`. Silenciar un error hace que la aplicación continúe en un estado desconocido.",
        colors.HexColor("#FCEEEE"),
        colors.HexColor("#B44646"),
    ))
    end_page(story)

    start_page(story, 9, "Modelo relacional y restricciones")
    story.append(code("""
CREATE TABLE incidente (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    solicitante_id BIGINT NOT NULL,
    CONSTRAINT fk_solicitante
        FOREIGN KEY (solicitante_id) REFERENCES usuario_tic(id),
    CONSTRAINT ck_estado
        CHECK (estado IN ('ABIERTO','EN_PROGRESO','CERRADO'))
);
    """))
    story.append(table([
        ["Restricción", "Protege"],
        ["PRIMARY KEY", "Identidad única y no nula."],
        ["FOREIGN KEY", "Relaciones con registros existentes."],
        ["NOT NULL", "Campos obligatorios."],
        ["UNIQUE", "Valores sin duplicar."],
        ["CHECK", "Dominio o regla simple."],
    ], [130, 390]))
    story.append(Paragraph(
        "Las validaciones de Java mejoran la experiencia, pero la base es la última barrera de integridad. Ambas capas "
        "deben proteger las reglas críticas.",
        S["body"],
    ))
    end_page(story)

    start_page(story, 10, "SELECT, JOIN y agregación")
    story.append(code("""
SELECT i.id, i.titulo, u.nombre AS solicitante
FROM incidente i
JOIN usuario_tic u ON u.id = i.solicitante_id
WHERE i.estado = 'ABIERTO'
ORDER BY i.fecha_creacion DESC;

SELECT u.nombre, COUNT(i.id) AS total
FROM usuario_tic u
LEFT JOIN incidente i ON i.tecnico_id = u.id
WHERE u.rol = 'TECNICO'
GROUP BY u.id, u.nombre;
    """))
    story.append(table([
        ["Elemento", "Uso"],
        ["WHERE", "Filtrar filas antes de agrupar."],
        ["GROUP BY", "Formar grupos para COUNT, SUM, AVG."],
        ["HAVING", "Filtrar grupos después de agrupar."],
        ["INNER JOIN", "Solo coincidencias."],
        ["LEFT JOIN", "Todas las filas izquierdas, exista o no coincidencia."],
        ["NOT EXISTS", "Comprobar ausencia de relación."],
    ], [115, 405]))
    story.append(bullet("Usa alias claros y califica columnas ambiguas."))
    story.append(bullet("Filtra el estado en la condición correcta antes de contar."))
    end_page(story)

    start_page(story, 11, "Transacciones, índices y concurrencia")
    story.append(code("""
BEGIN;

SELECT * FROM equipo WHERE id = 10 FOR UPDATE;
INSERT INTO prestamo (...);
UPDATE equipo SET disponible = FALSE WHERE id = 10;

COMMIT;
-- Ante error: ROLLBACK;
    """))
    story.append(Paragraph(
        "Una transacción agrupa cambios que deben ocurrir todos o ninguno. `FOR UPDATE` bloquea la fila para evitar que "
        "dos operaciones presten el mismo equipo simultáneamente.",
        S["body"],
    ))
    story.append(Paragraph("Control optimista", S["h2"]))
    story.append(code("""
UPDATE incidente
SET estado = ?, version = version + 1
WHERE id = ? AND version = ?;
    """))
    story.append(bullet("Si actualiza una fila: éxito."))
    story.append(bullet("Si actualiza cero: otro usuario cambió el registro o ya no existe."))
    story.append(Paragraph("Índices", S["h2"]))
    story.append(bullet("Aceleran filtros, joins y ordenamientos usados con frecuencia."))
    story.append(bullet("Consumen espacio y agregan costo a INSERT/UPDATE/DELETE."))
    story.append(bullet("Se definen a partir de consultas reales y se validan con plan de ejecución."))
    end_page(story)

    start_page(story, 12, "PostgreSQL y Oracle")
    story.append(table([
        ["Tema", "PostgreSQL", "Oracle"],
        ["Entero grande", "BIGINT", "NUMBER(19)"],
        ["Cadena", "VARCHAR", "VARCHAR2"],
        ["Booleano tabla", "BOOLEAN", "NUMBER(1) o CHAR(1)"],
        ["Texto largo", "TEXT", "CLOB"],
        ["Id", "IDENTITY", "IDENTITY o SEQUENCE"],
        ["Procedimientos", "PL/pgSQL", "PL/SQL"],
        ["URL JDBC", "jdbc:postgresql://...", "jdbc:oracle:thin:@//..."],
    ], [115, 200, 205]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Particularidades que suelen preguntar", S["h2"]))
    story.append(bullet("Oracle trata cadena vacía como `NULL`; PostgreSQL las diferencia."))
    story.append(bullet("PostgreSQL ofrece `ILIKE`; para portabilidad usa `LOWER(campo) LIKE LOWER(?)`."))
    story.append(bullet("Oracle tradicional usa secuencias; versiones modernas admiten identity."))
    story.append(bullet("Ambos soportan transacciones, joins, restricciones y `FETCH FIRST`."))
    story.append(callout(
        "No afirmes dominar Oracle. Explica que tus fundamentos SQL son transferibles y nombra las diferencias que "
        "revisarías antes de modificar producción.",
        colors.HexColor("#FFF8E5"),
        GOLD,
    ))
    end_page(story)

    start_page(story, 13, "JDBC paso a paso")
    story.append(code("""
String sql = "SELECT id, titulo FROM incidente WHERE id = ?";

try (Connection cn = factory.abrir();
     PreparedStatement ps = cn.prepareStatement(sql)) {

    ps.setLong(1, id);

    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) {
            return new Incidente(
                    rs.getLong("id"),
                    rs.getString("titulo"));
        }
        return null;
    }
}
    """))
    story.append(Paragraph("Responsabilidad de cada objeto", S["h2"]))
    story.append(bullet("`Connection`: sesión con la base y límite transaccional."))
    story.append(bullet("`PreparedStatement`: SQL precompilado y parámetros separados del texto."))
    story.append(bullet("`ResultSet`: cursor de resultados; `next()` avanza fila."))
    story.append(bullet("`try-with-resources`: cierra incluso si ocurre excepción."))
    story.append(Paragraph("Por qué evita inyección", S["h2"]))
    story.append(Paragraph(
        "El texto del usuario se envía como dato. No puede cerrar comillas y transformar la estructura SQL. "
        "Nunca reemplaces parámetros concatenando cadenas.",
        S["body"],
    ))
    end_page(story)

    start_page(story, 14, "Transacciones JDBC")
    story.append(code("""
try (Connection cn = factory.abrir()) {
    boolean original = cn.getAutoCommit();
    try {
        cn.setAutoCommit(false);

        // DAO 1 usando cn
        // DAO 2 usando la misma cn

        cn.commit();
    } catch (Exception error) {
        try {
            cn.rollback();
        } catch (SQLException rollbackError) {
            error.addSuppressed(rollbackError);
        }
        throw error;
    } finally {
        cn.setAutoCommit(original);
    }
}
    """))
    story.append(Paragraph("Errores críticos", S["h2"]))
    for text in [
        "Cada DAO abre una conexión diferente.",
        "Se hace commit después de capturar un error.",
        "Se olvida rollback.",
        "Se devuelve la conexión al pool con autoCommit alterado.",
        "Se cierra una conexión cuya propiedad corresponde al servicio.",
        "No se comprueba el número de filas afectadas.",
    ]:
        story.append(bullet(text))
    story.append(callout(
        "La transacción pertenece al caso de uso, no a una sentencia aislada. Por eso normalmente la coordina el servicio.",
    ))
    end_page(story)

    start_page(story, 15, "Maven y estructura de proyecto")
    story.append(code("""
proyecto/
  pom.xml
  src/main/java/
  src/main/resources/
  src/main/webapp/
  src/test/java/
    """))
    story.append(code("""
mvn clean        # elimina target
mvn compile      # compila main
mvn test         # compila y ejecuta pruebas
mvn package      # genera JAR o WAR
    """))
    story.append(Paragraph("Partes del pom", S["h2"]))
    story.append(bullet("`groupId`: organización o espacio de nombres."))
    story.append(bullet("`artifactId`: nombre del proyecto."))
    story.append(bullet("`version`: versión del artefacto."))
    story.append(bullet("`packaging`: jar o war."))
    story.append(bullet("`dependencies`: librerías y alcance."))
    story.append(bullet("Servlet API usa `provided` porque Tomcat la entrega."))
    story.append(callout(
        "Si Maven falla, lee si el problema es compilación, prueba, descarga o plugin. No borres código al azar.",
        colors.HexColor("#EAF7F4"),
        TEAL,
    ))
    end_page(story)

    start_page(story, 16, "HTTP, Servlet y JSP")
    story.append(table([
        ["Método", "Uso habitual"],
        ["GET", "Consultar; no debe modificar estado."],
        ["POST", "Crear o ejecutar acción."],
        ["PUT/PATCH", "Actualizar en API REST."],
        ["DELETE", "Eliminar en API REST."],
    ], [100, 420]))
    story.append(code("""
@WebServlet("/incidencias")
public class IncidenciaServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req,
                         HttpServletResponse resp)
            throws ServletException, IOException {
        req.setAttribute("incidencias", service.listar());
        req.getRequestDispatcher(
                "/WEB-INF/views/incidencias.jsp"
        ).forward(req, resp);
    }
}
    """))
    story.append(Paragraph("Separación", S["h2"]))
    story.append(bullet("Servlet: HTTP, parámetros, status, forward/redirect."))
    story.append(bullet("Service: reglas, permisos y transacciones."))
    story.append(bullet("DAO: SQL y mapeo."))
    story.append(bullet("JSP: presentación escapada; sin SQL ni lógica de negocio."))
    end_page(story)

    start_page(story, 17, "Tomcat y WAR")
    story.append(Paragraph(
        "Tomcat es un contenedor web. Carga el WAR, crea un contexto y administra Servlets, filtros, sesiones y JSP.",
        S["body"],
    ))
    story.append(code("""
mvn clean test package
cp target/incidentes.war $CATALINA_HOME/webapps/
$CATALINA_HOME/bin/startup.sh
tail -f $CATALINA_HOME/logs/catalina.out
    """))
    story.append(table([
        ["Síntoma", "Revisión"],
        ["404", "Context path, mapping, despliegue y log de arranque."],
        ["500", "Primera excepción, Caused by, parámetros y JDBC."],
        ["ClassNotFound Servlet", "Tomcat 9 javax vs Tomcat 10/11 jakarta."],
        ["Acentos dañados", "UTF-8 antes de leer parámetros, JSP y base."],
        ["Conexiones agotadas", "Cierre de recursos, pool y transacciones."],
    ], [145, 375]))
    story.append(callout(
        "<b>Compatibilidad:</b> Tomcat 9 usa `javax.servlet`; Tomcat 10 y 11 usan `jakarta.servlet`. No se mezclan.",
        colors.HexColor("#FFF8E5"),
        GOLD,
    ))
    end_page(story)

    start_page(story, 18, "Arquitectura de tres capas")
    story.append(code("""
Navegador / JSP
       |
       v
Servlet / Controller
       |
       v
Service / Reglas / Transacción
       |
       v
DAO / JDBC / SQL
       |
       v
Oracle o PostgreSQL
    """))
    story.append(Paragraph(
        "La arquitectura separa motivos de cambio. Una regla de transición no pertenece al Servlet ni al DAO. Una "
        "consulta SQL no pertenece a la JSP. Esta separación facilita pruebas y mantenimiento.",
        S["body"],
    ))
    story.append(Paragraph("Cómo explicarla en la prueba", S["h2"]))
    story.append(callout(
        "“El controlador traduce HTTP, el servicio aplica reglas y coordina la transacción, y el DAO encapsula "
        "persistencia. Así puedo probar reglas sin Tomcat y cambiar detalles de base sin reescribir la interfaz.”",
    ))
    story.append(Spacer(1, 12))
    story.append(bullet("Modelo/DTO: datos que cruzan capas."))
    story.append(bullet("Filtro: preocupaciones transversales como UTF-8, sesión o seguridad."))
    story.append(bullet("Configuración: fuera del código y separada por ambiente."))
    end_page(story)

    start_page(story, 19, "Seguridad mínima")
    story.append(table([
        ["Riesgo", "Control"],
        ["Inyección SQL", "PreparedStatement y permisos mínimos."],
        ["XSS", "Escapar al mostrar con c:out; CSP como defensa adicional."],
        ["CSRF", "Token de sesión en operaciones POST."],
        ["Acceso indebido", "Autenticación, roles y autorización por acción."],
        ["Secreto expuesto", "Variables de entorno o gestor de secretos; no Git."],
        ["Cambio sin evidencia", "Usuario, fecha, acción, resultado y correlación."],
        ["Pérdida de datos", "Respaldo verificado y plan de reversión."],
    ], [145, 375]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Los logs no deben contener", S["h2"]))
    story.append(bullet("Contraseñas."))
    story.append(bullet("Tokens completos."))
    story.append(bullet("Cadenas de conexión con credenciales."))
    story.append(bullet("Datos personales innecesarios."))
    story.append(callout(
        "Tu plus como especialista no es agregar controles sin contexto. Es identificar riesgo, elegir un control "
        "proporcional y comprobar que no rompe el proceso.",
        colors.HexColor("#EAF7F4"),
        TEAL,
    ))
    end_page(story)

    start_page(story, 20, "Pruebas")
    story.append(table([
        ["Tipo", "Qué valida", "Ejemplo"],
        ["Unitaria", "Regla aislada.", "Transición de estado."],
        ["Integración", "Componentes reales.", "DAO contra base de prueba."],
        ["Funcional", "Requerimiento.", "Crear incidencia desde formulario."],
        ["Regresión", "Que lo anterior siga funcionando.", "Suite antes de liberar."],
        ["Aceptación", "Necesidad del usuario.", "Validación con responsable."],
    ], [95, 195, 230]))
    story.append(code("""
@Test
void noPermiteCerrarDirectamente() {
    Incidente incidente = nuevoAbierto();

    assertThrows(
        IllegalStateException.class,
        () -> incidente.cambiarEstado(Estado.CERRADO)
    );
}
    """))
    story.append(Paragraph("Casos mínimos", S["h2"]))
    story.append(bullet("Camino correcto."))
    story.append(bullet("Campo vacío o nulo."))
    story.append(bullet("Longitud mínima y máxima."))
    story.append(bullet("Estado inválido."))
    story.append(bullet("Registro inexistente."))
    story.append(bullet("Entrada maliciosa."))
    end_page(story)

    start_page(story, 21, "Plan de práctica por sesiones")
    story.append(table([
        ["Sesión", "Trabajo", "Resultado"],
        ["1", "Guía 2–7 + laboratorio fundamentos.", "Clases, métodos y colecciones sin copiar."],
        ["2", "Guía 9–12 + 15 consultas SQL.", "DDL, joins, grupos y transacción."],
        ["3", "Guía 13–14 + proyecto JDBC.", "CRUD y cambio de estado transaccional."],
        ["4", "Guía 15–18 + WAR Tomcat.", "Servlet, JSP, capas y despliegue."],
        ["5", "Guía 19–20 + simulacro 1.", "Validación, seguridad y prueba cronometrada."],
        ["6", "Simulacro 2.", "JDBC sin ayuda."],
        ["7", "Simulacro 3 o versión reducida.", "Aplicación web explicable."],
    ], [60, 285, 175]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("En cada sesión", S["h2"]))
    story.append(bullet("20 minutos de lectura."))
    story.append(bullet("60–120 minutos de código sin solución."))
    story.append(bullet("15 minutos explicando en voz alta."))
    story.append(bullet("Comparar con solución y registrar tres errores."))
    story.append(callout(
        "No avances porque “entendiste al leer”. Avanza cuando puedas escribir y explicar sin mirar.",
    ))
    end_page(story)

    start_page(story, 22, "Hoja de memoria para la prueba")
    story.append(Paragraph("JAVA", S["h2"]))
    story.append(code("""
if (x == null) { ... }
"texto".equals(valor)
List<T> lista = new ArrayList<>();
Map<K,V> mapa = new HashMap<>();
Optional<T> resultado
try-with-resources
    """))
    story.append(Paragraph("SQL", S["h2"]))
    story.append(code("""
SELECT ... FROM ... JOIN ... ON ...
WHERE ... GROUP BY ... HAVING ... ORDER BY ...
INSERT INTO ... VALUES ...
UPDATE ... SET ... WHERE ...
BEGIN; COMMIT; ROLLBACK;
    """))
    story.append(Paragraph("JDBC", S["h2"]))
    story.append(code("""
Connection
PreparedStatement
setString / setLong
executeQuery / executeUpdate
ResultSet.next()
commit / rollback
    """))
    story.append(Paragraph("WEB", S["h2"]))
    story.append(code("""
GET consulta
POST modifica
Servlet -> Service -> DAO
forward si validación falla
redirect después de POST correcto
WAR -> Tomcat webapps
    """))
    story.append(callout(
        "<b>Última regla:</b> compila primero una versión pequeña. Después agrega validación, persistencia y seguridad. "
        "Deja comentarios claros para lo que no alcances.",
        colors.HexColor("#FFF8E5"),
        GOLD,
    ))
    end_page(story)

    start_page(story, 23, "Checklist de entrega")
    checks = [
        "[ ] El proyecto compila.",
        "[ ] Ejecuté al menos un caso válido.",
        "[ ] Probé un caso inválido.",
        "[ ] No comparé String con ==.",
        "[ ] Los atributos están encapsulados.",
        "[ ] No concatené entradas en SQL.",
        "[ ] Cerré Connection, Statement y ResultSet.",
        "[ ] La transacción tiene commit y rollback.",
        "[ ] Validé en servidor.",
        "[ ] No expuse credenciales ni trazas.",
        "[ ] Separé web, servicio y persistencia.",
        "[ ] Documenté cómo ejecutar.",
        "[ ] Puedo explicar una decisión y un riesgo.",
    ]
    for item in checks:
        story.append(bullet(item))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Cómo presentar lo incompleto", S["h2"]))
    story.append(callout(
        "“Implementé el flujo principal y dejé compilando la solución. Por tiempo no terminé el control CSRF. "
        "Antes de producción lo agregaría como filtro con token de sesión y una prueba de POST sin token. También "
        "validaría el despliegue en la versión exacta de Tomcat.”",
    ))
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Reconocer una brecha con un plan técnico preciso demuestra más criterio que ocultarla con código improvisado.",
        S["body"],
    ))

    doc.build(story, onFirstPage=page_header, onLaterPages=page_header)
    print(f"Guía generada: {OUTPUT}")


if __name__ == "__main__":
    build()
