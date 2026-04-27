---
title: "Pacelc"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, cap-theorem, consistency, latency, database, system-design]
---

# Pacelc

## Overview

PACELC (which stands for "Partition, Availability, Consistency, Else Latency, Consistency") is a theorem in distributed systems theory that extends and clarifies the famous [[CAP Theorem]]. While CAP states that during a network partition, a distributed system must choose between availability and consistency, PACELC goes further by asserting that even in the absence of partitions, distributed systems face a fundamental trade-off between latency and consistency.

The PACELC theorem was formalized by Daniel J. Abadi in 2012 as a response to what Abadi viewed as an oversimplification in the CAP formulation. The key insight is that CAP only describes system behavior during the rare event of a network partition, saying nothing about the much more common case where the network is functioning normally. In normal operation, every distributed database makes implicit choices about how much latency to accept in exchange for how much consistency — choices that CAP doesn't capture.

PACELC formalizes this as: **In a distributed system, either the system experiences a network partition (P), in which case it must choose between availability (A) and consistency (C); or else (E) — in the absence of partitions — the system must choose between latency (L) and consistency (C).** This creates a two-dimensional trade-off space rather than CAP's single binary choice.

## Key Concepts

**The PACELC Formulation**: The theorem can be expressed as a decision tree:

1. **IF** a partition occurs (P): Choose between Availability (A) or Consistency (C)
2. **ELSE** (E), no partition: Choose between Latency (L) or Consistency (C)

This means that distributed databases are characterized by two properties:
- Their behavior during partitions: PA or PC systems
- Their behavior in normal operation: EL or EC systems

Common classifications include **PA/EC** systems (choose availability during partitions, accept latency for consistency in normal operation) and **PC/EL** systems (choose consistency during partitions, accept lower consistency for lower latency in normal operation).

**PA/EC Systems (e.g., Cassandra, DynamoDB)**: These systems prioritize availability during partitions. During normal operation, they typically favor low latency over strong consistency, making them suitable for use cases where responsiveness is critical and eventual consistency is acceptable. These systems offer tunable consistency — you can choose per-query whether to prioritize latency (read from one node) or consistency (read from quorum of nodes).

**PC/EL Systems (e.g., HBase, Bigtable, traditional RDBMS)**: These systems prioritize consistency during partitions, potentially becoming unavailable. In normal operation, they favor consistency, meaning read-your-writes and other strong guarantees, at the cost of potentially higher latency due to synchronization overhead.

**Latency vs. Consistency Trade-offs**: In normal operation, a system can either invest network round trips and coordination effort to ensure consistency (higher latency) or accept weaker consistency guarantees to serve requests faster (lower latency). Synchronous replication ensures consistency but adds latency; asynchronous replication reduces latency but introduces inconsistency windows where reads may return stale data.

**Tunable Consistency**: Many modern distributed databases expose consistency as a knob. [[Cassandra]]'s configurable consistency level (ONE, QUORUM, ALL) allows applications to choose per-query whether they want lower latency (ONE) or stronger consistency (QUORUM/ALL). This is essentially choosing a point along the latency-consistency spectrum at runtime.

## How It Works

The trade-offs described by PACELC manifest in how databases handle replication and consensus:

**Synchronous Replication (favors consistency)**: When a write is acknowledged, all replicas confirm they've written the data before returning to the client. This ensures strong consistency but introduces latency proportional to the round-trip time between nodes. During a partition, this coordination may be impossible, causing the system to become unavailable.

**Asynchronous Replication (favors latency)**: Writes are acknowledged immediately after the primary node persists the data, with replication happening in the background. This minimizes write latency but creates windows where data may be lost if the primary fails before replication completes. Reads may return stale data if routed to a lagging replica.

**Quorum-based Operations**: Many systems use quorum algorithms where a write must be acknowledged by a majority of nodes (e.g., N/2+1) and reads must query a quorum. This provides good fault tolerance and tunable consistency, but the need to contact multiple nodes introduces latency that pure eventual consistency systems avoid.

The PACELC framework helps architects reason about these trade-offs systematically. A financial system requiring strong consistency might accept higher latency. A social media feed prioritizing responsiveness might accept eventual consistency. Neither choice is universally correct — the right point on the latency-consistency spectrum depends on the application's requirements.

## Practical Applications

**Choosing a Database**: Understanding PACELC helps select the right distributed database for an application. A system requiring strong ACID guarantees (banking, inventory) should favor PC/EL systems. A system prioritizing user-facing responsiveness (feeds, recommendations, session data) may benefit from PA/EC systems.

**Designing for Failure**: PACELC encourages architects to explicitly design for partition scenarios, not just assume the network is reliable. Applications must understand what happens during partitions and make conscious choices about whether availability or consistency matters more for specific operations.

