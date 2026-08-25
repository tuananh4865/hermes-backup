# Orchestrator Briefing Norms

> **AUTHORITATIVE SOURCE** — Load this file at orchestrator cron STARTUP.
> When `HEARTBEAT.md` and this doc conflict: **follow this doc**.
> This file is the "source of truth" for orchestrator decision logic.

## 🚨 MANDATORY RUNTIME PRE-FLIGHT CHECKS (Run BEFORE compiling any report)

> **PITFALL 27 (2026-06-30) — added at top because cron state.md files lag real-time host failures.** A perfectly-green profile state.md (qa-agent H76 PASS 10.0, ops-manager 06:00 audit clean, all 18 cron jobs `ok`) can co-exist with the host being unable to function (disk 100% full, gateway throwing ENOSPC, Telegram messages silently dropped). The mandatory checks below catch what state.md cannot.

```bash
# ===== RUNTIME HOST HEALTH (must pass BEFORE reading state.md) =====

# 1. DISK SPACE — single biggest runtime risk on macOS volumes
USAGE=$(df -h /Users/tuananh4865 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
if [ "${USAGE:-0}" -ge 95 ] 2>/dev/null; then
    echo "🚨 DISK CRITICAL: ${USAGE}% used"
    df -h /Users/tuananh4865
    # Surface as 🚨 BLOCKER bullet
fi
if [ "${USAGE:-0}" -ge 90 ] 2>/dev/null; then
    echo "⚠️ DISK WARNING: ${USAGE}% used — prune candidates:"
    du -sh /Users/tuananh4865/.hermes/state.db 2>/dev/null
    du -sh /Users/tuananh4865/.hermes/sessions 2>/dev/null
    du -sh /Users/tuananh4865/.hermes/logs 2>/dev/null
fi

# 2. RECENT GATEWAY ERRORS — last 30 min of gateway.log
tail -500 /Users/tuananh4865/.hermes/logs/gateway.log 2>/dev/null \
  | grep -E "ERROR|WARNING" \
  | tail -10
# Any ENOSPC / No space left / connection refused → surface

# 3. TELEGRAM DELIVERY HEALTH — count recent flood/expiry/fail patterns
tail -500 /Users/tuananh4865/.hermes/logs/gateway.log 2>/dev/null \
  | grep -cE "Flood control exceeded|Failed to deliver response"

# ===== THEN proceed to state.md + hermes cron list =====
```

**Rule (PITFALL 27):** "Cron reports `ok`" ≠ "System healthy." Cron reports whether the script EXITED 0 — not whether the host can still function. State.md is a snapshot of cron runs, not a runtime health check. ALWAYS run the runtime checks above FIRST.

