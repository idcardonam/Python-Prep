<?php
/**
 * Conexión PDO a MariaDB (prueba_ing)
 * Decisión técnica: PDO por preparación nativa, excepciones y transacciones claras.
 */
declare(strict_types=1);

$config = require __DIR__ . '/config.php';
$db = $config['db'];

$dsn = sprintf(
    'mysql:host=%s;port=%s;dbname=%s;charset=%s',
    $db['host'],
    $db['port'],
    $db['name'],
    $db['charset']
);

try {
    $pdo = new PDO($dsn, $db['user'], $db['pass'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
} catch (PDOException $e) {
    http_response_code(500);
    die('No fue posible conectar a MariaDB. Verifica XAMPP (Apache+MySQL) y config.local.php. Detalle: ' . htmlspecialchars($e->getMessage()));
}

/**
 * Usuario de auditoría de la aplicación (sin módulo de login en el alcance).
 */
function app_user(): string
{
    static $user = null;
    if ($user === null) {
        $cfg = require __DIR__ . '/config.php';
        $user = (string)($cfg['app_user'] ?? 'OPERADOR.TIC');
    }
    return $user;
}

function periodo_default(): string
{
    $cfg = require __DIR__ . '/config.php';
    return (string)($cfg['periodo_default'] ?? '202601');
}

function e(?string $texto): string
{
    return htmlspecialchars((string)$texto, ENT_QUOTES, 'UTF-8');
}

/**
 * Bitácora de auditoría en archivo (no altera el modelo de BD entregado).
 * Valor agregado: trazabilidad operativa institucional.
 */
function auditar(string $accion, array $detalle = []): void
{
    $dir = dirname(__DIR__) . '/logs';
    if (!is_dir($dir)) {
        @mkdir($dir, 0775, true);
    }
    $linea = [
        'fecha' => date('c'),
        'usuario' => app_user(),
        'accion' => $accion,
        'detalle' => $detalle,
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'cli',
    ];
    @file_put_contents(
        $dir . '/acciones.log',
        json_encode($linea, JSON_UNESCAPED_UNICODE) . PHP_EOL,
        FILE_APPEND | LOCK_EX
    );
}

function json_response(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}
