# OpenAI ChatGPT Plans — worked example

Snapshot date: **2026-07-17**. Pricing pages change silently — re-verify against sources before relying on any number here.

This file is a **cached starting point**, not a substitute for live fetch. Use the SKILL.md verification step to confirm freshness before sending the report to the user.

---

## Surface map (the URLs to fetch in parallel)

| Purpose | URL |
|---|---|
| Pricing landing page (canonical) | https://openai.com/chatgpt/pricing/ |
| Pricing landing page (mirror) | https://chatgpt.com/pricing/ |
| "What is ChatGPT Plus?" | https://help.openai.com/en/articles/6950777-chatgpt-plus |
| "About ChatGPT Pro tiers" | https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers |
| "GPT-5.6 in ChatGPT" (current flagship line) | https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt |
| "Access GPT-4o and GPT-4.1 mini" (legacy tier-framing reference) | https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4o-and-gpt-41-mini |
| ChatGPT release notes (retirements, model rollouts) | https://help.openai.com/en/articles/6825453-chatgpt-release-notes |
| "Introducing ChatGPT Pro" launch (Dec 5 2024) | https://openai.com/index/introducing-chatgpt-pro/ |
| API model catalog (context window, max output) | https://platform.openai.com/docs/models |
| API pricing (per-MTok, not chat subscriptions) | https://openai.com/api/pricing/ |

**Critical caveat about source-surface reliability:** `chatgpt.com/*` and `help.openai.com/*` both implement aggressive bot detection. Direct browser automation on these domains returns "Just a moment..." with zero content (verified 2026-07-17). Use `mcp__exa__web_fetch_exa` to extract the same canonical OpenAI pages — that tool bypasses the bot-detection page and returns the rendered content. See the SKILL.md tool-fallback note for the exact strategy.

---

## Cached data snapshot (July 2026)

### Plan inventory — consumer tier

| Plan | USD price | Billing | Best for |
|---|---|---|---|
| Free | $0 | N/A | Try out ChatGPT |
| **Go** | not cached — extract on demand | Monthly | Longer conversations (may include ads) |
| **Plus** | **$20/mo** | Monthly only (no annual) | Advanced work & productivity |
| **Pro $100** | **$100/mo** | Monthly only | Power user (5× Plus quota) |
| **Pro $200** | **$200/mo** | Monthly only | Research & coding (20× Plus quota, unlimited subject to abuse guardrails) |

Plus and Pro both explicitly state "no annual billing, no multi-month pre-pay" as of this snapshot.

Note: Pro now has two price tiers ($100 and $200) — the original $200 launched Dec 5 2024; the $100 tier was added later as a mid-tier. If the user asks "what's ChatGPT Pro?" without specifying, surface both tiers and the 5× vs 20× distinction.

### Plus features (vs Free / Go)

- Access to advanced reasoning models (full GPT-5.6 family: Sol, Terra, Luna, Thinking Mini)
- Expanded messages & uploads
- More complex & accurate image generation
- Expanded deep research
- Expanded memory & context
- Projects, scheduled tasks, custom GPTs
- Expanded Codex usage
- Expanded ChatGPT Work on desktop, web, and mobile
- **Early access to new features**
- Voice conversations, file uploads & analysis, deep research tools

### Pro features (in addition to Plus)

- **Pro reasoning with GPT-5.6 Sol Pro** (compute-intensive variant)
- 5× or 20× more usage (vs Plus; tier-dependent)
- **Maximum** Codex tasks
- **Unlimited & faster** image generation (subject to abuse guardrails)
- Maximum deep research
- Maximum memory & context
- Expanded projects, tasks, & custom GPTs
- Research preview of new features

### Rate limits — what OpenAI does and does NOT publish

| Metric | Free | Plus | Pro |
|---|---|---|---|
| Flagship model access | Limited GPT-5.5 Instant | Full GPT-5.6 Sol + reasoning variants | Full GPT-5.6 Sol Pro + all variants |
| Rolling window | 5-hour window (when reaching GPT-4o limit, falls back to GPT-4.1 mini) | "Expanded" — relative framing | "Unlimited" subject to abuse guardrails ($200) / 5× Plus ($100) |
| Per-session quota | Limited; fallback to mini model | Up to 5× Free (legacy GPT-4o era wording) | Unlimited or 5× Plus depending on tier |
| Requests/min, tokens/min | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| Multi-surface pool | Yes | Yes | Yes |
| Unused messages roll over? | No | No | No |

