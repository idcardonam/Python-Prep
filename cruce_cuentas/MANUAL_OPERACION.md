# Manual de operación
## Portal de gestión de cuentas Gmail institucionales
### Dirección de TIC · Estadísticas TIC · UNAB

Documento de uso para el área. Versión 2026-09.

---

## 1. Propósito

Este portal reúne en **un solo enlace** el seguimiento de cuentas Gmail institucionales:

- depuración de cuentas (inventario, bloqueos, inactividad);
- campaña de autenticación en dos pasos (2FA) de estudiantes vigentes;
- registro de meta del proyecto y de acciones realizadas.

No es necesario saber programar para consultar el portal ni para la actualización periódica de archivos.

**Dirección del portal**  
https://unabedu.sharepoint.com/sites/ProyectoDepuracinGmail/SitePages/CollabHome.aspx

El sitio SharePoint se llama **Proyecto Depuración Gmail**. Es un grupo privado: solo entra quien tenga permiso explícito.

---

## 2. Qué hay en el portal (tres piezas)

| Pieza | Qué se ve | Cómo se mantiene |
|-------|-----------|------------------|
| **Tablero Power BI** | Totales, estados de cuenta, avance | Tres archivos CSV en `etl/output` + listas. Power BI se actualiza **cada hora**. |
| **Resumen 2FA** | Cobertura por facultad y pendientes | Informe HTML y un CSV de pendientes en `etl/output`. |
| **Listas** | Meta del proyecto y bitácora de acciones | Se editan **en el propio sitio**, a mano. |

Las listas **no son archivos**. No se «suben». Se abren en el menú izquierdo (MetaProyecto, Acciones) y se editan como una tabla.

Los números del inventario **no** salen de las listas Cuentas / Dependencias / capacidad. Salen de los CSV `cuentas_powerbi.csv`, `dependencias_powerbi.csv` y `capacidad_powerbi.csv`.

---

## 3. Quién hace qué y cómo se da acceso

Hay dos perfiles. Se asignan en SharePoint, no en Power BI por separado (si el informe está incrustado en el sitio).

### 3.1 Consulta (revisar)

Puede abrir el portal, ver el tablero, el Resumen 2FA y las listas. **No** reemplaza archivos en `etl/output`.

**Cómo dar este acceso**

1. Entre al sitio **Proyecto Depuración Gmail**.
2. Arriba a la derecha: **engranaje** → **Permisos del sitio** (o **Información del sitio** → **Permisos**).
3. **Compartir sitio** (o **Invitar a personas**).
4. Escriba el correo institucional de la persona.
5. Nivel: **Lectura** (o grupo **Visitantes**).
6. Confirme. La persona recibe correo o verá el sitio en SharePoint.

También puede usar **Compartir** en la página de inicio y elegir **Puede ver**.

### 3.2 Operación (cargar archivos y editar listas)

Puede subir los seis archivos a `etl/output`, editar MetaProyecto y Acciones, y usar el procedimiento `actualizar.bat` en el equipo del área.

**Cómo dar este acceso**

1. Mismos pasos 1 a 4 de arriba.
2. Nivel: **Edición** (o grupo **Miembros**).
3. Confirme.

Quien opera **no** debe dejar `etl/input` abierto a todo el sitio: esa carpeta guarda CSV de origen. En la carpeta `input`: **…** → **Administrar acceso** → dejar solo al personal de operación.

### 3.3 Power BI

Si al abrir el tablero pide licencia o «no tiene permiso»:

