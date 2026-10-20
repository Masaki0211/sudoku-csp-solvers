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

import pandas as pd

def load_dataset(path):
    """Read the raw CSV and return a DataFrame with puzzle, solution, clues, difficulty.
    Note: As the data is already normalized, no normalization occurs here.
    """
    df = pd.read_csv(path, usecols=["puzzle", "solution", "clues", "difficulty"]);
    return df;


def assign_bands(df, n_bands=N_BANDS):
    """Creates a DataFrame with an added 'band' column (ranging from 0 as the easiest, to n_bands-1 as the hardest).
    Note: As a disporportionate amount of puzzles are considered difficulty "0.0," the bands are calculated in a strange way.
        Our classification works by estimating how many items should go into each bin based on how many items and bins are left (items / bins), and then
        filling into the next available bin all values corresponding to a unique difficulty value until the bin is at capacity or overflows. As it doesn't
        make sense to divide the bin between different items with the same difficulty rating, the bin keeps all of the overflow, and the estimated items
        per bin is recalculate, and the process repeats with the next available bin until all bins are filled, and all items are classified.
    """
    # (1)
    uniqueDifficultyValues = df['difficulty'].sort_values().value_counts(sort=False);
    # (2)
    band_partitions = [-1];
    totalLeft = df['difficulty'].count();
    accumulator = 0;
    bandsLeft = n_bands
    accumulatorCap = totalLeft / bandsLeft;
    # (3)
    for index, value in uniqueDifficultyValues.items():
        accumulator += value;
        if accumulator >= accumulatorCap:
            totalLeft -= accumulator;
            bandsLeft -= 1;
            if bandsLeft > 0:
                accumulatorCap = totalLeft / bandsLeft;
            else:
                accumulatorCap = totalLeft;
            accumulator = 0;
            band_partitions.append(index);
    #print(band_partitions); # DEBUG : This shows where exactly are the difficulty bands being placed
    df['band'] = pd.cut(df['difficulty'], bins=band_partitions, include_lowest=True, labels=range(n_bands));
    return df;


def count_solutions(puzzle, stop_at=2):
    """Return the number of solutions, stopping early once stop_at is reached.
        This can be implemented later, as it will be very costly to check all solution paths to each of these items,
        and it is unlikely that any of these problems contain duplicate solutions, based on the dataset's description.
    """
    raise NotImplementedError


def sample(df, per_band=PER_BAND, seed=SEED):
    """Return per_band unique-solution puzzles from each band.
        Note: Uniqueness is currently being assumed from the dataset. I belive this is a reasonable assumption,
        but irregardless, I will probably remove this assumption later.
    """
    
    finalSample = pd.DataFrame(columns=["puzzle", "solution", "clues", "difficulty"]);
    for bandValue in df['band'].unique():
        sample = (df[df['band'] == bandValue]).sample(n=per_band, random_state=seed);
        finalSample = finalSample.merge(sample, how='outer');
    
    return finalSample;


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