---
title: Agentic Company Setup
name: agentic-company-setup
created: 2026-05-04
type: skill
tags: [hermes, multi-agent, telegram, agentic]
description: Setup multiple Hermes agents as company employees - each with own Telegram bot, profile, role, and inter-agent communication
trigger: When user wants to create/expand agentic company structure
---

# Agentic Company Setup

> Setup multiple Hermes agents as company employees — each with own Telegram bot, profile, role, and inter-agent communication

## Architecture

```
Tuấn Anh (CEO - Human, Telegram: @TyayUno)
│
├── Hermes (Anh's main agent - default profile)
│
└── Company Agents (separate Hermes profiles + Telegram bots)
    ├── Content Director (@SaturdayClawdBot) ← TESTED 2026-05-04
    ├── Research Lead (pending)
    ├── Engineering Lead (pending)
    ├── Security Engineer (pending)
    ├── Code Reviewer (pending)
    ├── Refactor Specialist (pending)
    ├── QA Agent (pending)
    └── Operations Manager (pending)
```

## Core Concept

**Each agent = Hermes Profile + Telegram Bot Token**

| Component | Description |
|-----------|-------------|
| Profile | Isolated config, skills, memory, SOUL.md |
| Bot Token | Telegram bot API token for DM capability |
| Role | Defined in SOUL.md |
| Knowledge | Domain-specific wiki |

## Setup Steps (per agent)

### 1. Create Telegram Bot
```
1. Open @BotFather on Telegram
2. Send /newbot
3. Follow prompts to name bot
4. Copy API token
```

### 2. Create Hermes Profile
```bash
hermes profile create <agent-name> --clone-from default
```

> **⚠️ PITFALL (2026-06-17)**: `hermes profile create` generates an EMPTY `.env` and EMPTY SOUL.md. The profile will not function until you populate both. Copy `.env` from a working profile (see step 3 fix), not just the API keys.

### 3. Configure Profile Secrets (CRITICAL FIX)

**Wrong approach** (causes silent 401 errors):
```bash
# ❌ Just copying API keys — leaves out FAL_KEY, AUXILIARY_VISION_*, etc.
echo "MINIMAX_API_KEY=*** > ~/.hermes/profiles/<agent>/.env
# Symptom: 401 "login fail: Please carry the API secret key in the 'X-Api-Key' field"
```

**Right approach** (copy entire .env from a working profile):
```bash
# ✅ Copy full .env from a known-working profile
cp ~/.hermes/profiles/coder/.env ~/.hermes/profiles/<agent>/.env
chmod 600 ~/.hermes/profiles/<agent>/.env

# Required variables (minimum, but copy full file to be safe):
# - MINIMAX_API_KEY          (or openai/anthropic key)
# - HERMES_YOLO_MODE=true    (skip approval prompts)
# - FAL_KEY                  (image generation)
# - EXA_API_KEY              (web search via Exa MCP)
# - AUXILIARY_VISION_API_KEY (image analysis fallback)
# - LM_API_KEY               (utility LLM calls)
```

**Test the profile works before customizing SOUL.md**:
```bash
~/.local/bin/<agent> chat --yolo -q "Reply with just the word PONG." 2>&1 | tail -5
# Expected: "PONG" → profile fully functional
# If 401 → .env missing variables, re-copy from working profile
```

**⚠️ MODEL SELECTION (Pitfall 2026-06-17)**: After copying config.yaml, VERIFY the model name is one that works. Real failure: `qa-agent` failed with 401 when default config had `MiniMax-M3` because the local API key didn't have M3 access. Two fixes work:

```bash
# Option A: Switch to a model the API key can reach
sed -i '' 's|MiniMax-M3|MiniMax-M2.7|g' ~/.hermes/profiles/<agent>/config.yaml

# Option B: Keep M3 if default profile uses it successfully
# (Test default first: `hermes chat --yolo -m MiniMax-M3 -q "PONG"`)
```

**Trade-off (2026-06-17)**: M3 vs M2.7 for different agent types:
- `default` (Orchestrator, planning) → M3 OK (works with same API key)
- `qa-agent` (verification, web search) → M3 works for fast tasks
- `engineering-lead` (code generation, multi-tool) → M2.7 is FASTER (M3 hit 120s timeout on handoff-format test)
- `coder` (existing) → M2.7

**Rule**: After copying config.yaml, run the PONG test. If timeout > 60s on a single-tool task, switch to a faster model. Profile-specific model choice is OK — don't force all profiles to use the same model.

