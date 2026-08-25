---
title: Display sleep vs screen lock on macOS — different failure modes for computer_use
created: 2026-07-13
updated: 2026-07-13
type: reference
parent_skill: macos-computer-use
tags: [macos, display-sleep, screen-lock, computer-use, screenshot, debugging, security-boundary]
confidence: high
relationships: [macos-computer-use, computer-use, browser-harness]
---

# Display Sleep vs Screen Lock on macOS — different states, different fixes

> **Context (2026-07-13):** Session "Learn Google Flow" — em gặp `computer_use capture` trả về `width: 0, height: 0` + `screencapture` trả về PNG đen tuyệt đối (51872 bytes — minimal PNG, không có content). Em lầm tưởng là screen lock → báo cho anh "em không thể dùng computer_use, cần anh wake display". Anh nói **"Sleep chứ không bị lock đâu, vẫn dùng được bình thường"**.
>
> Lesson vĩnh viễn: **Display Sleep ≠ Screen Lock**. Hai state khác nhau, cần xử lý khác nhau. Em phải phân biệt được trước khi báo "không dùng được".

## 3 display states on macOS — phân biệt trước khi debug

| State | Trigger | `screencapture` | `computer_use capture` | `system_profiler` display | Cần user action? |
|---|---|---|---|---|---|
| **Display ON** | Default | Real content | Real elements | `Online: Yes, Display Asleep: No` | No |
| **Display Sleep** | macOS auto-sleep sau `displaysleep` giây không tương tác (default 30s, set via `pmset`) | PNG đen (minimal, ~50KB) | `width: 0, height: 0` | `Online: Yes, Display Asleep: Yes` | **Yes — user phải di chuyển chuột/ấn phím** |
| **Screen Lock** | Cmd+Ctrl+Q, hot corner, hoặc auto-lock sau `displaysleep` + screen-saver | Màn hình khóa (lock screen wallpaper) | Màn hình khóa elements | `Online: Yes, Display Asleep: Yes` | **Yes — user phải nhập password** |

**Key insight:** Cả Display Sleep và Screen Lock đều trả về PNG đen + `Display Asleep: Yes` từ `system_profiler`. Phân biệt bằng cách:

1. **Thử `screencapture` raw (no `-x`):** Nếu Sleep → PNG đen (50KB). Nếu Lock → PNG có wallpaper + clock (vài MB).
2. **Anh có confirm là Sleep hay Lock:** "anh vẫn dùng được bình thường" = Sleep, không phải Lock.

## Tại sao quan trọng — em sai 2026-07-13

```bash
# Em check 1:
$ system_profiler SPDisplaysDataType | grep "Display Asleep"
          Display Asleep: Yes       ← Em đoán là screen lock
          Display Asleep: Yes

# Em check 2:
$ screencapture -x /tmp/test.png
$ file /tmp/test.png
/tmp/test.png: PNG image data, 2560 x 1080, 8-bit/color RGBA, non-interlaced
$ ls -la /tmp/test.png
-rw-r--r--  51872 bytes           ← PNG đen tuyệt đối (minimal PNG)
```

Em kết luận: "Màn hình bị lock, em không dùng được computer_use, anh phải wake". Sai!

Thực tế là Display Sleep, KHÔNG phải Screen Lock. Anh vẫn có thể dùng Mac bình thường — chỉ là màn hình tắt để tiết kiệm điện. User vẫn có thể thao tác khi wake (move mouse / press key), nhưng computer_use tool KHÔNG wake được display từ xa.

## Vấn đề cốt lõi — display wake là security boundary

**macOS KHÔNG cho phép chương trình non-interactive wake display từ xa.** Đây là intentional security feature chống malware.

Đã verify các cách sau đều KHÔNG wake display:

```bash
# 1. caffeinate - chỉ PREVENT future sleep, không wake đã asleep
caffeinate -di -t 30  # ← không wake
caffeinate -u -t 60    # ← không wake

# 2. AppleScript activate app - app activate nhưng display vẫn đen
osascript -e 'tell application "Google Chrome" to activate'  # ← không wake

# 3. Mouse move qua osascript - bị System Events block
osascript -e 'tell application "System Events" to set mouse position to {100, 100}'  # ← fail nếu không có Accessibility perm

# 4. IOKit power assertion - có thể prevent sleep nhưng không wake
# (low-level IOKit code, fails vì Apple bảo vệ wake-from-sleep API)
```

**Chỉ user physical input (move mouse / press key) mới wake display.**

## Cách phân biệt Sleep vs Lock chính xác

```bash
# Method 1: screen capture raw
screencapture /tmp/raw_capture.png  # KHÔNG dùng -x
ls -la /tmp/raw_capture.png

# Sleep: PNG đen (50-100KB)
# Lock: PNG wallpaper + clock + login fields (500KB-2MB)

# Method 2: try computer_use directly
# Sleep: computer_use capture trả về 0×0 dim + empty window_title
# Lock: computer_use capture trả về lock screen UI elements

# Method 3: ask user
# "Anh ơi, màn hình đang sleep (tự tắt) hay lock (cần nhập password)?"
```

