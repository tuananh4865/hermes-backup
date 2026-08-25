# 2026-06-30 Clip Edit Iterations — Body Mix 110s → 55s

## Context
Tuấn Anh shared a 543 MB HEVC MP4 from Google Drive about Body Mix body spray (Vietnamese review). Asked em to edit clip with 9 atomic requirements. After V1, user said "không tốt, phải fix lại" — triggered 4 more iterations to reach acceptable quality.

## Source
- URL: `https://drive.google.com/file/d/1hlmtEy1syTSI67IbHWRn2dQLb6tzIqpU/view?usp=drivesdk`
- Resolution: 1728×3072 (9:16 portrait — preserved through all versions)
- Duration: 110.78s
- Size: 543 MB

## User's 9 atomic requirements (verbatim)
1. "Cắt ụm ờ" (cut filler "ờ", "ừm")
2. "khoảng nghĩ truyền tải nội dung ngắn gọn" (cut thinking pauses)
3. "Cắt các đoạn lặp voice anh thường khi nói sai sẽ lặp lại ở câu sau" (cut voice loops, keep MOST COMPLETE version)
4. "Ngắn gọn chỉ giới hạn dưới 2 phút thôi nếu dưới 1 phút càng tốt"
5. "Hãy làm theo các công thức tiktok" (apply TikTok formula)
6. "Giữ đúng tỉ lệ gốc của clip nhưng em gửi đang bị bóp lại thành hình vuông rồi!" (preserve 9:16)
7. "Cắt gọn hơn những khoảng ngừng nghĩ và kĩ hơn ở các câu từ khi dùng transcript"
8. "phải đánh dấu đúng đoạn cần cắt trước khi vào cắt clip" (MARK BEFORE CUT)
9. "tránh bị lặp ừm ờ, à và thừa câu từ" (avoid filler + redundant sentences)

## Iteration History

### V1 — FAILED (whole-segment cuts)
- Approach: Cut 11 full segments using segment-level timestamps
- Result: 55.02s, BUT multiple sentences broken at boundaries
- Specific failures:
  - CÂU 3 (tính chất): cut at 23.0s lost "khoái, phóng khoáng"
  - CÂU 5 (giữ mùi): cut at 38.0s lost "30 phút tới 1 tiếng thôi" — broken mid-word
  - CÂU 6 (cảm xúc): cut at 49.0s lost "rất là thích cái mùi này"
  - CÂU 8 (social proof): cut at 76.0s lost "Body Mix mà"
  - CÂU 16 (CTA): cut at 104.0s lost "Body Mix mà có thể bấm"
- User feedback: "Clip thành phẩm không tốt phải fix lại, có các đoạn ậm ờ không được cắt gọn, câu không đủ nghĩa đã bị cắt rồi!"

### V2 — Fixed to word-level precision
- Approach: Use `word_timestamps=True` in whisper-large-v3, cut at word boundaries only
- Result: 55.85s, all 10 sentences grammatically complete
- Removed CÂU 11 (CTA bridge "hôm nay mình mới lên mới review") to stay < 60s
- User assessment: 85%

### V3 — V2 + 2 improvements
- Added transition phrase between Action (54-59s) and Social proof (65-71s) to fix jump
- Tightened Social proof to end at "review" (was dangling at "là cái chai này")
- Result: 55.12s
- Issue: Transition "Nó cũng" too short (2 words), Social proof ends at "những" (dangling)

### V4 — Fixed V3 issues
- Extended transition to "Nó cũng đem lại cho mình một cái cảm giác" (2.82s)
- Extended social proof to include "review" (4.72s ending at natural word)
- Result: 57.19s
- User assessment: "Khá ok rồi" with new feedback about stretched vowels + stutter

### V5c — Removed stretched vowels
- Detected 27 words with duration > 0.6s
- Key stretches: `sạng` 1.36s, `chơi` 1.34s, `30` 2.30s, `đang` 1.40s, `tìm` 1.66s
- Action: split Tính chất (skip sạng), CTA (trim đang/tìm)
- Stutter "nó nó nó" in CÂU 4: kept as-is (removal breaks grammar)
- Result: 54.69s — accepted

## Key Learnings (extracted to SKILL.md Pitfalls #6, #7, #8)

1. **Word-level precision mandatory** — Always use `word_timestamps=True` with whisper-large-v3
2. **Detect stretched vowels** before building edit plan
3. **Accept stutters that break grammar** when removed
4. **Version output files** — never overwrite (allows comparison)
5. **Output path** = `/Volumes/Storage-1/Pocket3/Hermes-edit/clip_edited_v{N}.mp4`

## Final Files in `/Volumes/Storage-1/Pocket3/Hermes-edit/`
```
clip_edited_v1.mp4 (55.02s) — FAILED, broken sentences
clip_edited_v2.mp4 (55.85s) — 85% OK
clip_edited_v3.mp4 (55.12s) — fixed transitions
clip_edited_v4.mp4 (57.19s) — fixed dangling words
clip_edited_v5c.mp4 (54.69s) — FINAL, stretched vowels removed
```

## Time spent
- V1: 1 cut (broken) → user feedback → V2
- V2: 1 cut (working) → user feedback → V3
- V3: 1 cut (improved but new issues) → V4
- V4: 1 cut (working) → user feedback on stretches → V5c
- V5c: accepted as final

Total: 5 iterations, ~93 minutes of compute time per cut (ffmpeg HEVC decode + re-encode)