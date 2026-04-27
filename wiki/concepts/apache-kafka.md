---
title: "Apache Kafka"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [kafka, distributed-systems, streaming, messaging, event-streaming, apache]
---

# Apache Kafka

## Overview

Apache Kafka is a distributed event streaming platform that serves as a distributed [[Commit Log]] (or write-ahead log), enabling high-throughput, fault-tolerant ingestion and distribution of event streams. Originally developed at LinkedIn and later open-sourced as an Apache project, Kafka has become the de facto backbone for event-driven architectures, [[Microservices]] integration, real-time analytics pipelines, and stream processing applications. Unlike traditional [[Message Queue]] systems designed for point-to-point message delivery, Kafka uses a publish-subscribe model with durable, partitioned, replicated logs that can be consumed by multiple independent consumer groups simultaneously.

Kafka's core abstraction is a **topic**, a named stream of events organized into partitions. Producers write events to topics; consumers read from topics. Each partition is an ordered, immutable sequence of records that is appended-only. Partitions are replicated across brokers for fault tolerance, with configurable replication factors. This architecture decouples producers from consumers, allowing systems to evolve independently and enabling patterns like [[Event Sourcing]], [[CQRS]], and complex stream processing.

Kafka sits at the intersection of [[Message Queue]] and database paradigms. Like a database, it provides durable storage with configurable retention; like a message queue, it enables asynchronous communication between producers and consumers. But unlike most message queues, Kafka's retention is time-based and log-based, allowing consumers to replay events from any point within the retention window—a capability that fundamentally changes how systems can be designed.

## Key Concepts

**Topic and Partitions** — A topic is a named stream of events. Events within a topic are divided into partitions, each hosted on a broker. Partitions are ordered and immutable; each event gets a sequential offset number. Partitioning enables horizontal scaling—each partition can be served by a different broker, and producers can route events to specific partitions based on a partition key.

**Producers and Consumers** — Producers are client applications that publish events to Kafka topics. They can specify a partition key to control which partition receives an event (ensuring all events for a given key land in the same partition, maintaining ordering). Consumers read events from topics, maintaining their own offset position. Multiple consumer groups can subscribe independently; each group sees all events but tracks its own offset.

**Consumer Groups** — A set of consumers that cooperate to process a topic. Kafka partitions are distributed among consumers in a group. If a consumer fails, its partitions are rebalanced among remaining members. This provides both parallel processing and fault tolerance. Consumer groups are how Kafka achieves the "each event is processed exactly once" semantics when combined with idempotent producers and transactional consumers.

**Replication and Durability** — Partitions are replicated across brokers according to a replication factor. One broker is the "leader" for a partition; others are followers. All writes go through the leader; followers replicate asynchronously. If the leader fails, a follower becomes the new leader automatically. This provides fault tolerance and availability.

**Retention** — Kafka retains events for a configurable time period (or size). Unlike traditional queues that delete messages after consumption, Kafka keeps messages until retention expires. This enables:
- **Replay** — New consumers can process historical events
- **Event Sourcing** — Kafka can serve as an [[Event Store]]
- **Temporal queries** — Query events at any point in the retention window
- **Rebuilding projections** — Recompute read models from scratch

**Stream Processing** — Kafka Streams and Apache Flink are stream processing libraries that consume from Kafka topics, transform data, and write results back to Kafka. Kafka Streams is lightweight, runs as a library within your application, and provides exactly-once processing semantics.

## How It Works

A typical Kafka deployment consists of multiple brokers forming a cluster, with ZooKeeper or KRaft (in newer versions) managing cluster metadata and leadership election:

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Kafka Cluster                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ Broker 1│  │ Broker 2 │  │ Broker 3 │                      │
│  │ P0 (L)  │  │ P0 (F)   │  │ P1 (L)   │   L=Leader, F=Follower│
│  │ P1 (F)  │  │ P2 (L)   │  │ P2 (F)   │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘
        ↑                ↑                ↑
   Producer          Producer          Producer
   writes to         writes to         writes to
   P0               P1                P2
