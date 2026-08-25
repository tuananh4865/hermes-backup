---
title: Browser Harness
name: browser-harness
description: Direct browser control via CDP. Use when the user wants to automate, scrape, test, or interact with web pages. Connects to the user's already-running Chrome.
category: browser
tags: [browser, automation, CDP, web]
created: 2026-04-30
updated: 2026-07-13
source: ~/browser-harness/SKILL.md
relationships: [browser-use, browser, react-slate-editor, contenteditable-state-sync]
---

# browser-harness

Direct browser control via CDP. For task-specific edits, use `~/Developer/browser-harness/agent-workspace/agent_helpers.py` and `~/Developer/browser-harness/agent-workspace/domain-skills/`. For setup, install, or connection problems, read `browser-install`.

## ⛔ macOS COOKIE EXTRACTION — READ FIRST

**On macOS, Chrome encrypts auth cookies via the System Keychain. browser-harness CANNOT extract them** — not via CDP `Network.getCookies`, not via the headless daemon, not via `pkill Chrome + relaunch with --remote-debugging-port`. You will only get GUEST cookies (`gt`, `guest_id`, `personalization_id`). NEVER `auth_token` / `ct0` / `twid`.

**This is a hard macOS security boundary, not a browser-harness bug. No tool can bypass it.**

**If the task is "extract cookies so I can use them for auth"** — the answer is: don't. Use the platform's official API (e.g. `xurl` for X/Twitter — see `~/.hermes/skills/social-media/xurl/`). Pushing harder on browser extraction wastes the user's session and time.

**If the task is just CDP-based UI driving, screenshots, or `document.cookie` for session diagnostics** — this skill is fine. See the working `cdp()` patterns below and `references/cdp-cookie-extraction.md` for the verified Python websocket-client template.

This pitfall cost a real session in 2026-06-01 (X automation request). Read it before promising the user "I'll extract your Chrome cookies".

## ⛔ VERIFY-BEFORE-ANNOUNCE — READ FIRST (added 2026-07-11)

**`browser_navigate` returning `{success: true, url: ..., title: ...}` does NOT mean the user's local Chrome actually navigated.** Tool responses may come from a Browserbase proxy path (`"stealth_features": ["local"]` is misleading — local here means local proxy region, not user's machine).

**Case 2026-07-11:** Agent called `browser_navigate https://www.youtube.com/@VuiVe` → got `success: true` + 192 AX elements + "1.18M subscribers" channel data. Agent announced "vào kênh thành công". User pushed back: "thực sự là anh không thấy bất cứ browser nào ở youtube Vui Vẻ hiện tại cả". `computer_use` capture revealed user's actual Chrome was playing a Chinese music video "大风在刮大雪在下", signed in as Tuan Anh, with vidIQ extension — completely different from what the tool reported.

**Case 2026-07-13 (sibling failure — Chrome window hidden):** `computer_use capture app='Google Chrome'` returned `width: 0, height: 0` + only menu bar elements (no Chrome window content). Cause: Chrome window was on a different Space / minimized / covered — cua-driver can still drive elements on hidden windows but cannot capture screenshots of them. Solution: skip `computer_use` entirely, talk to Chrome directly via **CDP `curl + websocket-client`**: query `http://localhost:9222/json` for tabs, open WebSocket to `webSocketDebuggerUrl`, use `Runtime.evaluate` for DOM + `Page.navigate` for URL changes + `Input.dispatchMouseEvent` for clicks + `Input.dispatchKeyEvent` for typing. See `references/cdp-fallback-when-computer-use-returns-zero-dim.md` for full recipe + the `/usr/bin/python3` workaround (hermes_sandbox Python lacks `websocket-client`).

**⛔ Case 2026-07-13 (NEW pitfall — CDP events ≠ real user events for STATEFUL actions):** Even when CDP successfully dispatches `Input.dispatchMouseEvent` / `Input.dispatchKeyEvent` and Chrome shows the action visually, **Google/backend state may not update** because CDP events are synthetic — they don't carry the same fingerprint as a real user keystroke. Real symptom: agent clicks "Open project X" via CDP → backend returns "Đã xảy ra lỗi" (stale session); user opens same URL manually in same Chrome → project loads fine.

**Anh's verbatim feedback:** *"Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi"*

**Rule:** When the user says "open / navigate / click / login / save" on a site that tracks session state (Google, Facebook, TikTok Shop, banking, anything with OAuth tokens) — use **`computer_use` click/type on the user's real Chrome** (driving real macOS cursor), NOT CDP. CDP is fine for **READ** operations (DOM query, screenshot via Runtime.evaluate, extract URLs) and for **navigation** to public pages — but for **stateful write actions** that need a fresh session fingerprint, the only reliable path is `computer_use`.

