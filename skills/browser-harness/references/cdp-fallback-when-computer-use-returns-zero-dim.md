---
title: CDP fallback when computer_use returns 0x0 dim on Google Chrome
created: 2026-07-13
updated: 2026-07-13
type: reference
parent_skill: browser-harness
tags: [chrome, cdp, computer-use, fallback, python-path, websocket-client, macos, debugging]
confidence: high
relationships: [browser-harness, macos-computer-use, verify-chrome-navigation]
---

# CDP fallback when `computer_use capture app='Google Chrome'` returns 0×0 dim

> **Context (2026-07-13):** Session "Learn Google Flow" — anh đăng nhập sẵn tài khoản Google trên Chrome thật, cần em học cách dùng trang `https://labs.google/fx/tools/flow`. Em gọi `computer_use(action='capture', app='Google Chrome', mode='som')` → response trả về `width: 0, height: 0` + chỉ thấy menu bar (AXMenuBar, AXMenuBarItem) — không thấy Chrome window content. Lặp lại nhiều lần vẫn 0×0.
>
> Đây là failure mode MỚI, KHÁC với case 2026-07-11 trong `verify-chrome-navigation.md` (case cũ: `browser_navigate` returns success nhưng thực tế proxy → Chrome thật không navigate). Case này: `computer_use` BẢN THÂN NÓ không thể capture Chrome vì window ở Space khác / minimized / hidden.
>
> **Solution:** Pivot sang **CDP trực tiếp** qua `curl` (list tabs) + `websocket-client` (Python, query DOM). Đã verify work trong session này: vào Flow, đọc DOM, type prompt qua JS.

## Symptoms

```python
result = computer_use(action="capture", app="Google Chrome", mode="som")
# Returns:
# {
#   "mode": "som",
#   "width": 0,        ← ZERO
#   "height": 0,       ← ZERO
#   "window_title": "",
#   "elements": [
#     {"index": 0, "role": "AXMenuBar", "label": "", "bounds": [0, 0, 2560, 30]},
#     {"index": 3, "role": "AXMenuBarItem", "label": "Apple", ...},
#     ...1854 elements total, all menu bar items, NO browser content
#   ]
# }
```

Chrome window không visible trong capture → không thể verify, không thể click element.

## Why it happens

- Chrome window đang ở **Space khác** (anh switch sang Space khác làm việc khác)
- Chrome window bị **minimized** (vào Dock)
- Chrome window bị **che bởi full-screen app khác**

cua-driver vẫn có thể drive Chrome ở các trường hợp này (chỉ cần không bị che bởi window khác cùng Space), nhưng **capture screenshot fails** vì không có content visible.

## Diagnostic — confirm Chrome is alive at CDP port

Trước khi pivot, xác nhận Chrome + CDP còn hoạt động:

```bash
# 1. Chrome process running?
ps aux | grep "Google Chrome" | grep -v grep | head -3

# 2. CDP port listening?
lsof -nP -iTCP:9222 -sTCP:LISTEN

# 3. CDP endpoint responding?
curl -s http://localhost:9222/json/version
# Expected: {"Browser": "Chrome/149.x.x.x", "Protocol-Version": "1.3", ...}

# 4. List tabs (QUAN TRỌNG — xác nhận Chrome thật vẫn accessible)
curl -s http://localhost:9222/json | python3 -c "
import json, sys
tabs = json.load(sys.stdin)
for t in tabs:
    print(t.get('url','')[:100], '|', t.get('title','')[:50])
"
```

Nếu 1-3 fail → fix CDP setup trước (xem `chrome-cdp-autostart.md`).
Nếu 1-3 OK + 4 trả về list tabs → Chrome + CDP hoạt động, chỉ là `computer_use capture` không thấy → pivot sang CDP.

## Solution — query DOM via CDP directly

### 1. List tabs + find target tab

