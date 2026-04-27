---
title: "Consensus Algorithms"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [consensus-algorithms, distributed-systems, fault-tolerance, raft, paxos]
---

# Consensus Algorithms

## Overview

Consensus algorithms are protocols that enable distributed nodes to agree on a value or sequence of values despite the failure of some nodes and the unreliability of network communication. They represent one of the central challenges in distributed systems—the FLP impossibility result proved in 1985 that deterministic consensus is impossible in an asynchronous distributed system if even a single node can fail. Yet consensus algorithms work around this limitation through various mechanisms: randomized timing, failure detectors, or by relaxing the exact requirements for consensus.

In practical terms, consensus algorithms allow a group of distributed nodes to make decisions as a single logical entity. When you have five database replicas and a write comes in, consensus algorithms ensure all five agree on whether to commit the write and in what order relative to other writes. This agreement is essential for maintaining consistency—without consensus, different replicas might diverge, leading to split-brain scenarios where different nodes have different views of the data.

Modern distributed systems rely heavily on consensus algorithms for critical infrastructure. Coordination services like [[ZooKeeper]] and [[etcd]] use consensus to provide distributed locks, leader election, and configuration management. Distributed databases use consensus to replicate writes. Message queues use consensus to ensure durability and ordering. Understanding these algorithms is fundamental to building reliable distributed systems.

## Key Concepts

**Safety and Liveness**: Consensus algorithms must satisfy two properties. Safety (or consistency) means that all nodes that decide on a value agree on the same value—if one node decides X, no other node decides Y. Liveness means that eventually every non-faulty node decides on some value—the system doesn't deadlock forever. The FLP result shows you cannot have both properties simultaneously in a fully asynchronous system with even one possible failure, so practical algorithms sacrifice one under certain conditions (usually liveness during suspected failures).

**Leader-Based vs. Leaderless**: Some consensus algorithms (like [[Raft]]) elect a leader who coordinates decisions—the leader receives requests, logs them, and broadcasts decisions. Other algorithms (like some versions of Paxos) are leaderless, with any node able to propose values. Leader-based algorithms are often simpler to understand and implement; leaderless algorithms can be more resilient to leader failures but are typically more complex.

**Quorum Systems**: Most consensus algorithms use quorum systems—a write must be acknowledged by a majority (or quorum) of nodes before being considered committed. This majority overlap property ensures that any two quorums share at least one node, enabling nodes to learn about decisions made by other quorums. For a system with 2f+1 nodes, a quorum of f+1 nodes tolerates up to f failures while still being able to make progress.

**Log Replication**: Consensus algorithms often work by maintaining a replicated log—a sequence of commands that all nodes agree to apply in the same order. Consensus on the log implies consensus on the state (if all nodes apply the same commands in the same order, they reach the same state). [[Raft]] explicitly models this; [[Paxos]] can be used similarly but is sometimes described in terms of values directly.

**Term and Epoch Numbers**: To distinguish between current and stale leaders (in case of network partitions), algorithms use logical time divisions. Raft uses "terms" (incrementing integers); Viewstamped Replication uses "epochs." If a node receives a message from an older term, it's from a stale leader and can be ignored.

## How It Works

Understanding [[Raft]] helps illuminate how consensus algorithms function in practice:

**Leader Election**: Raft uses a randomized election timeout to trigger leader elections. Nodes start as followers; if a follower doesn't hear from a leader within its timeout, it becomes a candidate and requests votes from other nodes. Nodes vote for at most one candidate per term. A candidate wins by acquiring votes from a majority of nodes. This majority requirement ensures that only one leader can be elected per term (safety property).

**Normal Operation**: During normal operation, clients send requests to the leader. The leader appends the command to its local log and sends AppendEntries RPCs to followers. When a majority of nodes have written the entry, the leader applies it to the state machine and returns to the client. This is the "replicate" phase of Raft's two-phase approach.

