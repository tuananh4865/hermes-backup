---
name: youtube-channel-audit
description: Deep-dive brand/visual/thumbnail/title audit of a single YouTube channel. Use when the user asks "phân tích kênh YouTube X", "channel audit", "analyze visual identity of @handle", "break down thumbnail style of channel Y", "what makes this channel tick", or wants to extract replicable branding patterns (color palette, mascot, layout, title formulas, description template, ecosystem map, playlist structure) from any YouTube channel — competitor, niche leader, or own channel for benchmark. Produces a structured 3000–5000-word markdown report in Vietnamese or English, with hard evidence (verbatim titles, view counts, screenshot-analyzed thumbnails) and NO fabricated data. Distinct from `youtube-trending-research` (platform-wide trending niches), `social-media-research` (cross-platform topic research), and `youtube-content` (transcript/script extraction).
---

# YouTube Channel Audit — Deep Visual & Branding Analysis

You are auditing ONE channel end-to-end. The deliverable is a structured markdown report that another creator could use to *replicate* the channel's visual grammar and content formula. Every claim must be backed by real scraped data — never invent counts, titles, or partner contacts.

## When to load this skill

- User asks "phân tích kênh YouTube X" / "analyze @handle" / "channel deep dive"
- User wants thumbnail style breakdown, title pattern formulas, description template
- User is doing competitive analysis for their own YouTube channel
- User asks about a specific creator's branding, mascot, color palette, ecosystem

**Do NOT use for**: trending-topic research across the platform → use `youtube-trending-research`. Single video transcript extraction → use `youtube-content`. Cross-platform topic monitoring → use `social-media-research`.

---

## Workflow (8 phases, follow in order)

### Phase 1 — Channel header & metadata
1. `browser_navigate` to `https://www.youtube.com/@<handle>/videos`
2. Snapshot the page; extract via JS the **channel name, handle, sub count, video count, slogan, verified status** — all visible on the banner.
3. The snapshot's heading element (e.g. `ref=e142`) gives the channel name; subscriber + video counts are in the same group. Capture verbatim.

### Phase 2 — Video grid scrape (last 30 videos)
YouTube renders the video grid via **closed Shadow DOM** (`ytd-rich-item-renderer`). You CANNOT pierce it with normal `querySelector` from `document` — but `el.outerHTML` exposes the rendered HTML. Use:

```javascript
JSON.stringify(Array.from(document.querySelectorAll('ytd-rich-item-renderer')).map(el => {
  const a = el.querySelector('a.ytLockupViewModelTitle, a.ytLockupViewModelContentImage');
  const metaSpans = el.querySelectorAll('.ytContentMetadataViewModelMetadataText');
  const metaAria = Array.from(metaSpans).map(s => s.getAttribute('aria-label'));
  const badge = el.querySelector('.ytBadgeShapeText');
  const thumb = el.querySelector('img.ytCoreImageHost');
  return {
    href: a?.href,
    title: a?.title || el.querySelector('h3')?.getAttribute('title'),
    views: metaAria[0],   // e.g. "732 thousand views"
    ago:   metaAria[1],   // e.g. "4 days ago"
    duration: badge?.innerText,
    thumb: thumb?.src
  };
}))
```

Pitfalls:
- YouTube mutates the grid every few weeks (current 2026 layout uses `ytLockupViewModel*` not the older `ytd-rich-grid-media`). If selectors return empty, **inspect one element's outerHTML** to find the current class names — don't hardcode from prior knowledge.
- `metaAria` returns to the page in `1 second ago` / `1 minute ago` granularity — acceptable for reporting.
- **DO NOT install a separate browser via Python/playwright just for this** — the Hermes `browser_navigate` + `browser_console` + `browser_snapshot` tools are sufficient. Re-installing a second browser is wasted effort (learned the hard way).

### Phase 3 — Download thumbnails (vision sampling)
Use `terminal curl` to download the maxresdefault JPG for each video ID. URL pattern:
```
https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg
```
Fallback to `https://i.ytimg.com/vi/<VIDEO_ID>/hqdefault.jpg` if maxres returns < 5KB (404 placeholder).

Pick **10–18 representative thumbnails** (mix of high-view, low-view, recent, sponsored, edge cases) and run `vision_analyze` on each with a **standardized prompt** asking about: background color, illustration vs photo, central mascot/character presence, text overlay (font/color/position), grid layout of items, faces policy, sponsored markers.

**Goal of vision pass**: extract the brand's *visual grammar* — what stays constant vs what changes per topic.

### Phase 4 — Verbatim title catalog (30 videos)
Build a table of all 30 titles with columns: `Pattern | Word count | Has number? | Emoji/symbol? | Has superlative? | Sponsored marker?`.

