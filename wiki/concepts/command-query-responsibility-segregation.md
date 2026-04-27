---
title: Command Query Responsibility Segregation
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cqrs, architecture, event-sourcing, patterns]
---

## Overview

Command Query Responsibility Segregation (CQRS) is an architectural pattern that separates read and write operations into distinct models, allowing each to be optimized independently. The name derives from Bertrand Meyer's Command-Query Separation principle, which states that methods should either perform an action (command) or return data (query), but not both. CQRS extends this principle by proposing that the data structures used for writing (commands) and reading (queries) can and should be completely different, not just the methods.

In a traditional CRUD (Create, Read, Update, Delete) system, the same model handles both read and write operations. This approach works well for simple applications but becomes problematic at scale, where read and write workloads have fundamentally different performance characteristics, scalability requirements, and optimization strategies. CQRS addresses this by splitting the domain model into separate command-side and query-side representations, each tailored to its specific workload.

When a command (write operation) is executed, it modifies the state of the system. When a query (read operation) is executed, it simply retrieves data without modifying anything. In CQRS, these two sides can use entirely different data stores, different data schemas, and even different underlying technologies. For example, the command side might write to a normalized relational database optimized for write consistency, while the query side reads from denormalized read models or projection databases optimized for fast query performance.

## Benefits

The separation of read and write concerns in CQRS delivers several significant advantages for complex systems.

**Independent scaling** is one of the primary benefits. Read and write workloads often have very different traffic patterns and performance requirements. In a typical application, reads vastly outnumber writes, meaning the query side may need to scale horizontally to handle many concurrent read requests, while the command side may require fewer but more robust nodes ensuring data consistency. CQRS allows each side to scale independently based on its actual needs.

**Optimized read models** enable query-side data structures to be shaped specifically for the queries an application needs to support. Rather than reconstructing data from normalized structures on every read, the query side can maintain fully materialized, denormalized views that are pre-joined and pre-aggregated. This eliminates expensive joins at query time and can dramatically reduce latency for read operations.

**Clearer domain logic** results from separating the complex business rules that govern state changes (commands) from the data presentation requirements of clients (queries). Domain models on the command side can focus purely on enforcing business invariants and validations, while query models can be optimized for data representation without being constrained by domain logic.

**Enhanced flexibility** in handling cross-cutting concerns like auditing, caching, and security. Because the read and write paths are separated, each can implement its own caching strategy, security model, and validation rules independently.

## Event Sourcing

CQRS is frequently combined with [[event-sourcing]], where the state changes are stored as a sequence of immutable events rather than as current state. In this combination, the command side appends events to an event store, and the query side maintains read models by processing and projecting these events. This approach provides a complete audit trail of every state change, enables powerful temporal queries by replaying events to any point in time, and decouples the read and write sides even further.

Event sourcing naturally complements CQRS because commands become intent-based operations that produce events, and queries consume projected state derived from those events. The [[event-store]] becomes the source of truth, while the read models are merely convenient derivations. This makes the system highly resilient to schema changes, as historical events can be reprocessed to create new read models when requirements evolve.

Systems using CQRS with event sourcing often implement [[projection-based-reality]] to maintain multiple, possibly overlapping, read models from the same underlying event stream. This allows different parts of the application to have completely different views of the data, each optimized for its specific use case.

## Related

- [[Event Sourcing]] - Storing state changes as a sequence of immutable events
- [[Event Store]] - The persistence mechanism for event-sourced systems
- [[CQRS]] - This pattern's relationship with command-query segregation
- [[Domain-Driven Design]] - The broader context where CQRS is often applied
- [[Eventual Consistency]] - The consistency model typically used on the query side
- [[Read Models]] - The optimized query-side representations in CQRS
- [[Command Pattern]] - The design pattern underlying write operations in CQRS
