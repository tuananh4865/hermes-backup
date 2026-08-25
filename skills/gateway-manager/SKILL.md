---
name: gateway-manager
description: Manage Hermes Gateway lifecycle - restart, check status, troubleshoot channel adapters (Telegram/Discord/Slack)
---

# Gateway Manager Skill

## Gateway Architecture trên macOS

Gateway chạy qua **2 lớp auto-restart**:

```
launchd (plist) → run_hermes_gateway.sh (while-true loop) → hermes gateway
```

### Layer 1: launchd plist
- **File**: `~/Library/LaunchAgents/ai.hermes.gateway.plist`
- **Auto-start**: khi macOS khởi động (RunAtLoad: true)
- **Restart**: nếu script crash (KeepAlive: SuccessfulExit: false)

### Layer 2: run_hermes_gateway.sh
- **Location**: `~/.hermes/run_hermes_gateway.sh`
- **Logic**: while-true loop → restart gateway nếu crash
- **Restart delay**: 5 giây

## Commands

### Check Gateway Status
```bash
# Tất cả gateway processes (nhiều PID = bình thường nếu nhiều profile)
ps aux | grep -E "hermes.*gateway|gateway.*run" | grep -v grep

# Check launchd quản lý (PID 790 = content-director, PID 64965 = default — cả 2 PPID=1 = launchd managed)
launchctl list | grep hermes

# Kiểm tra process hierarchy (PPID=1 = launchd managed, OK)
ps -p <PID> -o pid,ppid,start,command

# Xem logs ( Telegram reconnect attempts auto-recover )
tail -20 ~/.hermes/logs/gateway.log
```

### Multiple Profiles = Multiple PIDs — BUT ONLY IF EACH HAS ITS OWN BOT TOKEN

The previous version of this section said "Multiple Profiles = Multiple PIDs (BÌNH THƯỜNG)" with no caveat. **That's wrong when profiles share a Telegram bot token.** If they all read the same `TELEGRAM_BOT_TOKEN` from `.env`, both processes race for every Telegram update via `getUpdates` and the user gets whichever profile wins the race — bot identity, model, `require_mention`, everything silently shifts to that profile's `~/.hermes/profiles/<name>/config.yaml`, ignoring `~/.hermes/config.yaml`.

**Verified 2026-07-07:** Two PIDs were running concurrently — one `--profile content-director` (8h43m old, `model.default: MiniMax-M2.7`) and one default (13m old, `model.default: MiniMax-M3`). User reported the bot responding with the wrong model + ignoring non-mention messages in the group. Same root cause.

**Safe pattern (multiple profiles + same channel):**
- ✅ Different Telegram bot token per profile (one bot token = one profile = one PID)
- ✅ OR: only ONE default profile running, others paused
- ❌ Multiple profiles + shared `TELEGRAM_BOT_TOKEN` from `.env`

When in doubt: kill all, restart one default gateway. `~/.hermes/profiles/<name>/config.yaml` model overrides are ONLY safe if each profile has its OWN bot token registered.

See **⚠️ Multi-Gateway Same-Bot-Token Conflict** pitfall below for full diagnostic + 4-option fix menu.

### Restart Gateway
```bash
~/.hermes/restart_gateway.sh
```

### Manual Start (nếu cần)
```bash
cd ~/.hermes && ./run_hermes_gateway.sh
```

## WARNING: Gateway Graceful Restart Does NOT Reload Python Modules

**Critical pitfall:** `hermes gateway restart` (via request protocol) is a **graceful restart** — it restarts the service but Python modules stay MEMORY-MAPPED. Old `.pyc` pycache files and previously-loaded module state persist.

**When this matters:**
- After patching `kanban_db.py` or other core modules
- After clearing `__pycache__`
- When workers still fail despite code fixes

**Symptom:** Worker continues failing with the same error even after multiple `hermes gateway restart` calls. Gateway logs show the new code isn't being picked up.

