---
title: Saga Choreography
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-systems, saga-pattern, microservices, orchestration, events]
---

## Overview

Saga Choreography is a decentralized approach to implementing sagas in microservices architectures where instead of a central orchestrator directing the flow of operations, each service involved in the saga publishes events that trigger the next steps in other services. Each service listens for relevant events, performs its local transaction, and publishes new events that may trigger subsequent services—forming a distributed state machine without centralized control.

This approach is named for its similarity to choreographed dance, where each dancer knows their steps and responds to music and cues from other dancers, rather than following a choreographer's explicit directions. Choreography relies on each participant's ability to listen to events, make decisions, and publish the next event in the sequence, creating a loosely coupled system where services do not need to know about each other's implementation details.

## Key Concepts

Understanding saga choreography requires understanding how distributed state machines emerge from event-driven interactions.

**Event-Driven Communication**

Services in a choreography-based saga communicate exclusively through events. When a service completes its local transaction, it publishes a success event; when it fails or needs to compensate, it publishes a failure or compensation event. Other services subscribe to relevant events and respond accordingly. This decoupled communication allows services to evolve independently without tight coupling.

**Domain Events**

Each event in a choreography saga should represent a meaningful domain occurrence: OrderCreated, InventoryReserved, PaymentCharged, Stockpile depleted. These events carry sufficient context for downstream services to make decisions and take appropriate action. Well-designed domain events are key to making choreography scalable and maintainable.

**Compensation Through Events**

When a service needs to undo its work, it publishes a compensation event rather than receiving a command from an orchestrator. Downstream services listen for these compensation events and respond by undoing their own work, potentially publishing further compensation events that propagate backward through the saga.

**Choreography vs Orchestration**

The fundamental distinction is decentralization versus centralization. Choreography offers lower coupling and better scalability, as services don't depend on a specific orchestrator. However, orchestration offers better visibility—you can observe the saga's progress from a single place—and simpler error handling logic. Many practical systems use a hybrid approach.

## How It Works

The choreography flow emerges from local decisions made by each service in response to events.

**Initiating the Saga**

The saga begins when an initiating service publishes an event representing the business request. For example, an Order Service publishes an OrderRequested event containing order details. This event carries all the information needed for downstream services to participate in the saga.

**Reactive Step Execution**

Each participating service subscribes to relevant events. When Inventory Service receives OrderRequested, it reserves inventory and publishes InventoryReserved (success) or InventoryReservationFailed (failure). The next service listens for these events and acts accordingly.

**Forward Recovery**

When a step succeeds, the saga continues forward. The Payment Service listens for InventoryReserved, charges the customer, and publishes PaymentCompleted. This chain continues until the saga completes or a failure triggers compensation.

**Backward Recovery**

When a step fails, the failing service publishes a failure event. Services that completed earlier subscribe to this event and execute their compensating actions. For example, if PaymentFailed is published, Inventory Service listens and publishes InventoryReservationCancelled. This backward propagation continues until all forward actions are undone.

## Practical Applications

Choreography-based sagas are common in event-driven microservices architectures.

**E-Commerce Platforms**

Order processing in e-commerce often follows a choreography pattern: order events trigger inventory checks, which trigger payment processing, which trigger fulfillment preparation. Each service acts independently based on events from upstream services.

**Financial Systems**

Financial transactions often involve multiple independent systems that must remain loosely coupled. Choreography allows compliance, fraud detection, and core banking systems to coordinate through events without direct integration.

**Supply Chain Management**

Complex supply chain processes involve multiple organizations and systems. Event choreography allows each participant to operate independently while contributing to the larger process.

## Examples

```python
# Event definitions
@dataclass
class OrderRequested:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    timestamp: datetime

@dataclass
class InventoryReserved:
    order_id: str
    reservation_id: str
    timestamp: datetime

@dataclass
class PaymentCompleted:
    order_id: str
    transaction_id: str
    amount: float
    timestamp: datetime

# Service implementations using an event bus
class InventoryService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    async def on_order_requested(self, event: OrderRequested):
        try:
            reservation = await self.reserve_inventory(event.order_id, event.items)
            await self.event_bus.publish(InventoryReserved(
                order_id=event.order_id,
                reservation_id=reservation.id,
                timestamp=datetime.now()
            ))
        except InsufficientStock as e:
            await self.event_bus.publish(InventoryReservationFailed(
                order_id=event.order_id,
                reason=str(e),
                timestamp=datetime.now()
            ))
    
    async def on_payment_failed(self, event: PaymentFailed):
        await self.cancel_reservation(event.order_id)

class PaymentService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    async def on_inventory_reserved(self, event: InventoryReserved):
        try:
            transaction = await self.charge_customer(event.order_id, event.amount)
            await self.event_bus.publish(PaymentCompleted(
                order_id=event.order_id,
                transaction_id=transaction.id,
                amount=transaction.amount,
                timestamp=datetime.now()
            ))
        except PaymentDeclined as e:
            await self.event_bus.publish(PaymentFailed(
                order_id=event.order_id,
                reason=str(e),
                timestamp=datetime.now()
            ))
```

This example shows how services react to events and publish new events to continue the saga or trigger compensation.

## Related Concepts

- [[Saga Orchestration]] - The centralized alternative
- [[Event-Driven Architecture]] - The broader pattern
- [[Microservices]] - Where choreography is commonly applied
- [[Compensating Transaction]] - How failures are handled
- [[Domain Events]] - The messages that drive choreography

## Further Reading

- "Enterprise Integration Patterns" by Gregor Hohpe and Bobby Woolf
- "Building Microservices" by Sam Newman
- "Domain-Driven Design" by Eric Evans

## Personal Notes

I've worked with both choreography and orchestration approaches. Choreography feels more "natural" in truly event-driven systems and works well when the saga flow is simple and the number of participants is small. However, I've found that as sagas grow more complex, choreography becomes harder to understand and debug. When I can't easily answer "what happened in that order saga?" by looking at a single place, I start considering moving to orchestration. The hybrid approach—orchestrators for complex flows but choreography for simple ones—has served me well.