**Configuring Consistency Levels**: When using tunable consistency databases, understanding PACELC helps set appropriate consistency levels per operation. Bulk reads can use lower consistency for speed; operations involving money or inventory should use higher consistency.

**Microservices Data Patterns**: In microservice architectures, each service can choose its own point on the PACELC spectrum. An order management service might choose strong consistency while a recommendation service tolerates eventual consistency. This is the [[microservices]] approach to handling the heterogeneity of data requirements.

## Examples

Comparison of distributed databases through the PACELC lens:

| Database | Partition Behavior | Normal Operation |
|----------|-------------------|------------------|
| [[Cassandra]] | PA (availability) | EL (low latency) |
| HBase | PC (consistency) | EC (consistency) |
| [[DynamoDB]] | PA (availability) | EL (low latency) |
| Zookeeper | PC (consistency) | EC (consistency) |
| [[Riak]] | PA (availability) | EL (low latency) |

Read latency comparison at different consistency levels in a 5-node Cassandra cluster:

```python
def read_latency(consistency_level, network_latency_ms=1):
    """
    Estimate read latency based on consistency level.
    Actual latency depends on coordination, contention, and replication.
    """
    if consistency_level == 'ONE':
        # Read from closest replica
        return network_latency_ms * 1 + 2  # 1 hop + processing
    elif consistency_level == 'QUORUM':
        # Read from quorum (3 of 5 nodes)
        return network_latency_ms * 2 + 5  # 2 hops average + coordination
    elif consistency_level == 'ALL':
        # Read from all nodes
        return network_latency_ms * 4 + 10  # 4 hops + slowest node
    return network_latency_ms * 1 + 2

# Example: Latency estimates (ms) with 1ms network latency
print(f"ONE: ~{read_latency('ONE')}ms")      # ~3ms
print(f"QUORUM: ~{read_latency('QUORUM')}ms") # ~7ms
print(f"ALL: ~{read_latency('ALL')}ms")       # ~14ms
```

Designing an application with PACELC in mind:

```python
class UserProfileStore:
    """
    Hybrid approach: use different consistency for different operations.
    This pattern reflects PACELC awareness in application design.
    """
    def __init__(self, db):
        self.db = db  # Assume Cassandra or similar tunable system

    async def update_display_name(self, user_id, name):
        # Writes need strong consistency — use QUORUM
        # If this fails during partition, we fail rather than corrupt data
        await self.db.execute(
            'UPDATE users SET display_name = ? WHERE id = ?',
            [name, user_id],
            consistency='QUORUM'
        )

    async def get_display_name(self, user_id):
        # Reads can be eventually consistent — use ONE for low latency
        # Accept that during concurrent writes we might briefly see stale name
        return await self.db.execute(
            'SELECT display_name FROM users WHERE id = ?',
            [user_id],
            consistency='ONE'
        )

    async def get_profile_photo_url(self, user_id):
        # Photo URL changes rarely — use LOCAL_QUORUM for balance
        # Local datacenter consistency with reasonable latency
        return await self.db.execute(
            'SELECT photo_url FROM users WHERE id = ?',
            [user_id],
            consistency='LOCAL_QUORUM'
        )
```

## Related Concepts

- [[CAP Theorem]] - The foundational theorem PACELC extends
- [[Distributed Systems]] - The domain where PACELC applies
- [[Cassandra]] - A PA/EL distributed database
- [[Consistency]] - The property traded off against availability and latency
- [[Microservices]] - Architecture pattern where PACELC considerations are critical
- [[Eventual Consistency]] - The weak consistency model favored by PA/EC systems

## Further Reading

- [PACELC Theorem — Daniel J. Abadi](https://www.cs.umd.edu/~abadi/papers/abadi-paxos.pdf)
- [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/2007/10/dynamo_amazons_highly_available.html)
- [Cassandra Documentation on Consistency](https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/dml/dml_config_consistency.html)

## Personal Notes

PACELC clarified something that always felt incomplete about [[CAP Theorem]]: CAP only describes the extreme case of a partition, but partitions are relatively rare compared to normal operation. In normal operation, every system is constantly making the latency-consistency trade-off — it's just usually implicit. Making it explicit through PACELC helps during architecture discussions because it forces everyone to acknowledge that "we want consistency" means accepting latency costs, not just that we're being careful.

For my own projects, I find that most user-facing applications benefit from an awareness of both axes. Reading this has made me more thoughtful about which operations actually need strong consistency (writes, financial data) and which can tolerate eventual consistency (display names, preferences). The pattern of using different consistency levels for different operations within the same application is powerful.
