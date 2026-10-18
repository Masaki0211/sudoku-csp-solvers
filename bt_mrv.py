"""Model 1 — BT+MRV: backtracking with minimum-remaining-values cell ordering.

Owner: Masaki Kajikuri
Idea source: Jana et al. [3] (fewest candidates first); Maji & Pal [1] (most-constrained cell first).

Same as BT, except the next cell is the blank cell with the fewest legal values.
Values are still tried in order 1..9. No inference after an assignment.
"""

import time

from .csp_model import SearchStats, parse


def select_mrv_cell(grid: list[int]) -> int | None:
    """Return the blank cell with the fewest legal values (ties: lowest index), or None if full.

    TODO(Masaki): legal values = DIGITS minus values already in the cell's peers.
    """
    raise NotImplementedError


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py.

    TODO(Masaki)
    """
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    raise NotImplementedError
