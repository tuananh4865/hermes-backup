---
title: "Game Days"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [game-days, chaos-engineering, incident-response, resilience, sre, testing, training]
---

# Game Days

## Overview

Game days are structured exercises where engineering teams simulate failure scenarios and practice their incident response procedures in a controlled environment. Named after the military concept of war games, game days bring together the technical and organizational aspects of resilience testing—unlike automated chaos experiments that focus on system behavior, game days explicitly test how people respond when things go wrong. The practice combines technical fault injection with human factors: communication during incidents, decision-making under pressure, escalation procedures, and the effectiveness of runbooks and documentation. A successful game day reveals not just system weaknesses but organizational gaps in how the team responds to production crises.

The core philosophy behind game days is that reliability is not just a property of systems but a property of the sociotechnical system comprising people, processes, and technology. A system might be designed to fail gracefully, but if the on-call engineer doesn't know how to interpret the alerts, or if the escalation path is unclear, or if the runbook for the failure scenario doesn't exist—the designed resilience mechanisms may not activate in time. Game days validate the entire response chain, from the monitoring system that detects the anomaly through the human response that remediates it. This holistic view of resilience distinguishes game days from purely technical testing approaches.

Game days are typically planned events with significant organizational investment—they require participants to set aside their normal work, often span several hours or an entire day, and involve coordination across multiple teams. Because of this investment, game days are most effective when they target high-priority scenarios with realistic complexity: complete loss of a critical service, data center failure, security breach response, or cascading failures that span multiple systems. The goal is not to test every possible failure mode (that's the purpose of ongoing chaos experiments) but to validate readiness for the most impactful scenarios and to identify gaps that require remediation before they become real incident liabilities.

## Key Concepts

**Scenario Design** is the process of defining what failure will be simulated and what outcomes will be measured. Good game day scenarios are grounded in realistic failure modes—things that could actually happen—not theoretical or contrived situations. They should be complex enough to require coordination across multiple teams and decision points, but not so complex that the exercise becomes unwieldy. The scenario typically specifies: the initial failure condition (what is injected), the expected user impact (how users are affected), the expected detection and alerting (how the team learns about it), the expected response steps (what the team should do), and the success criteria (how the team knows the incident is resolved).

**Blast Radius Management** in game days requires careful consideration because the exercise environment may not be production, but may involve real users or real business impact if not properly contained. Most game days are conducted in staging or dedicated environments that replicate production architecture but handle synthetic or non-critical traffic. When game days must be conducted in production (for maximum realism), they typically target non-production traffic, synthetic users, or a small percentage of real users with explicit acceptance of risk. The fundamental principle is that game days should be controlled experiments— if the exercise causes unexpected widespread impact, the exercise has failed its own safety properties.

**Role Assignment** structures participation during the game day. Key roles typically include: the injectors (team members responsible for introducing the fault and controlling its parameters), the responders (team members who will handle the incident as if it were real), the observers (team members who watch and document without participating in response), and the facilitator (who guides the exercise, controls timing, and may provide hints if responders are stuck). Clear role definition ensures that the exercise produces clean data about response capability without interference between exercise control and incident response.

**Debriefing and Learning** is where the real value of game days is extracted. Immediately following the exercise, the team conducts a structured debrief that examines: what worked well (what detection, communication, and remediation steps were effective), what didn't work (what gaps or failures occurred), what was surprising (what unexpected behaviors or outcomes occurred), and what needs to be fixed (specific action items for documentation, tooling, or process improvements). The debrief should be blameless—the purpose is organizational learning, not individual accountability. The action items from the debrief are tracked and resolved before the next game day.

## How It Works

A game day follows a structured timeline from planning through execution to learning:

```markdown
# Game Day Timeline

## Week Before
- Finalize scenario and inject parameters
- Confirm participant availability and roles
- Brief all participants on scenario (without revealing specifics)
- Verify environment readiness (staging replicate, monitoring, tooling)
- Establish abort criteria and kill switches

## Day Of: 30 Minutes Before
- Confirm all participants are present
- Review safety protocols and abort criteria
- Ensure observers are positioned with appropriate access
- Verify communication channels are clear

## Game Day Execution (2-4 hours typical)
| Time    | Activity                              |
|---------|---------------------------------------|
| 0:00    | Facilitator briefs scenario context  |
| 0:05    | Injectors introduce initial fault    |
| 0:05+   | Response phase - responders work     |
| Ongoing | Observers document actions/timeline   |
| +15min  | First checkpoint - facilitator review |
| ...     | Continue until resolution or timebox |
| End     | Debrief begins immediately           |

## Debrief (30-60 minutes)
- Timeline reconstruction
- What worked / what didn't
- Surprises and anomalies
- Action items with owners and dates
```

The injector's role is to introduce faults according to the scenario plan while monitoring for unintended consequences. They maintain abort criteria authority—if the exercise begins causing unacceptable real-world impact, the injector terminates the exercise immediately. This safety role is critical because game days in production carry inherent risk; the injector serves as the circuit breaker that prevents exercise casualties from becoming real incidents.

Observers play a crucial documentation role that enables meaningful debriefs. They maintain running timelines of significant events—who was notified when, what decisions were made when, what actions were taken, what the system behavior was at each step. This documentation becomes the foundation for the debrief and for subsequent improvement tracking. Observers should be instructed to document facts and behaviors, not judgments about individual performance.

## Practical Applications

**Incident Response Training** uses game days to build muscle memory for the communication and decision-making patterns that effective incident response requires. Engineers who have practiced running a major incident in a game day are significantly more effective when they face the real thing— they know the communication channels, the escalation paths, the typical failure patterns, and the pressure of time-critical decision-making. This is particularly valuable for organizations where major incidents are rare but high-impact, meaning engineers may only experience them a few times per year.

**Runbook Validation** tests whether documented procedures actually work when executed under pressure. A runbook that looks clear in a quiet office may prove incomprehensible when an on-call engineer is stressed and working quickly. Game days reveal these gaps: steps that are missing critical context, commands that don't work as documented, assumptions that aren't valid, and missing information about who has authorization to take critical actions. Updating runbooks based on game day findings directly improves real incident response.

**Cross-Team Coordination** exercises the interfaces between teams that may rarely interact during normal operations. A game day that simulates failure of a shared dependency tests whether the consumer team and the provider team have shared understanding of their interface contracts, clear escalation paths, and effective communication channels. These cross-team coordination failures are often at the root of prolonged incidents—game days surface them in a learning context rather than during actual incidents.

## Examples

A cloud provider conducts a game day simulating complete loss of their primary API gateway. The scenario begins with injectors terminating all API gateway instances. Observers note that: (1) existing WebSocket connections drop immediately, (2) monitoring detects the failure within 47 seconds, (3) the on-call engineer is paged within 60 seconds, (4) the engineer's initial response misidentifies the root cause as a DDoS attack rather than infrastructure failure, (5) 12 minutes pass before the correct escalation path to the infrastructure team is activated, (6) the infrastructure team identifies that auto-scaling failed to launch replacement instances due to a misconfigured IAM policy, (7) the issue is resolved by manually launching instances with correct permissions. The debrief identifies three action items: improve alerting specificity to distinguish infrastructure failure from attack, add the infrastructure escalation path to the API gateway runbook, and validate IAM policies monthly.

A fintech company runs a game day simulating a data breach. While their technical chaos experiments test system resilience, this game day focuses on human response: how quickly can the security team assess the scope, what communication is required to comply with regulatory notification timelines, how does customer support prepare talking points, what is the CEO's role in incident communication. The exercise reveals that the security team's incident response plan hasn't been updated in 18 months and contains outdated contact information, and that the legal team's input on regulatory notification requirements is needed earlier than the current escalation path provides. Both gaps are addressed following the game day.

## Related Concepts

- [[Chaos Engineering]] - The technical practice of injecting faults into systems, often combined with game days for human factors testing
- [[Incident Response]] - The organizational process for responding to production failures, which game days exercise and improve
- [[Site Reliability Engineering]] - The discipline that often owns game day programs as part of resilience validation
- [[Fault Injection]] - The technical mechanism for introducing failures, used within game day scenarios
- [[Resilience Engineering]] - The broader study of building resilient sociotechnical systems
- [[Observability]] - The system property that enables effective detection and diagnosis during game days and real incidents

## Further Reading

- [Game Day: Google SRE](https://sre.google/workbook/game-days/) — Comprehensive guide to running game days from Google's SRE team
- [Chaos Engineering community resources](https://chaosengineering.com/) — Practical guides and case studies
- [Incident Management Best Practices](https://www.pagerduty.com/) — Operational guidance for incident response

## Personal Notes

Game days are one of the highest ROI activities an engineering organization can undertake for resilience. The cost is a day of engineering time; the benefit is discovering gaps in a learning context rather than during live incidents with real user impact. The key to effective game days is treating them as experiments with hypotheses, not performances where success is predetermined. If everything goes perfectly, you haven't learned anything— the goal is to find the rough edges. Organizations that do game days well have a blameless culture where "we found a gap in our runbook during game day" is a success, not an embarrassment. The best game days end with participants saying "I didn't know I didn't know that" — that's when the real learning happens.
