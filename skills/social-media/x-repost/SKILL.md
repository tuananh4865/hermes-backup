---
name: x-repost
title: X/Twitter Repost Workflow
description: Post new content or find and repost existing X posts
updated: 2026-05-21
type: skill
tags: [social-media, x, twitter]
confidence: high
relationships: [social-media-automation]
---

# X Post and Repost Skill

## Trigger

## Response Style MANDATORY
**VIETNAMESE CÁCH KHÁC — VIẾT NGẮN GỌN, KHÔNG GIẢI THÍCH DÀI DÒNG**
- Tối đa 2-3 câu cho message thường
- KHÔNG: "vấn đề là...", "giải pháp là...", "tóm lại..."
- Nếu anh hỏi → trả lời thẳng, đi thẳng vào việc
- Khi user nói "rút ngắn chữ lại" → cắt ngay, không bào chữa

## X Free Account Limits
- ~300 words per post (không phải ký tự)
- Video: max 140s cho大多数 accounts
- Images: max 4 per post

## Trigger Logic
When Anh says "đăng lên X", "post lên X", "repost", "share lên X":
- **repost** → Find existing post and share it (Section A)
- **đăng post mới** → Create new post with optional media (Section B)

---

## Section A REPOST Find and Share Existing Post

### Step 1: Research Relevant Post
Search for posts related to the topic Anh cares about:
```
mcp_exa_web_search_exa(query="<topic> site:x.com OR site:twitter.com", numResults=10)
```

### Step 2: Select Best Post
Criteria:
- From credible source (tech news, verified accounts)
- High engagement (likes, RTs)
- Relevant to Anh's interests (AI agents, TikTok, productivity)
- Not political/controversial

### Step 3: Get Post URL
Find the exact tweet/post URL to repost.

### Step 4: Execute Repost via Playwright
```python
# ~/.hermes/hermes-agent venv has playwright installed
import asyncio
from playwright.async_api import async_playwright

async def repost(cookies_path="/tmp/x_cookies.json"):
    cookies = json.load(open(cookies_path))
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context()
        await ctx.add_cookies(cookies)
        page = await ctx.new_page()
        await page.goto(tweet_url)
        await page.wait_for_load_state("networkidle")
        # Click repost/retweet button — selector varies by X UI
        # Usually: [data-testid="retweet"]
        await page.click('[data-testid="retweet"]')
        await page.wait_for_timeout(500)
        # Confirm "Retweet" option (not "Quote Tweet")
        await page.click('text=Retweet')
        await asyncio.sleep(2)
        await browser.close()
```

### Step 5: Screenshot + Report
Take screenshot after repost to confirm success:
```
browser-harness screenshot → /tmp/repost_result.png
```
Report to Anh: "Đã repost bài về <topic> từ @<author>"

