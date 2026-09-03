# Manual de Operación — Portal Gestión de Cuentas Gmail

## Para quién es este manual

Para la persona encargada de actualizar mensualmente los informes de 2FA y depuración de cuentas Gmail en el portal SharePoint de TIC-UNAB.

**No necesita saber programar.** Solo seguir estos pasos una vez al mes.

---

## Qué hay en el portal

| Módulo | Qué muestra | Cómo se actualiza |
|--------|------------|-------------------|
| Panel depuración Gmail | Inventario, suspensiones, bloqueos (Power BI) | Se actualiza solo desde Power BI |
| Resumen 2FA | Cobertura por facultad, ranking, correos pendientes | **Usted lo actualiza** con este manual |
| Listas (MetaProyecto, Acciones) | Seguimiento del proyecto | Se editan directamente en SharePoint |

---

## Actualización mensual del Resumen 2FA

### Qué necesita antes de empezar

1. El archivo de **Google Admin Console** (CSV de usuarios)
2. La carpeta de **inscritos** del periodo (CSV del sistema académico)
3. (Opcional) VISTA DE CURRICULO.xlsx

Ponga los tres en **una sola carpeta** en su PC. Ejemplo:

```
D:\Datos_Cruce_Septiembre\
├── User_Download_01092026.csv     ← Google Admin
├── PREMATRIC_FAC_INGENIERIA.csv   ← Inscritos
├── PREMATRIC_FAC_SALUD.csv        ← Inscritos
├── PREMATRIC_FAC_ECONOMIA.csv     ← Inscritos
└── VISTA DE CURRICULO.xlsx        ← Opcional
```

### Paso 1 — Ejecutar el actualizador (doble clic)

1. Abra el **Explorador de Windows**
2. Navegue a la carpeta del proyecto:
   ```
   D:\Users\N00033120\Documents\CURSOR UNAB\UNAB\Python-Prep\cruce_cuentas
   ```
3. Haga **doble clic** en **`actualizar.bat`**
4. Se abre una ventana azul que le pide la ruta de los datos
5. Vaya a la carpeta donde tiene los CSV (paso anterior)
6. Haga **clic en la barra de dirección** del Explorador (arriba, donde dice la ruta)
7. **Copie** la ruta (Ctrl+C)
8. **Vuelva** a la ventana azul y **pegue** (clic derecho → Pegar, o Ctrl+V)
9. Presione **Enter**
10. Espere a que termine (30 segundos aprox.)

Si todo salió bien, verá:

```
[LISTO] Informes generados en la carpeta "salida"
```

Y se abrirá automáticamente la carpeta con los archivos generados.

### Paso 2 — Subir a SharePoint (arrastrar archivos)

1. Al presionar una tecla, se abre **SharePoint** en la carpeta `etl/output`
2. **Seleccione todos los archivos** de la carpeta `salida` (Ctrl+A)
3. **Arrástrelos** a la ventana de SharePoint
4. Cuando pregunte "¿Reemplazar?": haga clic en **Reemplazar**

### Paso 3 — Verificar

1. Abra el portal: [Gestión de Cuentas Gmail](https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/SitePages/CollabHome.aspx)
2. Haga clic en **Resumen 2FA**
3. Verifique que la fecha del corte sea la actual
4. Elija una facultad y confirme que se ven los correos

**Listo.** No hay más pasos.

---

## Resumen visual

```
┌──────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│  1. DESCARGAR CSV    │     │  2. DOBLE CLIC en    │     │  3. ARRASTRAR a    │
│                      │     │     actualizar.bat    │     │     SharePoint     │
│  Google Admin +      │ ──► │                      │ ──► │                    │
│  Inscritos del mes   │     │  Pegar ruta, Enter   │     │  etl/output        │
│  (en una carpeta)    │     │  Esperar 30 seg      │     │  (reemplazar)      │
└──────────────────────┘     └──────────────────────┘     └────────────────────┘
```

Tiempo total: **5 minutos**.

---

## Si algo sale mal

| Problema | Solución |
|----------|----------|
| "No se encontró Python" | Instale Python desde python.org. Marque **"Add Python to PATH"** |
| "No hallé export Google" | Verifique que el archivo `User_Download_*.csv` esté en la carpeta |
| "No hallé CSV de inscritos" | Verifique que hay al menos un CSV de inscritos en la carpeta |
| "La carpeta no existe" | Copie la ruta correctamente desde la barra del Explorador |
| El HTML no muestra datos nuevos | Limpie la caché del navegador (Ctrl+Shift+R) |
| El botón "Descargar facultad" no funciona | Abra el HTML en pestaña nueva (clic derecho → Abrir en nueva pestaña) |

---

## Archivos del proyecto (no mover ni borrar)

```
cruce_cuentas/
├── actualizar.bat        ← DOBLE CLIC AQUÍ para actualizar
├── cruzar.py             ← Script (no tocar)
├── config.example.yaml   ← Configuración (no tocar)
├── requirements.txt      ← Dependencias (no tocar)
├── MANUAL_OPERACION.md   ← Este manual
├── entrada/
│   └── _ejemplos/        ← Datos de prueba (no tocar)
└── salida/               ← Aquí se generan los informes
    ├── resumen.html
    ├── listado_sin_2fa.html
    └── (otros CSV)
```

---

## Contacto

Si tiene dudas o el script falla, contacte a **Estadísticas TIC**.
