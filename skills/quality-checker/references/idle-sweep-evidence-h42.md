---
sweep: H42
date: 2026-06-26 23:00 +07:00
trigger: qa-agent hourly gate
---

# H42 Evidence — Unique Phrase Anchor Pattern (NEW)

## What happened

H42 (2026-06-26 23:00:52 +07:00) successfully applied a **NEW anchor pattern** that wasn't documented in any prior sweep evidence: the **unique phrase anchor** with `content.count(phrase) == 1` pre-verification.

## The problem

By H42, the `## Verdict History` section header appeared **23 times** in `~/.hermes/profiles/qa-agent/state.md`:
- 1 actual section header at line ~78
- 22 inline references across prior row bodies (H6, H19, H23, H25, H26, H27, H28, H29, H31, H33, H34, H35, H36, H37, H41 all cited it in their notes)

The H15/H25 boundary recipe ("anchor on `\n\n## Verdict History`") and H18 lesson ("when boundary appears 2+ times, use multi-line context anchor") both fail when boundary count reaches 23 — multi-line context anchors also risk collision if any prior row's tail happens to be unique.

## The recipe (H42 — new pattern)

**Use a UNIQUE PHRASE from the END of the previous row's tail + the literal section header from the same line.**

```python
# Step 1: Pick a unique phrase from the last 60-100 chars of the prior row's tail
last_60_chars_of_H41 = "...0 conflicts, 0 escalations — system HEALTHY.**"
boundary_token = "## Verdict History"

# Step 2: Construct the anchor phrase
phrase = last_60_chars_of_H41 + "\n" + boundary_token

# Step 3: VERIFY UNIQUENESS before patching
content = open(state_md_path).read()
assert content.count(phrase) == 1, f"Anchor not unique: found {content.count(phrase)} matches"

# Step 4: Construct patch
ANCHOR_OLD = phrase
ANCHOR_NEW = last_60_chars_of_H41 + "\n" + H42_ROW + "\n" + boundary_token

patch(mode='replace', path=state_md_path, old_string=ANCHOR_OLD, new_string=ANCHOR_NEW)
```

## Why this works

The prior row's tail text is specific to the row that just ended (H41's conclusion text wouldn't appear in any other row). The `\n## Verdict History` literal sequence appears at the boundary immediately following H41. Combined, the phrase has TWO sources of uniqueness:
1. H41's unique conclusion text (varies per sweep)
2. The boundary token appearing exactly once AFTER H41 (sequence pattern, not just count)

## H42 result

- Pre-patch: `content.count(phrase) == 1` (verified)
- Patch applied cleanly on first attempt (no retries)
- Post-patch: row count went 41 → 42 (correct)
- H42 row appears at line 78, between H41 and `## Verdict History` header
- File size: 122,066 → 127,468 bytes (+5,402 bytes for H42 row)

## Comparison with prior anchor patterns

| Pattern | Sweep | Boundary count | Multi-line? | Worked? |
|---|---|---|---|---|
| `\n\n## Verdict History` (H15) | H15-H17 | 1 | No | Yes |
| 4-line context anchor (H25/H26) | H23-H37 | 2-15 | Yes (3+ lines) | Yes |
| Unique phrase anchor (H42) | H42 | 23 | No (just last 60 chars + boundary) | Yes |

## When to use H42 unique phrase anchor

Use when:
- The boundary token (`## Verdict History` or similar) appears ≥10 times in the file
- Prior row's tail is well-known (you've just read it)
- Multi-line context anchors are getting unwieldy (4+ lines of context)

Don't use when:
- Boundary token count is 1-2 (use simple H15 recipe)
- Prior row was truncated by `read_file` limit (anchor on wrong tail — see H19)
- You haven't read the prior row's tail recently

## H42 sweep summary

- **Verdict:** PASS (vacuous — Mode B no-pending)
- **Active crons:** 18, all healthy (per H38 cron-truth recipe)
- **H39 phantom-cron claim:** holds — research-lead cron ✅ registered, last_run 18:03:12
- **H34 ops-manager recovery:** holds — slip_ratio 0.0, on 6h cadence
- **Sibling-collision pre-check:** ran `grep -cE` IMMEDIATELY BEFORE patch (per H40 fix), count = 41 (expected 41, no collision)
- **Pipe prefix:** used single pipe `| H42 |` per H39 lesson (H37/H39/H40/H41 all used multi-pipe prefix as cosmetic drift)
- **H36 clock anomaly:** persists on ops-manager frontmatter, but per H38 recipe is harmless cosmetic drift

## Forecasts logged for H43+ verification

- H43 should re-run `content.count(phrase) == 1` pre-verification (the technique is repeatable)
- H43 should also continue using single pipe `| H<N> |` to avoid further drift
- H43 cron-truth sweep should show 18 crons (or more, if profile crons continue to grow per H39 pattern)
- H43 should expect ops-manager H34 to remain fully recovered (slip_ratio 0.0)

## Related

- `references/idle-sweep-evidence-h15.md` — H15 original boundary anchor recipe
- `references/idle-sweep-evidence-h18.md` — H18 boundary collision detection
- `references/idle-sweep-evidence-h25.md` — H25 multi-line context anchor
- `references/idle-sweep-evidence-h40.md` — H40 sibling-collision overwrite bug
- SKILL.md → "🆕 H42 Unique Phrase Anchor Recipe (NEW — 2026-06-26 23:01)"
