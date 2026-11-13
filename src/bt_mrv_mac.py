"""Model 3 — BT+MRV+MAC: MRV ordering plus maintained arc consistency (AC-3).

Owner: Aoto Kubota
Idea source: Russell & Norvig [4], Sec. 6.2.2 and 6.3.2 (AC-3, MAC);
Jana et al. [3] (per-cell candidate lists, fewest candidates first).

Like BT+MRV+FC, but after each assignment run AC-3 on the arcs (Y, X) for every
unassigned peer Y of the assigned cell X. When a domain shrinks, add its neighbors'
arcs back to the queue, so pruning spreads beyond direct peers.
If any domain becomes empty, the assignment fails. Restore all removals on backtrack.
AC-3 also runs once on all arcs before the search starts.

Counting (same rules as csp_model.py): a node is an assignment that survives AC-3;
a backtrack is an assignment undone because the search below it failed.
"""

from collections import deque

from .csp_model import Deadline, SearchStats, SearchTimeout, initial_domains, parse, peers


def revise(domains: list[set[int]], xi: int, xj: int) -> list[int]:
    """Remove values from domains[xi] that have no support in domains[xj] (the not-equal constraint).

    For not-equal, a value v in Xi loses support only when domains[xj] == {v}.
    Return the list of removed values.
    """
    if len(domains[xj]) == 1:
        (v,) = domains[xj]
        if v in domains[xi]:
            domains[xi].discard(v)
            return [v]
    return []


def ac3(domains: list[set[int]], queue: deque, deadline: Deadline | None = None) -> list[tuple[int, int]] | None:
    """Run AC-3 from the given arc queue.

    Return all (cell, value) removals so they can be restored, or None on a wipe-out
    (removals are already undone then).
    """
    removed = []
    queued = set(queue)
    while queue:
        if deadline is not None:
            deadline.check()
        xi, xj = queue.popleft()
        queued.discard((xi, xj))
        lost = revise(domains, xi, xj)
        if not lost:
            continue
        removed.extend((xi, v) for v in lost)
        if not domains[xi]:
            restore(domains, removed)
            return None
        for xk in peers(xi):
            if xk != xj and (xk, xi) not in queued:
                queue.append((xk, xi))
                queued.add((xk, xi))
    return removed


def restore(domains: list[set[int]], removed: list[tuple[int, int]]) -> None:
    """Put back every (cell, value) pair removed by AC-3."""
    for cell, v in removed:
        domains[cell].add(v)


def select_cell(domains: list[set[int]], grid: list[int]) -> int | None:
    """MRV over the current domains: the blank cell with the smallest domain (ties: lowest index)."""
    best, best_size = None, 10
    for cell, v in enumerate(grid):
        if v == 0 and len(domains[cell]) < best_size:
            best, best_size = cell, len(domains[cell])
            if best_size <= 1:
                break
    return best


def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py."""
    stats = SearchStats()
    deadline = Deadline(time_limit, every=256)
    grid = parse(puzzle)
    domains = initial_domains(grid)

    def search() -> bool:
        cell = select_cell(domains, grid)
        if cell is None:
            return True
        for value in sorted(domains[cell]):
            deadline.check()
            # assign: shrink the cell's domain to {value}, then propagate from it
            others = [(cell, v) for v in domains[cell] if v != value]
            domains[cell] = {value}
            removed = ac3(domains, deque((p, cell) for p in peers(cell) if grid[p] == 0), deadline)
            if removed is None:          # some domain wiped out: prune this branch
                restore(domains, others)
                continue
            grid[cell] = value
            stats.nodes += 1
            if search():
                return True
            grid[cell] = 0
            restore(domains, removed)
            restore(domains, others)
            stats.backtracks += 1
        return False

    try:
        start = deque((xi, xj) for xi in range(81) for xj in peers(xi))
        if ac3(domains, start, deadline) is not None:
            stats.solved = search()
    except SearchTimeout:
        stats.timed_out = True
    stats.seconds = deadline.elapsed()
    return (grid if stats.solved else None), stats
