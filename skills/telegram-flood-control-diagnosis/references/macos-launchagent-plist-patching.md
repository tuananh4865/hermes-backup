---
title: macOS LaunchAgent Plist Patching — Hermes Gateway Workflow
created: 2026-06-18
type: reference
applies_to: telegram-flood-control-diagnosis
---

# macOS LaunchAgent Plist Patching — Verified Workflow (18/06)

> Companion reference to `telegram-flood-control-diagnosis` Skill. Captures the **exact macOS plist patching workflow** used to fix Telegram flood control via env var injection. Reusable for ANY Hermes gateway env var change.

## When to use this reference

Load when:
- Need to add/modify environment variables for `ai.hermes.gateway` LaunchAgent
- Patching `~/Library/LaunchAgents/ai.hermes.gateway.plist` for any reason
- Restarting Hermes gateway on macOS without breaking the parent shell

## The Hermes gateway plist (verified 18/06)

**Location:** `~/Library/LaunchAgents/ai.hermes.gateway.plist`

**Anatomy (verified by `cat`):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.hermes.gateway</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Users/tuananh4865/.hermes/hermes-agent/venv/bin/python</string>
        <string>-m</string>
        <string>hermes_cli.main</string>
        <string>gateway</string>
        <string>run</string>
        <string>--replace</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/tuananh4865/.hermes</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/tuananh4865/.hermes/hermes-agent/venv/bin:...</string>
        <key>VIRTUAL_ENV</key>
        <string>/Users/tuananh4865/.hermes/hermes-agent/venv</string>
        <key>HERMES_HOME</key>
        <string>/Users/tuananh4865/.hermes</string>
    </dict>

    <key>LimitLoadToSessionType</key>
    <array>
        <string>Aqua</string>
        <string>Background</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/tuananh4865/.hermes/logs/gateway.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/tuananh4865/.hermes/logs/gateway.error.log</string>
</dict>
</plist>
```

**Note:** Hermes has a 2nd plist at `~/Library/LaunchAgents/ai.hermes.gateway-content-director.plist` (per profile). If user runs multiple profiles, patch ALL relevant plists.

## Step-by-step plist patching workflow

### Step 1: Read existing plist
```bash
cat ~/Library/LaunchAgents/ai.hermes.gateway.plist
```
Identify where the `</dict>` of `EnvironmentVariables` block is — that's your insertion point.

### Step 2: Edit plist (use `patch` tool, NOT shell heredoc)
Why: shell heredoc với variable interpolation fails on macOS plist format (sensitive to escape chars). Use `patch` tool with old_string + new_string.

**Template for adding env vars:**
```xml
    <key>HERMES_HOME</key>
    <string>/Users/tuananh4865/.hermes</string>
    <!-- {{COMMENT}} -->
    <key>{{NEW_VAR_NAME}}</key>
    <string>{{NEW_VAR_VALUE}}</string>
</dict>
```

**Real patch 18/06:**
- old_string: `    <key>HERMES_HOME</key>\n    <string>/Users/tuananh4865/.hermes</string>\n</dict>`
- new_string: same + 3 new HERMES_TELEGRAM_* env vars before `</dict>`

### Step 3: Validate plist syntax
**MANDATORY** before launchctl load:
```bash
plutil -lint ~/Library/LaunchAgents/ai.hermes.gateway.plist
```
**Expected output:** `OK`. **Any error** → DO NOT proceed with `launchctl load` (will fail silently).

### Step 4: Restart gateway (CAREFUL — see P0)
**Pitfall P0:** Do NOT restart from inside the gateway process. SIGTERM propagates to child shell.

**Helper script** (`~/.hermes/restart-gateway-telegram-fix.sh`):
```bash
#!/bin/bash
set -e
PLIST="$HOME/Library/LaunchAgents/ai.hermes.gateway.plist"
LOG="$HOME/.hermes/logs/restart-gateway.log"
echo "[$(date)] Restarting Hermes gateway..." | tee -a "$LOG"
launchctl unload "$PLIST" 2>&1 | tee -a "$LOG"
sleep 3
launchctl load "$PLIST" 2>&1 | tee -a "$LOG"
sleep 4
NEW_PID=$(pgrep -f "hermes_cli.main gateway" | head -1)
if [ -n "$NEW_PID" ]; then
  echo "[$(date)] Gateway restarted, PID=$NEW_PID" | tee -a "$LOG"
  ps eww "$NEW_PID" 2>/dev/null | tr ' ' '\n' | grep -E "HERMES_TELEGRAM" | head -5 | tee -a "$LOG"