**Decision tree:**
- READ-only / no state change (e.g. scraping public data, listing tabs) → CDP OK
- Write/state-change requiring auth (login, save, publish, buy, post) → MUST use `computer_use` on real Chrome
- `computer_use capture` returns 0×0 dim → first ask user to wake display (see Case 2026-07-13-c below), don't auto-pivot to CDP

**⛔ Case 2026-07-13-d (NEW — React Slate contenteditable: button stays disabled even with text set):** A subtle cousin of the "CDP events ≠ real user events" pitfall. When the prompt input is a `[contenteditable=true]` element using **Slate.js** (Google Flow, Notion, Linear, Figma, etc.), setting text via `ce.innerText = ...` + `dispatchEvent(new InputEvent('input', ...))` puts text in DOM but **does NOT sync Slate's internal state model** — the submit button stays visually grayed out (`bg: rgba(218, 220, 224, 0.05)`, `disabled` semantically but not in `button.disabled` attribute). User feedback: *"prompt của em có ở trong ô prompt nhưng nút gửi đi thì lại bị mờ không gửi được"*.

Methods that FAIL on Slate editors: `ce.innerText` + InputEvent, `document.execCommand('insertText')`, `cua-driver type_keystrokes` (may crash React app), Enter/Cmd+Enter hotkey. **Method that WORKS:** `cua-driver page insert_text` action — sends text via CDP `Input.insertText` (IME-style commit) which Slate's onChange listener picks up properly. After insert_text succeeds, button enables and JS `.click()` works to submit. See `references/cua-driver-page-tool-for-real-chrome.md` § "Pitfall — React Slate editor + button 'enabled' state" for full recipe + diagnostic to detect Slate editor + 5-minute polling pattern for AI generation.

**Case 2026-07-13-c (third sibling — display asleep blocks computer_use entirely):** Both Chrome windows return `Display Asleep: Yes` from `system_profiler SPDisplaysDataType` (macOS auto-sleeps after 30s of inactivity, default `displaysleep=30`). Symptoms: `screencapture` returns solid black PNG (51872 bytes — minimal PNG), `computer_use capture` returns 0×0 dim even though Chrome is alive in CDP. **No programmatic fix exists** — macOS security boundary prevents waking display from a non-interactive process. `caffeinate -di` only PREVENTS future sleep, does NOT wake already-asleep display. User must physically move mouse or press any key to wake display. After wake, `computer_use` works normally. See `references/display-asleep-blocks-computer-use.md`.

**Mandatory protocol — verify before announcing browser navigation success:**

1. **Before announcing ANY `browser_navigate` / `browser_click` success to the user**, run `computer_use(action='capture', app='Google Chrome')` to confirm the user's actual Chrome window matches what the browser tool returned.
2. If `computer_use` shows different content than the browser tool → the tool is proxying through Browserbase. STOP and tell the user: *"Em không điều khiển được Chrome anh — tool đang route qua proxy. Em chuyển sang dùng computer_use (click/type thẳng vào Chrome anh) được không?"*
3. **Workaround for local Chrome control when browser tool fails:**
   - `computer_use(action='capture', app='Google Chrome')` — see current state
   - `computer_use(action='click', element=N)` — click by SOM index
   - `computer_use(action='type', text='...')` — type into focused field
   - `computer_use(action='key', keys='Return')` — press keys
   - All actions route to user's real Chrome without proxy

4. **Never claim** "đã vào X", "đã click Y", "đã navigate đến Z" without `computer_use` screenshot evidence.

5. **Critical: don't read the AX tree blindly.** When `browser_snapshot` returns rich data (channel subscribers, comments, video info), it's tempting to assume that's the user's Chrome. ALWAYS cross-check the **window title** in `computer_use capture` output. If window title is "大风在刮大雪在下 - YouTube - Audio playing" but browser_navigate just returned Vui Vẻ channel data → MISMATCH. The window title is ground truth. AX tree content might be a stale cache, a proxy tab, or pure fabricated data.

