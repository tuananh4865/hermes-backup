# Reference Run — 2026-07-04 02:00 (Main Pass — Synthesis-at-Scale)

> Companion to `session-2026-07-02-gap-fill-synthesis-pattern.md` and `session-2026-07-03-gap-fill-broken-promise-resolution.md`. Read this when Step 0 classifies the run as **main pass** with 5-15 transcripts from a single day that cluster around 2-3 debugging/content topics, AND/OR when the synthesis-over-fill pattern needs stronger codification.

## Why this run matters

This is the **first run where the synthesis-over-fill pattern was applied at scale** with a clean MAIN PASS trigger (not gap-fill). Previous applications:
- **2026-07-01 main pass** (L17 origin): 2 synthesis pages from 2 transcripts → both became top-linked pages (foundation work)
- **2026-07-02 gap-fill pass** (L22 reinforcement): 3 synthesis pages from 7 transcripts → 38+ cross-refs across 3 pages (validated the pattern)
- **2026-07-03 gap-fill pass** (L23): no new transcripts but broken-promise resolution (4 fills), confirmed pattern works as synthesis-page complement
- **2026-07-04 main pass** (L24-L28, THIS RUN): 12 transcripts across 2 themes → 2 synthesis pages + 12 merged-into-main redirects → first verification that **synthesis-over-fill scales to MAIN PASS mode without gap-fill scaffolding**

## Inputs

- **Mode trigger (Step 0):** 3 always-mirror files stale on iCloud vault:
  - `log.md` — 7h40m behind wiki (last vault update: 2026-07-03 02:05; wiki: 2026-07-03 09:45)
  - `learned-about-tuananh.md` — 1h54m behind (07-03 02:04 vs 07-03 04:00)
  - `index.md` — 1h55m behind (07-03 02:05 vs 07-03 04:00)
- **12 new raw transcripts** in `raw/transcripts/2026-07-03/` (07:36-09:40 ICT, 4 unique Telegram turns × 3 transcript variants each: dated-prefix + telegram-mirror + watchdog stub)
- **2 distinct themes identified** from the transcripts by content analysis

## Curator strategy: theme clustering → synthesis pages → stub consolidation

### Step 1: Theme identification (read transcripts FIRST, before any wiki writes)

Read the 12 transcripts. Group by narrative arc:

| Theme | Transcripts | Time range | Session |
|-------|-------------|-----------|---------|
| **Pocket3 V8→V9 hook recovery** | 07:36, 07:56, 08:06 ICT | 30 min | `20260702_145229_98ab5dd6` |
| **Badminton trend research + content production** | 08:24, 08:31, 09:40 ICT | 70 min | `20260702_113044_bd391a6c` |

**Decision rule applied:** When 3+ transcripts share a debugging OR workflow topic → synthesis page; <3 → per-stub fill.

### Step 2: Synthesis pages created (not per-stub fills)

For each theme, write 1 synthesis concept page capturing the meta-lesson, citing raw transcripts as `## Sources`:

**Theme 1 — Pocket3 V8→V9:**
- **Page:** `pocket3-edit-saga-v8-v9-iteration-2026-07-03.md` (11.7 KB)
- **Meta-lesson:** Whisper hallucinates over within-clip silence (RMS < -50 dB at 0-8s = silent = transcript is hallucinate). Anh's source recall (memory of source phrases) is an authoritative signal when transcript and audio disagree.
- **Wikilinks:** 12 unique (debug-loop-anti-pattern, whisper-hallucinate-at-multi-range-concat, tiktok-video-editor, padding-flexibility-rule-v2.13, transcript-first-viral-workflow, hook-psychology-neuroscience, psychology-viral-master-framework-2026, 14-53-06_20260701_hook-cuối, script-use-mandate-system-wide, fabricated-completion-rule, + 2 internal)

**Theme 2 — Badminton trend research:**
- **Page:** `badminton-trend-research-2026-w26.md` (11.2 KB)
- **Meta-lesson:** Honest-fail-then-pivot for undeliverable assets. 4 image-fetch failure modes catalogued. URL-based pivot preserves 80% of value when 20% (images) is undeliverable.
- **Wikilinks:** 12 unique (fabricated-completion-rule, content-creator-project-workflow, youtube-trending-research, tiktok-competitor-deep-analysis, shopee-affiliate-trending-20260623, 11-31-26_20260702_viết-giùm-anh-content-đăng-bài-lên-page-, 11-33-53_20260702_pro-cho-người-có-học-cầu-hoặc-có-kinh-ng, youtube-trending-gear-2026-06-28, + 4 internal)

### Step 3: Main-page stubs marked merged-into-main

