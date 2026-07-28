<?php
/**
 * Configuración de ejemplo — copiar a config.local.php y ajustar.
 * NO entregues credenciales reales en el ZIP si te lo piden sanitizado;
 * usa este archivo como plantilla.
 */
declare(strict_types=1);

return [
    'db' => [
        'host' => '127.0.0.1',
        'port' => '3306',
        'name' => 'prueba_ing',
        'user' => 'root',
        'pass' => '', // en XAMPP suele ir vacío
        'charset' => 'utf8mb4',
    ],
    // Usuario de auditoría de la sesión de prueba (sin login en alcance)
    'app_user' => 'IVAN.CARDONA',
    // Período académico por defecto (ajústalo al valor real de GWRPIEM)
    'periodo_default' => '202630',
];
