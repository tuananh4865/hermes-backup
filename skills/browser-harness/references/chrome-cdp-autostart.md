---
title: Chrome CDP Auto-Start (LaunchAgent + persistent flag)
created: 2026-07-11
updated: 2026-07-11
type: reference
parent_skill: browser-harness
tags: [chrome, cdp, devtools-protocol, browser-harness, macos, launchagent, automation, proxy-fallback]
confidence: high
---

# Chrome CDP Auto-Start — Reference

> Companion to `browser-harness` SKILL.md § "Persistent CDP auto-start (LaunchAgent pattern)". This file captures the full session transcript, the failure modes encountered, and the recovery procedure. Read this when LaunchAgent is misbehaving or when port 9222 isn't listening.

## Session context (2026-07-11)

User reported: "browser-cdp là gì sao đang bị báo là không dùng được?" (CDP not available error in browser_* tools).

After fixing CDP (LaunchAgent + script + 3 flags), agent tested with `browser_navigate https://www.youtube.com/@VuiVe` → got `success: true` + 192 AX elements + "1.18M subscribers" channel data. Agent announced success. User pushed back: "thực sự là anh không thấy bất cứ browser nào ở youtube Vui Vẻ hiện tại cả" — then "em dùng browser headless hả?".

`computer_use(action='capture', app='Google Chrome')` revealed user's actual Chrome was playing a Chinese music video "大风在刮大雪在下", signed in as Tuan Anh, with vidIQ extension — completely different content from what `browser_navigate` reported.

## ⛔ NEW PITFALL (2026-07-11) — Proxy fallback masks failure

**Symptom:** `browser_navigate` returns `{success: true, url, title, snapshot: <192 elements>, stealth_features: ["local"]}`. But user's actual Chrome window shows completely different content.

**Root cause:** The browser tool silently fell back to a Browserbase proxy path. "local" in `stealth_features` means local proxy region, NOT user's machine. The proxy did navigate successfully — to a remote Chrome instance. User's local Chrome stayed untouched.

**Why the local CDP attach failed:** Possibly because the CDP profile (`~/.hermes/cache/chrome-cdp-profile/`) is empty/separate from user's main profile. Even though port 9222 listens, the Hermes browser client may have failed to claim the page and fell back to remote proxy.

**Mandatory verification protocol — before announcing ANY browser navigation success:**

```bash
# Always run after browser_navigate or browser_click:
computer_use(action='capture', app='Google Chrome')
```

If the screenshot shows different content than the tool reported → tool is proxying, not local. STOP and tell user: *"Em không điều khiển được Chrome anh — tool đang route qua proxy. Em chuyển sang computer_use."*

## Workaround — control user's Chrome via computer_use

When browser_navigate is unreliable, fall back to computer_use:

```python
# See current Chrome state
computer_use(action='capture', app='Google Chrome')

# Click by SOM element index (numbered overlay on screenshot)
computer_use(action='click', element=N)

# Type into focused field
computer_use(action='type', text='search query')

# Press keys
computer_use(action='key', keys='Return')

# Get address bar URL
computer_use(action='capture', app='Google Chrome')  # then read AX tree for AXTextField "Address and search bar"
```

computer_use routes to user's REAL Chrome without proxy. It does NOT support `browser_console` JS evaluation or full DOM access, but for visual verification, navigation, click, type, scroll — it works on the user's actual browser.

## Diagnostic checklist (run in this order)

```bash
# 1. Is Chrome running at all?
ps aux | grep -i "chrome\|chromium" | grep -v grep | head -5

# 2. Is the CDP port listening?
lsof -nP -iTCP:9222 -sTCP:LISTEN
# OR
curl -s --max-time 3 http://localhost:9222/json/version

# 3. Are Chrome binaries installed?
which chromedriver google-chrome chromium
ls -la ~/.hermes/browser-harness/

# 4. Is LaunchAgent registered?
launchctl list | grep chrome-cdp
```

If step 2 returns nothing → Chrome is missing the CDP flag → run recovery script below.

## Recovery script

```bash
bash ~/.hermes/scripts/launch-chrome-cdp.sh
```

This script:
1. Checks if Chrome is running without CDP → quit + relaunch
2. Checks if CDP port already listening → SKIP
3. Launches Chrome with all 3 flags: `--remote-debugging-port`, `--remote-allow-origins=*`, `--user-data-dir`
4. Waits up to 8s for port to come up
5. Logs to `/tmp/chrome-cdp.log`

