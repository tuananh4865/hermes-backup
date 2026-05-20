---
title: Social Media Automation via Browser-Harness + Playwright
name: social-media-automation
description: Quy trình automation social media (X, TikTok, Facebook, Instagram, etc.) bằng cách export cookies từ browser-harness (Chrome đang login), sau đó dùng Playwright để thực hiện actions (repost, like, share). Áp dụng cho tất cả nền tảng.
version: 2.0.0
created: 2026-05-20
updated: 2026-05-20
relationships: [browser-harness, playwright-automation, xurl]
---

# Social Media Automation Workflow

## Overview

Kết hợp **browser-harness** (export cookies từ Chrome đang login) + **Playwright** (automation mạnh) để automate actions trên **mọi nền tảng social media**.

**Pattern chính**: Browser đã login → export cookies → dùng cookies đó trong Playwright → automate.

## Universal Workflow

### Step 1: Export Cookies từ Browser-Harness

```bash
browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://TARGET_PLATFORM.com"])
cookies = result.get("cookies", [])
print(json.dumps(cookies))
PY
```

### Step 2: Setup Playwright + Cookies

```python
import json
from playwright.sync_api import sync_playwright

# Load và clean cookies (chỉ giữ lại fields Playwright cần)
def clean_cookies(raw_cookies):
    needed = ["name", "value", "domain", "path", "expires", "httpOnly", "secure", "session", "sameSite"]
    return [{k: c[k] for k in needed if k in c} for c in raw_cookies]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(clean_cookies(raw_cookies))
    page = context.new_page()
    # ... automation code
```

### Step 3: Platform-Specific Actions

---

## Platform: X.com (Twitter)

### Cookies URL
```
https://x.com hoặc https://www.x.com
```

### Essential Cookies
| Cookie | Purpose |
|--------|---------|
| `auth_token` | Authentication |
| `ct0` | CSRF token |
| `twid` | User ID |
| `guest_id*` | Guest tracking |

### Selectors
| Element | Selector |
|---------|----------|
| Repost button | `[data-testid="retweet"]` |
| Confirm repost | `[data-testid="retweetConfirm"]` |
| Quote textarea | `[data-testid="tweetTextarea_0"]` |
| Post button | `[data-testid="tweetButton"]` |
| Menu items | `[role="menuitem"]` |
| Article (post) | `article` |

### Repost Code
```python
page.goto("https://x.com/USERNAME/status/POST_ID", wait_until="domcontentloaded")
page.wait_for_timeout(3000)

# Click repost
page.locator('[data-testid="retweet"]').first.click()
page.wait_for_timeout(1500)

# Simple repost (not quote)
page.locator('[data-testid="retweetConfirm"]').first.click()
page.wait_for_timeout(2000)
print("✅ Repost done!")
```

### Quote Repost Code
```python
# Click repost → chọn Quote
page.locator('[data-testid="retweet"]').first.click()
page.wait_for_timeout(1000)

# Chọn Quote trong menu
for item in page.locator('[role="menuitem"]').all():
    if "quote" in item.inner_text().lower():
        item.click()
        break
page.wait_for_timeout(2000)

# Viết comment
page.locator('[data-testid="tweetTextarea_0"]').fill("Your comment here...")
page.wait_for_timeout(1000)

# Post
page.locator('[data-testid="tweetButton"]').click()
page.wait_for_timeout(2000)
print("✅ Quote repost done!")
```

### Find Relevant Posts
```python
# Scroll timeline và đọc posts
for _ in range(10):
    articles = page.locator("article").all()
    for article in articles:
        text = article.inner_text()
        link = article.locator('a[href*="/status/"]').first.get_attribute("href")
        # Filter theo keywords
        if any(k in text.lower() for k in ['ai', 'agent', 'automation', 'hermes']):
            print(f"Found: {link}")
    page.evaluate("window.scrollBy(0, 600)")
    page.wait_for_timeout(1000)
```

---

## Platform: TikTok

### Cookies URL
```
https://www.tiktok.com
```

### Notes
- **Logged-in Chrome bypasses CAPTCHA** — key finding
- CAPTCHA chỉ block khi Chrome KHÔNG login TikTok
- View counts nằm trong anchor text (e.g., "25.2M")

### Essential Selectors
| Element | Selector |
|---------|----------|
| Like button | `[data-e2e="like-button"]` |
| Comment button | `[data-e2e="comment-icon"]` |
| Share button | `[data-e2e="share-icon"]` |
| Video link | `a[href*="/video/"]` |

### Video Stats
```python
# Lấy view counts từ video links
videos = page.evaluate("""
() => {
    return Array.from(document.querySelectorAll('a[href*="/video/"]'))
        .filter(a => /\\d+[MK]/.test(a.innerText))
        .map(a => ({
            href: a.href,
            views: a.innerText.match(/(\\d+\\.?\\d*)[MK]/)?.[0]
        }));
}
""")
```

---

## Platform: Facebook

### Cookies URL
```
https://www.facebook.com
```

