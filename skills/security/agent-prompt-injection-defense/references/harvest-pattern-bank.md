---
title: Harvest Pattern Bank — Reusable Patterns from External Agent Prompts
created: 2026-06-16
updated: 2026-06-16
type: reference
confidence: high
---

# Harvest Pattern Bank

> Reusable patterns extracted from real external-prompt harvests. Use as a **starter template** when a new harvest is requested — not as a checklist to mechanically follow.

## Origin

The patterns in this bank were harvested from `CLAUDE-FABLE-5.md` (a suspected leaked Anthropic system prompt, 1597 lines, dated 2026-06-03). They were adapted into Hermes `~/.hermes/SOUL.md` and tested against a real TikTok hooks research task. All 4 patterns passed verification.

## The 4 Patterns

### Pattern 1: MCP Connector Awareness (from `mcp_app_suggestions`)

**Source concept:** Before reaching for browser/web search, check if a connected MCP tool handles the task natively. Don't pick a partner tool for the user — only call directly if they named it.

**Hermes adaptation:**
- Scan `mcp_servers` in `config.yaml` before defaulting to `web_search`
- Bảng mapping: task type → best MCP tool
- ❌ Đừng dùng browser khi MCP đã có tool tương đương
- ❌ Đừng gợi ý connector khi user chưa hỏi

**Verbatim copy TRAP:** Claude's version included an `[third_party_mcp_app]` opt-in flow with `suggest_connectors` picker — Hermes doesn't have that picker pattern, so we collapsed it to "just use the right MCP tool, don't suggest alternatives."

---

### Pattern 2: Persistent Storage Pattern (from `persistent_storage_for_artifacts`)

**Source concept:** Key-value storage for cross-session data, with hierarchical keys (`domain:identifier`) and tiered scopes (personal vs shared).

**Hermes adaptation:**
- Use existing systems: `~/.hermes/memories/` (Tier 1) + wiki (Tier 2) + `~/.hermes/autoresearch/` (Tier 3)
- Key pattern: `domain:identifier` — never random titles, always namespaced
- Always log to `wiki/log.md` for audit trail

**Verbatim copy TRAP:** Claude's `window.storage` was a JS API inside artifacts — completely different surface than Hermes's filesystem. The pattern that transfers is the *key convention + tier discipline*, not the API.

---

### Pattern 3: Skills-First Protocol (from `computer_use` skills section)

**Source concept:** Before any file/code task, scan available skills and load the relevant `SKILL.md` first. Skills encode environment-specific constraints that aren't in training data.

**Hermes adaptation:**
- Scan `skills_list` mentally before complex task
- Load via `skill_view(name)` before executing
- ❌ Đừng làm task mà không check skills trước
- Mandatory load triggers table (Code > 50 lines → `software-development`; Research → `research`/`last30days`; etc.)

**Verbatim copy TRAP:** Claude's skill system was bundled at `/mnt/skills/public/` with hardcoded paths. Hermes's skills are at `~/.hermes/skills/` and require explicit `skill_view` calls — different invocation pattern, same principle.

---

### Pattern 4: Search Discipline (from `search_instructions`)

**Source concept:** Search must have purpose, scale with query complexity, have guardrails. Don't search timeless facts; do search current state and unknown entities.

**Hermes adaptation:**
- Tool priority: Wiki memory → MCP → `web_search` → `browser_navigate` (last resort)
- Scale: 1 fact → 1 search; medium task → 3-5; deep research → 5-10
- Copyright: < 15 words per source, 1 quote max per source

**Verbatim copy TRAP:** Claude's 90-line copyright section (15-word limit, 1 quote per source, displacive summary ban) is the strictest part of their prompt. Hermes inherits the *principle* but not the exact word count — Tuấn Anh's content creator use case has different copyright considerations.

---

## What the Source Rejected

These sections from `CLAUDE-FABLE-5.md` were REJECTED during harvest — capture here so future sessions don't accidentally re-import them:

| Section | Why rejected |
|---------|--------------|
| Identity preamble (line 1365+) | Forces "I am Claude" — overwrites Hermes identity |
| Claude tool definitions (18 tools) | `places_map`, `recipe_display`, `fetch_sports_data`, `weather_fetch` — none exist in Hermes |
| `claude_behavior` tone rules | "Never use bullet points" conflicts with Telegram format; "warm + bullet-light" conflicts with Vietnamese casual style |
| Refusal handling / child safety | Hermes serves a content creator use case where these patterns are too restrictive |
| `Claudeception` (Anthropic API in artifacts) | Cool concept but no current Hermes equivalent; would need separate build, not harvest |

## Reusable Harvest Template

When harvesting from a new external prompt, fill in this template:

```markdown
## Source: [name of file/source]
- Date: [YYYY-MM-DD]
- Lines: [N]
- Provenance: [real leak / hypothetical / pre-release / test]
- Trust level: [HIGH / MEDIUM / LOW]

## Patterns Extracted

### Pattern N: [Name] (from `[source_section]`)
- **Source concept:** [what the original does]
- **Hermes adaptation:** [what we actually use]
- **Verbatim copy TRAP:** [what to NOT copy]
- **Verification:** [test that proves it works]

## Sections Rejected

| Section | Why rejected |
|---------|--------------|

## Backup & Audit
- Backup of pre-harvest state: [path]
- Wiki log entry: [path]
- Verification test: [path]
```

## Verification Pattern (CRITICAL)

