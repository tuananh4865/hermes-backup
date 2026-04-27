---
title: "CRDT"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [crdt, distributed-systems, eventual-consistency, conflict-free, replication]
---

# CRDT

## Overview

CRDT stands for Conflict-Free Replicated Data Type—a family of data structures designed to enable automatic resolution of conflicts in distributed systems where multiple nodes can update the same data independently without coordination. Unlike traditional approaches that require distributed locks or consensus protocols to serialize updates, CRDTs are built on mathematical principles that guarantee any two replicas, when merged, will converge to the same state regardless of the order in which updates were applied. This property makes CRDTs invaluable for building collaborative applications, distributed databases, and systems that must remain available during network partitions.

The concept was developed through academic research in the early 2000s and gained widespread practical adoption in the 2010s as applications needed to handle real-time collaboration, offline-first experiences, and globally distributed data. Companies like Apple (for Notes and iCloud), Bet365 (for sports betting odds), and SoundCloud (for audio metadata) have deployed CRDTs in production systems. The rise of conflict-free replication represents a shift from pessimistic approaches (coordination before operations) to optimistic ones (coordinate-free operations with conflict resolution after the fact).

The fundamental insight behind CRDTs is that if you structure your data and operations correctly, you can make conflicts impossible or automatically resolvable. This transforms the hard problem of distributed consensus into a simpler problem of merging state—a problem that can be solved locally without network communication.

## Key Concepts

**Commutativity as Foundation**: The core mathematical property that makes CRDTs work is that all operations are designed to commute—applying operation A then B produces the same result as applying B then A. This eliminates the order-dependency that causes conflicts in traditional replicated systems. When operations commute, replicas can apply updates in any order and still converge.

**Two Flavors: CmRDT and CvRDT**: CRDTs come in two complementary forms. CmRDTs (Commutative Replicated Data Types) define operations that commute—updates are transmitted as operations that can be applied in any order. CvRDTs (Convergent Replicated Data Types) represent state directly—replicas compare their states and merge them using a monotonic join operation. Both guarantee convergence but differ in what they transmit and how they resolve conflicts.

**Monotonicity**: CvRDT state updates must be monotonic—state can only increase in a lattice of possible values. This ensures that when two replicas merge, they can only converge upward in the lattice rather than diverging sideways. For example, a counter can only increment (never decrement), a set can only grow (never shrink for Grow-Only Sets), and a register can only be overwritten with newer values.

**Idempotence**: Many CRDT operations are also idempotent—applying the same operation twice produces the same result as applying it once. This property is crucial because in distributed systems, messages may be delivered multiple times due to network retries. Idempotent operations are safe to replay without causing duplicate effects.

## How It Works

CRDTs achieve conflict-free replication through carefully designed data structures and operations. Understanding a few canonical examples illuminates the approach:

**G-Counter (Grow-Only Counter)**: A counter that can only increment. Each node maintains its own count of increments, and the total value is the sum across all nodes. Because increments are monotonic (counts never decrease), replicas always converge: any two partial sums eventually merge to the same total. This is a CvRDT—the state itself (the vector of per-node counts) is what gets replicated and merged.

**LWW-Register (Last-Writer-Wins Register)**: A register that stores a value along with a timestamp. When merging, the write with the higher timestamp wins. While conceptually simple, LWW requires synchronized clocks or logical timestamps (see [[Vector Clocks]]) to work correctly. The key insight is that the conflict resolution policy is embedded in the data structure itself rather than requiring external coordination.

**OR-Set (Observed-Remove Set)**: A set that supports add and remove operations while guaranteeing convergence. Each element in the set is tagged with the node that added it and a unique version. Removes are recorded in a tombstone set, and during merge, an element is only present if it was added after its last removal. This allows concurrent adds and removes from different nodes to resolve automatically.

**RGA (Replicated Growable Array)**: Used for collaborative text editing. Elements are identified by unique IDs and include references to predecessor elements. Concurrent insertions at the same position are resolved by comparing IDs, ensuring all replicas converge to the same sequence regardless of edit order.

```python
# Simplified G-Counter CRDT implementation
from typing import Dict
import uuid

class GCounter:
    """
    A Grow-Only Counter CRDT.
    State is a vector of per-node increment counts.
    Merge takes element-wise maximum (join operation).
    Value is the sum across all nodes.
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.counts: Dict[str, int] = {}  # node_id -> count
    
    def increment(self) -> None:
        """Increment this node's local counter."""
        self.counts[self.node_id] = self.counts.get(self.node_id, 0) + 1
    
    def value(self) -> int:
        """Current counter value (sum of all nodes' counts)."""
        return sum(self.counts.values())
    
    def merge(self, other: 'GCounter') -> 'GCounter':
        """
        Merge with another replica.
        Takes element-wise maximum - monotonic join in lattice.
        """
        result = GCounter(self.node_id)
        all_nodes = set(self.counts.keys()) | set(other.counts.keys())
        for node in all_nodes:
            result.counts[node] = max(
                self.counts.get(node, 0),
                other.counts.get(node, 0)
            )
        return result
    
    def __repr__(self) -> str:
        return f"GCounter({self.counts}, value={self.value()})"


# Demonstration
counter_a = GCounter("A")
counter_b = GCounter("B")

counter_a.increment()
counter_a.increment()
counter_b.increment()

# Simulate network partition and independent updates
# When they reconnect, they merge:
merged = counter_a.merge(counter_b)
print(f"Counter A: {counter_a}")
print(f"Counter B: {counter_b}")
print(f"Merged: {merged}")
# Regardless of order, result is {A:2, B:1} -> value 3
```

