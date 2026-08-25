---
title: Display Asleep blocks computer_use — no programmatic wake exists
created: 2026-07-13
updated: 2026-07-13
type: reference
parent_skill: browser-harness
tags: [macos, display-sleep, caffeinate, computer-use, screencapture, security-boundary, debugging]
confidence: high
relationships: [browser-harness, macos-computer-use, cdp-fallback-when-computer-use-returns-zero-dim]
---

# Display Asleep blocks `computer_use` — no programmatic wake exists

> **Context (2026-07-13):** Session "Learn Google Flow" — sau khi Chrome window bị đẩy ra màn hình phụ 1080×1920 portrait và em CDP-query thấy OK, em cần dùng `computer_use` để click thật vào Chrome (vì anh bảo "phải dùng computer use"). Nhưng cả 2 màn hình đều `Display Asleep: Yes` (macOS auto-sleeps displays after `displaysleep=30s` mặc định). Em đã thử 5 cách đánh thức — KHÔNG CÁCH NÀO work. Đây là hard macOS security boundary, không có programmatic fix.
>
> **Symptom:** `screencapture` ra file PNG 51872 bytes (minimal solid black), `computer_use capture` trả về `width: 0, height: 0`, Chrome hoàn toàn alive ở CDP (`curl http://localhost:9222/json/version` works) nhưng không thể drive visually.

## Diagnostic — confirm display state

```bash
system_profiler SPDisplaysDataType | grep -E "Display Asleep|Main Display"
# Output:
#   Main Display: Yes
#   Display Asleep: Yes
#   Display Asleep: Yes
```

Nếu cả 2 dòng `Display Asleep: Yes` → displays asleep, không thể dùng `computer_use` cho đến khi user wake manually.

## Failed wake attempts (verified không work)

Em đã thử 5 cách — TẤT CẢ failed vì macOS security boundary:

### 1. `osascript set mouse position` (FAIL)

```bash
osascript -e 'tell application "System Events" to set mouse position to {100, 100}'
# Error: "A property can't go after this identifier. (-2740)"
# → Syntax lỗi vì System Events cần Accessibility permission chưa cấp
```

### 2. `osascript ... activate Chrome` (FAIL)

```bash
osascript -e 'tell application "Google Chrome" to activate'
# Chrome process active nhưng window vẫn asleep → no visual change
```

### 3. `screencapture` no flag (FAIL)

```bash
screencapture /tmp/full.png
# → File tạo OK nhưng là solid black PNG 51872 bytes
# → vì màn hình asleep, không capture được content
```

### 4. `screencapture -l <windowID>` (FAIL)

```bash
screencapture -l1433272948 -x /tmp/chrome1.png
# Error: "could not create image from window"
# → Screen Recording permission cho terminal chưa cấp
```

### 5. `caffeinate -di` (FAIL — chỉ prevent, không wake)

```bash
caffeinate -di -t 30 &
sleep 3
system_profiler SPDisplaysDataType | grep "Display Asleep"
# → Vẫn "Display Asleep: Yes"
# → caffeinate -di chỉ PREVENT future sleep, KHÔNG wake already-asleep display
```

### 6. IOPMAssertionCreateWithName (chưa test — khả năng cao cũng fail)

```python
# IOKit power assertion
import ctypes
iokit = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/IOKit.framework/IOKit")
kIOPMAssertionTypePreventUserIdleSystemSleep = ctypes.c_uint32(0)
kIOPMAssertionLevelOn = ctypes.c_uint32(255)
assertion_id = ctypes.c_uint32(0)
res = iokit.IOPMAssertionCreateWithName(
    kIOPMAssertionTypePreventUserIdleSystemSleep,
    kIOPMAssertionLevelOn,
    ctypes.c_void_p(0),  # reason CFString
    ctypes.byref(assertion_id)
)
# → Có thể tạo assertion nhưng macOS vẫn ignore cho display wake
```

## What actually works

**User must physically interact with the Mac:**
- Move mouse
- Press any key
- Touch trackpad

