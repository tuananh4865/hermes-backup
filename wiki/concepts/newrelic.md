---
title: "New Relic"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [monitoring, observability, apm, cloud, saas, performance]
---

# New Relic

## Overview

New Relic is a cloud-based observability platform founded in 2008 that provides comprehensive monitoring for applications, infrastructure, and user experiences. Originally focused on Application Performance Monitoring (APM) for web applications, New Relic has expanded into a full-stack observability platform offering APM, infrastructure monitoring, browser monitoring, mobile monitoring, log management, and synthetic checks. The platform is built around the concept of telemetry data—metrics, events, logs, and traces—that can be correlated to provide end-to-end visibility.

New Relic's differentiation lies in its data platform approach. Rather than treating different data types (APM, infrastructure, logs) as separate products, New Relic stores all telemetry in a single, unified data store called the Telemetry Data Platform. This architecture enables powerful cross-domain correlation—a spike in error rate can be instantly connected to the specific database query causing it and the infrastructure metrics of the host running the affected service.

In recent years, New Relic has shifted toward a usage-based pricing model (the New Relic One platform) and open-sourced components like the NR1 dashboard framework. Their recent acquisitions and developer-focused initiatives reflect a push to compete with cloud-native observability solutions like [[Datadog]] and [[Prometheus]]/[[Grafana]] stacks.

## Key Concepts

**Entities and Services**: In New Relic's model, an "entity" is any monitored component—applications, hosts, containers, databases, or custom services. Services are entities that produce telemetry data (metrics, events, logs, traces). The Service Map visualizes how entities relate to each other, showing dependencies and health status at a glance.

**APM Dashboard**: The core APM interface provides deep visibility into application performance. Key metrics include Apdex score (user satisfaction with response times), response time breakdowns (by web transaction, background task, and database calls), error rates, and throughput. The distributed tracing UI reveals the full path a request takes across services.

**Infrastructure Monitoring**: For host-level visibility, New Relic Infrastructure monitors servers (physical, virtual, containers). It automatically detects and instruments running processes, network connections, and storage devices. Integration with AWS, Azure, and GCP provides cloud-specific context like EC2 instance metrics, Lambda function invocations, and S3 bucket statistics.

**NRQL**: New Relic Query Language is the SQL-like language for querying all data in the Telemetry Data Platform. NRQL enables flexible aggregation, filtering, and visualization of any metric, event, log, or trace data. Functions like `facet`, `average`, `percentile`, and `rate` support sophisticated analysis.

## How It Works

New Relic's data collection and processing follows a cloud-hosted model:

1. **Instrumentation**: Applications are instrumented using New Relic agents (Java, .NET, Python, Ruby, Go, Node.js) or the OpenTelemetry SDK. Agents auto-instrument common frameworks (Spring, Django, Express, Rails) and capture span data for distributed traces. Infrastructure uses a lightweight daemon for host metrics, with cloud integrations pulling provider APIs.

2. **Data Ingestion**: Telemetry data is sent to New Relic's ingest endpoints over HTTPS. Agents batch and compress data to reduce network overhead. The Telemetry Data Platform receives millions of data points per minute from customers worldwide.

3. **Processing and Storage**: Ingested data flows through processing pipelines that parse, enrich, and index data. Spans are assembled into traces. Logs are parsed and correlated with corresponding traces and entities. All data becomes queryable within seconds of ingestion.

4. **Visualization and Alerting**: The New Relic One interface provides dashboards, the APM dashboard, Infrastructure UI, and Logs viewer. Alert policies define conditions using NRQL queries, with signal detection algorithms (static thresholds, baseline, anomaly) determining when to fire incidents.

```python
# Example: Custom instrumentation with New Relic Python agent
import newrelic.agent

@newrelic.agent.background_task()
def process_order(order_id):
    # Business logic
    newrelic.agent.add_custom_attribute('order_id', order_id)
    
    with newrelic.agent.capture_trace():
        # Critical section to trace
        result = payment_gateway.charge(order_id)
    
    return result
```

## Practical Applications

New Relic serves teams requiring deep application visibility with minimal operational overhead.

**Application Performance Monitoring**: Full-stack APM with automatic code-level visibility. Transaction traces show exact SQL queries, external HTTP calls, and time spent in each function. Database call graphs reveal slow queries and N+1 patterns. Error analytics group and analyze exceptions with full context.

**Browser Monitoring**: JavaScript errors, page load timing, AJAX requests, and user interactions tracked from the browser perspective. Session traces record actual user sessions for detailed debugging. Core Web Vitals (LCP, FID, CLS) are automatically measured.

**Infrastructure Observability**: Unified view of containers (Docker, Kubernetes), cloud services, and bare-metal servers. Processes and network connections are automatically inventoried. The Kubernetes cluster explorer provides real-time visibility into pod health, resource usage, and service dependencies.

## Examples

A New Relic alert policy for error rate monitoring:

```sql
-- NRQL query for alert condition
SELECT count(apm.service.error.count) / count(apm.service.transaction.duration) * 100 
FROM Metric 
WHERE appName = 'checkout-service' 
AND (errorLevel = 'ERROR' OR transactionError = true) 
FACET appName 
LIMIT 20
```

```yaml
# Synthetic monitor configuration for API endpoint
name: Checkout API Health Check
frequency: 5 minutes
locations:
  - us-east-1
  - eu-west-1
script: |
  $http.get('https://api.example.com/health', {
    headers: { 'Authorization': 'Bearer {{SECRET.API_KEY}}' }
  });
  if ($http.statusCode != 200) {
    $util.fail('Health check failed with status: ' + $http.statusCode);
  }
```

## Related Concepts

- [[Datadog]] - Competing cloud monitoring platform
- [[Prometheus]] - Open-source metrics collection
- [[Grafana]] - Visualization platform
- [[Sentry]] - Error tracking specialist
- [[APM]] - Application Performance Monitoring discipline
- [[Observability]] - The discipline New Relic enables
- [[OpenTelemetry]] - Vendor-neutral instrumentation standard

## Further Reading

- [New Relic Documentation](https://docs.newrelic.com/)
- [New Relic One Platform](https://docs.newrelic.com/docs/new-relic-one/)
- [New Relic GitHub](https://github.com/newrelic) - Open source components
- [Nerdlog](https://www.youtube.com/playlist?list=PLmV3xY3Cwsyc1n_pZL7pR7sS6kmlOdJCL) - Official YouTube channel

## Personal Notes

New Relic's code-level diagnostics in APM traces are excellent for debugging production issues. The ability to jump from an error in the error inbox to the exact line of code that threw the exception (when symbolication is configured) saves hours. However, the agent can be heavyweight for some use cases—consider sampling or reduced inventory settings for high-throughput services. The new usage-based pricing is more predictable than per-seat models, but watch data ingestion carefully; the free tier is generous but violations can spike costs quickly. The Explorer Hub and community forums are valuable resources for dashboards and best practices.
