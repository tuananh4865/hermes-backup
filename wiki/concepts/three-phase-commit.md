---
title: Three-Phase Commit
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, distributed-transactions, consensus, fault-tolerance]
---

## Overview

Three-Phase Commit (3PC) is an extension of the Two-Phase Commit protocol designed to eliminate the blocking problem that plagues 2PC when the coordinator crashes after participants have prepared. By introducing an additional phase with a pre-commit state, 3PC allows participants to safely timeout and proceed without blocking, improving availability and latency in distributed systems that require atomic commitment.

The core insight behind 3PC is that the blocking in 2PC occurs because participants do not know whether other participants have received the coordinator's decision. In 3PC, the protocol passes through an intermediate state that participants can observe, allowing them to make progress independently if the coordinator fails. This makes 3PC particularly attractive for systems that prioritize availability over consistency, such as high-throughput data stores and real-time processing systems.

## Key Concepts

Understanding 3PC requires grasping how it modifies the two-phase structure to achieve non-blocking operation.

**The Three Phases**

Phase 1 (Voting Phase) functions identically to 2PC: the coordinator asks participants to vote on whether they can prepare. If any participant votes no, the coordinator broadcasts abort; if all vote yes, the coordinator proceeds to Phase 2.

Phase 2 (Pre-Commit Phase) is new. The coordinator sends a pre-commit message to all participants, indicating that all have voted yes and the transaction will commit. Participants acknowledge receipt. If a participant times out waiting for the pre-commit message after voting yes, it can safely commit using its knowledge that all other participants also voted yes.

Phase 3 (Commit Phase) is similar to 2PC's commit phase but non-blocking. The coordinator sends commit messages; if a participant times out waiting for commit after receiving pre-commit, it proceeds to commit rather than blocking indefinitely.

**Non-Blocking Guarantees**

The critical property of 3PC is that once a majority of participants have acknowledged the pre-commit phase, the protocol can complete regardless of coordinator failure. This works because participants know that all nodes that could affect the decision have already indicated their intent to commit.

**Network Partitions and Minority Failures**

Unlike 2PC, which can block indefinitely if the coordinator fails, 3PC handles coordinator failures more gracefully. However, 3PC is still susceptible to blocking during network partitions where no majority can be formed. The protocol cannot guarantee safety under arbitrary network partitions without additional mechanisms.

## How It Works

The three-phase structure enables a recovery mechanism that avoids blocking by exploiting the pre-commit state.

**State Machine Representation**

Each participant can be modeled as a state machine with the following states: Initial, Prepared, Pre-Committed, Committed, Aborted. The coordinator similarly transitions through Init, Voting, Pre-Commit, Committed, Aborted states. Transitions occur only in response to messages or timeouts, and the protocol is designed so that any state can be recovered given sufficient information.

**Timeout-Driven Recovery**

When a participant times out waiting for a message, it examines what it knows about the global state. If the participant has voted yes but received no pre-commit, it can safely commit because it knows all participants voted yes. If it has not voted yet, it can abort. This timeout-driven recovery eliminates blocking.

**Coordinator Failure Handling**

If the coordinator fails, participants can elect a new coordinator. The new coordinator queries all participants to determine their current state, then drives the protocol to completion. Because participants have durable logs of their state and acknowledgments, the new coordinator can always determine whether to commit or abort.

**Limitations**

3PC assumes a synchronous or partially synchronous network with bounded delays and timeouts. In practice, if timeouts are set incorrectly or the network experiences prolonged delays, 3PC can still exhibit blocking behavior. Additionally, 3PC is not suitable for systems requiring strict serializability in the presence of network partitions.

## Practical Applications

Three-Phase Commit sees use in systems that require atomic commitment but cannot tolerate the blocking behavior of 2PC.

**High-Availability Databases**

Some distributed databases use 3PC or similar protocols to coordinate commits across replicas while maintaining availability during coordinator failures.

**Real-Time Transaction Processing**

Systems that cannot afford indefinite blocking, such as financial trading platforms or telecommunications infrastructure, may use 3PC to ensure timely commitment.

**Coordination Services**

Distributed coordination services like Apache ZooKeeper use protocols inspired by 3PC for managing distributed state, though they typically implement more sophisticated consensus algorithms.

## Examples

```python
import asyncio
from enum import Enum
from typing import Dict

class ParticipantState(Enum):
    INITIAL = "initial"
    PREPARED = "prepared"
    PRECOMMITTED = "precommitted"
    COMMITTED = "committed"
    ABORTED = "aborted"

class ThreePhaseCommitNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state = ParticipantState.INITIAL
        self.transaction_log = []
    
    async def on_vote_request(self, tx_id: str, operations: list):
        """Phase 1: Respond to vote request"""
        # Execute operations locally
        result = await self.execute_operations(operations)
        if result.success:
            self.state = ParticipantState.PREPARED
            self.transaction_log.append((tx_id, "PREPARED"))
            return "yes"
        else:
            self.state = ParticipantState.ABORTED
            return "no"
    
    async def on_precommit(self, tx_id: str):
        """Phase 2: Acknowledge pre-commit"""
        self.state = ParticipantState.PRECOMMITTED
        self.transaction_log.append((tx_id, "PRECOMMITTED"))
        return "ack"
    
    async def on_commit(self, tx_id: str):
        """Phase 3: Actually commit"""
        self.state = ParticipantState.COMMITTED
        await self.persist_changes()
        self.transaction_log.append((tx_id, "COMMITTED"))
    
    async def on_abort(self, tx_id: str):
        """Abort the transaction"""
        self.state = ParticipantState.ABORTED
        await self.rollback_changes()
        self.transaction_log.append((tx_id, "ABORTED"))
    
    async def execute_operations(self, operations):
        """Execute transaction operations"""
        pass
    
    async def persist_changes(self):
        """Persist committed changes"""
        pass
    
    async def rollback_changes(self):
        """Rollback uncommitted changes"""
        pass
```

## Related Concepts

- [[Two-Phase Commit]] - The foundation that 3PC builds upon
- [[Consensus Algorithms]] - Protocols like Raft that solve similar problems without blocking
- [[Distributed Systems]] - The broader context
- [[Saga Pattern]] - An alternative approach emphasizing availability over atomicity
- [[Fault Tolerance]] - The property that 3PC aims to improve

## Further Reading

- "The Three-Phase Commit Protocol" by Dalisky, G. and G. Bar (original 3PC paper)
- "Transaction Processing" by Jim Gray and Andreas Reuter
- "Introduction to Distributed Systems" by Maarten van Steen

## Personal Notes

3PC is one of those algorithms that is elegant in theory but complex in practice. The timeout values alone are tricky—set them too short and you get spurious aborts; too long and you defeat the purpose of non-blocking. Most production systems I've encountered use Raft or Paxos instead, which provide similar safety guarantees with better understood failure modes. I view 3PC as a good learning exercise and occasionally useful in specialized contexts, but rarely the first choice for new systems.
