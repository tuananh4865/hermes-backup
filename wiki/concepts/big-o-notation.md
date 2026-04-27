---
title: Big O Notation
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [big-o, algorithms, complexity, computer-science]
---

## Overview

Big O notation is a mathematical notation used in computer science to describe the upper bound or worst-case scenario of an algorithm's growth rate in terms of input size. It provides a standardized way to express how an algorithm's performance scales as the size of its input increases, allowing developers to compare algorithms independently of hardware, programming language, or implementation details.

The notation focuses on the dominant term in the growth function, ignoring constants and lower-order terms that become insignificant for large inputs. For example, an algorithm that performs 3n^2 + 5n + 2 operations is expressed simply as O(n^2), because the n^2 term dominates the growth as n becomes large. This simplification makes Big O particularly useful for predicting algorithm behavior at scale and for making informed decisions when selecting between competing algorithms.

Big O is part of a family of asymptotic notations that includes [[Big Theta]] (tight bound), [[Big Omega]] (lower bound), [[Little O]], and [[Little Omega]]. Each provides a different perspective on algorithm performance, but Big O is the most commonly used in practice because it describes the ceiling of performance that users can expect.

Understanding Big O is fundamental to [[algorithm analysis]] and forms the basis for evaluating everything from simple sorting routines to complex [[data structures]] and [[dynamic programming]] solutions.

## Common Complexities

### O(1) - Constant Time

O(1) represents algorithms whose execution time remains the same regardless of input size. Array index access, hash table lookups, and stack push/pop operations all exhibit constant time complexity. These are the most efficient algorithms possible, though they cannot solve all problems.

### O(log n) - Logarithmic Time

Logarithmic algorithms reduce the problem size by a constant fraction with each step. Binary search is the classic example, repeatedly halving a sorted array until the target is found. The [[binary search algorithm]] exemplifies O(log n) behavior and is fundamental to search operations in sorted data structures like [[binary search trees]].

### O(n) - Linear Time

Linear time algorithms scale directly with input size. Simple traversals, linear search, and single-pass array operations all run in O(n). An algorithm that examines each element exactly once typically achieves linear time.

### O(n log n) - Linearithmic Time

This complexity appears in efficient sorting algorithms that achieve the theoretical minimum for comparison-based sorting. [[Merge Sort]], [[Quick Sort]], and [[Heap Sort]] all run in O(n log n) on average or worst case. The n log n threshold is significant because it represents the best possible complexity for comparison-based sorting in the general case.

### O(n^2) - Quadratic Time

Quadratic algorithms grow proportionally to the square of the input size. Nested loops iterating over the same collection, naive bubble sort, and matrix multiplication using the standard algorithm all exhibit O(n^2) behavior. These algorithms become impractical for large datasets but may be acceptable for small or bounded inputs.

### Beyond Quadratic

Higher complexities like O(n^3), O(2^n), and O(n!) grow rapidly and are generally impractical for all but the smallest inputs. The exponential O(2^n) complexity is particularly notorious, appearing in naively implemented combinatorial problems like the [[travelling salesman problem]] and recursive generation of all subsets.

## Analysis

Analyzing an algorithm's Big O complexity involves identifying the fundamental operation being measured (typically comparisons for sorting, operations for general computation, or memory accesses) and expressing how many times it executes relative to the input size.

**Counting operations** is the most direct approach. Examine each line of code or each loop to determine how many times it executes, then combine these counts. When loops are nested, multiplicatively combine their complexities. Sequential statements take the maximum complexity of each statement, not their sum.

**Identifying dominant terms** matters when expressions contain multiple terms. The term that grows fastest as n increases is what matters for large inputs. For example, in 1000n + 5n^2, the n^2 term dominates for n > 200, so the overall complexity is O(n^2).

**Considering worst, average, and best cases** provides complete analysis. Quick Sort runs in O(n^2) worst case but O(n log n) on average. Hash table lookups are O(1) average case but O(n) worst case if collisions are poorly handled. Understanding these distinctions prevents surprises in production systems.

**Dropping constants and coefficients** is essential to Big O analysis. O(3n) simplifies to O(n), and O(n/2) also simplifies to O(n). The notation captures asymptotic behavior, not precise operation counts.

**Space complexity** is analyzed similarly to time complexity. An algorithm using n^2 auxiliary space has O(n^2) space complexity, which may be as important as time complexity for memory-constrained environments.

## Related

- [[Algorithm Analysis]] - The broader discipline of evaluating algorithm performance
- [[Data Structures]] - How data organization affects complexity
- [[Binary Search Tree]] - Data structure with O(log n) operations
- [[Sorting Algorithms]] - Survey of O(n^2) vs O(n log n) sorting methods
- [[Hash Table]] - Data structure achieving O(1) average-case lookups
- [[Dynamic Programming]] - Optimization technique for exponential problems
- [[Complexity Classes]] - P vs NP and computational complexity theory
