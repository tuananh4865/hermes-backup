# Z.ai / Zhipu AI (GLM) Plans — worked example

Snapshot date: **2026-07-17**. Pricing pages change silently — re-verify against sources before relying on any number here.

This file is a **cached starting point**, not a substitute for live fetch. Use the SKILL.md verification step to confirm freshness before sending the report to the user.

---

## Surface map (the URLs to fetch in parallel)

| Purpose | URL |
|---|---|
| Coding Plan landing + subscribe | https://z.ai/landing-page/coding-plan (also /subscribe) |
| API pricing per token | https://docs.z.ai/guides/overview/pricing |
| Usage Policy (rate limits / concurrency) | https://docs.z.ai/devpack/usage-policy |
| GLM-5.2 model page (1M context) | https://docs.z.ai/guides/llm/glm-5.2 |
| API rate-limit reference | https://docs.z.ai/api-reference/rate-limit.md (redirects to https://z.ai/manage-apikey/rate-limits — login-walled) |
| Main developer docs hub | https://docs.z.ai |
| China-domestic entry point (CNY pricing) | https://bigmodel.cn/ |
| Free chat (consumer-facing) | https://chat.z.ai/ |

**Critical naming note:** the international-facing product is `Z.ai` (domain z.ai, docs docs.z.ai), but it is the same company as **Zhipu AI / 智谱AI** whose developer platform is `bigmodel.cn`. Pricing differs — USD on z.ai, CNY on bigmodel.cn. Cite docs.z.ai or z.ai for USD pricing; flag explicitly if quoting the China-domestic page.

---

## Cached data snapshot (July 2026)

### Product surface — TWO different things, easy to confuse

Z.ai ships **two subscription products** that answer different questions:

1. **GLM Coding Plan** — flat-fee subscription for using GLM models inside coding tools (Claude Code, Cline, Roo Code, OpenClaw, Kilo Code, 20+ supported clients). Plan tiers are Lite / Pro / Max.
2. **Z.ai API (pay-per-token)** — no subscription, billed per million tokens. Model price varies per model.

They are NOT the same. The Coding Plan is only usable inside the listed coding tools; the API is OpenAI-compatible and works anywhere. A user who wants to embed GLM into their own product needs the API, not the Coding Plan.

### Plan inventory — GLM Coding Plan

| Plan | USD price (monthly) | USD price (annual, –30%) | Best for (vendor copy) |
|---|---|---|---|
| **Lite** | **$18/mo** | **$12.60/mo** ($151.2/yr) | "Built for lightweight iteration on small repo" |
| **Pro** (Popular) | $72/mo | $50.40/mo ($604.8/yr) | "Built for day-to-day development on mid-sized repo" — 5× Lite usage |
| **Max** (Max Usage) | $160/mo | $112/mo ($1344/yr) | "Built for advanced users working on mid-to-large repo" — 20× Lite usage |
| Free (chat.z.ai) | $0 | N/A | Web chatbot with GLM-4.5-Flash / GLM-4.7-Flash |

**Quarterly billing also exists, at –20%.** The annual 30% discount is the headline number — always quote both.

### Lite tier feature detail (the one closest to $20/mo budget)

- **Models included:** GLM-5.2 (flagship, 1M context), GLM-5-Turbo, GLM-4.7, GLM-4.5-Air — same lineup as Pro and Max
- **Quota:** ~80 prompts per 5-hour window, ~400 prompts per week
- **MCP allowance:** 100 web-search/reader calls per month (Vision Analysis, Web Search, Web Reader, Zread MCP)
- **Concurrency:** recommended for 1 project at a time (vs 1–2 for Pro, 2+ for Max)
- **Peak-hour multiplier:** 3× quota consumed during peak, 2× off-peak. **Promo through Sept 2026: 1× off-peak** (limited-time).
- **Tools supported:** 20+ coding tools including Claude Code, Cline, Roo Code, OpenClaw, Kilo Code
- **No pay-as-you-go overage.** Hit the cap and the plan stops — does NOT auto-upgrade.

### Tier-differentiating features (what Pro and Max add over Lite)

