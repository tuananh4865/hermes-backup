---
title: Distributed Tracing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [distributed-tracing, observability, microservices, tracing, opentracing, jaeger]
---

## Overview

Distributed tracing is an observability technique that tracks requests as they flow through a distributed system, providing end-to-end visibility into how a single transaction traverses multiple services, processes, and infrastructure components. In a microservices architecture, a single user request might touch dozens of services, each handling a portion of the work. Without distributed tracing, understanding why a request is slow or failing requires manually correlating logs across all affected services—a process that becomes increasingly difficult as system complexity grows.

The fundamental insight behind distributed tracing is that requests in a distributed system can be modeled as directed acyclic graphs (DAGs) of spans, where each span represents a unit of work performed by a single service or component. Spans are organized hierarchically by causality: a parent span creates child spans to represent nested work. The complete chain of spans from the initial request to all downstream services forms a trace, which captures the full journey of a transaction through the system.

Distributed tracing occupies a crucial position in the [[observability]] triad alongside metrics and logs. While metrics aggregate quantitative measurements over time and logs record discrete events, distributed traces provide the connective tissue—the ability to follow a specific request through its entire journey and understand the relationships between components. This makes distributed tracing particularly valuable for debugging latency issues, understanding system dependencies, and validating complex [[microservices]] interactions.

The OpenTelemetry project has become the dominant standard for distributed tracing instrumentation, providing vendor-neutral APIs, SDKs, and collectors that enable applications to emit tracing data to backends like Jaeger, Zipkin, Tempo, or commercial solutions. This standardization has dramatically reduced the friction of implementing distributed tracing, as organizations can switch tracing backends without changing application code.

## Key Concepts

Distributed tracing builds on several foundational concepts that work together to provide end-to-end visibility.

**Trace** is the complete record of a request's journey through a distributed system. A trace is identified by a unique trace ID that is generated at the entry point of the system (typically when an HTTP request arrives) and propagated through all subsequent service calls. All spans belonging to the same logical request share this trace ID, enabling observability platforms to reconstruct the full request path. Traces capture both the timing of operations and the causal relationships between them.

**Span** is the fundamental unit of work in distributed tracing, representing a single operation within a trace. Each span has a name identifying the operation (such as `http.request`, `db.query`, or `process_order`), start and end timestamps, optional attributes providing additional context, and a span ID unique within the trace. Spans form a tree structure where parent spans have zero or more child spans representing nested operations. A span for an HTTP request might have child spans for authentication, database queries, and external API calls.

**Span Context** is the metadata that enables spans to be connected across process boundaries. It consists of the trace ID, the span ID of the parent span, and sampling flags. When a service makes a remote call, it injects the span context into the request (for example, as HTTP headers), and the receiving service extracts the context to create a child span linked to the original trace. This propagation mechanism is what enables traces to span multiple processes and network boundaries.

**Instrumentation** is the process of adding tracing code to applications and libraries. Instrumentation can be automatic (using language-specific libraries that automatically wrap common operations like HTTP calls, database queries, and message queue operations) or manual (where developers explicitly create spans around specific code paths). Auto-instrumentation provides immediate value with minimal effort, while manual instrumentation enables detailed visibility into domain-specific operations. Popular auto-instrumentation libraries exist for Python, Java, Node.js, Go, Ruby, and most other major languages.

## How It Works

The mechanics of distributed tracing involve instrumentation, context propagation, and trace collection working together.

```python
# Manual distributed tracing with OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import requests

# Initialize tracer provider
trace.set_tracer_provider(TracerProvider())

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Get tracer for creating spans
tracer = trace.get_tracer(__name__)

# Propagator for context injection/extraction
propagator = TraceContextTextMapPropagator()

def call_downstream_service(url: str, data: dict):
    """Example of manual instrumentation with context propagation"""
    with tracer.start_as_current_span("call_downstream_service") as span:
        span.set_attribute("http.url", url)
        span.set_attribute("http.method", "POST")
        
        # Inject context into HTTP headers
        headers = {}
        propagator.inject(headers)
        
        response = requests.post(url, json=data, headers=headers)
        span.set_attribute("http.status_code", response.status_code)
        
        if response.status_code >= 400:
            span.set_attribute("error", True)
            span.record_exception(Exception(f"HTTP {response.status_code}"))
        
        return response.json()

def process_user_order(order_id: str):
    """Parent span that calls downstream services"""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Create child span for validation
        with tracer.start_as_current_span("validate_order") as child:
            child.set_attribute("validation.type", "business_rules")
            is_valid = validate_order(order_id)
            if not is_valid:
                span.record_exception(Exception("Order validation failed"))
                return {"error": "validation_failed"}
        
        # Call payment service
        payment_result = call_downstream_service(
            "http://payment-service/charge",
            {"order_id": order_id, "amount": 99.99}
        )
        
        # Call inventory service
        inventory_result = call_downstream_service(
            "http://inventory-service/reserve",
            {"order_id": order_id}
        )
        
        return {"status": "processed", "payment": payment_result, "inventory": inventory_result}
```

