# Wordle Solver

This program seeks to find the solution to the breakout hit game "Wordle" by providing mathematically beneficial suggestions. The goal of the game is to guess a specific 5 letter word within 6 attempts. This program takes a word as input, and, depending on what the Wordle game indicates about the letters, informs you which next guess is most advantageous to you. This is accomplished by scanning through the remaining possible words in the dictionary, and determining the frequencies of each letter. Then, each word receives a score based on the popularity of the letters in that word.

# Things to Improve:
- More forethought to structure (specifically w.r.t. functions, not requiring them to use externally instantiated lists)
- There are probably ways to consolidate multiple functions into one
- Perhaps pandas wasn't the best move, or perhaps I need a smaller dictionary: the first pass is always slow (5-8 seconds)
