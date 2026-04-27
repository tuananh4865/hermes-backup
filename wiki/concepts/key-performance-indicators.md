---
title: Key Performance Indicators
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [kpis, metrics, business-intelligence, performance-measurement, analytics]
---

## Overview

Key Performance Indicators (KPIs) are measurable values that demonstrate how effectively an organization, team, or individual is achieving critical business objectives. KPIs provide quantifiable evidence of progress toward goals, enabling data-driven decision-making across all organizational levels. Unlike vanity metrics that look impressive but lack actionable implications, effective KPIs are specific, measurable, achievable, relevant, and time-bound (SMART criteria).

## Key Concepts

**Leading vs Lagging Indicators**: Leading KPIs predict future outcomes and enable proactive management—customer satisfaction scores might lead revenue growth by a quarter. Lagging indicators confirm what has already happened, like quarterly revenue or annual churn rate. Effective KPI dashboards combine both types.

**Input vs Output Metrics**: Input metrics measure activities undertaken (hours trained, bugs fixed, features shipped). Output metrics measure results achieved (revenue generated, customer satisfaction achieved). Organizations sometimes track too many input metrics that feel productive but don't drive outcomes.

**Key Results vs Objectives**: In the OKR (Objectives and Key Results) framework, Key Results are quantifiable metrics that indicate whether an Objective has been achieved. For example, if the Objective is "Become the market leader," a Key Result might be "Increase market share from 15% to 25%."

**Normalization and Baselines**: Raw numbers often mislead without context. KPIs should be normalized (per employee, per transaction, year-over-year) and compared against baselines to reveal trends. A 10% conversion rate means different things with different traffic volumes.

**Thresholds and Benchmarks**: Effective KPIs have defined targets (thresholds) that trigger alerts when crossed and benchmarks that contextualize performance relative to industry standards or historical performance.

## How It Works

KPI implementation follows a structured process:

```text
1. Identify Strategic Objectives
   └── What are the 3-5 most important goals?

2. Define Key Results for Each Objective
   └── What metrics prove we've achieved this?

3. Establish Measurement Methods
   └── Where does data come from? How is it calculated?

4. Set Targets and Thresholds
   └── What does success look like? When do we intervene?

5. Build Dashboards and Reports
   └── How do we visualize and distribute KPI data?

6. Review and Iterate
   └── Are these KPIs still relevant? Do they drive behavior?
```

```sql
-- Example: E-commerce Customer Lifetime Value KPI
SELECT 
    customer_id,
    SUM(order_value) as total_revenue,
    COUNT(order_id) as order_count,
    MAX(order_date) as last_order,
    DATE_DIFF(MAX(order_date), MIN(order_date), DAY) as customer_tenure_days
FROM orders
GROUP BY customer_id
HAVING order_count > 1
ORDER BY total_revenue DESC;
```

## Practical Applications

KPIs permeate every business function. Engineering teams track deployment frequency, change failure rate, and mean time to recovery (DRE). Marketing measures cost per acquisition (CPA), return on ad spend (ROAS), and customer acquisition cost (CAC). Sales monitors pipeline value, win rate, and sales cycle length. Customer success tracks net promoter score (NPS), churn rate, and health scores. Executive dashboards aggregate departmental KPIs into organizational health metrics.

## Examples

- **SaaS Metrics**: Monthly Recurring Revenue (MRR), churn rate, LTV:CAC ratio, burn rate
- **Engineering**: Deployment frequency, lead time for changes, change failure rate, availability
- **Marketing**: Traffic, conversion rate, bounce rate, email open rates, social engagement
- **HR**: Employee retention rate, time to hire, training completion, engagement scores

## Related Concepts

- [[Business Intelligence]] - Systems that collect and analyze KPI data
- [[Data Analytics]] - Process of extracting insights from metrics
- [[OKRs]] - Framework for goal-setting that uses KPIs as Key Results
- [[Web Analytics]] - KPIs specific to web properties
- [[Engineering Metrics]] - KPIs for software development and operations

## Further Reading

- [KPI Library](https://www.kpilib.com/) - Repository of industry-specific KPIs
- [OKR FAQ](https://www.amplitude.com/okr-faq)
- [DORA Metrics](https://www.devops-research.com/research.html) - Software delivery performance KPIs

## Personal Notes

The biggest KPI mistake I've seen: measuring what Easy to measure rather than what matters. Shipping velocity means nothing if you're building the wrong features. I favor fewer, high-quality KPIs over dashboard clutter. A monthly review cadence works better than real-time obsession—daily metric watching creates noise, not signal.
