# Chrome AppleScript Quick Reference

Verified commands working as of 2026-05-14 on macOS with Google Chrome.

## Window + Tab Queries

```bash
# Front window name
osascript -e 'tell application "Google Chrome" to get name of front window'

# All tab names (front window only)
osascript -e 'tell application "Google Chrome" to get name of every tab of front window'

# All tab URLs (front window only)
osascript -e 'tell application "Google Chrome" to get URL of every tab of front window'

# All tabs ALL windows
osascript -e 'tell application "Google Chrome" to get URL of every tab of every window'
```

## Tab-by-Index (front window)

```bash
# Get URL of tab N (1-based index)
osascript -e 'tell application "Google Chrome" to get URL of tab 5 of front window'

# Get name of tab N
osascript -e 'tell application "Google Chrome" to get name of tab 5 of front window'
```

**Note:** `tab N` is 1-based. Tab 1 = leftmost. Tab numbering resets per window — each window has its own tab 1, tab 2, etc.

## NOT WORKING (pitfalls confirmed 2026-05-14)

```bash
# ❌ title of active tab — returns front window name, NOT active tab title
osascript -e 'tell application "Google Chrome" to get title of active tab of front window'
# → "(21) Home / X" (the window name, not the active tab)

# ✅ Use tab number instead — more reliable
osascript -e 'tell application "Google Chrome" to get name of tab 1 of front window'
```

## Chrome Windows in This Session (2026-05-14)

Front window tabs (z_index 16, on current space):
1. "(21) Home / X" — x.com/home
2. "Hermes-Automation - Google Drive" — drive.google.com
3. "tiktok-affiliates - Google Trang tính" — docs.google.com/spreadsheets
4. "Hiểu âm thanh | Gemma | Google AI" — ai.google.dev/gemma
5. "TikTok Shop Seller Center | Vietnam" — seller-vn.tiktok.com

Other windows: Google Chrome window (z_index 15, different space)