# Contratos para integrar sin sorpresas

Antes de dividir trabajo, acuerda contratos.

## Contrato de estados

```java
enum Estado {
    ABIERTA,
    EN_PROGRESO,
    CERRADA
}
```

No cambies nombres en una sola rama sin coordinar persistencia, JSP, pruebas y otros módulos.

## Contrato de servicio

```java
List<Incidencia> buscar(
        Estado estado,
        Prioridad prioridad);

Incidencia cambiarEstado(
        long id,
        int versionEsperada,
        Estado nuevoEstado,
        String usuario,
        String comentario);

List<EventoAuditoria> historial(long incidenciaId);
```

## Contrato HTTP

### Consultar

```text
GET /incidencias?estado=ABIERTA&prioridad=ALTA
```

Respuestas:

- `200`: listado.
- `400`: filtro inválido.

### Cambiar estado

```text
POST /incidencias/estado
```

Campos:

```text
id
version
nuevoEstado
comentario
csrfToken
```

Respuestas:

- `302`: éxito y redirect.
- `400`: dato inválido.
- `403`: sesión o CSRF inválido.
- `404`: incidencia inexistente.
- `409`: conflicto de versión.

## Contrato de base de datos

```sql
UPDATE incidencia
SET estado = ?,
    version = version + 1,
    fecha_actualizacion = CURRENT_TIMESTAMP
WHERE id = ?
  AND version = ?;
```

Historial:

```sql
INSERT INTO historial_incidente (
    incidente_id,
    usuario_id,
    estado_anterior,
    estado_nuevo,
    comentario
) VALUES (?, ?, ?, ?, ?);
```

Ambas sentencias pertenecen a una transacción.

## Compatibilidad

Si una historia necesita cambiar un contrato:

1. documenta el motivo;
2. identifica consumidores;
3. actualiza pruebas;
4. coordina orden de integración;
5. evita romper main;
6. contempla migración de base;
7. informa en la revisión del sprint.

## Revisión antes del merge

- [ ] Firma de métodos acordada.
- [ ] Enum y nombres consistentes.
- [ ] SQL compatible con esquema.
- [ ] Status HTTP definidos.
- [ ] Entrada validada.
- [ ] Error funcional diferenciado del técnico.
- [ ] Pruebas de consumidores actualizadas.
- [ ] No hay secreto ni dato sensible.
