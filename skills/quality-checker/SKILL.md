---
name: quality-checker
description: "Universal quality gate — verify mọi output từ maker agent trước khi deliver cho user. Apply cho system-wide Hermes workflow (Loop Engineering pattern). Check: format, voice, sources, quality bar, project-specific rules."
version: 1.0.0
author: Hermes Agent (Loop Engineering system)
license: MIT
platforms: [macos, linux]
prerequisites:
  commands: []
metadata:
  hermes:
    tags: [quality, checker, loop-engineering, system-wide, agent]
    parent_skill: loop-engineering
    related: [content-creator, autoloop, hermes-agent]
---

# Quality Checker — Universal Quality Gate

> **Trong pattern Loop Engineering: Maker (subagent/profile) → Checker (skill này) → Orchestrator (em) → User (anh)**
> Skill này = "Checker" — verify output từ Maker (sub-agent) trước khi em (Orchestrator) review và deliver cho anh (User).

---

## Khi nào invoke

**Auto-trigger** (qua `loop-engineering-hook`):
- ✅ Mọi task có output > 1 deliverable
- ✅ Mọi content generation (script, post, report, research)
- ✅ Mọi code change (commit-worthy)
- ✅ Mọi research output (có sources)
- ❌ KHÔNG trigger cho: simple Q&A, conversation, system check, navigation

**Manual invoke:**
```
@quality-checker verify {output}
@quality-checker check {file_path}
```

---

## 6 Universal Check Categories

### 1. FORMAT
- Output structure đúng spec?
- Markdown/JSON/YAML valid?
- Có headers, sections, code blocks khi cần?
- File naming convention đúng?

### 2. VOICE
- Hermes (general): "anh" + "em" (16/06 update)
- Content Creator scripts: "các bạn" (trung tính)
- **CẤM**: "mấy con vợ", "mấy đứa", "mấy chị", "mấy má", "anh ơi" lặp lại
- Tone đúng project (chuyên nghiệp / casual / technical)?

### 3. SOURCES (cho research)
- Mỗi data point có URL + ngày truy cập?
- ≥5 nguồn cho research tasks (theo quy tắc Content Creator)
- ≥2 nguồn cho factual claims
- Nguồn đa dạng (không phải chỉ 1 site)?

### 4. QUALITY BAR
- **NO** chung chung ("có thể", "thường thì", "nhiều khi")
- **NO** tự đoán (claim không có data)
- **NO** bịa số liệu
- **NO** template lặp lại (mỗi output phải unique)
- Có evidence/examples cụ thể cho mọi claim?

### 5. PROJECT-SPECIFIC RULES
Nếu output thuộc project cụ thể (Content Creator, etc.), apply rules riêng:
- **Content Creator**: 7 quy tắc Hiến pháp kênh (test thật, có nhược điểm, gắn nhãn affiliate...)
- **Research**: ≥5 nguồn, format chuẩn markdown
- **Code**: pass lint, có test, không có secrets

### 6. ACTIONABILITY
- Output có next steps rõ ràng?
- User biết phải làm gì sau khi đọc?
- Có links/files cần thiết?

---

## Output Format (Verdict)

```yaml
verdict: PASS | FAIL | WARN
score: 0-10  # 10 = perfect, 0 = unusable
task_type: content | research | code | report | script
profile: {profile_name}  # Hermes profile name (content-director, research-lead, coder, or default)

# Categories score (each 0-10)
format_score: 9
voice_score: 10
sources_score: 7
quality_score: 8
project_specific_score: 9
actionability_score: 8

# Issues (empty if PASS)
issues:
  - category: sources
    severity: critical | warning | minor
    description: "Data point #3 không có URL nguồn"
    location: "section 'Top 5 sản phẩm', row #3"
    suggestion: "Thêm link TikTok Shop product page + ngày truy cập"

# Suggestions (always, even if PASS)
suggestions:
  - "Bổ sung thêm 1 nguồn từ Group Facebook review"
  - "Sửa voice: thay 'mấy con vợ' → 'các bạn' (3 chỗ)"

# Overall reasoning
reasoning: |
  Output đạt chất lượng tốt về format và voice.
  Cần bổ sung sources cho 2 data points.
  Verdict: FAIL — cần re-run maker với feedback trên.
```

---

## Verdict Thresholds

**Score-based (default):**

