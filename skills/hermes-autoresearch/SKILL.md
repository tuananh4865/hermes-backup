---
title: Hermes Autoresearch — Karpathy-Style
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-05-04
type: skill
tags: [autoresearch, self-improvement, karpathy-pattern]
description: AutoResearch pattern lấy cảm hứng từ karpathy/autoresearch — tự cải thiện không ngừng mỗi đêm
trigger: Cron job chạy tự động, NEVER STOP cho đến khi human interrupt
---

# Hermes Autoresearch — Karpathy-Style

> Lấy cảm hứng từ [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
> Core idea: **give an agent a narrow scope + single metric + git memory = autonomous improvement**

## Core Philosophy

Karpathy's insight: "You're not touching Python files. You're programming the `program.md`."

Tương tự với Hermes:
- **KHÔNG modify code** — chỉ modify `program.md` (hướng dẫn cho agent)
- **1 metric duy nhất** để optimize
- **Git là memory** — rollback khi cần
- **NEVER STOP** — cho đến khi human interrupt

---

## Repository Structure

```
~/.hermes/autoresearch/
├── program.md          ← SKILL CHÍNH: human edit để program agent
├── knowledge.md        ← persistent memory: patterns đã thử, results
├── DISCARDED.md        ← những thứ đã thử và thất bại
├── RESULTS.tsv         ← log: metric per experiment
├── research.py         ← fixed: benchmark script để đo metric
└── pyproject.toml     ← dependencies
```

---

## The Single Metric

**Wiki Health Score (WHS)** — lower is better, 0 = perfect

```
WHS = broken_links × 10 + missing_frontmatter × 5 + orphan_pages × 1
```

Target: **WHS = 0**

---

## The Experiment Loop

```
LOOP FOREVER:
1. Đọc program.md để hiểu current instructions
2. Đọc knowledge.md để tránh lặp lại những gì đã thử
3. Đọc DISCARDED.md để tránh những thất bại đã biết
4. Sửa knowledge.md (bổ sung insights mới)
5. Tune program.md với experimental idea
6. git commit
7. Chạy: python3 research.py > run.log 2>&1
8. Đọc kết quả: grep "^whs:" run.log
9. Nếu WHS improved (lower) → giữ thay đổi
10. Nếu WHS same/worse → git reset
11. Ghi vào RESULTS.tsv
12. Lặp lại
```

---

## Program.md Template

```markdown
# Hermes Autoresearch Program

## Mission
Improve Hermes Agent's wiki health by reducing broken links, missing frontmatter, and orphan pages.

## Current Priority
[Agent fill: what should we focus on tonight?]

## Constraints
- MAX 3 phút per experiment (để chạy được nhiều experiments)
- KHÔNG sửa production code
- KHÔNG xóa pages có giá trị
- Nếu uncertain, DISCARD và note lý do

## Experiment Ideas to Try
[Human fill: những hướng nghiên cứu cụ thể]

## What NOT to try again
[From DISCARDED.md]
```

---

## Research.py (Fixed)

```python
#!/usr/bin/env python3
"""Fixed benchmark script - DO NOT MODIFY"""
import subprocess
import re

def run_benchmark():
    # Chạy wiki_lint.py và parse output
    result = subprocess.run(
        ["python3", "scripts/wiki_lint.py"],
        capture_output=True, text=True,
        cwd="/Volumes/Storage-1/Hermes/wiki"
    )
    
    output = result.stdout + result.stderr
    
    # Parse metrics
    broken_links = len(re.findall(r"broken.*link", output, re.I))
    missing_fm = len(re.findall(r"missing.*frontmatter", output, re.I))
    orphans = len(re.findall(r"orphan", output, re.I))
    
    whs = broken_links * 10 + missing_fm * 5 + orphans * 1
    
    print(f"whs: {whs}")
    print(f"broken_links: {broken_links}")
    print(f"missing_frontmatter: {missing_fm}")
    print(f"orphans: {orphans}")
    
    return whs

if __name__ == "__main__":
    run_benchmark()
```

---

## Cron Job Setup

```bash
# Create cron job - chạy mỗi đêm lúc 2AM
cronjob create \
  --name "Hermes Autoresearch Nightly" \
  --prompt "Run the autoresearch loop from ~/.hermes/autoresearch/program.md. READ program.md first, then execute the experiment loop. NEVER STOP until human interrupts. Report results to telegram when complete." \
  --schedule "0 2 * * *" \
  --repeat 30 \
  --deliver "telegram:1132914873:3764041476" \
  --skills ["hermes-autoresearch"]
```

### Test ngay
```bash
# Test research.py
python3 ~/.hermes/autoresearch/research.py

# Test experiment loop (1 iteration)
cd ~/.hermes/autoresearch
git checkout -b autoresearch/test
# Edit program.md với 1 idea
python3 research.py > run.log 2>&1
grep "^whs:" run.log
```

---

## Key Differences from Karpathy

| Aspect | Karpathy AutoResearch | Hermes AutoResearch |
|--------|----------------------|---------------------|
| Domain | LLM training | Wiki health |
| File to modify | train.py | program.md, knowledge.md |
| Metric | val_bpb (bits per byte) | WHS (wiki health score) |
| Time budget | 5 min per run | 3 min per experiment |
| Target | Lower = better | Lower = better |
| Memory | Git commits | knowledge.md + RESULTS.tsv |

## Why This Works

1. **Narrow scope**: Chỉ tập trung vào wiki health, không lan man
2. **Single metric**: Rõ ràng, không ambiguous
3. **Fast iteration**: 3 min × ~20 experiments/giờ = nhiều data points
4. **Git memory**: Rollback khi cần, never lose good state
5. **Never stop**: Cứ chạy, agent tự stop khi đạt WHS = 0

---

## References
- [[references/karpathy-autoresearch]] — Research notes on Karpathy's AutoResearch pattern (source of this design)

## Files

- **program.md**: Hướng dẫn cho agent — human edit
- **knowledge.md**: Tổng hợp insights từ experiments — agent update
- **DISCARDED.md**: Những thứ đã thử thất bại
- **RESULTS.tsv**: TSV log — commit hash, WHS, status, description

## Skills Improvement Focus (2026-05-04)

**Chủ đề: Tự cải thiện Hermes Agent skills mỗi đêm**

### Baseline (2026-05-04)
- SHS = 86
- Total skills: 28
- Low confidence: 28
- Missing examples: 6

### Single Metric: Skills Health Score (SHS)
```
SHS = stale_skills × 10 + missing_examples × 5 + broken_links × 3 + low_confidence × 2
Target: SHS = 0
```

### Cron job đã update
- Job ID: `a4b8e528983f`
- Schedule: 2AM hàng đêm, 30 lần
- Prompt: Skills improvement loop

## Why This Works

1. **Narrow scope**: Skills health = measurable, improvable
2. **Single metric**: SHS clear, no ambiguity
3. **Git memory**: Rollback when experiments fail
4. **Never stop**: Agent experiments all night
5. **Human edits program.md**: Guide the agent's focus

---

## Known Issues

- SHS = 0 có thể không đạt được nếu some skills truly need low confidence
- Script path phải là absolute vì cron job chạy từ directory khác
