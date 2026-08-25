---
title: Business Opportunity Research
name: business-opportunity-research
description: Discover, validate, and evaluate new income stream opportunities — from niche identification to automation feasibility to execution path. Used when Anh asks "what are the ways to make money with X", "find me a niche that can be 100% automated", or "lên plan mở X" (research-first + clarifying questions workflow). NOT for TikTok Shop content (that's tiktok-viral-script or research-analyst).
trigger: When Anh asks to explore a new income stream, find opportunities on a new platform/niche, validate a business model, or build a "plan to open a [shop/business]" (research-first + clarifying-questions-first). NOT for TikTok Shop content (that's tiktok-viral-script or research-analyst).
created: 2026-05-14
updated: 2026-07-29
type: skill
tags: [research, monetization, income-streams, opportunity-validation]
confidence: high
relationships: [research-analyst, tiktok-viral-script]
---

# Business Opportunity Research Skill

Discover, validate, and evaluate new income stream opportunities for Tuấn Anh. This skill fires when Anh asks to explore a new platform, find monetization methods, or evaluate an automation possibility.

## Trigger Conditions

- Anh asks "cách kiếm tiền từ [platform/tool/niche] với AI"
- Anh asks "tìm cho anh các cách kiếm tiền từ affiliate cùng AI"
- Anh asks "niche nào mà automation 100% và em có thể tự làm được"
- Anh asks to evaluate or research an income stream outside TikTok Shop
- Anh asks "is X viable?" or "what's the best way to make money with Y?"

## What This Skill Is NOT

- ❌ NOT for TikTok Shop product research → use `research-analyst`
- ❌ NOT for TikTok content scripts → use `tiktok-viral-script`
- ❌ NOT for TikTok platform strategy → use `research-analyst`

## Workflow

### Step 1: Understand Anh's Constraint

Anh's questions usually have implicit constraints. Identify them:

| Question Pattern | Implicit Constraint |
|-----------------|---------------------|
| "cách kiếm tiền từ X với AI" | Wants comprehensive overview, not deep dive |
| "niche nào automation 100%" | Wants viability assessment, must address "not truly 100%" honestly |
| "tìm cho anh cách kiếm tiền từ Y" | Wants actionable paths, not academic theory |
| "am hiểu nhiều. Bỏ qua!" | Wants new territory, not his existing expertise |
| **"lên plan X" / "lên kế hoạch mở X" / "build plan cho X"** | **Wants research-first → clarifying-questions-first → THEN detailed plan. Do NOT skip clarification phase.** |

**⚠️ CRITICAL (2026-05-14):** When Anh says "không phải ngách tôi am hiểu nhiều. Bỏ qua!" — he is explicitly REJECTING his existing expertise/niche. Proceed with FRESH research only. Do NOT reference his TikTok Shop knowledge.

**⚠️ CRITICAL (2026-07-29):** When Anh says "lên plan X" or "lên kế hoạch mở X" — he is explicitly requesting a **research-first → clarifying-questions-first → THEN plan** workflow. Literal phrasing pattern (29/07/2026 Kon Tum pasta shop): *"Sau khi research thu thập thông tin xong thì hỏi anh những câu hỏi gợi mở để xác định chính xác mục tiêu!"*. Workflow: research → save findings file → use `clarify` tool with 5-6 mixed questions → WAIT for response. Do NOT build a detailed plan before clarification.

### Step 2: Multi-Source Research

Run 3-5 parallel web searches to cover:
1. Current monetization methods (2025-2026 data)
2. Income benchmarks / case studies
3. AI tools involved
4. Automation feasibility
5. Risk/startup cost

### Step 3: Evaluate Against Anh's Constraints

For each opportunity, evaluate:

| Factor | Question |
|--------|-----------|
| Automation potential | Can em do this 100% autonomously after setup? |
| Startup cost | How much time/money to start? |
| Income ceiling | What's the realistic income range? |
| Timeline to first dollar | Weeks? Months? Never? |
| Skill required | Does em need to learn new skills beyond AI? |

### Step 4: Honest Assessment (CRITICAL)

**⚠️ NEVER promise 100% automation.** Every session must say this clearly.

Reality of "automated" affiliate marketing:
- Setup always requires human (accounts, verification, decisions)
- Payment systems need human verification
- Chargebacks/disputes need human decisions
- Platform ToS prohibits fully bot-run businesses

### Step 5: Present Findings + Ask Clarifying Questions (CRITICAL for "lên plan X" requests)

Two modes based on trigger:

**Mode A — pure research request** ("cách kiếm tiền từ X", "niche nào automation 100%"):
Use the existing Opportunity Map structure below. End with decision prompt letting Anh pick direction.

**Mode B — "lên plan mở X" / "build plan cho X"** (added 2026-07-29):
After research is saved to a findings file under `wiki/projects/<topic>-research/research/`, present:

1. **Bức tranh lớn** — market size, demographic, economy (3-5 bullet)
2. **Khoảng trống thị trường / competitors** — table with key gaps
3. **3-5 hướng đi khả thi** — table with vốn / USP / rủi ro columns
4. **Câu hỏi gợi mở** — 5-6 questions mixing multiple-choice (via `clarify` tool, max 4 options each) + open-ended constraints:
   - Vốn khả dụng? (<500tr / 500tr-1 tỷ / >1 tỷ)
   - Target khách hàng chính? (SV, gia đình, du khách, văn phòng, etc.)
   - Mục tiêu chính? (doanh thu ổn định / scale brand / test nhanh)
   - Đã có mặt bằng? (có / chưa / đang tìm)
   - Kinh nghiệm F&B trước đây? (chưa / 1-2 năm / nhiều năm)
   - Muốn em đi sâu hướng nào trước?
5. **WAIT for response** — do NOT build the detailed plan yet. Plan comes after Anh picks direction + answers constraints.

```
## [Platform/Tool]: [Opportunity Name]

### What it is
Brief description (2-3 sentences)

### How much money
Realistic income data with sources

### What em does
Specific tasks em can do with AI

### What em CANNOT do (honest)
What's blocked by platform rules / requiring human

### Startup path
What needs to happen before earning begins

### Verdict
Pursue / Pivot / Discard — with reasoning
```

## Session-Specific Learnings (References)

- `references/roblox-ai-monetization.md` — Roblox + AI income paths, AI tools (Roblox Assistant, Lux AI, MCP), revenue splits, case studies, success metrics
- `references/affiliate-ai-monetization.md` — Affiliate + AI income paths, AI tools for automation, high-tier programs, recurring commission strategy
- `references/automation-reality.md` — Why "100% automation" is marketing fiction, what's actually automatable, what requires human intervention
- `references/microtask-platforms.md` — Fast $30 income: Freecash (instant PayPal), Microworkers, Fiverr (slower). Platforms, min payouts, timeline to first dollar
- `references/kontum-pasta-shop-research-2026-07-29.md` — Case study: "lên plan mở tiệm mì Ý ở Kon Tum". Validates research-first + clarifying-questions workflow + 5-directions matrix template.

## Output Format

When presenting research results:

**Required sections:**
1. **Bức tranh lớn** — market size, overall income data
2. **Các con đường** — numbered list of income paths with specifics
3. **AI tools involved** — specific tools with purposes
4. **Revenue split/cut** — real numbers, not percentages only
5. **Case studies** — real examples with real numbers
6. **⚠️ Lưu ý quan trọng** — honest assessment of limitations
7. **Anh muốn đi sâu hơn vào con đường nào?** — decision prompt

**Tone:** Direct, honest about limitations, no fluff. Vietnamese casual.

## QA Checklist

- [ ] Real income data with sources (not "can earn thousands")
- [ ] Specific AI tools named (not "AI tools")
- [ ] Honest limitation assessment (no false promises)
- [ ] Actionable next steps (not "learn more")
- [ ] Decision prompt at end (let Anh choose direction)
- [ ] **For "lên plan X" requests**: clarifying questions asked via `clarify` tool BEFORE building detailed plan

## Pitfalls (AVOID THESE)

### Research Mistakes
- ❌ **Promising 100% automation** — always caveat. Even "fully automated" systems need setup + occasional human intervention
- ❌ **Using old data** — affiliate marketing changes fast. Use 2025-2026 data only
- ❌ **Vague income claims** — "can earn good money" = not research. Use real numbers

### Output Mistakes
- ❌ **Too long** — if >2 pages, it's a report not a brief
- ❌ **No decision prompt** — always give Anh a choice of direction
- ❌ **Ignoring Anh's constraints** — "not my niche" means don't reference existing TikTok knowledge
- ❌ **Skipping clarification phase** — for "lên plan X" requests, MUST ask clarifying questions via `clarify` tool before building detailed plan. Never start with "Here's your 10-step plan" without knowing budget/target/experience level.

### Framing Mistakes
- ❌ **Academic framing** — "here's how the industry works" = boring. Lead with money
- ❌ **Multiple options without commitment** — pick the highest-potential and say why

## Related
- [[research-analyst]] — TikTok Shop-specific research
- [[tiktok-viral-script]] — TikTok content creation
- [[hermes-autoresearch]] — Nightly research automation