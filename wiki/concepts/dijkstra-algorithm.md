---
title: "Dijkstra Algorithm"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, shortest-path, graph-algorithms, greedy-algorithms, weighted-graphs]
---

# Dijkstra Algorithm

## Overview

Dijkstra's algorithm finds the shortest paths from a source vertex to all other vertices in a weighted graph with non-negative edge weights. Published by Edsger W. Dijkstra in 1959, it remains one of the most important algorithms in computer science, forming the foundation for routing protocols, mapping services, and countless optimization problems. The algorithm combines the greedy method with a priority queue to achieve excellent performance, making it the default choice for shortest path problems in practice.

The key insight is that once a vertex is extracted from the priority queue with the smallest tentative distance, that distance is final—no shorter path to that vertex can ever be found. This optimality property, combined with non-negative weights, ensures correctness.

## Key Concepts

### Greedy Approach

Dijkstra is fundamentally greedy: at each step, it selects the unvisited vertex with the smallest known distance from the source. This locally optimal choice leads to a globally optimal solution when edge weights are non-negative, because any alternative path to the selected vertex would have to go through an unvisited vertex with at least as large a distance.

### Relaxation

The core operation in Dijkstra is edge relaxation. For a vertex u being processed, for each neighbor v with edge weight w(u,v), if the distance through u is shorter than v's current known distance, we update v's distance and set u as its predecessor:

```python
if dist[u] + w < dist[v]:
    dist[v] = dist[u] + w
    prev[v] = u
```

### Priority Queue Integration

The algorithm's efficiency depends critically on efficiently selecting the minimum-distance unvisited vertex. Using a binary heap (min-heap) gives O((V + E) log V) complexity. With a Fibonacci heap, extraction is O(log V) but amortized, yielding O(V log V + E).

## How It Works

### Algorithm Steps

1. Initialize distances: dist[source] = 0, dist[all others] = infinity
2. Add all vertices to priority queue with their current distances
3. While priority queue not empty:
   - Extract vertex u with minimum distance
   - If u is already processed (outdated entry), skip
   - For each neighbor v of u:
     - If dist[u] + weight(u,v) < dist[v]:
       - Update dist[v] and prev[v]
       - Decrease key in priority queue

```python
import heapq

def dijkstra(graph, source):
    dist = {v: float('inf') for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0

    pq = [(0, source)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:  # Skip outdated entries
            continue

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev
```

### Time Complexity

- **Binary Heap**: O((V + E) log V) — most common implementation
- **Fibonacci Heap**: O(V log V + E) — theoretical improvement for dense graphs
- **Array**: O(V²) — acceptable for small graphs, no extra space

## Practical Applications

- **GPS Navigation**: Real-time route finding with road network distances
- **Network Routing**: OSPF and IS-IS routing protocols use Dijkstra variants
- **Flight Reservations**: Finding cheapest routes considering ticket prices
- **Game Pathfinding**: NPC navigation in games with terrain costs
- **Robot Navigation**: Planning paths while avoiding obstacles with movement costs

## Examples

```python
# Reconstruct path from source to target
def reconstruct_path(prev, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = prev[current]

    path.reverse()
    return path

# Directed graph as adjacency list
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}

dist, prev = dijkstra(graph, 'A')
print(f"Shortest distances: {dist}")
print(f"Path to E: {reconstruct_path(prev, 'E')}")
```

## Related Concepts

- [[Bellman Ford]] - Handles negative weights and detects negative cycles
- [[Breadth First Search]] - Dijkstra without weights (unit edges)
- [[A Star]] - Dijkstra with heuristic guidance for targeted search
- [[Binary Search]] - Different search strategy for sorted data
- [[Heap]] - Priority queue data structure powering Dijkstra's efficiency

## Further Reading

- Dijkstra's original 1959 paper: "A note on two problems in connexion with graphs"
- "Introduction to Algorithms" (CLRS) - Chapter 24 for comprehensive coverage
- "Algorithms" by Sedgewick for practical implementation details

## Personal Notes

Dijkstra's elegance lies in its simplicity—three lines of relaxation logic combined with a priority queue produce such powerful results. I initially overlooked the nuance of handling outdated priority queue entries, but this "lazy deletion" pattern is crucial for correct implementation. For graphs with negative edge weights, always use Bellman-Ford instead.
