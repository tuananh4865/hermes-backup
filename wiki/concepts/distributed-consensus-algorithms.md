---
title: "Distributed Consensus Algorithms"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, consensus, fault-tolerance, blockchain, replication]
---

# Distributed Consensus Algorithms

> This page was auto-created by [[self-healing-wiki]] to fill a broken link.
> Please expand with real content.

## Overview

Distributed consensus algorithms enable a network of unreliable nodes to agree on a single value or sequence of values, despite failures and network partitions. In distributed systems, consensus is fundamental to achieving reliability and consistency—without it, different nodes might have conflicting views of the system's state, leading to data corruption and unpredictable behavior.

The field was revolutionized by the FLP impossibility result (Fischer, Lynch, Paterson, 1985), which proved that no deterministic consensus algorithm can guarantee termination in an asynchronous system if even a single node can fail. This theoretical finding drove practical research toward algorithms that either relax the problem (partially synchronous models), accept probabilistic termination, or make assumptions about failure detection.

## Key Concepts

**Byzantine Fault Tolerance (BFT)** extends crash fault tolerance to handle arbitrary node behavior—including nodes that behave maliciously or send contradictory information. Named after the Byzantine Generals Problem, BFT algorithms are essential in blockchain and adversarial environments.

**Paxos** is the canonical consensus algorithm, developed by Leslie Lamport. It achieves consensus through a two-phase process involving proposers and acceptors. Paxos is notoriously difficult to understand and implement correctly, but it provides strong consistency guarantees.

**Raft** was designed as a more understandable alternative to Paxos. It separates concerns into leader election, log replication, and safety. Raft's clarity has made it the algorithm of choice for many production systems like etcd and CockroachDB.

**Multi-Paxos** optimizes Paxos for the common case where a single leader processes many commands. Rather than running full two-phase consensus for each entry, a stable leader can append entries with simplified logic.

**ViewStamped Replication (VSR)** is another consensus algorithm developed independently of Paxos. It's used in production systems like Hyperledger and provides similar guarantees with different implementation characteristics.

## How It Works

The typical consensus algorithm operates in rounds or views:

1. **Leader Election**: Nodes periodically attempt to become leader using randomized or round-robin selection
2. **Proposal**: The leader proposes a value to all nodes
3. **Voting**: Nodes vote on the proposal, ensuring they only vote for values that don't conflict with their history
4. **Commit**: Once a quorum agrees, the value is committed and will not be changed

Paxos uses two phases:

```python
# Simplified Paxos proposer logic
class Proposer:
    def __init__(self, node_id, num_acceptors):
        self.node_id = node_id
        self.num_acceptors = num_acceptors
        self.quorum = num_acceptors // 2 + 1
    
    def propose(self, value):
        # Phase 1: Prepare
        proposal_id = generate_unique_id(self.node_id)
        promises = []
        
        for acceptor in acceptors:
            response = acceptor.prepare(proposal_id)
            if response.accepted_proposal_id > highest_seen:
                highest_seen = response.accepted_proposal_id
                accepted_value = response.accepted_value
            promises.append(response)
        
        if len(promises) >= self.quorum:
            # Phase 2: Accept
            value_to_propose = accepted_value or value
            accepts = 0
            
            for acceptor in acceptors:
                accepted = acceptor.accept(proposal_id, value_to_propose)
                if accepted:
                    accepts += 1
            
            return accepts >= self.quorum
```

Raft's leader election is more structured:

```python
# Raft election timeout simulation
import random

class RaftNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.current_term = 0
        self.voted_for = None
        self.state = 'follower'
        self.election_timeout = random.randint(150, 300)  # ms
        
    def check_election_timeout(self, elapsed_ms):
        if elapsed_ms >= self.election_timeout:
            self.start_election()
            
    def start_election(self):
        self.state = 'candidate'
        self.current_term += 1
        self.voted_for = self.node_id
        votes = 1
        
        for peer in self.peers:
            vote_granted = peer.request_vote(
                term=self.current_term,
                candidate_id=self.node_id,
                last_log_index=self.last_log_index,
                last_log_term=self.last_log_term
            )
            if vote_granted:
                votes += 1
        
        if votes > len(self.peers) // 2:
            self.become_leader()
```

## Practical Applications

**Distributed Databases** like etcd, CockroachDB, and Spanner use consensus algorithms to replicate data across nodes with strong consistency. Writes are proposed to the leader, replicated via consensus, then committed.

**Blockchain and Cryptocurrencies** rely on consensus to agree on the canonical chain of blocks. Proof-of-work (Bitcoin), proof-of-stake (Ethereum 2.0), and BFT variants (Hyperledger) all represent different approaches to achieving consensus in open, adversarial settings.

**Service Discovery** systems like Consul use consensus to maintain a consistent view of available services. This ensures that when a service fails, all nodes eventually agree on its unavailability.

**Coordination Services** including Apache Zookeeper implement consensus to provide distributed locking and configuration management. These are critical infrastructure for coordinating distributed applications.

## Related Concepts

- [[self-healing-wiki]]
- [[Paxos]] - The foundational consensus algorithm
- [[Raft]] - More understandable alternative to Paxos
- [[Byzantine Fault Tolerance]] - Handling malicious or arbitrary failures
- [[Distributed Systems]] - The broader field of study
- [[FLP Impossibility]] - Theoretical limitation on consensus in async systems
- [[Blockchain]] - Practical application of consensus in cryptocurrency

## Further Reading

- "Paxos Made Simple" by Leslie Lamport
- "In Search of an Understandable Consensus Algorithm" (Raft paper) by Ongaro and Ousterhout
- "The Byzantine Generals Problem" by Lamport, Shostak, Pease
- etcd Internals — Practical Raft implementation study

## Personal Notes

Understanding Raft before Paxos was the right path for me—Paxos's original paper is brilliantly written but assumes years of distributed systems experience. The key insight that helped me: consensus algorithms are really about maintaining replicated logs, not just agreeing on values. Once you see it as "how do we make sure every node has identical log entries in the same order," the two-phase structure makes intuitive sense.
