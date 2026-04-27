---
title: Message Brokers
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [message-brokers, messaging, distributed-systems, architecture]
---

# Message Brokers

## Overview

A message broker is a middleware service that facilitates asynchronous communication between distributed applications by acting as an intermediary that receives, stores, and forwards messages between producers and consumers. Message brokers decouple the sender and receiver, allowing services to communicate without requiring both parties to be available or online at the same time. This architectural pattern is fundamental in modern [[distributed-systems]] where services need to exchange data reliably and efficiently.

Message brokers work by exposing queues or topics that producers publish messages to. The broker then ensures messages are delivered to the appropriate consumers, handling concerns such as message persistence, delivery guarantees, load balancing, and fault tolerance. By abstracting away direct network connections between services, message brokers reduce complexity in service-to-service communication and enable systems to scale horizontally.

The benefits of using message brokers include improved system resilience since messages are persisted until consumers acknowledge them, enhanced scalability through transparent load distribution across multiple consumers, and greater flexibility in system design as services evolve independently. These advantages make message brokers a cornerstone of event-driven architectures and microservices ecosystems.

## Patterns

Message brokers support several communication patterns that serve different use cases.

**Point-to-Point Queueing** is the classic message queue pattern where each message is delivered to exactly one consumer. Producers send messages to a named queue, and one consumer receives and processes each message. Once processed, the message is removed or marked as complete. This pattern is ideal for task distribution, workload balancing, and job processing systems where each task needs single-node execution.

**Publish-Subscribe (Pub/Sub)** enables a broadcast-style communication model where producers publish messages to a topic, and all subscribed consumers receive each message. This pattern supports fan-out scenarios where the same event needs to trigger multiple independent actions. Pub/Sub is particularly valuable for event notification systems, real-time data distribution, and scenarios requiring multiple independent handlers for a single event.

**Request-Reply** is a synchronous-like pattern built on top of message queues where a producer sends a request message and waits for a correlated response. The broker routes the response back to the original requester using correlation identifiers. This pattern maintains the benefits of asynchronous communication while enabling request-response semantics.

**Dead Letter Queues** handle messages that cannot be processed successfully. When a consumer fails to process a message after repeated attempts, the broker routes it to a dead letter queue for later inspection, debugging, or reprocessing. This pattern is essential for building robust systems that must not lose data even under failure conditions.

## Examples

**RabbitMQ** is a widely adopted open-source message broker implementing the Advanced Message Queuing Protocol (AMQP). It supports multiple messaging patterns including point-to-point queues and pub/sub through topic exchanges. RabbitMQ is known for its flexibility, supporting various exchange types such as direct, fanout, topic, and headers-based routing. It runs on all major platforms and offers management interfaces for monitoring queues and connections.

**Apache Kafka** is a distributed event streaming platform often used as a high-throughput message broker. Originally developed by LinkedIn, Kafka persists messages to disk in a partitioned, replicated log structure. It excels at handling massive message volumes with low latency, making it suitable for real-time data pipelines, event sourcing, and log aggregation. Kafka's retention-based model allows consumers to replay messages from any point in the log.

**Amazon SQS** (Simple Queue Service) and **Amazon SNS** (Simple Notification Service) provide managed message broker functionality in cloud environments. SQS offers reliable point-to-point queueing without server management, while SNS implements pub/sub notifications. Both services integrate tightly with other AWS offerings, simplifying cloud-native architectures.

**ActiveMQ** is an open-source Java-based message broker supporting multiple protocols including AMQP, MQTT, and STOMP. It provides enterprise features like clustering, failover, and message persistence, serving as a flexible option for organizations requiring a self-hosted solution.

## Related

- [[message-queue]] — The foundational data structure underlying point-to-point message delivery
- [[event-sourcing]] — An architectural pattern that stores events as a sequence of messages, often utilizing message brokers
- [[distributed-systems]] — The broader field of study encompassing systems that communicate via message brokers
- [[pub-sub]] — The publish-subscribe pattern implemented extensively in message broker systems
- [[microservices]] — Architectural style where message brokers commonly enable service interoperability
- [[event-driven-architecture]] — Design approach heavily reliant on message brokers for asynchronous event propagation