```python
import urllib.request, json
tabs = json.loads(urllib.request.urlopen("http://localhost:9222/json").read())
flow_tab = next((t for t in tabs if "labs.google/fx" in t.get("url", "")), None)
print(flow_tab["webSocketDebuggerUrl"])  # → ws://localhost:9222/devtools/page/...
```

### 2. Connect WebSocket + query DOM

**QUAN TRỌNG:** Dùng `/usr/bin/python3` (system Python có `websocket-client` 1.9.0). KHÔNG dùng `execute_code` (hermes_sandbox Python thiếu module).

```python
import websocket, json

ws = websocket.create_connection(flow_tab["webSocketDebuggerUrl"], suppress_origin=True)

# Get document text
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                     "params": {"expression": "document.body.innerText", "returnByValue": True}}))
result = json.loads(ws.recv())
text = result["result"]["result"]["value"]

# Get title
ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate",
                     "params": {"expression": "document.title", "returnByValue": True}}))
title = json.loads(ws.recv())["result"]["result"]["value"]

# Get all buttons + links + inputs (UI inventory)
ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate",
                     "params": {"expression": """
JSON.stringify({
    buttons: Array.from(document.querySelectorAll('button')).slice(0, 50).map(b => ({
        text: (b.innerText||'').trim().slice(0, 80),
        aria: b.getAttribute('aria-label') || ''
    })).filter(b => b.text || b.aria),
    links: Array.from(document.querySelectorAll('a')).slice(0, 50).map(a => ({
        text: (a.innerText||'').trim().slice(0, 80),
        href: (a.href||'').slice(0, 120)
    })).filter(a => a.text),
    inputs: Array.from(document.querySelectorAll('input, textarea, [contenteditable]')).map(i => ({
        tag: i.tagName, type: i.type || '',
        placeholder: i.placeholder || '',
        aria: i.getAttribute('aria-label') || '',
        ce: i.getAttribute('contenteditable')
    })).filter(i => i.placeholder || i.aria || i.ce === 'true'),
    headings: Array.from(document.querySelectorAll('h1, h2, h3')).map(h =>
        h.innerText?.trim().slice(0, 120)).filter(t => t),
})
""", "returnByValue": True}}))
ui = json.loads(json.loads(ws.recv())["result"]["result"]["value"])
# ui is now JSON string — json.loads() it

ws.close()
```

### 3. Click via CDP Input.dispatchMouseEvent

```python
ws = websocket.create_connection(flow_tab["webSocketDebuggerUrl"], suppress_origin=True)

# Get bounding rect of target element via JS
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                     "params": {"expression": """
JSON.stringify({
    x: Math.round(document.querySelector('button.your-target').getBoundingClientRect().x + width/2),
    y: Math.round(document.querySelector('button.your-target').getBoundingClientRect().y + height/2)
})
""", "returnByValue": True}}))
coords = json.loads(json.loads(ws.recv())["result"]["result"]["value"])

# Click
ws.send(json.dumps({"id": 2, "method": "Input.dispatchMouseEvent",
                     "params": {"type": "mousePressed", "x": coords["x"], "y": coords["y"], "button": "left", "clickCount": 1}}))
json.loads(ws.recv())
ws.send(json.dumps({"id": 3, "method": "Input.dispatchMouseEvent",
                     "params": {"type": "mouseReleased", "x": coords["x"], "y": coords["y"], "button": "left", "clickCount": 1}}))
json.loads(ws.recv())

ws.close()
```

### 4. Type via CDP Input.dispatchKeyEvent (slow but reliable)

```python
ws = websocket.create_connection(flow_tab["webSocketDebuggerUrl"], suppress_origin=True)
test_prompt = "Your prompt here"
for i, ch in enumerate(test_prompt):
    ws.send(json.dumps({"id": 100+i, "method": "Input.dispatchKeyEvent",
                         "params": {"type": "char", "text": ch}}))
    json.loads(ws.recv())
ws.close()
```

### 5. FASTER: Focus + set via JS + dispatch input event (recommended for long text)

