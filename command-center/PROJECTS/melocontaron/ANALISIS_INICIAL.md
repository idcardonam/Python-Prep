# MELOCONTARON — Análisis inicial (`analisis_inicial`)
Fecha: 2026-08-04 · Semáforo: 🟡 Riesgo · Fase: aclaracion  
Fuente: `command-center/PARA_CURSOR_melocontaron.md`

---

### 1) Lo que entendí

MELOCONTARON es un restaurante campestre en Bucaramanga (finca) que hoy opera 100% manual: parqueadero con ticket papel (moto/carro), mesero asigna mesa, pedido y pago inmediato en caja, cocina por papel/radio, y salida sin control digital. El dolor central es falta de trazabilidad (ventas, parqueadero, pedidos incompletos o tardíos, mesas sin atender) y cero inventario/métricas. Quieren un aplicativo usable en teléfono, PC y pantalla de cocina que una: titular + vehículos → mesa → carta/pedido → cobro (comida + parqueadero + propina) → cola de cocina con checks/notas/alertas a meseros → validación de salida por placa. Más adelante: inventario “alcanza para N platos”, reportes, promos, carta QR con fotos ligada a stock, página web con logo, y facturación/IVA (idealmente electrónica). Restricción fuerte: poco internet en sitio. Stack aún no definido. No invento tarifas legales FE ni tiempos exactos hasta confirmar P0.

---

### 2) Preguntas humanizadas

**P0 — para no construir mal**
1. ¿El primer mes es solo el flujo parqueadero→mesa→caja→cocina→salida, o también inventarios/reportes/FE desde el día 1?
2. Con internet débil: ¿les sirve un servidor/PC en caja (red local) que sincronice cuando haya señal, o exigen todo en la nube?
3. ¿El cliente pide solo con mesero/caja, o también desde el QR de la carta?
4. ¿Cuántas mesas, meseros, cajas y “estaciones” de cocina hay en un sábado pico?
5. Parqueadero: ¿tarifa fija (moto/carro) o por tiempo? ¿Siempre se cobra junto con la comida?
6. ¿Ya tienen NIT, resolución DIAN e impresora, o en V1 basta ticket/factura interna con IVA bien desglosado y FE después?

**P1**
7. ¿Preferencia de tecnología (Python/PHP/otro) o aceptan la recomendación PWA + API?
8. ¿Hay logo y fotos de platos/finca listos, o hay que producirlos?
9. ¿La propina se reparte con % fijos configurables?
10. Inventario: ¿recetas (ingredientes → “40 hamburguesas”) desde V1 o stock por producto del menú primero?
11. ¿Ustedes definen minutos de preparación por plato, o el sistema solo aprende con tiempos reales?

**P2**
12. ¿Una sola entrada/salida de vehículos?
13. ¿Login por persona (PIN) o puestos compartidos por rol?
14. ¿Presupuesto hardware y si ya hay TV/HDMI en cocina?

---

### 3) Riesgos

| Riesgo | Detalle | Mitigación |
|--------|---------|------------|
| Internet inestable | App en nube se cae en servicio | Arquitectura LAN-first / PWA offline; cola local; sync diferido |
| Alcance inflado | Operación + inventario + FE + web + contable = no termina | MVP por fases; FE y contable fuera de V1 |
| FE DIAN | Reglas, proveedor, certificados, plazos | Ticket legal-ready + IVA; FE como fase con proveedor |
| Pedidos a medias | Hoy ya pasa; digital mal diseñado lo repite | Estado por ítem + “pedido completo”; no cerrar mesa/cuenta a ciegas |
| Salida sin pago | Moto/carro del combo sale sin cancelar | Gate de salida obliga placa + estado de cuenta; alerta audible/roja |
| Adopción del equipo | Poca tecnología en sala/cocina | UI grande, pocos taps, carta muy visual; capacitación por rol |
| Inventario mentiroso | Recetas mal cargadas → “hay 40” falso | Empezar stock simple; BOM después; conteo físico semanal |
| Dinero y propinas | Cierres mal cuadrados / desconfianza | Cierre diario efectivo vs transferencia; propina línea aparte; auditoría |

---

### 4) Estándar propuesto

