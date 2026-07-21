public class EvaluadorFundamentos {
    private static int correctas = 0;
    private static int total = 0;

    public static void main(String[] args) {
        System.out.println("======================================================");
        System.out.println("  EVALUADOR AUTOMATICO - FUNDAMENTOS JAVA");
        System.out.println("======================================================\n");

        System.out.println("NIVEL 1 - Validacion de correo");
        probarBooleano(
                "acepta correo valido",
                true,
                () -> PracticaFundamentos.correoValido("ivan@unab.edu.co"));
        probarBooleano(
                "rechaza texto sin arroba",
                false,
                () -> PracticaFundamentos.correoValido("ivan.unab.edu.co"));
        probarBooleano(
                "rechaza correo sin punto",
                false,
                () -> PracticaFundamentos.correoValido("ivan@unab"));
        probarBooleano(
                "rechaza null",
                false,
                () -> PracticaFundamentos.correoValido(null));
        probarBooleano(
                "rechaza cadena vacia",
                false,
                () -> PracticaFundamentos.correoValido(""));
        probarBooleano(
                "rechaza dominio incompleto",
                false,
                () -> PracticaFundamentos.correoValido("ivan@.com"));

        System.out.println("\nNIVEL 2 - Calculo de horas");
        probarDouble(
                "ocho horas normales",
                80_000,
                () -> PracticaFundamentos.calcularTotalHoras(8, 10_000));
        probarDouble(
                "diez horas con recargo",
                105_000,
                () -> PracticaFundamentos.calcularTotalHoras(10, 10_000));
        probarDouble(
                "cero horas",
                0,
                () -> PracticaFundamentos.calcularTotalHoras(0, 10_000));
        probarExcepcion(
                "rechaza horas negativas",
                () -> PracticaFundamentos.calcularTotalHoras(-1, 10_000));
        probarExcepcion(
                "rechaza valor negativo",
                () -> PracticaFundamentos.calcularTotalHoras(8, -10_000));

        System.out.println("\nNIVEL 3 - Prioridades");
        probarInt(
                "prioridad ALTA responde en 2 horas",
                2,
                () -> PracticaFundamentos.horasMaximasRespuesta(Prioridad.ALTA));
        probarInt(
                "prioridad MEDIA responde en 8 horas",
                8,
                () -> PracticaFundamentos.horasMaximasRespuesta(Prioridad.MEDIA));
        probarInt(
                "prioridad BAJA responde en 24 horas",
                24,
                () -> PracticaFundamentos.horasMaximasRespuesta(Prioridad.BAJA));

        System.out.println("\n======================================================");
        System.out.printf("RESULTADO: %d de %d pruebas correctas%n", correctas, total);

        if (correctas == total) {
            System.out.println("[LISTO] Superaste los tres primeros ejercicios.");
            System.out.println("Envia una captura y continuamos con clases y objetos.");
        } else {
            System.out.println("[CONTINUAR] Revisa solamente los casos marcados FALLO.");
            System.out.println("Guarda PracticaFundamentos.java y ejecuta nuevamente.");
        }
        System.out.println("======================================================");
    }

    private static void probarBooleano(
            String nombre,
            boolean esperado,
            OperacionBooleana operacion) {
        total++;
        try {
            boolean obtenido = operacion.ejecutar();
            if (obtenido == esperado) {
                correcta(nombre);
            } else {
                fallo(nombre, String.valueOf(esperado), String.valueOf(obtenido));
            }
        } catch (Throwable error) {
            error(nombre, error);
        }
    }

    private static void probarDouble(
            String nombre,
            double esperado,
            OperacionDouble operacion) {
        total++;
        try {
            double obtenido = operacion.ejecutar();
            if (Math.abs(obtenido - esperado) < 0.001) {
                correcta(nombre);
            } else {
                fallo(nombre, String.valueOf(esperado), String.valueOf(obtenido));
            }
        } catch (Throwable error) {
            error(nombre, error);
        }
    }

    private static void probarInt(
            String nombre,
            int esperado,
            OperacionInt operacion) {
        total++;
        try {
            int obtenido = operacion.ejecutar();
            if (obtenido == esperado) {
                correcta(nombre);
            } else {
                fallo(nombre, String.valueOf(esperado), String.valueOf(obtenido));
            }
        } catch (Throwable error) {
            error(nombre, error);
        }
    }

    private static void probarExcepcion(String nombre, Operacion operacion) {
        total++;
        try {
            operacion.ejecutar();
            fallo(nombre, "IllegalArgumentException", "no lanzo excepcion");
        } catch (IllegalArgumentException esperado) {
            correcta(nombre);
        } catch (Throwable error) {
            error(nombre, error);
        }
    }

    private static void correcta(String nombre) {
        correctas++;
        System.out.println("[OK] " + nombre);
    }

    private static void fallo(String nombre, String esperado, String obtenido) {
        System.out.println("[FALLO] " + nombre);
        System.out.println("        esperado: " + esperado);
        System.out.println("        obtenido: " + obtenido);
    }

    private static void error(String nombre, Throwable error) {
        System.out.println("[ERROR] " + nombre);
        System.out.println("        " + error.getClass().getSimpleName()
                + ": " + error.getMessage());
    }

    @FunctionalInterface
    interface Operacion {
        void ejecutar();
    }

    @FunctionalInterface
    interface OperacionBooleana {
        boolean ejecutar();
    }

    @FunctionalInterface
    interface OperacionDouble {
        double ejecutar();
    }

    @FunctionalInterface
    interface OperacionInt {
        int ejecutar();
    }
}
