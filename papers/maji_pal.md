# Paper notes — Masaki Kajikuri

## 1. Full citation
A. K. Maji and R. K. Pal, "Sudoku solver using minigrid based backtracking," in Proc. IEEE Int. Advance Comput. Conf. (IACC), Gurgaon, India, Feb. 2014, pp. 36–44.
DOI: https://doi.org/10.1109/IAdCC.2014.6779291

## 2. Index and citation count
Scopus · 17 citations · checked Oct. 12, 2026

## 3. Problem the paper addresses
Existing Sudoku solvers work cell by cell and either guess (backtracking, rule-based) or use heavy soft-computing search (genetic algorithms, bee colony). The authors argue this repeats a lot of work on a 9×9 grid and want a solver that does not guess.

## 4. Approach
- Split the grid into nine 3×3 minigrids instead of treating 81 cells separately (Sec. III, p. 39).
- For each minigrid, generate the permutations of its missing digits and keep only the ones consistent with clues in the same rows and columns (Sec. III-A, p. 40). A permutation tree prunes invalid prefixes early.
- Backtrack over minigrids in a fixed order (zigzag, spiral or semi-spiral, Fig. 8): pick a valid permutation for minigrid 1, then search for a compatible one in minigrid 2, and so on.
- Sec. II (pp. 37–39) reviews plain backtracking and elimination rules (naked single, hidden single, lone ranger, locked candidate, twin, triplet, quad), and names constraint propagation, forward checking, and "choosing most constrained value first" as ways to improve basic backtracking (p. 37). We read the last one as MRV (most constrained variable).

## 5. Evaluation and data
No benchmark set and no timing study. The method is shown on worked 9×9 examples (Figs. 2, 9). Table 1 (p. 36) gives a clue-count difficulty scale taken from earlier work.


## 6. Results (with numbers)
- Worked example: minigrid 1 has 5 blanks, so 5! = 120 possible orders, but only 7 are valid (p. 41), so about 94% are pruned before search.
- Table 1 difficulty scale: Extremely easy > 46 clues, Easy 36–46, Medium 32–35, Difficult 28–31, Evil 17–27 (p. 36).
- The authors note clue position also matters: with the same clue count, clustered clues make a harder puzzle (p. 37).


## 7. What we will take from it
- The three improvements to basic backtracking it names — most constrained first, forward checking, constraint propagation — which map to our BT+MRV, BT+MRV+FC and BT+MRV+MAC models.
- Its point that clue count alone does not set difficulty, which motivates RQ2.

## What we will do differently
- Actually measure each technique: nodes expanded, backtracks, time and completion on 500 rated puzzles.
- Keep a cell-based CSP so each technique can be added one at a time; we do not use the minigrid-permutation solver.

## Questions I expect in class
- Your paper has no experiments — why use it? It lists the exact improvements we test; the missing measurements are the gap our project fills.
- What is a minigrid permutation? An ordering of the missing digits inside one 3×3 box; only orders that don't clash with row and column clues are kept.
