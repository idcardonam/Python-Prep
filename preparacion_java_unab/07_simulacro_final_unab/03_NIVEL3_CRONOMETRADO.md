# Nivel 3 · Implementación cronometrada (60 minutos)

**Abrir solo cuando Nivel 2 esté corregido.**  
**Cronómetro: 60 minutos. Sin IA. Sin soluciones.**

---

## Escenario

Debes entregar un **MVP funcional en memoria** (sin BD obligatoria) del módulo de solicitudes.

## Requisitos mínimos (MVP)

### 1. Enums

```java
Rol: ESTUDIANTE, DOCENTE, ADMINISTRATIVO, ANALISTA_TIC
TipoSolicitud: INCIDENTE, REPORTE
Estado: ABIERTO, PENDIENTE_VERIFICACION_TIC, EN_GESTION, PENDIENTE_CONFIRMACION, CERRADO, RECHAZADO
Prioridad: BAJA, MEDIA, ALTA
```

### 2. Clase `Solicitud`

- id, titulo, descripcion, tipo, prioridad, estado, rolSolicitante, areaReporte (nullable)
- validaciones de título/descripción
- estado inicial según reglas:
  - INCIDENTE → ABIERTO
  - REPORTE con permiso → PENDIENTE_VERIFICACION_TIC
  - REPORTE sin permiso → RECHAZADO

### 3. Clase `SolicitudService`

```java
Solicitud crearIncidente(...)
Solicitud crearReporte(...)
Solicitud cambiarEstado(...)
List<Solicitud> listarPorEstado(...)
```

Reglas de transición:

- ABIERTO → EN_GESTION
- PENDIENTE_VERIFICACION_TIC → EN_GESTION o RECHAZADO
- EN_GESTION → PENDIENTE_CONFIRMACION o CERRADO (solo excepción con motivo)
- PENDIENTE_CONFIRMACION → CERRADO
- ABIERTO → CERRADO ❌

### 4. Demostración en `main`

1. Estudiante crea incidente válido
2. Admin nómina pide reporte académico sin permiso → RECHAZADO
3. Admin con permiso crea reporte → PENDIENTE_VERIFICACION_TIC
4. Analista toma un ticket a EN_GESTION
5. Intento inválido ABIERTO → CERRADO (debe fallar)

---

## Control de tiempo

| Minuto | Acción |
|---|---|
| 0–5 | Releer reglas y bocetar |
| 5–35 | Clases + validaciones + estados |
| 35–50 | Service + main de demostración |
| 50–60 | Probar y corregir fallos |

## Criterio de éxito

- Compila
- Cumple las 5 demos del `main`
- Explicas en 1 minuto qué priorizaste

Cuando termine el cronómetro, pega:

1. qué lograste
2. qué faltó
3. errores que viste

Luego pasamos a la **Prueba Crack 4h**.
