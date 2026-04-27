---
title: Two-Phase Commit
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, distributed-transactions, consensus, fault-tolerance]
---

## Overview

Two-Phase Commit (2PC) is a distributed transaction protocol that ensures all participants in a transaction either commit together or roll back together, maintaining atomicity across multiple independent data stores. It is the classic solution for coordinating distributed transactions, used in distributed databases, transaction processing systems, and distributed ledgers where multiple nodes must agree on whether to apply or revert a set of changes.

The protocol gets its name from its two distinct phases: a voting phase where the coordinator asks participants whether they are prepared to commit, and a completion phase where the coordinator decides the outcome and notifies all participants. This two-phase approach provides atomicity even when participants are on different machines, potentially in different data centers, ensuring that a distributed operation either succeeds completely or fails without leaving partial state.

## Key Concepts

Two-Phase Commit involves several critical concepts that work together to achieve atomic commitment.

**Coordinator and Participants**

The protocol involves one coordinator node that manages the transaction and multiple participant nodes that each hold some portion of the data being modified. The coordinator is typically the node that initiates the transaction, though in some implementations, a dedicated transaction manager handles this role. Each participant is responsible for its own data store and must be able to temporarily hold uncommitted changes while voting.

**The Vote Phase (Phase 1)**

During the voting phase, the coordinator sends a prepare message to all participants asking them to prepare for commitment. Each participant then makes any temporary changes durable (often by writing to a write-ahead log) and votes either "yes" to commit or "no" to abort. If a participant votes yes, it is promising to be able to commit if asked; if it votes no, it must roll back and release any locks it acquired.

**The Commit Phase (Phase 2)**

After all participants have voted, the coordinator makes a decision. If all participants voted yes, the coordinator sends a commit message and all participants apply their changes permanently. If any participant voted no (or failed to respond within the timeout), the coordinator sends a rollback message and all participants undo their temporary changes.

**Blocking Problem**

A significant limitation of 2PC is that once a participant votes "yes" and becomes prepared, it is blocked—it must wait for either a commit or rollback message from the coordinator. If the coordinator crashes after participants have prepared but before it can broadcast its decision, those participants remain in limbo, holding locks and unable to proceed. This blocking behavior makes 2PC unsuitable for high-availability systems where long pauses are unacceptable.

## How It Works

The complete Two-Phase Commit flow involves careful logging, timeouts, and recovery procedures.

**Transaction Initiation**

A client initiates a transaction with the coordinator, specifying the operations to perform across multiple participants. The coordinator creates a transaction record and begins tracking the state of each participant. Each participant executes its portion of the transaction up to the prepare point but does not commit.

**Prepare with Write-Ahead Logging**

Before voting yes, each participant writes its intended changes to a redo log (write-ahead log). This ensures that if the participant crashes and later recovers, it can complete or undo the transaction. The participant also acquires any necessary locks but defers releasing them until the transaction completes.

**Decision and Notification**

The coordinator decides based on all votes received. If unanimous yes, it writes a commit record to its log before sending commit messages; if any no, it writes an abort record before sending rollback messages. This logging ensures that the coordinator can recover correctly after a crash.

**Recovery Protocol**

When a participant or coordinator recovers from a crash, it consults its log to determine the transaction's state. If a commit or abort record exists, the recovery process completes the operation accordingly. If only prepare records exist but no decision record, the recovery must contact other nodes to determine the outcome—potentially leading to the blocking scenario described above.

## Practical Applications

Two-Phase Commit is used in scenarios where strong atomicity guarantees are required across multiple data stores.

**Distributed Databases**

Traditional distributed databases like those implementing SQL often use 2PC to coordinate commits across replicas and shards. When a transaction spans multiple physical databases, 2PC ensures all or nothing gets committed.

**XA Transactions**

The XA standard (eXtended Architecture) defines a way for multiple databases to participate in a global transaction using 2PC. Many enterprise database systems and message brokers implement XA for interoperable distributed transactions.

**Distributed Ledgers**

Some distributed ledger implementations use variants of 2PC to coordinate commits across nodes, though newer designs often prefer consensus algorithms that avoid blocking.

## Examples

Here is a simplified implementation demonstrating the 2PC protocol flow:

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class Vote(Enum):
    YES = "yes"
    NO = "no"

class Decision(Enum):
    COMMIT = "commit"
    ABORT = "abort"

@dataclass
class TransactionState:
    transaction_id: str
    participants: List[str]
    votes: dict
    decision: Decision = None

class TwoPhaseCommit:
    def __init__(self, participants: List[dict]):
        self.participants = participants
        self.state = None
    
    def execute_transaction(self, tx_id: str, operations: list):
        # Phase 1: Voting
        self.state = TransactionState(tx_id, [p['id'] for p in self.participants], {})
        
        # Ask all participants to prepare
        for participant in self.participants:
            vote = participant['node'].prepare(tx_id, operations)
            self.state.votes[participant['id']] = vote
        
        # Check if all voted yes
        if all(v == Vote.YES for v in self.state.votes.values()):
            self.state.decision = Decision.COMMIT
            # Phase 2: Commit
            for participant in self.participants:
                participant['node'].commit(tx_id)
        else:
            self.state.decision = Decision.ABORT
            # Phase 2: Rollback
            for participant in self.participants:
                participant['node'].rollback(tx_id)
        
        return self.state.decision
```

This example shows the core 2PC structure: collecting votes from all participants and then making a binary decision that applies uniformly to all.

## Related Concepts

- [[Three-Phase Commit]] - An extension that avoids blocking
- [[Distributed Systems]] - The broader context for 2PC
- [[Consensus Algorithms]] - Algorithms like Raft that solve similar problems
- [[Saga Pattern]] - An alternative approach for distributed transactions
- [[ACID Transactions]] - The guarantees that 2PC provides

## Further Reading

- "Concurrency Control and Recovery in Database Systems" by Philip Bernstein
- "Distributed Systems" by Maarten van Steen and Andrew Tanenbaum
- "Transaction Processing" by Jim Gray and Andreas Reuter

## Personal Notes

Two-Phase Commit taught me that atomicity in distributed systems is far more subtle than in single-node transactions. The blocking problem is a real killer in production—when a coordinator crashes and participants are left waiting, you end up with frozen accounts, stuck reservations, and very unhappy users. For this reason, many modern systems use the Saga pattern instead, trading atomicity for availability. I now reserve 2PC for cases where I truly need atomic commitment across a small, fixed set of nodes and can tolerate potential delays.
