# Browser Workflow — X.com Automation on macOS

> **⚠️ CRITICAL (2026-06-01): macOS Keychain blocks ALL cookie extraction.**
> Do NOT attempt cookie-based approaches on macOS. Read this entire file before
> deciding on an approach.

## The macOS Keychain Problem

Chrome on macOS stores cookies encrypted in the macOS Keychain. No automation
tool can extract them — not browser-harness, computer_use, Playwright, CDP,
osascript, or anything else. The Keychain is a system security boundary.

**Diagnosis:**
```bash
# This works → Chrome is logged in
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window'
# → https://x.com/home ✅

# But this returns empty → Keychain blocks cookie access
browser-harness -c 'cdp("Network.getCookies", urls=["https://x.com"])'
# → []  ❌
```

When step 1 = logged in but step 2 = empty → **Keychain problem, not login state.**
Switch immediately to xurl OAuth. Do not waste time trying other cookie methods.

## Decision Tree

```
Task: Automate X posting
│
├─ xurl CLI OAuth setup available?
│   → YES: Use xurl (Option A below) — RECOMMENDED
│
├─ Can use computer_use to drive Chrome UI?
│   → YES for clicks/types, NO for auth (no cookies)
│   → Only useful if user is ALREADY logged in AND has session
│
└─ Neither available?
    → Manual cookie export (Option B) — tedious, session-based
    → Or wait for xurl OAuth setup
```

## Option A: xurl OAuth (RECOMMENDED)

This is the ONLY reliable method on macOS. It uses X's official API via OAuth 2.0
PKCE — no cookies needed.

### One-time setup (user does outside agent):

1. Go to https://developer.x.com/en/portal/dashboard
2. Create app, get Client ID + Client Secret
3. Run in terminal:
   ```bash
   xurl auth apps add my-app --client-id YOUR_ID --client-secret YOUR_SECRET
   xurl auth oauth2 --app my-app YOUR_USERNAME
   xurl auth default my-app
   xurl whoami
   ```

### Agent verification:
```bash
xurl auth status
xurl whoami
```

### Post a tweet:
```bash
xurl post "Nội dung bài đăng"
```

## Option B: Manual Cookie Export (NOT RECOMMENDED — session-based)

Only use this if xurl OAuth is not available and the user needs immediate access.

### Step 1: User exports cookies from Chrome
1. Open x.com in Chrome (logged in)
2. DevTools (F12) → Application → Cookies → x.com
3. Copy all cookie name/value pairs

### Step 2: User gives cookies to agent
User pastes cookie data in chat.

### Step 3: Agent uses Playwright with manual cookies
```python
from playwright.sync_api import sync_playwright
import json

# User-provided cookies (must be in playwright format)
cookies = [
    {"name": "auth_token", "value": "xxx", "domain": ".x.com", "path": "/"},
    # ... more cookies from manual export
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context()
    ctx.add_cookies(cookies)
    page = ctx.new_page()
    page.goto("https://x.com")
    # Now can post/repost/etc.
```

**Problem:** Cookies expire. User must re-export periodically. xurl OAuth is permanent.

## Option C: computer_use UI Interaction (NOT for auth)

Use `computer_use + osascript` to drive Chrome's rendered UI. This WORKS for:
- Clicking elements
- Typing text
- Scrolling
- Taking screenshots

This does NOT work for:
- Reading Keychain-protected cookies
- Authenticating as the user
- Any action requiring the user's auth token

```bash
# Verify Chrome session state
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window'

# Navigate Chrome to a URL
osascript -e 'tell application "Google Chrome" to set URL of active tab of front window to "https://x.com"'

# Capture Chrome window
computer_use(action="capture", app="Google Chrome", mode="som")
```

## Quick Test — Always Run This First

Before attempting any cookie-based approach on macOS, always verify:

```bash
# Confirm Chrome is logged in
CHROME_URL=$(osascript -e 'tell application "Google Chrome" to get URL of active tab of front window' 2>/dev/null)
echo "Chrome URL: $CHROME_URL"

if [[ "$CHROME_URL" == *"x.com"* ]] || [[ "$CHROME_URL" == *"twitter.com"* ]]; then
    echo "✅ Chrome is logged into X"
    echo "❌ But cookie extraction is blocked by macOS Keychain"
    echo "→ Use xurl OAuth instead"
else
    echo "⚠️ Chrome is not logged into X"
fi
```

## Historical Test Results (2026-06-01)

| Tool | Chrome Session | Cookie Access | X Auth |
|------|---------------|---------------|--------|
| osascript | ✅ Logged in | ❌ Blocked by Keychain | ❌ (read-only) |
| browser-harness CDP | ✅ Logged in | ❌ Empty (Keychain) | ❌ |
| computer_use | ✅ Logged in | ❌ UI only | ❌ (no auth) |
| xurl OAuth | N/A | N/A | ✅ (if setup) |
| Manual cookie export | N/A | ✅ (if user provides) | ⚠️ (session-based) |

## Key Takeaway

**On macOS: xurl OAuth is the ONLY reliable automation path.**
All cookie-extraction tools are blocked by Keychain. Don't try browser-harness
CDP, Playwright, or any other cookie method on macOS — go straight to xurl.