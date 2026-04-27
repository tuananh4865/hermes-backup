---
title: "Optimization"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mathematics, computer-science, algorithms, machine-learning]
---

# Optimization

## Overview

Optimization is the mathematical discipline of finding the best available solution to a problem within defined constraints. It forms a cornerstone of computer science, operations research, economics, engineering, and machine learning. An optimization problem typically involves an objective function to minimize or maximize, along with constraints that define the feasible solution space.

The field ranges from simple problems like finding the minimum of a quadratic function to complex scenarios involving millions of variables, non-convex landscapes, and noisy gradient information. Understanding optimization is essential for training machine learning models, scheduling resources, routing logistics, designing engineering systems, and countless other practical applications.

## Key Concepts

**Objective Function**: The function being optimized, representing the quality metric to minimize (cost, loss) or maximize (profit, accuracy). The choice of objective function fundamentally shapes the solution.

**Constraints**: Restrictions on the solution space that any feasible solution must satisfy. Constraints can be equalities, inequalities, or bounds on variables.

**Local vs Global Optima**: A local optimum is best within its neighborhood, while a global optimum is the best across the entire feasible region. Non-convex problems may have many local optima.

**Convexity**: A property where the objective function and constraints form a convex set. Convex optimization problems have the desirable property that any local optimum is globally optimal.

**Gradient Information**: Derivatives that indicate the direction of steepest ascent (gradient) or descent (negative gradient). Most optimization algorithms use gradient information to guide the search.

## How It Works

Optimization algorithms traverse the solution space seeking optimal or near-optimal solutions. The approach varies significantly based on problem characteristics:

**Gradient Descent** methods iteratively move in the direction of steepest descent, commonly used in machine learning for training neural networks. Variants include stochastic gradient descent (SGD), momentum-based methods, and adaptive learning rate algorithms like Adam.

**Newton's Method** uses second-order derivative information (Hessian) for faster convergence near the optimum, though computing the Hessian is computationally expensive for high-dimensional problems.

**Evolutionary Algorithms** like genetic algorithms use population-based search inspired by natural selection, maintaining diversity and exploring non-convex landscapes effectively.

**Linear and Integer Programming** solve optimization problems with linear objectives and constraints, using algorithms like the simplex method or interior-point methods.

```python
# Simple gradient descent example in Python
def gradient_descent(gradient, start_x, learning_rate, n_iterations):
    x = start_x
    for _ in range(n_iterations):
        grad = gradient(x)
        x = x - learning_rate * grad
    return x

# Objective: minimize f(x) = x^2
# Gradient: f'(x) = 2x
result = gradient_descent(lambda x: 2 * x, start_x=10.0, learning_rate=0.1, n_iterations=50)
print(f"Minimum found at x = {result:.6f}")  # Approaches 0
```

## Practical Applications

Optimization touches virtually every domain:

- **Machine Learning**: Training models involves minimizing loss functions via backpropagation and gradient-based methods
- **Resource Scheduling**: Allocating computing resources, staff, or equipment optimally
- **Route Planning**: Finding shortest paths, traveling salesman problems, logistics optimization
- **Portfolio Management**: Selecting asset allocations that maximize returns for given risk levels
- **Engineering Design**: Optimizing structural designs, control systems, and manufacturing processes

## Examples

**Linear Programming Example**: A company manufacturing two products (A and B) with profit margins of $40 and $30 respectively. Machine time constraints and市场需求 limit production. The optimization problem:

```python
from scipy.optimize import linprog

# Maximize: 40*A + 30*B
# Subject to: 2*A + 4*B <= 100 (machine hours)
#            3*A + 2*B <= 80 (labor hours)
#            A >= 0, B >= 0

c = [-40, -30]  # scipy minimizes, so we negate
A_ub = [[2, 4], [3, 2]]
b_ub = [100, 80]
bounds = [(0, None), (0, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
print(f"Optimal: A={result.x[0]:.1f}, B={result.x[1]:.1f}, Profit=${-result.fun:.2f}")
```

## Related Concepts

- [[Machine Learning]] - Heavily relies on optimization for training models
- [[Algorithms]] - The study of computational procedures for solving problems
- [[Linear Programming]] - Optimization with linear objectives and constraints
- [[Neural Networks]] - Use gradient-based optimization for training
- [[Gradient Descent]] - Fundamental optimization algorithm in machine learning

## Further Reading

- "Convex Optimization" by Stephen Boyd and Lieven Vandenberghe
- "Numerical Optimization" by Jorge Nocedal and Stephen Wright
- [SciPy Optimization Documentation](https://docs.scipy.org/doc/scipy/reference/optimize.html)

## Personal Notes

Optimization is one of those foundational topics that appears everywhere once you start looking. The tension between global search methods (which are robust but slow) and local methods (which are fast but can get stuck) is a recurring theme. In machine learning, the non-convexity of neural network loss landscapes means we're often finding good local minima or saddle points rather than global optima—but this rarely matters in practice.
