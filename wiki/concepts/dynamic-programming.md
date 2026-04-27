---
title: "Dynamic Programming"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, optimization, problem-solving, recursion]
---

# Dynamic Programming

## Overview

Dynamic Programming (DP) is a powerful algorithmic paradigm that solves complex problems by breaking them into overlapping subproblems and computing each subproblem only once. The key insight is that many problems exhibit optimal substructure—where the optimal solution to the whole problem can be constructed from optimal solutions to its subproblems—and overlapping subproblems, where the same subproblems are solved multiple times in naive recursive solutions.

The technique was formalized by Richard Bellman in the 1950s while working at RAND Corporation. The name "dynamic programming" was chosen somewhat arbitrarily to be "something pleasant" and avoid admitting he was doing mathematical research—it's unrelated to "programming" in the software sense or "dynamic" in the modern programming context.

DP transforms exponential-time algorithms into polynomial-time solutions by eliminating redundant computation. The classic example is computing Fibonacci numbers: a naive recursive approach runs in O(2^n) time because it recomputes the same values countless times, while the DP solution completes in O(n) time by computing each value exactly once and storing it for future reference.

## Key Concepts

**Optimal Substructure** means that an optimal solution to a problem contains within it optimal solutions to subproblems. If this property holds, we can use DP; if it doesn't, DP won't help. For example, the shortest path problem has optimal substructure: the shortest path from A to C via B is the shortest path from A to B plus the shortest path from B to C.

**Overlapping Subproblems** occur when a recursive algorithm revisits the same subproblems multiple times. Without memoization or tabulation, algorithms like naive Fibonacci are exponential because they solve the same subproblem exponentially many times.

**Memoization (Top-Down)** solves problems recursively but caches results to avoid redundant computation. When a subproblem is encountered again, the cached result is returned immediately. This approach is often easier to implement because it follows the natural recursive structure of the problem.

**Tabulation (Bottom-Up)** solves problems iteratively by filling a table of subproblem results, typically from smallest to largest. Because it computes all possible subproblems, it can be more efficient than memoization when all subproblems must be solved anyway, and it avoids recursive call overhead.

**State Definition** is crucial in DP—the state captures everything needed to solve a subproblem. Choosing the wrong state can make the problem unsolvable with DP techniques. The state should be minimal and complete.

## How It Works

The DP problem-solving approach follows four steps:

1. **Identify the recursive structure**: Express the problem in terms of smaller subproblems. Find the recurrence relation that describes how the solution relates to solutions of smaller instances.

2. **Define the state**: Determine what information uniquely identifies a subproblem. This typically involves the parameters to the recursive function.

3. **Formulate the recurrence**: Write the mathematical recurrence that relates the solution for a given state to solutions of smaller states.

4. **Implement with memoization or tabulation**: Choose top-down (memoized recursion) or bottom-up (tabulation) based on the problem structure and constraints.

```python
# Fibonacci with memoization
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Fibonacci with tabulation
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

## Practical Applications

Dynamic programming appears across many domains:

**Sequence Problems**: Edit distance (Levenshtein), longest common subsequence, longest increasing subsequence, and sequence alignment in bioinformatics all use DP to handle string or array transformations efficiently.

**Optimization Problems**: The knapsack problem, weighted interval scheduling, and resource allocation problems find optimal solutions through DP by considering all ways to partition resources.

**Graph Problems**: Shortest paths in DAGs, context-free grammar parsing, and CYK parsing for phrase structure recognition use DP's ability to handle overlapping subproblems efficiently.

**Game Theory**: DP solves combinatorial games by computing optimal strategies from terminal positions backward, as in the classic dynamic programming approach to chess or go engines.

**Resource Allocation**: Problems like matrix chain multiplication, where the goal is to minimize scalar multiplications, use DP to find optimal parenthesizations.

## Examples

**Coin Change Problem**: Given coin denominations and a target amount, find the minimum number of coins needed to make that amount.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

# coins = [1, 2, 5], amount = 11 → 3 (5 + 5 + 1)
print(coin_change([1, 2, 5], 11))  # Output: 3
```

**Longest Common Subsequence**: Find the longest subsequence common to two strings, where a subsequence maintains character order but not contiguity.

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

print(lcs("abcde", "ace"))  # Output: 3 ("ace")
```

## Related Concepts

- [[Memoization]] - The top-down approach to DP that caches recursive results
- [[Tabulation]] - The bottom-up approach to DP that builds solutions iteratively
- [[Recursion]] - The foundational concept that DP optimizes through caching
- [[Divide and Conquer]] - Similar paradigm but typically without overlapping subproblems
- [[Greedy Algorithms]] - Different optimization approach that makes locally optimal choices
- [[Time Complexity]] - DP often reduces exponential time to polynomial time

## Further Reading

- [CLRS Introduction to Algorithms, Chapter 15](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - The definitive textbook treatment of dynamic programming
- [GeeksforGeeks: Dynamic Programming](https://www.geeksforgeeks.org/dynamic-programming/) - Practical examples and implementations
- [Overlapping Subproblems (GeeksforGeeks)](https://www.geeksforgeeks.org/overlapping-subproblems-property-in-dynamic-programming-dp-1/)

## Personal Notes

Dynamic programming clicked for me when I stopped trying to memorize specific patterns and instead focused on identifying whether a problem has optimal substructure and overlapping subproblems. The classic "how do you approach a DP problem?" answer is: pretend you're writing a recursive solution first, then add caching. This top-down approach is often easier to conceptualize than the bottom-up tabulation. Practice recognizing DP in disguise problems—like counting paths, palindrome partitioning, or string interleaving—where the recursive structure isn't immediately obvious.
