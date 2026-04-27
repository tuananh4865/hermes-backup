---
title: Binary Search Tree
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [binary-search-tree, data-structures, algorithms, trees, computer-science]
---

# Binary Search Tree

## Overview

A Binary Search Tree (BST) is a hierarchical data structure in which each node has at most two children—referred to as the left child and right child. The defining property of a BST is the **binary search tree invariant**: for any node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater than the node's value. This ordering enables efficient search, insertion, and deletion operations with average-case time complexity of O(log n) for balanced trees.

BSTs are one of the fundamental data structures in computer science and serve as the basis for more advanced structures like AVL trees, Red-Black trees, and B-trees. They naturally model ordered data and are used in database indexes, sets, maps, and anywhere sorted data needs to be maintained with frequent insertions and deletions.

The efficiency of BST operations depends critically on tree balance. In the worst case (when the tree becomes a linked list), operations degrade to O(n). Self-balancing variants like AVL trees and Red-Black trees maintain worst-case O(log n) guarantees by rebalancing during insertions and deletions.

## Key Concepts

**Node Structure**: Each node contains a key (or value), a left pointer, a right pointer, and often a parent pointer for easier traversal.

```python
class TreeNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
```

**Binary Search Tree Invariant**: For any node with key `k`:
- All keys in the left subtree: `key < k`
- All keys in the right subtree: `key > k`

This must hold recursively for all nodes. The invariant enables binary search-like lookup: at each node, we either found the target, or we know which subtree to continue searching in.

**Traversal Orders**: Three primary depth-first traversals:
- **Inorder**: Left → Root → Right (produces sorted sequence)
- **Preorder**: Root → Left → Right (useful for copying trees)
- **Postorder**: Left → Right → Root (useful for deleting trees)

**Search Operation**: Start at root, compare target to current node, go left if smaller or right if larger. O(h) where h is tree height.

**Insertion**: Search for the key (same as search), create a new leaf node when search reaches None. O(h)

**Deletion**: Three cases:
1. Node has no children — simply remove
2. Node has one child — replace node with its child
3. Node has two children — find inorder successor (minimum of right subtree), replace node's key/value with successor's, delete successor

## How It Works

When implementing a BST, several design decisions arise:

**Recursive vs Iterative**: Recursive implementations are elegant but use O(h) stack space. Iterative implementations use constant extra space but require more careful code for traversals.

**Handling Duplicates**: Standard BST definition excludes duplicates. Options: store counts, store duplicates in left subtree (≤), or store duplicates in right subtree (≥).

**Self-Balancing Variants**:
- **AVL Trees**: Balance factor (height difference between children) maintained at {-1, 0, 1}. More strict balancing = faster lookups but more rotations during insertions.
- **Red-Black Trees**: Color-based invariants ensure roughly balanced tree. Used in most language standard library implementations (C++ std::map, Java TreeMap).

```python
def search(root, key):
    """Iterative BST search - O(h) time, O(1) space"""
    current = root
    while current is not None:
        if key == current.key:
            return current
        elif key < current.key:
            current = current.left
        else:
            current = current.right
    return None

def insert(root, key, value=None):
    """Insert new key, return root of (sub)tree"""
    if root is None:
        return TreeNode(key, value)
    
    if key < root.key:
        root.left = insert(root.left, key, value)
        root.left.parent = root
    elif key > root.key:
        root.right = insert(root.right, key, value)
        root.right.parent = root
    else:
        root.value = value  # Update if key exists
    
    return root

def inorder_traverse(root):
    """Inorder traversal yields sorted sequence - O(n)"""
    result = []
    if root:
        result.extend(inorder_traverse(root.left))
        result.append(root.key)
        result.extend(inorder_traverse(root.right))
    return result
```

## Practical Applications

**Database Indexes**: B-trees (generalization of BSTs) are the primary index structure in relational databases. The ordering property enables efficient range queries like `SELECT * FROM users WHERE age BETWEEN 25 AND 35`.

**Sets and Maps**: Many language implementations use BSTs (or balanced variants) for ordered collections: C++ `std::set`, `std::map`; Java `TreeSet`, `TreeMap`; Go's `sync.Map` uses a concurrent variant.

**Auto-Complete/Trie Alternatives**: For small dictionaries, BSTs can implement auto-complete. For larger word lists, tries are preferred, but BSTs offer simpler implementation.

**Priority Queues**: Binary heaps are technically complete BSTs, used for scheduling, event simulation, and graph algorithms (Dijkstra's shortest path).

## Examples

**Building a BST from sorted array** (efficient O(n) construction):
```python
def sorted_array_to_bst(arr):
    """Build balanced BST from sorted array in O(n)"""
    def build(low, high):
        if low > high:
            return None
        mid = (low + high) // 2
        node = TreeNode(arr[mid])
        node.left = build(low, mid - 1)
        node.right = build(mid + 1, high)
        if node.left:
            node.left.parent = node
        if node.right:
            node.right.parent = node
        return node
    return build(0, len(arr) - 1)
```

**Finding k-th smallest element**:
```python
def kth_smallest(root, k):
    """Use inorder traversal to find k-th smallest - O(h + k)"""
    stack = []
    current = root
    count = 0
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        count += 1
        if count == k:
            return current.key
        
        current = current.right
```

## Related Concepts

- [[Trees]] — General tree data structures
- [[Algorithm Complexity]] — Time and space analysis
- [[AVL Trees]] — Self-balancing BST variant
- [[Red-Black Trees]] — Another self-balancing variant
- [[B-Trees]] — Generalization used in databases
- [[Sorting Algorithms]] — BST inorder traversal produces sorted output

## Further Reading

- CLRS (Cormen, Leiserson, Rivest, Stein) — "Introduction to Algorithms", Chapter 12: Binary Search Trees
- "Algorithms" by Robert Sedgewick — Excellent coverage of BST implementations and variants

## Personal Notes

The BST is deceptively simple—you can implement the basics in an hour. But truly understanding the nuance requires wrestling with deletion cases, appreciating why balance matters, and implementing a self-balancing variant. The moment you implement Red-Black tree insertion with all its rotation cases, you gain deep respect for what standard library authors give you for free.
