# Weekly Content-Niche Shorts Research — Worked Example Pattern

> Reusable template for ad-hoc weekly deep-dive research into **a specific content niche** (sports, hobby, product category) on a **specific week window** — NOT the daily Gen Z slang cron scan. Use when the user asks "Tìm N video YouTube Shorts [topic] hot nhất tuần X → Y" or "Top viral [topic] shorts tháng này".

## Distinguishing Trigger

| Pattern | Skill to use |
|---------|--------------|
| "Trending sounds / Gen Z slang tuần này" (cron, broad) | `social-media-trends` 7-step cron contract |
| "Tìm N viral shorts [specific topic] tuần X-Y" (one-off) | **THIS reference** |
| "Top gear reviews for mic/light/gimbal" (daily rotation) | `youtube-trending-research` |

## The Worked Example — Badminton Shorts 03-10/07/2026

User request: *"Tìm 15-20 video YouTube Shorts cầu lông hot nhất tuần 03/07 → 10/07/2026"*

### Step 1: Frame the Research Window

- **Niche:** badminton (cầu lông)
- **Date range:** 2026-07-03 → 2026-07-10 (8 days)
- **Format:** YouTube Shorts (cross-platform allowed)
- **Quantity target:** 15-20 videos
- **Output:** Markdown report at `~/badminton-shorts-week-03-10-july-2026.md`

### Step 2: Multi-Query Parallel Search

Run 6-8 queries in ONE assistant turn (parallel):

```
Query set A (general viral):
- "badminton shorts viral July 2026 smash trick shot"
- "badminton shorts youtube viral tuần này"

Query set B (topical events in window):
- "Canada Open 2026 badminton highlights"
- "US Smash 2026 finals BWF"
- "Asian Junior Championships 2026 Malaysia"

Query set C (specific creators known to viral in niche):
- "@aapopuhakka badminton trick shot"
- "Foong Yixin badminton tutorial"

Query set D (Vietnamese-language):
- "cầu lông short viral youtube việt nam tháng 7 2026"
- "yonex Canada Open 2026 vô địch Nhật Bản"

Query set E (community pages):
- site:facebook.com "badminton" "shorts" "viral" 2026
- site:instagram.com badminton reel
```

**Tool priority:** `mcp_exa_web_search_advanced_exa` (best date filtering + date-range param) → `mcp_MiniMax_web_search` (faster but less date control) → `web_search`.

### Step 3: Cross-Platform URL Discovery

For each short, capture BOTH:
- YouTube Shorts URL (if exists)
- Original TikTok/IG Reel URL (often the primary upload — many creators viral first on TikTok, then cross-post to YT Shorts 1-3 days later)

Real example from this session:
- Aapo Puhakka posted trick shot on TikTok 2026-07-07 first
- Cross-posted IG Reel 2026-07-08
- YouTube Shorts compilation followed
- **Single viral moment, 3 platform URLs, very different view counts**

### Step 4: Capture Per-Video Metadata

For each clip, collect:
- **Channel handle** (with verification status if available)
- **URL** (YouTube Shorts primary, others as cross-refs)
- **Views** (snapshot from snippet, mark as lifetime or window)
- **Topic tag** (trick shot / match highlight / tutorial / fail / ASMR / behind-the-scenes / challenge)
- **Viral reason** (what hook made it spread)
- **Copyright flag** (BWF / official pro tour = DO NOT re-upload; independent creator = safe to remix)

### Step 5: Group by Topic, Not by View Count

For a useful content-research deliverable, **group videos by topic angle** rather than ranking purely by views. From this session:

| Group | Count | Why this grouping matters |
|-------|-------|--------------------------|
| Trick shot / Skill | 7 | Highest virality, easiest to recreate |
| Match highlight pro | 4 | Copyright risk — REMIX only |
| Tutorial / Educational | 2 | Evergreen, always relevant |
| Behind-the-scenes / Emotional | 2 | Storytelling, brand-building |
| ASMR / Aesthetic | 1 | Trend format 2026 |
| Fail / Meme | 1 | Highest shareability |
| Tag-challenge | 1 | High viral mechanics |

This grouping tells the user "of the 18 trending clips this week, X are in your safe-to-recreate zone, Y need remix, Z are off-limits."

### Step 6: Add Adaptation Recommendations

The KEY differentiator vs. raw search output. For each video group, state:
- **YES adapt** — direct remakes safe, with voice-over example
- **YES with remix** — needs commentary in Vietnamese, attribution
- **NO** — copyright/quality issues
- **Tier 1/2/3 priority** — for the user's content calendar

