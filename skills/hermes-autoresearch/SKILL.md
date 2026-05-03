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
cd /Volumes/Storage-1/Hermes/wiki

# Step 1: Fast health check (broken links SKIPPED in fast mode)
python3 scripts/wiki_lint.py --fast

# Step 2: Run self-heal to fix issues
python3 scripts/wiki_self_heal.py --fix --all

# Step 3: CRITICAL - Verify with FULL lint, not fast
# self-heal may claim "No broken links" but full lint finds 375+
# Only full lint detects broken wikilinks
python3 scripts/wiki_lint.py
```

### ⚠️ CRITICAL: fast vs full lint behavior
- `--fast` mode: skips broken wikilink check AND orphan check
- Full lint: finds ALL issues including 375+ broken wikilinks
- **self-heal may report "No broken links found" but full lint still shows them**
- Always verify with full lint after self-heal
- If full lint still shows broken links after heal, the heal script has a bug — log as known issue

### Orphan Pages
- Orphan count grows ~20 per night (Telegram transcripts)
- Low priority — don't spend time linking transcripts
- Archive old orphans if they have no long-term value

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

### Delivery Format Pitfalls

**ĐỊNH DẠNG ĐÚNG:** `telegram:chat_id:thread_id`
- Ví dụ: `telegram:1132914873:3764041476`
- Dùng DẤU HAI CHẤM (`:`), KHÔNG phải dấu slash (`/`)

**LỖI THƯỜNG GẶP:**
```
invalid literal for int(): '1132914873:3764041476/604'
```
→ Thread ID bị thừa suffix `/604` hoặc dùng `/` thay vì `:`

**CÁCH SỬA:** Update job với deliver đúng:
```bash
cronjob update --job_id <id> --deliver "telegram:chat_id:thread_id"
```

**CÁCH DEBUG:** Kiểm tra `last_status` và `last_delivery_error`:
- `last_status: ok` + `last_delivery_error` ≠ null → Job chạy OK nhưng gửi thất bại
- `last_status: ok` + `last_delivery_error: null` → Job thành công hoàn toàn

## Known Issues (autoresearch)
- **self-heal vs lint discrepancy**: self-heal claims fixed but full lint still shows broken links — this is a script ordering/timing bug, not a real failure. Don't re-run, just note in report.
- **Telegram polling conflict**: Multiple Hermes PIDs conflict on Telegram getUpdates — requires manual `kill -9`. Not fixable via cron.
- **Gateway restart PID leak**: `hermes gateway restart` doesn't kill old processes — known bug, requires manual kill.

## Constraints
- MAX 30 phút chạy
- KHÔNG sửa production code
- KHÔNG xóa important wiki pages
- KHÔNG override user preferences
- If uncertain, SKIP and note in report
