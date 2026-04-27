---
title: "Red-Black Tree"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, algorithms, trees, balanced-search-trees, maps, sets]
---

## Overview

A Red-Black Tree is a self-balancing binary search tree (BST) that guarantees O(log n) worst-case time complexity for insertion, deletion, and search operations. It was invented in 1972 by Rudolf Bayer, who was working at Boeing Scientific Research Labs, building on earlier work on symmetric binary B-trees. Red-black trees achieve their balancing through a set of color-coded constraints—each node is assigned either a red or black color—rather than height-based invariants like [[AVL Tree]]s. This looser constraint makes red-black trees slightly less optimally balanced than AVL trees (height can reach 2*log₂(n+1) versus AVL's ~1.44*log₂(n+1)), but it dramatically reduces the number of rotations needed during insertions and deletions, making them faster in practice for workloads with frequent modifications.

Red-black trees are one of the most widely used balanced search tree implementations in computer science. They serve as the underlying structure for many standard library implementations: C++'s `std::map` and `std::set` (typically), Java's `TreeMap` and `TreeSet`, Go's `sync.Map` (formerly), and many others. Their combination of guaranteed worst-case performance, relatively low overhead, and cache-friendly structure makes them the default choice for in-memory ordered associative containers.

## Key Concepts

**Red-Black Properties**: A binary search tree is a red-black tree if it satisfies these five properties:

1. Every node is either red or black.
2. The root is black.
3. All leaves (NIL/null children) are black.
4. Red nodes cannot have red children (no two consecutive red nodes on any path).
5. For every node, all simple paths from that node to its descendant NIL leaves contain the same number of black nodes (the **black-height** property).

Together, properties 4 and 5 enforce balance. Property 4 prevents a chain of red-red violations, and property 5 ensures that paths from root to leaves have approximately the same length, since they must have the same black-height.

**Black-Height**: The black-height of a node is the number of black nodes on any path from that node (excluding the node itself) to a leaf, counting all NIL children as black leaves. Property 5 guarantees that this number is well-defined and consistent across all leaves under a given node.

**Rotations**: Like AVL trees, red-black trees use rotation operations to maintain balance. However, red-black trees typically require at most 2 rotations during insertion and at most 3 during deletion. The coloring scheme absorbs much of the rebalancing work that AVL trees do through rotations.

**Cases for Insertion**: Insertion in a red-black tree starts with standard BST insertion, coloring the new node red. This may violate property 2 (root could be red) or property 4 (red parent with red child). The algorithm proceeds through a series of cases, recoloring nodes and occasionally rotating, until the tree satisfies all red-black properties.

```python
# Pseudocode for Red-Black Tree insertion
class RBNode:
    def __init__(self, key, color='RED'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

# Insert as usual, then fix violations
def insert_fixup(tree, node):
    while node.parent and node.parent.color == 'RED':
        if node.parent == node.parent.parent.left:
            uncle = node.parent.parent.right
            # Case 1: Uncle is red → recolor
            if uncle and uncle.color == 'RED':
                node.parent.color = 'BLACK'
                uncle.color = 'BLACK'
                node.parent.parent.color = 'RED'
                node = node.parent.parent
            else:
                # Case 2: Uncle is black, node is right child → left rotate
                if node == node.parent.right:
                    node = node.parent
                    left_rotate(tree, node)
                # Case 3: Uncle is black, node is left child → right rotate
                node.parent.color = 'BLACK'
                node.parent.parent.color = 'RED'
                right_rotate(tree, node.parent.parent)
        else:
            # Symmetric cases for right side
            uncle = node.parent.parent.left
            if uncle and uncle.color == 'RED':
                node.parent.color = 'BLACK'
                uncle.color = 'BLACK'
                node.parent.parent.color = 'RED'
                node = node.parent.parent
            else:
                if node == node.parent.left:
                    node = node.parent
                    right_rotate(tree, node)
                node.parent.color = 'BLACK'
                node.parent.parent.color = 'RED'
                left_rotate(tree, node.parent.parent)
    tree.root.color = 'BLACK'  # Ensure root is black

def left_rotate(tree, x):
    y = x.right
    x.right = y.left
    if y.left:
        y.left.parent = x
    y.parent = x.parent
    if not x.parent:
        tree.root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
```

## How It Works

The red-black tree's balancing mechanism exploits the interplay between the red-color constraint and the black-height constraint. When inserting a red node under a black parent, no black-height violation can occur—but a red-red violation may. The fixup algorithm handles red-red violations by pushing the problem upward toward the root, potentially recoloring and rotating along the way. Because the algorithm moves at most two levels up per iteration and the tree height is O(log n), the fixup loop runs in O(log n) time.

A key insight is that red-black trees can always be repaired with at most 2 rotations for insertion (and 3 for deletion), regardless of the specific shape of the tree. This is in contrast to AVL trees, which may require more rotations and more complex case analysis. The simplicity and predictability of the rotation count makes red-black trees easier to implement correctly and faster in practice on modification-heavy workloads.

## Practical Applications

Red-black trees are the workhorse of in-memory ordered collections:

- **Standard library containers**: `std::map`/`std::set` in C++ (GCC's libstdc++), `TreeMap`/`TreeSet` in Java, `std::set` in Rust's standard library (though increasingly replaced by B-Tree maps), many language runtimes' internal data structures.
- **Scheduler implementations**: Linux's Completely Fair Scheduler (CFS) uses red-black trees to track process runtimes.
- **Memory allocators**: Some malloc implementations use red-black trees to manage free memory blocks.
- **Networking**: Network routing tables and timer wheels sometimes use red-black trees for ordered management of timeouts and routes.
- **File descriptors**: Linux's file descriptor table uses red-black trees to map fd numbers to file description structures.

## Examples

Inserting [10, 20, 30, 15, 25, 5, 1] into an empty red-black tree:
- Insert 10 as root → color BLACK (always applied to root after fixup)
- Insert 20 → red child of 10, no violation → done
- Insert 30 → red under red (20) → recolor 20 BLACK, 10 RED, rotate 20 to root → root becomes BLACK 20 with children 10(RED) and 30(RED) → all properties satisfied
- Continue inserting 15, 25, 5, 1 with fixup operations as needed

The tree maintains black-height balance: every path from root to any NIL leaf has the same count of black nodes (2 in this case), ensuring O(log n) worst-case operations.

## Related Concepts

- [[AVL Tree]] - Height-balanced BST with stricter balancing but more rotations on modification
- [[B-Tree]] - Wide, branching balanced tree optimized for disk storage
- [[Skip List]] - An alternative O(log n) ordered structure with probabilistic balancing
- [[Splay Tree]] - Amortized O(log n) tree that moves accessed nodes to the root
- [[Binary Search Tree]] - The unbalanced structure red-black trees build upon
- [[TreeMap]] - The language-specific ordered map interface typically implemented with red-black trees

## Further Reading

- "Introduction to Algorithms" (CLRS), Chapter 14: Red-Black Trees
- "Algorithms" by Robert Sedgewick (Red-Black tree section with full Java implementations)
- Linux kernel source: `lib/rbtree.c` — production-quality red-black tree implementation

## Personal Notes

The moment that made red-black trees click for me was realizing the relationship between the red-color and the black-height: red nodes are "sacrificial" in that they absorb imbalance without affecting the black-height count, allowing the tree to delay or avoid expensive multi-level rotations. AVL trees treat all imbalance equally and rotate immediately; red-black trees let red nodes "hold" the temporary imbalance and fix it more lazily. This design choice—trading optimal depth for fewer structural modifications—is a recurring pattern in data structure design, and red-black trees are one of its cleanest expressions.
