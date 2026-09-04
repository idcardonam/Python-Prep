# Innovación Manuel — API puente (más rápido que pegarle directo a Banner)

## Remotes (OK)

```text
origin → https://github.com/Idcardona/miportalu-lab.git   ← lab / push aquí
unab   → http://172.16.20.59:8082/web/miportalu.git     ← UNAB / NO push
```

## Qué dijo Manuel (y por qué tiene sentido)

Si MiPortalU hace en cada clic la misma query pesada a `V_RESERVAS_SALON` (como Reservitas), **se va a sentir lento**.  
Innovar “de cero” no es solo una UI bonita: es **separar la consulta a Banner detrás de una API** que:

1. Reciba filtros (tipo, sede, fecha, franja).  
2. Consulte Banner **una vez** (o con caché).  
3. Devuelva JSON liviano (espacios + bloques disponible/ocupado).  
4. **No** exponga docente ni permita escribir.

El módulo del portal solo pinta. La API es el puente.

## Cómo lo encajamos (sin romper las 4 capas)

```text
Navegador (estudiante)
        │
        ▼
MiPortalU — módulo disponibilidad.php (UI + jQuery/fetch)
        │  HTTP JSON
        ▼
API Disponibilidad (puente)  ← NUEVA
        │  OCI8 solo lectura + caché
        ▼
Banner TEST/PROD  V_RESERVAS_SALON
```

| Capa | Qué es ahora |
| --- | --- |
| Vista | Módulo Julián (tabs, grilla) |
| Clase portal (opcional) | Llama a la API; no embebe SQL gigante |
| **API** | Nuevo: endpoint(s) + caché + query acotada |
| Datos | Banner solo lectura |

No hace falta React. La UI sigue en el portal; la innovación es el **puente + caché**.

## Fases (realista)

### Fase 0 — Lunes (presentación)

Decir:

> Alternativa recomendada: implementación de cero en MiPortalU con **API puente** a Banner (no copiar day.php). La API filtra, cachea y entrega JSON; el portal solo consulta. Evita la lentitud de pegarle directo a la vista pesada en cada request.

Demo: prototipo UI + **API mock** (JSON fijo) en el lab.

### Fase 1 — Prototipo en `miportalu-lab` (ya)

1. UI módulo (plantilla Julián).  
2. Mini API en el mismo lab, ej.:  
   `api/disponibilidad/consultar.php?tipo=2&sede=1&fecha=2026-09-03`  
   → JSON mock.  
3. El módulo hace `fetch` / jQuery.getJSON a esa URL.

### Fase 2 — API real (después del lunes / con Manuel)

1. Mismo contrato JSON.  
2. Dentro: `oci_connect` TEST + `V_RESERVAS_SALON` con filtros (fecha, EDIF, ROOM).  
3. Caché corta (ej. 60–120 s por clave `tipo|sede|fecha`) en archivo o APCu.  
4. Sin docente en la respuesta.  
5. Medir tiempo vs Reservitas (innovación demostrable).

### Fase 3 — Si el área lo pide

API en servicio aparte (IIS/otro vhost), Redis, etc. **No** es requisito para el lunes.

## Contrato JSON sugerido (para el lab)

```json
{
  "fecha": "2026-09-03",
  "tipo": 2,
  "sede": 1,
  "resolucion_minutos": 30,
  "desde": "06:00",
  "hasta": "22:00",
  "espacios": [
    {
      "codigo": "ED-ING-L51-AINF",
      "edificio": "ED-ING",
      "disponible_franja": true,
      "bloques": [
        { "hora": "08:00", "estado": "ocupado", "titulo": "Cálculo Integral" },
        { "hora": "09:00", "estado": "libre", "titulo": null }
      ]
    }
  ]
}
```

Sin `docente`, sin `departamento`.

## Qué decirle a Manuel

> Vamos con API puente desde el diseño: el portal no ejecuta la vista pesada en cada pintada. En el lab primero mock + UI; luego enchufamos OCI TEST con caché. El lunes presentamos esa alternativa como la innovación de rendimiento.

## Qué NO hacer

- No clonar la lógica de reservas/préstamos en la API.  
- No React SPA.  
- No pegar SQL de `day.php` en el PHP de la vista.  
- No push a `unab`.

## Prompt extra para el chat del lab

Añadir al prompt de arranque:

```text
Innovación acordada con Manuel: API puente (JSON) entre el módulo y Banner.
Primero: endpoint api mock + UI que lo consuma.
Después: mismo contrato con OCI8 TEST + caché corta.
El módulo no debe embeber la query pesada de V_RESERVAS_SALON.
```
