# How Much Search Does Constraint Propagation Save?

**Comparing four backtracking solvers on rated 9×9 Sudoku** · CS 3368, Fall 2026 · Team AMZ

| Member | Model owned | Paper reviewed |
|---|---|---|
| Masaki Kajikuri | `BT` (baseline) and `BT+MRV` · shared CSP model | Maji & Pal, IACC 2014 |
| Zachary Lenfesty | `BT+MRV+FC` (forward checking) · data sampling | Kamal et al., ICIIP 2015 |
| Aoto Kubota | `BT+MRV+MAC` (maintained arc consistency, AC-3) | Jana et al., IEEE Access 2023 |

## Problem

We solve standard 9×9 Sudoku as a constraint satisfaction problem (CSP) and measure how much each technique reduces search:

- **RQ1:** How many nodes and backtracks do MRV, forward checking, and arc consistency save compared with plain backtracking?
- **RQ2:** How well does clue count predict solver effort, compared with the dataset's published difficulty rating?

State representation: **factored** — 81 variables, domains {1…9}, 27 all-different constraints.

## Models

Each model adds one technique to the one before it, on one shared CSP model (`src/csp_model.py`).

| Model | File | What it adds |
|---|---|---|
| BT | `src/bt.py` | Plain backtracking, fixed cell order (baseline) |
| BT+MRV | `src/bt_mrv.py` | Chooses the cell with the fewest legal values |
| BT+MRV+FC | `src/bt_mrv_fc.py` | After each assignment, removes the value from neighbors' domains |
| BT+MRV+MAC | `src/bt_mrv_mac.py` | After each assignment, runs AC-3 so pruning spreads |

## Measures

Nodes expanded, backtracks, solve time, and completion within a 60 s limit. Baselines: `BT` for total effect, `BT+MRV` for the added effect of propagation. RQ2 uses Spearman rank correlation.

## Data

[3 Million Sudoku Puzzles with Ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings) (Kaggle, CC0). Each row has the puzzle, its solution, the clue count, and a difficulty rating. We sample 500 puzzles (100 per rating band) and keep only puzzles with exactly one solution. See [`data/README.md`](data/README.md) for how to download it. The full dataset is **not** committed.

## Repository layout

```
docs/          proposal and presentation files
papers/        each member's notes on their peer-reviewed paper (no PDFs)
src/           shared CSP model and the four solvers
data/          download notes and sampling script (raw data is git-ignored)
experiments/   batch runner and results
tests/         correctness checks
```

## Running (once implemented)

```bash
python -m pip install -r requirements.txt
python data/sample.py --input data/raw/sudoku-3m.csv --output data/sample_500.csv
python experiments/run_all.py --puzzles data/sample_500.csv --limit 60
python -m pytest tests
```

## References

1. A. K. Maji and R. K. Pal, "Sudoku solver using minigrid based backtracking," in *Proc. IEEE Int. Advance Comput. Conf. (IACC)*, Gurgaon, India, Feb. 2014, pp. 36–44, doi: 10.1109/IAdCC.2014.6779291.
2. S. Kamal, S. S. Chawla, and N. Goel, "Detection of Sudoku puzzle using image processing and solving by backtracking, simulated annealing and genetic algorithms: A comparative analysis," in *Proc. 3rd Int. Conf. Image Inf. Process. (ICIIP)*, Waknaghat, India, Dec. 2015, pp. 179–184, doi: 10.1109/ICIIP.2015.7414762.
3. S. Jana, M. Mallik, A. Khan, A. K. Maji, and R. K. Pal, "Design and analysis of a modified 3D Sudoku solver," *IEEE Access*, vol. 11, pp. 27352–27368, 2023, doi: 10.1109/ACCESS.2023.3256420.