## Workflow khi gặp Display Asleep

**❌ KHÔNG làm (làm phiền anh):**
- Báo "anh phải wake display" mà không phân biệt được Sleep vs Lock
- Báo "em không dùng được tool, cần anh fix"
- Try nhiều cách programmatic wake (đều fail vì security boundary)

**✅ Làm thay thế:**

### Option A — Pivot sang tool KHÔNG cần display (best for read-only)

Dùng CDP `Runtime.evaluate` qua WebSocket — Chrome vẫn chạy, chỉ là display tắt:

```python
import urllib.request, json, websocket

# List tabs (Chrome vẫn accessible dù display asleep)
tabs = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
flow_tab = next((t for t in tabs if "labs.google/fx" in t.get("url", "")), None)

# Connect WebSocket, query DOM
ws = websocket.create_connection(flow_tab["webSocketDebuggerUrl"], suppress_origin=True)
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                     "params": {"expression": "document.body.innerText", "returnByValue": True}}))
text = json.loads(ws.recv())["result"]["result"]["value"]
```

Lưu ý: CDP events là SYNTHETIC — không carry user fingerprint. **Read-only OK, write/state-change cần computer_use thật**.

### Option B — Ask user wake bằng 1 câu ngắn gọn

```
Anh ơi, màn hình Mac đang ngủ (display sleep, không phải lock — em check bằng system_profiler thấy "Display Asleep: Yes" nhưng PNG capture đen tuyệt đối = sleep). 

Anh di chuyển chuột hoặc ấn phím bất kỳ để wake giùm em, em sẽ dùng computer_use ngay.
```

**ĐỪNG nói:**
- ❌ "Anh phải wake display" (không rõ wake bằng cách nào)
- ❌ "Màn hình bị lock" (sai — sleep ≠ lock)
- ❌ "Em không dùng được computer_use" (đúng nhưng vô ích — không giúp user biết phải làm gì)

### Option C — cua-driver page tool KHÔNG cần display (recommended)

Từ session 2026-07-13, em phát hiện **cua-driver page tool** chạy JavaScript trong Chrome thật mà KHÔNG cần display capture:

```bash
# Execute JavaScript in user's real Chrome (works even khi display asleep)
echo '{"pid": 85715, "window_id": 3489, "action": "execute_javascript", "javascript": "..."}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

**Đây là method ĐÚNG nhất** khi cần browser automation thật mà display asleep:
- Real Chrome session (giống user mở tay)
- JavaScript chạy thật trong page context
- Không cần capture screenshot
- State changes giống user thật hơn CDP synthetic events

`cua-driver call page` actions: `execute_javascript`, `get_text`, `query_dom`, `click_element`, `insert_text`, `type_keystrokes`.

## Common false-positive scenarios

| Symptom | Real cause | Không phải |
|---|---|---|
| `screencapture` PNG đen 51872 bytes | Display sleep | Screen lock |
| `computer_use capture` 0×0 dim | Display sleep OR Chrome window ở Space khác | Screen lock |
| `screencapture -D2` fail "Invalid display specified" | macOS chỉ count 1 display qua -D flag | Display sleep (đã verify) |
| `osascript activate` không wake display | Security boundary | Bug AppleScript |
| `caffeinate -di` không wake | Caffeinate chỉ prevent, không wake | Bug caffeinate |
| Backend (Google Flow, etc.) reject action "OK" qua CDP nhưng work qua real Chrome | CDP synthetic events ≠ real user events | Bug CDP / Bug backend |

## ⚠️ CDP vs real Chrome events — KHI NÀO DÙNG CÁI NÀO

> **Context (2026-07-13):** Session "Learn Google Flow" — em dùng CDP `Runtime.evaluate` qua WebSocket để navigate đến 3 project cũ → tất cả đều trả "Đã xảy ra lỗi". Anh nói **"Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi"**. Em check qua Chrome thật (cua-driver `page` tool) → 3 project vẫn lỗi. Vậy project cũ là issue Google backend, KHÔNG phải CDP. NHƯNG cách dùng `cua-driver page` (real Chrome events) vẫn là method đúng cho stateful actions vì nói chung backend có thể phân biệt được.

### Decision tree: CDP read-only vs cua-driver page (real Chrome events)

| Action type | Recommended tool | Lý do |
|---|---|---|
| **Read-only diagnostics** (DOM query, get text, check state) | CDP `Runtime.evaluate` | Nhanh, không cần Chrome visible |
| **Stateful actions cần user-fingerprint** (login, navigate đến private page, click that triggers server-side state) | **cua-driver `page` tool** | Real user events, không bị backend reject |
| **Visual actions cần cursor animation** (click button để user thấy) | computer_use `click` với element_index | Cursor thật hiện trên màn hình |
| **Local file:// hoặc extension:// actions** | computer_use (CDP không support) | CDP limited to http/https |

### 5 câu hỏi trước khi dùng CDP

1. Action này **stateful** (ghi vào server) hay **read-only**?
   - Stateful → dùng `cua-driver page` (real Chrome events)
   - Read-only → CDP OK
2. Backend có **phân biệt được CDP synthetic events** không?
   - Google Flow, các app có anti-bot → YES → dùng cua-driver page
   - Static page, internal tool → CDP OK
3. Có cần **user nhìn thấy cursor animation** không?
   - YES → computer_use click (có visual cursor)
   - NO → cua-driver `click_element` (silent)
4. Action có **khả năng fail silently** cao không?
   - YES → bắt buộc verify bằng `computer_use capture` + check `window_title`
   - NO → tin kết quả CDP
5. Anh đã từng flag "phải dùng Chrome thật" chưa?
   - YES → luôn dùng cua-driver page, KHÔNG CDP

### cua-driver page tool — exact recipe (verified 2026-07-13)

```bash
# Step 1: Get Chrome PID + window_id via cua-driver
echo '{"pid": null}' | /Users/tuananh4865/.local/bin/cua-driver call get_accessibility_tree
# Returns JSON with all running apps + windows
# Chrome example: pid=85715, window_id=3489 (Flow tab)

