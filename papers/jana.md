# Paper notes — Aoto Kubota

## 1. Full citation
S. Jana, M. Mallik, A. Khan, A. K. Maji, and R. K. Pal, "Design and analysis of a modified 3D Sudoku solver," IEEE Access, vol. 11, pp. 27352–27368, 2023.
DOI: https://doi.org/10.1109/ACCESS.2023.3256420

## 2. Index and citation count
Scopus · 7 citations · checked Oct. 12, 2026

## 3. Problem the paper addresses
Very few solvers exist for 3D Sudoku (a 9×9×9 cube). An earlier backtracking solver by the same group worked only on easy instances because the search tree grows too large.

## 4. Approach
- Algorithm 1: store every possible value for each blank cell (a candidate list per cell), always expand the blank cell with the fewest candidates (minimum remaining values), apply elimination rules (naked single, hidden single, lone ranger, twin, triplet) to shrink the lists, then backtrack.
- Algorithm 2: treat the cube as nine 2D layers, find all solutions of each 2D layer separately, then combine layer solutions that fit together into a 3D solution.
- Sec. VI estimates the worst-case search tree size to show why reducing candidates per cell matters.

## 5. Evaluation and data
75 3D instances from menneske.no, grouped by number of blank cells: 34 easy (180–395 blanks), 21 moderate (400–450), 20 hard (500–542). Compared the earlier solver, Algorithm 1 and Algorithm 2 on time and number of solutions found (Tables 5–7, pp. 27363–27364).

## 6. Results (with numbers)
- Earlier solver: all 34 easy, only 1 of 21 moderate (140.51 s), no hard instances.
- Algorithm 1: all 34 easy and all 21 moderate, no hard instances.
- Algorithm 2: all 75, with hard instances taking about 2.4 s to 160.4 s.
- Example (easy instance 34): 19.10 s earlier solver → 13.51 s Algorithm 1 → 4.96 s Algorithm 2.
- The authors note that blank-cell count alone does not set difficulty; blank positions matter too (p. 27364).

## 7. What we will take from it
- MRV ordering (fewest candidates first) for our BT+MRV model.
- A candidate list (domain) for every blank cell, which is the data structure behind our forward checking and MAC models.
