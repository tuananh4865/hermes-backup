---
name: clone-and-adapt-competitor
description: Feasibility analysis + adapted plan when user wants to clone a successful competitor for own project. Use when user says "phân tích tính khả thi + lên plan đi" after competitor research, or "clone kênh YouTube X", "em có nên làm giống Y không". Distinct from youtube-channel-audit (research only), business-opportunity-research (discover new streams), and plan (code-level implementation plan).
title: Clone & Adapt Competitor Analysis
created: 2026-07-11
updated: 2026-07-11
type: skill
tags: [planning, competitor-analysis, feasibility, clone, decision-matrix, roadmap, strategy]
confidence: high
relationships: [youtube-channel-audit, business-opportunity-research, plan]
---

# Clone & Adapt Competitor Analysis

You are evaluating whether to clone/adapt a successful competitor's strategy for the user's own project. Deliverable is a structured feasibility report + adapted roadmap. Triggered when user asks "clone kênh YouTube X", "em có nên làm giống Y không", "phân tích tính khả thi + lên plan đi".

## When to use this skill

- User asks "phân tích tính khả thi + lên plan đi" sau khi research competitor
- User wants to clone a successful creator/channel/product nhưng adapt cho own niche/resources
- User needs a 3-options decision matrix (100% clone / adapted / new direction)
- User asks "should I do X like Y?" với X = own project, Y = successful competitor
- User asks to "clone" a YouTube channel, TikTok account, podcast, or brand

**Distinct from:**
- `youtube-channel-audit` — chỉ research 1 channel (không có feasibility cho own project)
- `business-opportunity-research` — discover NEW income streams (không phải adapt existing competitor)
- `plan` — implementation plan cho code-level (không phải business-level decision)

**Workflow prerequisite (NEW 2026-07-11):**
If the competitor is a YouTube channel, ALWAYS load `youtube-channel-audit` FIRST (before this skill) to gather:
- Visual/branding patterns
- Title formula + description template
- Ecosystem map (sub-channels, social presence, partnership contacts)
- Top video case studies

This skill **inherits** audit findings — don't re-research what audit already collected. Audit Phase 1-13 covers everything you need for the feasibility comparison.

If user has NOT done a channel audit yet but says "clone kênh YouTube X", run the audit first, THEN come back to this skill for feasibility analysis.

**Reload-after-audit pattern (NEW 2026-07-11):** When user asks a follow-up dimension of an already-audited channel (e.g. "làm báo cáo chi tiết nữa về nội dung" after visual/branding audit), ALWAYS re-load `youtube-channel-audit` via `skill_view(name)` before continuing. Skill content auto-loaded earlier in the session may have rotated out of context — re-loading ensures Phase 9-13 deep-dive workflow rules (SRT extraction, confidence annotations, content categories) are followed correctly. Pitfall Lesson #21 in `youtube-channel-audit` codifies this rule.

## Workflow (5 phases, follow in order)

### Phase 1 — Inherit from audit skill

Nếu competitor là YouTube channel, LOAD `youtube-channel-audit` first và inherit:
- Visual/branding analysis (Phase 1-8)
- Content/script analysis (Phase 9-13, nếu đã deep-dive)
- Case study reference file (`references/vuive-2026-07-11-case-study.md` style)

Nếu competitor KHÔNG phải YouTube channel (TikTok account, brand, podcast), use generic research pattern:
1. Browse/extract 30+ posts/contents
2. Catalog visual style + content formula + monetization
3. Extract founder philosophy nếu có (interviews, about pages)
4. Build case study file with verbatim evidence

### Phase 2 — Resources comparison (12-chiều matrix)

So sánh competitor resources vs user resources trên 12 chiều:

