"""Run solvers on the same puzzles and save one row per (puzzle, solver).

Shared by all members. Each member can run only their own model and the files
are merged by experiments/analyze.py (one CSV per solver in the output folder).

Usage (from the repository root):
    python experiments/run_all.py                                  # every implemented solver
    python experiments/run_all.py --solvers bt_mrv_fc --n 50       # pilot on 50 puzzles
    python experiments/run_all.py --solvers bt bt_mrv --jobs 2     # two worker processes

Output: experiments/results/<solver>.csv with columns
    id, solver, clues, difficulty, band, nodes, backtracks, seconds,
    solved, timed_out, correct, matches_dataset
"""

import argparse
import csv
import importlib
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# module path inside src/ for every solver name
SOLVERS = {
    "bt": "src.bt",
    "bt_mrv": "src.bt_mrv",
    "bt_mrv_fc": "src.bt_mrv_fc",
    "bt_mrv_mac": "src.bt_mrv_mac",
    "minigrid": "src.paper_models.maji_pal_minigrid",
}
FIELDS = ["id", "solver", "clues", "difficulty", "band", "nodes", "backtracks",
          "seconds", "solved", "timed_out", "correct", "matches_dataset"]


def is_implemented(name: str) -> bool:
    """A solver counts as implemented if it solves a trivial puzzle without NotImplementedError."""
    try:
        solver = importlib.import_module(SOLVERS[name])
    except ModuleNotFoundError:     # solver file not in this copy of the project
        return False
    easy = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
    try:
        solver.solve("." + easy[1:], time_limit=5)
    except NotImplementedError:
        return False
    return True


def run_one(job):
    """Solve one puzzle with one solver; runs inside a worker process."""
    name, row, limit = job
    from src.csp_model import is_valid_solution, parse, to_string

    solver = importlib.import_module(SOLVERS[name])
    grid, st = solver.solve(row["puzzle"], time_limit=limit)
    correct = grid is not None and is_valid_solution(grid, parse(row["puzzle"]))
    return {
        "id": row["id"], "solver": name, "clues": row["clues"],
        "difficulty": row["difficulty"], "band": row.get("band", ""),
        "nodes": st.nodes, "backtracks": st.backtracks,
        "seconds": round(st.seconds, 4), "solved": st.solved,
        "timed_out": st.timed_out, "correct": correct,
        "matches_dataset": correct and to_string(grid) == row.get("solution", ""),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--puzzles", default=str(ROOT / "data" / "sample_500.csv"))
    parser.add_argument("--solvers", nargs="+", default=list(SOLVERS), choices=list(SOLVERS))
    parser.add_argument("--limit", type=float, default=60.0, help="seconds per run")
    parser.add_argument("--n", type=int, default=None, help="only the first n puzzles (pilot)")
    parser.add_argument("--jobs", type=int, default=1, help="worker processes")
    parser.add_argument("--out-dir", default=str(ROOT / "experiments" / "results"))
    args = parser.parse_args()

    with open(args.puzzles, newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows):
        r.setdefault("id", str(i))      # sample_500.csv has no id column: use row number
        if not r["id"]:
            r["id"] = str(i)
    if args.n:
        rows = rows[: args.n]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in args.solvers:
        if not is_implemented(name):
            print(f"{name}: skipped (not implemented or not included)")
            continue
        jobs = [(name, r, args.limit) for r in rows]
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(run_one, jobs, chunksize=4))
        with open(out_dir / f"{name}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(results)
        solved = sum(r["solved"] for r in results)
        wrong = sum(r["solved"] and not r["correct"] for r in results)
        print(f"{name}: {solved}/{len(results)} solved, {wrong} wrong, "
              f"{sum(r['timed_out'] for r in results)} timed out")


if __name__ == "__main__":
    main()
