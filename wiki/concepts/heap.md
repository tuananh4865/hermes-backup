---
title: "Heap"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, heap, priority-queue, binary-heap, algorithms]
---

# Heap

## Overview

A heap is a specialized binary tree-based data structure that satisfies the heap property. In a max-heap, parent nodes always have values greater than or equal to their children, making the largest element always accessible at the root. Conversely, a min-heap ensures parent nodes have values less than or equal to their children, with the smallest element at the root. Heaps are fundamental to many algorithms including priority queues, heap sort, and graph algorithms like Prim's and Dijkstra's.

The elegance of the heap lies in its ability to maintain the heap property efficiently after insertions and deletions, both operations completing in O(log n) time. This makes heaps indispensable when you need to repeatedly access the maximum or minimum element while maintaining a dynamic collection.

## Key Concepts

### Binary Heap Structure

A binary heap is a complete binary tree stored compactly in an array. Being "complete" means all levels except possibly the last are filled, and the last level is filled from left to right. This compact storage eliminates wasted space and enables simple index-based navigation between parent and child nodes.

For any node at index `i`:
- Parent index: `(i - 1) // 2`
- Left child index: `2 * i + 1`
- Right child index: `2 * i + 2`

### Heap Property

The defining characteristic that distinguishes heaps from ordinary binary trees. In a max-heap, `parent >= child` for all nodes. In a min-heap, `parent <= child`. This property must hold after every operation on the heap.

### Priority Queue Interface

Heaps naturally implement priority queues where elements are extracted based on their priority rather than insertion order. The root is always the highest-priority element, making access O(1) while insertion and extraction are both O(log n).

## How It Works

### Heapify: Building the Heap

Heapify is the process of converting an arbitrary array into a valid heap. Starting from the last non-leaf node (index `n//2 - 1`), we "sift down" each node by comparing it with its children and swapping if necessary. This operation cascades upward and runs in O(n) time.

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
```

### Insertion

To insert an element, add it at the next available position (end of array) and "sift up" by comparing with parent and swapping until the heap property is restored. This takes O(log n) time.

### Extraction (Pop Root)

Remove the root element, replace it with the last element, then sift down from the root to restore the heap property. This is the basis for heap sort and priority queue pop operations.

## Practical Applications

- **Priority Queue Implementations**: Task schedulers, event-driven simulations, and network packet processing rely on heaps to manage items by urgency
- **Heap Sort**: A comparison-based sorting algorithm with O(n log n) worst case and O(1) space
- **Graph Algorithms**: Prim's minimum spanning tree and Dijkstra's shortest path use min-heaps for efficient vertex extraction
- **Order Statistics**: Finding the k-th largest/smallest element in O(n) time using a variant called quickselect-heap

## Examples

```python
import heapq

# Min-heap (lowest element has highest priority)
heap = []
heapq.heappush(heap, (3, "task A"))
heapq.heappush(heap, (1, "task B"))
heapq.heappush(heap, (2, "task C"))

# Extract highest priority (lowest number)
print(heapq.heappop(heap))  # (1, "task B")

# For max-heap, negate values
max_heap = []
heapq.heappush(max_heap, (-3, "low priority"))
heapq.heappush(max_heap, (-1, "high priority"))
print(heapq.heappop(max_heap))  # (-1, "high priority")
```

## Related Concepts

- [[Binary Search Tree]] - Another tree structure for ordered data, though with different guarantees
- [[Priority Queue]] - Abstract data type commonly implemented with heaps
- [[Dijkstra Algorithm]] - Uses min-heap for efficient shortest path computation
- [[Binary Search]] - Different search strategy for sorted data

## Further Reading

- "Introduction to Algorithms" (CLRS) - Chapter 6 covers heaps and heap sort
- Heap visualization tools available through algorithm animation websites

## Personal Notes

Heaps are deceptively simple yet incredibly powerful. The insight that a complete binary tree can be stored so compactly and manipulated so efficiently remains one of the elegant results in data structures. Remember: if you need fast access to min/max with dynamic updates, reach for a heap.
