# STANDARDS — Calidad y seguridad (V1)

Aplicable a PHP / Java / Python / SQL. Ajustar cuando UNAB publique su estándar interno.

## 1. Seguridad
- Nunca commits de contraseñas, tokens, connection strings reales
- Config por entorno (`.env` / `config.local` fuera de Git)
- Validar y sanitizar entradas de usuario
- SQL siempre parametrizado
- Principio de mínimo privilegio en BD y archivos
- No loguear datos personales sensibles en claro

## 2. Trazabilidad
- Toda decisión relevante → `DECISIONS.md` (qué / por qué / fecha)
- Todo pedido de jefe → `REQUIREMENTS.md` con fecha
- Cambios de negocio → usuario + timestamp cuando el modelo lo permita
- PRs/commits con mensaje claro: `feat|fix|docs|security: ...`

## 3. Diseño adaptable
- Separar: UI / lógica / acceso a datos (aunque sea carpeta simple)
- No hardcodear URLs, periodos, ni IDs mágicos
- Preferir cambios pequeños y reversibles
- Antes de tocar un módulo compartido: impacto en otras conexiones

## 4. Confiabilidad
- Definir criterios de aceptación antes de codear
- Prueba manual mínima al entregar (pasos en DAYLOG o README del feature)
- Manejar errores con mensaje útil (sin stack trace al usuario final)

## 5. SQL
- Transacciones en operaciones multi-tabla
- No borrar físico si el negocio pide baja lógica
- Índices/constraints: respetar modelo existente; no rediseñar sin acuerdo

## 6. Entrega al PC empresa
Checklist al copiar:
- [ ] Lista de archivos tocados
- [ ] Orden de despliegue (SQL → backend → frontend)
- [ ] Config local no sobrescrita
- [ ] Prueba humo post-copia
