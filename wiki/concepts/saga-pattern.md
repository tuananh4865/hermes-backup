---
title: Saga Pattern
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [saga-pattern, distributed-transactions, microservices, choreography, orchestration]
---

## Overview

The Saga pattern is a design pattern for managing distributed transactions across multiple services in a microservices architecture, where a single logical business operation spans multiple bounded contexts. Unlike traditional ACID transactions that guarantee atomicity across database operations within a single database, the Saga pattern coordinates a series of local transactions across different services, each with its own database, while maintaining eventual consistency.

The core challenge the Saga pattern addresses is that distributed systems cannot rely on traditional two-phase commit protocols due to their blocking nature and coordinator failure modes. In a microservices architecture, a single business operation—like placing an order—might require actions across the Order Service, Inventory Service, Payment Service, and Shipping Service. Each service manages its own data and cannot participate in an atomic distributed transaction with the others. The Saga pattern provides a structured approach to coordinating these cross-service operations while accepting that failures will occur and must be handled gracefully.

Sagas come in two primary flavors: choreographed sagas, where each service participates by emitting and listening to events, and orchestrated sagas, where a central coordinator explicitly tells each service what action to take next. Both approaches handle failures through compensating transactions—operations that undo the effects of previously completed steps when a later step fails. For example, if a hotel booking fails after a flight has already been booked, the saga issues a compensating transaction to cancel the flight.

The pattern was originally described in a 1987 academic paper by Hector Garcia-Molina and Kenneth Salem as a mechanism for managing long-lived transactions in database systems. It has since been adapted and widely adopted in distributed systems architecture, particularly for scenarios involving financial transactions, booking systems, and order fulfillment pipelines where atomicity across services is required but traditional distributed transactions are impractical.

## Key Concepts

The Saga pattern involves several interconnected concepts that work together to coordinate distributed operations.

**Local Transactions** are the atomic operations executed by individual services within a saga. Each step in a saga is a local transaction from the perspective of the service performing it—the service can commit or rollback its own changes independently. However, the service must also implement compensating logic to undo its changes if the saga as a whole fails at a later step. This requirement to implement both forward progress and rollback behavior is a key design consideration for any saga participant.

**Compensating Transactions** are the mechanisms by which a saga undoes the effects of previously completed local transactions. Unlike database rollbacks that simply reverse a transaction, compensating transactions are often real business operations themselves—a cancellation, a refund, a reversal. The compensation must restore the system to a consistent state but may not literally undo the original operation's effects in the same way a rollback would. For example, a compensating transaction for a hotel booking might send a cancellation request to the hotel system rather than trying to reverse the original database insert.

**Saga Orchestrator** is a centralized coordinator that manages the execution and failure handling of a saga. The orchestrator maintains the state of the saga, determines which steps to execute next based on the outcomes of previous steps, and initiates compensating transactions when failures occur. An orchestrator is itself a service that can be implemented as a state machine, making the saga logic explicit and visible. This centralized approach simplifies debugging and provides a clear picture of saga progress, but can create a single point of failure if not designed carefully.

**Choreography-Based Sagas** distribute saga logic across participating services without a central coordinator. Each service listens for events from other services and responds by emitting its own events to trigger the next steps. Choreography works well for simple sagas with few participants but can become difficult to understand and maintain as complexity grows. Event logs serve as the implicit record of saga state, which can make debugging harder since there is no central entity observing the full saga.

## How It Works

The Saga pattern executes through a sequence of steps with explicit failure handling at each stage.

```python
from dataclasses import dataclass, field
from typing import Callable, List
from enum import Enum

class SagaStepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    execute: Callable[[], any]
    compensate: Callable[[], None]
    status: SagaStepStatus = SagaStepStatus.PENDING

class OrderPlacementSaga:
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.context: dict = {}
    
    def add_step(self, name: str, execute: Callable, compensate: Callable):
        self.steps.append(SagaStep(name, execute, compensate))
        return self
    
    async def execute(self) -> bool:
        completed_steps: List[SagaStep] = []
        
        try:
            for step in self.steps:
                print(f"Executing step: {step.name}")
                result = await step.execute()
                self.context[step.name] = result
                step.status = SagaStepStatus.COMPLETED
                completed_steps.append(step)
        
        except Exception as e:
            print(f"Saga failed at step {step.name}: {e}")
            # Compensate in reverse order
            await self._compensate(completed_steps)
            return False
        
        return True
    
    async def _compensate(self, completed_steps: List[SagaStep]):
        # Compensate in reverse order
        for step in reversed(completed_steps):
            try:
                print(f"Compensating step: {step.name}")
                await step.compensate()
                step.status = SagaStepStatus.COMPENSATED
            except Exception as ce:
                print(f"Compensation failed for {step.name}: {ce}")
                step.status = SagaStepStatus.FAILED
                # Saga compensation failed - requires human intervention

# Usage example
async def place_order_saga():
    saga = OrderPlacementSaga()
    
    saga.add_step(
        name="create_order",
        execute=lambda: order_service.create(),
        compensate=lambda: order_service.cancel()
    ).add_step(
        name="reserve_inventory",
        execute=lambda: inventory_service.reserve(),
        compensate=lambda: inventory_service.release()
    ).add_step(
        name="charge_payment",
        execute=lambda: payment_service.charge(),
        compensate=lambda: payment_service.refund()
    ).add_step(
        name="notify_shipping",
        execute=lambda: shipping_service.create_label(),
        compensate=lambda: shipping_service.cancel_label()
    )
    
    success = await saga.execute()
    return success
```

