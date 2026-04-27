---
title: "ZooKeeper"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, coordination, apache, consensus]
---

# ZooKeeper

Apache ZooKeeper is an open-source distributed coordination service that enables highly reliable distributed systems by providing a centralized service for maintaining configuration information, naming conventions, distributed synchronization, and group services. Originally developed at Yahoo! and later donated to the Apache Software Foundation, ZooKeeper implements the Paxos consensus algorithm (specifically ZAB, ZooKeeper Atomic Broadcast) to provide strong consistency guarantees across a distributed ensemble of servers. Understanding ZooKeeper is essential for developers building distributed applications, distributed databases, and microservices architectures because it solves the challenging problem of coordinating multiple processes in distributed environments where failures are normal rather than exceptional.

## Overview

Distributed systems face fundamental challenges that don't exist in single-machine environments: processes can crash, networks can partition, and messages can be delayed or lost. Coordinating actions across these unreliable components requires a trusted intermediary that all processes can consult. ZooKeeper fills this role by providing a distributed data store with strong consistency guarantees, allowing applications to coordinate through a shared namespace of data nodes organized hierarchically like a file system.

ZooKeeper's data model is elegant in its simplicity: a tree of data nodes called znodes, where each znode can contain data and have child znodes. Applications use this namespace for diverse purposes—storing configuration parameters, electing leaders, detecting failure, managing distributed locks, and tracking system state. The consistency guarantee that reads return the most recent write ensures that all clients see the same view of coordinated state.

The service is designed for reliability and scalability. A ZooKeeper ensemble typically consists of an odd number of servers (3, 5, or 7 for production) that replicate data among themselves using the ZAB protocol. As long as a majority of servers (a quorum) are available and can communicate with each other, the service remains operational even if some servers fail. This fault tolerance makes ZooKeeper suitable for coordinating critical infrastructure components.

## Key Concepts

Understanding ZooKeeper requires mastering several core concepts that define how the service operates and how applications interact with it.

**Znodes** are the fundamental data units in ZooKeeper's hierarchical namespace. Each znode has a path (like "/config/cluster/node1"), can contain optional data (up to 1MB by default), maintains metadata including version numbers and timestamps, and can be either ephemeral (temporary, deleted when the creating session ends) or persistent (survives session termination). Ephemeral znodes are particularly useful for detecting client presence and failure.

**Watches** provide an event notification mechanism that eliminates the need for polling. Clients can set watches on znodes, and ZooKeeper notifies them when the watched znode changes (data modified, child added/deleted, or node deleted). Watches fire exactly once for each change, requiring clients to reset watches to receive subsequent notifications.

**Sessions** represent a client's connection to the ZooKeeper ensemble. Clients establish sessions by connecting to any server in the ensemble and maintain sessions through periodic heartbeats. If a client fails to send heartbeats within the session timeout, the session is considered expired and all ephemeral nodes created by that session are automatically deleted.

**ZAB (ZooKeeper Atomic Broadcast)** is the protocol ZooKeeper uses to replicate state among servers and establish consensus. ZAB ensures that updates are delivered to all servers in the same order, that crashed servers recover state correctly when they restart, and that the service continues operating as long as a majority of servers remain available.

## How It Works

ZooKeeper ensembles operate through a leader-based architecture where one server is elected as the leader and others are followers. The leader receives all write requests, transforms them into transactions, and broadcasts them to followers using ZAB. Followers apply transactions after acknowledging them, and writes are considered committed once a quorum of servers (typically a majority) has acknowledged the proposal.

Read requests can be served by any server in the ensemble, though followers may return slightly stale data if they haven't yet received the latest committed updates. For applications requiring strict consistency, sync() can be called before reading to ensure the follower has caught up with the leader's state.

Leader election occurs when a leader fails or when the ensemble first starts. Servers propose themselves as leaders, exchange proposals, and eventually agree on a leader based onzxid (ZooKeeper transaction ID)—the server that has processed the most transactions becomes the leader. This ensures the new leader has the most up-to-date state.

