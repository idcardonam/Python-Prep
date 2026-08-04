# AGENTS.md — Instrucciones permanentes para Cursor

## Quién es el usuario
Iván David Cardona Mendoza. Rol esperado: **desarrollador híbrido** (también operación TIC).
Stack a manejar: **PHP, Java, Python, SQL**. Seguridad informática como sello personal.

## Contexto de trabajo
- Puede haber **PC empresa restringido** (sin Cursor). El código “oficial” puede vivir allá.
- Este Command Center y la generación de código ocurren en **PC personal**.
- Iván puede **copiar/transcribir** al PC empresa (doble trabajo aceptado para aprender).
- Reuniones: él envía transcript/texto (preferido), audio, PDF o imágenes.
- Muchos proyectos en paralelo → cada uno en `PROJECTS/<nombre>/` con trazabilidad.
- Flujo UI: `app.html` genera `PARA_CURSOR_<slug>.md` → chat `procesa` → JSON → import merge en la app.

## Comportamiento obligatorio
1. No inventar requisitos. Si falta info → preguntar.
2. Usar el orden del `PLAYBOOK.md`.
3. Priorizar: seguridad, trazabilidad, no romper integraciones, entregables verificables.
4. Hablar claro, humanizado, útil en reunión con jefes no técnicos.
5. Al iniciar un proyecto nuevo: basarse en `PROJECTS/_plantilla/`.
6. Estimar en rangos realistas de desarrollador con práctica.
7. Cuando haya avance a jefe de proyecto: usar tono de `templates/PM_UPDATE_SCRIPT.md`.
8. Enmascarar datos sensibles en ejemplos (nunca pedir ni guardar contraseñas reales aquí).
9. **Milla extra = trabajo de la IA**: en cada proyecto proponer 3–6 mejoras *nuevas* (no un catálogo repetido), cada una con beneficio, riesgo y mitigación. Iván solo elige con checks.
10. Aplicar `IDENTITY_CODE.md` (seguridad de la información como eje).
11. Si el comando es `procesa` (con o sin ruta a un `.md`):
    - Leer el archivo indicado (ej. `command-center/PARA_CURSOR_mi-proyecto.md`) o `PARA_CURSOR.md`.
    - Responder con el orden del PLAYBOOK.
    - Al final **exportar JSON** importable por `app.html`.
12. **Continuidad / MERGE (crítico):**
    - No borrar el idioma ni el estado del proyecto.
    - Respetar millas con `ok:true` y pasos con `done:true` del estado actual del `.md`.
    - No repetir preguntas ya respondidas; solo nuevas o abiertas.
    - En modos `actualizar_requerimientos` o `ajuste_camino`: actualizar/añadir; no wipe.
    - Diseño, features y alcance van en el mismo schema (pasos/millas/preguntas/riesgos).

## Schema JSON (siempre al final de `procesa`)
```json
{
  "project": "Nombre",
  "modo": "analisis_inicial|actualizar_requerimientos|ajuste_camino|fase_codigo",
  "estimacion": "...",
  "phase": "aclaracion|desarrollo|pruebas|entrega|integracion",
  "sem": "g|y|r",
  "preguntas": [{"prioridad":"P0","texto":"...","respuesta":""}],
  "riesgos": [{"titulo":"...","detalle":"...","mitigacion":"..."}],
  "millas": [{"titulo":"...","beneficio":"...","riesgo":"...","mitigacion":"...","ok":false}],
  "pasos": [{"title":"...","detail":"...","done":false}],
  "pm_update": "texto corto para el JP"
}
```
La app hace merge por título/texto: conserva respuestas, checks y pasos hechos.

## Calidad mínima en código que generes
- Validación de entradas
- Manejo de errores controlado
- Sin secretos hardcodeados
- Transacciones cuando hay integridad de datos
- Logs/auditoría en cambios de negocio
- SQL parametrizado / prepared statements
- Pasos de prueba manual cortos

## Prohibido
- “Rehacer todo el sistema” sin acuerdo
- Scope creep silencioso
- Ignorar estándares del equipo cuando se conozcan
- Wipe del tablero en actualizaciones (siempre merge)
- Grabación/ocultamiento ilegal: si menciona grabar reuniones, recordar consentimiento/política

## Cómo empezar cada chat de proyecto
Leer si existen: el `.md` que Iván indique, más `PROJECT.md`, `REQUIREMENTS.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `DAYLOG.md`.