**Fix: Hard kill + start fresh**
```bash
# 1. Find gateway PIDs
ps aux | grep "hermes_cli.main gateway" | grep -v grep

# 2. Kill hard (not graceful restart)
kill -9 <pid>  # -9 = SIGKILL, forces process death

# 3. Wait a moment
sleep 2

# 4. Restart via run_hermes_gateway.sh
cd ~/.hermes && ./run_hermes_gateway.sh
```

**When to use hard kill vs graceful restart:**
| Scenario | Method |
|----------|--------|
| Config change only | graceful restart OK |
| Code/patch change | Hard kill required |
| Worker still crashing after graceful restart | Hard kill required |
| Pycache suspected | Hard kill required |

### Debugging Worker Issues After Patch

When workers fail with `Unknown skill(s): kanban-worker` or similar errors after patching code:

```bash
# 1. Verify patch is in the file
grep -n "_kanban_worker_skill_available" ~/.hermes/hermes-agent/hermes_cli/kanban_db.py

# 2. Verify skill exists at expected path
find ~/.hermes/profiles/<profile>/skills -name "kanban-worker" -type f

# 3. Clear pycache in the hermes-agent venv
find ~/.hermes/hermes-agent/hermes_cli -name "__pycache__" -exec rm -rf {} +

# 4. Hard kill the gateway (NOT graceful restart)
ps aux | grep "hermes_cli.main gateway" | grep -v grep
kill -9 <pid>

# 5. Restart
cd ~/.hermes && ./run_hermes_gateway.sh
```

## Troubleshooting

### Lỗi "Could not find service ai.hermes.gateway"
- Đây là lỗi systemd - BỎ QUA trên macOS
- Gateway chạy standalone, không dùng systemd

### Gateway không respond
```bash
pkill -f "hermes_cli.main gateway"
sleep 2
cd ~/.hermes && ./run_hermes_gateway.sh
```

### Duplicate Gateway Conflict
Nếu thấy 2+ gateway processes cùng chạy (conflict Telegram bot token):
1. Kiểm tra process hierarchy: `ps -p <PID> -o pid,ppid`
2. Nếu PPID=1 → được quản lý bởi launchd
3. Kill process thủ công hoặc unload plist:
   ```bash
   launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist
   ```

### ⚠️ Multi-Gateway Same-Bot-Token Conflict (verified 2026-07-07)

**Symptom:** User reports Telegram bot replies with the wrong model (e.g. `MiniMax-M2.7` in the post-`/new` banner even though `model.default: MiniMax-M3` in `~/.hermes/config.yaml`) AND/OR bot ignores messages in a group chat unless `@mention`-ed.

**Root cause:** Two `hermes gateway run` processes registered the same `TELEGRAM_BOT_TOKEN`. Telegram Bot API dispatches each update to **only one** of them (first to call `getUpdates`). The user gets whichever profile that process is bound to — model + `require_mention` + every config-y thing therefore silently drifts from what `~/.hermes/config.yaml` shows.

**Why the previous "Multiple Profiles = Multiple PIDs" section was wrong:** It said multiple profiles = multiple PIDs is bình thường. That is only safe when each profile uses a **different** Telegram bot token (one bot per profile). If they all share `.env`'s `TELEGRAM_BOT_TOKEN`, they fight for the same updates → symptom above. (See the rewritten "Multiple Profiles = Multiple PIDs" section above.)

**Detection recipe (verified 2026-07-07):**
```bash
# 1. List EVERY gateway process — capture PID + uptime + full command
ps aux | grep -E "hermes_cli.main.*gateway" | grep -v grep
# Flag: if any 2 lines show elapsed time vastly different (e.g. 8h43m vs 13m),
#       one is stale from an earlier session and still holding the bot token.

# 2. For each PID, show what profile + what model it's bound to
for pid in $(pgrep -f "hermes_cli.main.*gateway"); do
  echo "=== PID $pid ==="
  ps -p "$pid" -o pid,etime,command
  echo "Profile: $(ps -p "$pid" -o command | grep -oE -- '--profile [^\s]+' || echo default)"
done

# 3. For each profile, resolve effective model
for prof in content-director default; do
  cfg="$HOME/.hermes/profiles/$prof/config.yaml"
  [ -f "$cfg" ] && grep -E "^  default:" "$cfg" | head -1 | awk -v p="$prof" '{print p": "$0}'
done
grep -E "^  default:" "$HOME/.hermes/config.yaml" | head -1 | awk '{print "default parent: "$0}'
# If any profile shows MiniMax-M2.7 but parent shows MiniMax-M3, that's the culprit.
```

