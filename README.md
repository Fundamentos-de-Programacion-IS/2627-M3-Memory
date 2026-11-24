# Memory-M3
En este tercer hito construiremos un juego de parejas clásico usando `pygame`, y le
añadiremos **estadísticas de las partidas con el mismo formato que el examen práctico y
que el Control 2**. El hito tiene dos partes:

1. **El juego** (`logic_student.py`): la lógica del turno, con listas, diccionarios, bucles
   y condicionales. La parte visual ya está resuelta en un motor.
2. **Las estadísticas** (`memory_stats.py`): un CSV de partidas, dos `NamedTuple`
   obligatorias y cinco funciones que leen, filtran, agregan y ordenan esos datos, más su
   módulo de pruebas. **El Control 2 usa datos de este mismo tipo, muy parecidos a éstos
   pero no idénticos**: lo que practiques aquí es lo que te pedirán ese día.

> **Cómo entregar (curso 26/27).** En el repositorio `2627-M3-Memory` pulsad
> **«Use this template» → Create a new repository** para crear el repositorio del grupo
> (ya no se usa *fork*). Cuando lo tengáis resuelto, comprimid el proyecto en
> `memory-<nombre del grupo>.zip` y subidlo al formulario de ev.us.es.
> **Fecha límite: jueves 10 de diciembre.** Basta con que lo suba una persona del grupo.

## Cómo se evalúa este hito

Este hito **no puntúa por sí solo**. Cumple dos funciones:

- **Derecho a asiento en el Control 2** (martes 15 dic): tienes que haberlo **entregado en
  plazo** y el proyecto tiene que **ejecutarse sin errores**, las dos partes: el juego
  arranca y `memory_stats.py` se importa y su `lee_partidas` lee `data/partidas.csv`. Se
  comprueba entrega por entrega: si no se cumple, no cuenta como entregada y no hay asiento.
- **Bonus**: el conjunto de los tres hitos puede aportar hasta **+0,5** sobre la nota de
  teoría por calidad y extras, según la rúbrica común.

La nota de teoría sale de los **dos controles individuales de laboratorio**
(martes 24 nov y martes 15 dic), de 110 minutos cada uno y con el mismo formato que el
examen práctico de enero. El Control 2 se plantea **sobre los datos de este hito**: un CSV
de partidas y unas `NamedTuple` muy parecidos a los de aquí, con otras preguntas. Cuanto mejor entiendas
el código que has escrito aquí, menos te costará el control.

