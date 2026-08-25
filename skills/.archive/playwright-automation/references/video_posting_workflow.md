# X.com Video Posting Workflow

**Date:** 2026-05-21
**Status:** Playwright approach blocked by bot detection for video posts
**Alternative:** Use xurl API for video posts

## Working: Photo posts with Playwright

Text-only posts or photo posts work with Playwright:
```python
page.locator('[data-testid="addPhoto"]').click()
# ... photo upload ...
page.locator('[data-testid="tweetTextarea_0"]').fill("caption")
page.locator('[data-testid="tweetButtonInline"]').click()
```

## Broken: Video posts with Playwright

Video posts fail at the final step — Post button ends up with `aria-disabled="true"` even when it visually appears enabled.

### Tested Sequence (all attempts failed)
1. Upload video → 100% ✓
2. Type caption → ✓
3. Wait for Post button → aria-disabled="true" ✗
4. JS click → returns "clicked" but doesn't submit ✗

### Why It Fails
- X.com detects Playwright browser automation
- Sets `aria-disabled="true"` on Post button when Playwright is detected
- Visual appearance is misleading — button LOOKS enabled but DOM is disabled
- No workaround found at browser-automation level

## Solution: Use xurl API

```bash
# Setup OAuth (one-time)
xurl auth oauth1
# → Enter API Key + Secret from developer.x.com

# Post video
xurl post "caption" --file /tmp/video.mp4
```

**Requirements:**
- X Developer account at developer.x.com
- App with Read/Write permissions
- OAuth1 or OAuth2 credentials

## Known Good Selectors

| Element | Selector |
|---------|----------|
| Media button | `[data-testid="addPhoto"]` or `[aria-label*="Add photos or video"]` |
| Caption textarea | `[data-testid="tweetTextarea_0"]` |
| Post button | `[data-testid="tweetButtonInline"]` |
| Video player | `[data-testid="videoPlayer"]` |
| Upload progress | `[aria-label*="Uploading"]` |

## Cookie Export (still works)

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

Save to `/tmp/x_cookies.json` before running Playwright.