**Why this matters — verified 2026-06-30 09:50:**
- All 18 cron jobs reported `ok` at 06:00–09:00
- qa-agent H76 sweep at 00:00 reported PASS 10.0
- ops-manager 06:00 audit: "18/18 ok, 0 stuck, 0 escalations"
- Yet: `df -h` showed 228Gi/228Gi used, 892Mi free
- gateway.log: `[Errno 28] No space left on device` ×5 since 09:29
- Telegram inbound messages dropping silently (sessions/*.tmp writes failing)

Every orchestrator briefing that read state.md + cron list WITHOUT runtime checks would have shipped "all healthy" — completely missing the disk-full emergency.

---

## 🚨 MANDATORY PRE-FLIGHT CHECKS (Run BEFORE compiling any report)

### 1. TRÁHN QA Gate
```bash
# CRITICAL: Use ABSOLUTE PATH — tilde (~) does NOT expand in cron context!
# $HOME in cron = /var/empty, so ~/hermes/... returns nothing
# ALL paths in cron context MUST use /Users/tuananh4865/hermes/...
LATEST=$(ls -t /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
    VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$LATEST" 2>/dev/null || echo "0")
    if [ "$VIOLATIONS" -gt 0 ]; then
        echo "🚨 TRÁHN BLOCK: $VIOLATIONS violation(s) in $LATEST"
        grep -n "đỉnh nóc\|quất một phát" "$LATEST"
        echo "FIX REQUIRED — edit file, re-scan, only then proceed"
        # DO NOT deliver content until violations = 0
    fi
fi
```

### 2. Format Check
```bash
REPORT_LEN=$(echo "$REPORT_BODY" | wc -c)
if [ "$REPORT_LEN" -gt 600 ]; then
    echo "⚠️ Report too long ($REPORT_LEN chars). Strip to 3 bullets."
    echo "Long content → write to file, put filepath in bullet."
fi
```

**⚠️ PITFALL 16 (2026-05-09 — REPEATED from same session):** The TRÁHN gate and 600-char format check were documented in THIS DOC but NOT RUN in this session. Orchestrator delivered a ~800-char verbose report. **Pattern: Documentation ≠ Execution. Reading this doc ≠ Running the checks.**

**⚠️ PITFALL 17 (2026-05-09):** Root cause identified — the orchestrator cron SOUL.md (`~/.hermes/workers/orchestrator/SOUL.md`) says to "load briefing rules" but cannot call `skill_view`. Cron jobs run with their own frozen system prompt context — they never load the briefing doc at runtime.

**REQUIRED FIX — Inline critical rules into cron SOUL.md:** The cron job SOUL.md must contain the rules inline, not as a reference. Append this to `~/.hermes/workers/orchestrator/SOUL.md`:

```
## MANDATORY ENFORCEMENT (inline — no skill_view available in cron)

### Pre-Delivery Gate (RUN THESE as commands, not read as notes)
1. TRÁHN scan (use ABSOLUTE paths — tilde fails in cron!):
   LATEST=$(ls -t /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
   VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$LATEST" 2>/dev/null || echo "0")
   → If VIOLATIONS > 0: FIX inline with sed, re-scan, block until clean
2. Format check:
   REPORT_LEN=$(echo "$REPORT_BODY" | wc -c)
   → If > 600 chars: strip to 3 bullets, one line each
3. Deliver only after BOTH gates pass

### 3-Bullet Format (NON-NEGOTIABLE)
Format: "Hoàn thành | Đang làm | Cần quyết định"
• Bullet 1: ONE LINE — Hoàn thành
• Bullet 2: ONE LINE — Đang làm  
• Bullet 3: ONE LINE — Cần quyết định
Long content → write to file at ~/hermes/workers/orchestrator/outputs/YYYY-MM-DD-report.md, put path in bullet
```

**⚠️ PITFALL 18 (2026-05-09):** Cron sessions cannot call `skill_view()` — briefing doc is never loaded at runtime. Rules documented in briefing ≠ rules enforced in cron. The MANDATORY ENFORCEMENT section must be inlined directly in cron SOUL.md prompts.

**⚠️ PITFALL 19 (2026-05-10):** The TRÁHN QA gate itself was broken in cron context — used `~/.hermes/...` paths which resolve to nothing when `$HOME=/var/empty`. All gates in cron context MUST use `/Users/tuananh4865/hermes/...` absolute paths. The gate would `exit 0` (pass) because `ls` found nothing → `$LATEST` empty → no violations checked → content delivered without QA. **Root cause of May 9-10 TRÁHN failures: gate was structurally broken, not just unenforced.**

**⚠️ PITFALL 20 (2026-05-10):** Orchestrator cron found Research Agent output May 8 (2026-05-08-evening-brief.md) and Content Creator output May 7 (2026-05-07-evening-content.md) — both VALID and recent. But `ls ~/hermes/workers/*/outputs/` showed empty because tilde doesn't resolve in cron. Using `/Users/tuananh4865/hermes/workers/*/outputs/` (absolute) showed files correctly. **Same pattern as Pitfall 17 but now confirmed affecting QA gate itself.**

---

> **⚠️ PITFALL 6 (2026-05-08):** Today's orchestrator cron compiled a detailed multi-paragraph report instead of following the 3-bullet rule. HEARTBEAT says "Brief: 3 bullets max, Format: Hoàn thành | Đang làm | Cần quyết định". The orchestrator must deliver CONCISE bullets, not verbose narrative. If detailed content needs sharing, attach it as a separate file reference — never bury it in the telegram message.

## Morning Brief (8-9AM) — for Anh

**⚠️ SOURCE PRIORITY (confirmed 2026-05-09):** There are TWO output locations — cron dirs and shared outputs/. **Cron dirs are PRIMARY, shared outputs/ are SECONDARY/fallback.**

| Priority | Source | When to Use |
|----------|--------|-------------|
| **PRIMARY** | `~/.hermes/cron/output/{job_id}/` | Always check first — workers fire and write here |
| SECONDARY | `~/hermes/workers/*/outputs/` | Fallback only — often EMPTY even when workers ran |
| SECONDARY | `~/.hermes/workers/memory/PENDING_TASKS.md` | Task tracking |
| SECONDARY | `~/.hermes/workers/memory/MEMORY.md` | PARA system |
| SECONDARY | `~/.hermes/cron/autonomous.log` | Overnight cron results |
| SECONDARY | `~/.hermes/cron/dojo.log` | Nightly self-evolution |

**Canonical check sequence (every orchestrator briefing):**
```bash
# PRIMARY — cron output dirs (workers actually wrote here)
ls -la /Users/tuananh4865/.hermes/cron/output/

# SECONDARY — shared outputs/ (often empty even when workers ran)
ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
ls -la /Users/tuananh4865/hermes/workers/research-agent/outputs/
```

**If cron dir has files but shared outputs/ is empty → cron dir is authoritative.** Workers fire → write to cron dir → orchestrator reads from there. Shared outputs/ may never fill — this is a known architecture gap, NOT a sign workers didn't run.

**Output format for Anh (3 bullets max — NEVER verbose narrative):**
```
Anh ơi, [date]:

Hoàn thành | Đang làm | Cần quyết định
```

**⚠️ PITFALL 9 (2026-05-08 morning briefing):** Orchestrator delivered verbose multi-paragraph narrative (3 sections of prose) instead of the required 3-bullet format. Anh expects:
```
Anh ơi, [date]:

Hoàn thành | Đang làm | Cần quyết định
• [bullet 1 — ONE LINE]
• [bullet 2 — ONE LINE]
• [bullet 3 — ONE LINE]
```

**Long technical content → write to separate file, reference it in bullet.** Never bury paragraphs in the Telegram message itself. Each bullet should be scannable in <3 seconds.

**⚠️ HARD LIMIT: 600 chars total.** Each bullet = 1 line. NO paragraphs, NO sub-bullets, NO tables in the Telegram message. If report exceeds 600 chars → strip to 3 bullets, write full content to file.

**⚠️ NEVER ask "Anh muốn em tự fix không?"** — Prohibited behavior. Fix it directly OR say "Cần quyết định" as last bullet only when genuinely blocked. "Tự xử" rule: if fixable without Anh's input (restart daemon, run repair, nudge worker) → just do it.

**Worker Status (VERIFIED 2026-05-07 — 6/7 crons working):**

| Cron | Worker | Status |
|------|--------|--------|
| Content Creator Morning (8AM) | content-creator | ✅ Working — 8KB morning brief produced |
| Content Creator Evening (6PM) | content-creator | ✅ Working — 18:03 ran |
| Research Analyst Morning (8:30AM) | research-agent | ✅ Working — 8:31 ran |
| Research Analyst Evening (6:30PM) | research-agent | ✅ Working — 18:50 ran |
| Orchestrator Morning (9AM) | orchestrator | ✅ Delivered to Anh |
| Orchestrator Monitor (2h) | orchestrator | ✅ 6 runs confirmed today |
| Orchestrator Nightly (9PM) | orchestrator | ⏳ Next: 21:00 today |

**⚠️ [SILENT] Decision Tree — CRITICAL (updated 2026-05-14):**

| Condition | Action |
|-----------|--------|
| ALL worker outputs/ empty AND orchestrator produced no direct brief | `[SILENT]` |
| Worker outputs present | **REPORT THEM** — never suppress |
| Workers stalled (no recent output) BUT orchestrator produced direct brief | **REPORT THE ORCHESTRATOR BRIEF** — do NOT suppress |
| Orchestrator compiled status from own research | **REPORT IT** — this IS the deliverable |
| Any worker has new deliverable | **REPORT IT** |

**⚠️ PITFALL 23 (2026-05-14):** Orchestrator detected workers stalled (CC: May 13 evening ~34h gap, RA: May 12 afternoon ~62h gap), compiled direct report (Summer Cooling NOW window, Neck Fan 64% margin, Gen Z slang: lọ=hot, ra dại, chả quyên, nấu xói), BUT still sent `[SILENT]`.

**Root cause:** HEARTBEAT-based decision tree only says "if all empty → [SILENT]". It doesn't handle: "orchestrator produced its own direct report = DELIVER IT".

**HARD RULE — [SILENT] Decision Logic (corrected):**
```
# CRON ORCHESTRATOR [SILENT] DECISION TREE — USE THIS, NOT HEARTBEAT

if orchestrator_own_report_exists:
    # Workers stalled BUT orchestrator filled the gap = ALWAYS DELIVER
    → DELIVER the orchestrator report
    → Include "Workers: CC ~34h, RA ~62h" as note inside report
elif worker_outputs_exist:
    → report worker outputs
else:
    → [SILENT]
```

**Key insight:** Orchestrator's fallback production IS the deliverable. Worker stall ≠ no content. Only `[SILENT]` when NEITHER workers NOR orchestrator produced anything.

**Confirmed state (2026-05-14 04:00):**
| Source | Status |
|--------|--------|
| Content Creator | ⚠️ Stalled since May 13 18:02 (~34h) |
| Research Agent | ⚠️ Stalled since May 12 14:08 (~62h) |
| Orchestrator direct | ✅ Compiled (Summer Cooling + Beauty + slang) |
| Dojo | ✅ Ran (4 pages, 3 skills) |

**⚠️ TRÁHN QA Gate Path Bug:** The gate at top of this doc uses `~/hermes/workers/content-creator/outputs/*.md` — tilde (`~`) does NOT expand in cron context where `$HOME=/var/empty`. ALL path references in cron context MUST use absolute `/Users/tuananh4865/hermes/workers/content-creator/outputs/*.md`.

**⚠️ PITFALL (2026-05-07):** Orchestrator midday check found Content Creator's morning brief (8,376 bytes) but sent `[SILENT]`. Mistaken logic: "I checked = nothing new" when the actual content WAS the morning brief. **Never suppress when worker output exists.**

**⚠️ PITFALL (2026-05-08):** Research Agent evening (May 7) MISSED — last ran May 6 18:31. Orchestrator correctly noted but sent [SILENT] instead of flagging as action item. **Any missed worker cron = explicit "Cần xử lý" bullet, not silent suppression.**

**⚠️ PITFALL (2026-05-08 evening):** Evening orchestrator report was 1,847 characters — far exceeding the 600 char limit. Multi-paragraph format with tables. **Enforcement: Count chars before sending.**

**Concrete "Tự xử" examples (JUST DO THESE without asking):**
| Symptom | Action |
|---------|--------|
| watchdog daemon down | `~/.hermes/restart_gateway.sh` or restart via skills |
| Worker missed run | Investigate: check cron logs, check if worker SOUL.md is correct, fix if needed |
| Worker output path gap | Update SOUL.md to write to shared outputs/ explicitly |
| Wiki has broken links | Run `wiki_self_heal.py --fix --all` |
| PENDING_TASKS has stale items | Clean it up |
| Skill outdated | `skill_manage patch` to fix |

**What to NEVER ask about (just do it):**
- Restarting a known-down daemon
- Running wiki repair scripts
- Fixing worker cron configuration
- Updating SOUL.md prompts

**What to flag as "Cần quyết định" (only these):**
- Business decisions (pricing, campaigns, partnerships)
- Spend approval (ads budget, tool subscriptions)
- Creative direction (what product to promote, which angle)
- Anything that changes revenue strategy

**⚠️ PITFALL 14 (2026-05-09): HEARTBEAT "Today" ≠ Actual Today**

**Symptom:** HEARTBEAT.md shows "Today's Activity" but it's actually referencing YESTERDAY's content because the heartbeat wasn't updated. Example:
```
# HEARTBEAT says:
## Today's Activity
- Evening brief summary (May 8)

## Today's Focus (Content Creator)
- Weekend aesthetic + Kẹp Tóc Nơ Bong Bóng (May 9)

# Reality:
- It's actually May 9, so "Today" in heartbeat IS correct for morning
- BUT "Evening brief summary (May 8)" is YESTERDAY's content
```

**Root cause:** HEARTBEAT isn't being updated by workers automatically — it's manually updated by orchestrator during health checks. Stale heartbeat = stale "today" references.

**Detection:**
```bash
# Check if heartbeat was actually updated today
grep "Last Updated" /Users/tuananh4865/hermes/workers/content-creator/HEARTBEAT.md
# If yesterday's date → heartbeat is stale

# Verify by checking actual output timestamps
ls -lt /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md | head -3
```

**Rule:** Never trust HEARTBEAT "Today" labels. Always cross-reference with:
1. Actual file timestamps
2. File header date (each brief starts with `**Date:** YYYY-MM-DD`)
3. Cron output dir timestamps

**HEARTBEAT is a STATUS TRACKING document, not a CONTENT document.** Read outputs/ for content, read HEARTBEAT only for status/health signals.

**⚠️ CRITICAL: HEARTBEAT.md vs This Doc — Use This Doc**

The orchestrator cron job (`a4b8e528983f`) runs with the `HEARTBEAT.md` rule set:
> "If ALL sources empty → [SILENT]"

**THIS IS OUTDATED.** The actual decision tree in this doc is richer and CORRECT. When this doc and `HEARTBEAT.md` conflict — **follow this doc**.

Known conflict: **2026-05-08** — Orchestrator cron found Research Agent missed its May 7 evening run, correctly detected the issue, but applied HEARTBEAT's simplistic "[SILENT]" rule instead. Missed worker issue not flagged to Anh.

**Rule**: `[SILENT]` ONLY when BOTH conditions hold:
1. ALL worker output directories are truly empty (no new files today)
2. No system changes, no new cron results, no pending tasks updated

**If any worker missed a scheduled run → ALWAYS report as "Cần xử lý" — never suppress.**

### Worker-Completion QA Checklist (MANDATORY for every briefing)

**⚠️ TIMING RULE (2026-05-09):** Morning orchestrator runs at 9AM. It compiles:
- Previous day's evening output (May 8 evening, May 9 morning)
- It CANNOT have current day's evening content (that fires at 6PM)

**Confusion matrix:**
| Orchestrator runtime | Can contain morning (8AM) | Can contain evening (6PM) |
|---------------------|--------------------------|-------------------------|
| 9AM morning run | ✅ YES (current day) | ❌ NO (fires later today) |
| 6PM evening run | ✅ YES (same day) | ❌ NO (fires later today) |
| 9PM nightly run | ✅ YES (today) | ✅ YES (today) |

**Source audit procedure (2026-05-09 refinement):**

```bash
# STEP 1: List ALL worker output files by timestamp
find /Users/tuananh4865/hermes/workers -name "*.md" -newer /tmp/$(date -v-1d +%Y-%m-%d) 2>/dev/null

# STEP 2: Attribute to correct worker — read file header to verify
head -3 /Users/tuananh4865/hermes/workers/*/outputs/*.md 2>/dev/null | grep -E "(Research Analyst|Content Creator|---)"

# STEP 3: Cross-reference with cron output (authoritative)
ls -la /Users/tuananh4865/.hermes/cron/output/*/2026-05-09*.md 2>/dev/null
```

**Source misattribution pattern (KNOWN ISSUE):** Research-agent outputs may appear in content-creator/outputs/ or vice versa. Always read file header to confirm true source, not just directory name.

**HEARTBEAT staleness detection:**
- HEARTBEAT.md shows "Last Updated" timestamp
- If HEARTBEAT shows yesterday's date but cron ran today → worker may have fired but didn't update heartbeat
- Check cron output dir for actual files if HEARTBEAT seems stale

Before finalizing report, verify EACH worker ran today:

```bash
# Check each expected output — compare timestamps with current date
ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/   # Should have YYYY-MM-DD files
ls -la /Users/tuananh4865/hermes/workers/research-agent/outputs/      # Should have YYYY-MM-DD files

# Check cron output too (primary source — workers write here first)
ls -la /Users/tuananh4865/.hermes/cron/output/*/2026-05-09*.md 2>/dev/null
```

| Worker | Expected | Morning Run (9AM) | Evening Run (6PM) |
|--------|----------|------------------|-------------------|
| Content Creator Morning | 8AM | ✅/❌ Today's file? | N/A |
| Content Creator Evening | 6PM | ❌ NOT YET | ✅/❌ Today's file? |
| Research Analyst Morning | 8:30AM | ✅/❌ Today's file? | N/A |
| Research Analyst Evening | 6:30PM | ❌ NOT YET | ✅/❌ Today's file? |

**❌ MISSING worker run → must appear in "Cần xử lý" section, not just noted in passing.**

### Script QA Pass (MANDATORY — correct BEFORE delivery, not after)

**Every content script MUST pass this check BEFORE appearing in any report to Anh:**

| Check | TRÁHN | Status |
|-------|-------|--------|
| "đỉnh nóc" or "đỉnh nóc kịch trần" | OUT | Must NOT appear (found repeated in May 8 evening brief Script 2) |
| "quất một phát" | OUT | Must NOT appear |
| "đã X là Y" cấu trúc cứng nhắc | OUT | Must NOT appear |
| Template repetition across scripts | OUT | Each script must feel unique |
| "anh" + "mấy con vợ" voice | ✅ IN | Must appear correctly |

**CORRECT PROTOCOL (2026-05-08 lessons):**
1. QA check FAILS → identify the specific TRÁHN violation
2. **CORRECT the script inline** — fix the violation before sending
3. THEN report corrected version to Anh
4. Do NOT just flag "QA FAIL" and let the bad content through

**Never report a failed script to Anh without correcting it first.**

**🔴 LIVE QA CATCH (2026-05-08):** Charm Mini Review script contained "đỉnh nóc luôn" — explicitly in the TRÁHN list. Script was flagged but NOT corrected before delivery. **This is a pattern failure: the orchestrator identified the issue but only flagged it instead of correcting it.**

**ACTION TAKEN:** Fixed the broken script inline in `~/.hermes/workers/content-creator/outputs/2026-05-07-evening-content.md` — replaced "đỉnh nóc luôn" with "ngon vậy" (same meaning, fresh phrasing).

**CORRECT PROTOCOL (REMEMBERED):** When QA fails:
1. Identify the specific TRÁHN violation
2. **CORRECT the script inline** — fix the violation immediately
3. Report the corrected version to Anh
4. Do NOT just flag "QA FAIL" and let bad content through

**⚠️ PITFALL 8 (2026-05-08):** The CORRECTION PROTOCOL section in this doc was already written but did NOT prevent the failure. Why? Because it was written as a reactive note rather than an ENFORCED rule.

**⚠️ PITFALL 13 (2026-05-08 evening — REPEATED FAILURE):** Despite PITFALL 8 + PITFALL 6 + PITFALL 9 all documenting the 3-bullet rule and QA correction protocol, Script 2 (Vòng Tay May Mắn) in the May 8 evening brief still contained "đỉnh nóc kịch trần". The orchestrator identified the TRÁHN violation but did NOT correct it inline before compiling the report. Pattern: documentation alone does not enforce behavior. The MANDATORY PRE-DELIVERY ENFORCEMENT gate (see above) is now the enforced mechanism — it MUST block delivery if TRÁHN violations are found.

**This protocol is now ENFORCED at the orchestrator level:** Any script failing QA must be corrected before it can appear in any report to Anh. No exceptions.

**If workers set up but outputs empty → flag it explicitly:**
```
⚠️ Workers set up [date] but no outputs yet — monitoring, will nudge if stalled
```

---

## Worker Verification Checklist (before declaring workers "running")

From multi-agent-orchestrator SKILL.md — run BEFORE any status claim:

```bash
# 1. System cron is running
ps aux | grep cron | grep -v grep

# 2. Output directory has recent files (use ABSOLUTE paths — tilde fails in cron!)
ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
ls -la /Users/tuananh4865/hermes/workers/research-agent/outputs/

# 3. Worker directories populated
ls -la /Users/tuananh4865/hermes/workers/{worker-name}/
```

**"Workers configured" (SOUL.md + HEARTBEAT.md exist) ≠ "Workers running" (outputs/ has files)**
This is the #1 false positive to avoid in briefings.

---

### Cron Log Review Pattern

When reviewing `autonomous.log` for morning briefing:

```
tail -50 /Users/tuananh4865/.hermes/cron/autonomous.log | grep -E "2026-05-07|script|content|TikTok|report|worker"
```

When reviewing `dojo.log`:
```
tail -30 /Users/tuananh4865/.hermes/cron/dojo.log | grep -E "complete|improved|committed"
```

### System Tasks with Priority 80+ — Act or Flag

Check `~/.hermes/cron/last_task_check.json` for system tasks:

```bash
cat ~/.hermes/cron/last_task_check.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data.get('system_tasks', []):
    if t.get('priority', 0) >= 80:
        print(f\"⚠️  Priority {t['priority']}: {t['text']}\")
"
```

**Rule**: Priority 80+ system tasks MUST be either:
- **Acted on** immediately (if fix is known and low-risk), OR
- **Flagged in report** as "Cần xử lý" bullet (never silently ignored)

**Known high-priority system task (recurring)**: `Restart watchdog daemon` (priority 80). If watchdog is already running (`ps aux | grep watchdog | grep -v grep`), mark as resolved in report.

### Multi-Run Deduplication (Orchestrator runs 2h)

Orchestrator runs every 2h. Morning brief (9AM) already reported content outputs. Subsequent noon+ runs should:

| Condition | Action |
|-----------|--------|
| Morning outputs already delivered at 9AM | Don't re-report — just confirm status |
| New afternoon output appeared (e.g., 6PM worker ran) | REPORT IT |
| Missed worker since last run | "Cần xử lý" bullet |
| No changes since last run | [SILENT] |

**Decision tree for noon+ runs:**
1. Did any worker produce NEW output since last orchestrator report?
   - YES → Report the new output
   - NO → Was any worker supposed to run but didn't (compared to expected schedule)?
     - YES → "Cần xử lý" bullet
     - NO → [SILENT]

**This prevents**: Re-reporting "morning briefs exist" at noon when they were already delivered at 9AM.

---

## Pending Tasks Format

Source: `/Users/tuananh4865/hermes/workers/memory/PENDING_TASKS.md`

```markdown
## Current Tasks
*(No pending tasks)*

## Recent Completions
- YYYY-MM-DD: [task] — [outcome]

## Blockers
*(None)*
```

If current tasks = empty AND recent completions = empty AND blockers = none → [SILENT]

---

## Known System Issues to Flag

| Issue | Symptom | File | Status |
|-------|---------|------|--------|
| watchdog_processor.py crash | `Path.write_text() mode=` bug, crashes every 15min | `scripts/watchdog_processor.py:392` | Known — see references/watchdog-python-bug.md |
| Worker crons misconfigured | Running generic scripts, not launching workers | cron jobs | Known since May 6 |
| Autonomous task loop | "Executing highest priority task" never actually executes | `task_checker.py` | Seen May 8 — task picked but no execution |
| Research Agent 48h+ gap | Last output May 6 evening, missing May 7+8 | `research-agent/outputs/` | Active gap — needs investigation |

---

## Escalation Thresholds (NEW — 2026-05-08)

### Worker Output Gap Escalation

| Gap Duration | Action |
|-------------|--------|
| < 24h (1 missed run) | Note in "Đang làm" bullet |
| 24-48h (2 missed runs) | Note in "Cần xử lý" bullet |
| > 48h (3+ missed runs) | Spawn investigation task, escalate to Anh |

**Research Agent example (May 8 session):**
- Last output: May 6 evening (18:31)
- Expected: May 7 evening + May 8 evening
- Current gap: ~46h at 4PM May 8
- Status: Should be in "Cần quyết định" with note "Research Agent — 46h không có output"

### Autonomous Task Checker Loop Detection (NEW — 2026-05-08)

**Symptom**: `autonomous.log` shows repeated:
```
🤖 **AUTONOMOUS MODE: Executing highest priority task...**
[2026-05-08 14:00:47] TASKS: 24 pending | NEXT: Restart watchdog daemon [80]
🤖 **AUTONOMOUS TASK CHECK — 14:00 08/05/2026**
...same message repeated at 16:00...
```

**Root cause**: `task_checker.py` identifies task [80] as highest priority, says it will execute, but the execution doesn't happen. Next run 2.5h later → same loop.

**Detection**: Check `~/.hermes/cron/autonomous.log` for:
```
grep "Executing highest priority task" /Users/tuananh4865/.hermes/cron/autonomous.log | tail -5
```
If same task appears 3+ times consecutively → loop detected.

**Action**: Write directly to PENDING_TASKS.md or execute the fix manually. Don't wait for autonomous task checker to handle it.

---

## Script QA Correction — Explicit Protocol (2026-05-08)

QA correction is NOT optional — it's a required step in the pipeline. Add to every content delivery:

```
### Script QA Check (MANDATORY)
Before any script appears in a report to Anh:
1. Run TRÁHN scan:
   grep -E "(đỉnh nóc|quất một phát|đã .* là .*)" <script_file>
   → Any match = FAIL
2. If FAIL:
   a. Identify exact violation
   b. Fix inline immediately (sed or manual edit)
   c. Re-verify: grep again to confirm fix
   d. THEN report corrected version
3. If PASS: Report normally
```

**This step must appear BEFORE "Deliver to Anh" in every workflow.**

### 🚨 MANDATORY PRE-DELIVERY ENFORCEMENT (enforced since 2026-05-08)

Before ANY report containing scripts is sent to Anh, you MUST run this gate:

```bash
# GATE 1: TRÁHN Scan
# CRITICAL: Use ABSOLUTE PATH — tilde (~) does NOT expand in cron context!
LATEST=$(ls -t /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
[ -z "$LATEST" ] && echo "ERROR: No content file found" && exit 1

VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$LATEST" 2>/dev/null || echo "0")
if [ "$VIOLATIONS" -gt 0 ]; then
    echo "🚨 QA FAIL: $VIOLATIONS TRÁHN violation(s) found in $LATEST"
    grep -n "đỉnh nóc\|quất một phát" "$LATEST"
    echo "FIX REQUIRED before delivery. Use sed to correct, then re-scan."
    exit 1  # BLOCK delivery until fixed
fi

# GATE 2: Format Check 
REPORT_LEN=$(echo "$REPORT_BODY" | wc -c)
if [ "$REPORT_LEN" -gt 600 ]; then
    echo "⚠️ Report too long ($REPORT_LEN chars). Strip to 3 bullets."
    exit 1
fi

echo "✅ QA PASS — ready to deliver"
```

**If exit 1 → Block delivery. Fix the violation. Re-run gate. Only send after ✅ QA PASS.**