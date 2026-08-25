---
name: chrome-cookie-bridge
description: Extract cookies from Chrome profile thật của user (macOS Keychain) + inject vào Chrome CDP riêng để automation với session Google thật. Trigger khi cần "drive Chrome với Chrome profile thật", "automation với session user", "extract Google cookies", "inject session vào Chrome mới".
version: 1.0.0
author: 'Tuấn Anh + Hermes Agent (15/08/2026 — verify Chrome Safe Storage decrypt + CDP injection)'
license: MIT
platforms: [macos]
metadata:
  category: automation
  tags: [chrome, cdp, cookies, keychain, google-flow, automation, session-injection]
---

# Chrome Cookie Bridge — Skill vĩnh viễn

> **Mục tiêu:** Trích xuất cookies từ Chrome profile thật của user (Chrome Safe Storage + Keychain) → inject vào Chrome CDP riêng → drive automation với Google session thật của user.

## 🎯 Use Cases (Verified)

1. **Drive Google Flow với Chrome thật + session thật** - 80 cookies extract được, 23 persist sau Chrome restart bao gồm SID/HSID/SSID/APISID/SAPISID
2. **Navigate bất kỳ Google service nào** với Chrome CDP riêng (Drive, YouTube, Gmail, Labs, AI Studio)
3. **Capture HttpOnly cookies** không access được qua `document.cookie`
4. **Bypass Chrome singleton lock** - extract cookies từ Chrome gốc, close Chrome, launch CDP riêng với cookies đã inject

## 🚨 Known Limitations (verified 15/08/2026)

| Limitation | Workaround |
|---|---|
| **Google APIs yêu cầu Bearer OAuth token** riêng (không phải cookies) | Capture Bearer runtime từ page Network requests |
| **reCAPTCHA Enterprise challenge** block Bearer capture | Click action manually trong Chrome thật để trigger reCAPTCHA, sau đó capture Bearer |
| **Bearer TTL ~1h** | Auto-refresh + cache file |
| **Google bot detection** fingerprint client + state | Dùng Chrome thật, KHÔNG bypass được bằng Python |
| **Cookie sessions expire** (Google session ~30 ngày) | Re-run extract từ Chrome thật |

## 📋 Prerequisites

1. **macOS** (verified trên macOS 14.5+, Chrome 151+)
2. **Chrome profile thật** đã login Google account trong Chrome
3. **Chrome Safe Storage keychain entry** tự động có khi Chrome lưu password/cookies
4. **Python 3.9+** với `cryptography` library

## 🔧 Cài đặt

```bash
pip install cryptography websockets
```

## 📦 Files

```
chrome-cookie-bridge/
├── SKILL.md                  ← File này
├── scripts/
│   ├── extract_cookies.py    ← Extract cookies từ Chrome DB
│   ├── inject_cookies.py     ← Inject cookies vào Chrome CDP profile
│   ├── launch_cdp.sh         ← Launch Chrome CDP với empty profile
│   ├── cdp_automation.py     ← Pure websocket CDP client
│   └── full_workflow.py      ← End-to-end automation demo
└── references/
    ├── chrome_safe_storage.md   ← Chi tiết kỹ thuật decrypt
    └── troubleshooting.md       ← Common issues + fixes
```

## 🚀 Quick Start (3 bước)

### Bước 1: Extract cookies từ Chrome thật của user

```bash
# Đóng Chrome trước (để unlock file)
osascript -e 'quit app "Google Chrome"'

# Extract
python3 scripts/extract_cookies.py \
  ~/Library/Application\ Support/Google/Chrome/Default/Cookies \
  /tmp/cdp-client/chrome-cookies.json
```

**Output:** JSON file với tất cả cookies đã decrypt (name, host, value, path, secure, httponly)

### Bước 2: Inject cookies vào Chrome CDP riêng

