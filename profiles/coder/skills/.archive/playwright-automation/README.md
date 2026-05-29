# Playwright Automation Skill

## Files

- **SKILL.md** - Main skill documentation
- **references/scripts.py** - Quick automation scripts
- **references/playwright_auto.py** - Python module for import

## Quick Usage

### 1. Get cookies from browser-harness

```bash
browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://x.com"])
cookies = result.get("cookies", [])
formatted = []
for c in cookies:
    formatted.append({
        "name": c.get("name"),
        "value": c.get("value"),
        "domain": c.get("domain", ".x.com"),
        "path": c.get("path", "/"),
        "secure": c.get("secure", True),
        "httpOnly": c.get("httpOnly", False),
        "sameSite": c.get("sameSite", "Lax"),
    })
print(json.dumps(formatted))
PY
```

### 2. Use with Playwright

```python
from playwright.sync_api import sync_playwright

cookies = [...]  # From above

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    
    page.goto("https://x.com", wait_until="domcontentloaded")
    page.wait_for_selector("article", timeout=15000)
    
    # Read posts
    articles = page.locator("article").all()
    for article in articles:
        print(article.inner_text())
    
    browser.close()
```

### 3. Using the helper module

```python
import sys
sys.path.insert(0, "/Users/tuananh4865/hermes/skills/playwright-automation/references")

from playwright_auto import AutomationHelper, sync_cookies

# Sync cookies from browser-harness
cookies = sync_cookies('x.com')

# Use helper class
with AutomationHelper('x.com', cookies) as helper:
    helper.goto('https://x.com')
    helper.wait_for('article')
    
    articles = helper.find('article').all()
    print(f"Found {len(articles)} articles")
    
    for a in articles:
        print(a.inner_text()[:100])
```

## Running Scripts

```bash
# Read X.com timeline
python3 ~/.hermes/skills/playwright-automation/references/scripts.py x_com

# Read GitHub trending
python3 ~/.hermes/skills/playwright-automation/references/scripts.py github

# Read page structure
python3 ~/.hermes/skills/playwright-automation/references/scripts.py read https://x.com
```

## Workflow

1. User login via Chrome (browser-harness)
2. Extract cookies via CDP
3. Add cookies to Playwright context
4. Automation with powerful DOM reading

## Requirements

- browser-harness installed and running
- Playwright installed: `pip install playwright`
- Chrome running with remote debugging enabled