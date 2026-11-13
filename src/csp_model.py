"""Shared CSP model for 9x9 Sudoku. Every solver builds on this file.

Owner: Masaki Kajikuri

Factored representation:
    variables   81 cells, indexed 0..80 (row = i // 9, col = i % 9)
    domains     set of possible digits for each cell; a clue has a single value
    constraints 27 all-different units (9 rows, 9 cols, 9 boxes);
                each cell has 20 neighbors (peers) it must differ from

Counting rules (every solver must follow these so results are comparable):
    node       one assignment of a value to a cell that passes the solver's own
               check (a child created in the search tree)
    backtrack  one assignment undone because the search below it failed
"""

import time
from dataclasses import dataclass

DIGITS = frozenset(range(1, 10))
N = 81


def _build_tables():
    rows = [[r * 9 + c for c in range(9)] for r in range(9)]
    cols = [[r * 9 + c for r in range(9)] for c in range(9)]
    boxes = [
        [(br * 3 + r) * 9 + bc * 3 + c for r in range(3) for c in range(3)]
        for br in range(3)
        for bc in range(3)
    ]
    units = rows + cols + boxes
    peer_table = []
    for cell in range(N):
        p = set()
        for unit in units:
            if cell in unit:
                p.update(unit)
        p.discard(cell)
        peer_table.append(frozenset(p))
    return units, boxes, tuple(peer_table)


UNITS, BOXES, PEERS = _build_tables()


@dataclass
class SearchStats:
    """Counters every solver must fill in the same way, so results are comparable."""
    nodes: int = 0          # one consistent assignment (see module docstring)
    backtracks: int = 0     # one assignment undone after the search below it failed
    seconds: float = 0.0
    solved: bool = False
    timed_out: bool = False


class SearchTimeout(Exception):
    """Raised inside a solver when the time limit is reached."""


class Deadline:
    """Cheap time-limit check: looks at the clock only every `every` calls."""

    def __init__(self, time_limit: float, every: int = 256):
        self.start = time.perf_counter()
        self.end = self.start + time_limit
        self.every = every
        self._count = 0

    def check(self) -> None:
        self._count += 1
        if self._count % self.every == 0 and time.perf_counter() > self.end:
            raise SearchTimeout

    def elapsed(self) -> float:
        return time.perf_counter() - self.start


def parse(puzzle: str) -> list[int]:
    """Turn an 81-character string into a list of 81 ints, 0 for blank ('.' or '0')."""
    puzzle = puzzle.strip()
    if len(puzzle) != N:
        raise ValueError(f"puzzle must have 81 characters, got {len(puzzle)}")
    grid = []
    for ch in puzzle:
        if ch in ".0":
            grid.append(0)
        elif ch.isdigit():
            grid.append(int(ch))
        else:
            raise ValueError(f"unexpected character {ch!r} in puzzle")
    return grid


def peers(cell: int) -> frozenset[int]:
    """Return the 20 cells that share a row, column, or box with `cell`."""
    return PEERS[cell]


def legal_values(grid: list[int], cell: int) -> set[int]:
    """Digits not used by any peer of `cell` in the current grid."""
    return set(DIGITS) - {grid[p] for p in PEERS[cell]}


def initial_domains(grid: list[int]) -> list[set[int]]:
    """Domain for every cell: {clue} for givens, otherwise DIGITS minus peers' clues."""
    return [{v} if v else legal_values(grid, i) for i, v in enumerate(grid)]


def is_consistent(grid: list[int], cell: int, value: int) -> bool:
    """True if no peer of `cell` already holds `value`."""
    return all(grid[p] != value for p in PEERS[cell])


def is_valid_solution(grid: list[int], puzzle: list[int]) -> bool:
    """True if `grid` is complete, keeps every clue, and every unit holds 1..9 once."""
    if grid is None or len(grid) != N:
        return False
    if any(p and g != p for g, p in zip(grid, puzzle)):
        return False
    return all({grid[i] for i in unit} == DIGITS for unit in UNITS)


def to_string(grid: list[int]) -> str:
    """Inverse of parse() for a solved or partial grid (0 shown as '.')."""
    return "".join(str(v) if v else "." for v in grid)
