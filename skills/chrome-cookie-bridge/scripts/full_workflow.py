"""
Full workflow demo: Extract cookies → Inject → Drive Flow
"""
import asyncio
import subprocess
import time
import os
import sys

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(__file__))

from extract_cookies import extract_cookies
from inject_cookies import inject_cookies
from cdp_automation import Chrome


async def main():
    # Configuration
    CHROME_PROFILE = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    CDP_PROFILE = "/tmp/chrome-flow-cdp"
    CDP_PORT = 9222
    PROJECT_ID = "1c4a5a79-f24e-4ea7-978c-94bb1bf45350"  # Your project ID

    print("=== Step 1: Close Chrome ===")
    subprocess.run(["pkill", "-9", "-f", "Google Chrome"], capture_output=True)
    time.sleep(3)

    print("\n=== Step 2: Extract cookies from Chrome ===")
    src_db = f"{CHROME_PROFILE}/Default/Cookies"
    cookies_file = "/tmp/cdp-client/chrome-cookies.json"
    cookies = extract_cookies(src_db, cookies_file)
    print(f"✅ Extracted {len(cookies)} cookies")

    print("\n=== Step 3: Launch Chrome CDP riêng ===")
    # Note: Need to launch CDP first to create the profile dir
    if not os.path.exists(CDP_PROFILE):
        os.makedirs(CDP_PROFILE)

    print(f"Launching Chrome CDP with empty profile at {CDP_PROFILE}...")
    subprocess.run([
        "osascript", "-e",
        f'do shell script "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={CDP_PORT} --user-data-dir={CDP_PROFILE} --no-first-run --no-default-browser-check > /tmp/chrome-cdp.log 2>&1 &"'
    ])
    time.sleep(6)

    # Verify CDP
    import urllib.request
    try:
        urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version").read()
        print(f"✅ Chrome CDP running on port {CDP_PORT}")
    except Exception as e:
        print(f"❌ Chrome CDP failed: {e}")
        return

    print("\n=== Step 4: Close CDP, inject cookies, restart ===")
    subprocess.run(["pkill", "-9", "-f", "Google Chrome"], capture_output=True)
    time.sleep(2)

    dst_db = f"{CDP_PROFILE}/Default/Cookies"
    inject_cookies(src_db, dst_db, cookies_file)

    # Restart CDP
    subprocess.run([
        "osascript", "-e",
        f'do shell script "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={CDP_PORT} --user-data-dir={CDP_PROFILE} --no-first-run --no-default-browser-check > /tmp/chrome-cdp.log 2>&1 &"'
    ])
    time.sleep(6)

    print("\n=== Step 5: Drive Chrome with CDP ===")
    chrome = Chrome(port=CDP_PORT)

    # Create target for Flow project
    target_id = await chrome.create_target(f"https://labs.google/fx/vi/tools/flow/project/{PROJECT_ID}")
    print(f"Target: {target_id}")

    session_id = await chrome.attach_to_target(target_id)
    print(f"Session: {session_id}")

    # Navigate to Flow editor
    await chrome.navigate(session_id, f"https://labs.google/fx/vi/tools/flow/create?projectId={PROJECT_ID}")
    await asyncio.sleep(10)

    # Get cookies - verify session
    cookies = await chrome.get_cookies(session_id, ["https://accounts.google.com"])
    google_cookies = [c for c in cookies if c['name'] in ['SID', 'HSID', 'SSID', 'APISID']]
    print(f"\nGoogle session cookies: {len(google_cookies)}")
    for c in google_cookies:
        print(f"  ✅ {c['name']} domain={c['domain']}")

    # Get URL
    url = await chrome.evaluate(session_id, "window.location.href")
    title = await chrome.evaluate(session_id, "document.title")
    print(f"\nURL: {url}")
    print(f"Title: {title}")

    print("\n✅ Automation ready - drive UI with chrome.evaluate(), chrome.click(), chrome.type_text()")
    print("\n⚠️  NOTE: Bearer token capture blocked by reCAPTCHA Enterprise")
    print("   To create videos: capture Bearer manually via Chrome DevTools Network tab")


if __name__ == "__main__":
    asyncio.run(main())
