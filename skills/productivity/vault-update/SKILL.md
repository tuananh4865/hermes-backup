---
name: vault-update
description: "Use when Tuấn Anh tells you something new about his life, work, projects, decisions, gear, pricing, location, or the people/brands he works with — INCLUDING when he mentions it in passing and never asks you to save it. Triggers on Vietnamese or English disclosure phrasing ('anh vừa', 'từ giờ anh', 'anh đang làm', 'anh chốt', 'nhớ giúp anh', 'i just', 'from now on', 'we decided', 'remember that'). Files the fact into the right wiki folder (concepts/ | entities/ | projects/{name}/), greps for an existing note on the same subject BEFORE creating a new one, and on contradiction writes a new note + marks the old one superseded with bidirectional wikilinks. Enforces one-current-note-per-volatile-subject, as_of = when the fact was ACTUALLY true (never today), intake channel recorded, append-only CHANGELOG line, never overwrite in place, never invent a date. Adapted from EP (@eptwts) Post A Prompt 2, x.com/eptwts/status/2080342488728904164 (2026-07-23)."
version: 1.0.0
author: Hermes Agent (v1.0.0 built 2026-08-13 from EP @eptwts Post A Prompt 2; composes with existing wiki-maintenance + nightly-memory-curation, replaces neither)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [vault, memory, knowledge-base, wiki, passive-capture, supersede, as-of, provenance, changelog, append-only, ep-prompt-2]
    related_skills: [wiki-maintenance, nightly-memory-curation, hermes-memory, evidence-gate, drift-recovery-framework-promotion]
    source_post: "x.com/eptwts/status/2080342488728904164"
    source_raw: "wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md"
    vault_root: "/Volumes/Storage-1/Hermes/wiki"
---

# vault-update — File What He Says Without Being Asked

> **Class scope:** every turn in which Tuấn Anh reveals a durable fact about himself, his work, his projects, his decisions, his gear, his money, his location, or the people and brands around him. The disclosure does **not** have to be a save request. A fact dropped mid-sentence while asking about something else still gets filed.

> **Source:** EP (@eptwts) Post A "this system will change your life", Prompt 2 — the filing skill (post `2080342488728904164`, published 2026-07-23; raw capture at `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md`). EP's own framing of the second half of that prompt: the date and contradiction rules are the important part, because without them you end up with a folder of notes that all claim to be true at once.

---

## When to Use

Fire this skill the moment a turn contains **new durable information**, in either language.

### 5 trigger phrase families (Vietnamese + English)

| # | Family | Vietnamese triggers | English triggers | Example that MUST fire |
|---|---|---|---|---|
| 1 | **State change / just happened** | "anh vừa…", "anh mới…", "hôm qua anh…", "tuần trước anh…" | "i just…", "yesterday i…", "last week we…" | "anh vừa đổi mic sang Rode Wireless Pro" |
| 2 | **Standing rule / from now on** | "từ giờ anh…", "sau này…", "mặc định anh…", "anh không dùng… nữa" | "from now on…", "going forward…", "i no longer use…" | "từ giờ anh không quay ở Quy Nhơn nữa" |
| 3 | **Decision / commitment** | "anh chốt…", "anh quyết định…", "anh chọn…", "thôi anh làm…" | "we decided…", "i'm going with…", "final answer is…" | "anh chốt giá booking 3 triệu / video" |
| 4 | **Work in progress / people** | "anh đang làm…", "anh đang hợp tác với…", "bên X liên hệ anh…", "chị Y phụ trách…" | "i'm working on…", "i'm partnering with…", "X reached out" | "bên Shopee liên hệ anh làm affiliate live" |
| 5 | **Explicit save request** | "nhớ giúp anh…", "lưu lại…", "ghi vào wiki…", "đừng quên…" | "remember that…", "save this…", "log this" | "nhớ giúp anh là anh dùng M4 24GB" |

