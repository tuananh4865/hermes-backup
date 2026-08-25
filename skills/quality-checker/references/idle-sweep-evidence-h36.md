# H36 Evidence — Frontmatter Future-Timestamp Clock Anomaly

**Sweep:** H24 (2026-06-26 08:00:50 +07:00, qa-agent hourly cron)
**Discovery class:** Mode B idle-sweep edge case
**Severity:** Minor (non-blocking; does not invalidate audit content)
**Companion to:** H20 (audit-freshness vs file-mtime), H34 (three-regime freshness)

---

## The Anomaly

During H24 sweep, ops-manager's state.md frontmatter read:

```yaml
---
profile: operations-manager
goal: 6h routing audit (cron 2026-06-26 12:00)
updated: 2026-06-26T12:00:00+07:00
loop_engineering: enabled
---
```

But the actual system time at sweep execution was **2026-06-26 08:00:50 +07:00**.

The frontmatter `updated:` timestamp is **4 hours in the FUTURE** relative to system time.

This breaks the naive freshness check that every prior sweep used:

```python
# Naive (WRONG for H36 case):
age = system_time - frontmatter.updated
if age < 2h: regime = FRESH  # ← this returns "audit is -4h old" — nonsensical
```

If qa-agent had used only the frontmatter for freshness classification, it would have:
1. Concluded ops-manager audit is "in the future" (= cannot be stale yet)
2. Failed to apply the H23 cross-validation recipe
3. Re-derived from primary reads unnecessarily (wasted tokens)
4. OR worse, treated the negative age as an error and escalated to Orchestrator

---

## How H24 Resolved It Correctly

H24 followed the H20 lesson ("measure freshness by content timestamp + file mtime, NOT frontmatter alone") and added a new check:

```python
# Step 1: Compute frontmatter age
frontmatter_age = frontmatter.updated - system_time()

# Step 2: Classify the SIGN of the age
if frontmatter_age < 0:
    # CLOCK_ANOMALY: frontmatter is in the future
    # DO NOT use frontmatter for freshness
    # Fall back to file mtime + audit content body
    pass

# Step 3: Cross-reference with file mtime
file_age = system_time - stat_mtime  # 2026-06-26 06:01:44 → ~2h old at 08:00

# Step 4: Cross-reference with audit content body
# Routing Log line: "2026-06-26 12:00: 6h routing audit (cron)..."
# Wait — that ALSO says 12:00. But the audit body references "cron gap: 30h late"
# which is consistent with content written at 06:01 (06:01 - 30h = 00:01 yesterday).

# Step 5: Decide ground truth
# File mtime is the OS-level canonical write time. Trust mtime over body text
# when they disagree. Body "12:00" is a copy-paste from a pre-stamped template.
```

**Conclusion:** ops-manager audit content was written at file mtime 06:01:44 today (≈2h old at sweep time) → **FRESH regime**. Body text "12:00" is template echo, not actual write time. The 12:00 frontmatter is the same template echo.

No fault detected. Audit is reliable. Cross-validation recipe applied (H23). Sweep verdict: PASS.

---

## H20 vs H36 — Distinction Table

| Aspect | H20 (past staleness) | H36 (future frontmatter) |
|---|---|---|
| Symptom | `stat -f %m` recent, but content old | `stat -f %m` and content old, but frontmatter is FUTURE |
| Why it fools you | `mtime` looks fresh because other sweeps touched file | frontmatter looks fresh because clock is skewed / template echo |
| Detection | Read audit content body, compare to `stat -f %m` | Compute `frontmatter.updated - system_time()`; if negative, skip frontmatter |
| Fallback ground truth | Audit content body + body timestamp | File `stat -f %m` + audit content's "cron gap: Nh late" math |
| Severity | Warning (audit was genuinely stale, risk of propagating stale data) | Minor (audit is FRESH, just frontmatter has clock skew) |
| Action | Re-derive from primary reads | Trust audit content, log anomaly, do not escalate |

