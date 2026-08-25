---
name: xurl
description: "X/Twitter via xurl CLI: post, search, DM, media, v2 API."
version: 1.1.1
author: xdevplatform + openclaw + Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [xurl]
metadata:
  hermes:
    tags: [twitter, x, social-media, xurl, official-api]
    homepage: https://github.com/xdevplatform/xurl
    upstream_skill: https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
---

# xurl — X (Twitter) API via the Official CLI

`xurl` is the X developer platform's official CLI for the X API. It supports shortcut commands for common actions AND raw curl-style access to any v2 endpoint. All commands return JSON to stdout.

Use this skill for:
- posting, replying, quoting, deleting posts
- searching posts and reading timelines/mentions
- liking, reposting, bookmarking
- following, unfollowing, blocking, muting
- direct messages
- media uploads (images and video)
- raw access to any X API v2 endpoint
- multi-app / multi-account workflows

This skill replaces the older `xitter` skill (which wrapped a third-party Python CLI). `xurl` is maintained by the X developer platform team, supports OAuth 2.0 PKCE with auto-refresh, and covers a substantially larger API surface.

---

## Secret Safety (MANDATORY)

Critical rules when operating inside an agent/LLM session:

- **Never** read, print, parse, summarize, upload, or send `~/.xurl` to LLM context.
- **Never** ask the user to paste credentials/tokens into chat.
- The user must fill `~/.xurl` with secrets manually on their own machine.
- **Never** recommend or execute auth commands with inline secrets in agent sessions.
- **Never** use `--verbose` / `-v` in agent sessions — it can expose auth headers/tokens.
- To verify credentials exist, only use: `xurl auth status`.

Forbidden flags in agent commands (they accept inline secrets):
`--bearer-token`, `--consumer-key`, `--consumer-secret`, `--access-token`, `--token-secret`, `--client-id`, `--client-secret`

App credential registration and credential rotation must be done by the user manually, outside the agent session. After credentials are registered, the user authenticates with `xurl auth oauth2` — also outside the agent session. Tokens persist to `~/.xurl` in YAML. Each app has isolated tokens. OAuth 2.0 tokens auto-refresh.

---

## Installation

Pick ONE method. On Linux, the shell script or `go install` are the easiest.

```bash
# Shell script (installs to ~/.local/bin, no sudo, works on Linux + macOS)
curl -fsSL https://raw.githubusercontent.com/xdevplatform/xurl/main/install.sh | bash

# Homebrew (macOS)
brew install --cask xdevplatform/tap/xurl

# npm
npm install -g @xdevplatform/xurl

# Go
go install github.com/xdevplatform/xurl@latest
```

Verify:

```bash
xurl --help
xurl auth status
```

If `xurl` is installed but `auth status` shows no apps or tokens, the user needs to complete auth manually — see the next section.

---

## One-Time User Setup (user runs these outside the agent)

These steps must be performed by the user directly, NOT by the agent, because they involve pasting secrets. Direct the user to this block; do not execute it for them.

1. Create or open an app at https://developer.x.com/en/portal/dashboard
2. Set the redirect URI to `http://localhost:8080/callback`
3. Copy the app's Client ID and Client Secret
4. Register the app locally (user runs this):
   ```bash
   xurl auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
   ```
5. Authenticate (specify `--app` to bind the token to your app):
   ```bash
   xurl auth oauth2 --app my-app
   ```
   (This opens a browser for the OAuth 2.0 PKCE flow.)

   If X returns a `UsernameNotFound` error or 403 on the post-OAuth `/2/users/me` lookup, pass your handle explicitly (xurl v1.1.0+):
   ```bash
   xurl auth oauth2 --app my-app YOUR_USERNAME
   ```
   This binds the token to your handle and skips the broken `/2/users/me` call.
6. Set the app as default so all commands use it:
   ```bash
   xurl auth default my-app
   ```
7. Verify:
   ```bash
   xurl auth status
   xurl whoami
   ```

