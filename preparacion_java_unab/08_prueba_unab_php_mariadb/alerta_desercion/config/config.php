<?php
/**
 * Carga de configuración local.
 * Prioridad: config.local.php → config.ejemplo.php
 */
declare(strict_types=1);

$local = __DIR__ . '/config.local.php';
$ejemplo = __DIR__ . '/config.ejemplo.php';

if (is_file($local)) {
    return require $local;
}

return require $ejemplo;
