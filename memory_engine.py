"""Motor gráfico simple para el hito Memory-M3.

Este archivo no debe modificarse durante la entrega: contiene la capa de
interfaz que pinta el tablero utilizando `pygame` y delega toda la lógica en
las funciones del módulo de lógica del alumnado (`logic_student.py`), que se
inyecta al instanciar ``MemoryUI``.

Además lleva el registro de partidas: cada partida que se juega se añade a
`data/mis_partidas.csv` con las mismas columnas que `data/partidas.csv`, y al completar
el tablero se pinta la clasificación que calculan `lee_partidas` y `ranking`, las
funciones del módulo de estadísticas del alumnado (`memory_stats.py`).
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple

import pygame

GameState = Dict[str, Any]
Position = Tuple[int, int]

DATA = Path(__file__).resolve().parent / "data"
HISTORICO = DATA / "partidas.csv"          # partidas de ejemplo: no se modifica
MIS_PARTIDAS = DATA / "mis_partidas.csv"   # aquí guarda el motor las tuyas
CABECERA = ["id_partida", "jugador", "fecha", "filas", "columnas", "movimientos",
            "parejas", "segundos", "dificultad"]


def dificultad_de(rows: int, cols: int) -> str:
    """FACIL hasta 12 cartas, MEDIA hasta 20 y DIFICIL a partir de ahí."""
    cartas = rows * cols
    if cartas <= 12:
        return "FACIL"
    if cartas <= 20:
        return "MEDIA"
    return "DIFICIL"


class MemoryUI:
    """Encapsula la parte visual del juego de memoria.

    El alumnado solo debe tocar el módulo de lógica. Este motor asume que dicho
    módulo expone las constantes ``OCULTA``, ``VISIBLE`` y ``ENCONTRADA`` además
    de las funciones ``crea_partida``, ``descubre_carta``, ``resuelve_turno`` y
    ``ha_ganado``. Del módulo de estadísticas usa ``lee_partidas`` y ``ranking``; si
    todavía no están hechas, el juego funciona igual y avisa en lugar de la clasificación.
    """

    BG_COLOR = (12, 17, 29)
    GRID_COLOR = (18, 98, 151)
    TEXT_COLOR = (235, 239, 243)
    HIDDEN_CARD = (55, 71, 79)
    VISIBLE_CARD = (197, 202, 233)
    FOUND_CARD = (67, 160, 71)

    CARD_MARGIN = 12
    CARD_SIZE = 110
    HEADER_HEIGHT = 90
    FPS = 60
    REVEAL_DELAY_MS = 900
    RANKING_SIZE = 5

    def __init__(self, logic_module: ModuleType, stats_module: Optional[ModuleType] = None,
                 jugador: str = "Anónimo") -> None:
        self.logic = logic_module
        self.stats = stats_module
        self.jugador = jugador.strip() or "Anónimo"
        self.start_ticks: int = 0
        self.final_seconds: Optional[int] = None
        self.recorded = False
        self.ranking_lines: List[str] = []
        self.small_font: Optional[pygame.font.Font] = None
        self.state_hidden = getattr(self.logic, "OCULTA", "oculta")
        self.state_visible = getattr(self.logic, "VISIBLE", "visible")
        self.state_found = getattr(self.logic, "ENCONTRADA", "encontrada")

        self.rows: int = 0
        self.cols: int = 0
        self.game: GameState = {}
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font: Optional[pygame.font.Font] = None
        self.card_font: Optional[pygame.font.Font] = None
        self.lock_until: Optional[int] = None

    # Público -----------------------------------------------------------------
    def run(self, rows: int = 4, cols: int = 4) -> None:
        """Inicializa pygame y ejecuta el bucle principal del juego."""

        if rows * cols % 2 != 0:
            raise ValueError("El tablero debe tener un número par de casillas")

        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 34)
        self.card_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 26)

        width, height = self._compute_window_size(rows, cols)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Memory M3")

        self.rows, self.cols = rows, cols
        self.game = self.logic.crea_partida(rows, cols)
        self.lock_until = None
        self.start_ticks = pygame.time.get_ticks()
        self.final_seconds = None
        self.recorded = False
        self.ranking_lines = []

        running = True
        while running:
            if not self.clock:
                break
            self.clock.tick(self.FPS)
            running = self._handle_events()
            self._update_logic()
            self._draw_scene()

        # Una partida abandonada a medias también cuenta: queda guardada sin terminar.
        if not self.recorded and int(self.game.get("movimientos", 0)) > 0:
            self._save_game()

        pygame.quit()

    # Bucle principal ---------------------------------------------------------
    def _handle_events(self) -> bool:
        assert self.screen is not None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
        return True

    def _handle_click(self, pos: Tuple[int, int]) -> None:
        if self.lock_until is not None:
            return

        board_pos = self._pixel_to_board(pos)
        if board_pos is None:
            return

        row, col = board_pos
        turned = self.logic.descubre_carta(self.game, row, col)
        if not turned:
            return

        pending = self.game.get("pendientes", [])
        if isinstance(pending, list) and len(pending) == 2:
            self.lock_until = pygame.time.get_ticks() + self.REVEAL_DELAY_MS

    def _update_logic(self) -> None:
        if self.lock_until is None:
            return

        now = pygame.time.get_ticks()
        if now < self.lock_until:
            return

        self.logic.resuelve_turno(self.game)
        self.lock_until = None

        if not self.recorded and self.logic.ha_ganado(self.game):
            self._save_game()
            self._load_ranking()

    # Registro de partidas y clasificación -------------------------------------------
    def _seconds(self) -> int:
        if self.final_seconds is not None:
            return self.final_seconds
        return (pygame.time.get_ticks() - self.start_ticks) // 1000

    def _save_game(self) -> None:
        """Añade la partida actual a `data/mis_partidas.csv` (una sola vez)."""
        self.final_seconds = self._seconds()
        self.recorded = True
        try:
            DATA.mkdir(exist_ok=True)
            guardadas = 0
            if MIS_PARTIDAS.exists():
                with open(MIS_PARTIDAS, encoding="utf-8", newline="") as fichero:
                    guardadas = max(0, sum(1 for _ in csv.reader(fichero)) - 1)
            nueva = not MIS_PARTIDAS.exists()
            with open(MIS_PARTIDAS, "a", encoding="utf-8", newline="") as fichero:
                escritor = csv.writer(fichero)
                if nueva:
                    escritor.writerow(CABECERA)
                escritor.writerow([
                    f"M{guardadas + 1:03d}",
                    self.jugador,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    self.rows,
                    self.cols,
                    int(self.game.get("movimientos", 0)),
                    int(self.game.get("parejas", 0)),
                    self.final_seconds,
                    dificultad_de(self.rows, self.cols),
                ])
        except OSError as exc:
            print(f"No se ha podido guardar la partida: {exc}")

    def _load_ranking(self) -> None:
        """Calcula la clasificación con las funciones de `memory_stats.py`."""
        dificultad = dificultad_de(self.rows, self.cols)
        if self.stats is None:
            self.ranking_lines = ["Clasificación no disponible: falta memory_stats.py"]
            return
        try:
            partidas = []
            for ruta in (HISTORICO, MIS_PARTIDAS):
                if ruta.exists():
                    partidas += self.stats.lee_partidas(str(ruta))
            mejores = self.stats.ranking(partidas, dificultad, self.RANKING_SIZE)
            self.ranking_lines = [f"Mejores partidas ({dificultad})"]
            for puesto, (jugador, movimientos, segundos) in enumerate(mejores, start=1):
                self.ranking_lines.append(
                    f"{puesto}. {jugador} - {movimientos} mov. - {segundos} s")
        except NotImplementedError:
            self.ranking_lines = ["Clasificación no disponible:",
                                  "completa lee_partidas y ranking",
                                  "en memory_stats.py"]
        except Exception as exc:  # pylint: disable=broad-except
            # El juego no debe romperse por un fallo en las estadísticas: se avisa y ya.
            print(f"Fallo al calcular la clasificación: {type(exc).__name__}: {exc}")
            self.ranking_lines = ["Clasificación no disponible:",
                                  f"{type(exc).__name__} en memory_stats.py",
                                  "(mira la consola)"]

    # Dibujo ------------------------------------------------------------------
    def _draw_scene(self) -> None:
        if self.screen is None:
            return

        self.screen.fill(self.BG_COLOR)
        self._draw_header()
        self._draw_cards()
        self._draw_ranking()
        pygame.display.flip()

    def _draw_ranking(self) -> None:
        """Panel con la clasificación, sobre el tablero, al completar la partida."""
        if not self.ranking_lines or self.screen is None or self.small_font is None:
            return
        line_height = 26
        width = self.screen.get_width() - 40
        height = line_height * len(self.ranking_lines) + 24
        top = self.HEADER_HEIGHT + 10
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((12, 17, 29, 235))
        self.screen.blit(panel, (20, top))
        pygame.draw.rect(self.screen, self.GRID_COLOR, (20, top, width, height), 2, border_radius=8)
        for i, line in enumerate(self.ranking_lines):
            surface = self.small_font.render(line, True, self.TEXT_COLOR)
            self.screen.blit(surface, (34, top + 12 + i * line_height))

    def _draw_header(self) -> None:
        assert self.screen and self.font
        moves = int(self.game.get("movimientos", 0))
        matches = int(self.game.get("parejas", 0))
        total = int(self.game.get("total_parejas", 0) or (self.rows * self.cols) // 2)

        summary = f"Mov.: {moves}   Parejas: {matches}/{total}   Tiempo: {self._seconds()} s"
        summary_surface = self.font.render(summary, True, self.TEXT_COLOR)
        self.screen.blit(summary_surface, (20, 20))

        if self.logic.ha_ganado(self.game):
            msg = "¡Completado! Pulsa ESC para cerrar"
        else:
            msg = "Haz clic en dos cartas para encontrar parejas"

        msg_surface = self.font.render(msg, True, self.TEXT_COLOR)
        self.screen.blit(msg_surface, (20, 50))

    def _draw_cards(self) -> None:
        assert self.screen and self.card_font
        board: List[List[Dict[str, Any]]] = self.game.get("tablero", [])
        for row_idx, row in enumerate(board):
            for col_idx, card in enumerate(row):
                rect = self._cell_rect(row_idx, col_idx)
                pygame.draw.rect(self.screen, self.GRID_COLOR, rect, border_radius=10)

                inner = rect.inflate(-6, -6)
                state = card.get("estado")
                if state == self.state_found:
                    color = self.FOUND_CARD
                elif state == self.state_visible:
                    color = self.VISIBLE_CARD
                else:
                    color = self.HIDDEN_CARD

                pygame.draw.rect(self.screen, color, inner, border_radius=10)

                if state in (self.state_visible, self.state_found):
                    symbol = str(card.get("simbolo", ""))
                    text_surface = self.card_font.render(symbol, True, self.BG_COLOR)
                    text_rect = text_surface.get_rect(center=inner.center)
                    self.screen.blit(text_surface, text_rect)

    # Helpers -----------------------------------------------------------------
    def _compute_window_size(self, rows: int, cols: int) -> Tuple[int, int]:
        width = cols * self.CARD_SIZE + (cols + 1) * self.CARD_MARGIN
        height = (
            rows * self.CARD_SIZE
            + (rows + 1) * self.CARD_MARGIN
            + self.HEADER_HEIGHT
        )
        return width, height

    def _cell_rect(self, row: int, col: int) -> pygame.Rect:
        x = self.CARD_MARGIN + col * (self.CARD_SIZE + self.CARD_MARGIN)
        y = (
            self.HEADER_HEIGHT
            + self.CARD_MARGIN
            + row * (self.CARD_SIZE + self.CARD_MARGIN)
        )
        return pygame.Rect(x, y, self.CARD_SIZE, self.CARD_SIZE)

    def _pixel_to_board(self, pos: Tuple[int, int]) -> Optional[Position]:
        x, y = pos
        if y < self.HEADER_HEIGHT:
            return None
        board: List[List[Any]] = self.game.get("tablero", [])
        for row_idx, row in enumerate(board):
            for col_idx, _ in enumerate(row):
                if self._cell_rect(row_idx, col_idx).collidepoint(x, y):
                    return row_idx, col_idx
        return None
