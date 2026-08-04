# SOLICITUD DE PROCESAMIENTO
Comando: **procesa** según PLAYBOOK.md + AGENTS.md + IDENTITY_CODE.md
Archivo: `PARA_CURSOR_melocontaron.md`

## Modo
analisis_inicial
(Análisis inicial)

## Regla de continuidad (OBLIGATORIA)
- Mismo idioma/estructura del proyecto: no reinventar desde cero.
- **MERGE**, no wipe: conservar preguntas ya respondidas, millas ya aprobadas (`ok:true`) y pasos ya hechos (`done:true`).
- Actualizar/añadir solo lo que cambió por nuevas notas, requerimientos, diseño o features.
- Si una milla/paso ya no aplica, márcalo en el texto del análisis; en JSON puedes omitirlo o dejarlo con nota en detail — la app preservará checks por título.
- Incluye diseño/UI si el modo es ajuste_camino o si las notas lo piden.

## Proyecto
- Nombre: MELOCONTARON
- Slug: melocontaron
- Fase: aclaracion
- Semáforo: 🟡 Riesgo
- Estimación actual: (pedir en análisis)
- Bloqueo: (ninguno)

## Instrucciones para la IA
1. Entendido (sin inventar)
2. Preguntas P0/P1/P2 (no repetir las ya respondidas abajo)
3. Riesgos + mitigación
4. Millas extra NUEVAS o actualizadas para ESTE proyecto (beneficio/riesgo/mitigación)
5. Plan de entregas S/M/L/XL
6. Pasos checkeables (archivos, SQL, UI/diseño, pruebas…)
7. Texto 60s para JP
8. Al final: bloque JSON importable (schema abajo)

## Formato JSON obligatorio al final
```json
{
  "project": "MELOCONTARON",
  "modo": "analisis_inicial",
  "estimacion": "...",
  "phase": "aclaracion|desarrollo|pruebas|entrega|integracion",
  "sem": "g|y|r",
  "preguntas": [{"prioridad":"P0","texto":"...","respuesta":""}],
  "riesgos": [{"titulo":"...","detalle":"...","mitigacion":"..."}],
  "millas": [{"titulo":"...","beneficio":"...","riesgo":"...","mitigacion":"...","ok":false}],
  "pasos": [{"title":"...","detail":"...","done":false}],
  "pm_update": "texto corto para el JP"
}
```
En millas/pasos ya aprobados o hechos, respeta `ok:true` / `done:true` del estado actual.

## Identidad
Identidad Iván — eje seguridad + claridad:
- Claridad para compañeros; nombres del negocio.
- Seguridad por defecto: validar frontera, SQL parametrizado, sin secretos en código, mínimo privilegio, no loguear PII.
- Transacciones en multi-paso; baja lógica si aplica.
- Errores humanizados al usuario; detalle en log.
- Cambios mínimos/reversibles; no romper módulos vecinos.
- Al entrar a código ajeno: mapear → adaptar → elevar seguridad sin reescribir todo.
- Milla extra: propuesta IA por proyecto (beneficio+riesgo), no adorno repetido.
Ver detalle completo en IDENTITY_CODE.md

## Estado actual — Millas aprobadas
(ninguna aún)

## Estado actual — Millas pendientes / no checkeadas
(ninguna)

## Estado actual — Pasos hechos
(ninguno)

## Estado actual — Pasos pendientes
(ninguno)

## Respuestas ya dadas
(ninguna)

## Adjuntos (rutas)
(ninguno anotado)

