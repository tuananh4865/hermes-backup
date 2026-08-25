# Mode 8 — The Silent Kill: when to NOT write a new sweep row (the 2026-06-24 H26 lesson)

> **The most dangerous patch is the one that should never have been made.** When a heartbeat sweeps a system that has been idle 20+ consecutive times, the agent's instinct is to "follow the protocol" and write a new H<N+1> row. This mode documents why that instinct is wrong, what to do instead, and how to recognize the boundary.

## The trap

The heartbeat protocol has 6 steps. Steps 1-3 (parallel read, structural check, freshness check) and Step 6 (emit report) are run every sweep regardless of system state. Steps 4 (cadence trigger) and 5 (pre-append integrity) are guard rails.

**The trap:** Step 4's H20 boundary says "after 20+ idle sweeps, STOP recommending cadence changes". But Step 6 still says "emit the report", which on a stateful system means "write a new row to qa-agent/state.md". The agent follows Step 6 literally, breaks the H20 boundary, and emits a verbose row that:
- Restates "system idle since 2026-06-17" (information-free)
- Restates "X consecutive idle sweeps" (information-free)
- Restates the same security perm checks (information-free)
- Adds 1-4 KB of file growth for zero new signal
- Risks corruption on every patch (the file is now 40+ KB, anchor collisions are real)

The result: the heartbeat becomes its own noise source. The very system designed to reduce noise is now adding to it.

## The real failure (2026-06-24 19:30, H26)

**Setup:** H25 sweep at 19:01 wrote a 4,300-byte row (file size 46249 bytes). System state: 25 consecutive idle sweeps, 0 security CRITICAL, 0 conflicts, 0 pending tasks, no maker activity delta since H24.

**The 3 failed patch attempts (real transcript):**

1. **Attempt 1 — Anchor on 1-line substring:**
   ```
   old_string = "qa-agent cron should be reduced from hourly to 6h NOW (saves ~22 invocations/day without losing signal). **VERDICT: ACCEPT** — system stable. **Orchestrator 30m heartbeat report:** see output below. |"
   ```
   **Result:** `Found 2 matches` — both H19 and the broken H20-row tail ended in similar boilerplate. Patch refused.

2. **Attempt 2 — Anchor on H25 row prefix:**
   ```
   old_string = "| H25 | 2026-06-24 19:01 | N/A | N/A | 0 | (hourly gate — no pending) | 25th consecutive idle sweep, 30m after H24 (hourly gate, not orchestrator over-fire — next H_N must be H26 if 30m heartbeat fires at ~19:31). **Pre-append integrity check passed via H18 triple-confirm**"
   ```
   **Result:** Patch SUCCEEDED — but the agent was overwriting H25's content with the same H25 content + "H26" suffix. **State.md corruption: H25 row was destroyed**, the "Pre-append integrity check" prefix was lost, the file now had the H25 content embedded inside what was supposed to be a new H26 row.

3. **Attempt 3 — Restore H25 by re-anchoring on the corrupted content:**
   ```
   old_string = "— all 3 row-ordering diagnostics agree H24 is chronologically-latest AND file-bottom"
   new_string = "**Pre-append integrity check passed via H18 triple-confirm** — all 3 row-ordering diagnostics agree H24 is chronologically-latest AND file-bottom"
   ```
   **Result:** Patch succeeded. H25 row restored. File back to clean state at 46249 bytes.

**Total damage:** 3 patch operations on a file that should never have been touched. The agent's correct final action was to STOP patching and deliver the report in the response only — but it took 3 attempts to reach that decision.

## The correct behavior (H21+ steady-state idle)

When **ALL** of the following are true, the heartbeat is a response-only delivery:

| Condition | Threshold |
|---|---|
| Consecutive idle sweeps (qa-agent H series) | ≥ 20 |
| Security CRITICAL/HIGH findings | 0 |
| Agent conflicts | 0 |
| Outputs awaiting QA verification | 0 |
| New maker activity since last sweep | 0 (no mtime delta in any specialist profile) |
| Cadence recommendations accumulated | ≥ 3 already delivered in past rows |

If any of these flips to non-zero, write a SHORT row (≤500 bytes) that mentions ONLY the new signal. Otherwise:

1. **Read all 5 profiles in parallel** (Step 1) — this is still required
2. **Structural-truth check** (Step 2) — still required, may detect a new regression
3. **Freshness check on ops-manager** (Step 3) — still required, may detect a new audit
4. **DO NOT touch qa-agent/state.md**
5. **Deliver report in the response only** — 1-line summary + table, ≤40 lines

The existing H1-H20 verdict history is the evidence the system is idle. New rows add no signal. The right action is to **not write**.

## The pre-write self-check (MANDATORY before any state.md patch in idle mode)

