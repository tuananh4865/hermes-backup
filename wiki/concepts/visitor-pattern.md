---
title: "Visitor Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, behavioral-patterns, software-architecture, object-oriented, double-dispatch]
---

# Visitor Pattern

## Overview

The Visitor Pattern is a behavioral design pattern that separates algorithms from the objects on which they operate. It lets you define a new operation without changing the classes of the elements on which it operates, following the Open/Closed Principle. This is particularly valuable when you have a hierarchy of classes and need to perform operations that don't naturally belong inside those classes.

The key challenge the Visitor solves is this: imagine you have a class hierarchy representing different shapes (Circle, Square, Triangle) and you want to add new operations (like area calculation, drawing, XML export) without modifying the shape classes themselves. Each new operation would require modifying every shape class, leading to a proliferation of methods and tight coupling.

The Visitor solves this by introducing a separate hierarchy of visitor classes, one for each operation. Each visitor implements all the variations of the operation for all element types. The elements "accept" visitors and call the appropriate method, using a technique called double dispatch to ensure the right visitor method is invoked.

The elegance of this pattern is that adding new operations requires only new visitor classes—no changes to the element classes. However, adding new element types requires updating all existing visitors to handle the new type. This is a deliberate trade-off: it prioritizes stability of the element hierarchy over flexibility of adding new elements.

## Key Concepts

**Visitor** declares a Visit method for each class of element it can operate on. The method typically follows the naming convention `visit<ElementType>`. Each visitor implements a complete set of operations—one variation for each element type it can handle.

**ConcreteVisitor** implements each operation declared by the Visitor. A concrete visitor contains the actual logic for performing an operation on elements of a specific type. It maintains any state needed during the algorithm's execution.

**Element** defines an `accept` method that takes a visitor as an argument. This method is the same across all element types but is implemented differently—each element type calls the visitor method appropriate to itself.

**ConcreteElement** implements the `accept` method. When `accept` is called with a visitor, the element knows which visitor method should handle it and invokes `visitor.visit<ThisElementType>(self)`.

**ObjectStructure** is a collection of elements that visitors can iterate over. It provides a way to access all elements so visitors can process them. This might be a list, tree, or any container that holds elements.

## How It Works

The Visitor pattern uses double dispatch to route calls correctly:

1. Client creates a ConcreteVisitor and passes it to an ObjectStructure
2. ObjectStructure iterates over elements, calling `element.accept(visitor)` for each
3. Each element's `accept` method receives the visitor and calls `visitor.visit<ThisType>(self)`
4. The visitor method that matches both the visitor type and element type executes

The magic is in step 3. When a Circle calls `visitor.visitCircle(self)`, it's explicitly naming itself as Circle. This explicit self-type information in the call means the compiler generates code that calls the specific `visitCircle` method rather than a generic one. The visitor's `visitCircle` method then knows it's working with a Circle and can access Circle-specific members (perhaps through a type cast).

This double dispatch means:
- New operations can be added by creating new Visitor subclasses
- The element hierarchy remains unchanged when adding operations
- But adding new element types requires updating all existing visitors

## Practical Applications

The Visitor Pattern is common in systems requiring many unrelated operations on a stable hierarchy:

**Compilers and Interpreters** - AST nodes (Abstract Syntax Tree) use visitors for type checking, code generation, optimization passes, and formatting. Each pass is a visitor that traverses and transforms the AST.

**File System Traversal** - Directory structures use visitors for searching, calculating sizes, permission checking, and archival operations without adding methods to file and directory classes.

**GUI Event Handling** - In some frameworks, visitors handle events across widget hierarchies, applying different behaviors based on widget type.

**Serialization** - Converting object graphs to JSON, XML, or other formats is often implemented as visitors that traverse the object structure.

**Testing Frameworks** - Test suites that traverse object structures (like DOM testing) often use visitors to apply assertions uniformly across element types.

**Billing and Reporting Systems** - Systems that need to apply different calculations or reports to different types of entities (employees, departments, locations) use visitors.

## Examples

```python
from abc import ABC, abstractmethod

# Element interface
class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: 'ShapeVisitor'):
        pass

# Concrete elements
class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    def accept(self, visitor: 'ShapeVisitor'):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    def accept(self, visitor: 'ShapeVisitor'):
        return visitor.visit_rectangle(self)

class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self._base = base
        self._height = height
    
    @property
    def base(self):
        return self._base
    
    @property
    def height(self):
        return self._height
    
    def accept(self, visitor: 'ShapeVisitor'):
        return visitor.visit_triangle(self)

# Visitor interface
class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: Circle):
        pass
    
    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle):
        pass
    
    @abstractmethod
    def visit_triangle(self, triangle: Triangle):
        pass

# Concrete visitors - new operations without modifying shapes
class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle):
        import math
        return math.pi * circle.radius ** 2
    
    def visit_rectangle(self, rectangle: Rectangle):
        return rectangle.width * rectangle.height
    
    def visit_triangle(self, triangle: Triangle):
        return 0.5 * triangle.base * triangle.height

class ShapeDrawer(ShapeVisitor):
    def visit_circle(self, circle: Circle):
        print(f"Drawing circle with radius {circle.radius}")
    
    def visit_rectangle(self, rectangle: Rectangle):
        print(f"Drawing rectangle {rectangle.width}x{rectangle.height}")
    
    def visit_triangle(self, triangle: Triangle):
        print(f"Drawing triangle with base {triangle.base} and height {triangle.height}")

class XMLExporter(ShapeVisitor):
    def visit_circle(self, circle: Circle):
        return f'<circle radius="{circle.radius}"/>'
    
    def visit_rectangle(self, rectangle: Rectangle):
        return f'<rectangle width="{rectangle.width}" height="{rectangle.height}"/>'
    
    def visit_triangle(self, triangle: Triangle):
        return f'<triangle base="{triangle.base}" height="{triangle.height}"/>'

# Object structure
class Drawing:
    def __init__(self):
        self._shapes: list[Shape] = []
    
    def add_shape(self, shape: Shape):
        self._shapes.append(shape)
    
    def accept(self, visitor: ShapeVisitor):
        results = []
        for shape in self._shapes:
            results.append(shape.accept(visitor))
        return results

# Usage
drawing = Drawing()
drawing.add_shape(Circle(5))
drawing.add_shape(Rectangle(4, 6))
drawing.add_shape(Triangle(3, 4))

print("=== Area Calculation ===")
area_calc = AreaCalculator()
areas = drawing.accept(area_calc)
print(f"Areas: {areas}")

print("\n=== Drawing ===")
drawer = ShapeDrawer()
drawing.accept(drawer)

print("\n=== XML Export ===")
exporter = XMLExporter()
shapes_xml = drawing.accept(exporter)
for xml in shapes_xml:
    print(xml)
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Composite Pattern]] - Often used together; visitors traverse composite structures
- [[Interpreter Pattern]] - Uses similar structure but focuses on grammar representation
- [[Double Dispatch]] - The mechanism that makes visitor work correctly
- [[Strategy Pattern]] - Similar intent (separating algorithms) but different implementation

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Head First Design Patterns" by Freeman & Robson
- "Domain-Driven Design" by Evans - discusses usage in complex domains

## Personal Notes

The Visitor pattern clicked when I stopped thinking about "visiting elements" and started thinking about "extracting operations from element classes." The mental model is: elements own their data, visitors own operations on that data. The double dispatch is just machinery to make this separation work without type casts in client code. I use visitors most often when I have a stable class hierarchy but evolving operation needs—like adding new report types or export formats to an existing system.
