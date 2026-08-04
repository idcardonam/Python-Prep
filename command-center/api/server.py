"""
API local OPCIONAL — esqueleto.
No llama a ningún proveedor hasta que configures la key y completes el cliente.
Por defecto devuelve un JSON de ejemplo para probar el import en app.html.
"""
from __future__ import annotations

import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return {"ok": True, "mode": "skeleton"}


@app.post("/analizar")
def analizar():
    """
    Body JSON: { "project": str, "texto": str, "controversias": str, "adjuntos": [] }
    Respuesta: formato importable por app.html
    """
    data = request.get_json(force=True, silent=True) or {}
    project = data.get("project") or "Proyecto"
    texto = (data.get("texto") or "")[:4000]

    # Si más adelante conectas Anthropic/OpenAI, reemplaza este bloque demo.
    # Mantener el mismo schema.
    demo = {
        "project": project,
        "estimacion": "1–2 días si responden P0 (L + M)",
        "phase": "aclaracion",
        "sem": "y",
        "preguntas": [
            {
                "prioridad": "P0",
                "texto": "¿Qué tablas o vistas existentes debemos usar y cuáles no se pueden tocar?",
                "respuesta": "",
            },
            {
                "prioridad": "P0",
                "texto": "¿Quién autoriza el acceso (roles) y dónde se valida en servidor?",
                "respuesta": "",
            },
            {
                "prioridad": "P1",
                "texto": "¿Cuál es el criterio de listo de la primera demo?",
                "respuesta": "",
            },
        ],
        "riesgos": [
            {
                "titulo": "Romper módulo existente",
                "detalle": "Cambios sin mapa de dependencias",
                "mitigacion": "Solo lectura primero; cambios mínimos; prueba humo",
            },
            {
                "titulo": "Exposición de datos sensibles",
                "detalle": "Listados sin control de acceso real",
                "mitigacion": "Validar autorización en servidor; no confiar solo en UI",
            },
        ],
        "millas": [
            {
                "titulo": "Bitácora de acceso al listado sensible",
                "beneficio": "Trazabilidad de quién consulta datos de riesgo",
                "riesgo": "Ruido/volumen de logs",
                "mitigacion": "Loggear usuario+timestamp+filtro, no el dataset completo",
                "ok": False,
            },
            {
                "titulo": "Enmascarado parcial de identificadores en UI",
                "beneficio": "Menos exposición accidental en reuniones/demos",
                "riesgo": "Puede molestar operativamente",
                "mitigacion": "Rol TIC ve completo; otros ven enmascarado",
                "ok": False,
            },
        ],
        "pasos": [
            {
                "title": "Mapear tablas/endpoints existentes",
                "detail": "Documentar en PROJECT.md qué se reutiliza",
                "done": False,
            },
            {
                "title": "Definir criterios de aceptación de la demo",
                "detail": "3–5 bullets medibles",
                "done": False,
            },
            {
                "title": "Implementar lectura/listado sin mutar cálculo",
                "detail": "PR pequeño + prueba manual",
                "done": False,
            },
        ],
        "pm_update": (
            f"Avance {project}: en aclaración. Semáforo amarillo. "
            "Bloqueo: respuestas P0 de datos/roles. "
            "Próxima entrega: mapa técnico + demo de lectura."
        ),
        "nota": "Demo local sin LLM. Texto recibido (recorte): " + texto[:180],
    }

    # Hook futuro:
    # if os.getenv("ANTHROPIC_API_KEY"): call_anthropic(...)
    # elif os.getenv("OPENAI_API_KEY"): call_openai(...)

    return jsonify(demo)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8787"))
    app.run(host="127.0.0.1", port=port, debug=True)
