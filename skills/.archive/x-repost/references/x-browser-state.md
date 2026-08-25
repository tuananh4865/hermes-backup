# X/Browser State Verification Reference

## Problem
`browser_snapshot()` returns "(empty page)" on X.com — the accessibility tree fails to capture X's React-rendered content.

## Verified Solution: Screenshot + image_analyze

```bash
# 1. Capture screenshot via browser-harness
browser-harness <<'PY'
capture_screenshot("/tmp/x_state.png")
print(page_info()['url'])
PY

# 2. Analyze with vision
mcp_MiniMax_understand_image(image_source="/tmp/x_state.png", prompt="Mô tả chính xác những gì đang hiển thị trên màn hình")
```

## Key Findings from 2026-05-21 Session

| Check | Tool | Result |
|-------|------|--------|
| URL + auth state | `page_info()` | ✅ Works — returns url, title, auth state |
| Accessibility tree | `browser_snapshot()` | ❌ Returns "(empty page)" on X |
| DOM console | `browser_console(expression=...)` | ⚠️ Works for JS evaluation |
| Page navigation | `browser_navigate(url)` | ❌ Times out on x.com URLs |
| Page navigation | `goto_url(url)` via browser-harness | ❌ Times out on x.com URLs |

## Verified: X.com Login State

- Account: @TyayUno (Anh Trinh)
- browser-harness Chrome IS logged in
- Screenshot analysis confirms: "Anh Trinh @TyayUno" visible in sidebar

## Compose Modal State

- Compose modal visible in screenshots when open
- `click_at_xy(152, 753)` on Post button in left sidebar — does NOT open modal when called via browser-harness automation
- When modal IS open (from manual interaction): shows "What's happening?" placeholder + Post button
- Textarea selector: `[data-testid="tweetTextarea_0"]` (may not appear in accessibility tree)

## Caption Text (confirm fits in 300 words)
```
🚀 Google I/O 2026 — Gemini 3.5 Flash, Omni, Spark, Universal Cart, Smart Glasses, Antigravity 2.0

The Era of Agentic AI is HERE.

#GoogleIO #AI #Gemini #Tech
```
~35 words ✅ fits within 300-word limit

## Video File
- Path: `/tmp/google-io-2026-draft.mp4`
- Duration: 30s, Size: 2817KB, Codec: h264, Resolution: 1920x1080

## Session Log
- Session started: 2026-05-21 09:50 AM
- Key: X login works visually, automation click doesn't trigger compose modal