```bash
# Launch Chrome CDP với empty profile + debug port
bash scripts/launch_cdp.sh /tmp/chrome-flow-cdp 9222

# Close Chrome CDP, inject cookies, re-launch
python3 scripts/inject_cookies.py \
  /tmp/chrome-flow-cdp/Default/Cookies \
  /tmp/cdp-client/chrome-cookies.json

# Restart Chrome CDP (cookies giờ trong DB)
bash scripts/launch_cdp.sh /tmp/chrome-flow-cdp 9222
```

### Bước 3: Drive automation với Chrome CDP

```python
import asyncio
from scripts.cdp_automation import Chrome

async def main():
    chrome = Chrome(port=9222)
    target_id = await chrome.create_target("https://labs.google/fx/vi/tools/flow/project/YOUR_PROJECT_ID")
    session_id = await chrome.attach_to_target(target_id)

    await chrome.navigate(session_id, "https://labs.google/fx/vi/tools/flow/create?projectId=YOUR_PROJECT_ID")
    cookies = await chrome.get_cookies(session_id, ["https://accounts.google.com"])

    # Now you can drive the Flow UI with real session
    # Note: reCAPTCHA Enterprise may block Bearer capture
```

## 🔐 Kỹ thuật Chrome Safe Storage (quan trọng)

Chrome macOS lưu cookies encrypted với **PBKDF2** key derive từ keychain entry "Chrome Safe Storage":

```python
# Extract keychain password
password = subprocess.run(
    ["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"],
    capture_output=True, text=True
).stdout.strip().encode("utf-8")

# Derive AES-128-CBC key (16 bytes)
key = hashlib.pbkdf2_hmac("sha1", password, b"saltysalt", 1003, 16)

# Chrome 151 macOS uses v10 format
# Format: b'v10' (3) + IV (16 spaces) + AES-CBC ciphertext
iv = b" " * 16
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
```

**CHROME EPOCH:** `11644473600000000` (Jan 1, 1601 → Unix)

## 📊 Real Case (15/08/2026)

- Chrome profile: 950KB / 357 cookies total / 80 Google-related
- Cookies injected: 73/80
- Cookies persist after Chrome restart: 23/73 (Chrome validates + drops some)
- Key cookies: `SID, HSID, SSID, APISID, SAPISID, NID, LSID, ACCOUNT_CHOOSER, __Host-GAPS, __Host-GAPSTS, next-auth.csrf-token`
- Google Flow navigation: ✅ Success với session thật
- Bearer token capture: ❌ Blocked by reCAPTCHA Enterprise (cần user click action thật)

## ⚠️ Critical Pitfalls

1. **Chrome KHÔNG share cookies** giữa 2 instance khi cùng profile → phải close Chrome gốc TRƯỚC khi launch CDP riêng
2. **Chrome validates `creation_utc`** khi restart - nếu cookies quá cũ → Chrome TỰ XÓA. Fix = UPDATE timestamps về NOW khi inject
3. **Network.setCookie KHÔNG work** ở Chrome CDP mới - workaround = copy full cookie rows từ DB
4. **HttpOnly cookies KHÔNG access** qua `document.cookie` - chỉ CDP `Network.getCookies` mới thấy
5. **SingletonLock** trên `~/Library/Application Support/Google/Chrome/` block mọi write → cần Chrome closed trước khi copy

## 🔗 Related Skills

- `chrome-cdp-automation` - Pure websocket CDP client
- `computer-use` - macOS native automation
- `tiktok-clip-editor-v2` - TikTok video editing (uses CDP for QA)
- `browser-harness` - Browser automation qua CDP

## 📚 References

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) - 56 domains, 256 methods
- [Chrome Safe Storage](https://chromium.googlesource.com/chromium/src/+/master/components/os_crypt/) - PBKDF2 + AES-CBC
- Wiki: `/Volumes/Storage-1/Hermes/wiki/concepts/chrome-cdp-automation-macos-2026-08-14.md`
