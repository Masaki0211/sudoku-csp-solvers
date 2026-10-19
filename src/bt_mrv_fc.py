"""Model 2 — BT+MRV+FC: MRV ordering plus forward checking.

Owner: Zachary Lenfesty
Idea source: Maji & Pal [1] (forward checking as an improvement to backtracking).

Keeps a domain (candidate set) for every blank cell.
After assigning value v to cell X, remove v from the domain of every unassigned peer of X.
If any peer's domain becomes empty, this assignment fails immediately (no deeper search).
On backtrack, restore exactly the values that were removed.
"""

import time

from .csp_model import SearchStats, parse, initial_domains, peers


def forward_check(domains: list[set[int]], cell: int, value: int) -> list[tuple[int, int]] | None:
    """Remove `value` from unassigned peers of `cell`.

    Return the list of (peer, value) pairs removed so they can be restored,
    or None if some peer's domain became empty.

    TODO(Zachary)
    """
    raise NotImplementedError


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py.

    TODO(Zachary): choose cells by smallest current domain (MRV over domains).
    """
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    raise NotImplementedError
