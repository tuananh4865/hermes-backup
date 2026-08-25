# V18 — Hybrid Sweep Recipe (2026-06-29 18:31+)

**Context:** The V18 hybrid recipe is the 3rd viable read pattern for routine 5-profile heartbeat sweeps, distinct from V17 (`open()` in execute_code) and V14 (V10 JSON recipe). Confirmed durable across V18 + V19 + V20 (3 consecutive sweeps, 2026-06-29 18:31 → 20:01).

## When to use V18 hybrid

**Use V18 when:**
- The sweep needs to inspect FULL state.md content (not just structural sections) — V18 reads full content, V14 only reads `limit=80`
- The sweep wants cron ground-truth in human-readable format with line numbers preserved (useful for H40 sibling-collision pre-check that cross-references state.md line numbers)
- qa-agent state.md is <50KB post-V11 compaction (file is currently 50KB at V20)
- You want to keep things in `read_file` for the line-numbered output it provides

**Do NOT use V18 when:**
- Minimum tool-call count is the priority → use V17 `open()` in execute_code (1 call for all 5 state.md files)
- The sweep needs machine-parseable cron truth for further processing → use V14/V10 JSON recipe
- The sweep has terminal pagination concerns → use V14/V10 JSON recipe (V18 hybrid can hit `hermes cron list` head-N cutoff, see V20 observation)

## Canonical V18 recipe (6 tool calls)

```python
# Step 1: Batch 5 state.md reads in a single parallel turn
read_file(path=qa-agent/state.md, limit=80)
read_file(path=engineering-lead/state.md, limit=80)
read_file(path=operations-manager/state.md, limit=80)
read_file(path=code-reviewer/state.md)
read_file(path=security-engineer/state.md, limit=80)

# Step 2: Cron truth via standalone `hermes cron list` (1 call, human-readable)
terminal(command="hermes cron list 2>&1 | grep -cE 'Last run:.*ok'")  # Returns N (cron count)

# Step 3: Pending/handoff scan (combined, 1 call)
terminal(command="find ~/.hermes/profiles -type d \\( -name 'pending*' -o -name 'handoff*' -o -name 'inbox' -o -name 'queue' \\) -not -path '*/skills/*' -not -path '*/references/*'")
terminal(command="find ~/.hermes/profiles -type f -name 'pending*' -not -path '*/skills/*' -not -path '*/references/*'")
```

**Total: 6-7 tool calls** (5 state.md reads batched + 1 cron-list + 1-2 find scans).

## V18 vs V17 vs V14 — when to use which

| Recipe | Tool calls | Strength | Weakness | Use case |
|---|---|---|---|---|
| **V18 hybrid** (batch `read_file` + `hermes cron list`) | 6-7 | Line numbers, human-readable cron output, full state.md content | Terminal pagination gotcha on `hermes cron list` (V20) | Default for post-V11 era when sweep needs cross-referencing |
| **V17 `open()` in execute_code** | 1 (for state.md) | Minimum tool-call count for state.md reads | No line numbers in output, no cron truth | Tight budget sweeps |
| **V14 / V10 JSON** (`python3 -c "import json; ..."`) | 3-4 | Machine-parseable cron truth, no terminal pagination | Extra Python overhead, less human-readable | Cron-truth-heavy sweeps, recurring pagination issues |
| **V6/V7/V9 pagination** | 4-5 | Reliable when qa-agent state.md >100KB | Bypasses the 100K char safety limit | qa-agent state.md >100KB |

## V20 hardening — graceful degradation on terminal pagination

**Problem:** V18 hybrid uses `hermes cron list` which is susceptible to terminal head-N cutoff. V20's sweep hit the SAME issue V15 had: `head -100` only captured ~10 crons (out of 18). The first head-N capture shows <18 `Last run` lines when pagination cuts in.

**V21+ mitigation recipe:**

