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

class DomainException(Exception):
    def __init__(self):
        super().__init__("CSP Variable with domain found!");

def forward_check(domains: list[set[int]], cell: int, value: int) -> set[int]:
    """Remove `value` from unassigned peers of `cell`.

    Return the set of indices for the cells with the given value removed so they can be restored,
    or raises an Exception if some peer's domain became empty.
    """
    adjustments : set[int] = {};
    for (peerIndex in peers(cell)):
        if value in domains[peerIndex]:
            if len(domains[peerIndex]) <= 1:
                raise DomainException();
            else:
                adjustments.add(peerIndex);
    for index in adjustments:
        domains[index].remove(value);
    return adjustments;

def solve(puzzle: str, time_limit: float = 60.0) -> tuple[list[int] | None, SearchStats]:
    """Return (solved grid or None, stats). Count nodes and backtracks exactly as in bt.py.

    TODO(Zachary): choose cells by smallest current domain (MRV over domains).
    """
    stats = SearchStats()
    start = time.perf_counter()
    grid = parse(puzzle)
    domains = initial_domains(grid)
    
    forceStopTime = start + time_limit;
    forceUnsolved = False;
    searchStack : list[tuple[int, int, set[int]]] = []; # [ ...(cell index, value, {set of removed indices})]
    blanksFilled : list[int] = []; # [...cell indices]
    while not forceUnsolved:
        cell : int = min(zip(grid, domains, range(len(grid))), key=lambda pair: (pair[0]==0) ? len(pair[1]) : 10)[2]; # work on the cell with the smallest domain
        if (grid[cell] == 0):
            while (grid[cell] == 0):
                stats.nodes += 1; # since we are trying to put a value into a variable, we need to increment our node counter.. for science!
                value : int = min(domains[cell]); # pick the smallest possible value in the domain of our specific cell
                try:
                    domains[cell].discard(value);
                    removals = append(forward_check(domains, cell, value));
                except DomainException:
                    if not domains[cell]:
                        stats.backtracks += 1;
                        if len(searchStack) > 0:
                            backtrackCell, backtrackValue, backtrackRemovals = searchStack.pop();
                            grid[backtrackCell] = 0;
                            for index in backtrackRemovals:
                                domains[index].add(backtrackValue);
                        else:
                            forceUnsolved = True;
                else:
                    searchStack.append((cell, value, removals));
                    grid[cell] = value;
        else:
            stats.solved = True;
            break;
        if time.perf_counter() > forceStopTime:
            stats.timed_out = True;
            break;
    
    stats.seconds = time.perf_counter() - start;
    return (stats.solved ? grid : None, stats);
