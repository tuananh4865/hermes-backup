# Troubleshooting — Chrome Cookie Bridge

## Common Issues + Fixes

### 1. Chrome KHÔNG launch được với `--remote-debugging-port`

**Symptom:** `Failed to create SingletonLock: Operation not permitted`

**Root cause:** macOS sandbox block Chrome process tạo SingletonLock trong `~/Library/Application Support/Google/Chrome/`

**Fix:**
```bash
# Option A: Kill Chrome trước, launch lại với debug port
osascript -e 'quit app "Google Chrome"'
sleep 3
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-cdp-new \
  --no-first-run --no-default-browser-check

# Option B: Dùng osascript (Launch Services bypasses sandbox)
osascript -e 'do shell script "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-cdp-new > /tmp/chrome-cdp.log 2>&1 &"'
```

### 2. Cookies biến mất sau Chrome restart

**Symptom:** Chrome giữ chỉ 3/73 cookies sau restart, các cookies quan trọng (SID, HSID, SSID) bị xóa

**Root cause:** Chrome validate `creation_utc` - nếu quá cũ (>1 ngày), Chrome xem như "stale" và tự xóa

**Fix:**
```python
# Update timestamps to NOW before inserting
import time
CHROME_EPOCH = 11644473600000000
now_chrome = int(time.time() * 1000000) + CHROME_EPOCH

# Update creation_utc + last_access_utc in your inject_cookies.py
new_row[cols.index('creation_utc')] = now_chrome
new_row[cols.index('last_access_utc')] = now_chrome
new_row[cols.index('last_update_utc')] = now_chrome
```

### 3. `Network.setCookie` không work

**Symptom:** `CDP error: 'Network.setCookie' wasn't found`

**Root cause:** Network domain KHÔNG enabled ở browser scope mặc định

**Fix:**
```python
# Enable Network trước khi gọi setCookie
await ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
await ws.send(json.dumps({"id": 2, "method": "Network.setCookie", "params": {...}}))
```

**Workaround tốt hơn:** Không dùng `Network.setCookie` - inject qua DB thẳng (xem SKILL.md step 2).

### 4. HttpOnly cookies không đọc được qua `document.cookie`

**Symptom:** `document.cookie` returns empty hoặc chỉ thấy non-HttpOnly cookies

**Root cause:** HttpOnly cookies bị browser block khỏi JS access (security)

**Fix:** Dùng CDP `Network.getCookies`:
```python
result = await chrome.get_cookies(session_id, ["https://accounts.google.com"])
# Returns TẤT CẢ cookies including HttpOnly
```

### 5. Bearer token capture fails

**Symptom:** `POST /v1:checkAppAvailability` returns 401, không Bearer header

**Root cause:** Google APIs yêu cầu **OAuth Bearer token** (không phải cookies). Bearer chỉ xuất hiện trong Network requests SAU KHI user click action trong UI.

**Fix options:**

**Option A: Trigger action thật trong Chrome thật**
1. Mở Chrome profile gốc của user
2. Navigate tới Google Flow
3. Type prompt + click Generate
4. Mở DevTools Network tab
5. Copy Bearer từ request Authorization header
6. Cache Bearer ra file + reuse

**Option B: Capture Bearer runtime bằng CDP**
```python
async def capture_bearer(chrome, session_id, url_filter="aisandbox-pa"):
    bearer = None
    async for raw in chrome.ws:
        msg = json.loads(raw)
        if msg.get("method") == "Network.requestWillBeSent":
            req = msg["params"]["request"]
            if url_filter in req["url"]:
                auth = req["headers"].get("Authorization", "")
                if auth.startswith("Bearer ") and "ya29" in auth:
                    bearer = auth[7:]
                    return bearer
```

**Option C: Dùng OAuth refresh flow**
Google có OAuth client_id + scope cho phép refresh token thành Bearer. Cần tìm client_id của Google Flow UI (có thể tìm trong Next.js bundle).

### 6. Chrome UI elements ở ngoài viewport - không click được

**Symptom:** `getBoundingClientRect()` returns y > window.innerHeight, button không click

**Root cause:** Page có `position: fixed` content hoặc carousel ngang

**Fix:**
```python
# Method A: ScrollIntoView qua JS
await chrome.evaluate(session_id, """
    document.querySelector('button.Create').scrollIntoView({behavior: 'instant', block: 'center'});
""")

# Method B: Click trực tiếp qua JS bypass visibility check
await chrome.evaluate(session_id, """
    document.querySelector('button.Create').click();
""")

# Method C: Set window size lớn hơn qua CDP
await chrome.send("Emulation.setDeviceMetricsOverride", {
    "width": 2560,
    "height": 1600,
    "deviceScaleFactor": 1,
    "mobile": False
})
```

### 7. Google bot detection block

**Symptom:** Request trả 403, "Forbidden" hoặc redirect tới captcha

**Root cause:** Google fingerprint Chrome client + state. Python request KHÔNG có fingerprint = bot.

**Fix:** BẮT BUỘC dùng Chrome thật (KHÔNG bypass được).

### 8. reCAPTCHA Enterprise challenge

**Symptom:** Page render reCAPTCHA iframe, không có Bearer token

**Root cause:** Google yêu cầu user verify "I'm not a robot" bằng challenge visual/audio

**Fix:**
1. Trong Chrome thật, complete reCAPTCHA manually (1 lần)
2. Cookie `grecaptcha` được set → Bearer được issue
3. Capture Bearer từ Network tab sau khi complete
4. Reuse Bearer cho session automation (TTL ~1h)

### 9. `creation_utc` quá xa trong tương lai

**Symptom:** Chrome bỏ qua cookie, console warning "creation_utc is in the future"

**Root cause:** Bug trong timestamp conversion (sai epoch)

**Fix:**
```python
# Chrome epoch = 11644473600000000 microseconds since 1601-01-01
# Unix epoch = 1000000 microseconds since 1970-01-01
# Difference = 11644473600000000

# CORRECT conversion
chrome_value = int(time.time() * 1_000_000) + 11644473600000000
```

### 10. CDP attach fails với "sessionId is invalid"

**Symptom:** `Target.attachToTarget` returns error or session disconnects

**Root cause:** Page navigated mid-attachment

**Fix:**
```python
# Wait for page load before attaching
await chrome.create_target(url)
await asyncio.sleep(3)  # Wait for initial load
session_id = await chrome.attach_to_target(target_id)
await chrome.enable_dom(session_id)
```

## Debug Tips

### Enable Chrome verbose logging
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --enable-logging=stderr --v=1 \
  --remote-debugging-port=9222
```

### Use `chrome://inspect` to debug CDP
Navigate to `chrome://inspect/#devices` in another Chrome instance để xem tabs + attach DevTools.

### Use `crawl` to dump CDP events
```python
async def dump_all_events(ws, duration=10):
    end = time.time() + duration
    while time.time() < end:
        msg = json.loads(await ws.recv())
        print(msg.get('method', 'unknown'), msg.get('params', {}).get('type', ''))
```

### Verify cookie persistence
```bash
# After Chrome restart, check DB
sqlite3 /tmp/chrome-cdp/Default/Cookies \
  "SELECT name, host_key, datetime(expires_utc/1000000 - 11644473600, 'unixepoch') as expires
   FROM cookies
   WHERE host_key LIKE '%google%'
   ORDER BY expires DESC"
```
