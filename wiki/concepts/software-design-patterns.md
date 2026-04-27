---
title: "Software Design Patterns"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, object-oriented, architecture, software-engineering, refactoring]
---

# Software Design Patterns

## Overview

Software design patterns are reusable, generalizable solutions to commonly occurring problems in software design and architecture. They represent best practices that have evolved over decades of collective experience across the software engineering community. Unlike specific algorithms, patterns are high-level templates that describe how to structure code and components to solve a problem while avoiding common pitfalls and anti-patterns.

The concept was popularized by the seminal book *Design Patterns: Elements of Reusable Object-Oriented Software* (1994), authored by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides — collectively known as the "Gang of Four" (GoF). This book catalogued 23 classic patterns that became the foundational vocabulary for discussing software architecture. However, design patterns existed before this book, and new categories have emerged since, particularly for functional programming, distributed systems, and concurrent programming.

Design patterns serve multiple purposes: they accelerate development by providing proven blueprints, they improve communication among developers by establishing a shared vocabulary, and they raise the abstraction level at which software design discussions occur. When a developer says "this class needs a factory pattern," other developers immediately understand the intent and structure without needing detailed explanation.

## Categories of Patterns

Design patterns are broadly categorized into three types based on their primary purpose and scope.

### Creational Patterns

Creational patterns deal with object creation mechanisms, controlling how objects are instantiated and composed. They help manage complexity by encapsulating knowledge about which concrete classes a system uses, rather than instantiating classes directly.

**Singleton** ensures a class has only one instance and provides a global access point to it. While sometimes overused, it is appropriate for scenarios like logging, configuration management, and connection pools where a single shared resource is genuinely warranted.

**Factory Method** defines an interface for creating objects but lets subclasses decide which class to instantiate. This defers instantiation logic to subclasses and promotes loose coupling.

**Abstract Factory** provides an interface for creating families of related objects without specifying concrete classes. This is useful when a system needs to be independent of how its products are created and composed.

**Builder** separates the construction of a complex object from its representation. This is particularly valuable when an object can be configured in many ways or when construction involves multiple steps that must be controlled precisely.

```python
# Builder pattern example
class Report:
    def __init__(self):
        self.sections = []

    def add_section(self, title, content):
        self.sections.append({'title': title, 'content': content})
        return self

class ReportBuilder:
    def __init__(self):
        self._report = Report()

    def with_header(self, title):
        self._report.header = title
        return self

    def with_body(self, content):
        self._report.add_section('Body', content)
        return self

    def with_footer(self, text):
        self._report.add_section('Footer', text)
        return self

    def build(self):
        return self._report
```

### Structural Patterns

Structural patterns focus on how classes and objects are composed to form larger structures. They help ensure that when components are combined, the resulting system is flexible, efficient, and easy to modify.

**Adapter** converts the interface of a class into another interface that clients expect. It allows incompatible interfaces to collaborate. Think of it as a bridge between two different APIs or data formats.

**Decorator** attaches additional responsibilities to an object dynamically. Unlike subclassing, which adds behavior permanently, decorators provide a flexible alternative for extending functionality. This pattern is the foundation of Python's `@wraps` decorator and Java's I/O stream classes.

**Facade** provides a unified interface to a set of interfaces in a subsystem. It simplifies complex systems by exposing a higher-level, simplified API while keeping the underlying complexity accessible for advanced use cases.

**Proxy** provides a surrogate or placeholder for another object to control access to it. Common applications include lazy initialization (virtual proxy), logging (protection proxy), and remote object access (remote proxy).

### Behavioral Patterns

Behavioral patterns are concerned with algorithms, responsibilities, and the assignment of duties between objects. They describe patterns of communication between objects and focus on how objects interact and distribute responsibility.

**Observer** defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. This pattern underlies modern reactive programming and event-driven architectures. Many JavaScript frameworks (React, Vue, Angular) use observer patterns extensively for state management.

**Strategy** defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**Command** encapsulates a request as an object, allowing parameterization of clients with different requests, queue or log requests, and support undoable operations. This pattern is fundamental to implementing transactional systems and command-line interfaces.

**State** allows an object to alter its behavior when its internal state changes. The object will appear to change its class. This pattern is particularly useful for workflow engines and parsers.

## Design Patterns in Modern Development

While the GoF patterns remain foundational, modern software development has produced patterns suited to contemporary challenges. In distributed systems and microservices, patterns like Circuit Breaker, Saga, and Event Sourcing address challenges the original patterns did not anticipate. Functional programming has produced patterns like Option/Maybe types, Either types for error handling, and monadic composition — patterns that don't map cleanly onto the GoF taxonomy.

[[Object-oriented programming]] still benefits enormously from classical patterns, but developers increasingly combine OOP patterns with functional approaches. [[Functional Programming]] patterns like pure functions, immutability, and composition offer complementary tools for writing correct, maintainable code.

## Code Example

A practical example combining Observer and Strategy patterns:

```python
from abc import ABC, abstractmethod
from typing import List, Callable

# Subject / Observable
class WeatherStation:
    def __init__(self):
        self._observers: List[Callable] = []
        self._temperature = 0.0

    def attach(self, observer: Callable):
        self._observers.append(observer)

    def detach(self, observer: Callable):
        self._observers.remove(observer)

    def set_temperature(self, temp: float):
        self._temperature = temp
        self._notify()

    def _notify(self):
        for observer in self._observers:
            observer(self._temperature)

# Usage
def display_on_screen(temp):
    print(f"Screen: {temp}°C")

def log_to_file(temp):
    print(f"Log: {temp}°C")

station = WeatherStation()
station.attach(display_on_screen)
station.attach(log_to_file)
station.set_temperature(22.5)
```

## Related Concepts

- [[Object-oriented Programming]] - The paradigm where GoF patterns originated
- [[Functional Programming]] - Alternative patterns and approaches
- [[Software Architecture]] - Higher-level structural decisions
- [[Refactoring]] - Applying patterns to improve existing code
- [[Clean Code]] - Writing readable, maintainable code that uses patterns appropriately

## Further Reading

- Design Patterns: Elements of Reusable Object-Oriented Software — Gang of Four
- Head First Design Patterns — Eric Freeman and Elisabeth Robson (more accessible introduction)
- Patterns of Enterprise Application Architecture — Martin Fowler
- Release It! — Michael Nygard (patterns for production systems)

## Personal Notes

Design patterns are a double-edged sword. Junior developers sometimes over-apply them, introducing unnecessary complexity when simpler code would suffice. The key insight is that patterns solve real problems — if you find yourself fighting against a pattern rather than benefiting from it, the pattern may be misapplied. I use patterns as communication tools as much as structural solutions. Saying "this is a classic adapter" conveys more intent than explaining the class hierarchy.

The evolution toward functional programming has been interesting to observe. Many GoF patterns (Strategy, Observer, Visitor) have functional equivalents that are often cleaner. But patterns like Singleton — now considered an anti-pattern in most contexts — show that not all GoF advice has aged equally well.
