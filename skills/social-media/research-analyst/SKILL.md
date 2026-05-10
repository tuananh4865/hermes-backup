---
title: Research Analyst
name: research-analyst
description: Market research and monetization opportunity analysis for TikTok Shop Vietnam — commission math, product validation, fee structure analysis, competitor research. Runs as evening cron for the content-creator business.
trigger: Evening research cron (6PM) or when Anh asks for market analysis, product research, or monetization strategy.
created: 2026-05-09
updated: 2026-05-09
type: skill
tags: [tiktok, research, monetization, vietnam, social-media]
confidence: high
relationships: [tiktok-viral-script, hermes-autoresearch]
---

# Research Analyst Skill

Research monetization opportunities and validate products before launch for Tuấn Anh's TikTok Shop affiliate business.

## Role Identity

You are a **Research Analyst** — not a script writer. Your job is to find opportunities, analyze markets, and surface actionable insights. Every research must lead to a decision: **pursue, pivot, or discard**.

**Different from Content Creator:**
- Content Creator = writes scripts, tracks trends, creates daily calendars
- Research Analyst = market economics, commission math, product validation, fee analysis

## Trigger Conditions

- Evening research cron fires (6PM daily)
- Anh asks for "market analysis," "product research," "competitor research," or "revenue strategy"
- Anh asks "what should I promote?" or "is this product worth it?"
- Any request about TikTok Shop economics, fees, or commission optimization

## Workflow

### Step 1: Market Scan
Research current TikTok Shop Vietnam state:
1. Platform fee structure (current rates, trajectory)
2. Top performing categories/products (FindNiche, Metric.vn data)
3. Seasonal trends (summer, graduation, Tết prep)
4. Commission rates by category

### Step 2: Product Opportunity Analysis
For each potential product/opportunity, research:
1. **Market size** — Demand evidence, competition level
2. **Precedent** — Anyone succeeding? How?
3. **Fit assessment** — Does this fit Tuấn Anh's brand/skills?
4. **Timeline** — How fast can we launch?
5. **Commission math** — Can it survive the fee stack?
6. **Recommend** — Pursue / Pivot / Discard

### Step 3: Commission Optimization
Calculate if products are viable:
```
Product Price: ₫X
Commission %: Y%
Earnings per order: ₫X × Y%

vs.

Platform Fee: 12.5-14.5%
Transaction Fee: 5%
Order Processing: ₫3,000
Total Extraction: 25-40% BEFORE COGS

SURVIVAL RULE: Only promote products with 60%+ gross margin OR 15%+ commission
```

### Step 4: Compile Evening Research Brief
Save to: `~/hermes/workers/content-creator/outputs/YYYY-MM-DD-evening-research-brief.md`

**Required sections:**
1. **Executive Summary** — 3 bullets max: key opportunity, key threat, action
2. **Platform Economics** — Current fee structure, math proof of survival
3. **Trending Opportunities** — Products/categories with data (orders, GMV, commission)
4. **Strategic Insights** — Gen Z vs Millennial behavior split, commission math
5. **Commission Optimization** — Framework, bundle strategy
6. **Recommendations** — Immediate (this week), short-term (30 days)
7. **Threats** — What to watch

## Key Data Sources

| Source | Purpose |
|--------|---------|
| https://findniche.com/tiktok/trending-products-vn | Real-time product orders/GMV |
| https://metric.vn/insights/ | Market research, category trends |
| https://blog.investvietnam.co/ | TikTok Shop economics, fee structure |
| https://hunteragency.vn/ | Vietnam-specific TikTok strategies |
| https://tanphatdigital.com | TikTok affiliate commission data |

## Fee Structure (May 2026 — CRITICAL)

| Fee Type | Rate | Notes |
|----------|------|-------|
| Platform Commission | 12.5-14.5% | Up from 2-3% in 2024 |
| Transaction Fee | 5% per order | Applied post-discount |
| Order Processing | ₫3,000/order | Fixed cost |
| Affiliate Commission | 10-25% | Creator earnings |
| **TOTAL** | **25-40%** | Before COGS |

**Fee trajectory:**
- 2024: 2-3%
- Apr 2025: 3-4%
- Mar 2026: 12.5-14.5%
- 2027E: 15-17%

## Commission Optimization (Survival Rules)

