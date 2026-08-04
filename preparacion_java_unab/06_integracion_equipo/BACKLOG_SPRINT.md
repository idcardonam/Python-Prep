# Backlog del sprint de integración

Duración simulada: una semana.

## Objetivo del sprint

Permitir que el equipo TIC filtre, atienda y audite incidencias sin romper el flujo existente de creación.

## US-01 · Filtrar incidencias

**Como** integrante del equipo TIC  
**Quiero** filtrar por estado y prioridad  
**Para** concentrarme en los casos relevantes.

### Criterios de aceptación

- Sin filtros se muestran todas.
- Estado filtra exactamente el enum seleccionado.
- Prioridad filtra exactamente el enum seleccionado.
- Ambos filtros pueden combinarse.
- Un valor inválido produce mensaje controlado.
- El filtro no modifica información.

### Riesgos

- Conversión insegura de enum.
- Estado guardado como texto inconsistente.
- Filtro implementado solo en interfaz.

## US-02 · Cambiar estado

**Como** técnico  
**Quiero** avanzar el estado de una incidencia  
**Para** reflejar el progreso de atención.

### Criterios de aceptación

- `ABIERTA → EN_PROGRESO`.
- `EN_PROGRESO → CERRADA`.
- No se permite cerrar directamente.
- No se permite reabrir.
- La acción utiliza POST.
- Si la incidencia no existe, devuelve 404.
- Después de éxito aplica Post/Redirect/Get.

### Riesgos

- Cambiar mediante GET.
- Perder actualización concurrente.
- Permitir transición inválida.

## US-03 · Registrar auditoría

**Como** responsable del proceso  
**Quiero** conocer quién cambió un estado y cuándo  
**Para** mantener trazabilidad.

### Criterios de aceptación

- Registra estado anterior y nuevo.
- Registra usuario, fecha y comentario.
- El historial se crea en la misma transacción.
- Si falla el historial, se revierte el cambio.
- No guarda secretos.
- Se consulta ordenado por fecha.

### Riesgos

- Estado actualizado sin historial.
- Dato personal innecesario en logs.
- Relojes o zonas horarias inconsistentes.

## Tareas transversales

- Actualizar contrato de servicio.
- Añadir pruebas unitarias.
- Añadir prueba de integración.
- Actualizar README.
- Revisar cabeceras y validación.
- Construir WAR.
- Desplegar en Tomcat.
- Ejecutar regresión de creación.

## Tablero

| Historia | Pendiente | En curso | Revisión | Integrada |
|---|---|---|---|---|
| US-01 | X | | | |
| US-02 | X | | | |
| US-03 | X | | | |

Actualiza el tablero solo cuando exista evidencia.

## Preguntas de revisión

- ¿El contrato cambió?
- ¿Alguna rama necesita ese cambio?
- ¿La migración de datos es compatible?
- ¿Qué ocurre si dos usuarios actualizan?
- ¿Qué prueba protege el comportamiento anterior?
- ¿Hay plan de reversión?
