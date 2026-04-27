---
title: Performance Management
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [engineering-management, productivity, OKR, KPIs, reviews]
---

## Overview

Performance management is the systematic process of improving organizational and individual performance by setting clear goals, measuring progress, providing feedback, and aligning efforts with strategic objectives. In software engineering organizations, it encompasses everything from goal-setting frameworks like OKRs (Objectives and Key Results) to formal performance reviews, continuous feedback loops, and career development conversations. Unlike annual reviews that happen once a year, modern performance management emphasizes ongoing dialogue between managers and engineers to keep everyone aligned and growing.

The discipline draws from organizational psychology, management science, and agile methodologies. It operates at multiple levels: the individual contributor (IC), the team, and the organization as a whole. Effective performance management creates transparency around expectations, surfaces blockers early, and ensures high performers are recognized and retained while underperformers receive structured support.

## Key Concepts

**OKRs (Objectives and Key Results)** is a goal-setting methodology popularized by John Doerr that links ambitious objectives to measurable key results. Objectives answer "where do we want to go?" while key results answer "how will we know we got there?" In engineering teams, an objective might be "Improve platform reliability" with key results like "reduce p99 API latency below 200ms" and "achieve 99.95% uptime."

**KPIs (Key Performance Indicators)** are the quantifiable metrics used to track performance against goals. Unlike OKRs which can be aspirational, KPIs typically reflect ongoing operational health. Engineering KPIs include deployment frequency, change failure rate, mean time to recovery (MTTR), and lead time for changes (the DORA metrics).

**Performance Reviews** are periodic evaluations—typically semi-annual or annual—where managers assess an employee's contributions, skills, and growth against pre-defined criteria. Modern approaches distinguish between **trajectory** (is the person growing?) and **current impact** (what have they delivered?).

**360-Degree Feedback** collects input from peers, reports, and cross-functional partners alongside manager assessment to give a well-rounded view of an engineer's collaboration and influence.

## How It Works

The performance management cycle typically begins with **goal setting** at the start of a review period. Managers and ICs collaboratively define objectives, often using the SMART framework (Specific, Measurable, Achievable, Relevant, Time-bound). These goals should cascade from team and org-level objectives down to individuals, creating vertical alignment.

During the review period, **ongoing feedback** is exchanged informally through 1:1 meetings, skip-level conversations, and peer shout-outs in tools like Lattice, Culture Amp, or Highspot. Many organizations now use "check-ins" or "pulse surveys" to capture sentiment and progress continuously rather than waiting for formal cycles.

The **review process** itself involves managers synthesizing data points—goals achieved, projects delivered, feedback received, self-assessments—into a coherent performance narrative. Calibration sessions ensure consistency across teams: a "strong performer" at one company means the same as "strong performer" at another. Ratings often map to compensation decisions (merit increases, promotions) and development plans.

Finally, the **output** of performance management includes promotion decisions, compensation adjustments, role changes, development plans, and in some cases, performance improvement plans (PIPs) for those consistently below expectations.

## Practical Applications

At a mid-sized tech company, an engineering team might run a quarterly OKR cycle aligned with product milestones. An individual engineer's objectives would connect to team objectives: if the team commits to launching a new API gateway, the IC's OKR might involve designing and implementing rate-limiting logic for that gateway.

After each sprint, engineers update their key results in the performance management system (e.g., "Key result 2: 4 of 5 rate-limiting endpoints deployed to production"). The manager reviews progress in weekly 1:1s, providing coaching and removing blockers. At the quarterly review, they assess overall impact and set next quarter's objectives.

For promotions, the bar often includes demonstrated ability at the next level: for senior engineers, this means evidence of technical leadership, cross-team influence, and growing the engineers around them—not just shipping individual features.

## Examples

A concrete example of goal alignment:

```
Objective: Scale the data pipeline to handle 10x traffic growth
Key Result 1: Migrate 3 legacy Kafka topics to the new streaming platform by Q2
Key Result 2: Achieve end-to-end processing latency under 50ms at p99
Key Result 3: Reduce pipeline infrastructure cost by 20% through auto-scaling
```

An engineer owning this OKR would break it into epics and stories, track metrics weekly, and present results in a quarterly review. The manager would assess whether the engineer showed increasing scope and impact compared to previous periods.

## Related Concepts

- [[engineering-management]] — The broader discipline of leading technical teams
- [[OKRs]] — Goal-setting methodology often paired with performance reviews
- [[DORA Metrics]] — Standard engineering performance indicators (deployment frequency, MTTR, etc.)
- [[360-degree-feedback]] — Multi-source feedback collection methodology
- [[career-ladders]] — Frameworks defining expectations at each engineering level

## Further Reading

- *Measure What Matters* by John Doerr — the definitive OKR reference
- Google's OKR resources and re:Work publications on performance management
- CircleCI's State of CI/CD reports on engineering productivity metrics

## Personal Notes

I've found that the biggest failure mode in performance management is treating it as a once-a-year compliance exercise rather than an ongoing conversation. Engineers who get consistent feedback (even when it's critical) grow faster and feel less blindsided during formal reviews. The best managers I've worked with had running documents tracking achievements and growth areas throughout the year, not just when it was time to write a review.
