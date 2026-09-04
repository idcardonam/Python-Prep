# Decisión de arquitectura — bonito, de cero, pero que encaje en MiPortalU

Fecha: 3 sep 2026. Contexto: Manuel sugiere “de cero” y algo novedoso (React). Julián dejó plantilla de módulo + 4 capas. Reservitas local está ofuscado/infectado en partes.

## Respuesta corta

| Idea | ¿Sí / no? | Por qué |
| --- | --- | --- |
| Construir **de cero** la consulta de aulas | **Sí** | Coinciden jefe, Manuel, guía y el backup de `day.php` |
| Meter **todo** en un React SPA aparte | **No (como entrega oficial)** | Rompe las 4 capas, PHP 5.6 del portal, includes, sesión y menú de MiPortalU |
| UI **moderna e interesante** dentro del portal | **Sí** | CSS/JS propios del módulo + jQuery/SweetAlert; se puede ver premium sin salir del portal |
| Revisar a fondo el Reservitas ofuscado completo | **No hace falta / no conviene** | Ya tenemos la fuente Banner; el ofuscado es ruido o riesgo (webshell). No lo ejecutes |
| Revisar `test_conexion.php` del portal | **Sí** | Ahí está el patrón de conexión a Oracle/Banner que debes reutilizar |

## Las 4 capas (cómo deben crecer los proyectos)

Así lo plantearon para **no dañar** lo demás:

| Capa | Dónde | Qué va de tu proyecto |
| --- | --- | --- |
| 1. Módulo (vista) | `modulos/disponibilidadAulas/` (o nombre acordado) | HTML + filtros + pinta resultados. Plantilla de Julián |
| 2. Clase (negocio) | `gestionContenidos/clases/` | Ej. `DisponibilidadAulas.php` — habla con Banner, arma disponibles/ocupados |
| 3. Assets | `assets/` o assets del módulo | CSS/JS **solo** de esta pantalla (grilla, animaciones ligeras) |
| 4. Datos | Banner TEST (solo lectura) + esquema portal si hace falta catálogo | `V_RESERVAS_SALON`; sin escritura |

La plantilla que te dieron encaja en capa 1+2:

```php
include("../../include/headerInt.inc");
include("../../include/lateralIzqInt.inc");
include($_SERVER["DOCUMENT_ROOT"]."/gestionContenidos/clases/nuevaClase.php");
$nuevaClase = new NuevaClase();
// Font Awesome + SweetAlert
// #desarrollo-contenidos → lógica
include("../../include/footerInt.inc");
```

**Todo lo nuevo de aulas debe nacer así**, no como app React suelta en otro puerto.

## Cómo hacer algo “muy bonito” sin pelear con el portal

Innovación útil = **experiencia**, no cambiar el stack del campus:

1. Misma cáscara MiPortalU (header, lateral, footer, sesión).
2. Interior del `#conten_central` con diseño limpio (tipo mockup, mejorado): tipo → sede → fecha → grilla clara disponible/ocupado.
3. Movimiento suave (hover, transición de tabs), SweetAlert en errores, tipografía/iconos Font Awesome ya cargados.
4. Responsive razonable.
5. Cero botón de reserva; leyenda “Consulta informativa — programación Banner”.

Si más adelante el área aprueba un piloto React, sería un **widget compilado** dentro del módulo (build → un JS en assets). Eso es fase 2 y necesita OK de Julián/Jonathan. **Para el lunes y la construcción inicial: PHP clase + módulo.**

## Reservitas ofuscado en tu PC

- Manuel ya sabe que no es el final.
- **No me subas el zip completo ofuscado.** No lo corras en XAMPP.
- Ya extrajimos lo crítico del `day.php` de backup: `V_RESERVAS_SALON`.
- Si quieres aportar más sin riesgo: solo archivos **legibles** y sin claves:
  - `day.php` (si hay copia sin malware)
  - `config1/2/3` **limpios** (sin el bloque ofuscado del inicio)
  - nombres de vistas/tablas que veas en SQL

## `test_conexion.php` — sí te sirve

Casi seguro prueba la conexión Oracle/MySQL del portal. **Eso es lo que necesitamos para la capa 2.**

Mándame el contenido con:

- host / servicio / usuario **tachados** (`***`),
- solo la forma de conectar (oci_connect, PDO, clase del portal, etc.).

Con eso vemos si la clase `DisponibilidadAulas` reutiliza el mismo mecanismo.

## Qué necesito que me envíes desde tu local (lista corta)

### De MiPortalU (prioridad)

1. `test_conexion.php` (claves tachadas).
2. Un ejemplo de clase en `gestionContenidos/clases/` que ya consulte Oracle/Banner (aunque sea otra funcionalidad) — patrón real.
3. Carpeta `modulos/disponibilidadAulas/` completa (ya tenemos el PHP de enlaces; si hay JS/CSS, mándalos).
4. Confirmación: ¿PHP local 5.6 como dijo Julián?

### De Reservitas (solo si es limpio)

5. `day.php` sin ofuscación al inicio, o confirmación de que el productivo usa `V_RESERVAS_SALON` igual que el backup.
6. Nada de carpetas enteras cifradas/infectadas.

### No envíes

- Passwords, LDAP internos en claro, dumps de BD, el Reservitas ofuscado completo.

## Plan de construcción (cuando tengas test_conexion)

1. Clase `DisponibilidadAulas` (capa 2): fecha + sede + tipo → lista espacios + bloques ocupación desde Banner TEST.
2. Módulo (capa 1): plantilla Julián + UI nueva.
3. Assets (capa 3): CSS/JS del módulo.
4. Equivalencia: 3 días/tipos vs pantalla vieja de Reservitas.
5. Push coordinado con Julián.

## Frase para el lunes / para Manuel

> Vamos de cero en MiPortalU, respetando las 4 capas. La UI será moderna dentro del portal (no un React SPA aparte, para no romper sesión ni estructura). La ocupación la leemos de `V_RESERVAS_SALON` en TEST solo lectura. Reservitas ofuscado no se porta; solo se usa como referencia de negocio.