**Log Consistency**: Raft maintains the invariant that if two nodes have an entry at the same index in their logs, they must have the same command for all preceding entries. The leader sends the index and term of the previous log entry when sending AppendEntries; followers reject entries that don't match their log.

**Failure and Recovery**: When a leader fails, a new election occurs. The new leader may have a longer log than some followers (which failed during the previous term). Raft ensures safety by only granting votes to candidates whose log is at least as up-to-date as the voter's log (using term and index comparison).

```python
# Simplified Raft follower implementation
import asyncio
import random
import time
from typing import Optional, Callable

class RaftFollower:
    """
    Simplified Raft follower node.
    Demonstrates leader heartbeat detection and vote granting.
    """
    
    def __init__(self, node_id: str, peers: list):
        self.node_id = node_id
        self.peers = peers  # Other node IDs
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: list = []  # List of (term, command)
        self.commit_index = 0
        
        # Randomized election timeout (150-300ms typical)
        self.election_timeout = random.uniform(0.15, 0.30)
        self.last_heartbeat = time.time()
        
        # State machine (simplified)
        self.state_machine = {}
    
    def is_election_timeout(self) -> bool:
        """Check if we haven't heard from leader recently."""
        return (time.time() - self.last_heartbeat) > self.election_timeout
    
    def receive_heartbeat(self, leader_term: int, leader_id: str) -> bool:
        """
        Process heartbeat from leader.
        Returns True if heartbeat was valid and accepted.
        """
        if leader_term < self.current_term:
            return False  # Stale leader
        
        if leader_term > self.current_term:
            # New term, become follower
            self.current_term = leader_term
            self.voted_for = None
        
        self.last_heartbeat = time.time()
        return True
    
    def request_vote(self, candidate_id: str, candidate_term: int,
                     last_log_index: int, last_log_term: int) -> tuple:
        """
        Handle RequestVote RPC.
        Returns (vote_granted: bool, current_term: int).
        """
        if candidate_term < self.current_term:
            return False, self.current_term
        
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.voted_for = None
        
        # Check if we've already voted for someone else
        if self.voted_for is not None and self.voted_for != candidate_id:
            return False, self.current_term
        
        # Check if candidate's log is at least as up-to-date as ours
        our_last_term = self.log[-1][0] if self.log else 0
        if last_log_term < our_last_term:
            return False, self.current_term
        if last_log_term == our_last_term and last_log_index < len(self.log):
            return False, self.current_term
        
        # Grant vote
        self.voted_for = candidate_id
        self.last_heartbeat = time.time()  # Reset election timer
        return True, self.current_term
    
    async def apply_committed_entries(self):
        """Apply log entries that are now committed to state machine."""
        while self.commit_index < len(self.log):
            term, command = self.log[self.commit_index]
            # Apply to state machine
            self.state_machine[command['key']] = command['value']
            self.commit_index += 1


class RaftLeader:
    """Simplified Raft leader node."""
    
    def __init__(self, node_id: str, peers: list):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.log: list = []
        self.next_index: dict = {}  # For each peer, next log index to send
        self.match_index: dict = {}  # For each peer, highest replicated index
        
        # Initialize next_index for each peer
        for peer in peers:
            self.next_index[peer] = len(self.log) + 1
    
    async def replicate_log(self, command: dict) -> bool:
        """
        Replicate a command to all followers.
        Returns True when majority acknowledges.
        """
        # Append to local log
        self.log.append((self.current_term, command))
        
        # Send AppendEntries to all followers
        ack_count = 1  # Leader's own log
        for peer in self.peers:
            success = await self._send_append_entries(peer)
            if success:
                ack_count += 1
        
        # Check if committed (majority)
        if ack_count > (len(self.peers) + 1) // 2:
            return True
        return False
    
    async def _send_append_entries(self, peer: str) -> bool:
        """
        Send AppendEntries RPC to a peer.
        Simplified—in production this handles retries and conflicts.
        """
        prev_index = self.next_index.get(peer, 1) - 1
        prev_term = self.log[prev_index][0] if prev_index > 0 and prev_index <= len(self.log) else 0
        
        entries = self.log[prev_index:] if prev_index < len(self.log) else []
        
        # In production: actual RPC call to peer
        # Here we simulate success
        return True
```

