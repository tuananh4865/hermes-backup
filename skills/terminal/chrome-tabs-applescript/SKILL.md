---
name: chrome-tabs-applescript
title: Chrome Tabs via AppleScript
description: Get Chrome window and tab info AND extract page content via osascript — fast and reliable scraping when HTTP/API paths are blocked
created: 2026-05-02
updated: 2026-06-17
type: skill
tags: [terminal, macos, chrome, scraping, ecommerce]
confidence: high
relationships: [browser-harness, macos-computer-use]
---

# Chrome Tabs via AppleScript — macOS

Get Chrome window and tab information using `osascript`.

## When to Use

- User asks what tabs are open in Chrome
- Need to check if a specific site is open
- Need to get URLs or titles of Chrome tabs for automation

## Commands

### Get front window name (fastest)
```bash
osascript -e 'tell application "Google Chrome" to get name of front window'
```

### Get all tab names of front window
```bash
osascript -e 'tell application "Google Chrome" to get name of every tab of front window'
```

### Get all tab URLs of front window
```bash
osascript -e 'tell application "Google Chrome" to get URL of every tab of front window'
```

### Get ALL tabs from ALL windows
```bash
osascript -e 'tell application "Google Chrome" to get URL of every tab of every window'
```

## Pitfalls

1. **`screencapture -x` hangs** — Don't use for Chrome tab capture, it can timeout
2. **Full window enumeration via System Events times out** — `get name of every window of every process` hangs
3. **`chrome://tabsearch/` navigation fails** — browser_navigate can't handle internal Chrome URLs
4. **Always query specific properties** — `name of front window` works when `every window of every process` times out
5. **`title of active tab of front window`** returns the **window name**, not the active tab title — use `name of tab N` instead

## What Works vs What Fails

| Approach | Result |
|---------|--------|
| `browser_navigate("chrome://newtab")` | ❌ Only shows new tab page, not real tabs |
| `osascript get name of front window` | ✅ Fast, reliable |
| `osascript get name of every tab of front window` | ✅ Fast |
| `osascript get URL of every tab of every window` | ✅ Works for full inventory |
| `screencapture -x` | ❌ Can hang/timeout, image often black |
| `System Events` full enumeration | ❌ Times out |

## Verification

Run one of the commands above — should return tab name(s) or URLs instantly.

## Quick Reference

Session-agnostic command reference: `references/commands.md`
- Tab index is 1-based (tab 1 = leftmost)
- `title of active tab of front window` → returns window name, NOT active tab — use `name of tab N` instead
- Tab numbering resets per window

**Domain-specific recipes:**
- `references/shopee-scrape-recipe.md` — verified recipe for scraping Shopee VN product pages
  (B2C Vietnamese e-commerce). When `web_extract` / `curl` / Shopee API all fail, this is the
  only path that works — uses the user's real logged-in Chrome. Same pattern works for TikTok
  Shop / Lazada / Tiki.

## Open Chrome + Navigate

```bash
# Open Chrome (brings to front)
open -a "Google Chrome"

# Navigate to URL in new tab (stays in Chrome)
osascript -e 'tell application "Google Chrome" to open location "https://x.com"'

# Activate Chrome (bring to front without focusing a tab)
osascript -e 'tell application "Google Chrome" to activate'
```

**Workflow for user asking "open X":**
1. `open -a "Google Chrome"` — launch if not running
2. `osascript -e 'tell application "Google Chrome" to open location "<URL>"'` — navigate
3. `osascript -e 'tell application "Google Chrome" to get name of front window'` — verify

## Open a new tab programmatically

Use `make new tab` when you need a specific URL opened in a known position:

```bash
# Add a new tab at the end of the front window
osascript -e 'tell application "Google Chrome"
    tell front window
        make new tab with properties {URL:"https://example.com"}
    end tell
end tell'
```

⚠️ **Pitfall:** If the user already has many tabs, the new tab can land at index N or N+1 depending on
whether Chrome was the active app. Always re-enumerate tabs after creation with
`get URL of every tab of every window` to find the actual index.

## Extract page content via JavaScript (scraping pattern)

**This is the most reliable way to scrape JavaScript-heavy sites** (Shopee, TikTok Shop, Lazada,
Sendo) when:
- `web_extract` / DuckDuckGo / Firecrawl fail
- `curl` returns empty HTML (SPA renders client-side)
- Official API requires auth tokens you don't have (Shopee returns `error_not_found` or
  `error 90309999` for missing cookies)

