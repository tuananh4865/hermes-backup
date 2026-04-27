---
title: "Kappa Architecture"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [architecture, streaming, data-engineering, event-processing]
---

# Kappa Architecture

## Overview

Kappa Architecture is a software architecture pattern for processing streaming data that simplifies the older Lambda Architecture by using a single technology stack for both batch and real-time processing. Proposed by Jay Kreps in 2014, Kappa Architecture argues that maintaining two separate codebases (batch and streaming) in Lambda Architecture creates unnecessary complexity, and that a well-designed streaming system can handle both historical reprocessing and real-time queries through the same infrastructure.

The core insight of Kappa Architecture is that your event log is the source of truth. Rather than maintaining separate batch and speed layers that must be merged, you treat all data as streams and use stream processing to materializing views at query time. If you need to recompute results from historical data, you replay the event log through your stream processor.

## Key Concepts

**Event Log as Source of Truth**: All data is captured as immutable events in an append-only log (e.g., Apache Kafka, Amazon Kinesis). This log preserves the complete history of what happened, enabling reprocessing and temporal queries.

**Stream Processing**: Data is processed as it arrives using stream processing engines like Apache Flink, Apache Spark Structured Streaming, or Kafka Streams. The same processing logic handles both real-time updates and historical replay.

**Dual Writes Problem**: Lambda Architecture requires writing to both batch and speed layers. Kappa Architecture eliminates this by writing once to the event log, from which all views are derived.

**Immutability**: Events are never modified or deleted. Corrections are expressed as new events (e.g., a "refund" event rather than mutating an "order" event). This simplifies reasoning about data consistency.

**Exactly-Once Semantics**: Modern stream processors provide exactly-once delivery guarantees, ensuring that reprocessing doesn't produce duplicate or incorrect results.

## How It Works

Kappa Architecture implements data processing through these steps:

1. **Data Ingestion**: Events are published to an append-only log. Each event has a timestamp and is immutable.

2. **Stream Processing**: A stream processor consumes the log and builds queryable views (tables, materialized views, search indices).

3. **View Materialization**: As events arrive, the processor updates the relevant views incrementally. Views are the denormalized, query-optimized representations of the data.

4. **Historical Replay**: To reprocess historical data, a new processor instance (or the same one reset) reads from the beginning of the log and rebuilds views. This works because the log retains all events.

5. **Query Execution**: Queries are executed against the materialized views, not the raw event log.

```
Event Log (Kafka) ──> Stream Processor (Flink) ──> Queryable Views
                         ↑
                    (replay from any offset)
```

## Practical Applications

Kappa Architecture is well-suited for:

- **Real-Time Analytics Dashboards**: Always-current metrics derived from streaming events
- **Event-Sourced Systems**: Domains where audit trails and temporal queries are important
- **Data Warehouse Modernization**: Replacing batch ETL with continuous data ingestion
- **Machine Learning Feature Stores**: Maintaining up-to-date feature values for model inference
- **Audit and Compliance Systems**: Immutable event logs provide complete auditability

## Examples

Using Kafka Streams to implement a Kappa-style word count:

```java
KStreamBuilder builder = new KStreamBuilder();
KStream<String, String> textLines = builder.stream("input-topic");

KTable<String, Long> wordCounts = textLines
    .flatMapValues(textLine -> Arrays.asList(textLine.toLowerCase().split("\\W+")))
    .groupBy((key, word) -> word)
    .count("word-count-store");

wordCounts.to(Serdes.String(), Serdes.Long(), "word-count-output");
```

To reprocess: reset the consumer offset to the beginning and let the processor rebuild the state store.

## Comparison with Lambda Architecture

| Aspect | Lambda Architecture | Kappa Architecture |
|--------|--------------------|--------------------|
| Batch Layer | Yes, separate | No |
| Speed Layer | Yes, separate | No |
| Codebase | Two (batch + streaming) | One (streaming only) |
| Complexity | Higher (two systems) | Lower |
| Consistency | Must merge batch/speed | Single source of truth |
| Reprocessing | Requires batch job | Replay event log |
| Use Cases | Complex analytics with batch + real-time | Pure streaming workloads |

## Related Concepts

- [[Lambda Architecture]] - The older pattern Kappa simplifies
- [[Event Sourcing]] - Using events as the primary store of state
- [[Stream Processing]] - Technology for processing data streams
- [[Apache Kafka]] - Common event log implementation for Kappa
- [[Apache Flink]] - Stream processing engine often used with Kappa
- [[CQRS]] - Query side separation; Kappa can implement CQRS via materialized views

## Further Reading

- Jay Kreps' original blog post "Questioning the Lambda Architecture"
- "Streaming Systems" by Tyler Akidau et al.
- Apache Kafka documentation on stream processing

## Personal Notes

Kappa Architecture clicked for me when I realized we were maintaining nearly identical logic in Spark batch jobs and Storm streaming code. The bugs in one weren't in the other, and keeping them in sync was a constant source of friction. Migrating to a Kafka + Flink stack let us eliminate the batch layer entirely—reprocessing was just replaying Kafka offsets. The catch: stream processors must handle late-arriving data and state rebuilding carefully. Flink's checkpointing saved us there, but it's not trivial to configure correctly.
