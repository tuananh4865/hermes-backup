---
name: loop-goal
description: "Universal loop runner — chạy task lặp lại tới khi đạt verified condition. Pattern từ Addy Osmani /goal primitive. Đứng thứ 2 trong 5 building blocks của Loop Engineering."
version: 1.0.0
author: Hermes Agent (Loop Engineering system)
license: MIT
platforms: [macos, linux]
prerequisites:
  commands: [python3, bash]
metadata:
  hermes:
    tags: [loop, goal, automation, loop-engineering, system-wide, agent]
    parent_skill: loop-engineering
    related: [quality-checker, hermes-agent]
---

# /goal Primitive — Universal Loop Runner

> **Trong pattern Loop Engineering: Maker (profile/subagent) → Checker (quality-checker skill) → Orchestrator (em) → User (anh)**
> Skill này = "Loop" — chạy task lặp lại tới khi đạt verified condition (separate model checks).

---

## Khi nào dùng

**Dùng khi:**
- ✅ Task có verifiable stopping condition (VD: "tất cả scripts có >80% engagement")
- ✅ Task lặp lại cùng pattern (research, content generation, code refactor)
- ✅ Cần iterate cho tới khi pass quality gate
- ✅ Anh muốn "đặt goal rồi đi ngủ, sáng mai có kết quả"

**KHÔNG dùng khi:**
- ❌ Simple one-shot task
- ❌ Task không có measurable success criteria
- ❌ Task cần human judgment (không thể verify tự động)

---

## API

```bash
/goal "<mô tả goal>" \
  --condition "<verifiable stopping condition>" \
  --max-runs N \
  --profile <profile_name> \
  --on-pass <action> \
  --on-fail <action>
```

**Parameters:**
- `goal` (required): Mô tả mục tiêu
- `--condition` (required): Verifiable stopping condition (machine-checkable)
- `--max-runs` (default 5): Số lần chạy tối đa trước khi abort
- `--profile` (default "default"): Profile/subagent thực thi (Hermes profile name: `content-director`, `research-lead`, `coder`, hoặc `default`)
- `--on-pass` (default "deliver"): Hành động khi PASS (deliver/archive/notify)
- `--on-fail` (default "archive"): Hành động khi hết max_runs (archive/retry/escalate)

---

## Examples

### 1. Content Creator — script viral

```bash
/goal "Viết 5 script TikTok viral cho phụ kiện quay dựng" \
  --condition "Mỗi script PASS quality-checker (≥9.0 score, no critical issues)" \
  --max-runs 5 \
  --profile content-director \
  --on-pass deliver_to_telegram
```

### 2. Research — trending products

```bash
/goal "Tìm top 5 sản phẩm trending TikTok Shop" \
  --condition "Mỗi sản phẩm có ≥5 nguồn, giá hiện tại, KOL review" \
  --max-runs 3 \
  --profile research \
  --on-pass deliver_to_hub
```

### 3. Code — refactor

```bash
/goal "Refactor auth module" \
  --condition "All tests pass + lint clean + no secrets detected" \
  --max-runs 5 \
  --profile code \
  --on-pass commit_and_notify
```

---

## How it works

```
[GOAL DEFINED] → [RUN 1: maker → output] → [CHECK: condition met?]
   ↓                                              ↓ NO
   ↓                                          [FEEDBACK: issues]
   ↓                                              ↓
   ↓                                          [RUN 2: maker re-run with feedback]
   ↓                                              ↓
   ↓                                              ...
   ↓                                          [CHECK after run N]
   ↓                                              ↓ YES → DELIVER
   ↓                                              ↓ NO (max_runs exceeded) → ARCHIVE + NOTIFY
```

**Each iteration:**
1. **Maker** = profile/subagent tạo output (resolve qua `HERMES_PROFILE` hoặc `--profile` arg)
2. **Checker** = quality-checker verify (loop engineering pipeline)
3. **Condition check** = check if output meets goal
4. If PASS → on-pass action
5. If FAIL → re-run maker with feedback (issues + suggestions)

---

## Condition Syntax

Conditions phải machine-verifiable. Hỗ trợ:

### Simple boolean
```bash
--condition "output_score >= 9.0"
--condition "no_critical_issues == true"
--condition "all_tests_pass == true"
```

### Complex (using quality-checker verdict)
```bash
--condition "checker_verdict == PASS"
--condition "checker_score >= 9.0 AND no_critical_issues"
```

### Aggregate (across multiple runs)
```bash
--condition "5_consecutive_passes"
--condition "3_passes_in_last_5_runs"
```

### Custom (Python expression)
```bash
--condition "output.engagement > 0.8 and output.duration < 30"
```

---

### Profile-Aware Behavior

Skill này là **global** — dùng được cho mọi Hermes profile (content-director, research-lead, coder, hoặc default).

State file path resolve tự động:
```python
profile = os.environ.get("HERMES_PROFILE", "default")
state_file = f"~/.hermes/profiles/{profile}/state.md"
```

---

# State tracking

Mỗi loop iteration log vào `~/.hermes/profiles/{profile}/state.md` (HERMES_HOME-aware):

```markdown
## Run #3 (2026-06-16 19:45)
- Goal: "Viết script viral"
- Maker: content-director v2
- Checker verdict: FAIL (score 7.5)
- Issues: ["voice dùng 'mấy con vợ' 2 lần", "thiếu 1 nguồn"]
- Next: Re-run with feedback
```

Loop state = append-only. Anh check back bất cứ lúc nào.

---

## Configuration

File: `~/.hermes/loop-engineering/loop-config.yaml`

```yaml
loop_goal:
  enabled: true
  default_max_runs: 5
  default_on_pass: deliver
  default_on_fail: archive
  
  # Token budget protection
  max_tokens_per_loop: 100000
  alert_on_budget_warning: 0.8  # 80% of budget
  
  # Auto-cleanup
  archive_after_days: 30
  keep_run_logs: 100
  
  # Default conditions per project
  project_defaults:
    content-director:
      condition: "checker_verdict == PASS"
    research:
      condition: "all_items_have_sources >= 5"
    code:
      condition: "tests_pass and lint_clean"
```

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | File này |
| `run.sh` | Main loop runner script |
| `condition-parser.py` | Parse và evaluate conditions |
| `test.sh` | Test suite |

---

## Related

- [[Loop-Engineering-System]] — Parent system
- [[quality-checker]] — Used by loop-goal for verification
- [[hermes-agent-complete-guide]]
- Bài Addy Osmani "Loop Engineering" (Substack 8/6/2026)

---

*Last updated: 2026-06-16*
*Part of: Loop Engineering system-wide deployment*
