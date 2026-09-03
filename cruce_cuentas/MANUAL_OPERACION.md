# Manual de Operación — Portal Gestión de Cuentas Gmail (UNAB TIC)

## Para quién es este manual

Para la persona que **una vez al mes** (o cuando haya un corte nuevo de Google Admin) actualiza el portal. **No necesita saber programar.**

---

## Qué hay en el portal (3 piezas distintas)

| Pieza | Qué muestra | Cómo se actualiza |
|-------|-------------|-------------------|
| **Power BI** (depuración Gmail) | Inventario, activas, suspendidas, a bloquear, avance | El `.bat` genera 3 CSV → usted los sube a `etl/output` → Power BI **se refresca cada hora** |
| **Resumen 2FA** (HTML) | Cobertura por facultad, correos pendientes | El mismo `.bat` genera HTML y CSV → usted los sube a `etl/output` |
| **Listas SharePoint** | Meta del proyecto, acciones, seguimiento | **No las toca el `.bat`.** Se editan a mano en el portal cuando cambie la meta o registre un trabajo |

---

## Cómo funcionan las LISTAS (esto es lo que suele confundir)

Las listas **no son archivos**. Son tablas que viven en SharePoint (como un Excel en la nube). Power BI las lee **directo del sitio**, no de `etl/output`.

| Lista | ¿La actualiza el `.bat`? | Qué hacer usted |
|-------|--------------------------|-----------------|
| **MetaProyecto** | **No** | Cuando cambie la meta (licencias a depurar, fecha de corte, % objetivo), **edite la lista** en el portal. En la siguiente hora Power BI lo refleja. |
| **Acciones** | **No** | Cuando bloquee cuentas, envíe comunicados o cierre un lote, **agregue una fila** en Acciones. Es el diario de trabajo. |
| **capacidad / Cuentas / Dependencias** (listas) | **No** | Si están vacías o casi vacías, está bien. Los números del tablero salen de los **CSV** (`capacidad_powerbi.csv`, `cuentas_powerbi.csv`, `dependencias_powerbi.csv`) que sí genera el `.bat`. No duplique datos a mano en esas listas. |

**Resumen:** el script actualiza **archivos** (CSV + HTML). Las listas son el **cuaderno de metas y acciones** que las personas escriben. Power BI une ambos: archivos (inventario) + lista MetaProyecto (proyección).

---

## Actualización mensual (un solo doble clic)

### Carpeta INICIAL (insumos) — NO son los 35 de salida

En **una sola carpeta** de su PC ponga solo lo que sale de los sistemas:

| Archivo | Obligatorio | Para qué |
|---------|-------------|----------|
| `User_Download_….csv` (Google Admin, todas las cuentas) | **Sí** | Power BI **y** 2FA |
| CSV de inscritos / prematriculados (pueden ser varios) | **Sí** (solo 2FA) | Cruce por facultad |
| `VISTA DE CURRICULO.xlsx` | No | Catálogo de planes |

No mezcle ahí los archivos `*_powerbi.csv` ni el `resumen.html`. Eso es **salida**, no entrada.

### Paso 1 — Doble clic en `actualizar.bat`

Carpeta del proyecto:

```
...\Python-Prep\cruce_cuentas\actualizar.bat
```

1. Pegue la ruta de la carpeta del corte (barra del Explorador → Copiar).
2. Espere (Power BI + cruce 2FA, 1–3 minutos).
3. Se abre sola una carpeta en el **Escritorio**:

```
Escritorio\Archivos_SharePoint_2026-09-03\
```

Ahí van **6 archivos** (no 35). Cada día es una carpeta nueva para que no se mezclen cortes.

### Paso 2 — Subir a SharePoint

1. Abra `Documentos → etl → output`
2. Suba **solo estos 6**:
   - `cuentas_powerbi.csv`
   - `dependencias_powerbi.csv`
   - `capacidad_powerbi.csv`
   - `resumen.html`
   - `listado_sin_2fa.html`
   - `02_estudiantes_sin_2fa.csv`
3. **Reemplazar** si pregunta

No suba los `sin_2fa_facultad.csv` ni el `LEAME`. Los CSV por facultad se generan en el PC por si TIC los necesita; el portal usa **un** CSV de pendientes y se filtra en Excel.

### Paso 3 — Power BI (horario)

El dataset está conectado a `etl/output` y a las listas. Debe quedar con **actualización programada cada hora** en [app.powerbi.com](https://app.powerbi.com):

1. Workspace del proyecto → el **conjunto de datos** (no el informe)
2. **… → Configuración → Actualización programada**
3. Activar → frecuencia **Cada hora** (zona horaria Bogotá)
4. Guardar

Si acaba de subir archivos y no quiere esperar la hora: **Actualizar ahora**.

**No hace falta** Power BI Desktop ni republicar el `.pbix` si las fuentes ya apuntan a SharePoint.

---

## Qué archivos genera el `.bat`

**Los 6 que van a SharePoint** (`etl/output`):

- `cuentas_powerbi.csv`, `dependencias_powerbi.csv`, `capacidad_powerbi.csv`
- `resumen.html`, `listado_sin_2fa.html`, `02_estudiantes_sin_2fa.csv`

**El resto queda en el PC** (`cruce_cuentas\salida\`): universo, CSV por facultad, etc. No los suba.

---

## Dibujo del flujo

```
User_Download + inscritos (una carpeta)
        │
        ▼
  actualizar.bat  (doble clic)
        │
        ├─► procesar_powerbi.py  →  3 CSV del tablero
        ├─► cruzar.py            →  HTML + CSV 2FA
        └─► Escritorio\Archivos_SharePoint_AAAA-MM-DD
                    │
                    ▼  (usted arrastra)
              SharePoint etl/output
                    │
                    ├─► Power BI  (refresh cada hora)
                    └─► Botón Resumen 2FA

Listas MetaProyecto / Acciones  ──edición en el portal──► Power BI (misma hora)
```

---

## Si algo sale mal

| Problema | Qué hacer |
|----------|-----------|
| "No se encontró Python" | Instalar Python y marcar **Add Python to PATH** |
| "No hallé export Google" | El CSV debe llamarse `User_Download…` o ser el export de Admin |
| "No hallé CSV de inscritos" | Faltan los archivos de prematriculados/inscritos en esa carpeta |
| Power BI no cambia | Confirme que reemplazó los 3 `*_powerbi.csv` en `etl/output`. Pulse **Actualizar ahora**. Espere hasta 1 hora si está programado. |
| La meta del tablero no cambia | Edite la **lista MetaProyecto**, no un CSV. Luego refresh de Power BI. |
| 404 al descargar pendientes | Suba también `02_estudiantes_sin_2fa.csv` junto al HTML |
| No aparece la carpeta en Escritorio | Mire `Escritorio` o `Desktop`. El `.bat` abre la carpeta al terminar |

---

## Contacto

Estadísticas TIC — Dirección de TIC.
