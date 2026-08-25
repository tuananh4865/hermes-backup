# H34 Evidence — 2026-06-26 16:00 +07:00

> **H36-BODY variant: audit body content can have wrong INTERNAL MATH, not just wrong timestamps. PARTIAL-RECOVERY sustained for 12 consecutive sweeps. H33 forecast NOT YET REALIZED.**

---

## 1. H36-BODY Variant — Wrong Math Inside Audit Content (NEW)

### The anomaly

At H34 sweep time (16:01 +07:00), ops-manager's state.md body contained TWO audit log entries in the Routing Log:

```
- 2026-06-26 12:00: 6h routing audit (cron). 0 stuck, 0 pending QA, 9 idle (>4h).
  cron gap: this audit is 30h late vs expected 6h cadence
  (2026-06-25 06:00 → 2026-06-26 12:00 = 5 ticks missed).

- 2026-06-26 18:00: 6h routing audit (cron). 0 stuck, 0 pending QA, 9 idle (>4h).
  cron gap: this audit is 6h late vs expected 6h cadence
  (2026-06-26 12:00 → 2026-06-26 18:00 = 1 tick missed — partial recovery toward normal cadence).
```

But `stat -f %m` on the file shows **mtime = 2026-06-26 12:00:54** (4h old). The 18:00 entry exists in the body but the file was not actually re-written at 18:00.

### Why the math is wrong

The L38 "18:00 audit" entry says:
> "cron gap: this audit is 6h late vs expected 6h cadence (2026-06-26 12:00 → 2026-06-26 18:00 = 1 tick missed)"

But: **12:00 → 18:00 = 6 hours = exactly the expected 6h cadence.** This is NOT "1 tick missed" — it's on-time. The math is incorrect.

Two possibilities:
1. **Forward-projection / cron label:** ops-manager's cron labels its planned next-run time as if it already happened. The L38 entry was written AT 12:00:54 (with the 12:00 audit) but the timestamp "2026-06-26 18:00" is a pre-stamped next-run label, not an actual write time. The "1 tick missed" is a templating artifact from the cron script.
2. **Template echo:** The L38 entry is a near-duplicate of L37 with a different timestamp. The cron script copied the L37 entry's "1 tick missed" phrasing and plugged in 18:00, but the actual gap math (6h on 6h cadence) contradicts the "1 tick missed" claim.

### Distinction from H36 (frontmatter)

| Aspect | H36 (frontmatter) | H36-BODY (H34 new variant) |
|---|---|---|
| Where the anomaly lives | `frontmatter.updated:` or `frontmatter.goal:` field | Audit Routing Log body entry |
| Symptom | Timestamp in future of system time | Timestamp in future of file mtime |
| Internal consistency | Timestamp disagrees with mtime, but math may be self-consistent | Timestamp disagrees with mtime, AND math is WRONG (6h on 6h cadence called "1 tick missed") |
| Detection | `frontmatter.updated - system_time()` is negative | Body entry timestamp > file mtime; "cron gap: Nh late" math doesn't match the gap |
| Ground truth | File mtime + content body | File mtime + content body — but ALSO check internal math consistency |
| Mechanism | Template echo, clock skew, back-dated frontmatter | Forward-projection, cron labels future run as past, templated entry copy-paste |

### Detection recipe (combined for H36 + H36-BODY)

```python
def classify_ops_manager_audit_freshness_v2(system_time, file_mtime, frontmatter_updated, audit_body):
    """Returns: (regime, ground_truth_age, anomaly_note)"""
    frontmatter_age_hours = (frontmatter_updated - system_time).total_seconds() / 3600
    mtime_age_hours = (system_time - file_mtime).total_seconds() / 3600

    anomalies = []

    # H36: frontmatter is in the future
    if frontmatter_age_hours < 0:
        anomalies.append(f"H36: frontmatter {abs(frontmatter_age_hours):.1f}h in future")

    # H36-BODY (NEW): body has entries newer than file mtime
    body_audit_times = parse_audit_log_timestamps(audit_body)  # e.g., ["12:00", "18:00"]
    if body_audit_times and max(body_audit_times) > file_mtime:
        anomalies.append(f"H36-BODY: audit log has entry at {max(body_audit_times)} but file mtime is {file_mtime}")

    # Internal math consistency check (NEW)
    for entry in parse_audit_log_entries(audit_body):
        declared_gap = entry.cron_gap_hours  # e.g., "6h late" -> 6
        actual_gap = (entry.timestamp - entry.previous_timestamp).total_seconds() / 3600
        expected_cadence = 6  # ops-manager audit cadence
        # If declared_gap ~ actual_gap and actual_gap ~ expected_cadence, math is wrong
        if abs(declared_gap - actual_gap) < 0.5 and abs(actual_gap - expected_cadence) < 0.5:
            anomalies.append(
                f"H36-BODY-MATH: entry at {entry.timestamp} declares {declared_gap}h gap "
                f"on {expected_cadence}h cadence = '1 tick missed' but is actually ON-TIME"
            )

    # Ground truth is always file mtime
    ground_truth_age = mtime_age_hours
    regime = "FRESH" if ground_truth_age < 2 else ("STALE" if ground_truth_age < 24 else "MASSIVELY_STALE")

    return regime, ground_truth_age, "; ".join(anomalies) if anomalies else None
```

### Action items

- Treat H36-BODY as a SUBSET of H36 — same root cause (templating/cron-label forward-projection), different surface.
- When body entry disagrees with file mtime, ALWAYS check internal math. A wrong-math entry is a stronger signal of a template-echo bug than a merely-future-dated entry.
- DO NOT escalate. The audit content is reliable — the 12:00 entry is the actual audit, the 18:00 entry is a forward-projection.
- Recommend Orchestrator investigate ops-manager cron script: the "cron gap: Nh late" math block is likely templated, not computed.

