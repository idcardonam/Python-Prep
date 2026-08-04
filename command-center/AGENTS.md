# AGENTS.md — Instrucciones permanentes para Cursor

## Quién es el usuario
Iván David Cardona Mendoza. Desarrollador híbrido (PHP, Java, Python, SQL) + operación TIC.
Sello: seguridad de la información + claridad.

## Cómo trabaja (OBLIGATORIO)
1. Contexto / reunión → preguntas → Iván responde.
2. Cuando el `.md` o el chat diga que **ya está pactado** / respuestas completas / `fase_codigo`:
   - **NO** pidas merge, JSON ni volver a la app para “desbloquear”.
   - **SÍ** pasa a crear código del proyecto de verdad.
3. Código vive fuera del Command Center, tipicamente:
   - `C:\dev\projects\<slug>\` o
   - `C:\xampp\htdocs\<slug>\` (PHP)
4. Entrega por bloques: “crea/pega estos archivos → prueba esto → escribe **sigue**”.
5. Los checks son recordatorio de verificación en el PC, **no** un gate.
6. Sigue hasta terminar el alcance pactado (o hasta que Iván diga pausa/cambio).

## Comando `procesa`
- Lee el `.md` indicado.
- Si hay preguntas **sin** respuesta → PLAYBOOK de aclaración (preguntas + riesgos cortos).
- Si **todas** están respondidas o el modo es `fase_codigo` / “ya pactado”:
  1. Resumen corto de lo pactado
  2. Carpeta destino del código
  3. **Empieza a generar archivos**
  4. Cierra el turno con: qué mirar en el PC + “escribe **sigue**”

JSON para `app.html` = **opcional**, solo si Iván lo pide. Nunca sustituye al código.

## Calidad de código
- Validación de entradas, errores controlados, sin secretos hardcodeados
- Transacciones si hay integridad; SQL parametrizado; logs sin PII
- IDENTITY_CODE.md
- No scope creep silencioso; no reescribir sistemas ajenos enteros

## Prohibido
- Mandar a “importa el merge” como paso obligatorio
- Repetir preguntas ya respondidas
- Parar el avance esperando checkboxes de la app
- Inventar requisitos
