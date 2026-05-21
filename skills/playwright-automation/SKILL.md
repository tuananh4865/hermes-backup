---
title: X.com Automation Skill
name: playwright-automation
description: "X.com repost/like/quote via Playwright using cookies from browser-harness."
version: 1.2.0
tags: [x, twitter, automation, playwright, social-media]
created: 2026-05-17
updated: 2026-05-21
relationships: [browser-harness]
---

# X.com Automation Skill

**⚠️ CRITICAL WORKFLOW: Use browser-harness to export cookies first, THEN playwright. Never launch separate browser or type credentials.**

## ⚠️ IMPORTANT: Don't Auto-Close Browser

**SAU KHI HOÀN THÀNH TASK AUTOMATION, KHÔNG ĐÓNG BROWSER!**

## 🖼️ Screenshot-First Verification (MANDATORY)AU KHI HOÀN THÀNH TASK AUTOMATION, KHÔNG ĐÓNG BROWSER!**

## 🖼️ Screenshot-First Verification (MANDATORY)

### Step 1: Export Cookies

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

Save output to `/tmp/x_cookies.json`.

### Step 2: Run Playwright

```python
import json
from playwright.sync_api import sync_playwright

with open("/tmp/x_cookies.json") as f:
    cookies = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    # ... automation ...
    browser.close()
```

---

## 🎯 Core Principles (MUST FOLLOW)

### 1. READ Before Action
- Read the actual content
- Understand context/situation  
- DON'T jump straight into code

### 2. KISS - Keep It Simple
- Simple click() > complex JS
- First solution = simplest solution
- Don't over-engineer

### 3. Quality Over Quantity
- Meaningful, specific comments > generic templates
- Do it right once > do it wrong 10 times

---

## 🔑 Working Selectors (X.com)

```
[data-testid="retweet"]         → repost button
[data-testid="retweetConfirm"]  → confirm repost in menu
[data-testid="tweetTextarea_0"]  → quote compose textarea
[data-testid="tweetButton"]      → post button
[role="menu"]                    → dropdown menu
[role="menuitem"]                → menu items
```

---

## 📋 Quote Repost Workflow

```
1. page.goto(url)
2. WAIT for content to load
3. READ the tweet content (first ~300 chars)
4. THINK about what comment fits
5. WRITE comment relevant to content
6. click([data-testid="retweet"])
7. WAIT for menu
8. Find and click "Quote" in menu
9. WAIT for compose modal
10. fill textarea with your thoughtful comment
11. click([data-testid="tweetButton"])
12. WAIT for success
```

---

## 📋 Simple Repost Workflow (working 2026-05-21)

```python
page.goto(url, wait_until="domcontentloaded")
page.wait_for_timeout(3000)

article = page.locator("article").first
article.locator('[data-testid="retweet"]').first.click()
page.wait_for_timeout(1500)

# Confirm via menu item text — NOT data-testid
for item in page.locator('[role="menuitem"]').all():
    try:
        txt = item.inner_text().lower()
        if "repost" in txt and "quote" not in txt:
            item.click()
            page.wait_for_timeout(2000)
            break
    except: pass
```

---

## Pitfalls (updated 2026-05-21)

| Problem | Fix |
|---------|-----|
| Cookie JSON parse errors | Strip to only `name,value,domain,path,expires,httpOnly,secure,session,sameSite` |
| No articles found on profile | Go to `/home` first, scroll, THEN find articles |
| `auth_token` httpOnly | browser-harness CDP reads it fine; playwright can't |
| Confirm button not `[data-testid="retweetConfirm"]` | It's a `[role="menuitem"]` with text matching |
| `page_info()` shows URL but browser shows logged-out page | CDP snapshot returns different DOM than visual render — use screenshot to verify actual auth state |
| User asks for screenshot to verify state | Always screenshot-first, send via MEDIA:, then short text description — never long technical paragraphs |

---

## 🔴 Always Remember

1. **READ content first** - understand what you're interacting with
2. **Write meaningful comments** - not generic templates
3. **Simple code** - don't add complexity if not needed
4. **Test simple first** - complex only if simple fails
5. **Don't close browser** - keep open for user inspection

---

## 🚫 Anti-Patterns

- ❌ Generic comments for all posts
- ❌ Pattern matching instead of reading content
- ❌ Complex JS when simple click() works
- ❌ Over-engineering simple tasks
- ❌ Debugging for 30+ minutes when solution is simple

