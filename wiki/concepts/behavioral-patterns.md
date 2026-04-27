---
title: "Behavioral Patterns"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, software-design, gof, behavioral, design]
---

# Behavioral Patterns

## Overview

Behavioral patterns are a category of design patterns in software engineering that focus on how objects communicate and how responsibilities are distributed between them. Unlike creational patterns that deal with object instantiation or structural patterns that address object composition, behavioral patterns characterize the interactions and control flow between objects and classes. These patterns help make systems more flexible, understandable, and maintainable by clarifying which objects are responsible for which behaviors and how they delegate tasks to one another.

The Gang of Four (Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides) documented eleven behavioral patterns in their seminal book "Design Patterns: Elements of Reusable Object-Oriented Software" (1994). These patterns represent proven solutions to common problems in object-oriented design, particularly around object interaction, algorithm encapsulation, and state management. Behavioral patterns remain highly relevant in modern software development, informing architectural decisions in applications ranging from desktop software to distributed systems.

## Key Concepts

### Responsibility Assignment

The core theme across behavioral patterns is the deliberate assignment of responsibilities. Rather than hardwiring communication between objects, behavioral patterns define explicit mechanisms for objects to interact without becoming tightly coupled. This separation of concerns allows changes to one part of the system without cascading changes throughout.

### Command Pattern

The Command pattern encapsulates a request as an object, allowing parameterization of clients with different requests, queuing of requests, and support for undoable operations. Each command object knows how to perform a specific action and optionally how to undo it. This pattern decouples the object invoking the operation from the one that knows how to perform it.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class TextEditor:
    def __init__(self):
        self.content = ""
    
    def insert(self, text):
        self.content += text
    
    def delete(self, length):
        self.content = self.content[:-length]
    
    def get_content(self):
        return self.content

class InsertCommand(Command):
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.insert(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))

class CommandManager:
    def __init__(self):
        self.history = []
    
    def execute_command(self, cmd):
        cmd.execute()
        self.history.append(cmd)
    
    def undo_last(self):
        if self.history:
            cmd = self.history.pop()
            cmd.undo()
```

### Observer Pattern

The Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. This pattern is the foundation of event-driven programming, implementing publish-subscribe relationships, and maintaining consistency between related objects without tight coupling.

### Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it. This pattern is particularly useful when you need to select an algorithm at runtime or when you have multiple variants of a computation and want to avoid conditional logic.

### State Pattern

The State pattern allows an object to alter its behavior when its internal state changes. The object will appear to change its class. This pattern is useful for finite state machines and for objects whose behavior depends on a mutable internal state that should be encapsulated in separate state objects.

### Template Method Pattern

The Template Method pattern defines the skeleton of an algorithm in a base class, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure. This pattern implements the Hollywood Principle—"don't call us, we'll call you"—inversion of control at the method level.

## How It Works

Behavioral patterns work by redistributing responsibilities across objects in a systematic way. In the Command pattern, rather than an object calling methods directly on another, the calling object holds a reference to a command object that encapsulates the action. The command object contains the receiver (the object that performs the work) and the action to perform. This indirection allows commands to be stored, queued, composed, and undone.

In the Observer pattern, subjects maintain a list of observers and notify them when state changes occur. Observers register themselves with the subject, and when the subject's state changes, it iterates through its observer list and calls an update method. The subject doesn't need to know concrete observer types—it only knows that observers conform to a common interface.

## Practical Applications

Behavioral patterns appear throughout software development. Text editors implement Command patterns for undo/redo functionality. GUI frameworks use Observer patterns extensively for event handling—when a button is clicked, registered observers receive notifications. Web frameworks use Strategy patterns for request handling, authentication, and response rendering—different strategies handle different request types. Game development uses State patterns for character behavior (idle, walking, jumping states) and for AI decision-making. Data processing pipelines often use the Template Method pattern, defining the overall flow while allowing pluggable processing steps.

## Examples

A practical example combining several behavioral patterns is a document editor with an undo system:

```python
# Continuing from the Command pattern example above

editor = TextEditor()
manager = CommandManager()

manager.execute_command(InsertCommand(editor, "Hello "))
manager.execute_command(InsertCommand(editor, "World!"))
print(editor.get_content())  # "Hello World!"

manager.undo_last()
print(editor.get_content())  # "Hello "
```

This simple system demonstrates how Command pattern enables undo functionality. Adding redo support would require a separate "redo stack" and additional logic to pop from it when redo is requested.

## Related Concepts

- [[Design Patterns]] - The broader category containing behavioral patterns
- [[Observer Pattern]] - Publish-subscribe communication between objects
- [[Command Pattern]] - Encapsulating requests as objects with undo capability
- [[Strategy Pattern]] - Interchangeable algorithm families
- [[State Pattern]] - Object behavior based on internal state
- [[Template Method Pattern]] - Algorithm skeleton with overridable steps
- [[Gang of Four]] - The four authors who documented these patterns
- [[Anti-Patterns]] - Common incorrect applications of patterns

## Further Reading

- "Design Patterns: Elements of Reusable Object-Oriented Software" - The original Gang of Four book
- "Head First Design Patterns" - Accessible introduction to behavioral and other patterns
- Source Making Design Patterns guide - Comprehensive online resource
- "Patterns of Enterprise Application Architecture" - Fowler's follow-on work

## Personal Notes

Behavioral patterns are often easier to apply than structural or creational patterns because the problem—objects interacting—is more universally encountered. The key insight is recognizing when communication complexity is building up: when an object knows too much about others (violating the Law of Demeter), when conditional logic for type-specific behavior is proliferating, or when adding new interaction types requires modifying multiple classes. These are signals that a behavioral pattern might help. However, pattern application should be driven by genuine need, not theoretical elegance—over-engineering with patterns can be as harmful as under-engineering.