> **Lo que pone la nota son los controles.** Este hito no da nota por sí solo: es la llave para
> poder presentarte a ellos.

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
   python game.py --rows 4 --cols 4 --jugador "Tu Nombre"
   ```
   Ajusta `--rows` y `--cols` para probar diferentes tamaños (recuerda que el
   número total de casillas debe ser par). Con `--jugador` eliges el nombre con el que se
   guardan tus partidas.

## Contexto
En el juego, tu trabajo es la lógica del turno: decidir qué cartas se pueden descubrir y
comprobar si hay pareja. La interfaz (`memory_engine.py`) pinta el tablero, lanza el bucle
principal y llama a tus funciones de `logic_student.py`. No hay clases: sólo listas,
diccionarios, tuplas, bucles y condicionales.

Cada partida que juegas queda guardada: el motor añade una línea a `data/mis_partidas.csv`
(también si la abandonas a medias). Y cuando completas el tablero, el motor llama a **tus**
funciones `lee_partidas` y `ranking` de `memory_stats.py` para pintar la clasificación de
tu dificultad. Mientras no las tengas hechas, el juego funciona igual y lo avisa en ese
panel.

## Ficheros en esta carpeta
- `memory_engine.py`: motor gráfico listo para usar. **No se modifica.**
- `game.py`: punto de entrada que conecta el motor con tu lógica y tus estadísticas.
- `logic_student.py`: la lógica del juego (dos funciones marcadas con `TODO`).
- `memory_stats.py`: las cinco funciones de estadísticas que debes completar.
- `memory_stats_test.py`: el módulo de pruebas de las estadísticas, que escribes tú.
- `data/partidas.csv`: partidas de ejemplo. **No lo modifiques**: los resultados esperados
  de este enunciado salen de él.
- `data/mis_partidas.csv`: lo crea el motor con tus partidas, con las mismas columnas.
- `PRUEBAS.md`: casos mínimos para comprobar las dos partes.

# Parte 1 · El juego

## Cómo es una partida
Una partida es un diccionario con estas claves (están también al principio de
`logic_student.py`):

| Clave | Contenido |
|---|---|
| `"tablero"` | lista de filas; cada fila es una lista de cartas |
| `"pendientes"` | posiciones `(fila, columna)` descubiertas en este turno (como mucho dos) |
| `"movimientos"` | turnos resueltos |
| `"parejas"` | parejas encontradas |
| `"total_parejas"` | parejas que hay en el tablero |
| `"filas"`, `"columnas"` | tamaño del tablero |

Cada carta es un diccionario `{"simbolo": str, "estado": str}`. El estado es siempre
una de las constantes `OCULTA`, `VISIBLE` o `ENCONTRADA`: úsalas tal cual, porque el
motor las lee para pintar las cartas.

## Ejercicios del juego
`crea_baraja(filas, columnas)`, `crea_partida(filas, columnas)` y `ha_ganado(partida)`
**te las damos hechas**. Léelas antes de empezar: son un buen ejemplo de lo que te pedimos
en las otras dos, y `crea_partida` te enseña cómo está construido el tablero.

Completa estas dos. **No cambies sus nombres, sus parámetros ni las claves de los
diccionarios**: el motor las usa tal cual.

1. **`descubre_carta(partida, fila, columna)`**: si la posición está dentro del
   tablero, la carta está oculta y aún no hay dos pendientes, la pone visible, añade la
   posición a `"pendientes"` y devuelve `True`. En cualquier otro caso devuelve `False`
   sin cambiar nada.
2. **`resuelve_turno(partida)`**: con las dos cartas pendientes, si son pareja pasan a
   encontradas y suma una pareja; si no, vuelven a ocultas. En los dos casos suma un
   movimiento y vacía `"pendientes"`. Devuelve `True` si eran pareja. Lanza `ValueError`
   si no hay exactamente dos cartas pendientes.

Antes de abrir el juego, ejecuta `python logic_student.py`: el bloque del final prueba
tus funciones sin ventana.

# Parte 2 · Las estadísticas

Esta parte tiene **el formato del examen práctico y del Control 2**: implementas las
funciones en `memory_stats.py` y escribes sus pruebas en `memory_stats_test.py`.

## Los datos

`data/partidas.csv` contiene partidas del juego Memory, en UTF-8 y con cabecera.
**No está ordenado por fecha.**

```
id_partida,jugador,fecha,filas,columnas,movimientos,parejas,segundos,dificultad
P001,Clara Ibáñez,2026-11-04 21:07,6,6,25,18,210,DIFICIL
P002,Félix Marín,2026-09-08 09:46,2,6,17,6,137,FACIL
```

- `fecha` está en formato `YYYY-MM-DD HH:MM`.
- `filas` y `columnas` describen el tablero; el número total de parejas de un tablero
  es `filas * columnas // 2`.
- `movimientos` es el número de turnos jugados y `parejas` el número de parejas encontradas.
- `dificultad` sólo puede valer `FACIL`, `MEDIA` o `DIFICIL`.

Una partida está **terminada** cuando `parejas` coincide con el total de parejas de su
tablero. Las que no lo están son partidas abandonadas a medias. Lo necesitarás en varios
ejercicios: **te conviene escribir una función auxiliar `esta_terminada(partida)`**.

## NamedTuple obligatorias

Ya vienen escritas en `memory_stats.py`:

