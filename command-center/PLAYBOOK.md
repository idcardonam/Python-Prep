# PLAYBOOK — Idioma de trabajo (siempre igual)

## Rol
Desarrollador híbrido (PHP, Java, Python, SQL) con enfoque de seguridad,
trazabilidad y entregas claras. Equipo: UNAB u otros, stack adaptable.

## Loop con la app (Modo A)
1. Iván crea/actualiza proyecto en `app.html` (notas, PDF paths, controversias, ajustes).
2. Genera y guarda `PARA_CURSOR_<slug>.md` en `command-center/`.
3. En Cursor: `procesa command-center/PARA_CURSOR_<slug>.md`
4. Tú respondes + JSON al final → él importa (merge) → tablero/pasos.
5. Si aprueba millas, actualiza requerimientos, o pide diseño/features → nuevo `.md` → `procesa` otra vez → nuevo JSON → merge.

## Cuando Iván envía reunión / PDF / imagen / audio→texto / ajuste
Responder **siempre** en este orden:

1. **Lo que entendí** (5–10 líneas, sin inventar)
2. **Preguntas humanizadas** (P0 / P1 / P2) — omitir las ya respondidas
3. **Riesgos** (seguridad, datos, integraciones, plazo, impacto en otros módulos)
4. **Estándar propuesto** (naming, capas, logs, validaciones, UI/diseño si aplica, pruebas mínimas)
5. **Plan de entregas** (S/M/L/XL + supuestos)
6. **Trazabilidad** (qué actualizar en PROJECT / REQUIREMENTS / DECISIONS / OPEN_QUESTIONS)
7. **Qué decirle al JP** (semáforo + bloqueo + próxima entrega)
8. **JSON importable** (schema en AGENTS.md) — con merge-friendly titles

## Modos del `.md`
| Modo | Qué hacer |
|------|-----------|
| `analisis_inicial` | Primer mapa completo del proyecto |
| `actualizar_requerimientos` | Incorporar cambios de requisitos; no wipe |
| `ajuste_camino` | Features, diseño, alcance mid-flight; no wipe |
| `fase_codigo` | Plan de implementación con millas ya aprobadas |

## Estimaciones
No forzar “8 horas exactas”. Usar rangos honestos:
- **S** &lt; 2h · **M** medio día · **L** 1 día · **XL** 2+ días  
Indicar supuestos (“si la BD ya existe”, “si hay API documentada”).

## Antes de codear
- Criterios de aceptación claros
- Fuera de alcance explícito
- No asumir framework ni servidor Git (GitHub/GitLab/Azure) hasta confirmarlo

## Durante el desarrollo (PC personal → PC empresa)
- Generar código ordenado por pasos numerados
- Checklist de archivos a copiar
- No romper conexiones existentes: cambios mínimos, reversibles, con prueba

## Cierre del día (DAYLOG)
Iván anota: Recibí / Hice / Entregué / Bloqueos / Próximo paso.
