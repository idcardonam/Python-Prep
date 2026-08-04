# Command Center — Iván (UNAB / Dev híbrido)

Torre de control personal: reuniones → análisis Cursor → tablero (preguntas, riesgos, millas, pasos).
**No es código de UNAB.** Vive en tu PC: `C:\dev\command-center`

## Loop (Modo A)
1. Abre `INICIAR.html` → crea proyecto, pega reunión + rutas PDF.
2. Genera `PARA_CURSOR_<slug>.md` y guárdalo en esta carpeta.
3. En Cursor: `procesa command-center/PARA_CURSOR_<slug>.md`
4. Importa el JSON en la app (**merge**: no pierde checks/respuestas).
5. Actualizas requisitos o diseño → nuevo `.md` → `procesa` → nuevo JSON.

Detalle: `COMO_EMPEZAR.txt`, `ARQUITECTURA.md`, `PLAYBOOK.md`, `AGENTS.md`.

## Estructura
```
command-center/
  app.html
  PLAYBOOK.md  AGENTS.md  IDENTITY_CODE.md  STANDARDS.md
  INBOX/<slug>/adjuntos/
  PROJECTS/_plantilla/
  templates/
  api/          (opcional, Modo B)
```

## Regla de oro
Aquí va **contexto y decisiones**. Secretos/PII reales no van a Git ni al chat sin enmascarar.
Código de apps → `C:\dev\projects\` (no aquí). PHP de prueba → `C:\xampp\htdocs\` cuando toque.