| Dimension | Competitor (0-10) | User (0-10) | Gap | Notes |
|---|---|---|---|---|
| Founder identity/persona | | | | |
| Team/Resources | | | | |
| Content niche (breadth) | | | | |
| Niche authority (cạnh tranh) | | | | |
| Niche monetization | | | | |
| Visual brand (mascot) | | | | |
| Knowledge depth | | | | |
| Customer access | | | | |
| Brand owner (xuất hiện trực tiếp) | | | | |
| Revenue runway | | | | |
| Time commitment | | | | |
| Audience overlap (mass vs niche) | | | | |

**Tính total** mỗi bên + gap percentage. **Identify**:
- **6 điểm mạnh user** (có lợi thế vs competitor) — dựa trên positive gaps
- **6 điểm yếu user** (rủi ro cần mitigate) — dựa trên negative gaps

### Phase 3 — 3-Options decision matrix

Đề xuất 3 options với risk/reward analysis:

**Option A — Clone 100%** (mass-market replication, no adaptation)
**Option B — Adapted Clone** (⭐ usually best — lấy pattern + adapt cho own strengths)
**Option C — New Direction** (pivot hoàn toàn, không clone)

Score matrix:

| Option | Khả thi | ROI | Synergy với existing business | TOTAL |
|---|---:|---:|---:|---:|
| A | x/10 | x/10 | x/10 | x/30 |
| B | x/10 | x/10 | x/10 | x/30 |
| C | x/10 | x/10 | x/10 | x/30 |

Recommend ONE option dựa trên highest score + strategic fit with user's situation.

### Phase 4 — Adapted plan (12-tháng roadmap)

Nếu Option B thắng, viết plan chi tiết:

