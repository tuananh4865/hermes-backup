# TikTok — Logged-in Chrome Access (Updated 2026-05-10)

## Key Finding

**TikTok works FINE with browser-harness when the user is logged into their Chrome account.**

The CAPTCHA puzzle-slider only triggers when:
- Chrome is NOT logged into TikTok
- Using an anonymous/incognito session
- Rapid-fire navigation triggers fraud detection

**If you see puzzle slider → HARD STOP on browser approach, switch to web search.** TikTok's CAPTCHA is deterministic for CDP sessions — retrying wastes iterations and risks IP block.

## View Count Extraction (Critical — Updated 2026-05-10)

TikTok displays view counts INSIDE the anchor text, NOT in `href` or data attributes:

```html
<a href="/video/ID" ...>25.2M</a>  ← "25.2M" is innerText, not a data attribute
```

**Old approach (FAILS):**
```javascript
document.querySelectorAll('a[href*="/video/"]')  // Returns empty or wrong elements
```

**Working approach (verified 2026-05-10):**
```javascript
all_videos = js("""
(function() {
    const links = Array.from(document.querySelectorAll('a[href*="/video/"]'))
        .filter(a => {
            const text = a.innerText?.trim() || '';
            return /\\d+[MK]/.test(text);  // View count is in innerText
        })
        .map(a => {
            const viewText = a.innerText?.trim() || '0';
            let views = 0;
            if (viewText.includes('M')) views = parseFloat(viewText) * 1000000;
            else if (viewText.includes('K')) views = parseFloat(viewText) * 1000;
            return { href: a.href, views: Math.floor(views), viewText: viewText };
        });
    links.sort((a, b) => b.views - a.views);
    return links.slice(0, 15);
})()
""")
// Result: [{'href': 'https://www.tiktok.com/@user/video/7442647063118073106', 'views': 533500000, 'viewText': '533.5M'}, ...]
```

## Profile Stats Extraction

```javascript
// Works even when video links are CAPTCHA-blocked
js("document.body.innerText")
// → "Lê Tuấn Khang\nletuankhang2002\n3\n13.3M\nFollower\n156.5M\nLượt thích"
```

## Fail-Fast Protocol (2026-05-10)

1. Try `browser-harness` → get profile text
2. If CAPTCHA present → try 1 more refresh with wait(5)
3. If still CAPTCHA after 2 attempts → **hard stop**, switch to `mcp_exa_web_search_exa` + news site parsing

**News sources for TikTok viral data:**
- 24h.com.vn
- tienphong.vn
- kenh14.vn
- saostar.vn

## What Works / Doesn't Work

| Action | Status |
|--------|--------|
| Profile stats (followers, likes) | ✅ Works always |
| Video links with view counts | ✅ Only with logged-in Chrome |
| Incognito/anonymous | ❌ CAPTCHA |
| Rapid navigation | ❌ May trigger fraud detection |
| SMS/email OTP verification | ❌ Cannot bypass |