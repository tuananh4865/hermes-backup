---
title: "Graphite"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [monitoring, observability, time-series, metrics, graphing]
---

# Graphite

## Overview

Graphite is an enterprise-scale monitoring tool that tracks and graphs the performance of computer systems and networks. Originally created by Orbitz Worldwide in 2006 and later released as open-source, Graphite was one of the pioneering time-series monitoring platforms that demonstrated the value of storing numerical metrics over time and rendering them as interactive charts. Despite the emergence of newer tools like [[Prometheus]] and [[InfluxDB]], Graphite remains widely deployed in legacy infrastructure and continues to serve as the backend for many monitoring pipelines.

The architecture separates metric collection, storage, and visualization into distinct components. Applications send numeric time-series data to the Graphite Carbon daemon, which stores metrics in a specialized time-series database using the Whisper library. The Graphite Web application then queries this stored data and renders graphs through a simple but powerful interface or via its HTTP API.

Graphite introduced many conventions that persist today, including the dot-separated metric naming hierarchy (e.g., `web-server-01.cpu-usage.user`), the concept of rolling time-series retention policies, and the Graphite Render API that most modern monitoring tools eventually emulate.

## Key Concepts

**Metric Naming Hierarchy**: Graphite uses dot-separated path names to organize metrics into a hierarchical tree structure. For example: `production.web.frontend-01.cpu.user`. This hierarchy enables intuitive organization and wildcard queries (e.g., `production.web.*.cpu.*`) to aggregate or select specific metric branches. The convention encourages descriptive naming that reflects infrastructure topology.

**Whisper Database**: Whisper is Graphite's fixed-size time-series database library. Unlike traditional databases that grow indefinitely, Whisper allocates fixed-size files per metric with configurable retention policies. Data is stored in rounded time buckets (e.g., 1-minute resolution for recent data, 5-minute resolution for older data), and when storage limits are reached, older data is automatically aggregated and discarded. This design ensures predictable storage usage.

**Carbon Daemons**: Carbon is the collection agent that receives metrics over the network. The main `carbon-cache.py` daemon listens on port 2003 for plaintext metrics (the standard format applications use to push data) and port 2004 for pickle protocol (a more efficient binary format). A separate `carbon-relay.py` distributes metrics across multiple backends for horizontal scaling.

**Graphite Render API**: The HTTP API generates graphs and retrieves metric data. URL-based queries like `/render?target=sumSeries(production.web.*.cpu.user)&from=-1h&until=now&format=json` return data in various formats (PNG images, SVG, JSON, CSV). This API powers countless dashboards and alerting systems.

## How It Works

Graphite's data flow follows a straightforward pipeline:

1. **Emission**: Applications instrumented with Graphite client libraries send metrics using the plaintext protocol: `metric.path value timestamp\n`. Many languages have official or community clients (Python, Go, Java, Ruby, Node.js). Alternatively, tools like StatsD act as aggregators that batch and forward metrics.

2. **Collection**: Carbon daemon listens on configured ports and receives emitted metrics. It validates metric names, resolves the storage location based on the metric path, and writes data points to the appropriate Whisper files. The daemon handles thousands of metrics per second.

3. **Storage**: Whisper files store metrics with predefined retention. A typical configuration might retain 1-minute resolution for 7 days, 5-minute resolution for 30 days, and 1-hour resolution for 5 years. Older data beyond the highest resolution is discarded automatically.

4. **Visualization**: The Graphite Web application (written in Django) queries Whisper files through the storage finder abstraction and renders results. Users build graphs interactively in the browser, configure functions (sum, average, alias, scale), and save dashboard configurations.

```
# Example: Sending metrics to Graphite
echo "production.web.frontend-01.cpu.user 45.2 $(date +%s)" | nc localhost 2003
echo "production.web.frontend-01.memory.used 8142 $(date +%s)" | nc localhost 2003
```

## Practical Applications

Graphite serves as the historical backbone for many monitoring and observability platforms.

**Infrastructure Monitoring**: Tracking server-level metrics like CPU, memory, disk I/O, and network throughput. The hierarchical naming scheme naturally maps to infrastructure topology, making it easy to aggregate metrics across servers, services, or regions.

**Application Performance Monitoring**: Custom application metrics (request latencies, error counts, queue depths) can be sent directly to Graphite. Business metrics like user signups or transaction volumes integrate seamlessly with the same pipeline.

**Capacity Planning**: Historical metric data enables trend analysis for capacity planning. Understanding how CPU usage grows over months helps predict when additional infrastructure will be needed.

## Examples

A complete Graphite dashboard configuration for web server monitoring:

```python
# Graphite function composition for dashboard
# Average CPU across all web servers
target = 'averageSeries(production.web.*.cpu.user)'

# Error rate (5xx responses / total requests * 100)
target = [
    'scale(production.web.*.http.status.5xx, 100)',
    'divideSeries(production.web.*.http.requests)'
]

# Memory usage with threshold annotation
target = 'aliasByMetric(production.web.*.memory.used)'
```

```bash
# Query Graphite API for JSON data
curl "http://localhost:8080/render/?target=production.web.frontend-01.cpu.user&from=-1h&format=json"

# Output
[{
    "target": "production.web.frontend-01.cpu.user",
    "datapoints": [[45.2, 1642008000], [46.1, 1642008060], ...]
}]
```

## Related Concepts

- [[Prometheus]] - Modern CNCF graduated monitoring system
- [[Grafana]] - Visualization platform often used with Graphite
- [[StatsD]] - Metric aggregation proxy that forwards to Graphite
- [[InfluxDB]] - Time-series database alternative to Whisper
- [[Time Series Database]] - The storage paradigm
- [[Observability]] - The discipline Graphite enables
- [[Whisper]] - Graphite's storage format

## Further Reading

- [Graphite Documentation](https://graphite.readthedocs.io/)
- [Graphite Wiki](https://github.com/graphite-project/graphite-web)
- [Installing and Configuring Graphite](https://graphite.readthedocs.io/en/stable/install.html)
- [Best Practices for Graphite](https://graphite.readthedocs.io/en/stable/config-p递归ursive.html)

## Personal Notes

Graphite's strength is its simplicity and proven reliability at scale. The plaintext protocol makes integration trivial—any system that can open a TCP socket can send metrics. However, Graphite lacks built-in alerting (requiring tools like Grafana or separate alerters), and the query language, while functional, is less powerful than PromQL. For greenfield projects, [[Prometheus]] is usually the better choice, but understanding Graphite remains valuable for working with legacy systems. The whisper occupancy tool (`whisper-info.py`) helps diagnose storage issues when disk usage unexpectedly grows.
