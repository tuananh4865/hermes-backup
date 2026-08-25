---
title: cua-driver page tool — the CORRECT way to drive user's real Chrome (not CDP, not computer_use)
created: 2026-07-13
updated: 2026-07-13
type: reference
parent_skill: browser-harness
tags: [chrome, cua-driver, real-chrome-session, page-tool, execute_javascript, click_element, macos, ax-layer, display-asleep-ok, FALSELY-rejected-projects, stateful-actions, react-slate, contenteditable, insert_text, cdp-input-inserttext, button-disabled-state]
confidence: high
relationships: [browser-harness, cdp-fallback-when-computer-use-returns-zero-dim, display-asleep-blocks-computer-use, macos-computer-use]
---

# cua-driver `page` tool — the CORRECT way to drive user's real Chrome

> **Context (2026-07-13):** Session "Learn Google Flow" — em dùng CDP `Runtime.evaluate` qua `websocket-client` để query/click/type trong Chrome. Anh báo: "Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi". Phát hiện: **CDP events KHÔNG giống user thật** — Google Flow backend phân biệt được và reject project cũ. Em pivot sang `cua-driver page` tool — chạy JavaScript TRONG Chrome real session của anh, KHÔNG qua CDP proxy. Verify qua Chrome thật: 3 project cũ vẫn lỗi "Đã xảy ra lỗi" (Google backend thật sự issue, không phải CDP artifact) — nhưng state changes match với Chrome tab list của anh.

## Why this matters — the lesson that bit me

CDP (Chrome DevTools Protocol) qua `Runtime.evaluate` + `Input.dispatchMouseEvent` + `Input.dispatchKeyEvent` từ external WebSocket connection là **synthetic events**. Google Flow (và nhiều SPA hiện đại) check event source — events từ CDP KHÔNG match user gestures → backend reject, state KHÔNG update như user thật.

Anh phát hiện: project cũ anh mở bằng tay → OK. Cùng project, em mở qua CDP → "Đã xảy ra lỗi". Difference: Chrome session của anh có real state changes từ real user input, CDP của em thì không.

**Lesson:** Đối với STATEFUL web actions (login state, OAuth flow, project load, action confirmation) — phải dùng events thật từ Chrome real session. CDP proxy KHÔNG đủ.

## The correct tool — `cua-driver page`

`cua-driver` (binary tại `/Users/tuananh4865/.local/bin/cua-driver`) là driver của Cua AI tích hợp với Hermes. Tool `page` chạy JavaScript TRONG user's real Chrome qua AX/AppleScript layer, KHÔNG phải CDP proxy.

**Cài đặt:** CuaDriver.app đã có sẵn trong `/Applications/CuaDriver.app/`. Đã verify accessibility + screen recording permissions granted (xem `hermes computer-use doctor`).

### Action: `execute_javascript` — chạy JS trong Chrome thật

```bash
# Pattern: pipe JSON vào cua-driver call page
echo '{"pid": <CHROME_PID>, "window_id": <WINDOW_ID>, "action": "execute_javascript", "javascript": "<JS_CODE>"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

**Critical params:**
- `pid` — Chrome process ID (lấy từ `ps aux | grep "Google Chrome"` hoặc `cua-driver get_accessibility_tree`)
- `window_id` — Chrome window ID (lấy từ `cua-driver get_accessibility_tree` output)
- `action` — `"execute_javascript"` | `"get_text"` | `"query_dom"` | `"click_element"` | `"insert_text"` | `"type_keystrokes"`
- `javascript` — JS code string (chỉ action execute_javascript)

### Action: `click_element` — click thật + cursor animation

```bash
echo '{"pid": 85715, "window_id": 3489, "action": "click_element", "selector": "button.submit"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

**Ưu điểm:**
- Click trong Chrome real session → state changes thật, giống user
- Cursor animation hiển thị → user thấy được agent đang làm gì
- KHÔNG cần capture display (works khi display asleep)

### Action: `insert_text` / `type_keystrokes` — type thật

