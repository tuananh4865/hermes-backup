---
name: ai-vendor-pricing-research
description: Research any AI/SaaS vendor's subscription plans (Free / paid tiers / Enterprise) and return a structured fact sheet — plan names, USD pricing, included features, rate/usage limits, context window or other key specs, and a clean Free-vs-paid-vs-top comparison — cited to the vendor's official pages. Use when the user asks "gói X của Y", "Y pricing tiers", "Pro plan của Z có gì", "so sánh gói Free và Pro của Y", "rate limits của API Y", or any research that needs the official pricing/features of an AI product (Anthropic, OpenAI, Google, Cursor, etc.) backed by vendor sources, not third-party blog summaries.
---

# AI Vendor Pricing & Plans Research

The deliverable for this class of task is a **vendor-verified fact sheet** — exact plan names, exact USD prices, the features that distinguish each tier, the rate/usage limits (or an honest statement that the vendor does not publish them), and a side-by-side comparison. Always cited to the vendor's own pages.

This is NOT a blog-roundup research task. Third-party "best AI tools 2026" articles are out of scope as primary sources — they are downstream of the vendor's own pages and often contain stale data. Go to the vendor.

## When to use this skill

Trigger when the user asks for any of:

- "Gói Pro / Max / Team / Enterprise của [vendor] có gì?"
- "$X/tháng của [vendor] bao gồm features gì?"
- "Rate limits / context window / token limits của [vendor]"
- "So sánh Free vs Pro vs [higher tier] của [vendor]"
- "Có nên upgrade lên [tier] không?"
- "Pricing của API [vendor]" — though API pricing is a sub-case; see step 5 below
- Delegated research: parent agent asks to "research gói X $Y/tháng" with a structured output schema

Distinct from these neighbors (do NOT use this skill):
- **Generic ML model benchmarks** → `ml-model-comparison-report`
- **Deep multi-pillar research** → `deep-research-multi-pillar`
- **Product research for affiliate content** (TikTok Shop / Shopee product pages) → `tiktok-shop-product-research`
- **YouTube/social platform strategy research** → `youtube-channel-audit`, `social-media-research`

## Step-by-step workflow

### 1. Identify the vendor's official pricing surface

Every AI vendor has at least one of these. Find and bookmark them in parallel:

- **Pricing page** — usually `/pricing` (e.g. `https://www.anthropic.com/pricing`, `https://openai.com/chatgpt/pricing`, `https://cursor.com/pricing`)
- **Plans help center** — usually under `support.<vendor>.com` or `help.<vendor>.com` (e.g. `https://support.anthropic.com/en/articles/11049762-choosing-a-claude-ai-plan`)
- **Per-plan articles** — one article per tier (`what-is-the-pro-plan`, `what-is-the-team-plan`, etc.)
- **Original launch announcement** — `/news/<plan-name>` on the vendor's newsroom (gives historical context)
- **Model documentation page** — for context window / max output (e.g. `https://docs.anthropic.com/en/docs/about-claude/models`)

Search query patterns that surface these directly:
- `site:<vendor>.com pricing` or `site:<vendor>.com plans`
- `"<plan name>" pricing <vendor>`
- `<plan name> site:support.<vendor>.com`

### 2. Fetch pricing + per-plan articles in parallel

Always fetch in one batched call — these pages are independent and load much faster together than serially.

Minimum set per task:
- The pricing landing page
- The specific plan article for the tier the user asked about (e.g. "What is the Pro plan?")
- The model/docs page if context window is in scope
- The launch announcement (only if you need historical context or the feature list is unclear)

If `web_extract` fails (DuckDuckGo backend returns "search-only" error), fall back to **`mcp__exa__web_fetch_exa`** which extracts full content from known URLs.

**Special case: `chatgpt.com/*` and `help.openai.com/*` block browser automation** with a Cloudflare "Just a moment..." interstice — direct `browser_navigate` returns `element_count=0`. `openai.com/*` pages render fine. Strategy for any ChatGPT research:

