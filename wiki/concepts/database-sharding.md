---
title: Database Sharding
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [database-sharding, database, scalability, distributed]
---

## Overview

Database sharding is a database architecture pattern that partitions data across multiple database instances, called shards. Each shard holds a subset of the total data, allowing the system to scale horizontally by distributing query load and storage requirements. Sharding is a form of [[horizontal partitioning]] where rows of a database table are split across different physical instances, in contrast to vertical partitioning which splits columns or tables onto different servers.

The core motivation behind sharding is scalability. As data volume and traffic grow, a single database server reaches its capacity limits in terms of CPU, memory, disk I/O, and network bandwidth. Rather than scaling up (vertical scaling or [[scale-up architecture]]), organizations scale out by adding more machines. Sharding enables this horizontal scaling by ensuring that no single shard bears the entire load.

Sharding is distinct from simple replication. In a [[replication]] setup, the same data exists on multiple nodes for fault tolerance and read scaling. In sharding, each piece of data exists on exactly one shard (unless using redundant sharding schemes), and each shard typically serves a different subset of queries. This makes sharding particularly effective for write-heavy workloads where replication would create synchronization overhead.

Modern distributed databases and [[NoSQL]] systems often incorporate sharding as a native feature, while traditional [[relational database]] systems may require application-level logic to route queries to the appropriate shard.

## Strategies

There are several strategies for determining how data is distributed across shards, each with distinct trade-offs in query patterns, data distribution, and operational complexity.

**Hash-based sharding** uses a [[hash function]] applied to one or more shard keys to determine which shard a row belongs to. A common approach calculates the hash of a user ID or similar identifier, then uses modulo arithmetic or a consistent hashing ring to map the hash value to a specific shard. Hash-based sharding provides relatively even data distribution, making it suitable for write-heavy workloads where access patterns are unpredictable. However, range queries that span multiple shards become expensive because the data is distributed pseudo-randomly. Adding new shards also requires reshuffling existing data, though [[consistent hashing]] can minimize data movement during cluster expansion.

**Range-based sharding** partitions data based on a contiguous range of values in a designated shard key. For example, users with IDs 1-1000000 might reside on shard 1, IDs 1000001-2000000 on shard 2, and so on. This approach supports efficient range queries and sequential reads, as data that is accessed together often resides on the same shard. The downside is the risk of [[hotspots]]—if one range receives disproportionately high traffic, that shard becomes a bottleneck. Range-based sharding also requires careful capacity planning to avoid uneven data distribution.

**Directory-based sharding** maintains a lookup table that maps each shard key to its corresponding shard. This approach offers flexibility in assigning data to shards based on arbitrary criteria, including geographic location, tenant ID, or business logic. The lookup table itself becomes a critical dependency that must remain highly available. While powerful, directory-based sharding introduces additional latency for shard resolution and creates a single point of failure if not properly replicated.

## Challenges

Sharding introduces significant operational complexity and trade-offs that must be carefully managed.

**Cross-shard queries** are one of the most common challenges. When data needed for a query spans multiple shards, the application must issue parallel queries to each relevant shard, aggregate results, and potentially sort or paginate them. This dramatically increases query latency and complexity compared to single-shard queries. Queries that involve joins, transactions, or aggregations across shards are particularly difficult to implement efficiently.

**Resharding operations** present another major hurdle. As data grows, adding new shards or rebalancing existing ones requires moving large volumes of data without causing significant downtime. Poorly planned resharding can degrade performance, corrupt data, or take an application offline for extended periods. [[Consistent hashing]] algorithms help reduce the amount of data that must move during resharding, but cannot eliminate it entirely.

**Loss of atomic operations** across shards is a fundamental limitation. [[ACID]] transactions that span multiple shards are difficult to implement correctly and often come with performance penalties. Many sharded databases relax consistency guarantees or require application-level two-phase commit protocols for cross-shard operations. This means developers must carefully consider which operations truly require atomicity and design their data models and queries accordingly.

**Operational complexity** increases substantially with sharding. Backup and restore operations must coordinate across all shards. Monitoring, indexing, and schema migrations become more complicated. Debugging performance issues requires tracing queries across multiple physical databases. Many organizations introduce [[database proxy]] layers or [[中间件]] to abstract shard routing, but these components add their own failure modes and latency.

## Related

- [[Horizontal Partitioning]] - The broader technique of splitting database rows across partitions
- [[Vertical Partitioning]] - An alternative partitioning strategy splitting by columns
- [[Consistent Hashing]] - A technique used to minimize data movement during resharding
- [[Database Replication]] - A complementary strategy for read scaling and fault tolerance
- [[SQL]] - The query language affected by sharding decisions in relational databases
- [[NoSQL]] - Database categories that commonly incorporate sharding
- [[Distributed Database]] - Systems designed to operate across multiple nodes
- [[CAP Theorem]] - Theoretical trade-offs that underpin sharding design decisions