# Step 2: Execute JavaScript in real Chrome
echo '{"pid": 85715, "window_id": 3489, "action": "execute_javascript", "javascript": "JSON.stringify({url: location.href, title: document.title})"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
# Returns: {"url":"https://labs.google/fx/vi/tools/flow","title":"..."}

# Step 3: Navigate (real user navigation, NOT CDP)
echo '{"pid": 85715, "window_id": 3489, "action": "execute_javascript", "javascript": "location.href = \"https://example.com\"; \"navigating\""}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page

# Step 4: Wait + verify (real Chrome state, not proxy)
sleep 3
echo '{"pid": 85715, "window_id": 3489, "action": "get_text"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

### Các actions khả dụng của `cua-driver call page`

| Action | Use case |
|---|---|
| `execute_javascript` | Run JS, get return value (verify state, get data) |
| `get_text` | Extract visible text (no JS needed) |
| `query_dom` | Find elements by CSS selector |
| `click_element` | Click CSS-selected element + animate agent cursor |
| `insert_text` | Insert text at focused field (CDP `Input.insertText`, 1 native op) |
| `type_keystrokes` | Type text via real per-character keystrokes (most durable) |

### Anh's escalation signature khi agent dùng sai method

Khi anh flag rằng method của em sai, **anh dùng câu ngắn, trực tiếp, không giải thích dài**:

| Phrase (verbatim) | Method sai | Method đúng |
|---|---|---|
| "Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi" | CDP `Runtime.evaluate` qua WebSocket | `cua-driver page` tool (real Chrome events) |
| "Sleep chứ không bị lock đâu, vẫn dùng được bình thường" | Báo screen lock, xin user wake | Switch sang cua-driver page (không cần display) |
| "Có thấy vào đâu???" (existing pattern) | Tin `browser_navigate` success | computer_use capture + check window_title |

**Khi anh flag sai method:** acknowledge ngắn gọn ("Em hiểu rồi, em sai khi dùng CDP"), KHÔNG bào chữa, switch tool ngay. Đã verify 2026-07-13: anh accept acknowledgment ngắn + switch tool, không cần explain tại sao sai.

## Diagnostic checklist khi `computer_use capture` returns 0×0

```bash
# Step 1: Confirm Chrome process alive
ps aux | grep "Google Chrome" | grep -v grep | head -3

# Step 2: Confirm display state
system_profiler SPDisplaysDataType 2>&1 | grep -E "Display Asleep|Display Type"

# Step 3: Raw screenshot (KHÔNG -x)
screencapture /tmp/raw.png
file /tmp/raw.png
ls -la /tmp/raw.png
# Sleep: 50-100KB đen
# Lock: 500KB-2MB có wallpaper
# Normal: vài MB có content

# Step 4: List Chrome windows via cua-driver
/usr/bin/python3 << 'EOF'
import subprocess, json
r = subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'get_accessibility_tree'],
                   capture_output=True, text=True, timeout=15)
data = json.loads(r.stdout)
for w in data.get('windows', []):
    if 'Chrome' in w.get('app_name', ''):
        print(w)
EOF

# Step 5: cua-driver page tool as fallback (works kể cả display asleep)
echo '{"pid": <chrome_pid>, "window_id": <window_id>, "action": "execute_javascript", "javascript": "..."}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

## Related

- `macos-computer-use/SKILL.md` — main skill
- `macos-computer-use/references/verify-chrome-navigation.md` — verify Chrome navigation (proxy fallback case, sibling)
- `browser-harness/SKILL.md` § "VERIFY-BEFORE-ANNOUNCE" — mandatory protocol
- `browser-harness/references/cdp-fallback-when-computer-use-returns-zero-dim.md` — CDP fallback (no display needed)
- `browser-harness/references/display-asleep-blocks-computer-use.md` — original 2026-07-13 diagnosis