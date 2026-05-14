# computer_use Verification & Debug Reference

## Key commands discovered this session

### Check tool state
```bash
hermes tools list | grep computer_use
cua-driver --version
```

### TCC permissions (Accessibility + Screen Recording required)
```bash
cua-driver check_permissions
# ⚠️ Run outside daemon → may show false negative
# Start daemon for accurate results:
open -n -g -a CuaDriver --args serve
cua-driver check_permissions
```

### Find on-screen windows (cua-driver MCP mode)
```bash
echo '{"on_screen_only": true}' | cua-driver list_windows
# Returns: app_name, pid, window_id, title, is_on_screen, z_index
# z_index: lowest = frontmost on macOS
```

### Get window screenshot via MCP
```bash
echo '{"window_id": 7044, "format": "jpeg", "quality": 70}' | cua-driver screenshot
# Requires window_id from list_windows
```

### Chrome tab inspection (osascript — fastest for inspection)
```bash
osascript -e 'tell application "Google Chrome" to get name of front window'
osascript -e 'tell application "Google Chrome" to get URL of every tab of front window'
osascript -e 'tell application "Google Chrome" to get name of every tab of front window'
osascript -e 'tell application "Google Chrome" to get URL of tab N of front window'
```

### python3 direct backend test
```python
# Use venv python (not system python3 — system may be 3.9, venv is 3.11)
import sys; sys.path.insert(0, '/Users/tuananh4865/.hermes/hermes-agent')
from tools.computer_use.tool import handle_computer_use
import json

cap = handle_computer_use({'action': 'capture', 'mode': 'som', 'app': 'Google Chrome'})
parsed = json.loads(cap) if isinstance(cap, str) else cap
print(parsed['meta'].get('elements'), 'elements')
```

## browser-harness vs computer_use on login-gated sites

| Scenario | browser-harness | computer_use |
|----------|-----------------|--------------|
| X/Twitter logged in | ❌ Shows login page | ✅ Works on real Chrome |
| TikTok logged in | ❌ CAPTCHA block | ✅ Works on real Chrome |
| Public site | ✅ Works fine | ✅ Works |

**Key signal:** osascript shows `https://x.com/home` but browser_navigate shows login → browser-harness is on separate unauthenticated instance.

## Known limitations

- `drag` action: not supported by cua-driver backend. Returns error. Use scroll+click workaround.
- Element index stale after UI shift → always re-capture before clicking
- AX tree from cua-driver: `mode=ax` returns very few elements (menu bar only), use `mode=som` for full element list