### 4. Define Role in SOUL.md
```bash
nano ~/.hermes/profiles/<agent-name>/SOUL.md
```

> **⚠️ See `references/qa-agent-soul-template.md`** for a complete independent-verifier SOUL.md (the QA Agent pattern), including the separation-of-duties rule that prevents self-verification bias.

### 5. Start Gateway
```bash
hermes gateway --profile <agent-name> start
```

### 6. Verify
```bash
hermes gateway --profile <agent-name> status
tail ~/.hermes/profiles/<agent-name>/logs/gateway.log
```

## Inter-Agent Communication

**CRITICAL: Telegram bots CANNOT DM each other directly**

Solution: Shared Telegram Group
```
1. Anh creates company group on Telegram
2. Adds all agent bots to group
3. Bots communicate via group messages
4. Use @mention to direct message specific agent
```

## Content Director (Tested 2026-05-04)

| Property | Value |
|----------|-------|
| Bot | @ClawdZ1E_Bot |
| Token | (current session token) |
| Profile | content-director |
| Gateway | Running |
| Status | ✅ Online — bot-to-bot working in thread 603 |

## Research Lead (Tested 2026-05-04)

| Property | Value |
|----------|-------|
| Bot | @Researcher_Clawd_Bot |
| Token | `8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0` |
| Profile | research-lead (pending setup) |
| Gateway | Starting |
| Status | ✅ Verified 2026-05-04 |

## Inter-Bot Communication (Verified 2026-05-04)

**Bot-to-bot messaging in Telegram supergroup topics WORKS:**
- Use format: `telegram:-1003764041476:603` (NEGATIVE chat ID + thread ID)
- Both bots must be admins in the supergroup
- Both bots must be in the same thread/topic
- @mention between bots WORKS — bot receives it via Telegram Bot API
- Latency: ~39s for bot-to-bot round-trip (2 API calls)

**Setup for new bot:**
1. Create bot via @BotFather → copy token
2. **MANDATORY**: Add bot as admin to O-Lab supergroup BEFORE any cron deliver target uses `telegram:-1003764041476:604`. A bot that isn't in the group will get `404 Not Found` on `getChatMember(self)` and silent delivery failure on cron output.
3. Ensure bot is added to `channel_directory.json` (auto-updated by gateway)
4. Use `telegram:-1003764041476:THREAD_ID` as target for send_message