Then compute aggregate statistics:
- % of titles matching each repeating formula
- Top 10 most-frequent "hook words"
- Avg word/char length
- Emoji usage rate (often 0% for serious channels)
- Capitalization quirks (ALL CAPS for emphasis, sentence case otherwise)
- Serialization markers (`(Phần N)`, `Part N`, `(.ft X)`, `(Bản full)`)

### Phase 5 — Description template (visit 3–5 videos)
Visit the most recent + 2 highest-view + 1 sponsored video. The description lives in **closed Shadow DOM** of `<ytd-watch-metadata>`. To extract the FULL description:

```javascript
const exp = document.querySelector('ytd-text-inline-expander#description');
if (exp) exp.click();  // expand "more" button
JSON.stringify(document.querySelector('ytd-watch-metadata')?.innerText)
```

Capture verbatim. Look for the template skeleton:
- Affiliate/sponsor link first
- Membership CTA
- Cross-platform links (often with 📌 emoji bullet)
- ASCII-dash wrapped copyright disclaimer (`Bản quyền thuộc về...` / `Copyright by... Please do not Reup`)
- Partnership contact block (email + Zalo + sometimes Chinese/English line for cross-border)
- `MM:SS Topic` chapter list at bottom

### Phase 6 — Ecosystem map
From the description's cross-platform block + the channel's `About` page, build an ecosystem table:
- Main channel handle + sub count
- Sub-channels (e.g. `@handleUncut`)
- Facebook fanpage handle
- Other socials (Instagram, TikTok, Twitter) — note ABSENCE as well as presence
- Email/Zalo/phone for partnerships
- Chinese-business email if present (163.com, qq.com = intentional CN targeting)
- Recruitment page (signs of studio, not solo creator)

### Phase 7 — Playlist structure
1. Visit `https://www.youtube.com/@<handle>/playlists`
2. Extract playlist titles + IDs (use `Array.from(document.querySelectorAll('a[href*="playlist"]')).map(a=>a.href)` then dedupe)
3. For each playlist URL, `browser_navigate` to `https://www.youtube.com/playlist?list=<ID>` and snapshot — the heading + a "N videos / M views" group gives count + cumulative views.
4. Categorize playlists: **branded series** (e.g. "Fact lmao động vật", "Đơn Giản Hóa Văn Học") vs **topic buckets** (e.g. "Lịch sử", "Game", "Bóng đá").
5. Look for **duplicate / renamed playlists** (different capitalization) — channel housekeeping signal.

### Phase 8 — Synthesize report (3000–5000 words)
Structure the final markdown with these sections (in order):
1. Channel header facts (small table)
2. Thumbnail style analysis (visual elements, palette, mascot, layout, text policy, hits vs flops)
3. Title formula analysis (verbatim table of 30 + aggregate stats)
4. Description structure (verbatim sample + template skeleton)
5. Channel ecosystem (table + cross-platform notes)
6. Playlists (list + counts + categorization)
7. Overall visual & tone style
8. **Replicable takeaways** (5–10 numbered, action-oriented)

**Reporting discipline**:
- Every fact must come from real scraped data — never invent counts, names, emails, phones.
- When a phase couldn't be completed (e.g. couldn't fetch sub-channel count), say so explicitly under "Outstanding".
- Use Vietnamese if the channel is Vietnamese; otherwise match the channel's primary language.

---

## Pitfalls (read these before starting)

1. **Don't `playwright install` a second browser.** Hermes already ships browser tools (`browser_navigate`, `browser_console`, `browser_snapshot`). Use those. Installing a parallel Playwright just duplicates effort.

2. **YouTube's video grid uses closed Shadow DOM.** `document.querySelector('ytd-rich-item-renderer').shadowRoot` returns null. The rendered HTML is in `outerHTML` instead — use that or inspect a single element's outerHTML to discover current class names.

3. **`maxresdefault.jpg` sometimes 404s.** The file is 1KB (placeholder). Detect by file size < 5KB and fall back to `hqdefault.jpg`.

4. **Description is collapsed by default.** Click `ytd-text-inline-expander#description` BEFORE reading `ytd-watch-metadata.innerText`, or you get only the first ~100 chars.

5. **YouTube URLs change class names periodically.** The 2026 layout uses `ytLockupViewModel*` + `ytContentMetadataViewModel*`. Older layouts used `ytd-rich-grid-media` + `#video-title`. If your selectors return `[]`, dump one element's `outerHTML` and re-discover.

