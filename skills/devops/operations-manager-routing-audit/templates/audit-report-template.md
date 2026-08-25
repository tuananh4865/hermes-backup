# Routing Audit Report Template

Copy and modify for each 6h audit tick.

---

# 6h Routing Audit — {YYYY-MM-DD HH:MM}

**Stuck tasks (>2h):** {N}
**Pending QA verification (>1h):** {N}
**Idle agents (>4h):** {N}

**Pipeline health:** {N}/{M} active crons healthy (`hermes cron list` ground truth). {cross-validator} {H<N>} sweep ({HH:MM}, ~{X}h ago) cross-validates independently — 6-check protocol {all pass / N issues}.

**Per-profile snapshot (file mtime at {HH:MM}):**

| Profile | Idle | Cron status | Notes |
|---|---|---|---|
| qa-agent | {X}h | ✅ {cadence} healthy | {H<N>} sweep {status} |
| security-engineer | {X}h | ✅ daily healthy | {verdict} |
| memory-curator | {X}h | ✅ nightly healthy | {last fire} |
| operations-manager | {X}h | ✅ 6h healthy | This audit |
| research-lead | {X}h | ✅ daily healthy | {next run} |
| code-reviewer | {X}h | ✅ {cadence} healthy | {reason for idle} |
| engineering-lead | {X}h | ✅ daily healthy | {last fire} |
| content-director | {X}h | ✅ daily healthy | {last run} |
| default | {X}h | n/a | Session host |
| coder | {X}h | {no cron / status} | {reason} |

**Verdict:** {System idle but pipeline healthy / faults detected / no action required}.

{Optional: Specific observations, fault tracking, recommendations}

**Recommendation:** {None / specific action with rationale}.

---

## Usage Notes

- Replace `{X}` with actual hours/metrics
- Mark ✅ for healthy, ⚠️ for warning, ❌ for fault
- Add rows for any profile not in the standard 10
- Reference qa-agent H<N> verdict for cross-validation
- Update cron truth table inline if any cron is degraded
