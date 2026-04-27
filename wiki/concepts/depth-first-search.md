---
title: "Depth First Search"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, graph-traversal, backtracking, recursive-algorithms]
---

# Depth First Search

## Overview

Depth First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking. Unlike breadth first search's layer-by-layer approach, DFS plunges deep into the graph's structure, making it particularly valuable for problems involving path finding, cycle detection, topological sorting, and solving puzzles by exhaustive search. The algorithm's recursive nature naturally mirrors how many problems unfold—exploring one possibility fully before considering alternatives.

DFS can be implemented recursively with an implicit stack (the call stack) or iteratively using an explicit stack data structure. Both approaches visit each vertex exactly once in an undirected graph, and can handle directed graphs with appropriate edge classification.

## Key Concepts

### Backtracking

The defining characteristic of DFS is its use of backtracking—after exploring one path completely, it returns to the previous vertex to try an unexplored branch. This systematic exploration guarantees that if a path exists, DFS will find it, though not necessarily the shortest path.

### Discovery and Finish Times

DFS assigns two timestamps to each vertex:
- **Discovery time (d[v])**: When the vertex is first visited
- **Finish time (f[v])**: When all descendants have been fully explored and backtracking occurs

These timestamps are fundamental to many DFS applications and form the basis of the parenthesis theorem: a vertex's discovery-finish interval properly contains its descendants' intervals.

### Edge Classification

In directed graphs, DFS edges are classified as:
- **Tree edges**: Lead to unvisited vertices (build the DFS forest)
- **Back edges**: Lead to an ancestor (indicate cycles)
- **Forward edges**: Lead to a descendant in same DFS tree
- **Cross edges**: Lead to neither ancestor nor descendant

## How It Works

### Recursive Implementation

```python
def dfs_recursive(graph, v, visited=None):
    if visited is None:
        visited = set()

    visited.add(v)
    print(f"Discovering {v}")  # Process vertex

    for neighbor in graph[v]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    print(f"Finishing {v}")  # Post-processing
    return visited
```

### Iterative Implementation

```python
def dfs_iterative(graph, source):
    visited = set()
    stack = [source]

    while stack:
        v = stack.pop()

        if v not in visited:
            visited.add(v)
            print(f"Discovering {v}")

            # Add neighbors in reverse order to process in order
            for neighbor in reversed(graph[v]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited
```

### Time and Space Complexity

- **Time**: O(V + E)—every vertex and edge is examined exactly once
- **Space**: O(V) for visited set and stack (or O(h) for recursion depth where h is the height of the DFS tree)

## Practical Applications

- **Topological Sort**: Ordering directed acyclic graphs for task scheduling, course prerequisites, build systems
- **Cycle Detection**: Identifying whether a graph contains cycles (critical for deadlock detection)
- **Path Finding**: Finding any path between two vertices (not necessarily shortest)
- **Connected Components**: Identifying strongly connected components in directed graphs using Kosaraju's algorithm
- **Maze Solving**: DFS can solve mazes, though it may not find the shortest solution
- **Strongly Connected Components**: Kosaraju and Tarjan's algorithms both rely on DFS

## Examples

```python
# Topological sort using DFS
def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(v):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(v)  # Push after exploring all neighbors

    for v in graph:
        if v not in visited:
            dfs(v)

    return stack[::-1]  # Reverse to get topological order

# Detecting cycles in directed graph
def has_cycle(graph):
    visited = set()
    rec_stack = set()  # Vertices in current recursion path

    def dfs(v):
        visited.add(v)
        rec_stack.add(v)

        for neighbor in graph[v]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True  # Back edge found = cycle

        rec_stack.remove(v)
        return False

    for v in graph:
        if v not in visited:
            if dfs(v):
                return True
    return False
```

## Related Concepts

- [[Breadth First Search]] - Layer-by-layer exploration vs. deep exploration
- [[Binary Search]] - Divide-and-conquer search for sorted data
- [[Dijkstra Algorithm]] - Shortest path in weighted graphs with priority queue
- [[Bellman Ford]] - Shortest path handling negative weights
- [[A Star]] - Heuristic-guided pathfinding using estimated distances

## Further Reading

- "Introduction to Algorithms" (CLRS) - Chapter 22 provides formal treatment
- "The Algorithm Design Manual" by Skiena - Practical DFS applications
- Visualgo and Graph Online for interactive exploration

## Personal Notes

DFS feels like exploring a maze with a trail of breadcrumbs. The recursive version is elegant and directly expresses the backtracking nature, but iterative is essential for graphs with extreme depth (to avoid stack overflow). The discovery/finish times were confusing at first but become intuitive once you realize they represent the entry and exit from the "scope" of each vertex's exploration.
