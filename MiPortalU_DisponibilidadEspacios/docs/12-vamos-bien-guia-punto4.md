# ¿Vamos bien? — Guía punto 4 + correo del jefe

Fecha: 3 sep 2026. Mientras llega el código final de Reservitas.

## Para dónde vamos (correo del jefe — una frase)

Evolucionar la **consulta de disponibilidad de espacios** hacia MiPortalU: el estudiante consulta aulas/salones/auditorios **sin salir del portal**, con Banner como fuente. **No** es préstamo de equipos (eso va por KOHA / Krystel). El lunes se revisan **hallazgos + alternativa técnica + siguiente paso**, no una pantalla terminada.

## Punto 4 de la guía — checklist

| # | Actividad (guía) | Resultado esperado | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| 1 | Confirmar ambiente local MiPortalU | Ambiente operativo o bloqueo | Parcial | Capacitación con Julián; clone/rama PPRD-IC. Confirmar que `localhost` abre el módulo. |
| 2 | Ubicar `disponibilidad.php` | Estructura, includes, JS/CSS, funcionamiento | **Hecho** | PHP real: solo tabs + enlaces; includes header/lateral/footer. |
| 3 | Documentar enlaces a Reservitas | Mapa tipos, sedes, parámetros | **Hecho** | `id_tipo` 1/2/3, `id_sede`, `area`; URLs en entregable. |
| 4 | Cuando llegue Reservitas: lógica de consulta | Archivo, conexión, query/vista, reglas | **Avanzado con backup** | Backup Manuel: `day.php` → Oracle `BANINST1.V_RESERVAS_SALON` (aulas). Falta versión final + `config1/2/3`. |
| 5 | Comparar datos Reservitas vs mockup | Mapeo campos y vacíos | **Parcial** | ROOM, EDIF, HI/HF, TITULO mapeados. Falta validar salones (`id_tipo=1`) y no mostrar DOCENTE. |
| 6 | Definir alternativa técnica | Reutilizar consulta o reconstruir capa | **Borrador listo** | UI de cero en MiPortalU; **reutilizar vista Banner**; no copiar PHP Reservitas; equipos fuera. Confirmar con Carlos. |
| 7 | Tres escenarios vs Reservitas | Misma disponibilidad legado vs propuesta | **Pendiente** | Falta acceso/consulta limpia en TEST y/o código final. |
| 8 | Traer hallazgos el lunes | Recomendación, dependencias, riesgos, siguiente | **En curso** | Paquete `MiPortalU_DisponibilidadEspacios` + entregable. |

## Pedidos del correo — ¿cubiertos?

| Pedido del jefe | Estado |
| --- | --- |
| Revisar mockup, guía, docs | Hecho (paquete + mockup en repo) |
| Empezar por `disponibilidad.php` | Hecho |
| Cuando esté carpeta Reservitas → Banner espacios/ocupación | Backup analizado; falta oficial |
| Micro sesión Carlos Duarte | Por agendar (pregunta ya redactada) |
| Manuel García → TEST SQL Developer | Conversación hecha; falta sesión datos + configs |
| Julián Ojeda si trancas con portal | Disponible; no bloquea el lunes |
| Lunes: hallazgos + alternativa + siguiente paso | Encaminados |

## Veredicto

**Sí, van bien** y en la dirección correcta del jefe.

No están “atrasados” por no tener UI: el correo pide **exploración y recomendación** para el lunes. Ya tienen el corte de alcance (solo aulas), el mapa de enlaces, y la fuente candidata Banner. Lo que falta es **cerrar con personas** (Carlos/Manuel) y **validar** con el código final / TEST — no inventar otra cosa mientras esperan.

## Rumbo fijo (no se mueve)

1. Solo módulo **Disponibilidad de Aulas** (`id_tipo` 1–3).  
2. Consulta **informativa** → no botón de reserva.  
3. Fuente: **Banner** (`V_RESERVAS_SALON` a confirmar).  
4. UI nueva en MiPortalU; no portar Reservitas ni PHP 8 al legado.  
5. Equipos = fuera (KOHA / Krystel).

## Qué falta antes del lunes (poco y concreto)

1. Agendar **30 min Carlos** con la pregunta de `V_RESERVAS_SALON` + salones.  
2. Pedir a Manuel `config1/2/3` (sin claves) + acceso TEST solo lectura.  
3. Si llega el `day.php` final: confirmar que la vista es la misma.  
4. Llevar el entregable (`docs/08-entregable-lunes.md`) impreso/en pantalla.  
5. Opcional: 1 captura salones + 1 auditorios.

Si el código final no llega: el lunes se presenta lo mismo + bloqueo explícito (“pendiente carpeta oficial”) y la recomendación provisional sobre la vista. Eso cumple el correo.
