---
title: "B Tree"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, algorithms, trees, databases, indexing]
---

## Overview

A B-Tree (Balanced Tree) is a self-balancing ordered search data structure that maintains sorted data in a way that enables efficient insertion, deletion, and search operations. Unlike binary search trees where each node has at most two children, a B-Tree node can hold multiple keys and multiple children, making it optimal for disk-based storage systems where reading a block of data is expensive relative to comparing keys in memory. B-Trees are the foundational data structure behind most modern relational databases (MySQL InnoDB, PostgreSQL) and file systems (NTFS, ext4, HFS+).

B-Trees were invented by Rudolf Bayer and Edward McCreight at Boeing in 1971, though the precise origin is sometimes attributed to a 1972 publication. The "B" stands for "balanced" (though Bayer himself has joked it could stand for "Boeing" or "broad"). The key property of B-Trees is that they remain height-balanced: all leaf nodes are at the same depth, which bounds the worst-case search complexity to O(log n) and ensures predictable performance regardless of tree size.

## Key Concepts

**Node Structure**: A B-Tree node contains an ordered list of keys (also called search keys or data entries) and a list of child pointers. If a node has `k` keys, it has `k+1` children. The keys partition the key space—the first child contains keys less than the first key, the second child contains keys between the first and second key, and so on.

**Order (B-Tree of order m)**: A B-Tree of order `m` satisfies these constraints:
- Each node has at most `m` children and at least `⌈m/2⌉` children (except the root)
- The root has at least 2 children (unless it is a leaf)
- A non-leaf node with `k` children contains `k-1` keys
- All leaves appear at the same depth

**Minimum Degree (t)**: Many textbooks define B-Trees using a minimum degree `t`, where:
- Each node (except root) has at least `t-1` keys and at most `2t-1` keys
- The root has at least 1 key
- A node with `k` keys has `k+1` children

**Leaf Nodes**: In a B-Tree, all actual data values reside in leaf nodes. Internal nodes store only keys and child pointers—they do not hold data. This separation allows internal nodes to be more compact and cache-friendly.

## How It Works

B-Trees maintain balance through two primary operations that occur during insertion:

**Insertion**: When inserting a key into a B-Tree:
1. Start at the root and traverse down the tree, comparing the key with keys in each node to determine the correct child.
2. When reaching a leaf node, insert the key in sorted order.
3. If the leaf overflows (exceeds maximum capacity), **split** the leaf: take the middle key, push it up to the parent, and create two new sibling leaves.
4. If the parent also overflows, propagate the split upward—potentially all the way to the root.
5. If the root splits, a new root is created with the middle key, increasing the tree's height by one.

**Deletion** is more complex and involves either borrowing keys from siblings (when a node underflows) or merging two siblings and pulling down a key from the parent.

```python
# Pseudocode for B-Tree split-child operation
def split_child(parent, index, child):
    """
    Split a full child node at parent[index].
    child has 2t-1 keys; split into two nodes with t-1 keys each.
    The middle key moves up to parent.
    """
    t = child.t  # minimum degree
    median_key = child.keys[t - 1]  # middle key

    # Create new right sibling
    new_node = BTreeNode(t)
    new_node.keys = child.keys[t:]      # right half
    new_node.children = child.children[t:]  # right children
    child.keys = child.keys[:t - 1]     # left half
    child.children = child.children[:t]  # left children

    # Insert median key into parent
    parent.keys.insert(index, median_key)
    parent.children.insert(index + 1, new_node)
```

## Practical Applications

B-Trees are ubiquitous in systems where data persistence and efficient range queries matter:

- **Relational Databases**: PostgreSQL, MySQL (InnoDB), Oracle, and SQLite all use B-Trees (or B+Tree variants) as their primary index structure. Database tables are often clustered around these indexes.
- **File Systems**: Most modern file systems use B-Trees or derivatives to organize directory structures and file metadata. ext4 uses HTrees (a hashed variant of B-Trees); Btrfs uses B-Trees extensively.
- **Key-Value Stores**: RocksDB, LevelDB, and many embedded databases use B-Tree-like structures for range scans and point lookups.
- **ISO File Systems and Optical Media**: The UDF filesystem uses B-Trees for file allocation tables.

## Examples

Consider a B-Tree of order 5 (minimum degree t=3, so nodes hold 2-5 keys). Inserting keys [10, 20, 5, 15, 30, 25] would progressively build the tree. When inserting 25, the leaf containing [20, 30] overflows to 3 keys, triggering a split: 25 becomes the middle key pushed up to the parent. The tree grows upward only when the root itself overflows, keeping the tree short and balanced even with many insertions.

## Related Concepts

- [[B+ Tree]] - A variant of B-Tree where all data is stored only in leaf nodes, with internal nodes serving purely as indexes
- [[AVL Tree]] - A height-balanced binary search tree, another self-balancing tree variant
- [[Red-Black Tree]] - A binary tree with color-based balancing, used in in-memory balanced search trees
- [[Database Indexes]] - The broader application domain where B-Trees are most commonly seen
- [[LSM Tree]] - A competing structure for write-intensive workloads (used in Cassandra, LevelDB)

## Further Reading

- "Introduction to Algorithms" (CLRS), Chapter 18: B-Trees
- "The Ubiquitous B-Tree" by Douglas Comer (1979) — a classic survey paper
- PostgreSQL documentation on B-Tree index implementation

## Personal Notes

The most intuitive way I've found to think about B-Trees is in terms of the underlying hardware: disk blocks are slow to fetch but can hold many keys. B-Trees are designed to minimize disk reads by keeping branching high (so tree height stays low) and packing keys tightly into blocks. When I first understood this, the mystery of why databases use B-Trees for indexing vanished—it was a direct consequence of hardware realities, not arbitrary convention.
