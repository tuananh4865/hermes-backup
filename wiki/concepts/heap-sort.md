---
title: "Heap Sort"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, sorting, data-structures, heap, in-place-sorting]
---

# Heap Sort

## Overview

Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure to sort elements in ascending or descending order. It combines the best properties of selection sort and binary heap processing: like selection sort, it performs in-place sorting with O(1) space complexity, but it reduces the number of comparisons needed by leveraging the heap's efficient max/min extraction property. Heap Sort achieves O(n log n) time complexity in all cases—best, average, and worst case—which makes it predictable and suitable for real-time systems where worst-case performance guarantees matter.

The algorithm works in two distinct phases. First, it builds a max-heap from the unsorted input array. Second, it repeatedly extracts the maximum element (the root of the heap) and places it at the end of the array, then restores the heap property for the remaining elements. This continues until the heap is empty and the array is fully sorted.

Heap Sort is not a stable sort, meaning it may change the relative order of equal elements during sorting. For applications requiring stability, alternative algorithms like [[Merge Sort]] or [[Insertion Sort]] should be considered.

## Key Concepts

### Binary Heap

A binary heap is a complete binary tree where each parent node has a value greater than or equal to (max-heap) or less than or equal to (min-heap) its children. For Heap Sort, we use a max-heap where the largest element is always at the root. The binary heap is stored as an implicit data structure in a contiguous array for cache efficiency.

In the array representation, for a node at index `i`:
- Parent node is at index `(i - 1) // 2`
- Left child is at index `2 * i + 1`
- Right child is at index `2 * i + 2`

### Heap Property

The heap property states that for every node, the value of the node is greater than or equal to the values of its children (in a max-heap). Maintaining this property is crucial during both the heap construction phase and the extraction phase.

### Complete Binary Tree

Heap Sort relies on the complete binary tree property, which ensures the tree is perfectly balanced except possibly for the last level. This guarantees O(log n) height, enabling efficient insertion, deletion, and extraction operations.

## How It Works

The Heap Sort algorithm proceeds through the following steps:

**Step 1: Build Max-Heap**
Convert the unsorted array into a max-heap. Starting from the last non-leaf node (index `n//2 - 1`), apply the `heapify` operation to each node going upward. The `heapify` operation ensures that a subtree rooted at a given index satisfies the heap property by comparing the node with its children and swapping if necessary, then recursively heapifying the affected child subtree.

```python
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def build_max_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
```

**Step 2: Extract Maximum**
Swap the root (maximum element) with the last element of the heap. Reduce the heap size by one. Restore the max-heap property by calling `heapify` on the new root. Repeat until all elements are extracted.

```python
def heap_sort(arr):
    n = len(arr)
    build_max_heap(arr)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move max to end
        heapify(arr, i, 0)  # Restore heap for remaining elements
```

## Practical Applications

Heap Sort is particularly useful in several scenarios:

**Priority Queue Implementations**: Heap Sort's underlying data structure—the binary heap—is ideal for implementing priority queues where quick access to the maximum (or minimum) element is needed. Operating system task schedulers use heaps to manage process priorities.

**Real-Time Systems**: The guaranteed O(n log n) worst-case time complexity makes Heap Sort suitable for systems where predictable performance is critical, such as embedded systems, financial trading platforms, and aerospace control systems.

**Memory-Constrained Environments**: With O(1) auxiliary space complexity, Heap Sort is preferred over [[Quick Sort]] (which requires O(log n) stack space in the worst case) in environments where memory is limited.

**K-th Largest Element Problems**: The heap structure allows efficient extraction of the k-th largest (or smallest) element without fully sorting the entire dataset, which is useful in analytics and data streaming scenarios.

## Examples

Consider sorting the array `[4, 10, 3, 5, 1]` using Heap Sort:

Initial array as binary tree:
```
        4
       / \
      10   3
     /  \
    5    1
```

After building max-heap:
```
        10
       /  \
      5    3
     / \
    4   1
```

After first extraction (swap 10 and 1, heapify):
```
        5
       / \
      4   3
     /
    1
```

After fully sorted: `[1, 3, 4, 5, 10]`

## Related Concepts

- [[Binary Tree]] - The foundational data structure for heap operations
- [[Priority Queue]] - A common application of heap data structures
- [[Quick Sort]] - Another O(n log n) comparison sort with different performance characteristics
- [[Merge Sort]] - Stable, O(n log n) sorting algorithm with higher space requirements
- [[Selection Sort]] - Simpler sorting algorithm with O(n²) complexity
- [[Heaps]] - The priority queue data structure underlying Heap Sort
- [[In-Place Sorting]] - Algorithms that use constant extra space

## Further Reading

- "Introduction to Algorithms" (CLRS) - Chapter 6 covers heap sort in detail
- "The Art of Computer Programming, Volume 3" by Donald Knuth - Classic reference on sorting algorithms
- Binary heap visualization tools online help build intuition for the algorithm's mechanics

## Personal Notes

Heap Sort's guarantee of O(n log n) in all cases is often overlooked in favor of Quick Sort's average-case performance. However, in production systems handling sensitive financial data or real-time operations, the predictable worst-case behavior is invaluable. The algorithm's in-place nature is also underappreciated—it uses no extra memory beyond the input array. When implementing, be careful with array indexing off-by-one errors, as the parent-child relationship calculations are a common source of bugs.
