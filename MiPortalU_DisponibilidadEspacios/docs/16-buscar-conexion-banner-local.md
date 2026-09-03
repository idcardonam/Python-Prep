# Buscar en tu MiPortalU local cómo se conecta a Banner

En este Cloud Agent **no está** el repo del portal. Tú sí lo tienes en el disco (XAMPP / `D:\repositorio\...`). Corre esto **allá** y pégame los resultados (claves tachadas).

## 1. Abrir PowerShell o CMD en la raíz de MiPortalU

Ejemplo:

```bat
cd /d D:\repositorio\portal
```

(Ajusta la ruta a donde Julián te dejó el clone.)

## 2. Buscar conexión Oracle / Banner

### Opción A — si tienes `rg` (ripgrep) o VS Code

En VS Code: `Ctrl+Shift+F` y busca una por una:

```text
oci_connect
oci_parse
oci_execute
NEW PDO
PDO(
Conec_ora
conecora
conexion_ora
oracle
BANINST1
V_RESERVAS
TNS
EZCONNECT
```

Incluye carpeta `gestionContenidos` y `include`.

### Opción B — PowerShell (sin instalar nada)

```powershell
cd D:\repositorio\portal

Get-ChildItem -Recurse -Include *.php,*.inc -ErrorAction SilentlyContinue |
  Select-String -Pattern 'oci_connect|oci_parse|Conec_ora|conecora|BANINST1|V_RESERVAS|PDO.*OCI|oracle' |
  Select-Object -First 40 Path, LineNumber, Line
```

### Opción C — CMD con findstr

```bat
cd /d D:\repositorio\portal
findstr /s /i /n "oci_connect oci_parse Conec_ora conecora BANINST1 V_RESERVAS" *.php *.inc
```

## 3. Archivos típicos a abrir si salen en la lista

| Nombre posible | Por qué |
| --- | --- |
| `conecora.php` / `conexionOracle.php` / `oracle.php` | Conexión Banner |
| `conec.php` | Ojo: a veces es MySQL del **portal**, no de Reservitas |
| Algo en `gestionContenidos/clases/` | Clase que ya consulta Banner |
| `test_conexion.php` **del portal** (no el de Reservitas) | Prueba oficial |

El `test_conexion.php` de Reservitas (`mrbs_room` + mysqli) **no** es este.

## 4. Qué pegarme aquí

De cada hallazgo:

1. **Ruta del archivo** (ej. `gestionContenidos/clases/Foo.php`).
2. **10–30 líneas** de la función de conexión / query (usuario, host, password → `***`).
3. Si ves `BANINST1.` o nombre de vista, anótalo.

Con eso vemos el patrón real y armamos `DisponibilidadAulas` igual.

## 5. Si no aparece nada de Oracle

Anótalo: “no hay oci_ en el clone”. Entonces la conexión Banner puede estar:

- solo en el servidor (archivo fuera de Git), o
- en un include que Julián te pasó aparte (`home`, etc.).

En ese caso la pregunta a Julián/Manuel es directa:

> En el clone local no encuentro `oci_connect`. ¿Dónde está la conexión a Banner TEST del portal?