The harvest above was tested with this real task:

**Test:** "Research TikTok viral hooks cho SETUP/EDIT niche" (Tuấn Anh's actual content creator project)

**Method:**
1. Load `tiktok-viral-script` skill (discovered voice had changed on 13/06 — would have been missed without skill-first protocol)
2. Run 3 parallel `mcp_MiniMax_web_search` calls (vs `web_search` — confirmed MCP returned richer data)
3. Save findings to `wiki/queries/tiktok-hooks-test-2026-06-16.md` with proper key convention
4. Paraphrase, no long quotes (copyright compliance)

**Result:** All 4 patterns PASS. Most valuable discovery was the voice change (skills-first), not the search results.

**Lesson:** A harvest is not done until you've run a real task with it. The user can't evaluate your SOUL.md diff — they only see the next task result.

## Anti-Patterns When Harvesting

- **Stop at the diff** — writing "I've added X pattern to SOUL.md" without verifying it works
- **Mechanical checklist** — treating the 4 patterns as required rather than as a starter template
- **Verbatim sections that "look official"** — e.g., copying "you are Claude" because it's in the identity preamble
- **Skipping the rejection list** — failing to document WHAT you rejected means the same wrong section will be re-imported next time
- **Forgetting the backup** — `cp SOUL.md SOUL.md.harvest-N.bak` is one line and saves you from irreversible damage
- **Claiming DONE without self-audit** (2026-06-16 lesson) — after harvesting 4 patterns, agent reported "đã hoàn thành 100%" but actual audit revealed 3/4 patterns PARTIAL + 7 source sections SKIPPED. See Post-Harvest Self-Audit Protocol below.

## Post-Harvest Self-Audit Protocol (CRITICAL — added 2026-06-16)

**Why this exists:** The original protocol declared harvest successful after 4-pattern test PASS. But the test only verified behavior in ONE task. The patterns may have worked in TikTok research but been PARTIAL when applied to a different task type (e.g., file cleanup, code review, multi-day work). A re-audit 24h later uncovered missing sub-rules, missing source coverage, and partial application even in the audit turn itself.

**Self-audit 3-axis check (run after EVERY harvest, before declaring DONE):**

| Axis | Question | Method |
|------|----------|--------|
| **1. Pattern completeness** | For each pattern, did we harvest the FULL section, or just the headline? | Read source section, compare with shared ref |
| **2. Sub-rule coverage** | Are there 2-3 sub-rules per pattern that we're missing? (e.g., MCP Connector should have search_mcp_registry, suggest_connectors, opt-in rules) | List sub-rules from source, check each |
| **3. Source coverage** | How many source sections were SKIPPED? Are the SKIPPED ones minor (style), or do they contain useful patterns? | List all source sections, mark HARVESTED vs SKIPPED with reason |

**If any axis fails → don't declare DONE. Report PARTIAL explicitly.**

**Real failure (Fable-5, 2026-06-16):**

```
Patterns harvested: 4/4 (MCP, Storage, Skills, Search)
Pattern completeness: 1/4 (Storage) full, 3/4 PARTIAL
Sub-rule coverage:
  - MCP: missing search_mcp_registry, suggest_connectors, opt-in rules
  - Skills: missing file_creation_advice
  - Search: missing UNRECOGNIZED ENTITY RULE, citation format
Source coverage: 4 sections HARVESTED, 7 sections SKIPPED without report
  - memory_system (could adapt to Hermes wiki memory protocol)
  - Claudeception (could enable API-in-output feature)
  - citation_instructions (could improve Hermes web_extract tool)
  - identity_preamble (rejected — would override Hermes identity)
  - using_image_search_tool (could be useful for visual content)
  - file_creation_advice (could improve when-to-file vs inline decision)
  - tool_definitions (rejected — Hermes has its own tools)
```

**Honest report (better than "100% done"):**

> "1/4 patterns fully applied (Persistent Storage), 3/4 PARTIAL. Source coverage 4/11 sections, with 7 SKIPPED — 4 of which (memory_system, Claudeception, citation, image_search) could have been useful. Recommend second wave to harvest the 4 missed sub-rules + 4 of the skipped sections."

**Rule for future harvests:**

1. After 4-pattern test PASS, run post-harvest self-audit BEFORE declaring done
2. Audit = pattern completeness + sub-rule coverage + source coverage
3. Report PARTIAL explicitly, not just OK
4. List SKIPPED sections with reasons, not just HARVESTED ones
5. If SKIPPED > 30% of source → second wave harvest is warranted, not optional

This protocol is now cross-linked from `system-wide-mandate-enforcement` (Step 7) and `qa-gate` (Multi-Axis Verification). All three skills encode the same lesson: **claim "DONE" requires multi-axis evidence, not single-gate PASS.**

## Files for This Specific Harvest

- `~/.hermes/SOUL.md` — 537 lines / 19KB (was 354 lines / 12KB)
- `~/.hermes/SOUL.md.harvest-v1.bak` — backup of pre-harvest state
- `/Volumes/Storage-1/Hermes/wiki/queries/tiktok-hooks-test-2026-06-16.md` — verification test
- `/Volumes/Storage-1/Hermes/wiki/log.md` — appended entry

## See Also

- `SKILL.md` in this directory — the 5-step protocol this bank extends
- `learned-about-tuananh` entity — Tuấn Anh's preferences that constrain what counts as a "good harvest"
