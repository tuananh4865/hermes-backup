---
title: Outbox Pattern
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, reliability, messaging, event-driven, patterns]
---

## Overview

The Outbox Pattern is a reliability pattern used in distributed systems to ensure that database updates and message publications happen atomically, eliminating the common problem of "what happens if we crash between updating the database and publishing the message?" Instead of publishing directly to a message broker after a database transaction, the outbox pattern stores the message in a dedicated outbox table within the same transaction as the business data, and a separate process delivers messages from the outbox to the broker.

This pattern solves a fundamental problem in event-driven architectures: the dual-write issue. When you update a database and publish an event to a message broker, these are two separate operations with no atomicity guarantee. If the system crashes after the database commit but before the broker publish, the event is lost. The outbox pattern solves this by treating the outbox table as a persistent queue that survives crashes and can be reliably processed by a separate delivery mechanism.

## Key Concepts

Understanding the outbox pattern requires understanding the dual-write problem and how outbox provides a solution.

**The Dual-Write Problem**

In typical applications, updating a database and publishing an event require two separate operations. If the first succeeds but the second fails, your system is in an inconsistent state—the database reflects the change but no event was published. If the first fails, you simply roll back, but the inverse case is catastrophic. The outbox pattern eliminates this failure mode by making both operations the same operation: writing to the outbox table.

**Outbox Table**

The outbox table stores messages that need to be published. Each row represents a message with fields like: message ID, event type, payload (JSON), created timestamp, processed timestamp, and retry count. This table lives in the same database and transaction as your business data, ensuring atomicity.

**Delivery Guarantee**

By writing to the outbox within the same transaction as business data, you guarantee that either both succeed (business data changed and outbox entry created) or both fail (transaction rolled back, no outbox entry). A separate process—the outbox relay—reads unpublished entries and delivers them to the message broker, handling retries until successful.

**At-Least-Once Delivery**

The outbox pattern provides at-least-once delivery, not exactly-once. The relay may deliver the same message multiple times if it crashes after publishing but before marking the entry as processed. Consumers must therefore implement idempotency. This trade-off is acceptable for most use cases and dramatically simplifies the implementation.

## How It Works

The outbox pattern involves coordinated database operations and a separate relay process.

**Writing to the Outbox**

When your application code updates business data, it also inserts a row into the outbox table within the same database transaction. The outbox entry contains the event type and payload. Because this happens in the same transaction as the business update, either both are committed or neither is.

```python
async def create_order(order_data: dict, db_pool):
    async with db_pool.connection() as conn:
        async with conn.transaction():
            # Insert order
            order = await conn.execute(
                "INSERT INTO orders (customer_id, total) VALUES ($1, $2)",
                order_data["customer_id"], order_data["total"]
            )
            
            # Insert outbox entry (same transaction)
            await conn.execute(
                """INSERT INTO outbox (event_type, payload, created_at)
                   VALUES ($1, $2, NOW())""",
                "OrderCreated", json.dumps({"order_id": order, "data": order_data})
            )
```

**The Outbox Relay**

A separate process—often a background worker, cron job, or dedicated service—periodically polls the outbox table for unpublished entries. It reads entries in order, publishes them to the message broker, and marks them as processed. The relay must be idempotent and handle failures gracefully.

**Batch Processing**

Production outbox implementations typically process entries in batches for efficiency. The relay queries for N unpublished entries, publishes them all, and marks them processed in a single transaction. This approach balances latency (how long before events are published) against throughput (how many events can be processed per second).

**Table Polling vs Change Data Capture**

Two common implementation approaches exist. Table polling simply queries the outbox table periodically. Change Data Capture (CDC) uses database features like PostgreSQL's logical replication to detect new outbox entries and signal the relay. CDC offers lower latency but requires additional infrastructure.

## Practical Applications

The outbox pattern is essential for any system that needs reliable event publication alongside data persistence.

**Event Sourcing**

Event sourcing systems store state changes as a sequence of events. The outbox pattern ensures these events are reliably persisted and published to interested consumers.

**Microservices Integration**

When microservices need to communicate through events (rather than synchronous calls), the outbox pattern ensures that events are never lost between services.

**Audit Logging**

Systems that must maintain an audit trail can use the outbox to store audit entries atomically with business operations, knowing they will be processed reliably.

## Examples

```python
import asyncio
import json
from datetime import datetime
from typing import List

class OutboxRelay:
    def __init__(self, db_pool, kafka_producer, batch_size: int = 100):
        self.db = db_pool
        self.producer = kafka_producer
        self.batch_size = batch_size
    
    async def process_outbox(self):
        while True:
            async with self.db.connection() as conn:
                # Read unpublished entries
                rows = await conn.fetch(
                    """SELECT id, event_type, payload 
                       FROM outbox 
                       WHERE processed_at IS NULL 
                       ORDER BY created_at 
                       LIMIT $1 
                       FOR UPDATE SKIP LOCKED""",
                    self.batch_size
                )
                
                if not rows:
                    await asyncio.sleep(0.1)
                    continue
                
                # Process each entry
                for row in rows:
                    try:
                        await self.producer.send(
                            topic=row['event_type'],
                            value=json.loads(row['payload'])
                        )
                        # Mark as processed
                        await conn.execute(
                            "UPDATE outbox SET processed_at = NOW() WHERE id = $1",
                            row['id']
                        )
                    except Exception as e:
                        # Update retry count, implement backoff
                        await conn.execute(
                            """UPDATE outbox SET retry_count = retry_count + 1, 
                               last_error = $2 WHERE id = $1""",
                            row['id'], str(e)
                        )
            
            await asyncio.sleep(0.01)  # Small delay between batches
```

## Related Concepts

- [[Transactional Outbox]] - The broader pattern that includes outbox
- [[Event-Driven Architecture]] - The architectural style the outbox supports
- [[Idempotency]] - Required property for consumers of outbox events
- [[Message Queue]] - Where outbox events are ultimately published
- [[Change Data Capture]] - An alternative implementation approach

## Further Reading

- "Implementing the Outbox Pattern" by Christian Posta
- "Zero Downtime Deployment" by Vaclav Turecki
- "Building Event-Driven Microservices" by Adam Bellemare

## Personal Notes

The outbox pattern is one of those patterns that seems complex at first but becomes obvious once you understand the problem it solves. I've seen teams struggle with mysterious data inconsistencies that trace back to dual-writes, and introducing the outbox pattern fixes them completely. My advice: start with table polling for simplicity; move to CDC only if latency becomes a real problem. Also, don't forget to clean up old outbox entries eventually, or your table will grow unbounded.
