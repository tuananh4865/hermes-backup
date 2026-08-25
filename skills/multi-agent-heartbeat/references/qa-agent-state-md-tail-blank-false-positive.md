# qa-agent state.md Read Failure Modes (3 variants)

**All 3 variants produce read_file errors on the same huge file (~100KB-200KB+). Discriminate by error message, then apply the right recipe. Discriminator table at the bottom.**

## Variant 1: Empty content from tail padding (2026-06-27 14:30)

**Symptom:**
- `qa-agent/state.md` is large (210KB+ / 121 lines)
- `read_file(path, limit=500)` returns `content: ""` and `length: 0`
- Frontmatter shows `updated: <yesterday>` (NOT stale per H36 since file mtime confirms)

**Diagnosis — NOT corruption:**
The file is normal. `read_file` returns the tail of the file. qa-agent's state.md ends with `## Profile-specific Config` followed by 3 short bullet lines, then a long stretch of blank padding lines. The `read_file` slicing hits the blank tail and reports `length: 0` because empty strings have no visible characters.

## Variant 2: 100K char safety limit refusal (2026-06-28 10:31)

**Symptom:**
- `qa-agent/state.md` is large (195KB+ / 117 lines)
- `read_file(path, limit=500)` returns an ERROR: `"Read produced 105,300 characters which exceeds the safety limit (100,000 chars). Use offset and limit to read a smaller range. The file has 117 lines total."`
- Error message includes the actual total line count

**Diagnosis — NOT corruption:**
The file is normal. The read_file tool has a hard 100,000-character safety limit. The 117-line qa-agent state.md (with each H-sweep row being ~2-5KB of text) easily exceeds 100K chars total.

**Recipe — use offset + limit to read what you need:**
```python
# Read first 60 lines — contains frontmatter, Current Goal, full verdict rows for ~12 most recent sweeps
read_file(path=qa_state_md, offset=1, limit=60)

# If you need older sweeps (e.g. for H34/H38 forensic checks), read in additional chunks
read_file(path=qa_state_md, offset=61, limit=60)
```

**You almost never need to read the whole file.** The first 60 lines cover everything the heartbeat needs:
- Frontmatter (profile, goal, updated, loop_engineering)
- Current Goal section
- Last ~12 verdict rows in full (each H-sweep row is ~3-5KB)
- The `## Verdict History` section header

**Why this is fine for the heartbeat:**
The heartbeat is a structural check, not a forensic read. The 60-line window is enough to:
- See frontmatter (current Goal)
- See the last 10-12 H-sweep rows (cron-truth cross-reference, H-number progression, H60/H65 auto-suspend tracking)
- Detect Mode 1-8 corruption in those rows
- Skip the bulk of H-sweep history that's only relevant for forensics

**For forensic reads (H34/H38 root-cause analysis), read the rest in chunks.** This is rare — only when investigating a specific H-number pattern that requires going back to the source.

## Variant 3: (theoretical, not yet observed) Binary / zero-byte corruption

**Symptom:** `wc -c` reports <1KB, `wc -l` reports 100+ lines, `file` reports "data" or "empty".

**Diagnosis — REAL corruption.** Apply H35/H39 recovery recipe.

## Variant 4: `read_file limit=60` doesn't reach the bottom of qa-agent state.md (2026-06-28 12:01)

**Symptom:**
- `qa-agent/state.md` is large (195KB+ / 117+ lines)
- `read_file(path, offset=1, limit=60)` SUCCEEDS but only covers the frontmatter + structural sections (Current Goal, Active Tasks tables which are empty for dormant system) + the OLDEST H-sweep rows in the file, not the newest
- The MOST RECENT H-sweep row (the one the heartbeat needs to cross-reference) is at the BOTTOM of the file, not the top
- Need to see what H-sweep just ran, what its verdict was, what the cron-truth sweep showed

**Diagnosis — Recipe drift:** the original `offset=1, limit=60` recipe assumed ~3-5KB H-sweep rows, so 60 lines = ~12 H-sweeps. By 2026-06-28, qa-agent's H-sweep rows had grown to 6-8KB each (deeper cron-truth sweeps, longer orchestrator handoff prose, pre-fire captures). 60 lines from the top = ~7-10 H-sweeps from when the file STARTED (H63+ range), NOT the most recent.

**Recipe — terminal `tail` is the right tool when you need the BOTTOM of the file:**

```bash
# Read the most recent 100 lines (no 100K limit, no read_file slicing math)
terminal(command="tail -100 ~/.hermes/profiles/qa-agent/state.md")

# Or if you need more (full row of the most recent H-sweep which can be 8-10KB)
terminal(command="tail -150 ~/.hermes/profiles/qa-agent/state.md")

# Combine: frontmatter from read_file + tail from terminal
# Step 1: read_file(limit=5) -> frontmatter (Goal, updated, loop_engineering)
# Step 2: terminal(tail -100) -> most recent H-sweep rows
```

**Why this works when `read_file limit=60` doesn't:**
- `tail` operates on raw bytes, doesn't have the 100K char safety limit
- `tail -N` always returns the LAST N lines regardless of file size
- For the heartbeat, you almost NEVER need the middle of the file — you need the FRONTMATTER + the MOST RECENT H-sweep row

**Trade-off vs `read_file offset=1, limit=60`:**
- tail gives you the actual most recent data
- No line-count math needed
- tail output isn't line-numbered (less precise for cross-referencing specific H-N rows)
- Uses 1 extra tool call vs 0 for read_file

