# API local opcional (Modo B)

Cursor **no** ofrece una API pública para que tu HTML le cree chats solo.
Si quieres que la *torre de control* analice sin pasar por el chat, puedes usar
esta API local con tu propia key de un proveedor de IA.

## Qué hace
`POST /analizar` recibe texto de reunión y devuelve JSON
(preguntas, riesgos, millas, pasos) compatible con el botón
**Importar al proyecto** de `app.html`.

## Requisitos
- Python 3.10+
- Variable de entorno `ANTHROPIC_API_KEY` o `OPENAI_API_KEY`

## Arranque (cuando decidas usarla)
```bash
cd C:\dev\command-center\api
pip install -r requirements.txt
python server.py
```

Luego se puede conectar `app.html` a `http://127.0.0.1:8787/analizar`.

## Recomendación
Mientras entras a UNAB: usa **Modo A** (`procesa` en Cursor).
Es más seguro (sin key en el navegador) y mejor para generar código con contexto de archivos.