6. **Playlists are nested under `YT-PLAYLIST-MANAGER`** with further closed shadows — can't extract counts from the `/playlists` index page. Must visit each playlist URL individually.

7. **Vision analysis cost.** Sampling 15+ thumbnails is fine; 30+ burns context. Aim for 12–18 representative ones (high view, low view, recent, sponsored, different topics).

8. **Don't trust LLM summaries of YouTube pages.** `web_extract` / `mcp__exa__web_fetch_exa` cannot execute JS and return mostly empty chrome. **Always use the browser tools**, not raw fetch.

9. **Sub-channel metadata often hidden.** Sub-channel sub counts may not render unless you're logged in or they have public view counts. Report as "not extractable" rather than guessing.

10. **Watch for sponsored content that breaks the visual template.** Note the BEFORE/AFTER — sponsored videos that retain the standard template usually outperform those that don't. This is a real branding insight, not a quirk.

11. **The user wants REPLICABLE patterns, not a museum catalog.** End every report with 5–10 numbered "what to copy" takeaways for the user's own channel.

12. **Subagent timeout — ALWAYS browse fallback FIRST.** When dispatching subagents for visual/thumbnail/title/description analysis, ALWAYS have the parent agent browse the channel header + first 10 video titles + 1 description VERBATIM BEFORE the subagent finishes. If the subagent hits the 600s timeout (common on visual-extraction tasks because browser_snapshot returns huge DOM trees), the parent can still ship a high-quality report from the directly-browsed data. **Real case 2026-07-11 (@VuiVe audit):** subagent for visual/branding timed out at 600.09s with 32 API calls, but parent had already cached 12+ titles, 3 verbatim descriptions, 14 playlists, 2 vision-analyzed thumbnails, and sub-channel @vuiveuncut data — enough to ship a 22KB report without retry. **Rule:** first 2-3 tool calls in any YouTube audit MUST be `browser_navigate` to the channel's main page + `/videos` + `/playlists` — cache this data into your context BEFORE dispatching subagents.

13. **Subagent may return video IDs from the WRONG channel.** When subagent uses `mcp__exa__web_search` to find "top videos of @handle", it may return results from channels with similar content (e.g. badminton channels when target was edutainment). **Always verify** the video's `channelName` field in the search result matches the target `@handle` before including it in the report. If unsure, `browser_navigate` to the video URL and confirm channel name in the player header. Real case: subagent returned `1xCvwNWNU-w` ("Why Haven't You Improved at Badminton?") which is from **Cộng đồng cầu lông Việt Nam - VN Badminton**, NOT @VuiVe — would have polluted the report.

14. **yt3.ggpht.com avatar URLs sometimes return 400 Bad Request** when fetched with `vision_analyze`. The channel-page avatar at the `s176-c-k-c0x00ffffff-no-rj-mo` size param occasionally fails. **Workaround:** use `browser_get_images` on the channel home page (returns multiple valid sizes + paths), or try `s800` instead of `s176`, or accept that the avatar may not be analyzable and describe it from the surrounding channel-page snapshot context instead. **DON'T** waste retries on the same URL.

15. **Save audit output to wiki `concepts/`, not home root.** The user will ask for the report again in future sessions — when the file lives at `/Users/<name>/channel-audit-<handle>.md` (home root), it's invisible to wiki cross-reference, search, and the Obsidian mirror. **Always save to** `/Volumes/Storage-1/Hermes/wiki/concepts/youtube-channel-<handle>-audit-<YYYY-MM-DD>.md` with frontmatter (`type: concept`, `tags: [youtube, branding, channel-audit, <niche>]`, `relationships: [...]`). Subagents dispatched for this task tend to default to home root — explicitly tell them in the prompt "save to wiki concepts/" and verify the path on completion.

16. **Sub-channel handle discovery via YouTube search.** When the description mentions a sub-channel name (e.g. "Vui Vẻ Uncut") but only shows a raw `@UCxxd6_Bshqm...` URL, the handle is hidden. **Workaround:** `browser_navigate` to `https://www.youtube.com/results?search_query=<channel>+<subname>` — the first result usually shows the clean handle (e.g. `@vuiveuncut`) + subscriber count + verified badge. This is more reliable than the raw channel-ID URL (which often returns 404). Real case 2026-07-11: `@vuiveuncut` resolved to 46.2K subs in one search query.