- **Arquitectura:** PWA multi-rol (parqueadero, mesero, caja, cocina, admin) + API + SQL. Preferible **nodo local en caja** (LAN) con respaldo/sync a nube cuando haya red.
- **Dominio (nombres de negocio):** `Titular`, `Vehiculo`, `CuentaVisita`, `Mesa`, `Pedido`, `ItemPedido`, `Pago`, `TurnoCaja`, `MovimientoInventario`, `Promo`.
- **Seguridad (IDENTITY):** roles por estación; validar autorización en servidor; SQL parametrizado; no loguear placas+nombre+pago juntos en claro de más; secretos en `.env`; transacciones en cobro + descuento inventario + estado pedido.
- **UI:** pantallas de cocina y caja a pantalla completa, tipografía grande, contraste alto; carta QR con fotos grandes y botones claros (poco texto técnico).
- **Diseño marca:** página campestre Bucaramanga — brand hero, foto real del lugar/platos, sin dashboard en el home; logo en web + factura.
- **Pruebas mínimas:** flujo feliz visita completa; salida bloqueada sin pago; cocina marca ítem → mesero ve alerta; cierre de caja cuadra; carta oculta producto sin stock.
- **Hardware (recomendación inicial):**
  - **Caja:** PC/mini-PC Windows o Linux, 8–16 GB RAM, SSD, pantalla 15–22", UPS; impresora térmica 80 mm USB/Ethernet.
  - **Cocina:** tablet 10–15" o TV HDMI + mini-PC/Chromebox; montaje a la vista; touch o botón grande “listo”.
  - **Meseros / parqueadero:** celular Android gama media con Chrome; funda + carga.
  - **Red:** router local dedicado al POS aunque el internet del ISP falle.

---

### 5) Plan de entregas

**Supuestos:** MVP acordado = flujo operativo sin FE DIAN; 1 caja; inventario simple; hay alguien que pruebe en sitio.

| Tamaño | Entrega | Supuesto |
|--------|---------|----------|
| **S** | Modelo de datos + wire del flujo visita + checklist aceptación MVP | Sin código de UI aún |
| **M** | Parqueadero (titular/vehículos/salida) + mesas + cuenta visita en LAN | Catálogo mesas conocido |
| **L** | Pedido + caja (pago, propina, ticket) + cocina (cola, checks, notas, alerta mesero) | Impresora básica OK |
| **XL** | Carta QR+fotos ligada a stock simple + cierre diario + reportes día + página web marca + promos ligeras | Fotos/logo disponibles |
| **Post-XL** | Recetas/BOM, métricas meseros avanzadas, FE DIAN, contable ampliado | P0 FE y proveedor cerrados |

Estimación global honest a hoy (con P0 abiertas): **MVP operativo L–XL**; producto “completo soñado” varios XL. Semáforo 🟡 hasta cerrar offline + MVP + factura.

---

### 6) Trazabilidad

Actualizar / creado:
- `PROJECTS/melocontaron/PROJECT.md`
- `REQUIREMENTS.md` (pedido 2026-08-04)
- `OPEN_QUESTIONS.md` (Q1–Q14)
- `DECISIONS.md` (fase aclaración + MVP propuesto)
- `DAYLOG.md` (2026-08-04)
- `PARA_CURSOR_melocontaron.md` (entrada)
- Este análisis + JSON para import merge en `app.html`

---

### 7) Qué decirle al JP (≈60s)

> Buen día. Objetivo: digitalizar MELOCONTARON (parqueadero, mesa, caja, cocina) porque hoy no hay trazabilidad y se escapan pedidos y cobros.  
> Hecho: análisis inicial del flujo real y riesgos (sobre todo internet de la finca y el tamaño del alcance).  
> Semáforo 🟡: necesitamos decidir el MVP del primer mes y si trabajamos con servidor local en caja.  
> Bloqueo: ninguno de terceros; falta esa decisión de alcance.  
> Riesgo: querer FE, inventario fino y web marketing al mismo tiempo atrasa lo que más duele (cocina y cobro).  
> Próxima entrega: tras cerrar esas preguntas, el plan MVP con pasos chequeables y demo del flujo visita.  
> ¿Confirmamos que el criterio de listo de la V1 es visita completa cobrada + cocina con checks + salida controlada?

---

### 8) JSON importable

