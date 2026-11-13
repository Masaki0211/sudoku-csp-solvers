"""Model 1 — BT+MRV: backtracking with minimum-remaining-values cell ordering.

Owner: Masaki Kajikuri
Idea source: Jana et al. [3] (fewest candidates first); Maji & Pal [1] ("most constrained first").

Same as BT, except the next cell is the blank cell with the fewest legal values.
Legal values are recomputed from the grid at each step; there is no stored domain
and no inference after an assignment (that is what FC and MAC add).
A blank cell with zero legal values is picked first, so dead ends fail at once.
"""

from .csp_model import DIGITS, PEERS, Deadline, SearchStats, SearchTimeout, parse


def select_mrv_cell(grid: list[int]) -> tuple[int, set[int]] | None:
    """Return (cell, legal values) for the blank cell with the fewest legal values.

    Ties go to the lowest index. Returns None if the grid is full.
    """
    best_cell, best_vals = None, None
    for cell, v in enumerate(grid):
        if v:
            continue
        vals = set(DIGITS) - {grid[p] for p in PEERS[cell]}
        if best_vals is None or len(vals) < len(best_vals):
            best_cell, best_vals = cell, vals
            if not vals:          # dead end: no need to look further
                break
    return None if best_cell is None else (best_cell, best_vals)


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Counting follows csp_model.py."""
    stats = SearchStats()
    deadline = Deadline(time_limit, every=64)
    grid = parse(puzzle)

    def search() -> bool:
        choice = select_mrv_cell(grid)
        if choice is None:
            return True
        cell, values = choice
        for value in sorted(values):
            deadline.check()
            grid[cell] = value
            stats.nodes += 1
            if search():
                return True
            grid[cell] = 0
            stats.backtracks += 1
        return False

    try:
        stats.solved = search()
    except SearchTimeout:
        stats.timed_out = True
    stats.seconds = deadline.elapsed()
    return (grid if stats.solved else None), stats
