"""Punto de entrada para lanzar el juego usando la lógica y las estadísticas del alumnado."""
from __future__ import annotations

import argparse

from memory_engine import MemoryUI
import logic_student
import memory_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Memory M3")
    parser.add_argument("--rows", type=int, default=4, help="Número de filas del tablero")
    parser.add_argument("--cols", type=int, default=4, help="Número de columnas del tablero")
    parser.add_argument("--jugador", default="Anónimo",
                        help="Nombre con el que se guardan tus partidas")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ui = MemoryUI(logic_student, memory_stats, jugador=args.jugador)
    ui.run(rows=args.rows, cols=args.cols)


if __name__ == "__main__":
    main()