In this example, the `process_order` function creates a parent span that encompasses the entire order processing operation. Child spans are created for validation and for calls to downstream services. When calling the downstream service, the span context is injected into HTTP headers (via the `TraceContextTextMapPropagator`), allowing the downstream service to create a properly linked child span. The Jaeger exporter batches these spans and sends them to the tracing backend, where they can be visualized and queried.

## Practical Applications

Distributed tracing has become essential for operating complex distributed systems, with applications ranging from development debugging to production incident response.

**Latency Debugging** is one of the most common use cases for distributed tracing. When a user reports that an API request is slow, engineers can look at the trace to identify which specific span took the most time. The hierarchical span structure makes it immediately obvious whether the bottleneck is in the initial service, a specific downstream dependency, or a particular database query. Without tracing, this investigation would require examining logs from potentially dozens of services and manually correlating timestamps—a process that could take hours.

**Production Traffic Analysis** with sampling enables understanding of system behavior under real load without storing traces for every single request. Production systems often use head-based or tail-based sampling to store traces for a representative subset of requests. Head-based sampling makes the sampling decision at the start of a trace, while tail-based sampling makes the decision after the trace completes, allowing intelligent sampling of only anomalous or interesting traces.

**Dependency Mapping** is a natural byproduct of distributed tracing data. By analyzing which services call which other services, organizations can automatically generate and maintain service dependency maps. These maps are crucial for understanding system architecture, planning changes, and identifying potential cascading failure risks. When combined with span-level timing data, dependency maps also reveal which dependencies are performance-critical.

**Error Correlation** enables engineers to understand exactly how an error in one service propagates to affect other services and ultimately impact users. When a downstream service throws an exception, the error is recorded on the span where it occurred. Because spans are linked through parent-child relationships, observability platforms can trace the error back through the call chain to find the root cause, even if the error manifests as a timeout or HTTP 500 several layers up the call stack.

## Examples

A practical example shows how distributed tracing helps debug a complex multi-service interaction.

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
Service: api-gateway | Duration: 847ms

├── Span: authenticate_user | Duration: 12ms
│   └── Span: db.query | Duration: 8ms
├── Span: fetch_product_catalog | Duration: 234ms
│   ├── Span: cache.lookup | Duration: 2ms
│   └── Span: db.query (cache miss) | Duration: 228ms  ⚠️ SLOW
├── Span: calculate_pricing | Duration: 156ms
│   ├── Span: discount_service.call | Duration: 145ms  ⚠️ SLOW
│   └── Span: tax_calculator | Duration: 10ms
├── Span: payment_service.charge | Duration: 289ms
│   ├── Span: payment_gateway.call | Duration: 245ms
│   └── Span: idempotency_check | Duration: 12ms
└── Span: inventory_service.reserve | Duration: 89ms
```

In this trace visualization, the engineer can immediately see that the two slowest operations are the `db.query (cache miss)` at 228ms and the `discount_service.call` at 145ms. The `discount_service.call` is particularly suspicious because it's an external service call that takes 145ms—close to the total duration of the entire `calculate_pricing` span. This trace points directly to two optimization opportunities: improving the cache hit rate for product catalog queries and investigating why the discount service is slow.

## Related Concepts

- [[observability]] — The broader discipline that distributed tracing supports
- [[microservices]] — Architecture style where distributed tracing is essential
- [[service-mesh]] — Infrastructure that often provides automatic distributed tracing
- [[OpenTelemetry]] — The dominant open standard for tracing instrumentation
- [[Jaeger]] — Popular distributed tracing backend system
- [[metrics]] — Complimentary observability signal type
- [[logging]] — Complimentary observability signal type

## Further Reading

- "Distributed Tracing" — OpenTelemetry documentation on tracing concepts
- "Learning OpenTelemetry" — Comprehensive guide to modern tracing
- "Observability Engineering" — Book covering tracing, metrics, and logs
- "Tracing the Path" — LightStep blog series on distributed tracing fundamentals

## Personal Notes

Distributed tracing is one of those tools where the value is hard to appreciate until you've tried debugging a complex production issue without it. Before tracing, I spent hours correlating logs. With tracing, the same debugging session takes minutes. My advice: start with auto-instrumentation for HTTP and database calls, then add manual spans for your business logic. Don't try to instrument everything at once—the key is to instrument enough to get visibility into the critical paths first.