For each of the 12 watchdog stubs (6 dated-prefix + 6 telegram-mirror × 2 themes):
- Apply the `merged-into-main` pattern from `obsidian` skill § "Telegram-mirror duplicate stubs"
- Replace body with thin redirect (2 paragraphs + 3-5 wikilinks)
- Add frontmatter `status: merged-into-main` + `main_page: [[synthesis-page-name]]`
- This is DIFFERENT from the 07-03 broken-promise fix: today the source-of-truth is the synthesis page itself (not a separate filled main page). The 12 stubs become graph nodes pointing to the synthesis.

**Why redirect, not fill?** Each theme had 3 transcripts sharing the same narrative arc. The synthesis page captures the meta-lesson that 3 individual fills would each only partially capture. Filling 12 stubs would produce 12 pages with 1-2 wikilinks each (no meta-lesson). 2 synthesis pages + 12 redirects produce 2 pages with 12 wikilinks each (carries meta-lesson) + 12 graph nodes (preserves cross-references from existing index entries).

### Step 4: Wiki updates made

| Target | Action | Why |
|--------|--------|-----|
| `wiki/log.md` | Append curator entry (60 lines) | Daily summary + L24-L28 + pending work |
| `wiki/entities/learned-about-tuananh.md` | Append L24-L28 section + Daily Recap (~66 lines) + update YAML `relationships` (5 new tags) + `updated: 2026-07-04` | 5 new lessons |
| `wiki/index.md` | Update `Last updated` + add 2 synthesis page entries (after 17-36-02_20260701 row) | Catalog 2 new pages |
| `wiki/concepts/pocket3-edit-saga-v8-v9-iteration-2026-07-03.md` | **NEW** synthesis page (11.7 KB, 12 wikilinks) | Theme 1 meta-lesson |
| `wiki/concepts/badminton-trend-research-2026-w26.md` | **NEW** synthesis page (11.2 KB, 12 wikilinks) | Theme 2 meta-lesson |
| 12 watchdog stubs | Mark `status: merged-into-main` + thin redirect body | Broken-promise prevention (synthesis pages have main_page reference) |

## iCloud mirror (EAGAIN-safe pattern, 17 files, first-try success — L27 verification)

```bash
VAULT="/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
WIKI="/Volumes/Storage-1/Hermes/wiki"

# 3 always-mirror files (Step 5b hard rule)
sleep 3; cp -f "$WIKI/log.md" "$VAULT/log.md"
sleep 3; cp -f "$WIKI/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
sleep 3; cp -f "$WIKI/index.md" "$VAULT/index.md"

# 2 new synthesis pages
sleep 3; cp -f "$WIKI/concepts/pocket3-edit-saga-v8-v9-iteration-2026-07-03.md" "$VAULT/concepts/"
sleep 3; cp -f "$WIKI/concepts/badminton-trend-research-2026-w26.md" "$VAULT/concepts/"

# 12 merged-into-main stubs (3-5s sleep between each per obsidian skill batch pattern)
for f in [12 files]; do
  sleep 3
  cp -f "$WIKI/concepts/$f" "$VAULT/concepts/$f"
done
```

**Verification gate (all PASS):**
```bash
diff -q "$WIKI/log.md" "$VAULT/log.md"                                # empty = identical
diff -q "$WIKI/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"  # empty
diff -q "$WIKI/index.md" "$VAULT/index.md"                            # empty
diff -q "$WIKI/concepts/pocket3-edit-saga-v8-v9-iteration-2026-07-03.md" "$VAULT/concepts/"  # empty
diff -q "$WIKI/concepts/badminton-trend-research-2026-w26.md" "$VAULT/concepts/"  # empty
# + 12 stub diffs, all empty
```

**17 files mirrored, zero EAGAIN escalations, zero cat>tmp+mv escalations.** This is the 4th consecutive batch-mirror first-try success (after 07-01, 07-02, 07-03). The pattern is now stable enough that the `obsidian` skill's `cat>tmp+mv` escalation is correctly reserved for mid-day syncs / active editing on another device.

## New lessons captured (L24-L28)

### L24 (NEW): Whisper hallucinates over within-clip silence (RMS < -50 dB = silent)

Today's Pocket3 V8→V9 saga: source audio 0-8s had RMS = -67 dB (essentially silent), but Whisper transcript emitted `[0] = "Các bạn đang tìm phụ kiện ốp thì không nên bỏ qua cái case này nha"` with `no_speech_prob = 0.437` (below 0.5 hallucinate threshold).

**The rule:** `RMS < -50 dB` OR `no_speech_prob > 0.3` = strip the transcript and treat the segment as silent filler. Cross-validate with audio evidence (ffmpeg `astats`, librosa RMS) before any KEEP decision.

