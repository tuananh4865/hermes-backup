# Competitor Channel Deep Analysis Pattern

> **Verified pattern (2026-07-11):** @VuiVe case (1.18M subs, 828 videos) — clone theo yêu cầu của Tuấn Anh
> **Mục đích:** Workflow template khi user nói "nghiên cứu kênh X" / "clone kênh X" / "phân tích kênh X"

---

## 1. KHI NÀO DÙNG PATTERN NÀY

Trigger phrases (từ user):
- "nghiên cứu kênh [X]"
- "phân tích kênh [X]"
- "clone kênh [X]"
- "làm content giống [X]"
- "học pattern từ kênh [X]"
- "đối thủ của mình là [X]"

## 2. 3-PHASE OUTPUT (PHẢI TÁCH RỜI)

User muốn xem TỪNG PHẦN riêng biệt, KHÔNG gộp 1 file lớn. Output 3 files:

### Phase 1 — Visual/Branding Analysis
**Trigger:** User nói "nghiên cứu kênh X" lần đầu

**Mục tiêu:** Hiểu phong cách hình ảnh, branding, thumbnail, title, description

**Cần làm:**
1. Browse trực tiếp channel (YouTube `/@handle/videos`, `/playlists`, `/about`)
2. Verify sub count, video count, verified badge
3. Browse 5-10 video top → lấy title + view count + duration
4. Vision_analyze ≥3 thumbnail thật (KHÔNG bịa)
5. Đọc ≥2 description VERBATIM (full text)
6. Sub-channel handles + counts (vd: Vui Vẻ Uncut @vuiveuncut 46.2K subs)
7. Affiliate/sponsor rotation pattern
8. Brand cohesion score (1-10)
9. Title formula + frequency + emoji/numbers
10. Description template (5 sections: affiliate → membership → 📌 socials → copyright → partnership)

**Tools:**
- `browser_navigate` + `browser_snapshot` + `browser_get_images`
- `vision_analyze` cho thumbnail thật
- `web_search` + `web_extract` để verify
- Dispatch subagent chuyên sâu visual nếu cần 18+ thumbnails

**Output file:**
`/Volumes/Storage-1/Hermes/wiki/concepts/youtube-channel-{handle}-{visual|branding}-analysis-YYYY-MM-DD.md`

### Phase 2 — Content/Script Analysis
**Trigger:** User nói "phân tích chi tiết nữa về nội dung" hoặc "báo cáo chi tiết về NỘI DUNG"

**Mục tiêu:** Hiểu script structure, narrative pattern, retention technique

**Cần làm:**
1. Extract verbatim SRT top hit video (yt-dlp --write-auto-sub --sub-lang vi-orig)
2. Đọc FULL SRT, phân tích:
   - Hook opening (first 30s verbatim)
   - Cam kết/Disclaimer (if any)
   - Table of contents (if any)
   - Deep dive segments (4-PHASE: định nghĩa/số liệu/case/takeaway)
   - CTA + moral (last 30s verbatim)
3. 12 chapters (nếu có)
4. Voice-over style analysis (tone, pace, slang)
5. Music/SFX inferred
6. Personal touch (xưng hô "anh em" / "tôi")
7. 3 case studies video top hit (verbatim hook + structure + retention)
8. Subagent bổ sung founder info + interview data

**Tools:**
- `yt-dlp --write-auto-sub --sub-lang vi-orig` (auto-sub trước, Whisper fallback)
- `terminal` để đọc SRT file
- `browser_navigate` để verify chapters
- Dispatch subagent content analysis (8 sections, 4000-6000 chữ)

**Output file:**
`/Volumes/Storage-1/Hermes/wiki/concepts/youtube-channel-{handle}-content-script-analysis-YYYY-MM-DD.md`

### Phase 3 — Plan + Pilot Scripts
**Trigger:** User nói "lên plan" / "clone kênh" / "feasibility"

**Mục tiêu:** Đánh giá khả thi + 3 options + plan chi tiết option được chọn + 3 pilot scripts

**Cần làm:**
1. So sánh resources channel mẫu vs project hiện tại (12 chiều)
2. Score matrix (Khả thi / ROI / Synergy) cho 3 options:
   - Option A: Clone 100% (mass-market, không tích hợp niche)
   - Option B: Adapted Clone (clone style + adapt cho niche)
   - Option C: New Direction (không clone, đi hướng riêng)
