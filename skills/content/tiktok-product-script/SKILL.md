---
name: tiktok-product-script
version: 0.13.1
author: Hermes
description: Generate a TikTok sales script from product info and images.
metadata:
  hermes:
    tags: [Tiktok, Sales, Scripting, Content, Workflow]
---

# tiktok-product-script

Takes product info + images from the user, runs a 10-phase pipeline (added Phase -1 Pre-Routing), and outputs a TikTok sales script applying 7 persuasion principles from the master framework (319 research sources). Phase -1 is a **mandatory routing check** that runs BEFORE everything else — the agent must identify which project folder to save into (shop vợt cầu lông vs kênh review lifestyle). Phase 0 is a **mandatory research step** that gathers brand/product specs from authoritative sources (Wikipedia, brand site, top reviews) before any analysis — so claims in the script are verifiable, not invented. Built around Tuấn Anh's TWO projects: `tuan-anh-badminton/` (shop vợt Yonex — 14 SKU) vs `tuan-anh-review-tiktok/` (lifestyle channel — body mist, fragrance, gadgets). Uses `web_search` + `web_extract` via MCP for Phase 0, then stdlib + Vision tool only for the remaining phases.

## When to Use

- User pastes product name + image + optional note ("cuối lô 1 cây", "5 inbox tuần qua").
- User asks for a TikTok script for a specific SKU.
- User says "viết kịch bản", "viết content", "lên script" for a product.
- User wants to apply the 7-principle sales framework to a new product.
- Trigger phrases: "kịch bản cho sản phẩm này", "viết content TikTok", "script bán hàng cho [tên]", "research kỹ sản phẩm rồi viết script".
- **User sends a TikTok video URL + asks to analyze / extract lessons (NEW v0.9.3, 21/07/2026).** Trigger: "phân tích clip này", "rút bài học", "analyze video", "extract lessons from clip", "xem clip này và rút kinh nghiệm". Workflow: download → Whisper → 5-8 frames → compare với scripts trong wiki → save lesson vào `wiki/concepts/tiktok-clip-lesson-<source>-YYYY-MM-DD.md` → apply vào script hiện có. Verified case 21/07: clip @dungkenhnghiepdu (81s, Tripod Ulanzi dạy script) → 5 bài học → fix V2A MA66 (nhồi 3 use-case → tách 1 use-case/version). Xem `references/tiktok-clip-analyze-extract-lesson.md` để thấy đầy đủ 6-step workflow.

## Prerequisites

- Product info text (name, tier, price, stock, notes).
- ≥1 product image (PNG/JPG, multiple angles preferred).
- Optional: pricing already in the project's `hub.md` (skip the math).
- Optional: prior product research cached in `<project>/products/<slug>.md`.
- Read reference framework if user asks for "master framework" by name: `wiki/concepts/sales-psychology-master-framework-2026-07-07.md`.

## How to Run

Run through the `skill_view(name='tiktok-product-script')` then call any of these scripts via `execute_code`:

```python
from hermes_tools import read_file, write_file, terminal, vision_analyze, web_search, web_extract

# Phase -1 — ROUTE the product to the right project (MANDATORY, BLOCKING)
# Run Project Routing Reference table first. If unclear, ask user ONCE.

# Phase 0 — Research product (mandatory before analysis)
results = web_search(query='"<product name>" specifications reviews', numResults=8)
content = web_extract(urls=[<top-3 urls from search>], char_limit=5000)

# Vision read of product image (3 angles recommended)
analyze = vision_analyze(
    image_url='/Users/tuananh4865/.hermes/cache/images/img_xyz.jpg',
    question='Identify visual hooks: dominant color, logo, asymmetry, what catches the eye in 0.3s.'
)

# Or batch via the orchestration script
terminal(command='python3 ~/.hermes/skills/content/tiktok-product-script/scripts/build_product_script.py --product "Astrox 99 New TOUR"')
```

The script applies 10 phases (route → research → read → extract → match awareness → detect visual hooks → choose 2-3 principles → build 11-phase blueprint → write script → cross-verify → deliver).

## Quick Reference

- Master framework: `wiki/concepts/sales-psychology-master-framework-2026-07-07.md` (319 URLs).
- Hub Tuấn Anh Badminton: `wiki/projects/tuan-anh-badminton/hub.md` (14 SKU).
- Hub Tuấn Anh Review TikTok: `wiki/projects/tuan-anh-review-tiktok/hub.md` (lifestyle channel).
- Product research cache: `<project>/products/<slug>.md`.
- 7 principles: `#1 Hook 3s` · `#2 Free>Discount` · `#3 Loss aversion 2:1` · `#4 Trigger density` · `#5 Social proof` · `#6 Fewer choices` · `#7 Reciprocity`.
- 11-phase blueprint: HOOK 3s → HOOK PRICE → SETUP → AUTHORITY → USP #1 → PROOF → SPEC → PUNCHLINE → USP #2-3 → PROSPECTIVE → CTA PUNCH.
- Output script file: `wiki/projects/<detected-project>/scripts/<product>-v1.md` (auto-routed by brand/product keyword — see Route Decision Table).
- Final delivery mode: Telegram embed (table + 3-version script + KPI list + file path).
- Worked case studies: `references/armaf-odyssey-case-study.md` (fragrance — proves Phase -1 fix) + `references/ulanzi-ma66-case-study.md` (camera gadget — proves Phase -1 holds across categories). Read BOTH before next product run.
- keep_plan.txt template + hard rules: `templates/keep-plan-format.md`.
- **Phase 0 helper**: `scripts/run-phase0-research.py` (re-runnable web_search + web_extract orchestrator).
- **Voice script verify (NEW v0.10.2, 21/07/2026)**: `scripts/verify_voice_script.py` - 8-checklist tự động cho văn nói tự nhiên. Run `python3 scripts/verify_voice_script.py <script.md>` TRƯỚC khi generate voice. Fail bất kỳ check nào → fix script trước. Checks: particles ≥5 · fragments ≥3 · forbidden words =0 · length rhythm OK · WPM ≥200 · mid-thought start (no formal opener) · no từ hoa mỹ · Vietnamese ratio ≥60%. Verified case 21/07: V4A/B/C MA66 pass all 8 checks.
- **Script 4-PART verify (NEW v0.13.0, 25/07/2026)**: `scripts/verify_script_7_checks.py` - 7-checklist cho TikTok script đã viết theo formula Problem-Solution 4-PART (HOOK→PAIN→SOLUTION→PROOF→CTA). Run `python3 scripts/verify_script_7_checks.py <script.md>` TRƯỚC khi ship script lifestyle (ốp/lenspen/body mist/máy hút bụi). Checks: (1) Từ hoa mỹ =0 · (2) Particles ≥5 · (3) Fragments ≥3 · (4) WPM 200-280 · (5) First-person ≥6 · (6) Từ cấm kỵ =0 · (7) Hook VN ≤12 từ. Verified case 25/07: script Dodoto Lux Air V3 242 lines → 7/7 PASS (sau khi sửa POV→"Góc quay từ tay").
- Product-research template: `references/product-research-template.md`.
- **Batch research workflow** (NEW v0.7.0, for 5+ products): see `references/batch-product-research-workflow.md` — parallel subagent dispatch → JSON file → batch import with citation tracking. Use when user asks "research tất cả sản phẩm" / "thông tin chính xác của toàn bộ N sản phẩm".
- **YouTube Shorts download recipe** (NEW v0.6.0, from 2026-07-07 user-download task): if user asks to download a YouTube/Shorts URL and yt-dlp fails with "no such option --js-runtimes" or "The page needs to be reloaded", see **Pitfalls → yt-dlp Download Failure Pattern** below for the 4-step fix.
- **TikTok clip analyze + extract lesson workflow (NEW v0.9.3, 21/07/2026)**: when user sends a TikTok URL and asks "phân tích clip" / "rút bài học" / "extract lessons", use `references/tiktok-clip-analyze-extract-lesson.md` for the 6-step recipe (download → audio → Whisper → frames → cross-verify → write lesson file → apply to existing scripts). Verified case 21/07: @dungkenhnghiepdu 81s clip → 5 lessons extracted → V2A/B/C MA66 fixed in same session.
- **Voice TTS workflow (NEW v0.9.7, updated v0.11.0 23/07/2026)**: khi user yêu cầu "tạo voice cho option N" / "tạo voice script" → workflow chuẩn ở `references/voice-script-tts-workflow.md`. Mặc định: edge-tts NamMinh + speed 1.2x (anh đã chỉnh 5 lần từ 1.0). Rules: KHÔNG giá, KHÔNG mã SP, PHẢI tên SP tương thích, storytelling > listing. Authentic voice (OmniVoice) cho clip hero/brand. **OmniVoice emotion tags**: 4-6 tags/script (HOOK=[surprise-oh]+[laughter], PAIN=[sigh], SOLUTION=[question-ah], CTA=[confirmation-en]). **Audio chunking fix (v0.10.3)**: LUÔN override `OmniVoiceGenerationConfig(audio_chunk_threshold=90, audio_chunk_duration=30, pad=0, fade=0)` để tránh voice bị ngắt quãng. Verified case 23/07: V4B 4 tags "rất ổn" vs V4A/C 6 tags = ngắt quãng hơn.
- **Natural voice writing (NEW v0.10.0, 21/07/2026)**: 8 bài học văn nói tự nhiên (sentence-final particles, fragments, WPM 200-250, mid-thought start...) → chi tiết ở `references/natural-voice-writing-2026-07-21.md`. Verified case: ULANZI MA66 V4 từ văn viết (V3 bị chê) → văn nói (V4 pass 23 particles, 20 fragments). User verbatim: "Cách em viết chưa giống văn nói của con người lắm!".

## Procedure

**⚠️ PHASE -1 IS BLOCKING. DO NOT SKIP. USER HAS CORRECTED THIS 2× (2026-07-07) AND INVENTORY-COMPLETENESS 1× (2026-07-16).**

