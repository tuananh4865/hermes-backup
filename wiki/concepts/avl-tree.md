---
title: "AVL Tree"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data-structures, algorithms, trees, balanced-search-trees,avl]
---

## Overview

An AVL Tree is a self-balancing binary search tree (BST) named after its inventors, Soviet mathematicians Georgy Adelson-Velsky and Landis, who published the concept in 1962. What distinguishes an AVL tree from a ordinary binary search tree is its strict balance invariant: for every node in the tree, the heights of its left and right subtrees differ by at most one. This guarantee ensures that the tree remains height-balanced, bounding the maximum height to approximately 1.44 * log₂(n+1), which in turn ensures O(log n) time complexity for search, insertion, and deletion operations in all cases.

AVL trees were the first mathematically rigorous balancing scheme proposed for binary search trees, preceding [[Red-Black Tree]]s by nearly a decade. The balancing condition is stricter than red-black trees—AVL trees are sometimes called "shorter" and more optimally balanced—but this comes at a cost: AVL trees require more frequent rotations during insertions and deletions to maintain their balance factor constraint. As a result, red-black trees are often preferred in practice for in-memory applications, while AVL trees remain the choice when search operations dominate and modifications are infrequent.

## Key Concepts

**Balance Factor**: The balance factor of a node is defined as `height(left subtree) - height(right subtree)`. In an AVL tree, every node must have a balance factor of -1, 0, or +1. Any node with a balance factor of -2 or +2 violates the AVL invariant and must be rebalanced.

**Height**: The height of a node is the number of edges on the longest path from that node to a leaf. The height of an empty (null) subtree is defined as -1. The AVL property ensures no leaf is more than one level deeper than any other leaf in the same tree.

**Rotations**: AVL trees use two fundamental rotation operations to restore balance:

- **Single Right Rotation (Zig)**: Applied when a left-heavy subtree (balance factor +2) has its left child balanced or left-heavy. The left child becomes the new subtree root, the original node becomes the right child of the new root, and the left child's right subtree becomes the left subtree of the original node.

- **Single Left Rotation (Zag)**: The mirror of the Zig operation, applied for right-heavy subtrees.

- **Double Rotation (Zig-Zag or Zag-Zig)**: A combination of two single rotations applied when a child subtree is heavier in the opposite direction. The most common case is left-right imbalance (a left-heavy node whose left child is right-heavy), which requires a left rotation on the child followed by a right rotation on the parent.

```python
# Pseudocode for AVL insertion with rotations
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0

def get_height(node):
    return node.height if node else -1

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def insert(node, key):
    # Standard BST insertion
    if not node:
        return AVLNode(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        return node  # no duplicates

    # Update height and rebalance
    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # Left Left case
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    # Right Right case
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    # Left Right case
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    # Right Left case
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node
```

## How It Works

The AVL insertion algorithm works as follows:

1. Perform a standard BST insertion, placing the new key in its appropriate leaf position.
2. On the recursive unwind (returning from the insertion path), update the height of each ancestor node.
3. After each height update, compute the balance factor of the current node.
4. If the balance factor is outside the range [-1, +1], apply the appropriate rotation(s) to restore the AVL property.
5. Propagate height updates upward as needed.

Because the tree height is bounded by O(log n), and each rotation takes O(1) time, the entire insertion operation completes in O(log n) time.

Deletion in AVL trees follows the same pattern but may require rebalancing up the entire path to the root (potentially O(log n) rotations), making deletion more expensive than insertion in practice.

## Practical Applications

AVL trees see use in several specialized scenarios:

- **In-memory databases**: Some in-memory database systems use AVL trees for index structures where search-heavy workloads dominate.
- **Text editors**: The ycmd code-completion server used by YouCompleteMe uses AVL trees for efficient prefix matching.
- **Embedded systems**: AVL trees' predictable O(log n) worst-case behavior makes them attractive in real-time systems where timing guarantees matter.
- **Language runtimes**: The Glibc malloc allocator historically used AVL trees for free block management (though more recent versions have moved to other structures).

## Examples

Consider inserting keys 10, 20, 30, 40, 50, 25 into an empty AVL tree:

- Insert 10 → tree: [10]
- Insert 20 → tree: [10, 20] (inorder: 10, 20)
- Insert 30 → causes right-right imbalance at 10 → left rotation at 10 → tree: [20, 10, 30]
- Insert 40 → insert into right subtree of 20 → causes right-right imbalance at 20 → left rotation at 20 → tree: [20, 10, [30, 40]]
- Insert 50 → continues accumulating on right path
- Insert 25 → causes left-right imbalance at 30

Each insertion triggers at most two rotations, maintaining the O(log n) bound.

## Related Concepts

- [[Red-Black Tree]] - A less strict but faster-to-maintain balanced binary search tree
- [[B-Tree]] - The disk-optimized balanced tree used in databases and file systems
- [[Self-Balancing Trees]] - The broader category of trees that maintain height balance
- [[Binary Search Tree]] - The underlying unbalanced structure that AVL trees augment with balancing
- [[Splay Tree]] - A amortized-balanced tree that moves accessed elements to the root

## Further Reading

- "Introduction to Algorithms" (CLRS), Chapter 13: AVL Trees
- "Data Structures and Algorithm Analysis in C++" by Mark Allen Weiss
- Original paper: "An Algorithm for the Organization of Information" by Adelson-Velsky and Landis (1962)

## Personal Notes

What I appreciate most about AVL trees is how clean and provable they are. The balance factor constraint gives you a precise bound on tree height, and every rotation has a clear geometric interpretation. That said, I've come to understand why red-black trees win in most real-world applications: the amortized cost of maintaining AVL balance on frequent insertions/deletions adds up. AVL trees are excellent when you need guaranteed tight bounds on search depth and your data changes infrequently.
