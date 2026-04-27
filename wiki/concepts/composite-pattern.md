---
title: "Composite Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, structural-patterns, software-architecture, object-oriented, tree-structures]
---

# Composite Pattern

## Overview

The Composite Pattern is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects. It solves the fundamental problem of treating single instances and compositions uniformly—clients can interact with both leaf objects and composite containers through the same interface without knowing whether they're dealing with a simple object or a complex hierarchy.

The pattern establishes a unified interface that both leaf objects and composite containers implement. This uniformity means you can write code that operates on the interface without caring about the underlying implementation details. The composite container holds a collection of child components and delegates work to them, while leaf objects perform the actual work directly.

This pattern is essential when building systems that must represent part-whole hierarchies, such as file systems, organizational charts, GUI toolkits, and document structures. Without the Composite Pattern, you'd need to write different code paths for handling individual objects versus collections, leading to tangled conditional logic that's hard to maintain and extend.

## Key Concepts

**Component** is the base interface or abstract class that defines the common interface for all objects in the composition. It declares the methods that both leaf objects and composites must implement, such as `operation()`. This interface should be simple enough that clients don't need to distinguish between leaves and composites.

**Leaf** represents individual objects that don't have children. A leaf implements the Component interface and performs actual work, such as rendering a shape, calculating a value, or processing data. Leaves are the terminal nodes in the composition tree.

**Composite** stores child components and implements the Component interface. It delegates work to its children rather than performing work directly. The composite also provides methods for adding and removing child components, making the structure dynamic and flexible.

**Client** works with all objects through the Component interface. It doesn't need to know whether it's manipulating a simple leaf or a complex composite—the same code works for both.

## How It Works

The Composite Pattern works by establishing a recursive composition where composites contain other components, which may themselves be leaves or more composites. When a client calls an operation on a component, the implementation differs based on whether it's a leaf or composite:

- **Leaf implementation**: Performs the work directly and returns the result.
- **Composite implementation**: Performs any preprocessing, delegates to all child components, may collect and combine their results, then returns its own result.

This recursive delegation creates a powerful abstraction. For example, when drawing a shape hierarchy, a group of shapes delegates the `draw()` call to each child, which may itself be a single shape or another group. The client code simply calls `draw()` on the top-level container and the entire structure renders correctly.

The pattern also enables operations that aggregate values across the hierarchy. A `get_size()` method on a file system would return the file size for files but the sum of sizes for directories. Both implement the same interface, so the calling code is identical.

## Practical Applications

The Composite Pattern is ubiquitous in software development wherever tree structures appear:

**File Systems** - Files and directories share a common interface. Directories can contain files or other directories, forming an arbitrarily deep hierarchy. Operations like `get_size()`, `delete()`, and `list_contents()` work uniformly on both.

**GUI Toolkits** - Buttons, labels, and text fields are leaf components, while panels and windows are composites that can contain other components. Layout managers apply to both single widgets and containers, recursively.

**Graphics Rendering** - Shapes like circles and rectangles are leaves, while compound shapes and groups are composites. Transformations and rendering operations apply uniformly across the entire scene graph.

**Organization Charts** - Individual employees and departments both implement a `get_salary()` method. Departments aggregate the salaries of their members recursively.

**AST in Compilers** - Abstract syntax trees use composite patterns where expressions, statements, and declarations are all nodes with different capabilities but common traversal methods.

## Examples

```python
from abc import ABC, abstractmethod

# Component interface
class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass
    
    @abstractmethod
    def display(self, indent: int = 0):
        pass

# Leaf
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size
    
    def get_size(self) -> int:
        return self._size
    
    def display(self, indent: int = 0):
        print(" " * indent + f"- {self._name} ({self._size} bytes)")

# Composite
class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self._name = name
        self._children: list[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent):
        self._children.append(component)
    
    def remove(self, component: FileSystemComponent):
        self._children.remove(component)
    
    def get_size(self) -> int:
        total = 0
        for child in self._children:
            total += child.get_size()
        return total
    
    def display(self, indent: int = 0):
        print(" " * indent + f"+ {self._name}/")
        for child in self._children:
            child.display(indent + 2)

# Usage
root = Directory("root")
docs = Directory("documents")
docs.add(File("resume.pdf", 45000))
docs.add(File("report.docx", 120000))

pictures = Directory("pictures")
pictures.add(File("photo.jpg", 2400000))

root.add(docs)
root.add(pictures)
root.add(File("readme.txt", 2000))

print(f"Total size: {root.get_size()} bytes")  # Recursively calculates
root.display()
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Decorator Pattern]] - Often used alongside composites but focuses on adding responsibilities dynamically
- [[Iterator Pattern]] - Used to traverse composite structures
- [[Visitor Pattern]] - Can add operations to composites without changing the component classes
- [[Chain of Responsibility]] - Both delegate to children, but chain passes to one child while composite iterates all

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Head First Design Patterns" by Freeman & Robson
- Source Making's Composite Pattern tutorial

## Personal Notes

The key insight with the Composite Pattern is that it works best when the component interface is minimal. The temptation is to put every possible method on Component, but this leads to awkward empty implementations in leaves. Better to keep the interface small and use visitor or other patterns when you need to add operations. I've found that most bugs with composites come from forgetting to handle the recursion correctly—usually missing a case where a composite might be empty or where a leaf might unexpectedly have children.
