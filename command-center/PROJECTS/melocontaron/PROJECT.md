# PROJECT — MELOCONTARON

**Estado:** en aclaración  
**Stack probable:** Web progresiva (PWA) + API (Python/PHP por confirmar) + SQL — priorizar offline/local por internet limitado en finca  
**Repo empresa:** (por confirmar; proyecto propio)  
**Stakeholders:** dueño/admin del restaurante; operación (parqueadero, meseros, caja, cocina)  
**Objetivo (1 párrafo):** Digitalizar el flujo del restaurante campestre MELOCONTARON (Bucaramanga): ingreso por parqueadero → titular + vehículos → asignación de mesa → carta/pedido → pago en caja (comida + parqueadero) → cocina por orden de llegada con checks y alertas → entrega por mesero, con inventario, cierres, métricas y carta QR; página pública del restaurante.

## Contexto
- Hoy todo es manual (papel, radio). No hay trazabilidad real de ventas ni de parqueadero.
- ~80% de clientes llegan en vehículo e ingresan por el portón.
- Parqueadero: moto ~2000 / carro ~3000 (valores a confirmar); ticket en papel.
- Mesero asigna mesa; pedido y pago inmediato en caja; ticket a cocina.
- Problemas: pedidos incompletos/tardíos, mesas sin atender, gente que se va pagando solo parqueadero, sin métricas.
- Finca con **poco internet** → arquitectura debe contemplar operación local / degradada.
- Actores: administrador, cocina, meseros, parqueadero, caja.

## Usuarios
- **Parqueadero:** registra titular, vehículos/placas, controla salida (pago OK).
- **Mesero:** asigna mesa, atiende, recibe alertas de “listo para recoger”, cierra entrega.
- **Caja:** cobra pedido + parqueadero, propina, factura impresa, cierre diario.
- **Cocina:** cola de pedidos, checks por ítem/orden, notas, alertas por vencer.
- **Administrador:** inventario, reportes, promos, métricas meseros/productos, contabilidad básica.
- **Cliente (carta QR / web):** consulta carta digital interactiva (sin pedir necesariamente desde mesa en V1 — por confirmar).

## Sistemas relacionados
- Facturación electrónica DIAN (Colombia) — fase posterior si se confirma.
- Impresora de factura/ticket (caja).
- Posible pantalla cocina (TV/tablet) + PC caja + celulares meseros/parqueadero.
- Página web pública del restaurante (marca + logo).

## Restricciones conocidas
- Internet limitado en sitio.
- Sin stack/lenguaje definido aún.
- Alcance amplio (operación + inventario + FE + web + hardware) → MVP por fases obligatorio.
- Cumplimiento legal factura/IVA restaurante Colombia.

## Enlaces útiles
- Ticket/correo: proyecto propio (origen chat/notas)
- Docs: `command-center/PARA_CURSOR_melocontaron.md`
- Análisis: `command-center/PROJECTS/melocontaron/ANALISIS_INICIAL.md`