**4.1 Brand concept**
- Tên kênh (đề xuất)
- Tagline
- Positioning
- Target audience
- Brand voice (mix competitor's tone + user's strengths)
- Mascot (KHÔNG copy — adapt)
- Visual style (photo real + graphic overlay nếu user is brand owner)
- Color palette (match user's existing brand colors)
- Logo brief

**4.2 Series pipeline (35-46 clips trong 9-12 tháng)**
- 5 series chính, mỗi series 5-12 clips
- Mỗi series = 1 competitor pattern adapted
- Total clip count + frequency

**4.3 Script template (5-PART structure)**
- Hook + Nguồn (0:00-0:30)
- Cam kết (0:30-1:00)
- Table of Contents (1:00-2:00)
- Deep Dive (mỗi segment ~2p, 4-PHASE: Định nghĩa → Số liệu → Case → Takeaway)
- CTA + Moral

**4.4 Visual style ADAPTED**
- Mascot: KHÔNG copy competitor's mascot — dùng user himself/herself
- Thumbnail: photo real + 1 dòng text punchy (vs competitor's NO big-font rule)
- Color: match user's existing brand
- Animation: real photo + graphic overlay
- Faces: user xuất hiện (vs competitor's anonymous mascot)

**4.5 4-Phase Launch Roadmap (12 tháng)**
- **Phase 1: Foundation** (T1-2) — 1K subs. Setup + 8 pilot clips
- **Phase 2: Iteration** (T3-6) — 10K subs. 24 clips + community + cross-platform
- **Phase 3: Scaling** (T7-9) — 50K subs. 2 clips/week + sponsor outreach
- **Phase 4: Maturity** (T10-12) — 100K subs. 2-3 clips/week + membership

Mỗi phase có KPI table:
- Subs milestone
- Total views
- Comments
- Conversion (cho user's business nếu applicable)
- Revenue (nếu applicable)

**4.6 Monetization roadmap**
| Nguồn | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|---|
| YouTube AdSense | | | | |
| Shop affiliate | | | | |
| Sponsorship | | | | |
| Membership | | | | |
| **TỔNG** | | | | |

**Break-even point** (khi revenue covers cost)

**4.7 Resource requirements**
- Time commitment per phase
- Equipment needed
- Editor (in-house vs freelance vs AI)
- Studio setup
- Budget per phase

**4.8 Risk analysis**
- 7 risks với Probability + Impact + Mitigation
- Burnout risk #1 (solo creator)
- Niche TAM limitation
- Algorithm changes
- Competitor reaction
- Sponsor availability
- Personal appearance comfort
- Content supply sustainability

### Phase 5 — Decision & next steps

**5.1 Recommend ONE option** với 5 lý do cụ thể
**5.2 Next deliverables** (nếu user accepts Option B):
- Week 1: 3 pilot scripts + channel branding brief + description template
- Week 2: 4 scripts Series #2 + thumbnail mockups + recording checklist
- Week 3-4: Quay 8 clips pilot + edit + upload + cross-post

## Pitfalls (read before starting)

1. **Don't ship Option A (100% clone) without serious analysis.** 100% clone rarely works because user doesn't have competitor's resources (team, time, network). Adapted clone = better strategic fit 90% of cases. **EXCEPTION:** if user explicitly says "clone luôn / 100% giống / y chang" AFTER seeing the 3-option matrix, then Option A IS the right call (entertainment-first, mass-market, style replication matters more than shop synergy). When this happens, ship Option A with full quality — don't second-guess.

2. **Don't conflate "audience size" with "strategic fit."** Competitor có 1.18M subs ≠ user phải target 1.18M. User's TAM (Total Addressable Market) có thể khác + user's competitive advantage có thể khác.

3. **Don't recommend Option C (new direction) without first exhausting A+B.** User thường đã invest vào A or B rồi mới hỏi C. Pivot hoàn toàn = wasted effort.

4. **Don't use generic roadmap copied from internet.** Roadmap PHẢI phù hợp với user's specific resources + timeline + risk tolerance.

5. **Don't promise quick wins.** Phase 1-2 thường chỉ 1K-10K subs = NOT impressive. Set realistic expectations.

6. **Don't skip risk analysis.** Burnout, niche quá hẹp, algorithm change = top 3 failure modes. Always include mitigation.

7. **Don't recommend monetization WITHOUT showing path to first revenue.** User cần biết khi nào break-even để decide continue.

8. **Don't ignore user's existing strengths.** Adapted clone = amplify user's strengths, không phải copy competitor's strengths.

- khi viết pilot, tự hỏi trước khi thêm bất kỳ claim mới nào: "claim này có trong dossier không?". Nếu không → bỏ hoặc đổi sang wording an toàn ("theo mô hình", "có thể").
11. **Patch + re-verify trong cùng session (NEW 29/07 evidence-dossier pipeline).** Adversarial verifier lần 1 bắt được 8 câu ngoài dossier; sau khi patch vẫn còn 2 câu sót (lensing detail + supermassive seed chain). **Quy tắc: nếu PARTIAL_PASS / FAIL, KHÔNG được skip verdict. Phải patch từng line rồi gọi lại Layer 2 cho tới PASS.** Nếu bỏ qua, script lỗi sẽ ship. Verifier thường flag sau 1–2 vòng vì câu phụ dễ giấu giữa câu chính xác. Khi viết pilot, tự hỏi trước khi thêm bất kỳ claim mới nào: "claim này có trong dossier không?". Nếu không → bỏ hoặc đổi sang wording an toàn ("theo mô hình", "có thể").

12. **Test mỗi chapter đủ 4-PHASE + ép spoken word trong tầm 3.000–3.500 (NEW 29/07).** Pilot 20 phút ở 150–170 từ/phút tiếng Việt. Tách spoken section bằng marker `# NGUỒN` để word count đo đúng. Verifier part 1 thường flag thêm "chapter thiếu takeaway" nếu nhiều chapter không có câu chốt. Sau 3.314 từ → 3.276 từ sau 2 vòng patch, đủ an toàn để ship.

13. **Match deliverable shape to prompt scope (NEW 2026-07-29).** "Nghiên cứu script cho youtube X" ≠ "phân tích tính khả thi clone kênh X". Scope = SCRIPT only → ship cheat-sheet, not 3000-5000 word feasibility plan. Detect scope keywords: full plan triggers ("phân tích feasibility / lên plan / launch roadmap") vs narrow triggers ("script / công thức / khung / template"). Wrong shape = user phải scroll qua nhiều content không cần.

11. **Verify upstream audit visual style claims before propagating to deliverables (NEW 2026-07-11).** When you inherit visual/branding claims from `youtube-channel-audit` (Phase 3 thumbnail vision analysis) into downstream artifacts (mascot prompts, replicate briefs, generation prompts), DOUBLE-CHECK the claims by `vision_analyze` on the actual mascot/avatar image from the channel — NOT just the thumbnails. Thumbnails may have a DIFFERENT art style than the mascot image (e.g. channel uses Western Cartoon Mỹ for mascot but rendered thumbnails in different style). **Real case 2026-07-11:** When generating mascot prompts for @VuiVe, I propagated the visual style claims from `youtube-channel-audit` ("2D chibi cartoon") directly into the mascot generation prompt. The user corrected me TWICE: first saying "phong cách vẽ không phải 2D chibi cartoon đâu em check lại" then providing the actual mascot image. Vision analysis on the mascot revealed it was Western Cartoon Mỹ (Adventure Time/Gumball style), NOT chibi. **Lesson:** When auditing + replicating a competitor's brand, the mascot/avatar image is the AUTHORITATIVE source for character style — not the thumbnails. ALWAYS `vision_analyze` the mascot image directly before generating clone-style content. Saved ~1 round of bad prompt generation. **Rule:** Before writing any prompt that copies competitor style (mascot, illustration, animation), `vision_analyze` the COMPETITOR'S MASCOT/AVATAR image at high res, NOT the video thumbnails. Thumbnails may be rendered by different artists / be in different format (collage vs character foreground).

## Cheat-Sheet Deliverable Mode (NEW 2026-07-29)

When user prompt is **"nghiên cứu script X"** / "công thức script X" / "khung script cho X" (short, scoped to SCRIPT dimension only, NOT full feasibility plan):

**DO NOT** ship the full 3000-5000 word feasibility plan. User wants the CLONE-READY CHEAT SHEET — actionable template họ có thể áp dụng ngay.

**Trigger signals:**
- "nghiên cứu script cho youtube X" (scope = script only)
- "công thức script clone X"
- "khung script X" / "template script X"
- No mention of "plan / feasibility / 3-options / roadmap / launch"

**Workflow cheat-sheet mode:**
1. ✅ Check wiki FIRST: `search_files` for existing research files (`*X*analysis*`, `*X*research*`, `*X*report*`)
2. ✅ Read existing transcripts/concepts — DON'T re-extract từ YouTube
3. ✅ Synthesize từ NGUỒN CÓ SẴN thành framework ngắn gọn
4. ✅ Deliver in chat (Telegram-readable): tables + formulas + key patterns
5. ❌ Skip 12-dimension matrix
6. ❌ Skip 3-option decision matrix (no options to choose)
7. ❌ Skip 12-month roadmap
8. ❌ Skip risk analysis

**Output structure (cheat-sheet):**
1. Tổng quan khung video (duration + phases table)
2. Công thức từng phần (Hook formula, segment structure, outro formula)
3. Cấu trúc retention technique (specific interrupts + frequency)
4. Style đọc (voice characteristics)
5. Kết luận ngắn: copy gì, bỏ gì, bắt đầu ở duration nào

**Real case 2026-07-29:** User asked "nghiên cứu script cho youtube vuive clone". Em đã check wiki → tìm thấy 2 reports đã có (`youtube-channel-vuive-content-script-analysis-2026-07-11.md` 33.5KB + `REPORT-CHUYEN-SAU-2026-07-24.md` 30.7KB) → synthesis cheat-sheet 5 phần trong chat (5-PART structure, 4-PHASE segment, hook 4 lớp, retention, style, outro). Không ship full feasibility plan vì scope quá nhỏ.

**Rule:** Match deliverable shape to user prompt scope. "Nghiên cứu script" ≠ "Phân tích feasibility clone kênh". Detect scope trước khi decide output format.

## Output Format

Save to:
```
/Volumes/Storage-1/Hermes/wiki/projects/<user-project>/<competitor>-clone-feasibility-plan.md
```

Structure (3000-5000 words):
1. **So sánh resources** (12-chiều score matrix + 6 strengths + 6 weaknesses)
2. **3 Options + Decision Matrix**
3. **Plan chi tiết Option recommended** (Brand + Series + Script + Visual)
4. **4-Phase Launch Roadmap 12 tháng** (KPIs mỗi phase)
5. **Monetization Roadmap**
6. **Resource Requirements**
7. **Risk Analysis**
8. **Decision & Next Steps** (recommend + 5 lý do + week-by-week deliverables)

Verified sources:
- Inherit từ audit skill (case study file)
- User's wiki project folder (existing assets, products, content calendar)
- User's memory (preferences, schedule, existing channels)

## Real Case Implementation (2026-07-11)

> **Full verbatim case study (12-dimension matrix + 3 pilot scripts + branding template + 30-day plan):** see `references/vuive-edutainment-case-study.md`. This file below is the summary; load the reference for actual scripts.

**Trigger:** User asked "phân tích tính khả thi + lên plan đi" sau khi audit xong kênh @VuiVe (1.18M subs edutainment).

**Recommended Option:** B (Adapted Clone) với concept "Cầu Lông Đúng Cách"

**Why adapted (not 100% clone):**
- User có customer access + knowledge depth + product portfolio + brand owner (4 advantages vs competitor)
- User KHÔNG có studio team + 5 năm experience + 10 channels (3 disadvantages)
- Pure clone would waste user's strengths (knowledge + customer)

**Critical insight từ session:** Option B score 25/30 vs Option A 11/30 vs Option C 20/30. Adapted clone dominates vì tận dụng user's strengths.

**Later in session:** User switched to Option A after seeing the matrix ("clone nội dung giống vui vẻ luôn, kiểu fact thú vị"). Skill correctly fired EXCEPTION rule (Pitfall #1) → shipped Option A with full quality. User confirmed separate project folder ("Project nằm ngoài độc lập chứ không nằm trong project badminton") → Skill correctly fired Pitfall #9 → created `wiki/projects/youtube-clone-vuive/` as separate folder.

**Mascot from photo (NEW 2026-07-11):** User explicitly asked to convert his real portrait into @VuiVe-style cartoon mascot ("chuyển hình của anh thành cách vẻ giống của vui vẻ"). When this trigger fires, load `references/mascot-from-photo.md` for the 4-step workflow + 4 prompt variations. Image generation may fail (FAL auth error 2026-07-11) — report blocker with copyable prompt template, don't fabricate output.

### KarmaVid — Adapted Clone of @herocat2309 (NEW 2026-07-11)

> **Full case study:** `references/karmavid-adapted-clone-case-study.md`

**Trigger:** User asked "phân tích tính khả thi + lên plan đi" sau khi audit kênh @herocat2309 (TikTok animation 2.5D onion girl, 120.7M views top video).

**Key difference vs @VuiVe case:**
- @VuiVe (edutainment): chốt Option A ngay (single direction)
- **KarmaVid (Pixar 3D animation): 5 PIVOTS trong 1 ngày** (16:32 → 18:25)

**5-pivot timeline (focus shift pattern):**
1. V1→V2: Visual (character form) — đồ ăn → CON NGƯỜI
2. V2→V3: Visual (style) — voxel → Pixar (typo correction)
3. V3→V4: Tool stack — Blender manual → Google AI (Gemini + Veo 3)
4. **V4→V5: Narrative depth** — visual+tool → +Character Bible 12 fields + 8 phần world-building

**Recommended Option:** B (Adapted Clone) — Visual Pixar 3D CON NGƯỜI Vietnamese + Karma concept (giữ nguyên từ @herocat2309) + 8-scene formula + 6-character universe

**Critical success factor:** Mỗi pivot có 1 FOCUS DIMENSION duy nhất → giữ nguyên layers trước + thêm layer mới. KHÔNG đổi toàn bộ. Áp dụng matrix pivot (giữ nguyên / đổi / thêm) trước mỗi pivot.

**5 lessons vĩnh viễn encoded trong `pixar-3d-animation` skill:**
1. Pivot Focus Shift pattern
2. Character Bible 12 Fields
3. NO REDEMPTION Arc (villain hard rule)
4. Karma Score tracked (consistency tool)
5. Confirm phrase ambiguous trước khi re-design

**Output:** 1 universe file × 50.3 KB (9,102 từ) + 4 deliverable files × ~18 KB = ~200 KB total.

## Related Skills

- `youtube-channel-audit` — upstream skill cho competitor research
- `business-opportunity-research` — cho NEW opportunities (không phải adapt existing competitor)
- `plan` — implementation plan cho code-level (không phải business-level decision)

## References

- `references/youtube-dom-extraction.md` — concrete JS/curl snippets for extracting video grid data, watch-page descriptions, playlist URLs, thumbnail downloads, and ecosystem signals (emails, phones, sub-channels, partnership contacts). Updated for the 2026 YouTube web layout.
- `references/vietnamese-youtube-grammar.md` — field notes on VN listicle channel title formulas, thumbnail grammar, description template, ecosystem signals, and hit-video patterns. Use as prior for Vietnamese channels; verify each claim.
- `references/vuive-2026-07-11-case-study.md` — verified reference data + lessons learned từ 2 sessions audit kênh @VuiVe ngày 2026-07-11 (visual/branding audit + script/narrative/retention/depth deep-dive). Dùng làm benchmark khi audit các kênh edutainment/facts VN khác, hoặc khi so sánh với kênh cầu lông đang xây.
- `references/mascot-from-photo.md` — 4-step workflow for generating a 2D chibi cartoon mascot from user's real portrait (when cloning edutainment channels that use signature mascots like @VuiVe). Load when user sends a portrait photo and asks for cartoon mascot conversion.
- `references/karmavid-adapted-clone-case-study.md` — **NEW 11/07 — KarmaVid case study (clone + adapt @herocat2309 onion girl universe thành Pixar 3D Vietnamese CON NGƯỜI). 5 pivots trong 1 ngày (visual → tool → narrative depth). Recommended Option B (Adapted Clone) với Google AI tool stack (Gemini Nano Banana Pro + Veo 3). 12-dimension resources matrix + 5 lessons vĩnh viễn encoded trong `pixar-3d-animation` skill.**
- `references/evidence-dossier-script-pipeline.md` — **Updated 29/07 — Evidence-dossier → script pipeline for cloning YouTube edutainment CONTENT STYLE onto a facts/science topic. 5 phases (inherit audit → scope → evidence dossier FIRST → script with [N] citations → 3-layer verify → fix loop). Forbidden-claim-list pattern + independent-verifier subagent + patch + re-verify rule (caveat: now requires minimum 2 verifier rounds — 1st pass often leaves 2 unsupported phrasings inside accurate chapters). Used 2026-07-29 to produce @VuiVe-style 20-min astronomy pilot (black holes, NASA/LIGO sources).**

## Evidence-Dossier-First Script Mode (NEW 2026-07-29)

When user asks "nghiên cứu X để viết script" / "thu thập bằng chứng cho script X" / "viết pilot script về chủ đề Y" — the deliverable shape is the FULL SCRIPT, not a feasibility plan. Workflow:

**Phase 1 — Inherit from audit skill.** Same as before. Load existing case study if user is cloning a known creator.

**Phase 2 — Scope the pilot.** Em ask user only if scope is genuinely ambiguous. Default: choose 1 pilot topic, 1 deliverable script, 1 folder structure. Don't propose 3 options for a single-topic script request.

**Phase 3 — Evidence dossier FIRST, script SECOND.** This is the critical phase. Two-step inside:
- **3a. Source mapping.** List the 8-15 evidence sources needed to cover the topic (NASA + ESA + LIGO + Wikipedia for facts topics; creator channel data for creator-style topics). For each source, capture the canonical URL.
- **3b. Evidence dossier file.** Build `/Volumes/Storage-1/Hermes/wiki/projects/<project>/research/<topic>-evidence-dossier-<YYYY-MM-DD>.md` with: claim sections (one per chapter), confidence per claim (HIGH/MEDIUM/LOW), citations to sources, explicit "claim cấm" (forbidden) list, chapter map showing which evidence feeds which chapter. DO NOT write script until this file exists.
- **3c. Forbidden-claim list.** Explicit list of "do not assert" claims (e.g. for black holes: "hố đen hút mọi thứ", "chân trời sự kiện = bề mặt rắn", "điểm kỳ dị = vật thể mật độ vô hạn"). Any script draft that violates the list must be rewritten.

**Phase 4 — Script with inline [N] citations.** Draft the script chapter by chapter in the order: Hook → scope-disclaimer → TOC → Chapter 1 → ... → Chapter N → Moral outro. Every numeric claim MUST carry an inline `[N]` marker that maps to the corresponding numbered citation in the script's # NGUỒN section. Multiple chapters may share a citation.

**Phase 5 — 3-layer independent verification.** Before declaring "xong":
- **Layer 1 — Internal automated check.** Run a Python check that asserts: chapter count = planned; inline `[N]` markers resolve to the # NGUỒN list; no forbidden-claim phrase appears in body; spoken word count is in the target range (3.0k-3.5k words for 18-22 min target).
- **Layer 2 — Adversarial subagent verifier.** Dispatch an independent leaf subagent with the script path + evidence dossier path + a 3-layer audit prompt (STRUCTURAL: chapter count + hook/outro/sources; SEMANTIC: every claim supported, uncertainty wording preserved, no mythology stated as fact; FUNCTIONAL: natural Vietnamese spoken voice, each chapter follows definition/evidence/example/takeaway, no copied source wording). Demand VERDICT PASS/FAIL/PARTIAL_PASS with raw counts AND exact problematic lines.
- **Layer 3 — Fix loop.** If verifier returns PARTIAL_PASS or FAIL, PATCH the script (don't ignore the verdict) to address EACH cited line. Re-verify in same session.

**Phase 6 — Final QA.** Forbidden-claim grep + citation-mapping grep + spoken-word-count grep. Only declare "xong script" after all 3 layers green.

**Skill defaults:**
- Default length: 18-22 minutes spoken ≈ 3.0k-3.5k words at 150-170 wpm Vietnamese narration.
- Default inline citations: ≥10 numbered sources, every claim with a number MUST carry `[N]`.
- Default chapter map: define chapter map (Câu hỏi giữ người xem × Bằng chứng chính × Confidence) BEFORE writing chapters. Means you never write a chapter whose evidence can't be cited.
- Default verify mandatory: do not skip Layer 2 even when confidence is high.

**Real case 2026-07-29 (black holes pilot):** User asked "nghiên cứu script cho youtube vuive clone" → picked astronomy → user picked "thiên văn – vũ trụ" → user said "oke bắt đầu nghiên cứu thu thập bằng chứng để viết script đi" → built evidence dossier FIRST (file 15.0KB, 10 chapters mapped, 19 sources) → user asked "làm tiếp đi" → wrote 10-chapter script with 33 inline citations (3.3k words) → adversary subagent returned PARTIAL_PASS with 8 specific problematic lines → patched all 8 + added takeaway lines to 5 chapters → re-verification. Workflow produced shippable pilot in single session.