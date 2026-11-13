"""Model 0 — BT: plain chronological backtracking (baseline).

Owner: Masaki Kajikuri
Idea source: Kamal et al. [2] (backtracking as the strongest baseline); Russell & Norvig, Ch. 6.

Cells are tried in fixed order (0..80); values 1..9 in order.
A value is placed only if is_consistent() allows it. No ordering heuristic, no inference.
"""

from .csp_model import Deadline, SearchStats, SearchTimeout, is_consistent, parse


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats)."""
    stats = SearchStats()
    deadline = Deadline(time_limit)
    grid = parse(puzzle)
    blanks = [i for i, v in enumerate(grid) if v == 0]

    def search(k: int) -> bool:
        if k == len(blanks):
            return True
        cell = blanks[k]
        for value in range(1, 10):
            deadline.check()
            if is_consistent(grid, cell, value):
                grid[cell] = value
                stats.nodes += 1
                if search(k + 1):
                    return True
                grid[cell] = 0
                stats.backtracks += 1
        return False

    try:
        stats.solved = search(0)
    except SearchTimeout:
        stats.timed_out = True
    stats.seconds = deadline.elapsed()
    return (grid if stats.solved else None), stats