**Quick verification that a new bot is in O-Lab** (run with each new bot's token):
```python
import urllib.request, json
token = "<new-bot-token>"
bot_id = token.split(":")[0]
url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id=-1003764041476&user_id={bot_id}"
with urllib.request.urlopen(url) as resp:
    status = json.loads(resp.read())["result"]["status"]
    print(f"Bot in O-Lab: {status}")  # "administrator" = ready for cron delivery
```

If `404 Not Found`: bot hasn't been added to the group yet. Tuấn Anh needs to `/addbot` in O-Lab (or add via Telegram admin UI) before cron jobs targeting thread 604 will work for this bot.

## Role Definitions

### Content Director
- TikTok content strategy
- Script writing
- Trend analysis
- Gen Z slang expertise

### Research Lead (TODO)
- Deep research
- Competitive intel
- Trend monitoring

### Engineering Lead (TODO)
- Code implementation
- Pipeline automation
- Technical architecture

### Security Engineer (TODO)
- Vulnerability scanning
- Security audits
- Threat analysis

### Code Reviewer (2026-06-17)
- **Profile**: `code-reviewer`
- **Status**: ✅ SOUL.md + state.md + E2E verified
- **Role**: 6-axis code review (correctness, style, error handling, type safety, security, testability)
- **Difference from qa-agent**: code-reviewer is QUALITATIVE (good code?), qa-agent is FUNCTIONAL (does it work?)

### Operations Manager (2026-06-17)
- **Profile**: `operations-manager`
- **Status**: ✅ SOUL.md + state.md + E2E verified
- **Role**: Pure task router — decomposes tasks, routes to agents, tracks status
- **Difference from Orchestrator (default)**: ops-manager is a pure router, no work execution. Orchestrator owns the overall goal.

### Security Engineer (2026-06-17)
- **Profile**: `security-engineer`
- **Status**: ✅ SOUL.md + state.md + E2E verified
- **Role**: Security audit — 7-category checklist (injection, secrets, path traversal, unsafe deserialization, file perms, dependency CVEs, auth)
- **Verdict format**: DO_NOT_SHIP / SHIP_OK / FAIL / WARN / PASS
- **Scoring**: 0-10 (lower = more issues found; 2.0 = 2 critical, 9.0 = clean)
- **Difference from code-reviewer**: security-engineer finds vulnerabilities, code-reviewer finds style/best-practice issues. They run in parallel.
- **Test results**: Detected all 4 intentional vulns in /tmp/el-test/vuln.py (shell injection, hardcoded key, pickle, path traversal). Verified /tmp/el-test/secure.py as SHIP_OK.

### QA Agent (2026-06-17)
- **Profile**: `qa-agent`
- **Status**: ✅ SOUL.md + state.md + E2E verified
- **Role**: Independent verifier — 6-check rubric, PASS/WARN/FAIL with score 0-10
- **Independence rule**: NEVER do the work, NEVER verify own work

### Engineering Lead (2026-06-17)
- **Profile**: `engineering-lead`
- **Status**: ✅ SOUL.md + state.md + E2E verified
- **Role**: Code implementation, pipeline automation, technical architecture
- **Workflow**: Implement → Local test (L1+L2) → Handoff to qa-agent → Ship on PASS

### Refactor Specialist (TODO)
- Code quality improvement
- Technical debt reduction
- Pattern optimization

### QA Agent (TODO)
- Testing frameworks
- Error detection
- Quality assurance

### Operations Manager (TODO)
- Task coordination
- Workflow optimization
- Progress tracking

## Separation of Duties — Independent Verifier (CRITICAL 2026-06-17)

**Tuấn Anh's rule**: "Nếu em tự check nó sẽ không còn khách quan nữa và có tỉ lệ cao bị tự nhận PASSED."

**Principle**: Maker ≠ Checker. Agents that produce work MUST be verified by a DIFFERENT profile.

| If agent X produces... | Then agent Y (independent) must verify |
|------------------------|----------------------------------------|
| Code (engineering-lead) | code-reviewer (style) + security-engineer (vulns) + qa-agent (function) — 3-stage chain |
| TikTok script (content-director) | qa-agent |
| Research (research-lead) | qa-agent |
| Wiki update (memory-curator) | qa-agent |
| Task routing (operations-manager) | qa-agent |
| Code review (code-reviewer) | qa-agent (sanity check the reviewer) |
| Security audit (security-engineer) | qa-agent (sanity check the auditor) |

**3-stage chain (engineering-lead → code-reviewer → security-engineer → qa-agent)**: Use when code quality AND security matter (pre-merge, production). The 2-stage chain (engineering-lead → qa-agent) is for quick prototypes. See `references/session-2026-06-17-3stage-chain.md` and `references/session-2026-06-17-final-5agents.md` for E2E test recipes.

**How to enforce**:
1. qa-agent profile is MANDATORY in any multi-agent setup
2. qa-agent has read-only access to others' outputs (verifies, doesn't edit)
3. qa-agent uses a fixed 6-check rubric (see `references/qa-agent-soul-template.md`)
4. Verdict format: `VERDICT: PASS|WARN|FAIL` + `SCORE: 0.0-10.0` + `EVIDENCE:` + `ISSUES:`
5. Default Orchestrator (em) routes outputs to qa-agent before declaring task done

**Anti-patterns to avoid**:
- ❌ Em (default) verifies em's own work → bias, no second opinion
- ❌ "It looks good to me" → vibes, not evidence
- ❌ Skipping verification "to save time" → quality collapse
- ❌ Letting qa-agent also do the work → conflict of interest in reverse

**Loop Engineering pattern** (DO → VERIFY → FIX → LOOP):
```
1. Build/DO the work (engineering-lead, content-director, etc.)
2. SEND to qa-agent for verification
3. IF verdict = PASS/WARN → ship
   IF verdict = FAIL → research, fix, send back to step 2
4. Log verdict to qa-agent's state.md for pattern analysis
```

**Iterate từng bước** (Tuấn Anh 2026-06-17): "Bắt đầu từng cái, làm xong tới đâu check verify lại tới đó đảm bảo mọi thứ hoạt động từng bước nếu lỗi thì research và làm lại cho đến khi hoàn thành, đó là loop mà anh muốn."

→ Don't batch-create multiple profiles. Create ONE, verify it works end-to-end (L1 code + L2 behavior + L3 future-proof), THEN move to the next.

## Orchestrator Decision Tree — AUTO-FIX vs ESCALATE (Tuấn Anh mandate 17/06)

**Context**: After 5-agent company setup, Tuấn Anh granted the Orchestrator (default profile = "em") authority to auto-resolve certain issues without asking. Apply this when Orchestrator runs heartbeat or finds tasks pending.

