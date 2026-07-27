# Nivel 2 · Diseño técnico + SQL (SIN cronómetro)

**Abrir solo cuando Nivel 1 esté corregido.**  
**Duración sugerida:** 45–60 min.  
**Entrega:** diseño + SQL. Aún no es obligatorio Java completo.

---

## Contexto

TIC aprueba el análisis del Nivel 1 y pide el diseño técnico del módulo **Solicitudes de Soporte**.

Stack institucional esperado:

- Java (POO)
- SQL (PostgreSQL o Oracle)
- Capas: Web / Servicio / DAO
- Seguridad y auditoría

---

## Entregables Nivel 2

### A. Arquitectura de capas

Explica en 8–12 líneas:

1. Qué hace la capa Web
2. Qué hace el Servicio
3. Qué hace el DAO
4. Dónde van las reglas de negocio
5. Dónde va el SQL

### B. Modelo de datos (DDL)

Diseña tablas mínimas:

```text
usuario
solicitud
historial_solicitud
permiso_reporte (si aplica)
```

Incluye:

- PK / FK
- NOT NULL
- CHECK de estados y prioridades
- índices útiles (estado, solicitante)

### C. Consultas SQL (5)

1. Listar solicitudes abiertas con nombre del solicitante
2. Contar solicitudes por estado y prioridad
3. Ver historial de una solicitud ordenado por fecha
4. Solicitudes de un área/reporte sin permiso (o rechazadas)
5. Transacción: cambiar estado + insertar historial

### D. Contratos Java (solo firmas)

Sin implementar todavía, escribe firmas:

```java
enum Rol { ... }
enum TipoSolicitud { ... }
enum EstadoSolicitud { ... }
enum Prioridad { ... }

class Solicitud { ... }
class SolicitudService {
    Solicitud crear(...);
    Solicitud cambiarEstado(...);
    List<Solicitud> filtrar(...);
}
```

### E. Matriz de transiciones

Tabla:

| Desde | Hacia | ¿Quién puede? | ¿Permitido? |
|---|---|---|---|

---

## Autoevaluación Nivel 2

- [ ] Separé reglas (servicio) de SQL (DAO)
- [ ] El DDL protege integridad
- [ ] Historial va en la misma transacción que el cambio
- [ ] Transiciones inválidas están explícitas
- [ ] No metí lógica de negocio en la vista

Cuando termines, pégame tu diseño. Corrijo y pasamos a **Nivel 3 cronometrado**.
