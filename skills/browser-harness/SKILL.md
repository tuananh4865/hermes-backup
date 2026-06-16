---
title: Browser Harness
name: browser-harness
description: Direct browser control via CDP. Use when the user wants to automate, scrape, test, or interact with web pages. Connects to the user's already-running Chrome.
category: browser
tags: [browser, automation, CDP, web]
created: 2026-04-30
updated: 2026-04-30
source: ~/Developer/browser-harness/SKILL.md
relationships: [browser-use, browser]
---

# browser-harness

Direct browser control via CDP. For task-specific edits, use `~/Developer/browser-harness/agent-workspace/agent_helpers.py` and `~/Developer/browser-harness/agent-workspace/domain-skills/`. For setup, install, or connection problems, read `browser-install`.

## ⛔ macOS COOKIE EXTRACTION — READ FIRST

**On macOS, Chrome encrypts auth cookies via the System Keychain. browser-harness CANNOT extract them** — not via CDP `Network.getCookies`, not via the headless daemon, not via `pkill Chrome + relaunch with --remote-debugging-port`. You will only get GUEST cookies (`gt`, `guest_id`, `personalization_id`). NEVER `auth_token` / `ct0` / `twid`.

**This is a hard macOS security boundary, not a browser-harness bug. No tool can bypass it.**

**If the task is "extract cookies so I can use them for auth"** — the answer is: don't. Use the platform's official API (e.g. `xurl` for X/Twitter — see `~/.hermes/skills/social-media/xurl/`). Pushing harder on browser extraction wastes the user's session and time.

**If the task is just CDP-based UI driving, screenshots, or `document.cookie` for session diagnostics** — this skill is fine. See the working `cdp()` patterns below and `references/cdp-cookie-extraction.md` for the verified Python websocket-client template.

This pitfall cost a real session in 2026-06-01 (X automation request). Read it before promising the user "I'll extract your Chrome cookies."

## Quick test

```bash
browser-harness -c 'print(page_info())'
```

**⚠️ Chrome ≥ 2026.x: `--remote-allow-origins=*` required for WebSocket clients**

If you launch Chrome with `--remote-debugging-port=9222` and try to connect via WebSocket (Python `websocket-client`, Node `ws`, etc.), you will get:

```
Handshake status 403 Forbidden
'Re jected an incoming WebSocket connection from the http://localhost:9222 origin.
 Use the command line flag --remote-allow-origins=http://localhost:9222 to allow
 connections from this origin or --remote-allow-origins=* to allow all origins.'
```

**Fix:** launch Chrome with both flags:

```bash
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default"
```

This is a 2026 Chrome security change — not a bug in browser-harness or your client. `browser-harness --doctor` may still report "ok" because it uses HTTP /json, not WebSocket.

**Verified pattern (2026-06-16):** Use `http://localhost:9222/json` to get tab list, then connect via WebSocket with `suppress_origin=True`:

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

When a site hides its download URL behind redirects or button clicks (e.g. FileHorse, Softpedia, Uptodown):

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