The saga executes steps sequentially, storing results in the context dictionary for use by subsequent steps. If any step fails, the saga enters the compensation phase, iterating through completed steps in reverse order and executing their compensating actions. This reverse-order compensation ensures that if step 3 fails after steps 1 and 2 succeeded, the system first undoes step 2, then undoes step 1. This approach guarantees that the system reaches a consistent state even when failures occur mid-saga.

## Practical Applications

The Saga pattern is essential for any distributed system where business operations span multiple services and traditional distributed transactions are not feasible.

**E-Commerce Order Processing** is the canonical saga use case. An order placement typically involves creating an order record, reserving inventory, processing payment, and initiating shipping. Each step is handled by a separate microservice with its own database. A failed payment step triggers compensation to release inventory and cancel the order. This flow maps naturally to a purchase saga with clear forward and backward paths.

**Travel Booking Systems** handle multi-leg journeys where flight, hotel, and car rental might be booked through different providers. If the hotel booking fails after the flight is already booked, the saga compensates by canceling the flight. Travel sagas often involve external third-party systems with their own failure modes and cancellation policies, requiring careful design of compensation logic.

**Financial Fund Transfers** between accounts held in different institutions cannot use traditional distributed transactions due to the lack of a common transaction coordinator across organizational boundaries. A cross-bank transfer saga initiates a debit from the source institution and a credit at the destination, with compensation handling cases where one side fails. Many payment networks implement saga-like patterns with explicit settlement and reconciliation phases.

**Multi-Step Workflows** in business process management systems are natural candidates for saga patterns. Employee onboarding might involve creating accounts in multiple systems (email, HR, badge access, software provisioning), with compensation removing all created artifacts if a later step fails. The explicit nature of saga orchestration makes these workflows auditable and debuggable.

## Examples

A concrete flight booking saga demonstrates choreography-based coordination:

```javascript
// Event-driven choreography saga for flight + hotel booking

// FlightService listens and reacts
eventBus.subscribe('BookingRequested', async (event) => {
  try {
    const flightReservation = await flightAPI.book(
      event.payload.flightId,
      event.payload.passengerId
    );
    
    eventBus.publish('FlightBooked', {
      correlationId: event.correlationId,
      reservationId: flightReservation.id
    });
  } catch (error) {
    eventBus.publish('FlightBookingFailed', {
      correlationId: event.correlationId,
      reason: error.message
    });
  }
});

// HotelService listens and reacts
eventBus.subscribe('FlightBooked', async (event) => {
  try {
    const hotelReservation = await hotelAPI.book(
      event.payload.correlationId,  // Links to same booking
      event.payload.checkIn,
      event.payload.checkOut
    );
    
    eventBus.publish('HotelBooked', {
      correlationId: event.correlationId,
      reservationId: hotelReservation.id
    });
  } catch (error) {
    // Compensate the flight
    await flightAPI.cancel(event.payload.reservationId);
    eventBus.publish('BookingFailed', {
      correlationId: event.correlationId,
      reason: error.message
    });
  }
});

// BookingService listens for completion
eventBus.subscribe('HotelBooked', (event) => {
  bookingRepository.update(event.correlationId, {
    status: 'confirmed',
    flightId: event.flightId,
    hotelId: event.hotelId
  });
});
```

In this choreography approach, each service reacts to events from other services without a central coordinator. The correlation ID links related events to the same booking session. When the hotel booking fails, the HotelService itself initiates compensation by canceling the already-booked flight—this is implicit choreography where compensation responsibility is distributed.

## Related Concepts

- [[distributed-transactions]] — The broader problem space that sagas address
- [[event-sourcing]] — Pattern often used alongside sagas for event-driven coordination
- [[CQRS]] — Architectural pattern commonly paired with saga for command handling
- [[compensating-transactions]] — The specific mechanism for undoing saga steps
- [[event-driven-architecture]] — Architecture style where choreography-based sagas fit naturally
- [[circuit-breaker]] — Pattern that prevents cascading failures during saga compensation
- [[microservices]] — Architecture where sagas are commonly necessary

## Further Reading

- "Saga Pattern" by Carlos Buenos — Original academic paper reference
- "Distributed Sagas" — Academic paper on formalizing saga semantics
- "Implementing Sagas with Azure Durable Functions" — Microsoft patterns documentation
- "Pattern: Saga" — Martin Fowler's description of the pattern

## Personal Notes

The hardest part of sagas is designing compensation logic upfront—not just for happy paths but for all the ways things can fail. My rule of thumb: if you can't clearly define the compensation for each step, you haven't finished designing the saga. Also, monitoring is critical—unlike ACID transactions where you get automatic failure detection, saga failures can silently leave the system in an inconsistent state without proper observability.