```
Heartbeat finds task pending / conflict / alert
    ↓
┌────────────────────────────────────────────────────────────┐
│ AUTO-FIX (Orchestrator handles, does NOT ask Tuấn Anh)     │
│                                                           │
│ ✅ Workers stuck >2h → nudge the agent                    │
│ ✅ QA outputs chờ verify >1h → route to qa-agent          │
│ ✅ Cron fail (non-401) → restart or fix config            │
│ ✅ Operations routing chậm → investigate log             │
│ ✅ Security CRITICAL findings → tự fix (per mandate)      │
│ ✅ Agent conflict (2 agents on same file) → tự quyết      │
│   priority (severity > reversibility > cost > deadline)  │
└────────────────────────────────────────────────────────────┘
    ↓
┌────────────────────────────────────────────────────────────┐
│ ESCALATE (ask Tuấn Anh via Telegram thread 604)            │
│                                                           │
│ ❓ Budget issue (API key hết, cost > threshold)           │
│ ❓ Content cần approve (TikTok script trước khi đăng)     │
│ ❓ Anything irreversible or reputation-affecting           │
└────────────────────────────────────────────────────────────┘
```

**Priority matrix when multiple agents conflict on the same file**:
1. **Severity**: Security CRITICAL > HIGH > feature > style
2. **Reversibility**: Fix reversible > irreversible
3. **Cost**: Low cost > high cost
4. **Deadline**: Urgent > not urgent

**Example**: engineering-lead fixing Security CRITICAL + code-reviewer reviewing style → engineering-lead xong trước, code-reviewer review sau (security > style).

**Anti-patterns**:
- ❌ Hỏi Tuấn Anh every 30 minutes → noise, mất focus
- ❌ Auto-approve content without checking → lỡ đăng = mất uy tín
- ❌ Bypass QA "to save time" → no second opinion = quality collapse

## Cron Jobs Setup (MANDATORY after profile creation)

After creating N profiles, set up cron jobs so each profile runs autonomously. **All cron jobs MUST deliver to O-Lab thread 604**: `telegram:-1003764041476:604`.

### Cron Syntax (CRITICAL gotcha — 2026-06-17)

```bash
# ✅ CORRECT: positional args (schedule + prompt first), then flags
hermes cron create "0 9 * * *" "PROMPT HERE" \
  --name "Job Name" \
  --deliver "telegram:-1003764041476:604" \
  --skill hermes-agent

# ❌ WRONG: --prompt flag does NOT exist
hermes cron create "0 9 * * *" --prompt "PROMPT" --name "..."  # ERROR

# ❌ WRONG: prompt after flags gets parsed as unrecognized arg
hermes cron create "0 9 * * *" --name "..." --deliver "..." --prompt "..."
```

**Verified**: 11 cron jobs created successfully in session 2026-06-17 with the correct syntax. See `references/session-2026-06-17-cron-jobs.md` for the 11-job setup script.

### Recommended Cron Schedule for Agentic Company (8 profiles)

| # | Profile | Cron Name | Schedule | Purpose |
|---|---------|-----------|----------|---------|
| 1 | default (Orchestrator) | Heartbeat | `*/30 8-22 * * *` | Check pending, nudge stuck agents, resolve conflicts |
| 2 | default | Daily Briefing | `0 8 * * *` | Send Tuấn Anh daily summary |
| 3 | default | Nightly Reflection | `0 23 * * *` | Self-review, update memory |
| 4 | default | Weekly Cleanup | `0 3 * * 0` | Archive old logs, mark stale state |
| 5 | qa-agent | Quality Gate | `0 * * * *` | Verify pending outputs |
| 6 | engineering-lead | Code Health | `0 9 * * *` | Git status + test suites |
| 7 | operations-manager | Routing Audit | `0 */6 * * *` | Find stuck tasks |
| 8 | code-reviewer | PR Watcher | `0 12 * * *` | Scan uncommitted code |
| 9 | security-engineer | Vuln Scan | `0 3 * * *` | Scan secrets, shell=True, etc. |
| 10 | memory-curator | Nightly Consolidation | `0 2 * * *` | Felix model: read logs, update wiki |
| 11 | research-lead | Trend Scan | `0 18 * * *` | Search Gen Z slang + TikTok trends |

**Verify cron works**:
```bash
# Manual trigger a job
hermes cron run <job-id>

# Check output written to:
ls -la ~/.hermes/cron/output/<job-id>/
head -50 ~/.hermes/cron/output/<job-id>/<timestamp>.md
```

## Test File Naming PITFALL (CRITICAL 2026-06-17)