```python
Tablero = NamedTuple("Tablero", [
    ("filas", int),
    ("columnas", int),
])

Partida = NamedTuple("Partida", [
    ("id_partida", str),
    ("jugador", str),
    ("fecha", datetime),
    ("tablero", Tablero),
    ("movimientos", int),
    ("parejas", int),
    ("segundos", int),
    ("dificultad", str),
])
```

## Las pruebas

Como en el examen, **las pruebas las escribes tú**: en `memory_stats_test.py`, una función
de prueba por ejercicio (`test_lee_partidas`, `test_ranking`…), llamada con los parámetros
adecuados para que imprima los **resultados esperados** que acompañan a cada ejercicio.
Ejecuta `python memory_stats_test.py` desde la carpeta del proyecto: las pruebas leen
`./data/partidas.csv`.

## Ejercicios de estadísticas

### 1. `lee_partidas(ruta) -> list[Partida]`

Lee el CSV de `ruta` y devuelve la lista de partidas, en el orden del fichero. Salta la
cabecera, convierte cada campo a su tipo y agrupa `filas` y `columnas` dentro de un
`Tablero`.

**Resultados esperados:**

<!-- esperados:lee_partidas -->
```text
TEST lee_partidas
Número de partidas leídas: 73

Las dos primeras partidas son:
Partida(id_partida='P001', jugador='Clara Ibáñez', fecha=datetime.datetime(2026, 11, 4, 21, 7), tablero=Tablero(filas=6, columnas=6), movimientos=25, parejas=18, segundos=210, dificultad='DIFICIL')
Partida(id_partida='P002', jugador='Félix Marín', fecha=datetime.datetime(2026, 9, 8, 9, 46), tablero=Tablero(filas=2, columnas=6), movimientos=17, parejas=6, segundos=137, dificultad='FACIL')

Las dos últimas partidas son:
Partida(id_partida='P072', jugador='Darío Núñez', fecha=datetime.datetime(2026, 9, 21, 11, 40), tablero=Tablero(filas=2, columnas=4), movimientos=4, parejas=4, segundos=38, dificultad='FACIL')
Partida(id_partida='P073', jugador='Gala Ortiz', fecha=datetime.datetime(2026, 10, 30, 21, 57), tablero=Tablero(filas=4, columnas=5), movimientos=14, parejas=2, segundos=123, dificultad='MEDIA')
```
<!-- /esperados -->

### 2. `ranking(partidas, dificultad=None, n=3) -> list[tuple[str, int, int]]`

Devuelve una lista de tuplas `(jugador, movimientos, segundos)` con las `n` mejores
partidas **terminadas**: las de **menos movimientos**. Si dos partidas empatan en
movimientos va antes la de **menos segundos**, y si el empate sigue, **la más antigua**.
Si `dificultad` no es `None`, sólo se tienen en cuenta las partidas de esa dificultad. Si
hay menos de `n` partidas, se devuelven las que haya.

Es la función que usa el juego para pintar la clasificación.

**Resultados esperados:**

<!-- esperados:ranking -->
```text
TEST ranking
Las 3 mejores partidas de dificultad None son:
Emma Soto con 4 movimientos en 31 segundos.
Darío Núñez con 4 movimientos en 38 segundos.
Félix Marín con 7 movimientos en 44 segundos.

TEST ranking
Las 3 mejores partidas de dificultad DIFICIL son:
Aitana Rey con 25 movimientos en 151 segundos.
Aitana Rey con 25 movimientos en 201 segundos.
Clara Ibáñez con 25 movimientos en 210 segundos.

TEST ranking
Las 5 mejores partidas de dificultad FACIL son:
Emma Soto con 4 movimientos en 31 segundos.
Darío Núñez con 4 movimientos en 38 segundos.
Félix Marín con 7 movimientos en 44 segundos.
Gala Ortiz con 7 movimientos en 44 segundos.
Aitana Rey con 8 movimientos en 73 segundos.
```
<!-- /esperados -->

### 3. `jugador_con_mas_victorias(partidas) -> tuple[str, int]`