After this, the agent can use any command below without further setup. OAuth 2.0 tokens auto-refresh.

> **Common pitfall:** If you omit `--app my-app` from `xurl auth oauth2`, the OAuth token is saved to the built-in `default` app profile — which has no client-id or client-secret. Commands will fail with auth errors even though the OAuth flow appeared to succeed. If you hit this, re-run `xurl auth oauth2 --app my-app` and `xurl auth default my-app`.

---

## Quick Reference

| Action | Command |
| --- | --- |
| Post | `xurl post "Hello world!"` |
| Reply | `xurl reply POST_ID "Nice post!"` |
| Quote | `xurl quote POST_ID "My take"` |
| Delete a post | `xurl delete POST_ID` |
| Read a post | `xurl read POST_ID` |
| Search posts | `xurl search "QUERY" -n 10` |
| Who am I | `xurl whoami` |
| Look up a user | `xurl user @handle` |
| Home timeline | `xurl timeline -n 20` |
| Mentions | `xurl mentions -n 10` |
| Like / Unlike | `xurl like POST_ID` / `xurl unlike POST_ID` |
| Repost / Undo | `xurl repost POST_ID` / `xurl unrepost POST_ID` |
| Bookmark / Remove | `xurl bookmark POST_ID` / `xurl unbookmark POST_ID` |
| List bookmarks / likes | `xurl bookmarks -n 10` / `xurl likes -n 10` |
| Follow / Unfollow | `xurl follow @handle` / `xurl unfollow @handle` |
| Following / Followers | `xurl following -n 20` / `xurl followers -n 20` |
| Block / Unblock | `xurl block @handle` / `xurl unblock @handle` |
| Mute / Unmute | `xurl mute @handle` / `xurl unmute @handle` |
| Send DM | `xurl dm @handle "message"` |
| List DMs | `xurl dms -n 10` |
| Upload media | `xurl media upload path/to/file.mp4` |
| Media status | `xurl media status MEDIA_ID` |
| List apps | `xurl auth apps list` |
| Remove app | `xurl auth apps remove NAME` |
| Set default app | `xurl auth default APP_NAME [USERNAME]` |
| Per-request app | `xurl --app NAME /2/users/me` |
| Auth status | `xurl auth status` |

Notes:
- `POST_ID` accepts full URLs too (e.g. `https://x.com/user/status/1234567890`) — xurl extracts the ID.
- Usernames work with or without a leading `@`.

---

## Command Details

### Posting

```bash
xurl post "Hello world!"
xurl post "Check this out" --media-id MEDIA_ID
xurl post "Thread pics" --media-id 111 --media-id 222

xurl reply 1234567890 "Great point!"
xurl reply https://x.com/user/status/1234567890 "Agreed!"
xurl reply 1234567890 "Look at this" --media-id MEDIA_ID

xurl quote 1234567890 "Adding my thoughts"
xurl delete 1234567890
```

### Reading & Search

```bash
xurl read 1234567890
xurl read https://x.com/user/status/1234567890

xurl search "golang"
xurl search "from:elonmusk" -n 20
xurl search "#buildinpublic lang:en" -n 15
```

### Users, Timeline, Mentions

```bash
xurl whoami
xurl user elonmusk
xurl user @XDevelopers

xurl timeline -n 25
xurl mentions -n 20
```

### Engagement

```bash
xurl like 1234567890
xurl unlike 1234567890

xurl repost 1234567890
xurl unrepost 1234567890

xurl bookmark 1234567890
xurl unbookmark 1234567890

xurl bookmarks -n 20
xurl likes -n 20
```

### Social Graph

```bash
xurl follow @XDevelopers
xurl unfollow @XDevelopers

xurl following -n 50
xurl followers -n 50

# Another user's graph
xurl following --of elonmusk -n 20
xurl followers --of elonmusk -n 20

xurl block @spammer
xurl unblock @spammer
xurl mute @annoying
xurl unmute @annoying
```

### Direct Messages

