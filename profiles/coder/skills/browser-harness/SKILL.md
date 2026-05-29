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

## Quick test

```bash
browser-harness -c 'print(page_info())'
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

**Symptom:** CDP `Network.getCookies` returns empty or only session cookies, but the browser shows you logged in.

**Why:** macOS Keychain encryption is independent of Chrome's process — browser-harness CDP runs in a separate headless Chrome instance that doesn't have access to the user's Keychain.

**Solutions:**
1. **Use xurl API** — for X/Twitter posts, use `xurl` which handles auth differently
2. **Use computer_use** — the user's actual Chrome instance can be controlled via `computer_use` which operates at the macOS window level
3. **Export manually** — user exports cookies from Chrome DevTools → you import into Playwright

**Note:** This is NOT a browser-harness bug — it's a fundamental macOS security boundary. No automation tool can bypass this.

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

## Design constraints

- Coordinate clicks default — `Input.dispatchMouseEvent` passes through iframes/shadow/cross-origin
- Connect to user's running Chrome — don't launch a separate browser
- CDP for anything helpers don't cover: `cdp("Domain.method", params)`
- Keep `agent-workspace/agent_helpers.py` for task-specific helpers
