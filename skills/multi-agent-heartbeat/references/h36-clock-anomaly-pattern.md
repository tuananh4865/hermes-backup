---
title: H36 clock-anomaly pattern — frontmatter `updated:` lying about write time
observed: 2026-06-26
affects: operations-manager (most common), qa-agent H24-H27, any profile whose cron has been overdue
severity: low (cosmetic) — but causes incorrect freshness classification if trusted
---

# H36 clock-anomaly pattern

## Symptom

A profile's `state.md` frontmatter reads:

```yaml
---
profile: operations-manager
goal: 6h routing audit (cron 2026-06-26 12:00)
updated: 2026-06-26T12:00:00+07:00
---
```

But `stat -f "%Sm"` shows the file was last written at **06:01:44** — 6 hours BEFORE the frontmatter claims.

When a heartbeat reads this file at 13:00 wall time, naive freshness calculation says:
- Frontmatter: 12:00 → 1h ago → FRESH
- Mtime: 06:01 → 7h ago → STALE

These disagree. The heartbeat must pick ONE ground truth to avoid reporting the wrong freshness band.

## Root cause (2 known paths)

### Path 1: cron clock-skew
The cron daemon fired the audit with a drifted system clock. The LLM agent wrote `updated: <intended audit time>` using its own time perception (which matched its prompt context), but the actual `mtime` recorded the real wall clock when the write hit the filesystem.

### Path 2: self-overdue recovery writing intended timestamp
Operations-manager's "self-overdue recovery mode" tells the agent to write `updated: <intended cron tick time>` even when the cron fires 30h late. So the frontmatter documents WHICH scheduled tick the audit claims to fulfill, while the mtime documents WHEN it actually wrote. These are different concepts.

**Real pattern (2026-06-26):** ops-manager H34 wrote `updated: 12:00:00` even though it ran at 06:01:44. The 12:00 timestamp was the INTENDED audit slot; the 06:01:44 mtime was the REAL write time. Subsequent H36 audit at 18:00 wall time faced this discrepancy.

## Recipe — when reading any profile state.md for freshness

```bash
# Step 1: Read frontmatter (intended audit time — may lie)
grep "^updated:" ~/.hermes/profiles/<name>/state.md

# Step 2: Read file mtime (real write time — ground truth)
stat -f "%Sm" ~/.hermes/profiles/<name>/state.md

# Step 3: Read content body timestamp (audit's claimed scheduled tick)
grep -E "cron [0-9-]+T[0-9:]+" ~/.hermes/profiles/<name>/state.md | tail -1

# Step 4: Classify freshness based on mtime (NOT frontmatter)
# FRESH <2h, SOFT-STALE 2-12h, HARD-STALE 12-24h, MISSING >24h
```

**When frontmatter ≠ mtime by >30 min:**
- Trust mtime as ground truth for "when was this file last written"
- Trust content body timestamp for "which scheduled tick this audit claims to fulfill"
- Treat frontmatter as informational only — it reflects the agent's intended audit time, not wall-clock write time
- When reporting freshness, ALWAYS cite mtime, NEVER frontmatter

## Symptom cross-check

If the audit content body references times that math out against the mtime (e.g. "cron gap: 30h late" = 30h before mtime) but NOT against the frontmatter (e.g. frontmatter says 12:00 but mtime says 06:01), then clock anomaly is confirmed and mtime is the ground truth.

## Persistence rule — when ops-manager writes its own state.md

When operations-manager is the WRITER (not the reader), follow this rule to minimize clock-anomaly exposure for future audits:

1. **Write frontmatter `updated:` to the AUDIT TIME (intended)** — the ISO timestamp that names the audit. e.g. for a 2026-06-26 18:00 audit, write `updated: 2026-06-26T18:00:00+07:00`.
2. **Trust file mtime** to record the actual wall-clock write time (system handles this automatically).
3. **In the Routing Log entry, document any drift** between intended and actual: "audit fired at 18:00:27 wall clock (intended 18:00:00, drift 27s — benign)".

This way, the frontmatter is the audit's IDENTITY (which scheduled tick it fulfills), the file mtime is its PHYSICAL TIMESTAMP (when it actually wrote), and any future audit reading the file has both signals to cross-check.

## Real outcomes

| Audit | Frontmatter | Mtime | Drift | Classification | Correct action |
|---|---|---|---|---|---|
| H34 (2026-06-26 12:00 intended) | 12:00:00 | 06:01:44 | 5h58m | SOFT-STALE based on mtime | Cite mtime, not frontmatter; cross-validate with qa-agent H23 |
| H36 (2026-06-26 18:00 intended) | 18:00:00 | (expected ~18:00) | <1m expected | FRESH (post-recovery) | Normal cadence; recovery confirmed |

## Cross-reference

- qa-agent H24-H27 discovered this pattern simultaneously
- Encoded in `multi-agent-heartbeat` SKILL.md Step 3 ("Clock-anomaly in ops-manager freshness check") and operations-manager variant section ("H36 clock-anomaly pitfall")
- Memory fact attempted 2026-06-26 but memory tool was unavailable; lesson is captured in this reference + SKILL.md instead

## Anti-pattern to avoid

❌ **Never** compute freshness as `now - frontmatter.updated`. Always use `now - mtime`.

❌ **Never** patch a state.md file based on frontmatter alone when deciding where to append — use mtime to confirm the file's physical state.

❌ **Never** report "audit at 12:00" to the user when the file's mtime says 06:01. The user cares about reality, not the audit's intended identity.

## Why this matters

A heartbeat that misclassifies ops-manager freshness can:
1. Skip re-derivation when re-derivation is needed (false FRESH → silent drift)
2. Trigger unnecessary re-derivation when audit is actually current (false STALE → wasted tool calls)
3. Mislead the user about whether the system is being monitored

The mtime-vs-frontmatter distinction is the single source of truth for "when did this file last write".