```bash
xurl dm @someuser "Hey, saw your post!"
xurl dms -n 25
```

### Media Upload

```bash
# Auto-detect type
xurl media upload photo.jpg
xurl media upload video.mp4

# Explicit type/category
xurl media upload --media-type image/jpeg --category tweet_image photo.jpg

# Videos need server-side processing — check status (or poll)
xurl media status MEDIA_ID
xurl media status --wait MEDIA_ID

# Full workflow
xurl media upload meme.png                  # returns media id
xurl post "lol" --media-id MEDIA_ID
```

---

## Raw API Access

The shortcuts cover common operations. For anything else, use raw curl-style mode against any X API v2 endpoint:

```bash
# GET
xurl /2/users/me

# POST with JSON body
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'

# DELETE / PUT / PATCH
xurl -X DELETE /2/tweets/1234567890

# Custom headers
xurl -H "Content-Type: application/json" /2/some/endpoint

# Force streaming
xurl -s /2/tweets/search/stream

# Full URLs also work
xurl https://api.x.com/2/users/me
```

---

## Global Flags

| Flag | Short | Description |
| --- | --- | --- |
| `--app` | | Use a specific registered app (overrides default) |
| `--auth` | | Force auth type: `oauth1`, `oauth2`, or `app` |
| `--username` | `-u` | Which OAuth2 account to use (if multiple exist) |
| `--verbose` | `-v` | **Forbidden in agent sessions** — leaks auth headers |
| `--trace` | `-t` | Add `X-B3-Flags: 1` trace header |

---

## Streaming

Streaming endpoints are auto-detected. Known ones include:

- `/2/tweets/search/stream`
- `/2/tweets/sample/stream`
- `/2/tweets/sample10/stream`

Force streaming on any endpoint with `-s`.

---

## Output Format

All commands return JSON to stdout. Structure mirrors X API v2:

```json
{ "data": { "id": "1234567890", "text": "Hello world!" } }
```

Errors are also JSON:

```json
{ "errors": [ { "message": "Not authorized", "code": 403 } ] }
```

---

## Common Workflows

### Post with an image
```bash
xurl media upload photo.jpg
xurl post "Check out this photo!" --media-id MEDIA_ID
```

### Reply to a conversation
```bash
xurl read https://x.com/user/status/1234567890
xurl reply 1234567890 "Here are my thoughts..."
```

### Search and engage
```bash
xurl search "topic of interest" -n 10
xurl like POST_ID_FROM_RESULTS
xurl reply POST_ID_FROM_RESULTS "Great point!"
```

### Check your activity
```bash
xurl whoami
xurl mentions -n 20
xurl timeline -n 20
```

### Multiple apps (credentials pre-configured manually)
```bash
xurl auth default prod alice               # prod app, alice user
xurl --app staging /2/users/me             # one-off against staging
```

---

## Error Handling

- Non-zero exit code on any error.
- API errors are still printed as JSON to stdout, so you can parse them.
- Auth errors → have the user re-run `xurl auth oauth2` outside the agent session.
- Commands that need the caller's user ID (like, repost, bookmark, follow, etc.) will auto-fetch it via `/2/users/me`. An auth failure there surfaces as an auth error.

---

## Agent Workflow

1. Verify prerequisites: `xurl --help` and `xurl auth status`.
   - Note: `xurl` installs to `~/.local/bin/` — ensure this is in PATH: `export PATH="$HOME/.local/bin:$PATH"`
2. **Check default app has credentials.** Parse the `auth status` output. The default app is marked with `▸`. If the default app shows `oauth2: (none)` but another app has a valid oauth2 user, tell the user to run `xurl auth default <that-app>` to fix it. This is the most common setup mistake — the user added an app with a custom name but never set it as default, so xurl keeps trying the empty `default` profile.
3. If auth is missing entirely AND the user said "post/repost it" or gave a clear go-ahead → **go straight to browser fallback** (see `references/browser-workflow.md`). Do NOT stop to ask the user which approach they want. Own the task by using the browser method automatically.
4. If auth is missing and no clear go-ahead was given → stop and direct the user to the "One-Time User Setup" section.
5. Start with a cheap read (`xurl whoami`, `xurl user @handle`, `xurl search ... -n 3`) to confirm reachability.
6. Confirm the target post/user and the user's intent before any write action (post, reply, like, repost, DM, follow, block, delete).
7. Use JSON output directly — every response is already structured.
8. Never paste `~/.xurl` contents back into the conversation.

