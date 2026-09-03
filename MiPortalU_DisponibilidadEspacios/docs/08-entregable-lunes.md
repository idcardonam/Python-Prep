# Entregable para la revisión del lunes

Completar con hallazgos reales. Lo que está escrito abajo es el estado **antes** de abrir el código (reunión + guía + mockup). Reemplazar las marcas `PENDIENTE` al explorar.

## 1. Flujo actual

**Qué hace MiPortalU**

La página `modulos/disponibilidadAulas/disponibilidad.php` presenta accesos por tipo de espacio y redirige a Reservitas. No muestra agenda.

**Qué hace Reservitas**

Consulta disponibilidad (fecha, campus/edificio, hora, espacio) y la pinta. Fuente: Banner u objeto intermedio **PENDIENTE**.

**Parámetros observados en HTML (por validar en código)**

| Tipo | Sedes vistas | Parámetro |
| --- | --- | --- |
| Aulas de informática | UNAB / Instituto Caldas | `id_tipo=2` |
| Salones | Campus Central / CSU / Campus El Bosque / La Casona | `id_tipo=1` |
| Auditorios | Campus Central | `id_tipo=3` |

**URL de destino Reservitas:** PENDIENTE  
**Archivos JS/CSS del módulo:** PENDIENTE  
**¿Hay query en el PHP del portal?** Hipótesis: no. Confirmar: PENDIENTE

## 2. Fuente

| Ítem | Valor |
| --- | --- |
| Sistema que ejecuta la consulta hoy | Reservitas |
| ¿Banner directo? | PENDIENTE |
| Owner.objeto (vista/paquete/tabla) | PENDIENTE — hipótesis: vista de Carlos Duarte usada en reservas |
| Archivo PHP de Reservitas | PENDIENTE (se mencionó un `day.php`; no confirmado) |
| Escritura en Banner | No requerida (a confirmar con Manuel García) |

## 3. Alternativa recomendada

Marcar una:

- [ ] **A.** Reutilizar consulta/reglas actuales; UI nueva en MiPortalU.
- [ ] **B.** Reconstruir capa de consulta en MiPortalU con equivalencia funcional.
- [ ] **Aún no se puede recomendar** porque falta: ________________

**Por qué (3–6 líneas):**

PENDIENTE. Marco de decisión en [05-alternativa-tecnica.md](05-alternativa-tecnica.md).

## 4. Mapeo

Ver tabla viva en [04-mapeo-datos.md](04-mapeo-datos.md). Resumen:

| UI | ¿Existe en la fuente? | Campo | Hueco |
| --- | --- | --- | --- |
| Tipo | PENDIENTE | | |
| Campus | PENDIENTE | | |
| Edificio | PENDIENTE | | |
| Código espacio | PENDIENTE | | |
| Fecha | PENDIENTE | | |
| Franja | PENDIENTE | | |
| Ocupación | PENDIENTE | | |
| Agenda del día | PENDIENTE | | |
| Responsable | No mostrar al estudiante | | Omitir si viene |

## 5. Prueba de equivalencia

| Escenario | Resultado Reservitas | Resultado propuesto | ¿Igual? |
| --- | --- | --- | --- |
| Informática | PENDIENTE | PENDIENTE | |
| Salones | PENDIENTE | PENDIENTE | |
| Auditorios | PENDIENTE | PENDIENTE | |

## 6. Bloqueos

| Bloqueo | Impacto | Dueño | Estado |
| --- | --- | --- | --- |
| Carpeta de desarrollo de Reservitas | No se ve la query real | Jonathan / equipo Reservitas | Solicitada |
| SQL Developer TEST solo lectura | No se valida objeto Banner | Manuel García | Por agendar |
| Validación vista vs. PHP | No se cierra A/B | Carlos Duarte | Por agendar |
| Usuarios Delta / SARA | Pruebas con perfil estudiante en PPRD | Jonathan | 3–4 días típicos |
| Código MiPortalU no está en este repositorio | Exploración del PHP en el equipo local UNAB | Iván | Ambiente interno |

## 7. Siguiente paso (propuesta)

Cuando la fuente esté clara:

1. Implementar clase de consulta en MiPortalU (PHP 5.6 + Oracle) según A o B.
2. Sustituir los enlaces de `disponibilidad.php` por la UI del mockup (ajustada a datos reales).
3. Tres pruebas de equivalencia en PPRD.
4. Coordinar push con Julián.

**Tamaño preliminar (sin código aún):** mediano. El riesgo no es la pantalla; es ubicar y reutilizar (o equivalente) la consulta de ocupación sin copiar el legado ni escribir en Banner.

**Actividad concreta inmediata (esta semana, antes del lunes):**

1. Documentar `disponibilidad.php` (enlaces y `id_tipo`).
2. Agendar 30 min con Carlos y 30 min con Manuel.
3. En cuanto llegue Reservitas, extraer owner.objeto y pegarlo en la sección 2.
