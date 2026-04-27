---
title: "CAP Theorem"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cap-theorem, distributed-systems, consistency, availability, partition-tolerance]
---

# CAP Theorem

## Overview

The CAP Theorem, also known as Brewer's Theorem, is a fundamental principle in distributed systems theory that was formulated by computer scientist Eric Brewer in 2000 and later proven formally by Seth Gilbert and Nancy Lynch in 2002. The theorem describes a fundamental trade-off that architects and engineers face when designing distributed data storage systems. It states that a distributed system can only simultaneously guarantee two out of three desirable properties: Consistency, Availability, and Partition Tolerance. Understanding this theorem is essential for anyone building or maintaining distributed databases, microservices architectures, or any system that replicates data across multiple nodes.

The theorem arises from the reality that network partitions—situations where communication between nodes is disrupted or delayed—are not a matter of "if" but "when" in real-world distributed systems. Networks will experience failures, routers will drop packets, and data centers will lose connectivity. Because partition tolerance is effectively mandatory for any distributed system that spans multiple network segments or data centers, the real choice architects face is between prioritizing consistency or availability when a partition occurs.

## The Three Properties

**Consistency** in the CAP sense means that every read operation receives the most recent write or an error. When a client queries any node in the system, they should see the same data at the same time, reflecting all completed writes. This is not the same as strong consistency in traditional database transactions, but rather linearizability—a formal guarantee that operations appear to happen atomically in some sequential order. Systems that prioritize consistency, such as traditional relational databases using two-phase commit, ensure that your data is always in a known, coherent state, but may become unavailable during network disruptions.

**Availability** means that every request received by a functioning node must result in a response, even if that response may not reflect the most recent write. Available systems prioritize keeping the lights on—ensuring that users can always read and write data, even during partial network failures. The trade-off is that different nodes might temporarily hold conflicting versions of data while the system heals. Many NoSQL databases like Cassandra and Dynamo were designed with availability as a primary goal, accepting eventual consistency in exchange for always-on responsiveness.

**Partition Tolerance** refers to the system's ability to continue operating when network partitions occur—meaning nodes can still communicate with their local storage, even if they cannot reach other nodes across the cluster. A partition-tolerant system can split into two or more isolated groups, each operating independently, and then reconstitute itself when connectivity is restored. Without partition tolerance, any network failure would bring down the entire system, making it impractical for geo-distributed deployments.

## Implications

The implications of CAP Theorem for system design are profound and influence architectural decisions across the industry. When choosing between CP (Consistency + Partition Tolerance) and AP (Availability + Partition Tolerance) systems, architects must understand their use case's tolerance for stale data versus downtime.

CP systems like [[HBase]], [[MongoDB]] in replica set configurations, and [[ZooKeeper]] sacrifice availability to guarantee consistency. These systems are ideal for applications where data accuracy is critical—financial transactions, inventory management, or any scenario where reading stale data could lead to incorrect decisions. When a partition occurs, these systems will typically become unavailable rather than serve inconsistent data, which is often the correct behavior for banking or reservation systems.

AP systems like [[Cassandra]], [[DynamoDB]], and [[Couchbase]] sacrifice strong consistency to guarantee availability. These systems are designed for scenarios where availability and low latency are paramount—social media feeds, product catalogs, or user-facing applications where temporary inconsistency is acceptable. When partitions occur, these systems continue to accept reads and writes, merging conflicts later through eventual consistency mechanisms like conflict-free replicated data types (CRDTs) or last-write-wins semantics.

It's worth noting that the consistency vs. availability choice is not binary at all times. Many modern databases offer tunable consistency levels, allowing you to choose how many nodes must acknowledge a read or write operation. This allows applications to adjust their consistency guarantees based on the specific operation, striking a nuanced balance between correctness and performance.

The CAP Theorem also paved the way for the [[PACELC]] model, which extends the discussion beyond partition scenarios to consider the latency-consistency trade-offs that exist even in systems without partitions. Additionally, understanding CAP is foundational to grasping concepts like [[Eventual Consistency]], [[Strong Consistency]], and the broader field of [[Distributed Consensus Algorithms]] such as [[Raft]] and [[Paxos]].

## Related

- [[Distributed Systems]] - The broader field of study concerning multiple cooperating computers
- [[Eventual Consistency]] - A consistency model where updates propagate to all replicas eventually
- [[Strong Consistency]] - Consistency models that guarantee immediate visibility of all writes
- [[PACELC]] - An extension of CAP that also considers latency trade-offs
- [[Raft]] - A consensus algorithm for managing replicated logs
- [[Paxos]] - Another widely-used distributed consensus algorithm
- [[HBase]] - A CP distributed database built on Hadoop
- [[Cassandra]] - An AP distributed database with tunable consistency
- [[DynamoDB]] - Amazon's globally distributed AP database service
- [[ZooKeeper]] - A CP coordination service for distributed applications