### Passing-mention rule (the hard part)

Families 1–4 usually arrive **inside a request about something else**. That is exactly the case EP's prompt was written for.

```
User: "cắt clip badminton hôm qua giúp anh, à mà anh mới chuyển studio về Kon Tum rồi"
                                             └────────── FILE THIS ──────────┘
```
Do the cut **and** file the studio relocation. Two outputs, one turn. Never trade one for the other.

### Skip when

- The information is about the **agent's own run** (tool errors, retries, render logs) → that belongs to session logs, and `nightly-memory-curation` picks it up at 02:00.
- The fact is **already recorded with the same `as_of`** → no-op, say so, do not create a duplicate.
- It is a **hypothetical / question / brainstorm** ("nếu anh chuyển sang Đà Nẵng thì sao?") → not a fact. If you file it at all, `epistemic: hypothesis`.
- It is **transient** ("anh đang ăn cơm") → nothing durable to keep.

---

## Why This Exists

**1. EP's diagnosis (2026-07-23).** Context about a person exists in thousands of places and none of it is where the agent can search it. EP's fix is one durable record on a machine that never sleeps, with a filing skill that runs unprompted. Prompt 2 is that skill. This file is Prompt 2 rebuilt for Tuấn Anh's already-mature vault instead of a fresh `~/vault`.

**2. Tuấn Anh's own drift history.** The wiki already carries the scar tissue:
- `wiki/concepts/drift-recovery-3-systems-2026-07-19.md` + skill `drift-recovery-framework-promotion` — rules promoted to VĨNH VIỄN because they kept evaporating at compaction.
- `2026-07-12` — the adversarial-verifier and nightly-curator-self-check mandates (`july-12-adversarial-verifier-validation`, `july-12-nightly-curator-self-check` in `entities/learned-about-tuananh.md`). The lesson of that day was that a memory system nobody audits silently rots: facts survive, but nothing marks which one is *current*.
- `skills/productivity/evidence-gate` — born from a fabricated "đã lưu 4 file" claim.

Passive capture without supersede discipline produces exactly the failure EP names: 149 concept files that all read as true simultaneously. `as_of` + `supersedes` + one-current-note is the fix.

**3. Composition, not replacement.**

| Skill | Cadence | Job |
|---|---|---|
| **vault-update** (this) | **real time, every turn** | catch the fact the moment it's said, file it, mark supersedes |
| `nightly-memory-curation` | cron 02:00 | consolidate the day's sessions, mirror to Obsidian, entity/concept cross-refs |
| `wiki-maintenance` | periodic / on request | prune stale files, rotate logs, health score, git hygiene |

vault-update writes **one small note now**. The nightly curator finds it already filed and consolidates instead of reconstructing. Never edit those two skills from here.

---

## Vault Map (Tuấn Anh's actual layout)

```
/Volumes/Storage-1/Hermes/wiki/
├── SCHEMA.md          # frontmatter contract — obey it
├── index.md           # catalog; add new page under its section
├── log.md             # append-only chronological action log
├── CHANGELOG.md       # ← vault-update's own append-only ledger (created on first run)
├── raw/               # IMMUTABLE. never write here from this skill
├── entities/          # 7 files. people, brands, companies, products, tools
│   └── learned-about-tuananh.md   # identity aggregate — the one file that IS edited by append
├── concepts/          # 149 files, FLAT. topics, facts, decisions, lessons
├── projects/          # 8 project folders (dam-me, mi-y-kontum-research, quynhon-edit,
│                      #   tuan-anh-badminton, tuan-anh-review-tiktok, vuive-channel-research,
│                      #   learn-google-flow, _template)
├── comparisons/       # side-by-side analyses (out of scope here)
└── queries/           # filed query results (out of scope here)
```

### Deviations from EP P2 — declared, not hidden