3. Plan 4-Phase 12 tháng (Foundation → Iteration → Scaling → Maturity)
4. Monetization roadmap
5. Risk analysis + mitigation
6. **3 pilot scripts VERBATIM** — chọn 3 patterns Vui Vẻ đã verify hit:
   - Misconception (top hit 1.7M views format)
   - Fact lmao (top hit 1.5M views format)
   - Simplify (top hit 903K views format)

**Tools:**
- `write_file` toàn bộ plan + scripts vào 1 file lớn
- Memory decision matrix

**Output file:**
`/Volumes/Storage-1/Hermes/wiki/projects/{project}/youtube-clone-{handle}-{option}-pilot-scripts.md`

## 3. CRITICAL RULES

### Rule 1: Khi user nói "clone X" + "giống X luôn" → DEFAULT OPTION A (Clone 100%)
- KHÔNG tự pivot sang "Adapted Clone cho niche badminton"
- Pivot CHỈ khi user explicit (vd: "làm cho kênh badminton")
- Plan 3 options luôn để user có choice, nhưng mark OPTION A as default

### Rule 2: MỖI OUTPUT PHẢI LÀ FILE RIÊNG
- KHÔNG gộp 3 phần vào 1 file duy nhất
- User đã explicit yêu cầu: "làm một báo cáo chi tiết nữa về nội dung" → tách visual/content

### Rule 3: VERBATIM QUOTES KHI CÓ
- Hook opening → quote nguyên văn từ SRT
- Description → quote nguyên văn từ YouTube
- 12 chapters → quote nguyên văn từ player
- ĐỪNG paraphrase khi user cần data thật để học pattern

### Rule 4: VISION_ANALYZE ≥3 THUMBNAIL THẬT
- KHÔNG tự mô tả thumbnail — dùng `vision_analyze` để AI nhìn thật
- Capture palette + mascot + layout + text overlay + props

### Rule 5: SRT EXTRACT QUA YT-DLP AUTO-SUB TRƯỚC
- Video VN → `yt-dlp --write-auto-sub --sub-lang vi-orig,vi --sub-format srt --skip-download`
- 2-3s download, không cần GPU
- Whisper fallback CHỈ khi không có auto-sub

## 4. TIMING BUDGET

| Phase | Time | Tools |
|---|---|---|
| Phase 1 (Visual/Branding) | 30-45 min | browse + vision + subagent |
| Phase 2 (Content/Script) | 30-45 min | yt-dlp + SRT analyze + subagent |
| Phase 3 (Plan + Scripts) | 20-30 min | write_file + memory |

**Total: 1.5-2.5 giờ cho 1 kênh** — đủ chi tiết để user quyết clone hay không.

## 5. CASE STUDY VERIFIED (@VuiVe 11/07/2026)

**Subagent timing thực tế:**
- Visual/branding subagent: 311s (5 min), 50 API calls, 18 thumbnails + 30 titles analyzed
- Content/script subagent: 331s (5 min), 13 API calls, full 8 sections
- Time spent on direct browse + SRT extract: ~30 min

**Output sizes thực tế:**
- Visual/branding report: ~30KB / 400+ dòng
- Content/script report: ~37KB / 600+ dòng
- Plan + 3 scripts: ~26KB / 3 verbatim scripts (15-20 phút mỗi cái)

**Total data extracted:** ~93KB structured analysis across 3 files

## 6. ANTI-PATTERNS

❌ **Tự pivot sang Adapted Clone** khi user nói "Clone thuần" → phải hỏi hoặc confirm trước
❌ **Gộp 3 phần vào 1 file** → user muốn xem từng phần riêng
❌ **Paraphrase hook opening** → user cần VERBATIM để học pattern
❌ **Tự mô tả thumbnail** → dùng vision_analyze để AI nhìn thật
❌ **Whisper fallback ngay** → thử yt-dlp auto-sub trước (nhanh hơn 10x)
❌ **Subagent visual/branding quá tải** → timeout risk nếu >600s. Nên cap 18-25 thumbnails
❌ **Bỏ qua Phase 3 plan** → chỉ Phase 1+2 mà không có plan là user chưa biết phải làm gì tiếp

## 7. NEXT-STEP PROMPT CHO USER

Sau khi deliver 3 files, ask user:
- Confirm tên kênh (đề xuất của em)
- Confirm mascot concept (để tránh copy mascot gốc)
- Confirm 3 pilot scripts (hay muốn viết thêm?)
- Confirm channel description template