1. **Skip `browser_navigate` for `chatgpt.com/*` / `help.openai.com/*`** — they bot-block.
2. **Use `mcp__exa__web_fetch_exa`** with the canonical URLs (`openai.com/chatgpt/pricing/`, `help.openai.com/en/articles/...`). exa returns the same rendered content OpenAI serves to browsers, bypassing the bot-detection page. Verified 2026-07-17.
3. **`openai.com` (root domain) DOES work in browser** — use `browser_navigate` there without issue.
4. **Always include the launch announcement URL in the batch** (`openai.com/index/introducing-<plan>/`) — for ChatGPT specifically, it carries historical context the live pages don't (e.g. Pro $200 launch benchmarks from Dec 5 2024).

This bot-block pattern may apply to other AI vendors too (Anthropic's `claude.ai`, Google's `gemini.google.com`, etc. — apply the same strategy preemptively if `browser_navigate` returns an empty snapshot on a `.com` consumer surface).

### 3. Extract the canonical schema

For each plan in the comparison, capture exactly these fields. Do not paraphrase prices — quote the number as written.

| Field | Rule |
|---|---|
| Plan name | Exact display name on the pricing page (e.g. "Pro", "Max 5x", "Team Standard") |
| Price (USD) | Monthly USD price. If billing has multiple cycles, list both (e.g. "$20/month or $17/month with annual — $200 up front") |
| Billing cycle | Monthly / Annual / Both / N/A |
| Target user | "Best for" verbatim from vendor |
| Usage/session limit | Quote the vendor's own metric. If they say "5× Free", quote that |
| Window | "5 hours" / "weekly" / "monthly" / "daily" — vendor's own framing |
| Key features | Only features that DIFFERENTIATE this tier from the one below |
| Context window | Only if the plan grants access to multiple models with different windows — list the per-model window |
| Citations | Vendor URL + section/heading anchor where the data came from |

### 4. Be honest about what the vendor does NOT publish

Many AI vendors intentionally do NOT publish granular rate limits. This is a feature, not a missing data point.

**Known non-disclosure patterns (vendor-verified):**
- **Anthropic Claude.ai plans:** No requests/min, no tokens/min, no daily cap in numbers. Uses composite "usage units" with rolling 5h session + weekly cap. State this explicitly in the report — do NOT fabricate a number.
- **OpenAI ChatGPT plans:** Similar — usage tiers described relatively ("more than Free", "5× Free", "5× / 20× Plus") with rolling-window quotas, not raw req/min. Quota pools are shared across surfaces; unused messages do NOT roll over. The GPT-4o / GPT-4 turbo quota question is now historically framed because those models were retired from ChatGPT in June 2026 — current line is GPT-5.6 family (Sol, Terra, Luna, Sol Pro).
- **Cursor / coding tools:** Often credit-based or "X requests/month" with model multipliers.

When the vendor hides numbers: quote the vendor's own qualitative language ("at least 5× more usage per 5-hour session") and call out the non-disclosure in a dedicated line. The user gets more value from "vendor does not publish" than from a hallucinated "60 requests/min".

### 5. Sub-case: API pricing

If the user asks about **API pricing** (not consumer/team plans), the schema shifts:

- Pricing is per million tokens (MTok) for input and output
- Prompt caching pricing is separate (write vs read)
- Batch API discount is ~50%
- Long-context pricing may tier (e.g. >200K tokens at 2×)
- Add the model name and API ID
- **Do NOT confuse API pricing with consumer-plan pricing** — the same vendor has both. ChatGPT Plus at $20/mo is flat-rate and does NOT include API credits.

Vendors often list API pricing on the SAME pricing page as consumer plans — pull both.

### 6. Compose the final report

Structure (adapt for the requested plan but keep this spine):

1. **Headline card** — plan name + price + one-line positioning
2. **Features** — Free-equivalent features + tier-differentiating features
3. **Rate limits** — verbatim numbers if published; explicit non-disclosure if not
4. **Context window / key specs** — per-model breakdown
5. **Comparison table** — Free vs requested plan vs next tier up
6. **Bottom line** — when this plan is the right call
7. **Citations** — full URLs of vendor pages used