| Feature | Lite | Pro | Max |
|---|---|---|---|
| Quota (5h / weekly) | 80 / 400 | 400 / 2,000 (~5× Lite) | 1,600 / 8,000 (~20× Lite) |
| MCP calls / month | 100 | 1,000 | 4,000 |
| Concurrent projects | 1 | 1–2 | 2+ |
| Model access | Rolling access | Priority access | First access to new flagship |
| Peak priority | Standard | Faster generation | Dedicated resources during peak |
| Curated MCP toolset | — | Yes | Yes (all of Pro's) |

### Rate limits — what Z.ai does and does NOT publish

**Z.ai Coding Plan does NOT use traditional RPM/TPM.** Quotas are prompt-based with a rolling 5-hour window plus a weekly cap. The official docs (`/devpack/usage-policy`) state only:

- "Rate (concurrency) limits are tied to your plan tier."
- "The platform dynamically adjusts these limits based on resource availability, with the general principle being Max > Pro > Lite."

For API users (not Coding Plan), the rate-limit reference page is at `docs.z.ai/api-reference/rate-limit.md` but redirects to a login-walled account page — exact RPM/TPM numbers per model require a registered API key to view.

**Right answer in the report:** *"Z.ai Coding Plan measures usage in prompts, not RPM/TPM. Lite ≈ 80 prompts per 5-hour rolling window and 400/week. Peak hours consume 3× quota (promo: 1× off-peak through Sept 2026). API rate limits (RPM/TPM) are published per logged-in account, not on public docs."* Do not invent numbers.

### Context window — GLM-5.2 (current flagship, available on all Coding Plan tiers)

| Spec | Value |
|---|---|
| Context window | **1,048,576 tokens (1M)** — solid (not degraded near the edge) |
| Max output | 131,072 tokens (128K) |
| Long-context model ID | `glm-5.2[1m]` — the `[1m]` tag matters; endpoint won't infer it |
| Thinking modes | Fast / Deep (dual thinking effort) |
| Architecture | 744B MoE (per third-party reporting) |

### API pricing — GLM-5.2 and adjacent models (USD per 1M tokens)

| Model | Input | Cached Input | Output | Notes |
|---|---|---|---|---|
| GLM-5.2 | $1.40 | $0.26 | $4.40 | Current flagship, 1M ctx |
| GLM-5.1 | $1.40 | $0.26 | $4.40 | Aligned with Claude Opus 4.6 |
| GLM-5 | $1.00 | $0.20 | $3.20 | |
| GLM-5-Turbo | $1.20 | $0.24 | $4.00 | |
| GLM-4.7 | $0.60 | $0.11 | $2.20 | |
| GLM-4.7-Flash | **Free** | **Free** | **Free** | Rate-limited |
| GLM-4.6 | $0.60 | $0.11 | $2.20 | |
| GLM-4.5 | $0.60 | $0.11 | $2.20 | |
| GLM-4.5-Air | $0.20 | $0.03 | $1.10 | |
| GLM-4.5-Flash | **Free** | **Free** | **Free** | Rate-limited |

Cached input storage is "Limited-time Free" across most models as of snapshot.

### Free tier (chat.z.ai)

- **Price:** $0
- **Models:** GLM-4.5-Flash, GLM-4.7-Flash free with rate limits; flagship models (GLM-5.x) accessible on the web chatbot but rate-limited and not officially documented
- **Context window:** 128K for Flash models; up to 1M for flagship when reached via API
- **Rate limits:** Not published; third-party reports ~50 requests/day on OpenRouter free tier for GLM-4.5-Air as a rough proxy

---

## Gotchas specific to Z.ai / Zhipu

1. **Two domains, one company.** z.ai (international, USD) ≠ bigmodel.cn (China-domestic, CNY). Same models, different pricing surfaces. Default to docs.z.ai for international users; flag the China-domestic alternative.
2. **There is no $20/mo tier.** The Lite plan is **$18/mo** monthly or **$12.60/mo** annual. If the user asks for a $20/mo plan and means "closest to $20", Lite is the answer. If they mean Anthropic Pro pricing parity ($20/mo), there is no direct equivalent — Lite is +$2 short, Pro is +$52 over.
3. **No traditional RPM/TPM.** Coding Plan quotas are prompt counts, not tokens-per-minute. Saying "RPM" or "TPM" for the Coding Plan is a category error. Mention it in the report.
4. **Quota is consumed 3× during peak hours, 2× off-peak.** Off-peak is currently discounted to 1× through Sept 2026 as a limited-time promotion. If the report lands after Sept 2026, re-verify the promo status.
5. **No pay-as-you-go overage.** When Coding Plan quota is exhausted, the plan stops — does NOT charge extra per prompt. This is different from Cursor/Windsurf-style credit top-ups.
6. **Login-walled rate limits.** Public docs do not show per-model RPM/TPM for API users. The reference page redirects to z.ai/manage-apikey/rate-limits which requires sign-in. If the user needs exact numbers, tell them to log in and check there.
7. **Plan is for coding tools only.** Using the Coding Plan outside Claude Code / Cline / OpenClaw etc. is prohibited per the Usage Policy and may result in subscription restrictions. Embedding GLM into your own product needs the API, not the Coding Plan.
8. **Free models exist in the API too.** GLM-4.5-Flash and GLM-4.7-Flash are genuinely free on the API (not just the chatbot), with rate limits. Useful baseline for budget-conscious developers.
9. **Regional availability.** chat.z.ai reportedly works without VPN from some regions (e.g. Russia per third-party reports); verify before recommending for the user's location. Default to: "available internationally via z.ai" without specifics.

---

## Notes for the next agent doing this same task

1. **Start at z.ai/landing-page/coding-plan** — it has all three tiers on one page with current pricing. The docs.z.ai pricing page has per-token API pricing but not the subscription tiers.
2. **For API-only questions (not subscription)**, use docs.z.ai/guides/overview/pricing. The full per-model table is rendered in the `<main>` element and can be extracted via `browser_console` with `expression="document.querySelector('main').innerText"` if `web_extract` fails (DuckDuckGo backend returns "search-only" errors on direct URL extraction).
3. **For free tier details**, chat.z.ai is the consumer surface — but it doesn't publish rate limits in a help-center article. Third-party aggregators (tokenmix.ai, free-llm.com) report approximate numbers; treat as proxy data, not official.
4. **The closest competitor benchmark** is Anthropic Pro at $20/mo. Z.ai Lite at $18/mo is +2 under; Z.ai Pro at $72/mo is ~3.6× Anthropic Pro; Z.ai Max at $160/mo competes with ChatGPT Pro at $200/mo.
5. **When user asks for "$20 plan of Zhipu"**, they likely heard about Z.ai from a coding-tools ecosystem post and confused the $20 figure with Anthropic's Pro tier. Surface the comparison explicitly in the report — don't just say "no $20 plan exists".