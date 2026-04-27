---
title: "BASE CAP"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [base, cap, distributed-systems, eventual-consistency, scalability]
---

# BASE CAP

## Overview

BASE is an acronym that stands for "Basically Available, Soft state, Eventually consistent"—coined by computer scientist Dan Pritchett at eBay in 2008. It represents a pragmatic approach to building highly scalable distributed systems by explicitly accepting eventual consistency as a design trade-off rather than fighting against the impossibility theorems that govern distributed computing. The name is deliberately a play on ACID (the traditional transaction properties), acknowledging that BASE systems take a different philosophical approach to data integrity—one that prioritizes availability and partition tolerance while acknowledging that strong consistency is temporarily sacrificed.

The BASE model emerged from eBay's practical need to scale their architecture beyond what traditional relational databases could handle. At massive scale, maintaining strong consistency across all nodes becomes prohibitively expensive or simply impossible within latency budgets. By accepting eventual consistency, eBay could build systems that remained available during partial failures while still eventually converging to correct state. This approach has since been adopted by countless internet-scale systems.

Understanding BASE is essential for anyone designing distributed systems because it provides a coherent vocabulary for discussing and reasoning about the consistency guarantees that non-traditional distributed databases provide. It sits in contrast to the "Strong Consistency" model implied by traditional ACID transactions and even the "consistency" in [[CAP Theorem]]'s sense.

## Key Concepts

**Basically Available**: This property states that the system guarantees availability, either total or partial, in the face of failures. The system may return responses that are stale or only partially updated, but it will always respond—unlike a CP system that might become completely unavailable when it cannot guarantee consistency. BA systems are designed to gracefully degrade rather than fail catastrophically. If some nodes fail, the remaining nodes continue operating, possibly with reduced functionality or reduced consistency guarantees.

**Soft State**: The "soft state" property acknowledges that the system's state may change over time, even without new input, because of eventual consistency mechanisms. Unlike hard state (which persists unchanged until explicitly modified), soft state reflects the reality that different replicas may temporarily hold different values for the same data. The system will eventually converge, but at any given moment, the state is "soft"—indicating it's provisional and subject to change. This is a fundamental acknowledgment that in distributed systems, you cannot always know the "current" true state.

**Eventually Consistent**: The core guarantee of BASE systems. If no new updates are made to a data item, eventually all replicas of that item will return the same value. The system will converge to a consistent state given sufficient time without new writes. The key word is "eventually"—there's no bound specified on how long convergence might take. Different implementations may offer different convergence guarantees: some might converge in milliseconds, others might take minutes. Some systems offer tunable parameters to control the trade-off between latency and consistency.

## Relationship to CAP Theorem

BASE is essentially the practical embodiment of choosing the AP (Availability + Partition Tolerance) side of the CAP theorem. When a partition occurs, AP systems remain available but may serve stale data. When the partition heals, they eventually converge. BASE extends this model to describe the system's behavior even during normal operation—not just during partitions.

The term "soft state" captures the idea that AP systems are always in a state of gradual convergence. Even without partitions, network latency means that updates propagate across the system over time. Different nodes may temporarily diverge, but the system continues operating and eventually resolves these differences. This is fundamentally different from CP systems, where consistency is maintained at all times (often through synchronous replication or consensus protocols) even if it means higher latency or unavailability.

It's worth noting that CAP and BASE address different aspects of system design. CAP is a theorem with mathematical precision, while BASE is a philosophical model and set of practical design principles. CAP proves that you cannot have all three properties simultaneously; BASE describes how to build useful systems that explicitly accept the resulting trade-offs.

## How It Works

BASE systems typically employ several techniques to achieve availability and eventual consistency:

**Asynchronous Replication**: Rather than synchronously propagating updates to all replicas before acknowledging a write, BASE systems often use asynchronous replication. A write is acknowledged immediately after being recorded locally or to a minority of replicas, then propagated to other replicas in the background. This provides low latency but means reads might hit replicas that haven't yet received the latest update.

**Conflict Resolution**: When concurrent or conflicting updates occur on different replicas, BASE systems need mechanisms to resolve these conflicts. Common approaches include last-write-wins (LWW), where the most recent timestamp determines the correct value; vector clocks (see [[Vector Clocks]]) for tracking causality; and CRDTs (see [[CRDT]]) which are data structures designed to merge concurrent updates without conflict.

**Version Vectors**: To track which updates have propagated to which replicas, systems often maintain version vectors or similar metadata. This allows the system to detect when replicas have diverged and may need reconciliation.

**Read Repair and Anti-Entropy**: Some systems proactively detect and repair inconsistencies during read operations (read repair) or periodically compare replica states to identify and resolve divergences (anti-entropy protocols).

## Practical Applications

BASE principles are employed by many of the world's largest websites and services:

**eBay and PayPal**: The original BASE practitioners, eBay's architecture separates data into fine-grained partitions (shards), each with independent storage. This avoids distributed transactions across shards while BASE principles govern replication within each shard.

