# Mensaje para enviar (copiar y pegar)

**Para:** (los dos ingenieros del área)  
**Asunto:** Portal unificado de gestión de cuentas Gmail institucionales — entrega de operación

---

Ingenieros:

Les comparto el **portal único** de gestión de cuentas Gmail institucionales, pensado para consulta, seguimiento y actualización periódica desde un mismo sitio SharePoint.

**Enlace del portal**  
https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/SitePages/CollabHome.aspx

---

### Qué quedó funcionando

El sitio concentra tres piezas que antes estaban separadas:

1. **Tablero Power BI (depuración de cuentas)**  
   Inventario, cuentas activas, suspendidas, candidatas a bloqueo y avance. Los datos salen de tres archivos CSV publicados en `Documentos / etl / output` y de las listas del sitio. El conjunto de datos debe refrescarse **cada hora**.

2. **Informe 2FA (estudiantes vigentes)**  
   Cruce del export de Google Admin con los CSV académicos. El botón **Resumen 2FA** abre el informe: cifras, ranking por facultad y listado de pendientes. La descarga de correos es un CSV único (`02_estudiantes_sin_2fa.csv`) que se filtra por facultad en Excel.

3. **Seguimiento en listas**  
   **MetaProyecto** (meta, fechas, proyección) y **Acciones** (registro de trabajo). Se editan en el portal; no las genera el proceso automático. En el siguiente refresco de Power BI se reflejan.

---

### Cómo se actualiza (operación)

Un solo procedimiento en el PC del área:

1. Se reúnen en **una carpeta** el `User_Download` de Google Admin, los CSV de inscritos y, si aplica, Vista de currículo.  
2. Doble clic en `actualizar.bat`.  
3. El proceso genera los CSV del tablero y el informe 2FA.  
4. En el escritorio aparece `Archivos_SharePoint_AAAA-MM-DD` con **seis archivos**.  
5. Esos seis se arrastran a SharePoint → `etl / output` (reemplazar).  

El mismo archivo de Google Admin alimenta **depuración y 2FA**, para no duplicar cortes.

El detalle paso a paso, permisos y solución de incidencias está en el **Manual de operación** (PDF adjunto).

---

### Acceso

Quienes **consultan** el tablero y el informe: permiso de **lectura** en el sitio.  
Quienes **actualizan archivos o listas**: permiso de **edición** (miembros del sitio).  
La carpeta `etl / input` debe quedar restringida al personal que opera los CSV de origen.

Quedo atento para asignar permisos y resolver cualquier duda de uso.

Cordialmente,  
[Nombre]  
Estadísticas TIC — Dirección de TIC  
Universidad Autónoma de Bucaramanga
