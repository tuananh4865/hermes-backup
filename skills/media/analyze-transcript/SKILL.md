---
name: analyze-transcript
description: 'Analyze transcript MD output (from tiktok-video-editor classify_segs.py) to detect narrative structure. Classifies each seg into HOOK/PROBLEM/SOLUTION/USP/COMPARE/AUTHORITY/CTA clusters + outputs time ranges. Used AFTER classify_segs.py to provide context analysis for the keep_plan build step. v3.19.1 NOTE: output is FEED for manual narrative-aware review (STEP 3 of tiktok-video-editor workflow), NOT a final keep_plan.'
tags: [narrative-analysis, transcript, hoặch, keep-plan-feed, v3.19.1-step3]
---

# Analyze Transcript — Narrative Cluster Detection

## Purpose
After `classify_segs.py` outputs `transcript_full.md`, this script reads the MD and detects narrative clusters (HOOK/PROBLEM/SOLUTION/USP/COMPARE/AUTHORITY/CTA). The output `narrative_analysis.md` gives the agent context to build a context-aware keep_plan.

## Usage

```bash
python3 scripts/analyze_transcript.py <transcript_md_path> [output_md_path]
```

Default output: `<transcript_md_dir>/narrative_analysis.md`

## What it does

1. **Parse MD**: read `transcript_full.md` table format → list of (idx, start, end, text)
2. **Classify each seg** by keyword matching:
   - `HOOK_KWS = ['mất 50%', 'không mua là thiệt', 'nên mua', 'cái này', 'bạn nào sở hữu', 'gia đình nào cũng']`
   - `PROBLEM_KWS = ['vấn đề', 'hỏng', 'tốn tiền', 'tốn thời gian', 'va chạm', 'vép', 'lỗi', 'khó chịu', 'lười', 'dây dài', 'gãy', 'rơi', 'hư']`
   - `SOLUTION_KWS = ['giải quyết', 'bảo vệ', 'phòng bệnh', 'đáp ứng', 'thay thế', 'nhanh hơn', 'tốt hơn', 'giải pháp', 'cứu']`
   - `USP_KWS = ['gấp gọn', 'nhỏ gọn', 'đa năng', 'thông minh', 'chắc chắn', 'mạnh', 'bền', 'tiện lợi', 'cao cấp', 'tinh tế', 'đầu hút', 'đầu thổi', 'phụ kiện']`
   - `COMPARE_KWS = ['so với', 'khác với', 'trong khi', 'còn', 'thay vì', 'ốp gốc', 'ốp góc', 'so sánh']`
   - `AUTHORITY_KWS = ['mình dùng', 'cá nhân', 'kinh nghiệm', 'từ khi', 'đã dùng', 'test', 'thử', 'review', 'phiên bản', 'nhà']`
   - `CTA_KWS = ['bấm', 'mua hàng', 'đừng bỏ lỡ', 'link dưới', 'subscribe', 'đăng ký', 'giá', 'giá thành', '385', 'tùy voucher']`

3. **Output** `narrative_analysis.md` with:
   - Auto-detected cluster table (per seg)
   - Cluster summary (count per cluster)
   - Cluster time ranges (start→end per cluster)

## Integration with tiktok-video-editor workflow

```
1. Whisper transcribe → audio.json
2. classify_segs.py → transcript_full.md + keep_plan_troncau.txt
3. analyze_transcript.py → narrative_analysis.md       ← THIS SKILL
4. ⭐⭐⭐ AGENT reads transcript_full.md + narrative_analysis.md     ← v3.19.1 BẮT BUỘC STEP 3
   Then applies 4-question gate (UNDERSTAND-FIRST EDITING):
     - "Câu này nói gì?"
     - "Phục vụ cảm xúc nào trong emotional arc?"
     - "Câu nào khác nói ý này ngắn hơn không?"
     - "Nếu bỏ câu này, emotional arc có gap không?"
   → manual keep_plan with emotional-arc awareness
5. Build filter → render → verify
```

The narrative_analysis.md helps the agent understand WHAT the clip is about (product type, USPs, demo structure) before building the final keep_plan with proper feature coverage.

## ⚠️ IMPORTANT (v3.19.1 lesson — 10/07/2026)

This script's output is a **FEED for the manual narrative review step** — it is NOT the final keep_plan. The full UNDERSTAND-FIRST EDITING lesson says:

> *"Em phải thực sự đọc đầy đủ transcript và hiểu được nội dung sau đó phân tích điểm nào giữ điểm bào thừa bỏ đi được [...] hỗ trợ cho nội dung giúp đánh đúng vào tâm lý và cảm xúc của khách hàng thì mới là edit thành công."* — Tuấn Anh, 10/07

The agent had been treating `narrative_analysis.md` as the final word for keep decisions. Tuấn Anh's hand-edit of 3 clips after this script ran was 41-62% shorter — because the human read the transcript and understood emotional arc, while the script only matched keyword clusters. Don't fall into that trap.

Cross-reference:
- `tiktok-video-editor` v3.19.1 — STEP 3 of 5-step workflow (ĐỌC-HIỂU-CẢM-XÚC)
- `video-cut-tiktok-shorts` v2.35 UNDERSTAND-FIRST section — 4-question gate before Step 3
