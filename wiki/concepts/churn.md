---
title: Churn
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [churn, saas, business-metrics, customer-retention, mrr, ltv]
---

# Churn

## Overview

Churn, also called customer attrition, is the rate at which customers stop doing business with a company over a given period. It is one of the most critical metrics for subscription-based businesses, particularly Software-as-a-Service (SaaS) companies, where revenue is recurring and customer relationships span multiple billing cycles. High churn can undermine growth even when new customer acquisition is strong, creating a "leaky bucket" problem that limits sustainable expansion.

Churn is typically expressed as a percentage of customers or revenue lost during a specific period—monthly churn of 5% means that 5% of the customer base departed in a typical month. For subscription businesses, both customer churn (number of customers lost) and revenue churn (MRR or ARR lost) matter, with revenue churn often receiving more attention from investors and leadership because it directly impacts financial projections.

Understanding churn requires examining not just the rate but also the reasons customers leave. Churn analysis combines quantitative tracking of churn rates with qualitative investigation of churn causes, forming the foundation for retention improvement initiatives.

## Key Concepts

**Customer Churn Rate** measures the percentage of customers who cancel or fail to renew within a period. If you start a month with 100 customers and end with 95, your monthly customer churn rate is 5%.

**Revenue Churn** (also called MRR Churn) measures the percentage of recurring revenue lost from cancellations and downgrades. Negative revenue churn—where expansion revenue from existing customers exceeds lost revenue—indicates a healthy, growing business.

**Net Revenue Retention (NRR)** combines revenue lost from churn with revenue gained from expansions and upsells. A NRR above 100% means existing customers are generating more revenue over time, even before new customer acquisition.

**Churn Cohorts** group customers by acquisition date to analyze churn patterns over the customer lifecycle. This reveals whether churn is concentrated in early stages (onboarding issues) or develops over longer relationships.

**Voluntary vs. Involuntary Churn** distinguishes between customers who actively choose to leave versus those who churn due to payment failures, expired trials, or other non-intentional reasons. Involuntary churn is often addressable through improved payment retry logic and dunning processes.

## How It Works

Churn calculation follows a straightforward formula:

```
Monthly Customer Churn Rate = (Customers Lost During Month) / (Customers at Start of Month) × 100
```

For more accurate tracking, many companies use the average customer count during the period rather than the starting count:

```
Average Customer Churn Rate = (Customers Lost) / ((Customers at Start + Customers at End) / 2) × 100
```

Revenue churn uses a similar approach with MRR figures:

```
Revenue Churn Rate = (MRR Lost from Churn + MRR Lost from Downgrades - MRR from Upgrades) / (MRR at Start of Period) × 100
```

Leading SaaS companies track churn at multiple granularities: overall company level, segment level (by plan tier, industry, company size), and individual customer level for high-value accounts.

## Practical Applications

**Churn Prediction** uses machine learning models to identify customers at high risk of churning before they actually leave. Features typically include product usage metrics, support ticket frequency, payment history, engagement scores, and tenure. Early warning enables proactive intervention—personal outreach, special offers, or improved onboarding.

**Retention Economics** calculates how much to invest in retention efforts. If customer acquisition cost (CAC) is $200 and average customer generates $100/month with 10% monthly churn, the payback period is 2 months but lifetime value is only $1,000. Reducing churn to 5% doubles lifetime value to $2,000, making retention investments highly profitable.

**Segment-Specific Strategies** recognize that churn drivers vary by customer segment. Enterprise customers may churn due to poor executive sponsorship or strategic misalignment, while SMB customers often churn due to price sensitivity or insufficient time-to-value.

```python
# Example: Simple churn prediction model
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def predict_churn(customers, events, support_tickets):
    """Predict customer churn based on behavioral features."""
    features = pd.DataFrame({
        'login_frequency_30d': customers.login_count.rolling(30).sum(),
        'support_tickets_30d': support_tickets.groupby('customer_id').count(),
        'feature_adoption_score': customers.calculate_feature_adoption(),
        'days_since_last_login': (pd.Timestamp.now() - customers.last_login).days,
        'payment_delinquency': customers.has_delinquent_payments()
    })
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(features, customers.churned_next_30_days)
    
    return model.predict_proba(features)

# Usage: Identify at-risk customers for proactive retention
at_risk = predict_churn(customers, events, tickets)
high_risk_customers = customers[at_risk[:, 1] > 0.7]
```

## Examples

**Gym Membership Model**: A gym with 1,000 members loses 50 members monthly (5% monthly churn). Annual churn is approximately 46%—most gym members don't stay past their initial commitment period. Successful gyms focus heavily on the first 90 days to build habits that reduce early churn.

**B2B SaaS Enterprise**: Enterprise customers typically have longer sales cycles and higher switching costs, resulting in lower churn (1-2% monthly) but longer and more expensive recovery processes when churn does occur. Success teams and regular business reviews are common retention mechanisms.

**Freemium Products**: Games and consumer apps often see very high churn (10-20% monthly) as users try an app briefly and never return. The focus shifts to optimizing the "aha moment"—the point where users first experience value—because users who reach this milestone churn at dramatically lower rates.

## Related Concepts

- [[saas]] — SaaS business model and metrics
- [[mrr]] — Monthly Recurring Revenue
- [[ltv]] — Customer Lifetime Value calculations
- [[model-routing]] — Not directly related, but may use churn prediction internally
- [[cost-optimization]] — Can intersect when analyzing customer profitability

## Further Reading

- ProfitWell Blog: Churn analysis and SaaS metrics
- Lincoln Murphy's writings on churn and customer success
- "Measuring and Managing Customer Lifetime Value" — various Harvard Business Review articles
- Segment's Customer Churn Analysis Playbook

## Personal Notes

Churn is the single metric I check first when evaluating a subscription business. The best product with poor churn will eventually fail; the worst product with exceptional retention can build a profitable business. Pay attention to cohort-based churn—it reveals whether you're improving over time or just treating symptoms. If monthly churn spikes when customers hit their first renewal, that's an onboarding problem. If it spikes after year two, you have an ongoing value delivery problem.