**Fix recipe — pick by case (4-option menu, validated 2026-07-07):**
| Option | Action | When |
|--------|--------|------|
| A | Kill stale PID, keep the one that matches parent config | User wants default profile behavior |
| B | Kill the matching one, keep the stale | User is intentionally running a profile-specific stack |
| C | Update stale profile's `config.yaml` → parent model, restart cleanly | User wants BOTH running but on same model (still risky with shared token) |
| D | Stop BOTH, restart via `~/.hermes/run_hermes_gateway.sh` (default) | Clean slate after debugging |

**Hard kill (NOT graceful restart — graceful reloads modules but keeps the bot registration alive):**
```bash
ps aux | grep "hermes_cli.main.*gateway" | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 2
~/.hermes/run_hermes_gateway.sh &
sleep 8
grep "Connected as\|No messaging platforms" ~/.hermes/logs/gateway*.log | tail -3
```

**Verify the fix:** After restart, send a NEW message to the bot. The post-`/new` banner MUST show the same model as `~/.hermes/config.yaml`'s `model.default`. If it shows anything else, the stale PID is still alive (kill -9 it again) or another long-running process is bound to the same token.

**If Telegram stays silent AFTER the multi-gateway fix (bot not responding, "anh nhắn tele không có phản hồi"):** → token lock recovery recipe is needed. See `references/telegram-token-lock-recovery-2026-07-07.md` for the 5-step recipe (kill → unload launchd plist → sleep 5 → load → curl verify `getUpdates`). Symptom is `[Telegram] Telegram bot token already in use (PID X)` repeating in `gateway.error.log`.

**Anti-pattern (DO NOT DO):** Tell the user "your config looks correct" and ship a fix while a duplicate gateway is still holding the bot token. The duplicate wins the getUpdates race and the user keeps seeing the wrong model until the stale PID is killed. **Verify by killing the stale process BEFORE claiming "fixed".**

**Cross-reference:** `hermes-config-edit` skill — has Pitfall #10 about profile-vs-default model override (sibling pattern: same config drift but from `config.yaml` reads instead of process arbitration).

**Companion cleanup pattern (verified 2026-07-07):** When user explicitly says "xóa toàn bộ các profile khác chỉ để main profile thôi, các profile khác anh không dùng" → Option A alone is INSUFFICIENT. Anh's hard rule is single-profile, not "kill stale keep new". The right recovery is Option A + profile cleanup + plist removal:

```bash
# 1. Apply Option A above (kill stale, keep new)
# 2. Backup profiles (in case rollback needed)
mkdir -p /tmp/hermes-profiles-backup-$(date +%Y%m%d-%H%M%S)
cp -R ~/.hermes/profiles/<unused>/ /tmp/hermes-profiles-backup-.../
# 3. Verify no cron jobs reference them
hermes cron list | grep -iE "<unused>" && echo "WARNING: cron reference found"
# 4. Delete profile + plist
rm -rf ~/.hermes/profiles/<unused>
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<unused>.plist
rm ~/Library/LaunchAgents/ai.hermes.gateway-<unused>.plist
```

Result: 1 gateway PID, 1 profile, 1 plist. No race possible. ~300MB disk freed in the typical case (11 profiles).

**Session evidence:** `references/multi-gateway-same-bot-token-2026-07-07.md` (this conversation) — captured the actual PIDs, profile model diff, and the 4-option menu delivered to the user before any kill.

### Check launchd Status
```bash
launchctl list | grep hermes
```

## YOLO Mode
- Config: `approvals.mode: off` trong config.yaml
- Env: `HERMES_YOLO_MODE=true` trong .env
- Toggle: `/yolo` trong chat

