# state.md Bloat Detection & Compaction

**Class:** Operations Manager / 30m Heartbeat
**Codified:** 2026-06-28 (H73 sweep — qa-agent/state.md hit 195,660 bytes / 117 lines)
**Status:** ACTIVE — bloat compounds silently, will degrade every subsequent sweep

## Why this exists

Profile `state.md` files accumulate verdict rows every sweep. With qa-agent on hourly cadence for 60+ sweeps × ~2-3KB per row, files grow from <10KB to 50KB→100KB→200KB+ within 10-14 days. Once a file exceeds the 100K char `read_file` safety limit, EVERY subsequent read requires a workaround. Left unchecked, bloat self-amplifies: the workaround burns tokens, the agent reads less, verdicts become more terse, and signal quality drops.

## Three-tier threshold (Codified 2026-06-28)

| Tier | Size | Symptom | Action |
|------|------|---------|--------|
| 🟢 HEALTHY | <50KB | `read_file` works fine | None |
| 🟡 BLOAT | 50-100KB | Reads work but slow; file is large | Note in heartbeat table; monitor |
| 🟠 COMPOUNDING | 100-200KB | `read_file` may refuse; must use `tail` workaround | Surface in every sweep; warn user |
| 🔴 UNREADABLE | >200KB | `read_file` refuses whole-file calls (response >100K chars); offset/limit pagination still works for targeted reads; `terminal tail` is the safe bulk fallback | **ESCALATE to user** for compaction |

## Detection recipe (run at start of every heartbeat)

```bash
# Get size of all profile state.md files in one shot
for p in ~/.hermes/profiles/*/state.md; do
  sz=$(wc -c < "$p")
  mt=$(stat -f "%Sm" "$p")
  echo "$sz $mt $p"
done | sort -rn
```

**Interpretation:**
- Largest file >100K bytes → 🟠/🔴 tier
- File mtime >24h on a profile with a cron → not necessarily bloat, may just be quiet day
- File mtime >24h on a profile WITHOUT a cron → bloat is the only explanation; investigate

## When `read_file` refuses (the 100K+ workaround)

`read_file` enforces a ~100K **response** char limit (not file size) and refuses whole-file calls. Three viable strategies, ordered by token efficiency:

**Strategy 1 — `read_file` with offset/limit pagination (best for targeted sections):**
```python
# Get frontmatter + early sections (lines 1-60)
read_file(path="~/.hermes/profiles/qa-agent/state.md", offset=1, limit=60)
# Get latest verdict rows (lines 60-end)
read_file(path="~/.hermes/profiles/qa-agent/state.md", offset=60, limit=200)
```
Works on any file size. Most token-efficient when you only need 2-3 specific regions (frontmatter + latest H row). Parallelize multiple profile reads in one batch.

**Strategy 2 — `terminal tail` (best for bulk recent content):**
```bash
# Get just the last 100 lines (most recent H rows)
tail -100 ~/.hermes/profiles/qa-agent/state.md

# Or: extract only the H-row table content (skip prose)
grep -E '^\| H[0-9]+ \|' ~/.hermes/profiles/qa-agent/state.md | tail -5
```
The `grep` approach is most token-efficient when you only need the H-row content (skips narrative prose between rows).

**Strategy 3 — `hermes cron list` instead (often sufficient for heartbeat):**
```bash
hermes cron list 2>&1 | head -100
```
For 30m heartbeat, you usually only need the last sweep's H row + cron truth — not the full file. H38 ground-truth sweep via `hermes cron list` provides 90% of the signal.

**Decision rule:** try Strategy 1 first (you already have `read_file` in your toolset), fall back to Strategy 2 if you need bulk content, fall back to Strategy 3 if cron ground-truth is sufficient.

**DO NOT** retry with `offset=1` thinking the limit was on file size — the limit is on the response, and the file's content is the same regardless of offset.

## When to escalate (Compaction trigger)

**ES**calate when ANY of these fire:
1. qa-agent/state.md >200K bytes (compound tier breached)
2. Two consecutive sweeps where `terminal tail` was required to read ANY profile state.md
3. `read_file` outright fails (caller sees "Read exceeds ~100K characters")

**Escalation message format:**
```
🟠 state.md BLOAT: qa-agent/state.md = N bytes (NN rows accumulated).
   Refused by read_file. Worked around with tail.
   → Recommend compaction via `heartbeat-state-md-bloat` recipe.
   Reference: hermes-agent skill → references/heartbeat-state-md-bloat.md
```

