---
title: Saga Orchestration
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, saga-pattern, microservices, choreography, transactions]
---

## Overview

Saga Orchestration is a pattern for managing distributed transactions across multiple services in a microservices architecture, where instead of using a centralized coordinator like Two-Phase Commit, a dedicated orchestrator service directs the execution of sagas—sequences of local transactions that each update data within a single service. The orchestrator tells each participant what local operation to perform next based on the outcome of previous steps, and handles both successful completion and compensatory rollback when failures occur.

The key insight behind saga orchestration is that while atomic commitment across services is often impractical or impossible, we can still achieve eventual consistency through a carefully orchestrated sequence of operations with explicit compensation logic. Unlike ACID transactions that guarantee atomicity through locking, sagas achieve consistency through application-level code that knows how to undo partial work when something goes wrong.

## Key Concepts

Understanding saga orchestration requires familiarity with several core patterns and mechanisms.

**The Orchestrator**

The orchestrator is the brain of the saga. It maintains the state of the saga, decides which steps to execute next, and handles failure recovery. Unlike a traditional transaction manager, the orchestrator does not hold locks across services; instead, it coordinates by sending commands and processing responses. The orchestrator is typically implemented as a state machine that transitions based on events from participants.

**Local Transactions**

Each step in a saga is a local transaction executed within a single service boundary. These local transactions may update a database, publish an event, call an external API, or perform any operation within the service's scope. Each local transaction must have a corresponding compensating transaction that can undo its effects.

**Compensating Transactions**

When a step in a saga fails, the orchestrator must undo previously completed steps by executing their compensating transactions. For example, if a hotel booking succeeds but the subsequent flight booking fails, the orchestrator must cancel the hotel reservation. Compensating transactions must be idempotent, commutative, and eventually successful to guarantee saga completion.

**Saga States**

A saga progresses through multiple states: Initial, Executing, Completing, Compensating, and Completed (either successfully or with rollback). The orchestrator tracks these states and ensures the saga always moves toward a terminal state, even in the presence of failures.

## How It Works

The orchestration flow involves creating a saga, executing steps sequentially, handling failures, and managing compensation.

**Saga Creation**

When a business operation requires multiple services (like placing an order that involves inventory, payment, and shipping), the orchestrator creates a new saga instance with a unique identifier. The initial state is set to Executing, and the first step is queued.

**Step Execution**

The orchestrator sends a command to the first participant service to execute its local transaction. The participant performs the work and responds with success or failure. On success, the orchestrator advances to the next step. On failure, the orchestrator transitions to Compensating state and initiates rollback.

**Compensation Flow**

When compensation begins, the orchestrator iterates through completed steps in reverse order, sending compensate commands to each participant. Each participant undoes its local transaction and responds. The orchestrator tracks which compensations have succeeded and retries failed ones until all are complete.

**Concurrency Considerations**

Multiple sagas may operate concurrently, and compensation for one saga may conflict with steps of another. Careful design is needed to handle such cases, often through idempotency, optimistic locking, or reservation patterns.

## Practical Applications

Saga orchestration is widely used in microservices architectures for business operations that span multiple services.

**Order Management Systems**

Placing an order might involve checking inventory, reserving items, charging payment, scheduling delivery, and sending notifications. Saga orchestration coordinates these steps, handling failures gracefully.

**Travel Booking Platforms**

Booking a trip might involve reserving flights, hotels, and car rentals from different providers. Saga orchestration ensures all reservations succeed or all are cancelled.

**Financial Services**

Opening a new account might require creating records in multiple systems (core banking, compliance, CRM). Saga orchestration handles the coordination and rollback if regulatory checks fail.

## Examples

Here is a simplified implementation of a saga orchestrator for an order placement saga:

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Callable
import logging

class SagaState(Enum):
    INITIAL = "initial"
    EXECUTING = "executing"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"

class OrderSagaStep:
    def __init__(self, name: str, execute_fn: Callable, compensate_fn: Callable):
        self.name = name
        self.execute_fn = execute_fn
        self.compensate_fn = compensate_fn

@dataclass
class OrderSaga:
    order_id: str
    steps: List[OrderSagaStep]
    completed_steps: List[str] = field(default_factory=list)
    state: SagaState = SagaState.INITIAL
    
    async def execute(self):
        self.state = SagaState.EXECUTING
        for step in self.steps:
            try:
                result = await step.execute_fn(self.order_id)
                self.completed_steps.append(step.name)
                logging.info(f"Saga {self.order_id}: Step {step.name} succeeded")
            except Exception as e:
                logging.error(f"Saga {self.order_id}: Step {step.name} failed: {e}")
                await self.compensate()
                return False
        self.state = SagaState.COMPLETED
        return True
    
    async def compensate(self):
        self.state = SagaState.COMPENSATING
        for step_name in reversed(self.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)
            try:
                await step.compensate_fn(self.order_id)
                logging.info(f"Saga {self.order_id}: Compensated {step_name}")
            except Exception as e:
                logging.error(f"Saga {self.order_id}: Compensation failed for {step_name}: {e}")
                raise
        self.state = SagaState.FAILED

# Example usage
async def reserve_inventory(order_id: str):
    # Call inventory service
    pass

async def cancel_inventory_reservation(order_id: str):
    # Call inventory service to cancel
    pass

saga = OrderSaga(
    order_id="order-123",
    steps=[
        OrderSagaStep("reserve_inventory", reserve_inventory, cancel_inventory_reservation),
        # Additional steps would go here
    ]
)
```

## Related Concepts

- [[Saga Choreography]] - The alternative decentralized approach to sagas
- [[Microservices]] - The architectural style where sagas are common
- [[Two-Phase Commit]] - The traditional distributed transaction approach
- [[Event-Driven Architecture]] - Sagas often use events for coordination
- [[Compensating Transaction]] - The mechanism for undoing saga steps

## Further Reading

- "Saga Pattern" by Gregor Hohpe and Bobby Woolf (Enterprise Integration Patterns)
- "Building Microservices" by Sam Newman
- "Designing Data-Intensive Applications" by Martin Kleppmann

## Personal Notes

I've found that saga orchestration works best when the orchestrator is treated as a first-class citizen in the system—not just utility code but a managed service with its own persistence, monitoring, and recovery mechanisms. The hardest part is writing correct compensating transactions; they must handle being called multiple times (idempotency) and must eventually succeed even under partial failures. I recommend starting with choreography for simple flows and moving to orchestration when you need better observability and control over complex multi-step processes.