Use the user's reading language (the request was Vietnamese → respond in Vietnamese; English request → English). Currency: USD unless the user specified otherwise.

## Output format — strict

The user asked for **CHÍNH XÁC** (exact) fields. Use this exact structure so a parent agent or downstream task can parse it deterministically:

```
## Tóm tắt
- Plan name: <exact>
- Price USD: <monthly>/<annual>
- Best for: <verbatim vendor copy>

## Features
- Tier-differentiating features (bullet)

## Rate limits
- Session window: <value>
- Per-session quota: <vendor's number or "5× Free-tier equivalent">
- Weekly/daily/monthly caps: <value or "vendor does not publish">
- Requests/min, tokens/min: <value or "NOT PUBLISHED — vendor uses composite usage units">
- Multi-surface pooling: <yes/no + what pools>

## Context window / specs
- Per-model token limits (table)

## Comparison Free vs Pro vs <next tier>
- Feature matrix table

## Citations
- <vendor URLs>
```

## Pitfalls

- **Don't trust third-party "AI tools comparison" blogs** as primary sources. They lag the vendor and often quote stale prices.
- **Don't conflate API pricing and consumer/team plan pricing.** API is per-MTok; consumer plans have no per-token cost (it's a flat subscription).
- **Watch the annual-discount footnote.** Most vendors list a monthly price but offer a discount for annual payment — e.g. Anthropic Pro is "$20/mo or $17/mo with annual ($200 up front)". Missing the annual price = wrong.
- **Region matters.** Anthropic lists price as $20 US / £18 UK in some surfaces — flag the region, default to USD.
- **Don't fabricate numbers when the vendor doesn't publish them.** "Vendor does not publish rate limits" is a valid and preferred answer over made-up req/min.
- **Snapshot the date.** Pricing pages change silently. The report should note the date the data was fetched so the user knows its shelf life.
- **Watch for retired model names in the user's question.** GPT-4o, GPT-4, GPT-4.1, o4-mini, o1-preview, o1-mini — all retired from ChatGPT as of mid-2026. Surface the retirement and pivot to the current line.

## Verification before delivery

Before sending the report, confirm:

1. **Price exactly matches** the text on the vendor's pricing page (no rounding, no "approximately")
2. **Every feature claim is from the vendor's own text** (or sourced to the vendor's docs) — not extrapolated
3. **Citations are live URLs** that you actually fetched, not guesses
4. **Comparison table dimensions** match what the vendor publishes (don't invent a row)
5. **Non-disclosures are explicit**, not hidden behind filler

## Reference points (curated vendor examples)

See `references/anthropic-claude-plans.md` for a worked example of this skill applied to **Anthropic Claude Pro** (the canonical case this skill was built from).

See `references/openai-chatgpt-plans.md` for a worked example applied to **OpenAI ChatGPT Plus**. It includes:

- A cached July 2026 snapshot of plan inventory, Plus/Pro features, the 2-tier Pro pricing ($100 / $200), the retirement of GPT-4o from ChatGPT, and the current GPT-5.6 family context window (1.05M tokens)
- The right URL surface map (including the bot-detection caveat for `chatgpt.com` and `help.openai.com`)
- Gotchas specific to OpenAI: dual Pro tiers, relative-language rate-limit framing, no annual billing on consumer plans, API vs consumer plan split, and the common user question about retired GPT-4o quota

When caching data in `references/<vendor>.md`, **always include the snapshot date and a re-verify-on-fetch reminder**. Vendor pricing pages are updated silently — a stale cache is worse than no cache.

## Cached vendor references (extend when you do this task)

See `references/<vendor>.md` for cached starting points with snapshot dates. Always re-verify against live vendor pages before relying on cached data.

- `references/anthropic-claude-plans.md` — Anthropic Claude (Pro / Max / Team / Enterprise). Quota-not-RPM pattern.
- `references/zai-zhipu-glm-plans.md` — Z.ai / Zhipu AI GLM Coding Plan (Lite / Pro / Max). Quota-not-RPM + dual-domain naming (z.ai USD vs bigmodel.cn CNY) + no-$20-tier gotcha.
