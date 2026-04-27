---
title: Binary Search Trees
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, algorithms, trees, computer-science, treesearch]
---

## Overview

A Binary Search Tree (BST) is a hierarchical data structure in which each node has at most two children—referred to as the left child and right child. The BST property enforces that for any node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater. This invariant enables efficient searching, insertion, and deletion operations with an average-case time complexity of O(log n) for balanced trees.

## Key Concepts

**BST Invariant**: The defining property that maintains order within the tree. If `node.left` exists, `node.left.value < node.value`. If `node.right` exists, `node.right.value > node.value`. This property recursively applies to all subtrees. Violating this property breaks the tree's search guarantees.

**Tree Traversal**: Three primary depth-first traversal orders exist—in-order (left, node, right), pre-order (node, left, right), and post-order (left, right, node). In-order traversal of a BST yields values in sorted order, making it useful for producing sorted sequences.

**Balancing**: Unbalanced BSTs degrade to O(n) search time, losing the efficiency advantage. Self-balancing variants like AVL trees and Red-Black trees maintain height balance through rotations or color constraints, guaranteeing O(log n) worst-case operations.

**Successor and Predecessor**: In-order successor of a node is the minimum value in its right subtree (or the first ancestor where the node is in its left subtree). Predecessor is symmetric. These are essential for delete operations when removing nodes with two children.

## How It Works

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)
    
    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
```

**Search Operation**: Starting at root, compare target with current node. If equal, found. If smaller, move left. If larger, move right. Repeat until found or node is null.

**Insertion**: Perform search for the value. When reaching a null child, insert new node there. Insertion point is deterministic based on value.

**Deletion**: Three cases—leaf node (remove directly), one child (replace with child), two children (find in-order successor, replace value, delete successor).

## Practical Applications

BSTs and their variants underpin many real-world systems. Database indexes often use B-trees (generalized BSTs) for efficient range queries and lookups. Filesystems use tree structures for directory organization. Priority queues and heaps can be implemented with BST variants. Event-driven simulations use BSTs for scheduling. Autocomplete and spell-check systems sometimes use tries, which are tree structures optimized for string keys.

## Examples

- **AVL Trees**: Height-balanced BST where left and right subtree heights differ by at most 1. Guarantees O(log n) but with stricter balancing than Red-Black trees.
- **Red-Black Trees**: Color-coded BST with relaxation balancing rules. Java's TreeMap and TreeSet use this structure.
- **Treaps**: Randomized BST combining heap and BST properties, providing probabilistic balance with simpler implementation.
- **B-Trees**: Multi-way search trees used in databases and filesystems, optimizing for block storage access.

## Related Concepts

- [[Data Structures]] - The broader category containing trees
- [[Algorithms]] - BST operations as algorithmic procedures
- [[Tree Traversal]] - Depth-first and breadth-first tree exploration
- [[Heaps]] - Priority queue implementation using tree structure
- [[Hash Tables]] - Alternative key-value store with O(1) average lookup

## Further Reading

- [CLRS: Binary Search Trees](https://mitpress.mit.edu/books/introduction-algorithms-third-edition) - Comprehensive treatment in "Introduction to Algorithms"
- [Visualgo: BST](https://visualgo.net/en/bst) - Interactive visualization of BST operations
- [Khan Academy: Trees](https://www.khanacademy.org/computing/computer-science/algorithms/recursive-algorithms/a/introduction-to-trees)

## Personal Notes

BSTs taught me that invariants matter—when you establish a property (left < root < right), maintaining it prevents subtle bugs. Writing recursive traversal functions强化了对树结构的直觉. In practice, I'd reach for built-in tree structures (Java's TreeMap, Python's bisect module) rather than rolling my own. For persistent data, immutable BST variants are elegant but rarely necessary unless building functional codebases.