### Video file discovery
When looking for recently-generated video files (e.g., Remotion renders), check `/tmp/` first — Remotion and similar tools write output there by default. Look for `*.mp4` files with recent modification timestamps.

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Auth errors after successful OAuth flow | Token saved to `default` app (no client-id/secret) instead of your named app | `xurl auth oauth2 --app my-app` then `xurl auth default my-app` |
| `unauthorized_client` during OAuth | App type set to "Native App" in X dashboard | Change to "Web app, automated app or bot" in User Authentication Settings |
| `UsernameNotFound` or 403 on `/2/users/me` right after OAuth | X not returning username reliably from `/2/users/me` | Re-run `xurl auth oauth2 --app my-app YOUR_USERNAME` (xurl v1.1.0+) to pass the handle explicitly |
| 401 on every request | Token expired or wrong default app | Check `xurl auth status` — verify `▸` points to an app with oauth2 tokens |
| `client-forbidden` / `client-not-enrolled` | X platform enrollment issue | Dashboard → Apps → Manage → Move to "Pay-per-use" package → Production environment |
| `CreditsDepleted` | $0 balance on X API | Buy credits (min $5) in Developer Console → Billing |
| `media processing failed` on image upload | Default category is `amplify_video` | Add `--category tweet_image --media-type image/png` |
| Two "Client Secret" values in X dashboard | UI bug — first is actually Client ID | Confirm on the "Keys and tokens" page; ID ends in `MTpjaQ` |

| `media processing failed` on image upload | Default category is `amplify_video` | Add `--category tweet_image --media-type image/png` |

## Browser Fallback Pitfalls (2026-05-21, updated 2026-06-01)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `xurl auth status` shows credentials but post fails | Credentials may be expired or misconfigured | Use `browser-harness` to visually verify session state — screenshot first |
| Cookie auth works in browser-harness but fails in Playwright | Separate browser instances have separate sessions | Use browser-harness's own automation helpers instead of separate Playwright |
| User asks "chụp hình xem" (take screenshot) | Wants visual confirmation, not text explanation | Screenshot → send via `MEDIA:/path.png` → short text summary. Never long paragraphs. |
| `browser-harness cdp Network.getCookies` returns empty on macOS | macOS Keychain encrypts Chrome cookies | Switch to xurl OAuth — see `references/browser-workflow.md` |
| `pkill Chrome + open with --remote-debugging-port=9222 + same profile` returns GUEST cookies | macOS Keychain blocks new Chrome process from reading own auth cookies | This is a hard macOS security boundary — xurl OAuth is the only path |
| CDP WebSocket handshake 403 with "Rejected an incoming WebSocket connection" | Chrome requires `--remote-allow-origins=*` flag in newer versions | Add `--remote-allow-origins=*` to Chrome launch args |

### CDP Cookie Extraction — What ACTUALLY Works (2026-06-01)

Verified in production session: even when Chrome is logged in, CDP only returns
**guest cookies** (`gt`, `guest_id`, `personalization_id`, `g_state`). NEVER returns
`auth_token`, `ct0`, `twid` — those are Keychain-protected.

**Working CDP discovery pattern (for verifying session state, NOT for auth):**

