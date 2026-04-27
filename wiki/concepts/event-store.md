---
title: "Event Store"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [event-sourcing, cqrs, databases, architecture, events]
---

# Event Store

## Overview

An event store is a database optimized for storing sequences of events, serving as the persistence layer for event-driven architectures and event sourcing patterns. Rather than storing current state like a traditional database, an event store records every state change as an immutable, append-only sequence of events. This creates a complete, auditable history of everything that happened in a system, enabling powerful capabilities like temporal queries, event replay, and reconstructing state at any point in time.

Event stores are foundational to [[Event Sourcing]], a pattern where the state of an application is derived entirely from a sequence of events. Instead of updating a record's current state, you append new events describing what happened. To find the current state, you replay all events for an entity from the beginning. This approach provides a complete audit trail and enables sophisticated features like snapshots, time-travel debugging, and maintaining multiple projections of the same data.

The [[CQRS]] (Command Query Responsibility Segregation) pattern pairs naturally with event stores. Commands (writes) produce events that are stored in the event store. Queries read from read models (projections) that are asynchronously built from those events. This separation allows write and read workloads to scale independently and enables different data models optimized for each side.

## Key Concepts

**Append-Only Log** — Events are never modified or deleted; they are only appended to the stream. This immutability is what makes event stores reliable for audit trails and enables event replay. Each event contains a stream ID (identifying the aggregate or entity), a sequence number or version, event type, payload, and metadata (timestamp, user ID, correlation ID).

**Streams** — Events are organized into streams, typically one per aggregate instance. For example, in an e-commerce system, each order would have its own stream `order-{id}` containing events like `OrderCreated`, `OrderItemAdded`, `OrderShipped`. The stream provides ordering guarantees for events within it.

**Event Types and Schemas** — Events have well-defined types (e.g., `UserRegistered`, `PaymentProcessed`) with structured payloads. Schema evolution is critical—over time, event structures change. Upcasting (transforming old event versions to current schema) or versioning strategies ensure old events can still be replayed correctly. Tools like Apache Avro or Protobuf help manage event schemas.

**Projections** — Read models built by consuming events and accumulating state. Projections can be run in-memory, stored in a relational database, or maintained in another event store. They answer business questions like "total revenue per month" or "users who abandoned checkout." [[Projections and Read Models]] are central to [[CQRS]].

**Snapshots** — For aggregates with long event histories, replaying from the beginning becomes slow. Snapshots store periodic state checkpoints, allowing replay to start from a recent snapshot rather than the first event. This is a performance optimization, not a structural requirement.

**Event Subscription** — Consumers subscribe to event streams to be notified of new events. Subscription models include polling, push notifications, and catch-up subscriptions (tracking position and fetching new events). Multiple independent subscribers can consume the same events simultaneously, each building their own projection.

## How It Works

At its core, an event store exposes a simple API for writing and reading events:

```text
# Write events to a stream
POST /streams/{stream-name}/events
{
  "eventType": "OrderPlaced",
  "data": { "orderId": "ord_123", "total": 99.99, "items": [...] },
  "metadata": { "userId": "user_456", "correlationId": "corr_789" }
}

# Read events from a stream (from a specific position)
GET /streams/{stream-name}/events?fromPosition=0

# Subscribe to new events (catch-up subscription)
GET /streams/{stream-name}/subscriptions/{group-name}/events
```

Event store implementations typically use a distributed log underneath (often [[Apache Kafka]] or a purpose-built log store) to provide durability, ordering, and replication. Some event stores (like EventStoreDB) are built specifically for this purpose; others are generalized append-only stores pressed into event sourcing service.

The event replay mechanism works by:
1. Loading all events for a given stream identifier from event store
2. Feeding them sequentially to the aggregate root
3. The aggregate root applies each event to its state via reducer functions
4. Final state is the result of applying all events in order

