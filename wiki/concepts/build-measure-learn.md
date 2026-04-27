---
title: "Build Measure Learn"
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [lean-startup, methodology, product-development, iteration]
related:
  - [[lean-startup]]
  - [[okrs-(objectives-and-key-results)]]
  - [[minimum-viable-product]]
  - [[solo-developer]]
  - [[startup-pivoting]]
sources:
  - https://theleanstartup.com/principles
---

# Build Measure Learn

**Build Measure Learn** is the core feedback loop of [[lean-startup]] methodology, coined by Eric Ries. It describes the fundamental cycle:

1. **Build** — Create a Minimum Viable Product ([[minimum-viable-product]]) quickly
2. **Measure** — Collect data on how customers use it
3. **Learn** — Decide whether to pivot or persevere

> "The fundamental activity of a startup is to turn ideas into products, measure how customers respond, and then learn whether to pivot or persevere."

## The Feedback Loop

```
BUILD → MEASURE → LEARN → (pivot or persevere) → BUILD
    ↑                                          |
    └──────────────────────────────────────────┘
```

**Key insight:** This is not a linear process — it's a **validated learning loop**. Every product decision should be tested, not assumed.

## Build — Creating the MVP

The goal is **speed to learning**, not perfection. An [[minimum-viable-product]]:

- Has just enough features to test your core hypothesis
- Can be built in days/weeks, not months
- Is used by **real customers**, not internal testers

**For solo developers:** Your MVP might be a landing page, a Notion doc, or a single Python script. The point is: ship something real that you can measure.

## Measure — Validating Hypotheses

**What to measure depends on your goal:**

| Goal | Metric |
|------|--------|
| Test demand | Sign-ups, waitlist count |
| Test engagement | DAU/WAU/MAU, feature usage |
| Test monetization | Conversion rate, MRR |
| Test retention | Churn rate, cohort retention |
| Test virality | NPS, referral rate |

**Vanity metrics vs. actionable metrics:**

❌ **Vanity:** Total users, page views, app downloads
✅ **Actionable:** Sign-up rate from landing page, churn this week, feature adoption

## Learn — Making Decisions

After measuring, you have two choices:

1. **Persevere** — Data supports your hypothesis. Double down.
2. **Pivot** — Data contradicts your hypothesis. Change direction.

**Types of pivots (per Eric Ries):**
- **Zoom-in pivot** — Single feature becomes the whole product
- **Zoom-out pivot** — Product becomes a single feature
- **Customer segment pivot** — Different target audience
- **Platform pivot** — Change from application to platform (or vice versa)
- **Technology pivot** — Same solution, different tech stack

## The Build Measure Learn Canvas

For each experiment, fill in:

```
HYPOTHESIS: [What we believe]
PRODUCT: [What we built to test it]
METRIC: [How we measured success]
RESULT: [What we learned]
DECISION: [Pivot or Persevere?]
```

## Common Mistakes

1. **Skipping to Build** — Jumping to product without a clear hypothesis to test
2. **Measuring vanity metrics** — Tracking impressions instead of conversion
3. **No baseline** — Not establishing what "success" looks like before building
4. **Ignoring negative data** — Discounting results that contradict your assumptions
5. **Building too much** — MVP has too many features, slowing the feedback loop

## Solo Developer Application

For a [[solo-developer]] building AI-powered products:

```
Week 1: BUILD
├── Ship landing page with waitlist (3 days)
└── Set up analytics (Heap, Posthog, or simple Google Forms)

Week 2: MEASURE
├── 500 visitors, 45 sign-ups (9% conversion)
├── Top objection from survey: "Want to see it before signing up"
└── 12 people said they'd pay $20/mo for early access

Week 3: LEARN
├── Decision: PIVOT from B2C to B2B
├── Build a 1-page demo instead of full product
└── Next: talk to 5 potential B2B customers
```

## Related Concepts

- [[lean-startup]] — The broader methodology
- [[minimum-viable-product]] — What to build
- [[okrs-(objectives-and-key-results)]] — Goal-setting aligned with BML
- [[solo-developer]] — Applying BML as a solo founder
- [[startup-pivoting]] — When and how to pivot

## Further Reading

- [The Lean Startup Principles](https://theleanstartup.com/principles) — Eric Ries
- [The Lean Startup Book](https://www.amazon.com/Lean-Startup-Eric-Ries/dp/0307887898) — Full book