1. En [app.powerbi.com](https://app.powerbi.com) abra el área de trabajo del informe.
2. **Acceso** (o Compartir informe).
3. Agregue el mismo correo, rol **Visor** (consulta) o **Colaborador** (si debe refrescar el conjunto de datos).

Quienes solo miran el portal suelen bastar con permiso de **lectura en SharePoint** más visor en el informe, si el informe está publicado en ese espacio.

---

## 4. Cómo consultar (uso diario)

1. Abra el enlace del portal (sección 1). Inicie sesión con la cuenta UNAB.
2. En la portada verá el **tablero de depuración**.
3. **Resumen 2FA**: abre el informe de estudiantes vigentes sin 2FA. Use facultad y programa para acotar. **Descargar CSV pendientes** abre un Excel; filtre la columna **facultad**.
4. **MetaProyecto**: consulte o ajuste la meta (solo con permiso de edición).
5. **Acciones**: consulte o registre lo ejecutado (bloqueos, comunicados, cierres de lote).

Si el tablero se ve desactualizado, espere el refresco horario o pida a quien opera **Actualizar ahora** en Power BI.

---

## 5. Actualización periódica de datos (quien opera)

Frecuencia sugerida: **cada vez que haya un corte nuevo** de Google Admin (típicamente mensual).

### 5.1 Qué reunir en UNA carpeta del PC (entrada)

Solo insumos de sistemas. **No** mezcle aquí los HTML ni los CSV `*_powerbi`.

| Archivo | Obligatorio | Origen |
|---------|-------------|--------|
| `User_Download_….csv` | Sí | Google Admin Console → informe de usuarios (todas las cuentas del dominio) |
| CSV de inscritos o prematriculados (uno o varios) | Sí | Extracto académico del periodo |
| `VISTA DE CURRICULO.xlsx` | No | Catálogo de planes |

El **mismo** `User_Download` sirve para el tablero de depuración y para el cruce 2FA.

### 5.2 Ejecutar el actualizador

1. En el equipo del área abra:  
   `Python-Prep\cruce_cuentas\actualizar.bat`  
   (doble clic).
2. Cuando pida la ruta: en el Explorador, abra la carpeta del punto 5.1, clic en la **barra de dirección**, copie (Ctrl+C) y pegue en la ventana azul. Enter.
3. Espere 1 a 3 minutos. Debe aparecer **LISTO**.
4. Se abre una carpeta en el escritorio:  
   `Archivos_SharePoint_AAAA-MM-DD`  
   (la fecha del día evita mezclar cortes).

### 5.3 Qué hay que cargar en SharePoint (solo seis archivos)

| Archivo | Función |
|---------|---------|
| `cuentas_powerbi.csv` | Tablero: detalle de cuentas |
| `dependencias_powerbi.csv` | Tablero: resumen por dependencia |
| `capacidad_powerbi.csv` | Tablero: licencias e inventario |
| `resumen.html` | Informe 2FA para consulta |
| `listado_sin_2fa.html` | Listado 2FA de trabajo |
| `02_estudiantes_sin_2fa.csv` | Descarga de pendientes |

**No suba** el archivo LEAME, ni los `sin_2fa_….csv` por facultad, ni `00_universo.csv`. Esos quedan en el PC, en `cruce_cuentas\salida\`.

### 5.4 Cómo cargar

1. En el sitio: **Documentos** → carpeta **etl** → **output**.
2. Seleccione los **seis** archivos de la carpeta del escritorio.
3. Arrástrelos a `output`.
4. Si pregunta **¿Reemplazar?**, elija **Reemplazar**.
5. Abra el portal y compruebe el Resumen 2FA (fecha del corte).
6. Power BI: se verá el corte en la **próxima hora**, o **Actualizar ahora** en el conjunto de datos (app.powerbi.com).

### 5.5 Power BI — programación cada hora (una sola vez)

1. Entre a https://app.powerbi.com con cuenta UNAB.
2. Área de trabajo del proyecto → el **conjunto de datos** (no el informe).
3. **…** → **Configuración** → **Actualización programada**.
4. Activar. Frecuencia: **Cada hora**. Zona: **Bogotá**.
5. Guardar.

No es necesario volver a publicar el archivo `.pbix` si las fuentes ya apuntan a SharePoint.

### 5.6 Error «Premium_ASWL_Error» / Workspace Identity (no refresca)

El tablero **no falla por los CSV**. Falla porque el conjunto de datos está autenticado con **identidad del área de trabajo (Workspace Identity)** y esa identidad **no existe** o quien publica el modelo **no tiene permiso de Colaborador** (o superior) en el área de trabajo.

**Camino rápido (recomendado para este portal):** usar cuenta organizacional, no identidad del área.

1. Entre a https://app.powerbi.com
2. Área de trabajo del informe → el **conjunto de datos** (modelo semántico) → **…** → **Configuración**
3. Abra **Credenciales del origen de datos**
4. En cada origen SharePoint (carpeta `etl/output` y listas): **Editar credenciales**
5. Método de autenticación: **OAuth2** o **Cuenta organizacional** (no «Identidad del área de trabajo»)
6. Inicie sesión con una cuenta institucional que **sí tenga acceso** al sitio Proyecto Depuración Gmail (edición o al menos lectura de `etl/output` y de las listas)
7. Nivel de privacidad: **Organizacional**
8. Guardar → **Actualizar ahora**

**Camino alternativo:** crear la identidad del área de trabajo.

1. Área de trabajo → **Configuración del área de trabajo** → **Identidad del área de trabajo** → **Crear**
2. Dé a esa identidad acceso al sitio SharePoint (al menos lectura en `etl/output` y listas)
3. Quien es **propietario del modelo** debe ser **Colaborador** o superior en el área de trabajo de Power BI
4. **Actualizar ahora**

Si el área de trabajo no es de capacidad Fabric/Premium, el primer camino (OAuth2) es el adecuado.

---

## 6. Listas: MetaProyecto y Acciones

| Lista | Para qué | Quién la cambia |
|-------|----------|-----------------|
| **MetaProyecto** | Meta de depuración, fechas, proyección | Quien define la meta del periodo |
| **Acciones** | Bitácora (qué se hizo, cuándo) | Quien ejecuta la operación |

**Para editar:** menú izquierdo → nombre de la lista → **Editar** o **+ Nuevo**. En minutos u hora, Power BI lo toma.

Si cambia la meta y el tablero no se mueve, no regenere CSV: edite la lista y refresque Power BI.

---

## 7. Flujo resumido

```
Carpeta del corte (Google Admin + inscritos)
        →  doble clic en actualizar.bat
        →  Escritorio\Archivos_SharePoint_fecha  (6 archivos)
        →  arrastrar a SharePoint  etl / output
        →  tablero (cada hora)  y  botón Resumen 2FA

Listas MetaProyecto / Acciones  →  se editan en el sitio  →  mismo refresco horario
```

---

## 8. Incidencias frecuentes

| Qué ocurre | Qué hacer |
|------------|-----------|
| «No se encontró Python» | Instalar Python desde python.org y marcar **Add Python to PATH**. |
| «No hallé export Google» | El archivo debe ser el de Admin (`User_Download…`) y estar en la carpeta que pegó. |
| «No hallé CSV de inscritos» | Faltan los archivos académicos en esa misma carpeta. |
| El tablero no cambia | Confirme que reemplazó los tres `*_powerbi.csv`. Pulse **Actualizar ahora**. |
| Error Premium_ASWL / Workspace Identity | Apartado 5.6: cambiar credenciales a cuenta organizacional (OAuth2). |
| La meta no cambia | Edite **MetaProyecto**, no un CSV. |
| 404 al descargar pendientes | Falta `02_estudiantes_sin_2fa.csv` en `etl/output`, junto al HTML. |
| No aparece la carpeta en el escritorio | Busque `Escritorio` o `Desktop`. El actualizador la abre al terminar. |
| «No tiene acceso» al sitio | Pedir inclusión con **lectura** o **edición** (sección 3). |
| El HTML 2FA se ve raro | Ábralo en **pestaña nueva**, no solo en la vista previa de SharePoint. |

---

## 9. Datos personales

Los CSV de origen y el universo de cuentas contienen información sensible. Trabaje en el equipo del área. No publique `etl/input` ni `00_universo.csv` en el portal de consulta. No envíe listados de correos por canales no institucionales.

---

## 10. Soporte

Estadísticas TIC — Dirección de TIC  
Universidad Autónoma de Bucaramanga
