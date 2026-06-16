---
title: Profile State Template
type: template
scope: hermes-profile
applies_to: every Hermes profile
---

# Profile State — Universal Template

> Template này tự động apply cho mọi Hermes profile. **KHÔNG edit thẳng vào file này** — đây là template. Mỗi profile có file `state.md` riêng, copy từ template này.

## Cách sử dụng

Mỗi profile có 1 state file tại: `~/.hermes/profiles/default (orchestrator)/state.md`

**Profile names hiện có:**
- `content-director` — TikTok content
- `research-lead` — Research
- `coder` — Code
- `default` — Main/orchestrator

**State file auto-update bởi:**
- `quality-checker` skill (sau mỗi check)
- `loop-goal` primitive (sau mỗi run)
- `loop-engineering-hook` (gateway level)

---

## Template

```markdown
---
profile: default (orchestrator)
goal: <current goal, nếu có>
updated: <ISO date>
loop_engineering: enabled
---

# Profile State — default (orchestrator)

## Current Goal
[What /goal is trying to achieve right now. Nếu không có goal → "None"]

## Recent Verdicts (từ quality-checker)
| # | Time | Verdict | Score | Issues | Worker | Goal |
|---|------|---------|-------|--------|--------|------|
| 1 | 2026-06-16 19:30 | PASS | 9.3 | [] | content-director | "Viết script viral" |
| 2 | 2026-06-16 19:25 | FAIL | 7.5 | ["voice", "sources"] | content-director | "Viết script viral" |

## Run History (từ loop-goal)
| # | Time | Goal | Worker | Runs | Result | Notes |
|---|------|------|--------|------|--------|-------|
| 1 | 2026-06-16 19:30 | "Viết script viral" | content-director | 3 | PASS | Score 9.3 sau 3 runs |
| 2 | 2026-06-16 18:00 | "Research trending" | research-lead | 1 | PASS | First try |

## What Worked (patterns to reuse)
- ✅ Hook pattern "Mấy con vợ ơi..." → engagement +25% (note: chỉ dùng ngoài script TikTok, KHÔNG dùng trong Hermes communication)
- ✅ Research depth 5 sources → quality score 9+
- ✅ Code refactor với tests trước → regression rate <1%

## What Failed (patterns to avoid)
- ❌ Script <60s → bounce rate 70%
- ❌ Research chỉ 2 sources → quality score <7
- ❌ Code changes không có tests → bug rate 40%

## Open Items
- [ ] Item 1
- [ ] Item 2

## Profile-specific Config
- Voice: "anh" + "em" (default) hoặc theo SOUL.md
- Max runs default: 5
- Skip conditions: [list]
```

---

## Hooking vào Hermes

State file tự động update bởi:

```python
import os
profile = os.environ.get("HERMES_PROFILE", "default")
state_file = f"~/.hermes/profiles/{profile}/state.md"
```

**Tự động trigger khi:**
- `quality-checker` chạy xong → append verdict row
- `loop-goal` finish (PASS hoặc max_runs) → append run history row
- Cron job chạy → append check-in row

**KHÔNG tự động trigger cho:**
- Simple Q&A
- Navigation commands
- Status checks

---

## Liên quan

- [[Loop-Engineering-System]] — Parent system
- [[quality-checker]] — Generates verdict rows
- [[loop-goal]] — Generates run history rows
- Hermes docs: https://hermes-agent.nousresearch.com/docs/user-guide/profiles

---

*Last updated: 2026-06-16*
*Part of: Loop Engineering system-wide deployment*
