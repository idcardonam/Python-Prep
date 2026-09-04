# Arranque ya — repo lab + lunes + prototipo + Cursor como IDE

## 1. Crear y cargar el repositorio nuevo (hazlo tú en el PC)

### Paso 1.1 — Crear el repo en GitHub (privado)

1. Entra a https://github.com/new  
2. **Repository name:** `miportalu-lab`  
3. **Private** (obligatorio).  
4. No marques README si vas a subir carpeta existente (o sí, da igual; luego pones el código encima).  
5. Create repository.  
6. Copia la URL, ej. `https://github.com/idcardonam/miportalu-lab.git`

### Paso 1.2 — Copiar MiPortalU a una carpeta lab (sin tocar el oficial)

En el Explorador de Windows:

1. Localiza el portal que te dejó Julián (ej. `D:\repositorio\portal`).  
2. Copia **toda** la carpeta.  
3. Pégala como `D:\lab\miportalu-lab` (nueva ruta).  
4. **No trabajes más el prototipo dentro del clone UNAB.** El oficial se queda quieto.

### Paso 1.3 — Sanitizar antes de Git

En `D:\lab\miportalu-lab`:

1. Abre `conecora.php` (y cualquier `conec.php` / config con claves).  
2. Deja usuario y password en `""` o muévelos a un archivo `*.local.php` que **no** vas a subir.  
3. Borra `error_log.log` si existe.  
4. **No** copies dentro Reservitas ofuscado.

Crea archivo `.gitignore` en la raíz del lab:

```gitignore
.env
*.local.php
**/error_log.log
*.log
.DS_Store
Thumbs.db
```

Crea `README.md` en la raíz:

```markdown
# miportalu-lab (SANDBOX)

Copia de laboratorio de MiPortalU.
NO es el GitLab UNAB. No subir secretos.
Proyecto activo: Disponibilidad de Aulas (consulta informativa).
```

### Paso 1.4 — Primer Git y push

Abre PowerShell:

```powershell
cd D:\lab\miportalu-lab

git init
git add .
git status
git commit -m "Sandbox inicial MiPortalU (sin secretos)"
git branch -M main
git remote add origin https://github.com/idcardonam/miportalu-lab.git
git push -u origin main
```

Si GitHub pide login: usa tu usuario y un **Personal Access Token** (no la clave de la cuenta), o GitHub Desktop / Git Credential Manager.

Si `git` dice que la carpeta ya es un repo del GitLab UNAB:

```powershell
# Quitar el remote de la UNAB sin borrar archivos
git remote -v
git remote remove origin
git remote add origin https://github.com/idcardonam/miportalu-lab.git
git push -u origin main
```

Si prefieres repo limpio sin historial UNAB:

```powershell
# Cuidado: solo en la copia lab
Remove-Item -Recurse -Force .git
git init
git add .
git commit -m "Sandbox inicial MiPortalU (sin secretos)"
git branch -M main
git remote add origin https://github.com/idcardonam/miportalu-lab.git
git push -u origin main
```

### Paso 1.5 — Abrir ese repo en Cursor (Cursor como IDE)

Cursor **es** el IDE (como VS Code) + agente.

1. Cursor → **File → Open Folder** → `D:\lab\miportalu-lab`  
   **o** Cloud Agent: “New agent” apuntando al repo `miportalu-lab`.  
2. Abre el chat del agente **en ese workspace** (no en Python-Prep).  
3. Pega el **prompt de arranque** de la sección 4 abajo.

Así Cursor edita archivos, corre terminal, busca en el código y arma el prototipo **dentro del lab**.

---

## 2. Qué presentamos el lunes (prioridad #1)

El jefe pidió **hallazgos + alternativa + siguiente paso**, no producción terminada.

### Llevar el lunes (checklist)

| # | Entregable | Estado actual |
| --- | --- | --- |
| 1 | Flujo actual: portal solo enlaza; Reservitas pinta | Listo |
| 2 | Alcance: solo aulas (`id_tipo` 1–3); equipos = KOHA/fuera | Listo |
| 3 | Fuente: `BANINST1.V_RESERVAS_SALON` (Carlos: también salones) | Listo |
| 4 | Conexión: OCI8 → SID TEST (`172.16.20.38:1521`) | Listo (patrón) |
| 5 | Alternativa: UI de cero en MiPortalU + reutilizar vista Banner; no copiar PHP Reservitas; no React SPA | Listo |
| 6 | Stack: plantilla Julián + clase + CSS/JS moderno | Listo |
| 7 | Demo/prototipo visual (si alcanza) | En lab, esta semana |
| 8 | Bloqueos: user TEST solo lectura; day.php oficial; configs limpias | Decir |

**Mensaje del lunes en una frase:**

