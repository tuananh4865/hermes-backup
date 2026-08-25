# Channel Adapter Diagnosis — Session Reference

**Date:** 2026-06-21
**Channel:** Telegram
**Symptom:** User reported "kiểm tra telegram bot token xem tại sao anh nhắn cho bot không được" (check the Telegram bot token, why can't I message the bot)

## Actual Root Cause

**`~/.hermes/.env` did not exist** → no `TELEGRAM_BOT_TOKEN` env var → gateway started with "No messaging platforms enabled" → Telegram adapter never initialized → bot never received any messages.

The user's assumption was a **bad bot token** (e.g., revoked or rotated). The reality was the token was **never set at all** in the gateway's runtime environment.

## Diagnostic Path (what worked, what wasted time)

### What worked — the 5-layer walk

1. **Process check** — `ps aux | grep gateway` → confirmed gateway running (PID 44698)
2. **Channel directory** — `cat ~/.hermes/channel_directory.json` → Telegram was registered (DM + groups visible)
3. **Main log** — `tail ~/.hermes/gateway.log` → found "Telegram Connect attempt failed" warnings
4. **Error log** — `tail ~/.hermes/logs/gateway.error.log` → found the **smoking gun**:
   ```
   WARNING gateway.run: No messaging platforms enabled.
   WARNING gateway.run: Update watcher: cannot resolve adapter/chat_id, falling back to completion-only
   ```
5. **Config check** — `grep TELEGRAM ~/.hermes/.env` → no `.env` file exists
6. **Config.yaml** — `telegram:` section had no `bot_token` field

### What wasted time — the dead ends

- **curl `api.telegram.org` from terminal** — returned 302 OK in 260ms. Concluded "network is fine" but this was a **red herring**: the gateway Python client fails to initialize the adapter **before** making any HTTP calls, so DNS/network are irrelevant when the token is missing.
- **Restarting the gateway** — didn't fix anything because the `.env` was still missing. Restart only helps if the underlying config is correct.
- **Reading the main `gateway.log` first** — the most recent lines were the old "Connect attempt failed" warnings, which made me think it was a network issue. The real error was in `gateway.error.log`, a separate file.

## Log Signatures Cheat Sheet

| Log line | File | Meaning | Action |
|----------|------|---------|--------|
| `No messaging platforms enabled` | `logs/gateway.error.log` | Token missing in env | Set token in `.env`, restart |
| `Update notification deferred: X adapter not connected yet` | `logs/gateway.log` (main) | Adapter running but polling failed | Check network, fallback IP, token validity |
| `Telegram Connect attempt N/3 failed: Timed out` | `logs/gateway.log` (main) | DNS/network unreachable | Test with curl, check VPN/proxy |
| `Primary api.telegram.org connection failed; trying fallback IPs` | `logs/gateway.log` (main) | Fallback path engaged | Check if fallback IP is correct Telegram range |
| `Connected as @botname` | `logs/gateway.log` (main) | Adapter healthy | Bot is working |
| `Flood control exceeded. Retry in N seconds` | `logs/gateway.error.log` | Rate-limited by Telegram | Slow down send rate |

## Key Insight: Two Log Files, Two Purposes

`gateway.log` (main, in `~/.hermes/`) is **startup output + adapter connection attempts**.
`gateway.error.log` (in `~/.hermes/logs/`) is **runtime warnings + non-fatal errors**.

**For "bot not responding" issues, always check `gateway.error.log` first.** The smoking gun is almost always there, not in the main log.

## Pitfall: "Connection failed" Warnings Are Stale

The main `gateway.log` accumulates over time. When the gateway starts fresh with no token, the adapter never even tries to connect — so you won't see new "connection failed" warnings. But you'll see **old** warnings from previous startups when the token was set.

**Diagnostic:** `ls -la ~/.hermes/gateway.log` — if the file hasn't been modified recently (hours/days), the warnings are stale.

**Better signal:** `gateway.error.log`'s `No messaging platforms enabled` is printed on **every startup** when no token is configured, so it's the authoritative indicator.

## Why Token Disappeared (likely)

User had a working bot before. Probable causes:
1. User rotated token at @BotFather (regenerate API token) but didn't update `.env`
2. `~/.hermes/.env` was deleted (cleanup, migration, fresh install)
3. Bot was migrated to a new Mac/profile and `.env` wasn't copied over
4. Token revoked because it was committed to git by accident

**The fix is always the same:** recreate `~/.hermes/.env` with the current token, chmod 600, restart gateway.

## BotFather Token Recovery Steps

1. Telegram → chat with `@BotFather`
2. `/mybots` → select the bot
3. Tap "API Token" → either copy existing or "Reset token" to generate new
4. Paste into `~/.hermes/.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   TELEGRAM_ALLOWED_USERS=1132914873,-1003764041476
   ```
5. `chmod 600 ~/.hermes/.env`
6. Hard kill + restart gateway
7. Verify: `grep "Connected as" ~/.hermes/logs/gateway.log`

## When to Hand Off to User

The agent **cannot** fetch a new token from @BotFather (requires user interaction with Telegram). When the issue is "no token in .env", the agent must:
1. Diagnose the issue completely
2. Explain the root cause clearly
3. List exact steps the user must take
4. Offer to do the rest (write `.env`, restart gateway) once user provides the token

Don't pretend to fix it without the token — that wastes a restart cycle.
