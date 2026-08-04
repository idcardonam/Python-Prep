# Arquitectura real del Command Center (qué sí / qué no)

## Loop que usas (confirmado)
1. Creas el proyecto en la app con todo lo de la reunión (notas, controversias, rutas PDF/imagen).
2. Clic **Generar .md del proyecto** → descarga `PARA_CURSOR_<slug>.md` → lo guardas en `command-center/`.
3. Nuevo chat Cursor: `procesa command-center/PARA_CURSOR_<slug>.md`
4. El agente responde + JSON → lo pegas/importas en la app → tablero con preguntas, riesgos, millas, pasos.
5. Apruebas millas / respondes / o actualizas requerimientos o diseño → nuevo `.md` → `procesa` → nuevo JSON.
6. La app hace **merge**: no se pierde lo ya checkeado ni las respuestas; se actualiza el camino.

## Qué NO puede hacer una página HTML sola
- Abrir sola un chat de Cursor y “mandar” al agente como API oficial pública.
- Cursor hoy **no** expone “créame un chat y codea esto” para llamarlo desde tu `app.html`.

## Qué SÍ funciona
### Modo A — Recomendado (sin pagar APIs)
- `app.html` = torre de control.
- Genera `PARA_CURSOR_<slug>.md` por proyecto y modo.
- Cursor `procesa` → JSON → import merge.
- Botones en Tablero: actualizar requerimientos / ajuste camino (diseño-features) / fase código.

### Modo B — API propia con IA (después)
- `api/server.py` + tu API key → menos fricción.
- Cursor sigue mejor para escribir código en el repo.

### Modo C — Solo Cursor
- Sin tablero visual; solo `AGENTS.md` + carpetas.

**Decisión V1.6:** Modo A con archivos nombrados + merge + modos de actualización.

## Adjuntos
```
C:\dev\command-center\INBOX\<slug>\adjuntos\   ← PDF, PNG, JPG
```
Anota rutas en la app. Si están en el workspace, Cursor puede leerlas al hacer `procesa`.

## Código ajeno del equipo
Fase **integracion**: mapear → no romper → elevar seguridad → PR pequeño → pruebas.