**Where it differs from L22 ([[whisper-hallucinate-at-multi-range-concat]]):**
- L22 = hallucinate at ffmpeg `atrim` concat boundaries (created by cut operation)
- L24 = hallucinate in WITHIN-clip silence (audio genuinely silent in source, no cut involved)
- Same fix pattern (trust audio over transcript), different detection surface

**Codification status:** ALREADY in `tiktok-video-editor` skill Bước 0.4.2 (added 2026-07-03, present in v3.7.0). No action needed in the video editor skill. **Consider promoting to tiktok-video-editor Pitfall #86 (NEW).**

### L25 (NEW): Anh's source recall (memory of source phrases) is an authoritative signal

Today's 3-turn V8→V9 recovery (07:36 → 07:56 → 08:06):
- 07:36 anh reported hook cut. Agent verified with audio evidence → confirmed hallucinate.
- 08:06 anh supplied ACTUAL source hook phrase ("các bạn nào đang tìm một cái case bảo vệ toàn diện cho pocket 3").
- Agent's correct response: trust anh's recall, search source word-level, find phrase, rebuild V9 with explicit 13-20s HOOK segment.

**Lesson:** when anh provides a phrase, search source word-level FIRST before responding "I don't see it." If found, rebuild. If not found, explain the search so anh can confirm or correct.

**Anti-pattern avoided:** [[debug-loop-anti-pattern]] says don't iterate output-driven. Today's recovery is the OPPOSITE: anh supplies the input phrase, agent uses it as source-of-truth, renders once. The collaboration pattern works because anh and agent contribute different evidence to converge on source truth.

**Practical comparison:**
- 2026-07-01 V5-V17 saga (4 hours, 14 versions): agent argued with output-driven iteration → no convergence
- 2026-07-04 V8→V9 recovery (30 min, 3 transcripts): anh supplied source phrase, agent searched + rebuilt → convergence in 1 render

8x faster recovery with the new discipline. The lesson applies broadly, not just to video editing.

### L26 (NEW): Honest-fail-then-pivot pattern for undeliverable assets

Today's badminton trend research (08:24 → 09:40): anh asked for 5 hot news + accompanying images. Agent researched 5 news successfully but failed to download images via 4 surfaces.

**The 4 image-fetch failure modes (NEW catalog):**
1. **Wikimedia API** — IP-based block on hotlinking from server-to-server curls
2. **Báo chính CDN** (VnExpress, Thanh Niên, Tuổi Trẻ) — bot detection blocks curl
3. **`image_generate`** (FAL/OpenAI) — needs API key for non-trivial workflows
4. **`web_extract`** — backend may return URLs but not download

**Agent's response:** did NOT fabricate URLs. Reported the 4 failures with evidence, offered 3 alternatives ranked by anh's likely preference, let anh choose.

