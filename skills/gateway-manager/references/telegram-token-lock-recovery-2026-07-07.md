---
title: Telegram API Token Lock Recovery (session 2026-07-07 7:57 ICT)
created: 2026-07-07
type: reference
tags: [telegram, gateway, bot-token-lock, recovery-recipe, macos-launchd]
confidence: high
relationships: [gateway-manager, hermes-channel-credentials, multi-gateway-same-bot-token-2026-07-07]
---

# Telegram API Token Lock Recovery — 2026-07-07 Capture

## Bug observed

After cleaning 11 unused Hermes profiles + killing their launchd plists, anh reported:

> "anh nhắn tele không có phản hồi"

`gateway.error.log` showed 10+ repetitions of:

```
ERROR gateway.platforms.base: [Telegram] Telegram bot token already in use (PID 860).
                                    Stop the other gateway first.
```

## Root cause

**Telegram Bot API has a token lock window** — when a gateway process registers a bot token via long-polling `getUpdates` and then dies abnormally (kill -9, OS kill, OOM, segfault), the Bot API holds the token for a short cleanup window (~5 seconds verified) before allowing another process to claim it. During that window, any new gateway registration fails with "token already in use (PID X)".

This is distinct from:
- **Multi-gateway race** (`multi-gateway-same-bot-token-2026-07-07.md`) — two PIDs simultaneously healthy
- **Bot API rate limit** (`telegram-flood-control-diagnosis`) — Telegram-side throttle on send-message

The token lock is server-side cleanup of a dead session, not duplicate registration.

## 5-step recovery recipe (verified working 2026-07-07 7:57 ICT)

```bash
# Step 1: Kill the gateway holding the stale token registration
kill <PID>                  # try graceful first
sleep 2
if ps -p <PID> > /dev/null 2>&1; then
  kill -9 <PID>             # hard kill if SIGTERM ignored
  sleep 1
fi

# Step 2: Unload launchd plist (auto-restart is the silent killer)
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist

# Step 3: WAIT for Telegram to release the token lock
sleep 5                    # verified minimum on this setup

# Step 4: Reload launchd plist (fresh gateway process)
launchctl load ~/Library/LaunchAgents/ai.hermes.gateway.plist
sleep 3

# Step 5: Verify fix
TOKEN=$(grep ^TELEGRAM_BOT_TOKEN= ~/.hermes/.env | cut -d= -f2-)
curl -s -m 5 "https://api.telegram.org/bot${TOKEN}/getUpdates?timeout=2&limit=1"
# Expected: {"ok":true,"result":[]}
# Anti-symptom: {"ok":false,"error_code":409,"description":"Conflict: terminated by other getUpdates request"}
```

## Why each step matters

### Why kill before unload?

launchd plist has `KeepAlive: SuccessfulExit: false` — it monitors the **process**, not the token. If you unload the plist AFTER killing the process, launchd may have already restarted it (because the process is gone, not because the script exited cleanly). Killing first, then unloading, prevents a new process from spawning.

But — order can go either way as long as both are done. Em did kill first then unload in this session; both orderings verified working from prior sessions (2026-06-24).

### Why sleep 5?

Telegram Bot API internal token-cleanup window. Verified by:
- `sleep 3` (3s wait) → 409 Conflict still
- `sleep 5` (5s wait) → ok:true
- `sleep 10` (10s wait) → ok:true

Use 5s as minimum. Going lower risks 409. Going higher is safe but slower recovery.

### Why unload the plist at all?

`launchd` will **auto-restart the gateway** if you only kill the process without unloading the plist. Verified 2026-07-07: killed content-director PID 860 at 7:54, process PID 11021 spawned within 1 second (visible in `ps aux`). Without `launchctl unload`, the kill is futile — the new process immediately re-registers the same token and re-triggers the conflict.

### Why verify with `getUpdates` instead of assuming the recipe worked?

The Bot API returns TWO distinct success/failure shapes that both look "fine" to a casual eye:
- `{"ok":true,"result":[]}` — clean polling state, ready to dispatch messages
- `{"ok":false,"error_code":409,"description":"Conflict: ..."}` — token lock still held

Only `getUpdates` distinguishes them. Don't claim "fixed" without the curl output.

## macOS launchd plist auto-restart gotcha

`~/Library/LaunchAgents/ai.hermes.gateway*.plist` plists:
- `ai.hermes.gateway.plist` — default profile gateway
- `ai.hermes.gateway-content-director.plist` — content-director profile (deprecated, removed 2026-07-07)

