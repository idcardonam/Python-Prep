# EMPEZAR AQUÍ · Preparación Java UNAB

Este es el único directorio que necesitas. Ignora las carpetas `M01` a `M10`: pertenecen a un curso anterior de Python.

## Primer objetivo

Hoy no vas a estudiar Tomcat, Oracle ni Spring. El primer objetivo es:

1. comprobar que Java funciona;
2. abrir un archivo;
3. completar tres métodos pequeños;
4. ejecutar el evaluador;
5. ver resultados correctos e incorrectos.

## Paso 1 · Verificar Java

Haz doble clic en:

```text
00_VERIFICAR_ENTORNO.bat
```

Debe mostrar:

```text
[OK] Java
[OK] Compilador Java
```

Maven y PostgreSQL pueden aparecer pendientes; no los necesitas para el primer ejercicio.

Si Java no está instalado, sigue:

```text
00_instalacion\INSTALACION_WINDOWS.md
```

## Paso 2 · Abrir el ejercicio

Entra en:

```text
01_fundamentos
```

Abre con IntelliJ o Bloc de notas:

```text
PracticaFundamentos.java
```

No abras todavía:

```text
soluciones
```

## Paso 3 · Resolver solamente el ejercicio 1

Busca:

```java
public static boolean correoValido(String correo) {
    // TODO: ejercicio 1
    return false;
}
```

Debes hacer que:

- un correo normal devuelva `true`;
- `null` devuelva `false`;
- una cadena vacía devuelva `false`;
- un texto sin `@` devuelva `false`.

Guarda el archivo.

## Paso 4 · Evaluar

Haz doble clic en:

```text
EVALUAR_FUNDAMENTOS.bat
```

Verás resultados parecidos a:

```text
[OK] correo válido
[FALLO] correo sin punto
[PENDIENTE] cálculo de horas
```

El evaluador no modifica tu código. Solo lo compila, ejecuta casos y muestra qué debes revisar.

## Paso 5 · Continuar

Cuando todos los casos de correo estén correctos:

1. resuelve `calcularTotalHoras`;
2. ejecuta nuevamente el evaluador;
3. resuelve `horasMaximasRespuesta`;
4. vuelve a evaluar.

## Archivo con enunciados

Consulta:

```text
01_fundamentos\ENUNCIADOS.md
```

Trabaja únicamente los ejercicios 1, 2 y 3 durante la primera sesión.

## Qué enviarme

Cuando termines, envíame:

1. una captura del resultado del evaluador; o
2. el contenido de los tres métodos.

Con eso revisamos tus respuestas y pasamos a clases y objetos.

## No hagas todavía

- No estudies código Python.
- No abras las soluciones.
- No instales Oracle.
- No intentes la aplicación Tomcat.
- No memorices toda la guía PDF.

Vamos por niveles. El evaluador te dirá cuándo la primera base está lista.
