# How Much Search Does Constraint Propagation Save?

Comparing four backtracking solvers on rated 9×9 Sudoku — CS 3368 Introduction to AI, Fall 2026, Texas Tech University.

**Team AMZ:** Masaki Kajikuri · Aoto Kubota · Zachary Lenfesty

## Problem

Sudoku is modeled as a constraint satisfaction problem (factored state): 81 variables (cells),
domains {1..9}, and 27 all-different constraints (rows, columns, boxes).
We measure how much search each technique saves over plain backtracking.

- **RQ1:** How many nodes and backtracks do MRV, forward checking, and MAC (AC-3) save?
- **RQ2:** Does clue count predict search effort as well as the dataset's difficulty rating? (Spearman ρ)

## Models

| Model | File | Owner | Status |
|---|---|---|---|
| BT (baseline) | `src/bt.py` | Masaki | done |
| BT+MRV | `src/bt_mrv.py` | Masaki | done |
| BT+MRV+FC | `src/bt_mrv_fc.py` | Zachary | done |
| BT+MRV+MAC (AC-3) | `src/bt_mrv_mac.py` | Aoto | done |
| Minigrid backtracking (Maji & Pal, comparison) | `src/paper_models/maji_pal_minigrid.py` | Masaki | done |

All solvers share `src/csp_model.py` (units, peers, domains, time limit, and the node/backtrack counting rules).

## Data

500 puzzles (`data/sample_500.csv`), 100 per difficulty band, drawn with seed 3368 from the
Kaggle dataset *3 Million Sudoku Puzzles with Ratings* (CC0). See `data/README.md`.
`experiments/check_unique.py` confirms every puzzle has exactly one solution.

## Run

Python 3.10+, from the repository root:

```bash
pip install -r requirements.txt
python -m pytest -q tests                      # correctness tests
python experiments/check_unique.py             # every puzzle has one solution
python experiments/run_all.py --jobs 2         # all implemented solvers, 60 s cap
python experiments/run_all.py --solvers bt_mrv_fc --n 50   # pilot one solver
python experiments/analyze.py                  # tables and figures
```

Results go to `experiments/results/` (one CSV per solver, summaries, figures).
No file paths are hard-coded; every script finds the repository root from its own location.

## Repository layout

```
data/          sample_500.csv, sample.py (sampling), README.md
src/           csp_model.py and the four solvers
src/paper_models/   comparison models from members' papers
experiments/   run_all.py, analyze.py, check_unique.py, results/
tests/         pytest checks shared by all solvers
papers/        notes on each member's paper
docs/          proposal paper and slides
```
