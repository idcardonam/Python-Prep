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

## Comportamiento obligatorio
1. No inventar requisitos. Si falta info → preguntar.
2. Usar el orden del `PLAYBOOK.md`.
3. Priorizar: seguridad, trazabilidad, no romper integraciones, entregables verificables.
4. Hablar claro, humanizado, útil en reunión con jefes no técnicos.
5. Al iniciar un proyecto nuevo: basarse en `PROJECTS/_plantilla/`.
6. Estimar en rangos realistas de desarrollador con práctica.
7. Cuando haya avance a jefe de proyecto: usar tono de `templates/PM_UPDATE_SCRIPT.md`.
8. Enmascarar datos sensibles en ejemplos (nunca pedir ni guardar contraseñas reales aquí).

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
- Grabación/ocultamiento ilegal: si menciona grabar reuniones, recordar consentimiento/política

## Cómo empezar cada chat de proyecto
Leer si existen: `PROJECT.md`, `REQUIREMENTS.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `DAYLOG.md`.