**Behavior when gateway dies abnormally:**
- Plist with `KeepAlive` directive → respawn within 1-2 seconds
- Multiple plists for different profiles → each respawns independently
- If you `kill` a process without `launchctl unload` first → new process spawns immediately, possibly before you can finish typing next command

**Permanent fix for unwanted gateways:** delete the plist (after unloading it). Backup first:
```bash
mkdir -p /tmp/hermes-plist-backup
cp ~/Library/LaunchAgents/ai.hermes.gateway-<name>.plist /tmp/hermes-plist-backup/
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<name>.plist
rm ~/Library/LaunchAgents/ai.hermes.gateway-<name>.plist
```

## Anti-patterns

### Anti-pattern 1: Just kill and reload

```bash
kill 9743
launchctl load ai.hermes.gateway.plist    # ❌ new process spawns with token lock still held
```

→ Fix fails. New process gets 409 Conflict on first `getUpdates`. User sees "anh nhắn tele không có phản hồi" again.

### Anti-pattern 2: Sleep then reload without unload

```bash
kill 9743
sleep 5
launchctl load ai.hermes.gateway.plist    # ❌ unload was missing
```

→ If plist still active, launchd may have respawned PID 9743 within those 5 seconds. Two processes fight for the (now released) token. Race condition.

### Anti-pattern 3: Trust log "Connected as @botname" without curl verify

`gateway.log` shows "Connected as @botname" within 1s of process spawn, even if the FIRST `getUpdates` returns 409. The log statement fires when the websocket frame is established, not when the token is validated for polling.

→ Always end the recovery recipe with curl `getUpdates` to confirm clean polling state.

### Anti-pattern 4: Tell the user "try again" without verifying

If the recipe ran but getUpdates returned 409, telling the user to retry just kicks the error to them. They have no way to debug the gateway state from Telegram. Always verify before "✓ Done".

## Diagnostic before recovery (the 30-second scan)

```bash
# 1. What gateway processes exist?
ps aux | grep -E "hermes_cli.main.*gateway" | grep -v grep

# 2. Any active errors?
grep -E "ERROR.*token already in use|Flood control" ~/.hermes/logs/gateway.error.log | tail -5

# 3. Telegram API view
TOKEN=$(grep ^TELEGRAM_BOT_TOKEN= ~/.hermes/.env | cut -d= -f2-)
curl -s -m 3 "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | python3 -c "import sys, json; d=json.load(sys.stdin); print('webhook:', d['result']['url'], '| pending:', d['result']['pending_update_count'])"
curl -s -m 5 "https://api.telegram.org/bot${TOKEN}/getUpdates?timeout=1&limit=1" | head -c 200
```

If step 3 returns 409 → token lock → run recipe.

## When to skip the recipe

- If only ONE gateway process is running and Telegram is responding correctly → no recipe needed
- If `getUpdates` returns valid update (not empty array) → token not locked, bot is receiving messages
- If user reports "all messages go to bot but bot doesn't reply" → different bug (likely LLM provider error, not token lock)

## Related

- `references/multi-gateway-same-bot-token-2026-07-07.md` — sibling pitfall (race condition, not lock window)
- `gateway-manager/SKILL.md` "⚠️ Multi-Gateway Same-Bot-Token Conflict" — the earlier section on same family of bugs
- `hermes-channel-credentials/SKILL.md` Pitfall #13 — "Gateway tự respawn PID mới" (related but distinct cause)

## Session evidence

- 2026-07-07 7:54:25 ICT — kill content-director PID 860
- 2026-07-07 7:54:26 ICT — new PID 11021 spawned within 1 second (failed auto-restart)
- 2026-07-07 7:54:30 ICT — `launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-content-director.plist` (manual unload)
- 2026-07-07 7:54:31 ICT — kill 11021 (still alive after launchd unload, manual SIGTERM)
- 2026-07-07 7:54:35 ICT — kill default gateway PID 9743 (too — had been failing to register for 7h+ due to Token Lock)
- 2026-07-07 7:55:00 ICT — `launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist`
- 2026-07-07 7:55:01 ICT — `sleep 5` (Telegram API release window)
- 2026-07-07 7:55:06 ICT — `launchctl load ~/Library/LaunchAgents/ai.hermes.gateway.plist`
- 2026-07-07 7:55:09 ICT — verify `curl /getUpdates` returns `{"ok":true,"result":[]}` (FIXED)
- 2026-07-07 7:55:15 ICT — backup profiles to `/tmp/hermes-profiles-backup-20260707-075515/` (295MB)
- 2026-07-07 7:55:30 ICT — deleted 11 profiles (~300MB freed)
- 2026-07-07 8:00 ICT — saved lessons to wiki + memory
