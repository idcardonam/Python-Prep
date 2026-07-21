# Laboratorio 1 · Fundamentos de Java

Duración recomendada: 2 horas. Trabaja sin IA y sin abrir `soluciones/`.

## Recordatorio mínimo

```java
int cantidad = 10;
String nombre = "Iván";
boolean activo = true;

if (cantidad > 0) {
    System.out.println("Hay registros");
}

for (int i = 0; i < cantidad; i++) {
    // repetir
}
```

En Java las cadenas se comparan con `equals()`:

```java
estado.equals("ABIERTO")
```

No con:

```java
estado == "ABIERTO"
```

## Ejercicio 1 · Validación

Crea:

```java
boolean correoValido(String correo)
```

Debe rechazar:

- `null`
- cadenas vacías
- cadenas sin `@`
- cadenas sin punto después de `@`

## Ejercicio 2 · Cálculo

Crea:

```java
double calcularTotalHoras(double horas, double valorHora)
```

Reglas:

- Ningún parámetro puede ser negativo.
- Hasta 8 horas se pagan al valor normal.
- Las horas superiores a 8 se pagan con recargo del 25 %.
- Lanza `IllegalArgumentException` cuando un dato sea inválido.

## Ejercicio 3 · Enum

Declara:

```java
enum Prioridad {
    BAJA, MEDIA, ALTA
}
```

Crea un método que reciba una prioridad y devuelva el número máximo de horas para responder:

- ALTA: 2
- MEDIA: 8
- BAJA: 24

Usa `switch`.

## Ejercicio 4 · Clase y encapsulación

Implementa `Incidente` con:

- `long id`
- `String titulo`
- `String descripcion`
- `Prioridad prioridad`
- `Estado estado`

Reglas:

- Atributos privados.
- Título de mínimo 5 caracteres.
- Descripción de mínimo 10 caracteres.
- Estado inicial `ABIERTO`.
- Constructor, getters y `toString()`.

## Ejercicio 5 · Transiciones

Declara:

```java
enum Estado {
    ABIERTO, EN_PROGRESO, CERRADO
}
```

Implementa:

```java
void cambiarEstado(Estado nuevoEstado)
```

Solo se permiten:

- `ABIERTO → EN_PROGRESO`
- `EN_PROGRESO → CERRADO`

No se puede reabrir ni cerrar directamente.

## Ejercicio 6 · List

Crea `GestorIncidentes` con una `ArrayList<Incidente>`.

Métodos:

```java
void agregar(Incidente incidente)
Optional<Incidente> buscarPorId(long id)
List<Incidente> buscarPorEstado(Estado estado)
```

No permitas identificadores duplicados. No devuelvas la lista interna.

## Ejercicio 7 · Map

Crea:

```java
Map<Prioridad, Long> contarPorPrioridad()
```

Debe devolver el número de incidentes por prioridad.

## Ejercicio 8 · Excepciones

Crea:

```java
class IncidenteNoEncontradoException extends RuntimeException
```

Implementa:

```java
Incidente obtenerObligatorio(long id)
```

Debe lanzar esa excepción cuando no exista.

## Ejercicio 9 · Ordenamiento

Devuelve una copia de los incidentes ordenada:

1. prioridad ALTA;
2. prioridad MEDIA;
3. prioridad BAJA;
4. a igual prioridad, por identificador ascendente.

## Ejercicio 10 · Demostración

En `main`:

1. Crea cinco incidentes.
2. Cambia dos a `EN_PROGRESO`.
3. Cierra uno.
4. Imprime el conteo por prioridad.
5. Busca por estado.
6. Intenta cerrar directamente un incidente abierto y demuestra que se rechaza.

## Autoevaluación

- [ ] Compila sin errores.
- [ ] No comparé cadenas con `==`.
- [ ] Los atributos son privados.
- [ ] Validé `null` antes de usar valores.
- [ ] Usé enum en lugar de cadenas libres.
- [ ] No devolví la colección interna.
- [ ] Probé al menos un dato inválido.
- [ ] Puedo explicar cada clase sin leerla.
