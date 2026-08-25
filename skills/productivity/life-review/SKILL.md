---
name: life-review
description: "Use when anh hỏi today brief / weekly review / monthly summary / quarterly review / stalled goals / project blockers / habit consistency / vault health. Reads-only check across Tuấn Anh's wiki + projects, delivers compact Telegram brief via 4 cron cadence (daily 07:30 ICT, weekly Sunday 18:00, monthly 28th 09:00, quarterly 90 days). Composed with daily-session-review skill; does NOT replace it. Parsed from EP (@eptwts) Post B 9-phase Life OS Phase 7 (reusable skills, validate independently) + EP vault P6 weekly check (Don't fix any of it)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [life-os, cron, weekly-review, telegram, obsidian-vault, second-brain, knowledge-base, hermes-agent, tuấn-anh, ep-eptwts]
    related_skills: [daily-session-review, nightly-memory-curation, project-checklist-management, hermes-cron-management, default-project-hub-pattern, evidence-gate, hermes-agent-decision-guard]
    composed_with: [daily-session-review]
    replaces: []
    frequency_profile: [daily, weekly, monthly, quarterly]
    delivery_channels: [telegram, local]
    timezone: Asia/Ho_Chi_Minh
---

# Life Review Skill — 4 Cadence Brief System

> **What this is:** A read-only, evidence-cited briefing system for Tuấn Anh's personal life + work OS. Four scheduled cadences (daily brief, weekly review, monthly summary, quarterly review) read the wiki + project hubs and emit compact Telegram-ready messages.
>
> **Source inspiration:** EP (@eptwts) Post B "9-phase Life OS" Phase 7 directive (reusable skills with predictable behavior, exact ops, independent validation — see `references/ep-source.md`) paired with EP vault prompt 6 "the weekly check" (Don't fix any of it — just send me the list).
>
> **Composition rule:** This skill READS from the same wiki Tuấn Anh's `daily-session-review` writes to, but does NOT replace or duplicate `daily-session-review`'s content creator filter / 0h cron logic. Each skill keeps its lane.

## When to Use

Apply this skill when the trigger phrase matches one of 8 patterns — manual invocation OR automatic cron delivery:

| # | Cadence | Vietnamese trigger | English trigger |
|---|---|---|---|
| 1 | Daily brief | "today brief" / "brief hôm nay" / "today checklist" / "sáng nay làm gì" | "what's on today" / "today's plan" / "morning brief" |
| 2 | Weekly review | "weekly review" / "review tuần" / "tuần này sao rồi" / "week recap" | "week summary" / "end of week check" |
| 3 | Monthly summary | "monthly summary" / "tổng kết tháng" / "cuối tháng" / "tháng review" | "month-end summary" / "month recap" |
| 4 | Quarterly review | "quarterly review" / "tổng kết quý" / "90 days" / "life goals progress" | "quarterly audit" / "90-day check" |
| 5 | Stalled goals (any cadence) | "stalled goals" / "goal nào kẹt" / "đang kẹt ở đâu" | "what's stalled" / "stuck goals" |
| 6 | Project blockers (any cadence) | "project blockers" / "dự án nào block" / "bị nghẽn chỗ nào" | "project blockers" / "what's blocking me" |
| 7 | Habit consistency (weekly+) | "habit consistency" / "thói quen có đều không" | "habit streak" / "consistency check" |
| 8 | Vault health (weekly+/manual) | "vault health" / "wiki có gì stale không" / "broken links" | "stale notes" / "broken wiki links" |

**Auto-triggered by cron jobs (NEVER requires user typing):**

- Daily brief: `0 7 * * *` (07:30 Asia/Ho_Chi_Minh) → Telegram `1132914873`
- Weekly review: `0 18 * * 0` (Sunday 18:00 ICT) → Telegram `1132914873`
- Monthly summary: `0 9 28 * *` (28th of month 09:00 ICT) → local first, manual send
- Quarterly review: `0 9 1 */3 *` (Jan/Apr/Jul/Oct 09:00 ICT) → local first, manual send

## Why This Exists — EP Phase 7 + EP P6 + Drift Recovery

### EP Phase 7 (Post B, 2026-08-10, 24,007 chars)

The Phase 7 directive of EP's nine-phase framework asks the operator to make durable agent capabilities for capturing, retrieving, correcting, and maintaining context, expressed as YAML-frontmattered skills whose structure is repeatable, whose commands are exact, and whose success can be checked on its own. The standard for each skill in that set: it predictably changes behavior, uses exact operations where possible, and validates independently. The 9 skills EP names explicitly are `life-tracker, goal-planning, life-review, weekly-check, habit-tracker, project-tracker`. This skill is the `life-review` slot in that list, paired with the `weekly-check` behavior through the same prompt 6 pattern. [Source: `wiki/raw/articles/ep-life-os-prompt-2026-08-13.md` L38 (skill roster) + L323 (skill authoring rules) + L398 (validation standard).]

### EP Prompt 6 — The Weekly Check (Post A, 2026-07-23, 10,907 chars)

EP's vault article prompt six set up a Sunday-six-pm cron whose only job is to inspect the vault and surface problems: summaries that are older than their underlying notes, notes missing a date or status, duplicate identifiers, links pointing at missing files, and items still marked current when their evidence is more than six months old. The phrasing is explicit: **don't fix any of it, just send the list.** The reason given is to keep the agent from silently rewriting the knowledgebase on its own judgment. [Source: `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md` L122-L130.]

### Tuấn Anh's 2026-07-19 drift recovery

In the major wiki cleanup of 2026-07-19, archived folders were mass-moved without an explicit non-destructive read-only inspection pass first. The cleanup shipped without a stub-check, so things like `_template/` got moved into `_disabled_2026-07-19/` and required manual rescue. A **read-only** briefing skill — one that ONLY reads, aggregates, and reports — prevents the same class of silent-fix failure that ruin a knowledgebase when an agent oversteps user intent. This skill is the explicit `safe-default` answer to drift-recovery drift: report findings, do not mutate.

### Gap analysis row (2026-08-13)

The gap analysis at `wiki/concepts/ep-profile-research-2026-08-13.md` L151 names `life-review` as one of six agent skills from Post B still missing. Phase 7 explicitly authorizes the build. This skill is the artifact.

## Core Workflow

The skill has four sub-workflows, one per cadence. They share a small library at `scripts/` and produce JSON for downstream delivery.

All four share the same top-level guard: **READ-ONLY**. No file under `/Volumes/Storage-1/Hermes/wiki/` is written by this skill during a normal run. If a fix is implied (e.g. an archive recommendation), the brief lists the file path + date and asks the user for explicit approval; the skill never acts.

### Sub-workflow A — Daily Brief (07:30 ICT)

**Goal:** Produce a ≤200-word Telegram-message-ready snapshot of today: top 3 active goals, 1 leading metric, 1 project's next action, top 3 recent log entries, any active habits if tracked.

**Inputs:**

- `wiki/entities/learned-about-tuananh.md` — top 20 lines (latest user-context window)
- `wiki/log.md` — 3 most recent dated entries
- `wiki/projects/<active-project>/HUB.md` — `next_action` field
- `wiki/projects/` — directory listing to pick the most-recently-updated hub

**Steps:**

1. Read `learned-about-tuananh.md` head (top 20) for current context window.
2. Tail `wiki/log.md` for the 3 most recent dated entries (filter on `## [YYYY-MM-DD]` heading line).
3. Find active project hub: sort `wiki/projects/*/HUB.md` by mtime, pick top 1 (excluding `_template` and `_backup`).
4. From the chosen hub, extract the `next_action` field (single-line).
5. Pull the 3 active goals from the most-recently-modified file in `wiki/projects/<active>/` that has a `goals:` block, OR fall back to top-of-file `## Goals` heading.
6. Pick 1 metric: the first numeric field in the chosen hub's `## Current Numbers` section. If absent, state "no metric tracked".
7. If `wiki/habits.md` or `wiki/projects/_meta/habits.md` exists, pull last 7 days of completion. Otherwise, `active_habits: []`.
8. Format the brief into a compact Telegram-ready payload (Vietnamese heading + compact bullets, **≤200 words**).
9. Deliver via cron hook → Telegram channel `1132914873`.

**Script:** `scripts/daily_brief.py` → emits JSON `{date, top_3_goals: [...], one_metric, one_project_next, active_habits: [...], recent_log_entries: [...], telegram_message: "<string ≤200 words>"}`.

**Output sample (target):**

```
📅 Daily Brief — Tue 2026-08-13

🎯 Top 3 Goals:
  1. Ship life-review skill (today)
  2. Hermes Agent drift recovery audit (this week)
  3. Daily TikTok scripting pipeline v6 (Aug)

📊 Metric: Wiki daily-session-review cron kept pass-rate 4/4 last night

🚧 Project next: tuấn-anh-badminton — next_action: re-edit clip_0093 v3 with com­pacted audio fade

📝 Recent log:
  - 12/08 23:50 nightly-memory-curation PASS (4 captures, 0 conflicts)
  - 12/08 19:20 short-form evidence-gate refactor shipped v1.5.0
  - 12/08 14:05 mi-y checklist v3 launchpad

🔁 Habits (7d): 6/7 morning session, 5/7 warehouse reset, 0/3 badminton drills.
```

### Sub-workflow B — Weekly Review (Sunday 18:00 ICT)

**Goal:** Read-only audit of the wiki and active projects. Surface (a) completed projects, (b) stalled goals (no `next_action` update in 7+ days), (c) project blockers, (d) habit consistency (if tracked), (e) superseded entities count, (f) broken links. Compact format (≤500 words).

**Inputs:** Full wiki scan + `wiki/projects/_meta/supersedes/` if present.

**Steps:**

1. Scan `wiki/projects/*/HUB.md` for `status: archived` or `status: completed` markers — list.
2. Stalled detection:
   - For each project hub, read the `next_action` line and its mtime.
   - If mtime is older than 7 days and `status: active`, flag as stalled; compute `days_since_update`.
3. Superseded entities: count entries under `wiki/concepts/*superseded*.md` OR files tagged `supersedes: true` in frontmatter. Sum.
4. Habit consistency: if `wiki/habits.md` exists, group the last 7 days of completion events. Report consistency %.
5. Duplicate IDs: simple heuristic — collapse any concept or entity ID like `2026-08-13-XXX` to counts and surface duplicates >1.
6. Notes missing dates: count frontmatter without an `updated:` field.
7. Broken links: opportunistic scan of `[[wikilink]]` references; cross-check existence. Provide top 5 broken-link candidates (full scan is slow; sub-sample).
8. Emit JSON; format Telegram message ≤500 words; deliver.

**Script:** `scripts/weekly_review.py` → emits JSON `{week_start, completed_projects: [...], stalled_goals: [{file, days_since_update, next_action}], habit_consistency: {habit, done: N, total: 7}, superseded_count: N, missing_date_count: N, broken_link_candidates: [...]}`.

### Sub-workflow C — Monthly Summary (28th 09:00 ICT)

**Goal:** Aggregate 4 weekly reports. Adjust cron triggers. Recommend light archive pass (read-only scan + recommendation log; no auto-archive).

**Inputs:** Read `wiki/lessons/<current-month>/` + 4 most recent weekly briefs.

**Steps:**

1. Read previous monthly summary (if any) from `wiki/_meta/life-review/<YYYY-MM>.md`.
2. Read 4 most recent weekly brief JSONs from `wiki/_meta/life-review/weekly/`.
3. Aggregate counts: stalled-goal weekly trend, completed projects this month, habit consistency averages.
4. Recommendation list:
   - Triggers to adjust (e.g. "daily brief too noisy at 07:30 → move to 07:00").
   - Files older than 90 days in `wiki/projects/` to consider for archive.
   - Suggestions for new entities/concepts surfaced in lessons.
5. **NEVER** auto-archive — write the recommendation to `wiki/_meta/life-review/<YYYY-MM>-summary.md` as a soft proposal only. User approves next-day.
6. Emit summary; deliver via Telegram (or local — see Cron Setup notes).

**Script:** Uses `scripts/weekly_review.py` as input; aggregator is inline Python or `scripts/monthly_summary.py` (future).

### Sub-workflow D — Quarterly Review (Jan / Apr / Jul / Oct — 09:00 ICT)

**Goal:** Aggregate 3 monthly summaries. Read `wiki/70-goals/` (if it exists) and surface life-goals progress. Project delivery %. Recommend goal reprioritization.

**Inputs:** 3 monthly summaries + active project hubs.

**Steps:**

1. Read the 3 most recent monthly summary files.
2. Read `wiki/70-goals/` if it exists; extract top goal entries.
3. For each top-level goal, count progress evidence: `next_action` mentions in any hub in the last 90 days, lessons referencing the goal, etc.
4. Compute project delivery % = (projects with `status: archived` or `status: completed` in the quarter) / (all projects touched in the quarter).
5. Produce a ≤1000-word briefing: 3 monthly → 1 quarterly narrative.
6. Recommend reprioritization (e.g. "drop goal X, promote goal Y"); never auto-edit.
7. Deliver locally first — user reviews + sends explicitly.

## Hard Rules

These are BẮT BUỘC for every cadence. The skill is safe-by-default.

1. **READ-ONLY.** No write to `wiki/` unless the user has explicitly typed an approval in the current session. Recommendations go in `wiki/_meta/life-review/` (a meta-only path that the user explicitly owns; the skill still only WRITES there after explicit approval).
2. **Compact format.** ≤200 words daily, ≤500 weekly, ≤1000 monthly/quarterly. Telegram-friendly.
3. **Cite file paths + dates.** Every finding carries `(path/to/file.md L<line> + YYYY-MM-DD)`. No statement without provenance.
4. **State uncertainty.** When a number is missing or untracked, the brief explicitly says so. EP rule: "preserve uncertainty and conflicts."
5. **Never invent data.** No filler goals, no fabricated habit percentages, no made-up completion counts. If absent → state "no data".
6. **Don't fix any of it.** Direct lift of EP P6 wording. Read, surface, report. User approves.
7. **Validate independently.** Re-run the JSON output through `python -c "import json; json.load(open(...))"` before delivering. If the schema breaks, do not deliver — surface the failure.
8. **Vietnamese heading preference.** Briefs default to Vietnamese headings + bullets unless user requests otherwise.
9. **No emoji bombs.** The sample uses 4 emoji; cadence briefs may use up to 6. No more.

## Cron Setup

The four cron jobs are set up via `scripts/setup_cron.sh`. The script is **dry-run by default**: it prints the planned `hermes cron create` invocations but does NOT execute them. The user (Tuấn Anh) reviews the schedule and runs the script with `--apply` to actually create the jobs.

### Sample schedules (printed by setup_cron.sh --dry-run)

```
hermes cron create \
  --name "life-review-daily-brief" \
  --schedule "0 7 * * *" \
  --timezone "Asia/Ho_Chi_Minh" \
  --prompt "Run /skill life-review cadence=daily and deliver to telegram:1132914873" \
  --deliver "local" \
  --notify_on_complete true

hermes cron create \
  --name "life-review-weekly-review" \
  --schedule "0 18 * * 0" \
  --timezone "Asia/Ho_Chi_Minh" \
  --prompt "Run /skill life-review cadence=weekly and deliver to telegram:1132914873" \
  --deliver "local" \
  --notify_on_complete true

hermes cron create \
  --name "life-review-monthly-summary" \
  --schedule "0 9 28 * *" \
  --timezone "Asia/Ho_Chi_Minh" \
  --prompt "Run /skill life-review cadence=monthly, deliver=local, require user approval before send" \
  --deliver "local" \
  --notify_on_complete true

hermes cron create \
  --name "life-review-quarterly-review" \
  --schedule "0 9 1 */3 *" \
  --timezone "Asia/Ho_Chi_Minh" \
  --prompt "Run /skill life-review cadence=quarterly, deliver=local, require user approval before send" \
  --deliver "local" \
  --notify_on_complete true
```

**Local-first for monthly and quarterly** — until Tuấn Anh trusts the format, the two slower cadences write to `wiki/_meta/life-review/YYYY-MM-DD-cadence.md` and stop. User reviews + manually `hermes send --file <path>` after approval. This is the BẮT BUỘC safe path.

**Daily + weekly auto-deliver** — these are scoped tighter and parameterized, so once Tuấn Anh has seen the format hold for 1–2 weeks, he can promote `deliver` from `local` to `telegram:1132914873` directly via `setup_cron.sh --apply --promote`.

## Integration

- **`daily-session-review` (sister skill)** runs at 0h00 with a content-creator filter, reads previous-day review files, emits a Telegram digest. `life-review` does NOT duplicate that filter — it READS from `wiki/log.md` which that skill also writes to. No interference.
- **`nightly-memory-curation` (cron 02:00)** consolidates durable facts. `life-review` may reference what `nightly-memory-curation` captured, but does not write to the curation store.
- **`hermes-cron-management`** provides the `hermes cron create` CLI surface the setup script wraps. The skill does not redefine cron scheduling — it just schedules itself.
- **`evidence-gate`** — every delivery from this skill MUST satisfy the 5-Evidence Gate: the brief is generated by running `scripts/<cadence>.py`, the output is JSON-validated, the Telegram message_id is captured, the path + line citations are paste-able in the brief.

## Verification Checklist (BẮT BUỘC after every run)

- [ ] Skill output JSON parses cleanly (`python -c "import json; json.load(open(<path>))"` returns 0)
- [ ] All cited file paths exist (`stat <path>` for each citation)
- [ ] Word count ≤200 daily / ≤500 weekly / ≤1000 monthly/quarterly
- [ ] No emojis beyond 6 in the Telegram message
- [ ] Telegram `message_id` returned for daily + weekly cron deliveries
- [ ] Local file path written for monthly + quarterly cron deliveries (user reviews before send)
- [ ] No write to `wiki/` outside `wiki/_meta/life-review/`
- [ ] No invented data: every numeric field backed by a (path + line) citation

## Failure Modes & Recovery

| Symptom | Cause | Recovery |
|---|---|---|
| `daily_brief.py` exits non-zero | Missing wiki path | Verify `WIKI_ROOT=/Volumes/Storage-1/Hermes/wiki/`; run `--self-check` |
| Telegram message split into chunks | Word count exceeded | Re-render with stricter word ceiling; not deliver until ≤200 |
| Stalled-goal list empty despite 14d no-update | mtime heuristic wrong on iCloud mount | Cross-check with `log.md` last-touched-date; flag as `data_quality: low` |
| Monthly summary too long | Aggregator pulls too many weekly briefs | Cap at 4 weeks input; surface "earliest aggregated week: ..." |
| Quarterly review has no `70-goals/` data | Skill folder absent | Recommend seed note; do not fabricate; report as `goals_tracked: 0` |

## Lifecycle

- **v1.0.0 (2026-08-13)** — Initial build. 4 cadence. Read-only. EP Phase 7 + P6 verbatim trace.
- **Future** — when user types `promote life-review to: <cadence>` the skill may flip delivery target via `setup_cron.sh --apply --promote --target <id>`.
- **Sunset rule** — if no run for 30 days (no evidence-gate trace), skill should report `untested` on next invocation and recommend deletion or re-test.

## References

- `references/ep-source.md` — EP Phase 7 + EP P6 verbatim citations (paraphrased), with line-number provenance.
- `scripts/daily_brief.py` — Daily brief generator (JSON out).
- `scripts/weekly_review.py` — Weekly review generator (JSON out).
- `scripts/setup_cron.sh` — Cron installer (dry-run default; --apply promotes).
- Cross-ref: `wiki/raw/articles/ep-life-os-prompt-2026-08-13.md` L38, L323, L398.
- Cross-ref: `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md` L122-L130.
- Cross-ref: `wiki/concepts/ep-profile-research-2026-08-13.md` L85 (P6 row), L151 (gap row).
