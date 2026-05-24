#!/usr/bin/env python3
"""
X.com Automation Scripts
Based on lessons learned - KEEP IT SIMPLE!

Key principles:
1. READ content first
2. Use simple code
3. Write meaningful comments
4. Don't over-engineer
"""

import subprocess
import json
from cloakbrowser import launch

def get_cookies():
    """Get cookies from browser-harness"""
    cmd = '''browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://x.com"])
print(json.dumps(result.get("cookies", [])))
PY'''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return json.loads(result.stdout)

def close_popups(page):
    """Simple popup handler"""
    page.evaluate("""
        () => {
            var mask = document.querySelector('[data-testid="mask"]');
            if(mask) mask.click();
        }
    """)
    page.wait_for_timeout(300)

def find_ai_tweets(page, max_count=3):
    """Find AI-related tweets on timeline"""
    ai_tweets = []
    seen = set()
    
    for _ in range(20):
        close_popups(page)
        articles = page.locator("article").all()
        
        for article in articles:
            try:
                link = article.locator('a[href*="/status/"]').first
                if link.count() > 0:
                    href = link.get_attribute("href")
                    if href and href not in seen:
                        text = article.inner_text().lower()
                        if any(k in text for k in ['ai', 'claude', 'gpt', 'agent', 'llm', 'anthropic', 'cursor']):
                            seen.add(href)
                            ai_tweets.append(href)
            except:
                pass
        
        page.evaluate("window.scrollBy(0, 600)")
        page.wait_for_timeout(400)
        
        if len(ai_tweets) >= max_count:
            break
    
    return ai_tweets[:max_count]

def get_tweet_content(page):
    """Get tweet content - READ FIRST"""
    return page.evaluate("""
        () => {
            var article = document.querySelector('article');
            if(!article) return "";
            var lines = article.innerText.split('\\n').filter(l => l.trim());
            return lines.slice(0, 5).join(' ').substring(0, 300);
        }
    """)

def quote_repost(page, url, comment):
    """Simple quote repost workflow"""
    print(f"   Navigating to: {url}")
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    close_popups(page)
    
    # Click retweet
    page.locator('[data-testid="retweet"]').first.click(force=True)
    page.wait_for_timeout(1500)
    
    # Click Quote in menu
    page.evaluate("""
        () => {
            var menu = document.querySelector('[role="menu"]');
            if(menu) {
                var links = menu.querySelectorAll('a');
                links.forEach(l => {
                    if(l.innerText?.trim().toLowerCase() === 'quote') l.click();
                });
            }
        }
    """)
    page.wait_for_timeout(2000)
    close_popups(page)
    
    # Fill comment
    page.evaluate(f"""
        () => {{
            var ta = document.querySelector('[data-testid="tweetTextarea_0"]');
            if(ta) {{
                ta.innerText = "{comment}";
                ta.dispatchEvent(new Event('input', {{bubbles: true}}));
            }}
        }}
    """)
    page.wait_for_timeout(1500)
    
    # Post
    page.evaluate("""
        () => {
            var btn = document.querySelector('[data-testid="tweetButton"]');
            if(btn && !btn.disabled) btn.click();
        }
    """)
    page.wait_for_timeout(3000)
    print(f"   ✅ Done!")

def simple_repost(page, url):
    """Simple repost (no quote)"""
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    close_popups(page)
    
    page.locator('[data-testid="retweet"]').first.click(force=True)
    page.wait_for_timeout(1500)
    
    page.locator('[data-testid="retweetConfirm"]').click()
    page.wait_for_timeout(2000)
    print("   ✅ Reposted!")

# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scripts.py <command> [args]")
        print("Commands: quote, repost, help")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "help":
        print("""
X.com Automation Scripts

Commands:
  quote <url> <comment>   - Quote repost with comment
  repost <url>           - Simple repost
  find                   - Find AI tweets on timeline
  test                   - Test connection

Examples:
  python scripts.py quote https://x.com/user/status/123 "Great post!"
  python scripts.py repost https://x.com/user/status/123
  python scripts.py find
        """)
    elif cmd == "quote" and len(sys.argv) >= 4:
        cookies = get_cookies()
        browser = launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        
        quote_repost(page, sys.argv[2], sys.argv[3])
        print("Quote repost done! Browser still open.")
    elif cmd == "repost" and len(sys.argv) >= 3:
        cookies = get_cookies()
        browser = launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        
        simple_repost(page, sys.argv[2])
        print("Repost done! Browser still open.")
    elif cmd == "find":
        cookies = get_cookies()
        browser = launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()
        
        page.goto("https://x.com", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        tweets = find_ai_tweets(page)
        print(f"Found {len(tweets)} AI tweets:")
        for i, t in enumerate(tweets, 1):
            print(f"  {i}. {t}")
        
        print("Browser still open.")
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'python scripts.py help' for usage.")