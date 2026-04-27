---
title: "Tabulation"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [dynamic-programming, algorithms, optimization, bottom-up]
---

# Tabulation

## Overview

Tabulation is the bottom-up approach to dynamic programming where solutions to subproblems are computed iteratively in a table (typically an array or 2D array), filling the table from the smallest subproblems up to the largest. The term "tabulation" reflects the way intermediate results are stored in a table for later lookup. Tabulation contrasts with memoization (top-down) by computing all subproblems proactively rather than computing only those actually needed on-demand.

The bottom-up approach is often preferred when all subproblems must be solved anyway, when space efficiency matters (tabulation can sometimes reduce space complexity), or when recursive function calls have significant overhead. It's also the approach of choice when the problem structure naturally lends itself to iteration—for example, when subproblems form a DAG with a natural ordering.

Tabulation transforms problems with optimal substructure and overlapping subproblems from exponential worst-case to polynomial time. The key is identifying the correct ordering of subproblems and the recurrence relation that connects them. Once these are established, filling the table is often straightforward.

## Key Concepts

**Subproblem Ordering** determines the iteration sequence. Tabulation requires that subproblems be solved in an order where all dependencies (smaller subproblems) are computed before they're needed. For Fibonacci, this means computing dp[0], dp[1], then dp[2], etc. For 2D problems like grid paths, this means iterating rows or columns in dependency order.

**State Transition** is the recurrence relation that defines how larger subproblems relate to smaller ones. The transition explains how to compute dp[i] from previous dp values. This transition is often the most challenging part—once correctly formulated, implementation is mechanical.

**Space Optimization** is possible in many tabulation solutions when only a subset of table values are needed to compute subsequent values. Fibonacci needs only the previous two values, reducing O(n) space to O(1). Knapsack can sometimes be optimized from O(nW) to O(W) by iterating weights in reverse.

**Table Initialization** sets up base case values that seed the table. These correspond to the smallest, directly solvable subproblems: dp[0] = 0 for counting problems, dp[i][0] = 0 for no items, dp[0][j] = 1 for subset sum, etc.

**Iterative Fill** is the main computation loop that populates the table according to the determined ordering. Each cell is computed using previously computed values via the state transition.

## How It Works

The tabulation approach follows these steps:

1. **Identify subproblems**: Define what each table cell represents (typically indexed by problem size or parameters)
2. **Determine ordering**: Find a linear ordering of subproblems where dependencies come first
3. **Initialize table**: Set up base case values
4. **Iterate and fill**: For each subproblem in order, compute using the recurrence relation
5. **Extract answer**: Return the table entry representing the original problem

```python
# Tabulation for Fibonacci
def fib_tab(n):
    if n <= 1:
        return n
    
    # Initialize table
    dp = [0] * (n + 1)
    dp[1] = 1
    
    # Fill table iteratively
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# Space-optimized version
def fib_tab_optimized(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1
```

## Practical Applications

**Sequence Problems**: Longest increasing subsequence, longest common subsequence, edit distance—all computed by filling 2D tables where each cell represents the answer for prefixes or substrings.

**Knapsack Problems**: The classic 0/1 knapsack computes maximum value for each weight capacity by iterating items and capacities, updating the table in a specific order to avoid using the current item multiple times.

**Counting Problems**: Number of ways to climb stairs (dp[i] = dp[i-1] + dp[i-2]), counting subsets with given sum, counting permutations—all use tabulation to build up from base cases.

**String Problems**: Palindrome partitioning, word break, regular expression matching—these fill tables based on string prefixes or suffixes.

**Graph Problems**: Shortest paths in DAGs can be computed via topological sort order, which is essentially tabulation on the graph's partial order.

## Examples

**Longest Common Subsequence (LCS)**:

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    
    # Initialize table with zeros
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill table bottom-up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

# Rebuild LCS string
def lcs_string(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to reconstruct
    i, j = m, n
    lcs_chars = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_chars.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs_chars))

print(lcs("abcde", "ace"))  # Output: 3
print(lcs_string("abcde", "ace"))  # Output: "ace"
```

**0/1 Knapsack**:

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    
    # Initialize table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Fill table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]

# Space-optimized version
def knapsack_optimized(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]

weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5
print(knapsack(weights, values, capacity))  # Output: 7 (items with weight 2,3)
```

## Related Concepts

- [[Dynamic Programming]] - The broader algorithmic paradigm
- [[Memoization]] - Top-down alternative to tabulation
- [[Fibonacci Sequence]] - Classic example of both approaches
- [[Knapsack Problem]] - NP-hard but DP-tractable for small capacities
- [[Longest Common Subsequence]] - Fundamental string DP problem
- [[Recursion]] - Tabulation is the iterative transformation of recursive solutions

## Further Reading

- [CLRS Chapter 15: Dynamic Programming](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - Definitive treatment
- [GeeksforGeeks: Tabulation vs Memoization](https://www.geeksforgeeks.org/tabulation-vs-memoization/) - Comparison
- [Dynamic Programming Patterns (LeetCode)](https://leetcode.com/discuss/general-discussion/458695/dynamic-programming-patterns) - Practical patterns

## Personal Notes

Tabulation is my default when I know the recurrence relation and can determine the subproblem ordering. I find it more predictable than memoization because the iteration is explicit and space usage is clear. The space optimization step (realizing you only need certain rows or columns) is one of my favorite DP "aha moments." When writing tabulation solutions, I always start by defining what dp[i] means—that clarity makes the transition formula almost obvious.