### Dashboard — Remote Access via Tailscale IP

The Mac Mini's Tailscale IP is `100.117.102.115`. Binding the dashboard to this IP directly makes it accessible from every device on the tailnet — no `tailscale serve` proxy needed.

**Prerequisites — install fastapi + uvicorn into the correct venv:**
```bash
# uv pip install targets Python 3.11 by default on this system
# Must use --python flag to target the hermes-agent venv (Python 3.12)
uv pip install --python /Users/tuananh4865/.hermes/hermes-agent/.venv/bin/python fastapi uvicorn
```

**Start dashboard bound to Tailscale IP:**
```bash
cd ~/.hermes/hermes-agent && ~/.hermes/hermes-agent/.venv/bin/python -c "
import sys
sys.argv = ['h', 'dashboard', '--skip-build', '--port', '9119', '--host', '100.117.102.115', '--insecure', '--no-open']
from hermes_cli.main import main
main()
"
```

Or with hermes CLI (if fastapi/uvicorn are importable):
```bash
hermes dashboard --skip-build --host 100.117.102.115 --port 9119 --insecure --no-open
```

**Verify:**
```bash
curl http://100.117.102.115:9119/api/status
# → {"version":"0.15.0","gateway_running":true,...}
```

**Access from any Tailscale device:** Safari/browser → `http://100.117.102.115:9119`

**⚠️ Security:** `--insecure` binds to non-localhost. Safe because ONLY devices on your Tailscale tailnet can reach it. No password by default.

**Common failure: npm build errors** — `web/` has no `dist/` and node has dyld issues with libllhttp. Use `--skip-build`; the FastAPI backend serves API responses even without the React UI build.

---

### Tailscale serve — Remote Access to Dashboard

> **DEPRECATED (for this setup):** Binding directly to the Tailscale IP (above) is simpler — no proxy needed. `tailscale serve` is still useful when you MUST bind to localhost and want a Tailscale HTTPS endpoint.

```bash
# Start dashboard on localhost only
hermes dashboard --port 9119 --insecure --no-open &

# Expose via Tailscale HTTPS proxy
tailscale serve --bg http://localhost:9119

# Verify
curl https://tuananhs-mac-mini.taila86c48.ts.net/
```

**Common failure:** `https+insecure://` protocol causes 502 from Tailscale edge. Always use `http://` for plain HTTP backends.

---

## Channel Adapter Not Connected (Telegram/Discord/Slack)

When user reports "I messaged the bot but got no response" — **the bot may never have been wired up at all**. Don't chase network/DNS issues first. Walk the diagnostic tree top-down.

### Signature symptom — the 90-second diagnostic

```bash
# 1. Check if gateway even loaded any platform
grep "No messaging platforms enabled" ~/.hermes/logs/gateway.error.log
# If present → platform adapter was NEVER initialized. Stop. Fix token/config.

# 2. Check for adapter-not-connected spam in main log
grep -c "deferred.*adapter not connected" ~/.hermes/logs/gateway.log
# Rising count = adapter is alive but can't connect to platform API

# 3. Check bot token presence (most common root cause)
[ -f ~/.hermes/.env ] && grep TELEGRAM_BOT_TOKEN ~/.hermes/.env || echo "NO .env"
# Or in config.yaml:
grep -A 1 "^telegram:" ~/.hermes/config.yaml | grep token
```

### Root cause hierarchy (most → least common)

| Rank | Root cause | Diagnostic | Fix |
|------|------------|------------|-----|
| 1 | **`~/.hermes/.env` missing or no `TELEGRAM_BOT_TOKEN`** | `[ -f ~/.hermes/.env ] && grep ...` | Create `.env` with token, restart gateway |
| 2 | **Token rotated/revoked at @BotFather** | `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"` returns 401/404 | Regenerate token, update `.env`, restart |
| 3 | **Token in config but not in `.env`** | `grep token ~/.hermes/config.yaml` | Move to `.env` (chmod 600) — config should not hold secrets |
| 4 | **Network/DNS blocks `api.telegram.org`** | `curl -m 5 https://api.telegram.org` from terminal | VPN or use proxy |
| 5 | **Adapter crashes silently in `getUpdates` loop** | Look for traceback in `gateway.error.log` | Patch adapter, hard restart gateway |
| 6 | **Webhook conflicting with polling** | Telegram API returns 409 conflict | Delete webhook: `curl https://api.telegram.org/bot<TOKEN>/deleteWebhook` |

