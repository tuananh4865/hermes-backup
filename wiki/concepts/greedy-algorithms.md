---
title: "Greedy Algorithms"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, optimization, problem-solving, design-paradigms]
---

# Greedy Algorithms

## Overview

Greedy algorithms build solutions piece by piece, always choosing the next piece that offers the most immediate benefit—the locally optimal choice—without considering how those choices affect future choices. The hope, and the key question for each greedy problem, is whether locally optimal choices lead to a globally optimal solution. When this property holds, called optimal prefix structure or the greedy-choice property, greedy algorithms can find optimal solutions efficiently.

The paradigm contrasts sharply with approaches like dynamic programming, which considers all possible choices and their future consequences. Greedy algorithms are typically faster (often O(n) or O(n log n)) because they make decisions in a single pass without lookahead. However, they only work when the problem exhibits the right structure.

Greedy algorithms underlie many fundamental computer science concepts and real-world systems. Huffman coding builds optimal prefix-free codes through greedy merging. Dijkstra's algorithm finds shortest paths by greedily selecting the nearest unvisited node. Minimum spanning tree algorithms like Kruskal's and Prim's use greedy approaches. Task scheduling, resource allocation, and compression all have greedy solutions.

## Key Concepts

**Greedy-Choice Property** is the critical requirement for greedy algorithms to be correct. It means that there exists an optimal solution where the first choice (or every choice) is the locally optimal one. If we can prove that making the locally optimal choice never prevents us from achieving the global optimum, the greedy algorithm is correct.

**Optimal Prefix Property** states that an optimal solution can be constructed by making locally optimal choices at each step. This is related to matroid theory—certain combinatorial structures guarantee that greedy algorithms work. Problems that form matroids include spanning trees, matching, and certain scheduling problems.

**Proof Techniques** for greedy correctness typically use exchange arguments. The proof shows that any optimal solution can be transformed into the greedy solution through a series of exchanges where each exchange replaces a choice with the greedy choice without making the solution worse. This demonstrates that the greedy solution is as good as any optimal solution.

**Irrevocability** distinguishes greedy from other approaches. Once a greedy choice is made, it's never reconsidered. This makes greedy algorithms fast and simple but requires that future consequences truly don't matter. For problems like the traveling salesman, this irrevocability dooms greedy approaches to produce poor results.

**Matroid Structure** provides a formal framework for understanding when greedy works. A matroid is a set system satisfying two properties: hereditary (any subset of a feasible set is feasible) and exchange (if two feasible sets have different sizes, you can add an element from the larger to the smaller while staying feasible). Greedy algorithms optimally solve any optimization problem where feasible sets form a matroid.

## How It Works

The greedy algorithm structure is deceptively simple:

1. **Selection**: Choose the best remaining element according to some heuristic (minimum cost, maximum value, closest distance, etc.)
2. **Feasibility**: Check if the choice maintains a valid solution space
3. **Termination**: Stop when a complete solution is built
4. **No Backtracking**: Once chosen, an element is never excluded

```python
# Activity Selection Problem: Maximum number of non-overlapping activities
def activity_selection(activities):
    # Sort by finish time (greedy criterion)
    sorted_activities = sorted(activities, key=lambda x: x[1])
    
    selected = []
    last_end = 0
    
    for start, end in sorted_activities:
        if start >= last_end:  # Greedy choice: pick if compatible
            selected.append((start, end))
            last_end = end
    
    return selected

# activities = [(start, end), ...]
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 12)]
print(activity_selection(activities))
# Output: [(1, 4), (5, 7), (8, 12)] - maximum non-overlapping activities
```

## Practical Applications

**Huffman Coding**: Builds optimal prefix-free variable-length codes for compression. The greedy algorithm repeatedly merges the two nodes with lowest frequency, forming a binary tree where leaf nodes represent symbols. This produces codes where frequent symbols get short representations—fundamental to ZIP files, JPEG, and MP3.

**Dijkstra's Shortest Path**: Finds shortest paths from a source to all vertices in a weighted graph with non-negative weights. The algorithm greedily extracts the vertex with minimum distance, updating distances through that vertex. It's the foundation of internet routing protocols like OSPF and IS-IS.

**Minimum Spanning Tree**: Both Kruskal's (sort edges, add smallest that doesn't form cycle) and Prim's (grow tree from a vertex, adding smallest connecting edge) are greedy algorithms. MST problems appear in network design, clustering, and approximation algorithms for other NP-hard problems.

**Task Scheduling**: When scheduling weighted jobs on a single machine to maximize weight completed before deadlines, the greedy algorithm sorts by weight/deadline ratio and schedules jobs that fit. This is provably optimal.

**Coin Change (特定 denominations)**: For canonical coin systems (like US coins: 1, 5, 10, 25), greedy produces optimal solutions. However, for arbitrary denominations, greedy can fail—demonstrating that greedy correctness depends on the specific problem structure.

## Examples

**Fractional Knapsack Problem**: Given items with weights and values, maximize value with weight limit, but you can take fractions of items:

```python
def fractional_knapsack(items, capacity):
    # Sort by value-to-weight ratio (greedy criterion)
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    
    for weight, value in sorted_items:
        if remaining_capacity == 0:
            break
        
        # Take as much as possible of this item
        take_weight = min(weight, remaining_capacity)
        total_value += take_weight * (value / weight)
        remaining_capacity -= take_weight
    
    return total_value

items = [(10, 60), (20, 100), (30, 120)]  # (weight, value)
capacity = 50
print(fractional_knapsack(items, capacity))  # Output: 240
# Take all of 10 (60) and 20 (100), and 2/3 of 30 (80) = 240
```

**Huffman Coding Example**:

```python
import heapq
from collections import Counter

def huffman_coding(text):
    # Count frequency of each character
    freq = Counter(text)
    
    # Create priority queue (min-heap by frequency)
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    
    # Greedy merge: combine two smallest frequencies
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    # Extract codes from root
    codes = heapq.heappop(heap)[1:]
    return {char: code for char, code in codes}

text = "hello world"
codes = huffman_coding(text)
print(codes)  # {'l': '00', 'o': '01', 'h': '100', 'e': '101', ...}
```

## Related Concepts

- [[Dynamic Programming]] - Alternative approach when greedy fails
- [[Divide and Conquer]] - Recursive paradigm without the greedy choice
- [[Dijkstra's Algorithm]] - Greedy shortest path algorithm
- [[Minimum Spanning Tree]] - Greedy MST algorithms
- [[Huffman Coding]] - Greedy compression algorithm
- [[Matroid Theory]] - Formal foundation for greedy correctness

## Further Reading

- [CLRS Chapter 16: Greedy Algorithms](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - Formal treatment with proofs
- [Greedy Algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Greedy_algorithm) - Overview and examples
- [Matroid Theory (Wikipedia)](https://en.wikipedia.org/wiki/Matroid) - Formal foundations

## Personal Notes

Greedy algorithms taught me that "obvious" choices can be mathematically proven correct—or subtly wrong. The hardest part isn't implementing greedy algorithms; it's proving they're correct. The exchange argument proof technique clicked when I realized it shows that any optimal solution can be transformed into the greedy solution step by step. When I'm stuck on a problem, I try greedy first: sort by some criterion, take the best, and see if it works. If it fails, the problem likely has overlapping subproblems requiring DP.
