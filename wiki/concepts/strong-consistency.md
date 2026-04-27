---
title: "Strong Consistency"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, consistency, databases, CAP-theorem]
---

# Strong Consistency

## Overview

Strong consistency is a consistency model in distributed systems that guarantees all nodes in a cluster see the exact same data at the same time. Once a write operation is acknowledged, all subsequent read operations must return that write's result or a newer value. This stands in contrast to eventual consistency, where reads may return stale data temporarily before the system converges to the latest state.

In the [[CAP theorem]] framework, strong consistency is the C (Consistency) guarantee that systems make when they choose CP (Consistency + Partition Tolerance) over AP (Availability + Partition Tolerance). Systems like [[etcd]], [[ZooKeeper]], and [[Google Spanner]] provide strong consistency guarantees, making them suitable for coordination tasks, distributed locks, and leader election.

## Key Concepts

**Linearizability** is the gold standard for strong consistency. A system is linearizable if every operation appears to happen atomically at some point between the operation's invocation and its response, and these points are totally ordered. This means reads and writes appear to happen in a single, instantaneous moment, even across distributed nodes. Linearizability implies strong consistency but is a stricter formal guarantee.

**Sequential Consistency** is slightly weaker than linearizability. It guarantees that all nodes see operations in the same order, but that order doesn't need to correspond to real time. If write A completes before write B starts in real time, A must appear before B in all nodes' views—but the exact timing of when each node observed the change can vary.

**Fencing Tokens** are used in distributed locks to prevent split-brain scenarios. When a client acquires a lock, it receives a monotonically increasing token. Any write operation protected by the lock must include the current token. The storage system rejects operations with stale tokens, preventing clients from accidentally overwriting data they didn't know had been written by another client.

## How It Works

Strong consistency typically relies on consensus algorithms like [[Raft]] or [[Paxos]]. In a Raft-based system, a leader node receives all writes and replicates them to follower nodes through a quorum. A write is only considered committed once a majority of nodes (quorum) have persisted it. Reads can be routed to the leader or also require quorum confirmation, depending on the implementation.

The quorum requirement is what provides the consistency guarantee. With n nodes, you need floor(n/2)+1 nodes to agree on each operation. This means any two quorums must overlap by at least one node, ensuring that any node that missed a write will discover it through the overlap and redirect the read.

For [[distributed transactions]], strong consistency often involves two-phase commit (2PC) or three-phase commit (3PC) protocols. These coordinate commit across multiple database partitions, ensuring atomicity at the transaction level.

## Practical Applications

Strong consistency is essential when incorrect data could cause serious problems:

- **Financial transactions**: Bank transfers, stock trades, and payment processing require all parties to see the same account balances simultaneously.
- **Distributed locks**: Service discovery with [[etcd]], leader election in [[Kafka]] brokers, and critical section coordination.
- **Inventory management**: Prevents overselling when multiple services read and modify inventory counts concurrently.
- **Configuration stores**: When services must agree on the same configuration version before proceeding.

## Examples

Using etcd for distributed locking with fencing tokens:

```go
// Acquire a lock with fencing token
resp, err := client.Txn(ctx).If(
    clientv3.Compare(clientv3.Version(key), "=", 0),
).Then(
    clientv3.OpPut(key, value, clientv3.WithLease(leaseID)),
).Commit()

// resp.Header.Revision is your fencing token
token := resp.Header.Revision

// All subsequent writes must include the token
_, err = client.Put(ctx, resourceKey, value, clientv3.WithPrevKV())
```

Using etcd for strongly consistent configuration:

```go
// Watch for changes - guaranteed to see all changes in order
rch := client.Watch(ctx, "config/app/", clientv3.WithPrefix())
for wresp := range rch {
    for _, ev := range wresp.Events {
        fmt.Printf("%s %s: %s\n", ev.Type, ev.Kv.Key, ev.Kv.Value)
        // All nodes process config changes in exactly the same order
    }
}
```

## Related Concepts

- [[Eventual Consistency]] - Weaker consistency model where reads may temporarily return stale data
- [[CAP Theorem]] - Theoretical framework explaining the tradeoffs between consistency, availability, and partition tolerance
- [[Raft]] - Consensus algorithm commonly used to achieve strong consistency
- [[Paxos]] - Alternative consensus algorithm for achieving strong consistency
- [[Distributed Transactions]] - Protocols for maintaining consistency across multiple databases
- [[Linearizability]] - Formal guarantee that underlies strong consistency

## Further Reading

- ["Consistency in Distributed Systems"](https://notes.eatonphil.com/consistency-in-distributed-systems.html) - Practical guide to consistency models
- [Raft Paper](https://raft.github.io/raft.pdf) - Inconsistency in Distributed Systems
- [Spanner Paper](https://research.google.com/archive/spanner-osdi2012.pdf) - Google's globally distributed database with strong consistency

## Personal Notes

Strong consistency comes at a performance cost. The quorum requirement means writes take longer (need majority agreement) and the system may become unavailable if a majority cannot be reached during a partition. The key insight from the CAP theorem is that during a partition, you must choose: sacrifice consistency for availability, or become unavailable. Strongly consistent systems (CP) choose the latter.

In practice, many systems use strong consistency only where absolutely necessary (locks, config, coordination) and eventual consistency for data that can tolerate temporary staleness (user profiles, analytics, caching layers). Understanding which operations require which consistency level is crucial for building correct, performant distributed systems.
