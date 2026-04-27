---
title: Hexagonal Architecture
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [architecture, software-design, domain-driven-design, patterns]
---

## Overview

Hexagonal Architecture, also known as Ports and Adapters, is a software design pattern introduced by Alistair Cockburn in 2005 that structures an application into inner and outer layers. The core business logic sits at the center, completely isolated from external concerns like databases, web frameworks, and UI components. All input and output flows through dedicated ports — interfaces that define how the outside world communicates with the core. This inversion of dependencies ensures the domain remains testable and independent of any specific technology stack.

The architecture gets its name from the visual metaphor: the core domain sits inside a hexagon, with ports arranged along its edges and adapters plugged into those ports. This geometry is arbitrary; any shape would work. The point is to illustrate that the application's logic has no natural edges facing outward — everything external is an adapter that must conform to a defined port contract.

## Key Concepts

**Ports** are the boundaries of the application. An input port (or driving port) defines how the outside world triggers the application — for example, a service interface that use-case classes implement. An output port (or driven port) defines what the application needs from the outside — for instance, a repository interface for fetching data. Ports are abstract; they belong inside the application core.

**Adapters** are the concrete implementations that sit outside the core. A REST controller is a driving adapter that receives HTTP requests and calls input ports. A database repository implementation is a driven adapter that satisfies an output port by querying an actual DB. Multiple adapters can plug into the same port — swapping MySQL for PostgreSQL requires only a new adapter.

**The Core (or Hexagon)** contains all business logic, domain models, and application services. It has no dependencies on frameworks, libraries, or infrastructure. This is what makes the architecture testable: you can exercise all business rules with simple in-memory adapters and no external systems.

## How It Works

When a user interaction arrives (e.g., an HTTP request), a driving adapter receives it and translates it into a call to an input port. The input port delegates to an application service or use case inside the core. That service orchestrates domain logic, potentially calling output ports to fetch or persist data. Output port calls are delegated to a plugged-in driven adapter, which translates the call into database queries, API calls, or file system operations.

The key mechanism is **dependency inversion**: the core defines the port interfaces, and adapters implement those interfaces. The core never references adapters directly. This keeps the core immune to changes in infrastructure.

```python
# Output port (defined in core - no external imports)
class UserRepository(Protocol):
    def find_by_id(self, user_id: str) -> User | None: ...
    def save(self, user: User) -> None: ...

# Application service (in core)
class RegisterUser:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def execute(self, email: str, name: str) -> User:
        if self._repo.find_by_email(email):
            raise ValueError("Email already registered")
        user = User(email=email, name=name)
        self._repo.save(user)
        return user

# Driven adapter (outside core - implements the port)
class PostgresUserRepository:
    def __init__(self, session: DbSession):
        self._session = session

    def find_by_email(self, email: str) -> User | None:
        row = self._session.query(UserRow).filter_by(email=email).first()
        return User.from_row(row) if row else None
```

## Practical Applications

Hexagonal Architecture is especially valuable in long-lived systems where the domain logic is stable but the surrounding technology changes frequently. A financial trading platform, for instance, might change its market data provider, its order routing infrastructure, or its user interface — all without touching the core domain. The architecture also supports test-driven development: you write the core logic against in-memory stubs, then deploy with real adapters.

It pairs naturally with [[domain-driven-design]], where bounded contexts map cleanly onto hexagonal boundaries. [[Clean Architecture]] by Robert C. Martin is a closely related variant that adds more layers (entities, use cases, interfaces) but shares the same dependency-inversion philosophy. [[Event-driven architecture]] can be layered on top, with domain events flowing through output ports to messaging adapters.

## Examples

Consider an e-commerce order fulfillment system. The core contains `Order`, `Inventory`, and `Shipment` domain objects with their associated business rules. An input port `OrderService` exposes operations like `place_order` and `cancel_order`. Driving adapters include a REST API controller, a GraphQL resolver, and a message queue consumer. Driven adapters include `PostgresOrderRepository`, `RedisInventoryCache`, and `StripePaymentGateway`. Swapping Stripe for a different payment provider requires only writing a new adapter — the core and all other adapters remain untouched.

## Related Concepts

- [[domain-driven-design]] — DDD's bounded contexts align naturally with hexagonal boundaries
- [[clean-architecture]] — Closely related pattern emphasizing layered dependency rules
- [[dependency-injection]] — The mechanism used to wire adapters into the core at runtime
- [[solid-principles]] — The design principles that underpin good port/interface design
- [[bounded-context]] — DDD's concept of split ownership that maps onto hexagonal isolation

## Further Reading

- Alistair Cockburn, "Hexagonal Architecture" (original article, 2005)
- "Getting Started with Hexagonal Architecture" — various implementations in Java, Python, Go
- "Ports and Adapters Pattern" on Martin Fowler's site

## Personal Notes

Hexagonal Architecture clicked for me when I stopped thinking of it as a framework and started treating it as a set of dependency rules. Any complexity beyond a few adapters usually signals that the port abstractions are leaking — the core is probably knowing too much about infrastructure details. The visual hexagon is less important than the discipline of keeping the core pure.
