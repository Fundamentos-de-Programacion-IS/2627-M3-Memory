# Memory-M3
En este tercer hito construiremos un juego de parejas clásico usando `pygame`. La
idea es centrarnos en una lógica muy procedural: listas, diccionarios, bucles y
condicionales. Toda la parte visual ya está resuelta en un motor que expone una
sencilla API basada en funciones.

> **Cómo entregar (curso 26/27).** En el repositorio `2627-M3-Memory` pulsad
> **«Use this template» → Create a new repository** para crear el repositorio del grupo
> (ya no se usa *fork*). Cuando lo tengáis resuelto, comprimid el proyecto en
> `memory-<nombre del grupo>.zip` y subidlo al formulario de ev.us.es.
> **Fecha límite: viernes 18 de diciembre.** Basta con que lo suba una persona del grupo.

## Cómo se evalúa este hito

Este hito **no puntúa por sí solo**. Forma parte de tu nota de teoría de dos maneras:

- **Requisito**: debe estar **entregado en plazo** y **ejecutarse sin errores**.
- **Bonus**: el conjunto de los tres hitos puede aportar hasta **+0,5** sobre la nota de
  teoría por calidad y extras, según la rúbrica común.

La nota de teoría sale de los **dos controles individuales de laboratorio**
(martes 24 nov y martes 15 dic), que se corrigen de forma **automática** y usan el mismo
formato que el examen práctico de enero. Los controles se plantean **sobre el dominio de
este hito**: cuanto mejor entiendas el código que has escrito aquí, menos te costará el
control.

> Trabajad el proyecto vosotros. Lo que no sepáis escribir sin ayuda no lo sabréis escribir
> en el laboratorio, que es donde se pone la nota.

### Uso de inteligencia artificial

Se **desaconseja** usar IA generativa para resolver los TODO. Antes de recurrir a ella,
utiliza los apuntes, la documentación, las pruebas propias y las tutorías. Si la usas de
forma puntual, decláralo en el README y comprueba que puedes explicar, probar y modificar
todo el código generado. La IA no está permitida en simulacros, controles ni exámenes.

## Requisitos previos
1. Python 3.10 o superior.
2. Instalar `pygame` si aún no lo tienes:
   ```bash
   python -m pip install pygame
   ```
3. Ejecuta el motor con:
   ```bash
   python game.py --rows 4 --cols 4
   ```
   Ajusta `--rows` y `--cols` para probar diferentes tamaños (recuerda que el
   número total de casillas debe ser par).

## Contexto
El alumnado debe ocuparse exclusivamente de la parte "clásica" del juego:
preparar los datos iniciales, gestionar qué cartas pueden revelarse y decidir si
hay pareja o no. La interfaz incluida (`memory_engine.py`) representa el tablero,
lanza el bucle principal y llama a funciones del módulo `logic`. De este modo se
mantiene una plantilla procedural sin clases ni decoradores.

## Ficheros en esta carpeta
- `memory_engine.py`: motor gráfico listo para usar. **No se modifica.**
- `game.py`: punto de entrada que conecta el motor con la lógica del alumno.
- `logic_student.py`: plantilla con todas las funciones `TODO` que debes completar.
- `logic.py`: solución de referencia del profesorado. **No debe incluirse en el
  repositorio que se entregue al alumnado.**
- `PRUEBAS.md`: casos mínimos para comprobar la lógica antes de abrir el juego.

## Ejercicios
Completa las funciones que aparecen en `logic_student.py` respetando los tipos y los
nombres de las claves descritas. Se recomienda resolverlas en este orden:

1. **`build_symbol_pool`** *(1 punto)*: construye la lista plana con todos los
   símbolos necesarios para rellenar el tablero. Cada símbolo debe aparecer dos
   veces. Puedes empezar con letras y números, y barajar al final con
   `random.shuffle`.
2. **`create_game`** *(2 puntos)*: a partir del resultado del paso anterior,
   construye el tablero (lista de listas de cartas) y devuelve un diccionario con
   los contadores iniciales: ``pending``, ``moves``, ``matches``, ``total_pairs``
   y las dimensiones.
3. **`reveal_card`** *(2 puntos)*: valida las coordenadas recibidas, evita
   revelar la misma carta dos veces y añade las posiciones a ``pending``. Solo
   puede haber dos cartas visibles a la vez.
4. **`resolve_pending`** *(3 puntos)*: cuando haya dos cartas en ``pending``,
   comprueba si coinciden. Si hay pareja marca el estado como `found` y suma un
   punto al contador de ``matches``; en caso contrario vuelve a ocultarlas. En
   ambos casos incrementa ``moves`` y vacía ``pending``.
5. **`has_won`** *(1 punto)*: devuelve `True` cuando las parejas encontradas
   alcancen a `total_pairs`.

Cada carta del tablero es un diccionario con las claves `symbol` y `state`. Los
únicos valores permitidos en `state` son las constantes `STATE_HIDDEN`,
`STATE_VISIBLE` y `STATE_FOUND` (reutiliza las que vienen en la plantilla para
mantener la comunicación con el motor).

## Consejos
- Mantén la lógica pura: evita variables globales fuera de las estructuras
  pedidas y céntrate en manipular la información del tablero.
- Usa bucles `for` y listas auxiliares para recorrer y modificar el tablero;
  intenta no recurrir a comprensiones complejas para que el código sea más
  legible.
- Valida siempre las coordenadas recibidas; si están fuera del tablero no deben
  producir errores.
- Experimenta con distintos tamaños (`--rows 2 --cols 6`, `--rows 6 --cols 6`,
  etc.) para verificar que tus funciones escalan bien.
- Al final del desarrollo ejecuta varias partidas completas para asegurarte de
  que `has_won` detecta correctamente el final de la partida y que los
  contadores de movimientos y parejas son coherentes.

## Criterios de calidad (bonus)

- Código bien escrito, con anotaciones de tipo respetadas y lógica pura (sin variables
  globales fuera de las estructuras pedidas).
- `ruff` y `pylint` sin errores.
- Uso correcto de las recomendaciones vistas en teoría.
- Se valorará positivamente ampliar el juego (tamaños de tablero, contador de tiempo,
  marcador persistente) siempre que no rompa la API que espera el motor.
