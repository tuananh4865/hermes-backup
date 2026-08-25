# Coupled-Artifacts Audit — Multi-File Mandate Verification

> **Date:** 2026-07-30
> **Trigger:** Independent re-audit after a "Fix pitfall #9" patch was claimed DONE.
> **What fired:** The patch fixed `evidence-gate/SKILL.md` correctly. It also claimed SOUL.md was patched. But the audit found that SOUL.md still had a contradictory heading next to its new "MỌI TASK" wording.
> **Use this reference when:** the rule lives across 3+ coupled files (SOUL.md + umbrella skill + cross-reference skill + wiki entity), and you need to verify patch completeness — not just per-file success.

## Why this exists

Standard mandate propagation (Fable-5, Layer 1-5 matrix) verifies each FILE individually. It does NOT verify **cross-file consistency** — i.e. that the same wording/heading/intent appears across all coupled files at the same time.

The real failure mode this catches:

> **Per-file: PASS. Cross-file: FAIL.** Patcher updated line 174/178 in SOUL.md to "MỌI TASK / không phân biệt độ lớn". But left line 203 unchanged: "**Subagent MANDATORY cho task 🔴 LARGE:**" with a 5-step workflow (lines 205-212) describing only LARGE tasks. Same file, same file, contradictory rule in two places.

This is invisible to single-file `grep "MỌI TASK"` — it returns match, file "complies". But it's visible to any reader (human or subagent) who reads the full file and tries to apply the rule.

## The 5-file audit checklist (called by Step 7)

When a mandate is owned by the user (NOT in shared ref) and lives across multiple coupled files, run this BEFORE claiming DONE. Each pass uses greps / line counts / quoted evidence.

| File class | What to grep | Why |
|---|---|---|
| **1. SOUL.md** (default profile) | `<rule marker>` in body, NO contradictory headings within ±50 lines of the new rule | Agent reads SOUL first on `session:start`. Internal contradiction = agent confused. |
| **2. Umbrella skill SKILL.md** | `<rule marker>` + `<cross-ref to verifier>` | Agent loads umbrella when QA question fires. |
| **3. Cross-referenced skill SKILL.md** | `<rule marker>` + `<cross-ref back to umbrella>` | Related skills must agree on wording. |
| **4. Wiki entity** | `<rule marker>` in current entities file | Persistent memory re-derives on compaction. |
| **5. (Optional) Shared reference / doc** | `pitfall #N` cite + date | Single source of truth for related skills. |

### Failure-mode detector (run FIRST before per-file greps)

```bash
# For each coupled file, check that the rule marker is consistent,
# AND that NO contradictory wording exists nearby.

RULE="every task / MỌI TASK / không phân biệt độ lớn"
COUNTER_RULE="LARGE\|chỉ large\|chỉ task lớn\|size-based\|size exception"

for file in ~/.hermes/SOUL.md \
            ~/.hermes/skills/<umbrella>/SKILL.md \
            ~/.hermes/skills/<cross-ref>/SKILL.md; do
  HAS_RULE=$(grep -c "$RULE" "$file" 2>/dev/null)
  HAS_COUNTER=$(grep -nc "$COUNTER_RULE" "$file" 2>/dev/null)
  echo "=== $file ==="
  echo "  rule marker present: $HAS_RULE"
  echo "  contradictory wording count: $HAS_COUNTER"
  if [ "$HAS_COUNTER" -gt 0 ]; then
    echo "  ⚠️  INTERNAL CONTRADICTION — show me these lines:"
    grep -n "$COUNTER_RULE" "$file" | head -5
  fi
done
```

**If `counter_rule > 0` in any file → file is INCONSISTENT, even if `rule > 0`. STOP and decide: was the old wording intentional (deprecation in progress) or residue (incomplete patch)?**

## Real case: evidence-gate pitfall #9 re-audit, 2026-07-30

**Setup:** User asked me to re-audit after `evidence-gate/SKILL.md` "no size exception" pitfall #9 patch.

**Files claimed patched:** 4 — `evidence-gate/SKILL.md`, `qa-gate/SKILL.md`, `learned-about-tuananh.md`, `~/.hermes/SOUL.md`.

**Audit verdict (per-file with raw evidence):**