```java
// Example: Java client interacting with ZooKeeper
import org.apache.zookeeper.*;
import org.apache.zookeeper.data.Stat;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.CountDownLatch;

public class ZooKeeperExample implements Watcher {
    private static final String ZOOKEEPER_ADDRESS = "localhost:2181";
    private static final int SESSION_TIMEOUT = 3000;
    private static final String CONFIG_PATH = "/config/service";
    private static final String LOCK_PATH = "/locks/distributed-lock";
    
    private ZooKeeper zooKeeper;
    private CountDownLatch connectionLatch = new CountDownLatch(1);
    
    public void connect() throws IOException {
        zooKeeper = new ZooKeeper(ZOOKEEPER_ADDRESS, SESSION_TIMEOUT, this);
        connectionLatch.await();
        System.out.println("Connected to ZooKeeper");
    }
    
    @Override
    public void process(WatchedEvent event) {
        if (event.getType() == Event.EventType.None) {
            if (event.getState() == Event.KeeperState.SyncConnected) {
                connectionLatch.countDown();
            }
        }
    }
    
    // Write configuration
    public void writeConfig(String configData) throws KeeperException, InterruptedException {
        Stat stat = zooKeeper.exists(CONFIG_PATH, false);
        if (stat == null) {
            zooKeeper.create(CONFIG_PATH, configData.getBytes(), 
                ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        } else {
            zooKeeper.setData(CONFIG_PATH, configData.getBytes(), stat.getVersion());
        }
    }
    
    // Read configuration with watch
    public String readConfig() throws KeeperException, InterruptedException {
        byte[] data = zooKeeper.getData(CONFIG_PATH, this, new Stat());
        return new String(data);
    }
    
    // Acquire distributed lock using ephemeral sequential node
    public String acquireLock() throws KeeperException, InterruptedException {
        String lockNode = zooKeeper.create(LOCK_PATH + "/lock-", 
            new byte[0], 
            ZooDefs.Ids.OPEN_ACL_UNSAFE, 
            CreateMode.EPHEMERAL_SEQUENTIAL);
        System.out.println("Created lock node: " + lockNode);
        return lockNode;
    }
    
    // Check if this is the smallest sequential number (lock acquisition)
    public boolean checkAndAcquireLock(String lockNode) throws KeeperException, InterruptedException {
        String parent = lockNode.substring(0, lockNode.lastIndexOf('/'));
        List<String> children = zooKeeper.getChildren(parent, false);
        children.sort(String::compareTo);
        
        String smallest = children.get(0);
        return lockNode.endsWith(smallest);
    }
    
    public void close() throws InterruptedException {
        zooKeeper.close();
    }
}
```

## Practical Applications

ZooKeeper's coordination services power critical infrastructure in distributed systems. **Service Discovery** uses ZooKeeper to maintain a registry of available service instances. As services start and stop, they register or deregister themselves, and clients can watch for changes to discover currently available instances. This pattern enables dynamic, resilient microservice architectures.

**Distributed Locks** implement mutual exclusion across processes running on different machines. Using ephemeral sequential znodes, processes can implement lock acquisition that works correctly even when processes fail—the lock is automatically released when the creating process's session ends, preventing locks from being held indefinitely by crashed processes.

**Configuration Management** centralizes configuration that needs to be consistent across multiple services or machines. When configuration changes in ZooKeeper, watches notify all affected processes, providing a reliable mechanism for dynamic reconfiguration without restarting services.

**Leader Election** designates one process among many to perform coordination tasks. Processes compete to create the same ephemeral znode, and whichever succeeds becomes the leader. If the leader fails, its session ends and the znode disappears, triggering re-election among remaining processes.

## Examples

A practical ZooKeeper example is coordinating a distributed database replica set. The primary database registers as the leader in ZooKeeper, and secondaries watch for changes in leadership. If the primary fails, ZooKeeper detects the session expiration and notifies secondaries, which compete to become the new primary. Only one succeeds, and the application continues with minimal interruption.

Another example involves managing distributed task assignment. A coordinator creates parent znodes representing task queues, and workers claim tasks by atomically renaming tasks to indicate assignment. The atomic operations provided by ZooKeeper (check-and-set through version numbers) ensure tasks are assigned to exactly one worker even when multiple workers attempt to claim simultaneously.

## Related Concepts

- [[Distributed Systems]] - The field ZooKeeper operates within
- [[Consensus Algorithms]] - Including Paxos and Raft that ZooKeeper relates to
- [[Microservices]] - Architecture pattern that uses ZooKeeper for coordination
- [[Apache Kafka]] - Distributed system that uses ZooKeeper for metadata
- [[etcd]] - Alternative coordination service using Raft consensus
- [[Consul]] - Service mesh and coordination tool

## Further Reading

- ZooKeeper Documentation - Official Apache project documentation
- "ZooKeeper: Wait-free coordination for Internet-scale systems" - Original paper describing ZAB
- "Building Microservices" by Sam Newman - Covers ZooKeeper usage patterns

## Personal Notes

ZooKeeper represents a foundational piece of infrastructure that addresses one of the hardest problems in distributed systems—getting independent processes to agree on something when any of them might fail at any time. The elegance of its data model—simple znodes with watches— belies the complexity of maintaining consistency across geographically distributed servers. What strikes me is how ZooKeeper distills years of distributed systems research into a practical, deployable service. Though alternatives like etcd and Consul have gained popularity for newer projects, ZooKeeper remains widely deployed in legacy systems and projects like Kafka that depend on its proven reliability. Understanding ZooKeeper provides a mental model for thinking about distributed coordination that transfers to any coordination technology.
