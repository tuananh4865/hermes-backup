# Fable-5 vs Loop Engine — Decision Framework (v2.3)

> When to use Fable-5 (foundation) vs Loop Engine (weapon). Single source of truth for the mental model clarification from Tuấn Anh 17/06 11:15.

## User's Mental Model (verbatim)

> *"fable cho toàn bộ và loop cho các công việc dev, hoặc em tự động nhận biết khi nào nên dùng cái nào, đại khái thì anh muốn fable 5 là cái cốt lõi và là nền tảng của hệ thống và loop là vũ khí!"*

Translation:
- **Fable-5** = cốt lõi / nền tảng của toàn bộ hệ thống → ALWAYS ON
- **Loop** = vũ khí cho công việc dev → USE WHEN NEEDED
- **Em tự động nhận biết** khi nào dùng cái nào

## Quick Decision Table

| Task type | Fable-5? | Loop? | Why |
|-----------|----------|-------|-----|
| 1-shot task (research 1 topic, fix 1 bug) | ✅ Always | ❌ | Loop overhead = waste |
| Quick research < 30 min | ✅ Always | ❌ | Too short for loop verification |
| Setup đơn lẻ (1 cron job) | ✅ Always | ❌ | Not multi-phase |
| Conversation / Q&A | ✅ Always | ❌ | Not action-oriented |
| **Project > 2 tuần** | ✅ Always | ✅ | Multi-phase + multi-agent |
| **Multi-agent coordination** | ✅ Always | ✅ | Verify-gate + retry needed |
| **Build tool/feature mới (dev work)** | ✅ Always | ✅ | Needs structured loop |
| Multiple tasks across days | ✅ Always | ✅ | Tracking + logging needed |

## Architecture (v2.3)

```
┌─────────────────────────────────────────┐
│  🏛️ FABLE-5 (FOUNDATION)                │
│  Always on — mọi task                   │
│  4 patterns: MCP, Storage, Skills,      │
│  Search Discipline                      │
└──────────────┬──────────────────────────┘
               │ principles (WHAT)
               ▼
┌─────────────────────────────────────────┐
│  ⚔️ LOOP ENGINE v2.3 (WEAPON)           │
│  Chỉ dùng cho dev/project work          │
│  Step 0 RESEARCH → PLAN → RESEARCH →    │
│  EXECUTE → VERIFY → NEXT (max 3 retry)  │
└─────────────────────────────────────────┘
```

## Per-step Fable-5 Mapping (khi Loop chạy)

| Loop Step | Fable-5 patterns | What it means |
|-----------|------------------|---------------|
| Step 0 RESEARCH | P1 + P3 + P4 | MCP web search + load skill first + multi-source citation |
| Step 1 PLAN | P2 + P3 | Save plan to wiki + load workflow skill |
| Step 1.5 RESEARCH | P1 + P4 | MCP re-verify + search discipline |
| Step 2 EXECUTE | P1 + P2 + P3 + P4 | All patterns — this is where most work happens |
| Step 3 VERIFY | P2 + P4 | YAML/wikilinks check + citation format |
| Step 4 NEXT | (orchestration only) | No Fable-5 patterns directly |

## Why This Distinction Matters (Lessons Learned)

### Before v2.3 (mistakes):
- Treated Fable-5 + Loop as 2 peer concepts → user confused about which to load when
- Default guidance was "apply Loop to all tasks" → wrong fit for 1-shot task
- 6-step loop overkill for simple research

### After v2.3 (clarification):
- **Fable-5 = layer 1** (always on, no decision needed)
- **Loop = layer 2** (opt-in, only when trigger conditions met)
- **Single rule:** Load Fable-5 first. Decide Loop based on task type.

## Auto-Detection Logic (for em)

When user says X, decide:
- Is it a 1-shot task or quick research? → Fable-5 only
- Is it a project setup or feature build? → Loop + Fable-5
- Is it a question or conversation? → Fable-5 only
- Is it multi-step coordination across days? → Loop + Fable-5

When in doubt:
- **Default to Fable-5 only** (don't over-engineer with Loop)
- If task spans > 1 day OR has 3+ steps → consider Loop

## Trigger Phrases for Loop (vs Fable-5)

User explicitly says Loop when:
- "Quản lý dự án nhiều tháng" → Loop
- "Tạo project mới với phases" → Loop
- "Track phases và tasks" → Loop
- "Loop verify trước khi next" → Loop
- "Tự động thực thi plan trong loop" → Loop
- "Chia việc cho từng role theo loop" → Loop
- "Multi-phase project workflow" → Loop
- "Research trước khi plan/execute" → Loop (Step 0 + 1.5)
- "Dùng loop cho dev work" → Loop

User wants Fable-5 only when:
- "Setup [X] cho em" (simple setup) → Fable-5 only
- "Research nhanh về [topic]" → Fable-5 only
- "Check [X] có [Y] không" → Fable-5 only
- Any casual question/conversation → Fable-5 only

## Cross-References

- `~/.hermes/profiles/_shared/fable5-patterns.md` — Fable-5 spec
- `~/.hermes/profiles/_shared/project-loop-engine.md` — Loop spec (v2.3)
- `~/.hermes/profiles/_shared/fable5-patterns.md` → "Relationship với Loop Engine" section
- `project-workflow-v2` SKILL.md → v2.3 Changes section (memory + decision framework)
- `system-wide-mandate-enforcement` SKILL.md → "Mental Model: Fable-5 = Foundation, Loop = Weapon" section

## When This Was Established

- **Date:** 2026-06-17 11:15 ICT
- **Source:** Tuấn Anh explicit feedback in session
- **Evolution:** v2.0 (4-step loop, no Fable-5 binding) → v2.1 (research-first) → v2.2 (retry policy) → v2.3 (mental model clarification)
- **Lesson:** Each v2.x was triggered by user catching a gap in previous version. Anticipate gaps better.