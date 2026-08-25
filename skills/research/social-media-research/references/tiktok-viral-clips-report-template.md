# TikTok Viral-Clips Report — Output Template

**Use when:** parent agent asks "N hottest viral TikTok/IG Reels clips for week X" or "viral content ideas for my channel".

**Source skill:** `social-media-research` (see Common Trap #9 for the no-API-key fallback path that produces this output).

---

## File path convention

Save to: `~/research/tiktok-{topic-slug}-hot-{YYYY-MM-DD-to-YYYY-MM-DD}.md`

Examples:
- `~/research/tiktok-badminton-hot-2026-07-03-to-07-10.md`
- `~/research/tiktok-skincare-viral-2026-W27.md`

---

## Document structure

### 1. Caveats block (AT TOP — non-negotiable)

```markdown
## ⚠️ Method & Caveats (đọc trước khi dùng)

- **Search backend:** `mcp__MiniMax__web_search` (Google) — primary tool. `last30days` + `SCRAPECREATORS_API_KEY` (TikTok API) **không có key** trong profile `default`, nên không dùng được cho metadata riêng của TikTok. Last30days Python 3.13 binary cũng chưa cài (`/opt/homebrew/bin/python3.13` không tồn tại).
- **View count:** **KHÔNG truy xuất được chính xác từ Google snippet**. Các con số "Views/Likes" dưới đây là *visible engagement tính tại thời điểm tìm* (likes/share thấy trong snippet), KHÔNG phải view count tuyệt đối. Nếu làm content quyết định reach → bắt buộc check lại bằng tay trên TikTok app.
- **Confidence:** MEDIUM. URL TikTok và metadata cơ bản (creator, handle, chủ đề, ngày đăng) đều verify được từ nguồn Google/TikTok snippet. View counts gắn cờ `TBD` cần check tay.
- **Cut-off search window:** {start} → {end} (trượt ±1 ngày). Một số clip từ {pre-week} vẫn được giữ vì đang viral trong tuần focus.
- **Diversity đạt:** {N smash/trick} · {N tutorial} · {N fail} · {N product/unboxing} · {N match highlight} · {N drama/entertainment/lifestyle} (đủ đa dạng theo yêu cầu).
```

### 2. Ranked list header

```markdown
## 🏆 RANKED LIST — Top {N} viral clips tuần {start} → {end}

> Format theo spec. Views = ước lượng tối thiểu (snippets ≤7 ngày thường hit FYP → dễ >100K). Likes là số liệu thấy được từ snippet.
```

### 3. Per-clip template (repeat N times)

```markdown
### Clip {N}: {Short catchy title — focus on the hook}

- **Creator:** @{handle} ({one-line context: e.g., "top badminton influencer Phần Lan, collab chính thức với BWF"})
- **URL:** {full TikTok URL or IG Reel URL}
- **Likes:** {visible number, or TBD} | **Shares:** {TBD} | **Comments:** {visible number, or TBD}
- **Chủ đề:** {one of: smash incredible | trick shot | match highlight | tutorial skill | product review | fail funny | entertainment | drama}
- **Tóm tắt:** {1-2 sentence — what happens in the clip, the specific moment that's viral}
- **Vì sao viral:** {1-2 sentence — the hook, the trend context, the "why share" factor}
- **Adapt cho kênh {Channel name}?** **YES/NO** — {1 sentence — how Tuấn Anh would recreate/stitch/quote, or why skip}
- **Ngày đăng:** ~{YYYY-MM-DD}
```

### 4. Bonus section (3 extra beyond N)

```markdown
## 🔥 BONUS (3 clip bổ sung ngoài top {N})

### Bonus 1: {Title}
- **Creator:** @{handle}
- **URL:** {url}
- **Likes:** {n or TBD} | **Chủ đề:** {category}
- **Tóm tắt:** {1 sentence}
- **Adapt:** YES/NO · **Ngày:** ~{date}
```

### 5. Topic breakdown table

```markdown
## 📊 TOPIC BREAKDOWN

| Chủ đề | Count | Top picks |
|---|---|---|
| Smash incredible / pro level | {n} | #{clip}, #{clip}, #{clip} |
| Trick shot | {n} | #{clip}, #{clip} |
| Match highlight (rally/block) | {n} | #{clip}, #{clip} |
| Fail funny / relatable | {n} | #{clip}, #{clip} |
| Tutorial / skill breakdown | {n} | #{clip} |
| Product review / racket | {n} | #{clip}, #{clip} |

Tổng: {N + 3 bonus}. Đủ đa dạng theo spec yêu cầu.
```

### 6. Recommended adaptations (for multi-channel reports)

```markdown
## 🎯 RECOMMENDED ADAPTATIONS cho {N} kênh

### Kênh 1 — {Channel name} ({description})
**Priorty A — làm ngay tuần này:**
1. **Clip {N} ({title})** → {specific adaptation: "làm lại với ống Yonex chính hãng bán tại shop"}
2. **Clip {N} ({title})** → {adaptation}
3. **Clip {N} ({title})** → {adaptation}

### Kênh 2 — {Channel name} ({description})
**Priorty A — làm ngay tuần này:**
1. **Clip {N} ({title})** → {adaptation}
```

### 7. Next-steps / TODO for parent agent

```markdown
## 🚨 NEXT STEPS / TODO cho parent agent

1. **Verify view counts** trên TikTok app cho {N} clip top → thay `TBD` → số thực
2. **Check copyright/đạo nhái** trước khi stitch/reaction clip #{N}, #{N}, ... (đều từ tài khoản chính thức)
3. **Lên script** dựa trên `tiktok-viral-script` skill — nếu có
4. **Triangulate** cross nguồn với last30days nếu user add SCRAPECREATORS_API_KEY
```

### 8. Sources block (at the very end, brief)

```markdown
## 📡 Sources / Tool ghi nguồn

- `mcp__MiniMax__web_search` (Google search backend) — {N} queries song song trong session
- TikTok discover pages & IG Reels links trả về trong snippet
- Không truy cập trực tiếp được TikTok (no SCRAPECREATORS key, no logged-in session) — vì vậy engagement chính xác là *TBD* trong hầu hết trường hợp
```

---

## Worked example (annotated)

Real example from 2026-07-10 (badminton viral clips):

```markdown
### Clip 1: Shuttle Lands in Yonex Tube — After Years of Trying
- **Creator:** @aapopuhakkabadminton (Aapo Puhakka — top badminton influencer Phần Lan, collab chính thức với BWF)
- **URL:** https://www.tiktok.com/@aapopuhakkabadminton/video/7659692415258758422
- **Likes:** 79 (rất mới · đang tăng nhanh) | **Shares:** TBD | **Comments:** TBD
- **Chủ đề:** trick shot — milestone cá nhân
- **Tóm tắt:** Aapo đánh shuttle xuyên lưới và **rơi gọn vào ống đựng cầu Yonex** ở phần sân đối diện — trick "impossible" mà anh ấy theo đuổi nhiều năm.
- **Vì sao viral:** Hook 3s visual shock cực mạnh ("nó vào thật rồi!"), yếu tố "dream come true" + collab BWF đẩy reach.
- **Adapt cho kênh Tuấn Anh?** **YES** — làm lại với ống Yonex thật, caption "cầu vào ống chính xác = 1.000.000đ đầu tư vợt". Perfect cho dòng sản phẩm Yonex.
- **Ngày đăng:** ~2026-07-07
```

Notice the elements that make this template work:
- **Context line after handle** (e.g., "top badminton influencer Phần Lan") — gives reader 1-second context without needing a separate lookup
- **Visible engagement only, no fabrication** — `TBD` is fine; making up numbers is never fine
- **"Vì sao viral" is not just "it's cool"** — explicitly identifies the hook + shareability factor
- **"Adapt" line forces actionability** — every clip must answer "what would Tuấn Anh actually do?" Not just "this is interesting"
- **Date as `~YYYY-MM-DD`** — exact dates from snippets are sometimes fuzzy; tilde signals "approximate"

---

## Variants

- **VN-language only report**: swap English queries for Vietnamese in the search-axes list above; keep output template identical.
- **Bilingual (VN + EN creator)**: keep this template; just add Vietnamese caption suggestion under each clip's "Adapt" line.
- **Short-form (5 clips only)**: collapse "Bonus" and "Recommended adaptations" sections; keep caveats + per-clip format.
- **Weekly digest (multi-topic, 5 clips × 3 topics)**: use this template per-topic, link all in one TOC at top.