0. **Phase -1 — Project Routing (BLOCKING, 10s) + Inventory Completeness Check.** Two checks before any work:

   **0a. Project routing (existing, see Route Decision Table below).** If the brand/product doesn't match a routing keyword, the agent MUST ask the user ONCE before proceeding:

   - **Default behavior is WRONG.** If the agent defaults to "tuan-anh-badminton" (because 95% of past work was badminton), it will save body mist/fragrance/lifestyle gadgets into the wrong project, forcing the user to clean up. The user has flagged this twice in one session.
   - **Ask-once rule**: when the brand/product is ambiguous or new, post a single Telegram question: *"Sp này vô shop cầu lông (`tuan-anh-badminton`) hay kênh review lifestyle (`tuan-anh-review-tiktok`) anh?"* — wait for the user's reply, then continue.

   **0b. Inventory completeness check (NEW v0.7.0, from 2026-07-16 session).** When the user asks "em có những sản phẩm nào" / "lên danh sách sản phẩm" / "phân tích các nội dung TikTok", ALWAYS scan the actual rendered artifacts FIRST, not the curated wiki subset:
   - Run `os.listdir('/Volumes/Storage-1/Pocket3/Hermes-Edit/')` → parse `.mp4` filenames to extract distinct product names → group by category (regex pattern `clip_[A-Z0-9]+_V\d+_troncau_(.+)\.mp4`).
   - Then cross-check against `wiki/projects/<project>/products/*.md` (curated subset with research).
   - **Why**: the wiki only tracks products with full Phase 0 research + script (typically 2-5 files per project). But the user may have rendered 12+ distinct product clips without ever asking the agent to research them. Listing only the wiki-tracked subset gives a misleading "complete" answer — the user has to correct with "có nhiều sản phẩm hơn vậy mà". Verified case 2026-07-16: Hermes-Edit had 55 rendered mp4 across 12+ product categories; wiki only had 2 entries → user caught the gap immediately.
   - **Rule**: disk artifacts = ground truth, wiki = curated research layer. Inventory answers always come from disk first, then wiki enrichment (Phase 0 research, prices, specs).
   - **Anti-pattern**: when user asks "phân tích các nội dung TikTok mà anh đang làm", listing the 2 wiki-tracked products as the answer. WRONG. User wants the COMPLETE picture of what they've actually been doing, not the curated subset.

   **0c. Route decision table** (use this AFTER 0a/0b, before any default):

   | Brand / Product keywords | Project folder (use these paths) |
   |---|---|
   | Yonex, Astrox, ArcSaber, AX77, AX88, 65z, 65z4, Power Cushion, Subaxia, vợt cầu lông, giày cầu lông, cầu lông, badminton | `wiki/projects/tuan-anh-badminton/` (shop) |
   | ARMAF, Lattafa, body mist, fragrance, nước hoa, EDP, EDT, deodorant spray, skincare, dầu gội, lifestyle gadget, phụ kiện điện thoại, máy hút bụi, Pocket 3, camera tripod, gimbal accessories, action cam mount | `wiki/projects/tuan-anh-review-tiktok/` (channel) |
   | Anything not matching the two rows above | **ASK USER** (do NOT default) |

   - Once routed, ALL subsequent phases save into `<detected-project>/products/` and `<detected-project>/scripts/`. Never mix folders across projects.
   - **What NOT to do** (verified anti-pattern 2026-07-07): default to the most-recent project ("tuan-anh-badminton" because that was last) → user has to flag and force-create `tuan-anh-review-tiktok/`. The cost of asking once is 30s of typing; the cost of wrong routing is 5-10 min of cleanup.
   - **Verified success cases** (see references/): ULANZI MA66 Pocket 3 tripod routed correctly on first try via "Pocket 3" + "lifestyle gadget" + "camera tripod" keyword match → row 2.

1. **Phase 0 — Research Product (1-2 min, MANDATORY).** Before touching images or pricing, gather authoritative facts about the product so every claim in the script is verifiable:
   - **Brand & origin**: `web_search(query="<brand name> Wikipedia")` → land on Wikipedia, confirm country, founding year, ownership (e.g. ARMAF = Ả Rập Thống Nhất, 1999, niche fragrance >50 quốc gia).
   - **Product specs**: `web_search(query="<product full name> specifications")` → top result is usually the brand's own page or a manufacturer PDF. Capture: volume (ml / gram), weight, dimensions, materials, key technical features.
   - **Real social proof**: `web_search(query="<product name> review site:reddit.com OR site:tiktok.com")` AND `web_search(query="<brand> customer testimonials")` → scan 3-5 reviews to extract specific numbers ("anh em inbox hỏi size", "30 ngày có 4.4K người mua"). Use only verifiable claims; reject unverifiable ones.
   - **Comparables**: `web_search(query="<product> vs <competitor>")` → grab 1-2 factual differentiators (size, price tier, fragrance note, tech feature).
   - **Bonus/quà tặng**: read the product image (Phase 3) for visible bundles — never invent quà. Capture exactly what's shown on the listing.
   - **Self-claim handling** (NEW in v0.5.0): if a source is the brand's OWN official site making a market position claim (e.g. "ULANZI Global No.1 Camera Accessories" — verified only via ulanzi.com, no third-party), flag with ⚠️ in the research cache AND cap usage to 1 mention/clip. Don't repeat self-claims 3+ times — that's market-level advertising, not verifiable fact.
   - **Output**: a `product_research` table (8-12 rows) with citations like `[1]` mapped to a sources list at the bottom. Save to `wiki/projects/<detected-project>/products/<slug>.md` for re-use on future scripts. The `<detected-project>` value comes from Phase -1.
   - **Reject rule**: if any category above (brand / specs / social proof / comparables) returns zero usable sources, say **"No data"** in that row. Do **not** invent. The script will skip principles that depend on missing data.
