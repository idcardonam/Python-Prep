# Sandbox MiPortalU — sí, es buena idea

## Veredicto

**Sí.** Es la mejor forma de avanzar sin dañar lo que te entregaron en el GitLab UNAB, y de no mezclar este trabajo con el repo Python-Prep / este chat eterno.

| Objetivo | Cómo lo cubre el sandbox |
| --- | --- |
| No tocar Git UNAB | Copia local → repo **privado** tuyo (o de laboratorio) |
| Que Cursor analice el código de verdad | El Cloud Agent / Cursor abre **ese** repo como workspace |
| Probar cómo quedará Disponibilidad | Prototipo ahí; luego llevas el diff limpio al portal oficial con Julián |
| Reutilizar en cada proyecto nuevo | Ese repo (o un fork/rama `lab/plantilla`) queda como base |
| Responder “¿hay oci_connect en el portal?” sin preguntar aún | Buscando en la copia |

## Qué NO es

- No es reemplazar producción.
- No es subir claves, LDAP passwords, ni el Reservitas ofuscado/infectado.
- No es pelear con la rama PPRD-IC del GitLab UNAB mientras prototipamos.

## Cómo armarlo (tú en el PC)

### 1. Crear repo privado nuevo en GitHub

Nombre sugerido: `miportalu-lab` o `miportalu-sandbox-ivan`.

Privado. Solo tú (y Cursor Cloud si lo vinculas).

### 2. Copiar el portal local **sanitizado**

Desde la carpeta que te configuró Julián:

1. Copia completa a otra carpeta, ej. `D:\lab\miportalu-lab`.
2. **Antes de subir**, limpia:
   - `conecora.php` / configs: usuario y clave → `""` o variables de entorno.
   - Borra o no subas logs, `error_log.log`, dumps.
   - No metas el Reservitas ofuscado dentro de este repo.
3. Añade `.gitignore`:

```gitignore
# secretos
**/conec*.php.local
**/*password*
**/.env
**/error_log.log
*.log

# basura local
.DS_Store
Thumbs.db
```

Opcional: deja `conecora.php` con TNS TEST pero **sin** clave; un `conecora.local.php` en gitignore con tus pruebas.

### 3. Primer commit y push

```bat
cd /d D:\lab\miportalu-lab
git init
git add .
git commit -m "Sandbox local MiPortalU para laboratorio (sin secretos)"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/miportalu-lab.git
git push -u origin main
```

### 4. Abrir en Cursor (importante)

- **Nuevo** agente / ventana Cursor sobre `miportalu-lab`, no sobre `Python-Prep`.
- Ahí pedimos: “analiza conexión Banner, arma módulo Disponibilidad de Aulas de cero con plantilla Julián”.
- Este chat / Python-Prep queda como **bitácora de exploración**; el desarrollo del prototipo vive en el lab.

### 5. Flujo sano con la UNAB

```text
Sandbox (GitHub privado + Cursor)
        │  prototipo, UI, clase, pruebas
        ▼
Diff limpio (solo archivos del módulo + clase)
        │
        ▼
Clone oficial UNAB (rama PPRD-IC) — copiar a mano / cherry-pick
        │
        ▼
Avisar a Julián → push GitLab UNAB → PPRD
```

Así **nunca** “empujas” el sandbox al GitLab de la universidad.

## Qué vamos a poder hacer en el lab

1. Buscar de verdad `oci_connect`, clases, módulos hermanos.
2. Reemplazar `disponibilidad.php` (enlaces) por UI nueva + clase.
3. Mockear Banner si aún no hay user TEST (JSON de ocupación) y luego enchufar OCI.
4. Presentar el lunes: “así quedaría” con capturas/demo local.
5. En el próximo proyecto: clonar el lab / crear rama `proyecto-xyz` y repetir.

## Relación con lo ya hecho

El paquete `MiPortalU_DisponibilidadEspacios/` en Python-Prep es la **memoria** (reunión, guía, day.php, V_RESERVAS_SALON, 4 capas, no React SPA).  
Cuando abras el lab, el primer mensaje puede ser: “lee el contexto del Drive/docs y construye sobre el portal real”.

## Riesgos y cómo evitarlos

| Riesgo | Mitigación |
| --- | --- |
| Subir passwords al GitHub | Sanitizar; repo privado; rotar si ya se pegaron en chat |
| Confundir lab con oficial | README grande: “SANDBOX — no es GitLab UNAB” |
| Repo público por error | Crear como **Private** |
| Meter malware de Reservitas | Reservitas fuera; solo referencia de negocio |

## Respuesta directa a “¿te parece?”

Sí. Es lo correcto para innovar, presentar y no romper nada.  
Siguiente acción tuya: **crear `miportalu-lab` privado, subir la copia sanitizada, abrir ese repo en Cursor**. Cuando esté, seguimos ahí el prototipo de Disponibilidad de Aulas.