```python
# Python websocket-client — connect to existing Chrome's debug port
import websocket, json
ws = websocket.create_connection(ws_url, suppress_origin=True)

# Get all cookies (returns guest cookies only on macOS)
ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies"}))
cookies = json.loads(ws.recv())["result"]["cookies"]
auth_token_present = any(c["name"] == "auth_token" for c in cookies)
# → False on macOS even when Chrome is logged in

# Check via document.cookie
ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {"expression": "document.cookie.includes('auth_token')"}
}))
auth_in_doc = json.loads(ws.recv())["result"]["result"]["value"]
# → False on macOS

# Check localStorage for utk (X's user token key)
ws.send(json.dumps({
    "id": 3,
    "method": "Runtime.evaluate",
    "params": {"expression": "localStorage.getItem('utk')"}
}))
utk = json.loads(ws.recv())["result"]["result"]["value"]
# → None on macOS

ws.close()
```

**If `auth_token` is missing from all three → switch to xurl OAuth immediately.**
Do not waste time trying alternative cookie paths.

### Chrome Launch with Debug Port (working command)

```bash
# Quit existing Chrome
osascript -e 'tell application "Google Chrome" to quit'
sleep 2

# Launch with debug port + remote-allow-origins (REQUIRED for newer Chrome)
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default"

sleep 4

# Verify
curl -s http://localhost:9222/json | python3 -c "import sys, json; print(len(json.load(sys.stdin)), 'tabs')"
# → N tabs

# Get list of tabs (for ws_url extraction)
curl -s http://localhost:9222/json
```

See `references/cdp-cookie-extraction.md` for full working code template.

### Use `computer_use` for UI driving, NOT for auth

`computer_use` can drive Chrome's UI (clicks, typing, screenshots) but cannot
read Keychain-protected cookies. **Only use for tasks that don't require
authentication** (e.g. viewing public tweets, capturing screenshots).

## Notes

- **Rate limits:** X enforces per-endpoint rate limits. A 429 means wait and retry. Write endpoints (post, reply, like, repost) have tighter limits than reads.
- **Scopes:** OAuth 2.0 tokens use broad scopes. A 403 on a specific action usually means the token is missing a scope — have the user re-run `xurl auth oauth2`.
- **Token refresh:** OAuth 2.0 tokens auto-refresh. Nothing to do.
- **Multiple apps:** Each app has isolated credentials/tokens. Switch with `xurl auth default` or `--app`.
- **Multiple accounts per app:** Select with `-u / --username`, or set a default with `xurl auth default APP USER`.
- **Token storage:** `~/.xurl` is YAML. Never read or send this file to LLM context.
- **Cost:** X API access is typically paid for meaningful usage. Many failures are plan/permission problems, not code problems.

- **Video post workflow:** See `references/video-post-quick.md` — step-to-step video upload + post with caption
- **Video file location:** `/tmp/` for Remotion outputs, `~/Downloads/` for user downloads
- **Browser fallback:** When CLI is unavailable or unconfigured, see `references/browser-workflow.md` for browser-based repost workflow.
- **CDP cookie extraction code:** See `references/cdp-cookie-extraction.md` for verified working Python code to extract Chrome's cookies via CDP, plus the guest-cookie tell (when Keychain blocks auth cookies).

---

## X.com Browser Automation Fallback (from playwright-automation + x-repost)

**⚠️ RESPONSE STYLE — VIETNAMESE CÁCH KHÁC (from x-repost)**
When posting/reposting to X, Anh prefers:
- Max 2-3 sentences for normal messages
- NO: "vấn đề là...", "giải pháp là...", "tóm lại..."
- Direct → go straight to action
- When Anh says "rút ngắn" → cut immediately, no explanation
- Vietnamese casual tone: "anh" + "mấy con vợ"

### ⚠️ Browser Fallback — macOS Keychain Blocks Cookie Extraction

When `xurl` API is unavailable, browser-based automation is possible but:

1. **On macOS: cookie extraction is IMPOSSIBLE** — Chrome Keychain blocks all tools.
   Even `browser-harness CDP`, `computer_use`, and Playwright return empty cookies.

2. **The ONLY reliable macOS path is xurl OAuth** — see `references/browser-workflow.md`
   Option A for setup instructions.