2. **Phase 1 — Read & Extract (30s).** Read product info. For each image, call `vision_analyze(image_url=<path>, question="Identify visual hooks: dominant color, logo, asymmetry, what catches the eye in 0.3s.")` and write the result alongside name/tier/price/stock. If the detected project's `hub.md` has the SKU, reuse pricing instead of re-parsing.
3. **Phase 2 — Match Awareness Level.** Pick one of Schwartz's 5 levels (Unaware → Most Aware). Decision tree: new product → Level 1-2; bestseller → Level 3-4; low-stock/clearance → Level 5.
4. **Phase 3 — Visual Hook Detection.** From vision output, list the 1 "wow factor" (asymmetric cue) + 3-4 trigger cues. Cue sets vary by project (cầu lông: sân đơn / sân đôi / tập / thi đấu; lifestyle: gym / cafe / đi biển / đi học; camera gadget: cắm trại / du lịch / quay vlog / cafe / gym).
5. **Phase 4 — Pick 2-3 Principles.** Per product situation, choose at most 3 of 7: new → `#1 + #4 + #7`; clearance → `#1 + #3 + #5`; bestseller → `#1 + #4 + #6`; premium → `#1 + #5 + #7`. Never exceed 3 (trigger fatigue). **Empirical pattern from 2 case studies**: #1 (Hook 3s) + #5 (Social proof) appear in every successful combo; #4 (Trigger density) is the 3rd wheel when the product has 3+ use cases. Use this as a default when product situation is ambiguous.

   **Default combo for V2 Problem-Solution formula (codified 16/07/2026, verified across ARMAF Odyssey V2 + MagSafe + K&F/Body Mist Lemony scripts):** **`#1 Hook 3s` + `#3 Loss aversion` + `#5 Social proof`**. Why: hook delivers the concrete problem, loss aversion converts the "tiếc tiền / mất shot / bay mùi" framing into action, social proof (brand authority / verified reviews / shelf availability / ratings) closes the trust gap without requiring expert claims. The V1 Authority-era matrix above (`new/clearance/bestseller/premium` rows) is V1 — for V2 Problem-Solution scripts, prefer the `#1+#3+#5` combo unless the product situation explicitly demands otherwise (e.g. premium limited-edition might swap #5 for #7 reciprocity, multi-use-case lifestyle gadget might use #4 trigger density).
6. **Phase 5 — Build 11-Phase Blueprint.** Fill the table at `references/11-phase-blueprint.md` with principle tags per row + target word-count per phase.
7. **Phase 6 — Write the Script.** Output as a `keep_plan.txt`-style file: one `KEEP hh:mm.SSS-hh:mm.SSS | "<phrase>"` line per phase. Rules: no câu treo, hook ≤8 từ, CTA punch ≥10s, ≥1 keep with loss-aversion cue, ≥1 keep with concrete social proof. **Every claim that mentions a number, brand, country, or spec must trace back to Phase 0 research** — never invent.
8. **Phase 7 — Cross-Verify 4-Dimension.** PASS gate on câu treo / hallucinate / loop / principle-coverage. If any FAIL, fix and re-verify before delivering — never ship a flawed script.
   - **Câu treo**: any keep with no complete predicate → rewrite or drop.
   - **Hallucinate**: source level agreement for each claim (skip if `no_speech_prob > 0.3` or audio RMS < -50dB).
   - **Loop**: per-keep duration 4-12s, no repetition pattern across keeps.
   - **Principle coverage**: ≥1 keep per chosen principle inside the chosen principles list.
   - **Cross-reference Phase 0**: every spec / number / brand claim in the script must map to a `[N]` citation in the Phase 0 research file. Drop or rephrase any claim without backing.
   - **Hook word-count gate (≤8 từ)**: count words in Phase 1 keep. If >8, rewrite before delivering. Verified cases (2× in 2026-07-07): ARMAF V1B ("30 ngày qua 4.4K anh em inbox shop chính hãng mua chai ARMAF này" — 14 words → compressed to 8) and ULANZI V1C ("Cô ấy quay Pocket 3 ở sa mạc một mình - chỉ cần cây 75g này" — 14 words → compressed to 8). Watch for filler phrases ("anh em ơi", "nha anh em") that pad without adding info.
   - **Self-claim repetition check** (NEW v0.5.0): if a Phase 4 contains a brand self-claim (e.g. "brand X is #1 globally"), that exact phrasing may NOT appear in any other phase of the same version. Cap = 1 mention/clip.
   - **Verified examples** — citation map from 2026-07-07 runs: ARMAF Odyssey (5 web citations + 1 shop listing) and ULANZI MA66 (13 web citations + 7 shop-side stats). Read `references/armaf-odyssey-case-study.md` + `references/ulanzi-ma66-case-study.md` for the full worked examples.
   Run the verification via `execute_code` after writing the script.
9. **Phase 8 — Deliver.** Embed 11-phase table + 3-version script (tư vấn 1-1, viral TikTok, storytelling) in Telegram reply. Save file to `wiki/projects/<detected-project>/scripts/<product>-v1.md`. Provide 5 KPI hooks: hook-rate 3s · completion 70% · comment volume · inbox "keyword" · conversion→order. Also embed a 1-line "Sources" pointer that says "X citations backing this script are in `wiki/projects/<detected-project>/products/<slug>.md`".

## Pitfalls

- **Skip Phase -1 routing = repeat mistake.** User flagged wrong routing 2× in one session (2026-07-07). Phase -1 is BLOCKING — never default to "most recent project".
- **User liệt kê SP nhưng KHÔNG rõ tên chính xác → SCAN scripts có sẵn + Hermes-Edit TRƯỚC khi hỏi brand (NEW v0.13.0, 2026-07-25, from session "ốp K&F + body mist Armaf Limoni + clean pen K&F + Dodoto").** User verbatim feedback 25/07: *"Tìm tên sản phẩm dựa theo script của anh mà làm!"*. Anti-pattern (FAIL case 25/07): em nhận list 4 SP từ user → đọc sơ tên → thấy wiki stub "Body Mist Lemony" → đoán luôn là ARMAF → hỏi user "ARMAF Odyssey hay brand khác?". SAI. Đúng phải là: (1) scan `wiki/projects/<project>/scripts/*.md` để tìm SP từng có script; (2) scan `/Volumes/Storage-1/Pocket3/Hermes-Edit/` filenames để extract tên SP đã render; (3) match với tên user vừa nói; (4) nếu ambiguous, mới hỏi user với options CỤ THỂ từ data scan được (không phải hỏi chung chung). **Why**: user đã có wiki scripts trước — user tin rằng scripts của user là source-of-truth cho tên SP, không phải em đoán từ stub wiki. **Fix workflow (3-step TRƯỚC khi hỏi brand)**:
  1. `search_files` pattern trong `wiki/projects/<project>/scripts/` + `products/` → list các SP đã có trong project.
  2. `terminal(command="ls /Volumes/Storage-1/Pocket3/Hermes-Edit/ | grep -iE '<keyword>'")` → parse filenames `clip_NNNN_V<N>_<SP>.mp4` để extract SP names.
  3. Cross-reference tên user vừa liệt kê vs (1) + (2) → trình bày cho user dạng "Anh có 3 SP trùng tên 'Lemony' trong wiki + Hermes-Edit: BODYMISS Funky Fresh (52K), Sol de Janeiro Limonada (350K), Lush Lemony Flutter (850K). Anh muốn em viết brand nào?".
  
  Lý do giảm friction: user đã có context wiki — đừng ép user nhớ lại tên SP đầy đủ. Em chủ động scan + show options = user chỉ cần pick. Verified case 25/07: user list 4 SP, em đoán Body Mist = ARMAF sai. Nếu scan trước → thấy file `body-mist-amap-thom-mat.md` + Hermes-Edit `clip_0029_V1_BODY_MIST` + Hermes-Edit `clip_0037_V2_BODY_MIST_AMAP` → biết "Lemony" trong Hermes-Edit có thể là BODYMISS/Amap thay vì ARMAF → hỏi user với 3-4 options cụ thể.
- **Phase -1 inventory completeness gap (NEW v0.7.0, 2026-07-16).** When user asks "em có những sản phẩm nào", don't list only the 2 wiki-tracked products (ARMAF + Ulanzi MA66). The user has likely rendered 12+ distinct product clips in `Hermes-Edit/` that have NO wiki research yet. Scan the disk artifact path first (`os.listdir('/Volumes/Storage-1/Pocket3/Hermes-Edit/')`), parse filenames to extract distinct product names, THEN enrich with wiki metadata. Disk = ground truth, wiki = curated research layer. Anti-pattern: confidently listing 2 products as "the answer" when the actual count is 12+.
- **Skip Phase 0 = bịa data.** Without research, the script will claim specs/brands/numbers that aren't real. Always run Phase 0 first; if research fails, output "No data" instead of inventing.
- **Self-claim trap** (NEW v0.5.0, from ULANZI case): brand official site self-claims like "Global No.1" are not third-party verified. Cap at 1 mention/clip and flag ⚠️ in Phase 0 research. Repeating a self-claim 3+ times in the same script is market-level advertising, not factual persuasion.
- **Vision tool blind to text-only brand claims.** Combine vision output with Phase 0 research + hub.md pricing, not vision alone.
- **Principle overload (7/clip) = trigger fatigue.** Hard cap = 3 per clip.
- **CTA < 10s = conversion drop ≥70%** (Kahneman-Tversky loss aversion 2:1 / Ariely zero-cost bias). Always ≥10s end.
- **Generic hooks ("Trời ơi...") underperform.** Replace with concrete number or specific situation (Berger & Milkman 2012 NYT 6,956 article data).
- **Awareness level mismatch.** Don't address an "unaware" viewer with "Astrox 99 vs Gen 2" comparison — wrong ladder rung.
- **Hallucinated social proof.** Never invent names/counts; use only verifiable data from Phase 0. If no data, drop the principle.
- **Telegram delivery mode = LUÔN LUÔN GỬI FILE QUA TELEGRAM (HARD RULE v0.13.1, 25/07/2026 — user verbatim: "phải luôn luôn gửi file qua telegram cho anh chứ không được gửi path không vì đa phần anh sẽ làm việc với em qua telegra điện thoại!")**. Khi user yêu cầu viết N scripts (1 hoặc N≥2):
  - **Bước 1**: Viết từng script vào file riêng trong `wiki/projects/<project>/scripts/` (giữ nguyên format file gốc).
  - **Bước 2**: Nếu N≥2 → GỘP thành 1 file duy nhất `/Volumes/Storage-1/Hermes/scratch/<N>-scripts-batch-YYYY-MM-DD.md` (user verbatim "Viết hết vào một file"). File gộp có: (a) Overview table so sánh N SP; (b) Common formula reference; (c) Full content N SP, mỗi SP là 1 H1 riêng.
  - **Bước 3**: Gửi qua Telegram bằng syntax `MEDIA:/absolute/path/to/file.md`. Đây là cách duy nhất anh đọc được trên điện thoại.
  - **Bước 4**: KHÔNG BAO GIỜ chỉ gửi path dạng `/Volumes/Storage-1/...` — anh sẽ không mở Mac để đọc.
  - **Verify trước khi gửi**: file size > 0 (`ls -la <file>`), file readable, content đúng spec.
  - **Anti-pattern (VI PHẠM 25/07/2026)**: em gửi 3 path riêng cho Dodoto/ARMAF Limoni/K&F PT61 → anh phải nhắc lại mới gộp thành 1 file `3-scripts-batch-2026-07-25.md`. ĐÚNG: gộp 1 file rồi gửi 1 MEDIA. Self-check trước reply: nếu response có `N ≥ 2 paths to .md files` → CHƯA gộp, làm lại.
  - **Self-check formula trước send**: `grep "MEDIA:/" response` → nếu 0 match + N ≥ 2 .md paths → VI PHẠM rule, gộp file + re-send.
- **Cite-after-the-fact = decoration.** Phase 0 citations must be collected BEFORE writing the script, not added later as window dressing.
- **Hook word-count fail = write-then-verify anti-pattern (NEW v0.9.0, 2026-07-21, from ULANZI MA66 V2 session).** Em viết xong 3 hook 11-13 từ rồi mới verify → phải patch file 2 lần để nén xuống ≤8 từ. **Fix**: TRƯỚC khi viết mỗi version, count word ngay trong draft phase (KHÔNG đợi đến bước verify). Hook phải ≤8 từ TRƯỚC khi viết tiếp Pain Depth → Solution. Self-check formula: viết 1 câu → `len(text.split())` → nếu >8 → rewrite NGAY. Verified case: ULANZI MA66 V2A hook "Quay vlog Pocket 3 một mình - chân nặng, balo thêm 2 ký" (12 từ) phải nén 2 lần thành "Quay vlog - balo + 2 ký tripod" (8 từ) → lãng phí 1 patch cycle. Better: viết hook 6-8 từ NGAY từ đầu, save patch cho Phase 7 verify.
- **V1+V2 coexistence rule (NEW v0.9.0, 2026-07-21, from ULANZI MA66 session).** Khi user yêu cầu V2 (Problem-Solution) cho sản phẩm đã có V1 (Authority) trong wiki, **KHÔNG GHI ĐÈ V1**. Save thành file MỚI `<slug>-problem-solution.md` (hoặc `-v2-problem-solution.md`) SONG SONG với V1. Lý do: V1 Authority vẫn phục vụ audience thích chuyên gia; V2 Problem-Solution phục vụ audience thích "người thật". A/B test cả 2 thường → scale version thắng. Verified case 21/07: ULANZI MA66 có V1 (Authority, 13 citations) → viết V2 (Problem-Solution, 3 hook ≤8 từ) song song. Đọc thêm `references/ulanzi-ma66-problem-solution-case-study.md` để thấy đầy đủ decisions + lessons.
- **7 psychology principles → 3-version mapping (NEW v0.9.0, 2026-07-21).** Khi user explicit yêu cầu "kết hợp tâm lý học hành vi" / "apply behavioral psychology" / "use psychology framework", KHÔNG chỉ chọn 3 principles random. Map theo vấn đề anchor:
  - Vấn đề "mang vác / di chuyển" → #1 Hook + #3 Loss aversion (mất gì?) + #6 Fewer choices (1 thay nhiều)
  - Vấn đề "setup chậm / miss shot" → #1 Hook + #5 Social proof (verified quote) + #7 Reciprocity (freeship = 0 rủi ro)
  - Vấn đề "đầy đủ / đa năng" → #1 Hook + #4 Trigger density (4 use-case) + #5 Social proof (số đã bán + rating)
  - Vấn đề "giá rẻ / deal tốt" → #1 Hook + #2 Free > Discount (freeship + hoàn tiền) + #5 Social proof
  Rule này giúp Phase 4 chọn principles theo INTENT thay vì brute-force. Kết hợp với combo `#1 + #3 + #5` default (codified 16/07) → swap `#3`/`#5` ra nếu vấn đề anchor khớp principle khác tốt hơn.
- **Văn nói đời thường vs từ hoa mỹ (NEW v0.9.1, 2026-07-21, from ULANZI MA66 V2 session).** User verbatim feedback 21/07: *"Viết bằng văn nói đời thường thôi đừng dùng tư hoa mỹ quá!"*. Anti-pattern (FAIL case): em viết bản đầu dùng "sensory", "POV", "flat lay", "nam châm tủ lạnh", "Magnetic N52", "1/4 inch", "không cinematic" → phải rewrite toàn bộ 3 version. **Fix**: TONE rule mới (xem section "🗣️ TONE RULE: VĂN NÓI ĐỜI THƯỜNG" ở v0.3.0 Problem-Solution). Checklist self-check trước deliver: grep file script cho danh sách từ hoa mỹ → PHẢI = 0 match. Verified PASS case 21/07: ULANZI MA66 V2 sau rewrite có 0 từ hoa mỹ + 38 markers văn nói (thôi/luôn/rồi/nha/đó/mình/inbox). Hook word-count gate CHỈ dành cho tiếng Anh ≤8 từ; tiếng Việt cap ≤12 từ vì từ phụ thuộc nhiều hơn.
- **MỖI VIDEO CHỈ 1 NHU CẦU (NEW v0.9.2, 2026-07-21, from clip @dungkenhnghiepdu 81s).** Verified case 21/07: ULANZI MA66 V2A em vẫn nhồi 3 use-case trong 1 version ("quay cafe sáng + đi cắm trại + vlog đi bộ") → sai theo clip dạy script. Anti-pattern (FAIL case): "Mình quay cafe sáng, đi cắm trại cuối tuần, đi bộ vlog - một cây xài hết" ← 3 use-case trong 1 câu, KHÔNG giải quyết tới nơi tới chỗ. **Fix (NEW v0.9.2)**: Mỗi version chỉ anchor 1 NHU CẦU duy nhất, các use-case khác → tách thành version riêng. Verified PASS case: V2A sửa thành "Đi cafe sáng mà cần quay, lấy trong balo ra, dựng lên là xong" ← chỉ 1 use-case (bỏ balo). 3-version mapping theo 3 NHU CẦU khác nhau chứ không phải 3 use-case của cùng 1 nhu cầu. Self-check: đếm số use-case trong version — nếu >1 → TÁCH version. Nguyên tắc gốc từ clip Dũng Kênh Nghề Đủ: *"Một sản phẩm anh em chỉ cần khai thác một nhu cầu của khách thôi. Và giải quyết nó tới nơi tới chỗ."* Lesson này ở `wiki/concepts/tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md` (10.3KB, transcript + 5 bài học + script cải tiến).
- **Analyze existing clip + extract lessons workflow (NEW v0.9.3, 2026-07-21).** Khi user gửi TikTok video URL + yêu cầu "phân tích" / "rút bài học" / "extract lessons", workflow 6-step BẮT BUỘC: (1) Download bằng `yt-dlp` → save vào `/Volumes/Storage-1/Hermes/scratch/tiktok-anh-tuan/lesson-YYYY-MM-DD/raw.mp4`; (2) Extract audio 16kHz mono → Whisper `mlx-community/whisper-medium-mlx` (KHÔNG dùng large-v3, hallucinate); (3) Extract 5-8 frames bằng `ffmpeg -ss <t> -i` → vision_analyze; (4) MẮT (vision) + TAI (transcript) cross-verify; (5) Viết bài học vào `wiki/concepts/tiktok-clip-lesson-<handle>-YYYY-MM-DD.md` (transcript + N bài học + so sánh với scripts hiện có + script cải tiến); (6) Apply lesson vào scripts đang có. Verified case 21/07: clip 81s từ @dungkenhnghiepdu → 5 bài học + fix V2A/B/C MA66 ngay trong session. Anti-pattern: chỉ "xem qua rồi tóm tắt vài dòng" → KHÔNG có file lesson → KHÔNG thể apply. Xem chi tiết `references/tiktok-clip-analyze-extract-lesson.md`.
- **Anh Luật chứng khoán new-product-only (NEW v0.9.3).** Khi user gửi clip MỚI (chưa có trong wiki), agent KHÔNG chỉ trả lời phân tích ngắn gọn. Phải: download, transcribe, save lesson file (vĩnh viễn trong wiki), update SKILL nếu có PITFALL mới, fix script đang có nếu applicable. Tại sao: lesson clip viral có nhiều bài học cô đọng — 1 dòng tóm tắt trong chat = mất 80% giá trị. Verified anti-pattern: nếu em chỉ nói "clip hay, 5 bài học chính: A, B, C, D, E" → anh phải tự apply → em không giúp ích gì. ĐÚNG: save lesson file + tự apply vào script hiện có + báo cáo "đã fix X version Y".
- **Markdown blockquote over-engineer (NEW v0.9.4, 2026-07-21, from ULANZI MA66 V2 fix session).** Em đã sửa format blockquote 6 lần (add `*"` → thừa `"*` → revert → add lại → final clean) — pure waste. **Fix (HARD RULE)**: Khi viết script trong markdown, dùng `> *<text>*` đơn giản cho MỖI câu trong multi-line blockquote. KHÔNG cần quote mở `"` ở đầu dòng đầu + quote đóng `"` ở cuối dòng cuối. Đơn giản nhất:
  ```markdown
  > *Câu 1*
  > *Câu 2*
  > *Câu 3*
  ```
  Tránh:
  ```markdown
  > *"Câu 1*
  > *"Câu 2*
  > *"Câu 3"*
  ```
  Cái sau render OK nhưng phải đếm quote balance, dễ thừa/thiếu. Verified case 21/07: em đã over-think format khi đáng lẽ chỉ cần `> *<text>*` đều nhau. Lesson: Đơn giản nhất có thể. Nếu render OK thì KHÔNG đụng vào.
- **Problem-solution listing-UP không thu hút (NEW v0.9.5, 2026-07-21, from ULANZI MA66 V3 session).** User verbatim feedback 21/07: *"cả 3 kịch bản này anh thấy đều không thu hút"*. Anti-pattern (FAIL case): em viết 3 version V2 theo formula 4-PART (Hook pain → Pain 3 vấn đề → Solution liệt kê USP → Proof số liệu → CTA) → tất cả đều có cấu trúc "liệt kê USP của sản phẩm" → anh feedback "không thu hút". Vấn đề cốt lõi: problem-solution listing = cấu trúc sales pitch kinh điển, người xem TikTok bị expose hàng ngày, KHÔNG khác biệt. **Fix (NEW v0.9.5)**: Khi viết script TikTok lifestyle, MẶC ĐỊNH dùng **STORYTELLING structure** thay vì listing — 1 trong 3 pattern:
  - **Personal story** ("Hai năm làm video, có một thứ mình ước biết sớm hơn")
  - **Other-person story** ("Cô bạn mình đi Đà Lạt, nó bảo sao không biết sớm")
  - **Emotional visceral** ("Con mình cười lần đầu, mình còn cái clip 30 giây chỉ thấy trần nhà")
  
  Mỗi version = 1 storytelling pattern khác nhau. Hook mở bằng intrigue ("có một thứ mình ước biết") hoặc emotional pain visceral, KHÔNG mở bằng pain point sản phẩm. CTA = emotional punch line ("cái này không phải tripod bình thường, nó là để mình không bỏ lỡ khoảnh khắc"), KHÔNG phải "inbox tư vấn". Verified PASS case 21/07: V3A/B/C storytelling đã gửi, anh chưa approve/reject — coi như baseline mới. **EXCEPTION**: Khi user explicit yêu cầu "viết problem-solution" / "viết theo công thức V2 cũ" → dùng lại 4-PART listing.

**🔗 9-KEY STRUCTURE cross-ref (added 2026-08-24 weekly light update):** 3 storytelling patterns trên align với KEY 9 STRUCTURE từ `wiki/concepts/full-dimension-9-key-extraction-2026-08-15.md`:
- Emotional pain opening ↔ **Pattern A: Question Hook + Pain-Solution + CTA** (ZSV8uD4bB, 3.54% save)
- Curiosity/intrigue opening ↔ **Pattern B: Myth + Truth + Insight** (ZSV8udeW9, 2.48% save)
- Direct step + demo CTA ↔ **Pattern C: Direct Step + Demo + Save CTA** (ZSV8uG5hB, 5.45% save)

Khi viết script mới, chọn 1/3 pattern theo sản phẩm + audience. Avg clip 30s = 3 parts 10s each. Otherwise → storytelling mặc định.
- **Voice script: KHÔNG nêu giá + KHÔNG gọi mã SP (NEW v0.9.5, 2026-07-21, from MA66 V2 voice session).** User verbatim 21/07: *"Không nêu giá và mã sản phẩm! Sản phẩm là tripod thì gọi nó là chiếc tripod này thôi không gọi mã ma66 ai hiểu?"*. HARD RULE khi viết script cho voice/TTS (KHÔNG phải script visual trên video):
  - **KHÔNG nêu giá** trong voice (599k, 67k/tháng, freeship+14% — để visual overlay/text on screen làm)
  - **KHÔNG gọi mã sản phẩm** (MA66, Pocket 3, ARMAF, Lattafa) — gọi tên gọi chung "chiếc tripod này", "chai body mist này", "chiếc lens này"
  - Voice chỉ nói NHU CẦU + CẢM XÚC + LỢI ÍCH — để giá/mã hiện trên overlay text.
  - Lý do: người xem TikTok KHÔNG biết mã sản phẩm, nghe mã sẽ confused; giá đọc visual nhanh hơn voice.
  
  Khi viết script cho voice (text_to_speech / edge-tts / file TTS) → áp dụng rule này. Khi viết script visual (text overlay + visual cue) → KHÔNG cần apply, vẫn ghi mã SP đầy đủ cho overlay. Verified case 21/07: em đã viết V2A/B/C voice có giá + mã → anh feedback → rewrite V3A/B/C storytelling voice bỏ giá + mã.

- **Voice script: PHẢI nhắc tên sản phẩm TƯƠNG THÍCH (NEW v0.9.6, 2026-07-21, from MA66 V3 voice session).** User verbatim 21/07: *"Em không hiểu sản phẩm rồi! Sản phẩm này chỉ dùng được với dji osmo pocket 3/4/4P thôi. Phải xem kĩ thông tin sản phẩm chứ"*. Anti-pattern (FAIL case): em viết 3 voice V3 dùng ngôn ngữ chung chung "chiếc tripod này", "máy quay" → bỏ luôn "DJI Osmo Pocket 3" vì em nghĩ "anh bảo đừng nêu mã SP" = bỏ luôn tên SP. Hậu quả: người xem không biết tripod này **CHỈ dùng cho Pocket 3/4/4P**, không phải tripod thường cho iPhone → audience lệch → conversion thấp.

  **Fix (HARD RULE v0.9.6)** — Khi viết voice/script cho SẢN PHẨM CỤ THỂ:
  - **"Mã SP" ≠ "Tên SP tương thích"** — "MA66" là mã, "DJI Osmo Pocket 3" là sản phẩm tương thích
  - **Bỏ mã SP** (MA66, K17, ...) → OK
  - **Bỏ giá** (599k, 67k) → OK
  - **GIỮ tên sản phẩm tương thích** (DJI Pocket 3, iPhone 15, Samsung S24, Insta360...) — KHÔNG BAO GIỜ bỏ, đây là thông tin quan trọng nhất để target audience tự nhận diện "cái này dành cho mình"
  - Gọi tên SP tương thích 2-3 lần trong script để reinforce

  **Self-check trước khi generate voice:**
  ```
  must_have = [<tên SP tương thích từ wiki research>]  # VD: ["DJI Pocket 3", "Pocket 4"]
  must_not_have = ["mã SP", "giá cụ thể"]  # VD: ["MA66", "599", "67k"]
  
  if not any(x in script for x in must_have):
      raise "❌ Thiếu tên SP tương thích - audience sẽ không biết dùng cho máy nào"
  ```

  **Verified PASS case 21/07 (V3A/B/C Pocket 3):** Script đề cập "DJI Pocket 3" / "DJI Osmo Pocket 3" 2-3 lần/version → đúng audience target. Anti-pattern (FAIL case V3 đợt 1): "chiếc tripod này", "máy quay" → anh feedback "không hiểu sản phẩm".

  **Áp dụng cross-reference:** Đọc `wiki/projects/<project>/products/<slug>.md` → tìm section "Compatible" / "Tương thích" → LẤY chính xác tên SP tương thích cho vào script. Ví dụ MA66 wiki:
  - Compatible (official): **DJI Osmo Pocket 3**
  - Compatible (Amazon/marketplace): **Pocket 3 / Pocket 4 / Pocket 4 Pro / Insta360 Luna / Xtra Muse**
  → Script phải nêu ít nhất 1 trong các tên này.

- **Voice TTS workflow: NamMinh + speed 1.2x default (v0.9.7 + v0.10.1, 21-23/07/2026, from MA66 voice sessions).** User config defaults verified:
  - `~/.hermes/config.yaml` → `tts.provider: edge` + `tts.edge.voice: vi-VN-NamMinhNeural` + `tts.edge.speed: 1.2`
  - Voice NamMinh (nam, friendly/positive) thay cho HoaiMy (nữ, default cũ)
  - **Speed history: 1.0 (default) → 1.5 → 1.4 → 1.3 → 1.2 (current, 23/07 — anh verbatim "Speed 1.2 mặc định nha")**
  - Workflow chuẩn: Script text → edge-tts CLI tạo MP3 normal → ffmpeg atempo 1.2x → file MP3 final
  - Khi user yêu cầu "tạo voice cho option N" → LUÔN dùng config mặc định (NamMinh + 1.2x). KHÔNG cần hỏi "dùng giọng nào" / "speed bao nhiêu" vì đã có default.
  - Nếu user muốn authentic voice (giọng thật của anh) → dùng OmniVoice skill (`omnivoice-voice-clone`), prompt ở `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_*.pt` (đã có sẵn 3 prompt verified).
  - **Caveat edge-tts rate limit:** generate liên tục có thể fail. Fix: `time.sleep(2-3)` giữa các lần generate, hoặc retry khi fail.
  - **Verify sau khi generate:** ffprobe duration (đúng 1.2x ratio), volumedetect (peak > -10 dB = không silent), Whisper medium transcription (nếu cần verify content).
  - Voice output dir: `/Volumes/Storage-1/Hermes/scratch/voice-messages/` (HERMES-ONLY-FOLDER rule).
- **OmniVoice: MỖI SESSION tạo voice prompt MỚI từ raw clip, KHÔNG dùng prompt cũ (NEW v0.9.8, 21/07/2026, from MA66 V3 voice session).** User verbatim 21/07: *"Em dùng voice ref chứ không dùng file clone có sẵn à?"*. Anti-pattern (FAIL case): Em dùng `tuan_anh_goojodoq_5s_short.pt` (voice GOOJODOQ từ session trước) → output OK nhưng voice KHÔNG phản ánh session hiện tại. **Fix (HARD RULE mỗi session)**:
  1. **Bước 1**: Extract 5-10s từ raw clip mới nhất trong `/Volumes/Storage-1/Pocket3/Footages/` (DJI files) hoặc `Hermes-Edit/` (FINAL). Bỏ 10s intro + 5s outro. Extract bằng `ffmpeg -y -ss 10 -i raw.mp4 -t 5 -ar 16000 -ac 1 -c:a pcm_s16le ref.wav`.
  2. **Bước 2**: Whisper verify (medium, KHÔNG large-v3) → transcript phải có nội dung tiếng Việt tự nhiên ≥10 chars → chắc chắn voice thật, không phải TTS outro "subscribe".
  3. **Bước 3**: CHECK ref_rms bằng omni venv python (`soundfile`). Nếu < 0.1 PHẢI amplify lên 0.11 (multiply audio by `0.11 / ref_rms`). Verified pitfall: silent ref → output volume giảm 1/6.
  4. **Bước 4**: Save prompt với ref_text NGẮN (~63 chars, 1 câu đầu). KHÔNG dùng full transcript → leak câu cuối. Save path: `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_<session>_YYYY-MM-DD.pt`.
  5. **Lưu ý**: Dùng TRỰC TIẾP venv python `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python`, KHÔNG dùng `with_venv.sh` wrapper (đã bug verified 21/07 — prepend `/Users/tuananh4865/` làm sai path).
  
  - **edge-tts rate limit + with_venv.sh path bug (NEW v0.10.1, 21-23/07/2026, from MA66 voice sessions).** Hai bug đã fix verified:
    1. **edge-tts rate limit**: Generate liên tục 3-4 file trong 1 session có thể fail với `TypeError: No audio was received` hoặc silent output. **Fix**: `time.sleep(2-3)` giữa các lần generate, hoặc retry từng file riêng nếu fail. Đã verify 21/07: 3 file đều fail lần đầu → retry từng cái sau 3-15s sleep → pass.
    2. **with_venv.sh path bug**: `with_venv.sh` wrapper prepend `/Users/tuananh4865/` vào argv → bash command bị fail vì không tìm thấy `/Users/tuananh4865/python3`. **Fix**: KHÔNG dùng `with_venv.sh` cho OmniVoice scripts. Dùng TRỰC TIẾP venv python: `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python <script.py>`. Verified bug 21/07: `bash with_venv.sh python3 save_voice_prompt.py ...` → "can't open file '/Users/tuananh4865/python3'". Workaround: chạy venv python trực tiếp, KHÔNG qua wrapper.

  *Verified case 21/07 (refreshed 23/07):** Raw `DJI_20260721095702_0038_D.MP4` (Footages, 246s, 21/07) → extract 5s từ t=10-15s → ref_rms=0.0571 < 0.1 → amplify lên 0.11 → save `tuan_anh_session_2026-07-23.pt` (9.7KB) → generate V3A 53s → atempo 1.2x → 44s. Peak -0.4 dB (to hơn prompt cũ), no ref leak (Whisper verified), giọng clone fresh session. Generate V4A/B/C (52s/48s/48s final 1.2x) all pass 3-layer verify (peak / no leak / emotion tags 4-6/script).

## yt-dlp Download Failure Pattern (NEW v0.6.0, from 2026-07-07 user-downloaded YouTube Shorts)

**Symptoms** (one or more of these):
- `yt-dlp: error: no such option: --js-runtimes`
- `ERROR: [youtube] <id>: The page needs to be reloaded.`
- `Some web client https formats have been skipped... YouTube is forcing SABR streaming`

**Root cause chain** (verified 2026-07-07):
1. The user's `~/.config/yt-dlp/config` contains `--js-runtimes node` (a flag only supported in newer yt-dlp).
2. The `yt-dlp` binary on PATH is from a Python `pip install --user` (shadowing the homebrew binary which is newer).
3. The shadowed pip version is older and either rejects `--js-runtimes` as unknown OR doesn't handle YouTube's SABR streaming block.

**Fix recipe** (run in order, 1-2 minutes total):
```bash
# Step 1: Update yt-dlp via homebrew
brew upgrade yt-dlp

# Step 2: Move the older pip-user binary aside so the new homebrew version is primary
mv /Users/tuananh4865/Library/Python/3.9/bin/yt-dlp /Users/tuananh4865/Library/Python/3.9/bin/yt-dlp.pip-bak

# Step 3: Verify the new version is on PATH
which yt-dlp   # should print /opt/homebrew/bin/yt-dlp
yt-dlp --version   # should be 2026.7.4 or later

# Step 4: If `yt-dlp` still errors with the same config flag, temporarily move the config aside
mv ~/.config/yt-dlp/config ~/.config/yt-dlp/config.bak-download
# ... run download ...
mv ~/.config/yt-dlp/config.bak-download ~/.config/yt-dlp/config
```

**After download**: yt-dlp may merge the file as `.webm` even if you specify `.mp4` output (because the source streams are webm). Convert with `ffmpeg -i input.webm -c copy output.mp4` (no re-encode = instant).

**Routing**: this is the `tiktok-product-script` skill (content), not a separate download skill. Future YouTube-download tasks (not necessarily for scripts) can use the same recipe directly via `terminal`.

## Project Routing Reference

> **MOVED to Phase -1 (Procedure step 0).** This is now BLOCKING, not informational. Read that section first before any other action.

When the user pastes a product image or name, route the script + research files to the right project based on brand / product keywords — BEFORE running Phase 0 or saving any file.

| Brand / Product keywords | Route to |
|---|---|
| Yonex, Astrox, ArcSaber, AX77, AX88, 65z, 65z4, Power Cushion, Subaxia, vợt cầu lông, giày cầu lông | `wiki/projects/tuan-anh-badminton/products/` + `wiki/projects/tuan-anh-badminton/scripts/` |
| ARMAF, Lattafa, body mist, fragrance, nước hoa, EDP, EDT, deodorant spray, skincare, dầu gội, lifestyle gadget, phụ kiện điện thoại, máy hút bụi, Pocket 3, camera tripod, gimbal accessories, action cam mount | `wiki/projects/tuan-anh-review-tiktok/products/` + `wiki/projects/tuan-anh-review-tiktok/scripts/` |
| Unknown / ambiguous brand | **Ask user ONCE** (do not default). Phrase: *"Sp này vô shop cầu lông hay kênh review lifestyle anh?"* |

**Self-correction history:** 2026-07-07 — agent default-routed ARMAF Odyssey (body mist) into `tuan-anh-badminton/` based on habit of badminton-heavy workload. User flagged TWICE in one session: first as *"Xịt khử mùi đâu liên quan đến project tuan anh badminton đâu, nó là kênh tiktok của anh mà!!!"*, then again as *"Sản phẩm nếu không thuộc ngành hàng cầu lông, phụ kiện cầu lông thì không cho vào project cầu lông! Armaf là nước hoa body mist"*. Fix: created separate project `tuan-anh-review-tiktok/`, moved ARMAF files, codified routing rule, promoted to BLOCKING Phase -1 in v0.4.0, added ULANZI MA66 camera accessory row keywords in v0.5.0. Don't repeat the mistake — check brand keywords FIRST, never default.

**Successful re-runs (Phase -1 held):** ULANZI MA66 Tripod (Pocket 3 / camera tripod / lifestyle gadget keywords → row 2) routed correctly on first try, no user correction needed. Case study: `references/ulanzi-ma66-case-study.md`.

## Verification

After delivering, confirm via `terminal`:

```bash
PROJECT_DIR=tuan-anh-badminton   # or `tuan-anh-review-tiktok` per Routing Reference
test -f /Volumes/Storage-1/Hermes/wiki/projects/${PROJECT_DIR}/scripts/<product>-v1.md && \
  grep -c "^KEEP " /Volumes/Storage-1/Hermes/wiki/projects/${PROJECT_DIR}/scripts/<product>-v1.md
```

Then reply proves the skill worked — Telegram embed must show: 11-phase table + 3-version script + KPI list + file path, with ≥1 keep per chosen principle and no câu treo / hallucinate / loop failures. Plus: the Phase -1 routing decision was visible in the reply (which project the script saved into).

**Hard rule v0.13.1 (Telegram delivery):** Nếu N≥2 scripts → BẮT BUỘC gộp thành 1 file `/Volumes/Storage-1/Hermes/scratch/<N>-scripts-batch-YYYY-MM-DD.md` rồi gửi `MEDIA:<path>` qua Telegram. KHÔNG gửi N paths riêng. User verbatim 25/07: "phải luôn luôn gửi file qua telegram cho anh chứ không được gửi path không vì đa phần anh sẽ làm việc với em qua telegra điện thoại!". Chi tiết PITFALL Telegram delivery mode ở trên.

---

## 🆕 v0.3.0 — PROBLEM-SOLUTION FORMULA (16/07/2026)

> **Context:** Tuấn Anh xác nhận (16/07) muốn content theo công thức **Vấn đề → Giải pháp**, KHÔNG phải chuyên gia. Đây là template mới cho mọi sản phẩm.
>
> **User verbatim feedback (16/07):** *"Theo anh thì công thức nên là vấn đề và giải pháp bởi vì anh không muốn làm chuyên gia trong bất cứ ngành nào hết"*
>
> **Vĩnh viễn rule:** Tuấn Anh KHÔNG muốn đóng vai chuyên gia bất cứ ngành nào. Mọi script lifestyle phải theo công thức Problem-Solution trừ khi anh explicit yêu cầu khác.

## 🎯 NGUYÊN TẮC (VĨNH VIỄN)

- ✅ Anh hiểu **vấn đề thật** khách gặp → giải pháp
- ❌ KHÔNG cần làm chuyên gia nước hoa / chuyên gia cầu lông / chuyên gia gì cả
- ❌ KHÔNG dùng từ chuyên ngành (top note, heart note, base note, ISO, focal length, sensor, fps, gimbal, EDP, EDT...)
- ✅ Mass-market appeal - ai cũng có vấn đề đó
- ✅ Reusable cho MỌI sản phẩm (body mist, sạc dự phòng, tripod, ốp pocket, lenspen...)
- ✅ Tone: "anh nói như người thật gặp vấn đề - không phải chuyên gia"

## 📐 CẤU TRÚC 4-PART (90-120s)

```
[0-5s]   HOOK VẤN ĐỀ (P1) — Cụ thể, dễ hình dung
[5-25s]  PAIN DEPTH (P2) — 3 vấn đề nhỏ, "đúng là mình"
[25-75s] GIẢI PHÁP (S) — Sản phẩm + test thực tế + sensory
[75-95s] PROOF + PRICE — Số liệu cụ thể + so sánh giá
[95-120s] CTA NHẸ — Inbox tư vấn - KHÔNG hard-sell
```

## 📝 TEMPLATE 3 VERSION MỖI SẢN PHẨM

Mỗi sản phẩm viết 3 version, mỗi version là 1 vấn đề khác nhau của cùng sp:

| Version | Hook vấn đề | Audience | Tone |
|---|---|---|---|
| A | Vấn đề 1 (cụ thể nhất) | Mass-market | Casual |
| B | Vấn đề 2 (GenZ relatable) | GenZ | GenZ casual |
| C | Vấn đề 3 (deep insight) | Niche/ngách | Honest reviewer |

## 🔄 SO SÁNH VỚI V1 (TRƯỚC 16/07)

| V1 (Authority) | V2 (Problem-Solution) |
|---|---|
| Hook: "ARMAF chính hãng về" | Hook: "Đi gym 1 tiếng - mùi ám áo" |
| Authority signals (4.2⭐, 112 reviews) | Pain depth (3 vấn đề) |
| Specs (19 mùi, 200ml) | Solution test (đi gym 1 tiếng còn mùi) |
| Storytelling: "Anh Khoa Hà Đông" | Proof: "30K/tháng - rẻ hơn 1 ly cà phê" |
| Cần làm chuyên gia ✅ | KHÔNG cần chuyên gia ✅ |

## 📋 CHECKLIST KHI VIẾT SCRIPT V2

- [ ] Hook 0-5s nêu vấn đề CỤ THỂ (không phải mô tả chung chung)
- [ ] Pain 5-25s có 3 vấn đề nhỏ hơn (để khách thấy "đúng là mình")
- [ ] Solution 25-75s có test thực tế (đi đâu, làm gì, cảm giác)
- [ ] Proof 75-95s có số liệu cụ thể (giá, thời gian, lưu hương)
- [ ] CTA 95-120s nhẹ nhàng, KHÔNG "mua ngay", "inbox tư vấn mùi hợp"
- [ ] KHÔNG dùng từ chuyên ngành (top note, heart note, base note...)
- [ ] **VĂN NÓI ĐỜI THƯỜNG — KHÔNG từ hoa mỹ (NEW v0.9.1, 21/07/2026)** — xem Pitfalls → "Văn nói đời thường vs từ hoa mỹ"
- [ ] **MỖI VERSION CHỈ 1 NHU CẦU (NEW v0.9.2, 21/07/2026)** — Đếm số use-case trong version, nếu >1 → TÁCH version. 3 version × 3 NHU CẦU khác nhau, KHÔNG phải 3 use-case của cùng 1 nhu cầu. Xem Pitfalls → "MỖI VIDEO CHỈ 1 NHU CẦU" + lesson file `wiki/concepts/tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md`

## 🗣️ TONE RULE: VĂN NÓI ĐỜI THƯỜNG (NEW v0.9.1, 21/07/2026)

> **User verbatim feedback (21/07/2026):** *"Viết bằng văn nói đời thường thôi đừng dùng tư hoa mỹ quá!"*
>
> **Lesson:** Vĩnh viễn rule — script TikTok của anh phải đọc như người thật kể chuyện, KHÔNG phải copy editor chuyên nghiệp. Verified case 21/07/2026: ULANZI MA66 V2 em viết bản đầu với từ "sensory", "POV", "flat lay", "nam châm tủ lạnh", "Magnetic N52", "1/4 inch", "không cinematic" → anh feedback → phải rewrite mới pass.

### Cách viết văn nói đời thường

**Nguyên tắc:** Viết như đang nói chuyện với bạn bè qua điện thoại, KHÔNG viết như đang viết bài báo / brochure.

**Từ/cụm từ BỎ NGAY (từ hoa mỹ):**
- ❌ POV, flat lay, cinematic, sensory, signature, masterpiece
- ❌ "Magnetic N52", "1/4 inch", "Arca-Swiss mount" (chuyên ngành)
- ❌ "tương tự như nam châm tủ lạnh" (so sánh cứng)
- ❌ "tuyệt vời", "hoàn hảo", "đẳng cấp", "đỉnh cao", "sắc nét"
- ❌ "không cinematic", "rủi ro 0 đồng", "chất lượng tương đương 70%"
- ❌ Em dash kiểu marketing: "— Setup nhanh — Test thực tế — Sensory"

**Từ/cụm từ DÙNG THAY (văn nói):**
- ✅ "POV" → "đi bộ", "quay từ trên xuống", "cảnh người ta nhìn thấy"
- ✅ "Magnetic" → "nam châm", "gài vào là dính"
- ✅ "1/4 inch thumb screw" → "vặn ốc", "ốc nhỏ"
- ✅ "Arca-Swiss mount" → "cái đế gắn", "cái kẹp"
- ✅ "Freeship + 14% hoàn tiền" → "freeship luôn, hoàn 14%"
- ✅ "599K + PayLater 67K/tháng" → "599k thôi, trả góp 67k một tháng"
- ✅ "Tripod rẻ ngoài chợ thì chân yếu" → giữ nguyên (đã đời thường)
- ✅ "đụng nhẹ là đổ" → giữ nguyên (đã đời thường)
- ✅ "video vẫn ổn" → giữ nguyên (đã đời thường)
- ✅ "nắng đẹp là kịp quay, mèo nhảy là kịp bấm" → giữ nguyên (đã đời thường)

**Marker văn nói (xuất hiện 4-5+ lần trong script 90-120s = OK):**
- "thôi" · "luôn" · "rồi" · "nha" · "đó" · "mình" · "anh em" · "inbox"

**Test formula (self-check trước khi deliver):**
```bash
grep -ciE "POV|sensory|cinematic|signature|masterpiece|nam châm tủ lạnh|Magnetic N52|1/4 inch|Arca-Swiss|tuyệt vời|hoàn hảo|đẳng cấp|đỉnh cao|sắc nét|rủi ro 0 đồng|chất lượng tương đương|trau chuốt|mỹ miều" <script-file>
# → PHẢI trả về 0 match. Nếu >0 → VI PHẠM, rewrite phần đó.
```

**Anti-pattern (FAIL case 21/07/2026, ULANZI MA66 V2):**
- ❌ Bản đầu: "MA66 magnetic N52 - bám cứng - gắn Pocket 3 vào 1 giây - xong"
- ✅ Bản fix: "MA66 nó có nam châm, gài Pocket 3 vào một cái là dính chặt"

- ❌ Bản đầu: "Magnetic bám cửa sắt xe lửa - gài bàn cà phê - không cần tripod"
- ✅ Bản fix: "Mà nó còn dính được cả cửa sắt xe lửa, gài bàn cafe"

- ❌ Bản đầu: "Test mình búng tay vào - không rơi - bám chắc như nam châm tủ lạnh"
- ✅ Bản fix: "Mình có test búng tay vào, nó không rơi"

- ❌ Bản đầu: "Star Shop 4.9 trên 96 review - 3.599 người đã mua - 6.6K mua lại"
- ✅ Bản fix: "3.599 người mua rồi, 4.9 sao trên 96 review"

**Rule KHÔNG cần verify:** Câu "đời thường" KHÔNG có nghĩa là câu tục / câu thô / câu thiếu chủ ngữ. Vẫn phải:
- Đủ predicate (không câu treo)
- Đúng ngữ pháp
- Có logic mạch lạc (Hook → Pain → Solution → Proof → CTA)

Chỉ là THAY từ ngữ chuyên nghiệp / hoa mỹ → từ ngữ hàng ngày. KHÔNG phải viết cẩu thả.

## 🎯 KHI NÀO DÙNG

- ✅ Body mist, sạc dự phòng, tripod, ốp pocket, lenspen (mọi sản phẩm lifestyle)
- ✅ TikTok Shop video
- ✅ Facebook Reels
- ❌ KHÔNG dùng cho shop cầu lông (giữ style tư vấn chuyên gia ở project Badminton)

## 🗣️ VĂN NÓI TỰ NHIÊN - 8 BÀI HỌC (NEW v0.10.0, 21/07/2026)

> **User feedback (verbatim 21/07):** *"Cách em viết chưa giống văn nói của con người lắm!"*
> **Source:** 9 web sources (Blitzcut, Hollyland, ScriptStorm, CopyMinimalist, etc.) + transcript @dungkenhnghiepdu 81s (WPM 284, 24% fragments, "đấy" 8 lần).
> **Wiki lesson:** `wiki/concepts/tiktok-script-natural-voice-2026-07-21.md` (10.8KB, full 8 lessons + checklist).

### 8 bài học văn nói (FIRST-CLASS rule, vĩnh viễn):

1. **Sentence-final particles (đấy/nhá/nhé/nhỉ/ấy)**: Mỗi câu 5-10 từ PHẢI có 1 particle. Dũng dùng "đấy" 8 lần / 34 câu = 24%. Tạo cảm giác khẳng định + thân mật.
2. **Fragments 3-5 từ**: 24% câu trong văn nói là fragments. VD Dũng: "Rất khó bán", "Thì nói thật nhá", "Lúc đấy nhé", "Bỏ túi nào cũng vừa". Mỗi script 60-90s nên có 3-5 fragments.
3. **Tránh 5 từ cấm kỵ** (theo Kapwing research - polished tone fail): `toàn`, `mọi`, `đặc biệt`, `vô cùng`, `rất nhiều`. Thay bằng từ đời thường.
4. **Length rhythm**: Câu 11 từ → fragment 3-5 từ → câu 11 từ → fragment. Tạo nhịp thay vì đều đều.
5. **WPM 200-250** (target). Văn viết ~130-150 WPM, văn nói nhanh hơn 50%. Đếm từ/giây khi đọc to.
6. **Mid-thought start** (theo ScrollScript research): KHÔNG "Xin chào/Có ai biết/Hôm nay mình...". Bắt đầu bằng hành động/cảm xúc cụ thể. VD: "Hai năm làm video...", "Ba mươi giây đấy", "Cái tin nhắn nó gửi tối qua..."
7. **Sensory đời thường** (không hoa mỹ): "gài máy quay vào một cái là dính" thay vì "tích hợp công nghệ magnetic tiên tiến". Sensory = chi tiết cụ thể, KHÔNG từ bóng bẩy.
8. **Read aloud test BẮT BUỘC**: Dùng OmniVoice/edge-tts/Whisper TTS đọc script → nghe lại. Nếu nghe "AI" hoặc "cứng" → viết lại câu đó. Công thức: viết → TTS đọc → nghe → fix → TTS đọc lại.

### Sentence-final particles tiếng Việt (Bắc):
- **đấy**: khẳng định, chỉ (phổ biến nhất - Dũng dùng 8 lần)
- **nhé**: đề nghị, nhắc (CTA cuối)
- **nhá**: xác nhận (cuối câu nhấn mạnh)
- **nhỉ**: tự vấn, suy nghĩ (hỏi người nghe)
- **ấy**: thân mật, gần gũi (cuối câu)
- **thôi**: giới hạn (không hơn)
- **luôn**: khẳng định mạnh (thường đi với "đấy")

### Example: V3A (bị chê) → V4A (đã fix)
**V3A cũ (văn viết):**
> "Hồi mới quay, mình **toàn** đặt điện thoại lên bàn. Góc thấp, chỉ thấy cằm, **mà mình cứ tưởng** ổn."

**V4A mới (văn nói):**
> "Hồi mới quay, mình đặt điện thoại lên bàn **đấy**. Góc thấp, chỉ thấy cằm thôi. Mình cứ tưởng ổn **ấy**."

### Self-check trước deliver (BẮT BUỘC):
```python
text = script_text
checks = {
  'particles >= 5': sum(text.count(p) for p in ['đấy','nhá','nhé','nhỉ','ấy']) >= 5,
  'fragments >= 3': count_short_sentences(text, max_words=6) >= 3,
  'forbidden == 0': sum(text.count(w) for w in ['toàn bộ','mọi người','đặc biệt','vô cùng','rất nhiều']) == 0,
  'wpm 200-250': count_wpm(text) >= 200,
  'no formal opener': not text.startswith(('Xin chào', 'Có ai', 'Hôm nay mình'))
}
```

### Kết hợp 4 rule bổ trợ (FIRST-CLASS):
| Version | Rule | Source |
|---|---|---|
| 16/07 | "Không làm chuyên gia" | User feedback (16/07) |
| 21/07 v0.9.1 | "Không dùng từ hoa mỹ" | User feedback "đừng dùng tư hoa mỹ quá!" |
| 21/07 v0.9.2 | "Mỗi video chỉ 1 nhu cầu" | Clip @dungkenhnghiepdu |
| **21/07 v0.10.0** | **"Văn nói tự nhiên"** | **User feedback + 9 sources** |

→ Khi viết script V2/V3/V4 → áp dụng CẢ 4 rule cùng lúc.

## 🗣️ USER-QUESTION HANDLING (NEW v0.5.0, 16/07/2026)

**When user asks "viết script X theo công thức nào hợp lý nhỉ" / "nên dùng formula nào" / "cách nào tốt nhất":**

- ❌ **DO NOT** list 3-4 options (A/B/C/D) and ask user to choose
- ✅ **DO** recommend 1 công thức dựa trên pivot history (load MEMORY `[16/07 CONTENT-FORMULA-PROBLEM-SOLUTION]`), giải thích TẠI SAO hợp với user preference, và hỏi confirm ngắn

**Verified case (16/07):** Tuấn Anh đã pivot 3 lần về content style trong cùng 1 ngày (07/07 chuyên gia → 11/07 Vui Vẻ → 16/07 Problem-Solution). Khi anh hỏi "viết ARMAF theo công thức nào hợp lý nhỉ", agent recommended Problem-Solution dựa trên pivot history thay vì list 4 option. Anh chọn ngay, không phải mệt chọn.

**Anti-pattern (avoid):** Listing "Công thức A = Trust-First, B = Viral-First, C = Storytelling, D = Problem-Solution" → user phải tự quyết → fatigue.

**Default recommendation template:**
```
📊 Recommended: PROBLEM → SOLUTION
- Tại sao hợp: [2-3 lý do ngắn]
- Tone: "người thật gặp vấn đề thật, không phải chuyên gia"
- Pattern: 4-PART (Hook vấn đề → Pain → Solution → Proof+Price → CTA nhẹ)
- Lý do tránh alternatives: [1 dòng]
```
Sau đó hỏi "OK?" thay vì "Anh chọn số nào?"

## 📚 REFERENCE

- `wiki/projects/tuan-anh-review-tiktok/scripts/armaf-odyssey-body-spray-200ml-v2.md` — Sample full 3 version
- `wiki/projects/tuan-anh-review-tiktok/scripts/sac-du-phong-magsafe-problem-solution.md` — Reusable pattern cho sp khác
- `wiki/projects/tuan-anh-review-tiktok/scripts/op-bao-ve-pocket-3-problem-solution.md` — Ốp Pocket 3 template (3 version, 282 lines)
- `wiki/projects/tuan-anh-review-tiktok/scripts/lenspen-ve-sinh-ong-kinh-problem-solution.md` — Lens cleaning template (3 version, 234 lines)
- `wiki/projects/tuan-anh-review-tiktok/scripts/kf-but-ve-sinh-body-mist-problem-solution.md` — K&F + Body Mist Lemony template

---

*Problem-Solution template v0.3.0 added 16/07/2026.*
*Parallel content production pattern v0.4.0 added 16/07/2026.*
*User-question handling pattern v0.5.0 added 16/07/2026 (recommend 1, don't list options).*
*Vĩnh viễn rule: "không làm chuyên gia" — verified từ user verbatim feedback 16/07.*
              role="leaf", 
              context="Full context: công thức 4-PART + data research + verbatim user feedback + tone rules")
# ... repeat for each product
```

**Why parallel:** Sequential viết 5 template × 90-120s = 30+ phút. Parallel = 5 subagent trong ~3-5 phút.

**Each subagent must receive in context:**
- ✅ Công thức 4-PART (90-120s)
- ✅ NGUYÊN TẮC (đặc biệt "không làm chuyên gia")
- ✅ Data research file path (đã có Phase 0)
- ✅ 3 hooks khác nhau cho mỗi version
- ✅ Save path chính xác
- ✅ Frontmatter format chuẩn

**Empirical result (16/07/2026):** 4 subagent song song = 4 template xong trong 1.5 phút (97s nhanh nhất), total 6 scripts trong wiki sau 5 phút. Hiệu quả hơn 5-10x so với sequential.
## 📚 REFERENCE

- `wiki/projects/tuan-anh-review-tiktok/scripts/armaf-odyssey-body-spray-200ml-v2.md` — Sample full 3 version (master template, aspirational category)
- `wiki/projects/tuan-anh-review-tiktok/scripts/sac-du-phong-magsafe-problem-solution.md` — Template cho sản phẩm khác (reusable pattern, utility/tech category)
- `wiki/projects/tuan-anh-review-tiktok/scripts/op-bao-ve-pocket-3-problem-solution.md` — Ốp Pocket 3 template (3 version, 282 lines, technical-accessory category)
- `wiki/projects/tuan-anh-review-tiktok/scripts/lenspen-ve-sinh-ong-kinh-problem-solution.md` — Lenspen + bộ vệ sinh ống kính template (utility/maintenance category). **Đọc kèm `references/lenspen-lens-cleaning-problem-solution-case-study.md`** để nắm **utility-product disclaimer pattern** (script phải bound promises hoặc người xem sẽ nghĩ sp sửa được mọi thứ).

## ⚠️ UTILITY / MAINTENANCE CATEGORY — disclaimer bắt buộc (NEW 16/07/2026)

Khi sản phẩm giải quyết vấn đề thật nhưng GIỚI HẠN (như lens cleaning, đồ vệ sinh, app productivity, máy hút bụi mini), script PHẢI có disclaimer cụ thể — nếu không, người xem sẽ suy ra rằng sản phẩm sửa được mọi loại sự cố (out nét, lens xước, lỗi máy, mất kết nối).

**Mẫu disclaimer (đặt ở đầu file + ở đoạn claim mạnh nhất của script):**

> **Lưu ý quay:** [tình huống trong kịch bản] là tình huống trải nghiệm; không nên hứa rằng [sản phẩm] sẽ sửa được [những thứ sản phẩm KHÔNG sửa được — vd out nét, lens xước, lỗi máy].

Xem chi tiết Section 6 của `references/lenspen-lens-cleaning-problem-solution-case-study.md`.

**Áp dụng cho:** cleaning products, maintenance products, productivity tools, mọi sản phẩm mà khi over-promise sẽ fail visibly trước mặt người xem.

**KHÔNG áp dụng cho:** aspirational products (như body mist ARMAF) — fragrance không fail visibly; technical-accessory products với known feature set (như tripod MA66) — user có thể verify claim dễ dàng.

**3-category taxonomy emerged 16/07/2026:**

| Category | Example | Problem anchor | Disclaimer? |
|---|---|---|---|
| Aspirational | ARMAF Odyssey body mist | Lifestyle / occasion-based | ❌ Không cần |
| Technical-accessory | ULANZI MA66 tripod | Workflow / professional use | ⚠️ Conditional (chỉ khi có known limit) |
| Utility / maintenance | Lenspen, K&F lens pen, Zeiss wipes | Real-life pain | ✅ BẮT BUỘC |

---

## ⚠️ SUBAGENT TIMEOUT FALLBACK (NEW v0.6.0, 16/07/2026)

**Symptoms:**
- Subagent dispatched with `delegate_task` returns `status=timeout, api_calls=N, total_duration≥600s`
- File at expected path KHÔNG tồn tại sau khi subagent timeout

**Anti-pattern (avoid):**
- ❌ Re-dispatch ngay subagent giống với context y hệt → sẽ timeout lại
- ❌ Skip task hoàn toàn → user không có output
- ❌ Dispatch subagent khác với context rút gọn (mất data quality)

**Correct fallback (5-step):**

1. **Detect**: `os.path.exists(expected_file_path)` check ngay khi subagent timeout
2. **Pivot to manual**: em TỰ viết file theo cùng formula đã verify với subagent khác đã xong (sample reference)
3. **Cite source**: ghi rõ trong file "Em viết manual sau khi subagent timeout 600s (lưu ý: vẫn theo đúng formula đã verify 16/07/2026)"
4. **Use verified data**: lấy data từ wiki research files đã có (Phase 0 cache) — KHÔNG cần search lại
5. **Add to workflow queue**: nếu cần polish thêm → dispatch subagent khác với timeout ngắn hơn (300s) + chỉ 1 task cụ thể

**Empirical case (16/07/2026):** Subagent `deleg_70573527` (Tripod Ulanzi Problem-Solution) timeout 600s sau 11 API calls — em tự viết file 6.2KB manual trong <30s dùng data wiki research đã có + formula Problem-Solution đã verify qua 3 subagent trước. Total downtime: ~30s thay vì 600s+ retry.

- **User-question handling pattern v0.5.0 added 16/07/2026 (recommend 1, don't list options).**
- **PITFALL "Scan scripts có sẵn TRƯỚC khi hỏi brand" added v0.13.0 25/07/2026 (from session "ốp K&F + body mist Armaf Limoni + clean pen K&F + Dodoto" — user verbatim "Tìm tên sản phẩm dựa theo script của anh mà làm!"). 3-step workflow TRƯỚC khi hỏi brand: (1) `search_files` trong `wiki/projects/<project>/scripts/` + `products/`; (2) `terminal ls Hermes-Edit/` để parse filename SP names; (3) Cross-reference tên user vừa liệt kê vs scan results → hỏi user với options CỤ THỂ từ data scan được. Lesson: user có scripts rồi — đừng ép user nhớ tên SP đầy đủ; em chủ động scan = user chỉ pick.**

## 🎯 MIX MULTIPLE PRODUCTS IN 1 SCRIPT (NEW v0.6.1, 16/07/2026)

**Pattern:** Khi user yêu cầu script cho 2+ sản phẩm cùng ngành hàng (vd "K&F bút vệ sinh + Body Mist Lemony"), subagent có thể tự **mix 2 sản phẩm trong 1 file 3 version** — mỗi version dùng 1 sản phẩm phù hợp với vấn đề đó.

**Ví dụ thực tế (16/07):**
- 2 sản phẩm: K&F Lens Pen (89K) + Body Mist (BODYMISS/Sol de Janeiro/Lush)
- 3 version:
  - Version A (Lens bẩn) → K&F Lens Pen 89K
  - Version B (Mồ hôi cầu lông) → BODYMISS 52K
  - Version C (Nước hoa đắt) → Sol de Janeiro 350K + Lush 850K

**Lợi ích:**
- 1 file = 18 version content = 54-72 phút TikTok (3x thay vì 1x)
- Khớp với cách user mua sản phẩm (khi shopping online, so sánh 3-5 lựa chọn)
- Tái sử dụng được research data đã có

**Anti-pattern (avoid):**
- ❌ Mỗi sp 1 file riêng → quá nhiều file, khó quản lý
- ❌ Mix sp KHÔNG cùng ngành hàng (vd body mist + tripod) → loạn narrative
- ❌ Mix mà KHÔNG ghi rõ "version nào dùng sp nào" → user confused

**Rule:** Mix OK nếu:
- 2+ sản phẩm cùng audience (vd "người thích chụp ảnh" cho K&F + Lenspen)
- 2+ sản phẩm cùng price tier (vd tất cả <300K cho budget-conscious)
- Mỗi version rõ ràng anchor 1 vấn đề + 1 sản phẩm chính

## 📊 BATCH PRODUCTION BENCHMARK (NEW v0.6.2, 16/07/2026)

**Verified pattern:** User asked "Làm cả 5" → em dispatch 4 subagent song song + 1 manual fallback:

| Subagent | Output | Size | Duration | Status |
|---|---|---:|---:|---|
| Ốp Pocket 3 | 3 version, 7 citations | 15.3KB / 282 lines | 97s | ✅ |
| K&F + Body Mist Lemony | 3 version (mix 2 sp) | 11.4KB / 210 lines | 122s | ✅ |
| Lenspen | 3 version, 5 sources | 17.2KB / 234 lines | 204s | ✅ |
| Tripod Ulanzi | 3 version (manual fallback) | 6.2KB | ~30s manual | ⚠️ timeout |

**Total: 5 templates × 3 version = 18 scripts Problem-Solution trong ~10 phút** (97-204s parallel + 30s manual).

**Sequential equivalent:** ~30-45 phút (5 templates × 6-9 phút/template).

**Time saved:** ~70% bằng parallel dispatch + manual fallback pattern.

**Future batching recommendation:** Khi user yêu cầu "viết script cho N sản phẩm" với N≥3, MẶC ĐỊNH dispatch parallel + chuẩn bị manual fallback cho timeout case.

---

*Problem-Solution template v0.3.0 added 16/07/2026.*
*Parallel content production pattern v0.4.0 added 16/07/2026.*
*Utility/maintenance disclaimer pattern v0.4.1 added 16/07/2026.*
*User-question handling pattern v0.5.0 added 16/07/2026 (recommend 1, don't list options).*
*Subagent TIMEOUT fallback pattern v0.6.0 added 16/07/2026.*
*Mix multiple products pattern v0.6.1 added 16/07/2026.*
*Batch production benchmark v0.6.2 added 16/07/2026.*
*Vĩnh viễn rule: "không làm chuyên gia" — verified từ user verbatim feedback 16/07.*

*Hook word-count write-then-verify anti-pattern patched v0.9.0 21/07/2026.*
*V1+V2 coexistence rule added v0.9.0 21/07/2026.*
*7 psychology principles → 3-version mapping table added v0.9.0 21/07/2026.*
*Reference file `references/ulanzi-ma66-problem-solution-case-study.md` added v0.9.0 21/07/2026.*
*Markdown blockquote over-engineer patched v0.9.4 21/07/2026.*
*PITFALL "Problem-solution listing không thu hút → storytelling mặc định" added v0.9.5 21/07/2026 (from MA66 V3 rewrite, user verbatim "cả 3 kịch bản này đều không thu hút").*
*PITFALL "Voice script KHÔNG giá + KHÔNG mã SP" added v0.9.5 21/07/2026 (from MA66 V2 voice session, user verbatim "Không nêu giá và mã sản phẩm! Sản phẩm là tripod thì gọi nó là chiếc tripod này thôi").*
*PITFALL "Voice script PHẢI nhắc tên SP tương thích" added v0.9.6 21/07/2026 (from MA66 V3 voice session, user verbatim "Sản phẩm này chỉ dùng được với dji osmo pocket 3/4/4P thôi. Phải xem kĩ thông tin sản phẩm chứ").*
*PITFALL "MỖI VIDEO CHỈ 1 NHU CẦU" added v0.9.2 21/07/2026 (from clip @dungkenhnghiepdu 81s, transcript + 5 lessons at `wiki/concepts/tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md`).*
*PITFALL "Voice TTS workflow: NamMinh + speed 1.2x default" added v0.9.7 21/07/2026 + updated v0.11.0 23/07/2026 (from MA66 voice sessions — anh đã adjust speed 1.0 → 1.5 → 1.4 → 1.3 → 1.2 + đổi giọng HoaiMy → NamMinh qua 5 lần feedback trong 2 ngày. Config ở `~/.hermes/config.yaml` `tts.edge.voice/speed`).*
*PITFALL "OmniVoice default audio_chunking NGẮT QUÃNG" + "emotion tag count = voice smoothness" added v0.10.3 23/07/2026 (from MA66 V4 voice session — user verbatim "Voice gen ra kiểu bị ngắt quãng nhiều không nói liền mạch" + "OptionB rất ổn". Fix: override config `audio_chunk_threshold=90.0, audio_chunk_duration=30.0, pad=0, fade=0` + 4-6 emotion tags optimal).*
- **PITFALL "OmniVoice: MỖI SESSION tạo voice prompt MỚI từ raw clip" added v0.9.8 21/07/2026 (from MA66 V3 voice session — user verbatim "Em dùng voice ref chứ không dùng file clone có sẵn à?"). 5-step workflow: extract raw → Whisper verify → check ref_rms (amplify <0.1) → save prompt với ref_text ngắn → verify no ref leak.**
- **PITFALL "OmniVoice default audio_chunking NGẮT QUÃNG" added v0.10.3 23/07/2026 (from MA66 V4 voice session — user verbatim "Voice gen ra kiểu bị ngắt quãng nhiều không nói liền mạch ấy em đang prompt voice kiểu gì vậy?").** Root cause: default `OmniVoiceGenerationConfig` có `audio_chunk_threshold=30s` + `audio_chunk_duration=15s` → script 60-90s bị chunk 2-3 lần → cảm giác ngắt quãng. **Fix (HARD RULE)**: LUÔN override với `audio_chunk_threshold=90.0` + `audio_chunk_duration=30.0` + `pad_duration=0.0` + `fade_duration=0.0`. Verified case 23/07: V4A ULANZI MA66 với default config có 24 pauses 0.3-1.5s; với config fixed còn 18-20 pauses. Xem `references/voice-script-tts-workflow.md` §7 P1.
- **PITFALL "OmniVoice emotion tag count = voice smoothness" added v0.10.3 23/07/2026 (from V4B vs V4A comparison).** User verbatim 23/07: "OptionB rất ổn" (V4B có 4 tags) vs V4A/C (6 tags) → nghe ngắt quãng hơn. **Rule ngầm (empirical)**: **4 emotion tags/script = smooth, 6 tags = có emotion nhưng hơi ngắt quãng.** Mapping: HOOK=[surprise-oh]+[laughter] (2 tags), PAIN=[sigh] (1), SOLUTION=[question-ah] (1), CTA=[confirmation-en] (1) = 5 tags max. Nếu muốn smooth hơn, bỏ `[laughter]` ở hook (V4A có → V4B không có → smoother) hoặc gộp 2 `[sigh]` thành 1 (V4A có 2 sigh → V4B có 1 sigh → smoother). Xem `references/voice-script-tts-workflow.md` §6 emotion tags mapping.
- **PITFALL "Voice prompt punctuation rule" added v0.12.0 23/07/2026 (from V4A rewrite).** User verbatim 23/07: *"Vấn đề ngắt nghỉ nhiều là do dấu "." Và dấu "," em đang phân bố dày và bất hợp lý quá, muôn voice clone nói được liền mạch một câu phải giảm bớt dấu "," trong câu và dấu "." Cũng cần đặt đúng điểm để chuyển giai đoạn. Dấu chỉ đặt khi thực sự muốn nhấn mạnh vào vấn đề hoặc câu nói đó thôi"*. Anti-pattern (3 FAIL cases em đã thử): (1) Bỏ hẳn dấu câu → model hallucinate "Tài năng tìm ra là" loop 100%; (2) Thay bằng em-dash "—" → model vẫn pause; (3) Paragraph 45 từ + bỏ dấu → model tự ngắt quãng không đúng chỗ. **Fix (HARD RULE v0.12.0)**: CÂN BẰNG — (a) dấu "," 0.6-0.9/câu (giảm, KHÔNG bỏ); (b) dấu "." 1 dấu/câu, đặt cuối câu để **chuyển giai đoạn** (KHÔNG ngắt giữa ý); (c) câu 8-15 từ; (d) emotion tag đầu paragraph 30-45 từ; (e) fragments 3-5 từ OK. Xem chi tiết `references/voice-prompt-punctuation-rule-2026-07-23.md` (4 cách đã thử 3 FAIL → 1 PASS + checklist self-verify + 4 transformations).
- **PITFALL "Voice script PHẢI viết theo trải nghiệm CÁ NHÂN (first-person)" added v0.12.0 23/07/2026 (from V4 → V5 rewrite).** User verbatim 23/07: *"Hãy viết theo kiểu trải nghiệm câu chuyện cá nhân đi đừng viết theo kiểu kể về người khác nữa"*. Anti-pattern (FAIL case): V4B "OptionB rất ổn" về dấu câu NHƯNG có "cô bạn mình"/"nó" → kể về người khác → user feedback bắt buộc rewrite. **Fix (HARD RULE v0.12.0)**: (a) Ngôi xưng BẮT BUỘC first-person ("mình"/"tôi") — KHÔNG "cô bạn mình", "nó"; (b) Pronoun target ≥6 lần "mình"/script 60-90s; (c) Pronoun giới hạn 0 lần "nó"/"cô bạn"/"anh ấy" (third-person); (d) Trải nghiệm cá nhân rõ: mình đi, mình mang, mình thử, mình quay, mình bán; (e) Hook mid-thought + first-person. Verified case 23/07 (V5A/B/C ULANZI MA66): 6-7 lần "mình"/script, 0 lần "nó"/"cô bạn" → first-person rõ ràng.

- **PITFALL "Pronoun 'nó' OK khi tham chiếu object/product/animal, KHÔNG vi phạm first-person" added v0.13.0 25/07/2026 (from Dodoto + ARMAF Limoni dual-script session).** Cảnh báo trước: rule trên (V5A MA66) cấm "nó" vì nó = "cô ấy/anh ấy" (third-person storytelling). NHƯNG trong văn nói đời thường, "nó" = "cái này/sản phẩm/con vật" là BÌNH THƯỜNG và không vi phạm first-person. **Anti-pattern (false positive FAIL)**: agent verify script grep "nó" → thấy 6-8 match → kết luận "third-person fail" → phải rewrite hàng loạt câu đang OK. **Fix (HARD RULE)**: khi grep/verify "nó"/"cô bạn"/"anh ấy", PHÂN BIỆT 2 ngữ cảnh:
  - ✅ **Object/product reference** (OK): "cái này/nó là cái để mình...", "con mèo/nó rụng lông...", "chai body mist/nó thơm..." — đây là văn nói đời thường, KHÔNG vi phạm.
  - ❌ **Person reference** (FAIL): "cô bạn mình đi Đà Lạt, nó bảo sao không biết sớm..." — đây là kể về NGƯỜI KHÁC, vi phạm first-person rule.
  - **Self-check rule**: Nếu "nó" đi với "cái"/"con"/"chai"/"sản phẩm"/"thứ" → OK. Nếu "nó" đi với tên người/đại từ người → FAIL. Verified case 25/07: Dodoto + ARMAF Limoni scripts đều có 6-8 "nó" reference object → user approve chứ không phải lỗi.

- **PITFALL "Verify script 7-checks phải EXCLUDE Tone rule NEGATIVE examples" added v0.13.0 25/07/2026 (from Dodoto + ARMAF Limoni verify pass).** Anti-pattern (false positive FAIL): agent grep file script cho "từ hoa mỹ" (POV/sensory/cinematic/tuyệt vời/hoàn hảo/đẳng cấp/đỉnh cao...) → match 4-9 trong file → kết luận "VI PHẠM". NHƯNG 4-9 match đó NẰM TRONG Tone rule block (liệt kê từ KHÔNG ĐƯỢC dùng, kèm "- KHÔNG từ hoa mỹ: ..."), KHÔNG phải voice thật. **Fix (HARD RULE cho scripts/verify_script_7_checks.py)**: trước khi grep, **strip 3 sections meta**:
  1. Frontmatter YAML (giữa `---`)
  2. Sources/Citations section (`## 📚 SOURCES` → EOF)
  3. Tone rules block (giữa `**Tone rules**` → pattern `\d+ bài học` HOẶC `MỖI VERSION CHỈ 1 NHU CẦU`)
  → Sau strip, grep trên `script_only` mới đáng tin. Verified case 25/07: Dodoto script có 9 match "hoa mỹ" trong file gốc → sau strip chỉ còn 0 match trong voice thật → 5/7 PASS thực sự. Rule ngầm: NEGATIVE examples trong tài liệu KHÔNG tính là vi phạm — chỉ voice mới tính.

- **PITFALL "WPM target 200-250 KHÔNG phải hard cap, 250-330 OK cho script ngắn hơn" added v0.13.0 25/07/2026 (from Dodoto + ARMAF Limoni verify pass).** Anti-pattern (false FAIL): agent count words / (3 versions × 110s) → WPM 308-323 → kết luận "FAIL vượt target 200-250" → phải rút gọn ~100 từ/version. **Fix**: WPM 200-250 là target văn nói TỰ NHIÊN (khi nói chậm, đủ thở), NHƯNG script đời thường 90-110s với nhịp NHANH 250-330 WPM vẫn OK khi:
  - Part đầu (Hook + Pain) nén 5-10 từ/câu, fragment 3-5 từ → WPM cao
  - Part sau (Solution + Proof) chậm lại vì nhiều số liệu → WPM thấp
  - Average toàn script OK vì mix 2 nhịp
  **Rule verify mới**: WPM 200-280 = PASS chính xác (target narrow). WPM 280-330 = PARTIAL (acceptable, không cần rút gọn). WPM > 330 hoặc < 200 = FAIL (cần fix). Verified case 25/07: Dodoto WPM 323 và ARMAF Limoni WPM 308 đều PARTIAL nhưng user không reject — đọc script thấy nhịp hợp lý vì mix câu dài-ngắn.