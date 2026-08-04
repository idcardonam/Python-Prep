# QUESTION BANK — Preguntas humanizadas (reutilizar)

## A. Alcance y “listo”
- Para no asumir: ¿qué tiene que poder hacer el usuario el día de la entrega?
- ¿Qué queda **fuera** de esta primera versión?
- ¿Hay un ejemplo (pantalla, Excel, sistema viejo) de cómo lo imaginan?
- ¿Quién prueba y quién da el OK final?

## B. Datos y seguridad
- ¿Hay datos personales / académicos / sensibles? ¿Quién puede verlos?
- ¿Usamos usuario de aplicación o el login de la persona?
- ¿Las claves van en config local o ya tienen un vault/estándar?
- Si algo falla a mitad: ¿se debe deshacer todo (transacción) o se guarda parcial?

## C. Base de datos
- ¿La tabla/modelo ya existe o hay que crearla? ¿Podemos alterarla?
- ¿Baja física o lógica (activo S/N)?
- ¿Hay llaves foráneas o procedimientos que no debamos romper?
- ¿Periodo / sede / programa filtran la información?

## D. Integraciones
- ¿Este módulo alimenta o depende de otro sistema?
- ¿Hay API, archivo plano, vista SQL, o solo pantalla?
- Si el otro sistema cae: ¿qué debe pasar aquí?

## E. Operación y soporte
- ¿Quién lo usará día a día (rol)?
- ¿Necesitan exportar (Excel/PDF) desde el día 1?
- ¿Hay horarios de ventana para desplegar?

## F. Avance con jefe de proyecto
- ¿El criterio de avance de esta semana es demo, PR, o documento?
- Si aparece un bloqueo mañana: ¿con quién escalamos?
- ¿Prefieren actualización por chat, correo o solo en la reunión de avance?

## G. Stack (cuando aún no está claro)
- ¿Este desarrollo va en PHP, Java o Python según el sistema existente?
- ¿Dónde está el repositorio (GitLab, Azure DevOps, GitHub) y la rama base?
- ¿Tienen ambiente de pruebas aparte de producción?