**The trick:** AppleScript can ask the active Chrome tab to run JavaScript and return the result.
Since the user is already logged into the site in their real Chrome, you get **real DOM content**
the way the user sees it, not guest/empty content.

```bash
# Get full page text (cleaned, no HTML tags)
osascript -e 'tell application "Google Chrome"
    tell tab N of front window
        execute javascript "document.body.innerText"
    end tell
end tell'
```

**N must be the actual tab index** (1-based) in `front window`. If unsure, enumerate first:

```bash
osascript -e 'tell application "Google Chrome"
    tell front window
        set output to ""
        repeat with j from 1 to (count of tabs)
            set output to output & "T" & j & ": " & (name of tab j) & linefeed
        end repeat
        return output
    end tell
end tell'
```

### Find tab by title (robust pattern)

```bash
# Activate the tab whose title contains "Shopee" and get its content
osascript -e 'tell application "Google Chrome"
    tell front window
        set cnt to count of tabs
        repeat with j from 1 to cnt
            if (name of tab j) contains "Goojodoq" then
                set active tab index to j
                return "FOUND_TAB=" & j
            end if
        end repeat
        return "NOT_FOUND count=" & cnt
    end tell
end tell'
```

**Combined workflow (verified 2026-06-17 with Shopee Goojodoq GD15 product):**

```bash
# Step 1: Open target URL in new tab
osascript -e 'tell application "Google Chrome" to open location "https://shopee.vn/product/SHOP_ID/ITEM_ID"'

# Step 2: Wait for page to load (JavaScript SPAs need 5-10s)
sleep 8

# Step 3: Find the new tab by title pattern and grab its content
SCRIPT='
tell application "Google Chrome"
    tell front window
        set targetTitle to "Goojodoq"
        set foundIdx to 0
        repeat with j from 1 to (count of tabs)
            if (name of tab j) contains targetTitle then
                set foundIdx to j
                exit repeat
            end if
        end repeat
        if foundIdx > 0 then
            set active tab index to foundIdx
            tell tab foundIdx
                return execute javascript "document.body.innerText"
            end tell
        else
            return "TAB_NOT_FOUND"
        end if
    end tell
end tell'
osascript -e "$SCRIPT"
```

### When to use this vs browser-harness

| Need | Use |
|------|-----|
| Just inspect tab URLs/titles | `chrome-tabs-applescript` (this skill) — fast, no daemon |
| Need screenshots / coordinate clicks / drag | `browser-harness` (CDP) |
| Need to extract text from a JS-rendered page the user is logged into | **`chrome-tabs-applescript` + `execute javascript`** — works without browser-harness daemon |
| Need to drive form inputs / multi-step flows | `browser-harness` |
| Need to scrape 10+ pages in batch | `browser-harness` (parallel) — osascript is single-threaded |

### Pitfalls for the `execute javascript` path

1. **Tab must have finished loading.** JavaScript SPAs (Shopee, TikTok Shop) need 5-10s after
   `open location`. If the result is short / looks like a loading skeleton, sleep longer and retry.
2. **Result size limit.** AppleScript strings cap at ~32KB in some cases. For long pages, extract
   in chunks:
   ```javascript
   document.body.innerText.substring(0, 10000)  // first 10K chars
   ```
3. **`innerText` vs `textContent`.** `innerText` respects visibility (skip hidden elements).
   `textContent` is faster but includes script/style text. Default to `innerText` for product
   pages.
4. **Active tab index in `front window` ≠ global tab count.** Tab indexing is per-window. A new
   tab created via `make new tab` goes into `front window` at index = (current count + 1), but
   `tab N of front window` will throw "Invalid index" if N exceeds the front window's count
   (e.g. you computed N across all windows).
5. **Returned text is escaped.** Quote/apostrophe are escaped; newlines are real `\n`. Decode
   in Python with `bytes(string, 'utf-8').decode('unicode_escape')` if needed.
6. **Permission prompt on first run.** First `execute javascript` call in a Chrome session may
   show a macOS "Chrome would like to control Google Chrome" dialog. User must accept. Once
   accepted, no more prompts.

## Cross-reference

For **acting** on Chrome (click, type, scroll) rather than just inspecting,
use `computer_use` tool via the `macos-computer-use` skill. For reading
tabs/windows, `osascript` is the right tool. For scraping JS-rendered pages
the user is logged into, use the `execute javascript` pattern above.

## Related
- [[macos-computer-use]] — Background macOS GUI control
- [[browser-harness]] — Browser control via CDP
