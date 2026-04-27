---
title: "Replication"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, databases, availability, consistency, fault-tolerance]
---

# Replication

## Overview

Replication is the practice of maintaining multiple copies of data across separate nodes to improve availability, durability, and read throughput. In distributed systems, replication is a fundamental mechanism for achieving [[Fault Tolerance]] and [[High Availability]]. When a dataset is replicated, clients can read from any replica, and writes are propagated to all copies through various synchronization protocols.

The CAP theorem formalizes the constraints of replicated systems: a distributed system can provide only two of Consistency, Availability, and Partition tolerance simultaneously. Replication strategies make explicit trade-offs along this spectrum. [[Eventual Consistency]] systems prioritize availability and partition tolerance, tolerating temporary divergence between replicas. [[Strong Consistency]] systems like those using [[Paxos]] or [[Raft]] consensus protocols ensure all replicas agree on state before acknowledging operations.

Replication appears everywhere in modern infrastructure—in [[Database]] systems like PostgreSQL and MongoDB, in [[Message Queue]] brokers like Kafka and RabbitMQ, in [[Redis]] for caching, and in distributed filesystems like HDFS.

## Key Concepts

### Synchronous vs Asynchronous Replication

**Synchronous replication** blocks writes until all replicas confirm the operation. This guarantees strong consistency but adds latency proportional to the slowest replica. It's suitable for systems where consistency outweighs performance, such as financial transaction processing.

**Asynchronous replication** acknowledges writes immediately after the primary commits, propagating changes to replicas in the background. This minimizes write latency but permits temporary inconsistency—clients might read stale data immediately after a write. Most [[Event Sourcing]] and [[CQRS]] systems prefer asynchronous replication for its performance benefits.

### Leader-Follower vs Multi-Leader

In **leader-follower replication** (also called primary-replica), all writes go to a designated leader that streams changes to followers. Followers serve reads and may participate in failover if the leader fails. This model appears in PostgreSQL streaming replication, MySQL binlog replication, and [[Redis]] master-slave setups.

**Multi-leader replication** allows writes to multiple nodes, each acting as a leader for its region or domain. Conflicts arise when the same data is modified concurrently on different leaders, requiring conflict resolution strategies. This model suits globally distributed systems where latency to a single leader would be unacceptable.

### Consensus-Based Replication

[[Raft]] and [[Paxos]] are consensus algorithms that enable replicated state machines. They guarantee that majority agreement is required for operations, tolerating minority node failures without data loss. These algorithms are the foundation of distributed databases like etcd (Raft) and Chubby (Paxos).

## How It Works

Replication implementations typically follow one of three propagation models:

**1. Statement-Based Replication** — The primary logs SQL statements (like `INSERT`, `UPDATE`) and replicas replay them. Simple but fragile—non-deterministic functions like `NOW()` or `RAND()` produce different results.

**2. Write-Ahead Log (WAL) Streaming** — The primary streams its WAL entries to replicas, which replay exactly the same operations. Used by PostgreSQL and SQLite. Guarantees exact state equivalence when replayed.

**3. Row-Based Replication** — The primary logs row-level changes (before/after images) rather than statements. More verbose but deterministic. MySQL's binlog uses this approach.

Replicas apply these logs through two mechanisms:
- **Physical replication**: Copy raw bytes or WAL entries
- **Logical replication**: Decode and replay semantic operations

## Practical Applications

### Database High Availability

[[PostgreSQL]] uses streaming replication for HA—standby servers continuously apply WAL records from the primary. In case of primary failure, a standby is promoted with minimal data loss. Tools like Patroni automate failover orchestration.

### Global Distribution

Content Delivery Networks ([[CDN]]) replicate assets across edge locations worldwide, placing content close to users. [[Anycast DNS]] routes users to the nearest replica automatically.

### Message Queue Clustering

Apache [[Kafka]] replicates topic partitions across brokers, configurable per-topic. Replication factor and minimum in-sync replicas determine durability guarantees.

## Examples

Configuration for PostgreSQL streaming replication:

```ini
# postgresql.conf on primary
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1GB

# pg_hba.conf on primary - allow replica connections
host replication repl_user 10.0.0.2/32 md5

# Recovery configuration on standby (standby.signal)
standby_mode = 'on'
primary_conninfo = 'host=10.0.0.1 port=5432 user=repl_user'
```

Redis replication configuration:

```bash
# On replica instance
replicaof 10.0.0.1 6379
# Or in redis.conf
replicaof 10.0.0.1 6379
replica-read-only yes
```

## Related Concepts

- [[Raft]] - Consensus algorithm for replicated state machines
- [[Fault Tolerance]] - Systems continuing operation despite failures
- [[Eventual Consistency]] - Consistency model where replicas converge
- [[High Availability]] - Systems designed to minimize downtime
- [[Distributed Systems]] - The broader context for replication

## Further Reading

- *Designing Data-Intensive Applications* by Martin Kleppmann — Chapters on replication models and trade-offs
- PostgreSQL Documentation: Logical Replication

## Personal Notes

Replication is where distributed systems get real. Simple single-node databases become significantly more complex when replicated. I've learned to think carefully about replication topology—ring, star, or mesh—because each has different failure characteristics. Asynchronous replication surprises newcomers who assume their writes are durable when the primary crashes before propagating. Monitoring replica lag is essential for operational awareness.
