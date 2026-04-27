---
title: "Hermes Skill Self-Improvement System"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [hermes, skill-system, self-improvement, agent]
description: "Hệ thống tự cải thiện cho Hermes Agent gồm skill_recommend, skill_insight_analyzer, auto_skill_patch"
sources: [raw/transcripts/2026-04-15-https-agentwrapper-status.md]
---

# Hermes Skill Self-Improvement System

## Tóm tắt

Hệ thống tự cải thiện cho Hermes Agent gồm 3 thành phần chính: **skill_recommend** (log usage data), **skill_insight_analyzer** (phân tích gaps), **auto_skill_patch** (tự động sửa trigger conditions yếu). Dựa trên triết lý "Thin Harness, Fat Skills" của Garry Tan.

## 3 thành phần

### 1. skill_recommend

- Tự động log mỗi lần gọi vào `~/.hermes/skills/_usage_log.jsonl`
- Log: timestamp, task_hash (MD5), task, recommended_skills[], selected_skill, outcome, session_id
- Lấy session_id từ `HERMES_SESSION_ID`, outcome từ `HERMES_OUTCOME`

### 2. skill_insight_analyzer

- Script: `/Volumes/Storage-1/Hermes/scripts/skill_insight_analyzer.py`
- Phân tích `_usage_log.jsonl` để tìm:
  - Missing skills gaps
  - Weak trigger_conditions
  - Low-success skills
  - Workflow patterns
- CLI: `python3 skill_insight_analyzer.py [--min-entries N] [--json] [--hours N]`

### 3. auto_skill_patch

- Script: `/Volumes/Storage-1/Hermes/scripts/auto_skill_patch.py`
- Safe auto-patches (không cần user approval): trigger_conditions, use_case_keywords, tags
- Risky (cần user confirm): tạo skill mới, xóa skill, rewrite body
- CLI: `auto_skill_patch.py --dry-run | --apply | --skill <name> --add-trigger | --report`

## Self-improvement loop

```
skill_recommend() → log vào _usage_log.jsonl
       ↓
skill_insight_analyzer (chạy 7AM cron hàng ngày)
       ↓
auto_skill_patch (áp dụng trigger_conditions improvements)
       ↓
Skills compound over time → ngày càng thông minh hơn
```

## Đã tạo

- `~/.hermes/skills/hermes/skill-insight-analyzer/SKILL.md`
- `~/.hermes/skills/hermes/auto-skill-patch/SKILL.md`
- `~/.hermes/skills/creative/architecture-diagram/SKILL.md` (từ Teknium's Cocoon AI port)
- `~/.hermes/skills/_usage_log.jsonl` (auto-created, gitignored)

## Liên quan

- [[hermes-dojo]]
- [[Garry Tan]] - "Thin Harness, Fat Skills" philosophy
- Teknium - upstream developer trên branch `gateway-plugin-loading`
- Cocoon AI - architecture-diagram-generator