17. **Dispatch 2-phase subagent pattern for deep-dive visual/branding (NEW 2026-07-11).** When task = "research sâu" + parent already shipped initial report → dispatch a SECOND subagent focused specifically on visual/branding for deeper analysis (18 thumbnails + 30 titles analyzed). This second subagent (deleg_d76451f1, 50 API calls, 311s) found insights parent missed: (a) **brand cohesion score 9/10** with breakdown, (b) **Visual A/B** — clean poster > busy infographic (903K views vs 122K), (c) **Sponsored content breaks template = fail** (CellphoneS 461K keeps template vs Kojima 122K breaks template). **Rule:** when user asks "research sâu" + parent can ship basic report → still dispatch a second focused subagent for visual/branding — the parent agent's vision_analyze is limited to 1-2 thumbnails due to context cost; the dedicated subagent can do 15-18 with consistent prompts.

18. **Incremental wiki update via patch (NOT write_file) after subagent insights (NEW 2026-07-11).** When subagent returns with new insights to merge into an existing wiki concept page, ALWAYS use `patch` (skill_manage action='patch' in background review mode) to add sections to the wiki — never `write_file`/`edit` which overwrites. The skill `youtube-channel-audit` references file `references/vuive-2026-07-11-case-study.md` follows this pattern: original 5 lessons + 4 new lessons added incrementally via patch. Each patch must verify uniqueness (no duplicate old_string). This preserves the original audit data while layering in new subagent discoveries.

19. **Phase 9 transcript extraction: PREFER `yt-dlp` over Exa (NEW 2026-07-11).** Khi Phase 9 cần verbatim transcript, dùng `yt-dlp --write-auto-sub --sub-lang vi-orig --sub-format srt --skip-download -o "/tmp/<id>.%(ext)s" <URL>` thay vì `mcp__exa__web_fetch_exa`. Lý do: (a) `yt-dlp` cho SRT verbatim trong 2-3 giây với độ chính xác cao (auto-generated Vietnamese subtitle của YouTube), (b) `Exa` cũng work nhưng chậm hơn + có cleanup artifacts nhỏ, (c) `youtubetranscript.com` bị YouTube block thường xuyên. **PITFALL:** Nếu user đã dùng Exa cho session trước (như @VuiVe transcript qua Exa) thì vẫn OK nhưng lần sau dùng `yt-dlp` cho nhanh + reliable. Real case 2026-07-11 turn 2: `yt-dlp` cho SRT 3,176 dòng trong 3 giây, đủ data để phân tích hook/outro/4-PHASE per segment verbatim.

20. **Phase 9 subagent TIMEOUT on content analysis (NEW 2026-07-11).** Subagent dispatched cho Phase 9 (content analysis với vision_analyze 15+ thumbnails + SRT processing) có thể timeout 600s. WORKAROUND: parent LUÔN cache SRT verbatim trước bằng `yt-dlp` (3 giây) → ship content analysis trực tiếp từ SRT + browser_snapshot chapters. Khi subagent timeout trên content task, parent vẫn ship được nhờ cache SRT trước. **Rule:** trong bất kỳ YouTube audit nào có content phase → parent LUÔN extract SRT bằng `yt-dlp` TRƯỚC khi dispatch subagent. SRT là data cheap (3s), visual analysis là data expensive (timeout risk cao).

21. **ALWAYS load this skill FIRST when user asks "phân tích kênh YouTube" / "channel audit" (NEW 2026-07-11 lesson từ session 2).** Em đã mắc pitfall này trong session 2 — user prompt "làm báo cáo chi tiết về NỘI DUNG" matched skill trigger, nhưng em đã skip loading skill đầu tiên → duplicate work với case study file có sẵn + miss Phase 1-8 visual/branding analysis hoàn toàn. **Rule:** LUÔN `skill_view(name="youtube-channel-audit")` đầu tiên khi user audit YouTube channel. Check case study file `references/vuive-2026-07-11-case-study.md` đã có data chưa trước khi browse.

22. **RELOAD skill before follow-up dimension on already-audited channel (NEW 2026-07-11).** When user has done a visual/branding audit on a channel, then asks a follow-up dimension (e.g. "làm báo cáo chi tiết nữa về nội dung" / "phân tích chuyên sâu về script" / "analyze content depth"), ALWAYS re-load this skill via `skill_view(name="youtube-channel-audit")` BEFORE proceeding. **Why:** Skill content auto-loaded earlier in the session may have rotated out of context (especially in long sessions with multiple skill loads or after context compression). Re-loading ensures Phase 9-13 deep-dive workflow rules (SRT extraction with yt-dlp fallback chain, confidence annotations HIGH/MEDIUM/LOW, content categories framework, case study structure, founder philosophy via press interview) are followed correctly. **Real case 2026-07-11:** User audit @VuiVe visual/branding in turn N, then asked "làm báo cáo chi tiết nữa về nội dung" in turn N+3. Em đã skip reload → did transcript extraction manually using `yt-dlp` (correct tool) but missed the structured Phase 9-13 framework already documented in skill, leading to less systematic output. **Rule:** `skill_view()` BEFORE any new audit dimension, even if "I just used it 3 turns ago". The 1-2 second reload cost is far cheaper than missing the skill's structured framework.

