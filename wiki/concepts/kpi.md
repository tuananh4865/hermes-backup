---
title: "Kpi"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [metrics, business, performance, analytics]
---

# KPI (Key Performance Indicator)

## Overview

A Key Performance Indicator (KPI) is a measurable value that demonstrates how effectively an organization, team, or individual is achieving key business objectives. KPIs are used at every level of an enterprise to evaluate success in reaching targets. Unlike simple metrics, KPIs are tied to specific goals and provide actionable insight into performance trends over time.

Organizations use KPIs to track progress, identify problems early, align teams around common goals, and make data-driven decisions. A well-designed KPI is specific, measurable, achievable, relevant, and time-bound (SMART criteria). Without clear KPIs, organizations struggle to understand whether their strategies are working or how resources should be allocated.

## Key Concepts

### Leading vs Lagging Indicators

KPIs can be classified as leading or lagging indicators.

**Leading indicators** predict future outcomes and provide early warning signals. Examples include customer satisfaction scores, employee engagement levels, and website traffic trends. These allow organizations to take preventive action.

**Lagging indicators** measure outcomes that have already occurred. Revenue, profit, churn rate, and market share are classic lagging indicators. While important, they don't allow for intervention since the result has already materialized.

### KPI Hierarchies

Organizations typically organize KPIs in hierarchies:

- **Strategic KPIs** (C-level) - Long-term organizational goals
- **Operational KPIs** (Management) - Medium-term departmental targets
- **Functional KPIs** (Team/Individual) - Short-term tactical metrics

### Quantitative vs Qualitative

Quantitative KPIs involve numerical data that can be statistically analyzed: revenue growth, conversion rates, response times. Qualitative KPIs assess subjective qualities: brand perception, culture health, customer sentiment.

## How It Works

### Setting Effective KPIs

The process of establishing KPIs begins with clear strategic objectives. Each objective should have 1-5 KPIs that directly measure progress toward it. For each KPI, you must define:

1. The exact metric and how it's calculated
2. The data source and collection method
3. Target values (thresholds for success)
4. Frequency of measurement and reporting
5. Responsible parties for each metric

### Measurement and Tracking

KPIs require consistent data collection and visualization. Most organizations use dashboards to display KPI status, trends, and comparisons against targets. Traffic light systems (green/yellow/red) provide quick status indicators.

```sql
-- Example: SQL query for calculating a KPI (customer retention rate)
SELECT 
    COUNT(DISTINCT customer_id) AS retained_customers,
    COUNT(DISTINCT customer_id_at_period_start) AS starting_customers,
    ROUND(
        COUNT(DISTINCT customer_id) * 100.0 / 
        NULLIF(COUNT(DISTINCT customer_id_at_period_start), 0), 
        2
    ) AS retention_rate_pct
FROM customer_period_activity
WHERE period = '2026-Q1';
```

## Practical Applications

KPIs are ubiquitous across business functions:

- **Sales**: Customer Acquisition Cost (CAC), Lifetime Value (LTV), conversion rate, pipeline velocity
- **Marketing**: Cost per Lead, Return on Ad Spend (ROAS), click-through rate, social engagement
- **Finance**: Gross margin, burn rate, runway months, accounts receivable days
- **Engineering**: Deployment frequency, mean time to recovery, change failure rate
- **HR**: Employee turnover rate, time to hire, training completion rate

## Examples

A SaaS company might track:

- **North Star Metric**: Weekly Active Users (WAU)
- **Health KPIs**: Churn rate < 2%, NPS > 50, MRR growth > 10%
- **Operational KPIs**: Support ticket resolution time < 4 hours, API uptime > 99.9%

## Related Concepts

- [[OKRs]] - Objectives and Key Results, a goal-setting framework
- [[Metrics Dashboard]] - Tools for visualizing KPIs
- [[Data Analytics]] - The practice of analyzing KPI data
- [[Business Intelligence]] - Systems for KPI reporting

## Further Reading

- "KPI Library" - Comprehensive database of industry KPIs
- "Measure What Matters" by John Doerr - OKR methodology linked to KPIs

## Personal Notes

The biggest KPI mistakes: tracking too many metrics (analysis paralysis), vanity metrics that look good but don't drive action, and setting targets without buy-in from those responsible for achieving them. KPIs should spark conversation, not just display numbers. When a KPI triggers concern, the real value is in investigating why and taking corrective action.
