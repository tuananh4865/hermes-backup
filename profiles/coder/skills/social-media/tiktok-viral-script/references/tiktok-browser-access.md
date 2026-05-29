# TikTok Browser Access — CAPTCHA & Workarounds (Updated 2026-05-10)

## Problem
TikTok uses puzzle-slider CAPTCHA to block automated browser access. 

**Symptoms:**
- Page loads but shows verification modal: "Drag the slider to fit the puzzle"
- Video grid shows grey placeholders, no clickable thumbnails
- JavaScript finds zero `<a href="/video/...">` links on the page

## Root Cause — Two Different Chrome Sessions

There are TWO different browser sessions that browser-harness can connect to:

### ❌ Fresh Chrome Instance (triggers CAPTCHA)
When browser-harness starts a fresh CDP session without attaching to user's real Chrome:
- New Chrome instance opens
- No TikTok login cookies
- TikTok detects CDP automation → CAPTCHA

### ✅ User's Real Chrome (NO CAPTCHA)
When browser-harness attaches to user's already-running Chrome:
- Uses existing cookies and session
- User is already logged into TikTok in that Chrome
- **NO CAPTCHA triggered** — works perfectly

## How to Verify Which Session You're Using

```bash
browser-harness --doctor
```

**Output shows:**
```
[ok] active browser connections — 1
      default — active page: (92)🐴 TikTok - Make Your Day — https://www.tiktok.com/@letuankhang2002
```

If it shows the user's actual TikTok session (profile name visible in title), you're on the real Chrome.

## What WORKS on User's Real Chrome (verified 2026-05-10)

```python
# Get ALL videos from profile sorted by views (NO CAPTCHA)
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
# Returns: [{'href': '.../video/7442647063118073106', 'views': 533500000, 'viewText': '533.5M'}, ...]

# Get profile stats
text = js("document.body.innerText")
# → "Lê Tuấn Khang\nletuankhang2002\n3\nĐã follow\n13.3M\nFollower\n156.5M\nLượt thích"

# Get video page engagement
full_text = js("document.body.innerText")
# → "8.8M\n719K\n532.6K\n355.2K" (likes/comments/shares/saves)
```

**Key discovery:** View counts appear INSIDE anchor text (e.g., "25.2M", "37.9M") — NOT in href attributes. Use regex `/\d+[MK]/` to filter video links.

## What Still Cannot Do
- ❌ Solve TikTok login OTP (SMS/email verification mid-session)
- ❌ Bypass fraud detection if triggered
- ❌ Access private/restricted accounts

## Fail-Fast Protocol (Original)

**Signal:** After 2 `browser-harness` attempts, if `page_info()` returns CAPTCHA → HARD STOP on browser approach.

**But this was BEFORE the discovery (2026-05-10):** The CAPTCHA only appears when NOT using user's real logged-in Chrome. If `browser-harness --doctor` shows user's TikTok session, the browser approach WILL work.

**Updated detection:**
1. Run `browser-harness --doctor` → check if shows user's TikTok session
2. If YES → browser approach works, use full technique above
3. If NO (fresh Chrome instance) → after 2 CAPTCHA attempts, switch to web search

## Practical Approach for Competitor Research

When researching TikTok creators (like Lê Tuấn Khang):

1. **Run `browser-harness --doctor`** → verify connection to user's Chrome
2. **If user's Chrome available:** Navigate to profile → extract all videos with views → sort → click top video → screenshot → analyze
3. **If NOT available:** Use `mcp_exa_web_search_exa` + news site parsing

**Result from 2026-05-10 session:**
- User's Chrome was at TikTok (logged in) → perfect access, no CAPTCHA
- Extracted 36+ videos with view counts
- Top video: 533.5M views ("Giả bộ té để được rửa sạch", 29/11/2024)
- Profile: 13.3M followers, 156.5M likes

## News Sources for TikTok Viral Data
- 24h.com.vn — breaking news on viral videos
- tienphong.vn — detailed viral video analysis  
- kenh14.vn — youth culture coverage
- saostar.vn — entertainment/trending content
- baoxaydung.vn — viral content breakdown