| EP P2 says | Here | Why |
|---|---|---|
| numbered folders `00-inbox`, `10-identity`, `20-projects`, `40-people`, `50-decisions`, `90-meta` | `concepts/`, `entities/`, `projects/<name>/` | vault predates EP by months; 149 flat concepts + `index.md` already work. Renumbering would break every wikilink. |
| `90-meta/CHANGELOG.md` | `wiki/CHANGELOG.md` | no `90-meta/`; root is the equivalent meta slot next to `log.md`. |
| always record source telegram | record the **actual** intake channel, default `telegram` | Telegram is the primary gateway but CLI / desktop / cron are real. Writing "telegram" for a CLI turn would be inventing provenance — the same class of sin as inventing a date. |
| dedicated `50-decisions` folder | `concepts/<topic>-YYYY-MM-DD.md` with `tags: [decision]` | tag taxonomy in `SCHEMA.md` already has `decision`. |

Everything else in P2 — search before create, supersede with links both ways, one current note, honest `as_of`, one CHANGELOG line, no in-place overwrite, no invented dates, report path + fields — is kept **as-is**.

---

## Core Workflow (7 steps)

### Step 1 — Detect the new information

Scan the turn for the 5 trigger families. For each hit, extract a **fact card** before touching disk:

```
subject      : what the fact is ABOUT      (e.g. "booking rate", "studio location", "primary mic")
claim        : the new value               (e.g. "3.000.000đ / video")
as_of        : when it became true         (ask if unknown — do NOT guess)
volatile?    : yes/no  (see volatile registry below)
epistemic    : fact | self_report | observation | hypothesis | preference
channel      : telegram | cli | desktop | cron
```

`self_report` is the default `epistemic` for anything Tuấn Anh says about himself — it is true that he said it; whether the world matches is unverified. Reserve `fact` for independently verifiable things.

If `as_of` is genuinely unrecoverable, set `needs_verification: true` and say so in the acknowledgement. Never substitute today's date to make the field look complete.

### Step 2 — Search before you create (lexical, not vector)

Grep first. Always. The vault has no embedding index and this skill must not depend on one.

```bash
# helper (preferred) — ranks concepts/ entities/ projects/ and returns top 3
python3 /Volumes/Storage-1/Hermes/skills/productivity/vault-update/scripts/find_target_folder.py \
  "booking rate 3 triệu per video" --json

# manual fallback
rg -il --glob '*.md' 'booking|rate card|giá quay' /Volumes/Storage-1/Hermes/wiki/{concepts,entities,projects}
rg -n '^title:|^tags:' <candidate.md>
```

Read the top candidates. Decide one of three outcomes:

| Outcome | Condition | Go to |
|---|---|---|
| **A. no-op** | same subject, same claim, same `as_of` already on disk | Step 7, report "already current" |
| **B. new subject** | nothing on this subject | Step 4 |
| **C. contradiction** | a live note asserts a different value for the same subject | Step 5 |

### Step 3 — Pick the folder

| Subject is… | Folder | Filename |
|---|---|---|
| a person, brand, agency, company, product, tool | `entities/` | `<slug>.md` |
| scoped to one of the 8 active projects | `projects/<project>/` | `<slug>-YYYY-MM-DD.md` |
| anything else — decision, rate, gear, workflow, lesson, location | `concepts/` | `<slug>-YYYY-MM-DD.md` |
| identity-level trait belonging to the aggregate | `entities/learned-about-tuananh.md` | **append a dated bullet**, plus a standalone `concepts/` note if the fact is volatile |
| raw source material | `raw/…` | **never written by this skill** |

Slug rules from `SCHEMA.md`: lowercase, hyphens, no spaces, no colons. The `-YYYY-MM-DD` suffix on `concepts/` files carries `as_of`, not today — that is what makes supersede chains readable in a plain `ls`.

### Step 4 — No conflict → create the note