**When to use which:**
- `read_file offset=1, limit=60` -> when you need frontmatter + structural sections (Current Goal, Active Tasks, Handoff History). Good for files < 100KB.
- `terminal tail -100` -> when you need the most recent H-sweep row's full content (cron-truth sweep, 6-check protocol verdict, recipe hold rate). Bypasses 100K limit.
- BOTH -> when you need full context (the heartbeat's normal case). 2 tool calls, both fast.

**Lesson:** For the qa-agent state.md in particular, treat frontmatter and most-recent-H-sweep as the two endpoints you actually need. The middle 100+ H-sweep rows are forensic detail — only relevant when investigating a specific H-number pattern. The heartbeat is a structural check, not a forensic read.

**Worked example (2026-06-28 12:01 sweep, 5-tool-call budget):**
1. `read_file(limit=5)` on qa-agent state.md -> frontmatter
2. `terminal(tail -100)` on qa-agent state.md -> most recent H-sweep (H69 at 06:02)
3. `read_file` on the 4 smaller profile state.md files (engineering-lead 10KB, operations-manager 27KB, code-reviewer 2KB, security-engineer 8KB - all fit in one read each)
4. `hermes cron list` -> ground truth
5. `find ~/.hermes/profiles -name "pending*"` -> pending/handoff scan

Total: 5-6 tool calls. Well within H32b budget of ~10. The tail of the qa-agent file already includes the `## Profile-specific Config` boundary, so step 1 (frontmatter-only read) is optional.

**Worked example (2026-06-28 18:00 sweep, 6-tool-call budget — V7 update):**
1. `read_file(path=qa_state, offset=1, limit=60)` — succeeds (returns H34-H60 range, ~95KB)
2. `read_file(path=qa_state, offset=60, limit=58)` — succeeds (returns H60-H70 range + `## Verdict History` table, ~95KB)
3. `read_file` on the 4 smaller profile state.md files (engineering-lead 10KB, operations-manager 32KB, code-reviewer 2.6KB, security-engineer 7.7KB - all fit in one read each)
4. `hermes cron list | head -80` -> ground truth (paginated to avoid context blowup)
5. `find ~/.hermes/profiles \( -name "pending*" -o -name "handoff*" \)` -> pending/handoff scan
6. `date "+%Y-%m-%d %H:%M:%S %Z"` -> sweep timestamp

Total: 6 tool calls. Well within H32b budget of ~10. The V6 recipe's `offset=59, limit=60` was off-by-one — V7 uses `offset=60, limit=58` to avoid double-reading line 60. Both work, but V7 form is cleaner.

**Discriminator table update:**
| Observation | Variant | Action |
|---|---|---|
| `read_file limit=60` succeeds but doesn't show the most recent H-sweep | 4 - recipe drift | Use `terminal tail -100` instead |

## Universal discriminator (one-liner per variant)

```bash
# Variant 1: tail padding
read_file returns content: "" → run `wc -c` → if huge, Variant 1 (skip)

# Variant 2: 100K safety limit
read_file returns ERROR with "exceeds the safety limit (100,000 chars)" → Variant 2 (re-read with offset=1, limit=60)

# Variant 3: real corruption
read_file returns tiny content OR error about binary → run `wc -c` + `file` → if <1KB or "data", Variant 3 (H35/H39 recovery)
```

## Discriminator table (canonical)

| Observation | Variant | Action |
|---|---|---|
| `wc -c` ≥ 50KB, `read_file` returns 0 chars | 1 — tail padding | Skip, no recovery needed |
| `read_file` returns "exceeds the safety limit (100,000 chars)" error | 2 — 100K limit | Re-read with `offset=1, limit=60` |
| `wc -c` < 5KB, last H-sweep row incomplete | 3 — real H35/H39 corruption | Invoke recovery recipe |
| `wc -l` says 100+ lines but `wc -c` says <1KB | 3 — binary/zero-byte | Real corruption, recover |
| Frontmatter `updated:` > 24h old BUT `wc -c` huge | H36 clock anomaly OR H26 Mode 8 silent sweep | Not corruption |

## Confirmation recipe (run when uncertain)

```bash
wc -l /Users/tuananh4865/.hermes/profiles/qa-agent/state.md
wc -c /Users/tuananh4865/.hermes/profiles/qa-agent/state.md
file /Users/tuananh4865/.hermes/profiles/qa-agent/state.md
python3 -c "import os; print(os.path.getsize('/Users/tuananh4865/.hermes/profiles/qa-agent/state.md'))"
```

**Lesson:** Don't waste tool calls on "state.md corruption" triage just because `read_file` returns empty OR errors. Always cross-check file size (`wc -c`) and line count (`wc -l`) before invoking H35/H39 recovery. For Variant 2 (100K refusal), the fix is a single re-read with offset/limit — saves 2-4 tool calls per sweep.

**When to apply the compaction recipe (the real fix):** If Variant 1 or Variant 2 fires repeatedly (more than 3 consecutive sweeps), the file is unhealthily large. Apply the heartbeat-state-md-bloat compaction recipe — keep only last 10-20 H-sweep rows + the structural sections, drop the rest. This is a separate operation, not part of the sweep itself.

**Sibling skill files:**
- `references/state-md-integrity-pattern.md` — full H35 corruption detection (when real)
- `references/h36-clock-anomaly-pattern.md` — frontmatter lies, use mtime
- `references/h39-inherited-truncation-pattern.md` — when prior sweep row was corrupted
