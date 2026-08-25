# TikTok Shop Product Research — Hermes Autoresearch

> Critical lessons learned 2026-05-05 during TikTok affiliate product research for Tuấn Anh.

## The Problem

Researching TikTok Shop products for affiliate marketing requires specific tab selection and eligibility checks that are NOT obvious from general web research.

---

## Rule #1: "Khớp Nhất" NOT "Bán Chạy Nhất"

**Wrong approach:** Research products from "bán chạy nhất" (best selling) tab
**Correct approach:** Use "khớp nhất" (relevance/recommended) tab

- "Bán chạy nhất" shows bestselling products but they often:
  - Have high competition
  - Already saturated by affiliate creators
  - May not be actively advertised
  - Don't necessarily have affiliate programs

- "Khớp nhất" shows products TikTok is actively promoting via:
  - Product matching to user interests
  - Active ad spend
  - Creator-friendly products
  - Higher affiliate potential

**URL pattern for TikTok Shop Vietnam:**
```
https://shop.tiktok.com/vn/search?q=[keyword]&tab=recommend
```

---

## Rule #2: Affiliate Eligibility — Not All Products Qualify

### FMCG Category = Strict Requirements

Products like **lạp xưởng** (sausage) are FMCG (Fast-Moving Consumer Goods) and have STRICT affiliate requirements:

| Requirement | Threshold |
|-------------|-----------|
| Shop Rating | ≥ 3 stars |
| Negative Review Rate | **< 1%** (FMCG only) |
| Seller-fault Return Rate | **< 2.5%** (FMCG only) |

**Why lạp xưởng fails:**
- Many small sellers can't meet the <1% negative review rate
- Low-quality packaging/shipping = negative reviews
- Even popular products (17K+ orders) may not qualify

### Affiliate Eligibility Check

Products must appear in **TikTok Shop Creator Center → Sàn sản phẩm affiliate** to be promotable.

**Verification method:** 
- Log into TikTok Shop Creator Center
- Check product marketplace for eligibility
- Web search CANNOT determine affiliate eligibility — requires creator account access

---

## Rule #3: Use Browser for TikTok Shop Research

**Why web search fails for TikTok Shop:**
- TikTok Shop is JavaScript-rendered (requires browser)
- Product listings change dynamically
- Tab filtering (khớp nhất vs bán chạy) is client-side
- Prices/stock update in real-time

**Browser approach required:**
```python
# Use browser-harness skill
# Navigate to TikTok Shop search
# Filter by "khớp nhất" tab
# Collect product data manually
```

---

## Rule #4: Product Niches for TikTok Affiliate

Tuấn Anh's target niches:

| Niche | Vietnamese | Examples |
|-------|-----------|----------|
| Snacks | Đồ ăn vặt | dried fruits, nuts, candy, chips |
| Home goods | Gia dụng | kitchen tools, organizers, cleaning |
| Tech | Công nghệ | phone accessories, smart devices, cables |