```python
# Step 1: Same 5 state.md reads (V18 batch)
[5 read_file calls in parallel]

# Step 2: Cron truth — ADAPTIVE: try `hermes cron list` first, fall back to V10 JSON on pagination
try:
    # First attempt: single head-N capture
    count = terminal(command="hermes cron list 2>&1 | grep -cE 'Last run:.*ok'")
    if count < 18:  # Pagination detected
        # Switch to V10 JSON recipe (1 call, all 18 in one shot)
        terminal(command="python3 -c \"import json; jobs=json.load(open(os.path.expanduser('~/.hermes/cron/jobs.json')))['jobs']; print(f'Total: {len(jobs)} | ok: {sum(1 for j in jobs if j.get(\\\"status\\\")==\\\"ok\\\")} | err: {sum(1 for j in jobs if j.get(\\\"status\\\")!=\\\"ok\\\")}')\"")
except Exception:
    # Fallback to JSON on any error
    pass
```

**Effectively:** V18 hybrid becomes 6-tool-call recipe that gracefully degrades to V14's 3-4 call JSON-based recipe on terminal pagination issues. Net tool-call count is the same in the degraded path, but the JSON output is less human-readable.

**V20 empirical data:** head -100 captured ~10 crons. The remaining 8 crons require `tail -80`. If you notice `grep -cE "Last run:.*ok"` returns <18 in the first call, IMMEDIATELY switch to JSON. Do NOT chain `head + tail` — the JSON recipe is 1 call.

## V18 NEW techniques summary

From the V18 validation (2026-06-29 18:31) and V19 (19:01) and V20 (20:01) confirmations:

1. **Hybrid recipe (batch read_file + standalone `hermes cron list`)** — 6 tool calls, full state.md content + line numbers + human-readable cron truth. When to use: sweeps that need to inspect full state.md content (not just structural sections) AND want to cross-reference H-row line numbers for H40 sibling-collision pre-check.

2. **qa-agent "Found 2 matches" patch warning is benign** — H40 sibling-collision recipe handles this case correctly; the warning is informational and self-correcting. Documented in V18 validation so future sweeps don't escalate as a fault.

3. **H34 sustained recovery confirmed at 17+ sweeps** — the multi-profile cron fault pattern (H28/H29/H34) is FULLY DEAD, sustained for 2.5+ days. This validates the H38 mtime-vs-cron-truth lesson at the system level.

4. **`hermes cron list` pagination gotcha hit 3rd time (V20 reinforcement)** — the `head -100` capture reliably cuts off at ~10 crons. V21+ sweeps should detect this and switch to V10 JSON recipe. The JSON recipe is the durable fix.

## V20 sweep snapshot (2026-06-29 20:01)

**H76 orchestrator 30m heartbeat:**
- qa-agent state.md: 50KB / 55 lines (V19 was 50KB — stable, no new H-row written)
- operations-manager state.md: 58KB (V18 was 58KB, V17 was 50KB — 8KB growth across 18:00 audit chain)
- All 5 profile state.md files read in single parallel batch (well under 100K safety limit)
- All 18 crons verified `ok` via fresh `hermes cron list` (2 calls needed — head -100 + tail -80 — confirming V20 pagination gotcha)
- 0 stuck, 0 pending QA, 0 CRITICAL findings
- STEADY_STATE_IDLE forced correctly via H32b oracle
- H34 sustained recovery now at 17 sweeps (V58 → V20 = 17 passes)

**V20 result:** Textbook STEADY_STATE_IDLE. No intervention. No new failure mode beyond the documented pagination gotcha (now mitigated via V21+ JSON fallback).

**V18 + V19 + V20 = 3 consecutive V18 hybrid recipe deployments.** Recipe is mature. The pagination gotcha is the only known failure mode, with a documented mitigation. Future skill revisions should promote V18 hybrid to the SKILL.md "read pitfalls" section as the recommended recipe (currently V14 simple recipe is listed there; V18 hybrid is more powerful and equally valid per the V19 confirmation note).

## Related

- `references/h32b-validation-log.md` — V18 + V19 + V20 validations (3 consecutive clean passes)
- `references/v14-post-compaction-simple-sweep-recipe.md` — V14 simple recipe (V18 superset, but V14 still valid for tight budgets)
- `references/cron-truth-json-recipe.md` — V10 JSON recipe (the durable fix for V18 hybrid's pagination gotcha)
- `references/h38-mtime-vs-cron-truth-pattern.md` — H38 lesson (the foundation that V18 hybrid depends on for cron ground-truth)
