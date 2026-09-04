# Conexión Oracle encontrada — `conecora.php` (Reservitas / referencia)

Fuente: archivo que Iván pegó (3 sep 2026). **No versionar claves.** En el pegado original había passwords en bloques comentados de PROD: **no reenviarlas**; avisar a Manuel que roten si circuló el backup.

## Qué es

Función `Conec_ora()` con extensión **OCI8** (`oci_connect`). Es el puente a **Banner Oracle**.

## Ambiente activo en ese archivo

| Parámetro | Valor (no secreto) |
| --- | --- |
| Host | `172.16.20.38` |
| Puerto | `1521` |
| SID | **`TEST`** |
| Usuario / clave | En el archivo actual van vacíos `""` — hay que llenarlos con el user de **solo lectura** que dé Manuel (no pegar aquí) |
| API | `oci_connect($usuario, $clave, $tnsname)` |

TNS (forma):

```text
(DESCRIPTION =
  (ADDRESS = (PROTOCOL = TCP)(HOST = 172.16.20.38)(PORT = 1521))
  (CONNECT_DATA = (SID = TEST)))
```

Había otro TNS comentado hacia **PROD** (`SID = PROD`, otro host). **MiPortalU / este proyecto solo TEST.**

## Patrón de código (sanitizado)

```php
function Conec_ora() {
    $usuario = ""; // ← user TEST solo lectura (Manuel)
    $clave   = ""; // ← nunca en Git ni en chat
    $tnsname = "(DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = 172.16.20.38)(PORT = 1521))
        (CONNECT_DATA = (SID = TEST)))";

    $link_ora = oci_connect($usuario, $clave, $tnsname);
    if (!$link_ora) {
        $error = oci_error();
        error_log("Error de conexión: " . $error['message'], 3, "error_log.log");
        die("Error conectando a la base de datos.");
    }
    return $link_ora;
}
```

## Cómo encaja con MiPortalU

1. **No copies** `conecora.php` de Reservitas al portal tal cual (es de otro sistema y trae historial sucio de claves).
2. En MiPortalU, en la **clase** `DisponibilidadAulas` (o un include del portal que Julián indique), usa el **mismo esquema**: `oci_connect` + TNS TEST.
3. Pregunta a Julián:  
   > ¿El portal ya tiene un `Conec_ora` / include Oracle? Si sí, lo reutilizo. Si no, ¿lo creo en `gestionContenidos` solo para lectura TEST?
4. Con `$link_ora` haces `oci_parse` / `oci_execute` sobre `BANINST1.V_RESERVAS_SALON`.

## Checklist local de Iván

- [ ] PHP del XAMPP tiene extensión **oci8** cargada (Julián lo configuró con Instant Client).
- [ ] Pedir a Manuel usuario TEST **solo SELECT** (no el user `reserva` de escritura/legado).
- [ ] Probar en un `test` del portal: conectar y `SELECT * FROM BANINST1.V_RESERVAS_SALON WHERE ROWNUM <= 5`.
- [ ] No subir claves a GitLab.

## Impacto en el lunes

Ya no es misterio el “cómo se conectan a Banner”: **OCI8 + SID TEST**. Falta el usuario de solo lectura y confirmar si MiPortalU ya encapsula eso o se crea en la clase nueva.
