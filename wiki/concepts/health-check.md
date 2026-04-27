---
title: Health Check
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [health-check, devops, reliability, kubernetes]
---

## Overview

A health check is a mechanism used to verify whether a service, application, or system component is functioning correctly and able to handle requests. It is a periodic probe performed by an external entity—such as a load balancer, orchestrator, or monitoring system—to determine the operational state of a target. Health checks form a foundational element of reliable distributed systems, enabling automated detection of failures, graceful handling of degraded states, and self-healing infrastructure.

In practice, a health check endpoint exposes a simple interface—typically an HTTP endpoint or a specific protocol—that returns a status indicating whether the component is healthy. The checking system polls this endpoint at regular intervals and evaluates the response. If the response indicates a failure or exceeds a timeout threshold, the checking system can trigger alerts, remove the instance from service, or attempt remediation. This automated feedback loop reduces manual intervention and minimizes downtime.

Health checks are especially critical in environments where applications run across multiple instances or containers. Without explicit health verification, a load balancer might continue routing traffic to a failing instance, resulting in degraded user experience or cascading failures. By embedding health verification into the operational layer, systems can achieve higher availability and resilience.

The concept extends beyond simple binary up-or-down checks. Modern implementations often include aggregated health reporting, where individual components report their status and a parent system computes an overall system health score. This hierarchical approach allows for nuanced responses—for example, degraded functionality might be acceptable during partial failures rather than triggering a complete outage.

## Patterns

There are several distinct patterns of health checks, each serving different operational purposes. Understanding the distinction between these patterns is essential for designing robust systems.

**Liveness probes** determine whether an application is running and has not entered a deadlocked or hung state. A failing liveness probe typically indicates that the process is still alive but unable to progress, and the remediation is usually to restart the container or process. Kubernetes uses liveness probes to determine when a pod should be restarted, making them a critical mechanism for maintaining application health in containerized environments. Liveness checks should be lightweight and fast, as they are executed frequently and a slow response can trigger unnecessary restarts.

**Readiness probes** determine whether an application is able to accept traffic. Unlike liveness probes, which focus on the process state, readiness probes verify that all dependencies and resources required to serve traffic are available. This includes database connectivity, cache availability, external API access, and any other runtime dependencies. A pod may be alive but not ready to serve requests—for example, during initialization, data loading, or when overwhelmed by a backlog. Kubernetes uses readiness probes to decide whether to route traffic to a pod, ensuring that only ready instances receive requests.

**Startup probes** are used for applications that require a longer initialization time. They check whether the application has finished starting up before other probes take over. This pattern is particularly useful for legacy applications or services that perform time-consuming setup operations such as cache warming or configuration loading. Once a startup probe succeeds, liveness and readiness probes take over normal monitoring duties.

Implementing these patterns correctly requires careful consideration of what each probe should verify. Overly simplistic checks—such as only verifying that the HTTP server is listening—may miss critical dependencies. Overly complex checks can introduce fragility or performance overhead. The best practice is to verify the specific conditions required for the application to serve requests meaningfully.

## Related

- [[Kubernetes]] - The container orchestrator that popularized liveness, readiness, and startup probes as first-class concepts
- [[Load Balancing]] - Systems that rely on health checks to route traffic only to healthy instances
- [[Service Mesh]] - Infrastructure layer that often provides built-in health checking and traffic management capabilities
- [[Monitoring]] - The broader discipline of observing system state, of which health checks are a component
- [[Circuit Breaker]] - A pattern that works alongside health checks to prevent cascading failures when services degrade
- [[Graceful Degradation]] - The ability of a system to maintain partial functionality during partial failures, often monitored via health checks
