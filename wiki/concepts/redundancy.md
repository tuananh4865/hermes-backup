---
title: "Redundancy"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [system-design, reliability, fault-tolerance, infrastructure]
---

# Redundancy

## Overview

Redundancy is the practice of duplicating critical system components, data, or infrastructure to ensure continued operation when failures occur. It is a fundamental principle in reliability engineering and fault-tolerant system design, employed across hardware, software, and network architectures. The core idea is simple: if one component fails, a redundant counterpart takes over, minimizing downtime and data loss.

Redundancy manifests at multiple levels of the technology stack. At the hardware level, organizations deploy redundant power supplies, RAID磁盘阵列, and duplicate network paths. At the application layer, this includes database replication, service replication, and load-balanced instances. The goal is to eliminate single points of failure—any individual component whose failure would bring down the entire system.

## Key Concepts

**High Availability (HA)** is the primary goal redundancy aims to achieve. HA systems are designed to remain operational despite component failures, typically targeting uptime percentages like 99.9% (three nines) or 99.99% (four nines). Each additional nine represents roughly a tenfold improvement in acceptable downtime.

**Redundancy vs. Resilience**: While related, these differ in approach. Redundancy adds backup components proactively, while resilience refers to a system's ability to recover and adapt after failure. Redundant systems assume failures will occur and prepare for them; resilient systems focus on graceful degradation and rapid recovery.

**N+1, N+2, and 2N Redundancy**: These denote the degree of backup capacity. N+1 provides one extra component beyond the minimum needed. N+2 provides two extras. 2N redundancy duplicates the entire system, providing full fallback capacity regardless of utilization.

**Active-Active vs. Active-Passive**: In active-active configurations, all redundant components operate simultaneously, sharing load. In active-passive (or standby) setups, backup components remain idle until needed, then take over.

## How It Works

Redundant systems rely on detection mechanisms to identify failures and switching logic to transfer operations to backup components. Heartbeat protocols continuously monitor component health—sending periodic signals to confirm availability. If a heartbeat is missed, the monitoring system triggers failover.

Failover can be automatic or manual. Automatic failover detects failure and redirects traffic or operations without human intervention, critical for systems requiring minimal downtime. Manual failover requires administrator action, which may be acceptable for planned maintenance windows.

Data redundancy uses replication strategies: synchronous replication writes to primary and backup simultaneously before acknowledging success, ensuring consistency but adding latency; asynchronous replication writes to primary, then replicates in the background, offering better performance at the cost of potential small data loss windows.

## Practical Applications

- **Database Systems**: Master-slave or master-master replication ensures database availability if the primary instance fails
- **Web Applications**: Multi-region deployments with load balancers route traffic around failed instances
- **Storage**: RAID configurations protect against disk failures; geographic replication protects against site-wide disasters
- **Networking**: Multiple ISP connections and router redundancy prevent network outages

## Examples

```yaml
# Example: Docker Compose redundancy configuration
version: '3.8'
services:
  app:
    deploy:
      replicas: 3  # 3 redundant instances
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```nginx
# Example: Nginx upstream redundancy
upstream backend {
    least_conn;
    server app1.example.com:3000;
    server app2.example.com:3000;
    server app3.example.com:3000 backup;
}
```

## Related Concepts

- [[fault-tolerance]] - System ability to continue operating despite component failures
- [[high-availability]] - Design approach targeting minimal downtime
- [[load-balancing]] - Distributing traffic across redundant instances
- [[replication]] - Copying data across multiple systems
- [[self-healing-wiki]] - System that auto-creates content to fill broken links

## Further Reading

- "Release It! Design and Deploy Production-Ready Software" by Michael Nygard
- Google SRE Book - Chapter on Addressing Cascading Failures

## Personal Notes

Redundancy isn't free—it increases cost, complexity, and operational overhead. The key is identifying which components truly need redundancy and choosing the appropriate redundancy model. Not everything needs 2N redundancy; sometimes N+1 or even simple restart-based recovery suffices. The ROI of redundancy should be measured against the actual cost of downtime for each specific system.