## The compaction recipe (delegate to user)

The actual compaction workflow lives in the `hermes-agent` skill:
- `references/heartbeat-state-md-bloat.md` — full compaction recipe for qa-agent/state.md

**Quick summary of what the recipe does:**
1. Keep only the LAST 20 H rows in the file
2. Archive older H rows to `~/.hermes/profiles/qa-agent/state.archive.md` with timestamp header
3. Preserve `## Current Goal`, `## Recent Verdicts`, and `## What Worked/Failed/Open Items` sections
4. Restart qa-agent cron — next sweep starts at H<N+1> with a clean state

**NEVER** do compaction from a heartbeat or routing audit sweep. Compaction is a destructive write that requires explicit user authorization per the H60 / heartbeat safety rule (read-only sweep).

## Why bloat happens (root cause)

qa-agent's hourly cadence writes ~3KB per sweep (full H row + 6-check protocol). At 24 sweeps/day × 3KB = 72KB/day. Within 10 days, the file hits 720KB. The H51 cadence-decay recipe reduced qa-agent from hourly to 6h (token savings ~83%), but the OLD H rows are still in the file.

**Preventive action (run once, not on every sweep):**
- When a profile is migrated from hourly → 6h, also archive H rows older than 30 days
- When a profile's cron is auto-suspended, archive the file completely (resumes from 0 rows on next activation)

## Real test data (Codified 2026-06-28)

```text
=== H73 sweep size check ===
qa-agent:           195,660 bytes, 117 lines, modified 2026-06-28 06:02 (state.md already past 100K)
engineering-lead:    10,407 bytes,  177 lines, modified 2026-06-28 09:11 (healthy)
operations-manager:  26,947 bytes,  169 lines, modified 2026-06-28 06:01 (healthy)
code-reviewer:        2,215 bytes,   49 lines, modified 2026-06-27 12:01 (very healthy)
security-engineer:    7,766 bytes,  140 lines, modified 2026-06-28 03:02 (healthy)
```

```text
=== Heartbeat 2026-06-28 18:36 size check (confirms compounding) ===
qa-agent:           211,969 bytes, 119 lines, modified 2026-06-28 18:02 (🔴 +16KB in ~12h, H71 sweep)
engineering-lead:    10,407 bytes, 177 lines, modified 2026-06-28 09:11 (stable, no growth)
operations-manager:  35,144 bytes, 192 lines, modified 2026-06-28 18:01 (🟡 +8KB in ~12h from H73, 6h-cadence)
code-reviewer:        2,672 bytes,  50 lines, modified 2026-06-28 12:01 (stable)
security-engineer:    7,766 bytes, 140 lines, modified 2026-06-28 03:02 (stable, daily rotation)
```

**Lesson:** qa-agent is the only profile that bloats because it's the only one on tight hourly cadence writing structured H rows. Other profiles write compact audit summaries (engineering-lead) or have natural rotation (security-engineer's daily findings get reset each scan).

**Heartbeat 18:36 verified workflow (offset/limit pagination works at 212KB):** read qa-agent/state.md with `offset=1, limit=60` for frontmatter + early H rows, then `offset=60, limit=119` for latest H71 + verdict history. Both calls succeeded. The `read_file` limit is on **response size**, not file size.

## Pitfalls

- **DO NOT** try `offset=1` after a 100K+ refusal — same file, same size, same refusal
- **DO NOT** do compaction from a heartbeat/routing-audit sweep — read-only by design (sibling-collision risk with qa-agent's write-only hourly gate)
- **DO NOT** archive H rows based on size alone — they may still be needed for audit (H36/H38 references)
- **DO NOT** truncate the `## Recent Verdicts` table — it's the cross-validation source for 6h routing audits
- **DO** surface bloat in the heartbeat table issues column, every sweep, until user authorizes compaction
- **DO** use `terminal tail` (not `read_file` with offset) when working around the 100K limit — it works in 1 call, not 3

## Related

- `../SKILL.md` — main routing-audit skill
- `references/30min-heartbeat-pattern.md` — 30m cadence variant (where bloat hits hardest)
- `references/cadence-decision-windows.md` — H60 auto-suspend (the policy that needs to be applied to file bloat, not just cadence)
- `~/.hermes/skills/hermes-agent/SKILL.md` → `references/heartbeat-state-md-bloat.md` — actual compaction recipe
