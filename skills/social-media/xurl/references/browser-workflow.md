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
grep -i "X_|TWITTER_|SOCIAL_" ~/.hermes/.env
```

### 2. If CLI unavailable → use computer_use (BEST)

**Use `computer_use` to control user's real Chrome directly.** This is the preferred method because:
- User's Chrome is already logged into X
- No cookie export needed
- No session migration needed
- Works with macOS Keychain-protected sessions

```bash
# Capture current Chrome state
computer_use(action="capture", app="Google Chrome")

# Navigate to X compose
computer_use(action="type", text="Your post text here")
# Use element index clicking for Post button
```

### 3. Alt: browser-harness with remote-debugging Chrome

If `computer_use` is unavailable:

1. User quits their Chrome
2. User opens Chrome with: `open -a "Google Chrome" --args --remote-debugging-port=9222`
3. browser-harness can now attach to user's profile (now at localhost:9222)
4. browser-harness will have access to the logged-in session

### 4. xurl OAuth (MOST RELIABLE when configured)

**xurl with OAuth is the most reliable long-term solution** but requires:
1. X Developer account
2. App registration at https://developer.x.com
3. User completes OAuth flow once manually

See xurl skill setup instructions.

---

## ⚠️ Cookie Export + Playwright — DO NOT USE (2026-05-21)

Chrome's X session tokens are stored in EncryptedValue (macOS Keychain-protected), not plain cookies. Exporting cookies via CDP or browser-harness only gets the cookie container, NOT the decryption key needed to restore the session.

**Symptom:** Cookies export successfully, Playwright imports them, but X still shows "Join today" (not logged in).

**This is why browser-harness automation fails for X even when Chrome is logged in.**

---

## X Anti-Bot Detection (2026-05-21)

X.com's React app marks action buttons (Post, Repost, Like) as `aria-disabled="true"` at the DOM layer, even when they appear visually enabled. Screenshot verification is insufficient.

**Check before clicking:**
```javascript
document.querySelector('[data-testid="tweetButtonInline"]')?.getAttribute('aria-disabled')
// Returns "true" = blocked by anti-bot
// Returns null = button is functional
```

## Sign of missing setup
If browser shows "Join today" landing page → not logged in → need credentials or OAuth setup.

## Key refs (dynamic)
Browser snapshot refs change on every page load — always call `browser_snapshot` after `browser_navigate` before clicking.