```json
{
  "project": "MELOCONTARON",
  "modo": "analisis_inicial",
  "estimacion": "MVP operativo L–XL (tras cerrar P0); producto completo varios XL. Supuesto: sin FE DIAN en V1, 1 caja, inventario simple, LAN-first.",
  "phase": "aclaracion",
  "sem": "y",
  "preguntas": [
    {
      "prioridad": "P0",
      "texto": "¿El MVP del primer mes es solo parqueadero→mesa→caja→cocina→salida, o también inventario/reportes/FE desde el día 1?",
      "respuesta": ""
    },
    {
      "prioridad": "P0",
      "texto": "Con poco internet: ¿aceptan servidor local en caja (LAN) + sync cuando haya red, o necesitan 100% nube?",
      "respuesta": ""
    },
    {
      "prioridad": "P0",
      "texto": "¿El cliente pide solo con mesero/caja, o también desde la carta QR (self-service)?",
      "respuesta": ""
    },
    {
      "prioridad": "P0",
      "texto": "¿Cuántas mesas, meseros, cajas y estaciones de cocina hay en un día pico?",
      "respuesta": ""
    },
    {
      "prioridad": "P0",
      "texto": "Parqueadero: ¿tarifa fija moto/carro u otros, fija o por tiempo? ¿Se cobra siempre junto con la comida?",
      "respuesta": ""
    },
    {
      "prioridad": "P0",
      "texto": "¿Ya tienen NIT, resolución DIAN, impresora y proveedor FE, o V1 es ticket/factura interna con IVA y FE después?",
      "respuesta": ""
    },
    {
      "prioridad": "P1",
      "texto": "¿Stack preferido (Python/PHP/otro) o aceptan recomendación PWA + API + SQL?",
      "respuesta": ""
    },
    {
      "prioridad": "P1",
      "texto": "¿Logo y fotos de platos/finca ya existen o hay que diseñar/tomar?",
      "respuesta": ""
    },
    {
      "prioridad": "P1",
      "texto": "¿La propina voluntaria se reparte con reglas/porcentajes configurables por admin?",
      "respuesta": ""
    },
    {
      "prioridad": "P1",
      "texto": "Inventario: ¿recetas (BOM) desde V1 para “alcanza para N platos”, o stock simple por producto del menú primero?",
      "respuesta": ""
    },
    {
      "prioridad": "P1",
      "texto": "¿Definirán minutos de preparación por producto o el sistema solo registrará tiempos reales?",
      "respuesta": ""
    },
    {
      "prioridad": "P2",
      "texto": "¿Hay una sola entrada/salida de vehículos? ¿Motos y carros comparten control?",
      "respuesta": ""
    },
    {
      "prioridad": "P2",
      "texto": "¿Login por persona (PIN/usuario) desde el día 1 o puestos compartidos por estación/rol?",
      "respuesta": ""
    },
    {
      "prioridad": "P2",
      "texto": "¿Presupuesto aproximado de hardware (caja + cocina + impresora) y si ya hay TV HDMI en cocina?",
      "respuesta": ""
    }
  ],
  "riesgos": [
    {
      "titulo": "Internet inestable en finca",
      "detalle": "Si la app depende de nube, se cae el servicio en el momento de mayor venta.",
      "mitigacion": "Diseño LAN-first / PWA con cola local y sincronización diferida; router dedicado al POS."
    },
    {
      "titulo": "Alcance demasiado amplio",
      "detalle": "Operación + inventario fino + FE + web + contable en un solo golpe atrasa el dolor real.",
      "mitigacion": "MVP por fases; FE DIAN y contable ampliado fuera de V1."
    },
    {
      "titulo": "Facturación electrónica DIAN",
      "detalle": "Requiere NIT, resolución, proveedor tecnológico y pruebas; no es un print HTML.",
      "mitigacion": "V1 ticket/factura interna con IVA correcto; FE como fase con proveedor."
    },
    {
      "titulo": "Pedidos incompletos o sin cierre",
      "detalle": "Hoy ya molesta al cliente; un sistema sin estado por ítem lo replica.",
      "mitigacion": "Estados por ítem y por pedido; alertas a mesero; no cerrar cuenta a ciegas."
    },
    {
      "titulo": "Salida de vehículo sin pago",
      "detalle": "Una moto del combo puede salir si no hay control de placa vs cuenta.",
      "mitigacion": "Pantalla/salida exige placa y muestra deuda; alerta si intentan liberar sin pagar."
    },
    {
      "titulo": "Inventario incorrecto",
      "detalle": "“Hay para 40 hamburguesas” falso genera sobreventa o desconfianza.",
      "mitigacion": "Empezar stock simple; recetas después; conteos físicos; carta oculta agotados."
    },
    {
      "titulo": "Adopción del personal",
      "detalle": "Equipo acostumbrado a papel/radio puede rechazar pantallas complejas.",
      "mitigacion": "UI de pocos toques, letras grandes, capacitación por rol, piloto en un turno."
    }
  ],
  "millas": [
    {
      "titulo": "Modo LAN-first con cola offline",
      "beneficio": "El restaurante sigue vendiendo aunque falle el ISP; reduce pelea operativa el sábado.",
      "riesgo": "Sync conflictivo si hay dos cajas sin diseño de conflicto.",
      "mitigacion": "V1 una caja autoridad; sync con marcas de tiempo; pruebas de corte de red.",
      "ok": false
    },
    {
      "titulo": "KDS cocina con semáforo por vencer",
      "beneficio": "Prioriza lo que se está demorando; baja quejas por espera.",
      "riesgo": "Alertas ruidosas si los umbrales son malos.",
      "mitigacion": "Umbrales configurables por tipo de plato; sonido solo en rojo.",
      "ok": false
    },
    {
      "titulo": "Cuenta visita unificada (comida + parqueadero + propina)",
      "beneficio": "Un solo cobro por nombre/titular; menos fugas y menos vueltas del cliente.",
      "riesgo": "Error al vincular placa/titular duplicado.",
      "mitigacion": "Búsqueda por nombre y placa; confirmación visual antes de cobrar.",
      "ok": false
    },
    {
      "titulo": "Carta QR visual ligada a stock",
      "beneficio": "Cliente ve fotos y no pide lo agotado; menos errores y mejor experiencia.",
      "riesgo": "Fotos pesadas en red mala.",
      "mitigacion": "Imágenes optimizadas y cache PWA; modo solo lectura offline.",
      "ok": false
    },
    {
      "titulo": "Cierre de caja con propina e IVA separados",
      "beneficio": "Ganancias claras del día; propina repartible; base limpia para FE futura.",
      "riesgo": "Mal clasificar transferencia vs efectivo.",
      "mitigacion": "Medio de pago obligatorio por transacción; reporte de arqueo.",
      "ok": false
    },
    {
      "titulo": "Alerta de salida por placa sin pago",
      "beneficio": "Evita que se escape una moto/carro del combo sin liquidar.",
      "riesgo": "Falsos positivos si hay dos visitas con placa parecida.",
      "mitigacion": "Placa normalizada + estado de cuenta visible; override solo admin con motivo.",
      "ok": false
    }
  ],
  "pasos": [
    {
      "title": "Cerrar P0 con dueño (MVP, LAN/nube, quién pide, capacidad, tarifas, factura)",
      "detail": "Responder en app.html las 6 P0; sin eso no se fija estimación ni stack.",
      "done": false
    },
    {
      "title": "Congelar MVP V1 y fuera de alcance",
      "detail": "Propuesta: visita completa + cocina checks/alertas + salida + carta QR lectura + cierre diario; FE/BOM/web marketing fase 2.",
      "done": false
    },
    {
      "title": "Mapear mesas, roles y catálogo mínimo de productos",
      "detail": "Lista de mesas, productos con precio/IVA, tipos vehículo/tarifas; CSV o hoja simple.",
      "done": false
    },
    {
      "title": "Definir modelo SQL cuenta_visita / pedido / item_pedido / pago / vehiculo",
      "detail": "Incluir estados, propina, medio pago, timestamps; transacciones en cobro.",
      "done": false
    },
    {
      "title": "Wireframes por rol: parqueadero, mesero, caja, cocina, admin",
      "detail": "Una composición clara por pantalla; cocina full-bleed cola; caja cobro simple.",
      "done": false
    },
    {
      "title": "Recomendación hardware cerrada (caja + cocina + impresora + red local)",
      "detail": "Mini-PC/PC caja + UPS + térmica 80mm; tablet/TV cocina; celulares operación; router LAN.",
      "done": false
    },
    {
      "title": "Recoger logo y fotos (platos + finca) para carta, factura y web",
      "detail": "Assets en INBOX/melocontaron/adjuntos/; definir tipografías/colores marca campestre.",
      "done": false
    },
    {
      "title": "Borrador página web restaurante campestre Bucaramanga",
      "detail": "Hero marca + foto lugar; sin cards de stats; CTA reserva/WhatsApp/cómo llegar; móvil OK.",
      "done": false
    },
    {
      "title": "Prototipo LAN del flujo feliz visita (sin FE)",
      "detail": "Parqueadero→mesa→pedido→pago→cocina check→aviso mesero→salida por placa.",
      "done": false
    },
    {
      "title": "Prueba en sitio con corte de internet",
      "detail": "Validar que caja/cocina siguen; documentar en DAYLOG resultados.",
      "done": false
    },
    {
      "title": "Diseño ticket/factura impresa con logo, IVA y propina",
      "detail": "Campos listos para FE futura; no secretos en código de impresión.",
      "done": false
    },
    {
      "title": "Backlog fase 2: BOM inventario, promos, métricas meseros, FE DIAN",
      "detail": "Queda documentado; no mezclar en sprint MVP salvo P0 que lo exija.",
      "done": false
    }
  ],
  "pm_update": "🟡 MELOCONTARON en aclaración: flujo manual entendido (parqueadero→mesa→caja→cocina→salida). Falta decidir MVP del primer mes y si operamos LAN-first por el internet de la finca. Próxima entrega tras P0: plan MVP con pasos y demo del flujo visita. V1 propuesta sin FE DIAN completa."
}
```