## Practical Applications

**ZooKeeper and etcd**: These coordination services are built on consensus algorithms. ZooKeeper uses a protocol called ZAB (Zookeeper Atomic Broadcast); etcd uses [[Raft]]. Applications use these services for distributed locks (e.g., ensuring only one node processes a task), leader election (e.g., determining which node handles incoming requests), and configuration management (e.g., distributing cluster membership).

**Distributed Databases**: Databases like CockroachDB, TiKV, and ScyllaDB use consensus to replicate writes across nodes. When you write to these databases, the write is acknowledged only after a quorum of replicas has committed it to their logs. This provides strong consistency with automatic failover—if the leader fails, a new leader is elected from the remaining replicas.

**Service Discovery**: Consensus algorithms help maintain consistent views of which services are available. In a dynamic cloud environment where nodes come and go, consensus ensures all nodes agree on the current cluster membership.

**Distributed Messaging**: Message queues like Kafka use consensus for metadata management and (in some configurations) for message replication. This ensures messages aren't lost even when nodes fail.

## Examples

Consensus algorithms appear in many production systems:

```python
# Demonstrating the quorum principle for consensus
import asyncio
from typing import List, Set

class SimpleQuorumConsensus:
    """
    Simplified quorum-based consensus.
    In production, use Raft, Paxos, or a library like etcd.
    """
    
    def __init__(self, nodes: List[str]):
        self.nodes = nodes
        self.quorum_size = len(nodes) // 2 + 1  # Majority
    
    async def propose(self, value: any) -> bool:
        """
        Propose a value to all nodes.
        Returns True if quorum agrees.
        """
        votes = await asyncio.gather(*[
            self._request_vote(node, value) 
            for node in self.nodes
        ])
        return sum(votes) >= self.quorum_size
    
    async def _request_vote(self, node: str, value: any) -> bool:
        """Simulate RPC to request node's vote."""
        # In production: actual network call
        # Node would check term, log completeness, etc.
        return True  # Simplified
    
    def get_quorum(self) -> Set[str]:
        """Return which nodes constitute a quorum."""
        return set(self.nodes[:self.quorum_size])
```

## Related Concepts

- [[Raft]] - A consensus algorithm designed for understandability
- [[Paxos]] - The classic consensus algorithm by Leslie Lamport
- [[ZooKeeper]] - Production consensus system using ZAB
- [[Distributed Systems]] - The broader context for consensus
- [[CAP Theorem]] - Consensus relates to achieving strong consistency
- [[etcd]] - Distributed key-value store using Raft
- [[Vector Clocks]] - Alternative approach for ordering events

## Further Reading

- "Paxos Made Simple" by Leslie Lamport (2001) - Accessible Paxos paper
- "In Search of an Understandable Consensus Algorithm" by Ongaro and Ousterhout (2014) - Raft paper
- "Consensus: Bridging Theory and Practice" (Ongaro's dissertation) - Comprehensive Raft guide
- MIT 6.824 Distributed Systems course - Lectures on Raft and Paxos
- "The Raft Consensus Algorithm" website - raft.github.io

## Personal Notes

I found Raft much easier to understand than Paxos despite them being theoretically equivalent. The insight that Raft separates concerns (leader election, log replication, safety) into distinct phases helped me build a mental model. The key thing I internalized is that consensus doesn't mean all nodes agree at the exact same instant—it means they eventually agree and will never disagree (safety). The path to agreement can involve timeouts, retries, and leader changes, but the safety invariant holds throughout. This "eventual" nature is what makes consensus possible despite the FLP impossibility.
