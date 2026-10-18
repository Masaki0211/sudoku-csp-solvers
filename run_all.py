"""Run all four solvers on the same puzzles and save one row per (puzzle, solver).

Shared by all members. Each member runs their own model in the full run (week of Nov 16).

Usage:
    python experiments/run_all.py --puzzles data/sample_500.csv --limit 60
    python experiments/run_all.py --puzzles data/sample_500.csv --solvers bt_mrv_fc --n 50   # pilot

Output columns:
    id, solver, clues, difficulty, band, nodes, backtracks, seconds, solved, timed_out, correct
"""

import argparse
import csv
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SOLVERS = ["bt", "bt_mrv", "bt_mrv_fc", "bt_mrv_mac"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puzzles", required=True)
    parser.add_argument("--solvers", nargs="+", default=SOLVERS, choices=SOLVERS)
    parser.add_argument("--limit", type=float, default=60.0, help="seconds per run")
    parser.add_argument("--n", type=int, default=None, help="only the first n puzzles (pilot)")
    parser.add_argument("--out", default="experiments/results/results.csv")
    args = parser.parse_args()

    from src.csp_model import parse, is_valid_solution

    with open(args.puzzles, newline="") as f:
        rows = list(csv.DictReader(f))
    if args.n:
        rows = rows[: args.n]

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "solver", "clues", "difficulty", "band", "nodes", "backtracks",
              "seconds", "solved", "timed_out", "correct"]
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for name in args.solvers:
            solver = importlib.import_module(f"src.{name}")
            for r in rows:
                grid, st = solver.solve(r["puzzle"], time_limit=args.limit)
                correct = bool(grid) and is_valid_solution(grid, parse(r["puzzle"]))
                writer.writerow({
                    "id": r["id"], "solver": name, "clues": r["clues"],
                    "difficulty": r["difficulty"], "band": r.get("band", ""),
                    "nodes": st.nodes, "backtracks": st.backtracks,
                    "seconds": round(st.seconds, 4), "solved": st.solved,
                    "timed_out": st.timed_out, "correct": correct,
                })
            print(f"{name}: done ({len(rows)} puzzles)")


if __name__ == "__main__":
    main()
