# REQUIREMENTS — Historial de lo pedido

## 2026-08-04 — Origen (chat / notas propias — análisis inicial)
**Pedido:** Aplicativo multi-dispositivo (teléfono, computador, pantalla cocina) para restaurante campestre MELOCONTARON en Bucaramanga, reemplazando operación 100% manual.

**Flujo operativo descrito:**
1. Ingreso por parqueadero: registrar titular + vehículos en una cuenta; tarifas por tipo (moto/carro).
2. Mesero asigna mesa al titular; muestra carta; toma pedido.
3. Cliente paga en caja (pedido + parqueadero) con identificación por nombre/titular; propina voluntaria; factura impresa con logo; IVA reglamentario; valorar FE.
4. Cocina recibe por orden de llegada; check por ítem/orden hasta completar; notas; pantalla de próximos a vencer; al salir platos, notificar meseros; al entregar, cerrar progresivamente.
5. Salida parqueadero: validar placa y que haya cancelado; alertar si sale vehículo del combo sin pago.
6. Inventario pesado: “hay para N hamburguesas / N perros…”; carta conectada a stock (disponible/no); ETA de pedido.
7. Admin: cierres diarios (efectivo/transferencias), ganancias día/mes, más/menos vendidos, órdenes más atrasadas, productos que salen rápido, métricas meseros (mesas atendidas, cancelaciones, menos gestión), promos para estancados/días especiales.
8. Carta digital con QR, imágenes, usable por gente poco tecnológica.
9. Página web restaurante campestre + logo en factura y sitio.
10. Recomendar hardware: PC caja + dispositivo cocina.

**Entrega esperada:** (por definir tras preguntas P0 — MVP operativo primero)

**Criterios de aceptación (borrador — validar):**
- [ ] Titular+vehículos se registran y se vinculan a mesa/cuenta
- [ ] Pedido se cobra junto con parqueadero en caja
- [ ] Cocina ve cola, marca salidas y mesero recibe aviso
- [ ] No sale vehículo sin estado de pago claro
- [ ] Inventario básico descuenta y afecta disponibilidad en carta
- [ ] Cierre diario efectivo + transferencias
- [ ] Carta QR con fotos usable en móvil
- [ ] Opera con internet intermitente (criterio a precisar)

**Fuera de alcance (propuesto para V1 — confirmar):**
- Facturación electrónica DIAN completa (dejar como milla/fase)
- Contabilidad formal multi-libro / nómina
- Pedido self-service desde la mesa sin mesero (salvo que se priorice)
- App nativa stores (preferir PWA/web)

**Notas:** Semáforo 🟡. Stack no definido. Priorizar flujo parqueadero→mesa→caja→cocina→salida.
