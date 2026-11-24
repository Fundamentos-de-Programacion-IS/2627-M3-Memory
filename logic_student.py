"""Hito M3 — Memory (juego de parejas).

Completa las dos funciones marcadas con TODO (`descubre_carta` y `resuelve_turno`). El
motor gráfico (`memory_engine.py`) las llama por su nombre: NO cambies los nombres de las funciones, sus parámetros ni las
claves de los diccionarios.

Puedes añadir todas las funciones auxiliares que quieras.

Cómo es una partida
-------------------
Una partida es un diccionario con estas claves:

- "tablero": lista de filas; cada fila es una lista de cartas.
- "pendientes": lista con las posiciones (fila, columna) de las cartas descubiertas
  en el turno actual (como mucho dos).
- "movimientos": número de turnos resueltos.
- "parejas": número de parejas encontradas.
- "total_parejas": número de parejas que hay en el tablero.
- "filas" y "columnas": tamaño del tablero.

Cada carta es un diccionario {"simbolo": str, "estado": str}, y su estado es siempre
una de las tres constantes de abajo.
"""

import random

OCULTA = "oculta"
VISIBLE = "visible"
ENCONTRADA = "encontrada"

SIMBOLOS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def crea_baraja(filas: int, columnas: int) -> list:
    """Lista de filas*columnas símbolos barajados: cada símbolo aparece exactamente dos veces.

    Lanza `ValueError` si `filas` o `columnas` no son positivas, si `filas*columnas` es
    impar o si no hay símbolos suficientes.

    (Esta te la damos hecha: úsala en `crea_partida`.)
    """
    if filas <= 0 or columnas <= 0:
        raise ValueError("El tablero necesita al menos una fila y una columna")
    if filas * columnas % 2 != 0:
        raise ValueError("El tablero debe tener un número par de casillas")
    num_parejas = filas * columnas // 2
    if num_parejas > len(SIMBOLOS):
        raise ValueError("No hay símbolos suficientes para un tablero tan grande")

    baraja = []
    for i in range(num_parejas):
        baraja.append(SIMBOLOS[i])
        baraja.append(SIMBOLOS[i])
    random.shuffle(baraja)
    return baraja


def crea_partida(filas: int, columnas: int) -> dict:
    """Diccionario con el estado inicial de una partida de `filas` x `columnas`.

    - "tablero": `filas` listas de `columnas` cartas. Las cartas se reparten en el orden
      de `crea_baraja`, fila a fila, y todas empiezan en estado OCULTA.
    - "pendientes": lista vacía.
    - "movimientos" y "parejas": 0.
    - "total_parejas": la mitad del número de cartas.
    - "filas" y "columnas": los valores recibidos.

    Lanza `ValueError` en los mismos casos que `crea_baraja`.

    (Esta también te la damos hecha: fíjate en cómo se construye el tablero.)
    """
    baraja = crea_baraja(filas, columnas)
    tablero = []
    siguiente = 0
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append({"simbolo": baraja[siguiente], "estado": OCULTA})
            siguiente += 1
        tablero.append(fila)
    return {
        "tablero": tablero,
        "pendientes": [],
        "movimientos": 0,
        "parejas": 0,
        "total_parejas": filas * columnas // 2,
        "filas": filas,
        "columnas": columnas,
    }


def descubre_carta(partida: dict, fila: int, columna: int) -> bool:
    """Descubre la carta de (`fila`, `columna`) y la añade a "pendientes".

    Devuelve True si la carta estaba OCULTA y ha pasado a VISIBLE. Devuelve False, sin
    cambiar nada, si:
    - la posición está fuera del tablero,
    - la carta no está OCULTA (ya está visible o encontrada), o
    - ya hay dos cartas pendientes.
    """
    # TODO
    raise NotImplementedError


def resuelve_turno(partida: dict) -> bool:
    """Resuelve el turno con las dos cartas pendientes. Devuelve True si son pareja.

    - Si tienen el mismo símbolo, las dos pasan a ENCONTRADA y "parejas" sube en 1.
    - Si no, las dos vuelven a OCULTA.
    - En los dos casos "movimientos" sube en 1 y "pendientes" queda vacía.

    Lanza `ValueError` si no hay exactamente dos cartas pendientes.
    """
    # TODO
    raise NotImplementedError


def ha_ganado(partida: dict) -> bool:
    """True si ya se han encontrado todas las parejas del tablero.

    (Esta te la damos hecha.)
    """
    return partida["parejas"] == partida["total_parejas"]


if __name__ == "__main__":
    # Pruebas rápidas sin ventana: ejecuta  python logic_student.py
    partida = crea_partida(2, 4)
    for fila in partida["tablero"]:
        print([carta["simbolo"] for carta in fila])
    print(descubre_carta(partida, 0, 0))   # True
    print(descubre_carta(partida, 0, 0))   # False: ya está visible
    print(descubre_carta(partida, 9, 9))   # False: fuera del tablero
    print(descubre_carta(partida, 0, 1))   # True
    print(resuelve_turno(partida), partida["movimientos"], partida["parejas"])
    print(ha_ganado(partida))              # False
