# Cruce de cuentas institucionales (Google × académico)

Herramienta local para TIC: cruza el CSV de **Admin Console** con el extracto **académico** (todos los estados **excepto graduados**) y arma una **ficha por correo** `@unab.edu.co`.

Sirve para **2FA** y también para operación: facultad, programa, sección, cuentas huérfanas, posibles egresados con correo activo, académico sin cuenta Google.

**No subas CSV reales a Git.** Corre en tu PC. Los archivos de `entrada/` (salvo `_ejemplos`) están ignorados.

## Idea (spine de identidad)

Cada correo es una ficha con tres capas:

1. **Google** — estado de cuenta, OU, último ingreso, 2FA inscrito / forzado  
2. **Académico** — estado, facultad, programa, sección, jornada, código… (todas las columnas del CSV)  
3. **Personal (opcional)** — docentes/administrativos **no salen** en estados académicos; si GH te da un CSV, el cruce deja de mezclarlos con “huérfanos”

```
Google Admin (todas las cuentas @unab.edu.co)
        │
        ├─ match correo ─► ESTUDIANTE_VIGENTE  (+ facultad/programa/sección)
        │
        ├─ match CSV GH ─► PERSONAL (docente / administrativo)
        │
        └─ sin match ────► POSIBLE_PERSONAL_POR_OU
                           POSIBLE_EGRESADO_CON_CUENTA
                           GOOGLE_SIN_MATCH_ACADEMICO
```

Los **graduados no vienen** en el académico: si siguen en Google, caen en “sin match”. Eso es útil: no son “estudiantes vigentes”; hay que decidir si deshabilitar, archivar o dejar con 2FA.

## Qué pedir (mínimo)

### A) Google Admin
Informe de usuarios (`User_Download_…csv` de Admin Console) con al menos:
- Email Address  
- Status  
- Last Sign In  
- **2sv Enrolled** (o *2-Step Verification Enrollment Status*) — esto es el 2FA **inscrito**  
- Org Unit Path y Enforcement, si el informe los trae (el export corto de Users a veces **no** incluye OU)

Si el CSV de Google está **en la misma carpeta** que los inscritos, `--academico-dir` lo omite (nombre `User_Download*` o encabezados de Admin). Puedes apuntar `--google` a esa ruta sin copiar el archivo.

```bash
python3 cruzar.py --google "…/User_Download_01092026_140316.csv" --academico-dir "…/REPORTE_INSCRITOS 2026" --salida salida
```

### B) Académico (varios CSV)
Si tienes una carpeta tipo `REPORTE_INSCRITOS 2026` con muchos archivos:

```bash
python3 cruzar.py --inspeccionar "D:\Users\...\REPORTE_INSCRITOS 2026"
```

Eso solo lista **encabezados y conteos** (no imprime correos). Luego el cruce:

```bash
python3 cruzar.py --google entrada/google_admin.csv --academico-dir "D:\Users\...\REPORTE_INSCRITOS 2026"
```

Une los CSV, guarda el periodo (ej. `202610`) y si un correo aparece en varios programas los concatena con ` | `. El detalle fila a fila queda en `08_academico_filas.csv`.

### C) Recomendado (personal GH)
CSV de **GH / nómina**: correo, tipo (docente/admin), área, sección, cargo.  
Sin esto, docentes y administrativos quedan mezclados con egresados y cuentas huérfanas.

### D) Vista de currículo (catálogo de planes)
`VISTA DE CURRICULO.xlsx` (o csv) en la misma carpeta. No son estudiantes: oferta de programas en el tiempo.

En el Excel UNAB: `TERM_EFF` suele ser el mismo para todas las filas; el periodo que cambia es **`TERM`**. El cruce toma el **último TERM** por escuela+programa+major.

```bash
py -3 -m pip install openpyxl
cd cruce_cuentas
py -3 cruzar.py --inspeccionar "D:\Users\...\REPORTE_INSCRITOS 2026"
py -3 cruzar.py --carpeta "D:\Users\...\REPORTE_INSCRITOS 2026" --salida .\salida
```

`--carpeta` busca solo: el Google más reciente (`User_Download*`), los Prematriculados, y la Vista de currículo. Cada corte académico: reemplazas esos archivos y vuelves a correr. El HTML **no se actualiza solo**; se regenera en `salida\resumen.html`.


## Cómo correr

```bash
cd cruce_cuentas
python3 cruzar.py --ejemplo
```

Con tus archivos:

```bash
python3 cruzar.py \
  --google entrada/google_admin.csv \
  --academico entrada/academico.csv \
  --personal entrada/personal.csv \
  --salida salida
```

Detecta columnas en español o inglés. Si un nombre no pega, copia `config.example.yaml` → `config.yaml` (el mapeo fino sigue por alias en el script).

## Salidas

| Archivo | Para qué |
|---------|----------|
| `00_universo.csv` | Ficha completa de cada correo |
| `01_sin_2fa.csv` | Todas las cuentas Google sin 2FA |
| `02_estudiantes_sin_2fa.csv` | Vigentes académicos sin 2FA (acción por facultad/sección) |
| `03_google_sin_match_academico.csv` | Personal + posibles egresados + huérfanas |
| `04_academico_sin_cuenta_google.csv` | Deberían tener cuenta y no están en Admin |
| `05_prioridad_alta_2fa.csv` | Personal o estudiantes activos sin 2FA |
| `06_cobertura_2fa_facultad.csv` | % 2FA por facultad |
| `07_cobertura_2fa_programa_seccion.csv` | % 2FA por programa y sección |
| `08_academico_filas.csv` | Una fila por inscripción (detalle) |
| `09_catalogo_planes_vigentes.csv` | Un plan vigente por programa (último periodo) |
| `10_cobertura_2fa_plan_vigente.csv` | % 2FA por programa con plan vigente |
| `resumen.html` / `resumen.json` | Tablero: acción estudiantes vs radar dominio |

## Prioridades 2FA

- `ALTA_PERSONAL_SIN_2FA` — staff (más riesgo operativo)  
- `ALTA_ESTUDIANTE_ACTIVO_SIN_2FA` — match académico y cuenta en uso  
- `MEDIA_*` — inactivas (90 días sin ingreso, configurable)  
- `REVISAR_EGRESO_Y_2FA` — posible graduado con cuenta aún viva  
- `OK` — ya tiene 2FA  

## Cuidado con datos

- Trabaja en carpeta local, no en OneDrive público ni en este repo.  
- No pegues CSV con cédulas en chats de IA.  
- Entrega a jefes: hojas de cobertura + listados sin columnas de más.

## Qué más se puede hacer con el mismo cruce

- Campaña 2FA por **facultad / sección** (correo masivo dirigido).  
- Cuentas Google **suspendidas** vs estado académico.  
- Académico vigente **sin** cuenta (provisioning).  
- OU de Google **≠** facultad del académico (datos sucios).  
- Inactividad + sin 2FA = apagar o forzar reset.  
- Segunda corrida el próximo mes: comparar `00_universo.csv` y ver avance de cobertura.