```yaml
---
title: Booking rate — 3.000.000đ per video
created: 2026-08-13          # when the note was WRITTEN (today is correct here, only here)
updated: 2026-08-13
type: concept
tags: [decision, project]
sources: [telegram]
confidence: high
relationships: [learned-about-tuananh, tuan-anh-review-tiktok]
id: dec-20260731-001
as_of: 2026-07-31            # when the fact was ACTUALLY true — from the user, never today by default
supersedes: []
epistemic: self_report
verification: user_reported
needs_verification: false
intake_channel: telegram
---

# Booking rate — 3.000.000đ per video

**As of 2026-07-31** (told via Telegram 2026-08-13).

- Rate: 3.000.000đ per delivered video.
- Scope: …

## Provenance
- Intake: Telegram, 2026-08-13
- Reported by: Tuấn Anh (self-report)

## Related
- [[learned-about-tuananh]]
- [[tuan-anh-review-tiktok]]
```

Minimum 2 wikilinks per `SCHEMA.md`. `created` may be today; `as_of` may not, unless the fact truly became true today.

### Step 5 — Conflict → new note wins, old note is superseded (never deleted)

Three writes, in this order:

**5a. Write the new note.** Same template as Step 4, plus the backward link:
```yaml
supersedes: [booking-rate-2026-05-02]
```

**5b. Mark the old note superseded — additively.** Do not rewrite its body, do not change its claim, do not touch its `as_of`. Only add/flip the status fields and append a pointer:
```yaml
superseded: true
superseded_by: [booking-rate-2026-07-31]
superseded_on: 2026-08-13
updated: 2026-08-13
```
```markdown
> **Superseded 2026-08-13** — current note: [[booking-rate-2026-07-31]]. Kept for history; the claim below was true as of its own `as_of`.
```

**5c. Verify the links point both ways.**
```bash
rg -n 'supersedes|superseded_by' \
  /Volumes/Storage-1/Hermes/wiki/concepts/booking-rate-2026-07-31.md \
  /Volumes/Storage-1/Hermes/wiki/concepts/booking-rate-2026-05-02.md
```
A one-way link is a failed step, not a partial success.

#### Volatile subject registry — exactly one `current` note each

EP's list, mapped to this vault. For every row: at most one note without `superseded: true`.

| Volatile subject | Where it lives | Slug prefix |
|---|---|---|
| what he charges (booking / rate card / affiliate cut) | `concepts/` | `booking-rate-`, `rate-card-` |
| where he lives / shoots | `concepts/` | `studio-location-`, `base-location-` |
| what he's working on (active project set) | `projects/<name>/` + `concepts/` | `active-projects-` |
| who he works with (brands, agencies, collaborators) | `entities/` | `<brand-slug>` |
| current gear (mic, camera, machine) | `concepts/` | `gear-current-` |
| ingredient / supplier pricing (mì Ý Kontum) | `projects/mi-y-kontum-research/` | `cost-` |
| pricing or plan of a paid tool he subscribes to | `concepts/` | `pricing-` |

Before finishing a volatile write, count the live notes:
```bash
rg -l '^title:.*[Bb]ooking rate' /Volumes/Storage-1/Hermes/wiki/concepts/ \
  | xargs rg -L '^superseded: true'
```
Expect exactly one path. Two means Step 5b was skipped somewhere — fix before reporting.

### Step 6 — Append one line to `wiki/CHANGELOG.md`

One line. Append-only. Never rewritten, never sorted, never deduped.

```bash
python3 /Volumes/Storage-1/Hermes/skills/productivity/vault-update/scripts/log_change.py \
  --file concepts/booking-rate-2026-07-31.md \
  --action create \
  --reason "new rate mentioned in passing on Telegram" \
  --as-of 2026-07-31 \
  --supersedes concepts/booking-rate-2026-05-02.md
```

produces

```
[2026-08-13 14:30 ICT] vault-update | file=concepts/booking-rate-2026-07-31.md | action=create | reason="new rate mentioned in passing on Telegram" | as_of=2026-07-31 | supersedes=concepts/booking-rate-2026-05-02.md
```

