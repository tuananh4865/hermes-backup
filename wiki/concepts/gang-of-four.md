---
title: Gang of Four
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [gang-of-four, design-patterns, gof, software-architecture, oop]
---

# Gang of Four (GoF) Design Patterns

## Overview

The Gang of Four (GoF) refers to the four authors of the landmark book "Design Patterns: Elements of Reusable Object-Oriented Software"—Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides—published in 1994. This book catalogued 23 classic design patterns that represent best practices for solving common software design problems in object-oriented programming. These patterns have profoundly influenced software development, becoming essential vocabulary for architects and developers discussing software structure and design.

The GoF patterns are not code libraries or frameworks but rather general, repeatable solutions to recurring problems in software design. They represent the accumulated wisdom of experienced object-oriented designers, capturing solutions that have been refined over many years of practice. While some patterns have been superseded by language features or newer paradigms (like functional programming approaches), the GoF patterns remain foundational knowledge for understanding software architecture and communicating design ideas.

## Key Concepts

### Creational Patterns

Patterns concerned with object creation mechanisms:

**Singleton**: Ensures a class has only one instance with global access point
```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
```

**Factory Method**: Defines an interface for creating objects, letting subclasses decide which class to instantiate

**Abstract Factory**: Provides an interface for creating families of related objects without specifying concrete classes

**Builder**: Separates the construction of complex objects from their representation

**Prototype**: Creates new objects by copying an existing object (clone)

### Structural Patterns

Patterns dealing with object composition:

**Adapter**: Converts one interface into another that clients expect
```python
# Legacy payment processor with incompatible interface
class LegacyPaymentProcessor:
    def process_payment(self, amount, currency):
        # Old API expects (amount, currency) order
        return f"Processed {currency}{amount}"

# Adapter to make it compatible with new interface
class PaymentAdapter:
    def __init__(self, legacy):
        self.legacy = legacy
    
    def pay(self, currency, amount):
        # Swaps arguments to match new API
        return self.legacy.process_payment(amount, currency)
```

**Decorator**: Attaches additional responsibilities to objects dynamically

**Facade**: Provides a simplified interface to a complex subsystem

**Proxy**: Provides a surrogate to control access to another object

### Behavioral Patterns

Patterns concerned with object interaction and responsibility:

**Observer**: Defines a one-to-many dependency so when one object changes, all dependents are notified
```python
class EventManager:
    def __init__(self):
        self._subscribers = {}
    
    def subscribe(self, event, callback):
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(callback)
    
    def notify(self, event, data):
        for callback in self._subscribers.get(event, []):
            callback(data)
```

**Strategy**: Defines a family of algorithms, encapsulates each, and makes them interchangeable

**Command**: Encapsulates a request as an object, enabling undo/redo, queuing

**State**: Allows an object to alter behavior when its internal state changes

**Template Method**: Defines the skeleton of an algorithm, deferring some steps to subclasses

**Iterator**: Provides a way to access elements sequentially without exposing underlying structure

## How It Works

The GoF patterns are united by several principles:

1. **Program to an interface, not an implementation**: Favor abstraction over concrete classes
2. **Favor object composition over class inheritance**: Assemble objects to get new functionality
3. **Encapsulate what varies**: Identify aspects that vary and separate them from what stays the same

Patterns are described with a consistent structure: intent, motivation, structure, implementation, trade-offs, and related patterns.

## Practical Applications

Modern applications of GoF patterns:

- **React and Vue Components**: Higher-order components, render props (Observer/Strategy patterns)
- **Middleware Systems**: Express.js middleware (Chain of Responsibility)
- **State Management**: Redux actions and reducers (Command pattern)
- **Database ORMs**: Active Record, Repository patterns
- **Event Systems**: Observer pattern in GUI frameworks, message buses

## Examples

Applying the Observer pattern for a notification system:

```python
from abc import ABC, abstractmethod

# Subject interface
class Subject:
    @abstractmethod
    def attach(self, observer): pass
    
    @abstractmethod
    def detach(self, observer): pass
    
    @abstractmethod
    def notify(self): pass

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, message): pass

# Concrete implementation
class NewsAgency(Subject):
    def __init__(self):
        self._observers = []
        self._latest_news = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def set_news(self, news):
        self._latest_news = news
        self.notify()
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._latest_news)

class NewsChannel(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, message):
        print(f"{self.name} broadcasting: {message}")
```

## Related Concepts

- [[design-patterns]] — Broader category of reusable software solutions
- [[software-architecture]] — High-level structure and organization of software systems
- [[solid-principles]] — Related design principles for OOP
- [[refactoring]] — Improving existing code structure, often applying patterns
- [[clean-code]] — Writing maintainable, readable code

## Further Reading

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612) - The original GoF book
- [Head First Design Patterns](https://www.headfirstlabs.com/books/hfdp/) - More accessible introduction
- [Pattern-Oriented Software Architecture](https://en.wikipedia.org/wiki/Pattern-oriented_software_architecture) - GoF's successor volumes

## Personal Notes

The Gang of Four patterns were required reading when I started my software career, and while some feel dated (Factory Method is less relevant with dependency injection), the vocabulary is invaluable. Patterns like Observer, Strategy, and Decorator appear constantly in modern codebases, often without being explicitly named. Understanding these patterns changed how I think about code structure and extensibility. My advice: learn the patterns, but don't force them—write code that's simple first, then refactor to patterns when you see the actual problem they solve.
