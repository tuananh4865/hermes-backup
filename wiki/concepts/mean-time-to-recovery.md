---
title: "Mean Time To Recovery"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [reliability, sre, operations, incident-management, sla]
---

# Mean Time To Recovery

## Overview

Mean Time To Recovery (MTTR) is a key reliability metric that measures the average time it takes to restore a system, service, or component to full operational status after a failure has been detected. It is one of the four classic "golden signals" of Site Reliability Engineering (SRE), alongside Mean Time Between Failures (MTBF), Mean Time to Detect (MTTD), and availability. MTTR captures the effectiveness of an organization's incident response process—how quickly can the team identify, diagnose, and fix problems that cause service degradation or outage.

MTTR is typically measured from the moment a failure is detected (by monitoring, alerting, or user report) until the service is fully restored and normal operations resume. The exact definition can vary: some organizations measure until the immediate fix is deployed, while others measure until full customer impact is resolved and post-incident review is complete. It's important to agree on a consistent definition within your organization to make MTTR comparisons meaningful over time.

A low MTTR indicates that an organization has mature incident management practices: effective monitoring and alerting, clear escalation paths, well-documented runbooks, capable on-call engineers, and robust deployment/rollback mechanisms. A high MTTR suggests systemic issues in any of these areas.

## Key Concepts

### MTTR Components

MTTR is often decomposed into distinct phases:

- **Mean Time to Detect (MTTD)**: How quickly does the system detect that a failure has occurred? This depends on the quality of monitoring, alerting thresholds, and the nature of the failure itself.
- **Mean Time to Acknowledge (MTTA)**: How quickly does an engineer begin actively working on the incident after the alert fires? This measures on-call responsiveness and escalation efficiency.
- **Mean Time to Repair/Resolve (MTTR)**: The time to diagnose the root cause and implement a fix or workaround.
- **Mean Time to Restore (RTO)**: The business-level objective for how quickly the service must be back up, often defined in SLAs.

### MTTR vs MTBF

Together, MTTR and Mean Time Between Failures (MTBF) paint a complete picture of system reliability:

```
Availability = MTBF / (MTBF + MTTR)
```

For a system with MTBF of 100 hours and MTTR of 2 hours:
```
Availability = 100 / (100 + 2) = 0.9804 = 98.04%
```

Reducing either MTTR or increasing MTBF improves availability. MTTR is often the more actionable metric because organizations have more direct control over their response processes than over preventing all possible failures.

### Error Budgets

MTTR is intimately connected to error budgets—a core SRE concept. If your SLA promises 99.9% availability, that allows 0.1% downtime (about 43.8 minutes per month). Your MTTR and incident frequency determine whether you will stay within that budget. High MTTR with frequent incidents quickly exhausts error budgets, signaling that reliability work needs to take priority over new feature development.

### On-Call Practices

Effective on-call is a prerequisite for low MTTR. Best practices include:

- Clear on-call rotation with redundant coverage
- Well-crafted alerts that minimize noise and false positives
- Runbooks and decision trees for common failure modes
- Authority to make decisions without extensive approval chains
- Post-on-call time for investigating and fixing root causes

## How It Works

MTTR is calculated by aggregating incident data over a period:

```python
def calculate_mttr(incidents: list[dict]) -> float:
    """
    Calculate Mean Time To Recovery from a list of incidents.
    
    Each incident dict must have:
      - detected_at: datetime when failure was discovered
      - resolved_at: datetime when service was fully restored
    
    Returns MTTR in minutes.
    """
    if not incidents:
        return 0.0
    
    total_recovery_time = sum(
        (inc["resolved_at"] - inc["detected_at"]).total_seconds()
        for inc in incidents
    )
    
    return (total_recovery_time / len(incidents)) / 60.0

# Example usage
incidents = [
    {"detected_at": ..., "resolved_at": ...},  # 45 minutes
    {"detected_at": ..., "resolved_at": ...},  # 23 minutes
    {"detected_at": ..., "resolved_at": ...},  # 67 minutes
]

mttr = calculate_mttr(incidents)
print(f"MTTR: {mttr:.1f} minutes")  # ~45 minutes average
```

### Blameless Postmortems

MTTR can only improve if organizations learn from incidents. Blameless postmortems focus on systemic factors rather than individual mistakes. A good postmortem identifies:

- What happened, timeline of events
- Root cause(s) and contributing factors
- Impact (duration, users affected, revenue lost)
- What went well in the response
- Action items with owners and deadlines

```yaml
# Example postmortem structure
postmortem:
  id: INC-2024-089
  title: "Payment service outage — 47 minutes"
  severity: High
  mttr: 47  # minutes
  timeline:
    - "09:14 — Alert fires: elevated error rate in payment service"
    - "09:15 — On-call engineer acknowledges, begins investigation"
    - "09:23 — Root cause identified: bad database migration"
    - "09:31 — Rollback initiated"
    - "09:47 — Service restored, error rates normal"
  root_cause: "Migration script omitted WHERE clause, deleted 12k records"
  action_items:
    - id: AI-001
      description: "Add migration pre-flight checks and dry run capability"
      owner: platform-team
      priority: P1
    - id: AI-002
      description: "Implement point-in-time recovery for payment DB"
      owner: dba-team
      priority: P1
```

## Practical Applications

- **SLA Compliance**: MTTR directly affects whether you meet contractual availability targets
- **SRE Benchmarks**: Compare your MTTR against industry standards to identify improvement areas
- **Runbook Development**: High MTTR incidents highlight gaps in documentation or tooling
- **Capacity Planning**: Understanding recovery patterns helps size infrastructure
- **Incident Trend Analysis**: MTTR trending up over time is an early warning sign

## Related Concepts

- [[site-reliability-engineering]] — Google's SRE discipline and practices
- [[error-budgets]] — Measuring and managing reliability risk
- [[incident-management]] — Process for responding to production outages
- [[on-call]] — Practices for maintaining effective on-call rotations
- [[chaos-engineering]] — Proactively testing system resilience through experiments

## Further Reading

- Betts, Dominic, et al. *Seeking SRE* (2018) — Conversations about running production systems
- Murphy, Niall. "Post-Incident Reviews: Freeing the Blameless" — Google SRE blog on blameless postmortems
- Allspaw, John, and Rob Rie. "Blameless PostMortem and Psychological Safety" — Healthy postmortem culture
- Onsi, Alejandro. "SLOs, Error Budgets, and the Future of Reliability" — Understanding error budget-driven prioritization

## Personal Notes

MTTR is one of those metrics where the target varies wildly by context—a 10-minute MTTR for a payments system is excellent, but for a batch reporting pipeline might be excessive. What matters is benchmarking against your own historical trends and peer organizations in similar domains. I've found that the most impactful MTTR reductions often come not from faster individual engineers but from better tooling: automated rollback, canary deployments, and comprehensive dashboards that surface the right context during incidents.