```bash
# 1. Count consecutive idle sweeps from qa-agent state.md
LAST_H=$(grep -oE '^\| H[0-9]+ \|' ~/.hermes/profiles/qa-agent/state.md | tail -1 | grep -oE 'H[0-9]+')
echo "Last row: $LAST_H"

# 2. Read the last 3 rows' content
grep -A0 "^$LAST_H |" ~/.hermes/profiles/qa-agent/state.md | head -3
# Look for: "Xth consecutive idle sweep" → if X >= 20, you're in steady-state

# 3. If in steady-state, check if there's any NEW signal:
#    - Security regression: find ... -perm /600 -type f | head
#    - Agent conflict: grep for "OVERLAP" or "2 agents active in same file"
#    - New activity: stat -f "%Sm" all profile state.md, compare to last sweep

# 4. If no new signal → DO NOT PATCH. Deliver in response.
# 5. If there IS new signal → write SHORT row (≤500 bytes), no restating.
```

## What "deliver in response only" looks like

```markdown
## Orchestrator 30m Heartbeat — 2026-06-24 19:30

**1-line:** Hệ thống idle hoàn toàn — 5/5 profiles Goal=None, 0 task pending, 0 output chờ qa-agent, 0 conflict, 1 auto-fix security (12 files `profile/*/state.md` revert 600→644, đã `chmod 600` lại).

| Profile | Last Active | Status | Note |
|---|---|---|---|
| qa-agent | 19:30 (this sweep) | ACTIVE | 26th consecutive idle sweep; cron reduction hourly→6h URGENT |
| ... | ... | ... | ... |

**Counts:** 5 active, 0 stuck, 0 verified-pending, 0 escalated, 1 auto-fix (LOW severity security perm drift).
```

That's the entire report. No state.md touch. The H25 row in qa-agent/state.md remains the latest evidence of the system's idle state. The next sweep (H27 at 20:00 if the cron doesn't get reduced) will do the same.

## Why this is a "kill" and not just "skip"

The verb matters. The instinct is "skip the write" — which sounds passive. The reality is **active suppression** of the agent's natural tendency to produce output.

Every LLM has a default bias toward "doing something visible". On a recurring task, the bias becomes "leave a mark each time" → "write a row each sweep" → "the state file is my canvas". This is fine on small files. On a 40+ KB file with strict append-only + integrity check protocol, every mark is a corruption risk.

The "silent kill" is the active decision to NOT write when the protocol literally says you can. The protocol doesn't forbid the write — the protocol says "emit the report", which is a softer constraint. The H20 boundary + the H23 STEADY-STATE IDLE rule + this Mode 8 together form a tri-layered defense against the LLM's "always produce" bias.

## The 3-layer defense (when system is in H21+ steady-state)

1. **Layer 1 — H20 boundary (Step 4 of SKILL.md):** Stop recommending cadence changes. Log "Cadence trigger URGENT" once per sweep max. After 20+ sweeps, file a single escalation and stop.
2. **Layer 2 — H23 STEADY-STATE IDLE marker file (SKILL.md "MANDATORY pre-write self-check"):** Write `~/.hermes/profiles/qa-agent/.steady-state-idle` on first entry. Marker existence = STEADY_STATE_IDLE mode. Rows in this mode MUST be ≤200 bytes.
3. **Layer 3 — Mode 8 (this file):** When all 6 conditions in the table above are met, do NOT write at all. Deliver in response only. The marker file is informational, not a requirement — Mode 8 is the more conservative default.

**Defense in depth:** Even if the marker file is missing, even if Step 4's H20 boundary is ignored, Mode 8 still applies. The 6-condition check is purely self-derived from the file's own content. No external state needed.

## The hard rule (effective H26, 2026-06-24 19:30)

> **If the last row in qa-agent/state.md says "Xth consecutive idle sweep" where X ≥ 20, AND no new maker activity, AND no security regression, AND no agent conflict, AND no QA-pending output → DO NOT WRITE A NEW ROW.**

The right output is a response-only heartbeat. The state.md file is left untouched. The next sweep that has a real new signal will break the silence and write a row. Until then, the file is the evidence — don't add more.

## Real outcome of H26 (the "what actually went right")

After 3 failed patch attempts and 2 successful reverts, the agent's final action was:

1. **Stopped patching** qa-agent/state.md
2. **Auto-fixed** the 12 security perm regressions (the only file modification justified)
3. **Delivered** the heartbeat in the response only
4. **Stated** explicitly: "Tôi KHÔNG chèn thêm row H26 để tránh thêm rủi ro sai sót — task orchestrator heartbeat đã hoàn thành"

The file ended at H25 (46249 bytes), exactly where H25 left it. The system state is preserved. The heartbeat was delivered. The agent did not corrupt the file. **This is the correct H21+ behavior.**

## Cross-references

- SKILL.md Step 4 — "Authority boundary (H20 lesson)" — the boundary that triggered H26's dilemma
- SKILL.md "MANDATORY pre-write self-check" — the marker file + compressed row recipe (Layer 2)
- This file (Mode 8) — the response-only delivery mode (Layer 3, the most conservative)
- `references/idle-escalation-recipe.md` — the H20 boundary's original design + post-H21 lessons