**Key takeaway:** H20 detects past staleness; H36 detects future frontmatter. Both require NOT trusting a single signal — cross-reference ≥2 sources (frontmatter + mtime + content body) before classifying regime.

---

## Root Cause Hypothesis

The most likely cause is one of:

1. **Template-echo bug:** When ops-manager's profile was last regenerated/templated, the frontmatter `updated:` field was hardcoded to a future timestamp (e.g., "next expected cron run") rather than dynamically generated. Subsequent sweeps then never updated the frontmatter, leaving it stale-but-future.

2. **Cron clock skew:** The cron daemon or operations-manager script uses a different time reference (UTC vs +07:00, or a drifted system clock) when writing the frontmatter. Body content uses real time; frontmatter uses the daemon's clock.

3. **Manual frontmatter edit:** Someone manually edited the frontmatter at 12:00 with intent to "stamp next audit time," but did not realize this would confuse future freshness checks.

None of these block the audit's correctness. The audit content body + file mtime are sufficient ground truth.

---

## When to Apply This Lesson

Apply H36 detection when **all of** the following are true:
- ✅ Sweep is in Mode B (idle sweep)
- ✅ ops-manager (or other audited profile) frontmatter is being read for freshness
- ✅ `frontmatter.updated - system_time()` is negative (frontmatter ahead of system clock)
- ✅ File mtime + content body are NOT also in the future (they're normal)

If file mtime IS in the future too, the whole system has clock skew — escalate to Orchestrator.

---

## Companion Lessons

- **H20** (`references/idle-sweep-evidence-h20.md`) — original audit-freshness vs mtime pitfall (past staleness)
- **H22** (`references/idle-sweep-evidence-h22.md`) — forecast-realization tracking + 4-read token-economy scope
- **H34** (`references/idle-sweep-evidence-h34.md`) — three-regime freshness classification (fresh/stale/massively-stale)
- **H23** (SKILL.md body) — cross-validation token-economy recipe (skip primary re-derivation when ops-manager is FRESH)

H36 EXTENDS H20 (now bidirectional: past staleness + future frontmatter) without superseding it.

---

## Recipe Code (pseudocode for future sweeps)

```python
def classify_ops_manager_audit_freshness(system_time, file_mtime, frontmatter_updated, audit_body):
    """Returns: (regime, ground_truth_age, anomaly_note)"""
    
    frontmatter_age_hours = (frontmatter_updated - system_time).total_seconds() / 3600
    mtime_age_hours = (system_time - file_mtime).total_seconds() / 3600
    
    # H36: frontmatter is in the future
    if frontmatter_age_hours < 0:
        anomaly = f"CLOCK_ANOMALY: frontmatter {abs(frontmatter_age_hours):.1f}h in future"
        # Trust mtime as ground truth (H20 lesson)
        ground_truth_age = mtime_age_hours
        # Sanity-check body text for consistency
        body_age = parse_audit_body_cron_gap(audit_body)
        if abs(body_age - mtime_age_hours) > 1.0:
            anomaly += f" + body age mismatch ({body_age:.1f}h vs mtime {mtime_age_hours:.1f}h)"
        regime = "FRESH" if ground_truth_age < 2 else ("STALE" if ground_truth_age < 24 else "MASSIVELY_STALE")
        return regime, ground_truth_age, anomaly
    
    # H20: frontmatter is in the past but mtime is fresher
    if abs(mtime_age_hours - frontmatter_age_hours) > 2.0:
        anomaly = f"MTIME_FRESHER: mtime {mtime_age_hours:.1f}h vs frontmatter {frontmatter_age_hours:.1f}h"
        ground_truth_age = mtime_age_hours
    else:
        anomaly = None
        ground_truth_age = frontmatter_age_hours
    
    regime = "FRESH" if ground_truth_age < 2 else ("STALE" if ground_truth_age < 24 else "MASSIVELY_STALE")
    return regime, ground_truth_age, anomaly
```

---

*Captured: 2026-06-26 08:00 (H24 sweep) by qa-agent*
*Companion to: SKILL.md v2.5.7, H24 pitfall block*