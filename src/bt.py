"""Model 0 — BT: plain chronological backtracking (baseline).

Owner: Masaki Kajikuri

Cells are tried in fixed order (0..80); values 1..9 in order.
A value is placed only if is_consistent() allows it. No ordering heuristic, no inference.
"""

import time

from .csp_model import SearchStats, parse, is_consistent


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats).

    TODO(Masaki):
      - count stats.nodes once per value tried
      - count stats.backtracks once each time a cell is reset to 0 after all values fail
      - stop and set stats.timed_out when time.perf_counter() passes the limit
    """
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    raise NotImplementedError
