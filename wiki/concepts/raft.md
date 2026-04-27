---
title: "Raft"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, consensus, fault-tolerance, replication]
---

# Raft

## Overview

Raft is a consensus algorithm designed for managing replicated state machines in distributed systems. It was developed by Diego Ongaro and John Ousterhout at Stanford University as a more understandable alternative to the complex Paxos algorithm. Raft achieves distributed consensus by electing a leader among a cluster of nodes, then delegating all management responsibilities to that leader. This leader-based approach simplifies the reasoning about system behavior and makes Raft particularly well-suited for building reliable distributed databases, coordination services, and coordination primitives like distributed locks.

The algorithm decomposes consensus into three relatively independent sub-problems: leader election, log replication, and safety. By separating these concerns, Raft provides a clean mechanism for maintaining consistency across a cluster even when nodes fail, networks partition, or messages are lost. Raft has been widely adopted in production systems and serves as the consensus layer for projects like etcd, CockroachDB, and TiKV.

## Key Concepts

**Replicated Log**: All changes to the system are submitted as entries to a shared log. Each node maintains its own copy of this log, and the consensus algorithm ensures that all healthy nodes agree on the exact sequence of entries.

**Leader Election**: Raft uses a randomized election timeout mechanism to elect a leader. When a follower doesn't hear from a leader within its timeout period, it becomes a candidate and requests votes from other nodes. The candidate with the most votes wins the election. This randomized approach prevents split-vote infinite loops.

**Terms**: Time in Raft is divided into numbered terms. Each term begins with an election, and if a leader is elected, it serves through the term. Terms act as a logical clock and help nodes detect stale information.

**Log Replication**: Once a leader is elected, it accepts client requests, appends them to its log, and replicates them to followers via AppendEntries RPCs. An entry is considered committed once a majority of nodes have written it to their logs.

## How It Works

The Raft cluster operates with a strong leader paradigm. All client requests route through the leader, which orchestrates replication to followers. When a client submits a command, the leader:

1. Appends the command to its local log
2. Issues AppendEntries RPCs in parallel to all followers
3. Waits for acknowledgment from a majority of nodes
4. Applies the command to its state machine
5. Returns the result to the client

If followers crash or network latency increases, the leader continues with a smaller majority, ensuring liveness. However, it cannot commit entries from previous terms without also committing entries from the current term—a nuance that prevents a class of subtle consistency violations.

Leader election follows a heartbeat-based approach. The leader sends periodic heartbeats (empty AppendEntries RPCs) to all followers. If a follower misses several heartbeats, it transitions to candidate state and begins an election. Election timeouts are randomized within a range (e.g., 150-300ms) to probabilistically avoid simultaneous candidates.

```go
// Simplified Raft leader election pseudocode
func (r *Raft) runElectionTimer() {
    timeout := randomTimeout(150, 300) * time.Millisecond
    for {
        select {
        case <-time.After(timeout):
            if r.state != Leader {
                r.startElection()
            }
        case <-r.resetCh:
            timeout = randomTimeout(150, 300) * time.Millisecond
        }
    }
}

func (r *Raft) startElection() {
    r.state = Candidate
    r.currentTerm++
    r.votedFor = r.id
    votes := 1 // vote for self
    
    for peer := range r.peers {
        go func(p string) {
            if r.sendRequestVote(p) {
                votes++
                if votes > len(r.peers)/2 {
                    r.becomeLeader()
                }
            }
        }(peer)
    }
}
```

## Practical Applications

Raft's practical applications are extensive in modern infrastructure:

**etcd**: The primary storage backend for Kubernetes, etcd uses Raft to maintain a consistent, highly-available key-value store for cluster state, pod specifications, and configuration data.

**CockroachDB**: A distributed SQL database that uses Raft for replicating ranges of data across nodes, ensuring consistency and automatic recovery from node failures.

**TiKV**: The storage engine behind PingCAP's TiDB, built on Raft for distributed data replication and horizontal scaling.

**Consul**: HashiCorp's service networking solution uses Raft for bootstrapping the consensus protocol among Consul servers.

## Examples

A minimal Raft cluster consists of 3 nodes, tolerating 1 failure. For 5 nodes, you can tolerate 2 simultaneous failures. The trade-off is that larger clusters have higher replication overhead but greater fault tolerance.

```bash
# Example: Starting a 3-node etcd cluster with Raft
# Node 1
etcd --name=node1 --listen-peer-urls=http://10.0.0.1:2380 \
     --listen-client-urls=http://10.0.0.1:2379 \
     --initial-cluster-state=new

# Node 2  
etcd --name=node2 --listen-peer-urls=http://10.0.0.2:2380 \
     --listen-client-urls=http://10.0.0.2:2379 \
     --initial-cluster="node1=http://10.0.0.1:2380,node2=http://10.0.0.2:2380"
```

## Related Concepts

- [[Paxos]] - An older consensus algorithm that Raft was designed to replace
- [[Distributed Systems]] - The broader field Raft operates within
- [[Consensus Algorithms]] - The category of algorithms Raft belongs to
- [[Leader Election]] - A sub-problem Raft solves
- [[etcd]] - A production Raft implementation
- [[Replicated Log]] - The data structure Raft manages

## Further Reading

- "In Search of an Understandable Consensus Algorithm" (Ongaro & Ousterhout, 2014) - The original Raft paper
- The Raft website at https://raft.github.io/ contains visualizations and the specification
- "Consensus: Bridging Theory and Practice" (Ongaro's PhD thesis) - Comprehensive Raft reference

## Personal Notes

Raft's greatest strength is its understandability. While Paxos can take months to truly internalize, Raft's clear separation of concerns allows new distributed systems engineers to reason about the protocol quickly. The reference paper explicitly prioritized understandability as a design goal, and it shows. When implementing Raft, pay close attention to election safety and the "don't commit entries from previous terms" rule—these subtle points are the source of most implementation bugs.