## X Credentials
- Account: @TyayUno (Anh Trinh's X account)
- Cookies: `/tmp/x_cookies.json` (export via browser-harness CDP)
- Cookies export command:
```bash
cd ~ && browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://x.com"])
print(json.dumps(result.get("cookies", [])))
PY
```

---

## Section B POST NEW CONTENT Text and Media

### Step 0: Check Login State ALWAYS FIRST
```
browser_navigate("https://x.com")
```
- "Join today" = NOT logged in
- Home timeline = logged in

### If NOT Logged In — Three Options

**Option 1: computer_use AppleScript (BEST for this user)**
Use `computer_use` to control user's real Chrome directly — no restart needed:
```
computer_use(action="capture", app="Google Chrome")
# Navigate to x.com/compose/post
# Upload video, type text, click Post via element index
```
This uses the user's already-running Chrome with full session.

**Option 2: Restart Chrome with remote-debugging**
1. User quits their Chrome
2. User opens Chrome with: `open -a "Google Chrome" --args --remote-debugging-port=9222`
3. browser-harness can now attach to user's profile

**Option 3: xurl API setup**
1. X Developer account → create app → OAuth 2.0
2. `xurl auth apps add <name> --client-id <ID> --client-secret <SECRET>`
3. `xurl auth oauth2 --app <name>`
4. `xurl post --text "..." --media /path/to/file`

### If Logged In — Browser-harness Post

**Step 1:** Navigate to compose
```
browser_navigate("https://x.com/compose/post")
```

**Step 2:** Upload media
Use browser-harness helpers.py `upload_file()` at line 452 — NOT Playwright directly.
Wait for video thumbnail to appear before proceeding.

**Step 3:** Type caption
```python
fill_input("[data-testid=\"tweetTextarea_0\"] .first", caption_text)
```

**Step 4:** Wait for button enable
`[data-testid="tweetButtonInline"]` enables ONLY after:
- Video fully processed server-side (can take 30-60s)
- Text entered

Polling: check every 5s, timeout 120s.

**Step 5:** Click post

**Step 6:** Verify
- URL changes to /<username>/status/<id>
- Tweet appears in timeline

### Bot Detection Workaround
If button stays disabled after video appears:
1. Take screenshot — verify video thumbnail visible
2. Wait longer (server-side processing)
3. Refresh page after video thumbnail shows
4. Last resort: use xurl API (needs OAuth setup)

**⚠️ CRITICAL LESSON (2026-05-21): When Post Button Enables → CLICK IMMEDIATELY**

Session May 20 (repost): Video+text worked, Post button enabled, clicked immediately → SUCCESS.
Session May 21 (video post): Video uploaded 100%, text typed, Post button enabled → DIDN'T CLICK, kept debugging → button disabled → FAILED.

**Rule: When tweetButtonInline enables with correct content, CLICK WITHIN 5 SECONDS. Do not continue debugging.**

---

## Credentials
- Account: @TyayUno (Anh Trinh)
- Cookie file: /tmp/x_cookies.json
- xurl installed: ~/.local/bin/xurl

## Key Learnings 2026-05-21
1. "Repost" = find existing post, NOT create new content
2. Always check login state FIRST before attempting anything
3. "300 words" limit = NOT characters
4. Video requires server-side processing before button enables
5. Response style: Vietnamese casual, short, no long explanations
6. When user says "rút ngắn chữ lại" → cut immediately, no excuses

## Pitfalls

### browser_snapshot returns "(empty page)" on X
`browser_snapshot()` FAILS to capture X's React-rendered content — always returns empty. **Use screenshot + vision instead:**
```bash
# Capture
browser-harness <<'PY'
capture_screenshot("/tmp/x_state.png")
PY
# Analyze
mcp_MiniMax_understand_image("/tmp/x_state.png", "Mô tả chính xác...")
```

### browser_navigate/goto_url time out on x.com URLs
X.com triggers timeout in browser-harness navigation tools. Use `page_info()` to check current state, `capture_screenshot()` for visual verification.

### browser-harness Uses SEPARATE Chrome Instance — NOT User's Chrome
**CRITICAL ARCHITECTURE (2026-05-21):** browser-harness spawns its own headless Chrome with a separate `user-data-dir` at `/var/folders/.../agent-browser-chrome-*/`. It does NOT connect to the user's running Chrome instance.

**Two Chrome processes can run simultaneously:**
- `/Applications/Google Chrome.app` — user's real Chrome, LOGGED IN to X
- Agent's headless Chrome at `/var/folders/.../agent-browser-chrome-*/` — NOT LOGGED IN

**Implication:** Exporting cookies from browser-harness CDP gives you agent's Chrome cookies, which are NOT logged into X. The user's real Chrome cookies are encrypted by macOS Keychain (`encrypted_value` field, no plain text) and cannot be extracted without user interaction.

**Solution when browser-harness shows "not logged in":**
1. **Best:** Use computer_use (AppleScript) to control user's real Chrome directly
2. **Alternative:** Quit user's Chrome → restart with `--remote-debugging-port=9222` so browser-harness can attach
3. **Fallback:** Setup xurl API (OAuth) — does not depend on browser session

### osascript `do JavaScript` FAILS for Chrome — Empty Output Always
**osascript AppleScript cannot run JavaScript in Google Chrome.** All `do JavaScript` calls return empty string with error "Expected end of line but found identifier" or similar syntax errors. This applies to both standard AppleScript and JXA (JavaScript for Automation) modes.

Workaround: Use osascript only for:
- Navigation: `tell application "Google Chrome" to open location "..."`
- URL retrieval: `tell application "Google Chrome" to return URL of active tab of window 1`
- Mouse/keyboard events via System Events

For JS execution in Chrome, use `computer_use` with cua-driver daemon.

### cua-driver Daemon Must Be Running for computer_use
`computer_use` requires the CuaDriver daemon running. If you get:
`cuadaemon not reachable on /Users/.../cua-driver.sock`
Start it with: `open -n -g -a CuaDriver --args serve`
Then retry computer_use.

### Video upload + text → Post button enables → CLICK IMMEDIATELY
Video uploaded 100%, text typed, Post button enabled → session failed because agent kept debugging instead of clicking. **Rule: When tweetButtonInline enables WITH correct content, click within 5 seconds. Stop all debugging.**

## Support Files
- `references/x-browser-state.md` — Session log and verified state checks for X.com automation
- `references/video-post-worked-may20.md` — May 20 successful video post details
- `references/chrome-automation-architectures.md` — browser-harness vs osascript vs computer_use comparison (2026-05-21)

## Related
- [[tiktok-viral-script]] — for content creation tasks
- [[social-media-automation]] — umbrella skill for all social platforms
