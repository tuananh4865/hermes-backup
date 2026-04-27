---
title: Domain-Driven Design
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ddd, software-architecture, domain-model, microservices]
---

## Overview

Domain-Driven Design (DDD) is a software development methodology that emphasizes aligning code structure and design decisions with the core business domain—the real-world processes, rules, and terminology that the software is meant to support. Rather than treating business logic as an afterthought to be bolted onto a technical architecture, DDD places the domain model at the center of the design process. This approach was formalized by Eric Evans in his seminal book "Domain-Driven Design: Tackling Complexity in the Heart of Software" published in 2003.

The fundamental premise of DDD is that software is most effective when it reflects the mental models and language used by domain experts—the people who deeply understand the business problem being solved. When developers and domain experts share a common language, often called the "ubiquitous language," the resulting software becomes more accurate, maintainable, and adaptable to changing business requirements. This shared language is embedded directly into the codebase through class names, method names, and the structure of domain objects.

DDD is particularly valuable in complex domains where business rules are intricate, relationships between entities are nuanced, and the domain itself evolves over time. It provides a framework for managing complexity by breaking down the overall domain into smaller, more manageable pieces while maintaining a coherent overall structure. This makes it especially relevant in modern software development contexts such as [[microservices]] architecture, where services are often designed around business capabilities rather than technical layers.

## Key Concepts

### Bounded Contexts

A bounded context is the central pattern in DDD for managing complexity at an organizational scale. It defines a specific boundary within which a particular domain model applies exclusively. Inside the boundary, all terms, concepts, and rules of the [[ubiquitous language]] are consistent and unambiguous. Outside the boundary, the same words might have different meanings or different models may apply.

In practice, a bounded context often corresponds to a distinct business capability or department. For example, in an e-commerce system, the "order management" bounded context would have its own model of what an "order" means—including states like "pending," "shipped," and "delivered." Meanwhile, the "inventory" bounded context would have its own model of product availability, with different rules about stock levels and reservations. These two contexts interact but maintain distinct models, preventing the confusion that arises when a single model tries to please everyone.

Bounded contexts also define ownership boundaries in large organizations. Each team can develop and evolve their bounded context independently, as long as they maintain the integrity of the contracts (often implemented as [[anti-corruption layers]]) that connect their context to others. This autonomy is why DDD pairs so naturally with microservices architectures, where service boundaries are ideally drawn along business capability lines.

### Aggregates

Aggregates are clusters of related domain objects that are treated as a single unit for data changes. An aggregate has a root entity called the aggregate root, which is the only member of the aggregate that external objects are allowed to hold references to. This design ensures that all changes to objects within the aggregate pass through the aggregate root, maintaining consistency and enforcing business rules that span multiple entities.

The concept of an aggregate is critical for maintaining [[invariant]]s—conditions that must always hold true for the domain to remain valid. For example, in an order processing system, an Order aggregate might contain the Order entity plus multiple OrderLineItem entities. The aggregate root enforces rules like "an order cannot be shipped if it has no line items" or "the total price must equal the sum of line item prices." By encapsulating these rules within the aggregate, the system ensures that invariants are never violated, regardless of how external code attempts to modify the data.

Aggregate boundaries also define the scope of data transactions in DDD. Each aggregate should be independently durable—changes to one aggregate should not require coordinated changes to another aggregate in the same operation. This principle enables eventual consistency patterns that are essential for distributed systems and [[microservices]] architectures, where synchronous database transactions across service boundaries are not practical or desirable.

### Entities and Value Objects

Within DDD, objects are categorized as either entities or value objects based on their identity characteristics. Entities are objects defined by a unique identifier that persists over time, even as their attributes change. A Customer or an Order is typically an entity because two orders with identical attributes are still distinct orders. Value objects, by contrast, are defined entirely by their attributes and have no conceptual identity. A Money amount or a MailingAddress is a value object—it is the attributes that matter, not which particular instance we are referring to.

This distinction influences how objects are designed and used. Entities are typically stored with their identifiers as keys, while value objects are often embedded within entities or stored as part of the entity's record. Value objects are also immutable by design—instead of modifying a Money object, you create a new Money with the new value. This immutability simplifies reasoning about state and prevents side effects that could violate domain rules.

## Related

- [[Microservices]] - Architecture style that often benefits from DDD bounded context design
- [[Event Sourcing]] - Pattern commonly used alongside DDD for capturing aggregate state changes
- [[Command Query Responsibility Segregation]] - Architecture pattern that pairs well with DDD
- [[Domain Model]] - The pattern of representing business concepts directly in code
- [[Ubiquitous Language]] - The shared language between developers and domain experts
