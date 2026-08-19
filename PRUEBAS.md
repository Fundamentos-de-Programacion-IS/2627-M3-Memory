# Comprobaciones visibles de M3

Prueba las funciones de lógica antes de abrir la interfaz gráfica:

- `build_symbol_pool(2, 4)` crea ocho símbolos, cada uno exactamente dos veces;
- dimensiones impares o no positivas se rechazan según el contrato de la plantilla;
- no se puede revelar una posición fuera del tablero ni una carta ya visible;
- nunca hay más de dos cartas pendientes;
- una pareja queda encontrada y dos símbolos distintos vuelven a ocultarse;
- cada resolución incrementa una vez el número de movimientos;
- `has_won` sólo es verdadero al encontrar todas las parejas.

Después juega partidas de 2×4, 2×6 y 4×4 para comprobar la integración con el motor.