Devuelve `(jugador, victorias)` del jugador que **más partidas ha terminado**. Si dos
jugadores empatan, gana el que va antes en **orden alfabético**. Si no hay ninguna partida
terminada, devuelve `(None, 0)`.

**Resultados esperados:**

<!-- esperados:jugador_con_mas_victorias -->
```text
TEST jugador_con_mas_victorias
El jugador con más victorias es Aitana Rey con 11 partidas terminadas.

TEST jugador_con_mas_victorias
El jugador con más victorias es None con 0 partidas terminadas.
```
<!-- /esperados -->

### 4. `mejor_tiempo_por_tablero(partidas) -> dict[Tablero, tuple[str, int]]`

Devuelve un diccionario que asocia a cada tablero su **mejor tiempo**: la tupla
`(jugador, segundos)` de la partida **terminada** más rápida jugada en ese tablero. Las
partidas sin terminar no cuentan, aunque duren menos, y un tablero en el que nadie ha
terminado no aparece. Si dos partidas terminadas empatan en segundos, el mejor tiempo es
de **la más antigua**.

**Resultados esperados:**

<!-- esperados:mejor_tiempo_por_tablero -->
```text
TEST mejor_tiempo_por_tablero
En el tablero 2x4 el mejor tiempo es de Emma Soto con 31 segundos.
En el tablero 2x6 el mejor tiempo es de Aitana Rey con 47 segundos.
En el tablero 3x4 el mejor tiempo es de Félix Marín con 44 segundos.
En el tablero 4x4 el mejor tiempo es de Aitana Rey con 91 segundos.
En el tablero 4x5 el mejor tiempo es de Gala Ortiz con 143 segundos.
En el tablero 6x6 el mejor tiempo es de Aitana Rey con 151 segundos.
```
<!-- /esperados -->

### 5. `partidas_por_mes(partidas, jugador=None) -> dict[str, int]`

Devuelve un diccionario que asocia cada mes, con el formato `'YYYY-MM'`, con el **número de
partidas jugadas** ese mes, terminadas o no. Si `jugador` no es `None`, sólo se cuentan las
partidas de ese jugador. Un mes sin partidas no aparece.

**Resultados esperados:**

<!-- esperados:partidas_por_mes -->
```text
TEST partidas_por_mes
Las partidas por mes del jugador None son:
2026-09: 26
2026-10: 31
2026-11: 16

TEST partidas_por_mes
Las partidas por mes del jugador Bruno Salas son:
2026-09: 2
2026-11: 4

TEST partidas_por_mes
Las partidas por mes del jugador Nadie son:
```
<!-- /esperados -->

## Consejos
- No uses variables globales: todo lo que cambia durante la partida vive en el
  diccionario `partida`.
- Usa bucles `for` y listas auxiliares para recorrer y modificar el tablero;
  intenta no recurrir a comprensiones complejas para que el código sea más
  legible.
- Valida siempre las coordenadas recibidas; si están fuera del tablero no deben
  producir errores.
- Experimenta con distintos tamaños (`--rows 2 --cols 6`, `--rows 6 --cols 6`,
  etc.) para verificar que tus funciones escalan bien.
- Al final del desarrollo ejecuta varias partidas completas para asegurarte de
  que los contadores de movimientos y parejas son coherentes y de que tus partidas
  aparecen en `data/mis_partidas.csv` y en la clasificación.
- En las estadísticas, todo se puede resolver con diccionarios normales (`get`, `in`) y
  `sorted` con `key`; no hacen falta `Counter` ni `defaultdict`.
- No entregues las estadísticas sin haber ejecutado `memory_stats_test.py`: un módulo que
  no se puede importar no concede asiento.

## Criterios de calidad (bonus)

- Código bien escrito, con anotaciones de tipo respetadas y lógica pura (sin variables
  globales fuera de las estructuras pedidas).
- `ruff` y `pylint` sin errores.
- Uso correcto de las recomendaciones vistas en teoría.
- Se valorará positivamente ampliar el juego (tamaños de tablero, contador de tiempo,
  marcador persistente) siempre que no rompa la API que espera el motor.
