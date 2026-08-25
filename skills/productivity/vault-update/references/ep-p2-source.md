---
title: "EP P2 provenance — the filing skill (vault-update)"
created: 2026-08-13
type: reference
parent_skill: vault-update
source_author: "EP (@eptwts, blue verified)"
source_post_id: "2080342488728904164"
source_url: "https://x.com/eptwts/status/2080342488728904164"
source_title: "this system will change your life..."
source_published: 2026-07-23
raw_capture: "wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md"
raw_capture_line_range: "70-81 (prompt 2 section)"
tags: [provenance, ep-prompt-2, vault, knowledge-base]
confidence: high
---

# EP P2 — Provenance Card for `vault-update`

## Source

| Field | Value |
|---|---|
| Author | EP — `@eptwts` (blue verified) |
| Article | "this system will change your life..." — 6 prompts to build a personal knowledge vault on Hermes Agent |
| Post ID | `2080342488728904164` |
| URL | https://x.com/eptwts/status/2080342488728904164 |
| Published | 2026-07-23 |
| Ingested here | 2026-08-13 |
| Immutable raw copy | `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md` (164 lines, ~10.9k chars) |
| Prompt 2 location in raw | section heading "prompt 2: the skill for filing things without being asked", lines ~70–81 |
| Engagement at capture | 737 likes · 42 RT · 2471 bookmarks · 229,417 views |

**Do not quote the prompt at length here.** The verbatim text lives once, in the immutable
`raw/` capture, which is the vault's single source of truth for source material
(`SCHEMA.md`: never modify files in `raw/`). Read it there:

```bash
sed -n '70,82p' /Volumes/Storage-1/Hermes/wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md
```

EP's own note on why the second half of the prompt matters, paraphrased: the date and
contradiction rules are the load-bearing part — omit them and you get a folder of notes
that all claim to be true simultaneously.

## What Prompt 2 mandates (paraphrased clauses)

EP's P2 asks the agent to author a skill named `vault-update` that:

1. Runs on **every** disclosure about the user's life, work, projects, decisions, or the
   people they work with.
2. Includes **passing mentions** — no save request required.
3. Chooses the correct destination folder.
4. **Searches the vault for an existing note on the subject before creating a new one.**
5. On contradiction: **write the new note, mark the old one superseded, link both ways.**
6. For anything that changes over time — rate, location, current work, current
   collaborators — **only one note may be the current one**.
7. `as_of` = **when the thing was actually true**, never the logging date.
8. Record the **intake channel** (EP's own setup: Telegram).
9. Append **one line** to the meta changelog.
10. **Never overwrite a note in place. Never invent a date.**
11. On completion, **report the file path and what was set.**

EP also recommends, for the first week only, turning on write approval for memory and
skills so nothing lands without a yes.

## Clause → implementation map

| EP P2 clause | Where it lands in this skill |
|---|---|
| runs on every disclosure | `SKILL.md` → "When to Use", 5 trigger families (VI + EN) |
| passing mentions count | `SKILL.md` → "Passing-mention rule", worked two-output example |
| pick the right folder | Step 3 folder table + `scripts/find_target_folder.py` (`suggest_new`) |
| search before create | Step 2, ripgrep/grep only — no vector DB — via `find_target_folder.py` |
| contradiction → new note + supersede + links both ways | Step 5 (5a/5b/5c), verification check #4 |
| one current note per volatile subject | Step 5 volatile registry, verification check #5 |
| honest `as_of` | Hard rule #2; `log_change.py` exits non-zero when `--as-of` == today unless `--allow-today` |
| record intake channel | Hard rule #3; `sources:` + `intake_channel:` in the note template |
| one changelog line | Step 6 → `scripts/log_change.py`, append-only, header on first run |
| never overwrite in place | Hard rule #4; Step 5b annotates additively and preserves the old body + `as_of` |
| never invent a date | Hard rule #5; `needs_verification: true` instead of guessing |
| report path + fields | Step 7 acknowledgement block |
| write approval for week 1 | Operator-side setting, not code — noted in "Adoption" below |

## Deliberate deviations (and why)

| EP P2 | Here | Reason |
|---|---|---|
| numbered folders (`00-inbox` … `90-meta`) | existing `concepts/` (149 files, flat), `entities/` (7), `projects/` (8 dirs) | vault predates the article; renumbering breaks every existing wikilink and `index.md` entry |
| `90-meta/CHANGELOG.md` | `wiki/CHANGELOG.md` | no `90-meta/` exists; vault root is the meta slot, alongside `log.md` and `SCHEMA.md` |
| `50-decisions/` folder | `concepts/<slug>-YYYY-MM-DD.md` with `tags: [decision]` | `SCHEMA.md` tag taxonomy already carries `decision` |
| `40-people/` folder | `entities/` | same role, name already established |
| always record "telegram" | record the **real** intake channel, default `telegram` | Telegram is the primary gateway, but CLI / desktop / cron turns happen. Writing "telegram" for a CLI turn would fabricate provenance — same class of error as fabricating a date |
| fresh `~/vault` | `/Volumes/Storage-1/Hermes/wiki/` | the mature vault is the target; EP P1 (build the vault) is already satisfied |

Frontmatter fields `id`, `as_of`, `supersedes`, `epistemic`, `verification`,
`needs_verification` were added to `wiki/SCHEMA.md` on 2026-08-13 as **optional
forward-only** fields from EP P1 — `vault-update` uses them, existing notes are not
retro-migrated.

## Adoption notes

- **Week-1 approval gate (EP's advice):** keep memory/skill write approval on while the
  trigger families are being tuned, so no mis-parsed fact lands unattended. Once the
  false-positive rate is acceptable, let it run unprompted — that is the whole point of P2.
- **Composition:** `vault-update` files in real time; `nightly-memory-curation` (cron
  02:00) consolidates; `wiki-maintenance` prunes and rotates. Three cadences, no overlap.
  Neither existing skill was modified to add this one.

## Related

- `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md` — full article, all 6 prompts
- `wiki/concepts/ep-life-os-prompt-gap-analysis-2026-08-13.md` — gap analysis of the follow-up 9-phase post
- `wiki/concepts/ep-profile-research-2026-08-13.md` — author profile research
- `wiki/SCHEMA.md` — frontmatter contract this skill writes against
- `../SKILL.md` — the skill itself
