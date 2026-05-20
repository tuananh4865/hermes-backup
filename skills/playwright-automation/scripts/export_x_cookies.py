#!/usr/bin/env python3
"""
X.com Cookie Extractor — run via browser-harness
Output: /tmp/x_cookies.json (playwright-compatible format)

Usage:
  browser-harness <<'PY'
  exec(open("/path/to/this/file").read())
  PY
"""

import json

result = cdp("Network.getCookies", urls=["https://x.com", "https://www.x.com"])
cookies = result.get("cookies", [])

# Strip non-essential fields for playwright compatibility
essential = ("name", "value", "domain", "path", "expires", "httpOnly", "secure", "session", "sameSite")
clean = [{k: v for k, v in c.items() if k in essential} for c in cookies]

print(json.dumps(clean, indent=2))