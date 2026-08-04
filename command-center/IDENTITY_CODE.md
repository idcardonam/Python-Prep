# Identidad de programación — Iván (robusta, evolutiva)

Propósito: que cualquier compañero lea el código y entienda **qué hace, por qué existe y por qué es seguro**.
No es estilo “de IA”. Es estilo **profesional de equipo + seguridad de la información**.

---

## 1) Principios no negociables
1. **Claridad > cleverness** — código obvio para un junior del equipo.
2. **Seguridad por defecto** — si hay duda, se cierra el acceso / se valida / no se expone.
3. **Trazabilidad** — decisiones y cambios de negocio dejan rastro.
4. **Cambios mínimos y reversibles** — no romper módulos vecinos.
5. **Datos ajenos no son de prueba** — enmascarar PII en ejemplos, logs y chats.
6. **La milla extra la propone el análisis**, no un checklist eterno igual en todos los proyectos.

---

## 2) Seguridad de la información (obligatorio en todo proyecto)

### 2.1 Datos
- Clasificar mentalmente: público / interno / sensible / restringido.
- Nunca hardcodear contraseñas, tokens, connection strings.
- Config por entorno (`config.local`, `.env` fuera de Git).
- Logs: no imprimir contraseñas, tokens, ni documentos de identidad completos.
- En desarrollo usar datos ficticios o enmascarados (`U******1`, `***@correo.com`).

### 2.2 Entradas y salidas
- Validar tipo, longitud, rango y formato en la frontera (API/form/UI).
- SQL siempre parametrizado / prepared statements (cero concatenar SQL con input).
- Escapar salida HTML (XSS) cuando haya render server-side.
- Subidas de archivo: tipo permitido, tamaño máximo, nombre sanitizado, fuera de webroot si aplica.

### 2.3 Control de acceso
- Toda operación sensible pregunta: ¿quién puede hacerlo?
- No confiar en “ocultar el botón” como seguridad; validar en servidor.
- Sesiones/tokens: expiración, no exponer secretos al cliente.
- Principio de mínimo privilegio en BD (usuario app ≠ root en producción).

### 2.4 Integridad
- Transacciones cuando hay multi-paso (si falla uno, no queda a medias).
- Baja lógica cuando el negocio lo pida (no borrar evidencia operativa).
- Errores al usuario: claros y seguros; detalle técnico solo en log.

### 2.5 Dependencias y despliegue
- No subir secretos al repo.
- Revisar qué cambia en módulos compartidos antes de tocarlos.
- Checklist de prueba humo post-despliegue.

### 2.6 Frases que debemos usar en código/comentarios de riesgo
- `// Seguridad: validar autorización antes de mutar`
- `// No loguear payload completo: puede traer PII`
- `// Parametrizado a propósito (evitar SQLi)`

---

## 3) Estilo de código (legible para compañeros)
- Nombres del **dominio del negocio** (estudiante, periodo, riesgo), no `tmp1`, `data2`.
- Funciones cortas, una responsabilidad.
- Comentarios = **por qué / riesgo / decisión**, no narrar lo obvio.
- Estructura predecible: UI → servicio/lógica → acceso a datos.
- Mensajes UI en español sobrio, institucional, sin “Oops” ni relleno.
- Commits/PR: `feat|fix|security|docs: …` + impacto.

### Anti-patrones (evitar)
- Bloques gigantes sin funciones
- Copiar-pegar con variantes mínimas sin extraer
- `catch` vacío
- “Dejar para después” validaciones de seguridad
- Textos mágicos sin constante/config

---

## 4) Cómo entramos a código ajeno (fase tardía / equipo)
Cuando otros envíen código:
1. **Mapear** (qué carpetas, entrypoints, config, BD).
2. **No reescribir** — adaptar al estilo del repo existente primero.
3. Si el repo no tiene estándar: proponer el nuestro en un PR pequeño (una mejora).
4. Toda intervención con: impacto → riesgo → prueba.
5. Documentar en `DECISIONS.md` del proyecto: “seguimos convención X del equipo”.

Regla de oro: **respetar el idioma del equipo; elevar seguridad sin pelear egos**.

---

## 5) Milla extra (definición)
No es un menú fijo de adornos.
Es: *“entendido este requerimiento, ¿qué mejora notable, segura y proporcional aporta valor al negocio o reduce riesgo?”*
Cada proyecto tendrá millas **distintas**, con beneficio + riesgo + cómo mitigarlo.

---

## 6) Evolución de esta identidad
Cuando aprendamos una regla nueva útil en un proyecto real, se agrega aquí en una línea datada:

### Historial
- 2026-08-04 — Identidad V1 robusta con eje de seguridad de la información.
