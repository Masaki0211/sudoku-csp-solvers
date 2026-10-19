# Data

**Source:** [3 Million Sudoku Puzzles with Ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings) (Kaggle, CC0: Public Domain).
A copy of the same data is on OpenML as dataset 43476: <https://api.openml.org/d/43476>.

Each row contains:

| Column | Meaning |
|---|---|
| `id` | Row number |
| `puzzle` | 81 characters, row by row; blanks are `.` or `0` (check after download) |
| `solution` | 81 digits, the unique solution |
| `clues` | Number of given digits (19–31 in this dataset) |
| `difficulty` | Rating from 0 to 8.5, computed by an automated solver as the average search-tree depth over 10 attempts |

Because the rating comes from a search-based solver, we report RQ2 as *agreement* between clue count, this rating, and our solvers' effort, not as independent validation.

## Download (pick one)

The raw file is large, so it goes in `data/raw/`, which is git-ignored. **Do not commit it.**

**A. Kaggle website (easiest)**
1. Sign in at kaggle.com and open the dataset link above.
2. Click **Download**, unzip, and put the CSV in `data/raw/`.

**B. Kaggle command line**
1. `pip install kaggle`
2. On kaggle.com → Settings → API → **Create New Token**; save `kaggle.json` to `~/.kaggle/` (Windows: `C:\Users\<you>\.kaggle\`).
3. Run:
   ```bash
   kaggle datasets download -d radcliffe/3-million-sudoku-puzzles-with-ratings -p data/raw --unzip
   ```

**C. OpenML (no account needed)** — download dataset 43476 from the OpenML link above, or in Python:
```python
from sklearn.datasets import fetch_openml
df = fetch_openml(data_id=43476, as_frame=True).frame
```

## Sampling (owner: Zachary)

`data/sample.py` builds `data/sample_500.csv`:

1. Split puzzles into five difficulty bands.
2. Draw 100 puzzles per band with a fixed random seed, so everyone gets the same 500.
3. Keep a puzzle only if a solution counter stops at exactly one solution.
4. Save `id, puzzle, solution, clues, difficulty, band`.

The 500-row sample is small and CC0, so it **is** committed.
