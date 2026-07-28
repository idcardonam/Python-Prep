<?php
/**
 * Configuración local de la VM (ajusta si root tiene clave).
 * Este archivo SÍ se usa en la máquina de la prueba.
 */
declare(strict_types=1);

return [
    'db' => [
        'host' => '127.0.0.1',
        'port' => '3306',
        'name' => 'prueba_ing',
        'user' => 'root',
        'pass' => '',
        'charset' => 'utf8mb4',
    ],
    'app_user' => 'IVAN.CARDONA',
    'periodo_default' => '202601',
];
