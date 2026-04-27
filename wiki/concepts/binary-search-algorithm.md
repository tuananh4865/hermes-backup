---
title: "Binary Search Algorithm"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, computer-science, search, data-structures, time-complexity]
---

# Binary Search Algorithm

## Overview

Binary search is an efficient algorithm for finding a target value within a sorted array. It works by repeatedly dividing the search interval in half — comparing the target to the middle element and eliminating half of the remaining elements based on whether the target is greater than or less than the middle value. This repeated halving gives binary search its signature logarithmic time complexity of O(log n), making it dramatically faster than linear search O(n) for large datasets.

The algorithm was first documented in 1946 by John Mauchly and was the basis for many early computer science innovations in information retrieval. Binary search is a fundamental building block in computer science education and underlies countless real-world systems: database index lookups, compiler symbol tables, dictionary search features, and version control systems like Git all rely on binary search or closely related structures. Any problem involving finding an element in a sorted collection is a candidate for binary search.

## Key Concepts

**Sorted Input Requirement** — Binary search only works on sorted data. If the data is unsorted, you must sort it first (O(n log n)) before applying binary search. The sorting requirement is the algorithm's main practical constraint.

**Logarithmic Time Complexity O(log n)** — Each comparison eliminates half of the remaining candidates. Starting with n elements, after k steps you have n/2^k elements remaining. You stop when n/2^k < 1, i.e., when k > log_2(n). This means searching a billion-element array takes at most 30 comparisons.

**Divide and Conquer** — Binary search is a textbook divide-and-conquer algorithm: solve a smaller subproblem, and combine results. The "conquer" step here is trivial (just one comparison), which makes it an especially efficient form of divide-and-conquer.

**Iterative vs Recursive** — Binary search can be implemented iteratively (with a while loop and two pointers) or recursively (with base case at empty range). The iterative version is generally preferred for production code to avoid call stack overhead, though both have the same time complexity.

**Integer Overflow** — A subtle bug in many naive implementations is integer overflow when computing the middle index as `(low + high) / 2`. The safe formula is `low + (high - low) / 2`, which avoids overflow when low and high are large 32-bit integers approaching `Integer.MAX_VALUE`.

**Lower Bound / Upper Bound** — Variants of binary search can find the first occurrence of a target value (leftmost) or the last occurrence (rightmost), which is crucial when duplicates are present. These require slight modifications to the core algorithm.

## How It Works

```
Sorted array: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
Target: 11

Step 1: low=0, high=9, mid=4
        arr[4] = 9 < 11 → target is in RIGHT half
        low = mid + 1 = 5

Step 2: low=5, high=9, mid=7
        arr[7] = 15 > 11 → target is in LEFT half
        high = mid - 1 = 6

Step 3: low=5, high=6, mid=5
        arr[5] = 11 == 11 → FOUND at index 5

Total: 3 comparisons (vs 6 for linear search)
```

```python
def binary_search(arr: list, target: int) -> int:
    """
    Iterative binary search.
    Returns the index of target in arr, or -1 if not found.
    Time: O(log n), Space: O(1)
    """
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2  # Avoids integer overflow
        mid_val = arr[mid]

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1   # Target is in right half
        else:
            high = mid - 1  # Target is in left half

    return -1  # Target not found


def binary_search_recursive(arr: list, target: int, low: int, high: int) -> int:
    """Recursive version — same time complexity but uses O(log n) stack space."""
    if low > high:
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)


# Usage examples:
scores = [2, 8, 14, 23, 37, 51, 66, 78, 91, 100]
print(binary_search(scores, 37))   # → 4
print(binary_search(scores, 42))   # → -1 (not found)
```

## Practical Applications

- **Database Index Lookups** — B-trees and B+ trees used by relational databases use binary-search-like algorithms to navigate index levels and find exact keys or ranges efficiently.
- **Version Control (Git)** — Git uses binary search to find the commit that introduced a bug using `git bisect`. With thousands of commits, linear searching would be impractical.
- **IDE Symbol Search** — Compilers and IDEs maintain sorted symbol tables; binary search finds variable and function definitions instantly.
- **Spell Checkers** — Dictionary lookups use binary search to validate words against a sorted word list in milliseconds.
- **Competitive Programming** — Binary search on the answer is a common pattern for optimization problems like finding minimum time to finish jobs given concurrency limits.

## Examples

**Finding insertion position** — Binary search can find where to insert a new element to maintain sorted order, which is how Python's `bisect` module works:

```python
import bisect

sorted_list = [1, 3, 5, 7, 9]
index = bisect.bisect_left(sorted_list, 6)  # → 3 (before element 7)
sorted_list.insert(index, 6)  # → [1, 3, 5, 6, 7]
```

**Binary search on answer** — A powerful pattern where you binary-search the result rather than the data:

```python
def min_days_to_deliver(boxes: list[int], capacity: int) -> int:
    """
    Find minimum days needed to deliver all boxes given daily capacity.
    Binary search on answer: can we deliver in D days?
    """
    def can_deliver_in(days):
        return sum((b + days - 1) // days for b in boxes) <= capacity

    lo, hi = 1, max(boxes)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if can_deliver_in(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Lower bound with duplicates** — Find first occurrence:

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

## Related Concepts

- [[Algorithms]] — The broader discipline of systematic problem-solving procedures
- [[Time Complexity]] — Big O notation for measuring algorithm efficiency
- [[Sorted Arrays]] — The prerequisite data structure for binary search
- [[Divide and Conquer]] — The algorithmic paradigm binary search exemplifies
- [[Linear Search]] — The O(n) alternative that works on unsorted data
- [[Binary Search Tree]] — A data structure that maintains sorted order with binary-search-like operations
- [[B-Tree]] — The index structure used by databases, built on binary-search-like navigation

## Further Reading

- Cormen, T. et al. "Introduction to Algorithms" (CLRS) — Chapter 3 (growth of functions) and Chapter 4 (divide-and-conquer) provide foundational context.
- "Binary Search" — Khan Academy's interactive visualization of the algorithm step-by-step.
- "Git Bisect" — How Linus Torvalds built binary search into Git for debugging.
- "The Joy of Algorithms" — A collection of elegant binary search variations and applications.

## Personal Notes

Binary search is one of those algorithms that feels obvious in hindsight but took years for computer scientists to properly formalize. The bugaboos are integer overflow (always use `low + (high - low) // 2`) and off-by-one errors in the loop condition. I find the iterative version more intuitive to reason about — the recursion adds conceptual overhead without any practical benefit for a tail-recursive algorithm. What really opened my eyes was the "binary search on answer" pattern: the idea that you can binary search the *result* space rather than the input data unlocks solutions for a surprising number of optimization problems.
