---
title: "Data Analytics"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [business-intelligence, analytics, data-science, dashboards, sql]
---

# Data Analytics

## Overview

Data analytics is the broader discipline of collecting, organizing, and analyzing data to draw conclusions and support decision-making. While closely related to data analysis, data analytics tends to emphasize the organizational and strategic context—using data not just to understand what happened, but to inform business strategy, optimize operations, and predict future outcomes. It encompasses a spectrum ranging from purely historical descriptive analytics (what happened) to diagnostic analytics (why it happened), predictive analytics (what will happen), and prescriptive analytics (how can we make it happen).

The term "data analytics" is often used in business contexts to describe the practice of extracting insights from data to drive organizational decisions. This distinguishes it from more academically oriented "data science," though in practice the two terms overlap considerably. Data analytics is supported by a mature ecosystem of business intelligence tools (Tableau, Looker, Power BI), SQL-based querying, and increasingly, machine learning models deployed in production analytics systems.

## Key Concepts

**The Analytics Maturity Spectrum** — Organizations typically progress through four stages of analytics capability. Descriptive analytics answers "what happened?" through reports and dashboards. Diagnostic analytics investigates "why did it happen?" through drill-down and correlation analysis. Predictive analytics asks "what will happen?" using forecasting models. Prescriptive analytics recommends "what should we do?" using optimization and simulation.

**Business Intelligence (BI)** — Tools and processes for transforming raw data into meaningful and useful information for business analysis purposes. BI dashboards aggregate key metrics (KPIs), allow slicing by dimensions (time, geography, product), and provide visualizations that make trends accessible to non-technical stakeholders.

**ETL Pipelines** — Extract, Transform, Load processes that move data from source systems (transactional databases, third-party APIs, event logs) into a data warehouse or data lake in a cleaned, structured format ready for analysis.

**Cohort Analysis** — Segmenting users or customers into cohorts based on a shared characteristic (typically time of first purchase or signup) and tracking their behavior over time. This reveals retention patterns and the long-term impact of engagement strategies.

**A/B Testing** — A controlled experiment comparing two variants to determine which performs better against a defined metric. A/B testing is a cornerstone of data-driven product development and marketing optimization.

## How It Works

Data analytics typically begins with a business question or hypothesis: "Will offering free shipping increase customer retention?" An analyst then designs the data collection or extraction needed to answer the question, writes SQL queries or uses BI tools to pull relevant data, performs analysis (which may include statistical tests, regression, or segmentation), and produces findings with appropriate caveats.

In modern organizations, data is usually stored in a data warehouse (Snowflake, BigQuery, Redshift) or data lake. Analysts query these systems using SQL, sometimes supplemented with Python (pandas, scipy) or R for more complex analysis. Results are shared through dashboards that auto-refresh as new data arrives, slide decks for stakeholder meetings, or automated reports delivered via email.

The quality of analytics depends heavily on data quality and the analyst's ability to ask the right questions. Garbage in, garbage out applies with full force here—a sophisticated model applied to poor-quality data produces poor-quality insights.

## Practical Applications

Data analytics is used to optimize marketing spend by identifying which channels deliver the highest ROI, to improve product retention by analyzing user behavior patterns, to manage supply chains by forecasting demand, to detect fraud by identifying anomalous transaction patterns, and to personalize customer experiences by segmenting users and tailoring recommendations. Every function—finance, HR, operations, sales—benefits from analytics-driven decision-making.

## Examples

SQL query for cohort retention analysis:

```sql
SELECT
  DATE_TRUNC('month', first_purchase_date) AS cohort_month,
  COUNT(DISTINCT customer_id) AS cohort_size,
  COUNT(DISTINCT CASE
    WHEN purchase_date >= first_purchase_date + INTERVAL '30 days'
    AND purchase_date < first_purchase_date + INTERVAL '60 days'
    THEN customer_id
  END) AS retained_30d,
  ROUND(100.0 * COUNT(DISTINCT CASE
    WHEN purchase_date >= first_purchase_date + INTERVAL '30 days'
    AND purchase_date < first_purchase_date + INTERVAL '60 days'
    THEN customer_id
  END) / COUNT(DISTINCT customer_id), 2) AS retention_rate_30d
FROM customer_purchases
GROUP BY DATE_TRUNC('month', first_purchase_date)
ORDER BY cohort_month;
```

Calculating customer lifetime value:

```python
import pandas as pd

customers = pd.read_csv("customer_transactions.csv")
clv = customers.groupby("customer_id").agg(
    total_revenue=("amount", "sum"),
    order_count=("order_id", "count"),
    avg_order_value=("amount", "mean")
)
clv["estimated_clv"] = clv["avg_order_value"] * clv["order_count"] * 12
print(clv.sort_values("estimated_clv", ascending=False).head(10))
```

## Related Concepts

- [[data-analysis]] — Foundational analytical techniques underlying analytics
- [[apache-hadoop]] — Large-scale data processing infrastructure for analytics
- [[knowledge-management]] — Organizing analytical findings for organizational access
- [[snowflake]] — Data warehouse platform commonly used for analytics

## Further Reading

- Avinash Kaushik, *Web Analytics 2.0* and *Analytics Best Practices*
- "Numsense!" by Anand Chandramouli and Karthik Ramasubramanian — for non-technical readers
- Mode Analytics SQL Tutorial: https://mode.com/sql-tutorial/
- Looker documentation: https://cloud.google.com/looker/docs

## Personal Notes

I think of data analytics as the bridge between raw data and organizational action. The technical skills (SQL, Python, BI tools) are necessary but not sufficient—effective analytics requires understanding the business context deeply enough to ask meaningful questions and interpret results in ways that lead to good decisions. One thing I've learned is that most stakeholders don't care about the p-value; they want to know "should we do X or Y?"