else
  echo "[$(date)] FAILED to start" | tee -a "$LOG"
  exit 1
fi
```

**Usage:** Run from terminal OUTSIDE the gateway process. Script does `unload → wait 3s → load → wait 4s → verify PID`.

### Step 5: Verify env vars applied
```bash
NEW_PID=$(pgrep -f "hermes_cli.main gateway" | head -1)
ps eww "$NEW_PID" | tr ' ' '\n' | grep HERMES_TELEGRAM
```

**Expected:** All 3 env vars show with new values.

## Plist patching pitfalls (real session 18/06)

### P0: Restart from inside gateway = self-kill
**Symptom:** `launchctl unload` returns, then command dies because SIGTERM propagates.
**Why:** Gateway is a parent process for the current shell (when shell was launched from gateway). Unloading the LaunchAgent kills the parent → child shell gets SIGTERM.
**Fix:** Always restart from a SEPARATE terminal. The helper script works because `bash` exits before SIGTERM arrives.

### P1: Plist syntax error = silent fail
**Symptom:** `launchctl load` returns no output, gateway never starts, no log.
**Why:** Invalid XML/structure = LaunchAgent refuses to load.
**Fix:** ALWAYS `plutil -lint` before `launchctl load`. Common mistakes:
- Forgetting `</dict>` closing tag
- Mismatched `<key>...</key>` with `<string>...</string>` (must be paired)
- Adding `</plist>` inside `EnvironmentVariables` dict
- Whitespace inconsistency (XML is forgiving but plist sometimes strict)

### P2: Env vars in shell don't persist to gateway
**Symptom:** `export HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS=1.0` in shell → restart gateway → env var not seen.
**Why:** LaunchAgent reads `EnvironmentVariables` block from plist at launch, NOT shell env. Shell env only affects the shell + children, not LaunchAgent's process.
**Fix:** Always put in plist's `EnvironmentVariables` block.

### P3: Wrong env var name (typo) = silent no-op
**Symptom:** Env var set in plist but no effect.
**Why:** Hermes code reads `HERMES_TELEGRAM_*` exact names. Typo = var exists in process env but no consumer.
**Fix:** Check `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py` for exact env var names. Common ones (verified 18/06):
- `HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS` (0.08-2.0s)
- `HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS` (1.0-4.0s)
- `HERMES_TELEGRAM_MEDIA_BATCH_DELAY_SECONDS` (no min/max specified)

### P4: LaunchAgent `KeepAlive` = auto-restart on crash
**Symptom:** After `launchctl unload` + manual `launchctl load`, gateway still shows old PID.
**Why:** `KeepAlive: true` in plist means launchd auto-restarts. If the old process didn't fully die, the new launchctl load is ignored.
**Fix:** Add `launchctl kill -SIGTERM {PID}` before `launchctl unload` to ensure clean shutdown. Or wait 5+ seconds between unload and load.

## Verification recipe (post-patch)

```bash
# 1. Plist syntax OK?
plutil -lint ~/Library/LaunchAgents/ai.hermes.gateway.plist

# 2. Env vars in plist (not in shell)
plutil -p ~/Library/LaunchAgents/ai.hermes.gateway.plist | grep HERMES_TELEGRAM

# 3. Gateway process running?
pgrep -f "hermes_cli.main gateway"

# 4. Env vars in process (after restart)
NEW_PID=$(pgrep -f "hermes_cli.main gateway" | head -1)
ps eww "$NEW_PID" | tr ' ' '\n' | grep HERMES_TELEGRAM

# 5. Test behavior (send 5 messages in 10s — should NOT flood)
# Then check gateway.log for "Flood control" events in last 10 min
```

## Related references

- `telegram-flood-control-diagnosis` SKILL.md — Main diagnosis + fix workflow
- `references/hermes-gateway-retry-config.md` — Default retry values
- Apple docs: `man launchctl`, `man plutil`
- `~/.hermes/restart-gateway-telegram-fix.sh` — Helper script (working file)
