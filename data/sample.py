"""Build the 500-puzzle test set from the Kaggle rated Sudoku dataset.

Owner: Zachary Lenfesty

Usage:
    python data/sample.py --input data/raw/<kaggle-file>.csv --output data/sample_500.csv

Steps (see data/README.md):
    1. Load the CSV (only the columns we need: id, puzzle, solution, clues, difficulty).
    2. Assign each puzzle to one of five difficulty bands.
    3. Draw PER_BAND puzzles per band with a fixed seed.
    4. Keep only puzzles with exactly one solution.
    5. Write the sample to --output.
"""

import argparse

SEED = 3368          # fixed so every member gets the same sample
N_BANDS = 5
PER_BAND = 100


def load_dataset(path):
    """Read the raw CSV and return a DataFrame with id, puzzle, solution, clues, difficulty.

    TODO(Zachary): the file has about 3 million rows; read only the needed columns.
    TODO(Zachary): normalise blanks so '.' and '0' both mean an empty cell.
    """
    raise NotImplementedError


def assign_bands(df, n_bands=N_BANDS):
    """Add a 'band' column (0 = easiest).

    TODO(Zachary): decide how to cut the bands and write the reason here.
    Many puzzles are rated 0, so equal-width bins may leave some bands nearly empty;
    quantile bins (pandas.qcut) are one option.
    """
    raise NotImplementedError


def count_solutions(puzzle, stop_at=2):
    """Return the number of solutions, stopping early once stop_at is reached.

    TODO(Zachary): a plain backtracking counter is enough; reuse src/csp_model.py.
    """
    raise NotImplementedError


def sample(df, per_band=PER_BAND, seed=SEED):
    """Return per_band unique-solution puzzles from each band.

    TODO(Zachary): draw extra candidates per band, filter with count_solutions,
    then keep the first per_band that pass.
    """
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/sample_500.csv")
    args = parser.parse_args()

    df = load_dataset(args.input)
    df = assign_bands(df)
    out = sample(df)
    out.to_csv(args.output, index=False)
    print(f"wrote {len(out)} puzzles to {args.output}")


if __name__ == "__main__":
    main()
