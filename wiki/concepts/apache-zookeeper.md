---
title: Apache ZooKeeper
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [infrastructure, coordination, distributed-systems, consensus]
sources: []
---

# Apache ZooKeeper

## Overview

Apache ZooKeeper is an open-source centralized service that provides distributed coordination, configuration management, synchronization, and group services for distributed applications. Originally developed at Yahoo! and later donated to the Apache Software Foundation, ZooKeeper has become a fundamental building block for many distributed systems, including [[Kafka]], Hadoop, HBase, and numerous other big data technologies. It solves the notoriously difficult problem of coordinating between multiple processes in a distributed environment by offering a simple, reliable, and high-performance coordination service.

At its core, ZooKeeper maintains a distributed hierarchical namespace (similar to a file system) where applications can store configuration data, status information, locks, and other coordination metadata. This namespace is replicated across multiple servers in a ZooKeeper ensemble, ensuring high availability and fault tolerance. Applications connect to ZooKeeper through a client library and can read, write, and watch for changes in this namespace.

## Key Concepts

**ZooKeeper Ensemble**: A ZooKeeper deployment consists of multiple servers (called an ensemble) that replicate data among themselves using a protocol based on Zab (ZooKeeper Atomic Broadcast). The ensemble elects a leader that processes all write requests, while followers can serve read requests. A quorum (majority) of servers must be available for the ensemble to function correctly.

**ZNodes**: The data entities in ZooKeeper's namespace are called ZNodes. Each ZNode can store a small amount of data (typically up to 1MB) and maintain a version number and timestamps. ZNodes can be marked as ephemeral (automatically deleted when the client session ends) or persistent (manually deleted), and support sequential naming for generating unique identifiers.

**Watches**: Clients can set watches on ZNodes to receive asynchronous notifications when the ZNode's data or children change. This mechanism enables applications to react to configuration changes, lock acquisitions, or leader elections without constant polling.

**Sessions**: Clients establish a session with ZooKeeper when they connect. Sessions are maintained through periodic heartbeats, and if a client fails to communicate within the session timeout, the session is considered expired and all ephemeral nodes associated with that session are deleted.

## How It Works

ZooKeeper's consistency model is designed around sequential consistency and atomic operations. All write requests go through the leader, which assigns a monotonically increasing transaction ID (zxid) to each operation. This total ordering of operations ensures that all servers in the ensemble agree on the same state.

The Zab protocol works in two modes: recovery (when the ensemble starts or the leader fails) and broadcast (normal operation). During broadcast, the leader proposes a value and waits for acknowledgments from a quorum of followers before committing the change. This is similar to a two-phase commit but optimized for the leader-heavy workload typical of coordination tasks.

For reads, followers can serve data from their local replica, which is guaranteed to be at least as recent as the last acknowledged state. However, for operations that require strong consistency guarantees (such as checking a lock before proceeding), clients can request a sync operation to bring the follower up to date with the leader.

## Practical Applications

**Service Discovery**: Applications register themselves in ZooKeeper as ephemeral nodes. Other services can discover them by watching for changes, enabling dynamic service discovery without a separate discovery service.

**Configuration Management**: Centralized configuration stored in ZooKeeper can be watched by all application instances. When configuration changes, all watching instances receive notifications and can reload their settings without restart.

**Distributed Locks**: Using sequential ephemeral ZNodes, applications can implement distributed mutual exclusion locks. The lock holder is the ZNode with the lowest sequence number, and other clients watch the next-lower ZNode to detect when they can acquire the lock.

**Leader Election**: Applications can use ZooKeeper to elect a leader among competing instances. The leader is typically the ZNode with the lowest sequence number among candidate nodes, ensuring exactly one leader at any time.

**Barrier Synchronization**: ZooKeeper can coordinate distributed barriers by creating a barrier ZNode and having processes enter/exit by creating or deleting their marker ZNodes under the barrier.

## Examples

A simple ZooKeeper-based configuration management setup in Python using the `kazoo` client:

```python
from kazoo.client import KazooClient

zk = KazooClient(hosts='zoo1:2181,zoo2:2181,zoo3:2181')
zk.start()

# Store configuration
zk.set('/config/app/database_url', b'postgresql://localhost:5432/mydb')

# Watch for configuration changes
@zk.DataWatch('/config/app/database_url')
def watch_config(data, stat):
    print(f'Config changed to: {data.decode()}')

# Use ephemeral node for service registration
zk.create('/services/myapp/instance-001', b'running', ephemeral=True)

# Distributed lock acquisition
lock = zk.Lock('/locks/myresource', 'my-process-id')
with lock:  # Blocks until lock is acquired
    print('Lock acquired, performing exclusive operation')
    # ... critical section ...

zk.stop()
```

A Java example for leader election using Apache Curator:

```java
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.leader.LeaderLatch;
import org.apache.curator.retry.ExponentialBackoffRetry;

CuratorFramework client = CuratorFrameworkFactory.newClient(
    "zoo1:2181,zoo2:2181,zoo3:2181",
    new ExponentialBackoffRetry(1000, 3)
);
client.start();

LeaderLatch latch = new LeaderLatch(client, "/leader-election", "my-instance-id");
latch.start();

latch.await();  // Blocks until this instance becomes leader
System.out.println("I am the leader!");

// ... do leader work ...

latch.close();
client.close();
```

## Related Concepts

- [[Kafka]] — ZooKeeper is used by Kafka for broker coordination and controller election (though Kafka is moving away from ZooKeeper in newer versions)
- [[distributed-systems]] — The broader field of systems that span multiple machines
- [[consensus-algorithms]] — Algorithms like Raft and Paxos that ZooKeeper's Zab protocol is related to
- [[service-discovery]] — The pattern of dynamically locating services in a distributed system
- [[airbyte]] — A data integration tool that can use ZooKeeper for distributed coordination

## Further Reading

- [Apache ZooKeeper Official Documentation](https://zookeeper.apache.org/doc/current/)
- [ZooKeeper: Wait-free coordination for Internet-scale systems](https://www.usenix.org/legacy/events/atc10/tech/full_papers/Hunt.pdf) — Original ZooKeeper paper
- [Apache Curator](https://curator.apache.org/) — High-level recipes built on top of ZooKeeper
- [Zab Protocol Explained](https://blog.twitter.com/engineering/en_us/a/2014/twitter-tracing-servicefoobar.html) — Twitter's analysis of ZooKeeper's atomic broadcast protocol

## Personal Notes

ZooKeeper is one of those tools that feels complex at first but becomes indispensable once you understand its model. The key insight is thinking of it as a notification system first, and a data store second — most of the power comes from watches and ephemeral nodes, not from storing large amounts of data. When designing systems that use ZooKeeper, it's important to keep the data small and focused on coordination, offloading application data elsewhere.
