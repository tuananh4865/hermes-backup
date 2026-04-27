---
title: Layered Architecture
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-architecture, design-patterns, separation-of-concerns, n-tier]
---

# Layered Architecture

## Overview

Layered architecture is a software design pattern that organizes code into horizontal layers, each with a specific responsibility and purpose. The layers form a hierarchy where each layer depends only on the layer directly beneath it. This separation of concerns makes systems more maintainable, testable, and scalable by isolating different types of logic and enabling teams to work on individual layers independently.

The most common form is the three-tier architecture consisting of presentation (UI), business logic (domain), and data access layers. More complex systems may have additional layers for caching, messaging, or infrastructure concerns. The key principle is that dependencies flow in one direction—downward—never upward or diagonally.

Layered architecture is one of the most established and widely used architectural patterns in enterprise software development. It provides clear boundaries and contracts between teams, making it suitable for large organizations where different teams own different layers.

## Key Concepts

### Presentation Layer (UI)

The topmost layer handles all user interface logic and user interaction. It renders data for users and captures user input. This layer should contain no business logic—it delegates to the layer below and focuses purely on presentation concerns.

Examples: React components, Angular controllers, Django views, Spring MVC controllers.

### Business Logic Layer (Domain)

Also called the domain layer, this is where application-specific rules and logic live. It processes data, enforces business rules, and coordinates operations. This layer should be independent of both the UI and data access technologies, making it the most testable and reusable part of the architecture.

### Data Access Layer (Persistence)

This layer handles communication with databases, file systems, and external services. It implements the repository pattern, providing a clean API for CRUD operations. Changing from MySQL to PostgreSQL should only affect this layer, not the business logic above it.

### Additional Layers

- **Service Layer**: Orchestrates multiple domain operations, often used in complex applications
- **Infrastructure Layer**: Cross-cutting concerns like logging, caching, and messaging
- **Application Layer**: Coordinates between UI and domain, often holds use cases and workflows

## How It Works

Request flow in layered architecture follows a strict pattern:

```
User Action → Presentation → Business Logic → Data Access → Database
                ↑                                      │
                └──────────── Response ─────────────────┘
```

1. User interacts with the presentation layer
2. Presentation layer validates input and calls the business logic layer
3. Business logic executes rules and calls data access for persistence
4. Data access queries the database and returns results
5. Results bubble up through each layer back to the user

Each layer has clear boundaries and responsibilities. Dependencies are injected rather than hardcoded, enabling mocking in tests and swapping implementations.

## Practical Applications

### Enterprise Web Applications

Most traditional web applications follow layered architecture. A Java Spring application might have Controllers (presentation), Services (business logic), and Repositories (data access). Each layer is a separate package or module.

### Mobile Applications

Android and iOS apps often follow this pattern. ViewModels or Presenters handle presentation logic, Use Cases or Interactors contain business rules, and Repositories manage data access.

### API Development

REST and GraphQL APIs use layered architecture internally. Request handlers parse input, services execute business logic, and repositories fetch or persist data.

## Examples

A Python example demonstrating layered architecture:

```python
# Presentation Layer
class OrderController:
    def __init__(self, order_service):
        self.order_service = order_service
    
    def create_order(self, request):
        # Validate and extract data from request
        order_data = self._parse_request(request)
        order = self.order_service.place_order(order_data)
        return self._render_response(order)

# Business Logic Layer
class OrderService:
    def __init__(self, order_repository, inventory_service):
        self.order_repository = order_repository
        self.inventory_service = inventory_service
    
    def place_order(self, order_data):
        # Business rules
        if not self.inventory_service.check_availability(order_data.items):
            raise InsufficientInventoryError()
        
        order = Order(order_data)
        order.calculate_total()
        order = self.order_repository.save(order)
        
        self.inventory_service.reserve_items(order_data.items)
        return order

# Data Access Layer
class OrderRepository:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def save(self, order):
        # Direct database interaction
        query = "INSERT INTO orders (customer_id, total) VALUES (?, ?)"
        cursor.execute(query, (order.customer_id, order.total))
        return order
```

## Related Concepts

- [[Microservices]] - Distributing architecture across process boundaries
- [[Clean Architecture]] - A stricter layered architecture with inward dependencies
- [[Domain-Driven Design]] - Bounded contexts and rich domain models
- [[Repository Pattern]] - Abstracting data access behind interfaces
- [[Service Layer]] - Orchestrating domain operations

## Further Reading

- "Patterns of Enterprise Application Architecture" by Martin Fowler
- "Clean Architecture" by Robert C. Martin
- Microsoft .NET application architecture guides

## Personal Notes

Layered architecture works best when you have clear team boundaries—different teams can own different layers. The main anti-pattern is "smart UI" where presentation layer contains business logic, defeating the purpose. Another issue is creating too many layers, which adds unnecessary indirection. I generally prefer 3-4 well-defined layers over 7+ tiny layers. Also, the "service layer" is often unnecessary complexity unless you genuinely have multiple use cases that need orchestration.