## Common failure modes (encountered 2026-07-11)

### 1. "DevTools remote debugging requires a non-default data directory"

**Symptom:** `/tmp/chrome-cdp.log` shows this error, port 9222 never comes up.

**Cause:** Used `--user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default"` (default Chrome profile dir). Chrome 2026.x refuses CDP on the default profile.

**Fix:** Use a dedicated, non-default profile dir:
```bash
--user-data-dir=/Users/tuananh4865/.hermes/cache/chrome-cdp-profile
```

### 2. WebSocket "403 Forbidden"

**Symptom:** Port 9222 listening, but Python `websocket-client` or Node `ws` fails to connect.

**Cause:** Missing `--remote-allow-origins=*`. Chrome 2026.x blocks WebSocket connections from any origin by default.

**Fix:** Add `--remote-allow-origins=*` to the launch flags.

### 3. LaunchAgent not running after edit

**Symptom:** Edited `~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist` but behavior didn't change.

**Cause:** LaunchAgent does NOT auto-reload on file change.

**Fix:**
```bash
launchctl unload ~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist
launchctl load ~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist
launchctl list | grep chrome-cdp  # verify
```

### 4. CDP works but user sees their main Chrome instead

**Symptom:** Chrome opened via CDP shows fresh, un-signed-in state. User's main Chrome with all their tabs/logins is elsewhere.

**Cause:** CDP runs in `~/.hermes/cache/chrome-cdp-profile/`, completely separate from the user's main Chrome profile `~/Library/Application Support/Google/Chrome/Default`.

**Fix:** Either:
- Sign in once in the CDP profile (cookies persist in CDP profile, not main Chrome)
- OR sync logins from main Chrome (while both Chromes are FULLY closed):
  ```bash
  cp ~/Library/Application\ Support/Google/Chrome/Default/{Cookies,Login\ Data,Bookmarks} \
     ~/.hermes/cache/chrome-cdp-profile/Default/
  ```

### 5. browser_navigate succeeds but user sees different content (NEW 2026-07-11)

**Symptom:** Tool returns success + rich data, but `computer_use` capture of user's Chrome shows a completely different page.

**Cause:** Tool silently fell back to Browserbase proxy. Local CDP attach failed (likely empty profile), but tool kept trying via remote Chrome and reported that as "success".

**Fix:** Always verify with `computer_use` after browser_navigate. If mismatch → switch to computer_use-only workflow.

## Files involved

| Path | Purpose |
|---|---|
| `~/.hermes/scripts/launch-chrome-cdp.sh` | Idempotent launch script (chmod +x) |
| `~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist` | LaunchAgent (RunAtLoad=true, KeepAlive=false) |
| `~/.hermes/cache/chrome-cdp-profile/` | Dedicated Chrome user-data dir (separate from main profile) |
| `/tmp/chrome-cdp.log` | Chrome stderr/stdout |
| `/tmp/chrome-cdp-launchagent.log` | LaunchAgent output |

## Why `KeepAlive=false`?

Intentionally NOT keepalive. If Chrome crashes mid-session, the LaunchAgent will NOT auto-restart it (which would lose the user's open tabs in the CDP profile). User manually re-runs `bash ~/.hermes/scripts/launch-chrome-cdp.sh` if they want CDP back.

Trade-off considered: full auto-restart would be more convenient but risks losing tab state. The user prefers manual control here.

## Verification protocol

After any Chrome restart or CDP setup change, run all 3 checks:

```bash
# 1. Port listening
lsof -nP -iTCP:9222 -sTCP:LISTEN | head -3
# Expected: "Google Chrom" line with LISTEN state on *:9222

# 2. CDP endpoint responding
curl -s http://localhost:9222/json/version | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['Browser'], '|', d['webSocketDebuggerUrl'])"
# Expected: Chrome/149.x.x.x | ws://localhost:9222/...

# 3. End-to-end Hermes tool test + computer_use verify
browser_navigate(url="https://example.com")  # expect success
computer_use(action='capture', app='Google Chrome')  # MUST show example.com
```

Step 3 is the load-bearing check. If it fails → tool is proxying, not local.

## Related

- `browser-harness/SKILL.md` § "Persistent CDP auto-start (LaunchAgent pattern)" — overview
- `browser-harness/SKILL.md` § "VERIFY-BEFORE-ANNOUNCE — READ FIRST" — mandatory verify protocol
- `~/.hermes/wiki/concepts/chrome-cdp-auto-start-2026-07-11.md` — wiki concept page