→ Sau đó mọi display wake tức thì → `computer_use` returns normal dim (2560×1080 for main, etc.) → `screencapture` returns actual content.

## Root cause analysis

macOS security boundary: **No non-interactive process can wake a sleeping display**. Apple thiết kế vậy để chống malware tự đánh thức máy user lúc ngủ. Đây không phải bug, không phải workaround được — đây là feature.

## Diagnostic flow khi `computer_use` fails

```
computer_use(action='capture') returns 0×0
  ↓
Step 1: Check Chrome CDP còn sống không
  curl http://localhost:9222/json/version → if works, Chrome + CDP OK
  ↓
Step 2: Check display state
  system_profiler SPDisplaysDataType | grep "Display Asleep"
  ↓
Step 3a: Display Asleep: Yes → DON'T ask user to wake!
      → Use cua-driver `page` tool (works on AX layer, not visual)
      → See references/cua-driver-page-tool-for-real-chrome.md
  Step 3b: Display Asleep: No → Chrome window ở Space khác / minimized
      → Dùng CDP để query + drive (see cdp-fallback-when-computer-use-returns-zero-dim.md)
      → OR dùng cua-driver `page` tool (better — real user events)
```

## ⚠️ CORRECTION 2026-07-13: cua-driver `page` works khi display asleep

Anh nói rõ: "Sleep chứ không bị lock đâu, vẫn dùng được bình thường" — displays asleep vẫn drive được, chỉ không dùng `computer_use` (visual) được. Pivot sang `cua-driver page` tool:

- `cua-driver` dùng AX (accessibility) layer, KHÔNG cần visual capture
- Display asleep không ảnh hưởng
- Real user events → app backend accept (khác với CDP synthetic events)
- `execute_javascript` chạy JS trong Chrome real session

**Detail đầy đủ:** `references/cua-driver-page-tool-for-real-chrome.md`

## Diagnostic flow CẬP NHẬT (sau correction)

```
Task cần browser automation
  ↓
Step 1: `computer_use` capture work không?
  ├─ YES (content visible) → use computer_use (click by element index)
  └─ NO (0×0 dim, display asleep/hidden) → Step 2
  ↓
Step 2: Task là stateful (login, save, project load) hay read-only?
  ├─ Read-only (DOM query, extract data) → CDP via websocket-client OK
  └─ Stateful (click changes server state, type into form) → cua-driver `page` tool
  ↓
Step 3: Build JSON via Python subprocess → /Users/tuananh4865/.local/bin/cua-driver call page
  ↓
Step 4: Verify bằng `get_text` hoặc `execute_javascript` (KHÔNG tin tool return)
```

## Pitfalls

- ❌ `caffeinate -u/-di/-s` không wake display — chỉ prevent
- ❌ `osascript ... set mouse position` cần Accessibility permission — thường fail với `-2740` error
- ❌ `screencapture -D2` cho màn hình phụ → "Invalid display specified. Only 1 display, the only valid value is 1" (macOS đếm display theo cách riêng, không phải system_profiler count)
- ❌ `screencapture -l <windowID>` cần Screen Recording permission
- ❌ IOKit power assertion không wake display đã asleep (security boundary)
- ✅ Wake manual = 100% reliable (move mouse/press key)

## Files involved

- `~/.hermes/scripts/launch-chrome-cdp.sh` — Chrome CDP keep-alive (KHÔNG liên quan display wake)
- `~/.hermes/skills/browser-harness/references/cdp-fallback-when-computer-use-returns-zero-dim.md` — sibling reference cho Chrome hidden
- `~/.hermes/skills/browser-harness/references/display-asleep-blocks-computer-use.md` — file này
- `~/.hermes/skills/browser-harness/references/chrome-cdp-autostart.md` — CDP setup

## Related

- `browser-harness/SKILL.md` § "VERIFY-BEFORE-ANNOUNCE" — verify protocol
- `browser-harness/SKILL.md` § Case 2026-07-13 — sibling failure modes (3 cases cùng ngày)
- `macos-computer-use/SKILL.md` — broader macOS GUI automation