---

## 📁 Related Files

- `scripts/export_x_cookies.py` - cookie export via browser-harness (run inside `browser-harness <<'PY'` heredoc)
- `scripts/repost.py` - simple repost script (run standalone after cookies exported)
- `references/playwright_auto.py` - working Playwright reference with cookie injection
- `references/video_posting_workflow.md` - video posting specific workflow and selectors

## ⚠️ Video Posting — CRITICAL: Playwright BLOCKED by X.com Bot Detection

**For video posts, use xurl API directly. Playwright will NOT work.**

X.com detects Playwright browser automation and sets `aria-disabled="true"` on the Post button — even when:
- Upload is 100% complete
- Caption is typed correctly
- Button VISUALLY appears enabled (visual inspection shows enabled)
- Proper `wait_for_function` checks pass

The `aria-disabled` attribute is set at a level that bypasses all JavaScript workarounds.

**Working path for video posts:**
```bash
# Setup OAuth once (see xurl skill)
xurl auth oauth2 --app my-app

# Post video
xurl media upload /tmp/video.mp4
# → returns MEDIA_ID
xurl post "Your caption" --media-id MEDIA_ID
```

**Selectors for video posts:** (for photo posts only — video posts don't work with Playwright)

```python
# 1. Click media button FIRST
page.locator('[data-testid="addPhoto"]').click()
page.wait_for_timeout(1000)

# 2. Set file input (hidden), dispatch change event
page.evaluate("""
fileInput = document.querySelectorAll('input[type="file"]')[0];
dataTransfer = new DataTransfer();
dataTransfer.items.add(fileObject);
fileInput.files = dataTransfer.files;
fileInput.dispatchEvent(new Event('change', {bubbles: true}));
""", fileObject=file_object)

# 3. WAIT for upload to complete (blue progress circle disappears)
page.wait_for_function("""
() => {
  const spinner = document.querySelector('[data-testid="videoPlayer"]');
  const uploading = document.querySelector('[aria-label*="Uploading"]');
  return !spinner && !uploading;
}
""", timeout=30000)

# 4. THEN type caption
page.locator('[data-testid="tweetTextarea_0"]').fill(caption)

# 5. WAIT for Post button to become enabled (may take 5-15s after typing)
page.wait_for_function("""
() => {
  const btn = document.querySelector('[data-testid="tweetButtonInline"]');
  return btn && btn.getAttribute('aria-disabled') === 'false';
}
""", timeout=20000)

# 6. Click Post
page.locator('[data-testid="tweetButtonInline"]').click()
```

**Why buttons get stuck disabled:**
- If you click Post before upload fully completes → stuck disabled forever
- If you type before upload finishes → text gets corrupted
- `aria-disabled="true"` is NOT visual — button LOOKS enabled but DOM says disabled
- This is X.com bot detection activating on Playwright browser

**Selectors for video posts:**
- Media button: `[data-testid="addPhoto"]` or `[aria-label*="Add photos or video"]`
- Video player (appears after upload): `[data-testid="videoPlayer"]`
- Post button: `[data-testid="tweetButtonInline"]`
- Caption textarea: `[data-testid="tweetTextarea_0"]`

**Pitfalls (updated 2026-05-21)**

| Problem | Fix |
|---------|-----|
| Cookie JSON parse errors | Strip to only `name,value,domain,path,expires,httpOnly,secure,session,sameSite` |
| No articles found on profile | Go to `/home` first, scroll, THEN find articles |
| `auth_token` httpOnly | browser-harness CDP reads it fine; playwright can't |
| Confirm button not `[data-testid="retweetConfirm"]` | It's a `[role="menuitem"]` with text matching |
| `page_info()` shows URL but browser shows logged-out page | CDP snapshot returns different DOM than visual render — use screenshot to verify actual auth state |
| User asks for screenshot to verify state | Always screenshot-first, send via MEDIA:, then short text description — never long technical paragraphs |
| Post button `aria-disabled="true"` after upload | WAIT for upload complete before typing, then WAIT for button enable before clicking |
| Button looks enabled but `aria-disabled="true"` | Don't trust visual — always check DOM attribute via `page.evaluate()` |
| X.com bot detection on Playwright | For video posts, try xurl API instead (see xurl skill) |