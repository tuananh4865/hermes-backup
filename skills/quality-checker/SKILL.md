---
name: quality-checker
description: "Universal quality gate — verify mọi output từ maker agent trước khi deliver cho user. Apply cho system-wide Hermes workflow (Loop Engineering pattern). Check: format, voice, sources, quality bar, project-specific rules."
version: 3.6.3
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

**⚠️ Test file naming PITFALL (CRITICAL — 2026-06-17)**: 

When checking code outputs that include test files, verify the file name does NOT match `disk_cleanup` plugin's auto-delete pattern. Files matching `test_*.py` or `*.test.py` will be silently deleted 8s-2min after creation by `~/.hermes/disk-cleanup/cleanup.log` on `on_session_end`.

```python
# disk_cleanup.py source
_TEST_PATTERNS = ("test_", "tmp_")
_TEST_SUFFIXES = (".test.py", ".test.js", ".test.ts", ".test.md")
```

**Verified safe alternatives**: `verify_handler.py`, `check_handler.py`, `test.py` (no `_` prefix), `handler_test.py`.

**How to check**: If the maker creates a test file, run the file name through the pattern check. If it WILL DELETE, return FAIL with suggestion to rename to `verify_*.py`.

This is a CRITICAL issue (silent data loss), so it triggers the critical-override rule → FAIL regardless of score.

### 2. VOICE
- Hermes (general): "anh" + "em" (16/06 update)
- Content Creator scripts: "các bạn" (trung tính)
- **CẨM**: "mấy con vợ", "mấy đứa", "mấy chị", "mấy má", "anh ơi" lặp lại
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

## Workflow — Two Modes

### Mode A: Per-Output Verification (reactive — output arrives)

```
1. Nhận output từ Maker (profile hoặc subagent)
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

### Mode B: Idle Sweep (proactive — cron / heartbeat, qa-agent role)

**When**: Cron-driven qa-agent hourly/periodic sweep where the primary job is **discover if there's anything pending**, not verify a known output. Default verdict when nothing is pending is **PASS (vacuously satisfied)**.

**Why this matters**: The qa-agent profile runs as a scheduled cron job. Most ticks will find 0 pending outputs. Treating that as a defect ("nothing to check = failure") is wrong. Treating it as "no-op, skip report" loses the heartbeat signal that proves the QA gate is alive.

**Steps**:
```
1. Read OWN state.md → load prior verdict context, last sweep timestamp
2. Parallel read maker profiles' state.md (engineering-lead, content-director,
   research-lead, coder, code-reviewer, security-engineer, memory-curator).
   Batch ALL reads in ONE tool turn — saves N round-trips vs serial.
3. Read operations-manager/state.md → look for recent 6h audit summary.
   If ops-manager's last audit is <2h old and reports "0 pending QA",
   treat as cross-validation; you can rely on it instead of re-deriving.

   **Ops-manager audit freshness has THREE regimes** (learned H7/H34, 2026-06-25):
   - **Fresh (<2h old):** cross-validation available — trust ops-manager summary.
   - **Stale (2-12h old):** RE-DERIVE from primary profile reads, but ops-manager
     structural signals (Idle/Active matrix, routing log) still informative.
   - **Massively stale (>24h old):** ops-manager cron itself is broken — treat as
     a NEW multi-profile cron fault instance parallel to code-reviewer (H28)
     and security-engineer (H29). qa-agent must fully re-derive from primaries;
     add ops-manager to the cron-fault investigation list. See
     `references/idle-sweep-evidence-h34.md` for detection logic and impact.
4. Targeted search for pending/handoff files, BUT scope to
   `~/.hermes/profiles/` only. Files matching `pending*`/`handoff*`
   elsewhere (Telegram pairing queue, state snapshots, hermes-agent
   source code, git backup refs) are FALSE POSITIVES — ignore.
5. If something pending found → switch to Mode A on that specific output.
   If nothing pending → verdict = PASS (N/A), score = N/A, evidence =
   the read history proving you checked.
6. Append new row to OWN state.md "Recent Verdicts" table.
7. Report: PASS + sweep summary + idle duration observations.
```

**⚠️ Mode B sweep row insertion recipe (H15/H18/H19/H20/H22 lessons consolidated):**

Before appending a new sweep row to qa-agent/state.md:

1. **Pre-append integrity check:** Verify all prior rows have clean `| H<N> |` format. If any row is corrupted (truncated mid-cell, table column-count broken, orphan rows outside table), flag it in the new sweep's "row_corruption" note and LOG it but DO NOT attempt mid-sweep repair (per H20 scope-discipline rule).

2. **Read the FULL file with `limit=2000`** before patching. `read_file` truncates rows >~3KB silently in the cell body (the `[truncated]` marker appears in the wrapper, NOT in the cell text itself — easy to miss). Per H19: ALWAYS re-read with `limit=2000` if the previous row exceeds ~3KB.

3. **Boundary anchor verification:** Before using `\n\n## Verdict History` (or any section header) as a `patch` `old_string`, run `content.count(boundary)`. If `count > 1`, the boundary token appears inside a row body → use a multi-line context anchor (3+ lines of the previous row's tail) per H18. If `count == 1`, the H15/H25 boundary recipe is safe.

4. **Forecast realization check:** If a prior sweep row contained a forecast (e.g., "H21 will breach 24h threshold"), explicitly check the forecast in the current sweep: REALIZED / MISSED / PARTIAL. Forecasts in row bodies are auditable evidence — they demonstrate predictive calibration.

5. **Regression detection (H22 lesson):** If a previously-recovered profile (per H29 bidirectional tracking) re-faults, log it as a regression event with `recovered_at` timestamp and `gap_hours` (time between recovery and re-fault). Recovery-window-duration is a metric: shorter = more brittle recovery.

6. **Patch and verify:** After patch, read the modified file to confirm row count +1, no orphan content, table column-count preserved.

7. **Sibling-collision detection (learned H31, 2026-06-26 14:02):** Before patching, count current rows via `grep -cE "^\|{1,2} H[0-9]+ \|" state.md`. Expected count = `prev_sweep_index` (e.g., expected 30 if H30 was last). If `actual_count > expected`, a parallel cron sweep (orchestrator 30m heartbeat, sibling qa-agent tick, or daily backup cron) wrote a row between your dispatch and your read. **DO NOT patch with the planned anchor** — it would either overwrite the sibling's row or insert your new row mid-table. Re-anchor on the actual highest `H<N>` row's tail. Critical: if the sibling's row is a merged content row (e.g., H30 captured mid-H29 write as a single merged row), the "true" tail is the LAST sentence of the merged row, NOT the original expected tail. Use 4-line context anchor per H25. See `references/idle-sweep-evidence-h31.md` for full detection recipe + H31 case study.

   **⚠️ H40 SIBLING-COLLISION OVERWRITE BUG (CRITICAL — 2026-06-26 22:00):** The H31 recipe's row-count check must be run **IMMEDIATELY BEFORE THE PATCH** — not at sweep start. At H40, I read state.md at sweep start (saw H39 = expected H40), then spent ~5 minutes running profile reads + cron list. The orchestrator 30m heartbeat cron wrote H40 at 21:30 during that gap. When I patched with the H39-tail anchor, I overwrote the orchestrator's H40 row instead of renumbering to H41. **Correct procedure (mandatory):**
   - Run `grep -cE "^\|{1,2} H[0-9]+ \|" state.md` **right before constructing the patch**, not just at sweep start.
   - If a sibling row appeared since sweep start, **renumber YOUR sweep to the next available integer** (H41 in this case), re-anchor on the actual highest `H<N>` row's tail.
   - Default behavior on detected collision: **RENUMBER UP, NEVER OVERWRITE**. Even if your content is "better" than the sibling's, the sibling got there first and their row deserves to stay.
   - The H31 "renumber-upward worked example" (H31→H32 sibling→H33 your sweep) is the standard pattern — apply it consistently. H40 deviated and overwrote; H41+ must not.
   - Token cost of renumbering: zero. Token cost of overwriting: silent data loss of sibling's audit record.

   **Renumber-upward worked example (confirmed H33, 2026-06-26 15:00):** When a sibling already took the next integer slot (e.g., orchestrator wrote H32 while qa-agent hourly was about to write H32), do NOT overwrite their row. Instead: **renumber YOUR sweep to the next available integer (H33)**. This preserves the sibling's contribution AND keeps the sequence monotonic. Symptom of getting this wrong: two rows sharing the same H<N> ID, or a row missing entirely. Correct outcome: H31 → H32 (sibling/orchestrator) → H33 (your sweep), all present, all well-formed. The renumber is a meta-event worth logging in the new row's Notes column ("SIBLING-COLLISION DETECTED + RESOLVED — sibling subagent wrote H<N> at HH:MM between my dispatch and patch; renumbered to H<N+1> per H31 recipe"). Don't blame the sibling — they're filling a legitimate slot; your sweep is the additional signal. See `references/idle-sweep-evidence-h33.md` for the full H33 repro (orchestrator 30m heartbeat at 14:32 vs qa-agent hourly at 15:00).

8. **Recovery acceleration metric (learned H31, 2026-06-26):** When a profile is in PARTIAL-RECOVERY state per H29, compute `recovery_acceleration = slip_ratio[t-1] / slip_ratio[t]`. Codified thresholds for ops-manager H34 classification:

   | Acceleration | slip_ratio | Classification |
   |---|---|---|
   | >5.0 for 2+ sweeps | <0.5 | WITHIN TOLERANCE (healthy cadence) |
   | 1.0–5.0 sustained | 0.5–2.0 | RECOVERED-but-erratic |
   | 0.5–1.0 | 2.0–5.0 | PARTIAL-RECOVERY (masking pattern) |
   | <0.5 | >5.0 | PERSISTENT-with-masking |

   Track `recovery_acceleration` across consecutive sweeps. When `>1.0` sustained for 2+ sweeps AND `slip_ratio < 1.0`, transition PARTIAL-RECOVERY → WITHIN TOLERANCE.

   **PARTIAL-RECOVERY re-slip recipe (confirmed H33, 2026-06-26 15:00):** When `recovery_acceleration` flips back below 1.0 after a transient recovery (e.g., H28→H29 acceleration = 29.4, then H29→H33 acceleration = 0.17 due to slip_ratio regression 0.17 → 1.0), DO NOT immediately reclassify as PERSISTENT-with-masking. First compute the absolute slip_ratio: if still <2.0, it's PARTIAL-RECOVERY with mild re-slip (not PERSISTENT). If >5.0, escalate to PERSISTENT-with-masking. This is the difference between "the underlying cron is firing but with variable delay" (PARTIAL) and "the cron is fundamentally broken" (PERSISTENT). H33 case: ops-manager H34 PARTIAL-RECOVERY sustained across H22→H33 (10 sweeps), but with high variance — cron IS firing, just inconsistently. Real case trajectory: slip_ratio = 5.0 (H23) → 5.0 (H28) → 0.17 (H29) → 0.33 (H31) → 1.0 (H33). Pattern: never sustainedly <0.5, never sustainedly >5.0 → PARTIAL-RECOVERY with mild re-slip, NOT PERSISTENT, NOT yet WITHIN TOLERANCE. See `references/idle-sweep-evidence-h33.md` for the full slip_ratio timeline + forecast-miss documentation (H29 forecast "transition to WITHIN TOLERANCE if H32 shows improvement" was MISSED).

---

## 🆕 H46 Schedule vs Last-Run Refinement (H64 lesson, 2026-06-27 20:01)

**The H46 schedule-vs-nextrun rule was correct in principle ("trust `Schedule:` as ground truth for cadence, not `Next run:`"), but the practical formula when writing forecast rows was incomplete.** At H63, I wrote "research-lead Trend Scan next 2026-06-28T18:00" based on `Next run:` field. At H64 (1h later), the cron had ALREADY fired at 18:07:24 today — 24h ahead of my forecast.

**Refined H46 application recipe (H64 — Permanent):**

