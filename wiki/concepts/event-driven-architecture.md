---
title: event-driven-architecture
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [event-driven-architecture, events, async, microservices]
---

# event-driven-architecture

## Overview

Event-Driven Architecture (EDA) is a software design paradigm in which system components communicate and exchange data by producing and reacting to events. An event is a significant state change or occurrence—such as a user placing an order, a sensor detecting motion, or a file being uploaded—that gets captured and propagated through the system. Rather than components directly invoking one another through synchronous calls, they publish events to a shared channel and let other interested components consume and respond to those events independently.

This decoupling is the central advantage of EDA. Producers of events do not need to know which consumers will handle them, how many consumers exist, or what those consumers do with the information. This enables systems to scale horizontally, evolve independently, and remain resilient to partial failures. Event-driven systems are inherently asynchronous, which makes them well-suited for use cases requiring real-time processing, loose coupling between services, and high throughput under variable load.

EDA is a foundational pattern in modern distributed systems and is closely associated with [[microservices]] architecture, where services benefit from not being tightly bound to one another. It also forms the backbone of reactive systems, which aim to be responsive, resilient, and elastic under the [[Reactive Manifesto]] principles.

## Components

The Event-Driven Architecture comprises three primary categories of participants: event producers, event channels, and event consumers.

**Event Producers** are services or applications that detect or generate events when something meaningful happens in the system. A producer only knows that an event has occurred—it has no awareness of downstream effects. For example, an e-commerce checkout service might produce a "OrderPlaced" event when a customer completes a purchase. Producers are designed to be stateless and fire-and-forget, which contributes to the system's overall scalability.

**Event Channels** serve as the transport layer between producers and consumers. These are typically message brokers or event streaming platforms that persist, route, and manage event distribution. Popular implementations include [[Apache Kafka]], RabbitMQ, and Amazon Kinesis. Kafka, in particular, organizes events into topics—immutable, append-only logs that consumers can read from independently at their own pace. Topics enable event replay, which is valuable for debugging, auditing, or bootstrapping new consumer services without interrupting existing ones.

**Event Consumers** are services that subscribe to one or more channels and process events relevant to their responsibilities. A consumer may perform business logic, update its own state, trigger side effects, or produce new events that cascade through the system. Because consumers operate independently, they can scale up or down based on processing demand without affecting producers or other consumers.

## Related

- [[Microservices]] - Architectural style often paired with EDA for building loosely coupled distributed systems
- [[Apache Kafka]] - Distributed event streaming platform commonly used as the event channel in EDA implementations
- [[Message Queues]] - Related async communication pattern, often used alongside or as an alternative to event streaming
- [[Publish-Subscribe Pattern]] - The messaging pattern where producers publish events and consumers subscribe to receive them
- [[Event Sourcing]] - Related technique that stores state changes as a sequence of events rather than current state snapshots
- [[CQRS]] - Command Query Responsibility Segregation, often used with EDA to separate read and write operations
- [[Async Messaging]] - Broader category of asynchronous communication patterns that includes event-driven approaches
