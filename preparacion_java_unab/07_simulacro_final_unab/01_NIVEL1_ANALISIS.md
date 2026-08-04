# Nivel 1 · Análisis del requerimiento (SIN cronómetro)

**Duración sugerida:** 30–45 min (sin presión).  
**Entrega:** solo texto / papel. **No codear todavía.**

---

## Contexto institucional (como en UNAB)

El Departamento TIC necesita un módulo interno de **Solicitudes de Soporte Académico-Administrativo** para:

- Estudiantes
- Docentes
- Administrativos
- Analistas TIC

Hoy las solicitudes llegan por correo y WhatsApp. Hay demoras, pérdida de trazabilidad y riesgos de acceso a información sensible (notas, documentos de identidad, datos financieros).

### Objetivo del módulo

Permitir registrar, clasificar, atender, escalar y cerrar solicitudes con control de roles, estados y auditoría.

---

## Enunciado Nivel 1

Como analista/desarrollador, responde **por escrito** (Word, Notion o papel):

### A. Actores y permisos

1. Lista los 4 roles.
2. Para cada rol, escribe **qué puede hacer** y **qué no puede hacer**.

### B. Tipos de solicitud

Define al menos 3 tipos. Ejemplo libre, pero institucionales:

- INCIDENTE_TECNICO (portal, correo, WiFi)
- SOLICITUD_REPORTE (reportes administrativos)
- CAMBIO_DATOS (corrección de información)

Para cada tipo indica si requiere **autorización especial**.

### C. Estados del ciclo de vida

Propón mínimo **6 estados** y dibuja el flujo (flechas).

### D. Criterios de aceptación (mínimo 5)

Formato obligatorio:

```
Dado que ...
cuando ...
entonces ...
```

Deben cubrir:

1. Campos obligatorios
2. Permisos por rol
3. Transición de estado válida
4. Transición inválida bloqueada
5. Registro en historial / auditoría

### E. Riesgos (mínimo 3)

Para cada riesgo:

- qué puede pasar
- impacto en la universidad
- control propuesto

Incluye al menos uno de **datos personales (Ley 1581)**.

### F. Pregunta al jefe TIC

Escribe **una sola pregunta** que harías a Jonathan Espinel / Vicky Lozano antes de desarrollar.

---

## Plantilla de respuesta (cópiala)

```text
1. ROLES
- Estudiante: puede... / no puede...
- Docente: ...
- Administrativo: ...
- Analista TIC: ...

2. TIPOS DE SOLICITUD
- ...
- ...
- ...

3. ESTADOS
ABIERTO -> ...
...

4. CRITERIOS
1) Dado... Cuando... Entonces...
2) ...
3) ...
4) ...
5) ...

5. RIESGOS
1) ...
2) ...
3) ...

6. PREGUNTA AL JEFE
...
```

---

## Autoevaluación Nivel 1

Marca solo cuando sea cierto:

- [ ] Separé roles con permisos claros
- [ ] Distinguí incidente vs reporte/autorización
- [ ] Mis estados no se contradicen
- [ ] Mis criterios son medibles (sí/no)
- [ ] Incluí trazabilidad y datos personales
- [ ] Mi pregunta al jefe es concreta (no genérica)

Cuando termines, **pégame tu respuesta completa** aquí.  
Te corrijo como Director TIC y recién ahí pasamos al **Nivel 2**.