### ⚠️ Critical pitfall: "Connection failed" warnings are STALE LOGS

`gateway.log` shows historical `Telegram Connect attempt failed` warnings from past runs. **Don't be fooled** — these lines are from previous startups where the token WAS present. Check the **last modified time** of the log file:

```bash
ls -la ~/.hermes/gateway.log
# If mtime is hours/days old, those warnings are stale
```

The **authoritative signal** is `gateway.error.log`'s `No messaging platforms enabled` line, which fires on EVERY startup when no token is configured.

### ⚠️ Critical pitfall: Log says "Connection error" but service is actually fine

**The trap (2026-06-25 19:43 incident):** User reports "anh nhắn tele không được". Agent reads `gateway.log` and sees 30 lines of `APIConnectionError` from MiniMax provider. Agent concludes "API MiniMax down, that's why Telegram bot doesn't respond." Wrong. User is currently messaging the agent from this exact CLI session via the same provider — provider is working. The log lines were from background cron jobs during a transient provider hiccup, NOT from the user's message.

**Diagnostic rule — verify ground truth BEFORE blaming a layer:**
1. **Can the user send a NEW message right now and get a response?** If yes → current request path is working. The log errors are from a different code path (cron, sub-agent, historical).
2. **`ps aux | grep hermes_cli.main gateway`** — is the gateway process alive? PPID=1 = launchd-managed = OK.
3. **Run a fresh `curl -m 5` to the suspected broken endpoint** — does it respond from THIS terminal, right now?
4. **Check the log timestamp** — is the "broken" log line from 30 minutes ago, or from the last 5 seconds?
5. **Match the error to the failed message** — does the log actually contain a traceback for the user's specific chat_id / message_id, or is it from a cron request_dump file?

**Anti-pattern (DO NOT DO):**
```text
❌ "Tin nhắn của anh không được vì API MiniMax bị lỗi Connection error"
   ← This is lazy log-reading. The error is in the log, but it's not from the
     user's message. You just saw a log line and assumed causation.
```

**Right pattern:**
```text
✅ "Gateway đang chạy (PID X). Để em check log xem tin nhắn cụ thể nào bị miss
    và pattern của nó — trước khi kết luận nguyên nhân."
   ← Investigate WHICH messages are missed, WHEN they were sent, and WHETHER
     the log errors correlate with those timestamps. Don't blame a layer you
     haven't verified.
```

**Why this matters:** User pushed back hard on the wrong diagnosis ("em vẫn trả lời được đây thôi!"). Once the agent attributes the failure to the wrong layer (API provider vs. gateway vs. network), every subsequent fix targets the wrong component. The user loses trust AND the actual cause goes uninvestigated.

**Cross-reference:** Sibling pitfall to `telegram-flood-control-diagnosis` and `telegram-video-20mb-limit`. All three are "diagnose Telegram delivery failure" — but each catches a DIFFERENT layer (provider rate limit, file size, log-stare confusion). Always walk the diagnostic tree in the order above; don't jump to conclusions from log text alone.

### Distinguishing "never wired up" vs "wired up but disconnected"

| Signal | Meaning |
|--------|---------|
| `No messaging platforms enabled` in error log | Token missing → adapter never initialized |
| `Update notification deferred: X adapter not connected yet` spam (count rising every 2s) | Adapter loaded, polling failed |
| `Telegram Connect attempt 1/3 failed: Timed out` | DNS/network/firewall issue |
| `[Telegram] Connected as @botname` | Working — look elsewhere |

### Quick fix commands (after token is in `.env`)

