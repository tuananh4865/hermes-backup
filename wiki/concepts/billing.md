---
title: Billing
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [billing, payments, saas, subscriptions, invoicing]
---

# Billing

## Overview

Billing in SaaS (Software as a Service) refers to the comprehensive system of invoicing customers, collecting payments, and managing financial transactions for subscription-based services. Unlike traditional one-time software purchases, SaaS billing operates on recurring revenue models where customers pay periodically—monthly or annually—for continued access to software and services. Effective billing systems are critical to the financial health of any subscription business, directly impacting cash flow, customer retention, and revenue predictability.

The billing process encompasses everything from initial subscription setup and plan management to invoice generation, payment processing, and revenue recognition. Modern SaaS billing systems must handle complex scenarios including proration, upgrades, downgrades, cancellations, trials, and usage-based pricing models. The sophistication of a company's billing infrastructure often correlates with its ability to experiment with pricing models and optimize revenue per customer.

## Key Concepts

**Subscription Lifecycle** refers to the entire journey of a customer subscription from trial through active subscription to cancellation and potential churn. Understanding where a customer stands in this lifecycle is essential for billing operations, as different stages may require different billing behaviors, grace periods, and dunning (payment retry) strategies.

**Payment Methods** are the mechanisms customers use to pay for subscriptions. These typically include credit cards, debit cards, ACH bank transfers, and increasingly, payment platforms like PayPal or Stripe. The payment method landscape continues to evolve with buy-now-pay-later options and cryptocurrency gaining adoption in some markets.

**Billing Cycles** define how frequently customers are charged. Common cycles include monthly, annual, biennial, or custom arrangements. Many SaaS companies offer discounts for annual commitments, incentivizing longer billing periods to improve revenue predictability and reduce churn during the contract period.

**Dunning Management** is the process of handling failed payments and recovering lapsed subscriptions. Effective dunning involves automated retry schedules, customer notifications at various stages of payment failure, and ultimately, subscription suspension protocols for prolonged non-payment.

## How It Works

A typical SaaS billing workflow begins when a customer signs up and enters trial or immediately begins a paid subscription. The billing system creates a customer record, associates payment method information (typically tokenized through a payment processor like Stripe or Braintree), and schedules future invoices according to the selected plan and billing cycle.

When an invoice is due, the billing system attempts to charge the stored payment method. Successful charges trigger subscription continuation and receipt generation. Failed charges initiate the dunning process, which typically involves progressive outreach to the customer with increasing urgency before ultimately cancelling or suspending the subscription.

For usage-based billing models, the system tracks consumption metrics throughout the billing period and calculates the final invoice amount at cycle end. This is common in infrastructure services like cloud computing, where customers pay for actual resource consumption rather than a fixed subscription tier.

```javascript
// Example: Stripe subscription creation
const subscription = await stripe.subscriptions.create({
  customer: 'cus_123456',
  items: [{ price: 'price_monthly_basic' }],
  billing_cycle_anchor: Math.floor(Date.now() / 1000),
  proration_behavior: 'create_prorations',
});
```

## Practical Applications

SaaS billing systems integrate with customer relationship management (CRM) platforms to provide visibility into customer payment status within the broader customer context. Sales and customer success teams need to know which accounts have payment issues, upcoming renewals, or potential expansion opportunities based on billing patterns.

Revenue recognition is another critical application. Modern accounting standards (ASC 606, IFRS 15) require companies to recognize revenue as it is earned over the subscription period, not when payment is received. Billing systems must maintain the data necessary for accurate revenue recognition, tracking deferred revenue and contract liabilities.

Tax compliance represents a significant practical challenge, particularly for SaaS companies selling internationally. Billing systems must calculate, collect, and remit sales tax, VAT, and GST across multiple jurisdictions, requiring integration with tax calculation services like Avalara or TaxJar.

## Examples

A small SaaS startup might use a simple Stripe-only integration with three pricing tiers: Free, Pro ($29/month), and Enterprise (custom). Their billing system handles straightforward monthly subscriptions with automatic card charging and basic invoice generation.

A mature enterprise SaaS company might offer hybrid billing with a base subscription plus usage-based overages. They would require complex proration calculations for mid-cycle plan changes, custom billing terms (Net-30, Net-60), and integration with their ERP system for proper revenue recognition and financial reporting.

Marketplaces and platforms add another layer of complexity, often involving split payments where the platform takes a commission and passes the remainder to service providers. This requires billing systems capable of handling multi-party transactions and generating appropriate tax documentation for all parties.

## Related Concepts

- [[SaaS]] — The broader business model that billing supports
- [[MRR]] — Monthly Recurring Revenue, the metric billing systems track
- [[Subscription]] — The recurring payment model central to SaaS billing
- [[Payment Gateway]] — Technology for processing card transactions
- [[Churn Rate]] — Metric closely tied to billing and subscription management

## Further Reading

- Stripe's "SaaS Billing Guide" for comprehensive subscription billing patterns
- Recurly's documentation on usage-based billing implementations
- ASC 606 Revenue Recognition guidelines for subscription businesses

## Personal Notes

Billing seems like a back-office concern until payment failures start eating into revenue. Investing in robust billing infrastructure early prevents painful accounting headaches later. Proration edge cases especially tend to surface at the worst times—during customer disputes or when scaling teams need accurate data.