### Essential Selectors
| Element | Selector |
|---------|----------|
| Like button | `[data-testid="fb-ufi-likelink"]` |
| Share button | `[role="button"][aria-label*="Share"]` |
| Post article | `[data-pagelet="FeedUnit"]` |
| Comment textarea | `[data-testid="UFI2CommentComposerInput"]` |

### Actions
```python
# Like
page.locator('[data-testid="fb-ufi-likelink"]').first.click()

# Share (mở menu)
page.locator('[role="button"][aria-label*="Share"]').first.click()
page.wait_for_timeout(1000)
```

---

## Platform: Instagram

### Cookies URL
```
https://www.instagram.com
```

### Essential Selectors
| Element | Selector |
|---------|----------|
| Like button | `article button[type="button"] svg[aria-label="Like"]` |
| Unlike (liked state) | `article button[type="button"] svg[aria-label="Unlike"]` |
| Comment textarea | `article textarea` |
| Post link | `article a[href*="/p/"]` |

### Like/Unlike
```python
# Like
like_btn = page.locator('article button[type="button"] svg[aria-label="Like"]').first
if like_btn.count() > 0:
    like_btn.click()
    print("✅ Liked!")
```

---

## Platform: LinkedIn

### Cookies URL
```
https://www.linkedin.com
```

### Essential Selectors
| Element | Selector |
|---------|----------|
| Like button | `[data-test-id="social-actions-like"]` |
| Comment button | `button[aria-label*="comment"]` |
| Share button | `[data-test-id="social-actions-share"]` |
| Post article | `.feed-shared-update-v2` |

---

## Platform: YouTube

### Cookies URL
```
https://www.youtube.com
```

### Essential Selectors
| Element | Selector |
|---------|----------|
| Like button | `like-button-view-model button[aria-label*="like"]` |
| Subscribe button | `subscribe-button ytd-subscribe-button-renderer` |
| Video link | `ytd-rich-item-renderer a[href*="/watch"]` |

---

## Generic Helper Functions

### Export Cookies (All Platforms)
```bash
# Run trong browser-harness
browser-harness <<'PY'
import json
domains = [
    "https://x.com",
    "https://www.tiktok.com", 
    "https://www.facebook.com",
    "https://www.instagram.com",
    "https://www.linkedin.com"
]
result = cdp("Network.getCookies", urls=domains)
print(json.dumps(result.get("cookies", [])))
PY
```

### Save Cookies to File
```python
import json, sys

raw = sys.stdin.read()
cookies = json.loads(raw)

# Save full cookies
with open("/tmp/social_cookies_full.json", "w") as f:
    json.dump(cookies, f)

# Save platform-specific
platforms = {}
for c in cookies:
    domain = c.get("domain", "")
    for platform in ["x.com", "tiktok.com", "facebook.com", "instagram.com", "linkedin.com"]:
        if platform in domain:
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(c)

for platform, pc in platforms.items():
    safe_name = platform.replace(".", "_")
    with open(f"/tmp/cookies_{safe_name}.json", "w") as f:
        json.dump(pc, f)
    print(f"Saved {len(pc)} cookies for {platform}")
```

### Quick Load & Automate
```python
import json
from playwright.sync_api import sync_playwright

PLATFORM = "x.com"  # Đổi theo platform
COOKIE_FILE = f"/tmp/cookies_{PLATFORM.replace('.', '_')}.json"

with open(COOKIE_FILE) as f:
    cookies = json.load(f)

# Clean cho Playwright
cleaned = [{k: c[k] for k in ["name","value","domain","path","expires","httpOnly","secure","session","sameSite"] if k in c} for c in cookies]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context()
    ctx.add_cookies(cleaned)
    page = ctx.new_page()
    
    # TODO: Add platform-specific automation here
    print(f"Logged in to {PLATFORM}")
    
    browser.close()
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 0 articles/posts found | Scroll page, increase `wait_for_timeout` |
| Cookies expired | Re-export cookies từ browser-harness |
| Button not found | Screenshot → inspect → verify selector |
| CAPTCHA appeared | User chưa login đúng trên Chrome |

---

## Quick Reference

| Platform | Cookie Domain | Key Selector |
|----------|--------------|--------------|
| X.com | `x.com` | `[data-testid="retweet"]` |
| TikTok | `tiktok.com` | `[data-e2e="like-button"]` |
| Facebook | `facebook.com` | `[data-testid="fb-ufi-likelink"]` |
| Instagram | `instagram.com` | `svg[aria-label="Like"]` |
| LinkedIn | `linkedin.com` | `[data-testid="social-actions-like"]` |
| YouTube | `youtube.com` | `[aria-label*="like"]` |

---

## Notes

- **Headless**: `headless=False` → inspect trực tiếp; `headless=True` → background
- **Cookies persist**: Chỉ valid trong vài ngày → re-export khi hết hạn
- **Browser vẫn mở**: Sau automation, browser để open để inspect
- **Headless cho cron**: Khi chạy tự động qua cron, dùng `headless=True`