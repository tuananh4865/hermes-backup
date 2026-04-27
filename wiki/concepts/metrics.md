---
title: Metrics
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [metrics, monitoring, observability]
---

# Metrics

## Overview

Metrics are numerical measurements that quantify the behavior, performance, and health of systems, applications, and infrastructure. In the context of software engineering and operations, metrics provide objective, quantifiable data points that enable teams to understand how their systems behave under various conditions. Unlike logs, which capture discrete events, or traces, which follow requests through a system, metrics represent aggregated measurements over time. This makes them particularly valuable for detecting trends, establishing baselines, and triggering automated alerts when values deviate from expected ranges.

Metrics serve as the foundation of any robust monitoring and observability strategy. They transform complex system behavior into manageable numbers that can be stored efficiently, queried rapidly, and visualized in dashboards. Whether tracking the number of requests per second handled by a web server, measuring the latency distribution of database queries, or monitoring CPU utilization on production hosts, metrics provide the quantitative insight needed to operate reliable systems at scale.

## Key Concepts

Understanding metrics requires familiarity with several foundational concepts that determine how metrics are collected, stored, and interpreted.

**Cardinality** refers to the number of unique time series a metric can generate. High-cardinality metrics, such as those with user IDs or request IDs as labels, can grow exponentially and strain storage systems. Low-cardinality metrics, like server-level CPU usage, are more predictable and easier to aggregate.

**Granularity** defines the interval at which metrics are sampled or reported. High-resolution metrics (e.g., every 10 seconds) provide fine-grained visibility but consume more storage. Lower resolution (e.g., every 5 minutes) reduces costs but may miss short-lived spikes or anomalies.

**Aggregation** is the process of combining multiple data points into summary statistics. Common aggregations include sum, count, average, min, max, and percentiles (p50, p95, p99). The choice of aggregation affects what you can learn from the data and how it scales.

**Metric Types** typically fall into several categories: counters (incrementing values like request counts), gauges (point-in-time values like current memory usage), histograms (distributions of values like response times), and rate metrics (derivatives that measure change over time).

## How It Works

Metrics collection typically follows a push or pull model. In the pull model, a monitoring system periodically scrapes metrics endpoints exposed by applications and infrastructure components. This is the pattern used by Prometheus, where targets expose a `/metrics` endpoint that the server scrapes at regular intervals. In the push model, applications and services actively send metrics to a central collector. Systems like StatsD and the Graphite protocol use this approach, where clients emit metrics to a gateway that forwards them to storage.

Once collected, metrics are typically stored in time-series databases (TSDB) optimized for append-heavy workloads and time-range queries. Popular options include Prometheus (which uses a custom TSDB), InfluxDB, TimescaleDB, and cloud-native solutions like Amazon CloudWatch and Google Cloud Monitoring. These systems support efficient querying for visualization and alerting.

Query languages allow engineers to filter, aggregate, and transform metrics. PromQL (Prometheus Query Language) enables powerful expressions like calculating request latency percentiles across all instances, or detecting when error rates exceed a threshold. Grafana provides visualization layers that consume these queries and render dashboards.

## Practical Applications

Metrics are indispensable across virtually every operational scenario. They form the backbone of Service Level Objectives (SLOs), where teams define target values for metrics like availability and latency. Dashboards display these metrics in real-time, and alerting rules automatically notify on-call engineers when SLOs are at risk.

Capacity planning relies heavily on metrics to predict future resource needs. By analyzing trends in request volume, storage consumption, and computational load, teams can provision infrastructure proactively rather than reactively. Metrics also guide right-sizing decisions, helping organizations avoid paying for unused capacity.

Anomaly detection systems use metrics to identify unusual behavior. Machine learning models can establish baselines for expected values and flag deviations that might indicate security threats, performance degradation, or impending failures. For example, a sudden spike in failed login attempts might signal a credential stuffing attack.

Incident response benefits from metrics that provide context during outages. When a service begins failing, metrics reveal whether the problem is localized (one instance) or widespread (all instances), whether it correlates with deployment changes, and which specific error types are occurring.

## Examples

Here is a practical example of how metrics might be defined in a Prometheus-compatible format for a simple HTTP server:

```promql
# Counter for total HTTP requests
http_requests_total{method="GET", status="200"}

# Histogram for request duration
http_request_duration_seconds{method="GET", handler="/api/users"}

# Gauge for current active connections
http_connections_active{state="active"}
```

Querying these metrics reveals insights:

```promql
# Calculate request rate per second over the last 5 minutes
rate(http_requests_total[5m])

# Get p99 latency for the user API handler
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{handler="/api/users"}[5m]))

# Alert when error rate exceeds 1%
(
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
) > 0.01
```

## Related Concepts

Metrics connect to several other observability and monitoring concepts:

- [[observability]] — The broader discipline of understanding system behavior from its outputs, with metrics as one of three pillars (alongside logs and traces)
- [[metrics-collection]] — The specific processes and tools used to gather metrics from systems
- [[alerting]] — Using metrics thresholds to trigger notifications
- [[dashboards]] — Visual representations of metrics data
- [[slo]] — Service Level Objectives, which define target values for key metrics
- [[tracing]] — Distributed tracing complements metrics by providing request-level visibility

## Further Reading

- "Monitoring and Observability" by Charity Majors and Liz Fong-Jones
- Prometheus documentation on metric types
- Google SRE Handbook chapters on monitoring distributed systems

## Personal Notes

Metrics represent one of the most cost-effective investments in system reliability. The key is starting with business-relevant metrics rather than trying to monitor everything. Focus on the four golden signals: latency, traffic, errors, and saturation. From there, expand based on what questions your team actually needs to answer during incidents and planning sessions.