23. **Sample mascot/avatar image SEPARATELY from thumbnails when auditing character-driven channels (NEW 2026-07-11).** Channels with signature mascots (@VuiVe, @herocat2309, etc.) often have TWO different art styles: (a) the **mascot/avatar** (hand-drawn, consistent character, used on channel page + intro/outro) and (b) the **thumbnail illustrations** (can be more varied, may include collages + multiple characters + data viz). When user asks for style replication, ALWAYS `vision_analyze` the mascot/avatar image DIRECTLY — not just thumbnails. Real case 2026-07-11: I analyzed @VuiVe thumbnails (18 images) and concluded "2D chibi cartoon" — but the actual mascot is Western Cartoon Mỹ (Adventure Time/Gumball style) with closed/squinting eyes, square head, hand on chin, lopsided tie. Thumbnails use the mascot as one element among many others (pyramids, grids, character portraits) but the mascot ITSELF is rendered in a specific style that gets lost when analyzing thumbnails alone. **Pitfall to add:** When user says "phong cách vẽ X" or "convert my photo to cartoon like X", `vision_analyze` the COMPETITOR'S MASCOT/AVATAR image FIRST. The avatar URL is in channel metadata or homepage banner — fetch directly via `browser_get_images` on channel home, OR via `https://yt3.ggpht.com/<channel_id>=s800-c-k-c0x00ffffff-no-rj-mo` (use s800 to maximize chance of avoiding 400 errors seen with s176). NEVER conclude a style from thumbnail analysis alone when the channel uses a signature mascot.

20. **User prompt structure signals dimension scope (NEW 2026-07-11).** When user says "phân tích sâu" + asks about specific dimensions explicitly mentioned ("phong cách hình ảnh, nội dung, thumbnail, title, description" = 5 dimensions, OR "script structure, narrative, retention, content depth" = 4 dimensions) → expect user to ask FOLLOW-UP reports focused on different dimensions. Real case: anh Tuấn Anh first asked "phân tích sâu kênh @VuiVe" (general), then asked separately for visual/branding report, then content/script report. **Rule:** when first request is broad, ship 1 comprehensive report covering all dimensions but FLAG which dimensions could be deeper — then proactively offer to dispatch focused subagents for the depth areas user might ask about next. Don't wait for user to ask follow-up before offering deeper analysis.

21. **Confidence annotation (HIGH/MEDIUM/LOW) required for content deep-dive (NEW 2026-07-11).** When shipping script/narrative/retention/depth analysis from ONE verbatim transcript, you MUST flag confidence per claim. Use this scheme:
  - **HIGH**: Direct verbatim transcript evidence (quote 5+ words from transcript)
  - **MEDIUM**: Inferred from pattern across multiple videos (not direct evidence)
  - **LOW**: Caveat explicit (single sample, video deleted, no transcript available)
  - Include a "Data Confidence" appendix at end of each major section. User @VuiVe session 2026-07-11 praised this pattern (no pushback on report) → keep as standard for any content analysis without multiple-sample verification.

22. **Subagent returns may have stale summary truncations (NEW 2026-07-11).** When async delegation completes, the message you receive is OFTEN truncated to head+tail with "SUMMARY TRUNCATED" warning. **ALWAYS** read the full subagent output file at `/Users/<name>/.hermes/cache/delegation/subagent-summary-<id>-<ts>.txt` (full path in the truncated summary) before merging insights. Truncation can cut key insights in the middle. Real case: @VuiVe content subagent (deleg_0d19b218, 331s) had middle section about founder philosophy + 5 badminton content ideas — would have been missed if I trusted only the head+tail summary.

23. **Companion raw data file pattern for 3000+ word reports (NEW 2026-07-11).** When shipping a long-form report with significant verbatim evidence (transcripts, source URLs, all view counts, all timestamps), create 2 files: (a) main report `*-analysis.md` (polished, readable), (b) raw data `*-data.md` (all source material verbatim). User can deep-dive into raw data anytime without re-running audit. Saves future sessions 10-20 min of re-collection. Reference implementation: `/Users/tuananh4865/Documents/learning-english/vuive-content-deep-analysis.md` + `/Users/tuananh4865/Documents/learning-english/vuive-content-analysis-data.md`.

---

## Verification