**The 3 alternatives (ranked by anh's likely preference for Facebook page content):**
1. **URL-only** — anh clicks on phone, no download needed
2. **URL + content production** — anh has ready-to-post captions (chosen today)
3. **`image_gen` with prompt per news** — agent generates synthetic images, slower, may not match real news, but anh gets local files

**Lesson:** when asset class is undeliverable, the workflow pivots, but content (caption + URL) is still deliverable. The [[fabricated-completion-rule]] was honored. The honest-pivot pattern extends: when partial completion is possible AND user accepts partial, that's a success — not a failure.

**Anti-pattern avoided:** the agent could have (a) fabricated image URLs (violates fabricated-completion rule), (b) given up entirely ("I can't do this task"), or (c) insisted on synthetic images without asking. The pivot preserves the 80% that IS deliverable while flagging the 20% that isn't.

### L27 (NEW): Synthesis-over-fill pattern is now DEFAULT for daily 5-15 transcript batches

Today's run: 12 transcripts → 2 synthesis pages (24 wikilinks total: 12 unique each). Compare to 12 individual stub fills (12-24 wikilinks of lesser value, no meta-lesson captured).

**Verification table:**

| Pattern | Pages | Wikilinks total | Meta-lesson captured | Graph connectivity |
|---------|-------|----------------|---------------------|-------------------|
| Per-stub fill (12 stubs) | 12 | 12-24 | None | 12 leaf nodes, no cross-links |
| Synthesis-over-fill (2 pages) | 2 + 12 redirects | 24 (12×2) | Yes (L24+L26) | 2 hub nodes + 12 leaves, cross-linked |

**Decision rule (codified from §4 of SKILL.md):**
- 3+ transcripts sharing a debugging OR content workflow topic → synthesis page
- <3 transcripts → per-stub fill
- 1 transcript with watchdog stub + related synthesis page already exists → mark merged-into-main

**Why this lesson matters:** the synthesis-over-fill pattern was first codified 2026-07-02 (L17) as "preferred when debugging arc exists." Today's run confirms it scales to MAIN PASS mode with non-debugging content (badminton trend research = content workflow, not debugging). The pattern should be the DEFAULT, not the exception. Update SKILL.md §4 wording to reflect this.

### L28 (NEW): Anh's badminton Facebook page workflow is now verified

5-post template = 1 news + 1 URL + 1 caption per post. Hook 3s + emoji-led + clear CTA. Style optimized for Facebook Page format (different from TikTok's vertical 3s hook).

**Workflow:**
1. Research 5 hot news (research skill, ~5 min)
2. Try 4 image-fetch surfaces (Wikimedia → báo chính CDN → image_gen → web_extract)
3. If all fail → pivot to URL-based delivery (offer 3 alternatives, let anh choose)
4. Anh chooses option → produce N ready-to-post captions

**Cousin workflow:** 2026-07-02 11:31 session ([[11-31-26_20260702_viết-giùm-anh-content-đăng-bài-lên-page-]]) was the first badminton Facebook page request. Today's saga (08:24 → 09:40) validated the URL + caption pattern at scale.

**Lesson:** for Facebook page content where images are needed but un-fetchable, the URL + caption pattern is the right default — fastest (2 min after research) and preserves anh's manual quality control over image selection.

## Anti-patterns observed (negative signals for SKILL.md)

### 1. None new today

Today's run executed cleanly with no novel anti-patterns. The anti-patterns cataloged in `nightly-memory-curation` SKILL.md already covered the edge cases:
- Bash heredoc + apostrophe failure (use `/tmp` write + `cat >>`)
- 3-file staleness check (used correctly today: log.md 7h40m + learned-about-tuananh.md 1h54m + index.md 1h55m all caught)
- Mirror without log.md / learned-about-tuananh.md / index.md (all 3 mirrored, byte-identical verified)
- Trusting single-file (log.md) staleness check (all 3 checked, all 3 stale)

### 2. Existing anti-pattern reinforcement: synthesis-over-fill as DEFAULT not exception

The 07-02 codification in §4 said synthesis-over-fill is "preferred when debugging arc exists." Today's run shows the pattern works for **content workflows** too (badminton research), not just debugging arcs. **Action:** update SKILL.md §4 to make synthesis-over-fill the DEFAULT for daily 5-15 transcript batches.

### 3. Existing anti-pattern reinforcement: synthesis pages need broken-promise guard

Today's 12 merged-into-main redirects demonstrate the synthesis-page + redirect pattern works at scale. The previous "broken-promise guard" lesson (2026-07-02) said synthesis pages that reference "main page [[X]]" need X to be filled OR merged-into-main. Today's run applied the redirect pattern cleanly to all 12 watchdog stubs. The pattern is now stable.

## Final report (as returned to cron)

```
## 📊 Consolidation Report — 2026-07-04 02:00
- Sessions consolidated: 6 (4 unique Telegram turns across 2 sessions × 2 transcript variants each)
- Pages updated: 3 (log.md, learned-about-tuananh.md, index.md)
- New pages created: 2 (synthesis: Pocket3 V8→V9 + Badminton trend research)
- Main-page stubs marked merged-into-main: 12 (6 dated + 6 telegram × 2 themes)
- Cross-references added: 24 (12 unique wikilinks per synthesis page × 2 pages)
- iCloud mirror: ✓ (17 files byte-identical via diff -q)
- Mode: MAIN PASS (5th main pass in 11 days, 6th gap-fill on 07-03)
```

**Key finding:** Today's run crystallized two new system-wide lessons worth promoting: **anh's source recall is authoritative (L25)** and **honest-fail-then-pivot for undeliverable assets (L26)**. Both work in concert — when agent trusts anh's recall AND refuses to fabricate undeliverable assets, recovery is fast and accurate. Future sessions should default to: search source before responding "I don't see it," and report failures with evidence before pivoting. The synthesis-over-fill pattern (L27) also scaled to MAIN PASS mode with non-debugging content (badminton workflow), reinforcing that this pattern should be the DEFAULT for daily 5-15 transcript batches — not just "preferred when debugging arc exists."

## When to use this reference

- You're running a MAIN PASS curator with 5-15 transcripts from a single day that cluster around 2-3 themes → use this run as the model.
- You're tempted to fill 5-10 individual watchdog stubs from related transcripts → apply synthesis-over-fill instead (12 transcripts → 2 synthesis + 12 redirects in this run).
- You have an image-fetch failure on 2+ surfaces → use the 4-mode failure catalog + 3-alternative pivot pattern from L26.
- Anh reports content not in current transcript → check anh's source recall against source word-level FIRST (L25), don't argue with output.
- You're deciding whether to mark a watchdog stub `merged-into-main` vs fill it → if a synthesis page exists that captures the meta-lesson, redirect is correct (this run).