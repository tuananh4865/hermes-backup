---
title: "Flyweight Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, structural-patterns, software-architecture, performance, memory-optimization]
---

# Flyweight Pattern

## Overview

The Flyweight Pattern is a structural design pattern that minimizes memory usage by sharing common state among multiple objects. Instead of creating a large number of similar objects, the pattern separates objects into two categories: intrinsic state (shared, immutable data) and extrinsic state (unique, context-dependent data). By extracting the sharable intrinsic state and managing the extrinsic state externally, you can fit thousands of objects into memory that would otherwise require megabytes.

The pattern is named after the boxing weight class "flyweight," referring to its ability to handle many lightweight objects efficiently. It's particularly valuable when dealing with large numbers of similar objects that differ only in a few parameters, such as characters in a text document, trees in a forest, or particles in a particle system.

The key insight is that not all object data needs to be unique. Many objects share underlying characteristics. A tree in a forest doesn't need its own copy of tree-specific data like leaf shape or bark texture—those can be shared across all oak trees. What varies is the tree's position, age, and health—the extrinsic state that the client provides when needed.

## Key Concepts

**Flyweight** is the interface through which flyweights receive and act upon the extrinsic state. It defines methods that allow the flyweight to be manipulated with extrinsic state. In many implementations, this is an abstract class or interface that concrete flyweights implement.

**ConcreteFlyweight** implements the Flyweight interface and stores intrinsic state. This state must be sharable across multiple objects. The concrete flyweight should be immutable—once created, its intrinsic state never changes.

**UnsharedConcreteFlyweight** is an optional variation where the Flyweight interface is implemented but objects are not actually shared. This might be used in composite structures where leaf nodes are still treated as flyweights for interface uniformity.

**FlyweightFactory** creates and manages flyweight objects. When a client requests a flyweight, the factory either creates a new one (if it doesn't exist) or returns an existing one (if it does). This caching ensures that flyweights are shared appropriately.

**Client** maintains the extrinsic state and computes or stores it outside the flyweights. The client passes this state to flyweights when invoking their operations.

## How It Works

The Flyweight Pattern operates by separating object data into two distinct categories:

**Intrinsic state** is the data that's the same across many objects. This data is stored inside the flyweight object and is never changed after construction. Examples include the character code for a text character, the texture for a tree type, or the font for a text style.

**Extrinsic state** is the data that varies between objects and is therefore not stored in the flyweight. This state must be provided by the client when calling flyweight methods. Examples include the position of a character on a page, the coordinates of a tree in a forest, or the size of rendered text.

The pattern typically works like this:
1. A FlyweightFactory maintains a pool of flyweight objects, keyed by intrinsic state
2. When a client needs a flyweight, it asks the factory, which returns an existing object or creates a new one
3. The client provides extrinsic state when calling operations on the flyweight
4. The flyweight combines intrinsic state with the passed extrinsic state to produce the result

This separation allows dramatic memory savings. Instead of storing full position, style, and content data for every character in a document, you store only the content and style (intrinsic), while position (extrinsic) is computed and passed at render time.

## Practical Applications

The Flyweight Pattern appears in many performance-critical systems:

**Text Editors** - Each character in a document can be a flyweight. The character code and font information are shared across all instances of the same character, while position is computed as characters are rendered. This allows documents with millions of characters to be edited with minimal memory.

**Computer Graphics** - In rendering engines, shared resources like textures, shaders, and meshes are flyweights. A forest with thousands of trees shares the tree mesh data while each tree instance has its own position, rotation, and scale.

**Game Development** - Particle systems often use flyweights. Thousands of particles share the same texture and behavior code while having unique positions, velocities, and lifetimes computed externally.

**Web Browsers** - Browsers use flyweight patterns for DOM nodes and CSS style objects. Styles are shared across nodes with identical style definitions, while DOM positions and content are stored per-node.

**Network Servers** - Connection handlers can be flyweights, sharing protocol logic while handling unique connection state.

## Examples

```python
# Intrinsic state - shared flyweight
class TreeType:
    def __init__(self, name: str, color: str, texture: str):
        self._name = name
        self._color = color
        self._texture = texture
    
    def draw(self, canvas, x, y):
        # Draw the tree using shared intrinsic state
        # Position (x, y) is extrinsic - passed in
        print(f"Drawing {self._name} at ({x}, {y}) with {self._color} color")

# Flyweight factory
class TreeFactory:
    _tree_types: dict[str, TreeType] = {}
    
    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
            print(f"Created new TreeType: {name}")
        return cls._tree_types[key]

# Client - uses flyweights
class Tree:
    def __init__(self, x: int, y: int, name: str, color: str, texture: str):
        self._x = x
        self._y = y
        self._type = TreeFactory.get_tree_type(name, color, texture)
    
    def draw(self, canvas):
        self._type.draw(canvas, self._x, self._y)

# Forest with thousands of trees
class Forest:
    def __init__(self):
        self._trees: list[Tree] = []
    
    def plant_tree(self, x, y, name, color, texture):
        tree = Tree(x, y, name, color, texture)
        self._trees.append(tree)
    
    def draw(self, canvas):
        for tree in self._trees:
            tree.draw(canvas)

# Usage - thousands of trees share only a few TreeType objects
forest = Forest()
for i in range(1000):
    forest.plant_tree(i * 5, i * 3, "Oak", "green", "rough")
    forest.plant_tree(i * 7, i * 2, "Pine", "dark green", "smooth")

print(f"Tree count: 2000, but only 2 TreeType objects in memory")
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Singleton Pattern]] - Often used to implement the flyweight factory
- [[Factory Method]] - Factory patterns commonly create flyweight objects
- [[Object Pool]] - Similar goals but focuses on reuse rather than sharing intrinsic state
- [[Memoization]] - Similar caching concept applied to function results

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Effective Java" by Joshua Bloch - discusses flyweight considerations in Java
- Refactoring Guru's Flyweight Pattern guide

## Personal Notes

The flyweight pattern taught me that memory optimization often comes down to understanding what truly varies versus what stays the same. The hardest part is correctly identifying the boundary between intrinsic and extrinsic state. Make the wrong call and you either lose sharing benefits or create thread-safety nightmares. I tend to err on the side of more sharing (intrinsic) since the memory gains are usually substantial and thread safety can be managed with immutable objects.
