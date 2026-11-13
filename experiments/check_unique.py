"""Check that every puzzle in the sample has exactly one solution.

Owner: Masaki Kajikuri

Counts solutions with an MRV search that stops at 2. A puzzle with 0 or 2+
solutions would make node counts meaningless, so it must be replaced.

Usage (from the repository root):
    python experiments/check_unique.py [--puzzles data/sample_500.csv]
"""

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.bt_mrv import select_mrv_cell  # noqa: E402
from src.csp_model import parse  # noqa: E402


def count_solutions(puzzle: str, cap: int = 2) -> int:
    grid = parse(puzzle)
    found = 0

    def search():
        nonlocal found
        choice = select_mrv_cell(grid)
        if choice is None:
            found += 1
            return found >= cap
        cell, values = choice
        for v in values:
            grid[cell] = v
            if search():
                return True
            grid[cell] = 0
        return False

    search()
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puzzles", default=str(ROOT / "data" / "sample_500.csv"))
    args = parser.parse_args()
    with open(args.puzzles, newline="") as f:
        rows = list(csv.DictReader(f))
    bad = [(i, n) for i, r in enumerate(rows) if (n := count_solutions(r["puzzle"])) != 1]
    print(f"{len(rows) - len(bad)}/{len(rows)} puzzles have exactly one solution")
    for i, n in bad:
        print(f"  row {i}: {n if n < 2 else '2+'} solutions")


if __name__ == "__main__":
    main()
