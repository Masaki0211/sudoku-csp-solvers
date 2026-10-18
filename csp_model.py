"""Shared CSP model for 9x9 Sudoku. Every solver builds on this file.

Owner: Masaki Kajikuri

Factored representation:
    variables   81 cells, indexed 0..80 (row = i // 9, col = i % 9)
    domains     set of possible digits for each cell; a clue has a single value
    constraints 27 all-different units (9 rows, 9 cols, 9 boxes);
                each cell has 20 neighbors (peers) it must differ from
"""

from dataclasses import dataclass

DIGITS = frozenset(range(1, 10))


@dataclass
class SearchStats:
    """Counters every solver must fill in the same way, so results are comparable."""
    nodes: int = 0          # one node = one value tried for one variable
    backtracks: int = 0     # one backtrack = undoing an assignment after all its values failed
    seconds: float = 0.0
    solved: bool = False
    timed_out: bool = False


def parse(puzzle: str) -> list[int]:
    """Turn an 81-character string into a list of 81 ints, 0 for blank.

    TODO(Masaki): accept '.' and '0' as blanks; check length is 81.
    """
    raise NotImplementedError


def peers(cell: int) -> frozenset[int]:
    """Return the 20 cells that share a row, column, or box with `cell`.

    TODO(Masaki): precompute once for all 81 cells (e.g., a module-level table).
    """
    raise NotImplementedError


def initial_domains(grid: list[int]) -> list[set[int]]:
    """Domain for every cell: {clue} for givens, otherwise DIGITS minus peers' clues.

    TODO(Masaki)
    """
    raise NotImplementedError


def is_consistent(grid: list[int], cell: int, value: int) -> bool:
    """True if no peer of `cell` already holds `value`.

    TODO(Masaki)
    """
    raise NotImplementedError


def is_valid_solution(grid: list[int], puzzle: list[int]) -> bool:
    """True if `grid` is complete, keeps every clue, and every unit holds 1..9 once.

    TODO(Masaki): used by tests and by experiments/run_all.py to check every result.
    """
    raise NotImplementedError
