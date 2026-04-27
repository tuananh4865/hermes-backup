---
title: Kafka
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [kafka, apache, streaming, event-driven, distributed]
---

# Kafka

## Overview

Apache Kafka is an open-source distributed event streaming platform originally developed by LinkedIn and later donated to the Apache Software Foundation. It serves as a high-throughput, fault-tolerant messaging system capable of handling trillions of events per day across thousands of nodes. Kafka is designed around the concept of distributed [[event streaming]], where data is produced as a continuous stream of events organized into logical topics.

Unlike traditional message brokers such as RabbitMQ or IBM MQ, Kafka persists messages to disk rather than deleting them immediately after consumption. This retention-based model enables powerful patterns like event replay, [[event sourcing]], and time-travel debugging. Messages in Kafka are stored with a key-value pair structure, where the key determines partitioning behavior and the value holds the actual payload. Consumers read messages at their own pace, and Kafka maintains consumer position via offsets, allowing precise control over consumption semantics.

Kafka's core API surface includes the Producer API for publishing events, the Consumer API for subscribing, the Streams API for transforming and aggregating data in real time, and the Connect API for integrating with external systems. The platform is built on a distributed, multi-broker architecture that provides horizontal scalability and automatic fault tolerance through replication.

## Architecture

Kafka's architecture is built around several key components that work together to deliver reliable, scalable event streaming.

**Brokers** are the individual server instances that make up a Kafka cluster. Each broker handles incoming write requests, manages disk storage, and serves read requests from consumers. Brokers communicate with each other to replicate data and coordinate cluster leadership. A healthy Kafka deployment typically spans three or more brokers to ensure availability and durability.

**Topics** are named logical channels to which producers publish events and from which consumers subscribe. Each topic defines a category of data flow within the system. Topics are configured with a retention policy that determines how long messages are kept, ranging from hours to years, or indefinitely.

**Partitions** are the fundamental unit of parallelism and distribution in Kafka. Each topic is divided into one or more partitions, with each partition residing on a single broker. Partitions are further replicated across multiple brokers for fault tolerance. The assignment of partition leadership is managed by the cluster controller, which in newer Kafka versions relies on KRaft (Kafka's built-in Raft-based consensus) rather than Apache ZooKeeper.

**Producers** publish events to topic partitions, optionally specifying a key that Kafka uses to determine which partition receives the message. This key-based routing ensures that all events with the same key land in the same partition, preserving ordering guarantees for related records.

**Consumers** read from partitions and track their position using offsets. Consumer groups allow multiple instances to share the workload of a topic, with each partition being assigned to exactly one consumer within a group. Kafka guarantees that messages within a partition are delivered in order to any single consumer.

The combination of broker clustering, partition replication, and offset-based consumption provides Kafka with its characteristic durability, scalability, and fault tolerance properties.

## Use Cases

Kafka's versatility has led to its adoption across a wide range of production scenarios.

**Real-time data pipelines** are among the most common use cases. Kafka acts as a central nervous system that ingests data from disparate sources such as databases, application logs, and IoT sensors, then streams that data to destinations like data warehouses, search indexes, or analytics platforms. Companies use Kafka to replace brittle point-to-point integrations with a durable, auditable streaming backbone.

**Event sourcing** and [[cqrs]] patterns rely heavily on Kafka's immutable, ordered log semantics. Rather than storing current state, event-sourced systems append every state change as an event to a Kafka topic. This creates a complete audit trail and enables rebuilding state by replaying events. Kafka's retention and compaction features make it well-suited as an event store for these architectures.

**Stream processing** applications built with Kafka Streams or Apache Flink consume from Kafka topics, perform transformations, aggregations, or joins, and produce results back to other topics. This enables patterns such as real-time dashboards, anomaly detection, and dynamic pricing engines.

**Microservices communication** increasingly uses Kafka as an event bus for asynchronous, decoupled service interactions. Instead of direct synchronous calls, services emit domain events to Kafka, allowing other services to react independently. This pattern supports better fault isolation, independent scaling, and polyglot service development.

**Log aggregation and observability** pipelines use Kafka to centralize logs and metrics from hundreds of services into a unified stream, feeding downstream systems for monitoring, alerting, and forensic analysis.

## Related

- [[event-streaming]] - The broader paradigm that Kafka implements
- [[Distributed Systems]] - The foundational concept enabling Kafka's scalability and fault tolerance
- [[Message Brokers]] - Traditional messaging middleware that Kafka evolved beyond
- [[Event Sourcing]] - Architectural pattern that leverages Kafka's immutable log
- [[apache-zookeeper]] - Previously used for Kafka cluster coordination (now deprecated in favor of KRaft)
- [[kafka-streams]] - Java library for building stream processing applications on top of Kafka
