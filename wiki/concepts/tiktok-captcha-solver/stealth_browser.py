"""
Stealth Browser Wrapper — Ẩn automation signatures để giảm CAPTCHA rate
"""

from typing import Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from playwright_stealth import Stealth


class StealthBrowser:
    """
    Browser với stealth mode để giảm bị phát hiện là bot.
    
    Features:
    - Ẩn webdriver signature
    - Fake navigator properties
    - Randomize viewport
    - Apply stealth plugins
    """
    
    def __init__(
        self,
        headless: bool = False,
        proxy: Optional[dict] = None,
        viewport: dict = None,
        user_agent: str = None
    ):
        self.headless = headless
        self.proxy = proxy
        self.viewport = viewport or {"width": 1280, "height": 800}
        self.user_agent = user_agent
        
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.stealth = Stealth()
    
    def launch(self):
        """Launch stealth browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
            ]
        )
        return self
    
    def new_context(self) -> BrowserContext:
        """Tạo new context với stealth settings."""
        context_args = {
            "viewport": self.viewport,
            "ignore_https_errors": True,
        }
        
        if self.proxy:
            context_args["proxy"] = self.proxy
        
        if self.user_agent:
            context_args["user_agent"] = self.user_agent
        
        self.context = self.browser.new_context(**context_args)
        return self.context
    
    def new_page(self) -> Page:
        """Tạo new page với stealth mode."""
        if self.context is None:
            self.new_context()
        
        page = self.context.new_page()
        
        # Apply stealth to page
        self.stealth.apply_stealth_sync(page)
        
        return page
    
    def close(self):
        """Close browser."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


def create_stealth_browser(
    headless: bool = False,
    proxy: dict = None
) -> StealthBrowser:
    """
    Factory function để tạo stealth browser.
    """
    return StealthBrowser(headless=headless, proxy=proxy)


if __name__ == "__main__":
    # Demo
    with StealthBrowser(headless=False) as browser:
        browser.launch()
        page = browser.new_page()
        page.goto("https://www.tiktok.com")
        print("Stealth browser opened TikTok")
