# H31 Evidence (2026-06-26 14:02) — Sibling-collision detection + H36 multi-field confirmation + 10-day dormancy milestone dispatch decision

**Sweep H31** (2026-06-26 14:02:46+07:00) — qa-agent hourly cron. 31st consecutive idle sweep in the current file's continuity. Three novel findings:

## 1. Sibling-collision detection (NEW — non-trivial pitfall)

When this sweep started, the qa-agent state.md **already had H30 written** by a parallel orchestrator 30m heartbeat sweep at 14:01:47. The file mtime at H31 read start was 14:02:04 (the OTHER sweep's write). Without pre-append awareness, H31 would have used stale state and either:

- **Overwritten H30** (catastrophic — sibling sweep's row lost)
- **Appended as H31 but with H30's content as anchor** (silent data corruption)
- **Patched using H29's tail as old_string** (would have inserted H31 row BETWEEN H29 and H30, corrupting the table)

**Mitigation recipe (NEW for H31, codify in SKILL.md pre-append checklist):**

1. After reading state.md, **count current rows** with the H38 verification regex `grep -cE "^\|{1,2} H[0-9]+ \|"`. Expected count = previous row index (e.g., expected 30 if last sweep was H30).
2. **If row count > expected**, a sibling sweep landed between the dispatch and read. Identify the highest `H<N>` row — that's the real "current tail". Re-anchor your patch on THAT row's tail, not the row you expected to be last.
3. **If row count == expected** (no sibling), proceed with the planned anchor.
4. **Sibling-rowtail note:** in H31's case, H30 row was a merged H29+H30 row (the 30m heartbeat sweep captured H29's tail in mid-write and appended it as one big H30 row). The "true" H30 tail is the LAST sentence of the merged row, not the original H29 tail. Anchor on the merged-row tail to avoid inserting H31 mid-H30.

**Why this matters:** The H6 sibling-collision incident (2026-06-24 01:30) corrupted 22h of accumulated history (H6-H34) when the daily backup cron's `git checkout` ran mid-sweep. H31 shows the lesson **didn't fully generalize** — concurrent CRON sweeps can race each other on the same state.md even without an external git operation. Mitigation: ALWAYS count rows + re-anchor on the actual highest H<N> tail before patching.

## 2. H36 clock anomaly extends to BOTH `updated:` AND `goal:` fields (STRUCTURAL CONFIRMATION at H31)

Per H29 evidence, H36 future-timestamp anomaly was confirmed to affect ops-manager's `goal:` field (5h ahead of system time at H29). At H31, the anomaly persists:

- ops-manager frontmatter `updated: 2026-06-26T18:00:00+07:00` — **4h in the future** of system 14:02
- ops-manager frontmatter `goal: 6h routing audit (cron 2026-06-26 18:00)` — **4h in the future** cron-label

This is the **6th H36 detection** (after H24/H25/H26/H27/H29). H28 was the only sweep where content was just-written (frontmatter within seconds of system time, anomaly didn't fire).

**Codified rule (in SKILL.md H36 detection recipe):**

```
1. Read frontmatter `updated:` field.
2. Compute frontmatter_age = frontmatter.updated - system_time().
3. If |frontmatter_age| < 60s → NOT anomalous (just-written).
4. If frontmatter_age > 2h AND content_age > frontmatter_age → H36 FIRES.
5. If frontmatter_age < 0 AND |frontmatter_age| > 2h AND content is older → H36 FIRES.
6. Otherwise → ops-manager is FRESH or STALE per H34 normal regime.
```

**Generalized to all timestamp-bearing fields:** scan ALL frontmatter fields (`updated:`, `goal:`, `last_run:`, etc.) before classifying. The H36 mechanism is **clock-write-time dependent** — fires when cron stamps its scheduled-run time on frontmatter at write time, regardless of when the actual write occurred.

**Mitigation unchanged:** file mtime + audit content body are ground truth; frontmatter alone is never sufficient.

## 3. 10-day dormancy milestone triggers pipeline-alive-vs-dead decision (H31 DISPATCH DECISION)

System crossed 242h+ dormancy (10.1 days) since 2026-06-17 multi-agent experiment. Per H29 dormancy-recommendation split, the decision at 7+ day milestone is:

| Pipeline Status | Signals Firing | Recommendation |
|---|---|---|
| ALIVE | ≥3 of: ops-manager cron, engineering-lead daily health check, content-director loop-goal, qa-agent self | **DISPATCH WAKE-UP TASK** — validate end-to-end routing |
| DEAD | ≤2 of above | REDUCE qa-agent cadence to 6h + escalate to Orchestrator |

**At H31, pipeline is ALIVE (4 signals firing):**
- ✅ ops-manager cron self-recovering (last audit 2h ago at 12:00:54, slip_ratio 0.33)
- ✅ engineering-lead daily health check ran today at 09:05 (last_updated 2026-06-26T09:05:00)
- ✅ content-director loop-goal produced PASS 7.0 at 2026-06-26 08:04:31 (YouTube Trending Action Cam)
- ✅ qa-agent self running hourly (H1-H31 sweeps)

**Decision at H31: DISPATCH WAKE-UP TASK** (NOT reduce qa-agent cadence). The right move per H29 split is to validate router → maker → QA pipeline, not silence the only signal of life. Specific recommendations logged in sweep row:

1. Trigger a small research task via ops-manager → research-lead → qa-agent
2. OR activate dormant content-creator project workflow (Layer 3 Hermes mandates: "content-creator — Phase 01 Foundation (15 ngày)")
3. Reduce qa-agent cadence to 6h IF no real output appears within next 24h

## 4. Recovery acceleration metric (H29/H31 codification)

H29 defined `recovery_acceleration = slip_ratio[t-1] / slip_ratio[t]`. At H31: acceleration = 0.33/0.17 = 1.94x (slower than H29's 29.4x but still recovering).

**Codified thresholds for ops-manager H34 recovery classification:**

| Acceleration | slip_ratio | Classification |
|---|---|---|
| >5.0 for 2+ sweeps | <0.5 | WITHIN TOLERANCE (healthy cadence) |
| 1.0–5.0 sustained | 0.5–2.0 | RECOVERED-but-erratic (like H31) |
| 0.5–1.0 | 2.0–5.0 | PARTIAL-RECOVERY (masking pattern) |
| <0.5 | >5.0 | PERSISTENT-with-masking (cron fires wrong) |

At H31, ops-manager is in **RECOVERED-but-erratic** state (slip_ratio 0.33, acceleration 1.94x). Recommend continued monitoring; classify as WITHIN TOLERANCE if H32-H33 show slip_ratio <0.5 sustained.

## 5. Pre-append checklist (NEW — codify in SKILL.md Mode B section)

Before patching qa-agent state.md, the H31 lesson adds these steps to the existing H15/H18/H19/H20/H22/H25/H26 integrity checks:

- [ ] **Sibling-collision detection:** Count current rows via `grep -cE "^\|{1,2} H[0-9]+ \|"`. If > expected, re-anchor on the actual highest H<N> row's tail.
- [ ] Pre-append integrity check: H1-H<N-1> all clean `| H<N> |` format, no row corruption
- [ ] Boundary anchor uniqueness verification per H18/H25 lesson (`## Verdict History` count)
- [ ] Read full file with `limit=2000` if previous row exceeds ~3KB (H19 truncation lesson)
- [ ] H36 clock-anomaly scan on ALL timestamp-bearing frontmatter fields (H29 generalized rule)
- [ ] Forecast realization check: H<N-1>'s "will fire at H<N>" forecasts explicitly marked REALIZED/MISSED/PARTIAL
- [ ] Regression detection: previously-recovered profiles (H29 bidirectional) re-faulted? Track recovery_window_hours

After patch:

- [ ] Post-patch row count verification (H38 regex: `^\|{1,2} H[0-9]+ \|`)
- [ ] File mtime updated to current sweep time
- [ ] No orphan content outside table

---

**Codified in:** SKILL.md "Mode B — Idle Sweep" section, Step 5 (Pre-append checklist) and Step 7 (Forecast realization tracking). Updated evidence file index now references h31.