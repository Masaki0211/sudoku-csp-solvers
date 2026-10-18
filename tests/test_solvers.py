"""Correctness checks shared by all solvers. Run with: python -m pytest tests

A solver that still raises NotImplementedError is skipped, not failed,
so each member can work on their own model independently.
"""

import importlib

import pytest

# A well-known easy puzzle and its solution, used only as a smoke test.
PUZZLE = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
SOLUTION = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"

SOLVERS = ["bt", "bt_mrv", "bt_mrv_fc", "bt_mrv_mac"]


@pytest.mark.parametrize("name", SOLVERS)
def test_solves_easy_puzzle(name):
    solver = importlib.import_module(f"src.{name}")
    try:
        grid, stats = solver.solve(PUZZLE, time_limit=10)
    except NotImplementedError:
        pytest.skip(f"{name} not implemented yet")
    assert stats.solved
    assert "".join(map(str, grid)) == SOLUTION
    assert stats.nodes > 0


@pytest.mark.parametrize("name", SOLVERS[1:])
def test_not_more_nodes_than_baseline(name):
    """Sanity check: adding a technique should not expand more nodes than BT on this puzzle."""
    base = importlib.import_module("src.bt")
    other = importlib.import_module(f"src.{name}")
    try:
        _, b = base.solve(PUZZLE, time_limit=10)
        _, o = other.solve(PUZZLE, time_limit=10)
    except NotImplementedError:
        pytest.skip("solver not implemented yet")
    assert o.nodes <= b.nodes
