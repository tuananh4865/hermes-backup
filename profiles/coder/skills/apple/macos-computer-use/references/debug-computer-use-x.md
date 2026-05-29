# computer_use Debugging Reference
**Session:** 2026-05-14 | **Context:** Testing computer_use on X.com (logged-in Chrome)

## Key Findings

### 1. `screenshot` tool vs `get_window_state` — different window ID systems

`cua-driver screenshot` uses the OLD integer `window_id` system. `cua-driver get_window_state` uses the NEW MCP structured window objects (pid + window_id).

- `list_windows` with MCP returns structured content with `window_id` in the new format
- `screenshot` tool cannot find windows using these IDs → "no shareable window with id XXXX"
- `get_window_state` (used by `computer_use` capture in SOM/AX mode) correctly handles the new format

**Workaround:** Never use `screenshot` tool directly for Chrome. Use `computer_use(action="capture", mode="som", app="Google Chrome")` instead.

### 2. Chrome window hierarchy — multiple windows, same process

```
Chrome PID 31837:
  window_id=7044 → z_index=17 → (21) Home / X [FRONTMOST — what user sees]
  window_id=7048 → z_index=16 → (248) BẤT QUÁ NHÂN GIAN - CHU THÚY QUỲNH
```

`list_windows` output (sorted by z_index, lowest = frontmost on macOS):
```
31837 7044 Google Chrome (21) Home / X z=17
31837 7048 Google Chrome (248) BẤT QUÁ NHÂN GIAN - ... z=16
10794 9241 Claude Claude z=15
```

When doing `capture(app="Google Chrome")` with no specific window_id, the backend picks the FIRST on-screen window (z_index lowest = frontmost).

### 3. SOM capture returns 673 elements for Chrome — AX tree is rich but labels empty

`computer_use(action="capture", mode="som", app="Google Chrome")` returns:
- Full screenshot (PNG via MCP images[])
- 673 interactable elements (AX tree)
- Element indices are 1-based (#0 = AXWindow, #1 = AXGroup, etc.)

**BUT element labels are often EMPTY (`''`)** because Chrome renders content dynamically via WebArea. The SOM overlay on the screenshot is what you actually use for clicking.

### 4. `osascript` + computer_use scroll combo — reliable X workflow

```bash
# Inspect first
osascript -e 'tell application "Google Chrome" to get URL of active tab of front window'

# Use osascript keystroke to scroll (Cmd+ArrowDown = timeline scroll on X)
osascript -e 'tell application "System Events" to keystroke key code 125 using {command down}'

# Then verify with computer_use capture
```

**Why not `computer_use(action="scroll", direction="down", amount=5)`?**
- Scroll on a web page may scroll the wrong container
- `keystroke key code 125` = ArrowDown, Cmd+ArrowDown = scroll down on X timeline
- This is more reliable for social media feeds

### 5. Bounds are (0,0,0,0) for all elements — SOM screenshot required

All AX tree elements from `get_window_state` show `bounds=(0,0,0,0)` — the accessibility tree doesn't have real coordinates. The SOM overlay on the PNG screenshot is what provides click targets.

For X/Twitter: element index clicks are NOT reliable for navigating to specific posts. Use the SOM screenshot to find visual targets, then click by coordinate or by finding the right element in the screenshot.

### 6. `drag` action is blocked by backend

`computer_use(action="drag", ...)` returns:
```
{"ok": false, "action": "drag", "message": "drag is not supported by the cua-driver backend."}
```

This is a backend limitation, not a schema issue. The schema includes drag but the cua-driver MCP server doesn't implement it.

## Status at end of session

| Component | Status |
|-----------|--------|
| `hermes tools enable computer_use` | ✅ Works |
| cua-driver binary | ✅ 0.1.5 installed |
| TCC permissions | ✅ Accessibility + Screen Recording |
| capture(mode='som') | ✅ 673 elements, PNG image |
| capture(mode='ax') | ✅ AX tree only |
| list_apps | ✅ Works |
| click (guard) | ✅ blocks without element/coordinate |
| screenshot tool | ❌ Cannot find windows (wrong ID scheme) |
| drag | ❌ Not supported by backend |
| X.com in real Chrome | ✅ User is logged in at window_id 7044 |
| scroll via osascript | ✅ Cmd+ArrowDown works for X timeline |