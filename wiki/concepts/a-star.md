---
title: "A Star"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, pathfinding, heuristic-search, shortest-path, game-development]
---

# A Star

## Overview

A* (pronounced "A-star") is a best-first search algorithm that finds the shortest path from a start node to a goal node by combining Dijkstra's algorithm with a heuristic estimate of the remaining distance. It is both complete (will find a path if one exists) and optimal (will find the shortest path) when using an admissible heuristic. A* is the workhorse of pathfinding in games, robotics, and any domain where efficient targeted search matters more than exploring the entire graph.

The genius of A* is that it doesn't just react to what it discovers—it uses heuristic guidance to explore the most promising paths first. This can reduce search complexity from O(V+E) to dramatically less, especially when the heuristic provides good estimates.

## Key Concepts

### Heuristic Function

The heuristic h(n) estimates the minimum cost from node n to the goal. An admissible heuristic never overestimates the true cost—it always returns a value less than or equal to the actual shortest path distance. Common admissible heuristics include:

- **Euclidean distance**: Straight-line distance (for continuous spaces)
- **Manhattan distance**: |x1-x2| + |y1-y2| (for grid-based movement)
- **Hamming distance**: Count of different digits (for puzzle problems)

### Evaluation Function

A* uses f(n) = g(n) + h(n) where:
- g(n): Actual cost from start to current node n
- h(n): Estimated cost from n to goal (heuristic)
- f(n): Estimated total path cost through n

The algorithm always expands the node with the lowest f(n), balancing known cost against estimated remaining cost.

### Admissibility and Consistency

- **Admissible**: h(n) ≤ true cost to goal for all n (ensures optimality)
- **Consistent (monotonic)**: h(n) ≤ cost(n, successor) + h(successor) (ensures efficiency and allows early termination when goal is reached)

## How It Works

### Algorithm Steps

1. Initialize open set with start node (priority queue ordered by f-score)
2. While open set not empty:
   - Extract node with lowest f-score
   - If node is goal, reconstruct and return path
   - For each neighbor:
     - Calculate tentative g-score
     - If this path to neighbor is better than any previous:
       - Update neighbor's g, h, f scores
       - Set current as predecessor
       - Add neighbor to open set if not already there
3. Return failure if open set exhausted (no path exists)

```python
import heapq

def a_star(graph, start, goal, h):
    """
    graph: dict { node: [(neighbor, cost), ...] }
    h: heuristic function h(node) = estimated cost to goal
    """
    open_set = [(h(start), start)]  # (f-score, node)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: h(start)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor, cost in graph.get(current, []):
            tentative_g = g_score[current] + cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found
```

### Time and Space Complexity

- **Time**: O(E) in worst case, but typically much less with good heuristics
- **Space**: O(V) worst case—all nodes may be in memory

## Practical Applications

- **Game AI Pathfinding**: NPCs navigating game worlds with obstacles, the classic application
- **Robot Navigation**: Path planning for autonomous vehicles around obstacles
- **GPS Navigation**: Route finding with real-world distances and terrain
- **Puzzle Solving**: 8-puzzle, 15-puzzle, Rubik's cube solving
- **Network Routing**: Efficient routing with domain-specific distance estimates
- **Robot Arm Planning**: Moving robotic arms through obstacle-filled spaces

## Examples

```python
import math

def manhattan_distance(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def euclidean_distance(pos, goal):
    return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

# Grid-based pathfinding with obstacles
def astar_grid(grid, start, goal):
    def heuristic(node):
        return manhattan_distance(node, goal)

    graph = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:  # Walkable
                neighbors = []
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < len(grid) and 0 <= nx < len(row):
                        if grid[ny][nx] == 0:
                            neighbors.append(((ny, nx), 1))
                graph[(y, x)] = neighbors

    return a_star(graph, start, goal, heuristic)
```

## Related Concepts

- [[Dijkstra Algorithm]] - A* without heuristic (pure exploration)
- [[Breadth First Search]] - A* with h(n) = 0 and uniform edge costs
- [[Depth First Search]] - Different exploration strategy (not optimal)
- [[Bellman Ford]] - Handles negative weights
- [[Binary Search]] - Different search paradigm for sorted data

## Further Reading

- "Heuristics: Intelligent Search Strategies for Computer Problem Solving" by Pearl
- "Game Programming Patterns" by Bob Nystrom - Chapter on pathfinding
- A* visualization at Red Blob Games (redblobgames.com)

## Personal Notes

A* was the algorithm that made pathfinding click for me. The insight that you can guide search with domain knowledge while maintaining optimality is powerful. The key lesson: your heuristic must never overestimate (be admissible) or you might miss the optimal path. For game development,IDA* is often preferred over A* due to lower memory usage for large maps.
