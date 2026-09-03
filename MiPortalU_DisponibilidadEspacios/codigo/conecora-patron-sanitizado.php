<?php
/**
 * REFERENCIA SANITIZADA — patrón Conec_ora (Reservitas).
 * NO usar en producción del portal sin acuerdo con Julián.
 * NO poner usuario/clave reales en este archivo.
 * Ambiente objetivo: Banner TEST (SID=TEST).
 */
function Conec_ora_referencia_test() {
    $usuario = ""; // user TEST solo lectura (Manuel)
    $clave   = "";
    $tnsname = "(DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = 172.16.20.38)(PORT = 1521))
        (CONNECT_DATA = (SID = TEST)))";

    $link_ora = oci_connect($usuario, $clave, $tnsname);
    if (!$link_ora) {
        $error = oci_error();
        error_log("Error de conexión Oracle: " . $error['message']);
        return false;
    }
    return $link_ora;
}