A supersede pair emits **two** lines: `action=create` for the new note, `action=supersede` for the old one. The script creates `CHANGELOG.md` with a header on first run. `wiki/log.md` stays the human narrative log — that is `wiki-maintenance` and the nightly curator's surface, not this one's.

### Step 7 — Acknowledge with path + fields set

Report, do not summarise vaguely. Minimum shape:

```
📥 Filed: wiki/concepts/booking-rate-2026-07-31.md
   as_of        : 2026-07-31  (từ anh, không phải hôm nay)
   supersedes   : concepts/booking-rate-2026-05-02.md  → đã mark superseded: true, link 2 chiều ✓
   sources      : [telegram]
   epistemic    : self_report / user_reported
   changelog    : +2 dòng wiki/CHANGELOG.md
```

If anything was assumed or left open, say it in the same block — e.g. "as_of chưa rõ, em set `needs_verification: true`, anh xác nhận ngày giúp em."

Per `evidence-gate`: before writing that block, confirm the files exist on disk (`ls -la`, `wc -c`, `rg` the key field). A filing claim is a completion claim.

---

## Hard Rules (from EP P2 — non-negotiable)

1. **One current note per volatile subject.** Rates, location, active work, collaborators: exactly one note may be live. Everything older carries `superseded: true` and points forward.
2. **`as_of` = when the fact was actually true.** Not today. Not "probably last month". If unknown, ask, or set `needs_verification: true`. Today's date is only legitimate in `created` / `updated`, or when the fact genuinely began today.
3. **Record the intake channel.** `sources: [telegram]` + `intake_channel: telegram` for the Telegram gateway; record the real channel when it is not Telegram. Every note must answer "how did this get in here?"
4. **Never overwrite a note in place.** New claim → new file. The old file is annotated additively (status fields + a superseded banner) and keeps its original body and `as_of`.
5. **Never invent a date.** No back-filling, no interpolating from context, no "probably". Missing beats fabricated.
6. **Search before create.** Grep `concepts/` + `entities/` + `projects/` first. A duplicate note on an existing subject is a failed run even if the content is correct.
7. **Links point both ways.** `supersedes` on the new note, `superseded_by` on the old. One-way = broken.
8. **File it even when he didn't ask.** Passing mentions are the primary use case, not an edge case.

---

## Anti-Patterns

- ❌ **`as_of: <today>` because the real date wasn't handy.** Kills the whole supersede chain — every note ends up looking like the newest. This is the single failure EP's prompt exists to prevent.
- ❌ **Editing the old note's claim instead of superseding it.** Destroys history and makes "what did he charge in May?" unanswerable. Contradiction is data; append a status, don't rewrite the past.
- ❌ **Creating note #150 without grepping first.** Result: two live "gear hiện tại" notes with different mics and nothing marking which one is current. Step 2 is not optional.
- ❌ **Only filing when he says "lưu lại".** Families 1–4 arrive unrequested. Skipping them is exactly the drift the vault was built to stop.
- ❌ **Rewriting or reordering `CHANGELOG.md`.** It is append-only. Tidying it deletes the audit trail that makes the vault verifiable.
- ❌ **Stamping `sources: [telegram]` on a CLI turn.** Inventing provenance is the same class of error as inventing a date.
- ❌ **Reporting "đã lưu" without an `ls` / `rg` check.** See `evidence-gate` — filing claims need the same 5-evidence discipline as any other artifact claim.

---

## Verification Checklist

Run before the Step 7 acknowledgement. All five must pass.

