---
title: "Memoization"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [optimization, performance, algorithms, caching, dynamic-programming]
---

# Memoization

## Overview

Memoization is an optimization technique that caches the results of expensive function calls and returns the cached result when the same inputs occur again. The term derives from the Latin word "memorandum" (to be remembered), reflecting its purpose: remembering computed results to avoid redundant work. In computer science, memoization transforms algorithms with overlapping subproblems—particularly recursive implementations of problems exhibiting optimal substructure—into efficient solutions by trading memory space for computation time.

The technique is fundamental to dynamic programming, where it implements the "top-down" approach to solving recurrence relations. Rather than computing all subproblems iteratively as in bottom-up DP, memoized recursion computes only the subproblems actually needed, storing results for future lookups. This can dramatically reduce time complexity, often bringing exponential algorithms down to polynomial time. The space-time tradeoff is inherent: memoization requires O(n) or O(n²) additional space depending on the number of unique input combinations.

## Key Concepts

**Referential Transparency** is a prerequisite for memoization. A function is referentially transparent if it always produces the same output for the same input and has no side effects. Pure functions that don't modify global state, mutate arguments, or perform I/O are memoizable. Functions with side effects—logging, database queries, API calls, random number generation—cannot be safely memoized without careful consideration of cache invalidation.

**Cache Keys** determine how inputs map to stored results. For single-argument functions, the argument itself often serves as the key. Multiple arguments require a composite key strategy: concatenated strings, serialized arrays, or structured objects. The choice matters for performance and correctness—particularly when distinguishing between types that might coerce to the same value (e.g., `1` and `"1"`).

**Cache Invalidation** addresses the challenge of keeping cached values current when underlying data changes. In static contexts where inputs never map to different outputs, invalidation is unnecessary. But in reactive systems where dependencies change, strategies include time-based expiration (TTL), dependency tracking, and manual invalidation APIs. Some memoization implementations provide selective invalidation by key.

**Space Complexity** grows with the number of unique inputs cached. Unbounded memoization in long-running processes can cause memory leaks if the cache never purges old entries. Implementations may use LRU (Least Recently Used) eviction, size limits, or time-based cleanup to bound memory usage. Choosing an appropriate cache size involves profiling typical input distributions.

## How It Works

The implementation pattern wraps a function to interpose cache logic between the caller and the original function. On each call, the wrapper checks whether the result exists in the cache using the computed key. If found (a cache hit), it returns the cached value immediately without executing the original function. On a cache miss, it calls the original function, stores the result indexed by the input key, and returns the result to the caller.

```python
def memoize(func):
    cache = {}
    
    def memoized(*args):
        key = str(args)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    
    memoized.cache = cache
    memoized.clear = lambda: cache.clear()
    return memoized

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

This classic Fibonacci example demonstrates the transformation: the naive recursive implementation runs in O(2^n) time due to repeated computation of the same subproblems, while the memoized version completes in O(n) time by computing each value exactly once.

## Practical Applications

**Recursive Algorithms** benefit most obviously from memoization. Fibonacci, factorial, and binomial coefficient calculations become trivial. More sophisticated applications include recursive string editing distance (Levenshtein), matrix chain multiplication, and parsing with context-free grammars. Any recursive algorithm where subproblems overlap is a candidate.

**React Components** use memoization to prevent unnecessary re-renders. `React.memo` wraps components to bail out of re-rendering when props haven't changed, while `useMemo` and `useCallback` hooks memoize computed values and function references within hooks. These optimizations matter in large component trees where rendering is expensive.

**API Response Caching** caches remote data locally to reduce network calls and improve perceived performance. HTTP caching headers (ETag, Last-Modified) provide server-side invalidation, while client-side caches in service workers or state management libraries can provide offline-first experiences. Memoization here intersects with broader caching strategies.

**Database Query Optimization** uses memoization within ORM layers and query builders. Repeated queries with identical parameters return cached results rather than hitting the database. This is particularly valuable in request handlers that might call the same lookup logic multiple times within a single request context.

## Examples

Memoization in JavaScript using a Map-based approach:

```javascript
const memoize = (fn) => {
  const cache = new Map();
  
  return (arg) => {
    if (cache.has(arg)) {
      return cache.get(arg);
    }
    const result = fn(arg);
    cache.set(arg, result);
    return result;
  };
};

const expensiveCalculation = (n) => {
  // Simulate expensive computation
  return Array(n)
    .fill(null)
    .reduce((acc, _, i) => acc + Math.sqrt(i), 0);
};

const memoizedCalc = memoize(expensiveCalculation);

console.log(memoizedCalc(1000000)); // First call: slow
console.log(memoizedCalc(1000000)); // Second call: instant (cached)
```

This pattern extends to multiple arguments by using JSON serialization or WeakMap for object keys.

## Related Concepts

- [[Dynamic Programming]] - The algorithmic paradigm that employs memoization
- [[Caching]] - Broader concept of storing data for reuse
- [[Pure Function]] - Functions compatible with memoization
- [[Lazy Evaluation]] - Deferred computation strategy
- [[Recursion]] - The execution pattern memoization most often optimizes

## Further Reading

- [Introduction to Dynamic Programming (GeeksforGeeks)](https://www.geeksforgeeks.org/dynamic-programming/)
- [Wikipedia: Memoization](https://en.wikipedia.org/wiki/Memoization)
- [You Might Not Need Memoization (Kent C. Dodds)](https://kentcdodds.com/blog/you-might-not-need-memoization)

## Personal Notes

Memoization is often the first optimization I consider when profiling reveals repeated computation. Before memoizing, ensure the function is pure—I've seen subtle bugs emerge when memoized functions inadvertently relied on mutable global state. For production React code, use the built-in hooks rather than hand-rolled memoization; they integrate properly with React's concurrent features. Consider whether an LRU cache is more appropriate than unbounded memoization for functions with many possible inputs.