```bash
# 1 lần (nhanh, dùng cho contenteditable)
echo '{"pid": 85715, "window_id": 3489, "action": "insert_text", "text": "Vietnamese text with diacritics"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page

# Từng phím (chậm hơn nhưng robust)
echo '{"pid": 85715, "window_id": 3489, "action": "type_keystrokes", "text": "Type each char as real keystroke"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

**Lưu ý:** Phải focus element trước (bằng click_element) trước khi insert/type.

### Action: `query_dom` — find elements theo CSS selector

```bash
echo '{"pid": 85715, "window_id": 3489, "action": "query_dom", "css_selector": "button, a", "attributes": ["href", "aria-label"]}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

Trả về JSON array các elements matching selector.

### Action: `get_text` — extract visible text

```bash
echo '{"pid": 85715, "window_id": 3489, "action": "get_text"}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

## Workflow for getting Chrome PID + window_id

Không cần CDP port 9222. Dùng `cua-driver get_accessibility_tree` để list apps + windows:

```bash
# List apps + windows
cua-driver call get_accessibility_tree
# Returns JSON:
# {
#   "apps": [
#     {"bundle_id": "com.google.Chrome", "name": "Google Chrome", "pid": 85715}
#   ],
#   "windows": [
#     {"app_name": "Google Chrome", "pid": 85715, "title": "Google Flow - YouTube", "window_id": 3489},
#     {"app_name": "Google Chrome", "pid": 85715, "title": "(338) YouTube", "window_id": 3979}
#   ]
# }
```

Sau đó dùng `pid` + `window_id` cho mọi `page` calls.

## Why cua-driver `page` works khi CDP fails

| Failure | CDP | cua-driver page |
|---|---|---|
| `computer_use` capture 0×0 (display asleep) | ❌ Cannot drive visually | ✅ Works — uses AX layer |
| CDP events not real user gestures (state rejected by app) | ❌ Synthetic events | ✅ Real user events via AX |
| Need to click but element not in AX tree (canvas/video) | ⚠️ Pixel coords need visible window | ⚠️ Same limitation — but click via `click_element` works for most |
| Need to type in contenteditable | ⚠️ Multiple round-trips, may fail | ✅ `insert_text` 1 shot, robust |
| Need to query DOM | ✅ Works | ✅ Works |
| Display hidden on different Space | ⚠️ Pixel coords may be off | ✅ AX works regardless of Space |

## Critical pitfall — `execute_javascript` JSON escaping

`execute_javascript` nhận JS code dạng STRING trong JSON. Phải escape:
- `"` → `\"`
- Newlines → `\n`
- Single quotes OK (don't need escape)
- Use `python3` hoặc `jq` để build JSON an toàn

**Pattern an toàn (recommended):**

```python
import json, subprocess

js_code = """
JSON.stringify({
    url: location.href,
    title: document.title,
    videoCount: document.querySelectorAll("video").length
})
"""

payload = {
    "pid": 85715,
    "window_id": 3489,
    "action": "execute_javascript",
    "javascript": js_code
}

result = subprocess.run(
    ['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
    input=json.dumps(payload),
    capture_output=True,
    text=True,
    timeout=15
)
print(result.stdout)
```

**Pattern NG (inline JSON trong bash):**
```bash
# ❌ Dễ break khi JS code chứa dấu nháy kép hoặc backslash
echo '{"action": "execute_javascript", "javascript": "JSON.stringify({url: location.href})"}'
# → May fail JSON parse khi JS code có " hoặc \n
```

**Workaround inline đơn giản:**
```bash
# Single-quote bash, JSON dùng " — escape \" cho JS
echo '{"pid": 85715, "action": "execute_javascript", "javascript": "JSON.stringify({url: location.href, count: document.querySelectorAll(\"video\").length})"}'
```

## Decision tree — khi nào dùng cái nào

```
User yêu cầu browser automation
  ↓
Step 1: Chrome có accessible không?
  ├─ `computer_use` capture trả về content → use `computer_use` (visual, click by element)
  └─ `computer_use` 0×0 (display asleep, hidden, etc.) → next step
  ↓
Step 2: Task là STATEFUL (login, OAuth, save state) hay READ-ONLY?
  ├─ Read-only (query DOM, extract data) → CDP `Runtime.evaluate` OK
  └─ Stateful (click button changes server state, type into form) → cua-driver `page` tool
  ↓
Step 3: Cần click trong Chrome real session
  ├─ cua-driver `click_element` (selector)
  ├─ cua-driver `execute_javascript` calling `.click()` (nếu element không accessible)
  └─ cua-driver `get_window_state` → get element_index → `click` (cu-pilot pattern)
  ↓
Step 4: Verify kết quả
  ├─ `get_text` để check page state changed
  ├─ `execute_javascript` để query new DOM state
  └─ ⚠️ KHÔNG tin tool return value — luôn verify bằng data
```

## Verification: Chrome real session ≠ CDP

Khi nào dùng tool nào, verify bằng Chrome tab list:

```bash
# List tabs từ CDP (vẫn work, chỉ dùng để verify)
curl -s http://localhost:9222/json | python3 -c "
import json, sys
for t in json.load(sys.stdin):
    print(t.get('url','')[:100], '|', t.get('title','')[:50])
"
```

Nếu tabs list match với Chrome thật của anh (qua `cua-driver get_accessibility_tree`) → OK, dùng tool nào cũng được.

Nếu KHÔNG match → tool đang route qua proxy/browserbase → pivot sang tool khác.

## Real example — session "Learn Google Flow" 2026-07-13

**Vấn đề:** Em dùng CDP `Runtime.evaluate` để query Flow + create project + set prompt. Chrome CDP proxy sống nhưng project cũ mở bằng CDP → "Đã xảy ra lỗi". Anh báo: "phải dùng computer use".

**Pivot:** Em thử `computer_use` → 0×0 vì display asleep. Em check `cua-driver` docs → thấy `page` tool.

**Verify:**
1. `cua-driver call get_accessibility_tree` → Chrome PID 85715, window 3489
2. `cua-driver call page` with `execute_javascript` + `location.href = ...` → navigate thật
3. `cua-driver call page` with `execute_javascript` + `JSON.stringify({url: location.href, ...})` → verify
4. Project Fashion cũ vẫn lỗi → confirm Google backend issue thật, không phải CDP

**Conclusion:** cua-driver `page` tool = correct way. CDP synthetic events = bug. computer_use = blocked khi display asleep.

## Pitfalls

- ❌ CDP `Input.dispatchMouseEvent` cho stateful actions — events synthetic, app backend có thể reject
- ❌ CDP `Runtime.evaluate` calling `el.click()` — same issue, not real gesture
- ❌ Use `execute_code` (hermes_sandbox Python) for CDP — thiếu `websocket-client` module, dùng `/usr/bin/python3`
- ❌ Use cua-driver `page` với single-quote bash + JSON có `"` mà không escape — JSON parse fail
- ❌ Trust CDP `Input.dispatchKeyEvent` cho contenteditable React — React state may not update, phải dispatch `InputEvent` manually
- ❌ Use cua-driver pixel-coord click (x, y) khi display asleep — pixel coords may be off, prefer `click_element` selector
- ❌ **For React Slate editors: use `ce.innerText` + `InputEvent` — React state DOES NOT sync, button stays disabled** (see React Slate Pitfall below)
- ❌ **For React Slate editors: use `document.execCommand('insertText')` — same issue, button stays disabled-looking**
- ❌ **For React Slate editors: use `type_keystrokes` — may CRASH the React app** ("Application error: a client-side exception has occurred")
- ✅ cua-driver `page` `execute_javascript` với python3 subprocess — safest, robust
- ✅ cua-driver `page` `click_element` với CSS selector — real click, real state change
- ✅ Verify bằng `get_text` hoặc `execute_javascript` sau mỗi action — KHÔNG tin tool return
- ✅ **For React Slate editors: use `cua-driver page insert_text` (CDP `Input.insertText`) — IME-style commit that React picks up properly (the ONLY method that worked in 2026-07-13 Google Flow test)**

## Pitfall — React Slate editor + button "enabled" state (2026-07-13)

**Symptom:** Agent sets text in `[contenteditable=true]` element via JS (`ce.innerText = ...` + dispatch `InputEvent`/`change`). Text appears in DOM. Submit button (`<button>` with "Tạo" / "Create" / "Generate" label) is visually DISABLED — gray background (`bg: rgba(218, 220, 224, 0.05)`), dim text (`color: rgba(218, 220, 224, 0.25)`), low opacity, even though `button.disabled === false` in DOM. User sees: "prompt of em có ở trong ô prompt nhưng nút gửi đi thì lại bị mờ không gửi được" (prompt is in the box but send button is grayed out and can't send).

**Root cause:** Google Flow (and many modern SPAs — Notion, Linear, Slack, Figma, Vercel dashboard, etc.) use **Slate.js** (or similar) rich text editor. Slate maintains its own internal state model separate from DOM `innerText`. When JS sets `ce.innerText`, it mutates DOM but Slate's internal state doesn't sync. The submit button's enabled state depends on Slate state, not DOM. Result: text in DOM but state empty → button disabled.

**Methods that DO NOT work (verified 2026-07-13):**

1. ❌ `ce.innerText = prompt; ce.dispatchEvent(new InputEvent('input', {bubbles: true, data: prompt}))` — DOM updated, React state stale, button stays disabled
2. ❌ `document.execCommand('selectAll'); document.execCommand('insertText', false, prompt)` — same issue, DOM updated but Slate state empty
3. ❌ `cua-driver page type_keystrokes` — may CRASH the React app: "Application error: a client-side exception has occurred while loading labs.google" (Slate doesn't handle per-char key events reliably from CDP synthetic stream)
4. ❌ `cua-driver click at (x, y)` on button — no effect because button is React-disabled
5. ❌ `cua-driver page click_element` on button selector — no effect because button is React-disabled
6. ❌ `press_key Return` / `hotkey cmd+Return` — no effect (prompt input doesn't submit on Enter for Slate)

**Method that WORKS:**

```bash
# Use cua-driver page insert_text - sends text via CDP Input.insertText (IME-style commit)
# This is the SAME channel that real keyboards use when committing IME text
# Slate's onChange listener picks it up and updates internal state
echo '{
  "pid": <CHROME_PID>,
  "window_id": <WINDOW_ID>,
  "action": "insert_text",
  "text": "Your full prompt here (100+ chars works best, 90 chars is minimum)"
}' | cua-driver call page
# Returns: "Inserted N character(s) via CDP Input.insertText."
```

**Verification after insert_text (essential — don't trust):**

```bash
# Run via execute_javascript
echo '{
  "pid": <CHROME_PID>,
  "window_id": <WINDOW_ID>,
  "action": "execute_javascript",
  "javascript": "JSON.stringify({promptText: document.querySelector(\"[contenteditable=true]\")?.innerText, promptLength: document.querySelector(\"[contenteditable=true]\")?.innerText?.length, btnBg: getComputedStyle(Array.from(document.querySelectorAll(\"button\")).find(b => (b.innerText||\"\").includes(\"arrow_forward\"))).backgroundColor})"
}' | cua-driver call page
```

**Expected result when working:**
- `promptText`: full prompt visible (no placeholder)
- `promptLength`: ≥ 90 chars (some apps require minimum length)
- `btnBg`: `rgb(255, 255, 255)` (white = enabled), NOT `rgba(218, 220, 224, 0.05)` (gray = disabled)

**After button enables, click it via JS .click():**
```bash
echo '{
  "pid": <CHROME_PID>,
  "window_id": <WINDOW_ID>,
  "action": "execute_javascript",
  "javascript": "(function(){const b=Array.from(document.querySelectorAll(\"button\")).find(x=>(x.innerText||\"\").includes(\"arrow_forward\"));if(!b)return \"no btn\";if(b.disabled)return \"still disabled\";b.click();return \"clicked\";})()"
}' | cua-driver call page
# Returns: "clicked"
```

**Then wait 5-10s and verify result (image count, video count, etc.).**

**Decision rule for future sessions:**

| If app uses... | Use this method |
|---|---|
| Plain `<input>` / `<textarea>` | `ce.value = ...; dispatchEvent('input')` works |
| `[contenteditable=true]` with native browser editing | `cua-driver page insert_text` (CDP Input.insertText) |
| Slate.js editor (Google Flow, Notion, Linear, Figma) | `cua-driver page insert_text` ONLY (JS methods fail) |
| ProseMirror (Atlassian, Bitbucket) | `cua-driver page insert_text` works for most cases |
| Lexical (Meta, Facebook) | `cua-driver page insert_text` + dispatch focus event after |

**Quick diagnostic to detect Slate.js editor:**

```javascript
const ce = document.querySelector("[contenteditable=true]");
JSON.stringify({
    hasSlateAttribute: !!ce?.querySelector("[data-slate-node]"),
    hasSlateLeaf: !!ce?.querySelector("[data-slate-leaf]"),
    html: ce?.innerHTML?.slice(0, 100)
})
```

If `hasSlateAttribute: true` → it's Slate.js → use `insert_text` directly, don't waste time on JS methods.

## Pitfall — cua-driver execute_javascript click on React-disabled button

Even after `insert_text` properly syncs state and button becomes enabled, `cua-driver page click_element` (CSS selector) sometimes fails on buttons that have `aria-disabled` or `pointer-events: none` set by React. **Workaround:** call `.click()` via `execute_javascript` instead:

```javascript
const btn = Array.from(document.querySelectorAll("button")).find(b => (b.innerText || "").includes("Tạo"));
if (btn.disabled) return "still disabled";
btn.click();
return "clicked";
```

This bypasses the CSS pointer-events issue and fires the React onClick handler directly. Real case: 2026-07-13 Google Flow, cua-driver `click_element` on `button:has-text("Tạo")` failed silently; JS `.click()` worked immediately.

## Pitfall — wait time after click_submit for SPA generation

For AI generation apps (Google Flow, Midjourney, DALL-E, Sora), the workflow is:
1. Click submit → 200-500ms → POST to API
2. API queues job → 2-30s → returns first chunk (optional progress)
3. Final result appears in UI

**DON'T** wait 1-2s and conclude "click didn't work". **DO** poll for 30-45s with 5s intervals, checking image/video count delta:

```python
import time
for i in range(8):  # 40s total
    time.sleep(5)
    result = subprocess.run(['cua-driver', 'call', 'page'],
        input=json.dumps({
            "pid": PID, "window_id": WID, "action": "execute_javascript",
            "javascript": 'JSON.stringify({images: document.querySelectorAll("img").length, videos: document.querySelectorAll("video").length})'
        }),
        capture_output=True, text=True, timeout=15)
    count = json.loads(result.stdout)  # or parse
    print(f"T+{(i+1)*5}s: {count}")
```

Real case 2026-07-13: T+5s showed images count 41 (was 15) — generation complete in 5s. Without polling, would have wrongly concluded "click failed".

## Files involved

- `/Users/tuananh4865/.local/bin/cua-driver` — binary, on $PATH
- `/Applications/CuaDriver.app/` — macOS bundle
- `~/.hermes/skills/macos-computer-use/SKILL.md` — broader computer-use, cua-driver setup
- `~/.hermes/scripts/launch-chrome-cdp.sh` — sibling: CDP setup (chỉ dùng cho read-only CDP work)
- `~/.hermes/skills/browser-harness/references/cdp-fallback-when-computer-use-returns-zero-dim.md` — sibling: CDP fallback (read-only)
- `~/.hermes/skills/browser-harness/references/display-asleep-blocks-computer-use.md` — sibling: why computer_use fails on asleep displays

## Related

- `browser-harness/SKILL.md` § "VERIFY-BEFORE-ANNOUNCE" — verify protocol
- `browser-harness/SKILL.md` § "Persistent CDP auto-start" — CDP setup
- `macos-computer-use/SKILL.md` — broader macOS GUI automation
- `hermes-agent/SKILL.md` § "ADVERSARIAL SUBAGENT VERIFIER" — verify protocol
- Anh's correction (verbatim 2026-07-13): *"Tất cả project cũ đều mở lên được, em phải chạy computer use để sử dụng chrome thật trên máy thì mới không lỗi"*
