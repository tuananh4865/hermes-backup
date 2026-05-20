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

---

## 🎯 Core Workflow: browser-harness → Playwright

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

## ⚠️ Pitfalls (learned 2026-05-21)

| Problem | Fix |
|---------|-----|
| Cookie JSON parse errors | Strip to only `name,value,domain,path,expires,httpOnly,secure,session,sameSite` |
| No articles found on profile | Go to `/home` first, scroll, THEN find articles |
| `auth_token` httpOnly | browser-harness CDP reads it fine; playwright can't |
| Confirm button not `[data-testid="retweetConfirm"]` | It's a `[role="menuitem"]` with text matching |

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

- `pre-automation-checklist.md` - checklist to follow
- `x-com-automation-lessons.md` - lessons learned
- `scripts/export_x_cookies.py` - cookie export via browser-harness (run inside `browser-harness <<'PY'` heredoc)
- `scripts/repost.py` - simple repost script (run standalone after cookies exported)

## ⚠️ Pitfalls

Last updated: 2026-05-17