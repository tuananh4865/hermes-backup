---
title: OpenTelemetry
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [opentelemetry, observability, tracing, metrics, monitoring]
---

# OpenTelemetry

## Overview

OpenTelemetry (OTel) is an open-source observability framework that provides a unified standard for collecting telemetry data including traces, metrics, and logs. Originally born from the merger of OpenCensus and OpenTracing in 2019, OpenTelemetry is now a CNCF incubating project that aims to make observability a first-class citizen in modern software systems. It enables developers to instrument their applications once and export telemetry data to any backend analysis system, avoiding vendor lock-in and providing flexibility in choosing observability tools.

The framework addresses a critical need in distributed systems: understanding how requests flow through multiple services, identifying performance bottlenecks, and diagnosing failures across complex architectures. As microservices and cloud-native deployments have become standard practice, the ability to trace requests across service boundaries has moved from nice-to-have to essential operations capability.

## Key Concepts

**Signals** are the three pillars of observability that OpenTelemetry standardizes. Traces track the progression of a request as it moves through multiple services, forming a causal chain of operations. Metrics are numerical measurements collected at intervals, such as CPU usage, request counts, or latency percentiles. Logs are timestamped text records emitted by applications, capturing discrete events and errors.

**Collectors** are middleware components that receive, process, and export telemetry data. The OpenTelemetry Collector can be deployed as an agent (sidecar) or as a standalone service, providing a buffer and processing pipeline between applications and backends. It supports various processors for batch handling, retries, and data transformation.

**Semantic Conventions** define a standardized naming and structure for common observability attributes, ensuring consistency across different services and languages. This standardization makes it easier to correlate data across systems and build通用的 dashboards and alerts.

## How It Works

Applications integrate OpenTelemetry through language-specific SDKs that provide APIs for instrumenting code. Instrumentation can be automatic ( bytecode injection, framework hooks) or manual (explicit span creation). When a request enters a service, the SDK creates a span representing that operation. If the request calls another service, the span context is propagated via HTTP headers (W3C Trace Context format).

```python
# Example: Manual instrumentation in Python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Nested spans for sub-operations
        with tracer.start_as_current_span("validate_inventory"):
            validate_inventory(order_id)
        
        with tracer.start_as_current_span("process_payment"):
            process_payment(order_id)
        
        return {"status": "completed"}
```

The SDK batches and exports spans to an endpoint (collector or direct to backend), where they can be visualized and analyzed. Backends like Jaeger, Zipkin, Prometheus, or commercial solutions consume the standardized format.

## Practical Applications

OpenTelemetry is essential in microservices architectures where a single user request might traverse dozens of services. Operations teams use it to understand latency contributions of each service, identify which dependencies are causing slowdowns, and establish baselines for normal behavior. During incident response, distributed traces provide the context needed to reconstruct exactly what happened.

Service level objectives (SLOs) rely on metrics exported via OpenTelemetry to track availability and performance against targets. Security teams can use trace data to detect anomalous patterns indicating attacks or data exfiltration.

## Examples

A typical e-commerce application might use OpenTelemetry to trace a purchase flow: from the frontend API gateway, through inventory service, payment processor, and order fulfillment. Each service contributes spans, and the resulting trace shows total duration and where time was spent.

Configuration for a Node.js application sending traces to a collector:

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
```

## Related Concepts

- [[observability]] — The broader discipline of understanding system behavior
- [[jaeger]] — Distributed tracing system often used with OpenTelemetry
- [[prometheus]] — Metrics collection and alerting (often paired with OTel)
- [[distributed-systems]] — Where observability becomes critical
- [[metrics]] — Quantitative measurements in observability

## Further Reading

- OpenTelemetry official documentation at opentelemetry.io
- CNCF OpenTelemetry project page
- OpenTelemetry Protocol (OTLP) specification

## Personal Notes

OpenTelemetry represents a significant step forward in standardizing observability across the industry. The once-fragmented landscape of proprietary agent formats and vendor-specific instrumentation libraries is giving way to a universal approach. I've found that investing time in proper span naming conventions and attribute standardization pays dividends when building dashboards that need to work across teams and services.
