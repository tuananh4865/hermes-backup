---
title: LTV
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ltv, saas, metrics, customer-value, revenue]
---

# LTV (Lifetime Value)

## Overview

Lifetime Value (LTV), also known as Customer Lifetime Value (CLV or CLTV), is a metric that estimates the total net revenue a business can reasonably expect to generate from a single customer account over the entire duration of their relationship. LTV is one of the most fundamental metrics in subscription-based businesses, particularly in SaaS, because it directly informs how much a company can afford to spend on customer acquisition. A business with a clear understanding of its LTV can make data-driven decisions about marketing spend, product investment, and customer success priorities.

LTV differs from simple revenue-per-transaction metrics in that it captures the long-term economic value of a customer relationship. A customer might generate modest monthly revenue, but if they remain a customer for five years, their LTV could be substantial. Conversely, a high-revenue customer who churns after three months might have a lower LTV than expected. Understanding these dynamics is critical for sustainable growth.

## How It Works

The basic LTV formula for a SaaS business is:

```
LTV = Average Revenue Per Account (ARPA) / Churn Rate
```

For example, if your ARPA is $100/month and your monthly churn rate is 2%, the LTV is $100 / 0.02 = $5,000. This means each customer is worth $5,000 on average over their lifetime.

A more detailed calculation incorporates [[gross-margin]] to arrive at contribution-based LTV:

```
LTV = (ARPA × Gross Margin %) / Churn Rate
```

For businesses with varying contract lengths and pricing tiers, a cohort-based LTV calculation using survival analysis or hazard modeling may be more accurate. This approach groups customers by acquisition cohort and tracks their revenue contribution over time, accounting for expansion revenue, contraction, and churn at each period.

## Key Concepts

**ARPU vs ARPA** — Average Revenue Per User (ARPU) divides total revenue by all users, including free users. Average Revenue Per Account (ARPA) or Average Revenue Per Paying User (ARPPU) excludes free tiers, giving a more accurate picture of monetizable value.

**Churn Rate** — The percentage of customers who cancel or do not renew within a given period. Churn is the primary driver of LTV, and small improvements in churn rate have disproportionate effects on LTV due to the compounding nature of customer retention.

**Payback Period** — While not part of the LTV formula directly, payback period (how long until acquisition cost is recovered) should be considered alongside LTV. A high LTV is only sustainable if the business can acquire customers profitably.

**LTV:CAC Ratio** — The ratio of Lifetime Value to Customer Acquisition Cost. A ratio of 3:1 is often cited as healthy for SaaS businesses, meaning you earn three dollars for every dollar spent acquiring a customer.

## Practical Applications

LTV is used across the business to guide strategic decisions. Product teams use LTV to prioritize features that increase retention and expansion revenue. Marketing teams use it to determine acceptable customer acquisition costs. Investors use LTV (along with growth and burn rate) to evaluate business health and unit economics. Customer success teams use individual LTV estimates to tier accounts and allocate resources.

## Examples

Consider a B2B SaaS platform with the following metrics:
- Monthly ARPA: $500
- Annual contract value: $5,500 (with annual discount)
- Monthly churn rate: 1.5%
- Gross margin: 80%

```
LTV = ($500 × 0.80) / 0.015 = $26,667
```

This means each paying customer is worth approximately $26,667 in gross profit over their lifetime. If the sales and marketing cost to acquire a customer (CAC) is $8,000, the LTV:CAC ratio is 3.3, indicating healthy unit economics.

## Related Concepts

- [[churn]] — Customer churn rate and its impact on retention
- [[saas]] — SaaS business models and metrics
- [[cac]] — Customer Acquisition Cost
- [[unit-economics]] — The study of direct revenues and costs at the customer level
- [[arpa]] — Average Revenue Per Account

## Further Reading

- Profitwell: How to Calculate LTV
- SaaStr: The Correct LTV Calculation
- HubSpot: Customer Lifetime Value Guide

## Personal Notes

I find that early-stage startups often neglect LTV modeling, treating it as a metric for "later." This is a mistake—even rough LTV estimates help founders make better decisions about pricing, packaging, and go-to-market strategy from day one. The formula seems simple, but the inputs (especially accurate churn data) often aren't tracked well in nascent businesses. Building the habit of measuring and updating LTV as the business evolves pays dividends.
