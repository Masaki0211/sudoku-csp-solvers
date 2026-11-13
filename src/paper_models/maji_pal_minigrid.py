"""Comparison model from Masaki's paper — minigrid-based backtracking (Maji & Pal [1]).

Owner: Masaki Kajikuri

Reimplementation of the idea in A. K. Maji and R. K. Pal, "Sudoku solver using
minigrid based backtracking," IACC 2014, Sec. III:

  1. Treat the grid as nine 3x3 minigrids instead of 81 cells.
  2. For each minigrid, generate the permutations of its missing digits over its
     blank cells, keeping only those that do not clash with clues in the same
     rows and columns (a permutation tree prunes bad prefixes early).
  3. Backtrack over the minigrids in a fixed sequence, choosing for each one a
     valid permutation that is compatible with the minigrids already filled.

Differences from the paper (stated in the slides):
  - Minigrids are visited in row-major order (0..8); the paper also discusses
    zigzag and spiral sequences.
  - Counting follows csp_model.py, except that one node is one whole-minigrid
    placement rather than one cell, so node counts are reported separately from
    the cell-based solvers. Time and completion rate are directly comparable.
"""

from ..csp_model import BOXES, Deadline, SearchStats, SearchTimeout, parse


def valid_permutations(grid, box, deadline):
    """All placements of a box's missing digits that avoid clues in the same rows/cols."""
    blanks = [i for i in box if grid[i] == 0]
    missing = sorted(set(range(1, 10)) - {grid[i] for i in box if grid[i]})
    row_clues = {r: {grid[r * 9 + c] for c in range(9)} - {0} for r in {i // 9 for i in blanks}}
    col_clues = {c: {grid[r * 9 + c] for r in range(9)} - {0} for c in {i % 9 for i in blanks}}
    allowed = [
        {d for d in missing if d not in row_clues[i // 9] and d not in col_clues[i % 9]}
        for i in blanks
    ]
    perms, chosen, used = [], [], set()

    def extend(k):
        deadline.check()
        if k == len(blanks):
            perms.append(tuple(chosen))
            return
        for d in missing:
            if d in allowed[k] and d not in used:
                used.add(d)
                chosen.append(d)
                extend(k + 1)
                chosen.pop()
                used.discard(d)

    extend(0)
    return blanks, perms, len(missing)


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats).

    Extra attributes on stats: `perm_total` (valid permutations generated over all
    minigrids) and `perm_space` (sum of k! over minigrids before filtering).
    """
    from math import factorial

    stats = SearchStats()
    deadline = Deadline(time_limit, every=64)
    grid = parse(puzzle)
    stats.perm_total = 0
    stats.perm_space = 0

    try:
        tables = []
        for box in BOXES:
            blanks, perms, k = valid_permutations(grid, box, deadline)
            tables.append((blanks, perms))
            stats.perm_total += len(perms)
            stats.perm_space += factorial(k)

        row_used = [{grid[r * 9 + c] for c in range(9)} - {0} for r in range(9)]
        col_used = [{grid[r * 9 + c] for r in range(9)} - {0} for c in range(9)]

        def search(b):
            if b == 9:
                return True
            blanks, perms = tables[b]
            if not blanks:
                return search(b + 1)
            for perm in perms:
                deadline.check()
                if any(d in row_used[i // 9] or d in col_used[i % 9] for i, d in zip(blanks, perm)):
                    continue
                for i, d in zip(blanks, perm):
                    grid[i] = d
                    row_used[i // 9].add(d)
                    col_used[i % 9].add(d)
                stats.nodes += 1
                if search(b + 1):
                    return True
                for i, d in zip(blanks, perm):
                    grid[i] = 0
                    row_used[i // 9].discard(d)
                    col_used[i % 9].discard(d)
                stats.backtracks += 1
            return False

        stats.solved = search(0)
    except SearchTimeout:
        stats.timed_out = True
    stats.seconds = deadline.elapsed()
    return (grid if stats.solved else None), stats
