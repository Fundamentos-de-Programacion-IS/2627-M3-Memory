"""Hito M3 — Memory. Estadísticas de las partidas.

Completa las cinco funciones. Este módulo tiene el mismo formato que el examen práctico y
que el Control 2 (que usa datos muy parecidos a éstos, pero no idénticos): un CSV, dos
NamedTuple obligatorias y funciones que leen, filtran, agregan y ordenan esos datos.
NO cambies los nombres de las funciones, sus parámetros ni
los campos de las NamedTuple: el motor usa `lee_partidas` y `ranking` para pintar la
clasificación al terminar una partida.

Puedes añadir todas las funciones auxiliares que quieras. Escribe sus pruebas en
memory_stats_test.py y ejecuta ese módulo para probarlas.
"""

import csv
from datetime import datetime
from typing import NamedTuple, Optional

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


def lee_partidas(ruta: str) -> list:
    """Ejercicio 1."""
    raise NotImplementedError


def ranking(partidas: list, dificultad: Optional[str] = None, n: int = 3) -> list:
    """Ejercicio 2."""
    raise NotImplementedError


def jugador_con_mas_victorias(partidas: list) -> tuple:
    """Ejercicio 3."""
    raise NotImplementedError


def mejor_tiempo_por_tablero(partidas: list) -> dict:
    """Ejercicio 4."""
    raise NotImplementedError


def partidas_por_mes(partidas: list, jugador: Optional[str] = None) -> dict:
    """Ejercicio 5."""
    raise NotImplementedError
