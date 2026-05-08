---
name: chrome-tabs-applescript
title: Chrome Tabs via AppleScript
description: Get Chrome window and tab info on macOS using osascript — fast and reliable
created: 2026-05-02
updated: 2026-05-02
type: skill
tags: [terminal, macos, chrome]
confidence: high
relationships: [browser-harness]
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

## Related
- [[browser-harness]] — Browser control via CDP
