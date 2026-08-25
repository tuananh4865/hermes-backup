---
name: hermes-file-edit-logging
description: System-wide protocol for logging every file edit as append-only NDJSON at `/Volumes/Storage-1/Hermes/logs/daily/YYYY-MM-DD.jsonl`. Mirror path + before/after size + reason for audit trail / backlog / restore. V2 pattern (NDJSON flat, 1 file/day, grep-friendly) — REPLACED V1 over-engineered nested JSON. Load when user wants logs / lịch sử / restore / backlog / khôi phục / mirror vị trí / append-only changelog. Class-level skill — works for ANY file type (.md, .py, .json, .yaml, .sh, MP4 metadata, skill SKILL.md).
---

# Hermes File-Edit Logging

## Why this skill exists

**User verbatim (2026-07-19):** *"Tạo một thư mục trong storage-1/Hermes tên logs... phân loại gần giống mirror vị trí của file em chỉnh sửa hoặc thêm mới... chi tiết em đã làm gì và thay đổi từ cái gì thành cái gì... để khi muốn khôi phục hoặc backlog lại thì có thể biết chính xác em đã thêm những gì và trước đó là gì"*

The pain point: Agent edits a file, user wants to know "what changed" days later → no audit trail exists unless the user manually diffs. When the user wants to restore or backlog, they have to guess.

The fix: Every file edit appends one **NDJSON line** with **mirror path + before/after size + reason**. Append-only, never overwrite, grep-friendly (Stripe/CloudTrail/AWS audit log pattern).

## When to load

- User explicitly says "logs / lịch sử / restore / backlog / khôi phục / mirror vị trí / track file edits"
- User asks "em đã sửa gì?" or "trước đó là gì?"
- After a 5+ tool-call session that touched many files
- Before claiming "đã xong" on a task that involved file edits
- **Hermes-Only-Folder-Rule (load BEFORE writing ANY file inside `~/.hermes/`)** — see Lesson 5 below. Hardcoded Hermes paths (e.g. `~/.hermes/memory_store.db`) require the SYMLINK pattern, not a direct write.

## Folder structure (V2 — FLAT NDJSON, replaces V1 nested JSON)

```
/Volumes/Storage-1/Hermes/logs/
├── README.md                       # Overview + protocol
├── daily/                          # ⭐ MOST IMPORTANT — 1 NDJSON file per day
│   └── YYYY-MM-DD.jsonl            # Append-only, 1 line/edit
├── errors/                         # Errors with context (manual write)
│   └── YYYY-MM-DD-errors.log
└── archive/                        # Files >90 ngày
    └── YYYY/YYYY-MM/{file}
```

**V2 vs V1** — why we refactored:
| Metric | V1 (over-engineered) | V2 (current) |
|--------|----------------------|--------------|
| Subcommands | 4 (init/edit/history/manual) | 2 (append/query) |
| Folders | 6 | 3 |
| Script lines | 293 | 159 (-46%) |
| Script bytes | 10.2KB | 5.5KB (-47%) |
| File layout | Nested `file-edits/{date}/{mirror-path}/{file}.json` | Flat `daily/{date}.jsonl` |
| JSON format | Pretty-printed (4-space indent) | NDJSON compact (no space after `:`) |
| Industry pattern | Custom | Stripe/CloudTrail/AWS audit log |

**Why NDJSON compact:** `json.dumps(entry, separators=(",", ":"))` — grep-friendly (`grep '"action":"modify"'`), small (~50% size reduction vs pretty), 1 line per entry → diff/awk/sort work natively.

## 3 Mirror roots (mirror path = path RELATIVE to nearest root)

```python
MIRROR_ROOTS = [
    Path("/Volumes/Storage-1/Hermes"),     # → "Hermes/..."
    Path("/Volumes/Storage-1/Pocket3"),     # → "Pocket3/..."
    Path("/Users/tuananh4865"),             # → "Users/tuananh4865/..."
]
```

**Examples:**
- `/Volumes/Storage-1/Hermes/wiki/projects/foo.md` → `Hermes/wiki/projects/foo.md`
- `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip.mp4` → `Pocket3/Hermes-Edit/clip.mp4`
- `/Users/tuananh4865/.hermes/skills/x.md` → `Users/tuananh4865/.hermes/skills/x.md`

## Canonical log entry format (NDJSON, append-only)

```json
{"ts":"2026-07-19T21:24:39+07:00","file":"Hermes/scripts/foo.py","action":"create","reason":"Init log system","before":0,"after":10255}
```

Fields:
- `ts`: ISO 8601 với timezone ICT (+07:00)
- `file`: Mirror path (relative to `/Volumes/Storage-1/` or Mac home)
- `action`: `create` | `modify` | `delete`
- `reason`: WHY this edit was made (anh đọc cái này để biết intent)
- `before`, `after`: Size in bytes (integer)

