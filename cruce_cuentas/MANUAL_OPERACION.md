# Manual de Operación — Portal Gestión de Cuentas Gmail · UNAB

## Qué es este portal

Un solo sitio en SharePoint donde se consolidan:

1. **Depuración de cuentas Gmail** — tablero Power BI con inventario, suspensiones, bloqueos y avance.
2. **Campaña 2FA** — informe interactivo por facultad generado con `cruzar.py`.
3. **Seguimiento** — listas MetaProyecto y Acciones incrustadas en la portada.

URL del portal:
```
https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/SitePages/CollabHome.aspx
```

---

## Estructura de archivos en SharePoint

```
Documentos/
└── etl/
    ├── input/   ← CSV crudos (solo TIC, restringido)
    │   ├── User_Download_DDMMAAAA.csv   (Google Admin)
    │   ├── REPORTE_INSCRITOS 2026/      (extracto académico)
    │   ├── personal.csv                 (nómina GH, opcional)
    │   └── VISTA DE CURRICULO.xlsx      (catálogo, opcional)
    │
    └── output/  ← Informes para compartir (lectura para todos)
        ├── resumen.html          ← Jefatura: cifras + ranking + correos
        ├── listado_sin_2fa.html  ← Operativo: buscador de correos
        ├── 02_estudiantes_sin_2fa.csv
        ├── 06_cobertura_2fa_facultad.csv
        └── (otros CSV de cobertura)
```

---

## Cómo actualizar los datos (paso a paso)

### Frecuencia recomendada
- **Mensual** o cuando haya un nuevo corte de inscritos/Admin Console.

### Paso 1 — Descargar los CSV frescos

| Fuente | Qué descargar | Dónde guardarlo |
|--------|--------------|-----------------|
| Google Admin Console | Informe de usuarios → Exportar CSV | `entrada/google_admin.csv` (o `User_Download_…csv`) |
| Banner / sistema académico | Extracto de inscritos vigentes (todos excepto graduados) | Carpeta `entrada/REPORTE_INSCRITOS 2026/` |
| GH / Nómina (opcional) | CSV de personal: correo, tipo, área | `entrada/personal.csv` |
| Banner (opcional) | VISTA DE CURRICULO.xlsx | Misma carpeta de inscritos |

### Paso 2 — Ejecutar el cruce en tu PC

Abre terminal (CMD o PowerShell) en la carpeta `cruce_cuentas`:

```powershell
cd "D:\Users\N00033120\Documents\CURSOR UNAB\UNAB\Python-Prep\cruce_cuentas"
```

**Opción A — Carpeta con todos los archivos juntos:**
```powershell
py -3 cruzar.py --carpeta "D:\Users\...\REPORTE_INSCRITOS 2026" --salida .\salida
```

**Opción B — Archivos separados:**
```powershell
py -3 cruzar.py --google entrada\google_admin.csv --academico-dir "D:\Users\...\REPORTE_INSCRITOS 2026" --salida .\salida
```

Espera a que termine. Verás:
```
✓ resumen.html generado
✓ listado_sin_2fa.html generado
✓ 12 archivos en salida/
```

### Paso 3 — Subir a SharePoint

1. Abre **Documentos → etl → output** en el navegador
2. Selecciona los archivos de tu carpeta `salida/`:
   - `resumen.html`
   - `listado_sin_2fa.html`
   - `02_estudiantes_sin_2fa.csv`
   - (y los demás CSV que quieras)
3. Arrastra al navegador o usa **Crear o cargar → Archivos**
4. Cuando pregunte "¿Reemplazar?": **Sí, reemplazar**

**El botón "Resumen 2FA" del portal sigue funcionando** porque apunta a la misma URL. Solo cambia el contenido del archivo.

### Paso 4 — Verificar

1. Abre el portal
2. Clic en **Resumen 2FA**
3. Confirma que las cifras corresponden al corte nuevo
4. Prueba el buscador y el botón "Descargar esta facultad"

---

## Cómo abrir el HTML correctamente en SharePoint

**Importante:** SharePoint por defecto abre los `.html` en modo "vista previa" (iframe), lo que puede bloquear algunas funciones (descarga de CSV, buscador).

### Solución: abrir en pestaña nueva
- Clic derecho en `resumen.html` → **Abrir en una pestaña nueva**
- O desde el portal: configura el botón "Resumen 2FA" con la opción **"Abrir en una pestaña nueva"**

### Alternativa: cambiar comportamiento de la biblioteca
1. Ve a **Documentos → etl → output**
2. **⚙️** → **Configuración de biblioteca** → **Configuración avanzada**
3. "Abrir documentos en el explorador" → **Abrir en el cliente** o **Abrir en una pestaña nueva**

---

## Listas de seguimiento

| Lista | Para qué | Quién edita |
|-------|----------|-------------|
| **MetaProyecto** | Meta de cuentas, % avance, objetivo | TIC / Jefatura |
| **Acciones** | Registro de acciones ejecutadas | TIC |
| **Cuentas** | Detalle de cuentas específicas | TIC |
| **Dependencias** | Dependencias con otras áreas | TIC |
| **capacidad** | Capacidad operativa | TIC |

Se editan directamente en SharePoint (clic en la lista → editar fila). No requieren script ni carga de archivos.

---

## Permisos

| Rol | Acceso |
|-----|--------|
| TIC (operador) | **Control total** — edita listas, sube CSV, corre el script |
| Jefatura | **Lectura** — ve portal, Power BI, HTML, listas |
| Compañeros | **Lectura** — lo que jefatura defina compartir |

**ETL/input está restringido** — solo TIC. Los CSV crudos con datos personales no son visibles para jefatura.

---

## Resumen rápido de actualización

```
1. Descarga CSV frescos (Google Admin + inscritos)
2. Corre:  py -3 cruzar.py --carpeta "..." --salida .\salida
3. Sube salida/ a SharePoint → etl/output (reemplazar)
4. Verifica en el portal
```

Tiempo estimado: **10–15 minutos** por corte.

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| El botón "Descargar esta facultad" no funciona | Abrir el HTML en pestaña nueva (clic derecho → nueva pestaña), no en la vista previa de SharePoint |
| El HTML se ve en blanco | SharePoint lo abrió en iframe. Abrir en pestaña nueva |
| "No hay correos para descargar" | Primero elija una facultad en la lista desplegable |
| El script falla al correr | Verifica que `py -3` funciona. Si no: `python3` o `python`. Instala dependencias: `py -3 -m pip install -r requirements.txt` |
| Los CSV tienen caracteres raros | Abrir en Excel → Datos → Desde texto/CSV → Codificación UTF-8 |
| Power BI no carga | Verificar que la cuenta tiene licencia Power BI y acceso al dataset |
