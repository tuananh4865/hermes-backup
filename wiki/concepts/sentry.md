---
title: "Sentry"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [monitoring, error-tracking, debugging, observability, developer-tools]
---

# Sentry

## Overview

Sentry is an error monitoring and performance tracking platform designed for developers. Founded in 2012, Sentry's primary purpose is to help developers understand exactly what went wrong when their applications fail—providing detailed context about the error, the user action that triggered it, the state of the system at the time, and the chain of events leading to the failure. Unlike general-purpose monitoring tools that track system-level metrics, Sentry is developer-centric, treating each error or performance issue as an actionable debugging artifact.

Sentry supports over 50 programming languages and frameworks through official SDKs, including Python, JavaScript, TypeScript, React, Angular, Ruby, Go, Java, Kotlin, Swift, Objective-C, and .NET. The SDKs hook into language runtimes to automatically capture unhandled exceptions, handle errors gracefully, and breadcrumbs that record the execution path leading to a failure.

The platform operates as a SaaS product (with a self-hosted option called Sentry On-Crescent), receiving error reports from applications and organizing them into issues—groups of similar errors representing the same root cause. This aggregation prevents developers from being overwhelmed by thousands of identical error reports and enables trend analysis: is error rate increasing or decreasing? Did a recent deployment cause new failures?

## Key Concepts

**Issues**: An issue represents a unique error event, determined by fingerprinting algorithms that group similar errors together. By default, Sentry fingerprints stack traces, so the same error thrown in different locations or users creates multiple issues. Custom fingerprinting rules allow teams to customize how errors are grouped—for example, grouping all database connection errors regardless of stack trace.

**Events**: An event is a single occurrence of an error sent to Sentry. Each event contains the stack trace, local variables, user context, tags, breadcrumbs, and environment details (OS version, browser, device). Events within an issue share the same fingerprint but may have different user impact or metadata.

**Breadcrumbs**: Breadcrumbs are a trail of events that occurred before an error. Sentry automatically captures system events (HTTP requests, database queries, logging statements) as breadcrumbs. Developers can also manually add breadcrumbs to capture application-specific context: "User clicked submit button," "Form validation passed."

**Releases**: Sentry correlates errors with code deployments through release tracking. By providing a release identifier when configuring the SDK, Sentry can show which errors are new in a release, which were resolved, and which persist across releases. This linkage between errors and deploys is crucial for determining deployment impact.

## How It Works

Sentry's architecture consists of SDKs embedded in applications and a cloud processing backend:

1. **Capture**: When an exception occurs (or is explicitly captured via `Sentry.capture_exception()`), the SDK collects context: stack trace, thread information, local variables (with scrubbing for sensitive data), user information, and breadcrumb trail. The SDK batches events to reduce network overhead and sends via HTTPS.

2. **Processing**: Events arrive at Sentry's intake service and enter a processing pipeline. PII is scrubbed according to data scrubbing rules. Stack traces are symbolicated (converting memory addresses to source code locations). Errors are fingerprinted and grouped into issues. The event is indexed for search and stored.

3. **Storage and UI**: Processed events are stored and indexed. The Sentry UI displays issues, event details, graphs showing error frequency over time, user impact counts, and performance distributions. Webhooks and integrations enable external notification.

4. **SDK Integration**: SDKs provide both automatic instrumentation (catching unhandled exceptions) and manual APIs for explicit error capture. Performance monitoring is enabled separately, creating transaction spans for distributed tracing.

```python
# Example: Sentry Python SDK configuration
import sentry_sdk
from sentry_sdk import capture_exception, add_breadcrumb

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    release="myapp@1.0.0",
    environment="production",
    traces_sample_rate=0.1,  # 10% of transactions for performance
)

def checkout(request, cart_id):
    add_breadcrumb(
        category="cart",
        message=f"Processing cart {cart_id}",
        level="info",
    )
    
    try:
        result = payment_service.charge(cart_id)
        return render_success(result)
    except PaymentDeclined as e:
        capture_exception(e, tags={"cart_id": cart_id})
        return render_payment_error()
```

## Practical Applications

Sentry is essential for maintaining application reliability and reducing mean time to resolution (MTTR) for production issues.

**Production Error Tracking**: Capture and triage exceptions in production without relying on users to report bugs. The Sentry UI becomes the single pane of glass for all application errors across services, with Slack alerts, email notifications, or PagerDuty integration for critical issues.

**Release Regression Detection**: Link errors to deploys to identify regressions immediately. If error rate spikes after a deployment, Sentry shows which errors are new and which were introduced in that release. Comparing error rates before and after deploy quantifies impact.

**Performance Monitoring**: Sentry's performance product provides distributed tracing within and between services. Slow transactions are captured, spans show where latency occurs, and flame graphs visualize time spent across code paths. This complements [[APM]] tools by focusing on error and latency issues specifically.

**User Impact Analysis**: Knowing how many users are affected by an error is critical for prioritization. Sentry tracks unique users affected by each issue, enabling data-driven decisions about which bugs to fix first.

## Examples

Configuring Sentry with custom data scrubbing and routing:

```python
import sentry_sdk
from sentry_sdk.scratch import add_global_frames_to_scrub

sentry_sdk.init(
    dsn="https://...",
    before_send=filter_error,  # Custom filter function
    send_default_pii=False,    # Don't send personally identifiable info
)

def filter_error(event, hint):
    # Filter out expected errors
    if "ExpectedTimeout" in str(hint.get("exc_value")):
        return None  # Don't send this error
    # Add custom context
    event["tags"]["custom_id"] = get_custom_identifier()
    return event
```

## Related Concepts

- [[Prometheus]] - Infrastructure metrics monitoring
- [[Grafana]] - Visualization and dashboards
- [[Datadog]] - Full-stack monitoring platform
- [[New Relic]] - APM and observability platform
- [[APM]] - Application Performance Monitoring
- [[Observability]] - The discipline Sentry enables
- [[Error Tracking]] - The specific discipline Sentry focuses on

## Further Reading

- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry SDK Reference](https://develop.sentry.dev/)
- [Sentry Blog](https://blog.sentry.io/)
- [Sentry Changelog](https://develop.sentry.dev/sdk/changelog/) - SDK updates

## Personal Notes

The performance tracing in Sentry is often overlooked but powerful—enabling `traces_sample_rate` even at 0.01 (1%) gives visibility into slow endpoints without overwhelming data. Configure PII scrubbing carefully; `send_default_pii=False` is a good default, but some errors need user context (for example, which user's data caused the crash). Slack integration for critical errors is essential, but tune notification rules to avoid alert fatigue—new issues and regression alerts are more valuable than "this error has occurred 100 times in the last hour" spam. The allocation and quota system in Sentry can surprise teams; monitor usage and adjust sampling rates before hitting limits.
