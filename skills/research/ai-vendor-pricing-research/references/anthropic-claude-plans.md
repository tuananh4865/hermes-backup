# Anthropic Claude Plans — worked example

Snapshot date: **2026-07-17**. Pricing pages change silently — re-verify against sources before relying on any number here.

This file is a **cached starting point**, not a substitute for live fetch. Use the SKILL.md verification step to confirm freshness before sending the report to the user.

---

## Surface map (the URLs to fetch in parallel)

| Purpose | URL |
|---|---|
| Pricing landing page | https://www.anthropic.com/pricing |
| "Choose a Claude plan" guide | https://support.anthropic.com/en/articles/11049762-choosing-a-claude-ai-plan |
| Pro plan article | https://support.anthropic.com/en/articles/8325606-what-is-the-pro-plan |
| Max plan article | https://support.anthropic.com/en/articles/11049741-what-is-the-max-plan |
| Team plan article | https://support.anthropic.com/en/articles/9266767-what-is-the-team-plan |
| Enterprise plan article | https://support.anthropic.com/en/articles/9797531-what-is-the-enterprise-plan |
| Models overview (context window) | https://docs.anthropic.com/en/docs/about-claude/models |
| Pro launch announcement (historical) | https://www.anthropic.com/news/claude-pro |

For any plan-specific deep dive, the per-plan help-center article is the highest-fidelity source — it sits below the marketing-style pricing page and gets updated when limits change.

---

## Cached data snapshot (July 2026)

### Plan inventory

| Plan | USD price | Billing | Best for |
|---|---|---|---|
| Free | $0 | N/A | Occasional use |
| **Pro** | **$20/mo** (or $17/mo with annual — $200 up front) | Monthly or annual | Regular use |
| Max 5x | $100 | Monthly | Frequent users |
| Max 20x | $200 | Monthly | Daily power users |
| Team (Standard seat) | $20/seat/mo annual, $25 monthly | Monthly or annual | Teams of 2–150 |
| Team (Premium seat) | $100/seat/mo annual, $125 monthly | Monthly or annual | Heavy team users |

### Pro features (vs Free)

- At least 5× usage per session
- Priority access at high-traffic periods
- Early access to new features
- Claude Code (CLI agent)
- Claude Cowork
- Claude Design
- Claude Science
- Research (deep research mode)
- Unlimited Projects
- Access to more Claude models (Opus, Sonnet, Haiku)
- Claude for Microsoft 365

### Pro rate limits — what Anthropic does and does not publish

| Metric | Value |
|---|---|
| Session window | **5 hours** rolling |
| Weekly limit | Yes — reset at a fixed day/time per account |
| Session quota | **≥ 5× Free** |
| Requests/min | **NOT PUBLISHED** |
| Tokens/min | **NOT PUBLISHED** |
| Daily cap | Not explicitly published; Anthropic reserves the right to add weekly/monthly caps at its discretion |
| Multi-surface pool | **Yes** — web + desktop + mobile + Claude Code share one quota |

The right answer in the report is: **"Anthropic does not publish requests/min or tokens/min for the Pro plan. Usage is measured as composite units; Pro gets at least 5× Free per 5-hour session, plus a weekly cap. All surfaces (web/desktop/mobile/Claude Code) draw from a single pool."** Do not invent numbers.

### Context window by model (available on Pro)

| Model | Context | Max output |
|---|---|---|
| Claude Opus 4.8 | 1M tokens | 128k |
| Claude Sonnet 5 | 1M tokens | 128k |
| Claude Haiku 4.5 | 200K tokens | 64k |
| Claude Fable 5 | 1M tokens | 128k (less available on claude.ai consumer plans) |

---

## Notes for the next agent doing this same task

1. **The pricing-page header for Pro shows "$17 / Per month with annual subscription discount ($200 billed up front). $20 if billed monthly."** — both numbers belong in the report. The help-center "Pro plan" article headline says "$20 per month (US)" and treats $20 as the canonical number. Either is defensible; the report should carry both to avoid surprise at checkout.
2. **Anthropic has aggressive annual promos.** Around major holidays (e.g. "Holiday 2025 Usage Promotion") they run temporary usage boosts — check `/articles/...` recent promos if the task lands near a holiday window.
3. **The Pro launch announcement (Sep 2023, 5x-from-Claude-2 framing) is now historical context only.** Don't quote it as current — it's a snapshot from the Claude 2 era. The help-center articles are the current source.
4. **API pricing is on the same `/pricing` page** but in a separate section. If the user asks about API (not Claude.ai plans), the schema flips to per-MTok input/output + prompt caching rates. API plans are NOT the same as Pro/Max — the Pro plan does not include API usage (explicitly noted in the Pro plan article).
5. **Model training opt-out differs by plan.** Free/Pro/Max all let you opt out of training on your data. Team/Enterprise plans have "no model training on your content by default" — different framing. When the user cares about training data, surface this distinction.
