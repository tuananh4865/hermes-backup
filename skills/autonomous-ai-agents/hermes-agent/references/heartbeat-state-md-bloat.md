# Heartbeat State.md Bloat — Compaction Recipe

## Problem

qa-agent (and to a lesser extent operations-manager) accumulate a verdict row every sweep:

```markdown
| H42 | 2026-06-26 23:00 | N/A | N/A | 0 | (qa-agent hourly gate — H38/H39/H41 cron-truth sweep, 6-check protocol) | 42nd sweep in current file's continuity ... [5000 chars] |
```

After 50+ sweeps, qa-agent/state.md hits **200KB+ / 123 lines**. The `read_file` tool caps at 100K chars and refuses to load it whole, forcing `offset=81` pagination. Worse, the actual signal ("0 pending, all healthy") is buried in 5000-char rows of self-referential history.

## Symptom in sweeps

```
[read_file] error: Read produced 112,471 characters which exceeds the safety limit (100,000 chars).
Use offset and limit to read a smaller range. The file has 123 lines total.
```

When this fires, you lose ability to spot-check prior sweep decisions, sibling-collision context, and accumulated lessons. The bloat self-amplifies — you can't see the problem because the file is too big to read.

## Compaction recipe (manual, safe)

Run when qa-agent/state.md exceeds ~150KB:

```bash
# 1. Backup current state (preserve audit trail)
cp ~/.hermes/profiles/qa-agent/state.md \
   ~/.hermes/profiles/qa-agent/state.md.bak.$(date +%Y%m%d_%H%M%S)

# 2. Keep only the last 10 H<N> rows in the verdict table (most recent context)
# Plus the "Recent Verdicts" / "Handoff History" / "What Worked" / "What Failed" /
# "Open Items" sections which are summaries, not per-sweep rows.

# 3. Add a one-line note at the top of the compacted table:
# "Compacted from N rows on YYYY-MM-DD. Prior sweeps in state.md.bak.YYYYMMDD_HHMMSS."
```

**What to keep:**
- Top 80 lines (Current Goal, Handoff History, What Worked, What Failed, Open Items, Profile Config)
- Last 10 H<N> rows from the verdict table (recent cross-validation context)

**What to drop:**
- H<N> rows older than the most recent 10
- Inline H5/H10/H34/H38/H40/H42 recipe explanations (they're already in `multi-agent-heartbeat-protocol.md`)

## Prevention (better than cure)

Two long-term fixes worth considering:

1. **Reduce qa-agent cadence from hourly to 6h** when system is confirmed idle. The hourly cron has been firing for 50+ sweeps producing 0-actionable-finding rows. A 6h cadence would still catch real issues (within H38 24h-overdue window) while reducing bloat 6×.

2. **Move per-sweep detail to dated log files** instead of inline rows. E.g., `~/.hermes/profiles/qa-agent/sweeps/2026-06-27-H59.md` containing the full row text, while state.md only carries a 1-line summary:
   ```markdown
   | H59 | 2026-06-27 15:01 | N/A | 0 | sweeps/2026-06-27-H59.md |
   ```
   This keeps state.md readable indefinitely while preserving full audit trail.

## When to act

- **< 100KB:** ignore, system is healthy
- **100KB–200KB:** schedule compaction within the week
- **> 200KB:** urgent — read_file safety limit is close, sweep analysis is degraded
- **> 500KB:** state.md is effectively dead — compaction must happen before next sweep

## Pitfalls when compacting

1. **Don't lose the "Last sweep verdict" anchor** — qa-agent and orchestrator siblings use the highest H<N> number for context anchoring. If you renumber rows, sibling-collision recipes break.
2. **Keep the frontmatter `updated:` timestamp current** — otherwise H36 clock-anomaly detection (already in main reference) flags it as cosmetic drift.
3. **Preserve cross-validation links** — operations-manager audit IDs, cron last_run references, etc. that downstream sweeps will need to verify.
4. **Test the compacted file with a read_file load** before declaring done — if it still >100K, compact again more aggressively.