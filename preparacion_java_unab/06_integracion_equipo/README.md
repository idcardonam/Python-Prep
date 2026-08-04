# Laboratorio final · Sprint, Git e integración

Este laboratorio simula el trabajo descrito por la directora:

1. El equipo recibe un proyecto.
2. Divide el alcance en historias.
3. Asigna trabajo.
4. Cada persona desarrolla en una rama.
5. Se revisa el avance durante el sprint.
6. Se integran los cambios.
7. Se prueba el resultado completo.

Aunque practiques solo, representarás tres integrantes trabajando sobre el proyecto `04_web_tomcat`.

## Diferencia importante

- **Sprint:** periodo de trabajo de Scrum.
- **Spring:** framework de Java.

La directora describió sprints semanales. Confirma después si el equipo también utiliza Spring o Spring Boot.

## Objetivo final

Integrar tres historias sobre la aplicación de incidencias:

- US-01: filtros de listado.
- US-02: cambio de estado.
- US-03: auditoría de cambios.

## Preparación

Crea una copia fuera del repositorio principal:

```bash
cp -R preparacion_java_unab/04_web_tomcat /tmp/sprint-unab
cd /tmp/sprint-unab
rm -rf target
git init
git add .
git commit -m "Base aplicación de incidencias"
```

## Flujo de ramas

```text
main
 ├── feature/us-01-filtros
 ├── feature/us-02-estados
 └── feature/us-03-auditoria
```

No desarrolles directamente en `main`.

## Simulación

### Integrante A · Filtros

```bash
git switch -c feature/us-01-filtros
```

Implementa:

- filtro opcional por prioridad;
- filtro opcional por estado;
- conservación de filtros al mostrar resultados;
- pruebas del servicio.

Commits sugeridos:

```bash
git add .
git commit -m "Agregar filtros de prioridad y estado"
git commit -m "Probar combinación de filtros"
```

Vuelve a main:

```bash
git switch main
```

### Integrante B · Estados

```bash
git switch -c feature/us-02-estados
```

Implementa:

- `ABIERTA → EN_PROGRESO`;
- `EN_PROGRESO → CERRADA`;
- rechazo de otras transiciones;
- endpoint POST;
- prueba de transición.

### Integrante C · Auditoría

```bash
git switch main
git switch -c feature/us-03-auditoria
```

Implementa historial con:

- id de incidencia;
- estado anterior;
- estado nuevo;
- usuario;
- fecha;
- comentario.

No registres contraseñas, tokens ni datos innecesarios.

## Revisión semanal simulada

Para cada rama responde:

1. ¿Qué historia estoy resolviendo?
2. ¿Qué terminé?
3. ¿Qué falta?
4. ¿Qué bloqueo tengo?
5. ¿Qué contrato compartido puede afectar?
6. ¿Qué prueba demuestra el avance?

No digas únicamente “voy en 80 %”. Muestra un comportamiento ejecutable.

## Integración

Desde `main`:

```bash
git switch main
git merge --no-ff feature/us-01-filtros
mvn clean test

git merge --no-ff feature/us-02-estados
mvn clean test

git merge --no-ff feature/us-03-auditoria
mvn clean test package
```

Después de cada merge:

- compila;
- ejecuta pruebas;
- revisa conflicto funcional, no solo conflicto de texto;
- prueba el flujo completo.

## Conflicto intencional

Haz que US-01 y US-02 modifiquen `IncidenciaService`.

Al integrar:

1. lee ambas versiones;
2. conserva filtros y transición;
3. elimina duplicidad;
4. compila;
5. ejecuta pruebas;
6. registra el motivo de la resolución.

No resuelvas escogiendo automáticamente “la mía” o “la de ellos”.

## Definition of Done

Una historia está terminada cuando:

- [ ] cumple criterios de aceptación;
- [ ] compila;
- [ ] tiene pruebas;
- [ ] no expone secretos;
- [ ] conserva arquitectura por capas;
- [ ] está documentada;
- [ ] fue integrada con main;
- [ ] pasó prueba de regresión;
- [ ] puede demostrarse.

## Demostración de sprint

En cinco minutos:

1. recuerda el objetivo;
2. muestra cada historia funcionando;
3. explica una decisión;
4. muestra las pruebas;
5. señala riesgo o deuda pendiente;
6. pide retroalimentación.

## Retrospectiva

Escribe:

- Continuar: práctica que funcionó.
- Detener: práctica que generó problema.
- Empezar: mejora para el siguiente sprint.

## Qué decir si preguntan por trabajo en equipo

> En proyectos compartidos considero clave acordar contratos y criterios de aceptación antes de dividir tareas. Trabajo en una rama pequeña, hago commits explicables y pruebo mi componente. Antes de integrar reviso impactos sobre datos, interfaces y seguridad; después del merge ejecuto regresión. En la revisión semanal no reportaría solo porcentaje: mostraría una funcionalidad y los riesgos pendientes.
