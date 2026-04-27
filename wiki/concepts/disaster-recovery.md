---
title: Disaster Recovery
description: Strategies and processes for restoring systems and data after catastrophic failures
tags: [devops, backup, reliability, infrastructure]
---

# Disaster Recovery

Disaster recovery (DR) encompasses the policies, tools, and procedures for restoring systems, data, and business operations after a catastrophic incident.

## Key Concepts

- **RTO (Recovery Time Objective)**: Maximum acceptable downtime before systems must be restored
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss measured in time
- **Backup Frequency**: How often data is snapshots (hourly, daily, weekly)
- **Failover**: Automatically switching to redundant systems

## Strategies

- **Backup & Restore**: Regular snapshots to object storage or off-site location
- **Pilot Light**: Minimal running version of core systems, scaled up on failure
- **Warm Standby**: Partial redundancy with reduced capacity
- **Multi-Region**: Active-active deployment across geographic regions

## Related

- [[backup-and-recovery]]
- [[infrastructure]]
- [[reliability]]
