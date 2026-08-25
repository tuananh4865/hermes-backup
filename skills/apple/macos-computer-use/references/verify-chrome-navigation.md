---
title: Verify Chrome navigation via computer_use (not just browser tool return)
created: 2026-07-11
updated: 2026-07-11
type: reference
tags: [chrome, navigation, verification, browser-harness, computer-use, macos, ax-tree]
confidence: high
relationships: [browser-harness, macos-computer-use, computer-use, evidence-first-delivery]
---

# Verify Chrome navigation via computer_use

> **Context:** Session 2026-07-11 — agent called `browser_navigate https://www.youtube.com/@VuiVe` and got back `success: true` + 192 AX elements + "1.18M subscribers" channel data. Agent announced "vào kênh thành công". User pushed back twice: "thực sự là anh không thấy bất cứ browser nào ở youtube Vui Vẻ hiện tại cả" → "em chỉ mới nhập address bar thôi". Each agent claim was wrong because the agent trusted the tool return value, not the visible state of the user's Chrome.

## Why browser_harness fails silently

The `browser_navigate` / `browser_snapshot` / `browser_click` tools may silently fall back to a **Browserbase proxy** when local CDP attach fails. Tool returns:

- `success: true`
- `stealth_features: ["local"]` — "local" here means the proxy is in a local region, NOT the user's machine
- `stealth_warning: "Running WITHOUT residential proxies. Bot detection may be more aggressive."` — this is a HINT that proxy is in use
- Rich data (channel subscribers, comments, video info) — real, but from a different Chrome instance

The success response is REAL (Browserbase did navigate) — but it's a remote Chrome, not the user's local one. The user's Chrome stays untouched.

## The 3-wrong-claim cascade (2026-07-11 lesson)

What went wrong, in order:

| # | Agent claim | Why it was wrong | What would have caught it |
|---|---|---|---|
| 1 | "browser navigate thành công vào @VuiVe" | Tool return was proxy data, not user's Chrome | `computer_use capture app='Google Chrome'` would show user's actual window |
| 2 | "Chrome thật đã ở @VuiVe" (after computer_use type) | Agent had only typed into address bar — hadn't pressed Enter yet. 192 elements from `browser_snapshot` were stale playlist data, not channel page | Window title in `computer_use capture` was still "SON TUNG M-TP x TYGA" |
| 3 | "Chrome navigate sang @VuiVe rồi" (after capture) | Agent captured BetterDisplay app by accident instead of Chrome. Cross-app confusion from missing `app='Google Chrome'` on the initial capture | `window_title` would have shown "Google Chrome" prefix, not "BetterDisplay" |

Each claim was a self-deception cascade: trusted tool return → read AX tree selectively → ignored contradictory signals (window title, user's words, BetterDisplay capture noise).

## The protocol — verify every Chrome action with window_title

Before announcing ANY browser_* action to the user:

```python
# 1. Capture user's actual Chrome
capture = computer_use(action="capture", app="Google Chrome", seconds=3)

# 2. Check window_title — this is GROUND TRUTH
window_title = capture.window_title   # e.g. "(336) Justin Bieber - YouTube"

# 3. Compare against what browser_* tool reported
#    If they don't match → tool is proxying. Don't claim success.

# 4. Only THEN announce to the user
```

`window_title` is more reliable than:
- AX tree labels (can be empty for dynamically-rendered pages)
- Screenshot (useful but doesn't fit in chat unless delivered as PNG)
- `browser_snapshot` JSON output (may be proxy data)

## User escalation signatures (anh's specific phrases)

When anh is pushing back about a failed navigation, watch for these exact phrases — each is a demand to verify with `computer_use`:

| Phrase | What anh means |
|---|---|
| "có thấy vào đâu???" | "I'm asking if you ACTUALLY navigated — show me with a screenshot" |
| "em chỉ mới nhập address bar thôi" | "You're confusing typing with navigating. The visible state is the URL bar, not the loaded page" |
| "thực sự là anh không thấy..." | "I'm looking at my Chrome right now and the page is not what you claim" |
| "anh không thấy browser nào ở..." | "Your tool's view of the world doesn't match my Chrome's reality" |

When you see any of these, **stop claiming**, **acknowledge the gap**, and **re-capture Chrome**.

## Recipe: navigate user's Chrome to URL X (verified)

```python
# Step 1: capture current state
capture = computer_use(action="capture", app="Google Chrome")
# Note element index of address bar from response.elements
# (usually AXTextField with label "Address and search bar")

# Step 2: click address bar
computer_use(action="click", element=N)   # N = index from step 1

# Step 3: select all to overwrite any existing URL
computer_use(action="key", keys="cmd+a")

# Step 4: type URL
computer_use(action="type", text="https://www.youtube.com/@VuiVe")

# Step 5: press Enter to actually navigate
computer_use(action="key", keys="Return")

# Step 6: WAIT for page load (Chrome navigation needs 3-5s)
computer_use(action="wait", seconds=5)

# Step 7: VERIFY by re-capturing and checking window_title
verify = computer_use(action="capture", app="Google Chrome")
assert "Vui Vẻ" in verify.window_title, f"Navigation failed, got {verify.window_title}"

# Step 8: ONLY NOW announce success to user
```

Skipping step 6-8 produces self-deception claims like "Chrome đã navigate sang @VuiVe" before Chrome actually loaded the page.

## What if `computer_use` captures the wrong app?

If `computer_use capture` returns a tiny 1x1 capture with `app: "BetterDisplay"` or some other app, that means:

1. **You forgot to pass `app='Google Chrome'`** — the default is the current frontmost app. Re-capture with explicit app.
2. **Chrome is hidden behind another window** — cua-driver still drives it correctly, but the screenshot shows whatever window is on top. Use `window_title` to disambiguate.

If Chrome is on a different Space, you can still drive it — but capture will show the wrong Space's content. In that case, ask the user to bring Chrome to the foreground (or use `focus_app app="Google Chrome"`).

## How this differs from the existing "browser-harness vs real Chrome" section in SKILL.md

The SKILL.md section already covers the high-level distinction and tells you when to use `computer_use` vs `browser-harness`. This reference is the **operational protocol** — the exact step sequence + verify pattern + user-phrase recognition — that prevents the self-deception cascade documented above.

If you find yourself in the middle of a session and anh asks "có thấy vào đâu???" — come back to this file. Don't try to debug `browser_navigate`. Switch to `computer_use`, capture Chrome, check `window_title`, then act from there.