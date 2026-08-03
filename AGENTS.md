# AGENTS.md

## Cursor Cloud specific instructions

This repo is a multi-track learning / job-prep monorepo (Henry Python prep course, a
Challenge simulator, and a UNAB Java/PHP prep track). The actively developed product on
this branch is the **CV / portfolio PDF generator** (`cv_assets/` and
`preparacion_java_unab/generar_guia.py`), a set of Python CLI scripts built on
`reportlab` + `pyyaml`. There is no root `package.json`, `Makefile`, `requirements.txt`,
lockfile, or lint/CI config; runnable pieces are per-subproject.

### CV / PDF generator (primary product)
- Deps (`reportlab`, `pyyaml`) are installed by the startup update script; no per-run
  install needed.
- Run from the repo root so the scripts' relative paths (fonts, images, output dirs)
  resolve:
  - `python3 cv_assets/generar_cv.py --perfil cv_assets/perfil_base.yaml` → writes to `cv_output/`
  - `python3 cv_assets/generar_carta.py --output <path.pdf>` (`--output` is required)
  - `python3 cv_assets/generar_entrevista_unab.py` → writes to `entregables/`
  - `python3 preparacion_java_unab/generar_guia.py` → writes to `entregables/`
- Non-obvious: `cv_output/` is git-ignored (scratch output); `entregables/` is committed
  and holds pre-built deliverable PDFs, so regenerating there overwrites tracked files.
- No test/lint suite for the generators; verify by opening the produced PDF.

### Python Challenge simulator
- `cd "Simulación Challenge" && python3 tests.py` runs the stdlib `unittest` suite.
- Expected to FAIL out of the box: `checkpoint.py` is the intentionally-incomplete student
  template. The reference solution lives in `checkpoint_Resuelto.py`. Failing tests here
  are normal, not an environment problem.

### Java / PHP tracks (not needed for the CV generator)
- `preparacion_java_unab/` labs need extra services (JDK 21 + Maven, PostgreSQL, Tomcat,
  or Apache + MariaDB) that are NOT installed by the update script. Set those up on demand
  per `preparacion_java_unab/README.md` only if you work in that track.
