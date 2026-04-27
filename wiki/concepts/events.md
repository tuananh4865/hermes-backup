---
title: "Events"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [events, architecture, microservices, async]
---

# Events

## Overview

In software architecture, an **event** is a significant change in state or an occurrence that a system recognizes and can react to. Events are the foundation of event-driven architecture, a design paradigm where components communicate by producing and consuming asynchronous messages rather than making direct synchronous calls.

Unlike traditional request-response patterns where a caller waits for a response, event-driven systems operate on a fire-and-forget model. When something happens—such as a user placing an order, a sensor reading exceeding a threshold, or a file being uploaded—an event is published to a message broker or event bus. Interested services then react to these events independently, without the producer needing to know who is listening.

This decoupling between producers and consumers is the central advantage of event-driven systems. It enables greater scalability, resilience, and flexibility in distributed architectures.

## Patterns

### Publish/Subscribe (Pub/Sub)

The publish/subscribe pattern is the most common event distribution model. In pub/sub, event producers publish messages to a topic or channel, and interested consumers subscribe to receive those messages. The publisher has no knowledge of its subscribers, and messages can be broadcast to multiple independent consumers simultaneously.

Message brokers like Apache Kafka, RabbitMQ, and AWS SNS/SQS implement pub/sub at scale, supporting features such as message filtering, dead-letter queues, and guaranteed delivery.

### Event Sourcing

Event sourcing is a pattern where the state of an application is stored as a sequence of immutable events rather than as current-state snapshots. Every change to the application's state is captured as an event, creating a complete audit trail.

Instead of updating a record, the system appends a new event to an event store. To reconstruct the current state, the system replays all events in order. This pattern is particularly valuable in domains requiring audit trails, temporal queries, or the ability to rebuild state at any point in time.

### Event-Driven Microservices

In microservices ecosystems, events serve as the backbone of inter-service communication. Services emit events when state changes occur, and other services react accordingly. This allows services to remain loosely coupled—they do not call each other directly but instead react to shared events.

## Use Cases

Event-driven architecture shines in several scenarios:

- **Real-time applications**: Chat systems, live notifications, collaborative tools, and gaming servers all benefit from the immediate propagation of events.
- **Financial systems**: Transaction processing, fraud detection, and audit logging rely on immutable event streams for accuracy and compliance.
- **IoT and sensor networks**: Large volumes of telemetry data are naturally modeled as streams of events from distributed devices.
- **Data pipelines**: ETL processes, change data capture (CDC), and stream analytics use events to move and transform data between systems.

## Related

- [[microservices]]
- [[message-brokers]]
- [[event-sourcing]]
- [[async-communication]]
- [[distributed-systems]]
