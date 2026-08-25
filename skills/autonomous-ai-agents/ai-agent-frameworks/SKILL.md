---
name: ai-agent-frameworks
description: "Research, analyze, and apply AI coding agent frameworks — Loop Engineering, harness engineering, sub-agent patterns, Builder-Judge-Manager self-correcting loops. When Anh shares an X/Substack article about coding agents (Claude Code, Codex, OpenAI tools, MCP), or asks to compare agent architectures, or wants to implement a 5-block loop pattern (automations, worktrees, skills, MCP, sub-agents)."
title: AI Agent Frameworks — Research & Application
created: 2026-06-01
updated: 2026-07-19
type: skill
tags: [ai, agents, engineering, research, framework, loop-engineering, self-correcting, builder-judge-manager]
confidence: high
relationships: [xurl, hermes-autoresearch, adversarial-content-verifier, wiki-product-ground-truth, evidence-first-delivery, qa-gate, evidence-gate]
trigger: |
  - Anh shares an article/tweet about Claude Code, Codex, MCP, sub-agents, or AI agent patterns
  - Anh asks "phân tích bài này" + URL of an X post or Substack about coding agents
  - Anh asks about applying agent patterns to his own workflows
  - Anh wants to implement automations, worktrees, skills, MCP, or sub-agents
  - Anh asks "làm sao để em tự bắt lỗi trước khi gửi anh?" or shares self-correcting-loop content
---

# AI Agent Frameworks — Research & Application

## Trigger Conditions

Load this skill when Anh:
- Shares a tweet/Substack URL about Claude Code, Codex, MCP, sub-agents, or AI agent frameworks
- Asks to analyze a recent article by Addy Osmani, Boris Cherny, Peter Steinberger, Cyril (@cyrilXBT), or other AI agent thought leaders
- Wants to implement 5-block loop pattern (automations, worktrees, skills, MCP, sub-agents) in his own systems
- Asks "what's new in AI agent development" or "latest coding agent trends"
- Asks "làm sao để em tự bắt lỗi trước khi gửi anh?" (self-correcting loop design)

## Core Frameworks Covered

### 0. Builder-Judge-Manager Self-Correcting Loop (cyrilxbt, July 2026)

**Origin:** Tweet `2077827005777588266` (2026-07-19) — *"How to Build a Self-Correcting AI Loop That Catches Its Own Mistakes Before You See."* Full X Article linked. Cyril @cyrilXBT, AI/Tech/Crypto educator (one-person-company stack — Obsidian + Claude Code + multi-agent loops). Anh shared the URL → 70% overlap with existing Hermes patterns.

**Definition:** A pipeline where the agent catches its own obvious mistakes before showing output to the user. Three separated roles with different prompts, ideally different frames of reference, so the Judge is not contaminated by the same blind spots that created the mistake.

**3 Roles:**

| Role | Job | CRITICAL rule |
|---|---|---|
| **Builder** | Produce draft from source + brief | Output MUST be structured (`draft` + `confidence` + `uncertainty_list`). NEVER just prose — Judge needs explicit fields to check. |
| **Judge** | Evaluate Builder's output against ground truth | MUST reference the **original source material / brief / test suite** — NOT just re-read the Builder's output. Judge with no ground truth can only check coherence, not correctness (confidently wrong answers will sail past). |
| **Manager** | Read Judge's verdict, route next action | Hard cap retries (typically 3) → escalate to human. On failure, send back SPECIFIC correction (e.g. "claim X unverified" not "double-check accuracy"). Per-check routing: fact-check fail → Builder with claim flagged; brief-compliance fail → Builder with missing requirement named; scope mismatch → human immediately. |

**3 Ground-Truth Sources (per task type):**
- **Coding tasks** → test suite execution, lint, build status. Not "does this code look right" — "did it actually pass when run."
- **Content tasks** → original source material + original brief, side by side with the draft. Not "does this read well" — "does every claim trace back to source, and does it satisfy every requirement in the brief."
- **Research tasks** → actual search results + source documents the research was based on. Not "does this sound authoritative" — "can every claim be traced to a specific source."

**The Confidently-Wrong Test:** Before shipping the loop, feed Judge an output you KNOW is subtly wrong (reads well, contains specific factual error). If Judge passes it → your ground truth reference is not actually being checked, OR the check is too shallow.

**Mapping to existing Hermes skills (70% overlap, 3 gaps to close):**

| Component | Cyril đề xuất | Hermes hiện tại | Gap |
|---|---|---|---|
| **Builder** | LLM with structured output + confidence + uncertainty list | LLM | ⚠️ Add `uncertainty_list` to all structured outputs |
| **Judge** | Separate LLM, source + brief side-by-side, structured verdict | `~/.hermes/scripts/adversarial_verify.py` + `adversarial-content-verifier` skill (12/07 ship) | ✅ Exists — verify Judge prompt actually references ground truth source |
| **Ground truth** | Source gốc + brief + test suite | `wiki-product-ground-truth` (research cache), `transcript-first-viral-workflow` (transcript as ground truth), `wiki/concepts/*.md` | ✅ Exists |
| **Manager** | Hard cap 3 retries → escalate human | Cron + manual ack/reject pattern | ⚠️ Missing confidence threshold |
| **Confidence threshold** | Judge confidence <0.6 → human queue | None explicit | ❌ MISSING |
| **Confidently-wrong test** | Self-test with known-bad input | Adversarial verifier has 3-layer check (STRUCTURAL/SEMANTIC/FUNCTIONAL) | ⚠️ Add "feed known-bad" to skill verification step |