**The right answer in the report:** "OpenAI does not publish requests/min or tokens/min for any ChatGPT consumer tier. Plus is described as 'expanded' (legacy phrasing: 'up to 5× Free'); Pro $100 is 5× Plus; Pro $200 is unlimited subject to abuse guardrails. Quota pools are shared across web/iOS/Android. Unused messages do not roll over."

### Context window by model (GPT-5.6 family, API)

| Model | Context window (API) | Max output |
|---|---|---|
| GPT-5.6 Sol | **1.05M tokens** | 128K |
| GPT-5.6 Terra | **1.05M tokens** | 128K |
| GPT-5.6 Luna | **1.05M tokens** | 128K |
| GPT-5.6 Sol Pro | Same family; explicit Plus/Pro only | 128K |

In the ChatGPT consumer interface, the context window is **shared** — the user-input portion is smaller than the API total because space is also used for system instructions, memory content, and internal processing. The pricing page footnote flags this explicitly.

---

## Gotchas specific to OpenAI ChatGPT plans

1. **`chatgpt.com` blocks browser automation.** A live `browser_navigate(url='https://chatgpt.com/pricing')` returns `"Just a moment..."` with `element_count=0` — the page is bot-detected before render. `openai.com` pages render fine. Strategy: route all ChatGPT/help.openai.com extraction through `mcp__exa__web_fetch_exa`, which returns the same canonical content. This bypasses the bot-detection interstice.

2. **GPT-4o and GPT-4 Turbo are RETIRED from ChatGPT as of June 26, 2026.** (Per help center "Retiring GPT-4o" release notes.) Users frequently ask "what's the GPT-4o vs GPT-4 turbo quota in Plus?" — that question is now historically framed. The current flagship line is GPT-5.6 (Sol, Terra, Luna, Sol Pro). When the user asks about retired models, explicitly call out the retirement and present the current line.

3. **OpenAI does not publish numbers** for messages/hour/day on Plus (or any tier). They use relative framing. Third-party sites cite figures like "150 messages/3 hours" or "80 messages/3 hours for GPT-4o" — these come from community observation, not the vendor. Do NOT cite them as official; the vendor's help-center prose is the source of record.

4. **Two Pro tiers now exist:** $100 (5× Plus) and $200 (20× Plus / unlimited). The December 2024 launch announcement only covers the $200 tier. If the user is reading older material, they may not know $100 exists. Surface both.

5. **Pro $200 ≠ unlimited of all models.** Even Pro $200 has abuse guardrails. Use the verbatim phrase "Unlimited subject to abuse guardrails."

6. **"Plan Go" sits between Free and Plus.** It exists, includes ads, and is mentioned on the pricing page. The user typically asks about the major four (Free / Plus / Pro). If the Go plan is not in scope, mention it briefly so the comparison row count is accurate.

7. **API ≠ consumer plans.** ChatGPT Plus does NOT include API usage — explicit in the Plus help article ("API usage is separate and billed independently"). The $20 consumer plan is flat-rate, not metered. API pricing lives at https://openai.com/api/pricing/ with per-MTok input/output rates.

8. **Plus helps center article is short on numbers but rich on qualitative framing.** Quote the exact bullets ("Higher model limits", "Advanced reasoning access", "Faster response speeds") — these are OpenAI's own words and carry more weight than paraphrases.

---

## Working research note (this session's output)

The 2026-07-17 session for the user covered the Plus plan specifically. Output shape was: 3-column comparison table (Free / Plus / Pro $200), features bullet list, explicit "where OpenAI does NOT publish" section, and citations. The Markdown research note at `/Users/tuananh4865/.hermes/state/research/chatgpt-plus-pricing-research.md` was the working artifact — refer to it if a downstream task asks for the verbatim output of that session.