6. **User phrases that demand verification (anh's escalation signatures):**
   - "có thấy vào đâu???" → user is asking if you actually navigated. Capture Chrome and show the URL bar contents.
   - "em chỉ mới nhập address bar thôi" → user is telling you the visible state is not what you claimed. Acknowledge the gap and re-capture.
   - "thực sự là anh không thấy..." → user sees something different. Trust the user, NOT the tool return value.

7. **Anti-pattern that caused 3 wrong claims in 1 session (2026-07-11):**
   - Claim "vào kênh thành công" after browser_navigate (no capture)
   - Claim "Chrome đã ở @VuiVe" after seeing 192 elements that were actually playlist data
   - Claim "đã navigate sang @VuiVe" after computer_use type but BEFORE computer_use capture to verify Enter was actually pressed
   - Each claim was a self-deception cascade: trusted tool return → read AX tree selectively → ignored contradictory signals (window title, user's words, BetterDisplay capture noise)

**Why this happens:** The browser tool may silently fall back to Browserbase proxy when local CDP attach fails. The success response is real (Browserbase did navigate) but it's a remote Chrome, not the user's local one. The user's Chrome stays untouched.

## 🌐 Google Flow SPECIFIC UX quirks (added 2026-07-24)

When driving Google Flow (`https://labs.google/fx/tools/flow`) project editor:

- **"Scroll xuống" means HORIZONTAL carousel, not vertical scroll.** Media grid uses `transform: matrix(...)` to shift items left; `scrollHeight == clientHeight` so `window.scrollBy` does nothing. Walk children by `getBoundingClientRect().x` to enumerate items off-screen to the right.
- **Project list NOT on homepage.** Homepage shows only "Dự án mới" button + 6 features + loading skeleton ("Đang tải..."). Older projects are accessed via Chrome tab list (`curl http://localhost:9222/json` → look for tab title "Google Flow - <ProjectName>") or direct URL `/tools/flow/project/{uuid}`.
- **Project sub-paths:** `/characters` (Nhân vật), `/tools` (Công cụ), `/edit/{scene-uuid}` (video edit mode with start/end frame controls).
- **Sidebar items may not switch main view.** Clicking "Xem hình ảnh" / "Xem video" / "Tác nhân" sidebar only highlights, doesn't always navigate. Verify with `body.innerText` snapshot before assuming the view changed.
- **Before claiming "generated N images" on Flow:** see `references/slate-editor-verify-before-claim.md` for the 4-step before/after unique ID diff recipe. Counting `img.length` is NOT proof — only diffing unique media IDs (`/trpc/media.getMediaUrlRedirect?name=<uuid>`) is.

## 3 sibling Chrome-failure cases (2026-07-11 → 2026-07-13) — which one are you in?

All three look similar (`computer_use` returns 0×0 or wrong content) but have different root causes and different fixes. Diagnose FIRST before choosing the workaround:

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| 1 | `browser_navigate` returns success + wrong content | Browserbase proxy fallback | Use `computer_use` on user's real Chrome |
| 2 | `computer_use capture app='Google Chrome'` returns 0×0 dim | Chrome window on different Space / minimized | CDP `curl + websocket-client` (see `references/cdp-fallback-when-computer-use-returns-zero-dim.md`) |
| 3 | Same as #2 PLUS `screencapture` returns solid black | Both displays asleep (`Display Asleep: Yes`) | **Ask user to wake display** (move mouse / press key) — see `references/display-asleep-blocks-computer-use.md` |

**Anh's verbatim escalation that unlocked case #1 fix:** *"có thấy vào đâu???"* — user sees different content than tool reported.

**Anh's verbatim escalation that triggered case #2/3 deeper investigation:** *"Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi"* — revealed CDP events ≠ real user events for stateful actions. **Rule:** for stateful write actions (login, save, publish, buy) on authenticated sites, use `computer_use` on real Chrome, NOT CDP. CDP is fine for READ-only (DOM query, extract data) and public navigation.

## 🚨 NEW (2026-07-13) — Better fallback when `computer_use` fails: `cua-driver call page`

If you find yourself in case #2 or #3 (computer_use can't capture, but Chrome is alive and CDP is working), `cua-driver page` tool is **BETTER than raw CDP** for stateful write actions. It runs JavaScript in user's real Chrome (same session as user) and supports click/insert_text/type_keystrokes — synthetic events have less fingerprint mismatch than raw CDP `Input.dispatchMouseEvent`.

```bash
# Run JS in user's real Chrome (works even when display is asleep — no capture needed)
echo '{"pid": 85715, "window_id": 3489, "action": "execute_javascript", "javascript": "JSON.stringify({url: location.href, title: document.title})"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page

# All 6 actions: execute_javascript | get_text | query_dom | click_element | insert_text | type_keystrokes
```

**When `cua-driver page` wins over raw CDP:**
- Real Chrome session (state changes match user-visible behavior)
- Works even when display is asleep (no capture needed — uses AX layer)
- Built-in `click_element` with CSS selector — no need to compute pixel coords
- `insert_text` and `type_keystrokes` for real IME-style text entry

**When raw CDP still wins:**
- Bulk DOM extraction (no need for full page tool plumbing)
- Network inspection (`Network.getCookies`, `Network.requestWillBeSent`)
- Page lifecycle control (`Page.navigate`, `Page.reload`, `Page.printToPDF`)

**See also:**
- `references/verify-chrome-navigation.md` — case #1 detailed
- `references/cdp-fallback-when-computer-use-returns-zero-dim.md` — case #2 detailed
- `references/display-asleep-blocks-computer-use.md` — case #3 detailed
- `references/cua-driver-page-tool-for-real-chrome.md` — cua-driver `page` tool (the CORRECT way for stateful actions)
- `references/slate-editor-verify-before-claim.md` — React Slate editor: verify before claiming "generated" (before/after unique ID diff recipe, network interception)
- `~/.hermes/skills/apple/macos-computer-use/references/display-sleep-vs-screen-lock-macos.md` — Sleep vs Lock distinction (case #3 in more detail)

## ⛔ NEW (2026-07-13) — "Image count delta" ≠ "Generation triggered from MY prompt"

A subtle anti-self-deception trap. After successfully clicking submit on a Slate editor (button enabled, `insert_text` worked, JS `.click()` fired), the agent sees `images: 41` (was 15) and reports "10 new images generated from my prompt". WRONG — the count delta could be from:
1. A queued old prompt from a previous click (cached submission)
2. Background generation triggered by app-side state change (e.g. user navigated away and back)
3. The submit used a partially-stale prompt (React state + DOM text both stale)

**The check that catches this:** after polling for change, **verify the prompt input field STILL contains YOUR prompt** (or was cleared by app after submit). If the prompt is still there with the old content, the submit may not have used it.

```python
# After click + poll for change, run this BEFORE reporting success
verify_generation_triggered(pid, wid, expected_prompt="Your full prompt here")
# Returns: {currentPrompt, matches: True/False, promptLength, isCorrect}
```

**Case 2026-07-13 (anh's verbatim correction):** *"Anh thấy em chưa gửi prompt đi mà"* — em báo "đã tạo 10 ảnh mới" sau khi thấy image count tăng, nhưng thực ra em chỉ set prompt + click Tạo 1 LẦN, không verify submit dùng prompt đúng. Anh catch được gap giữa visual state (count tăng) và actual action (submit fired with correct payload).

**Rule:** for any "I created/generated/published X" claim, the verification chain MUST be:
1. Set prompt → **verify button enabled** (bg white not gray)
2. Click submit → **verify click fired** (JS .click() returned "clicked", no error)
3. Poll for result → **verify result is from THIS prompt** (not cached/old)
4. Only THEN report "generated 10 images"

**⛔ Case 2026-07-14 (sibling — JS .click() fires event but backend ignores stale prompt payload):** A more subtle cousin of the "Image count delta" trap. Even after `cua-driver page insert_text` syncs React Slate state and button enables (bg `rgb(255, 255, 255)`), calling `btn.click()` via JS may dispatch the click event successfully (button's onClick handler fires) BUT **the backend may use a stale prompt payload** if React's internal state and DOM `innerText` diverged between insert_text and the click handler reading the value. Real symptom 2026-07-14: agent set prompt "Một quả cam tươi..." (159 chars via insert_text), verified prompt visible + button enabled, called JS `.click()`, waited 36s — `images` count stayed at 83 (unchanged from before). Intercepted `window.fetch` calls: **0 calls to `/trpc/` endpoint** during 10s post-click. The button click event dispatched but the React handler never invoked the API client.

**Anh's verbatim correction (2026-07-14, 3rd escalation in same project):** *"Em vẫn chưa tạo được bất cứ hình ảnh mới nào, làm lại"* — after em had already reported "10 new images generated" TWICE (both wrong). The 3rd time anh pushed back, em did the actual before/after verification: snapshot unique media IDs in DOM HTML → click → wait → snapshot again → diff. Result: 0 new IDs, 0 TRPC calls. Em had been seeing "26%" and "36%" progress indicators on screen, but those were from queued stale generations from anh's earlier manual clicks (or app-side estimates), NOT from em's submit.

**Verification recipe (BEFORE claiming "generated N images"):**

```python
import json, subprocess

def snapshot_media_ids(pid, wid):
    """Capture unique media IDs from DOM HTML + attribute scan."""
    js = '''(function() {
        const urls = new Set();
        document.querySelectorAll("*").forEach(el => {
            for (const attr of el.attributes) {
                if (attr.value?.includes("getMediaUrlRedirect")) {
                    const m = attr.value.match(/name=([a-f0-9-]+)/);
                    if (m) urls.add(m[1]);
                }
            }
        });
        const html = document.body.innerHTML;
        const matches = html.match(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g) || [];
        matches.forEach(id => urls.add(id));
        return JSON.stringify([...urls]);
    })()'''
    payload = {"pid": pid, "window_id": wid, "action": "execute_javascript", "javascript": js}
    result = subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
        input=json.dumps(payload), capture_output=True, text=True, timeout=15)
    return set(json.loads(result.stdout.strip()))

# 1. Snapshot BEFORE
before_ids = snapshot_media_ids(85715, 3489)
# 2. Set prompt + click + wait 15s
# (your click code here)
# 3. Snapshot AFTER
after_ids = snapshot_media_ids(85715, 3489)
new_ids = after_ids - before_ids
if not new_ids:
    print("❌ NO NEW IDs - generation did NOT trigger from MY submit")
    # Do NOT report "generated N images"
else:
    print(f"✅ {len(new_ids)} new IDs confirmed")
```

**Anti-pattern (DON'T):**
- ❌ Trust `image count delta` alone (e.g., "15 → 41 = 26 new images") without diffing unique IDs. Counts can include deleted, cached, or stale queued items.
- ❌ Trust `progress %` UI indicators (e.g., "26%", "36%"). These may be queued from previous clicks or app-side estimates, not from your submit.
- ❌ Trust JS `.click()` returned "clicked" without verifying a backend call was made. Intercept `window.fetch` to confirm `/trpc/` endpoint was hit.
- ❌ Report "đã generate" if before/after ID diff returns empty.

**Subagent lesson:** This case (2026-07-14) is sibling to 5 evidence-first-delivery fail cases (clip 0704, mascot Vui Vẻ, etc.). Same root cause: **self-verify PASS bias + skipping diff verification**. Always diff a unique identifier (file content, media ID, count of distinct elements) before reporting completion. See `references/slate-editor-verify-before-claim.md` for full recipe.

**Reusable script:** `scripts/cua_driver_page_action.py` — wraps all the above (focus → insert_text → verify button → click → poll → verify_generation_triggered). Import in any script that drives Slate-based apps (Google Flow, Notion, Linear, Figma). CLI mode for quick debugging:

```bash
python3 scripts/cua_driver_page_action.py find-window "Google Flow"
python3 scripts/cua_driver_page_action.py btn-state 85715 3489 "Tạo"  # white bg = enabled
python3 scripts/cua_driver_page_action.py insert 85715 3489 "Your prompt"
python3 scripts/cua_driver_page_action.py click-btn 85715 3489 "Tạo"
python3 scripts/cua_driver_page_action.py media-count 85715 3489  # watch for delta
```

## Quick test

```bash
browser-harness -c 'print(page_info())'
```

## ⚠️ Chrome ≥ 2026.x: 3 required flags for CDP

If you launch Chrome with `--remote-debugging-port=9222` and try to connect via WebSocket (Python `websocket-client`, Node `ws`, etc.), you will get one of two errors depending on what's missing:

**Missing `--remote-allow-origins=*`:**
```
Handshake status 403 Forbidden
'Rejected an incoming WebSocket connection from the http://localhost:9222 origin.
 Use the command line flag --remote-allow-origins=http://localhost:9222 to allow
 connections from this origin or --remote-allow-origins=* to allow all origins.'
```

**Missing non-default `--user-data-dir`:**
```
DevTools remote debugging requires a non-default data directory.
Specify this using --user-data-dir.
```

**Fix:** launch Chrome with all 3 flags (Chrome ≥ 2026.x):

```bash
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/.hermes/cache/chrome-cdp-profile"
```

**Why 3 flags:**
- `--remote-debugging-port=9222` — opens the WebSocket endpoint
- `--remote-allow-origins=*` — Chrome 2026.x blocks WebSocket from any origin unless explicitly allowed
- `--user-data-dir=<NON-DEFAULT>` — Chrome 2026.x REQUIRES a separate folder. You CANNOT use the default `~/Library/Application Support/Google/Chrome`.

**Verified (2026-07-11):** Use `~/.hermes/cache/chrome-cdp-profile` as the dedicated CDP profile dir. It is separate from the user's normal Chrome profile so Chrome sessions, cookies, and extensions don't mix.

## 🔧 Persistent CDP auto-start (LaunchAgent pattern)

**The problem:** Chrome restart (Mac reboot, crash, manual quit, macOS update) wipes the CDP flags. Every restart, you must re-launch Chrome with all 3 flags or `browser_*` tools fail with "CDP not available".

**The solution:** A LaunchAgent that runs an idempotent shell script at every Mac boot. Verified 2026-07-11, persistent across reboots.

### Step 1 — Script: `~/.hermes/scripts/launch-chrome-cdp.sh`

Idempotent (safe to run multiple times):

```bash
#!/bin/bash
# Launch Chrome with CDP flags. Idempotent.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
USER_DATA_DIR="${CHROME_USER_DATA_DIR:-/Users/tuananh4865/.hermes/cache/chrome-cdp-profile}"
mkdir -p "$USER_DATA_DIR"

# If Chrome is running without CDP → quit and relaunch
if pgrep -f "Google Chrome" > /dev/null && \
   ! lsof -nP -iTCP:${DEBUG_PORT} -sTCP:LISTEN > /dev/null 2>&1; then
  osascript -e 'quit app "Google Chrome"' > /dev/null 2>&1 || true
  sleep 2
fi

# If CDP port already listening → SKIP
if lsof -nP -iTCP:${DEBUG_PORT} -sTCP:LISTEN > /dev/null 2>&1; then
  echo "[launch-chrome-cdp] CDP ready on port ${DEBUG_PORT} → SKIP"
  exit 0
fi

# Launch Chrome with all 3 flags
nohup "$CHROME" \
  --remote-debugging-port=${DEBUG_PORT} \
  --remote-allow-origins=* \
  --user-data-dir="$USER_DATA_DIR" \
  > /tmp/chrome-cdp.log 2>&1 &

# Wait up to 8s for port to come up
for i in {1..8}; do
  sleep 1
  if lsof -nP -iTCP:${DEBUG_PORT} -sTCP:LISTEN > /dev/null 2>&1; then
    echo "[launch-chrome-cdp] ✅ Chrome CDP ready (after ${i}s)"
    exit 0
  fi
done

echo "[launch-chrome-cdp] ❌ Failed after 8s. Check /tmp/chrome-cdp.log"
exit 1
```

`chmod +x ~/.hermes/scripts/launch-chrome-cdp.sh`.

### Step 2 — LaunchAgent: `~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.tuananh.chrome-cdp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/tuananh4865/.hermes/scripts/launch-chrome-cdp.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/chrome-cdp-launchagent.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/chrome-cdp-launchagent.log</string>
    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
```

### Step 3 — Activate

```bash
launchctl load ~/Library/LaunchAgents/com.tuananh.chrome-cdp.plist
launchctl list | grep chrome-cdp  # verify PID is registered
```

### Recovery when `browser_*` fails

```bash
bash ~/.hermes/scripts/launch-chrome-cdp.sh
```

No sudo needed. The script handles both cases: Chrome not running, and Chrome running without CDP.

### Why `KeepAlive=false`?

Intentionally NOT keepalive — if Chrome crashes mid-session, the LaunchAgent will NOT auto-restart it (which would lose the user's open tabs). User manually re-runs the script if they want CDP back.

### macOS quirks

- `launchctl unload && launchctl load` is required to reload after editing the plist (LaunchAgent does NOT auto-reload on file change)
- LaunchAgent (user-level) is sufficient — no need for LaunchDaemon (system-level)
- Profile dir is separate from main Chrome profile. To sync logins/cookies from main Chrome → manually copy `~/Library/Application Support/Google/Chrome/Default/{Cookies,Login Data,Bookmarks}` into `~/.hermes/cache/chrome-cdp-profile/Default/` while Chrome is fully closed.

## Verified Python websocket-client template

```python
import urllib.request, websocket, json

tabs = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
x_tab = next(t for t in tabs if "x.com" in t.get("url", ""))
ws = websocket.create_connection(x_tab["webSocketDebuggerUrl"], suppress_origin=True)
ws.send(json.dumps({"id": 1, "method": "Network.getCookies",
                     "params": {"urls": ["https://x.com"]}}))
print(json.loads(ws.recv()))
ws.close()
```

## Usage pattern

```bash
browser-harness -c '
new_tab("https://example.com")
wait_for_load()
print(page_info())
'
```

- Invoke as `browser-harness` — it's on $PATH. No cd, no uv run.
- First navigation is `new_tab(url)`, not `goto_url(url)` — goto runs in the user's active tab and clobbers their work.

## Key principles

- **Screenshots first**: `capture_screenshot()` to understand the current page, find visible targets, decide next action.
- **Coordinate clicks**: `capture_screenshot()` → read pixel → `click_at_xy(x, y)` → screenshot to verify.
- **Bulk HTTP**: `http_get(url) + ThreadPoolExecutor`. No browser for static pages.
- **After goto**: always `wait_for_load()`.
- **Auth wall**: redirected to login → stop and ask the user. Don't type credentials.

## ⚠️ TikTok — Logged-in Chrome Works

**When the user is logged into their Chrome account, TikTok works fine with NO CAPTCHA.**

The CAPTCHA only blocks when:
- Chrome is NOT logged into TikTok
- Using an anonymous/incognito session

**What works (logged-in Chrome):**
```python
# Get profile stats
goto_url("https://www.tiktok.com/@username")
text = js("document.body.innerText")  # → "13.3M\nFollower\n156.5M\nLượt thích"

# Get all video links with view counts (sorted)
all_videos = js("""
(function() {
    const links = Array.from(document.querySelectorAll('a[href*="/video/"]'))
        .filter(a => /\\d+[MK]/.test(a.innerText?.trim() || ''))
        .map(a => {
            const viewText = a.innerText?.trim() || '0';
            let views = 0;
            if (viewText.includes('M')) views = parseFloat(viewText) * 1000000;
            else if (viewText.includes('K')) views = parseFloat(viewText) * 1000;
            return { href: a.href, views: Math.floor(views), viewText };
        });
    links.sort((a, b) => b.views - a.views);
    return links.slice(0, 15);
})()
""")

# Get video page engagement metrics
goto_url("https://www.tiktok.com/@user/video/ID")
full_text = js("document.body.innerText")  
# → "8.8M\n719K\n532.6K\n355.2K" (likes/comments/shares/saves)

# Click a video
click_at_xy(x, y)  # Use screenshot to find coordinates
```

**Key finding from session 2026-05-10:** TikTok video view counts appear INSIDE the anchor text of video links (e.g., "25.2M", "37.9M") — these are visible in `innerText` but NOT in `href` or other attributes. Use the regex `/\\d+[MK]/` to filter for videos.

**⚠️ CAPTCHA only blocks when Chrome is NOT logged in.** If you see puzzle slider → check if user's Chrome is logged in. If not logged in → stop browser approach, use web search instead.

**Full working technique (verified 2026-05-10):**
```python
# Get ALL videos from a profile sorted by views
all_videos = js("""
(function() {
    const links = Array.from(document.querySelectorAll('a[href*="/video/"]'))
        .filter(a => {
            const text = a.innerText?.trim() || '';
            return /\\d+[MK]/.test(text);
        })
        .map(a => {
            const viewText = a.innerText?.trim() || '0';
            let views = 0;
            if (viewText.includes('M')) views = parseFloat(viewText) * 1000000;
            else if (viewText.includes('K')) views = parseFloat(viewText) * 1000;
            return { href: a.href, views: Math.floor(views), viewText: viewText };
        });
    links.sort((a, b) => b.views - a.views);
    return links.slice(0, 15);
})()
""")
# Result: [{'href': 'https://www.tiktok.com/@user/video/7442647063118073106', 'views': 533500000, 'viewText': '533.5M'}, ...]
```

**Cannot do:**
- Any action requiring TikTok login verification mid-session (solve SMS/email OTP)
- Bypassing TikTok's fraud detection if triggered

### ⚠️ Chrome Keychain Cookies — macOS-Specific Limitation

Chrome on macOS stores cookies encrypted via the system Keychain. browser-harness CANNOT read these cookies even when Chrome is logged into a site.

**Symptom:** CDP `Network.getCookies` returns empty or only session cookies (guest cookies: `gt`, `guest_id`, `personalization_id`, `g_state`, `__cuid`, `__cf_bm`). NEVER returns auth cookies like `auth_token`, `ct0`, `twid`.

**Why:** macOS Keychain encryption is independent of Chrome's process — even when you `pkill Chrome` and relaunch with `--remote-debugging-port=9222 --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default"`, the new process cannot decrypt the original Keychain-protected cookies. This is a hard macOS security boundary.

**Solutions:**
1. **For X/Twitter automation:** Use `xurl` (OAuth 2.0 PKCE) — see `~/.hermes/skills/social-media/xurl/SKILL.md`. The OAuth token auto-refreshes and works around the Keychain limit. This is the only reliable path on macOS.
2. **For session-state diagnostics** (e.g. "is Chrome logged into X right now?"): use CDP `Runtime.evaluate` on `document.cookie` / `localStorage.getItem('utk')` — these work for guest-cookie checks but not for auth extraction. See `references/cdp-cookie-extraction.md` for the working Python websocket-client template.
3. **For UI driving** (clicks, screenshots, scrolling on public pages): browser-harness works fine, the Keychain limit only affects cookie-based auth.
4. **Export manually** as a last resort: user exports cookies from Chrome DevTools → you import into Playwright. Tedious, session-based, expires often.

**Note:** This is NOT a browser-harness bug — it's a fundamental macOS security boundary. No automation tool can bypass it.

**Lesson learned (2026-06-01):** When the user asks "use browser to extract cookies for auth," try the diagnostic path ONCE (CDP `getAllCookies` + `document.cookie` + `localStorage.utk` check) so you can show the guest-only result with evidence. Then immediately switch to the platform's official API. Do not loop on `pkill + relaunch + new profile dir + new debug port` combinations — they all hit the same wall.

Location: `~/Developer/browser-harness/interaction-skills/`
- cookies, cross-origin-iframes, dialogs, downloads, drag-and-drop, dropdowns
- iframes, network-requests, print-as-pdf, profile-sync, screenshots, scrolling
- shadow-dom, tabs, uploads, viewport

## Domain skills (site-specific)

Location: `~/Developer/browser-harness/agent-workspace/domain-skills/`
- tiktok/upload.md
- polymarket/scraping.md

Search first before inventing a new approach:
```bash
rg --files ~/Developer/browser-harness/agent-workspace/domain-skills
```

## Maintenance

- `browser-harness --doctor` — version, install mode, daemon + Chrome state
- `browser-harness --setup` — re-run browser attach flow
- `browser-harness --update -y` — pull latest, restart daemon (runs automatically when banner appears)

### TikTok Research Reference
For TikTok creator/content research (viral videos, stats, trends): use `mcp_exa_web_search_exa` instead of direct browser navigation. See `references/tiktok-scraping-research.md` for the workflow and known limitations.

**⚠️ TikTok CAPTCHA trap — PREVENTED THIS SESSION:**
Initial attempts failed with CAPTCHA puzzle slider because:
- Browser harness was connecting to a fresh Chrome instance (not the user's logged-in Chrome)
- The user's actual Chrome at `chrome://inspect/#remote-debugging` was already logged into TikTok

**What to do:**
1. Run `browser-harness --doctor` — check "active browser connections — 1" means you're using user's real Chrome
2. If CAPTCHA appears, verify user's Chrome is at TikTok and logged in
3. The key difference: user's real logged-in Chrome bypasses all CAPTCHA, unauthenticated Chrome gets blocked

**Verification: Is this the user's real Chrome?** Check `browser-harness --doctor` output shows "default — active page: ... TikTok ..." — if it shows TikTok already open, you're on user's session.

## Website research workflow

When the user asks to find/install something from a known domain:
1. **Try browser first** — navigate directly in Chrome. Browser DNS ≠ terminal DNS. Terminal can't resolve a host doesn't mean Chrome can't reach it.
2. **Skip terminal DNS checks** — don't `ping`, `nslookup`, or `curl` to test reachability before using the browser. The browser has its own DNS resolver and proxy settings.
3. **Search as fallback** — if direct URL fails in browser, THEN search.

**Pitfall**: You spent 20+ tool calls doing terminal DNS lookups (`ping`, `nslookup`, `curl`) before trying the browser. The browser's DNS is independent of the terminal's. Always try `browser_navigate` to the direct URL first.

## Download workflow (REMEMBER THIS)

When the user asks to "find X and install on Mac/PC":

1. **Try direct URL in browser FIRST** — browser has independent DNS from terminal. Don't waste calls on `ping`/`nslookup`/`curl`.
2. **Find download page via search** — use browser navigate to Google/Web search if direct URL fails.
3. **Extract URL via `browser_console`** — never assume button clicks trigger downloads. Inspect element.
4. **Download via `curl -L -o`** — get the URL, pipe to terminal.
5. **Mount/unmount DMG, copy to /Applications** — standard macOS install.
6. **Open app and screenshot** — `open /Applications/X.app` + `screencapture`.

**Key lesson from Antigravity install**: The user had to correct me TWICE because I over-explained problems instead of trying solutions. DNS failing in terminal means NOTHING for browser. Just open browser → navigate → inspect → download → install → screenshot. Done.

## Extracting direct download URLs

When a site hides its download URL behind redirects or button clicks (e.g. FileHorse, Softpedia, Uptonetown):

1. Navigate to the download page in the browser
2. Click the download button (may not trigger actual download, that's OK)
3. Use `browser_console` to run JavaScript and find the actual URL:
   ```javascript
   document.querySelector('a[href*=".dmg"]')?.href
   // or for any download
   document.querySelector('a[href*="download"]')?.href
   ```
4. If no luck, broaden the search:
   ```javascript
   // Find any link pointing to known hosting domains
   [...document.querySelectorAll('a[href]')].find(a => 
     a.href.includes('gvt1') || a.href.includes('googlevideo') || a.href.includes('edgedl')
   )?.href
   ```
5. Copy the URL and download directly via terminal with `curl -L -o`

**Example from this session**: FileHorse's "Start Download" button didn't trigger a download, but `browser_console` revealed the direct URL: `https://edgedl.me.gvt1.com/edgedl/release2/.../Antigravity.dmg`

## X/Twitter Video Viewing

**Videos on X/Twitter are viewable via browser even through auth walls.** See `references/x-twitter-video.md` for the full workflow.

**⚠️ PITFALL (June 2026):** Daemon can go offline between sessions — `browser-harness --doctor` shows "0 active connections" with daemon still registered. This is a distinct failure mode from CAPTCHA. Resolution: `~/.hermes/restart_gateway.sh` or `browser-harness --update -y`. Always verify daemon health BEFORE TikTok monitor runs.

## Design constraints

- Coordinate clicks default — `Input.dispatchMouseEvent` passes through iframes/shadow/cross-origin
- Connect to user's running Chrome — don't launch a separate browser
- CDP for anything helpers don't cover: `cdp("Domain.method", params)`
- Keep `agent-workspace/agent_helpers.py` for task-specific helpers

## Related

- See `references/chrome-cdp-autostart.md` for the full LaunchAgent + script setup with troubleshooting steps.