When writing a forecast for a cron in a sweep row:

1. **Read `Schedule:` first** → compute expected_cadence (e.g., `0 18 * * *` = every day at 18:00).
2. **Read `last_run:`** → compute `now - last_run`.
3. **Apply state classification (H29/H34/H50 recipes):**
   - `exit_status == "error"` → REAL FAULT
   - `|now - next_scheduled_fire| <= 60s` → PRE-FIRE (H50)
   - `now - last_run > expected_cadence × 1.5` → OVERDUE
   - `now - last_run < expected_cadence` → HEALTHY
4. **When writing the forecast row, NEVER use the `Next run:` field's date stamp alone.** Instead:
   - Compute `next_scheduled_fire` from `Schedule:` and `last_run:` (NOT from `Next run:` field).
   - For a recovering cron that just fired, the next scheduled fire is `last_run + expected_cadence` (e.g., today 18:07 + 24h = tomorrow 18:07, not `Next run:` which may show a different date).
   - For a cron that hasn't fired in 24h+ but is `Schedule: 0 18 * * *`, the next fire could be TODAY (not tomorrow) — verify with `now - last_run` math.
5. **Forecast caveat for recovering crons:** always add "or earlier if cron fires on today's tick" when last_run is older than `now - expected_cadence` AND the cron is in PARTIAL-RECOVERY state per H29.

**The H63→H64 missed-forecast case:**
- H63 read: `Last run: 2026-06-26T18:03:12`, `Schedule: 0 18 * * *`, `Next run: 2026-06-28T18:00`.
- I trusted `Next run:` and wrote "next 2026-06-28T18:00".
- Actual: cron fired at 2026-06-27T18:07:24 (today, 24h before my forecast).
- Root cause: `Next run:` field reflects the scheduler's next-expected-tick computation, but a cron that just recovered from a fault may fire on a different cadence than `Next run:` implies.

**Counter-detection:** if a sweep row contains a "next YYYY-MM-DD" forecast for a daily cron, and `now - last_run` is within `expected_cadence × 1.5`, the forecast is WRONG. The cron will fire on its next scheduled tick (e.g., today), not on `Next run:`'s date.

See `references/idle-sweep-evidence-h64.md` for full H64 sweep details.

---

**🆕 H70 awk-Tail Pitfall (2026-06-28 12:00) — NEW PERMANENT PATTERN**

**When constructing the H44 2-line anchor, NEVER use `awk '/^\| H<N-1> \|/' state.md | tail -1` to extract the prior row's tail.** `awk` returns the ENTIRE matching line (7,000+ chars for an evidence-rich sweep row), not a tail fragment. Using the full row as your anchor `old_string` causes:
1. Token waste (~7KB redundant context)
2. Collision risk with the new row's content (H19 pitfall class)
3. False "anchor not found" if the full row has minor whitespace differences

**Correct construction (use this for H44 anchor):**
```bash
grep -E '^\|{1,2} H<N-1> \|' state.md | tail -1 | tail -c 80
```

**Or in Python:**
```python
import re
content = open('state.md').read()
matches = re.findall(r'^\| H<N-1> \|.*$', content, re.MULTILINE)
tail = matches[-1][-80:] if matches else 'NOT FOUND'
```

**Rule:** for H44 2-line anchor, ALWAYS use `tail -c 40-100` to extract a true tail fragment. The H44 recipe assumes the prior row's tail is ≤100 chars; using `awk` violates this assumption silently.

**Detection recipe:** if `content.count(anchor)` is unexpectedly high OR your `old_string` parameter is >1KB, you used `awk`. Re-extract with `tail -c 80` and re-verify.

See `references/idle-sweep-evidence-h70.md` for the H70 case study + full recipe hold rate (9/9) + post-cadence-transition validation.

---

## 🆕 H38 Cron-Truth Recipe (2026-06-26 17:01) — PERMANENT RULE

**⚠️ THE MOST IMPORTANT METHODOLOGY CORRECTION IN QA-AGENT HISTORY.**

The H28 (code-reviewer), H29 (security-engineer), and H34 (operations-manager) "multi-profile cron fault pattern" tracked across 32+ sweeps (H1-H33) was a **PHANTOM PATTERN caused by using state.md file mtime as a proxy for cron health**. At H34, the root cause was identified; at H35, the corrected recipe was validated at full rigor.

### The Recipe (H38 — Permanent)

**BEFORE classifying ANY profile as a cron fault, run `hermes cron list` and check:**
1. `Last run` timestamp — when did the cron actually last fire?
2. `ok` / `error` status — exit_status is ground truth
3. Any `error:` annotation — what failed?

If `Last run` is recent AND status is `ok`, the profile is **HEALTHY** regardless of state.md mtime lag. Do NOT classify as fault based on mtime alone.

### Why mtime fails as a proxy

- state.md file is only rewritten when there's something meaningful to report
- A "0 findings, 0 pending, 9 idle" audit log entry is APPENDED only when there's something to report — clean cron runs don't always rewrite state.md
- Therefore mtime can lag actual cron execution by hours/days even when cron is firing on schedule
- The 5 profiles classified as H28/H29/H34 "phantom faults" all had cron `Last run` within 24h but mtime lag of 5h-10d

### H35 Full Validation (17 active crons checked)

| Status | Count | Action |
|---|---|---|
| ✅ ok | 16 | No action — healthy regardless of mtime |
| ❌ error | 1 (research-lead) | Real fault — escalate to Orchestrator |

**Rescinded classifications:**
- H28 code-reviewer "PERSISTENT 217h+" → actually HEALTHY (cron fires daily, mtime lag = clean cron run pattern)
- H29 security-engineer "WITHIN TOLERANCE 17h45m" → actually HEALTHY (cron fires daily, mtime lag = clean cron run pattern)
- H34 operations-manager "ACTIVE INSTANCE 5h+ brittleness" → actually HEALTHY (cron fires every 6h, mtime lag = audit content ground truth)

### Combined H38 + H36 detection pseudocode

```python
def is_cron_healthy(profile_name):
    # Step 1: Primary signal — `hermes cron list` ground truth
    cron_info = get_cron_last_run(profile_name)
    if cron_info.last_run_within_expected_cadence and cron_info.status == "ok":
        return True  # HEALTHY, regardless of mtime
    
    # Step 2: Secondary signal — state.md mtime (for profiles without `hermes cron list` entry)
    state_mtime = stat(state_md_path)
    if state_mtime_within_expected_cadence:
        return True  # HEALTHY
    
    # Step 3: Tertiary signal — file mtime vs audit body timestamp (H36-BODY check)
    audit_body_timestamp = parse_audit_log_latest_entry(state.md)
    if audit_body_timestamp > state_mtime:
        # H36-BODY: forward-projected entry, never actually written
        return True  # mtime is ground truth, body is templated
    
    return False  # Real fault — escalate
```

### Why this rule is permanent (not contextual)

- The H28/H29/H34 phantom pattern cost 32+ sweeps of wasted analysis (H8-H34)
- The pattern was reinforced by confirmation bias — each sweep "found" the same fault, making it seem real
- The false positive was a CLASSIC measurement artifact: using a proxy (mtime) for the real signal (cron last_run)
- Any future sweep that classifies a profile as a cron fault WITHOUT first running `hermes cron list` should be treated as suspect — repeat the H34 lesson

**🆕 H46 Schedule vs Next-run lesson (2026-06-27 03:00):** When reading `hermes cron list` output, **trust the `Schedule:` field as ground truth for cadence, NOT the `Next run:` timestamp's "weekly/daily" inference**. Real case at H46: a prior sweep row (H45) wrote "Wiki Memory Forget Daily next 2026-06-28T03:00" suggesting the cron wouldn't fire until the next day. But the `Schedule:` field was `0 3 * * *` (every day at 03:00) — and the H46 sweep caught the cron firing at 2026-06-27 03:00:46, 10s after the sweep started. The `Next run:` field shows the NEXT scheduled time, but if the sweep catches a cron in flight, the most recent `Last run:` is the truth. **Detection rule:** when writing sweep rows that reference future cron behavior, cross-check the `Schedule:` cron expression against the `Last run:` cadence. If `Last run` is within `Schedule` cadence, the cron is healthy REGARDLESS of how far away `Next run:` looks. Don't write "next 2026-06-28" if the cron's `Schedule:` is daily — the row text becomes stale immediately and confuses downstream readers.

See `references/idle-sweep-evidence-h35.md` for the H35 full validation sweep and the H36-BODY forward-projection confirmation.

---

**Pitfalls** (learned 2026-06-23, qa-agent H1-H4 sweeps):
- ❌ Reporting only "no pending" without evidence — looks like you skipped work.
- ❌ Searching `~/.hermes/**/*.pending*` recursively — floods with false positives.
- ❌ Re-running ops-manager's 6h audit from scratch — wastes tokens; ops-manager
  already aggregates this. Read its state.md instead.
- ❌ Reading maker profiles serially (one tool call per profile) — burns 7 round-trips.
  Batch all reads in one parallel block.
- ❌ Treating system-wide dormancy (>4h idle on all makers, >7 days) as a defect —
  it's a structural finding to flag, not a QA failure.

**Maker profile non-task sections (scope discipline, learned H28 2026-06-26):**
Some profiles maintain state.md sections that LOOK like pending tasks but are NOT
awaiting qa-agent verification. Future sweeps must NOT false-positive flag these:

- **engineering-lead — "Daily Code Health Check" section:** appended by
  engineering-lead's own daily health cron (independent of maker task queue).
  Contains git status, uncommitted file lists, etc. — operational telemetry, NOT
  pending QA work. Skip when scanning Active/Pending Tasks.
- **content-director — "Run History" section:** loop-goal auto-appends successful
  research runs here (e.g. "YouTube Trending Action Cam 2026-06-26 PASS 7.0").
  These are loop-goal self-runs with PASS verdicts already — NOT awaiting qa-agent
  re-verification. Skip when scanning for handoffs.
- **security-engineer — "Daily Scan Findings" section:** daily vulnerability scan
  output. Self-verdict (DO_NOT_SHIP / SHIP_OK / CLEAN) already applied by
  security-engineer itself. NOT pending qa-agent review.
- **operations-manager — "Routing Log" + "Audit Summary" sections:** routing
  telemetry + self-generated 6h audit. Already verified by ops-manager; qa-agent
  consumes these as cross-validation sources, not as targets.

**Detection rule:** When scanning a profile's state.md for pending QA work, only
treat as actionable if the entry appears in `## Active Tasks`, `## Pending Tasks`,
`## Blocked Tasks`, or `## Handoff History (to qa-agent)` sections AND has
Status="in progress"/"queued"/"blocked"/no-verdict. Other sections (Daily X
Check, Run History, Audit Summary, Routing Log, Recent Reviews, Recent Audits)
are PROFILE-OWNED and self-verdicted — qa-agent observes them as signals, not
as work to do.

**Why this matters:** Without this scope discipline, a sweep observing
content-director's Run History PASS 7.0 entry might falsely classify it as
"pending verification" and spawn unnecessary work. With this rule, those
entries are correctly identified as loop-goal self-runs and skipped.

**Companion recipe for anomalies within self-verdict entries:** see
`references/h68-anomaly-within-self-verdict-recipe.md` — adds a 3rd action
branch (observe / flag / don't act) for cases where H28's binary
"verify / don't verify" decision tree doesn't fit (data anomaly observed
in a profile-owned self-verdict that is NOT a security finding and NOT a
maker task handoff).

**Pitfalls** (extended H10-H12 sweeps, 2026-06-25):
- ❌ **Treating at-exactly-2h ops-manager audit as "still fresh"** — H34 regime
  boundary is strict: `<2h` = fresh, `>=2h` = stale. When audit timestamp is
  exactly 2h0m (e.g. H11, H12 with ops-manager 06:00 audit run at 08:00 / 20:00
  sweep), treat as **STALE** per strict interpretation → re-derive from primary
  reads. Both H11 and H12 applied this consistently; do not regress to a
  "soft boundary" reading that treats 2h as fresh.
