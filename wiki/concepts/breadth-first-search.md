---
title: "Breadth First Search"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, graph-traversal, shortest-path, unweighted-graphs]
---

# Breadth First Search

## Overview

Breadth First Search (BFS) is a fundamental graph traversal algorithm that explores vertices in layers, visiting all neighbors of a vertex before moving to their neighbors. Starting from a source vertex, BFS visits all vertices at distance 1, then all at distance 2, and so on, naturally discovering the shortest path in unweighted graphs. This layer-by-layer exploration gives BFS its distinctive character and makes it ideal for problems involving shortest paths, level-order traversal, and connected component identification.

The algorithm uses a queue data structure to maintain the frontier of exploration, ensuring vertices are processed in the order they were discovered. This FIFO (First In, First Out) behavior is precisely what produces the breadth-first layering effect.

## Key Concepts

### Queue-Based Exploration

BFS processes vertices in first-in-first-out order. When a vertex is dequeued, all its unvisited neighbors are enqueued. This guarantees that when a vertex is first discovered, the path used to reach it is the shortest possible path in an unweighted graph.

### Distance and Parent Tracking

During BFS, we track two critical pieces of information for each vertex:
- **Distance**: Number of edges from the source to this vertex (shortest path length)
- **Parent**: The vertex from which this one was first discovered (enabling path reconstruction)

### Visited Set

To prevent infinite loops in cyclic graphs, BFS maintains a visited set. Once a vertex is marked visited, it will never be enqueued again, ensuring each vertex is processed exactly once.

## How It Works

### Algorithm Steps

1. Initialize a queue with the source vertex, mark it visited, set distance to 0
2. While queue is not empty:
   - Dequeue vertex v
   - For each unvisited neighbor u of v:
     - Mark u visited
     - Set u's parent to v
     - Set u's distance to v's distance + 1
     - Enqueue u

```python
from collections import deque, defaultdict

def bfs(graph, source):
    visited = set()
    parent = {}
    distance = {source: 0}

    queue = deque([source])
    visited.add(source)

    while queue:
        v = queue.popleft()

        for u in graph[v]:
            if u not in visited:
                visited.add(u)
                parent[u] = v
                distance[u] = distance[v] + 1
                queue.append(u)

    return parent, distance
```

### Time and Space Complexity

- **Time**: O(V + E) where V is vertices and E is edges—every vertex and edge is examined exactly once
- **Space**: O(V) for the visited set, queue, and distance/parent dictionaries

## Practical Applications

- **Shortest Path in Unweighted Graphs**: Finding minimum number of hops between nodes in social networks, routing protocols, or game move planners
- **Level-Order Tree Traversal**: Printing binary tree nodes level by level (useful for visualization)
- **Connected Components**: Finding all reachable vertices from a source in undirected graphs
- **Bipartite Graph Checking**: Using BFS to color and verify bipartite property
- **Web Crawlers**: Crawling pages at constant depth before going deeper (politeness policy)

## Examples

```python
# Reconstruct shortest path from source to target
def reconstruct_path(parent, source, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path if path and path[0] == source else []

# BFS with early exit when target found
def bfs_find_target(graph, source, target):
    if source == target:
        return [source]

    queue = deque([source])
    visited = {source}
    parent = {source: None}

    while queue:
        v = queue.popleft()

        for u in graph[v]:
            if u == target:
                # Reconstruct path
                path = []
                while u is not None:
                    path.append(u)
                    u = parent[u]
                return path[::-1]

            if u not in visited:
                visited.add(u)
                parent[u] = v
                queue.append(u)

    return None  # Target not reachable
```

## Related Concepts

- [[Depth First Search]] - Explores aggressively along each branch before backtracking
- [[Binary Search]] - Works on sorted data with O(log n) complexity vs BFS's O(V+E)
- [[Dijkstra Algorithm]] - Extension for weighted graphs with non-negative weights
- [[Binary Search Tree]] - Tree structure where BFS-level order yields sorted sequence in some contexts

## Further Reading

- "Introduction to Algorithms" (CLRS) - Chapter 22 covers graph search algorithms
- Visualgo website provides interactive BFS/Dijkstra/A* visualization
- Graph theory textbooks for formal treatment of BFS properties

## Personal Notes

BFS was my first introduction to thinking about graph algorithms, and the queue-based approach still feels intuitive. The key insight is that BFS gives you shortest paths in unweighted graphs for free—not just the distance, but by tracking parents, you can reconstruct the actual path. For weighted graphs, you need Dijkstra or Bellman-Ford.
