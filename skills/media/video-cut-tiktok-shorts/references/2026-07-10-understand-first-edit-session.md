# 2026-07-10 — UNDERSTAND-FIRST EDITING session (lensMacroKF / TripodZ / kfCleanPen)

## Context

Tuấn Anh took 3 clips the agent had previously auto-edited (output V1) and re-edited them by hand. **Every single one was 41-62% shorter than the agent's V1.** The agent was running an `auto-classify + apply patterns` pipeline without ever reading the transcripts.

Three clips in `Tiktok-Tuan-Anh/` re-edited folder:
- `lensMacroKF.mov` (lens macro KNF cho Pocket 3 — 101.8s anh dựng, source 250.92s)
- `TripodZ.mov` (tripod ULANZI 1m6 — 90.5s anh dựng, source 267.27s)
- `kfCleanPen.mov` (bút vệ sinh KNF — 117.4s anh dựng, source 216.18s)

## User's 3 verbatim corrections (escalating)

### #1 — First mild prompt
> *"Cải tiến skill transcript viết hết ra file md sau đó em phải đọc và phân tích ngữ cảnh từng transcript xem nội dung nói về cái gì sau đó lọc ra các đoạn câu có nghĩa hoàn chỉnh để cắt ghép và loại bỏ các khoảng lặng, câu treo và ựm ờ à tránh việc có câu treo trong video (câu treo là một câu dài hơn 2 từ trở lên và khác với từ đơn vô nghĩa nha, cả 2 đều phải loại bỏ nhưng thường em hay chỉ loại bỏ từ đơn vô nghĩa mà không loại bỏ câu treo vô nghĩa)"*

Surface ask: write transcript to MD and apply better classify. Hidden ask: "I have to remind you about câu treo every time" — agent was only catching 1-word filler, missing 2+ word hanging sentences.

### #2 — Second escalation, after the 5-clip session
> *"Em phải thực sự đọc đầy đủ transcript và hiểu được nội dung sau đó phân tích điểm nào giữ điểm bào thừa bỏ đi được thì sẽ làm được như anh thôi."*
> *"Tìm cách nâng cấp skill lên để edit clean được như anh đi"*

This is the core lesson — agent had NOT been reading transcripts at all. Just running scripts.

### #3 — Third escalation, after v3.19.0 pattern-compact attempt still fell short
> *"Ủa là từ trước tới giờ em vẫn không tự đọc hiểu ngữ cảnh của transcript để đưa ra lựa chọn chính xác à?"*

Frustration signal — agent tried to fix by adding 7 MORE patterns (BRIDGE_NGAN, USP_LAP, CTA_HARDSELL, DEMO_DAI, INTRO_DAI, TREO_FILLER, NARRATIVE_COMPACT) via `narrative_compact.py` script. Result: still 15% shorter than user's, still missing the understand-first principle.

### #4 — Final, blunt statement
> *"Fix lại skill để em luôn phải tự đọc hiểu transcript và chọn ra các đoạn keep chính xác đúng mục đích và hỗ trợ cho nội dung giúp đánh đúng vào tâm lý và cảm xúc của khách hàng thì mới là edit thành công chứ em không hiểu được nội dung clip thì làm sao cắt thành công được"*

Compiled lesson: **Edit thành công = ĐỌC HIỂU nội dung + ĐÁNH ĐÚNG tâm lý/cảm xúc khách hàng.**

## Real metrics (proof user's complaint was valid)

| Clip | Source | Agent V1 auto | User re-edit | User saved |
|------|--------|---------------|--------------|------------|
| 0706 lensMacroKF | 250.92s | 163.24s | 94.48s | -68.76s (**-42%**) |
| 0705 kfCleanPen | 216.18s | 197.30s | 117.10s | -80.20s (**-41%**) |
| 0715 TripodZ | 267.27s | 236.91s | 90.40s | -146.51s (**-62%**) |

User's savings came from cutting **different segments**, not just cutting more. User read transcripts and understood narrative arc; the agent had pattern-matched.

## What user dropped that agent kept (7 pattern categories)

