---
title: Session 2026-06-17 — Cron Jobs for 5-agent company
created: 2026-06-17
session_id: 20260622_220000
type: session-reference
tags: [cron, telegram, agentic-company, ownership]
status: complete
---

# Session 2026-06-17 — 11 cron jobs for the 5-agent company

Tuấn Anh approved the full Loop Engineering company setup: 5 new profiles (qa-agent, engineering-lead, operations-manager, code-reviewer, security-engineer) + 11 cron jobs. All jobs deliver to **O-Lab thread 604** (`telegram:-1003764041476:604`).

## 11 jobs created

| # | Profile | Job name | Schedule |
|---|---------|----------|----------|
| 1 | default (Orchestrator) | Heartbeat | `*/30 8-22 * * *` |
| 2 | default | Daily Briefing | `0 8 * * *` |
| 3 | default | Nightly Reflection | `0 23 * * *` |
| 4 | default | Weekly Cleanup | `0 3 * * 0` |
| 5 | qa-agent | Quality Gate | `0 * * * *` |
| 6 | engineering-lead | Code Health | `0 9 * * *` |
| 7 | operations-manager | Routing Audit | `0 */6 * * *` |
| 8 | code-reviewer | PR Watcher | `0 12 * * *` |
| 9 | security-engineer | Vuln Scan | `0 3 * * *` |
| 10 | memory-curator | Nightly Consolidation | `0 2 * * *` |
| 11 | research-lead | Trend Scan | `0 18 * * *` |

## Cron syntax that works (positional args, then flags)

```bash
hermes cron create "<schedule>" "<prompt>" \
  --name "<job name>" \
  --deliver "telegram:-1003764041476:604" \
  --skill <skill-name>
```

`--prompt` flag does **not** exist. Prompt is the 2nd positional argument, right after the schedule.

## Setup script (drop-in)

The full 11-job setup script lives at `/tmp/setup_cron_jobs.sh` (em wrote it during this session and executed it successfully — 11/11 jobs created).

To re-run: `bash /tmp/setup_cron_jobs.sh` (idempotent only if you check existing job names first; otherwise you get duplicate jobs).

## Verification

Manual trigger + check output:
```bash
hermes cron run <job-id>
sleep 10
ls -la ~/.hermes/cron/output/<job-id>/ | head -5
head -50 ~/.hermes/cron/output/<job-id>/<timestamp>.md
```

Verified working this session: Orchestrator Heartbeat fired at 22:44, wrote 59,339 bytes of output (full state.md of all 5 profiles, table format, "0 stuck / 0 pending QA" all-clear).

## Bot membership gate (NEW lesson)

When Tuấn Anh pasted 7 new bot tokens (`8497520334:***`, `8706108095:***`, etc.), em verified them via `getMe` (all 7 returned valid usernames: TechLead_ClawBot, Researcher_Clawd_Bot, ClawSecurityAllyBot, QAQC_ClawBot, DevOpsClawBot, SaturdayClawdBot, Friday_OCSPBot).

**BUT** when em tried `getChatMember(self, chat_id=-1003764041476)`, all 7 returned **404 Not Found** — meaning the bots have not been added to O-Lab yet. Without that step, cron jobs targeting thread 604 will silently fail to deliver (no membership = no `sendMessage` permission).

**Verification recipe** (Python urllib, see `references/session-2026-06-17-7bots-blocking.md` for full source):

```python
import urllib.request, json
token = "<new-bot-token>"
bot_id = token.split(":")[0]
url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id=-1003764041476&user_id={bot_id}"
with urllib.request.urlopen(url) as resp:
    print(json.loads(resp.read())["result"]["status"])
# Expected: "administrator" → bot is in O-Lab
# If 404 → Tuấn Anh must add the bot to O-Lab first
```

**Blocking issue**: em cannot add bots to the group (no admin UI in tool surface). Tuấn Anh must do this manually in Telegram, then em re-verifies and proceeds.

## API key rotation (independent discovery)

During this session, em discovered the **MiniMax API key had been rotated** (was REVOKED per the memory state at start of session, but had been silently replaced). Cron jobs that had been failing for days started working again **without** explicit user intervention. The gateway's `last run` errors went from `HTTP 401` to `ok` after the new key took effect.

Lesson: when investigating "why aren't my cron jobs running?", always check (a) `~/.hermes/.env` for current key, (b) direct API call to verify the key works, (c) gateway process uptime vs last `.env` mtime. If gateway started before the new key was placed in `.env`, the gateway caches the old key — requires out-of-band restart.

## Open items (next session)

- 7 new bots need to be added to O-Lab supergroup by Tuấn Anh (admin UI, em cannot do this from tool surface)
- After add: re-verify `getChatMember(self)` for each bot → expect `"administrator"`
- Then: create per-profile `.env` files in `~/.hermes/profiles/<name>/.env` with each bot's `TELEGRAM_BOT_TOKEN` so the gateway routes cron output through the right bot
- Cron `--deliver` format doesn't need to change (still `telegram:-1003764041476:604`) — the per-profile `.env` is what determines which bot sends

## What worked well

- 3-layer verify (L1 code exists, L2 behavior test, L3 E2E chain) caught no failures in the 5-agent setup — all profiles passed on first try after copying `.env` and switching model M3 → M2.7 for engineering-lead (M3 timed out at 120s on multi-tool code task).
- Decision-style "lead with trigger conditions, then when NOT to fire" worked well when Tuấn Anh asked "loop kích hoạt ở trường hợp nào?" — gave him trigger list + non-trigger list upfront.
- Tuấn Anh's iterate-từng-cái rule (one profile at a time, verify before moving on) caught the M3 timeout on engineering-lead before it propagated to the other 4 agents.

## What to do differently next time

- Bot membership check should happen BEFORE writing `.env` files. Otherwise em wastes time setting up tokens that can't actually deliver.
- Verify bot tokens via `getMe` first (cheap), then `getChatMember` (cheap), then update `.env` (expensive) — gated, not bulk.