Before delivering the final report, check:
- [ ] Channel header table has all 5 fields (name, handle, subs, videos, slogan) verified live
- [ ] At least 25 video titles captured with view + age data
- [ ] At least 12 thumbnails vision-analyzed with consistent prompt
- [ ] At least 1 full description captured verbatim with partnership contacts
- [ ] Ecosystem table includes ABSENCES (which socials they DON'T use)
- [ ] Playlist list captured with at least 2 with confirmed counts
- [ ] Final report is 3000–5000 words
- [ ] Every claim references scraped data — no invented facts
- [ ] Replicable takeaways section has 5–10 actionable items
- [ ] **If user explicitly asked for script/narrative/retention/depth dimensions**, also Phase 9-13 ran with verbatim transcript + confidence annotations

---

## Phase 9-13 — SCRIPT/NARRATIVE/RETENTION/DEPTH DEEP-DIVE (NEW 2026-07-11)

**Trigger:** User prompt explicitly mentions ≥2 trong 4 dimensions: "script structure", "narrative pattern", "retention technique", "content depth". Những dimension này KHÔNG có trong Phase 1-8 — chúng là phần "deep-dive nội dung" bổ sung. Đã verified với @VuiVe session 2026-07-11 ("Phân tích CHUYÊN SÂU về NỘI DUNG kênh YouTube @VuiVe - script structure, narrative pattern, retention technique, content depth").

### Phase 9 — Verbatim transcript extraction (CRITICAL foundation)

**Standard workflow của skill `youtube-transcript-extractor` KHÔNG work trong nhiều trường hợp** cho audit deep-dive. Fallback chain đã verify 2026-07-11 với @VuiVe:

1. **`yt-dlp --write-auto-sub --sub-lang vi-orig`** — KHÔNG dùng cho channels KHÔNG enable captions (như @VuiVe). `yt-dlp --list-subs` returns empty.
2. **YouTube built-in captions** — `youtubetranscript.com` thường bị YouTube block với error "YouTube is currently blocking us from fetching subtitles".
3. **`mcp__exa__web_fetch_exa`** với URL YouTube watch page → ✅ **WORKED**, trả về full transcript verbatim (~3000-4000 words cho video 14-15 phút, có tags "Channel", "Length", "Views", "Keywords", "Transcript"). Ưu tiên này làm fallback chính.
4. **Manual transcription** bằng `mcp_MiniMax_understand_image` trên frames video — quá chậm, không cần thiết.

**Caveat Exa transcript:** Trả về tiếng Việt đúng cách (kể cả filler words "ấ", "nhá", "ơ") nhưng đôi khi ASR cleanup nhỏ ("trong th" thay vì "trong thế giới"). Đủ tốt cho script analysis.

**EXCEPTION:** Nếu video đã bị owner xóa/private → Exa cũng fail với error `CRAWL_NOT_FOUND`. Cần dùng Wayback Machine hoặc aggregator caches.

### Phase 10 — Hook / Intro / Body / Outro micro-template (verbatim)

Sau khi có transcript, decompose thành 4 sections với verbatim quote cho mỗi phần:

```
[0:00–0:30] HOOK (verbatim 2-3 câu đầu)
[0:30–2:00] INTRO (set up topic + disclaimer + CTA community)
[2:00–X:XX]  BODY (each fact = 1 segment, decompose per-fact pattern)
[X:XX–end]  OUTRO (CTA, end screen, không có cliffhanger)
```

**Per-fact micro-template (rút ra từ transcript @VuiVe):**

```
CLAIM bold/shock (1 câu) → CONTEXT (2-3 câu) → DETAIL data (30s) → 
PUNCHLINE humor (1 câu) → RHETORICAL "ảo chưa?" → TRANSITION sang fact tiếp
```

**Vui Vẻ specific patterns to check** (rút ra từ transcript 2026-07-11):

| Pattern | Có/Không | Evidence |
|---------|----------|----------|
| Hook opener = "Sau khi làm [N] phần về [X] thì tôi..." (series callback + humblebrag) | CÓ | Transcript verbatim |
| Disclaimer "thông tin chúng tôi cũng có nhặt trên mạng thôi" upfront | CÓ | Transcript verbatim |
| Sponsor segment dài 200-400 từ verbatim spec sheet | CÓ | OPPO Find X9 Ultra transcript |
| Xưng hô "anh em" (KHÔNG dùng "các bạn") | CÓ | Transcript verbatim |
| Punchline = reduction xuống mức "ghê/thô thiển" | CÓ | Transcript "nó ỉa ra người mình ấy" |
| Cold-open teaser preview cuối video | KHÔNG | - |
| Spoken-word cliffhanger ("P2 sẽ giải thích...") | KHÔNG | - |
| Honorable mention segment | KHÔNG | - |

### Phase 11 — Confidence annotation (HIGH/MEDIUM/LOW) — NEW 2026-07-11

Mọi claim trong báo cáo deep-dive cần flag confidence level:

| Level | Khi nào dùng |
|-------|--------------|
| **HIGH** | Verbatim transcript + direct channel snapshot + interview founder |
| **MEDIUM** | Suy ra từ pattern qua nhiều video (single verbatim transcript + infer rest) |
| **LOW** | Caveat explicit (video cũ bị xóa, chỉ có 1 sample, không verify được) |

**Rule:** Cuối mỗi major section có phụ lục "Data Confidence" liệt kê từng claim với level. User đọc 3,750 từ biết ngay đâu tin được, đâu là inference. Session 2026-07-11 không bị user complain về confidence section → pattern work.

### Phase 12 — Output structure for deep-dive reports

Standard structure (verified cho @VuiVe 2026-07-11, 3,750 từ):

```
1. TỔNG QUAN CHIẾN LƯỢC NỘI DUNG (philosophy + master formulas)
2. SCRIPT STRUCTURE (hook → intro → body → outro, verbatim evidence)
3. NARRATIVE PATTERN (storytelling, analogy, ranking)
4. USP / FACT RANKING (depth, emotional hook, coverage)
5. RETENTION TECHNIQUE (pattern interrupt, curiosity loop, personal touch)
6. CONTENT DEPTH & RESEARCH QUALITY (research hours, voice-over, music)
7. CONTENT CATEGORIES (4-5 formats phân loại sâu)
8. CASE STUDY 3 VIDEO (verbatim analysis + view counts)
9. CONTENT GAP & OPPORTUNITIES (5 ý tưởng cụ thể theo pattern)
10. KEY TAKEAWAYS cho replication (5 vàng + 3 đừng)
```

**Word target:** 3,500-4,500 từ cho Vietnamese report (đủ chi tiết không quá dài). User requested 4,000-6,000 từ nhưng 3,750 cũng acceptable nếu đủ depth.

8. **Phase 9 — Script/Narrative/Retention/Depth deep-dive (NEW 2026-07-11).** Khi user explicitly asks "làm báo cáo chi tiết về NỘI DUNG" sau khi visual/branding report đã ship, mở rộng thêm 4 dimensions:
   - **9.1 — Hook analysis**: Extract SRT của 1 top-hit video → grep first 60 dòng → decompose 4 lớp (topic statement / nguồn / scope limit / disclaimer). Pattern @VuiVe: "Hôm nay chúng ta sẽ nói về [TOPIC]. Dựa trên [NGUỒN 1] + [NGUỒN 2]. Nếu sai, comment bên dưới." (academic source + disclaimer, KHÔNG "POV"/"Bạn có biết")
   - **9.2 — Per-Fact micro-template**: Mỗi segment 4-PHASE = Định nghĩa (30s) → Số liệu (40s) → Case study (40s) → Takeaway (10s). Verified từ SRT verbatim.
   - **9.3 — Outro moral + soft CTA**: Pattern "MORAL MESSAGE" + "Đừng quên đăng ký" (không aggressive)
   - **9.4 — Curiosity loop**: Mỗi segment mở loop ở đầu, close ở cuối → viewer không skip được

   **Tool cho Phase 9**: `yt-dlp --write-auto-sub --sub-lang vi-orig --sub-format srt --skip-download -o "/tmp/<id>.%(ext)s" <URL>` → SRT trong 2-3 giây. KHÔNG cần GPU, KHÔNG cần Whisper. **PREFER over Exa fetch** vì: (a) reliable, (b) 3s vs 30s, (c) không bị YouTube block như `youtubetranscript.com`.

   **Output file:** `/Volumes/Storage-1/Hermes/wiki/concepts/youtube-channel-<handle>-content-script-analysis-<YYYY-MM-DD>.md` (separate từ visual/branding report). Cross-link qua `relationships: [youtube-channel-<handle>-visual-branding-analysis-<YYYY-MM-DD>]`.

9. **Phase 10 — Sponsor integration analysis** (nếu applicable). Extract sponsor segment verbatim từ SRT (typically ở position 30-60% của video), document: (a) position, (b) duration, (c) content style (spec sheet read vs testimonial vs demo), (d) CTA pattern, (e) disclaimer presence trong spoken script (thường KHÔNG có).

10. **Phase 11 — Patterns ABSENT analysis** (negative findings quan trọng bằng positive findings). Document những pattern KHÔNG dùng: cold-open teaser preview, spoken cliffhanger, honorable mention segment, formal xưng hô "các bạn", academic citation trong spoken script.

11. **Phase 12 — Founder philosophy & business model** (nếu accessible). Search Vietnamese press (dantri.com.vn, vnexpress.net) cho founder interview → verify business model + team size + revenue strategy. Cross-reference với description contacts.

12. **Phase 13 — Companion raw data file (NEW 2026-07-11)**

**Rule:** Khi ship final report + có 3,000+ words evidence → tách riêng raw data file (verbatim transcripts, source URLs, all view counts, all timestamps) thành `*-data.md` companion. Cho phép:

- Final report gọn, đọc flow được
- Raw data check được bất cứ lúc nào
- Reuse data cho future session mà không phải re-collect

**File path convention:**
- Report: `~/Documents/<topic>/<handle>-content-deep-analysis.md`
- Raw data: `~/Documents/<topic>/<handle>-content-analysis-data.md`

**Reference implementation:** `/Users/tuananh4865/Documents/learning-english/vuive-content-deep-analysis.md` + `/Users/tuananh4865/Documents/learning-english/vuive-content-analysis-data.md` (2026-07-11).

### Lessons learned (NEW 2026-07-11)

1. **ALWAYS load `youtube-channel-audit` skill TRƯỚC khi bắt đầu bất kỳ channel audit nào.** User prompt "Phân tích kênh YouTube X" matches skill trigger description gần như verbatim. Skip loading = duplicate work đã có case study + miss Phase 1-8 visual/branding analysis. Session 2026-07-11 em KHÔNG load skill → đã re-do work có sẵn trong `references/vuive-2026-07-11-case-study.md` + miss thumbnail vision analysis (Phase 3) hoàn toàn.

2. **`mcp__exa__web_fetch_exa` thay thế được transcript services bị YouTube block.** Khi `youtubetranscript.com` fail → dùng Exa fetch với YouTube watch URL → trả về full transcript verbatim. Đã verify với @VuiVe video 14:48 = ~3500 từ Vietnamese transcript. Patched to `youtube-transcript-extractor` skill separately.

3. **Confidence annotation (HIGH/MEDIUM/LOW) là pattern reusable** cho bất kỳ research task Vietnamese nào cần evidence-based claims. Đặc biệt quan trọng khi transcript chỉ có 1 sample nhưng cần generalize pattern — flag rõ phần nào là verbatim, phần nào là inference.

4. **Standard audit scope (brand/visual/title/thumbnail) + deep-dive scope (script/narrative/retention/depth) là HAI output types khác nhau.** User cần biết trước khi start. Nếu user chỉ nói "audit" → ship standard Phase 1-8. Nếu user explicitly yêu cầu 4 dimensions (script/narrative/retention/depth) → ship Phase 1-13 (bao gồm cả standard + 9-13).

5. **Wiki save path cho deep-dive reports:** Nên save vào `/Volumes/Storage-1/Hermes/wiki/concepts/youtube-channel-<handle>-script-analysis-<YYYY-MM-DD>.md` (separate từ visual-branding analysis). Cross-reference 2 file trong frontmatter `relationships:`.

---

## Deliverable

A single markdown file (or chat reply) with the structure in Phase 8. Save to `~/.../channel-audit-<handle>.md` if the user wants it persisted. Match the user's primary language (Vietnamese for Vietnamese channels).

## References (linked)

- `references/youtube-dom-extraction.md` — concrete JS/curl snippets for extracting video grid data, watch-page descriptions, playlist URLs, thumbnail downloads, and ecosystem signals (emails, phones, sub-channels). Updated for the 2026 YouTube web layout.
- `references/vietnamese-youtube-grammar.md` — field notes on VN listicle channel title formulas, thumbnail grammar, description template, ecosystem signals, and hit-video patterns. Use as prior for Vietnamese channels; verify each claim.
- `references/vuive-2026-07-11-case-study.md` — verified reference data + lessons learned từ 2 sessions audit kênh @VuiVe ngày 2026-07-11 (visual/branding audit + script/narrative/retention/depth deep-dive). Dùng làm benchmark khi audit các kênh edutainment/facts VN khác, hoặc khi so sánh với kênh cầu lông đang xây.

## Related skills

- `youtube-trending-research` — for trending niches across the platform, not a single channel
- `social-media-research` — for cross-platform topic monitoring
- `social-media-trends` — for trend surveillance (last 30 days)
- `youtube-content` — for transcript/script extraction from a single video
- `mcp-search-workarounds` — when `web_search` returns 1027 errors; NOT relevant here (YouTube = browser, not search API)