# CDP Cookie Extraction — Verified Working Code (2026-06-01)

> **⚠️ IMPORTANT CONTEXT:** This file documents what WORKS for CDP-based
> cookie/state inspection on macOS. **It will return GUEST cookies only** when
> Chrome is logged in — macOS Keychain blocks auth cookie access. Use this for
> **session-state diagnostics** and **UI driving**, NOT for authentication.
>
> For actual X authentication: use `xurl` OAuth (see `browser-workflow.md`).

## Why this file exists

In the 2026-06-01 session, we discovered that all standard cookie extraction
methods fail on macOS due to Keychain encryption. This file captures the
**techniques that DO work** for CDP-based introspection, which turned out
to be valuable for:

1. **Verifying Chrome session state** without needing to read cookies
2. **Detecting when macOS Keychain is blocking auth** (vs other failures)
3. **Driving Chrome's UI** via CDP for non-auth tasks (screenshot, click)

## Prerequisites

```bash
# Python websocket library (already installed on Tuấn Anh's system)
python3 -c "import websocket; print('OK')"
# → OK

# Chrome must be running with --remote-debugging-port=9222
# See launch command at end of file
```

## Working CDP Discovery Pattern

### Step 1: List Chrome tabs

```python
import json
import urllib.request

base = "http://localhost:9222"
req = urllib.request.Request(f"{base}/json")
with urllib.request.urlopen(req, timeout=5) as resp:
    tabs = json.loads(resp.read())

for tab in tabs:
    print(f"ID: {tab['id'][:30]}")
    print(f"URL: {tab.get('url', 'N/A')[:80]}")
    print(f"Title: {tab.get('title', 'No title')[:60]}")
```

### Step 2: Find target tab (e.g. x.com)

```python
x_tab = next(
    (t for t in tabs
     if 'x.com' in t.get('url', '') and 'blob' not in t.get('url', '')),
    None
)
if not x_tab:
    raise Exception("No x.com tab found")

ws_url = x_tab['webSocketDebuggerUrl']
```

### Step 3: Connect via WebSocket

```python
import websocket

# CRITICAL: suppress_origin=True to bypass Chrome's origin check
ws = websocket.create_connection(ws_url, timeout=10, suppress_origin=True)
```

### Step 4: Run CDP commands

```python
# Get ALL cookies (returns guest cookies only on macOS)
ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies"}))
ws.settimeout(5)
resp = ws.recv()
data = json.loads(resp)
cookies = data.get("result", {}).get("cookies", [])

# Diagnostic: which cookies came back?
auth_present = any(c.get("name") == "auth_token" for c in cookies)
ct0_present = any(c.get("name") == "ct0" for c in cookies)
print(f"auth_token: {auth_present}")  # → False on macOS
print(f"ct0: {ct0_present}")          # → False on macOS
print(f"Total cookies: {len(cookies)}")
```

### Step 5: Check document.cookie + localStorage

```python
# document.cookie (X hides auth cookies here too on macOS)
ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {"expression": "document.cookie"}
}))
data = json.loads(ws.recv())
doc_cookies = data.get("result", {}).get("result", {}).get("value", "")
print(f"document.cookie has auth_token: {'auth_token' in doc_cookies}")

# localStorage utk (X's user token key)
ws.send(json.dumps({
    "id": 3,
    "method": "Runtime.evaluate",
    "params": {"expression": "localStorage.getItem('utk')"}
}))
data = json.loads(ws.recv())
utk = data.get("result", {}).get("result", {}).get("value")
print(f"localStorage utk: {utk}")

ws.close()
```

**If `auth_token` is missing from Network.getAllCookies + document.cookie +
localStorage utk is None → switch to xurl OAuth immediately.**

## Chrome Launch Command (REQUIRED flags)

```bash
# Quit existing Chrome
osascript -e 'tell application "Google Chrome" to quit'
sleep 2

# Launch with debug port (note: --remote-allow-origins=* is REQUIRED)
open -a "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default"

# Wait for Chrome to start
sleep 4

# Verify it's listening
lsof -i :9222 | grep LISTEN
# → Google Chrome ... TCP localhost:teamcoherence (LISTEN)

# Verify tabs are visible
curl -s http://localhost:9222/json | python3 -c "import sys, json; print(len(json.load(sys.stdin)), 'tabs')"
```

## Why the standard browser-harness `cdp()` wrapper times out

In our session, `browser-harness <<'PY' cdp("Network.getCookies", ...) PY`
timed out repeatedly. Working theory: `browser-harness` opens its own
WebSocket connection that may conflict with an existing Chrome instance, OR
its Python event loop blocks waiting for a response that doesn't come in the
expected format.

**Workaround:** Use raw `websocket.create_connection()` directly. The pattern
above is more reliable because you control the WebSocket lifecycle.

## The Guest-Only-Cookie Tell

When you successfully extract cookies via CDP and they all look like:

```
gt=2061294963896312058
guest_id=v1%3A...
guest_id_marketing=v1%3A...
guest_id_ads=v1%3A...
personalization_id="v1_..."
__cf_bm=QA9WsEV...
__cuid=...
g_state={"i_l":0,...}
NID=531=...   # Google NID, not X auth
```

...you're seeing **guest session cookies**, NOT authenticated user cookies.
On a real logged-in X account, you would also see:
- `auth_token` (the actual auth credential)
- `ct0` (CSRF token)
- `twid` (Twitter user ID, format: `u%3D<numeric_id>`)

**Seeing guest cookies only = macOS Keychain is blocking your access.**

## Alternatives (when xurl is unavailable)

| Goal | Tool | Works? |
|------|------|--------|
| Verify Chrome is logged in | `osascript URL of active tab` | ✅ |
| Get cookies for auth | CDP Network.getAllCookies | ❌ (Keychain) |
| Drive Chrome UI | CDP Input.dispatchMouseEvent | ✅ |
| Take screenshots | CDP Page.captureScreenshot | ✅ |
| Read page content | CDP Runtime.evaluate | ✅ |
| Auto-post as user | xurl OAuth | ✅ (only path) |

## Related

- `browser-workflow.md` — full decision tree for X automation on macOS
- `../browser-harness/SKILL.md` — note on Chrome Keychain limitation
