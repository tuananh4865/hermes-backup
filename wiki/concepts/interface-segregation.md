---
title: "Interface Segregation"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [solid-principles, design-principles, object-oriented-programming, software-design, architecture]
---

# Interface Segregation

## Overview

The Interface Segregation Principle (ISP) is one of the five SOLID principles of object-oriented design, articulated by Robert C. Martin in his 2000 paper "Design Principles and Design Patterns." ISP states that clients should not be forced to depend on interfaces they do not use. In practical terms, this means that rather than having one large, general-purpose interface, you should split it into smaller, more specific interfaces that are tailored to the actual needs of each client or group of clients.

The principle addresses a common problem in software design: fat interfaces. When a class implements an interface that defines methods it never calls, it becomes coupled to behavior it doesn't need. This coupling creates several problems. The implementing class becomes harder to understand and maintain because it carries unnecessary method signatures. Changes to the interface affect all implementers, even those that don't use the changed method. Most critically, clients that depend on only a subset of the interface's methods still become indirectly coupled to all of them through the interface contract.

ISP is closely related to the concept of [[separation of concerns]] and [[single responsibility principle]], which together encourage designing systems where each component has a focused, well-defined role. The principle is especially valuable in large codebases where multiple teams work on different parts of the system, as it reduces the blast radius of interface changes.

## Key Concepts

Understanding ISP requires familiarity with several foundational ideas:

**Fat Interfaces** are the primary problem ISP solves. A fat interface defines many methods that not all implementing classes need. For example, a `Machine` interface with methods like `print()`, `scan()`, `fax()`, and `copy()` forces any client that only needs printing to also be aware of scanning, faxing, and copying capabilities. If any of these methods changes, the client may be affected even though it never used that method.

**Role Interfaces** are the solution. Instead of one `Machine` interface, ISP suggests splitting it into focused interfaces: `Printer`, `Scanner`, `FaxMachine`, and `Copier`. Each interface contains only the methods relevant to its role. Classes can then implement only the interfaces they actually need, reducing coupling and improving cohesion.

**Client-Specific Interfaces** take this further by defining interfaces based on what each specific client actually needs, not just broad roles. A `DocumentEditor` might need `print()` and `save()` from a document class, while a `DocumentArchiver` only needs `save()` and `export()`. Defining interfaces around these specific client needs prevents unnecessary dependencies.

**Interface Contracts** define the communication boundary between components. When an interface is small and focused, its contract is easier to reason about, test, and implement correctly. Larger interfaces have more complex contracts that are harder to satisfy without introducing errors.

## How It Works

In practice, ISP manifests in several concrete patterns. Consider a [[dependency injection]] scenario where a class needs to send notifications. Rather than having that class depend on a massive `NotificationService` interface with methods for email, SMS, push notifications, and in-app messaging, you define separate interfaces: `EmailSender`, `SmsSender`, `PushNotifier`. The class then depends only on the interface it actually uses.

```python
# Anti-pattern: fat interface
class NotificationService:
    def send_email(self, to, subject, body): ...
    def send_sms(self, to, message): ...
    def send_push(self, token, message): ...
    def send_in_app(self, user_id, message): ...

class OrderProcessor:
    def __init__(self, notifications: NotificationService):  # depends on all methods
        ...

# ISP-compliant: role interfaces
class EmailSender:
    def send_email(self, to, subject, body): ...

class SmsSender:
    def send_sms(self, to, message): ...

class OrderProcessor:
    def __init__(self, emailer: EmailSender):  # only depends on what it needs
        ...
```

The same principle applies in API design. A REST API endpoint that returns a massive object with dozens of fields forces every client to parse and handle all of them, even if the client only needs a few fields. A better approach provides focused endpoints or uses query parameters to select specific fields, following ISP's philosophy of not forcing clients to depend on what they don't use.

## Practical Applications

Interface Segregation has wide-ranging applications across software development:

**Library and Framework Design** benefits enormously from ISP. When designing a framework used by many clients, you cannot predict every use case. By providing small, focused extension points (interfaces) rather than monolithic ones, you give framework users the flexibility to implement only what they need. This is why modern frameworks tend toward specialized interfaces like `Serializer`, `Validator`, and `Handler` rather than single comprehensive contracts.

**Microservices Integration** often involves clients that consume multiple services. Each service client interface should be focused on one service's capabilities. A payment service client interface should not also include notification capabilities. This isolation makes it easier to swap implementations, test with mocks, and understand the dependencies in complex systems.

**Plugin Architectures** rely on ISP for extensibility. A plugin system might define `IPlugin` with just `initialize()` and `execute()` methods, rather than burdening every plugin with methods for configuration, persistence, and UI rendering. Plugins that need these capabilities can implement additional, optional interfaces.

**Database Access Layers** benefit from ISP when different parts of an application need different data access operations. A reporting component might only need `read()` methods, while a transaction-processing component needs both `read()` and `write()`. Segregated interfaces allow each component to depend only on the data operations it actually performs.

## Examples

Consider a [[state machine]] implementation where different states have different available transitions. Rather than having a single `State` interface with methods for every possible transition (which would force all states to implement methods for transitions they don't support), you define transition-specific interfaces.

```python
# Without ISP: states must implement all transitions
class State:
    def move_to_start(self): ...
    def move_to_processing(self): ...
    def move_to_complete(self): ...
    def move_to_failed(self): ...
    def retry(self): ...
    def cancel(self): ...

# With ISP: states implement only what they support
class Startable(Protocol):
    def move_to_processing(self) -> "ProcessingState": ...

class Completable(Protocol):
    def move_to_complete(self) -> "CompletedState": ...

class Cancellable(Protocol):
    def cancel(self) -> "CancelledState": ...
```

Another example involves a [[data mapper pattern]] implementation. An `IEntityMapper` interface that forces implementations to handle every possible database operation is fat. Instead, separate `IReader`, `IWriter`, and `IDeleter` interfaces allow read-only mappers to implement only `IReader`, keeping them honest and preventing accidental writes.

## Related Concepts

- [[SOLID Principles]] — The broader family of design principles that includes ISP
- [[Single Responsibility Principle]] — Closely related principle that also promotes focused, cohesive classes
- [[Dependency Inversion Principle]] — Often used together with ISP to depend on abstractions rather than concretions
- [[Separation of Concerns]] — The broader design philosophy that ISP embodies
- [[Design Patterns]] — Patterns like [[strategy-pattern]] and [[adapter-methods]] that benefit from ISP
- [[Dependency Injection]] — A technique commonly used alongside ISP to inject focused interface dependencies
- [[Liskov Substitution Principle]] — Works alongside ISP to ensure interface contracts are meaningful
- [[Clean Architecture]] — Architecture styles that naturally encourage interface segregation through layered boundaries

## Further Reading

- Robert C. Martin, "Design Principles and Design Patterns" (2000) — Original SOLID paper
- Robert C. Martin, "Agile Software Development: Principles, Patterns, and Practices" — Expanded treatment of SOLID principles
- "Implementing Lean Deliver" by Mary and Tom Poppendieck — Related principles for focused, minimal interfaces in manufacturing-inspired software development
- [[solid-principles]]

## Personal Notes

> ISP is one of the most practical SOLID principles because its violations are immediately felt: you write empty method stubs, you pass parameters you don't use, your tests grow unnecessarily complex. When I refactor toward ISP, I often start by asking which methods each client actually calls on an interface. If clients call different subsets, the interface is almost certainly too big.