- ❌ **Ignoring sync timestamps across profiles** — when 2+ maker profiles
  have identical `mtime` (e.g. engineering-lead + security-engineer both at
  2026-06-25 03:03 in H12), this is a **signal** — either shared cron trigger
  OR operations-manager fan-out dispatching a wake-up sweep. Note it in the
  sweep row's "No new faults" section. It is NOT a defect per se, but if it
  appears suddenly after long dormancy (>=7 days) it confirms the pipeline
  end-to-end (router → maker → QA) is alive.

**Pitfalls** (H15 sweep, 2026-06-25):
- ❌ **`patch` old_string collision on long Note cells** — when the previous
  row's Notes column ends mid-sentence with text like `...NOT YET** a new H29
  instanc...` (truncated by editor) and the next row's Notes column begins with
  near-identical text (`...NOT YET** a new H29 instance...`), `patch(mode='replace')`
  fails with "Found 2 matches for old_string" because the row-prefix tags make
  both prefixes unique BUT the body still appears twice in the file (once truncated
  mid-H<N-1>, once full in H<N>). The fix per H25 boundary pattern: anchor on the
  SECTION BOUNDARY (`\n\n## Verdict History` separator, which appears exactly once
  in the file) rather than the previous row's body — this gives the patcher a
  truly unique old_string. Alternative: use 3+ lines of surrounding context to
  force uniqueness. See `references/idle-sweep-evidence-h15.md` for full repro.

**Pitfalls** (H18 sweep, 2026-06-26) — boundary-token collision:
- ❌ **Section header text appearing inside row bodies** — the H15/H25 fix
  ("anchor on `\n\n## Verdict History`") BREAKS when a previous sweep row's
  Notes column contains the same boundary token inline (e.g. referencing
  `` `## Verdict History` `` in backticks while describing the recipe). The
  patcher finds N>1 matches and injects content inside the wrong row.
  Symptom: orphan row outside the table, table column-count corruption,
  section header duplicated. Fix: BEFORE patching, run `content.count(boundary)`;
  if >1, switch to multi-line context anchor (3+ lines of the previous row).
  See `references/idle-sweep-evidence-h18.md` for H18 case study + recovery recipe.

**Pitfalls** (H19 sweep, 2026-06-26) — mid-row truncation anchor pitfall:
- ❌ **`read_file` truncates rows >~3KB silently** — when the previous row is
  large (>3KB), `read_file(limit=2000)` returns a `[truncated]` marker in the
  wrapper, and the cell body shown to you ends mid-sentence. If you use the
  truncated tail as your patch `old_string`, the row's tail gets orphaned
  because the actual file content is longer than what you saw. ALWAYS re-read
  with `limit=2000` if the previous row exceeds ~3KB, OR anchor on the last
  100 chars of the Notes column. Distinct from H15/H18/H25; complementary rule.
  See `references/idle-sweep-evidence-h19.md` for full repro.

**Pitfalls** (H20 sweep, 2026-06-26) — audit-freshness vs file-mtime:
- ❌ **Conflating file `mtime` with audit-content freshness** — operations-manager's
  state.md file `mtime` gets updated whenever ANY tool reads/writes the file
  (including qa-agent sweeps themselves). At H20, ops-manager's mtime was
  1782393369 (2026-06-25 20:16:09, ~7h45m ago — recent by file mtime!) BUT
  its frontmatter `Goal:` still read `"6h routing audit (cron 2026-06-25 06:00)"`
  — meaning the actual audit content was ~22h old. Per H34, freshness is
  measured by the **audit content/timestamp** (frontmatter Goal, or the
  Audit Summary block), NOT the file's filesystem mtime. Always read the
  audit content to verify age — `stat -f %m` alone can give a misleadingly
  fresh reading when other sweeps have touched the file.

**Pitfalls** (H20 sweep, 2026-06-26) — scope discipline on pre-existing row corruption:
- ❌ **Repairing historical row corruption mid-sweep** — H19 row at H20 contained
  tail-duplication residue `|tern unbroken 9+ days)...` from a prior patch
  attempt's failed uniqueness check. Sweep correctly LEFT it as-is and noted
  it in the report. Repairing prior-sweep corruption is out of scope for a
  cron sweep — it's a separate cleanup task. Risk of mid-sweep repair: it
  complicates the patch anchor uniqueness math, may corrupt the row you're
  trying to fix, and produces no operational value (the system works fine
  with a slightly garbled row). Recommend logging the corruption in the
  new sweep row's "Notes" column + flagging it as a separate cleanup task
  for Orchestrator to triage.

