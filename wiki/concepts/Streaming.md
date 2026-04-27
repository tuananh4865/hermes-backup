---
title: Streaming
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [streaming, data-engineering, real-time, pipelines]
---

# Streaming

## Overview

Data streaming, also known as stream processing, is a paradigm for processing data in motion rather than in batches. In streaming architectures, data is continuously generated, typically by external sources such as sensors, web applications, financial transactions, or social media feeds, and processed in real time as it arrives. The defining characteristic is that each data element is processed shortly after generation, enabling immediate insights and actions based on the most current information available.

Unlike traditional batch processing where data is collected over a period and processed in discrete chunks, streaming processing treats data as an unbounded, continuous flow. This approach imposes different design constraints and offers different trade-offs. Systems must handle potentially infinite streams of data while maintaining low latency between ingestion and output. The state may be ephemeral, computed from a sliding window of recent events, or maintained durably across the lifetime of a processing job.

Streaming systems typically consist of several key components: sources (where data originates), processors (transformations, aggregations, joins), and sinks (destinations for processed data). The abstraction hides much of the complexity around parallel processing, fault tolerance, and state management, allowing developers to focus on business logic rather than infrastructure concerns.

## Stream vs Batch

The distinction between streaming and batch processing reflects fundamentally different philosophies about how and when data should be processed.

**Batch processing** collects data over time, accumulates it into groups, and processes these groups in discrete intervals. This approach suits operations where complete datasets are required, such as end-of-day financial reconciliation, large-scale ETL transformations, or generating daily reports. Batch systems can often achieve higher throughput by processing data in bulk and can optimize resource utilization by scheduling jobs during off-peak hours. However, batch processing introduces latency measured in hours or days, making it unsuitable for use cases requiring immediate response.

**Stream processing** handles data as it arrives, with latency measured in milliseconds to seconds. This enables use cases like real-time fraud detection, where transactions must be evaluated immediately, or live dashboards that reflect current system state. Stream processing naturally handles unbounded datasets without requiring periodic restarts or batch windows. The trade-off is added complexity in handling out-of-order events, managing state across time, and ensuring exactly-once processing semantics.

Modern data architectures often combine both paradigms. The [[lambda architecture]] approach layers streaming and batch systems to balance latency and correctness, while the [[kappa architecture]] favors a pure streaming approach using log-based systems as the source of truth. Choosing between them depends on use case requirements, data volume, and operational complexity tolerance.

## Frameworks

Several frameworks have emerged as standard tools for building streaming data pipelines, each offering different trade-offs in programming model, scalability, and operational complexity.

**Apache Kafka Streams** is a lightweight, library-style framework built on top of Apache Kafka. It allows developers to build applications that consume from Kafka topics, process data, and produce to other topics using familiar functional programming concepts. Kafka Streams excels in scenarios where Kafka is already the messaging backbone, offering seamless integration, exactly-once semantics, and deployment simplicity as standalone Java applications without requiring a separate cluster manager. Its state stores enable powerful stateful operations like joins and aggregations while maintaining fault tolerance through Kafka's partitioned log model.

**Apache Flink** is a full-featured stream processing framework that operates as a cluster application. Flink supports both streaming and batch workloads, treating batch processing as a special case of streaming with bounded input. It provides sophisticated windowing semantics, sophisticated event time processing with watermarks, and a rich set of operators for complex event processing. Flink's checkpointing mechanism enables exactly-once state consistency even in the presence of failures. Organizations running Flink typically deploy it on Kubernetes, YARN, or standalone clusters, accepting greater operational complexity in exchange for expressive capability.

Other notable frameworks include **Apache Spark Streaming** (which uses micro-batching rather than true streaming), **Apache Storm** (low-latency but higher operational overhead), and cloud-native options like **AWS Kinesis Data Analytics** and **Google Cloud Dataflow**.

## Use Cases

Streaming data processing powers a wide range of modern applications where real-time insights and actions provide business value.

**Fraud detection** in financial services processes transaction streams to identify suspicious patterns in real time, blocking fraudulent transactions before they complete. This requires sub-second latency and the ability to correlate current transactions with historical patterns.

**Operational monitoring and alerting** systems track metrics from infrastructure, applications, and business processes. Streams of log events, metrics, and traces are analyzed to detect anomalies, predict failures, and trigger alerts before issues impact users.

**Real-time analytics and dashboards** display current business metrics, website traffic patterns, or social media sentiment as data arrives. Rather than waiting for daily reports, stakeholders can monitor business health continuously and respond quickly to changing conditions.

**Personalization and recommendation engines** process user behavior events in real time to update user profiles and deliver immediately relevant content or recommendations. This creates more responsive, engaging user experiences compared to batch-computed recommendations that may be hours old.

**Internet of Things (IoT)** applications ingest sensor data from connected devices, enabling real-time monitoring, predictive maintenance, and automated control of industrial processes, smart buildings, and autonomous vehicles.

## Related

- [[Lambda Architecture]] - Combining batch and stream processing layers
- [[Kappa Architecture]] - Pure streaming approach using log-based systems
- [[Apache Kafka]] - Distributed event streaming platform commonly used as streaming infrastructure
- [[Real-Time Processing]] - Broader concept of immediate data processing
- [[Data Pipelines]] - Automated data flow systems that often incorporate streaming
- [[Complex Event Processing]] - Detecting patterns across streaming data events