```bash
# 1. Set token securely
echo "TELEGRAM_BOT_TOKEN=***" > ~/.hermes/.env
echo "TELEGRAM_ALLOWED_USERS=1132914873,-1003764041476" >> ~/.hermes/.env
chmod 600 ~/.hermes/.env

# 2. Verify token works (should return bot info, not 404/401)
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe" | head -c 200

# 3. Hard kill gateway (graceful restart may not reload .env)
ps aux | grep "hermes_cli.main gateway" | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 2

# 4. Restart
~/.hermes/run_hermes_gateway.sh &

# 5. Verify
sleep 8 && grep "Connected as\|No messaging platforms" ~/.hermes/logs/gateway*.log | tail -3
```

### Two log files, two purposes

- `~/.hermes/gateway.log` (main) — startup output + adapter connection attempts
- `~/.hermes/logs/gateway.error.log` — runtime warnings + non-fatal errors

**For "bot not responding" issues, check `gateway.error.log` first.** The smoking gun is almost always there, not in the main log.

### Related reference
- [[references/hook-debugging.md]] — Hook architecture + debugging + **"Disabling a Hook" 3-step recipe (added 2026-07-19)** + 🚨 pitfall "Quên cleanup SOURCE DATA hook đã ghi" (extended same day after anh flagged stale `raw/transcripts/` with 2,484 files / 3.50 MB). READ BEFORE disabling any hook OR cleaning up hook-generated data.
- **Wiki counterpart (same lesson, class-level workflow):** `wiki-maintenance` SKILL.md → "Hook-Generated Source Data Cleanup (added 2026-07-19)" section + `references/wiki-big-bang-overhaul-2026-07-19.md` Step 6 ADDED. When wiki has hook-generated data (`raw/transcripts/`, etc.) + hook disabled, run Big-Bang Overhaul Step 6 to archive source data — KHÔNG chỉ dừng ở iCloud mirror cleanup.
- [[references/log-vs-ground-truth-misdiagnosis.md]] — "Log says Connection error but service is fine" misdiagnosis (2026-06-25). Trap: jumping to conclusion from log text without verifying the user-facing path is actually broken. 5-step diagnostic rule.
- [[references/env-config-permission-regression.md]] — **CRITICAL companion ref**: `.env` regression to 644 because gateway uses `open(path, 'w')` without explicit mode → inherits process umask 022. Documents 2026-06-24 03:01:29 mtime cluster (same-second writes = single batched gateway write) + diagnosis + auto-fix sweep. **Read this BEFORE debugging any "perm 644 / perm reset" issue.**
- [[references/multi-gateway-same-bot-token-2026-07-07.md]] — Two healthy gateway processes racing for the same bot token. Different from the token-lock recipe below — race condition, not lock window. Covers full session transcript + 4-option fix menu.
- [[references/telegram-token-lock-recovery-2026-07-07.md]] — **Telegram Bot API token-lock recovery recipe** (verified 2026-07-07 7:57 ICT). Symptom: `ERROR ... Telegram bot token already in use (PID X)` after killing a gateway. Cause: Telegram holds token for ~5s cleanup after abnormal gateway death. **5-step recipe: kill → unload → sleep 5 → load → curl verify**. Includes macOS launchd plist auto-restart gotcha and 4 anti-patterns. **Read this BEFORE trying to recover from "anh nhắn tele không phản hồi" reports after a gateway crash.**

### ⚠️ Critical pitfall: Gateway umask 022 pattern (`open(path, 'w')` without mode)

**Symptom (verified 2026-06-24 + 2026-06-25):** `~/.hermes/.env`, `config.yaml`, `profiles/*/.env` show perm `644` (rw-r--r--) right after a security sweep that just fixed them to `600`. Same-second mtime cluster across multiple files = single batched write process.

**Root cause:** A running gateway process rewrites `.env` / `config.yaml` during a config-sync or env-reload operation using Python's `open(path, 'w')` without explicit mode. New files inherit the **process umask (022)** → end up at **644**.