## Mandatory workflow

```bash
# Step 1: Make the edit
write_file /path/to/file.md "..."

# Step 2: Append 1 NDJSON line (MUST RUN — never skip)
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py append /path/to/file.md \
    --reason "Anh yêu cầu X" \
    [--action create|modify|delete]

# Step 3: Verify log was appended
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py query --file /path/to/file.md
# OR grep the raw NDJSON:
grep '"file":"Hermes/scripts/foo.md"' /Volumes/Storage-1/Hermes/logs/daily/2026-07-19.jsonl
```

## Query recipes (3 ways)

```bash
# 1. CLI query (formatted)
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py query --last 10
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py query --file Hermes/scripts/foo.py
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py query --date 2026-07-19

# 2. Raw NDJSON grep (industry-standard)
grep '"action":"create"' /Volumes/Storage-1/Hermes/logs/daily/*.jsonl
grep '"file":"Hermes/scripts/foo.py"' /Volumes/Storage-1/Hermes/logs/daily/*.jsonl

# 3. jq for structured output
cat /Volumes/Storage-1/Hermes/logs/daily/2026-07-19.jsonl | jq -s 'sort_by(.ts) | .[-5:]'
```

## Restore / backlog recipe

```bash
# Step 1: Find history
python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py query --file /path/to/file.md

# Step 2: Read the reason field — tells you WHY each version existed
# (e.g., "Add line 1", "Refactor v1→v2 (293→158 lines)")

# Step 3: Restore content
# - If git tracked: git checkout <commit> -- <file>
# - If git NOT tracked: rebuild manually from reason + recent reads,
#   OR request a daily snapshot (TODO: cron .backups/{date}/{path})
```

**NOTE:** NDJSON does NOT store content — only metadata. To enable real restore, set up daily backup cron (TODO): copy file gốc sang `/Volumes/Storage-1/Hermes/.backups/{date}/{path}` mỗi 23:00.

## Anti-patterns (refuse)

| Anti-pattern | Why it fails |
|---|---|
| Edit file KHÔNG log | User mất khả năng restore/backlog |
| Log inline vào file đang edit | Circular dependency — file edit triggers log → log write triggers file edit |
| Ghi đè log cũ | Mất lịch sử — phải append (NDJSON append-only by design) |
| Pretty-printed JSON thay vì NDJSON compact | `grep '"action":"modify"'` fails on `"action": "modify"` (space after colon) |
| Mirror path sai (vd dùng `/Volumes/Storage-1/Hermes/...` thay vì `Hermes/...`) | Pattern match fail khi search/filter |
| Log chỉ size, không reason | Không biết WHY edit — chỉ biết byte đổi |
| Bỏ qua tool calls nhỏ ("không quan trọng") | Anh yêu cầu "dù nhỏ đến mức em nghĩ không cần báo cáo thì cũng phải logs" |
| **V1 nested JSON layout** (`file-edits/{date}/{mirror}/{file}.json` array) | Over-engineered — V2 NDJSON flat đơn giản hơn, grep được, 46% code nhỏ hơn |
| **6 sub-folders** (file-edits + session-summaries + tool-calls + errors + cron-outputs + archive) | Most never used in practice — V2 chỉ cần 3 (daily + errors + archive) |

## Auto-cleanup (TODO cron)

- File `daily/*.jsonl` >90 ngày → move sang `archive/YYYY/YYYY-MM/`
- File `archive/*` >365 ngày → compress `.gz` hoặc delete (hỏi anh trước)
- Cron monthly: `~/.hermes/cron/log-archive-monthly.sh` (chưa setup — TODO)

## Linked files

- `scripts/log_helper.py` — Canonical CLI tool at `/Volumes/Storage-1/Hermes/scripts/log_helper.py` (V2: 159 lines, 5.5KB, 19/07/2026)
- `references/v2-ndjson-compact-pattern.md` — Why NDJSON compact (no space after `:`), reusable across any audit log

> **Note:** `references/logs-protocol-detailed.md` was V1's over-engineered nested-JSON reference. V2 replaced it entirely with NDJSON flat layout — do NOT link V1 anymore. If you find yourself wanting nested folders, re-read this SKILL.md's Anti-patterns section first.

## Lessons learned (vĩnh viễn — 19/07/2026)

### Lesson 1 — Senior engineer check before ship
**Trigger:** Em tạo V1 (293 lines, 6 folders, 4 subcommands) quá nhanh. Anh phản hồi: *"phân tích kĩ yêu cầu của anh sau đó lên plan và tìm kiếm tham khảo thêm cách set up quản lý log để backlog hiệu quả nhất mà không over engineer"*.

**Rule:** TRƯỚC KHI ship 1 design, hỏi: *"Would a senior engineer say this is overcomplicated?"* — nếu YES, refactor. Áp dụng cho MỌI class-level design (script, skill, file structure).

