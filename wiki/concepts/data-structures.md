---
title: "Data Structures"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [computer-science, algorithms, data-structures, programming, complexity]
---

# Data Structures

## Overview

Data structures are organized formats for storing, managing, and retrieving data efficiently. They define how data is arranged in memory and the operations that can be performed on that data. The choice of data structure significantly impacts the performance and capabilities of software systems—selecting the wrong structure can make operations O(n²) that should be O(1), while the right choice can turn an intractable problem into a trivial one.

Data structures form the foundation of computer science and software engineering. Every non-trivial program uses them—whether implicitly (as the runtime organizes your objects) or explicitly (when you choose a list over a map). Understanding data structures develops the algorithmic thinking necessary to reason about program efficiency and scalability.

The field distinguishes between abstract data types (ADTs)—mathematical specifications of data organization and operations—and concrete implementations. A List ADT specifies insert, delete, and access operations; whether those operations are O(1) or O(n) depends on the implementation (array vs. linked list).

## Key Concepts

**Arrays**: Contiguous memory storage with O(1) random access by index. Elements are stored side-by-side, enabling efficient sequential access and cache-friendly iteration. However, insertion and deletion in the middle require shifting elements, making these O(n) operations. Dynamic arrays (ArrayList, Python list) automatically resize, amortizing resize costs.

**Linked Lists**: Nodes containing data and pointers to next (singly) or previous (doubly) nodes. Insertion and deletion at known positions are O(1), but random access requires traversal from the head, making it O(n). Linked lists excel when insertions/deletions are frequent and access is sequential.

**Hash Tables**: Key-value stores using a hash function to compute array indices from keys. With good hash functions and sufficient capacity, lookups, insertions, and deletions are O(1) average case. Collisions (when two keys hash to the same index) are handled via chaining (linked lists) or open addressing (probing). Worst case degrades to O(n).

**Trees**: Hierarchical structures with parent-child relationships. Binary search trees (BST) maintain sorted order, enabling O(log n) search, insertion, and deletion when balanced. Self-balancing trees (AVL, Red-Black) maintain balance through rotations. B-trees optimize for disk storage and are used in databases.

**Graphs**: Structures with vertices (nodes) and edges (connections). Can be directed/undirected, weighted/unweighted, cyclic/acyclic. Adjacency lists (storing neighbor lists per vertex) are space-efficient for sparse graphs; adjacency matrices are O(1) for edge existence checks but O(n²) space.

**Stacks and Queues**: LIFO (Last-In-First-Out) and FIFO (First-In-First-Out) abstractions. Stacks enable backtracking algorithms (function call stack, expression evaluation). Queues enable scheduling and breadth-first traversal.

## How It Works

Each data structure optimizes for specific operations while trade-offs affect others. Understanding these trade-offs guides selection:

```
Operation Complexity Comparison:
                    Array    Linked List    Hash Table    BST (balanced)
Access by index     O(1)        O(n)          O(1)           O(log n)
Search              O(n)        O(n)          O(1)*          O(log n)
Insertion at head   O(n)        O(1)          O(1)           O(log n)
Deletion at head   O(n)        O(1)          O(1)           O(log n)
Insertion at tail   O(1)**     O(1)***       O(1)           O(log n)

* Average case with good hash function
** Amortized for dynamic arrays
*** With tail pointer
```

Modern programming languages provide standard collections that hide implementation details. Python's `list` is a dynamic array, `dict` is a hash table, `set` uses a hash table. Java's `ArrayList` is an array, `LinkedList` is a true linked list, `HashMap` is a hash table, `TreeMap` is a Red-Black tree. Choosing between them requires understanding what's under the hood.

## Practical Applications

**Caching**:LRU (Least Recently Used) caches combine hash tables for O(1) lookups with doubly-linked lists for O(1) ordering updates. Libraries like Python's `functools.lru_cache` implement this pattern.

**Database Indexes**: B-trees maintain sorted data with efficient range queries. LSM (Log-Structured Merge) trees combine write-ahead logging with periodic compaction for write-optimized storage.

**Graph Algorithms**: Social networks use adjacency lists to efficiently traverse friend relationships. Pathfinding uses priority queues (heaps) for Dijkstra's algorithm.

**Task Scheduling**: Operating system task queues use priority queues to manage process scheduling. Message queues (Kafka, RabbitMQ) use append-only logs.

## Examples

Implementing a stack with array and understanding when to use linked list:

```python
class Stack:
    """Array-based stack - O(1) push/pop, O(1) peek"""
    def __init__(self):
        self._data = []
    
    def push(self, item):
        self._data.append(item)  # Amortized O(1)
    
    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()  # O(1)
    
    def peek(self):
        return self._data[-1]
    
    def is_empty(self):
        return len(self._data) == 0


class LinkedListStack:
    """Linked list-based stack - always O(1) for all operations"""
    class _Node:
        def __init__(self, item):
            self.item = item
            self.next = None
    
    def __init__(self):
        self._head = None
    
    def push(self, item):
        node = self._Node(item)
        node.next = self._head
        self._head = node
    
    def pop(self):
        if not self._head:
            raise IndexError("pop from empty stack")
        item = self._head.item
        self._head = self._head.next
        return item
```

## Related Concepts

- [[Algorithms]] - Procedures that operate on data structures
- [[Big O Notation]] - Analyzing operation complexity
- [[Hash Tables]] - Key-value stores with O(1) average access
- [[Trees]] - Hierarchical data structures
- [[Graphs]] - Network structures with vertices and edges
- [[Stacks and Queues]] - LIFO and FIFO abstractions
- [[Heaps]] - Priority queue implementations

## Further Reading

- [CLRS Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - The definitive algorithms textbook
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/) - Complexity comparisons
- [Visualgo](https://visualgo.net/) - Interactive data structure visualization
- [Python Wiki - Time Complexity](https://wiki.python.org/moin/TimeComplexity)

## Personal Notes

I interview candidates regularly, and the most common gap I see is not understanding when to use which structure. Many candidates can describe array vs. linked list complexity, but stumble on when you'd choose one over the other. The real insight: arrays excel when you need cache locality (iterating through all elements) and most operations are at the end. Linked lists win when you're frequently inserting/deleting at known positions and access is always sequential from the current position. I always ask candidates to walk me through a scenario, not just list complexities. Understanding that `list.append()` is amortized O(1) while `list.insert(0, item)` is O(n) (because it shifts everything) is the kind of practical knowledge that affects daily coding decisions.