```javascript
// Simple event-sourced aggregate in JavaScript
class Order {
  constructor(events = []) {
    this.id = null;
    this.status = 'draft';
    this.items = [];
    this.total = 0;
    
    // Replay events to reconstruct state
    for (const event of events) {
      this.apply(event);
    }
  }
  
  apply(event) {
    switch (event.type) {
      case 'OrderCreated':
        this.id = event.data.orderId;
        this.status = 'created';
        break;
      case 'OrderItemAdded':
        this.items.push(event.data.item);
        this.total += event.data.price;
        break;
      case 'OrderShipped':
        this.status = 'shipped';
        break;
    }
  }
  
  placeOrder() {
    return { type: 'OrderCreated', data: { orderId: this.id, items: this.items } };
  }
}
```

## Practical Applications

- **Financial ledgers** — Banks and trading platforms use event sourcing to maintain complete audit trails of every transaction. Regulatory requirements demand immutability and full traceability. Event replay enables reconstructing account state at any historical point.
- **Inventory management** — Tracking every inventory movement (receipts, reservations, shipments, returns) as events provides accurate stock levels and enables "what-if" analysis by replaying scenarios.
- **Customer relationship management** — Storing every customer interaction as events (emails opened, support tickets, purchases) creates a rich timeline and enables machine learning models to predict churn or next best action.
- **Supply chain systems** — Goods movement through a supply chain generates events that must be tracked immutably for compliance and traceability (e.g., food safety requires knowing the provenance of every ingredient).
- **Gaming** — Game state can be event-sourced to enable replay, cheating detection, and player behavior analytics.

## Examples

**EventStoreDB** — A purpose-built event store database by the creators of Event Sourcing. It provides streams, projections, subscriptions, and manages schema evolution. Used in production by many organizations for event-centric architectures.

**Apache Kafka** — While primarily a distributed log and [[Message Queue]], Kafka can serve as an event store when used with log compaction (retaining the latest value per key). Kafka Streams provides state store functionality built on top of Kafka.

**Axon Framework** — A Java framework for building event-sourced applications. It handles aggregate lifecycle, command handling, event publishing, and projection management. Integrates with EventStoreDB and other event stores.

```yaml
# Example: Event store stream configuration (EventStoreDB)
streams:
  - name: order
    events:
      - OrderCreated
      - OrderItemAdded
      - OrderItemRemoved
      - OrderPlaced
      - OrderShipped
      - OrderDelivered
      - OrderCancelled
  - name: user
    events:
      - UserRegistered
      - UserEmailChanged
      - User deactivated
```

## Related Concepts

- [[Event Sourcing]] — Deriving state from a sequence of events
- [[CQRS]] — Separating command (write) and query (read) responsibilities
- [[Projections and Read Models]] — Building queryable views from event streams
- [[Apache Kafka]] — Distributed log often used as event store backend
- [[Message Queue]] — Asynchronous messaging patterns that complement event stores
- [[Event-Driven Architecture]] — Systems built around event production and consumption
- [[Saga Pattern]] — Managing distributed transactions using events in [[Microservices]]

## Further Reading

- "Event Sourcing" by Martin Fowler — The foundational article introducing the pattern.
- "What is Event Sourcing?" by Axon Framework — Practical guide to implementing event sourcing.
- EventStoreDB Documentation — Official docs for a purpose-built event store.
- "CQRS and Event Sourcing" by Greg Young — Deep dive by one of the pattern's advocates.

## Personal Notes

Event sourcing is a powerful pattern but comes with significant complexity. The biggest lesson I've learned is that not everything needs to be event-sourced—use it for the core domain objects where audit trail and temporal queries add genuine value, and use regular state storage for simpler entities. The impedance mismatch between how developers think (current state) and how event-sourced systems work (history) is real and can slow onboarding. Investing in good tooling for viewing and replaying events pays dividends. Also, schema evolution isn't theoretical—plan for it from day one, or you'll face painful migrations later.
