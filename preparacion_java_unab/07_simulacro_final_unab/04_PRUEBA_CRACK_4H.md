# Prueba Crack · Simulacro completo tipo UNAB (4 horas)

**Hazlo solo una vez, preferible la noche anterior o la mañana temprana.**  
**Sin IA. Sin mirar soluciones. Ambiente lo más parecido al aula.**

---

## Instrucciones de presentación (simula el aula)

Imagina que recibes:

1. Enunciado en PDF/Word
2. PC con JDK + IntelliJ/Eclipse + cliente SQL
3. Carpeta de entrega: `APELLIDO_NOMBRE_PRUEBA/`

Debes entregar:

- `analisis.md` o `analisis.docx`
- `modelo.sql`
- `src/` (Java)
- `README_ENTREGA.txt` (qué funciona / qué falta)

---

## Enunciado oficial simulado

### Cargo
Ingeniero(a) de Sistemas y Operación TIC / Desarrollador(a)

### Caso
UNAB requiere un módulo de **Gestión de Solicitudes TIC** integrado al ecosistema institucional.

### Alcance funcional

1. Registro de solicitudes por rol
2. Clasificación por tipo y prioridad
3. Flujo de estados con reglas
4. Escalamiento a otra área
5. Confirmación de solución y cierre
6. Auditoría de cambios
7. Consultas operativas para mesa TIC

### Restricciones técnicas

- Java POO
- SQL (PostgreSQL u Oracle)
- Capas Web/Servicio/DAO (si no alcanza web, documenta la interfaz)
- `PreparedStatement` si hay JDBC
- No concatenar SQL
- Validar en servicio (no solo UI)

### Datos sensibles

Las descripciones pueden contener datos personales. Debes proponer controles (validación, minimización, logs sin datos innecesarios).

---

## Distribución sugerida de las 4 horas

| Bloque | Tiempo | Entregable |
|---|---|---|
| Análisis | 0:00–0:30 | Actores, estados, criterios, riesgos |
| Diseño | 0:30–0:55 | Capas + DDL + transiciones |
| Java núcleo | 0:55–2:30 | Modelo + service + demo |
| SQL / JDBC | 2:30–3:20 | Script + consultas + 1 transacción |
| Web o documentación | 3:20–3:40 | Servlet/JSP básico o contrato HTTP |
| Cierre | 3:40–4:00 | Pruebas, README, explicación oral |

---

## Rúbrica del evaluador (100)

| Criterio | Puntos |
|---|---:|
| Análisis de negocio y roles | 20 |
| Estados / criterios / riesgos | 15 |
| Java (validación + transiciones) | 25 |
| SQL / integridad / auditoría | 20 |
| Seguridad y trazabilidad | 10 |
| Priorización y comunicación | 10 |

---

## Preguntas orales que pueden hacerte al final

1. ¿Por qué el estado inicial de un reporte no es ABIERTO?
2. ¿Qué pasa si dos analistas cambian el mismo ticket?
3. ¿Dónde validas permisos y por qué no solo en la pantalla?
4. ¿Qué diferencia Oracle vs PostgreSQL te importaría aquí?
5. ¿Cómo evitarías que un estudiante vea solicitudes de otro?

---

## Después del simulacro

Escribe 10 líneas:

- qué te bloqueó
- qué harías distinto mañana
- 3 frases listas para la defensa oral

Luego ábreme `soluciones/CLAVES_NIVELES.md` solo para comparar.
