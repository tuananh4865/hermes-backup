---
title: "Travelling Salesman Problem"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [algorithms, optimization, np-hard, combinatorial-optimization, graph-theory]
---

# Travelling Salesman Problem

> This page was auto-created by [[self-healing-wiki]] to fill a broken link.
> Please expand with real content.

## Overview

The Travelling Salesman Problem (TSP) is one of the most famous and extensively studied problems in computer science and operations research. Given a list of cities and the distances between each pair of cities, the TSP asks: what is the shortest possible route that visits every city exactly once and returns to the starting city? Despite its seemingly simple formulation, the TSP is NP-hard, meaning there is no known polynomial-time algorithm to solve it exactly for large instances.

The TSP appears in a surprising variety of real-world contexts beyond its obvious application to logistics and route optimization. It models problems in circuit board drilling, telescope scheduling, DNA sequencing, and the placement of wind turbines. Its theoretical importance stems from the fact that many other combinatorial optimization problems can be reformulated as TSP instances.

## Key Concepts

**NP-Hardness** is what makes the TSP computationally challenging. The number of possible routes grows factorially with the number of cities—for just 20 cities, there are approximately 2.4 × 10^18 possible tours. This exponential growth makes exhaustive search impossible for practical problem sizes.

**Metric TSP** is a special case where distances satisfy the triangle inequality (going directly from A to C is never longer than going A→B→C). This metric property enables approximation algorithms that guarantee solutions within a constant factor of optimal.

**Held-Karp Algorithm** is a dynamic programming approach that solves the TSP in O(n^2 · 2^n) time—better than factorial brute force but still exponential. It computes the shortest tour by building up solutions to subproblems.

**Approximation Algorithms** like the Christofides algorithm (for metric TSP) can guarantee solutions within 1.5× of optimal in polynomial time. This is valuable for practical applications where "close enough" is acceptable.

## How It Works

Exact TSP solvers use several sophisticated techniques:

**Branch and Bound** systematically explores the search space while discarding large portions that cannot yield better solutions than already-found ones. It's the basis for many state-of-the-art exact TSP solvers like Concorde.

**Integer Linear Programming (ILP)** formulations model TSP as a set of linear constraints with binary variables. Modern ILP solvers with clever cuts and preprocessing can solve instances with thousands of cities exactly.

**Cutting Plane Methods** iteratively add constraints to tighten the LP relaxation, eventually converging to an integer solution. This is the approach used by Concorde TSP Solver.

For approximate solutions, **heuristics** are essential:

**Nearest Neighbor** is a simple greedy algorithm that always visits the closest unvisited city next. It's fast (O(n²)) but can produce tours up to 25% longer than optimal.

**2-Opt** and **Lin-Kernighan** are local search improvement heuristics that repeatedly replace edges to shorten the tour until no improvement is possible.

## Practical Applications

**Logistics and Delivery Routes** are the most intuitive applications. Companies like UPS and FedEx use TSP-based algorithms for daily package delivery optimization, saving millions in fuel and labor costs annually.

**Drill Movement Optimization** for printed circuit boards (PCBs) uses TSP to minimize the total distance the drill travels between holes, reducing manufacturing time significantly.

**Telescope Scheduling** in astronomy requires scheduling observations of different sky regions in an order that minimizes total slew time—a direct TSP formulation.

**DNA Sequencing** involves ordering DNA fragments to reconstruct the original sequence. The problem can be mapped to TSP where fragments are cities and overlap similarity is distance.

## Examples

A simple Python implementation using a brute-force approach for small TSP instances:

```python
from itertools import permutations
import math

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def tsp_brute_force(cities):
    n = len(cities)
    min_tour = None
    min_cost = float('inf')
    
    for tour in permutations(range(1, n)):
        tour = (0,) + tour + (0,)  # Return to start
        cost = sum(distance(cities[tour[i]], cities[tour[i+1]]) for i in range(n))
        if cost < min_cost:
            min_cost = cost
            min_tour = tour
    
    return min_tour, min_cost

# Example: 5 cities
cities = [(0, 0), (1, 3), (4, 2), (3, 5), (6, 1)]
tour, cost = tsp_brute_force(cities)
print(f"Optimal tour: {tour}, Cost: {cost:.2f}")
```

For larger instances, use Google OR-Tools:

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_tsp_or_tools(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]
    
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.Christofides
    return routing.Solve()
```

## Related Concepts

- [[self-healing-wiki]]
- [[NP-Hard Problems]] - The complexity class that TSP belongs to
- [[Dynamic Programming]] - Used in the Held-Karp algorithm
- [[Approximation Algorithms]] - Methods for finding near-optimal solutions efficiently
- [[Graph Theory]] - The mathematical foundation of TSP
- [[Vehicle Routing Problem]] - A generalization of TSP with multiple vehicles

## Further Reading

- "In Pursuit of the Traveling Salesman" by William J. Cook — An excellent accessible introduction
- Concorde TSP Solver (concordecoder.com) — State-of-the-art exact solver
- TSPLIB — Library of standard TSP benchmark instances

## Personal Notes

I first encountered TSP in an algorithms course and underestimated it—seemed simple enough to solve with greedy. The reality of NP-hardness hit when I tried small instances and watched brute force take forever. The gap between "obvious" greedy solutions and true optimality is surprisingly large; nearest neighbor can be 25-40% worse than optimal on random instances.
