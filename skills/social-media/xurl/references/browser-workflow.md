# X Browser Workflow (when xurl CLI unavailable)

Use browser when:
- `xurl` not installed, OR
- No credentials in `~/.xurl`, OR
- User wants visual confirmation before posting

## Workflow

### 1. Check prerequisites first
```bash
# Check if xurl CLI exists
xurl --help 2>&1 | head -3

# Check auth status
xurl auth status 2>&1

# Check for X credentials in .env
grep -i "X_\|TWITTER_\|SOCIAL_" ~/.hermes/.env
```

### 2. If CLI unavailable → use browser

Navigate to `https://x.com` and:
1. Click **Sign in** link (ref changes each load — use browser_snapshot first)
2. Fill login form (email/phone/username → Next → password)
3. After login, navigate to target post URL
4. Find **Repost** button → **Repost** option → Confirm

### 3. Cookie Export + Playwright (when browser-harness is available)

If `browser-harness` is available AND Chrome is already logged into X, use this workflow instead of manual login. It bypasses re-login entirely.

**Step 1**: Export cookies from Chrome via browser-harness (authenticated session):
```bash
browser-harness -c '
export_cookies("x_com_cookies.json")
'
```

**Step 2**: Use Playwright with the exported cookies to perform actions (repost, quote, reply, etc.):
```python
from playwright.sync_api import sync_playwright
import json

with open("x_com_cookies.json") as f:
    cookies = json.load(f)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    
    # Navigate to target post and repost
    page.goto("https://x.com/user/status/POST_ID")
    page.click("[data-testid='retweet']")
    page.click("[data-testid='retweet']")  # Confirm repost
```

**Why this works**: Chrome is already logged into X. Exporting its session cookies and applying them to Playwright transfers the authenticated session without any login flow.

**When to use this**:
- xurl CLI is not installed or unconfigured
- User wants repost without re-authenticating
- browser-harness + Playwright are both available on the system

**Finding relevant posts**: For Tuấn Anh's interests (TikTok Shop, AI agents, content creation):
- Search: `https://x.com/search` for relevant hashtags/topics
- Timeline: `https://x.com/home` for following feed
- No credentials needed for reading (except for repost action)

## Key refs (dynamic)
Browser snapshot refs change on every page load — always call `browser_snapshot` after `browser_navigate` before clicking.

## Sign of missing setup
If browser shows "Join today" landing page → not logged in → need credentials or OAuth setup.