> Migraremos la consulta informativa de aulas a MiPortalU de cero (módulo + clase), leyendo `V_RESERVAS_SALON` en Banner TEST; no tocamos reserva ni equipos; el prototipo lo validamos en sandbox sin tocar GitLab UNAB.

El paquete de bitácora sigue en Python-Prep (`MiPortalU_DisponibilidadEspacios/`).

---

## 3. Qué es el “proyecto nuevo” en el lab (prioridad #2)

Nombre: **Disponibilidad de Aulas en MiPortalU**

### Objetivo del prototipo

Reemplazar los enlaces de `modulos/disponibilidadAulas/disponibilidad.php` por una pantalla que:

1. Use la **plantilla Julián** (header, lateral, clase, footer, FA, SweetAlert).  
2. Permita tipo (1/2/3), sede, fecha.  
3. Muestre disponibles / ocupados (mock JSON primero; Banner después).  
4. **No** tenga botón de reserva.  
5. Se vea moderna (mejor que Reservitas) **dentro** del portal.

### Capas a crear

| Capa | Archivo / lugar |
| --- | --- |
| Vista | `modulos/disponibilidadAulas/disponibilidad.php` (reescrito) |
| Clase | `gestionContenidos/clases/DisponibilidadAulas.php` |
| Assets | CSS/JS del módulo o `assets/...` |
| Datos | Mock → luego `oci_connect` TEST + `V_RESERVAS_SALON` |

### Orden de construcción en el lab

1. Analizar repo: includes, sesión, un módulo hermano, si ya hay Oracle.  
2. Prototipo UI con **datos mock** (para presentar aunque no haya user TEST).  
3. Enchufar Oracle cuando Manuel dé solo lectura.  
4. Exportar lista de archivos tocados para copiar luego a PPRD-IC.

### Fuera de alcance (no construir)

Equipos, KOHA, React SPA, escritura Banner, actualizar Reservitas.

---

## 4. Prompt para pegar en el Cursor del repo `miportalu-lab`

Copia tal cual en el **nuevo** chat (workspace = lab):

```text
Eres mi IDE/agente sobre el sandbox miportalu-lab (NO es GitLab UNAB).

Contexto del proyecto:
- Solo Disponibilidad de Aulas (id_tipo 1=salones, 2=informática, 3=auditorios).
- Consulta informativa; reservas de aula son Banner; equipos fuera (KOHA).
- Fuente objetivo: BANINST1.V_RESERVAS_SALON vía OCI8 SID TEST.
- Stack: plantilla Julián (header/lateral/clase/footer + Font Awesome + SweetAlert). No React SPA.
- Primero: prototipo presentable (mock OK). Luego conexión Banner.

Tareas ahora:
1) Explora el repo: estructura, disponibilidad.php, clases, cualquier oci_connect/conecora.
2) Resume en 10 líneas cómo arranca una página interna.
3) Propón e implementa el prototipo de Disponibilidad de Aulas (módulo + clase + CSS/JS) con datos mock realistas (códigos ED-…-AINF, bloques 06:00–22:00).
4) No pongas secretos en el código. No toques nada fuera del sandbox.

Bitácora previa (si la necesitas): en otro repo Python-Prep carpeta MiPortalU_DisponibilidadEspacios — reunión, day.php, mapa id_tipo, veredicto no-React.
```

---

## 5. Cómo “iniciamos de una” (orden de hoy)

| Orden | Quién | Acción |
| --- | --- | --- |
| 1 | Tú | Crear repo privado `miportalu-lab` en GitHub |
| 2 | Tú | Copiar portal a `D:\lab\miportalu-lab`, sanitizar claves |
| 3 | Tú | `git init` / push a GitHub |
| 4 | Tú | Cursor → Open Folder → esa carpeta (o Cloud Agent en ese repo) |
| 5 | Tú | Pegar el prompt de la sección 4 |
| 6 | Agente en lab | Explorar + armar prototipo |
| 7 | Tú | Mientras: armar slides/notas del lunes con hallazgos (sección 2) |

Cuando el lab esté en GitHub y abierto en Cursor, escribe ahí: **“ya estoy en miportalu-lab, empieza el prototipo”**.

---

## 6. Cursor como IDE — en corto

| Qué | Cómo |
| --- | --- |
| Editar código | Cursor abre la carpeta = IDE |
| Buscar en todo el portal | Agent + búsqueda del IDE |
| Crear módulo/clase | El agente escribe archivos en el lab |
| Probar en navegador | Tú: XAMPP apuntando a la carpeta lab (o copias el módulo al DocumentRoot local) |
| No dañar UNAB | El remote es solo tu GitHub privado |

No hace falta otro programa aparte: **Cursor = IDE + agente**. El navegador + XAMPP siguen siendo para ver la página.
