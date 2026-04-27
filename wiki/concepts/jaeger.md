---
title: Jaeger
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [jaeger, tracing, observability, distributed-systems, microservices]
---

# Jaeger

Jaeger is an open-source distributed tracing system originally developed by Uber Technologies and now part of the Cloud Native Computing Foundation (CNCF). It provides comprehensive monitoring and troubleshooting capabilities for complex distributed systems, particularly microservices architectures. By capturing the flow of requests as they traverse multiple services, Jaeger enables developers and operators to understand system behavior, identify performance bottlenecks, and diagnose failures in production environments.

## Overview

Modern applications often consist of dozens or hundreds of microservices that communicate through APIs, message queues, and databases. When a user request慢 experiences a problem—whether slow performance, errors, or complete failure—determining which service is responsible becomes extraordinarily difficult. Distributed tracing addresses this by assigning each request a unique identifier and tracking its progression through the entire system as a cohesive unit called a trace.

Jaeger follows the OpenTracing standard and is designed for cloud-native environments. It collects trace data from instrumented applications, stores it efficiently, and provides a rich UI for visualization and analysis. The system handles high-volume trace data with sampling strategies that balance detail against storage costs, ensuring that even in high-traffic systems, critical traces are captured while routine ones are sampled.

## Key Concepts

**Traces and Spans** form the fundamental data model in distributed tracing. A trace represents the complete journey of a request through the system, while each individual operation (an HTTP handler, database call, or external API invocation) becomes a span within that trace. Spans contain timing information, metadata, and references to parent spans, creating a directed acyclic graph (DAG) that shows the structure of the request's execution.

**Context Propagation** is the mechanism that maintains trace continuity across service boundaries. When a service calls another service, trace context (trace ID, span ID, and sampling decision) must be passed along, typically via HTTP headers or message queue metadata. Jaeger supports multiple propagation formats including Zipkin's B3 headers and W3C Trace Context.

**Sampling Strategies** determine which traces are collected and stored. Naive sampling captures a fixed percentage of all traces. Rate limiting sampling ensures a minimum number of traces per second. Adaptive sampling adjusts rates based on traffic patterns, capturing more traces during unusual activity. Tail-based sampling captures complete traces for requests matching specific criteria (like errors or slow responses) even if other similar requests were sampled out.

## How It Works

Instrumenting applications to work with Jaeger typically involves adding client libraries in the application's language. Popular frameworks include OpenTelemetry SDK, which provides vendor-agnostic instrumentation that can send traces to Jaeger. Services are instrumented at key points: incoming HTTP requests, outgoing HTTP calls, database operations, and message queue interactions.

The Jaeger collector receives traces from instrumented applications, validates them, and stores them in a backend database. Jaeger supports Elasticsearch, Cassandra, and Kafka as storage backends, with different tradeoffs around scalability, operational complexity, and cost. The query service retrieves traces from storage and serves the Jaeger UI, which provides multiple views for analyzing trace data.

## Practical Applications

Distributed tracing with Jaeger is essential for microservices debugging and performance optimization. Teams use it to understand why specific requests are slow by identifying which service or operation introduces latency. When errors occur, traces reveal the full error chain across services. Capacity planning benefits from understanding request flows and resource consumption patterns. New team members use traces to understand system architecture and dependencies.

Jaeger integrates with [[observability]] ecosystems including metrics systems (like Prometheus) and logging systems (like Loki or ELK). The three pillars of observability—metrics, logs, and traces—work together to provide complete visibility into system behavior. Traces often serve as the entry point for investigation, linking to related metrics and logs for deeper diagnosis.

## Examples

Instrumenting a Node.js application with OpenTelemetry and Jaeger:
```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');

const jaegerExporter = new JaegerExporter({
  endpoint: 'http://jaeger-collector:14268/api/traces',
});

const sdk = new NodeSDK({
  traceExporter: jaegerExporter,
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

Viewing trace data via Jaeger UI:
```
Search for traces by:
- Service name
- Operation name
- Trace ID
- Time range
- Tag filters (error=true, http.status_code=500)
```

## Related Concepts

- [[observability]] — System visibility and monitoring
- [[metrics]] — Quantitative measurements
- [[distributed-systems]] — Multi-service architectures
- [[microservices]] — Service-oriented architecture
- [[opentracing]] — Distributed tracing standard

## Further Reading

- Jaeger Documentation — Official getting started and reference materials
- OpenTelemetry — Vendor-neutral observability instrumentation
- "Distributed Systems Observability" by Cindy Sridharan — Comprehensive guide to observability practices

## Personal Notes

Jaeger has become my go-to tool for understanding complex service interactions. The dependency graph view is particularly valuable for visualizing system architecture without needing separate service discovery documentation. One gotcha: in high-throughput systems, sampling configuration is critical—capturing too many traces overwhelms storage, while too few may miss important edge cases. Start with aggressive sampling and refine based on actual debugging needs.
