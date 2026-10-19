"""Model 3 — BT+MRV+MAC: MRV ordering plus maintained arc consistency (AC-3).

Owner: Aoto Kubota
Idea source: Maji & Pal [1] (constraint propagation); Jana et al. [3] (per-cell candidate lists).

Like BT+MRV+FC, but after each assignment run AC-3 on the arcs (Y, X) for every
unassigned peer Y of the assigned cell X. When a domain shrinks, add its neighbors'
arcs back to the queue, so pruning spreads beyond direct peers.
If any domain becomes empty, the assignment fails. Restore all removals on backtrack.
"""

import time
from collections import deque

from .csp_model import SearchStats, parse, initial_domains, peers


def revise(domains: list[set[int]], xi: int, xj: int) -> list[int]:
    """Remove values from domains[xi] that have no support in domains[xj] (the not-equal constraint).

    For not-equal, a value v in Xi loses support only when domains[xj] == {v}.
    Return the list of removed values.

    TODO(Aoto)
    """
    raise NotImplementedError


def ac3(domains: list[set[int]], queue: deque) -> list[tuple[int, int]] | None:
    """Run AC-3 from the given arc queue.

    Return all (cell, value) removals so they can be restored, or None on a wipe-out.

    TODO(Aoto)
    """
    raise NotImplementedError


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py.

    TODO(Aoto)
    """
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    raise NotImplementedError