Example from this session for the user's "Tuấn Anh Badminton" channel:
> Tier 1 adapt: Aapo Puhakka Yonex tube trick shot (clip 1) — voice-over "Nhiều năm tập, cuối cùng đã làm được"

### Step 7: Suggest 7-Day Content Calendar

Map top 5-7 picks to a 7-day production calendar, mixing formats (voice-over recap / behind-the-scenes / trick shot attempt / tutorial remake / ASMR / challenge / highlight) — this is the **deliverable** the user actually wants, not the raw list.

## Output Template

```markdown
# 🎯 {N} video YouTube Shorts {topic} hot nhất tuần {DD/MM} → {DD/MM}/{YYYY}

> Mục đích: Content inspiration + cross-upload cho kênh {user's channel}
> Lưu ý bản quyền: Video có gắn nhãn ©BWF/@badmintonworldfederation KHÔNG nên re-upload thẳng.
> View counts là ước tính theo thời điểm crawl — ghi rõ lifetime vs weekly.

## TỔNG QUAN
| Chủ đề | Số clip | Điểm nổi bật |

## TOP {N} CLIPS (theo thứ tự group, KHÔNG theo view count)
### Clip 1: {Hook/Title}
- Channel: {handle + verification}
- URL: {primary YouTube Shorts URL}
- Views: {lifetime} (cross-platform: {TikTok/IG if higher})
- Chủ đề: {trick shot / match / tutorial / ...}
- Vì sao viral: {1-2 câu phân tích hook}
- Adapt cho kênh Tuấn Anh? ✅/⚠️/❌ — {lý do ngắn}

## TOP PICKS (Tier 1/2/3)
## CHIẾN LƯỢC CONTENT CALENDAR 7 NGÀY
## METHODOLOGY + CAVEATS (crawl date, view count warnings)
```

## Pitfalls (specific to this pattern, NOT the cron pattern)

1. **View count inflation from cross-posting** — A single viral moment can show 1.6K on YouTube but 250K+ on TikTok. Always state the platform with the view count.
2. **BWF/Pro tour copyright** — Almost every "official" highlight comes from BWF TV. NEVER suggest re-uploading. REMIX with commentary is OK.
3. **Web search returns ARTICLES about the topic, not the videos themselves** — For sports niches, add the BWF official channel query + tournament name queries explicitly.
4. **Niche-specific creators dominate YouTube Shorts** — Aapo Puhakka (Finland, 256M lifetime), Foong Yixin (Malaysia, verified), various Indian/Malaysian/Indonesian channels. Searching for "badminton" alone misses the cross-posted cross-region viral.
5. **Local-language queries often surface higher-quality regional content** — Vietnamese query "cầu lông short viral" surfaces different results than English "badminton shorts viral". Always include at least one local-language query.
6. **Don't rank purely by views** — A 1.3K-view Shorts from a tiny channel can be MORE useful for the user than a 100K-view BWF official clip (because the small one is safe to adapt). Rank by **adaptability × view count**.

## Quality / Confidence

| Score | Criteria |
|-------|----------|
| HIGH | 8+ queries fired, ≥18 unique videos found, topic grouping clean, 5+ Tier 1 picks identified |
| MEDIUM | 5-7 queries, 10-17 videos, grouping mostly clean, 2-4 Tier 1 picks |
| LOW | <5 queries, <10 videos, grouping unclear, no clear Tier 1 |

## Related Skills

- `youtube-trending-research` — DAILY gear-niche rotation (mic/light/gimbal). Use that for product-review content.
- `tiktok-competitor-deep-analysis` — DEEP single-channel analysis (50+ clips stratified sampling). Use that when the user wants to dissect ONE channel.
- `tiktok-transcript-pipeline` — Extract full transcript + structure analysis of one specific video. Use that when the user wants to understand ONE video's script.
- `social-media-trends` (umbrella) — DAILY cron Gen Z slang + sounds scan. Use that for the evening cron.
- `tiktok-viral-script` — WRITE a viral script in Tuấn Anh's voice (after research is done).
- `content-creator-script-style` — Quy tắc viết script cho kênh Content Creator (3 trụ EDIT+SETUP+ÁNH SÁNG). Different niche — be careful not to mix.

## Signals this Reference Applies

User says ANY of:
- "Tìm N video {topic} hot nhất tuần X-Y"
- "Top {N} viral {topic} shorts"
- "{N} video {topic} trending tháng này / quý này"
- "Research {topic} shorts tuần qua"
- "Badminton / football / cooking / etc. viral shorts"

Output goes to file: `~/{topic}-shorts-week-{DD-MM-YYYY}.md` (or under `~/Workspace/Claude/Projects/{Project}/Research/{date}/` if the project structure exists per project-setup-ritual).