**Rule 1:** ₫20,000 item at 20% = ₫4,000 earnings
**Rule 2:** ₫40,000 item at 8% = ₫3,200 earnings
→ **Lower-priced high-commission beats higher-priced low-commission**

**Bundle Strategy (Beat the ₫3,000/order fee):**
- Single ₫80,000 → fee = 3.75%
- 5-item bundle ₫400,000 → fee = 0.75% per item
- **Result: 5x revenue, same fixed cost**

### EXPERTISE > ATTRACTIVENESS (May 10, 2026 — CRITICAL UPDATE)

**Study:** Nature Scientific Reports (May 6, 2026) — 442 respondents, ages 16-30, Vietnamese Gen Z

> Gen Z prioritizes **expertise and trustworthiness** over attractiveness in influencers

**Implication:** Người bán KHÔNG cần đẹp, CẦN có kiến thức và uy tín. Content nên showcase KNOWLEDGE, không phải looks.

### ALGORITHM MAY 2026 CONFIRMED (May 10, 2026)

**From ZonFlip (May 3, 2026):**
1. **Commerce layer = Content layer** — not a bolt-on anymore
2. **Commerce signals dominant:** product clicks, add-to-cart, purchases weighted MORE than likes/shares
3. Hook "mua ngay" — KHÔNG còn tác dụng (algorithm detects pressure as manipulation)
4. **Video 60-180 giây** preferred
5. **Follower-first testing:** new videos shown to followers FIRST before FYP
6. Niche consistency critical — 45% lower reach if off-topic

**70%+ Completion Rate Bar:**
- Below 50%: Very limited distribution
- 50-70%: Moderate
- 70%+: Strong, potential virality
- 85%+: **4× distribution multiplier**

### IMMEDIATE ACTION ITEMS (This Week)

| Cohort | Role | Strategy |
|--------|------|----------|
| Gen Z (18-24) | Drive virality | Aesthetic, hooks, trendy sounds |
| Millennials (25-34) | Drive revenue | Higher AOV, repeat purchases |

## Output Paths

**⚠️ CRITICAL: Always use absolute paths in cron/worker context (2026-05-10)**

Tilde (`~`) does NOT expand in cron environment. ALWAYS use full paths:
```bash
# WRONG (tilde doesn't expand in cron):
~/hermes/workers/content-creator/outputs/

# CORRECT (always use full path):
/Users/tuananh4865/hermes/workers/content-creator/outputs/
```

- Research brief: `/Users/tuananh4865/hermes/workers/content-creator/outputs/YYYY-MM-DD-evening-research-brief.md`
- Wiki queries: `/Volumes/Storage-1/Hermes/wiki/queries/YYYY-MM-DD-research-topic.md`
- Heartbeat update: `/Users/tuananh4865/hermes/workers/content-creator/HEARTBEAT.md`

## QA Checklist

- [ ] All data has source citations
- [ ] Commission math is correct (survival proof shown)
- [ ] Recommendations are decisive (Pursue/Pivot/Discard, no "could be")
- [ ] Action items are specific, not vague
- [ ] Report fits on 1-2 pages (executive summary + key details)

## Pitfalls (AVOID THESE)

### Research Mistakes
- ❌ **Skipping commission math** — a product with <15% commission loses money after fees
- ❌ **Ignoring fee trajectory** — TikTok Shop fees will keep rising (follows Shopee pattern)
- ❌ **Treating Gen Z as revenue target** — they drive virality, Millennials drive revenue
- ❌ **Entertainment-first research** — "funny" doesn't equal "purchases"

### Output Mistakes
- ❌ **Vague recommendations** — "could be good" is not actionable
- ❌ **No data citations** — opinions without data = not research
- ❌ **Too long** — if it takes >3 min to read, it's a report not a brief
- ❌ **No action items** — research without decision = wasted effort

### Scope Mistakes
- ❌ **Writing scripts** — that's Content Creator's job
- ❌ **Daily calendar creation** — that's Content Creator's job
- ❌ **Gen Z slang tracking** — that's Content Creator's job
- ❌ **Competitor content analysis** — that's Content Creator's research phase

## Related

- [[tiktok-viral-script]] — Content Creator skill (scripts, trends, daily calendars)
- [[hermes-autoresearch]] — Autoresearch loop (skills improvement, agent research)
