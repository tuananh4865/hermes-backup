# H68 Anomaly-Within-Self-Verdict Recipe (2026-06-28 00:01) — NEW PERMANENT PATTERN

> **Companion to the H28 scope discipline section in SKILL.md.** This reference
> documents the third action branch qa-agent can take when observing profile-owned
> self-verdict entries: observe-and-flag-without-spawning-work.

---

## The Gap (why this recipe exists)

The H28 scope discipline section in `SKILL.md` provides a binary decision tree
for profile-owned entries (engineering-lead daily health, content-director Run
History, security-engineer daily scan, operations-manager audit log):

- **H28 default:** "Skip — these are PROFILE-OWNED, not pending qa-agent re-verification."
- **H28 exception:** Real security CRITICAL findings always escalate via the H29/security-engineer path, separate from the scope discipline.

But H28 does **not** cover what qa-agent should do when a sweep observes a
**data anomaly** within a profile-owned self-verdict entry — something that
looks wrong but is not a security finding and not a maker task handoff.

Real case (H68, 2026-06-28 00:01):

- content-director's Run History #12 (2026-06-27 08:03:57, "YouTube Trending Lens")
  showed **Result=PASS but Score=0.0** — loop-goal recorded a self-verdict as
  PASS but failed to compute a real score.

Three possible responses:

1. **Ignore the anomaly entirely** → signal lost, loop-goal continues with broken score computation.
2. **Treat as maker task handoff** → spawn verification work that doesn't fit (loop-goal self-verdicts are NOT in the maker-handoff model).
3. **Note in sweep row, classify as scope-discipline-bounded, escalate signal to Orchestrator via the sweep row itself** (not via separate escalation path). ✅

## The Recipe (H68 — Permanent)

When a qa-agent idle-sweep observes a profile-owned self-verdict entry (per H28
scope discipline) that contains anomalous data:

1. **DO** apply H28 scope discipline → entry is NOT pending qa-agent verification. Do not switch to Mode A.
2. **DO** note the anomaly in the sweep row's "Notable Observations" / "Per-profile status" section with:
   - Specific data point that looks wrong (e.g., "Score=0.0 with Result=PASS")
   - Source profile + entry identifier (e.g., "content-director Run History #12")
   - Loop-goal run type / context (e.g., "YouTube Trending Lens 2026-06-27")
3. **DO** classify explicitly: "NOT triggering verification action (not a maker task handoff), but flagging for Orchestrator awareness."
4. **DO** NOT spawn separate escalation, separate handoff file, or Mode A switch. The sweep row IS the escalation channel.
5. **DO** leave the profile-owned self-verdict entry untouched in its source profile — qa-agent does not modify maker state files for observation-only findings.
6. **DO** forecast: "If anomaly persists at H<N+1>, the underlying loop-goal/profile script may have a bug worth investigating by Orchestrator." Future sweeps should re-check the same field.

## Why this is distinct from H28

| Aspect | H28 (scope discipline) | H68 (anomaly-within-self-verdict) |
|---|---|---|
| Trigger | Any profile-owned self-verdict entry | Profile-owned self-verdict with anomalous DATA |
| Action | Skip (don't verify) | Observe + flag (don't verify, don't ignore) |
| Output channel | None (silent skip) | Sweep row "Notable Observations" section |
| Escalation path | None | Sweep row itself (no separate escalation) |
| Mode switch | Stay in Mode B | Stay in Mode B (no Mode A) |
| Future behavior | Same skip on next sweep | Re-check on next sweep for persistence |

H28 is binary: verify / don't verify. H68 adds a third action: **observe / flag / don't act**.

## When to use H68

- Sweep observes a profile-owned entry (per H28 list) that contains visibly anomalous data
- Anomaly is NOT a security CRITICAL finding (those escalate via security-engineer path, separate)
- Anomaly is NOT a "0 stuck / 0 pending / N idle" ops-manager audit log (those are H34-cadence-only signals)
- Anomaly is NOT a "broken state.md" file integrity issue (those are H44/H52 anchor-pitfall territory)

**Don't use for:**

- A "loop-goal PASS 7.0" entry with no data anomalies → normal H28 skip
- A security-engineer CRITICAL finding → security-engineer escalation path
- An ops-manager audit content with wrong math → H36-BODY pattern, separate

## Real H68 case summary

content-director Run History #12 anomaly: Score=0.0 with Result=PASS. Loop-goal
recorded a self-verdict but failed to compute a real score for the YouTube
Trending Lens run type.

**Per H68 action taken:**
- Noted in H68 sweep row under "Content-director Run History #12 verification (NOT a new pending output, but anomaly check)"
- Classified as loop-goal self-run (NOT a maker task handoff)
- Flagged for Orchestrator awareness in the sweep row
- No separate escalation spawned
- Forecast: at H69, re-check content-director Run History to see if loop-goal's scoring bug is consistent or transient

## Why this rule is permanent

- Sweeps that observe anomalies in self-verdict entries face the dilemma: ignore (lose signal) or escalate (spawn unnecessary work). H68 codifies the middle path.
- The H28 binary "verify / don't verify" decision tree has been qa-agent's default for 30+ sweeps. H68 adds a 3rd branch (observe / flag / don't act) for cases where the data is clearly off but doesn't fit the maker-handoff model.
- Future sweeps at H69+ will encounter similar anomalies (loop-goal bugs, profile script drift, content-director scoring issues). H68 provides a pre-decided path so the sweep doesn't have to re-derive the right action each time.
- Pattern generalization: the H28 + H68 pair forms a 3-state model for profile-owned entries: (1) clean data → skip silently (H28), (2) anomalous data → note + flag in sweep row (H68), (3) security CRITICAL → separate escalation path (H29). This 3-state model is more complete than H28's binary.

## H68 sweep row template (recommended)

```
**Notable Observations:**

- **[profile-name] Run History #[N] anomaly** (NOT a new pending output, but anomaly check):
  - Data point: [what looks wrong, e.g., "Score=0.0 with Result=PASS"]
  - Context: [loop-goal run type / timestamp / entry identifier]
  - Classification: loop-goal self-run per H28 scope discipline
  - Action: NOT triggering verification, flagging for Orchestrator awareness
  - Forecast: re-check at H<N+1> to see if anomaly persists
```

This template keeps the anomaly visible in the sweep row (Orchestrator sees it),
explicitly bounds the scope (no verification spawned), and provides a forecast
(future sweep will re-check) — all without polluting the Pending/Active tasks
queues that maker profiles track.

## Cross-references

- H28 scope discipline (in SKILL.md) — defines what NOT to verify
- H34 ops-manager cron-fault regime (in SKILL.md) — separate anomaly class (cron timing, not data)
- H36 / H36-BODY clock-anomaly recipes (in SKILL.md) — separate anomaly class (frontmatter timing, not data)
- H44 cadence-decay option (a) (in SKILL.md) — defines when to STOP repeating recommendations; complements H68's "note in sweep row" approach

## H68 validation status

- **H68 (this sweep):** First application. Real case: content-director Run History #12 Score=0.0 anomaly. Per H68 recipe: noted in sweep row, classified as scope-bounded, flagged for Orchestrator, no separate escalation. Re-check scheduled at H69.
- **H69+:** Validate forecast realization — does the loop-goal scoring bug persist? If yes, escalate via repeat-observation pattern (H68 step 6). If no, treat as transient and close the loop.