```python
ws = websocket.create_connection(flow_tab["webSocketDebuggerUrl"], suppress_origin=True)
ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                     "params": {"expression": """
(function() {
    const ce = document.querySelector('[contenteditable="true"]');
    if (!ce) return 'no CE';
    ce.focus();
    ce.innerText = 'YOUR PROMPT HERE — supports Vietnamese, multi-line, special chars';
    ce.dispatchEvent(new InputEvent('input', {bubbles: true, data: ce.innerText}));
    return JSON.stringify({focused: document.activeElement === ce, text: ce.innerText});
})()
""", "returnByValue": True}}))
result = json.loads(ws.recv())["result"]["result"]["value"]
# result is a JSON-encoded string — json.loads() it
ws.close()
```

**Why faster:** 1 CDP round-trip vs N round-trips for char-by-char. Useful for prompts >50 chars.

**Caveat:** React apps may need additional `dispatchEvent('change')` to pick up state change. Pattern works for most contenteditable + input fields; if not, fall back to char-by-char.

### 6. Navigate to URL via CDP

```python
ws.send(json.dumps({"id": 1, "method": "Page.navigate",
                     "params": {"url": "https://labs.google/fx/tools/flow"}}))
json.loads(ws.recv())
import time
time.sleep(3)  # wait for page load
```

## Critical pitfall — Python module path

`hermes_sandbox` (the Python runtime behind `execute_code` tool) uses a DIFFERENT Python interpreter than `/usr/bin/python3`. The sandbox Python is missing `websocket-client`:

```python
# In execute_code (sandbox Python):
import websocket
# ModuleNotFoundError: No module named 'websocket'

# Workaround: write the script to /tmp/flow_cdp.py and run via terminal:
# /usr/bin/python3 /tmp/flow_cdp.py
```

**Mandatory pattern** — write CDP script to `/tmp/script.py`, run via `terminal(command="/usr/bin/python3 /tmp/script.py")`. The `execute_code` tool is NOT usable for CDP work because of this module gap.

## When to use which path

| Symptom | Path |
|---|---|
| `computer_use capture` returns rich content (elements, screenshots) | Use `computer_use` — visual click by element index |
| `computer_use capture` returns 0×0 width/height (display asleep) | Use **`cua-driver page` tool** (NEW — better than CDP, works on AX layer, real user events) — see `cua-driver-page-tool-for-real-chrome.md` |
| `computer_use capture` returns 0×0 (Chrome hidden on different Space) | Use **cua-driver `page` tool** OR CDP `curl + websocket-client` (this reference) |
| Stateful action needed (login, save, project load) | Use **`cua-driver page` tool** — CDP synthetic events rejected by modern SPA backends (anh's correction 2026-07-13) |
| Read-only DOM query, extract data | CDP `Runtime.evaluate` OK (this reference) |
| `browser_navigate` returns success but `computer_use` shows different content | `browser_navigate` is proxying — use `computer_use` with user's Chrome |
| Browser not logged in to target site (TikTok/X/Facebook etc.) | Use `xurl` for X, or accept CAPTCHA — browser-harness fails on login walls |

## Files involved

- `~/.hermes/scripts/launch-chrome-cdp.sh` — ensure Chrome CDP ready
- `/usr/bin/python3` — system Python with `websocket-client` 1.9.0
- `/tmp/cdp_*.py` — ad-hoc CDP scripts (write to /tmp, run via terminal)

## Related

- `browser-harness/SKILL.md` § "Persistent CDP auto-start" — CDP setup
- `browser-harness/SKILL.md` § "VERIFY-BEFORE-ANNOUNCE" — mandatory verify protocol
- `browser-harness/references/chrome-cdp-autostart.md` — LaunchAgent pattern
- `macos-computer-use/references/verify-chrome-navigation.md` — SIBLING case (proxy fallback, not 0×0 dim)
- `macos-computer-use/SKILL.md` § "browser-harness vs real Chrome" — when to use which tool