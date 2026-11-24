# Comprobaciones visibles de M3

## Parte 1 · El juego

Prueba las funciones de lógica antes de abrir la interfaz gráfica (el bloque final de
`logic_student.py` es un buen punto de partida):

- `descubre_carta` devuelve `False` para una posición fuera del tablero, para una carta
  ya visible o encontrada y cuando ya hay dos cartas pendientes;
- nunca hay más de dos cartas en `"pendientes"`;
- `resuelve_turno` deja una pareja en `ENCONTRADA` y vuelve a ocultar dos símbolos
  distintos; en ambos casos suma un movimiento y vacía `"pendientes"`;
- `resuelve_turno` lanza `ValueError` si no hay exactamente dos cartas pendientes.

Después juega partidas de 2×4, 2×6 y 4×4 para comprobar la integración con el motor.

## Parte 2 · Las estadísticas

Escribe en `memory_stats_test.py` una función de prueba por ejercicio y comprueba que
`python memory_stats_test.py` imprime los «Resultados esperados» del README. Además:

- `ranking(partidas, "FACIL", 5)` ordena bien los empates: a igualdad de movimientos, menos
  segundos; a igualdad de segundos, la partida más antigua;
- `ranking([])` y `partidas_por_mes([])` devuelven una lista y un diccionario vacíos;
- `jugador_con_mas_victorias` resuelve un empate por orden alfabético: los datos de ejemplo
  no traen ninguno, así que pruébalo con una lista pequeña de `Partida` hecha a mano;
- en `mejor_tiempo_por_tablero`, la partida más rápida del tablero 6×6 no está terminada y
  no debe salir;
- al completar una partida en el juego, la tuya aparece en `data/mis_partidas.csv` y, si
  es de las mejores de su dificultad, en la clasificación.
