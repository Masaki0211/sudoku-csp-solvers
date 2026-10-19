# Paper notes — Zachary Lenfesty
## 1. Full citation
S. Kamal, S. S. Chawla, and N. Goel, "Detection of Sudoku puzzle using image processing and solving by backtracking, simulated annealing and genetic algorithms: A comparative analysis," in Proc. 3rd Int. Conf. Image Inf. Process. (ICIIP), Waknaghat, India, Dec. 2015, pp. 179–184.
DOI: https://doi.org/10.1109/ICIIP.2015.7414762

## 2. Index and citation count
Scopus · 12 citations · checked Oct. 12, 2026

## 3. Problem the paper addresses
- How do you process an image of a standard Sudoku 9x9 puzzle quickly and accurately?
- Which algorithm out of backtracking, simulated annealing, and genetic algorithms solves Sudoku puzzles fastest?

## 4. Approach
For image processing:
- The image was made grayscale and the global mean brightness was calculated
- Experimentally, the authors created a linear combination of the global mean brightness and any given pixel's standard deviation of brightness, calling it the local threshold
- Comparing each pixel with its local threshold allows the authors to force the image into a BW (black-and-white) image
- The BW image can then cluster all enclosed spaces, find the largest enclosed space, and use a Hough transformation find the exact quadrilateral of the largest enclosed space, and a geometric transformation to conform the quadrilateral onto a predefined square (450x450 pixels)
- From here, the image is divided into 81 square blocks (by dividing the length and width by 9, forming 50x50 blocks), and the squares are assigned a row and column value 1 to 9 based on their position in the image
- Each of blocks is run through OCR to determine whether it contains a digit from 1 to 9, or if it is empty, for which it is assigned the value of 0

For solving the Sudoku puzzles:
- standard Backtracking, where every cell is filled in a recursive manner, backtracking whenever it trespasses a rule, but otherwise digging deeper until every cell is filled
- Simulated Annealing, where every cell is filled randomly, and then the number of mistakes are calculated. Random cells are swapped, and the algorithm calculates if this new move is better or worse, if it is better or randomly if the "temperature" is warm enough, it will switch to the new state, if not it stays where it is at. After many (attempted) swaps, it cools a little. If it hasn't found a solution by the time it has cooled to its lowest temperature, the algorithm gives up
- Genetic Algorithm, where a population of various randomly filled puzzles are ranked by how well they follow the rules, and then through a roulette algorithm, are randomly selected and spliced together with a bit of added noise to create a new generation; if the generations stagnates (in this case, 15 generations), then the next generation is composed of an entirely random population again

## 5. Evaluation and data
- Detection was tested on 30 images
- All three algorithms were tested on an unknown number of puzzles (at least 52) varying from 68 to 17 clues (which the authors call "complexity")
- Algorithms timed out after 3600 seconds (being 1 hour)

## 6. Results (with numbers)
<!-- Give page / table / figure numbers so you can answer questions in class. -->
- Detection succeeding in 73.33% of the presented cases, and correctly guessed 99.424% of detected numbers (detecting 98.835% of numbers)
- Detection took an average of 1.813 seconds to preform
- Figure 6 shows the information on how well the algorithms performed on a log10 scale of time on the vertical axis and clue number on the horizontal. It is from this graph that it can be concluded that their were at least 52 tested puzzles
- Genetic algorithm took more than 10 seconds in every case, and was no longer able to finish within an hour below around 30 clues
- Backtracking and simulated annealing show similar speeds, with simulated annealing being about one order of magnitude slower, which drifts up to two or more orders of magnitude slower below 40 clues
- Backtracking is the only algorithm that finishes every puzzle within an hour, with its worse case being around 100 seconds, with the graph implying that it only passed above 10 seconds in two of the puzzles, and with only three puzzles in the time range between 1 and 10 seconds

## 7. What we will take from it
- Simulated annealing and genetic algorithm are _not_ faster than backtracking
- Implementing a hard cap on time makes analysis easier
- Showing results with a log graph can be quite beneficial

## What we will do differently
- Our time cap will be 60 seconds, instead of 3600 seconds
- We do not care about image processing
- Recording of how many nodes were checked and how much backtracking was there, instead of just timing the algorithms (in order to obtain results that are independent of the testing machine)
- We will confirm that uniqueness our solutions are unique per puzzle
- Testing of various puzzles within each of the provided difficulty ranges, instead of presumably just one

## Questions I expect in class
- _Why bring up a paper that spends a great deal of time discussing algorithms that we will not be using?_ Because this paper justifies why we will be focusing on backtracking instead of other algorithms, such as simulated annealing and genetic algorithms.
- _Why are we using backtracking, when the abstract says that simulated annealing is better?_ Because the results of the paper shows, and the authors write that backtracking is better. The only place that says that simulated annealing is better is in the abstract, and in comparison to genetic algorithms.
- _Why not use simulated annealing or genetic algorithms as one of our models?_ Because the authors have already shown that those algorithms are slower than simply backtracking, and more importantly, because our research questions is directed towards how specific optimizations improve the backtracking model, rather than which model is best for Sudoku puzzles.