**Amazon Dynamo**: Amazon's Dynamo database (and its derivatives like [[Cassandra]] and [[Riak]]) explicitly targets BASE properties. Dynamo is designed for high write availability and low latency, accepting that concurrent writes may create conflicts that are resolved later.

**Social Media Platforms**: Systems like Twitter, Facebook, and Instagram use BASE-style architectures to manage user feeds, comments, and likes. The occasional stale count or temporarily missing post is acceptable in exchange for keeping the service available during traffic spikes.

**NoSQL Movement**: Many NoSQL databases—including document stores, wide-column stores, and key-value stores—are designed with BASE principles in mind. They sacrifice strong consistency to achieve performance, scalability, and availability that ACID-compliant relational databases cannot match at internet scale.

## Examples

```python
# Simplified BASE-style eventual consistency implementation
import asyncio
import time
from typing import Any, Optional, Dict
from collections import defaultdict
import uuid

class BASEDocumentStore:
    """
    A simplified document store demonstrating BASE properties:
    - Basically Available: Always responds, even if data is stale
    - Soft State: State changes without input due to async replication
    - Eventually Consistent: Updates propagate and converge over time
    """
    
    def __init__(self, replica_count: int = 3):
        self.replicas: list[Dict[str, Any]] = [
            {} for _ in range(replica_count)
        ]
        self.version_vectors: list[Dict[str, int]] = [
            {} for _ in range(replica_count)
        ]
        self.pending_writes: asyncio.Queue = asyncio.Queue()
        self.replica_count = replica_count
    
    async def put(self, key: str, value: Any) -> str:
        """
        Write with basic availability - returns immediately
        after writing to local replica. Async propagation.
        """
        write_id = str(uuid.uuid4())
        local_replica = 0  # Always write to "local" first
        
        # Immediately update local replica
        self.replicas[local_replica][key] = value
        self.version_vectors[local_replica][key] = \
            self.version_vectors[local_replica].get(key, 0) + 1
        
        # Async propagation to other replicas (soft state begins)
        asyncio.create_task(self._propagate_write(
            write_id, key, value, local_replica
        ))
        
        return write_id
    
    async def _propagate_write(self, write_id: str, key: str, 
                                value: Any, source_replica: int):
        """Propagate write to other replicas asynchronously."""
        for i in range(self.replica_count):
            if i != source_replica:
                # Simulate network latency
                await asyncio.sleep(0.05)  # 50ms propagation delay
                self.replicas[i][key] = value
                self.version_vectors[i][key] = \
                    self.version_vectors[i].get(key, 0) + 1
    
    def get(self, key: str) -> Optional[Any]:
        """
        Read with eventual consistency - may return stale data.
        This is basically available but returns soft state.
        """
        # In a real system, might read from multiple replicas
        # and use version vectors to detect divergence
        for replica in self.replicas:
            if key in replica:
                return replica[key]
        return None
    
    async def wait_for_consistency(self, key: str, timeout: float = 1.0):
        """Wait for a key to become consistent across replicas."""
        start = time.time()
        while time.time() - start < timeout:
            values = [r.get(key) for r in self.replicas]
            if len(set(values)) == 1 and values[0] is not None:
                return True  # All replicas agree
            await asyncio.sleep(0.01)
        return False  # Timed out without convergence
```

## Related Concepts

- [[Distributed Systems]] - The broader context where BASE operates
- [[CAP Theorem]] - The theoretical foundation that motivates BASE
- [[PACELC Theorem]] - Extends CAP to consider latency trade-offs
- [[Eventual Consistency]] - The consistency model BASE guarantees
- [[Strong Consistency]] - The alternative model that BASE sacrifices
- [[CRDT]] - Data structures that enable conflict-free eventual consistency
- [[Vector Clocks]] - Mechanism for tracking causality in distributed updates
- [[Consensus Algorithms]] - Protocols for achieving stronger consistency
- [[Cassandra]] - A widely-used BASE/NoSQL database

## Further Reading

- Dan Pritchett's original BASE paper (2008) - "Base: An Acid Alternative"
- "Dynamo: Amazon's Highly Available Key-value Store" - The paper that popularized BASE-style systems
- "Designing Data-Intensive Applications" by Martin Kleppmann - Excellent coverage of consistency models
- "NoSQL Distilled" by Pramod Sadalage and Martin Fowler - Practical guide to non-relational databases

## Personal Notes

BASE was a pivotal insight for me—it provided vocabulary for what I was seeing in production systems. The theoretical ACID model simply wasn't compatible with building services that needed to stay available during partial failures. Accepting soft state and eventual convergence felt uncomfortable at first, like giving up on correctness. But the key insight is that BASE systems don't give up correctness—they give up on the illusion that you can have a single, authoritative "current" state in a distributed system. Once you accept that reality, you can design systems that are honest about their guarantees and therefore more robust.