3. **If xurl is not configured yet:**
   - User must setup OAuth manually (see One-Time User Setup section above)
   - OR use manual cookie export (tedious, session-based, expires)

**Quick diagnostic:**
```bash
# Check if xurl is ready
xurl auth status 2>&1

# Check if Chrome is logged in (works)
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window' 2>/dev/null
```

**If xurl auth is missing AND user can't setup OAuth right now:**
→ Ask if user wants to proceed with manual cookie export OR wait for xurl setup.

### Cookie Export (required first step)
```bash
cd ~
browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://x.com", "https://www.x.com"])
cookies = result.get("cookies", [])
clean = [{k:v for k,v in c.items() if k in ("name","value","domain","path","expires","httpOnly","secure","session","sameSite")} for c in cookies]
print(json.dumps(clean))
PY
```
Save to `/tmp/x_cookies.json`.

### Simple Repost (via Playwright)
```python
import json
from playwright.sync_api import sync_playwright

with open("/tmp/x_cookies.json") as f:
    cookies = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context()
    ctx.add_cookies(cookies)
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    article = page.locator("article").first
    article.locator('[data-testid="retweet"]').first.click()
    page.wait_for_timeout(1500)
    for item in page.locator('[role="menuitem"]').all():
        try:
            txt = item.inner_text().lower()
            if "repost" in txt and "quote" not in txt:
                item.click()
                page.wait_for_timeout(2000)
                break
        except: pass
```

### Key X.com Selectors
| Element | Selector |
|---------|----------|
| Repost button | `[data-testid="retweet"]` |
| Confirm repost | menu item text matching "repost" |
| Quote textarea | `[data-testid="tweetTextarea_0"]` |
| Post button | `[data-testid="tweetButton"]` / `[data-testid="tweetButtonInline"]` |

### ⚠️ CRITICAL: aria-disabled Check Before Clicking Post
X.com sets `aria-disabled="true"` on Post button even when it visually appears enabled. **Always check DOM before clicking:**
```python
page.wait_for_function("""
() => {
  const btn = document.querySelector('[data-testid="tweetButtonInline"]');
  return btn && btn.getAttribute('aria-disabled') === 'false';
}
""", timeout=20000)
```

### Video Upload via Playwright (⚠️ blocked for video — use xurl instead)
X.com bot detection sets `aria-disabled="true"` on Playwright for video posts. For video, use `xurl media upload` + `xurl post --media-id`.

### Chrome Cookie Extraction on macOS — CRITICAL LIMITATION

**On macOS, Chrome's auth cookies (including X auth_token) are encrypted via the macOS Keychain.**
Remote debugging (CDP) cannot access Keychain-encrypted cookies — even when Chrome is launched with the same user profile and `--remote-debugging-port`.

**What this means:**
- `Network.getCookies` / `Network.getAllCookies` via CDP → returns GUEST cookies only (no auth_token)
- `browser-harness` → same limitation on macOS
- `computer_use` → controls macOS UI only, cannot read Chrome Keychain
- Manual cookie export from DevTools → the ONLY manual workaround

**If you need X authentication for automation, use xurl OAuth (see below).**

## X Credentials — macOS Keychain Limitation
- Account: @TyayUno (Anh Trinh's X account)
- ⚠️ Cookie file `/tmp/x_cookies.json` CANNOT be auto-generated on macOS — Chrome Keychain blocks all cookie extraction tools. Use **xurl OAuth** instead (see Option A in `references/browser-workflow.md`).
- **For automation: setup xurl OAuth** — this is the only reliable path on macOS.

## Related
- [[tiktok-viral-script]] — TikTok content creation
- [[browser-harness]] — cookie export via CDP

## Attribution

- Upstream CLI: https://github.com/xdevplatform/xurl (X developer platform team, Chris Park et al.)
- Upstream agent skill: https://github.com/openclaw/openclaw/blob/main/skills/xurl/SKILL.md
- Hermes adaptation: reformatted for Hermes skill conventions; safety guardrails preserved verbatim.
