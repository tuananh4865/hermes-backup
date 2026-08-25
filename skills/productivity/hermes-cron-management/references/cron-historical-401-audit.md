---
title: Historical 401 / Auth Failure Audit for Cron Health
created: 2026-06-28
type: reference
tags: [cron, health-check, 401, auth-failure, audit, h38, h39]
applies-to: weekly-cleanup, monthly-audit, post-incident-verification
related: [cron-truth-h38-recipe.md]
---

# Historical 401 / Auth Failure Audit (Layer 2 of Cron Health)

## Problem (discovered 2026-06-28, weekly cleanup)

`hermes cron list` only shows the **most recent run** of each job as `ok` or `error`. This is sufficient for "is the system healthy RIGHT NOW?" but **blind to past failures** that have since recovered.

**Real example from 2026-06-28 cleanup:**
- `hermes cron list` showed all 17 jobs with `ok` status — system looks healthy
- But `grep "non_retryable_client_error.*401" ~/.hermes/sessions/*.json | wc -l` → **27 historical 401 errors**
- Last 401 was on **2026-06-25 19:54** (orchestrator-heartbeat 30m cron, 27 separate sessions)
- The MiniMax 401 burst had resolved by 2026-06-26 — current `ok` state hides 2+ days of failed runs

Without the historical grep, an audit would have reported "all green" while the orchestrator heartbeat had been silently failing for 48 hours.

## The Two-Layer Cron Health Check

**Layer 1 (current state):** `hermes cron list` → ok/error per job
**Layer 2 (historical auth failures):** grep session request dumps for 401 patterns

Always run BOTH in a cron health audit. Layer 1 alone misses resolved-but-not-root-caused incidents.

## Layer 2 Recipe (5 commands)

```bash
# 1. Count session request dumps with 401 errors
grep -l "non_retryable_client_error.*401" \
  ~/.hermes/sessions/*.json 2>/dev/null | wc -l

# 2. Find the MOST RECENT 401 — was the incident resolved?
grep -l "non_retryable_client_error.*401" \
  ~/.hermes/sessions/*.json 2>/dev/null \
  | xargs -I {} stat -f "%Sm %N" "{}" 2>/dev/null \
  | sort | tail -1

# 3. List affected cron jobs
grep -l "non_retryable_client_error.*401" \
  ~/.hermes/sessions/*.json 2>/dev/null \
  | sed -E 's/.*request_dump_cron_([a-f0-9]+)_.*/\1/' \
  | sort -u

# 4. Check current errors.log for ongoing 401s
grep -i "401" ~/.hermes/logs/errors.log 2>/dev/null | tail -10

# 5. Check cron.log specifically
grep -i "401" ~/.hermes/logs/cron.log 2>/dev/null | tail -10
```

## Decision Rules

| Layer 1 (`cron list`) | Layer 2 (historical 401) | Verdict |
|---|---|---|
| All `ok` | 0 historical 401s | ✅ Healthy |
| All `ok` | Historical 401s, last one >7 days ago | ✅ Recovered, log for awareness |
| All `ok` | Historical 401s, last one <7 days ago | ⚠️ **Recent incident** — investigate root cause even if recovered |
| Any `error` | Any 401s | 🚨 **Active failure** — escalate immediately |
| Any `error` | 0 historical 401s | 🔍 Different failure mode — not auth-related, check errors.log |

## MiniMax 401 Pattern (recurring — see SOUL.md)

When the affected provider is **MiniMax**, the root cause is almost always one of:
1. `MINIMAX_API_KEY` missing/empty in `~/.hermes/.env`
2. `.env` not loaded at gateway startup (gateway needs `/restart`)
3. Key sent in `Authorization: Bearer` header instead of `X-Api-Key` (provider requirement)

Detection: every session in a 24h window fails identically with the same 401 pattern → auth config drift, not network blip.

**Fix sequence (do NOT skip steps):**
1. `grep MINIMAX ~/.hermes/.env` — confirm key is present
2. `hermes gateway restart` — reload .env
3. Wait 2 min, trigger one cron manually: `hermes cron run <job_id>`
4. Check `~/.hermes/logs/cron.log` for fresh 401 entries
5. If still failing → check `auxiliary.vision.provider` isn't set to a model requiring a missing key

## When to Use This Layer 2 Check

- **Weekly cron audits** — always include (cheap, catches incidents cron list misses)
- **Post-incident verification** — confirm an auth failure has truly stopped, not just paused
- **Monthly health reports** — historical 401 count over 30 days = good incident metric
- **NOT needed** during interactive sessions or one-off task runs (Layer 1 + session log is enough)

## What NOT to Do

- **Don't trust Layer 1 alone** — "all ok" is current state, not history
- **Don't suppress historical 401s in reports** — they're diagnostic gold, even if resolved
- **Don't auto-restart gateway based on a single 401** — could be transient. Investigate pattern first
- **Don't report "no issues" if Layer 2 shows recent 401s** — be explicit: "all jobs currently ok, but 27 historical 401s between Jun 25-26 from orchestrator-heartbeat, root cause: MiniMax API key rotation. Resolved 2026-06-26."

## Sample Weekly Cleanup Report Section

```
Cron health: ✅ All 17 active jobs: ok (Layer 1)
Historical 401 check: ⚠️ 27 historical 401 errors, last on 2026-06-25 19:54
Affected: orchestrator-heartbeat (job 28c34e383254)
Root cause: MiniMax API key rotation on 2026-06-25, restored 2026-06-26
Current state: resolved — no 401s in last 48h
```

This format tells anh: (a) current is healthy, (b) past failure happened, (c) what fixed it, (d) it's not silently happening again.

## Related

- `cron-truth-h38-recipe.md` — Layer 1 (current cron health check via `hermes cron list`)
- `cron-audit-patterns.md` — 4-step pattern for audit/inspection cron jobs (inventory → classify → honest zero-report → save log)
- `hermes-agent` skill (SOUL.md) — "MiniMax 401 Auth Failure Pattern" section
