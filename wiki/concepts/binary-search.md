---
title: "Binary Search"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, search, divide-and-conquer, logarithmic-time]
---

# Binary Search

## Overview

Binary search is a highly efficient algorithm for finding a target value within a sorted array. It works by repeatedly dividing the search interval in half, comparing the middle element to the target, and eliminating half of the remaining elements based on this comparison. With O(log n) time complexity, binary search transforms what could be millions of operations into just a handful of comparisons, making it essential for any performance-conscious developer working with sorted data.

The algorithm's power stems from a simple insight: because the array is sorted, we can make decisions that completely eliminate half of the remaining candidates with each comparison. This logarithmic reduction is dramatic—a sorted array of one billion elements requires at most 30 comparisons to find any target.

## Key Concepts

### Prerequisites

Binary search requires the array to be sorted in a known order (ascending or descending). Without this ordering guarantee, binary search produces incorrect results. If your data isn't sorted, consider whether the cost of sorting (O(n log n)) is justified by the search frequency.

### Search Space

The fundamental unit in binary search is the search space—the contiguous range of indices where the target might exist. Initially, this spans the entire array. Each iteration narrows this space by adjusting either the low or high boundary.

### Termination Conditions

Binary search terminates when:
- The target is found (return its index)
- The search space becomes empty (low > high), indicating the target doesn't exist

## How It Works

### Iterative Implementation

The iterative approach uses a while loop with two pointers tracking the search boundaries:

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2  # Integer division

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1  # Target is in right half
        else:
            high = mid - 1  # Target is in left half

    return -1  # Target not found
```

### Recursive Implementation

The recursive version naturally expresses the divide-and-conquer nature:

```python
def binary_search_recursive(arr, target, low, high):
    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)
```

### Avoiding Overflow

In languages with fixed-size integers, computing `mid = (low + high) // 2` can overflow for very large arrays. Safer alternatives include:
- `mid = low + (high - low) // 2`
- `mid = (low ^ high) + ((low & high) << 1)` (bitwise approach)

## Practical Applications

- **Database Index Searches**: B-tree structures in databases use principles similar to binary search for fast lookups
- **Dictionary Lookups**: Finding words in sorted dictionaries or phone numbers in sorted contact lists
- **Debugging Version Control**: Finding the specific commit that introduced a bug using git bisect
- **Monotonic Function Finding**: Finding roots of monotonic functions or solving optimization problems with binary search on the answer

## Examples

```python
# Finding first occurrence of target (lower bound)
def binary_search_first(arr, target):
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1  # Continue searching left
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result

# Finding insertion position in sorted array
import bisect
index = bisect.bisect_left(sorted_array, target)
```

## Related Concepts

- [[Heap]] - Different data structure for different access patterns (min/max vs. arbitrary search)
- [[Breadth First Search]] - Graph traversal that explores level by level, unlike binary search's focused narrowing
- [[Depth First Search]] - Another graph traversal approach with different exploration patterns
- [[Interpolation Search]] - Variant that estimates position based on value distribution

## Further Reading

- "Algorithms" by Sedgewick and Wayne - Binary search variants and applications
- "Programming Pearls" by Jon Bentley - Classic treatment of binary search implementation pitfalls

## Personal Notes

Binary search is often underestimated yet hides subtle implementation pitfalls. The classic bug is using `mid = (low + high) / 2` with integer overflow or off-by-one errors in boundary conditions. Always verify your implementation with edge cases: empty array, single element, target at boundaries, target not present. The bisect module in Python is a production-ready reference implementation.
