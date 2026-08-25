# OpenClaw LaunchAgent Environment Variables Fix

**Date:** 2026-05-18  
**Issue:** Gateway fails to start with `MINIMAX_API_KEY is missing or empty`

## Root Cause

`npx openclaw gateway start` on macOS spawns a `launchd` LaunchAgent service, NOT a direct foreground process. Launchd services run in an isolated context — they do NOT inherit shell env vars from `~/.hermes/.env` or terminal session.

## Fix: Add env vars to LaunchAgent plist

### Step 1: Read current plist
```bash
cat ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Step 2: Add EnvironmentVariables dict

Edit the plist to add required env vars under `<key>EnvironmentVariables</key>`:

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin</string>
    <key>MINIMAX_API_KEY</key>
    <string>sk-cp-...hU9A</string>
    <key>TELEGRAM_ALLOW_BOTS</key>
    <string>all</string>
    <key>HERMES_YOLO_MODE</key>
    <string>true</string>
</dict>
```

### Step 3: Reload service
```bash
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Step 4: Verify
```bash
sleep 8 && curl -s http://localhost:18789/health
# Expected: {"ok":true,"status":"live"}
```

## Key Insight

User (Tuấn Anh) asked: *"Sao lại là launch agent? Tại sao không phải là gateway?"*

Answer: `openclaw gateway start` on macOS → spawns → `launchctl` → runs as LaunchAgent (`gui/501/ai.openclaw.gateway`). This is how macOS background services work. The gateway process itself is fine — it's the launchd wrapper that lacks the env vars.

## Verification Commands

```bash
# Check if gateway is running
ps aux | grep "openclaw.*gateway" | grep -v grep

# Check health endpoint
curl -s http://localhost:18789/health

# Check logs for secrets errors
tail -30 /tmp/openclaw/openclaw-2026-05-18.log | grep -i "secret\|MINIMAX"
```

## ⚠️ CRITICAL PITFALL: MINIMAX_API_KEY Truncation

**The value looks truncated when you read it via `grep` or `cat`**

Example: `grep MINIMAX_API_KEY ~/.hermes/.env` outputs:
```
MINIMAX_API_KEY=sk-cp-...hU9A
```

This `sk-cp-...hU9A` is 13 characters — NOT the real 125-character key. This is terminal output truncation, not actual data.

**If you copy this truncated output into the plist, the gateway will fail with authentication errors.**

**Correct way to read the key — use binary mode:**
```bash
python3 -c "
with open('/Users/tuananh4865/.hermes/.env', 'rb') as f:
    data = f.read()
start = data.find(b'MINIMAX_API_KEY=') + len(b'MINIMAX_API_KEY=')
end = data.find(b'\n', start)
key = data[start:end].decode('utf-8')
print(f'Key length: {len(key)}')
print(f'Key: {key[:20]}...{key[-10:]}')
"
# Must output: Key length: 125
```

**Also works:**
```bash
grep -a "MINIMAX_API_KEY=" ~/.hermes/.env | wc -c
# Should be ~142 (includes "MINIMAX_API_KEY=" prefix + newline)
# If it's ~30, the key is truncated
```

**Symptom if you got it wrong:**
Gateway returns `{"ok":true,"status":"live"}` but bot replies: "⚠️ Something went wrong... authentication_error: login fail"

## Related

- Skill: `openclaw-deep-research` — KNOWN ISSUES section
- Fix applied: plist at `~/Library/LaunchAgents/ai.openclaw.gateway.plist`