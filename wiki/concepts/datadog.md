---
title: "Datadog"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [monitoring, observability, cloud, saas, apm, infrastructure]
---

# Datadog

## Overview

Datadog is a cloud-based monitoring and security platform that provides comprehensive observability across infrastructure, applications, logs, and user experience. Founded in 2010, Datadog has grown into one of the leading SaaS monitoring solutions, offering integrated Application Performance Monitoring (APM), infrastructure monitoring, log management, real user monitoring (RUM), and security analytics in a single unified platform. Its strength lies in eliminating data silos by correlating metrics, traces, and logs within one interface.

Unlike open-source alternatives like [[Prometheus]] or [[Grafana]] that require self-hosted components, Datadog operates entirely as a managed service. Agents and integrations send data to Datadog's cloud infrastructure, where it's processed, stored, and made queryable through a powerful expression language called DQL (Datadog Query Language). This SaaS approach reduces operational overhead but introduces considerations around data residency, cost at scale, and vendor lock-in.

Datadog's integration ecosystem is extensive—over 400 official integrations cover cloud providers (AWS, Azure, GCP), databases, message queues, web servers, and application frameworks. This breadth makes it particularly attractive to organizations with heterogeneous technology stacks seeking unified observability.

## Key Concepts

**The Datadog Agent**: The agent is a lightweight daemon installed on hosts (servers, containers, VMs) that collects and forwards metrics, logs, and traces to Datadog. Written in Go, the agent runs as a sidecar or system service, with minimal resource overhead. The agent auto-discovers services, collects system metrics (CPU, memory, disk, network), and can be extended through custom checks written in Python or Go.

**Metrics and Tags**: Datadog uses a flat key-value tagging system rather than Graphite's hierarchical naming. Every piece of data can be tagged with arbitrary dimensions (e.g., `env:production`, `service:checkout`, `region:us-east-1`). This flexible tagging enables powerful aggregation and filtering at query time. Metric names in Datadog are simpler, with all context encoded in tags.

**Services and Traces**: In Datadog APM, an application is composed of services (discrete units like `api-gateway`, `database`, `cache`) that communicate via traces. A trace is the complete journey of a request through multiple services, made up of spans (individual operations with timing, errors, and metadata). This distributed tracing capability is essential for understanding latency in microservices architectures.

**Dashboards and Monitors**: Dashboards provide real-time visualization of any metric or log data, supporting both time-series graphs and log analytics views. Monitors define alerting conditions using threshold, anomaly, or forecast detection, with notifications routed through email, Slack, PagerDuty, or custom webhooks.

## How It Works

Datadog's architecture centers on data collection and cloud processing:

1. **Collection**: Datadog Agents, library instrumentation (for APM), and cloud integrations continuously collect data. The agent runs on each host, while integrations may query cloud APIs periodically or receive streaming data from cloud services.

2. **Ingestion and Processing**: Data arrives at Datadog's intake layer and is processed in real-time. Metrics are indexed and made queryable immediately. Traces are assembled from span data (which may arrive out of order), and logs are parsed and tagged using pipeline processors.

3. **Storage**: Time-series metrics are stored with configurable retention (15 months for paid tiers). Logs can be retained for varying periods based on indexing and archiving settings. Trace data retention is typically shorter (30 days by default).

4. **Query and Visualization**: The web UI and API provide access to all data types. DQL enables complex queries across metrics, logs, and traces. The dashboards and monitors evaluate queries continuously to update visualizations and trigger alerts.

```python
# Example: Submitting custom metrics to Datadog
from datadog import initialize, statsd

initialize(api_key="your_api_key", app_key="your_app_key")

# Counter
statsd.increment('web.requests', tags=['endpoint:/api/users', 'method:GET'])

# Gauge
statsd.gauge('web.response_time', 0.234, tags=['endpoint:/api/users'])

# Histogram
statsd.histogram('web.request_size', 1024, tags=['endpoint:/api/users'])
```

## Practical Applications

Datadog excels at providing unified observability across complex, multi-cloud environments.

**Infrastructure Monitoring**: Automatic detection and monitoring of AWS EC2 instances, RDS databases, ELB load balancers, Lambda functions, and dozens of other AWS/Azure/GCP services. The Infrastructure List view provides a unified map of all monitored entities.

**Application Performance Monitoring**: Deep visibility into application performance with automatic instrumentation for Python, Ruby, Java, Go, Node.js, and .NET. Flame graphs show where time is spent across code paths. Service maps visualize service dependencies.

**Log Management**: Centralized log aggregation with full-text search, structured field extraction, and pattern detection. Logs can be correlated with corresponding traces and metrics for complete debugging context.

## Examples

A typical Datadog monitor configuration for service availability:

```json
{
  "name": "API Error Rate High",
  "type": "metric alert",
  "query": "sum(last_5m):sum:api.errors{env:production}.as_count() / sum:api.requests{env:production}.as_count() > 0.05",
  "message": "API error rate exceeds 5%.\n\n{{#is_alert}}🚨 Alert{{/is_alert}}\n\nService: {{service.name}}\nError Rate: {{value}}%",
  "tags": ["service:api", "severity:high"],
  "options": {
    "thresholds": {
      "critical": 0.05
    },
    "notify_no_data": true,
    "no_data_timeframe": 2
  }
}
```

## Related Concepts

- [[Prometheus]] - Open-source monitoring system
- [[Grafana]] - Open-source visualization platform
- [[New Relic]] - Competing APM vendor
- [[Sentry]] - Error tracking and performance monitoring
- [[Observability]] - The discipline Datadog enables
- [[APM]] - Application Performance Monitoring discipline
- [[Infrastructure Monitoring]] - Tracking system-level metrics

## Further Reading

- [Datadog Documentation](https://docs.datadoghq.com/)
- [Datadog API Reference](https://docs.datadoghq.com/api/latest/)
- [Integrations Catalog](https://docs.datadoghq.com/integrations/)
- [Datadog Blog](https://www.datadoghq.com/blog/) - Best practices and feature announcements

## Personal Notes

Datadog's strength is the correlation between data types—clicking a spike in a metric and instantly seeing the corresponding logs and traces is powerful. The cost model can be surprising at scale; carefully plan which data you send and leverage sampling for high-volume traces. The synthetic monitoring feature is underutilized—it lets you create API tests and browser scripts that run from Datadog's global network, catching issues before real users do. For Kubernetes, the Datadog Operator provides declarative management of the agent lifecycle.
