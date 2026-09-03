# Checklist de exploración

Usar en orden. Lo que no se pueda cerrar, va a **Bloqueos** del entregable del lunes.

## 1. Ambiente

- [ ] Clone de MiPortalU abre en `localhost`
- [ ] Login local funciona
- [ ] Se localiza `modulos/disponibilidadAulas/`
- [ ] Rama de trabajo: PPRD-IC (no commitear a master sin Julián)

## 2. Módulo actual del portal

- [ ] Leer `disponibilidad.php` y sus includes
- [ ] Listar JS/CSS propios del módulo
- [ ] Capturar HTML de los tres tipos y sedes
- [ ] Documentar URL y query string hacia Reservitas
- [ ] Validar en código el significado de `id_tipo` 1 / 2 / 3
- [ ] Confirmar que no hay consulta a BD en este PHP (hipótesis: solo enlaces)

Registrar hallazgos en [08-entregable-lunes.md](08-entregable-lunes.md) sección “Flujo actual”.

## 3. Reservitas (cuando llegue la carpeta)

- [ ] Ubicar el PHP de agenda/consulta (confirmar si existe algo tipo `day.php`)
- [ ] Anotar archivo, conexión y credenciales **solo en notas internas**, no en Git público
- [ ] Extraer query / vista / procedimiento
- [ ] Anotar filtros: tipo, sede, edificio, fecha, horas
- [ ] Ver si el PHP filtra después de la BD
- [ ] Ver si trae responsable u otros datos personales

## 4. Banner TEST (con Manuel)

- [ ] Conexión SQL Developer OK
- [ ] Describe/select de prueba sobre el objeto identificado (solo lectura)
- [ ] Confirmar owner.objeto
- [ ] Medir tiempo de una consulta de un día y un campus

## 5. Carlos Duarte

- [ ] Preguntas de [06-preguntas-equipo.md](06-preguntas-equipo.md) resueltas
- [ ] Decisión A o B escrita en una frase
- [ ] Riesgos y dependencias anotados

## 6. Equivalencia (si hay acceso a Reservitas + fuente)

- [ ] Escenario informática
- [ ] Escenario salones
- [ ] Escenario auditorios
- [ ] Diferencias documentadas (no “corregir” Reservitas en esta etapa)

## 7. Antes del lunes

- [ ] Completar [08-entregable-lunes.md](08-entregable-lunes.md)
- [ ] Dejar bloqueos explícitos (carpeta, permisos, VPN, usuarios Delta)
- [ ] Proponer **una** siguiente actividad de construcción y un tamaño (grande/mediano/chico), no un calendario

## Qué no hacer esta semana

- No implementar la UI final en producción.
- No crear tablas réplica de espacios en el esquema del portal.
- No pedir permisos de escritura en Banner.
- No mezclar reserva de equipos.
- No pushear al GitLab del portal sin avisar a Julián.
