---
title: News + Image Delivery Workflow — Server-to-Server Failure Modes
created: 2026-07-02
updated: 2026-07-02
type: reference
tags: [news, image-delivery, telegram, mcp-failure]
confidence: high
relationships: [tiktok-viral-script, video-download-yt-dlp, telegram-embed-deliver-rule, five-evidence-gate-recovery-pattern]
---

# News + Image Delivery Workflow

**When to use:** Anh asks for news/research + kèm hình ảnh (sport news, gear review, trending topic). Different from script writing — voice rules don't apply here, but Telegram-embed rule + 5-evidence gate DO apply.

## The 4-Failure Pattern (verified 2026-07-02, badminton news research)

When trying to download images server-side from a news article, all 4 standard paths failed:

| # | Method | Tool/Command | Failure mode | Why |
|---|--------|--------------|--------------|-----|
| 1 | Direct curl | `curl -sL URL > img.jpg` | 403 Forbidden | Wikimedia blocks server-to-server requests without valid User-Agent + Referer |
| 2 | Browser-style curl | `curl -H "Referer: ..." -A "Mozilla/5.0" URL` | 0 bytes / 403 | CDNs (Xinhua, BWF, Olympics) block non-residential IPs |
| 3 | image_generate | `image_generate(prompt=...)` | "Authentication required" | FLUX Klein 9B backend needs separate API key, not in default Hermes config |
| 4 | web_extract | `web_extract(urls=[...])` | "DuckDuckGo is a search-only backend" | DDG backend can't extract content, only search |
| 5 | exa fetch | `mcp_exa_web_fetch_exa` | "MCP server 'exa' is not connected" | Exa MCP frequently disconnected from this profile |
| 6 | VLM via URL | `mcp_MiniMax_understand_image(image_source=URL)` | 403 Forbidden | Same as #1, Wikimedia blocks hot-linking |

## Correct Workflow — Deliver via URL Reference, Not Local Download

### Step 1: Research text content (web search works)
- Use `mcp_MiniMax_web_search` for news content — this DOES work
- For each news item, identify: date, source URL, headline, key facts (scores, names, context)

### Step 2: Find ORIGINAL photo URLs (don't download, just record)
Search these sources IN ORDER for images:
1. **BWF World Tour** — `bwfworldtour.bwfbadminton.com/news-single/...` — credit "BADMINTONPHOTO" or named photographer (Yves Lacroix, Honda Yao)
2. **Xinhua News** — `english.news.cn/...` — captioned official photos
3. **Olympics.com** — credits AFP, Reuters, Action Images via Reuters
4. **Wikimedia Commons** — `commons.wikimedia.org/wiki/File:...` — CC licensed (for personalities/profile shots)

Verify URL by searching: `"[name]" badminton 2026 site:bwfbadminton.com OR site:olympics.com OR site:english.news.cn`

### Step 3: Embed URLs in Telegram reply as markdown
Telegram gateway auto-detects markdown image URLs and renders as native photos:
```markdown
![Caption with full attribution](https://full-url-to-image.jpg)
```

### Step 4: Provide 3 self-fetch options to user
Anh is on mobile (Telegram) — he can't see Mac files. Always provide 3 ways to get full-size image:

```markdown
**Cách 1:** Bấm link ảnh → báo mở trong Safari/Chrome → nhấn giữ → "Lưu vào Thư viện"
**Cách 2:** Mở link trong Mac browser → click chuột phải ảnh → "Save Image As..."
**Cách 3:** Em dùng `computer_use` (Chrome thật trên máy anh) để tải hộ về `~/Downloads/<topic>/`
```

### Step 5: Offer 3 next-step options (A/B/C pattern)
Always end news research with concrete options:
- **A)** Em viết caption TikTok overlay cho tin (hình + text → video short viral)
- **B)** Em research sâu hơn cho 1 tin cụ thể (e.g. "5 VĐV dùng Arcsaber 11")
- **C)** Em viết content Facebook/TikTok shop dựa trên tin (kết hợp với sales anti-pattern rules)

## Self-Verify Checklist (apply every news+image request)

```markdown
- [ ] Mỗi tin có ≥1 URL ảnh gốc từ báo chính thống (BWF/Xinhua/Olympics/Wikimedia)
- [ ] Caption ảnh khớp nội dung tin (không ảnh random)
- [ ] Date của tin ≤ 7 ngày (freshness OK for "tuần qua" type queries)
- [ ] KHÔNG generate ảnh AI (no real data)
- [ ] KHÔNG claim "đã tải ảnh về" without actual file on disk (5-evidence gate)
- [ ] 3 next-step options (A/B/C) cụ thể, không hỏi "anh muốn gì?"
- [ ] Nếu anh muốn tải về → dùng `computer_use` browser, NOT curl
```

## When `computer_use` IS the Right Tool

If anh says "tải giúp anh" sau khi em đã liệt kê URLs → switch to `computer_use` workflow:
1. `computer_use(action='capture')` on anh's Mac → screenshot desktop
2. Open Chrome → navigate to URL → screenshot the article page
3. Right-click image → "Save Image As..." → save to `/Users/tuananh4865/Downloads/<topic>/`
4. Verify with `terminal ls -la` → file size > 0
5. Optionally use `MEDIA:/path/to/image.jpg` to deliver inline via Telegram gateway

This works because `computer_use` goes through anh's actual Mac browser with residential IP, bypassing CDN/Wikimedia blocks.

## Pitfalls (real)

- ❌ **Don't try image_generate as default** — needs separate API key not in default Hermes config (verified 2026-07-02, "Cannot access application fal-ai/flux-2-klein. Authentication is required")
- ❌ **Don't retry curl with different User-Agents** — CDNs block by IP, not UA. Curl WILL fail again.
- ❌ **Don't pretend "đã tải về"** when file is 0 bytes / 2009-byte HTML error page — violates 5-evidence gate + fabricated completion rule
- ❌ **Don't generate fake Wikipedia-style URLs** — violates source-driven principle
- ❌ **Don't use BWF profile stats from HTML scraping** if you hit CAPTCHA — Wikipedia/BWF CDN blocks Hermes. Switch to web search + news sites.

## Source Attribution Pattern

When delivering news with image references, ALWAYS cite source:
```markdown
📸 [Source Name + Date] — [Photographer/Credit]
🔗 https://exact-url-to-article
```

This is both journalistic correctness AND anh's preference (cites + date).

## Related

- [[tiktok-viral-script]] — parent skill (Trigger Conditions + Image-Attachment News Delivery section)
- [[video-download-yt-dlp]] — sibling skill for video download patterns (different domain but same image-source problem)
- [[telegram-embed-deliver-rule]] — Telegram-embed content pattern (memory rule)
- [[five-evidence-gate-recovery-pattern]] — 5 evidence required before claiming delivery
- [[mcp-search-workarounds]] — MCP failure workarounds