---
title: Zipkin
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [zipkin, tracing, observability, distributed-systems, debugging]
---

# Zipkin

## Overview

Zipkin is an open-source distributed tracing system originally developed by Twitter and modeled after Google's Dapper paper. It is designed to help developers gather timing data across multiple services in a microservices architecture, making it easier to understand the flow of requests and diagnose latency bottlenecks. Zipkin provides a clean UI for exploring traces, a collector for aggregating trace data, and support for multiple storage backends including in-memory, MySQL, PostgreSQL, Elasticsearch, and Cassandra.

In a distributed system, a single user request might traverse dozens of services—API gateways, authentication services, business logic services, databases, and external APIs. When such a request is slow or fails, pinpointing the culprit is extraordinarily difficult without instrumentation. Zipkin addresses this by assigning each request a unique trace ID and propagating it through every service, with each service recording spans that represent individual operations. These spans capture timing information, annotations, and metadata that together form a complete picture of the request's journey.

## How It Works

Zipkin operates on a client-server model. Applications instrument their code with Zipkin client libraries (available for Java, Python, Go, Node.js, Ruby, and other languages) that intercept inbound and outbound requests and record timing data. Each unit of work within a trace is called a span—a named, timed operation representing a segment of the request path.

When a request enters the system, the first service creates a trace with a unique 64-bit or 128-bit trace ID. As the request flows to downstream services, the trace ID is propagated via HTTP headers (typically `B3` headers like `X-B3-TraceId` and `X-B3-SpanId`) or messaging headers. Each service adds its own span to the trace, noting the start and end time, any annotations (like "server received" or "client sent"), and key-value tags.

```
# Example B3 headers propagated across services
X-B3-TraceId: 4bf92f3577b34da6a3ce929d0e0e4736
X-B3-SpanId: 00f067aa0ba902b7
X-B3-ParentSpanId: 4bf92f3577b34da6
X-B3-Sampled: 1
```

The spans are sent asynchronously to the Zipkin collector, which stores them in the configured backend. The Zipkin UI then allows developers to query traces by trace ID, service name, duration, or timestamp, displaying a waterfall diagram of all spans within a trace.

## Key Concepts

**Trace** — A complete end-to-end request path, identified by a single trace ID. A trace consists of one or more spans organized in a parent-child hierarchy.

**Span** — A single unit of work within a trace, representing an operation (such as an HTTP request, database query, or function call) with timing data and optional metadata. Spans have a name, start and end timestamps, a span ID, and optionally a parent span ID.

**Annotations** — Timestamped events within a span, such as `cs` (Client Send), `cr` (Client Received), `ss` (Server Start), and `sr` (Server Receive). These are used to calculate the duration between client and server interactions.

**Context Propagation** — The mechanism by which trace and span IDs are passed between services. Zipkin uses a `TraceContext` to carry this information, typically via HTTP headers or message bus headers.

## Practical Applications

Zipkin is particularly valuable in complex microservices environments where requests span dozens of services. Development teams use it to identify which service is causing latency in a slow request. Operations teams use it to establish baseline performance and alert on anomalies. SREs use Zipkin traces to conduct post-incident analysis and understand failure propagation.

It integrates well with popular frameworks through auto-instrumentation modules. Spring Boot applications can enable Zipkin tracing with minimal configuration using `spring-cloud-sleuth-zipkin`. In Kubernetes environments, Zipkin can be deployed alongside service meshes that handle trace context propagation transparently.

## Examples

A typical trace for an e-commerce checkout request might look like this:

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
  Span: api-gateway (12ms)
    Span: auth-service (3ms)
    Span: cart-service (8ms)
      Span: inventory-db (2ms)
      Span: pricing-service (5ms)
    Span: payment-service (45ms)
      Span: payment-gateway (40ms)
```

This waterfall view immediately shows that `payment-service` (45ms) and its downstream `payment-gateway` (40ms) are the primary contributors to latency in this request.

## Related Concepts

- [[jaeger]] — Another popular open-source distributed tracing system from Uber
- [[opentelemetry]] — The emerging standard for observability instrumentation, which supports Zipkin as a exporter
- [[observability]] — The broader discipline of understanding system state from outputs
- [[tracing]] — Distributed tracing as a practice
- [[microservices]] — The architectural style Zipkin is most commonly used to observe

## Further Reading

- Zipkin Official Documentation
- Dapper Paper (Google): Large-Scale Distributed Systems Tracing
- OpenZipkin Community Repositories

## Personal Notes

I've used Zipkin on a few microservices projects and found it invaluable during debugging. The waterfall view is particularly intuitive for explaining latency issues to stakeholders who aren't familiar with distributed tracing concepts. One gotcha to keep in mind: in high-throughput systems, ensure sampling is configured appropriately—tracing every single request can introduce significant overhead and storage costs. Most teams sample between 1% and 10% of requests while ensuring all slow or errored requests are always captured.
