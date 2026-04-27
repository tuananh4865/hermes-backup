---
title: "Structural Patterns"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, object-oriented, architecture, software-engineering]
---

# Structural Patterns

## Overview

Structural design patterns are a category of software design patterns that focus on how classes and objects are composed to form larger, more complex structures. Named and catalogued by the Gang of Four (Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) in their seminal 1994 book "Design Patterns: Elements of Reusable Object-Oriented Software," structural patterns address recurring problems in how objects fit together — whether through inheritance, composition, or relationships between interfaces.

The core insight of structural patterns is that the way you compose software components determines the flexibility, reusability, and maintainability of your system. Problems like "I need to add behavior to an existing class without modifying it," "I want to expose a simplified interface to a complex subsystem," or "I need objects with incompatible interfaces to work together" appear repeatedly across software development. Structural patterns provide battle-tested solutions to these assembly problems.

## Key Concepts

**Adapter Pattern** bridges incompatible interfaces. When you have a component that expects interface A but you have a component implementing interface B, an adapter sits between them, translating calls from one interface to the other. This allows existing components to be reused in new contexts without modification.

**Bridge Pattern** separates abstraction from implementation, allowing both to evolve independently. Rather than binding an abstraction to a specific implementation (which creates a combinatorial explosion of subclasses), the bridge keeps them as separate hierarchies connected by a reference.

**Composite Pattern** lets you treat individual objects and compositions uniformly. By defining a common interface for both simple objects and containers of objects, clients can work with single instances or arbitrarily nested structures through the same interface.

**Decorator Pattern** attaches additional responsibilities to objects dynamically. Rather than subclassing to add behavior (which is static and inflexible), decorators wrap objects and add functionality before or after delegating to the wrapped object.

**Facade Pattern** provides a simplified interface to a complex subsystem. Rather than forcing clients to understand and coordinate many components, a facade offers a single entry point that handles the complexity behind the scenes.

**Flyweight Pattern** shares objects efficiently when many instances with identical state are needed. By separating intrinsic state (shared) from extrinsic state (unique per instance), flyweight dramatically reduces memory for large numbers of similar objects.

**Proxy Pattern** provides a surrogate or placeholder for another object, controlling access to it. Proxies add indirection for lazy initialization, access control, logging, caching, or remote communication.

## How It Works

Each structural pattern solves a specific composition problem:

```python
# Adapter Pattern: Making incompatible interfaces work together
class MediaPlayer:
    def play(self, filename: str):
        raise NotImplementedError

class AdvancedMediaPlayer:
    def play_vlc(self, filename: str):
        print(f"Playing VLC: {filename}")
    
    def play_mp4(self, filename: str):
        print(f"Playing MP4: {filename}")

# Adapter makes AdvancedMediaPlayer work as MediaPlayer
class MediaAdapter(MediaPlayer):
    def __init__(self, filename: str):
        self.filename = filename
        self.advanced_player = AdvancedMediaPlayer()
        
        # Determine format from filename
        if filename.endswith('.vlc'):
            self.format = 'vlc'
        elif filename.endswith('.mp4'):
            self.format = 'mp4'
    
    def play(self):
        if self.format == 'vlc':
            self.advanced_player.play_vlc(self.filename)
        elif self.format == 'mp4':
            self.advanced_player.play_mp4(self.filename)
```

```python
# Decorator Pattern: Adding behavior dynamically
class Coffee:
    def cost(self) -> float:
        return 2.00

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()

class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25

# Usage: coffee with milk and sugar
coffee = Sugar(Milk(Coffee()))  # $2.75
```

```python
# Composite Pattern: Uniform treatment of individual and composite objects
from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    @abstractmethod
    def ls(self, indent: str = ""):
        pass

class File(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
    
    def ls(self, indent: str = ""):
        print(f"{indent}file: {self.name}")

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children: list[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent):
        self.children.append(component)
    
    def ls(self, indent: str = ""):
        print(f"{indent}dir: {self.name}/")
        for child in self.children:
            child.ls(indent + "  ")
```

## Practical Applications

Structural patterns appear constantly in real codebases:

- **Wrapper classes**: Many languages' I/O libraries use decorators extensively (BufferedInputStream wraps FileInputStream, which wraps FileDescriptor)
- **GUI toolkits**: Composite pattern for rendering windows, panels, buttons uniformly
- **Web frameworks**: Facade pattern simplifying database access, HTTP handling, and template rendering
- **Microservices**: API gateways act as facades to complex backend service meshes
- **Caching layers**: Proxy pattern controlling access to underlying data stores

## Related Concepts

- [[Design Patterns]] - The broader category containing structural patterns
- [[Adapter Pattern]] - Bridging incompatible interfaces
- [[Decorator Pattern]] - Adding responsibilities dynamically
- [[Composite Pattern]] - Treating compositions uniformly
- [[Proxy Pattern]] - Controlling access to objects
- [[Creational Patterns]] - Patterns for object creation vs. composition
- [[Behavioral Patterns]] - Patterns focusing on object interaction

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" - The original Gang of Four book
- "Head First Design Patterns" - Accessible introduction to patterns
- "Architecture Patterns with Python" - Modern implementation in Python

## Personal Notes

Structural patterns reward understanding the composition problems they solve. I find myself reaching for decorator most often — it's elegant for adding cross-cutting concerns like logging, caching, or validation without polluting the core class. Facades are underappreciated; as systems grow complex, having simplified entry points prevents accidental coupling to internals. The key mistake is over-engineering — not every interface mismatch needs an adapter, sometimes it's cleaner to refactor the interfaces themselves. I also notice structural patterns often emerge during refactoring rather than being applied upfront; you realize two components need to work together and reach for the adapter. Understanding patterns gives you vocabulary for discussing these solutions with other developers.
