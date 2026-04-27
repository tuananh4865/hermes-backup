---
title: "Bridge Pattern"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, structural-patterns, software-architecture, object-oriented]
---

# Bridge Pattern

## Overview

The Bridge Pattern is a structural design pattern that decouples an abstraction from its implementation so that the two can vary independently. It solves the problem of "class explosion" where multiplying combinations of abstractions and implementations creates an unmanageable number of classes. By separating concerns into two separate class hierarchies—one for abstractions and one for implementations—the pattern enables flexibility and extensibility without tight coupling.

The pattern is particularly useful when you need to:
- Avoid permanent binding between an abstraction and its implementation
- Support multiple platforms or backends
- Enable runtime switching of implementations
- Isolate platform-specific code from business logic

## Key Concepts

The Bridge Pattern centers on two main components that work together through composition rather than inheritance:

**Abstraction** defines the high-level control logic for the feature. It maintains a reference to an Implementor object and delegates the actual work to it. The abstraction knows nothing about the concrete implementation classes—it only defines the interface that clients use.

**Implementor** defines the interface for implementation classes. This is typically a lower-level interface that handles primitive operations. The abstraction and implementor evolve separately, allowing either to change without affecting the other.

**RefinedAbstraction** extends the interface provided by Abstraction with more specialized methods. It may add methods or override behavior while still delegating core functionality.

**ConcreteImplementor** provides the actual implementation of the Implementor interface. Each concrete implementor handles a specific platform, backend, or technology.

## How It Works

The pattern works by establishing a "bridge" between the abstraction hierarchy and the implementation hierarchy. Instead of inheriting implementation details into the abstraction class, you compose the abstraction with an implementor object that it can call upon.

When a client calls a method on the abstraction, the abstraction might perform some logic and then call a method on its implementor. The implementor performs the actual low-level work and returns results up the chain. This means:
- Adding new abstractions doesn't require new implementations
- Adding new implementations doesn't require modifying existing abstractions
- You can combine different abstractions with different implementations at runtime

This separation is especially valuable when the abstraction and implementation need to evolve for different reasons. For example, a graphics rendering abstraction might be extended with new shapes while the rendering implementation switches between OpenGL, DirectX, or Vulkan.

## Practical Applications

The Bridge Pattern appears frequently in cross-platform applications and systems with plugin architectures:

**Database Drivers** - Database abstraction layers use the bridge to separate the high-level query API from the low-level database protocol implementations, allowing applications to work with any database by swapping implementations.

**Device Drivers** - Operating systems use the bridge to separate application interfaces from hardware-specific driver implementations, enabling the same API to work across different hardware.

**GUI Toolkits** - Windowing systems separate UI component logic from platform-specific rendering and event handling, allowing code to remain portable while platform implementations vary.

**Logging Frameworks** - Logging libraries often separate the logging API from the actual output mechanisms, allowing logs to go to console, files, databases, or remote services interchangeably.

## Examples

```python
# Implementor interface
class DrawingAPI:
    def draw_circle(self, x, y, radius):
        pass

# Concrete implementor 1
class RasterDrawingAPI(DrawingAPI):
    def draw_circle(self, x, y, radius):
        print(f"Drawing circle at ({x}, {y}) with radius {radius} using raster")

# Concrete implementor 2
class VectorDrawingAPI(DrawingAPI):
    def draw_circle(self, x, y, radius):
        print(f"Drawing circle at ({x}, {y}) with radius {radius} using vector")

# Abstraction
class Shape:
    def __init__(self, drawing_api: DrawingAPI):
        self._drawing_api = drawing_api
    
    def draw(self):
        pass

# Refined abstraction
class CircleShape(Shape):
    def __init__(self, x, y, radius, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._radius = radius
    
    def draw(self):
        self._drawing_api.draw_circle(self._x, self._y, self._radius)

# Usage
raster_api = RasterDrawingAPI()
vector_api = VectorDrawingAPI()

circle1 = CircleShape(1, 2, 3, raster_api)
circle2 = CircleShape(4, 5, 6, vector_api)

circle1.draw()  # Raster implementation
circle2.draw()  # Vector implementation
```

## Related Concepts

- [[Design Patterns]] - The broader category of reusable software solutions
- [[Adapter Pattern]] - Similar structure but serves a different purpose (interface conversion)
- [[Strategy Pattern]] - Similar composition-based approach but focuses on algorithms
- [[Abstract Factory]] - May use bridge patterns internally for platform-specific products
- [[Object-Oriented Programming]] - The programming paradigm that enables this pattern

## Further Reading

- Gamma, Erich, et al. "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Pattern-Oriented Software Architecture" by Buschmann et al.
- Refactoring Guru's Bridge Pattern guide

## Personal Notes

The Bridge Pattern clicked for me when I thought of it as "composition over inheritance" taken to its logical conclusion. The key insight is that if you find yourself creating combinations of classes like `WindowsButton`, `MacButton`, `LinuxButton` and `WindowsDialog`, `MacDialog`, `LinuxDialog`, you're probably missing a bridge. The two dimensions—abstraction and platform—should evolve independently.
