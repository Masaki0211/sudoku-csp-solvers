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
    solver = pytest.importorskip(f"src.{name}")
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
    other = pytest.importorskip(f"src.{name}")
    try:
        _, b = base.solve(PUZZLE, time_limit=10)
        _, o = other.solve(PUZZLE, time_limit=10)
    except NotImplementedError:
        pytest.skip("solver not implemented yet")
    assert o.nodes <= b.nodes


def test_minigrid_paper_model():
    """Comparison model from Maji & Pal [1] must solve the same smoke puzzle."""
    maji_pal_minigrid = pytest.importorskip("src.paper_models.maji_pal_minigrid")

    grid, stats = maji_pal_minigrid.solve(PUZZLE, time_limit=10)
    assert stats.solved
    assert "".join(map(str, grid)) == SOLUTION
    assert 0 < stats.perm_total <= stats.perm_space


def test_timeout_is_reported():
    """A tiny time limit on a hard puzzle must stop the search and set timed_out."""
    from src import bt

    hard = "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4.."
    grid, stats = bt.solve(hard, time_limit=0.05)
    assert grid is None and stats.timed_out and not stats.solved