**Pitfalls** (H22 sweep, 2026-06-26) — forecast-realization tracking:
- ❌ **Forgetting to check prior-sweep forecasts** — forecasts in earlier sweep
  rows (e.g., H20's "H21/H22 will breach 24h threshold") are auditable evidence.
  If the current sweep hits the predicted event, explicitly note it as
  REALIZED in the new row. If missed, note as MISSED. If hit at a different
  time, note as PARTIAL with the actual timing. This builds a forecast-accuracy
  metric over time. Without explicit realization check, forecasts decay into
  forgotten notes that no future sweep verifies.
- ❌ **Missing regression events** — when a previously-recovered profile
  (per H29 bidirectional tracking) re-faults, you must log it as a REGRESSION
  event. The H29 pattern's bidirectional tracking (added at H10) handles
  fault + recovery but not post-recovery regression. At H22, ops-manager
  recovered at H10 (2026-06-25 06:00) and re-faulted at H22 (2026-06-26 06:00)
  — a 24h recovery window. Track this gap as a brittleness metric.

- **Pitfalls** (H24 sweep, 2026-06-26) — frontmatter future-timestamp anomaly:
- ❌ **Trusting frontmatter `updated:` over audit content + file mtime** — at
  H24, ops-manager's frontmatter `updated: 2026-06-26T12:00:00+07:00` was 4h
  in the FUTURE relative to system time 08:00. If you read frontmatter first
  and stop there, you conclude "audit is in the future = cannot be FRESH" and
  escalate incorrectly. The H20 lesson ("measure freshness by content
  timestamp + file mtime, NOT frontmatter") only covered PAST staleness — not
  the case where frontmatter is ahead of system clock. Detection recipe:
  1. Compute `frontmatter_age = frontmatter.updated - system_time()`.
  2. If `frontmatter_age < 0` (negative — frontmatter is in the FUTURE),
     classify as **CLOCK_ANOMALY** — do NOT use frontmatter for freshness.
  3. Fall back to **file mtime** (`stat -f %m`) + **audit content body**
     (Routing Log line timestamp + Audit Summary block) to determine true
     content age.
  4. Cross-check audit body for self-consistency (e.g., "cron gap: Nh late"
     math should be consistent with the content's actual write time).
  5. Log the anomaly in the sweep row + note "frontmatter skipped for
     freshness, content used as ground truth." Do NOT trigger a fault — the
     audit content is consistent with ground truth; the frontmatter is just
     clock-skewed.
  Root cause hypothesis: cron daemon running with drifted system clock OR
  back-dated frontmatter on profile creation. Non-blocking — audit content
  is reliable. See `references/idle-sweep-evidence-h36.md` for full repro +
  H20-vs-H36 distinction table.

  **H36 → STRUCTURAL PATTERN (learned H25/H26, 2026-06-26):** After 3 consecutive
  detections (H24 1st, H25 2nd, H26 3rd) with consistent ~2-4h offset, H36 is no
  longer an edge case — it's a structural finding. Ops-manager's frontmatter
  `updated:` is consistently 2-4h ahead of actual system time. The pattern
  persists across the recovery cycle (H23 12:00 → H24 12:00 → H25 12:00 → H26
  12:00 — all in the future of their respective sweep times). Probable root
  cause: ops-manager's cron uses a different clock source for frontmatter
  vs audit content (likely cron run-time schedule, not actual write time).
  Mitigation: ALWAYS measure freshness via file mtime + audit content body,
  never via frontmatter alone — this rule is now a permanent fixture, not a
  contextual workaround.

  **H36 TRIGGER CONDITION CLARIFICATION (refined H28, 2026-06-26):** H36 anomaly
  is **clock-write-time dependent**, not constant. Specifically:
  - **FIRES** when frontmatter `updated:` time is significantly ahead of system
    time (>2h) AND audit content timestamp is older than frontmatter (i.e. the
    frontmatter was bumped but the body wasn't re-written).
  - **DOES NOT FIRE** when frontmatter matches system time within seconds
    (e.g. H28 12:00:25 sweep vs ops-manager frontmatter `updated: 2026-06-26T12:00:00`).
    In that case, content WAS just written, so frontmatter-vs-content age delta
    is ~0 — not anomalous.
  - **Re-check trigger:** After any fresh ops-manager audit write, expect H36 to
    re-fire at the NEXT sweep (when frontmatter stays put but system clock
    advances 1+ hour). H28 forecast: H36 will fire again at H29 (~13:00 sweep)
    unless ops-manager updates frontmatter between sweeps.
  - **Detection recipe (final):** Compute `frontmatter_age = frontmatter.updated - system_time()`.
    If `|frontmatter_age| < 60s` → not anomalous (just-written). If
    `frontmatter_age > 2h AND content_age > frontmatter_age` → H36 fires. If
    `frontmatter_age < 0 AND |frontmatter_age| > 2h AND content is older →
    H36 fires. Otherwise → ops-manager is FRESH or STALE per H34 normal regime.

  **H36 EXTENDS TO `goal:` FIELD (learned H29, 2026-06-26):** At H29, ops-manager's
  frontmatter `goal: 6h routing audit (cron 2026-06-26 18:00)` showed the same
  5h-future clock-write-time anomaly as `updated:`. The `goal:` field is a cron-label
  (planned next-run time), but ops-manager's cron writes it as if it were a write
  timestamp — same drift mechanism as `updated:`. **Generalized rule:** ANY
  frontmatter timestamp-bearing field can drift. When checking freshness, scan
  ALL timestamp fields (`updated:`, `goal:`, `last_run:`, etc.) before
  classifying. The mitigation rule is unchanged: file mtime + audit content body
  are ground truth; frontmatter alone is never sufficient. See
  `references/idle-sweep-evidence-h29.md` section 1 for detection recipe.

  **H29 FORECAST CALIBRATION (lessons from H28→H29):** H28 forecast said "H36 may
  NOT fire at H29 (1h gap < 2h threshold)". Actual: H36 DID fire at H29 because
  the gap was measured against the LATEST cron-label (18:00), not the previous
  frontmatter write (12:00). The 5h-ahead gap was 5× larger than forecast.
  **Updated forecast recipe:** when predicting H36 firing probability, measure
  the gap as `system_time - latest_cron_label` (the next-run time ops-manager
  stamps on every write), NOT `system_time - previous_frontmatter_write`. The
  delta is roughly constant at `time_until_next_6h_tick`, so H36 fires
  continuously between audit writes once the threshold is breached.

  **PARTIAL-RECOVERY → RECOVERY TRAJECTORY (learned H29, 2026-06-26):** The H28
  PARTIAL-RECOVERY sub-pattern (slip_ratio 5.0) was a snapshot. At H29, ops-manager
  showed rapid recovery: slip_ratio dropped from 5.0 → 1.0 → 0.17 over three
  sweeps (H23 → H28 → H29). This is a real recovery trajectory, not steady-state
  PARTIAL-RECOVERY. **New metric: `recovery_acceleration` = `slip_ratio[t-1] / slip_ratio[t]`**.
  If >1.0, profile is recovering. If <1.0, profile is re-slipping. When
  `recovery_acceleration > 1.0` sustained for 2+ sweeps AND `slip_ratio < 1.0`,
  transition classification from PARTIAL-RECOVERY → WITHIN TOLERANCE. See
  `references/idle-sweep-evidence-h29.md` section 2 for full trajectory table.

- **Pitfalls** (H34 sweep, 2026-06-26 16:00) — H36-BODY variant (wrong internal math inside audit body):
- ❌ **Trusting audit body entries with future timestamps + wrong math** — at H34, ops-manager's Routing Log contained an L38 entry with timestamp "2026-06-26 18:00" that claimed "cron gap: 6h late vs expected 6h cadence (2026-06-26 12:00 → 2026-06-26 18:00 = 1 tick missed)." But 12:00→18:00 = exactly 6h = expected cadence, NOT 1 tick missed. The math is WRONG. This is a H36-BODY variant: forward-projected entry (templated by cron script to look like a real audit) with internally inconsistent math. The file mtime was 12:00:54, confirming the 18:00 entry was never actually written.
  - **Detection recipe (extends H36):** Beyond checking `frontmatter.updated - system_time()` for the frontmatter variant, also scan audit body Routing Log entries for: (1) timestamp > file mtime, AND (2) "cron gap: Nh late" math that contradicts the actual gap (compute gap = `entry_timestamp - previous_entry_timestamp`; if it matches the expected cadence, the "1 tick missed" claim is wrong).
  - **Mitigation:** file mtime is still ground truth. The 12:00 audit is real, the 18:00 entry is a forward-projection/template echo. Log the anomaly, do NOT escalate, recommend Orchestrator investigate ops-manager cron script's "cron gap" math block.
  - **Why this matters:** the frontmatter H36 pattern is a templating issue at the profile-creation layer. The H36-BODY pattern is a templating issue at the cron-script layer. They have different root causes (frontmatter vs script) but the same shape (forward-dated content with self-inconsistency). Treating them as one class of anomaly misses the diagnostic value.
  - See `references/idle-sweep-evidence-h34.md` for full repro + classification pseudocode (combined H36 + H36-BODY detection function).

- **Pitfalls** (H26 sweep, 2026-06-26) — verification grep double-pipe prefix (H38 NEW):
- ❌ **Using single-pipe regex for post-patch row count** — at H26, first verification
  used `grep -c "^| H2[0-6] |"` which returned 0 because the H37 anchor's
  `new_string` template propagated the `|| # |` (double-pipe) header format, so
  H26 row was inserted as `|| H26 |` (double pipe) instead of `| H26 |` (single
  pipe). Both formats coexist in the file's history — original 4 rows (2026-06-17
  Verdict History section) use `|| # |...|| 1 |...` legacy layout, while later
  Recent Verdicts rows use `| # |...| H<N> |`. **Correct verification regex:**
  ```bash
  grep -cE "^\|{1,2} H[0-9]+ \|" state.md
  ```
  Or in Python:
  ```python
  verdict_rows = [l for l in content.split('\n') if re.match(r'^\|{1,2} H\d+ \|', l)]
  ```
  See `references/idle-sweep-evidence-h26.md` for H38 detection recipe + first
  occurrence + remediation.

**H15 Degradation Tracking** (2026-06-25, NEW metric): When ops-manager's audit
age crosses 12h but stays below 24h, classify as **STALE-but-not-yet-fault** and
track the trajectory. The H10→H15 trajectory was: FRESH(1h) → STALE(2h) →
STALE(2h) → STALE(15h) → STALE(16h) → STALE(17h). Slip rate: ~1h/qa-sweep past
H11. Will cross 24h threshold at H16 (estimated 2026-06-26 00:01 +07:00). When
it does, this becomes a NEW H29 multi-profile cron fault instance (4th after
code-reviewer H28, security-engineer H29, ops-manager H34). **Recommendation**:
flag `STALE-but-not-yet-fault` in sweep rows as actionable evidence — it gives
Orchestrator lead time to investigate before the threshold breach, rather than
reacting after. See `references/idle-sweep-evidence-h15.md` for trajectory table.

**H29 bidirectional tracking** (learned H10, 2026-06-25): The H29 multi-profile cron fault pattern is bidirectional — track BOTH fault detection AND recovery. When a previously-faulted profile (e.g., ops-manager between H8/H9 massively-stale and H10 fresh) recovers, explicitly note the recovery in the sweep row + reduce the running stuck-cron count. Recovery events break the streak length (3 stuck crons at H9 → 2 stuck crons at H10). Future sweeps should also flag "previously-recovered" profiles if they re-fault (regression).

**H29 regression tracking** (learned H22, 2026-06-26): When a previously-recovered profile re-faults, log:
- `profile_name`
- `recovered_at` (ISO timestamp from sweep row where recovery was logged)
- `re_faulted_at` (ISO timestamp of current sweep)
- `recovery_window_hours` = re_faulted_at - recovered_at
- `instance_count` for that profile (e.g., ops-manager: 1st at H8/H9, recovered H10, 2nd at H22)

This data feeds into a brittleness metric: shorter recovery windows indicate less robust recovery (e.g., ops-manager's 24h recovery window is short, suggesting the underlying cron fault was never actually fixed — only temporarily masked).

**H29 PARTIAL-RECOVERY sub-pattern (learned H28, 2026-06-26):** Distinct from
PERSISTENT (never recovers) and WITHIN TOLERANCE (recovers on cadence). A
profile in PARTIAL-RECOVERY state:
- Does self-recover each cycle (audit/task lands within the day)
- But always runs significantly late (e.g. 30h late on 6h cadence)
- Underlying cron fault is unfixed but masking behavior continues
- Classify as **ACTIVE H29 INSTANCE with partial-recovery behavior** (NOT
  PERSISTENT, NOT WITHIN TOLERANCE)

**Detection recipe:**
1. Profile was previously a H29 instance (logged in Multi-Profile Cron Fault Pattern table).
2. Current sweep finds the profile's cron DID fire since last sweep (recovery event).
3. But the gap between expected cadence (e.g. 6h) and actual time-since-last-write
   (e.g. 30h) is >2x the expected cadence.
4. → Log as PARTIAL-RECOVERY. Update brittleness metric:
   `slip_ratio = actual_gap / expected_cadence` (e.g. 30h / 6h = 5.0).
5. Forecast: if `slip_ratio > 5.0` consistently, classify as PERSISTENT-with-masking
   (worse than PERSISTENT because cron is firing but wrong, harder to diagnose).

**Real case (H28):** ops-manager was 4th H29 instance at H22 (24h breach).
Recovered partially at H23 (ran 30h-late audit at 12:00). Slipped again H24-H27.
At H28, recovered again with another 30h-late audit. slip_ratio = 30h / 6h = 5.0.
Brittleness metric updates: 24h (H10→H22) → 5h (H22 detection → H28 confirmation).
This is a PERSISTENT-with-masking pattern, not full PERSISTENT — cron DOES fire,
just always 5x late. Recommend investigation by Orchestrator: cron daemon may be
running but with a stuck scheduler, OR a wrapper script has a sleep/blocking bug
that delays write by ~24h.

**Why this matters:** Silent false-positive triages that should have been real handoffs = missed QA work = maker output shipped unverified. The reverse (real handoff dismissed as FP) is the worse failure mode. When in doubt, escalate to Orchestrator instead of auto-dismissing.

**Dormancy flag** (when all makers idle >4h for multiple consecutive sweeps):
Include in Suggestions (not Issues):
- "System idle observation: N specialist profiles dormant >X days. Consider
  dispatching a wake-up task to validate router → maker → QA pipeline."
- "Cron frequency sanity check: if 0-output pattern persists >7 days, consider
  reducing qa-agent cadence to 6h to save tokens."

**Dormancy recommendation split (learned H29, 2026-06-26):** The blanket
"reduce cadence at 7+ days" recommendation above misses the diagnosis. At 7-10+
day dormancy milestones, split the response based on pipeline-alive signals:

- **Pipeline ALIVE (≥3 of these firing):** ops-manager cron, engineering-lead
  daily health check, content-director loop-goal, qa-agent self → Recommendation:
  **DISPATCH WAKE-UP TASK** to ops-manager → a maker → qa-agent. Validates
  end-to-end routing. This is the higher-value action because it diagnoses
  whether the routing layer is broken vs just idle. Do NOT reduce qa-agent
  cadence yet — keeping hourly catches the wake-up event immediately.

- **Pipeline DEAD (≤2 of the above alive):** Recommendation: **REDUCE qa-agent
  cadence to 6h** AND escalate to Orchestrator that the entire pipeline may
  be stalled. 6h cadence still catches events with 6h latency.

- **Trigger milestone:** Apply the split at 7+ days, not 10. Earlier diagnosis
  is better than later.

- **Why this matters (H29 observation):** At 240h+ dormancy (exactly 10 days),
  ops-manager cron was firing (1h-late), engineering-lead daily health check
  ran at 09:05, content-director loop-goal produced research PASS at 08:04,
  qa-agent self was running hourly. Only the routing layer was dormant (no
  Pending/Active tasks in any profile). Blanket "reduce cadence" would have
  missed the real diagnosis: routing is silent because no tasks are queued,
  not because the pipeline is broken.

**Cadence**:
- Default: hourly (heartbeat).
- If 0 outputs for 7+ consecutive daily sweeps → reduce to 6h (apply the dormancy
  split above FIRST — only reduce cadence if pipeline signals are dead).
- If real outputs appear → reset to hourly until idle again.

**Token-economy read scope** (learned H22, 2026-06-26): For confirmed-dormant systems (>4 days idle across all makers, no pending outputs in 3+ consecutive sweeps), reduce primary profile reads from 8 to 4 (engineering-lead, content-director, research-lead, operations-manager — the routing pipeline core). Saves ~4 read_file calls per sweep. Re-expand to 8 reads if:
- A fault is detected (need fuller signal coverage)
- System shows signs of wake-up (sync-timestamp signal crosses profiles)
- A real handoff/pending file is found (Mode A switch)

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
- **References / templates / evidence files:**
  - `references/check-criteria.md` — chi tiết từng check category
  - `templates/verdict-format.yaml` — Template output verdict
  - `references/idle-sweep-evidence-h23.md` — **H23 evidence (2026-06-26 13:00)** — ops-manager H34 RECOVERY (partial — audit fresh, cron still slipping) + patcher-dedup sub-lesson (H18 boundary collision can produce duplicate lines that patcher silently removes) + cross-validation token-economy recipe (skip primary re-derivation when ops-manager audit is FRESH)
  - `references/idle-sweep-evidence-h22.md` — **H22 evidence (2026-06-26 06:00)** — 24h00m BREACH confirmed + ops-manager REGRESSION after H10 recovery + forecast-realization check + 4-read sweep token-economy recipe
  - `references/idle-sweep-evidence-h34.md` — Three-regime ops-manager audit freshness (fresh/stale/massively-stale) + ops-manager cron fault as 3rd H29 pattern instance
  - `references/idle-sweep-evidence-h18.md` — H18 boundary-token collision pitfall — section header text (`## Verdict History`) can appear inside inline row descriptions, breaking the H15/H25 "anchor on boundary" recipe. Use multi-line context anchor (3+ lines) when `content.count(boundary) > 1`. Companion to H15 (row-body collisions) and H25 (newline-count boundary); does NOT supersede them.
  - `references/idle-sweep-evidence-h19.md` — H19 mid-row truncation anchor pitfall — when `read_file` truncates long rows mid-sentence and the truncated text is used as the patch `old_string`, the row's tail gets orphaned. ALWAYS re-read with `limit=2000` if the previous row exceeds ~3KB, OR anchor on the last 100 chars of the Notes column. Distinct from H15/H18/H25; complementary rule.
  - `references/idle-sweep-evidence-h20.md` — H20 audit-freshness vs file-mtime pitfall — `stat -f %m` gives false fresh reading when another sweep touched the file. Always cross-check against frontmatter `updated:` field. Also: scope-discipline on pre-existing row corruption (leave-as-is vs mid-sweep repair). H21-H22 forecast: ops-manager 24h threshold breach → 4th H29 instance.
  - `references/idle-sweep-evidence-h35.md` — **H35 evidence (2026-06-26 17:01)** — H10 ops-manager cron RECOVERY — H29 pattern now bidirectional (fault + recovery detection) + H5 false-positive recipe extended to directory matches
  - `references/idle-sweep-evidence-h60.md` — **H60 evidence (2026-06-27 16:00)** — Two NEW failure modes + recovery recipes: (1) **Row-body self-reference anchor trap** — prior row body contains literal discussion of the anchor recipe; `content.count == 1` check passes but match is inside row body, not at file boundary. Detection recipe: verify anchor is at column 0 of line AND preceded by newline. Recovery: switch to row-start anchor (`| H<N> | <date>`) which has count=1 at TRUE line boundary. (2) **git-checkout data loss** — `git checkout state.md` silently destroys 1-24h of uncommitted sweep rows. NEVER use during active sweep. Use Python in-memory operations instead. Includes H60 anchor decision tree + Python verification template + recipe hold rate (18/18).
  - `references/idle-sweep-evidence-h64.md` — H64 evidence (2026-06-27 20:01): H46 schedule-vs-last-run lesson REINFORCED (H63 forecast "research-lead Trend Scan next 2026-06-28T18:00" was WRONG, cron actually fired 24h earlier). Refined H46 application recipe: compute `now - last_run` against `Schedule:` cadence FIRST; never write "next YYYY-MM-DD" without "or earlier if cron fires on today's tick" caveat. 17/17 crons verified healthy, 7/7 recipe hold rate.

---

## 🆕 H23 Cross-Validation Token-Economy Recipe (2026-06-26)

When **ops-manager audit is FRESH (<2h old) AND ops-manager's Profile Activity Matrix shows 0 ACTIVE AND no Profile has changed Goal/Active Tasks since qa-agent's last sweep**, qa-agent can **skip primary re-derivation** and cite ops-manager's audit as ground truth.

**Token savings:** ~6 read_file calls per sweep avoided (no need to re-read maker profiles when ops-manager audit is FRESH and confirms 0 pending/0 stuck).

**Spot-check rule:** Every 6th sweep, do at least 1-2 primary reads even when ops-manager is FRESH — prevents silent error propagation if ops-manager's audit is wrong.

**Caveat:** This is a CRITICAL trust assumption. If ops-manager audit is wrong or stale, qa-agent propagating the error is a silent failure mode. Mitigation: spot-check + regime boundary discipline.

---

## 🆕 H23 Patcher Dedup Sub-Lesson (2026-06-26)

When the H18 boundary-token collision fires (boundary string appears 2+ times in file), the patcher may successfully apply the patch but **silently dedupe duplicate lines** that were created by the collision's ambiguity.

**Implication for row-count verification:**
- Pre-patch row count may INCLUDE the orphan duplicate that the collision produced
- Post-patch row count is the CORRECT count (patcher cleaned up)
- Do NOT panic if pre-patch count > expected — verify AFTER patch, not before

**Detection:** If `content.count(boundary_token) > 1`, ALWAYS use multi-line context anchor per H18. After patch, verify row count = expected (pre-patch count minus any duplicates the patcher removed).



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

## 🆕 H37 Phantom-Cron-Claim Recipe (2026-06-26 19:01) — H38 EXTENSION

**The H38 recipe (run `hermes cron list` to verify cron health) is necessary but NOT sufficient.** A prior audit can claim "profile X cron has error Y" based on state.md evidence, and that claim gets propagated through multiple sweeps even if the cron was never registered in the first place.

**H37 case study (real):**
- H34/H35/H36 audits (including my own H36 row) all attributed a "Research Lead Trend Scan" cron to research-lead with `last_run: 2026-06-25 18:01:46` and `error: RuntimeError: Connection error + platform 'telegram' not configured/enabled`.
- H37 ran `hermes cron list` and found **NO research-lead cron registered at all** — only 11 active jobs (Daily Backup, Autoresearch, X Research, Session Review, Wiki Health, Wiki Memory Forget, TikTok 5-Channel, Orchestrator Heartbeat/Daily Briefing/Nightly Reflection/Weekly Cleanup). None owned by research-lead.
- The "Connection error" attribution was tracking a **phantom cron** — either it was never registered, was removed between H36 and H37, or was renamed.
- research-lead activity is **loop-goal-driven** (per its state.md Run History section), not `hermes cron list`-driven. The 22:30 PASS 9.0 run was a loop-goal auto-run, not a `hermes cron list` cron tick.

**The H37 refinement to H38:**

**Before accepting ANY prior audit's fault claim, verify the cron actually exists in `hermes cron list`.** The H38 recipe says "before classifying as a fault, check `hermes cron list`" — H37 extends this to: **"before ACCEPTING an inherited fault claim, check that the cron in the claim matches a real `hermes cron list` entry."**

**Why this matters:**
- Inherited phantom-fault claims get reinforced by each sweep (each row says "research-lead is overdue 24h" because the prior row said so)
- The H38 validation only fires when you're about to classify a NEW fault — it does NOT automatically re-validate inherited claims
- A 4-sweep propagation window (H34 → H35 → H36 → H37) of a phantom claim is enough to distort the entire multi-profile fault pattern narrative

**Detection recipe:**
1. When a prior sweep row contains a fault claim attributed to a specific cron, parse the cron name.
2. Run `hermes cron list` and grep for that cron name (case-insensitive substring match).
3. If the cron is NOT in the registry → the claim is a PHANTOM. Rescind the classification immediately.
4. If the cron IS in the registry → apply normal H38 validation (check `Last run` + `ok`/`error` status).
5. Log the phantom detection in the new sweep row's "Notes" column with the exact cron name + the sweep where the claim first appeared.

**Provenance recipe (NEW):** When logging a fault claim, always cite the SOURCE — both the sweep row where the claim originated AND the `hermes cron list` entry it maps to. Claims without `hermes cron list` provenance are NOT citable as faults. This is a hard rule, not a soft one.

```python
# Detection pseudocode
def is_cron_claim_valid(claim, cron_list_output):
    # Extract cron name from claim text (e.g., "Research Lead Trend Scan")
    claimed_cron_name = extract_cron_name(claim)
    
    # Check if it exists in `hermes cron list`
    if claimed_cron_name not in cron_list_output:
        return False  # PHANTOM — cron never registered
    
    # If it exists, check exit_status
    cron_entry = find_cron_entry(cron_list_output, claimed_cron_name)
    if cron_entry.status == "ok" and cron_entry.last_run_within_cadence:
        return True  # Real cron, real fault
    return False  # Real cron, but not actually faulting
```

**Real H37 outcome:**
- H36 forecast: "research-lead fault is officially overdue (24h breach) — Connection error persists"
- H37 actual: phantom claim, **RESCIND H36 "OVERDUE 24h breach" classification**
- research-lead loop-goal DID complete a run at 22:30 (PASS 9.0) — this is real work, but it's NOT a `hermes cron list` cron
- The H28/H29/H34 "multi-profile cron fault pattern" was already FULLY RESCINDED at H35; H37 adds research-lead's H34-classification to the rescinded list

**Why this rule is permanent:**
- Multi-sweep propagation of phantom claims is the SAME class of error as the original mtime-as-proxy problem: using a proxy (audit log text) for the real signal (cron registry)
- The 4-sweep propagation window (H34→H37) is a structural finding — even with H38 active, inherited claims can persist if not explicitly re-validated
- Future sweeps must apply BOTH H38 (validate before classifying) AND H37 (validate before accepting inherited claims)

See `references/idle-sweep-evidence-h57.md` for the H57 sweep + phantom-cron-claim recipe.)

---

## 🆕 H58 Anchor-When-Prior-Row-Contains-Legacy-Separator (2026-06-27 14:01)

**Permanent pattern for when Recent Verdicts row is inserted above legacy `## Verdict History` section AND absorbs the legacy `|------|---------|...|-------|` separator into its tail.** H44 2-line anchor and H42 unique-phrase anchor both fail (`content.count = 0`) because `\n## Verdict History` is no longer the immediate boundary — `\n| 1 | <legacy row>` is. Fix: **H58 extended anchor = prior_row[-60:] + `\n` + first 22 chars of legacy row**. Pre-flight detection: `prior_row.endswith('|------|---------|------|-------|---------|-------|')`. Verified `content.count = 1`, first-try patch. See `references/idle-sweep-evidence-h58.md` for full decision tree, pre-flight Python check, and H44/H42/H56/H57 collision history.

---

## 🆕 H39 Transient-Cron-Registry Refinement (2026-06-26 21:01)

**The H37 phantom-cron recipe is correct but its verdict can be wrong.** A cron that is MISSING from `hermes cron list` at sweep N can become REGISTERED at sweep N+1 — and vice versa. The H37 recipe said: "if not in `hermes cron list`, qa-agent cannot verify via cron-truth → RESCIND fault claim permanently." **This was too strong.** Real case (H37→H38/H39):

- H37 (19:01): `Research Lead Trend Scan` cron MISSING from `hermes cron list` → rescinded the research-lead fault claim and attributed all activity to loop-goal-driven work.
- H38 (20:01): same cron STILL MISSING → H38 confirmed H37's rescission held.
- **H39 (21:01): cron is NOW REGISTERED** in `hermes cron list`, last_run 2026-06-26 18:03:12 ✅ ok. The cron was ADDED to the registry between H37 (19:01) and H39 (21:01) — either Orchestrator re-registered it, or H37 caught a transient state during a re-registration event.

**Why H37 was wrong (mechanically):** when a sweep observes a cron is missing from `hermes cron list`, there are three real possibilities:
1. The cron was never registered (true phantom — H37's default assumption)
2. The cron was REMOVED from the registry recently (legitimate deprecation)
3. **The cron is in the process of being REGISTERED** (transient state during re-registration event)

H37's recipe treated only #1 as the operative explanation. In reality, #2 and #3 happen — and the only way to distinguish them is to **verify at the next sweep** rather than declare the rescission permanent.

**Refined H37 recipe (corrected at H39):**

When `hermes cron list` shows a previously-known cron is MISSING:
- **DO NOT immediately declare "phantom claim — permanent rescission."**
- Instead: log as **"DEFERRED — cron missing from registry at this sweep. Verifying at next sweep."**
- If the cron reappears at next sweep → rescind H37's "phantom" claim and restore the cron as REAL + HEALTHY (or whatever its actual status is).
- If the cron is still missing 2+ consecutive sweeps → THEN classify as truly absent / deprecated / phantom.
- **Track `transient_absence_count`** metric: number of consecutive sweeps where the cron was missing from `hermes cron list`. When count = 1, log "transient state possible." When count >= 2, log "likely genuinely absent."

**Updated provenance recipe (extends H37):**

```python
def classify_cron_absence(cron_name, current_sweep, prior_sweeps):
    absent_count = 1  # current sweep
    for prior in prior_sweeps:
        if cron_name not in prior.cron_list_output:
            absent_count += 1
        else:
            break  # cron was present in some prior sweep
    
    if absent_count == 1:
        return "TRANSIENT_ABSENCE — verify at next sweep"
    elif absent_count < 3:
        return "LIKELY_ABSENT — track for 1 more sweep"
    else:
        return "CONFIRMED_ABSENT — phantom or deprecated, rescind inherited fault claim"
```

**Real H39 outcome:**
- H37 phantom-cron claim **FULLY RESCINDED** (re-evaluated at H38/H39)
- H38/H39: `Research Lead Trend Scan` is REAL, registered, last_run 2026-06-26 18:03:12 ✅ ok, daily cadence healthy
- The "research-lead reactivated via loop-goal" narrative at H37 was a MISDIAGNOSIS — it was actually cron re-registration that brought research-lead back online
- **Lesson:** when qa-agent's narrative keeps shifting between sweeps (phantom → loop-goal → cron), the truth is probably simpler than any single narrative suggested. Track evidence across multiple sweeps before committing to an explanation.

**Why this rule is permanent:**
- H37's recipe was used to make a definitive claim ("research-lead cron never existed") that turned out to be wrong within 2 hours
- The original H37 verification (running `hermes cron list` and not finding the cron) was CORRECT — but the inference drawn from that observation was wrong
- This is a CLASS of error: "correct observation, wrong generalization" — the system literally doesn't have the cron AT THIS INSTANT, but "doesn't have" ≠ "never had"
- Any future sweep that observes a missing cron should track absence across consecutive sweeps before declaring phantom status

---

## 🆕 H39 Double-Pipe Row Prefix Drift (2026-06-26 21:01)

**Persistent file corruption finding:** Past sweeps (H26, H34, H37) wrote rows with the WRONG pipe prefix format `|| H<N> |` (double pipe) instead of `| H<N> |` (single pipe). This drift is now permanent in state.md — those 3 rows cannot be retroactively fixed without breaking the file's continuity.

**Why it happened:**
- The Recent Verdicts table header at the top of the file uses single pipe: `| # | Time | Verdict | ...`
- The legacy `## Verdict History` section header (lines 75+) uses double pipe: `|| # | Time | Subject | Task | Score | Verdict | Notes |`
- When patches anchored between sections, sometimes the new row picked up the double-pipe prefix from the wrong table style

**Mandatory verification regex (corrected at H26, confirmed at H39):**

```bash
# CORRECT — catches both formats
grep -cE "^\|{1,2} H[0-9]+ \|" state.md

# WRONG — misses double-pipe rows
grep -cE "^\| H[0-9]+ \|" state.md
```

**Lesson for future sweeps:** NEW rows in Recent Verdicts MUST use single pipe `| H<N> |`. Always verify the prefix of the row immediately above the boundary before constructing the patch — if it's double pipe, use single pipe in the new row to maintain consistency with the dominant format.

**Cosmetic impact:** zero — both formats render fine in markdown. Operational impact: only affects the post-patch verification count. No data loss.

---

## 🆕 H42 Unique Phrase Anchor Recipe (2026-06-26 23:01) — NEW PERMANENT PATTERN

**The H15/H18/H25 boundary-anchor recipes all degrade when the section header token (`## Verdict History`) appears ≥10 times in the file.** At H42, the boundary token appeared **23 times** in `~/.hermes/profiles/qa-agent/state.md` (1 actual section header + 22 inline references across prior row bodies). The multi-line context anchor recipe (3-4 lines) gets unwieldy at this scale. H42 introduces a new anchor pattern that scales better.

### The Recipe (H42 — Permanent)

**Use a UNIQUE PHRASE from the END of the previous row's tail + the literal section header from the same line.**

```python
# Step 1: Pick a unique phrase from the last 60-100 chars of the prior row's tail
last_60_chars_of_H41 = "...0 conflicts, 0 escalations — system HEALTHY.**"
boundary_token = "## Verdict History"

# Step 2: Construct the anchor phrase
phrase = last_60_chars_of_H41 + "\n" + boundary_token

# Step 3: VERIFY UNIQUENESS before patching
content = open(state_md_path).read()
assert content.count(phrase) == 1, f"Anchor not unique: found {content.count(phrase)} matches"

# Step 4: Construct patch
ANCHOR_OLD = phrase
ANCHOR_NEW = last_60_chars_of_H41 + "\n" + H42_ROW + "\n" + boundary_token

patch(mode='replace', path=state_md_path, old_string=ANCHOR_OLD, new_string=ANCHOR_NEW)
```

### Why this works (two sources of uniqueness)

1. **Prior row's tail text is unique to that row** — H41's conclusion ("0 conflicts, 0 escalations — system HEALTHY") wouldn't appear in any other row's body. Every sweep's conclusion is different.
2. **Boundary token appears once AFTER H41** — the `\n## Verdict History` sequence appears at the boundary immediately following H41, but at most once (other occurrences are inside row bodies, not at line boundaries).

Combined, the phrase has sequence-level uniqueness that survives even when boundary token count is high.

### Anchor pattern evolution

| Pattern | Sweep | Boundary count | Multi-line? | Worked? |
|---|---|---|---|---|
| `\n\n## Verdict History` (H15) | H15-H17 | 1 | No | Yes |
| 4-line context anchor (H25/H26) | H23-H37 | 2-15 | Yes (3+ lines) | Yes |
| **Unique phrase anchor (H42)** | **H42+** | **10+** | **No (60-char tail + boundary)** | **Yes** |

### When to use H42 unique phrase anchor

Use when:
- Boundary token (`## Verdict History` or similar) appears ≥10 times in file
- Prior row's tail is well-known (you've just read it)
- Multi-line context anchors are getting unwieldy (4+ lines of context)

Don't use when:
- Boundary token count is 1-2 (use simple H15 recipe)
- Prior row was truncated by `read_file` limit (anchor on wrong tail — see H19)
- You haven't read the prior row's tail recently

**H42 result**

- Pre-patch: `content.count(phrase) == 1` (verified)
- Patch applied cleanly on first attempt (no retries)
- Post-patch: row count went 41 → 42 (correct)
- H42 row appears at correct position between H41 and `## Verdict History` header

**🆕 H57 GENERALIZATION (2026-06-27):** The H42 recipe's boundary token is NOT specific to `## Verdict History` — it works with ANY literal line separator that appears exactly once at the boundary position. At H56/H57, the boundary was `\n|---|` (not `## Verdict History`) because the file had been restructured by H53/H54 inserts. Recipe extended: try candidates `["\n## Verdict History", "\n|---|", "\n---\n"]` in order; use the first with `content.count(phrase) == 1`. See `references/idle-sweep-evidence-h57.md` for the generalized recipe + decision tree.

See `references/idle-sweep-evidence-h42.md` for full sweep details.

---

## 🆕 H44 Unique-Phrase-Anchor Refinement (2026-06-27 00:00) — TRUNCATION-SAFE FALLBACK

**The H42 unique-phrase-anchor recipe (last 60-100 chars of prior row tail + literal `## Verdict History` boundary) silently breaks when the prior row is truncated by `read_file`.** At H43, the prior row (H42) was so long that `read_file(limit=2000)` returned a `[truncated]` marker in the wrapper, and the cell body shown to me ended with "H42 continues the idle pattern but with research-lead reactivation providing first real signal since H1. Sweep ready for next event." — a TRUNCATED mid-sentence ending, not the row's true tail.

**Why this matters:**
- The H42 recipe assumes you know the prior row's true tail text
- If your read of the prior row was truncated, anchoring on the truncated tail produces a phrase that does not exist in the file → `patch` fails with "Could not find a match for old_string"
- The "correct" recipe (H42's step 3: `content.count(phrase) == 1`) catches this — `count == 0` means your anchor is wrong
- BUT the failure mode is still wasted work: re-read with terminal/awk to find the true tail, then re-anchor

**The H44 refinement (truncation-safe fallback):**

When the H42 unique-phrase-anchor recipe fails (pre-patch check `content.count(phrase) == 0`):
1. **DO NOT** try to extend the anchor with more tail chars — the tail you have IS the truncated tail, more chars won't help
2. **DO** fall back to a 2-line literal anchor: pick a SHORT known-good string from the very END of the row (e.g., the last 30-40 chars of the most recent `awk NR==<row_line>` output via terminal, or the last sentence of any cell that is clearly near the row's end), then `\n` + `## Verdict History`
3. The 2-line anchor works because `\n## Verdict History` as a sequence appears EXACTLY ONCE in the file (right after the most recent row, before any other content)
4. If even the 2-line anchor fails (e.g., another sweep wrote a new row between your read and your patch — sibling collision), renumber UP per H31/H40 recipes

**H43 actual recipe used (truncation-safe fallback):**
```python
# After read_file truncation, ran terminal to find true row tail:
#   $ awk 'NR==78' state.md | tail -c 250
#   → "...nothing to verify).** Mode B no-pending sweep successful; H42 continues the idle pattern but with research-lead reactivation providing first real signal since H1. Sweep ready for next event."

# Used SIMPLEST possible 2-line anchor (the absolute last unique chars + boundary):
ANCHOR_OLD = "Sweep ready for next event.\n## Verdict History"
# This worked first try because:
# 1. "Sweep ready for next event." appears in exactly one cell (H42's Notes column ending)
# 2. The literal "\n## Verdict History" immediately after it is a one-of-one boundary
```

**H44 unified decision tree (canonical pre-patch anchor selection):**

```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → choose anchor:
   a. If boundary token (`## Verdict History`) count == 1 → use H15 simple boundary
   b. If boundary token count 2-9 → use H25 4-line context anchor
   c. **If boundary token count ≥10 AND prior row's true tail is ≤40 chars AND known via grep/awk** → use H44 2-line fallback (PREFERRED — simpler than H42, works in all conditions including truncation)
   d. If boundary token count ≥10 AND prior row's tail is >40 chars or ambiguous → use H42 unique phrase anchor (fallback for long/ambiguous tails)
   e. **If boundary token count ≥10 AND prior row's tail is TRUNCATED in your read** → use H44 2-line fallback (only choice that works)
4. Always verify with `content.count(ANCHOR_OLD) == 1` before patching
```

**H44 anchor preference validated at H44 (2026-06-27 01:00, see references/idle-sweep-evidence-h44-validation.md):** The 2-line fallback ("last short unique tail + boundary") succeeded on first attempt when applied to a 19-boundary-ref file, with no truncation in the prior row. The H42 unique-phrase anchor (60-char tail) is now strictly the fallback for longer/ambiguous tails; H44 2-line is the PREFERRED choice whenever applicable.

**H47 anchor preference validation (2026-06-27 04:00, see references/idle-sweep-evidence-h47.md):** H47 sweep confirmed H44 2-line anchor as the gold standard for sweeps where prior row tail is known and ≤40 chars. 3 consecutive sweeps (H44, H45, H47) all used H44 2-line anchor successfully with first-try patch, no retries, no row corruption. H42 60-char unique phrase anchor was never needed in H44-H47 window. **Default rule: use H44 2-line anchor for all sweeps where prior row tail is known and ≤40 chars; fall back to H42 only if H44 anchor uniqueness check fails (content.count > 1).**

**🆕 H52 bold-marker + trailing-pipe variant (validated H62+H63, 2026-06-27):** When prior row's tail ends with `**Sweep ready for next event.** |` (or similar `**bold-marker** |` structure), anchor as `**closing phrase.** |\n## Verdict History` — count=1. Naive anchor stripping the bold markers fails (count=0). The `**...** |` sequence is part of the row structure, not strippable. See `references/idle-sweep-h60-plus-protocol.md` for the full H60+ sweep protocol.

**Why this rule is permanent:**
- The H42 recipe's pre-condition (knowing the true tail) is not always met
- `read_file(limit=2000)` truncates row bodies >~3KB silently — confirmed at H43 (H42 row was ~7KB, read_file output was truncated mid-sentence)
- Without H44, future sweeps at H44+ will hit the same "anchor not found" failure when prior rows are large
- The 2-line fallback is strictly SIMPLER than H42 (no 60-char-tail construction) AND works in more conditions (truncation-safe)

**Real H43 outcome:**
- First patch attempt with H42 recipe (constructed from truncated tail) → **FAILED**: "Could not find a match for old_string in the file"
- Recovered by running `awk NR==78` via terminal to find the true row tail
- Discovered the truncation cost me precision; fell back to H44 2-line anchor (`Sweep ready for next event.\n## Verdict History`)
- Patch succeeded on first attempt with the simpler anchor

**H44 also documents a SECOND signal: cadencetrigger boilerplate has become noise at 43+ idle sweeps.** When the same "CADENCE TRIGGER PERSISTS — N consecutive idle sweeps, recommend reducing qa-agent cron from hourly to 6h" line has appeared in 43 consecutive rows, it is no longer actionable signal — it is background noise. The recommendation needs to evolve:
- Sweeps H1-H7: "recommendation to reduce qa-agent cron from hourly to 6h is now strongly justified"
- Sweeps H8-H20: same line, escalating "URGENT" tags
- Sweeps H21-H33: still "URGENT" / "CRITICAL"
- Sweeps H34-H42: "URGENT" / "PERSISTS" / "deprioritized"
- **Sweep H43+**: **REPLACE** the boilerplate with one of:
  - "CADENCE TRIGGER ALREADY KNOWN — orchestrator has been told 43 times. If not actioned, this row's signal is zero. Do not re-state in subsequent rows."
  - OR escalate with a SPECIFIC new evidence (e.g., token-cost projection: "43 sweeps × ~3000 tokens/sweep = ~129K tokens spent on idle sweeps this dormancy window; if not actioned by H50, recommend auto-suspending qa-agent cron entirely")

The lesson: **when a recommendation has been made 5+ times without action, the recommendation is no longer signal — it is overhead**. Replace it with either: (a) explicit "noted, no action needed" + new signal focus, or (b) escalation with new evidence. Repeating the same recommendation verbatim dilutes the new evidence in each row.

- `references/idle-sweep-evidence-h44.md` — H43 sweep + H44 2-line anchor recipe.

---

**🆕 H51 Coder-No-Cron Health-Default Rule (2026-06-27 08:00) — PERMANENT**

**Profiles without a registered cron in `hermes cron list` are HEALTHY BY DEFAULT, regardless of state.md mtime lag.** At H51, the `coder` profile had a 252h state.md mtime lag (last write 2026-06-16 19:54) but no cron registered. A naive application of the H38 cron-truth recipe would either (a) flag coder as "OVERDUE 252h" (using state.md mtime as proxy) or (b) skip coder entirely (no cron to check). Both are wrong.

**Correct application of H38 to coder:**
1. Check `hermes cron list` for coder-owned cron → NOT FOUND
2. Conclusion: coder is on-demand / event-driven, NOT cron-driven
3. State.md mtime lag of 252h = NORMAL, because coder is not a scheduled job
4. coder is HEALTHY (no cron to fail) regardless of state.md mtime

**Detection rule:**
```python
def is_profile_healthy(profile_name, cron_list, state_mtime, system_time):
    # Step 1: Does the profile own a cron?
    owned_crons = [c for c in cron_list if profile_name.lower() in c.name.lower()]
    if not owned_crons:
        return True  # No cron = no cron to fail = healthy
    
    # Step 2: Profile has crons — apply H38 cron-truth check
    for cron in owned_crons:
        if cron.exit_status == "error" or cron.is_overdue:
            return False  # Real fault
    return True  # All owned crons healthy
```

**Implication for sweep row reporting:** When listing per-profile status, distinguish between "cron-driven profiles" (qa-agent, ops-manager, security-engineer, memory-curator, research-lead, content-director via loop-goal) and "on-demand profiles" (coder, engineering-lead, code-reviewer). On-demand profiles should be classified by their last ACTUAL work output, not by state.md mtime.

**Why this matters:** without this rule, a future sweep at H52+ could falsely classify coder as a fault (252h mtime lag looks alarming) and waste tokens investigating a phantom. The H37 phantom-cron lesson applies: just as missing-cron claims need verification, missing-cron profiles need correct classification.

---

**🆕 H51 Cadence-Decay Escalation Timeline (2026-06-27 08:00) — REFINES H44**

**H44 cadence-decay option (a)** said: "replace boilerplate URGENT recommendation with 'noted, no action needed' when recommendation has been made 5+ times without action." H44 suggested H60 as a tentative auto-suspend threshold. H51 sharpens the timeline:

| Sweep | Action | Token cost (est.) |
|---|---|---|
| H1-H7 | Initial recommendation | ~21K |
| H8-H20 | Escalating "URGENT" tags | ~39K |
| H21-H43 | PERSISTS/CRITICAL | ~69K |
| H44-H50 | H44 option (a): "noted, no action needed" | ~21K |
| H51-H54 | Refrain from re-stating; focus on recipe validation | ~12K |
| **H55** | **FINAL WARNING with explicit "next opportunity is H60"** | ~3K |
| H56-H59 | Quiet observation; track H36, H34, H50 recipe health | ~12K |
| **H60** | **AUTO-SUSPEND qa-agent hourly gate cron** if still no action | ~3K |

**Total token cost cap:** ~180K tokens before auto-suspend. At H60 the cron is removed and qa-agent re-runs only when explicitly triggered by orchestrator dispatch (heartbeat, mode-A verification, or wake-up task).

**Detection rule for auto-suspend:**
```python
if sweep_index == 60 and pending_outputs == 0 and all_recipes_holding:
    # All 3 conditions met: 60+ idle sweeps, no pending work, recipes stable
    # Recommend auto-suspend in H60 row
    auto_suspend_recommendation = True
```

**Why H55/H60 and not sooner:** The 5-sweep gap (H55→H60) gives the orchestrator time to see the final warning and act BEFORE the auto-suspend triggers. This is a graceful degradation, not an abrupt stop. If the orchestrator acts at H56-H59 (changes qa-agent cron schedule), the H60 auto-suspend is bypassed.

**Real H51 forecast:** 51 sweeps × ~3000 tokens = ~153K tokens spent on idle sweeps. H55 final warning → H60 auto-suspend. The orchestrator has 9 more sweeps (H52-H60) to act.

---

**🆕 H50 Pre-Fire Inflection Window Recipe (2026-06-26 17:01) — NEW PERMANENT PATTERN

**The H38/H49 cron-truth sweep assumes each cron is in one of two states: "fired on time" or "overdue." There's a THIRD state that wasn't previously named: PRE-FIRE (scheduled to fire at HH:MM but sweep lands before execution).** At H50 (07:00:30), two crons were due to fire at 07:00 and 07:30 respectively — at sweep time the first had NOT yet fired (last_run still yesterday 07:08:26). Logging this as "OVERDUE" would have been wrong — the cron was scheduled for HH:MM today and the sweep just landed in the pre-fire window.

**Detection recipe (H50 — Permanent):**

When `hermes cron list` shows a cron whose `Schedule:` cron expression's next-fire-time is ≤60s away from the current sweep time:
1. **DO NOT** classify as OVERDUE — the cron is in PRE-FIRE window.
2. **DO** note in the sweep row: "Cron X scheduled to fire at HH:MM today (Schedule: `Y M * * *`), at sweep time HH:MM:SS it has NOT yet fired. Will realize at next sweep."
3. **DO** forecast to next sweep: "At H(N+1), expect Cron X to have fired by then."
4. The pre-fire window is **the 60s window BEFORE the scheduled fire time** — crons rarely fire exactly at HH:MM:00 (typical variance: 1-10s delay), so a sweep at HH:MM:30 with last_run still showing the prior cycle is NORMAL, not overdue.

**Forecast realization categories (extends H22):**

| Category | Definition | Sweep action |
|---|---|---|
| REALIZED | Predicted event occurred by next sweep | Confirm in row, no escalation |
| MISSED | Predicted event did not occur at all | Escalate if persistent (3+ sweeps) |
| PARTIAL | Event occurred at different time than predicted | Note actual timing, adjust forecast model |
| **PRE-FIRE (NEW H50)** | **Sweep landed before predicted event fired; cron scheduled for HH:MM but last_run still shows prior day** | **Capture pre-fire state, forecast to next sweep, do NOT escalate** |

**H50 case study (real):**
- H49 forecast: "Hermes Autoresearch Nightly + Hermes Agent X Research Daily crons both scheduled to fire at 07:00 and 07:30 — first major activity since H22."
- H50 sweep at 07:00:30: Hermes Autoresearch Nightly last_run = 2026-06-26 07:08:26 (yesterday). Schedule: `0 7 * * *` = exact 07:00 fire time.
- Wrong classification: "Autoresearch OVERDUE 24h" — would have been false positive.
- Correct classification: "PRE-FIRE window — Schedule matches sweep time within 30s, last_run still yesterday's 07:08:26. Will realize at H51 (08:00)."
- Hermes Agent X Research Daily similarly in pre-fire for 07:30 tick (sweep at 07:00:30, 30 min before scheduled fire).

**Why this rule is permanent:**

The PRE-FIRE window is a structural feature of any cron-driven system, not an edge case. Sweeps can land at any second of any minute; crons fire at HH:MM:00 ± some delay. When a sweep lands within ±60s of a scheduled fire time, the cron appears "stale" by `last_run` but is actually about to fire. Misclassifying PRE-FIRE as OVERDUE:
1. **Inflates fault counts** — false positives in the audit log
2. **Triggers unnecessary escalation** — Orchestrator gets paged for a non-issue
3. **Pollutes forecast models** — predicted events appear to "miss" when they just hadn't fired yet at sweep time

**Decision tree for cron state classification:**

```
For each cron in `hermes cron list`:
1. exit_status == "error"?
   YES → REAL FAULT (escalate to Orchestrator)
   NO  → continue
2. Schedule cron expression parse → get next_fire_time
3. |now - next_fire_time| <= 60s?
   YES → PRE-FIRE (note, forecast to next sweep)
   NO  → continue
4. now - last_run > expected_cadence * 1.5?
   YES → OVERDUE (classify per H29 thresholds)
   NO  → HEALTHY (log status, no action)
```

**H57 PRODUCTION VALIDATION (2026-06-27 13:00):** 5th consecutive sweep where H50 pre-fire observations all realized correctly. At H57, the H56 forecast batch (4 crons in pre-fire at 12:01:05) ALL realized — Operations Manager (12:03:24, 3min), Code Reviewer (12:02:03, 2min), Orchestrator Heartbeat (12:30:41, 41s), qa-agent (in-flight at 13:00). Recipe generalizes across daily, every-30min, and every-6h schedules. **Validation timeline**: H50 self (1st) → H51 (2nd) → H52 (3rd) → H53 (4th) → H56 (5th). See `references/idle-sweep-evidence-h57.md` for full H57 forecast-realization table.

**H36 self-resolution via time progression (related finding from H50):** At H50, ops-manager frontmatter `goal: 6h routing audit (cron 2026-06-27 06:00)` was 1h in the PAST of system time 07:00. H36 did NOT fire because the trigger condition (`frontmatter >2h ahead of system AND content older than frontmatter`) was not met. This validates the H28/H36 trigger clarification: the H36 anomaly is a forward-looking cron-label drift that **naturally self-resolves** as time advances past the cron-label. After each fresh ops-manager audit write, H36 re-fires at the NEXT sweep (when system clock advances 1+ hour beyond frontmatter) and self-resolves at the sweep AFTER THAT. This is a 1-sweep cycle, not a persistent fault. **H51 second validation:** frontmatter 14h in past, H36 still not firing — confirms the 1-sweep cycle and the reliability of the self-resolution mechanism.

**Python heredoc anchor verification (small technique from H50):** Used `python3 << 'EOF'` heredoc to compute `content.count(anchor) == 1` without f-string backslash issues (Python f-strings can't contain backslashes inside `{}` expressions). More reliable than `grep -c` for multi-line anchors. Pattern:

```bash
python3 << 'EOF'
content = open('state.md').read()
anchor = "last_unique_phrase |\n## Verdict History"
print(f'Anchor count: {content.count(anchor)}')
EOF
```

This is strictly an alternative to `grep -c` — both work. Use whichever is convenient in the moment.

See `references/idle-sweep-evidence-h50.md` for the full H50 sweep + pre-fire inflection window repro + H36 self-resolution validation.

---

**🆕 H49 Cron-List Terminal-Truncation Recipe (2026-06-27 06:00) — PERMANENT RULE**

> **H74 2-line anchor double-newline boundary pitfall (2026-06-29):** When the file's natural boundary is `\n\n<section>` (double-newline) and your `new_string` includes the section header text, the H44 2-line anchor can silently emit a duplicate section header. Always check the file's actual newline structure before constructing `new_string`, and verify post-patch with `real_headers = 1` assertion. Full case study + recovery recipe in `references/idle-sweep-evidence-h74.md`.

**The H38 cron-truth sweep assumes the `hermes cron list` capture is complete. It's not always.**

**H49 case study (real):**
- `terminal(command="hermes cron list 2>&1 | head -100")` returned 11 visible cron entries (Hermes Daily Backup through Orchestrator Weekly Cleanup).
- The 7 profile-owned crons (QA Agent Quality Gate, Engineering Lead Code Health, Operations Manager Routing Audit, Code Reviewer PR Watcher, Security Engineer Vuln Scan, Memory Curator Nightly Consolidation, Research Lead Trend Scan) were NOT visible in the captured output.
- Wrong response would be: log "18/18 crons ok ✅" based on H48's prior sweep confirmation + assumption of consistency.
- Correct response (applied at H49): log "11/18 verified fresh; 7 profile-owned crons cited from H48 confirmation — NOT fresh verification."

**Detection recipe (H49 — Permanent):**
1. After running `hermes cron list`, count the captured cron entries (count lines matching `^\s*[a-f0-9]{12}\s+\[active\]` or similar cron-job-id pattern).
2. Compare to the expected count from your prior sweep's known registry (currently 18 at H49).
3. If actual < expected → terminal output truncated.
4. Explicitly note in the sweep row: "X of Y crons verified fresh; Y-X profile-owned crons cited from H<N-1> confirmation."
5. Do NOT fabricate fresh status for the missing crons.

**Recovery options (in priority order):**
1. **Re-run with larger capture window:** `hermes cron list 2>&1 | head -200` — extends the head limit; often sufficient.
2. **Count lines first:** `hermes cron list 2>&1 | wc -l` — gives expected total line count.
3. **Targeted fetch:** `terminal(command="hermes cron list 2>&1 | grep -E "QA Agent Quality Gate|Engineering Lead|Operations Manager"")` — fetches just the missing entries.
4. **No recovery possible:** If truncation persists, log the partial verification clearly and cite prior sweep.

**Why this rule is permanent:**
- The H38 cron-truth recipe was built on the assumption of complete capture. Silent truncation breaks that assumption.
- Logging "verified" without fresh verification is the SAME class of error as the original H28/H29/H34 mtime-as-proxy problem: using a proxy (assumed consistency) for the real signal (fresh cron list).
- Without this rule, future sweeps at H50+ will repeat the error whenever the registry grows or terminal capture fails.

**Why the prior sweep's confirmation is acceptable but must be cited:** In a stable system, the prior sweep's status usually holds for short windows (1-6h). But "usually holds" is not "verified" — the audit log requires distinguishing the two. Citing the prior sweep preserves audit integrity without blocking the sweep on terminal infrastructure.

See `references/idle-sweep-evidence-h49.md` for the full H49 sweep + detection recipe + recovery options.

---

---

## 🆕 H40 Sibling-Collision Pre-Patch Check (2026-06-26 22:00) — CRITICAL TIMING FIX

**The H31 sibling-collision detection recipe was followed at H31 and H33 but FAILED at H40 due to a timing issue.** H40 reads state.md at sweep start, runs profile reads + cron list (~1.5 min), then patches — but the orchestrator 30m heartbeat wrote H40 in that gap. Result: silent data loss of the orchestrator's H40 row.

### The Bug

- Row-count check was run AT SWEEP START (count = 39, H39 latest, expected = H40)
- No re-check IMMEDIATELY BEFORE THE PATCH
- By patch time (~1.5 min later), orchestrator had already written H40
- Patching with H39-tail anchor overwrote the orchestrator's H40 row

### The Fix (H40 — Permanent)

**ALWAYS run `grep -cE "^\|{1,2} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE constructing the patch, not just at sweep start.**

```bash
# Run TWICE per sweep:
# 1. At sweep start (sanity check)
grep -cE "^\|{1,2} H[0-9]+ \|" state.md

# 2. IMMEDIATELY before patch (correctness check)
grep -cE "^\|{1,2} H[0-9]+ \|" state.md
```

If the second check returns a higher count than the first → a sibling row was written in the gap. Default behavior: **RENUMBER UP, NEVER OVERWRITE**. Re-anchor on the actual highest `H<N>` row's tail and use `H<N+1>` for your sweep.

### Token cost

- Row-count check: ~1ms, ~0 tokens
- Renumbering: ~0 tokens
- Overwriting: silent data loss of sibling's audit record

### Why this rule is permanent

- The 1.5-minute window between "sweep start read" and "patch" is exactly the orchestrator 30m heartbeat cadence
- any sweep taking >30 minutes has a non-zero probability of overlapping with a heartbeat
- H40/H41+ sweeps MUST run the check twice

See `references/idle-sweep-evidence-h40.md` for full repro + deviation table.

---

## 📊 Cron Registry Growth Pattern (learned H39, 2026-06-26)

The active-cron count has grown over time as Hermes has been reconfigured:
- H35 (2026-06-26 17:01): 11 active crons
- H37 (2026-06-26 19:01): 11 active crons (research-lead phantom-claim still absent)
- H39 (2026-06-26 21:01): **18 active crons** (research-lead cron re-registered, adding +7 to previous baseline via QA Agent, Engineering Lead, Operations Manager, Code Reviewer, Security Engineer, Memory Curator, Research Lead profile-owned crons)

**Implication for the H38 cron-truth sweep:** the count is dynamic. Sweeps that cite "X active crons" should always include a fresh read at sweep time, not a cached number from a prior sweep. A change in count between sweeps is **normal operational growth** (new profile crons added as needed), NOT a fault signal.

---

- `references/idle-sweep-h60-plus-protocol.md` — **H60+ Mode B idle sweep protocol (2026-06-27)** — Codified 4-step recipe for sweeps in the H60+ regime: pre-patch integrity, anchor selection (H44/H52/H42 decision tree), token-economized H38 cron-truth sweep, H50 pre-fire + H60 forecast-realization. Includes H60→H65 decision window action matrix, H63 worked example, recipe hold rate tracker (6/6 held at H63).
- `references/idle-sweep-evidence-h47.md` — **H47 evidence (2026-06-27 04:00)** — H44 2-line anchor recipe validated 3rd consecutive sweep (H46 tail + boundary, first-try patch success); H34 ops-manager PARTIAL-RECOVERY → WITHIN TOLERANCE sustained 4th sweep (slip_ratio 0.0, 4 consecutive); H36 clock-anomaly trigger condition validated (NOT firing when frontmatter in PAST of system time); H44 cadence-decay option (a) operationalized successfully; 7/7 recipe hold rate; 47 cumulative sweeps PASS vacuous; structural observation: H38 cron-truth is now the dominant signal for dormancy-period sweeps.
- `references/idle-sweep-evidence-h50.md` — H50 evidence (2026-06-27 07:00): pre-fire inflection window recipe codified (PRE-FIRE as third state distinct from HEALTHY/OVERDUE; cron classification decision tree); H36 self-resolution via time progression validated; Python heredoc anchor verification; 9/9 recipe hold rate.
- `references/idle-sweep-evidence-h51.md` — **H51 evidence (2026-06-27 08:00)** — H50 PRE-FIRE recipe **FIRST PRODUCTION VALIDATION** (Autoresearch + X Research fired on schedule as H50 forecast, both within normal cron variance 5-6 min); H51 applied H50 recipe a 2nd time to Orchestrator Heartbeat (Schedule `*/30 8-22 * * *`, pre-fire for 08:00 first tick of day); H36 self-resolution via time progression validated 2nd time (14h-past frontmatter does NOT fire H36); H34 ops-manager WITHIN TOLERANCE sustained **6th consecutive sweep** (longest sustained recovery in file history, codified H28/H33 threshold met for "stable"); cadence-decay escalation threshold REFINED — H55 final warning, H60 auto-suspend qa-agent hourly gate; NEW finding: profiles without registered crons (e.g., coder) are healthy by default per H38 (no cron = no cron to fail); 10/10 recipe hold rate.
- `references/idle-sweep-evidence-h52.md` — H52 (2026-06-27 09:00): 3 RECIPE REFINEMENTS — (1) H44 2-line anchor extended with bold-marker + trailing-pipe variant; (2) H51 coder-no-cron rule extended to TWO classes (no registered cron, OR cron writes elsewhere like memory-curator `Skills: obsidian` → obsidian vault); (3) H50 PRE-FIRE validated 4th time. 11/11 recipe hold rate.
- `references/idle-sweep-evidence-h56.md` — **H56 evidence (2026-06-27 12:01)** — H44 2-line anchor COLLISION detected (count=2 when multiple rows end with same closing phrase; both H53 + H55 ended with `Sweep ready for next event.** |`). Resolved by escalating to H42 unique-phrase anchor (80-char tail, count=1, patch succeeded first try). NEW RULE: if H44 2-line anchor count > 1, auto-escalate to H42 unique-phrase recipe (60-100 char tail OR mid-row unique phrase). H50 PRE-FIRE validated 4th time (3 crons captured in pre-fire window at 12:01:05). H34 ops-manager WITHIN TOLERANCE sustained 9th consecutive sweep. 11/11 recipe hold rate.
- `references/idle-sweep-evidence-h69.md` — **H69 evidence (2026-06-28 06:00)** — **FIRST 6h-cadence sweep + H60→H65 window ACTIONED.** Orchestrator changed QA Agent Quality Gate schedule from `0 * * * *` hourly → `0 */6 * * *` 6h (H51 option (b) realized, NOT option (c) auto-suspend). Token-cost savings ~83% (72K → 12K tokens/day). H44 2-line anchor validated 7th consecutive sweep across cadence transition (proves the recipe stack is cadence-agnostic). H38 cron-truth sweep confirmed all 18 crons healthy. H68 forecast (research-lead Trend Scan next 2026-06-28T18:00) CONFIRMED; H66 forecast (ops-manager 06:00 audit) REALIZED. Recipe hold rate 9/9. No new recipes needed — existing H38/H40/H44/H52/H49/H50 stack handles cadence transitions cleanly. H70 forecast at 2026-06-28 12:00.
- `references/idle-sweep-evidence-h70.md` — **H70 (2026-06-28 12:00)** — SECOND 6h-cadence sweep + **NEW H70 awk-Tail Pitfall codified**. NEVER use `awk '/^\| H<N-1> \|/' state.md | tail -1` (returns full row, 7KB+); ALWAYS use `grep -E ... | tail -1 | tail -c 80` for true tail fragment. Post-cadence-transition regime validated. 9/9 recipe hold rate.
- `references/idle-sweep-evidence-h73.md` — **H73 evidence (2026-06-29 00:00)** — Day-rollover 6h-cadence sweep, 73rd sweep, Mode B vacuous PASS. H44 2-line anchor 7th consecutive sweep. H49 NOT triggered. H50 pre-fire N/A. H34 ops-manager WITHIN TOLERANCE sustained (15+ sweeps). **NEW H73 technique: Token-economy profile read via `stat -f "%Sm %N"` (mtime-only) when Goal/Active-Tasks content not needed — saves 6 read_file calls per sweep.** 9/9 recipe hold rate.
- `references/idle-sweep-evidence-h74.md` — **H74 evidence (2026-06-29 12:00)** — 6h-cadence sweep, 74th sweep. **NEW H74 PERMANENT PATTERN: H44 2-line anchor double-newline boundary pitfall** — when file's natural boundary is `\n\n<section>` and `new_string` includes the header text, anchor can silently emit duplicate section header. Pre-construction: inspect boundary style (SINGLE_NEWLINE / DOUBLE_NEWLINE / NO_NEWLINE). Post-patch: verify `real_headers == 1` via regex. Recovery recipe + decision tree in reference file. 10/10 recipe hold rate despite the bug.
- `references/idle-sweep-evidence-h77.md` — **H77 (2026-06-30 12:00)** — NEW **MCWF** recipe (see SKILL.md H77 section).
*Part of: Loop Engineering system-wide deployment*