**NOT qualifying:**
- Lạp xưởng (FMCG, doesn't meet affiliate thresholds)
- Any product with negative review rate ≥1%

---

## Research Workflow (Corrected)

```
1. Open TikTok Shop (real Chrome, NOT headless)
2. Search keyword in target niche
3. Switch to "khớp nhất" tab (relevance)
4. Identify products with:
   - Active ads (many creators promoting)
   - Affiliate-eligible badge
   - Reasonable price point (150K-500K VND)
5. Check Creator Center for eligibility
6. Collect product links
7. Write simple hook script (<45s)
```

---

## Script Format for TikTok Affiliate

**Requirements:**
- Simple shock hook (under 45 seconds)
- NOT complex narrative scripts
- Casual voice: "anh" + "mấy con vợ"
- Gen Z Vietnamese slang

**Hook patterns that work:**
- "Mấy con vợ ơi cứu anh với!" + situation
- "Đây là thứ mà..." + reveal
- "Không ai nói cho anh biết về..." + hook

---

## Key Corrections from Session

| What I Did Wrong | Correction |
|------------------|------------|
| Used "bán chạy nhất" tab | Use "khớp nhất" (relevance) |
| Thought lạp xưởng qualifies | FMCG doesn't meet affiliate threshold |
| Used web search for TikTok | Need browser with real Chrome |
| Complex script approach | Simple hook under 45s |

---

## Rule #5: Platform Fee Reality (Updated 2026-05-07)

**CRITICAL UPDATE:** TikTok Shop Vietnam fees have DRAMATICALLY increased since March 2026:

| Fee Type | Rate | Notes |
|----------|------|-------|
| Platform Commission | 12.5% (marketplace) / 14.5% (Mall) | UP from 2-3% in 2024 |
| Transaction Fee | 5% per order | Applied to post-discount price |
| Order Processing | VND 3,000/order | Fixed, regardless of quantity |
| Affiliate Commission | 10-25% | Paid to creators |
| Advertising Spend | 15-30% of revenue | Market standard |
| **TOTAL COST** | **25-40% of revenue** | Before COGS |

**Profitability math (VND 200,000 product, 50% COGS):**
- After platform fees + affiliate commission + ads = **NET LOSS**
- **ONLY products with 60%+ gross margin survive**
- Fixed VND 3,000/order fee means SINGLE ITEMS under VND 100,000 are unprofitable
- **Bundle strategy is essential** — 5-unit bundles spread the fixed fee

**Fee hike timeline:**
| Period | Commission Rate |
|--------|---------------|
| 2023-2024 | 2-3% (the "easy money" era) |
| Apr 2025 | 3-4% (first hike) |
| Mar 2026 | 12.5% (second hike) |
| Apr 2026+ | Full fee on returned/refunded orders |

---

## Rule #6: Commission Optimization Threshold (Updated 2026-05-07)

**With fees this high, minimum commission is now 15%, target is 20%+:**

| Product | Price | Commission | Earnings |
|---------|-------|------------|----------|
| Item A | VND 20K | 20% | VND 4,000 |
| Item B | VND 40K | 8% | VND 3,200 |

**A VND 20,000 item at 20% EARNS MORE than a VND 40,000 item at 8%.**

---

## Rule #7: Gen Z Buying Behavior — What ACTUALLY Drives Sales (2026 Research)

**IJRPR 2025 academic research (N=204) found:**
- **KOL/KOC influence is #1** (Beta = 0.580) — STRONGEST factor
- **Content trustworthiness is #2** (Beta = 0.301)
- **Entertainment value = NOT significant** (Beta = 0.014, Sig = 0.790)

**Implication:** "Entertaining content attracts attention but does NOT substantially drive purchasing." Gen Z buys because they TRUST the person, not because it's funny.

**For Tuấn Anh's script style:** Personal storytelling + authentic voice = CORRECT strategy. Don't try to be "funny" — try to be TRUSTED.

---

## Rule #8: The "Kiềng Ba Chân" Model (Hunter Agency Vietnam)

**Winning TikTok Shop system — three channels working together:**

| Channel | Role | KPI |
|---------|------|-----|
| TikTok Ads | Scale proven winners, cold reach | ROAS, CPM, CTR |
| Affiliate (KOL) | Expand reach through creator network | Active affiliates, GMV/person |
| KOC (Micro) | Build trust, convert cold → hot | Views, comments, KOC-link orders |

**Why it works:** CPA drops 30-40%, ROAS doubles/triples vs. ads alone.
**KOC budget allocation:** 60% micro (10K-50K) / 30% mid (50K-200K) / 10% macro (200K+)

---

## Rule #9: Gen Z vs Millennial — Different Revenue Roles

| Cohort | Role | Characteristics |
|--------|------|-----------------|
| Gen Z (under 27) | Virality driver | Trend-sensitive, impulse buys, price-sensitive |
| Millennials (25-34) | Revenue driver | Higher AOV, repeat purchases, quality-focused |

**Strategy:** Use Gen Z content patterns for reach, but target Millennials for actual revenue. Same content, different product selection.

---

## Related

- Skill: `hermes-autoresearch` — 2AM nightly research
- Skill: `browser-harness` — for TikTok Shop navigation
- Wiki: `tiktok-viral-script` — script structure
- Wiki: `learned-about-tuananh` — Tuấn Anh's preferences
- Wiki: `queries/tiktok-shop-monetization-research-2026-05` — full research report
