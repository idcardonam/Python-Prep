# Identidad de programación — Iván + Cursor (evolutiva)

Objetivo: código que se sienta **humano, claro y de equipo**, no “plantilla de IA”.

## Firma de estilo (aplicar en todos los proyectos)
1. Nombres en el idioma del dominio del negocio (español o inglés del sistema existente; no mezclar sin motivo).
2. Funciones cortas: una responsabilidad por función.
3. Comentarios solo donde aporten decisión de negocio o riesgo (“por qué”), no narrar el código obvio.
4. Validar entradas cerca de la frontera (API/formulario); lógica interna asume datos ya limpios.
5. Errores: mensaje claro para usuario + detalle técnico en log.
6. SQL/parametrizado siempre; transacciones cuando hay multi-paso.
7. Config fuera del código; cero secretos en repo.
8. Cambios pequeños y reversibles; no “reescribir el mundo”.
9. Toda feature nace con: criterios de aceptación + prueba manual de 3–5 pasos.
10. Milla extra solo si está marcada en el checklist del proyecto (no adornar sin acuerdo).

## Tono de mensajes UI
- Español claro, respetuoso, sin jerga innecesaria.
- Evitar: “Oops”, emojis de más, textos robóticos.
- Preferir: “No fue posible guardar. Revise el periodo e intente de nuevo.”

## Evolución
Cada proyecto puede añadir 1 regla nueva aprendida en `DECISIONS.md` si mejora el estándar global.