## Practical Applications

**Collaborative Editing**: The most visible CRDT application is real-time collaborative document editing. Tools like Notion, Figma's text tools, and Apple's iWork suite use CRDTs to allow multiple users to edit documents simultaneously without coordination. When you insert a character in a shared document, the operation is broadcast to all participants and merged using a data structure like RGA or Treedoc—no locking required.

**Chat and Messaging**: Modern messaging systems often use CRDTs for managing concurrent message edits and reactions. When you edit a message while offline and then reconnect, the edit is merged with any other edits that occurred in the interim, with conflicts resolved automatically rather than requiring manual resolution.

**Distributed Databases**: Databases like [[Cassandra]] (with certain configurations), Riak, and Antidote use CRDTs to provide eventual consistency with automatic conflict resolution. Instead of requiring consensus for every write, these databases accept writes locally and use CRDT semantics to merge concurrent updates.

**Shopping Carts and Inventory**: E-commerce platforms use CRDT-based carts to allow users to add items from multiple devices or tabs without coordination. If you add an item on your phone while the desktop browser is open, both additions merge seamlessly when the devices next sync.

**Distributed Gaming**: Game state (scores, inventory, world state) can be managed with CRDTs, allowing players to have consistent views without requiring a centralized server for conflict resolution.

## Examples

```python
# LWW-Register (Last-Writer-Wins) CRDT
from typing import Optional, Tuple
import time
import uuid

class LWWRegister:
    """
    Last-Writer-Wins Register.
    Each update includes a timestamp (vector clock component).
    On merge, the update with higher timestamp wins.
    """
    
    def __init__(self, node_id: str, timestamp: float, value: any):
        self.node_id = node_id
        self.timestamp = timestamp  # Logical or physical timestamp
        self.value = value
    
    @classmethod
    def create(cls, node_id: str, value: any, 
               timestamp: Optional[float] = None) -> 'LWWRegister':
        return cls(node_id, timestamp or time.time(), value)
    
    def update(self, value: any, timestamp: Optional[float] = None) -> 'LWWRegister':
        """Create new register with updated value."""
        return LWWRegister(self.node_id, timestamp or time.time(), value)
    
    def merge(self, other: 'LWWRegister') -> 'LWWRegister':
        """
        Merge with another replica.
        Higher timestamp wins; ties broken by node_id for determinism.
        """
        if self.timestamp > other.timestamp:
            return self
        elif other.timestamp > self.timestamp:
            return other
        else:
            # Same timestamp - use node_id as tiebreaker (deterministic)
            return self if self.node_id < other.node_id else other


class PNCounter:
    """
    Positive-Negative Counter - supports both increments and decrements.
    Maintains two G-Counters: one for increments, one for decrements.
    Value = P_count - N_count
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.positive = GCounter(node_id)
        self.negative = GCounter(node_id)
    
    def increment(self) -> None:
        self.positive.increment()
    
    def decrement(self) -> None:
        self.negative.increment()
    
    def value(self) -> int:
        return self.positive.value() - self.negative.value()
    
    def merge(self, other: 'PNCounter') -> 'PNCounter':
        result = PNCounter(self.node_id)
        result.positive = self.positive.merge(other.positive)
        result.negative = self.negative.merge(other.negative)
        return result
```

## Related Concepts

- [[Distributed Systems]] - The broader context where CRDTs operate
- [[Eventual Consistency]] - The consistency model CRDTs enable
- [[Vector Clocks]] - Often used alongside CRDTs to track causality
- [[CAP Theorem]] - CRDTs enable AP systems to achieve convergence
- [[BASE CAP]] - CRDTs are a key technology for BASE-style systems
- [[Consensus Algorithms]] - Alternative approach to distributed agreement

## Further Reading

- "A Comprehensive Study of Convergent and Commutative Replicated Data Types" by Shapiro et al. (2011) - foundational CRDT paper
- "CRDTs: An Overview" by Kleppmann et al. - practical introduction
- "Automerge" library documentation - a popular CRDT library for JavaScript
- "Yjs" documentation - another widely-used CRDT implementation
- Riak documentation on CRDTs - production experience with CRDTs

## Personal Notes

CRDTs changed my mental model of distributed systems. Instead of trying to prevent conflicts through coordination, we can embrace a model where conflicts are inevitable but automatically resolvable. The key insight is that the choice of data structure determines what conflicts are possible and how they resolve. A Grow-Only Set will never have a "remove vs. add" conflict because removals aren't supported. A Last-Writer-Wins Register always resolves conflicts through timestamps. Once you internalize this, you start seeing CRDT patterns everywhere in well-designed collaborative systems.
