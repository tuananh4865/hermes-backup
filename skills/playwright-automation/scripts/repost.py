#!/usr/bin/env python3
"""
X.com Simple Repost — via Playwright using browser-harness cookies

Usage:
  python3 scripts/repost.py https://x.com/user/status/1234567890

Workflow:
  1. browser-harness exports cookies → /tmp/x_cookies.json
  2. This script reads cookies and runs repost via Playwright
"""

import sys
import json
from playwright.sync_api import sync_playwright

COOKIE_FILE = "/tmp/x_cookies.json"

def simple_repost(url: str) -> bool:
    with open(COOKIE_FILE) as f:
        cookies = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()

        print(f"Navigating to: {url}")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # Read content
        article = page.locator("article").first
        if article:
            text = article.inner_text()[:150]
            print(f"Tweet: {text}...")

        # Click repost
        page.locator('[data-testid="retweet"]').first.click()
        page.wait_for_timeout(1500)

        # Confirm via menu item "Repost"
        for item in page.locator('[role="menuitem"]').all():
            try:
                txt = item.inner_text().lower()
                if "repost" in txt and "quote" not in txt:
                    item.click()
                    page.wait_for_timeout(2000)
                    print("✅ Repost successful!")
                    browser.close()
                    return True
            except:
                pass

        print("❌ Could not find repost button")
        browser.close()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <tweet_url>")
        sys.exit(1)
    simple_repost(sys.argv[1])