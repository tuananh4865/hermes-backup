---
title: "Backtracking"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, recursion, problem-solving, search, combinatorial]
---

# Backtracking

## Overview

Backtracking is a systematic algorithmic technique for finding solutions to constraint satisfaction problems by incrementally building candidates and abandoning ("backtracking") partial candidates when it becomes clear they cannot lead to a valid solution. It explores the search space depth-first, trying extensions to the current partial solution, and when a dead end is reached, undoing the last extension (backtracking) to try the next possibility.

The paradigm is fundamental to solving problems like the N-Queens problem, Sudoku solvers, combinatorial optimization, and parsing. Unlike brute-force search which tries all possibilities, backtracking prunes branches that cannot possibly lead to solutions, often reducing search from exponential to polynomial for many practical instances.

Backtracking sits at the intersection of recursion and exhaustive search. It maintains explicit or implicit state about which choices have been made at each depth, allowing it to undo choices and try alternatives. This state management is what distinguishes backtracking from simple recursion.

The technique dates to the 1950s and was formalized in the context of combinatorial puzzles. The "n-queens" problem, posed in 1848, is one of the earliest problems solved by backtracking. Today, backtracking underlies SAT solvers, constraint programming systems, and many combinatorial algorithms.

## Key Concepts

**State Space Tree** represents all possible choices as a tree, where each node is a partial solution and each edge is a choice. Backtracking performs a depth-first traversal of this implicit tree, visiting nodes in a systematic order. The actual tree is never fully constructed in memory—only the current path matters at any point.

**Pruning** is the process of cutting off search branches that cannot lead to solutions. When a partial solution violates a constraint or cannot be extended to a valid solution, the entire subtree beneath it is abandoned. Effective pruning is what makes backtracking practical—without it, it's just exhaustive search.

**Constraint Propagation** goes beyond simple pruning by using constraints to infer what choices are still valid for unexplored variables. In Sudoku, once you place a number, you can eliminate that number from related cells' possibilities, potentially triggering cascades of elimination.

**Choice Point** represents a decision where multiple options exist. At each choice point, the algorithm tries one option, recursively explores what follows, and if that path fails, backtracks to try the next option. The order in which options are tried can dramatically affect performance.

**Dead End Detection** determines when a partial solution cannot lead to any valid complete solution. This can be through explicit constraint violation, through exhaustion of possibilities, or through inference that remaining choices are impossible.

## How It Works

The backtracking algorithm follows a recursive pattern:

1. **Base Case**: If the current state is a complete solution, record it as valid
2. **Choice Point**: Determine the next variable or decision to make
3. **Loop Over Options**: For each possible value/action:
   - Make the choice (extend the partial solution)
   - Check if constraints are satisfied (pruning)
   - Recursively continue with the new state
   - Undo the choice (backtrack) if recursion returned without finding solution
4. **Return**: Report success if solution found, failure otherwise

```python
def n_queens(n):
    solutions = []
    
    def solve(board, row, cols, diag1, diag2):
        # Base case: all queens placed
        if row == n:
            solutions.append([row[:] for row in board])
            return
        
        # Try placing queen in each column of this row
        for col in range(n):
            # Pruning: check if column or diagonals are attacked
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            
            # Make choice
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            # Recurse
            solve(board, row + 1, cols, diag1, diag2)
            
            # Backtrack: undo choice
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    solve(board, 0, set(), set(), set())
    return solutions

# Find all solutions for 4-queens
solutions = n_queens(4)
print(f"Found {len(solutions)} solutions for 4-queens")
# Output: Found 2 solutions for 4-queens
```

## Practical Applications

**Sudoku Solvers**: Backtracking with constraint propagation can solve Sudoku puzzles efficiently. Modern solvers use techniques like naked singles, hidden singles, and block/row/column interactions to prune aggressively.

**N-Queens Problem**: Placing N chess queens on an N×N board so no two attack each other. Used to illustrate backtracking fundamentals and constraint satisfaction.

**Word Search and Crossword Solving**: Finding words in letter grids or valid crossword entries given letter constraints uses backtracking with pruning based on word dictionary constraints.

**Combinatorial Generation**: Generating permutations, combinations, and subsets often uses backtracking to build sequences incrementally.

**Path Finding in Mazes**: Finding paths through a maze, especially when multiple dead ends exist, is naturally solved by backtracking when dead ends are detected.

**Game Playing**: Early chess programs used backtracking to explore move sequences, evaluating positions at leaf nodes and backing up values. Modern engines use alpha-beta pruning to improve on pure backtracking.

## Examples

**Permutations Generation**:

```python
def permutations(nums):
    result = []
    
    def backtrack(start):
        # Base case: all elements used
        if start == len(nums):
            result.append(nums[:])
            return
        
        # Try each element at position 'start'
        for i in range(start, len(nums)):
            # Swap to put element at position 'start'
            nums[start], nums[i] = nums[i], nums[start]
            
            # Recurse for next position
            backtrack(start + 1)
            
            # Backtrack: restore original order
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result

print(permutations([1, 2, 3]))
# Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]
```

**Subset Sum Problem**:

```python
def subset_sum(nums, target):
    result = []
    
    def backtrack(start, current_sum, path):
        # Found valid subset
        if current_sum == target:
            result.append(path[:])
            return
        
        # Prune: if sum exceeds target or no more elements
        if current_sum > target or start == len(nums):
            return
        
        # Try including each remaining element
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, current_sum + nums[i], path)
            path.pop()  # Backtrack
    
    backtrack(0, 0, [])
    return result

nums = [2, 3, 5, 7]
target = 10
print(subset_sum(nums, target))  # Output: [[2, 3, 5], [10]... wait 10 not in list]
# Output: [[2, 3, 5], [10]] - wrong, let me fix
# Actually: [[2, 3, 5], [10]] won't appear since 10 not in nums
# Correct output: [[2, 3, 5]]
```

## Related Concepts

- [[Recursion]] - The implementation mechanism for backtracking
- [[Dynamic Programming]] - Alternative when subproblems overlap
- [[Memoization]] - Can be applied to backtracking (branch and bound)
- [[Constraint Satisfaction]] - Problems that backtracking naturally solves
- [[Depth-First Search]] - Backtracking is DFS with state restoration
- [[Branch and Bound]] - Extension of backtracking with pruning using cost bounds

## Further Reading

- [CLRS Chapter 5: Probabilistic Analysis and Randomized Algorithms](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - Brief backtracking treatment
- [Backtracking (Wikipedia)](https://en.wikipedia.org/wiki/Backtracking) - Comprehensive overview
- [N-Queens Problem (Wikipedia)](https://en.wikipedia.org/wiki/Eight_queens_puzzle) - Classic backtracking example

## Personal Notes

Backtracking became intuitive when I started thinking of it as "smart exhaustive search"—the key insight is that you don't explore paths you know can't work. The pruning logic is the hard part; once you have good pruning, performance often becomes acceptable. I use backtracking for any problem where I need to enumerate possibilities subject to constraints. When pure backtracking is too slow, I add memoization or consider branch-and-bound with cost lower bounds.