| File | grep "no size exception" | grep "MỌI TASK" | grep "🔴 LARGE" | Verdict |
|---|---|---|---|---|
| `evidence-gate/SKILL.md` | 1 (line 149) | n/a | 0 | **PASS** |
| `qa-gate/SKILL.md` | n/a | present (line 8, 10) | 0 | **PASS** |
| `learned-about-tuananh.md` | n/a | present (line 692) | 0 | **PASS** |
| `~/.hermes/SOUL.md` | n/a | partial (line 178) | **1 (line 203)** | **FAIL — internal contradiction** |

**Failure detail in SOUL.md:**
- Line 174: `**Task nào PHẢI chạy independent subagent QA trước khi báo xong — KHÔNG phân biệt độ lớn:**` (NEW)
- Line 178: `| **MỌI TASK** | ...` (NEW — single-row table updated)
- **Line 203:** `**Subagent MANDATORY cho task 🔴 LARGE:**` (OLD — unchanged)
- **Lines 205-212:** 5-step `delegate_task()` workflow describing only LARGE tasks (OLD — unchanged)

**Detection:** This passes the per-file `grep "MỌI TASK"` check (returns 1 match). Fails the cross-file consistency check (counter-rule `LARGE` returns 1 within ±40 lines of the new rule).

## What was missed in the original patch

| Why the patch looked "done" | What actually leaked |
|---|---|
| evidence-gate pitfall #9 was the only file in scope | SOUL.md had stale `Subagent MANDATORY cho task 🔴 LARGE` heading 30 lines below new "MỌI TASK" wording |
| `grep "no size exception" evidence-gate/SKILL.md` → 1 match | SOUL.md still has size-based classification |
| Daily log (2026-07-30.jsonl) had 14 patch entries with reasons like "every-task independent subagent QA" | Log shows attempts, NOT cross-file consistency |

## Fix recipe (4 steps, run as a single audit pass)

When patching a cross-file rule, follow this order. Don't patch one file, claim "partially done", then continue.

```
1. ENUMERATE — List ALL files that contain the OLD rule wording
   grep -rl "<old-wording>" ~/.hermes/ /Volumes/Storage-1/Hermes/wiki/

2. PATCH-ALL-IN-ONE — Edit every coupled file in one session
   Don't leave "evidence-gate done, SOUL.md later" — that's how contradictions survive

3. AUDIT-CROSS — Run the failure-mode detector above on all files together
   Each file: rule_marker > 0 AND counter_rule == 0 within ±50 lines

4. REPORT-ALL-OR-NONE — Either all files clean or none
   Don't report PASS for files cleaned and silence on files still in flight
```

## Connected to existing skill sections

- **SKILL.md Step 7 (Audit A + B)** — extends source-coverage audit from "did I harvest all sections of source" to "did I patch all consumers of source" (different question!)
- **SKILL.md Scope Decision table** — applies: a "system-wide" mandate = 4+ files minimum, so default to FULL 3-phase workflow, NOT single-file merge
- **`/Users/tuananh4865/.hermes/skills/devops/self-verify-after-workaround/SKILL.md` → "5-Layer Verification Matrix"** — same principle, different surface (system-wide infrastructure vs. cross-file mandate). Single-layer verification = false confidence in BOTH contexts.

## Anti-patterns (don't repeat)

1. ❌ **"I patched the umbrella skill, that's the rule source"** — but the rule ALSO needs to live in SOUL.md + a couple of related skills + the wiki entity. The umbrella is a reference, not the only source.
2. ❌ **"Per-file grep returns match → file PASS"** — without checking for counter-rules in the same file. Internal contradiction is invisible to single-pattern greps.
3. ❌ **"Daily log shows the patch entry → DONE"** — the log records attempts. It does NOT verify cross-file consistency. Read the files, not the log.
4. ❌ **"I'll finish the rest next session"** — half-applied mandates are worse than not started. They create the illusion of compliance. Either run all-or-none, or report the partial state explicitly with the contradiction visible.

## When NOT to use this reference

- **Single-file scope** ("merge into SOUL.md", "save to memory") — this skill's Scope Decision table already covers that case. Don't over-deploy.
- **A new mandate that has not existed before** (vs. an EXISTING mandate being patched) — there's no "old wording" to detect. Just write the rule cleanly in all coupled files from the start.

## Real-world cost of skipping this check

- 1 failed re-audit round (≈ 30 min agent time, plus user escalates)
- User perceives "you keep saying done but it's still half-fixed" → trust erosion
- Next session has contradictory rules loaded in context → behavior drift

Reference this when running `references/idempotent-script-qa-protocol.md` Step 7 audits for mandates.