**6 phase loop** (Plan → Research → Decide → Execute → Verify → Reflect) anh dặn 19/07:
1. **PARSE** yêu cầu thành atomic deliverables (10 atomic từ 1 câu)
2. **RESEARCH** industry patterns (git/file-watcher/JSONL/snapshot — 4 patterns)
3. **GRILL** trade-offs (ưu/nhược table — pick best fit)
4. **PLAN** minimum design (Senior engineer check)
5. **EXECUTE** (refactor đơn giản)
6. **VERIFY** test thật + bug hunt

### Lesson 2 — NDJSON compact (no space after `:`)
**Trigger:** V1 dùng `json.dumps(entry)` default → có space sau `:` → `grep '"action":"modify"'` FAIL vì format thực tế là `"action": "modify"`. Em hunt bug trong test 6 → fix bằng `json.dumps(entry, separators=(",", ":"))`.

**Rule:** KHI ghi log vào audit file dùng cho grep, LUÔN dùng **NDJSON compact format** (industry standard: NDJSON specification, CloudTrail/Stripe/AWS). Code:
```python
json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
```
**Reusable:** Cho MỌI audit log (security, cron, session, error) — pattern này apply khắp nơi, không chỉ file edit.

### Lesson 3 — Hermes-Only Folder Rule (with SYMLINK escape hatch for hardcoded paths)
**Trigger:** Anh yêu cầu 19/07: *"anh muốn em làm mọi việc trong Volumes/Storage-1/Hermes phải tạo và làm tất cả mọi thứ trong đó!!!"*. Lần thứ 2 anh catch em vi phạm với DB memory_store.db: *"Anh đã nói tất cả path chuyển sang storage-1/Hermes mà"*.

**Rule:** Mọi file MỚI em tạo cho anh PHẢI nằm trong `/Volumes/Storage-1/Hermes/`. KHÔNG tạo ở `/Users/tuananh4865/` trừ system config bắt buộc (`~/.hermes/` vì gateway reads `config.yaml` khi start). Scope `~/.hermes/` + `/Volumes/Storage-1/Pocket3/Hermes-Edit/` giữ NGUYÊN vì:
- `~/.hermes/` chứa gateway config — move đi = break
- `Pocket3/Hermes-Edit/` chứa clip ship + raw footage ở cùng volume — move tăng latency

**⚠️ SYMLINK escape hatch for hardcoded Hermes paths (Pitfall P3):**
Khi Hermes hardcode 1 path trong `~/.hermes/` (vd `~/.hermes/memory_store.db`, `~/.hermes/config.yaml`, hook directories), KHÔNG copy file thật vào `~/.hermes/` — dùng symlink pattern:
```bash
# Real file at Hermes
mkdir -p /Volumes/Storage-1/Hermes/.hermes-data
touch /Volumes/Storage-1/Hermes/.hermes-data/<file>

# Symlink at the hardcoded Hermes path
ln -sf /Volumes/Storage-1/Hermes/.hermes-data/<file> ~/.hermes/<file>

# Verify (Hermes reads via symlink = same file)
ls -la ~/.hermes/<file>
```

**Why:** Anh's rule says "all in `/Volumes/Storage-1/Hermes/`" but Hermes system reads from `~/.hermes/<file>` directly — symlink gives both: file lives in Hermes, Hermes system still finds it. Same pattern works for `~/.hermes/cron/output/<job-id>/` (mirror to `/Volumes/Storage-1/Hermes/cron-output/<job-id>/` via symlink if needed).

**Plan doc:** `/Volumes/Storage-1/Hermes/docs/HERMES-ONLY-FOLDER-PLAN-2026-07-19.md`

### Lesson 4 — Anti-fabrication: Self-hunt bugs in own output
**Trigger:** Phase 6 verify, test 6 (grep on pretty JSON) fail — em tự investigate root cause (NDJSON standard) thay vì đổ lỗi cho tool.

**Rule:** Sau mỗi verify pass, em TỰ HUNT 1 bug edge case khác (không chỉ pass là xong). Adversarial mindset: "cái gì có thể SAI mà em chưa check?". Nếu grep work thì test command cũng work, nếu work thì test pipe với jq, etc.

## Related skills

- `evidence-first-delivery` — Sister skill. This handles audit trail; that handles completion-claim proof. Load both together for "đã xong" claims on multi-file tasks.
- `self-verify-after-workaround` — Workaround-specific verification; this is general-purpose logging.
- `code-simplification` — Load khi suspect code đang over-engineered (apply senior engineer check).

---
*V2 refactored 2026-07-19 from V1 over-engineered (293 lines → 159 lines, 6 folders → 3, nested JSON → flat NDJSON). Class-level — applies to ALL future file edits, not just one session.*
