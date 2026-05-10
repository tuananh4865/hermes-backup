# TikTok Research via Browser Harness

## Problem
TikTok has aggressive bot detection. Direct navigation to search pages returns "Something went wrong" even when logged in.

## What DOESN'T work
- `new_tab("https://www.tiktok.com/search?q=...")` → "Something went wrong" error page
- Google search from terminal IP → CAPTCHA block ("IP address: ...")
- `web_search` (Hermes tool) → 400 error

## What WORKS (updated 2026-05-10)

### Method 1: Browser via user's logged-in Chrome (BEST)
When user is logged into Chrome AND browser-harness attaches to that session:
```bash
browser-harness -c '
goto_url("https://www.tiktok.com/@username")
wait_for_load()
wait(3)
# Get video links with views sorted
all_videos = js("""
(function() {
    const links = Array.from(document.querySelectorAll("a[href*=\"/video/\"]"))
        .filter(a => /\\d+[MK]/.test(a.innerText?.trim() || ""))
        .map(a => {
            const viewText = a.innerText?.trim() || "0";
            let views = 0;
            if (viewText.includes("M")) views = parseFloat(viewText) * 1000000;
            else if (viewText.includes("K")) views = parseFloat(viewText) * 1000;
            return { href: a.href, views: Math.floor(views), viewText: viewText };
        });
    links.sort((a, b) => b.views - a.views);
    return links.slice(0, 15);
})()
""")
print(all_videos)
')
```
Key: View counts appear INSIDE anchor text (e.g., "25.2M", "37.9M"), not in href. Use regex `/\d+[MK]/` to filter.

### Method 2: mcp_exa_web_search_exa
```python
mcp_exa_web_search_exa(numResults=10, query="...")
```
Bypasses TikTok/Google blocking. Good for research when browser fails.

## Workflow for TikTok Creator/Content Research
1. Run `browser-harness --doctor` → verify "active browser connections — 1"
2. If user's Chrome is at TikTok and logged in → browser works perfectly, no CAPTCHA
3. Navigate to profile URL → scroll → extract video links via `js()`
4. Sort by view count → click top video → screenshot → vision analyze

## Key Findings from Lê Tuấn Khang Research (2026-05-10)

| Metric | Value |
|--------|-------|
| Profile | @letuankhang2002 |
| Followers | 13.3M |
| Likes | 156.5M |
| Top video views | **533.5M** ("Giả bộ té để được rửa sạch", 29/11/2024) |
| Top 5 videos | 533.5M, 154.6M, 115.5M, 88.9M, 86.4M |

Note: Earlier web search said ~300M — the actual number is 533.5M. Browser extraction is more accurate than web search.

## Limitations
- Cannot solve TikTok login OTP mid-session (SMS/email verification)
- Cannot bypass fraud detection if triggered
- CAPTCHA puzzle slider appears when NOT using user's logged-in Chrome session