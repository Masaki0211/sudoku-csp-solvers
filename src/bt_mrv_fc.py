"""Model 2 — BT+MRV+FC: MRV ordering plus forward checking.

Owner: Zachary Lenfesty
Idea source: Maji & Pal [1] (forward checking as an improvement to backtracking).

Keeps a domain (candidate set) for every blank cell.
After assigning value v to cell X, remove v from the domain of every unassigned peer of X.
If any peer's domain becomes empty, this assignment fails immediately (no deeper search).
On backtrack, restore exactly the values that were removed.

The search is iterative: an explicit stack replaces recursion.
"""

import time

from .csp_model import SearchStats, parse, initial_domains, peers

class DomainException(Exception):
    def __init__(self):
        super().__init__("CSP variable with empty domain found!");

def forward_check(domains: list[set[int]], grid: list[int], cell: int, value: int) -> set[int]:
    """Remove `value` from unassigned peers of `cell`.

    Return the set of indices for the cells with the given value removed so they can be restored,
    or raises an Exception if some peer's domain became empty (nothing is removed in that case).
    """
    adjustments : set[int] = set();
    for peerIndex in peers(cell):
        if grid[peerIndex] == 0 and value in domains[peerIndex]:
            if len(domains[peerIndex]) <= 1:
                raise DomainException();
            else:
                adjustments.add(peerIndex);
    for index in adjustments:
        domains[index].remove(value);
    return adjustments;

def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py."""
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    domains = initial_domains(grid)

    forceStopTime = start + time_limit;
    searchStack : list[tuple[int, int, set[int], set[int]]] = []; # [ ...(cell index, value, {removed peer indices}, {values tried in this cell})]
    cell : int | None = None; # cell we are currently trying values for
    tried : set[int] = set(); # values already tried in that cell
    while True:
        if time.perf_counter() > forceStopTime:
            stats.timed_out = True;
            break;
        if cell is None:
            cell = min(zip(grid, domains, range(len(grid))), key=lambda pair: len(pair[1]) if pair[0] == 0 else 10)[2]; # work on the cell with the smallest domain
            if grid[cell] != 0: # every cell is filled
                stats.solved = True;
                break;
            tried = set();
        if not domains[cell]: # no values left for this cell: undo the previous assignment
            domains[cell] |= tried; # put back the values we tried here
            if not searchStack:
                break; # nothing left to undo: no solution
            cell, backtrackValue, backtrackRemovals, tried = searchStack.pop();
            grid[cell] = 0;
            for index in backtrackRemovals:
                domains[index].add(backtrackValue);
            stats.backtracks += 1;
            continue; # keep trying the remaining values of that earlier cell
        value : int = min(domains[cell]); # pick the smallest possible value in the domain of our specific cell
        domains[cell].discard(value);
        tried.add(value);
        try:
            removals = forward_check(domains, grid, cell, value);
        except DomainException:
            continue; # a peer would lose its last value: try the next value
        grid[cell] = value;
        stats.nodes += 1; # the assignment survived forward checking, so it counts as a node.. for science!
        searchStack.append((cell, value, removals, tried));
        cell = None;

    stats.seconds = time.perf_counter() - start;
    return (grid if stats.solved else None), stats;