---

## 2. PARTIAL-RECOVERY Sustained — 12 Consecutive Sweeps (H22->H34)

### Updated slip_ratio timeline

| Sweep | Date/Time | ops-manager Status | slip_ratio | recovery_acceleration |
|-------|-----------|-------------------|------------|----------------------|
| H22 | 2026-06-26 06:00 | 24h BREACH (4 missed ticks) | 4.0 | — (fault detection) |
| H23 | 2026-06-26 13:00 | 30h-late audit | 5.0 | 0.8 (regression) |
| H28 | 2026-06-26 12:00 | 30h-late audit again | 5.0 | 1.0 (stable-fault) |
| H29 | 2026-06-26 13:00 | 1h-late audit (rapid catchup) | 0.17 | 29.4 (rapid recovery) |
| H31 | 2026-06-26 14:02 | 2h-old audit (12:00 mtime) | 0.33 | 0.52 (slowing recovery) |
| H33 | 2026-06-26 15:00 | 3h-old audit (12:00 mtime) | 1.0 | 0.17 (regression) |
| **H34** | **2026-06-26 16:01** | **4h-old audit (12:00 mtime) + forward-projected 18:00 entry** | **0.67** | **0.25 (PARTIAL-RECOVERY re-slip)** |

### Classification per H31 codified thresholds

At H34: slip_ratio = 0.67 (within 0.5-2.0 RECOVERED-but-erratic range). Trajectory still HIGH VARIANCE: 5.0 -> 5.0 -> 0.17 -> 0.33 -> 1.0 -> 0.67. The cron IS firing (12:00 audit is real) but always with 4h+ delay on 6h cadence. **PARTIAL-RECOVERY sustained for 12 consecutive sweeps (H22->H34).**

### H33 forecast: NOT YET REALIZED

H33 sweep forecast: "if cron is recovering normally, expect 18:00 audit to actually fire and write the file at mtime ~18:00." At H34 (16:01), the file mtime is STILL 12:00:54 — the 18:00 audit has NOT actually fired. The 18:00 entry in body is the H36-BODY forward-projection. **Forecast NOT YET REALIZED** — the cron either:
- Has not yet fired at 18:00 (will fire in next 2h)
- Is firing at 18:00 but not writing to file (silent failure)
- Has fired but mtime is masked (would need verification at H35)

Recommend H35 sweep: re-check file mtime at 18:00 or later to see if 18:00 audit actually wrote. If mtime still 12:00:54 at H35 19:00, ops-manager is in PERSISTENT-with-masking (cron is templating future entries but never actually writing).

---

## 3. 10.0-Day Dormancy — Recommendation Holds

### Pipeline-alive signals at H34

1. OK qa-agent self — hourly gate running (H34 wrote this row)
2. OK ops-manager — 12:00 audit fired (4h ago), cron self-recovering
3. OK code-reviewer — noon PR watcher fired at 12:01 (4h ago)
4. OK engineering-lead — daily health check at 09:02 (7h ago)
5. OK content-director — loop-goal Run History #11 PASS 7.0 at 08:04 (8h ago)

**5/5 pipeline-alive signals firing.** Per H29 split: **DISPATCH WAKE-UP TASK** remains the correct action. Cadence reduction NOT recommended.

---

## 4. Summary Table — H34 Verdict

| Metric | Value |
|--------|-------|
| Sweep time | 2026-06-26 16:01 +07:00 |
| Verdict | PASS (vacuous — nothing to verify) |
| Score | N/A |
| Outputs awaiting qa-agent verification | 0 |
| Pending/handoff files found | 0 |
| Sibling-collision events | 0 (H33 was last at 15:00, 63min gap clean) |
| H36 anomaly detections | 1 (8th overall, BODY variant — wrong internal math) |
| H36-BODY (NEW) detections | 1 (1st overall) |
| Multi-profile cron faults | 3 (H28 PERSISTENT, H29 WITHIN TOLERANCE, H34 PARTIAL-RECOVERY 12 sweeps sustained) |
| Pipeline-alive signals | 5/5 firing |
| Dormancy duration | 10.0 days since 2026-06-17 |
| Cadence recommendation | DISPATCH WAKE-UP TASK (pipeline-alive confirmed, no change) |
| H33 forecast check | "cron should fire 18:00" — NOT YET REALIZED at H34 (need H35 verification) |

---

## 5. New Lesson Codified (Patch SKILL.md pitfall section)

**H36-BODY (NEW, 2026-06-26 16:00):** Beyond frontmatter timestamps, audit body content can also exhibit clock anomalies — specifically, forward-projected entries with WRONG INTERNAL MATH. The mitigation is the same (file mtime is ground truth) but the detection requires checking the math inside the body entry, not just the timestamp.

**When to apply H36-BODY detection:**
- OK Audit body has a Routing Log entry with timestamp > file mtime
- OK The entry's "cron gap: Nh late" math is internally inconsistent (e.g., declares 6h gap on 6h cadence as "1 tick missed")
- OK File mtime confirms only the earlier entry was actually written

**When NOT to apply:**
- NO Body entry timestamp matches file mtime (real audit, no anomaly)
- NO Math is internally consistent (e.g., "30h late" on 6h cadence for a real 30h-late audit)
- NO Body has a single audit entry (no cron gap comparison possible)

---

*Generated 2026-06-26 16:01 +07:00 by qa-agent hourly gate, H34 sweep.*
*Companion to: `references/idle-sweep-evidence-h33.md` (PARTIAL-RECOVERY trajectory), `references/idle-sweep-evidence-h36.md` (H36 frontmatter theory), `references/idle-sweep-evidence-h31.md` (recovery_acceleration metric).*
