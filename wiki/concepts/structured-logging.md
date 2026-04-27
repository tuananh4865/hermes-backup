---
title: Structured Logging
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [structured-logging, logging, observability, json, logging-best-practices]
---

# Structured Logging

## Overview

Structured logging is a logging practice where log messages are recorded in a defined, machine-readable format—typically [[JSON]]—rather than plain human-readable text strings. Instead of writing `"User 1234 logged in at 10:30 AM"`, a structured logger produces `{"user_id": 1234, "event": "login", "timestamp": "2026-04-13T10:30:00Z", "level": "info"}`. This transformation from unstructured text to structured data enables powerful querying, filtering, and analysis that is impossible with traditional "printf-style" logging.

Structured logging is a cornerstone of modern [[observability]] practices. In an era where applications generate millions of log lines per day across distributed [[microservices]], being able to filter logs by specific fields (e.g., "show me all ERROR logs from service `checkout-api` where `user_id > 1000`") is essential for effective debugging and monitoring.

## Key Concepts

### Structured vs. Unstructured Logging

**Unstructured logging** produces flat text strings:
```
2026-04-13 10:30:00 INFO UserService: User 1234 logged in from IP 192.168.1.1
```

**Structured logging** produces typed, nested data:
```json
{
  "timestamp": "2026-04-13T10:30:00Z",
  "level": "INFO",
  "service": "user-service",
  "event": "user_login",
  "user_id": 1234,
  "ip_address": "192.168.1.1"
}
```

The structured format allows programmatic access to every field. The human readability is slightly reduced for raw output, but tooling (like `jq`, [[Grafana]] Loki, [[Elasticsearch]]/[[Kibana]]) renders it beautifully.

### Log Levels

Structured logs preserve severity levels:
- **DEBUG**: Detailed diagnostic information for development
- **INFO**: General operational events (login, API call, background job start)
- **WARN**: Unexpected but handled situations (retry, fallback, deprecated API)
- **ERROR**: Errors that caused a request to fail
- **FATAL**: Application-wide crashes requiring immediate attention

### Context Propagation

One of the most powerful features of structured logging is the ability to attach contextual information that persists across function calls. A request ID, user ID, or tenant ID can be attached to the logger context at the start of a request and automatically included in every subsequent log entry:

```python
logger = logger.bind(request_id="abc-123", user_id=456)
logger.info("Processing order")  # Includes request_id and user_id automatically
```

This is especially important in distributed systems where [[tracing]] correlation IDs link logs across services.

### Field Naming Conventions

Consistent field naming is critical for log analysis. Common conventions:
- `timestamp` (ISO 8601 format)
- `level` (uppercase: DEBUG, INFO, WARN, ERROR)
- `service` or `logger` (source service/component)
- `event` or `message` (what happened)
- `error` object (for errors: type, message, stack trace)
- `duration_ms` (timing information)
- `request_id`, `trace_id`, `span_id` (correlation IDs)

## How It Works

In most structured logging libraries, you don't build JSON strings manually. Instead, you call logger methods with key-value pairs:

```python
# Python: structlog library
import structlog

log = structlog.get_logger()
log.info("order_processed",
    order_id="ord_789",
    customer_id="cust_456",
    amount_cents=2999,
    item_count=3,
    duration_ms=142
)
```

The library:
1. Serializes the log entry to JSON (or another format like CBOR)
2. Writes to stdout/stderr or a log collector
3. A log aggregation system (Fluentd, Vector, Promtail) ships logs to a backend

### Log Aggregation Pipeline

Typical production flow:
```
Application → Structured Logger → stdout/stderr → Log Agent (Fluentd/Vector) 
    → Centralized Store (Elasticsearch/Loki/S3) → Query UI (Kibana/Grafana)
```

For [[Kubernetes]] environments, logs are typically written to stdout and collected by an agent DaemonSet on each node.

## Practical Applications

Structured logging is essential for:

- **Debugging production issues**: Filter by any field, not just text search
- **Metrics derivation**: Extract numeric fields (latency, bytes) and create dashboards
- **Alerting**: Trigger alerts when error rate exceeds threshold (counting `level=ERROR`)
- **Audit logging**: Record every user action with actor, action, target, timestamp
- **Request tracing**: Correlate logs across services using shared trace IDs
- **Cost analysis**: Attribute resource usage to specific tenants or features

## Examples

### Python with structlog (JSON output):

```python
import structlog
import logging

# Configure structlog to output JSON
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()
log.info("api_request",
    method="GET",
    path="/api/users/123",
    status_code=200,
    duration_ms=45,
    user_agent="Mozilla/5.0"
)
```

Output:
```json
{"event": "api_request", "method": "GET", "path": "/api/users/123", "status_code": 200, "duration_ms": 45, "level": "info"}
```

### Node.js with Pino (extremely fast JSON logger):

```javascript
const pino = require('pino')

const log = pino({
  level: 'info',
  base: { service: 'payment-service' },
  timestamp: pino.stdTimeFunctions.isoTime,
})

// Add context that persists across all child loggers
const childLogger = log.child({ order_id: 'ord_999' })

childLogger.info({ amount: 49.99, currency: 'USD' }, 'Payment processed')
// Output: {"level":30,"time":"2026-04-13T10:30:00.000Z","service":"payment-service","order_id":"ord_999","amount":49.99,"currency":"USD","msg":"Payment processed"}
```

### Querying structured logs in [[Grafana]] Loki with LogQL:

```logql
# Find all ERROR logs from checkout service for user 1234
{service="checkout-api"} |= "ERROR" | json | user_id="1234"

# Calculate p99 latency per endpoint
sum by (path) (
  rate(
    {service="api-gateway"} | json | duration_ms > 0 [1m]
  )
)

# Error rate over time
sum by (level) (
  rate(
    {service=~".+"} | json [5m]
  )
)
```

## Related Concepts

- [[logging]] — General logging concept
- [[observability]] — The discipline that structured logging enables
- [[JSON]] — The most common structured logging format
- [[Elasticsearch]] — Search backend often used with structured logs
- [[Kibana]] — Visualization for Elasticsearch log data
- [[Grafana]] — Dashboard and alerting tool supporting structured logs
- [[microservices]] — Where structured logging is most valuable (distributed tracing)
- [[tracing]] — Correlating logs across distributed services

## Further Reading

- [structlog documentation](https://www.structlog.org/) — Python structured logging
- [Pino documentation](https://getpino.io/) — Node.js fast JSON logger
- [LogQL: Grafana Loki query language](https://grafana.com/docs/loki/latest/logql/)
- [The value of structured logging](https://www.honeycomb.io/blog/structured-logging-the-what-why)
- [12-Factor App: Logs](https://12factor.net/logs)

## Personal Notes

The biggest shift I made was moving from `console.log` spam to structured logging in all new projects. Using `structlog` in Python or `pino` in Node.js is trivially easy and the performance overhead is negligible—Pino is one of the fastest Node.js loggers. The payoff comes when you're debugging a production incident at 2 AM: instead of regex-matching a wall of text, you filter `level=ERROR and service=checkout and duration_ms > 5000` and immediately see what's broken. One tip: always include `trace_id`/`request_id` in every log entry—it turns a chaotic flood into a navigable timeline.
