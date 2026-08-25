# TikTok 5-Channel Nightly Monitor — 10 Videos Complete Run

> Session: 2026-06-07. Full 10-video analysis from 5 channels × 2 videos each. Source: cron job `546c141c8fb9`.

## Channel Roster
| Channel | Niche | Latest Videos |
|---------|-------|-------------|
| @duymuoi | Content creator education | 7621544652222926088, 7618037474811579668 |
| @anhsacanh.vn | Tech gear reviews | 7635163991668690196, 7633785255303957781 |
| @nguyenducduong9699 | Hustle/personal brand | 7569219969733446932, 7309799232657968389 |
| @tam_thefox | Channel building tips | 7645214457043471636, 7639956703974280468 |
| @goccontent | Content mentorship | 7582440823149710599, 7588318365236595976 |

## Key Findings (10-video synthesis)

### Hook Types That Dominated
1. **"1 Mẹo" / "1 Tip" Format** — Promise easy solution in title → highest retention
   - "1 MẸO NHỎ GIÚP XÁC ĐỊNH CÁC CHỦ ĐỀ DỄ VIRAL"
   - "NHẠC HOT LÊN XU HƯỚNG" (1 tip = use trending audio)
   - WHY IT WORKS: Easy promise + massive reward = thumb-stop

2. **Pattern Disrupt (Bold Statement)** — Shock statements break expectations
   - "ĐỪNG HỌC NỮA — Hành động đi" (@tam_thefox)
   - "BẠN CẦN BỎ NGAY: CHÀO CHÀO HỎI HỎI" (@goccontent)
   - WHY IT WORKS: Controversy → comment war → algorithm boost

3. **Expert Authority Positioning** — Kính + bookshelf/car = instant credibility
   - No studio needed — clean background + professional look

### CTA Pattern Discovery
| CTA Type | Example | Engagement |
|----------|---------|------------|
| **Question (WINNER)** | "Comment X nhé" | High — natural interaction |
| **Directive** | "Follow mình đi" | Low — pushy, algorithm detects pressure |

### Series / Episode Pattern
- "Tập 1, Tập 2, Tập 3..." → FOMO → habit return
- @anhsacanh.vn: "Tập 3 series nấu cơm chồng" → viewer misses continuity if they skip

## Technical Notes

### Deduplication
- JSON tracker: `~/.hermes/cron/tiktok-monitor/seen-videos.json`
- Key: `video_id` — extract from URL (`/video/7621544652222926088`)
- Update tracker AFTER successful analysis, BEFORE sending Telegram summary

### URL Discovery Workflow
```
mcp_MiniMax_web_search(query="site:tiktok.com/@username latest video 2026")
→ Extract vm.tiktok.com/ or tiktok.com/video/ URLs from results
→ yt-dlp -o "file.mp4" "https://vm.tiktok.com/..." (URL MUST be quoted)
→ Extract video_id from filename or --print JSON
```

### Frame Extraction
```bash
for f in tamthefox_1 tamthefox_2 nguyenducduong_1; do
  ffmpeg -i "${f}.mp4" -vf fps=1 -frames:v 20 "${f}_%03d.jpg" -y
done
# Output: 20 frames per video at 1fps
```

### video_id Extraction from yt-dlp Output
```bash
yt-dlp --print video_id -o "%(id)s.mp4" "URL"  # get ID before downloading
# OR parse from download output: "Destination: channel_1.mp4"
# Video ID format: 19-20 digit number (e.g., 7621544652222926088)
```

## Report Output Path
`~/.hermes/cron/tiktok-monitor/YYYY-MM-DD/report.md`

## Telegram Summary Format
<500 words. Structure:
1. **Top 3 Trends** — hook/format/style patterns
2. **Top 3 Lessons** — actionable for Anh's channel
3. **TikTok Shop Recommendations** — product/content fit
4. Full report path note

## Sources
- Session: 2026-06-07, cron job `546c141c8fb9` test run
- All 10 videos analyzed via yt-dlp → ffmpeg → MiniMax vision pipeline
- Seen tracker: `~/.hermes/cron/tiktok-monitor/seen-videos.json`