**Problem**: `disk_cleanup` plugin (Hermes built-in) auto-deletes files matching `test_*.py` or `*.test.py` patterns on `on_session_end` event.

**Symptom**: Test file disappears 8 seconds to 2 minutes after creation, even within the same session.

**Source**: `/Users/tuananh4865/.hermes/disk-cleanup/cleanup.log`

**Code (disk_cleanup.py)**:
```python
_TEST_PATTERNS = ("test_", "tmp_")
_TEST_SUFFIXES = (".test.py", ".test.js", ".test.ts", ".test.md")
```

**Verified safe alternatives**:
- `verify_handler.py` ✅
- `check_handler.py` ✅
- `test.py` ✅ (lacks `_` prefix)
- `handler_test.py` ✅

**Verification command**:
```python
import re
test_patterns = ("test_", "tmp_")
suffixes = (".test.py", ".test.js", ".test.ts", ".test.md")
filename = "your_file.py"
will_delete = filename.startswith(test_patterns) or filename.endswith(suffixes)
print(f"{filename}: {'❌ WILL DELETE' if will_delete else '✅ SAFE'}")
```

**Rule**: Never name test files `test_*.py` in `~/.hermes/hooks/` or any tracked directory. Use `verify_*.py` instead.

## Reference Files

- `references/agentic-company-gap-analysis.md` — gap checklist (8 roles vs current state), SOUL.md template skeleton, diagnostic command, fix recipes. Read this BEFORE creating new profiles.
- `references/qa-agent-soul-template.md` — complete independent-verifier SOUL.md template (copy + customize for new QA agents). Includes 6-check rubric, anti-bias rules, output format.
- `references/session-2026-06-17-engineering-lead.md` — session notes from the qa-agent + engineering-lead pair test: 3-layer verify pattern, M3 vs M2.7 trade-off, "load skill BEFORE creating" lesson.
- `references/session-2026-06-17-3stage-chain.md` — second half of session: operations-manager + code-reviewer profiles, **3-stage maker→reviewer→qa chain** demonstrated in production, 4-agent E2E test recipe, "lead with trigger conditions" decision-style rule.
- `references/session-2026-06-17-final-5agents.md` — final part: security-engineer profile, full **4-stage chain (eng→reviewer→security→qa)**, 5-agent E2E test, separation-of-concerns matrix, "iterate one at a time" rule (Tuấn Anh 2026-06-17).
- `references/session-2026-06-17-cron-jobs.md` — cron jobs setup for 5-agent company: 11 new jobs, syntax gotcha (`--prompt` flag doesn't exist), delivery to thread 604, Orchestrator decision tree, API key rotation discovery.
- `references/session-2026-06-22-7bots-blocking.md` — 7 new bot tokens received, all 7 verified via `getMe`, all 7 fail `getChatMember(self)` against O-Lab with 404. Blocking issue: Tuấn Anh must add bots to O-Lab manually via Telegram admin UI before cron delivery to thread 604 works for those bots. Includes fallbacks (single-bot + prefix).

## Known Issues

1. **Telegram bots can't DM each other** - must use shared group
2. **Profile tokens stored in .env** - ensure security
3. **Gateway per profile** - each needs separate process
4. **Cannot restart gateway from inside a gateway-owned session (2026-06-17)** - `pkill -f "hermes_cli.main gateway"` from a tool call inside the running gateway returns "Blocked: cannot restart or stop the gateway from inside the gateway process. The gateway would kill this command before it could complete (SIGTERM propagates to child processes)." Same for `kill <pid>`. The fix is `hermes gateway restart` run from a separate terminal session, not from the Hermes tool. If a cron job's API key rotates (e.g. 401 → new key in `~/.hermes/.env`), the gateway caches the old key in its loaded env. The visible cron error will keep showing 401 until the gateway process is restarted out-of-band. Verified this session: direct API call worked with the new key, but cron runs failed until restart.

## Paths

| Path | Purpose |
|------|---------|
| `~/.hermes/profiles/` | All agent profiles |
| `~/.hermes/profiles/<name>/SOUL.md` | Role definition |
| `~/.hermes/profiles/<name>/.env` | Bot token |
| `~/.hermes/profiles/<name>/logs/` | Gateway logs |

## Testing New Agent

```bash
# 1. Check bot is reachable
curl https://api.telegram.org/bot<TOKEN>/getMe

# 2. Start gateway
hermes gateway --profile <name> start

# 3. Check logs
tail -f ~/.hermes/profiles/<name>/logs/gateway.log

# 4. Send test message via BotFather
# Or: DM the bot on Telegram
```
