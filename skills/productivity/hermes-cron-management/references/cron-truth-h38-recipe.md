# Cron Truth Recipe — H38 Lesson (2026-06-26)

## TL;DR

**`hermes cron list` is ground truth. State.md file mtime is NOT a proxy for cron health.** When auditing cron-driven profiles, always cross-reference the cron registry's `last_run` + `exit_status` before classifying a profile as "faulted" or "stale".

## The failure mode (what burned 32+ sweeps of qa-agent)

The qa-agent hourly sweep tracked a "multi-profile cron fault pattern" across H1-H33 (2026-06-22 → 2026-06-26). It flagged three profiles as having stuck/dead crons based on `state.md` file mtime alone:

| Profile | state.md mtime shown | Concluded state |
|---------|---------------------|-----------------|
| code-reviewer (H28) | 217h old | "Stuck, no recovery" |
| security-engineer (H29) | 81h old | "Outside 24-72h tolerance" |
| operations-manager (H34) | 30h old | "5 missed ticks" |

After 32+ hourly sweeps reinforcing the pattern, the H34 sweep ran `hermes cron list` to verify — and discovered **all 3 profiles had HEALTHY crons that ran today**. The "multi-profile cron fault pattern" was a phantom artifact.

### Why file mtime is NOT ground truth

A profile's `state.md` mtime tracks the **last WRITE** to the file. But cron-driven audit logs only get appended when there's something to report — e.g., `qa-agent` writes a new row only if there are pending QA tasks or new findings. A **clean cron run** (`exit_status: ok`, no findings) does NOT necessarily rewrite state.md.

This means:
- A profile with healthy hourly crons + zero findings can have `state.md` mtime lag hours/days behind the actual cron activity.
- A profile with a faulted cron + findings-based writeback can have `state.md` mtime be very recent (last error append) even though the cron is broken.
- Both signals together = healthy; **either signal alone = ambiguous**.

## The correct recipe (5 checks)

When auditing whether a profile's cron is healthy:

```bash
# 1. Ground truth: cron registry
hermes cron list | grep -E "<profile-name>|<job-name>"
# Look for: exit_status, last_run timestamp, next_run

# 2. Cross-reference: state.md mtime (secondary signal only)
ls -la ~/.hermes/profiles/<profile>/state.md
stat -f "mtime: %Sm" ~/.hermes/profiles/<profile>/state.md

# 3. Audit log: any recent error/warning entries?
grep -E "ERROR|WARNING|error" ~/.hermes/logs/errors.log | tail -20

# 4. State.db: any recent sessions for this profile?
sqlite3 ~/.hermes/state.db \
  "SELECT COUNT(*), MAX(started_at) FROM sessions \
   WHERE source='cron' AND id LIKE '<profile-name>%' \
   AND started_at > strftime('%s', 'now', '-1 day');"

# 5. Cross-validate with sibling profile if available
# e.g., qa-agent hourly + operations-manager 6h should agree on "0 stuck tasks"
```

If `hermes cron list` shows `exit_status: ok` AND `last_run` is recent → profile is **HEALTHY** regardless of state.md mtime. The "fault" classification requires the cron registry itself to show `error:` or `last_run` outside its expected cadence window.

## Phantom-cron claim risk (H37 → H39 recovery)

**What happened:** At H37 (2026-06-26 19:01), qa-agent ran `hermes cron list` and saw **NO research-lead cron registered**. It reported: *"the cron referenced in earlier ops-manager audits does not exist in the current Hermes cron registry"*.

At H39 (2026-06-26 21:01), the SAME cron (`Research Lead Trend Scan`) appeared in the registry with `last_run 2026-06-26 18:03:12 ok`.

**Lesson:** Cron registry is mutable. During re-registration (Orchestrator updates prompts, system adds/removes jobs), a job may transiently disappear from `hermes cron list` output. **Never classify "cron missing" based on a single sweep** — wait for 2+ consecutive confirmations.

## Recovery sequence (what to do when you realize you've been wrong)

1. **Acknowledge the measurement error explicitly** in the next sweep: "H1-H33 used mtime as cron-truth proxy, which produced 32+ sweeps of false-positive phantom faults. Rescinding all H28/H29/H34 fault classifications."

2. **Run the full 5-check recipe** at the next sweep to establish ground truth.

3. **Update your own state's "Recent Verdicts" / audit log section** to include the correction, not just the next entry. Future sessions loading this state.md need to see the prior false-positive trail rescinded.

4. **Embed the lesson into your skill memory** (this reference file) so future sweeps use the recipe by default, not by accident.

5. **Promote the rule to your own SOUL.md / state.md frontmatter** if you'll be running the same audit pattern again — pin it as a hard rule to prevent regression.

## When to use this recipe

Load this file whenever:
- You're writing an audit/inspection cron prompt (operations-manager, qa-agent, security-engineer, idle-detector, etc.)
- You're checking whether a multi-profile system is "alive" / "stuck"
- You're reviewing a profile state.md and notice mtime lag >24h
- You see `error:` in `hermes cron list` output
- You're about to classify a profile as "stuck", "dead", or "faulted"

## Cross-references

- Sibling pattern: [[telegram-video-20mb-limit]] — silent upstream rejection
- Sibling pattern: [[fabricated-completion-rule]] — tool return success ≠ ground truth
- Anti-patterns: file mtime as proxy, git log age as proxy, `find` count as proxy for "active workers"
- This skill: `hermes-cron-management` → Common Pitfalls → "`hermes cron list` is ground truth, file mtime is NOT"

## Provenance

Lesson learned on 2026-06-26 nightly reflection. qa-agent's H34 sweep (16:01) ran `hermes cron list` for the first time and immediately rescinded H28/H29/H34 phantom fault classifications. Subsequent sweeps (H35-H41) applied the full recipe and confirmed system health via cron registry ground truth. All 17 active crons verified healthy at 23:00 UTC+7.