1. **BRIDGE_NGAN** — Short 2-3 word transitions like "vô tư" / "ở đây nè" / "á" / "ha" / "nhé" (chuyển tiếp, không emotional beat)
2. **USP_LAP** — Same feature repeated 2+ times, kept only 1 with full predicate
3. **CTA_HARDSELL** — "Bấm link mua hàng" hard-sell closing → replaced with emotional close ("bền bĩ hơn theo thời gian") or removed
4. **DEMO_DAI** — Long demo 3-5 sentences → kept 1 sentence summarizing
5. **INTRO_DAI** — 3-4 sentence HOOK → tightened to 1 punchy sentence
6. **TREO_FILLER** — Câu treo 2+ words with predicate rời (anh đã dạy: "câu treo dài hơn 2 từ trở lên là TREO khác với từ đơn vô nghĩa")
7. **NARRATIVE_COMPACT** — One feature → 1 sentence ngắn gọn nhất serving emotional arc

But: **the 7 patterns alone CHƯA produce user's results** (still 30-90s longer than user). The missing axis is the **emotional arc check** ("does this serve a HOOK/PROBLEM/SOLUTION/USP/AUTHORITY/CTA beat? if not, drop it"). Patterns can be applied to wrong sentences. Only after reading the transcript and answering "what emotion does this serve" can the agent decide correctly.

## v2.35 patch — what changed

`video-cut-tiktok-shorts` SKILL.md gained:
- Section "🧠 UNDERSTAND-FIRST EDITING (v2.35)" inserted BEFORE `## Pitfall NSP-100%-NOT-HALLUCINATE`
- 4-question gate that must be applied BEFORE Step 3 (Build TikTok Script):
  1. "Câu này nói gì?" — tóm tắt được
  2. "Phục vụ cảm xúc nào trong emotional arc?"
  3. "Câu nào khác nói ý này ngắn hơn không?"
  4. "Nếu bỏ câu này, emotional arc có gap không?"
- Emotional arc template (HOOK 0-3s / PROBLEM 3-10s / SOLUTION+USP 10-30s / AUTHORITY 30-50s / CTA 50-60s)
- Cross-reference to `tiktok-video-editor` v3.19.1 (in-play umbrella carrying the same lesson)
- Bumped `updated:` field 2026-07-02 → 2026-07-10
- Added tags: `understand-first`, `emotional-arc`, `customer-psychology`, `v2.35`

## What `tiktok-video-editor` v3.19.1 added (umbrella carrier)

The 10/07 escalation happened while editing via `tiktok-video-editor` workflow. That skill already had a 3-LAYER REASONING section (Lớp 1 ngữ pháp / Lớp 2 mục đích sản phẩm / Lớp 3 framework position) referenced from `video-cut-tiktok-shorts`. v3.19.1 extended Lớp 2 with **emotional arc / customer psychology** as Lớp 4 implicit check.

Workflow v3.19.1 5-step:
1. Whisper transcribe → audio.json
2. Auto-classify → transcript_full.md + keep_plan_troncau.txt (DRAFT)
3. ⭐⭐⭐ ĐỌC-HIỂU-CẢM-XÚC (BẮT BUỘC)
4. Chọn keeps narrative-aware
5. Render → re-Whisper verify → 4-DIM gate

Step 3 is the new mandatory gate. v3.19.0 NARRATIVE-COMPACT (7-pattern auto-apply) was SUPERSEDED — pattern-only insufficient.

## Lesson captured across both skills

**For future Vietnamese TikTok editing sessions:**

1. NEVER trust `classify_segs.py` output as final — it's DRAFT
2. ALWAYS read `transcript_full.md` end-to-end before any keep/remove decision
3. ALWAYS ask the 4 questions at every decision point
4. NEVER trust pattern scripts (`narrative_compact.py`) without narrative-aware review
5. The agent's job is to serve **customer psychology** — features are evidence, emotion is the editor

## Files affected

- `/Users/tuananh4865/.hermes/skills/media/tiktok-video-editor/SKILL.md` → v3.19.1 (patched this session)
- `/Users/tuananh4865/.hermes/skills/media/video-cut-tiktok-shorts/SKILL.md` → v2.35 with UNDERSTAND-FIRST section (patched this session)
- `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` → appended 10/07 UNDERSTAND-FIRST section
- `/Users/tuananh4865/.hermes/skills/media/tiktok-video-editor/references/session-2026-07-10-3-clip-anh-dung-narrative-compact.md` → existing reference for the 3-clip case study

## Cross-references

- `tiktok-video-editor` v3.19.1 step 3 (read-understand-emotion gate)
- `video-cut-tiktok-shorts` v2.35 UNDERSTAND-FIRST section
- `analyze-transcript` — runs BEFORE manual review per v3.19.1 step 3
- `narrative_compact.py` at `/Volumes/Storage-1/Pocket3/Hermes-Edit/scripts/` — TOOL only, NOT sufficient