```

Event flow for a typical e-commerce order:
```text
1. OrderService publishes OrderPlaced event to "orders" topic
2. InventoryService consumes from "orders", decrements stock
3. ShippingService consumes from "orders", creates shipment
4. AnalyticsService consumes from "orders", updates real-time dashboards
5. FraudDetectionService consumes from "orders", scores transactions
```

```java
// Producer: Publishing an event to Kafka
KafkaProducer<String, OrderEvent> producer = new KafkaProducer<>(props);
OrderEvent event = new OrderEvent("order_123", "user_456", items, 99.99);
producer.send(new ProducerRecord<>("orders", event.getUserId(), event));
producer.flush();
```

```java
// Consumer: Reading events from Kafka
KafkaConsumer<String, OrderEvent> consumer = new KafkaConsumer<>(props);
consumer.subscribe(List.of("orders"));
while (true) {
  ConsumerRecords<String, OrderEvent> records = consumer.poll(Duration.ofMillis(100));
  for (ConsumerRecord<String, OrderEvent> record : records) {
    processOrder(record.value());
    consumer.commitSync(); // Commit offset after successful processing
  }
}
```

## Practical Applications

- **Microservices integration** — Kafka acts as the "backbone" for asynchronous communication between microservices. Instead of direct HTTP calls, services publish domain events. This decouples services temporally (consumers process at their own pace) and structurally (producers don't know who consumes).
- **Real-time analytics** — Clickstreams, sensor data, and financial ticks flow through Kafka into stream processing pipelines that compute real-time metrics, aggregations, and alerts.
- **Event sourcing backbone** — Kafka's durable, replayable log makes it suitable as the event store in event sourcing architectures. The log IS the source of truth; projections are built by consuming events.
- **Data ingestion for data lakes** — Kafka feeds data into [[Apache Hadoop]], data warehouses, and lakehouse architectures, providing exactly-once delivery guarantees and handling backpressure.
- **Audit logging and compliance** — Financial and healthcare systems use Kafka's immutable log as an audit trail. Every state change is captured as an event; the log is tamper-evident and queryable.
- **Complex event processing** — Patterns like "notify user if they abandon cart within 24 hours" require correlating multiple events over time—Kafka Streams enables this with state stores.

## Examples

**Confluent Platform** — The commercial distribution of Kafka by Confluent, adding schema registry (for Avro/Protobuf schemas), REST proxy, JDBC connector, and stream governance tools.

**Kafka Connect** — A framework for connecting Kafka with external systems. Connectors exist for databases (Debezium CDC connector captures database changes as events), cloud storage (S3 sink), search engines, and more. Debezium + Kafka is a popular pattern for [[Change Data Capture]]:

```json
// Debezium CDC event from MySQL binlog
{
  "before": null,
  "after": { "id": 123, "email": "alice@example.com", "updated_at": 1713000000 },
  "source": { "db": "ecommerce", "table": "users", "lsn": 123456 },
  "op": "u",  // create, update, delete, read
  "ts_ms": 1713000001000
}
```

**Kafka Streams Word Count** — A simple stream processing topology:

```java
// Kafka Streams: Real-time word count
StreamsBuilder builder = new StreamsBuilder();
KStream<String, String> textLines = builder.stream("text-input");

KTable<String, Long> wordCounts = textLines
  .flatMapValues(text -> Arrays.asList(text.toLowerCase().split("\\W+")))
  .groupBy((key, word) -> word)
  .count(Materialized.as("counts"));

wordCounts.toStream().to("word-count-output");
```

## Related Concepts

- [[Message Queue]] — Traditional point-to-point messaging (contrast with durable log)
- [[Event-Driven Architecture]] — Paradigm that Kafka enables
- [[Event Sourcing]] — Pattern where Kafka can serve as the event store
- [[CQRS]] — Write-read separation enabled by event streaming
- [[Microservices]] — Kafka as the backbone for async service communication
- [[Apache Flink]] — Advanced stream processing engine that consumes from Kafka
- [[Change Data Capture]] — Debezium and Kafka Connect patterns
- [[Commit Log]] — The data structure Kafka implements
- [[Stream Processing]] — Kafka Streams and real-time event transformation

## Further Reading

- "Kafka: The Definitive Guide" by Neha Narkhede et al. — Comprehensive Kafka reference.
- Apache Kafka Documentation — Official docs covering architecture, configuration, and APIs.
- "Building Event-Driven Microservices" by Adam Bellemare — How to design microservices around Kafka.
- Confluent Blog — Deep dives on Kafka Streams, schema registry, and best practices.

## Personal Notes

Kafka is one of those technologies that looks simple (it's just an ordered log) but has significant operational complexity at scale. The mental shift from queues to logs is key—once you embrace that consumers own their position and can replay, the design possibilities open up. I've found that organizations starting with Kafka often underestimate the need for schema registry and schema evolution—without it, you get producer/consumer coupling through implicit knowledge of data formats. Also, consumer group rebalancing can cause "stop-the-world" pauses if not configured carefully with session timeouts. The new KRaft mode (removing ZooKeeper dependency) simplifies operations significantly.