## Controversias
mi funcionamiento pensado. se ingresa por el parqueadero se registra el nombre de un titular y se le guardan los vehiculos que traigan en una sola cuenta, suben y el mesero le asigna la mesa al titular ingresado muestra la carta y hace el pedido inmediatamente le dice que debe acercarse a caja pagar el pedido, con su nombre en caja le cobran su pedido y lo del parqueadero, en cocina reciben los pedidos por orden de llegada debe ir saliendo y check de cada pedido que cada orden hasta terminar y completar el pedido, me gustaria ver una pantalla con los pedidos que esten proximos a vencer y no olvidar las notas de cada pedido. cuando ya el pedido vayan saliendo le notifique a los meseros que ya hay que recoger algo para entregar cuando ya lo recojan y entreguen vayan cerrando poco a poco.
dentron del aplicativo para el administrador el tema de cocina se debe tener todo pesado e inventariado dentro del aplicativo para ir conociendo que falta y que no para abastacer con tiempo, por ejemplo el aplicativo debe decir tenemos para 40 hamburguesas, para 40 perros y asi, conocer las ordenes que mas se retrasaron en la fecha del dia o la escogida, conocer los productos que salieron rapidos por orden
en caja deben haber cierres diarios de vendido por lo que hay en caja y en transferencias, conocer ganancias del dia del mes, conocer los productos mas vendidos, los menos vendidos, lnventario de todo lo que hay para identificar que hay y que falta
en la salida se debe pedir o ver la placa para que los dejen salir y saber si ya cancelo, por ejemplo si salio una moto de todo ese combo debe informarse por si no pagan o algo asi 
la carta debe ser totalmente digital con qr que los clientes la puedan visualizar con imagenes y muy bien interactiva que los que no utilicen tanta tecnologia la puedan visualizar y escoger bien sin errores  
los meseros debe mostrar cuantas mesas atencio y cual fue el mesero que menos gestiono, cual mesa se le fue, cual mesa cancelo debe mostrar toda informacion relevante a sus gestiones, inmediatamente mostrar que hay disponible y que no por eso me gustaria que la carta se conecte con inventario y al generar una orden sepa cuanto debe tardar el pedido 
me gustaria que el aplicativo sirviera con temas contables y sirva para facturacion electronica si se puede, la facturacion debe ser impresa se le adiciona el tema de propina voluntaria, en las ganacias identificar bien eso para distribuirla con todo el equipo, se debe gestionar el tema de iva para que las facturas salgan bien reglamentarias de todo lo que se necesita para facturacion de un restaurante en orden legalmente 

debemos tener opcion de crear promos para sacar productos estancados y cosas asi de bebidas por dias especiales

## Ajustes del camino / diseño / features nuevas
debemos imcorporar logo en la factura, en la pagina, debemos recomendar que tipo de computador comprar para caja, que dispositivo se utiliza en cocina para visualizar y marcar salidas de las comidas, una pagina de un restaurante campestre en bucaramanga

## Origen
proyecto propio

## Transcript / notas
Actores: administrador, cocina, meseros, parqueadero, caja de pago
Descripcion de necesidad: se requiere un aplicativo el cual pueda ser utilizado en telefono, computador y alguna pantalla para cocina
el restaurante melocontaron funciona totalmente manual no se conoce trazabilidad de ventas, ganancias 100% reales de parqueadero, ni cual producto se vende mas ni como evolucionar mejor los productos con poca venta
el 80% de los clientes llegan por transporte y son ingresados por el porton el parqueadero donde se les entrega un papel con el tipo de vehiculo sea moto 2000 o carro 3000 el tiempo que demoren dentro del restaurante, cuando parquean el vehiculo un mesero los espera y le muestra que mesa tiene disponible y se la asigna. entonces van a caja le muestran la carta y hacen el pedido en caja pagando inmediatamente su pedido es tomado en papel y llevado a cocina para preparacion por orden de llegada o lo que puedan ir sacando mas rapido que ya este precocido, cuando ya pagan el cliente se va a sentar y cuando ya esta el mesero le informan a traves de radio que ya esta el pedido mesa x, lo llevan aveces tardan demasiado o aveces llevan una parte y se demora la otra parte no se conoce si se cerro todo el pedido en algunas ocaciones y la gente se molesta. o aveces los ingresan y no los atienden y se van enfadados pagando el parqueadero, entonces se requiere revisar un aplicativo aun no tengo definido lenguaje ni que tipo de aplicativo, el restaurante es una finca con poco internet,
