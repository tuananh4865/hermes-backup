---
name: x-repost
title: X/Twitter Repost Workflow
description: Find a relevant X post and repost/share it. Does NOT mean create new content — "repost" = find existing content and share.
trigger: When Anh says "repost", "đăng lên X", "share lên X" without specifying new content creation.
created: 2026-05-21
updated: 2026-05-21
type: skill
tags: [social-media, x, twitter]
confidence: high
relationships: [social-media-automation]
---

# X Repost Skill

## Trigger
When Anh says "repost lại một bài", "đăng lên X", "share lên X" — this means FIND a relevant post and repost it. NOT create new content.

**Key distinction:**
- "repost" / "đăng lên X" → Find and share existing post → USE THIS SKILL
- "viết script" / "tạo video" → Create new content → Use tiktok-viral-script

## Workflow

### Step 1: Research Relevant Post
Search for posts related to the topic Anh cares about:
```
mcp_exa_web_search_exa(query="<topic> site:x.com OR site:twitter.com", numResults=10)
```

### Step 2: Select Best Post
Criteria:
- From credible source (tech news, verified accounts)
- High engagement (likes, RTs)
- Relevant to Anh's interests (AI agents, TikTok, productivity)
- Not political/controversial

### Step 3: Get Post URL
Find the exact tweet/post URL to repost.

### Step 4: Execute Repost via Playwright
```python
# ~/.hermes/hermes-agent venv has playwright installed
import asyncio
from playwright.async_api import async_playwright

async def repost(cookies_path="/tmp/x_cookies.json"):
    cookies = json.load(open(cookies_path))
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context()
        await ctx.add_cookies(cookies)
        page = await ctx.new_page()
        await page.goto(tweet_url)
        await page.wait_for_load_state("networkidle")
        # Click repost/retweet button — selector varies by X UI
        # Usually: [data-testid="retweet"]
        await page.click('[data-testid="retweet"]')
        await page.wait_for_timeout(500)
        # Confirm "Retweet" option (not "Quote Tweet")
        await page.click('text=Retweet')
        await asyncio.sleep(2)
        await browser.close()
```

### Step 5: Screenshot + Report
Take screenshot after repost to confirm success:
```
browser-harness screenshot → /tmp/repost_result.png
```
Report to Anh: "Đã repost bài về <topic> từ @<author>"

## X Credentials
- Account: @TyayUno (Anh Trinh's X account)
- Cookies: `/tmp/x_cookies.json` (export via browser-harness CDP)
- Cookies export command:
```bash
cd ~ && browser-harness <<'PY'
import json
result = cdp("Network.getCookies", urls=["https://x.com"])
print(json.dumps(result.get("cookies", [])))
PY
```

## Key Learning (2026-05-21)
**"Repost" ≠ create content.** When Anh says "em lên X repost lại một bài", the task is to FIND a relevant existing post and share it. I mistakenly asked what video format he wanted — wrong. The word "repost" means sharing existing content.

## Related
- [[tiktok-viral-script]] — for content creation tasks
- [[social-media-automation]] — umbrella skill for all social platforms