| # | Check | Command | Pass condition |
|---|---|---|---|
| 1 | New note exists and is non-empty | `ls -la <path> && wc -c <path>` | file present, size > 0 |
| 2 | `as_of` is not today (unless truly true today) | `rg '^as_of:' <path>` | value ≠ `date +%F`, or explicitly justified |
| 3 | Intake channel recorded | `rg '^sources:\|^intake_channel:' <path>` | both present, channel matches reality |
| 4 | Supersede links point both ways | `rg -n 'supersedes\|superseded_by\|superseded: true' <new> <old>` | new→old and old→new both found |
| 5 | Exactly one live note for the subject | `rg -l '^title:.*<subject>' <folder> \| xargs rg -L '^superseded: true'` | exactly 1 path returned |
| 6 | CHANGELOG grew by the right number of lines | `tail -3 /Volumes/Storage-1/Hermes/wiki/CHANGELOG.md` | 1 line per file touched, correct fields |

Any FAIL → fix and re-verify. Do not report a partial filing as done.

---

## Helper Scripts

| Script | Purpose |
|---|---|
| `scripts/find_target_folder.py` | Free-text snippet → top 3 `(folder, file_path, score, rationale)` candidates via ripgrep/grep over `concepts/`, `entities/`, `projects/`, `comparisons/`, matched against frontmatter `title` + `tags` with **word-boundary** scoring (title 5.0 > tag 3.0 > slug 2.5 > body 1.0, normalised to 0.0–1.0). Skips `_archive*` / `_backup*` / `_template`. Down-weights already-superseded notes ×0.4. Flags `likely_conflict` when the snippet touches a volatile subject. `--json` for machine use. |
| `scripts/log_change.py` | Appends exactly one `CHANGELOG.md` line in the fixed format; opens in `"a"` mode only (never read-modify-write); writes the header on first run. **Refuses** `--as-of` == today (exit 3) unless `--allow-today`, refuses future/invalid dates (exit 2), and refuses `--action supersede` without `--superseded-by` (exit 2) because links must point both ways. |

```bash
cd /Volumes/Storage-1/Hermes/skills/productivity/vault-update
python3 scripts/find_target_folder.py "anh chốt giá booking 3 triệu mỗi video" --json
python3 scripts/log_change.py --file concepts/x.md --action create --reason "test" --as-of 2026-07-31 --dry-run
```

**Verified 2026-08-13 against the live vault:** router correctly sends "chi phí nguyên liệu mì Ý Kontum" → `projects/mi-y-kontum-research/` and surfaces `concepts/mi-y-kontum-business-plan-2026-07-29.md`; gear snippets → `concepts/`; brand snippets → `entities/`. Logger guardrails T1–T6 all behave as specified above (today-date refusal, invalid-date refusal, one-way-link refusal, create+supersede pair, `--allow-today` escape hatch).

Interpretation guide for the router's `verdict`:

| verdict | do this |
|---|---|
| `no_candidates_create_new` | Step 4, create in `suggested_new_note.folder` |
| `likely_conflict_check_supersede` | **read the top candidates before writing**, then Step 5 if the claim differs |
| `possible_existing_note_read_before_create` | read; append or supersede rather than duplicate |
| `weak_matches_probably_create_new` | scan titles once, then Step 4 |

The router **advises**; it never decides. Read the candidate file before choosing create vs supersede.

---

## References

- `references/ep-p2-source.md` — provenance card for EP P2: post ID, what the prompt mandates, and the clause-by-clause mapping to this skill.
- `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md` — immutable raw capture of the full article (all 6 prompts).
- `wiki/SCHEMA.md` — frontmatter contract, tag taxonomy, page thresholds, update policy.
- `wiki/concepts/drift-recovery-3-systems-2026-07-19.md` — why persistence rules get promoted to VĨNH VIỄN here.
- `skills/productivity/evidence-gate/SKILL.md` — the completion-claim gate that Step 7 inherits.
- `skills/nightly-memory-curation/SKILL.md` — the 02:00 consolidation pass that consumes what this skill files.
- `skills/wiki/wiki-maintenance/SKILL.md` — pruning, rotation, health score. Not modified by this skill.
