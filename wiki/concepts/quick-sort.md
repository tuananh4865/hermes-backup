---
title: "Quick Sort"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, sorting, divide-and-conquer, recursion, in-place]
---

# Quick Sort

## Overview

Quick Sort is a highly efficient, comparison-based divide-and-conquer sorting algorithm invented by Tony Hoare in 1959. It achieves an average time complexity of O(n log n) and frequently outperforms other sorting algorithms in practice due to its efficient cache utilization and low overhead. Quick Sort works by selecting a "pivot" element from the array and partitioning the other elements into two subarrays—those less than the pivot and those greater than or equal to the pivot—then recursively sorting the subarrays.

Despite its worst-case O(n²) complexity (which occurs with poorly chosen pivots on already-sorted data), randomized or median-of-three pivot selection strategies make this scenario exceedingly rare in practice. Quick Sort is an in-place algorithm requiring only O(log n) auxiliary space for the recursion stack, making it memory-efficient for large datasets.

## Key Concepts

**Pivot Selection**: The choice of pivot critically affects Quick Sort's performance. Common strategies include:
- First or last element (risky for sorted inputs)
- Median-of-three (first, middle, last elements)
- Random element (provides probabilistic guarantees)
- Ninther: median of three medians of three (used in some optimized implementations)

**Partitioning**: The core operation that rearranges elements around the pivot. The Lomuto partition scheme is simpler; the Hoare partition scheme is more efficient but trickier to implement correctly.

**In-Place Sorting**: Quick Sort achieves space efficiency by performing partitioning operations directly on the input array, swapping elements in position rather than creating copies.

**Recursion and Tail Call Optimization**: Recursive calls can be converted to iterative loops with explicit stack management for environments that don't optimize tail recursion.

## How It Works

The algorithm follows these steps:

1. **Choose a pivot** from the array (commonly the last element or a random element)
2. **Partition** the array into two parts:
   - Elements less than pivot → left side
   - Elements greater than or equal to pivot → right side
3. **Place pivot** in its final sorted position (between the two parts)
4. **Recursively sort** the left and right subarrays
5. **Base case**: Arrays of size 0 or 1 are already sorted

```python
def quicksort(arr, low, high):
    """
    Quick Sort implementation with Hoare partitioning.
    Time:  O(n log n) average, O(n²) worst
    Space: O(log n) for recursion stack
    """
    if low < high:
        pivot_index = hoare_partition(arr, low, high)
        quicksort(arr, low, pivot_index)      # Exclude pivot
        quicksort(arr, pivot_index + 1, high)

def hoare_partition(arr, low, high):
    """
    Hoare partition scheme - more efficient than Lomuto.
    Returns index where elements < pivot are on left, >= on right.
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Move i right until we find element >= pivot
        while True:
            i += 1
            if arr[i] >= pivot:
                break
        
        # Move j left until we find element < pivot
        while True:
            j -= 1
            if arr[j] < pivot:
                break
        
        # Swap and continue, or return if pointers cross
        if i >= j:
            return j
        
        arr[i], arr[j] = arr[j], arr[i]
```

## Practical Applications

- **General-purpose sorting** in standard libraries (many language runtimes use introsort—a hybrid of Quick Sort, Heap Sort, and Insertion Sort)
- **Database sorting** for ORDER BY queries on large datasets
- **External sorting** when data doesn't fit in memory, using a hybrid merge sort
- **Embedded systems** where memory is constrained (in-place nature helps)
- **Parallel implementations** — Quick Sort's divide-and-conquer structure maps well to parallel processing

## Examples

Sorting the array `[3, 7, 1, 8, 4, 2, 9, 5, 6]` with last-element pivot:

```
Initial: [3, 7, 1, 8, 4, 2, 9, 5, 6], pivot = 6
After partition: [3, 1, 4, 2, 5 | 6 | 7, 8, 9]
Recursively sort [3, 1, 4, 2, 5] and [7, 8, 9]
...
Final: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

For sorted input `[1,2,3,4,5]` with first-element pivot, naive Quick Sort degrades to O(n²). Using randomized pivot selection ensures O(n log n) expected time regardless of input order.

## Related Concepts

- [[Merge Sort]] - Another O(n log n) divide-and-conquer sort; stable but requires O(n) extra space
- [[Heap Sort]] - Guaranteed O(n log n); in-place but not cache-efficient
- [[Introsort]] - Hybrid algorithm defaulting to Quick Sort but switching to Heap Sort on poor recursion depth
- [[Binary Search]] - Shares divide-and-conquer recursive structure
- [[Big O Notation]] - Used to characterize algorithm complexity

## Further Reading

- Hoare, C.A.R. (1961). "Algorithm 64: Quicksort" - Original publication
- Bentley, Jon. "Programming Pearls: Quicksort-based sorting" - Practical insights
- Sedgewick, Robert. "Algorithms" - Comprehensive treatment of Quick Sort variants

## Personal Notes

Quick Sort remains my go-to sorting algorithm for most practical applications. The key insight is that its average-case performance is so much better than other O(n log n) algorithms in practice that the theoretical worst case rarely matters—unless you're writing code that must handle adversarial inputs. In production systems, I typically prefer introsort (as used by C++ STL and .NET) which gets Quick Sort's average performance with Heap Sort's worst-case guarantee.
