---
title: "Distributed Database"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [databases, distributed-systems, consistency, scalability, nosql]
---

# Distributed Database

## Overview

A distributed database is a collection of multiple logically related databases interconnected physically and communicating over a network. Unlike centralized databases that reside on a single machine, distributed databases span multiple servers, data centers, or geographic regions, providing horizontal scalability, fault tolerance, and high availability. Data is stored across different nodes, with sophisticated mechanisms ensuring consistency, synchronization, and query transparency across the entire system.

The fundamental challenge in distributed databases stems from the CAP theorem, which states that a distributed system can only guarantee simultaneously two of three properties: Consistency (all nodes see the same data at the same time), Availability (every request receives a response), and Partition Tolerance (the system continues operating despite network failures). Database designers must make explicit trade-offs based on their use case requirements, choosing between strongly consistent systems like [[Google Spanner]] or eventually consistent systems like [[Amazon DynamoDB]].

Modern distributed databases are categorized broadly into NewSQL (relational databases that scale horizontally, like [[CockroachDB]] and [[TiDB]]), NoSQL (non-relational designs optimized for specific access patterns, like [[MongoDB]] and [[Cassandra]]), and multi-model databases that support multiple data models within a single engine.

## Key Concepts

**Sharding** — The practice of horizontally partitioning data across multiple nodes, where each shard contains a subset of total records. Sharding keys are chosen carefully to ensure even data distribution and to minimize cross-shard queries. Poor shard key selection can create hotspots that degrade performance. [[Sharding]] is distinct from [[Vertical Partitioning]], which splits columns rather than rows.

**Replication** — Data is copied to multiple nodes for fault tolerance and read scalability. Replication topologies include single-leader (one primary accepts writes, followers replicate), multi-leader (multiple nodes accept writes, sync bidirectionally), and leaderless (writes read from any node with quorum-based coordination). Replication introduces challenges around consistency, conflict resolution, and handling split-brain scenarios.

**Consensus Protocols** — Distributed databases use consensus algorithms to agree on data state across nodes. [[Paxos]] and [[Raft]] are the dominant protocols. Raft, in particular, has become popular due to its understandable design and is used in systems like [[etcd]] and CockroachDB. These protocols ensure that writes are committed only after a majority of nodes agree.

**ACID in Distributed Contexts** — Traditional ACID properties (Atomicity, Consistency, Isolation, Durability) become more complex across distributed nodes. Distributed transactions require coordination protocols like [[Two-Phase Commit]] or [[Three-Phase Commit]], which introduce latency and can become bottlenecks. Some systems opt for "BASE" properties (Basically Available, Soft state, Eventually consistent) to favor availability.

**Consistent Hashing** — A technique used primarily in leaderless databases to map keys to nodes in a way that minimizes reshuffling when nodes are added or removed. Consistent hashing forms the foundation of [[Amazon DynamoDB]] and [[Cassandra]] token ring architecture.

## How It Works

A distributed database engine typically consists of several layers working together:

```text
┌─────────────────────────────────────────────────────┐
│                 Query Layer                         │
│  (Parsing, Optimization, Query Routing)              │
├─────────────────────────────────────────────────────┤
│                 Transaction Layer                    │
│  (ACID guarantees, Concurrency Control)             │
├─────────────────────────────────────────────────────┤
│                 Replication Layer                    │
│  (Data sync, Conflict Resolution, Failover)         │
├─────────────────────────────────────────────────────┤
│                 Storage Layer                       │
│  (Local storage, Indexing, Compaction)              │
└─────────────────────────────────────────────────────┘
```

When a client submits a query, the query layer parses it and determines which nodes hold relevant data. The transaction layer coordinates commits using consensus when multiple nodes are involved. The replication layer ensures changes propagate to replicas according to the configured consistency level. The storage layer handles local read/write operations, compaction, and indexing.

## Practical Applications

- **Global-scale web applications** — Systems serving users across continents use geo-distributed databases to place data near users, reducing latency while maintaining consistency (e.g., [[Cloudflare D1]], [[PlanetScale]]).
- **Financial systems** — Banking and trading systems require strong consistency and fault tolerance, often using distributed relational databases with synchronous replication.
- **IoT telemetry ingestion** — Time-series data from sensors generates massive write volumes that require horizontal scaling, addressed by wide-column stores like Cassandra or specialized time-series databases.
- **E-commerce platforms** — Product catalogs, inventory, and orders are distributed across shards to handle peak loads during events like Black Friday.
- **Social media feeds** — Systems like Twitter/X and Facebook use eventually consistent distributed databases to serve billions of read requests with minimal latency.

## Examples

**Amazon DynamoDB** — A fully managed NoSQL database using consistent hashing for automatic partitioning. It offers eventually consistent and strongly consistent reads, with a pay-per-request pricing model suitable for unpredictable workloads.

**CockroachDB** — A distributed SQL database inspired by Google Spanner, offering horizontal scaling with full ACID transactions. It uses the Raft consensus protocol and supports geo-partitioning for compliance with data residency requirements.

**Apache Cassandra** — A wide-column store optimized for write-heavy workloads, using a peer-to-peer architecture with no single point of failure. It uses consistent hashing and supports tunable consistency levels.

```sql
-- Example: Query routing in a sharded PostgreSQL setup
-- Applications typically use a shard key to route queries
SELECT * FROM orders 
WHERE user_id = 'user_12345' 
AND created_at > '2026-01-01';
-- The query router directs this to the shard containing user_12345
```

## Related Concepts

- [[Sharding]] — Horizontal partitioning of data across nodes
- [[Replication]] — Copying data across nodes for redundancy
- [[CAP Theorem]] — Fundamental trade-offs in distributed systems
- [[NoSQL]] — Non-relational database models suited for distributed architectures
- [[NewSQL]] — Horizontally scalable relational databases
- [[ACID Transactions]] — Atomicity, consistency, isolation, durability guarantees
- [[Consensus Protocols]] — Paxos and Raft for agreement in distributed systems
- [[Vertical Partitioning]] — Splitting columns within a table (contrast with sharding)

## Further Reading

- "Designing Data-Intensive Applications" by Martin Kleppmann — The definitive guide to distributed databases and modern data systems.
- "The Chubby Lock Service for Loosely-Coupled Distributed Systems" — Google's paper on consensus-based locking.
- "Dynamo: Amazon's Highly Available Key-value Store" — Foundation for many modern eventually-consistent databases.
- [[Google Spanner]] — Google's globally distributed, strongly consistent relational database.

## Personal Notes

Distributed databases are one of the most nuanced areas in systems engineering. The CAP theorem isn't a binary choice—most real systems tune consistency levels per operation rather than picking a side wholesale. I've found that starting with a well-understood consistency model (like eventual consistency with quorum reads) and adding stronger guarantees only where needed avoids over-engineering. The operational complexity of distributed databases is often underestimated—monitoring, failover, and debugging across nodes is significantly harder than a single-node database.