**3 gaps to close (in priority order):**
1. **Builder uncertainty list** — when em produces structured output for any judge-able task, append `uncertainty_list: [claim_X, claim_Y]` (claims em không chắc 100%). Cost: ~10 tokens per output, downstream Judge knows where to look hard.
2. **Confidence threshold routing** — extend Manager rule: if `verdict.confidence < 0.6` → escalate human immediately (skip remaining retries). Hardcode in `~/.hermes/scripts/adversarial_verify.py` prompt template.
3. **Confidently-wrong test pattern** — whenever em patches a skill or updates a verification script, append a `KNOWN_BAD_CASE` fixture to `references/test-fixtures/` and require the script to FAIL on it. If script PASSES the known-bad case → verification logic is broken (similar to Cyril's confidently-wrong test).

**Anti-patterns (Cyril nhấn mạnh):**
- ❌ Judge chỉ re-read output mà không có source gốc → chỉ check coherence, không check correctness. Confidently wrong → sail past.
- ❌ Generic re-prompt on failure ("double-check accuracy") — Judge phải cite SPECIFIC unverified claim + Builder phải address THAT claim.
- ❌ Unbounded retry loop — ALWAYS hard cap (3 typical) + human escalation path.
- ❌ Collapsed single score (e.g. "verdict: 0.7") — phải per-check pass/fail so Manager biết route đi đâu (fact-check vs brief-compliance vs scope).
- ❌ Hedged prose verdict ("the output seems mostly correct but has some issues") — phải structured pass/fail/needs-revision.

**When to apply this framework:**
- Bất kỳ pipeline nào em đang build → ship → user review → fix → re-ship pattern. Especially: research synthesis, content generation, code generation with verification, batch processing with QA.
- Trigger phrase: "làm sao để em tự bắt lỗi trước khi gửi anh?" hoặc anh share Cyril's tweet / similar self-correcting-loop content.

---

### 1. Loop Engineering (Addy Osmani, June 2026)

**Definition:** Replacing the human-as-prompter with a system that recursively prompts the agent. A loop = a recursive goal where you define purpose and AI iterates until complete.

**5 Building Blocks + 1:**
| # | Block | Codex | Claude Code |
|---|-------|-------|-------------|
| 1 | Automations (heartbeat) | Automations tab | `/loop`, `/goal`, hooks, GitHub Actions |
| 2 | Worktrees (isolation) | Built-in worktrees | `git worktree`, `--worktree`, `isolation: worktree` |
| 3 | Skills (project knowledge) | `$skill` or `/skills` | `SKILL.md` folders |
| 4 | Plugins/Connectors (MCP) | MCP support | MCP support |
| 5 | Sub-agents (maker vs checker) | `.codex/agents/` TOML | `.claude/agents/` + teams |
| +1 | Memory (state file) | Markdown / Linear | External files |

**3 Pitfalls (KEEP these in mind):**
1. **Verification is still on you** — loop running unattended is loop making mistakes unattended
2. **Comprehension debt** — faster loop = bigger gap between what exists and you understand
3. **Cognitive surrender** — easy to stop having an opinion and just take whatever the loop gives back

### 2. Agent Harness Engineering (cousin of Loop Engineering)

**Definition:** The environment a single agent runs inside + the factory model = the system that builds the software. Loop engineering sits ONE FLOOR ABOVE the harness.

**Components:**
- Skills (project context, conventions)
- Tools/MCP (real-world action)
- Memory (state between runs)
- Sub-agents (specialization)

### 3. Multi-Agent Orchestration Patterns

**Key insight from 0xCodez (Claude Managed Agents):**
- Up to 20 agents in a roster
- Each agent has own model + prompt + scoped toolset
- Coordinator agent delegates to specialists in parallel
- `agent_toolset_20260401` enables delegation
- Common split: 1 explores, 1 implements, 1 verifies

## Research Methodology (When Anh Shares URL)

### Step 1: Fetch Content
```python
# Try in order
mcp_exa_web_fetch_exa(urls=[URL], maxCharacters=10000)
# If fails, fall back to:
mcp_exa_web_search_exa(query="<author> <topic> <date>", numResults=5)
```

### Step 2: Identify the Author's Original Sources
For AI agent articles, the original insight usually traces back to:
- Anthropic engineering docs
- OpenAI cookbook
- Boris Cherny (head of Claude Code)
- Peter Steinberger (coding agent practitioner)
- Addy Osmani (engineering leadership perspective)
- Cyril @cyrilXBT (one-person-company Obsidian + Claude Code stack)

**Always cite which source an article builds on** — most AI agent articles in 2026 are derivative summaries.

### Step 3: Classify the Article
| Type | Signal | Response |
|------|--------|----------|
| Original essay | Long-form, new framework, multiple examples | Deep analysis, extract framework |
| TL;DR / Roadmap | "X-step roadmap" + bullet points | Quick comparison with original |
| Tutorial / How-to | Step-by-step, code examples | Extract reusable patterns |
| Opinion / Take | Hot take on existing framework | Note the opinion, compare to other takes |

### Step 4: Distill Actionable Patterns
For each framework, extract:
- **What it is** (1-sentence definition)
- **When to use it** (trigger conditions)
- **How to apply it** (concrete steps)
- **Pitfalls** (what goes wrong)

## Application Workflow (For Anh's Systems)

When Anh wants to apply a framework to his Felix model / Hermes / worker system:

### Step 1: Gap Analysis
Compare the framework's components to Anh's current setup:
| Framework Component | Hermes Equivalent | Match? |
|---------------------|-------------------|--------|
| Automations | Heartbeat worker + cron jobs | ✅ 80% |
| Worktrees | Sub-agents in different contexts | ⚠️ Need explicit isolation |
| Skills | Skills (gskill files) | ✅ 100% |
| Plugins/MCP | MCP servers (browser, exa, v.v.) | ✅ 100% |
| Sub-agents | Single agent per task | ❌ **Missing maker vs checker split** |
| Memory | Wiki + memory system | ✅ 100% |
| Self-correcting loop (Cyril BJM) | Adversarial verifier + evidence gate + wiki ground truth | ✅ 70% — see Framework 0 above for the 3 gaps |

### Step 2: Recommend Top 3 Actions
Always recommend in priority order with concrete first-step:

1. **Sub-agent checker pattern** (biggest gap)
   - Worker (maker) → Worker (checker) → Hermes review → Anh approve
   - Use case: research, script writing, code generation
   - First step: Add a verification step in current workflow

2. **Implement `/goal` primitive** (loop until verified)
   - Worker agent runs loop until PASS verified condition
   - Use case: content posting, data gathering, batch processing
   - First step: Define a verifiable condition for one workflow

3. **Builder uncertainty list + confidence threshold routing** (Cyril BJM gap fill)
   - Append `uncertainty_list` to all structured Builder outputs (claim-by-claim)
   - If Judge verdict confidence < 0.6 → escalate human immediately
   - First step: patch `~/.hermes/scripts/adversarial_verify.py` to add `< 0.6` threshold + wire `uncertainty_list` field through

### Step 3: Anti-Patterns to Avoid

❌ **Looping without verification** — agent says "done" but isn't
❌ **Skipping human review** — even with checker, you still need to ship code you understand
❌ **Too many automations at once** — start with 1, scale later
❌ **Ignoring token cost** — loop's token burn can dwarf prompt-engineering cost
❌ **Cognitive surrender** — taking loop output without thinking
❌ **Judge without ground truth** — see Framework 0 — silently turns correctness check into coherence check

## Response Style for AI Agent Analysis

When Anh shares an article URL:

### Format
1. **Quick classification** (1 line): "This is a TL;DR of Addy Osmani's essay"
2. **Summary** (2-3 sentences): Core thesis
3. **Framework extraction**: Tables, comparison to other frameworks
4. **Application to Anh's systems**: 3 specific recommendations
5. **Source attribution**: Where the original insight came from

### Tone
- Vietnamese casual ("anh" + "em" for non-TikTok context)
- Direct, no fluff
- 3 actionable next steps, not "let me know what you want"

### Avoid
- Re-explaining the article in full
- Listing options without committing
- Asking "có muốn em đi sâu vào cái nào?"
- Inventing facts not in the source

## Sources to Track

| Source | Frequency | Best For |
|--------|-----------|----------|
| Addy Osmani Substack | ~2x/month | Engineering management + AI agents |
| Boris Cherny (Claude Code head) | ~1x/month | Claude Code roadmap, primitives |
| Peter Steinberger | ~1x/month | Practitioner insights |
| 0xCodez | ~5x/week | TL;DR summaries, X-specific trends |
| Anthropic Engineering Blog | ~2x/month | Official Claude Code updates |
| OpenAI Cookbook | ~3x/month | Codex patterns, multi-agent |
| Cyril @cyrilXBT | ~5x/week | Self-correcting loops + one-person-company stack |

## Related
- [[xurl]] — X/Twitter research tool
- [[hermes-autoresearch]] — Nightly research loop (already implements automations pattern)
- [[adversarial-content-verifier]] — Hermes Judge implementation (12/07)
- [[wiki-product-ground-truth]] — Hermes ground-truth source for product content
- [[evidence-first-delivery]] — 5-Evidence Gate (anti-fabrication)
- [[evidence-gate]] — Per-task completion claim gate
- [[qa-gate]] — Per-step verification
- `references/loop-engineering-summary.md` — Full summary of Addy Osmani's essay (created 2026-06-01)
- `references/ai-agent-articles-log.md` — Log of articles researched this skill
- `references/cyrilxbt-bjm-summary.md` — Full Builder-Judge-Manager framework summary (created 2026-07-19, source tweet 2077827005777588266)