| Score | Verdict | Action |
|-------|---------|--------|
| 9-10 | PASS | Deliver to user |
| 7-8 | WARN | Deliver + note issues for next time |
| 5-6 | FAIL | Re-run maker với feedback |
| 0-4 | FAIL (critical) | Reject, escalate to user |

**⚠️ CRITICAL-OVERRIDE RULE (mandatory):**

**A single `critical` severity issue → verdict = FAIL, regardless of score.**

```python
# In run_checker (test.py):
has_critical = any(i.get("severity") == "critical" for i in all_issues)
if has_critical:
    verdict = "FAIL"  # override score-based verdict
elif final_score >= 9.0:
    verdict = "PASS"
# ...
```

**Why this rule exists (lesson from 2026-06-16):**
Test case "BAD voice" scored 8.8 (would be WARN), but contained a critical issue (banned word "mấy con vợ" 3x in content-creator project). Pure score-based verdict wrongly passed it as WARN. The override made it FAIL → re-run → correct outcome.

**Rule of thumb:** Score measures quality. Severity measures safety. A passing score with a critical safety issue is still a fail. Critical issues are: banned words, missing required sections, fabricated data, security violations, broken contracts.

---

## Workflow

```\n1. Nhận output từ Maker (profile hoặc subagent)
2. Detect task_type
3. Load project-specific rules (nếu có)
4. Check 6 categories
5. Score + generate verdict
6. Log to profile state file (HERMES_HOME-aware)
7. Return verdict to Orchestrator (em)
```

**Nếu FAIL**: Orchestrator re-runs Maker với feedback cụ thể (issues + suggestions)
**Nếu PASS**: Orchestrator reviews + delivers to User
**Nếu WARN**: Orchestrator delivers + logs for learning

---

## Configuration

File: `~/.hermes/loop-engineering/checker-config.yaml`

```yaml
quality_checker:
  enabled: true
  auto_trigger: true
  
  # Thresholds
  pass_threshold: 9
  warn_threshold: 7
  fail_threshold: 5
  
  # Auto-trigger conditions
  trigger_on:
    - file_outputs_count: ">=1"
    - content_keywords: ["report", "script", "research", "analysis"]
    - project_match: ["content-creator", "autoloop", "any"]
  
  # Skip conditions
  skip_on:
    - task_type: ["qa", "navigation", "system_check"]
    - output_size: "<100_chars"
  
  # Project-specific rules
  project_rules:
    content-creator:
      voice: "các bạn"  # not "mấy con vợ"
      min_sources: 5
      must_have:
        - affiliate_label
        - real_test_proof
        - cons_list
      forbidden:
        - "quất một phát"
        - "đỉnh nóc kịch trần"
```

---

## Integration với Loop Engineering

**Maker → Checker flow:**
```
[MAKER] output draft
   ↓
[CHECKER] ← THIS SKILL
   ↓ verdict: PASS/FAIL/WARN
[ORCHESTRATOR] = em review
   ↓ if FAIL: re-run Maker với feedback
[USER] = anh approve
```

**Auto-invoke** qua `loop-engineering-hook`:
```python
@hook("agent:end")
def auto_invoke_checker(task_result, **kwargs):
    if should_check(task_result):
        return invoke_skill("quality-checker", task_result)
```

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | File này — main spec |
| `references/check-criteria.md` | Chi tiết từng check category |
| `templates/verdict-format.yaml` | Template output verdict |

---



## Profile-Aware Behavior

Skill này là **global** — đặt ở `~/.hermes/skills/quality-checker/` (default profile's home) và **mọi profile đều dùng được**:
- `~/.hermes/profiles/content-director/` (TikTok content)
- `~/.hermes/profiles/research-lead/` (Research)
- `~/.hermes/profiles/coder/` (Code)

State file path resolve tự động:
```python
profile_name = os.environ.get("HERMES_PROFILE", "default")
state_file = f"~/.hermes/profiles/{profile_name}/state.md"
```

Không cần config riêng cho mỗi profile. Mọi output check xong đều log vào state.md của profile đó.

---

## Related

- [[Loop-Engineering-System]] — Parent system
- [[hermes-agent-complete-guide]]
- [[content-creator]]
- Bài Addy Osmani "Loop Engineering" (Substack 8/6/2026)

---

*Last updated: 2026-06-16*
*Part of: Loop Engineering system-wide deployment*