**Code path đã được patch (2026-06-25)**: `~/.hermes/hermes-agent/hermes_cli/env_loader.py:191-201` — sử dụng `_preserve_file_mode()` + `_restore_file_mode()` từ `utils.py` sau `atomic_replace()`. `atomic_replace()` returns `real_path` (resolved symlink) để caller `os.chmod(real_path, original_mode)` đúng file behind symlink. Pattern reuse:
```python
from utils import atomic_replace, _preserve_file_mode, _restore_file_mode
original_mode = _preserve_file_mode(path)
# ... mkstemp + write ...
real_path = atomic_replace(tmp, path)
_restore_file_mode(Path(real_path), original_mode)
```
**Applies for any code path ghi `.env`/`config.yaml` qua `tempfile.mkstemp()` + `atomic_replace()`** — present ở `env_loader.py`, `config.py:6101`, `auth.py:1118/1994`. Search pattern: `grep -rln "atomic_replace.*env_path\|atomic_replace.*config_path" ~/.hermes/hermes-agent/hermes_cli/`.

**Writer process signature:**
```bash
ps aux | grep "hermes_cli.main gateway" | grep -v grep
# PID XXXXX, started YYYY-MM-DD HH:MM, still running. The --replace flag means
# it manages its own config lifecycle.
```

**Why all profiles' `.env` regressed simultaneously:** The gateway iterates `~/.hermes/profiles/*/.env` during profile-state sync. So fixing `.env` on N profiles yesterday gets undone today across all profiles at the same instant.

**Diagnostic 4-step (verified effective 2026-06-24):**
```bash
# 1. mtime cluster detection (FASTEST signal)
stat -f "%Sm %N" ~/.hermes/.env ~/.hermes/config.yaml ~/.hermes/profiles/*/.env 2>/dev/null
# All files showing same second = same writer batch (NOT human activity)

# 2. Process check — find the running gateway
ps aux | grep "hermes_cli.main gateway" | grep -v grep

# 3. Diff sweep — re-run find/xargs/stat from yesterday to identify regression
find ~/.hermes -type f \( -name ".env*" -o -name "*.db*" -o -name "auth.json" -o -name "config.yaml" \) \
  -not -path "*/wiki/*" -not -path "*/.venv/*" -not -path "*/venv/*" \
  | while read f; do
      [ "$(stat -f "%Lp" "$f")" != "600" ] && echo "REGRESSED: $f ($(stat -f "%Lp" "$f"))"
    done

# 4. Auto-fix + verify
chmod 600 <regressed files>
ls -la <regressed files>  # confirm 600
```

**Permanent fix — `PostToolUse` hook SHIPPED 2026-06-25 at `~/.hermes/hooks/env-permission-guard/`:**

**HOOK.yaml**:
```yaml
name: env-permission-guard
description: Re-apply 0o600 on protected secret/config files after Write/Edit tool use. Prevents gateway umask-inheritance regression (Jun 24 incident).
events:
  - PostToolUse
version: "1.0"
```

**handler.py** (sync `def handle(event_type, context)` — consistent với existing hooks):
```python
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))

PROTECTED_PATTERNS = [
    HERMES_HOME / ".env",
    HERMES_HOME / "config.yaml",
    HERMES_HOME / "auth.json",
]
PROTECTED_GLOB_PARTS = [
    HERMES_HOME / "profiles" / "*" / ".env",
    HERMES_HOME / "state-snapshots" / "*" / ".env",
]

def handle(event_type: str, context: dict) -> dict:
    if event_type != "PostToolUse":
        return {"action": "skip", "reason": f"event {event_type} not handled"}
    payload = context if isinstance(context, dict) else {}
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path or not _file_matches_protected(file_path):
        return {"action": "skip", "reason": "no match"}
    if not Path(file_path).exists():
        return {"action": "skip", "reason": "file does not exist"}
    os.chmod(file_path, 0o600)
    return {"action": "chmod", "path": file_path, "new_mode": "0o600"}
```

