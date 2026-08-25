#!/usr/bin/env python3
"""
Playwright Automation Module
=============================
Import this module for easy automation.

Usage:
    from playwright_auto import get_cookies, create_page
    
    cookies = get_cookies('x.com')
    page = create_page('x.com', cookies)
    
    # Do stuff
    articles = page.locator("article").all()
    ...
    
    page.close()
"""

import json
import subprocess
from playwright.sync_api import sync_playwright

# Cookie directory
COOKIE_DIR = "/tmp/automation-cookies"

__all__ = [
    'get_cookies',
    'save_cookies', 
    'load_cookies',
    'create_page',
    'AutomationHelper'
]


# ============================================================
# Cookie Functions
# ============================================================

def get_cookies(domain):
    """
    Lấy cookies từ browser-harness (Chrome đang chạy)
    
    Args:
        domain: ví dụ 'x.com', 'github.com'
    
    Returns:
        List of cookie dicts
    """
    urls = [f"https://{domain}", f"https://www.{domain}"]
    
    cmd = f'''browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls={urls})
cookies = result.get("cookies", [])
formatted = []
for c in cookies:
    formatted.append({{
        "name": c.get("name"),
        "value": c.get("value"),
        "domain": c.get("domain", ".{domain}"),
        "path": c.get("path", "/"),
        "secure": c.get("secure", True),
        "httpOnly": c.get("httpOnly", False),
        "sameSite": c.get("sameSite", "Lax"),
    }})
print(json.dumps(formatted))
PY'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except:
            pass
    return []


def save_cookies(domain, cookies):
    """Lưu cookies vào file"""
    import os
    os.makedirs(COOKIE_DIR, exist_ok=True)
    filepath = f"{COOKIE_DIR}/{domain.replace('.', '_')}.json"
    with open(filepath, 'w') as f:
        json.dump(cookies, f, indent=2)
    return filepath


def load_cookies(domain):
    """Đọc cookies từ file"""
    filepath = f"{COOKIE_DIR}/{domain.replace('.', '_')}.json"
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return []


def sync_cookies(domain):
    """Sync cookies từ browser-harness và lưu"""
    cookies = get_cookies(domain)
    if cookies:
        save_cookies(domain, cookies)
    return cookies


# ============================================================
# Page Creation
# ============================================================

def create_page(domain, cookies=None, headless=False):
    """
    Tạo Playwright page với cookies
    
    Args:
        domain: ví dụ 'x.com'
        cookies: list of cookies, nếu None thì load từ file
        headless: True = headless browser
    
    Returns:
        tuple: (playwright_ctx, browser, context, page)
    """
    if cookies is None:
        cookies = load_cookies(domain)
    
    if not cookies:
        print(f"⚠️ No cookies for {domain}")
        return None
    
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless)
    context = browser.new_context()
    context.add_cookies(cookies)
    page = context.new_page()
    
    return pw, browser, context, page


def create_page_with_url(url, cookies=None, headless=False):
    """Tạo page và navigate đến URL"""
    domain = url.split('/')[2].replace('www.', '')
    pw, browser, context, page = create_page(domain, cookies, headless)
    page.goto(url, wait_until="domcontentloaded")
    return pw, browser, context, page


# ============================================================
# Helper Class
# ============================================================

class AutomationHelper:
    """Helper class cho automation tasks"""
    
    def __init__(self, domain, cookies=None, headless=False):
        self.domain = domain
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None
        
        # Get cookies
        if cookies is None:
            cookies = get_cookies(domain) or load_cookies(domain)
        
        if cookies:
            self.pw = sync_playwright().start()
            self.browser = self.pw.chromium.launch(headless=headless)
            self.context = self.browser.new_context()
            self.context.add_cookies(cookies)
            self.page = self.context.new_page()
        else:
            print(f"⚠️ No cookies for {domain}")
    
    def goto(self, url, wait="domcontentloaded"):
        """Navigate đến URL"""
        if self.page:
            self.page.goto(url, wait_until=wait)
        return self
    
    def wait_for(self, selector, timeout=10000):
        """Đợi element"""
        if self.page:
            self.page.wait_for_selector(selector, timeout=timeout)
        return self
    
    def find(self, selector):
        """Tìm elements"""
        if self.page:
            return self.page.locator(selector)
        return None
    
    def find_text(self, text):
        """Tìm by text"""
        if self.page:
            return self.page.get_by_text(text)
        return None
    
    def click(self, selector=None, text=None, **kwargs):
        """Click element"""
        if selector:
            self.page.locator(selector).click(**kwargs)
        elif text:
            self.page.get_by_text(text).first.click(**kwargs)
        return self
    
    def fill(self, selector, value):
        """Fill input"""
        if self.page:
            self.page.locator(selector).fill(value)
        return self
    
    def read(self, selector):
        """Đọc text"""
        if self.page:
            return self.page.locator(selector).inner_text()
        return None
    
    def count(self, selector):
        """Đếm elements"""
        if self.page:
            return self.page.locator(selector).count()
        return 0
    
    def close(self):
        """Đóng browser"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


# ============================================================
# Quick Functions
# ============================================================

def quick_read(url, selector="article", limit=5):
    """Quick read: sync cookies và đọc elements"""
    domain = url.split('/')[2].replace('www.', '')
    cookies = sync_cookies(domain)
    
    pw, browser, context, page = create_page(domain, cookies)
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_selector(selector, timeout=15000)
    
    elements = page.locator(selector).all()
    results = []
    
    for el in elements[:limit]:
        results.append(el.inner_text())
    
    browser.close()
    pw.stop()
    
    return results


def quick_click(url, text_or_selector):
    """Quick click: sync cookies và click element"""
    domain = url.split('/')[2].replace('www.', '')
    cookies = sync_cookies(domain)
    
    pw, browser, context, page = create_page(domain, cookies)
    page.goto(url, wait_until="domcontentloaded")
    
    if text_or_selector.startswith('/') or text_or_selector.startswith('#') or text_or_selector.startswith('.'):
        page.locator(text_or_selector).click()
    else:
        page.get_by_text(text_or_selector).first.click()
    
    pw.stop()
    return True


# ============================================================
# Demo
# ============================================================

if __name__ == "__main__":
    print("🚀 Playwright Automation Module")
    print("=" * 50)
    print("\nFunctions available:")
    print("  get_cookies(domain)         # Lấy cookies từ browser-harness")
    print("  load_cookies(domain)          # Đọc cookies từ file")
    print("  sync_cookies(domain)         # Sync + save cookies")
    print("  create_page(domain, cookies) # Tạo page với cookies")
    print("  AutomationHelper(domain)    # Class-based helper")
    print("  quick_read(url, selector)    # Quick read elements")
    print("  quick_click(url, selector)    # Quick click element")
    print("\nExample:")
    print("""
    from playwright_auto import AutomationHelper
    
    with AutomationHelper('x.com') as helper:
        helper.goto('https://x.com')
        helper.wait_for('article')
        
        articles = helper.find('article').all()
        for a in articles:
            print(a.inner_text())
    """)
    print("=" * 50)