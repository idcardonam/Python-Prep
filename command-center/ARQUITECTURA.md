# Arquitectura real del Command Center (qué sí / qué no)

## Tu visión (correcta)
1. Crear proyecto → subir reunión/PDF/imagen/controversias  
2. Iniciar análisis → preguntas, riesgos, millas extra (sugeridas por IA), estimaciones  
3. Tú respondes preguntas + check de millas  
4. Vista paso a paso (crear archivo, SQL, prueba…) con checks  
5. Fase pruebas / entregables / bloqueos (“falta autorización del jefe”)  
6. Código con identidad segura y humanizada  

## Qué NO puede hacer una página HTML sola
- Abrir sola un chat de Cursor y “mandar” al agente como API oficial pública.
- Cursor hoy **no** expone “créame un chat y codea esto” para llamarlo desde tu `app.html` como si fuera WhatsApp.

## Qué SÍ podemos hacer (y funciona bien)
### Modo A — Recomendado ahora (sin pagar APIs)
- `app.html` = torre de control (proyectos, archivos, pasos, bloqueos, semáforo).
- Un clic genera/actualiza `PARA_CURSOR.md` (+ copia adjuntos a `INBOX/`).
- En Cursor escribes `procesa` → yo (agente) lleno el análisis.
- La app tiene botón **“Importar respuesta de Cursor”**: pegas mi JSON/markdown y se llenan preguntas, millas, pasos, riesgos en la UI.

### Modo B — API propia con IA (si quieres menos fricción)
- Servidor local (`api/server.py`) con tu API key (OpenAI/Anthropic/etc.).
- La app llama `POST /analizar` y rellena sola preguntas/millas/pasos.
- Cursor sigue siendo mejor para **escribir código en el repo** con contexto de archivos.
- Implica: clave personal, costo por uso, no subir la key al Git.

### Modo C — “Todo automático dentro de Cursor”
- No depende de HTML: trabajamos solo en Cursor con `AGENTS.md` + carpetas.
- Menos tablero visual; más velocidad de código.

**Decisión V1.5:** Modo A completo en la UI + esqueleto Modo B listo para cuando pongas API key.

## Adjuntos (PDF / imágenes)
Carpeta:
```
C:\dev\command-center\INBOX\proyecto-xxx\
  reunion.txt
  audio\
  adjuntos\   ← PDF, PNG, JPG
```
En la app: zona “Adjuntos” (guardas archivos ahí y anotas la lista en el proyecto).
En Cursor: me dices `procesa` y, si los archivos están en el workspace, puedo leer imágenes/PDF texto cuando aplique.

## Cuando el equipo te manda código ajeno
Fase del proyecto: **integración / adaptación**.
Pasos fijos en la app: mapear repo → no romper → alinear seguridad → PR pequeño → pruebas.
