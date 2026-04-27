---
title: "Paxos"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, consensus, algorithms, fault-tolerance]
---

# Paxos

## Overview

Paxos is a family of consensus algorithms designed to achieve agreement among a distributed set of processes that may fail or experience network partitions. Developed by Leslie Lamport in 1989 and published in 1998, Paxos is considered the gold standard for solving the consensus problem in distributed systems. It ensures that all non-failed nodes in a distributed system agree on the same value, even when some nodes fail or messages are lost.

Paxos forms the theoretical foundation for many practical distributed systems including Google's Chubby (used internally for lock service), Apache Zookeeper, and various distributed databases. Despite its reputation for complexity, understanding Paxos is essential for building reliable distributed systems.

## Key Concepts

**Consensus Problem**: In a distributed system, consensus requires all correct processes to agree on the same value. This problem is notoriously difficult due to the possibility of node failures, network partitions, and message delays or loss.

**Roles in Paxos**: Paxos defines three roles that nodes can play:
- **Proposer**: Initiates the consensus protocol by proposing a value
- **Acceptor**: Votes on proposed values and stores accepted values
- **Learner**: Learns the agreed-upon value once consensus is reached

A single node can play multiple roles, and in practice, all nodes typically participate as all three roles.

**Quorum**: A majority of acceptors (more than half) must approve a value for it to be accepted. This quorum property ensures that at most one value can be chosen—any two quorums must overlap, so if a quorum accepts value A, no other quorum can accept a different value B.

**Proposal Number (Ballot)**: A unique, monotonically increasing identifier that orders proposals. Higher proposal numbers take precedence and help nodes distinguish between newer and older proposals.

**Phase 1 (Prepare)**: A proposer selects a proposal number n and sends prepare(n) requests to a quorum of acceptors. Acceptors promise not to accept any proposal numbered less than n and share their highest-numbered accepted proposal if any.

**Phase 2 (Accept)**: If the proposer receives responses from a quorum, it sends accept(n, v) requests where v is either its proposed value or the value from the highest-numbered response if any acceptor already accepted a value.

## How It Works

The Paxos algorithm operates in two phases with several rounds:

```
Phase 1: Prepare
Proposer → Prepare(n) → All Acceptors
Acceptor → Promise(n, [previous accept]) → Proposer

Phase 2: Accept
Proposer → Accept(n, v) → All Acceptors  
Acceptor → Accepted(n, v) → All Learners
```

1. A proposer generates a new proposal number n and sends prepare(n) to acceptors
2. Acceptors receiving prepare(n) respond with promise to not accept proposals < n, and may share a previously accepted value
3. The proposer examines responses; if any acceptor already accepted a value, it uses that value (to maintain consistency), otherwise it uses its own
4. Proposer sends accept(n, v) to acceptors
5. Acceptors accept the proposal if n matches their highest promised number
6. Once accepted by a quorum, the value is chosen; learners are notified

```python
# Simplified Paxos implementation concept
class Proposer:
    def __init__(self, node_id, acceptors):
        self.node_id = node_id
        self.acceptors = acceptors
        self.proposal_number = 0
    
    def propose(self, value):
        self.proposal_number += 1
        n = self.proposal_number
        
        # Phase 1: Prepare
        promises = []
        for acceptor in self.acceptors:
            response = acceptor.prepare(n)
            if response.ack:
                promises.append(response)
        
        # Determine value to propose
        if promises:
            # Use highest numbered accepted value if any
            highest = max(p.accepted_number for p in promises if p.has_accepted)
            proposed_value = next(p.accepted_value for p in promises 
                                   if p.accepted_number == highest)
        else:
            proposed_value = value
        
        # Phase 2: Accept
        accepted_count = 0
        for acceptor in self.acceptors:
            if acceptor.accept(n, proposed_value):
                accepted_count += 1
        
        return accepted_count >= len(self.acceptors) // 2 + 1
```

## Practical Applications

**Distributed Databases**: Systems like Google Spanner and CockroachDB use consensus protocols inspired by Paxos for replicating data across nodes.

**Configuration Management**: Services like etcd use Raft (a Paxos variant) to maintain consistent cluster configuration.

**Distributed Locking**: Zookeeper provides distributed coordination services based on Paxos-like guarantees.

**State Machine Replication**: Replicating a deterministic state machine across multiple nodes using consensus to ensure all replicas process the same sequence of commands.

## Examples

Paxos is notoriously difficult to implement correctly. Most production systems use Raft instead, which was designed to be more understandable while providing the same guarantees.

```go
// Example of a simplified Paxos acceptor in Go
type Acceptor struct {
    promisedProposal  int
    acceptedProposal  int
    acceptedValue     interface{}
    mu                sync.Mutex
}

func (a *Acceptor) Prepare(n int) (bool, int, interface{}) {
    a.mu.Lock()
    defer a.mu.Unlock()
    
    if n > a.promisedProposal {
        a.promisedProposal = n
        return true, a.acceptedProposal, a.acceptedValue
    }
    return false, 0, nil
}

func (a *Acceptor) Accept(n int, v interface{}) bool {
    a.mu.Lock()
    defer a.mu.Unlock()
    
    if n >= a.promisedProposal {
        a.acceptedProposal = n
        a.acceptedValue = v
        return true
    }
    return false
}
```

## Related Concepts

- [[Raft]] - An alternative consensus algorithm designed to be more understandable than Paxos
- [[Consensus Algorithms]] - The broader category of algorithms for distributed agreement
- [[Distributed Systems]] - Systems where Paxos and consensus are essential
- [[Fault Tolerance]] - The property that Paxos provides despite node failures
- [[Byzantine Fault Tolerance]] - A more severe fault model than Paxos handles
- [[Zookeeper]] - A practical system implementing Paxos-like guarantees

## Further Reading

- "Paxos Made Simple" by Leslie Lamport (2001)
- "The Part-Time Parliament" by Leslie Lamport (original Paxos paper, 1998)
- "Consensus in the Cloud" - Paxos in modern distributed systems
- [The Paxos Algorithm Explained](https://www.youtube.com/watch?v=PN5M0o0sS3U)

## Personal Notes

While Paxos is theoretically elegant, I find Raft significantly easier to understand and implement. In practice, unless you're building a system from scratch, you'd typically use an established library (etcd's Raft implementation, Zookeeper) rather than rolling your own. Understanding the principles helps when debugging distributed systems issues.