**Verify hook loaded on next gateway restart**:
```bash
grep "env-permission-guard" ~/.hermes/logs/gateway.log
# Expected: [hooks] Loaded hook 'env-permission-guard' for events: ['PostToolUse']
```

**End-to-end verification (4-step recipe, verified 2026-06-25)** — KHÔNG chỉ confirm hook loaded, phải verify hook ACTUALLY fires + side-effect works:

```bash
# Step 1: Confirm hook loaded (post-restart)
grep "env-permission-guard" ~/.hermes/logs/gateway.log

# Step 2: Manually chmod protected file to NON-protected mode (simulate regression)
chmod 644 ~/.hermes/.env
echo "Before: $(stat -f '%Lp' ~/.hermes/.env)"  # expect 644

# Step 3: Simulate PostToolUse dispatch (mimics gateway behavior)
echo '{"event_type": "PostToolUse", "tool_name": "write_file", "tool_input": {"file_path": "/Users/tuananh4865/.hermes/.env"}}' \
  | /Users/tuananh4865/.hermes/hermes-agent/venv/bin/python /Users/tuananh4865/.hermes/hooks/env-permission-guard/handler.py
# Expected stderr: [env-permission-guard] 🔒 write_file → chmod 0o600 on PATH (now 0o600)

# Step 4: Verify mode restored
echo "After: $(stat -f '%Lp' ~/.hermes/.env)"  # expect 600
```

**Negative tests** (must NOT trigger chmod):
- `{"file_path": "/tmp/random.txt"}` → `{"action": "skip", "reason": "file not protected"}`
- `{"event_type": "session:start", ...}` → `{"action": "skip", "reason": "event session:start not handled"}`

**Hook signature MUST be sync `def handle(event_type, context)`** (not `async def`) — existing hooks (`loop-engineering`, `fable5-compliance-check`) đều sync. Async hook "loads" successfully but never executes (gateway calls `.handle()` directly without `await`). Nếu test thấy hook không fire mặc dù log show "Loaded" → check signature sync vs async. **Generalization**: any new Hermes hook phải match sync convention; LSP có thể complain về `asyncio.run(handle(...))` trong `__main__` test block — fix bằng cách gọi `handle(...)` directly, không qua asyncio.

**Defense in depth**: hook + gateway code patch. Gateway code `env_loader.py:191-201` đã được patch với `_preserve_file_mode` + `_restore_file_mode` (preserves original mode qua `tempfile.mkstemp` + `atomic_replace`). Hook catches future regression paths. See `hermes-daily-backup` SKILL.md pitfall #21q (gateway code fix) + #21r (hook fix) cho full implementation log.

Until both layers ship, expect to re-apply 600 in every daily security sweep.

**Sweep output (verified 2026-06-24, 55 files auto-fixed):**
- CRITICAL (2): `~/.hermes/.env`, `~/.hermes/config.yaml`
- HIGH (53): 3 more `.env` (state-snapshot + 2 profiles), 3 `.envrc` / `.env.example` templates, 36 `kanban.db.corrupt.*.bak`, 7 `logs/*.log`, `sessions/sessions.db`

**Single-liner sweep (use in any security audit):**
```bash
find ~/.hermes -type f \( -name ".env*" -o -name "*.db*" -o -name "auth.json" -o -name "config.yaml" \) \
  -not -path "*/wiki/*" -not -path "*/.venv/*" -not -path "*/venv/*" \
  | while read f; do
      [ "$(stat -f "%Lp" "$f")" != "600" ] && chmod 600 "$f" && echo "FIXED: $f"
    done
find ~/.hermes/logs -name "*.log" -type f | while read f; do
  [ "$(stat -f "%Lp" "$f")" != "600" ] && chmod 600 "$f" && echo "FIXED: $f"
done
```

**Cross-reference:** Companion pattern to `hermes-daily-backup` PITFALL #20 (`.env` wiped from disk by cron `git reset --hard`). Both share the same shape: tool/process returns success, ground truth disagrees, no error message. Different root cause (cron git wipe vs gateway umask write) but same defensive posture: verify ground truth (mtime + perm), don't trust tool return alone.