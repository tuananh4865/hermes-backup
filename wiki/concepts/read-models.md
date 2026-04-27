---
title: "Read Models"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [CQRS, event-sourcing, data-structures, architecture]
---

# Read Models

## Overview

A read model is a data representation optimized for reading and querying, as opposed to the domain model optimized for writing and maintaining invariants. In architectures that separate read and write operations—most notably Command Query Responsibility Segregation (CQRS)—read models are fully independent projections of the underlying data, tailored to specific query patterns. They are typically denormalized, flattened structures that allow applications to retrieve exactly the data needed for a display or report without complex joins or aggregations at request time.

Read models emerge from the principle that the optimal data structure for writes (normalized, transaction-safe, enforcing business rules) is fundamentally different from the optimal structure for reads (denormalized, query-friendly, potentially materialized). By maintaining separate read models, systems can scale read and write workloads independently, optimize each path without compromise, and present data in forms directly useful to consumers.

## Key Concepts

**Denormalization**: Read models intentionally duplicate and flatten data that would be normalized in a write model. For example, a read model for "Order Summary" might include customer name, product titles, and aggregate totals—data that lives across multiple tables in the normalized write model.

**Projections**: In event-sourced systems, read models are built by applying events to a projection function. Each event (e.g., `OrderPlaced`, `PaymentReceived`, `ShipmentDispatched`) is processed to update the read model accordingly. This allows the read model to be rebuilt entirely from the event log at any time.

**Materialized Views**: Traditional relational databases support materialized views—pre-computed query results stored as tables. Read models extend this concept by supporting multiple concurrent read models, each optimized for a specific consumer's needs.

**Eventual Consistency**: Because read models are updated asynchronously from the write path, they may temporarily lag behind the latest state. This eventual consistency is acceptable for many applications but requires careful handling in UX design.

** CQRS Separation**: The write model (command side) handles intent (create, update, delete) and enforces business rules. The read model (query side) handles presentation and has no business logic.

## How It Works

Read models are built and maintained through a propagation mechanism:

1. **Update Trigger**: When a write occurs (command or event), the system identifies which read models need updating.
2. **Projection**: The relevant data is extracted and transformed according to the read model's projection definition.
3. **Storage**: The projected data is written to the read model store—a database, cache, or in-memory structure optimized for the expected query pattern.
4. **Query Execution**: Read requests hit the read model directly, bypassing the complexity of the write model.

In an event-sourced CQRS implementation:

```python
class OrderReadModelProjection:
    def handle_event(self, event):
        if isinstance(event, OrderPlaced):
            self.orders[event.order_id] = {
                'id': event.order_id,
                'customer_name': event.customer_name,
                'total': event.amount,
                'status': 'placed'
            }
        elif isinstance(event, PaymentReceived):
            self.orders[event.order_id]['status'] = 'paid'
        elif isinstance(event, OrderShipped):
            self.orders[event.order_id]['status'] = 'shipped'
```

## Practical Applications

Read models are foundational in several architectural patterns:

- **CQRS Architectures**: Systems like Event Store, Axon Framework, and NServiceBus use read models extensively
- **Reporting Dashboards**: Pre-aggregated data for fast chart rendering
- **Search Interfaces**: Elasticsearch indices are essentially read models optimized for full-text search
- **Mobile Backend**: Server-generated response payloads tailored to mobile UI requirements
- **Microservices Data**: Each service maintains its own read model; cross-service queries are handled via events

## Examples

A "User Dashboard" read model might aggregate data from multiple write-side aggregates:

```json
{
  "user_id": "usr_123",
  "name": "Alice Johnson",
  "total_orders": 47,
  "lifetime_value": 9420.50,
  "last_order_date": "2026-04-10",
  "pending_shipments": 2,
  "loyalty_tier": "gold",
  "recent_views": ["prod_456", "prod_789"]
}
```

This structure would require multiple joins in a normalized write model. As a read model, it's a single document fetch.

## Related Concepts

- [[CQRS]] - Command Query Responsibility Segregation, the architecture that defines distinct read and write models
- [[Event Sourcing]] - Storing events as the source of truth; read models are projections of the event log
- [[Eventual Consistency]] - The consistency model when read and write paths are separated
- [[Materialized Views]] - Database feature that pre-computes query results
- [[Dimensional Modeling]] - Data warehousing technique for structuring read-optimized data

## Further Reading

- "CQRS" by Martin Fowler - Original pattern description
- "Event Sourcing" by Martin Fowler - Complementary pattern
- Axon Framework documentation - Practical CQRS/ES implementation guide

## Personal Notes

The first time I implemented CQRS with dedicated read models, I was struck by how natural it felt to design queries without worrying about write implications. I could create a read model perfectly shaped for the mobile app's UI, completely independently from the domain model that enforced business rules. The downside: debugging eventual consistency issues required building robust tooling to trace event flow. Invest early in observability for event-driven read models—it's worth it.
