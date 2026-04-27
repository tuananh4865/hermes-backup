---
title: Tracing
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [tracing, observability, debugging, distributed-systems]
---

## Overview

Tracing is a method of [[observability]] that provides visibility into the flow of requests as they propagate through a distributed system. Unlike traditional logging, which captures discrete events, tracing tracks the complete journey of a request across multiple services, components, and network boundaries. This makes tracing especially valuable in modern architectures built around [[microservices]], where a single user action can trigger dozens of interdependent service calls.

Tracing falls under the three pillars of observability, alongside [[metrics]] and [[logging]]. While metrics provide quantitative measurements and logs offer detailed event records, traces deliver contextual insight into causally related operations. The result is that engineers can understand not just that a system behaved incorrectly, but exactly where and why the failure occurred.

Distributed tracing has become essential as systems scale horizontally and communication patterns grow more complex. Without tracing, debugging performance issues in production environments would require significant manual effort, correlating logs across dozens of services, and reconstructing request flows from fragmented evidence.

## How It Works

Tracing operates through two fundamental concepts: traces and spans. A trace represents the complete lifecycle of a request from initiation to completion. It serves as a container for all related operations and carries a unique identifier that propagates through the system.

A span is the fundamental unit of work within a trace. Each span represents a discrete operation or unit of work, such as an HTTP request, database query, or function execution. Spans capture key metadata including the operation name, start and end timestamps, potential error conditions, and parent-child relationships. This hierarchical structure allows spans to be nested, reflecting the call tree of the underlying system.

When a request enters a system, the tracing framework creates a new trace and root span. As the request travels between services, correlation identifiers are propagated via HTTP headers or message queue metadata. Each service contributes its own span, establishing the causal chain. At the end of the request lifecycle, all spans are assembled to reconstruct the full request path.

This data enables several powerful capabilities. Engineers can identify which operations consume the most time, detect where errors occur, understand service dependencies, and reconstruct exact request paths through the system.

## Tools

Several specialized tools exist for collecting, storing, and visualizing trace data.

[[Jaeger]] is an open-source distributed tracing system originally developed by Uber. It provides real-time distributed tracing, transaction monitoring, and root cause analysis. Jaeger supports multiple storage backends and offers a web-based UI for exploring traces.

[[Zipkin]] is another prominent open-source tracing system, originally created at Twitter. It uses a collector to gather trace data, which can then be queried through a web interface or API. Zipkin has a rich ecosystem of integrations and supports multiple instrumentation libraries.

[[OpenTelemetry]] has emerged as the industry standard for observability instrumentation. It provides unified APIs, SDKs, and language-specific implementations for generating trace data, alongside metrics and logs. OpenTelemetry's vendor-neutral design allows organizations to switch between different tracing backends without changing application code. It has largely superseded earlier approaches and is now the recommended approach for new observability implementations.

## Related

Tracing connects closely to broader [[observability]] practices and the concept of the [[observability pipeline]]. Effective tracing implementations often work alongside [[structured logging]] and [[metrics collection]] to provide comprehensive system visibility. The practice is especially relevant in [[microservices]] architectures where [[service mesh]] technologies frequently provide built-in tracing capabilities.
