---
title: "Clean Architecture"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-architecture, design-patterns, solid-principles, code-organization]
---

# Clean Architecture

## Overview

Clean Architecture is a software design philosophy that organizes code into concentric layers with strict dependency rules, placing business logic at the center and pushing infrastructure concerns to the outer edges. Introduced and popularized by Robert C. Martin (Uncle Bob), the pattern aims to create systems that are independent of frameworks, testable, independent of UI, independent of databases, and independent of any external agency. The core principle is that dependencies should point inward—outer layers can depend on inner layers, but inner layers should never depend on outer layers.

The architecture emerged from decades of software engineering experience recognizing that traditional layered architectures often allow business logic to become entangled with database schemas, UI frameworks, and external services. This coupling makes systems fragile, difficult to test, and resistant to change. Clean Architecture provides a blueprint for structuring projects that remain maintainable as requirements evolve and technologies change.

## Key Concepts

**Layers** form the structural backbone of Clean Architecture. The innermost layer, Entities, contains enterprise-wide business rules—algorithms and data structures that would exist regardless of whether this software existed. The next layer, Use Cases, contains application-specific business rules that orchestrate the flow of data to and from entities. Outer layers—Interface Adapters, Frameworks and Drivers—contain the implementation details: UI components, data access code, external services, and utility functions.

**The Dependency Rule** is the most critical constraint: source code dependencies may only point inward. This means that code in the Use Cases layer cannot mention the UI, database, or external frameworks. Instead, abstractions (typically interfaces or abstract classes) define contracts that outer layers implement. This inversion of dependencies enables testing business logic without instantiating actual databases or UI components.

**Boundaries** separate each layer conceptually and physically. A boundary might be implemented as a separate package, module, or project in the codebase. Communication across boundaries should use the abstractions defined at the boundary, never concrete implementations from outer layers. This separation enables teams to work on different layers independently and allows outer layers to be replaced without affecting inner layers.

**Preserving the Inner Circles** requires discipline. The Entities and Use Cases layers should not know anything about the outside world. When a use case needs to send an email, for example, it defines an output port interface (e.g., `NotificationService`) without specifying how notifications are delivered. The outer layer implements this interface with actual email sending code.

## How It Works

In practice, Clean Architecture manifests through specific structural patterns. A typical project might organize packages as: `domain/` containing entities and use case interfaces, `application/` containing use case implementations, `infrastructure/` containing database repositories and external service clients, and `interface/` containing REST controllers and UI components.

```python
# Example: Clean Architecture in Python

# domain/entities.py
class Order:
    def __init__(self, order_id: str, items: list, status: str):
        self.order_id = order_id
        self.items = items
        self.status = status
    
    def total(self) -> Money:
        return sum(item.subtotal() for item in self.items)

# domain/ports.py (interfaces defining boundaries)
class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def find_by_id(self, order_id: str) -> Order | None: ...

class PaymentGateway(Protocol):
    def charge(self, amount: Money, payment_method: PaymentMethod) -> TransactionId: ...

# application/use_cases.py
class PlaceOrderUseCase:
    def __init__(self, order_repo: OrderRepository, payment: PaymentGateway):
        self._order_repo = order_repo  # Dependencies via constructor injection
        self._payment = payment
    
    def execute(self, command: PlaceOrderCommand) -> OrderResult:
        order = Order(order_id=generate_id(), items=command.items, status="pending")
        
        try:
            transaction_id = self._payment.charge(order.total(), command.payment)
            order.mark_paid(transaction_id)
            self._order_repo.save(order)
            return OrderResult.success(order)
        except PaymentDeclined:
            order.cancel()
            return OrderResult.failed("Payment declined")
```

## Practical Applications

Clean Architecture shines in complex domains where business rules are the core value proposition and likely to evolve independently of technical infrastructure. Enterprise applications, financial systems, healthcare software, and SaaS platforms all benefit from the separation of concerns. The pattern enables teams to add new features by modifying use cases without touching database code, change databases without rewriting business logic, and add new interface types (mobile, API, web) without duplicating domain rules.

The architecture also supports evolutionary design. When a monolithic application must be decomposed into microservices, Clean Architecture naturally suggests service boundaries along use case lines. When a system must migrate from on-premise infrastructure to cloud services, the infrastructure layer provides a natural seam for adaptation.

## Examples

Consider an e-commerce platform built with Clean Architecture. The domain layer contains pure Python classes: `Order`, `Product`, `Customer`, `PricingRule`—no imports from Django, SQLAlchemy, or any external library. Use cases like `PlaceOrderUseCase`, `RefundOrderUseCase`, and `CalculateShippingUseCase` orchestrate business rules without knowing whether orders are stored in PostgreSQL, MongoDB, or flat files.

The infrastructure layer implements the repository interfaces defined in the domain. `PostgresOrderRepository` handles database operations. `StripePaymentGateway` integrates with the payment provider. `EmailNotificationService` handles customer communications. Each can be developed, tested, and replaced independently.

The interface layer exposes functionality through REST APIs, GraphQL resolvers, or CLI commands, each adapting external protocols to the use case interfaces that the application layer expects.

## Related Concepts

- [[SOLID Principles]] - Five object-oriented design principles that complement Clean Architecture
- [[Domain-Driven Design]] - Strategic and tactical patterns for complex domains
- [[Hexagonal Architecture]] - Similar pattern with different terminology (ports and adapters)
- [[Microservices]] - Architectural style that Clean Architecture can inform
- [[Repository Pattern]] - Data access abstraction used within Clean Architecture

## Further Reading

- *Clean Architecture* by Robert C. Martin
- *Architecture: The stuff you can't Google* - Robert Martin's blog posts
- *Get Your Hands Dirty on Clean Architecture* by Tom Hombergs
- Hexagonal Architecture by Alistair Cockburn

## Personal Notes

Clean Architecture requires more upfront structure than simpler patterns, which can feel like overkill for small projects. However, I've consistently seen it pay dividends when projects grow—typically faster than expected. The key discipline is maintaining the dependency rule: when you find yourself importing from outer layers, stop and reconsider. The boundary violations compound over time until the architecture collapses into a big ball of mud. Invest in the structure early; it's much harder to add to an existing mess than to start organized.
