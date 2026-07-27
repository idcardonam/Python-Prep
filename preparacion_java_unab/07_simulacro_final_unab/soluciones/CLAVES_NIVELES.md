# Claves de evaluación · Simulacros finales UNAB

Ábrelo **solo después** de intentar cada nivel.

---

## Nivel 1 · Qué busca un Director TIC

### Roles (ejemplo sólido)

| Rol | Puede | No puede |
|---|---|---|
| Estudiante | Crear incidente, ver propios, confirmar solución | Pedir reportes administrativos, ver tickets ajenos |
| Docente | Crear incidente académico/técnico, ver propios | Acceder a reportes de nómina/finanzas |
| Administrativo | Crear incidente y reportes de **su área** | Reportes de otras áreas sin permiso |
| Analista TIC | Gestionar, escalar, verificar, cerrar, ver historial | Alterar sin motivo/trazabilidad |

### Estados recomendados

```
INCIDENTE:
ABIERTO → EN_GESTION → PENDIENTE_CONFIRMACION → CERRADO
                 ↘ ESCALADO → (vuelve a EN_GESTION)

REPORTE:
PENDIENTE_VERIFICACION_TIC → EN_GESTION → ...
                           ↘ RECHAZADO
```

### Criterios buenos vs malos

**Mal:** “el sistema debe ser seguro”  
**Bien:** “si estudiante solicita REPORTE, el sistema rechaza y muestra mensaje de no autorizado”

### Riesgos esperados

1. Datos personales en descripción → logs/historial  
2. Escalamiento sin notificación → usuario sin respuesta  
3. Cierre sin confirmación → falsa sensación de solución  
4. Permiso solo en UI → bypass  

### Pregunta buena al jefe

> “¿Existe matriz oficial de roles/permisos por tipo de reporte y área, o debemos definirla en esta primera versión?”

---

## Nivel 2 · Claves técnicas

- Reglas en **Servicio**, SQL en **DAO**, UI sin lógica sensible.
- Historial en **misma transacción** que el cambio de estado.
- CHECK/ENUM de estados en BD + validación en Java.
- Índice `(estado, prioridad)` para mesa TIC.
- Transición `ABIERTO → CERRADO` bloqueada salvo excepción documentada.

---

## Nivel 3 · Checklist MVP

- [ ] `estadoInicial(INCIDENTE,*) = ABIERTO`
- [ ] `estadoInicial(REPORTE,false) = RECHAZADO`
- [ ] `estadoInicial(REPORTE,true) = PENDIENTE_VERIFICACION_TIC`
- [ ] `ABIERTO → CERRADO` lanza excepción
- [ ] `main` demuestra los 5 casos

---

## Prueba Crack · Interpretación de puntaje

| Puntaje | Lectura para contratación |
|---|---|
| < 55 | Aún no listo sin supervisión fuerte |
| 55–69 | Potencial; faltan controles |
| 70–84 | Perfil viable para UNAB con mentoring |
| 85–100 | Candidato sólido de mesa TIC |

Recuerda: con **2 años** pedían experiencia certificable. La prueba mide **juicio + ejecución**, no años en el papel.
