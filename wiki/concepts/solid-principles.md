---
title: "Solid Principles"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-design, object-oriented-programming, design-patterns, clean-code]
---

# Solid Principles

## Overview

The SOLID principles are five fundamental design guidelines in object-oriented programming that promote maintainable, flexible, and robust software architecture. Coined by Robert C. Martin (Uncle Bob) in the early 2000s and popularized through his book "Agile Software Development, Principles, Patterns, and Practices," SOLID provides a mnemonic for remembering these interconnected principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.

These principles address common software design problems that accumulate over time as codebases grow and requirements change. Violations of SOLID often manifest as "big ball of mud" architectures where changes in one area unexpectedly break unrelated functionality, making maintenance increasingly expensive and risky. Following SOLID helps developers create systems where adding new features doesn't require modifying stable existing code, reducing regression bugs and development time.

While originally formulated for object-oriented languages, these principles translate broadly to software design concepts applicable across programming paradigms. Understanding why each principle exists helps developers apply them appropriately rather than treating them as rigid dogma. The goal is not adherence to rules but creating software that can evolve gracefully with changing requirements.

## Key Concepts

**Single Responsibility Principle (SRP)** states that a class should have only one reason to change—meaning it should have only one job or responsibility. When a class has multiple responsibilities, changes to one responsibility may affect the others, creating unintended coupling. SRP doesn't mean a class does only one trivial thing; rather, it encapsulates a coherent set of behaviors that change together for the same reason.

**Open-Closed Principle (OCP)** states that software entities should be open for extension but closed for modification. Well-designed modules allow new behavior to be added without changing existing code. This is achieved through abstraction, inheritance, composition, and polymorphism. The key insight is that once a module is tested and deployed, modifying it introduces risk—extending it through new code is safer.

**Liskov Substitution Principle (LSP)** states that objects of a superclass should be replaceable with objects of a subclass without breaking the application. This means subclasses must honor the contracts of their parent classes—fulfilling method preconditions (not strengthening), postconditions (not weakening), and invariants. A square inheriting from rectangle is a classic LSP violation because setting width differently than height violates the expected rectangle behavior.

**Interface Segregation Principle (ISP)** states that clients should not be forced to depend on interfaces they don't use. Large, monolithic interfaces create pollution where classes must implement methods they don't need. Better to have many small, specific interfaces than one large general-purpose interface. This reduces unintended coupling and makes systems more modular.

**Dependency Inversion Principle (DIP)** states that high-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions. This inversion of typical dependency direction enables flexible architectures where high-level business logic doesn't couple to specific database or framework implementations.

## How It Works

Applying SOLID principles requires iterative refactoring as understanding of requirements evolves. Start by identifying code that frequently changes together versus code that changes for different reasons. Extract classes with multiple responsibilities into separate components. Introduce abstractions (interfaces or abstract classes) to decouple high-level policies from low-level details.

Dependency injection and inversion of control containers support DIP by allowing dependencies to be supplied externally rather than hard-coded. This enables swapping implementations (real vs mock objects for testing) and alternate strategies without changing consumer code. Constructor injection is preferred as it makes dependencies explicit and ensures objects are fully initialized before use.

The SOLID principles reinforce each other. SRP makes ISP easier because focused classes naturally have smaller interfaces. DIP enables OCP because abstractions isolate change. LSP ensures inheritance hierarchies make semantic sense. Together they create code that's easier to test, extend, and reason about.

## Practical Applications

1. **Framework Design**: Libraries and frameworks apply SOLID to provide extension points without requiring users to modify framework code.

2. **Test-Driven Development**: SOLID-compliant code is easier to unit test because dependencies are explicit and classes are single-purpose.

3. **Microservices Architecture**: Service boundaries naturally enforce SRP at system level; DIP guides service interaction design.

4. **Legacy Code Refactoring**: SOLID provides criteria for identifying refactoring targets and evaluating proposed changes.

```python
# Example: Applying SRP - separating concerns
# Bad: Class handles multiple responsibilities
class UserManager:
    def authenticate(self, username, password): ...
    def send_email(self, message): ...
    def generate_report(self): ...
    def save_to_database(self): ...

# Good: Each class has single responsibility
class AuthenticationService:
    def authenticate(self, username, password): ...

class EmailService:
    def send_email(self, message): ...

class ReportingService:
    def generate_report(self): ...

class UserRepository:
    def save(self, user): ...
```

## Examples

**DIP in Practice**: Instead of a high-level `OrderProcessor` directly depending on low-level `MySQLDatabase`, both depend on an abstraction `IRepository`:

```python
class OrderProcessor:
    def __init__(self, repository: IRepository):  # DIP: depends on abstraction
        self.repository = repository
    
    def process(self, order):
        self.repository.save(order)

class MySQLRepository(IRepository):
    def save(self, item): ...
    
class InMemoryRepository(IRepository):  # Swap for testing
    def save(self, item): ...
```

**ISP in Practice**: A `Machine` interface shouldn't force `Printer` classes to implement `scan()`:

```python
# Segregated interfaces
class PrinterProtocol:
    def print(self, document): ...

class ScannerProtocol:
    def scan(self) -> Document: ...

# Flexible implementation
class MultiFunctionPrinter(PrinterProtocol, ScannerProtocol):
    def print(self, document): ...
    def scan(self) -> Document: ...

class SimplePrinter(PrinterProtocol):
    def print(self, document): ...  # No scan() pollution
```

## Related Concepts

- [[Object-Oriented Programming]] - The paradigm SOLID is rooted in
- [[Design Patterns]] - Reusable solutions to common problems
- [[Clean Code]] - Writing readable, maintainable code
- [[Refactoring]] - Improving code structure without changing behavior
- [[Dependency Injection]] - Technique supporting DIP
- [[Interface Design]] - Principles for effective API boundaries
- [[Test-Driven Development]] - Development methodology complementing SOLID

## Further Reading

- "Agile Software Development" by Robert C. Martin
- "Clean Architecture" by Robert C. Martin - SOLID in system design
- "Refactoring" by Martin Fowler - Techniques for improving code structure
- "Design Patterns" by Gamma, Helm, Johnson, Vlissides (GoF)

## Personal Notes

SOLID principles have become so widely taught that they're sometimes applied mechanically without understanding intent. Not every violation is a problem—if a class truly has one reason to change and extension points aren't needed, adding abstractions is unnecessary complexity. The principles are guidelines learned through experiencing the pain of their violations. Start applying them when you feel the friction, not prophylactically.
