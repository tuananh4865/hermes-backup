---
title: Hermes Agent Autoresearch
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-04-27
type: skill
tags: [autoresearch, self-improvement, hermes-agent]
description: AutoResearch pattern cho Hermes Agent - tự cải thiện mỗi đêm
trigger: Cron job chạy tự động mỗi đêm
---

# Hermes Agent Autoresearch

> Pattern từ karpathy/autoresearch — áp dụng cho Hermes Agent
> Chạy tự động mỗi đêm, không cần human in loop

## Core Loop

```
1. Đọc program.md (hướng dẫn từ lần trước)
2. Chạy self-improvement tasks
3. Đo metrics
4. Ghi log
5. Cập nhật program.md nếu cần
6. Lặp lại
```

## IMPORTANT PATHS (verified working)

```
Wiki:         /Volumes/Storage-1/Hermes/wiki
Scripts:      /Volumes/Storage-1/Hermes/wiki/scripts
Skills:       /Volumes/Storage-1/Hermes/skills  (symlinked to ~/.hermes/skills)
Memories:     ~/.hermes/memories
Cron output:  ~/.hermes/cron/output
```

## Wiki Maintenance Commands

```bash
# Health check (fast mode - skip slow broken links check)
cd /Volumes/Storage-1/Hermes/wiki
python3 scripts/wiki_lint.py --fast

# Auto-heal all issues (broken links, missing frontmatter)
python3 scripts/wiki_self_heal.py --fix --all

# Full health check to verify fixes
python3 scripts/wiki_lint.py
```

## Metrics để Track

| Metric | Target | Đo bằng |
|--------|--------|---------|
| Broken links | 0 | wiki_lint.py |
| Pages missing frontmatter | 0 | wiki_lint.py |
| Orphan pages | < 5% | wiki_lint.py |
| Task success rate | > 90% | Session logs |
| Retry count | Giảm qua thời gian | Memory |

## Những việc làm mỗi đêm

### 1. Wiki Maintenance
```bash
cd /Volumes/Storage-1/Hermes/wiki
python3 scripts/wiki_lint.py --fast          # Report issues
python3 scripts/wiki_self_heal.py --fix --all  # Auto-fix
python3 scripts/wiki_lint.py                # Verify
```
- Check orphan pages — tạo links hoặc archive
- Update freshness scores

### 2. Skill Improvement
- Review skills yếu (low confidence scores)
- Research best practices cho từng skill domain
- Update SKILL.md với findings
- Thêm examples mới

### 3. Knowledge Acquisition
- Research AI agent trends mới nhất
- Update wiki với concepts mới
- Tìm và ingest有价值的内容
- Update learned-about-tuananh.md nếu có patterns mới

### 4. Self-Critique
- Review lại errors từ session trước
- Tìm patterns trong failures
- Update memory với lessons learned
- Đề xuất improvements cho workflow

## Output Format

Mỗi đêm tạo report:

```
# Autoresearch Nightly Report — YYYY-MM-DD

## Metrics
- Broken links: X (was Y)
- Missing frontmatter: X (was Y)
- Task success rate: X%
- New wiki pages: X
- Skills improved: X

## Actions Taken
1. [Action 1]
2. [Action 2]

## Findings
- [Finding 1]
- [Finding 2]

## Next Steps
1. [Step 1]
2. [Step 2]
```

## Cron Job Setup

```bash
# Create cron job
cronjob create \
  --name "Hermes Autoresearch Nightly" \
  --skill hermes-autoresearch \
  --schedule "0 2 * * *" \
  --repeat 30 \
  --deliver "telegram:chat_id:thread_id"
```

## Constraints
- MAX 30 phút chạy
- KHÔNG sửa production code
- KHÔNG xóa important wiki pages
- KHÔNG override user preferences
- If uncertain, SKIP and note in report
