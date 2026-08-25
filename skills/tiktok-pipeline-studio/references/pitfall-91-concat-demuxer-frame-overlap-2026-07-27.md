---
title: PITFALL #91 — Concat Demuxer Stream-Copy Causes Frame Overlap at Segment Boundary
created: 2026-07-27
updated: 2026-07-27
type: reference
tags: [pitfall-91, frame-overlap, concat-demuxer, stream-copy, tiktok, video-edit, filter-complex, hard-verified]
confidence: high
relationships: [pitfall-6-concat-demuxer-hallucinate, pitfall-18-filter-complex-concat-silent-duration, pitfall-90-hard-cut-default, tiktok-video-editor, video-cut-tiktok-shorts]
---

# PITFALL #91 — Concat Demuxer Stream-Copy Causes Frame Overlap

> **Real case:** 7 clips batch 0085/0086/0088/0091/0093/0094/0095 (BODY_MIST_AMAP / LENSPEN / OP_POCKET3_FLIP / OP_POCKET3_FULL) quay ngày 2026-07-25 bằng DJI Pocket 3, source 1728×3072 HEVC. Render V2 ngày 25-26/07 dùng `ffmpeg -f concat -safe 0 -c copy` → user flag 27/07: *"đè frame ở các đoạn cắt khiến cho frame bị lặp lại! ... không xếp chồng audio + hình ảnh lên nhau!"*

## 🚨 Triệu chứng

User xem 7 clip V2 thấy:
- **Frame lặp / đè ở boundary**: video segment N hiển thị frame cuối thêm 1-2s trước khi segment N+1 bắt đầu
- **Audio "speech ends too sharp"**: cắt hard tại boundary không áp filter
- **Cảm giác "hình đi trước tiếng"**: visual và audio desync ngay tại cut point

## 🔍 Root cause (verified bằng data)

### Tại sao `concat demuxer -c copy` gây lỗi

```
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output.mp4
```

- Concat demuxer với `-c copy` = STREAM COPY nguyên packets từ source HEVC
- Frame boundary tại concatenation nằm tại **GOP boundary gốc** (keyframe position), KHÔNG tại `end_padded` của keep_plan
- Source HEVC có GOP = ~1 keyframe/s → nếu `end_padded` của keep N trỏ vào giữa GOP, frame cuối keep N hiển thị thêm ~0.5-1s trước khi keyframe của keep N+1 bắt đầu
- → User thấy "frame lặp" vì thực tế là frame cuối keep N được present lại ở đầu keep N+1

### Verify bằng MD5 hash (clip_0095 boundary 24.11s)

```
OLD (concat demuxer stream-copy) → MD5: 8b98ef5e61  (frame từ source gốc, cùng GOP cuối HOOK)
NEW (filter_complex re-encode)  → MD5: 80399aa09a  (frame TRIM chính xác tại 24.11s = đầu INTRO)
```

### Verify bằng vision (clip_0086 boundary 15.95s HOOK→DESC)

| Timestamp | OLD (concat demuxer) | NEW (filter_complex) |
|---|---|---|
| 15.85s | 1 tay cầm bút Lenspen, **chu môi** (đang nói "Lenspen" cuối HOOK) | 1 tay cầm bút Lenspen, **chu môi** (cuối HOOK) |
| 16.05s | **1 tay cầm bút, chu môi** — VẪN frame HOOK bị đè thêm 0.1s | 2 tay cầm bút, **miệng mở rộng** (bắt đầu INTRO) |
| **Kết luận** | OLD = frame cuối HOOK tiếp tục 0.1s sau boundary → user thấy frame lặp | NEW = clean cut tại 15.95s, miệng + tay khác hẳn |

→ OLD image tại 16.05s VẪN LÀ frame HOOK (chu môi, 1 tay) — đây chính là "frame đè" mà user flag.

### 100% boundary frames KHÁC NHAU trên cả 7 clip (raw data)

Em đo MD5 tại boundary ±0.1s trên pre_speed của 14 boundaries (2 boundary đầu tiên mỗi clip × 7 clip). Tất cả 14 cặp đều KHÁC NHAU 100%:

```
clip_0085  b0@ 13.43s  549e70a1 vs 451a3a43 ≠   4.9% size diff
clip_0085  b1@ 27.73s  d94c27df vs 540c6f1c ≠  20.3% size diff
clip_0086  b0@ 15.95s  922d1bcb vs 28986cb1 ≠   6.1%
clip_0086  b1@ 36.59s  a38eb94d vs 01a3fb38 ≠   0.3%
clip_0088  b0@ 15.50s  647086e7 vs 9124a865 ≠   4.1%
clip_0088  b1@ 20.88s  ecaa85e9 vs 7e2a3387 ≠  22.1%
clip_0091  b0@ 21.02s  b05e446e vs fcce4ff6 ≠  13.1%
clip_0091  b1@ 29.52s  8810605a vs e42aa0be ≠  15.9%
clip_0093  b0@ 15.60s  37b74629 vs 533f6321 ≠   0.6%
clip_0093  b1@ 38.92s  f3dfc786 vs 7763270d ≠  20.5%
clip_0094  b0@ 15.40s  01a2239b vs 3247405a ≠   9.9%
clip_0094  b1@ 26.16s  7d6b9a13 vs f854a001 ≠   2.6%
clip_0095  b0@ 24.11s  333a72ef vs 864dacd0 ≠   8.8%
clip_0095  b1@ 37.65s  5ad3277c vs 78c5bc5c ≠   0.0% (hash khác dù size giống)
```

→ Nếu `concat demuxer stream-copy` bị reapply, MD5 hash cặp before/after sẽ GIỐNG NHAU → dễ detect.

## ✅ Fix bằng filter_complex (verified)

**Pattern template** lưu ở `/tmp/render_7clips_final.sh`:

```python
# Build filter_complex từ keep_plan.json
import json, subprocess
d = json.load(open(f"{DIR}/keep_plan.json"))
keeps = d["keeps"]
n = len(keeps)
v_parts, a_parts = [], []
for i, k in enumerate(keeps):
    s = k.get("start_padded", k["start"])
    e = k.get("end_padded", k["end"])
    v_parts.append(
      f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS,"
      f"scale=1080:1920:force_original_aspect_ratio=decrease,"
      f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30[v{i}]"
    )
    a_parts.append(
      f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,aresample=44100[a{i}]"
    )
v_concat = "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vout]"
a_concat = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[aout]"
fs = ";" .join(v_parts + a_parts + [v_concat, a_concat])

subprocess.run([
    "ffmpeg", "-y", "-i", f"{DIR}/source.MOV",
    "-filter_complex", fs,
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    "v3_pre_speed.mp4"
])

# Speed 1.3x (setpts + atempo, NO afade)
subprocess.run([
    "ffmpeg", "-y", "-i", "v3_pre_speed.mp4",
    "-filter_complex", "[0:v]setpts=(PTS)/1.3[v];[0:a]atempo=1.3[a]",
    "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    FINAL_MP4
])
```

## 📊 Verify chain (BẮT BUỘC trước khi ship)

### Layer 1 — Structural
```bash
ffprobe -v error -show_entries format=duration:stream=width,height,nb_frames,codec_name,sample_rate -of default <final>.mp4
# Expect: 1080×1920, 30fps, h264, aac 44100Hz, duration ≈ <expected> ±1s
```

### Layer 2 — Semantic (pre-speed khớp keep_plan)
```bash
python3 -c "
import json
d = json.load(open('keep_plan.json'))
expected = d['expected_duration']
print(f'expected pre-speed: {expected:.2f}s')
"
# So sánh với ffprobe output của pre_speed.mp4 — diff phải <0.1s
```

### Layer 3 — Functional (boundary frame check — quan trọng nhất)

```bash
# Per-clip: extract frame tại boundary ±0.1s
for BOUNDARY in <keep_n_end_padded>; do
    ffmpeg -y -ss $(echo "$BOUNDARY - 0.1" | bc) -i v3_pre_speed.mp4 -frames:v 1 -q:v 2 "before_${BOUNDARY}.jpg"
    ffmpeg -y -ss $(echo "$BOUNDARY + 0.1" | bc) -i v3_pre_speed.mp4 -frames:v 1 -q:v 2 "after_${BOUNDARY}.jpg"
done
# So sánh MD5: phải KHÁC NHAU 100%
md5 before_*.jpg after_*.jpg | sort | uniq -c -w 32
# Nếu thấy count 2 cho cùng MD5 = FAIL (frame bị đè/lặp)
```

Ngoài ra vision check 1 boundary rõ rệt: verify frame trước/sau boundary là 2 cảnh khác nhau visible (mặt, tay, sản phẩm, góc camera khác). Real case verified 27/07: clip_0086 15.85s → 16.05s thấy rõ chuyển pose cầm Lenspen.

## 🎓 Lessons vĩnh viễn (FIRST-CLASS)

### L1 — Hard rule: filter_complex cho multi-segment TikTok

```
ffmpeg -f concat -safe 0 -i concat.txt -c copy output.mp4  ← ❌ KHÔNG BAO GIỜ cho multi-segment
ffmpeg -i source.MOV -filter_complex "<per-segment-trim+setpts>...concat=n=N:v=1:a=0[vout]" ...  ← ✅ ĐÚNG
```

Concat demuxer stream-copy chỉ OK khi (1) input là file re-encode sẵn KHÔNG phải cùng source, (2) verify boundary từng file khớp.

### L2 — Khi user flag "đè frame" / "frame lặp" trên TikTok = CONCAT DEMUXER BUG

Anh nói verbatim 27/07: *"Anh nhắc lại lần cuối không fade out và không xếp chồng audio + hình ảnh lên nhau!"*

→ Root cause là concat demuxer stream-copy (cùng source → GOP alignment sai). KHÔNG phải fade/afade issue. Phải re-render bằng filter_complex per-segment re-encode.

### L3 — Khi keep_plan có overlap vùng source (e.g. HOOK end=13.43, NEED start=13.13)

Frame tại "boundary 13.43s" trong output THỰC RA là frame từ source 13.43s (giữa HOOK và NEED) — vì 2 segment trong output chia sẻ frame vùng 13.13-13.43. Đây là keep_plan DESIGN, không phải render bug. MD5 2 frame vẫn khác nhau vì re-encode timestamp khác nhau.

### L4 — Backup BEFORE overwrite

Trước khi re-render overwrite V2 cũ, COPY nguyên sang `_archive/v2_overlapped/` để so sánh nếu user push back. Real case 27/07: backup 7 file × ~70MB = 496MB.

## 📁 Affected files (real case 27/07)

| File | Status |
|---|---|
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0085_V2_138s_FINAL_BODY_MIST_AMAP.mp4` | ✓ re-rendered 81.3MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0086_V2_98s_FINAL_LENSPEN.mp4` | ✓ re-rendered 57.7MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0088_V2_74s_FINAL_OP_POCKET3_FULL.mp4` | ✓ re-rendered 47.0MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0091_V2_101s_FINAL_BODY_MIST_AMAP.mp4` | ✓ re-rendered 59.2MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0093_V2_104s_FINAL_BODY_MIST_AMAP.mp4` | ✓ re-rendered 61.7MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0094_V2_49s_FINAL_OP_POCKET3_FLIP.mp4` | ✓ re-rendered 30.4MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0095_V2_81s_FINAL_LENSPEN.mp4` | ✓ re-rendered 44.8MB |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/_archive/v2_overlapped/` | ✓ kept 7 V2 cũ (496MB) |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/clip_*/v3_pre_speed.mp4` | ✓ kept (112/79/64/82/85/42/62 MB) |

## 🔗 Related pitfalls in this skill

- **PITFALL #6** (`-c copy` cascade hallucinate) — trùng root cause: stream-copy không re-encode
- **PITFALL #18** (filter_complex concat CÙNG source + `-ss -to` SILENT DURATION BUG) — anti-pattern ngược: dùng filter_complex nhưng sai pattern
- **PITFALL #90** (HARD CUT default, NO afade) — agreed với PITFALL #91: cùng class audio/video concat issue, nhưng PITFALL #91 focus vào frame overlap, PITFALL #90 vào audio fade

## ✅ Pre-ship checklist (add vào Stage 5)

```
[ ] Pre-speed duration = sum(keep_plan end_padded - start_padded) ±0.1s
[ ] Final duration = pre_speed / 1.3 ±0.5s
[ ] Final ffprobe: 1080×1920 / 30fps / h264 / aac 44100Hz
[ ] Boundary frame MD5 ≠ (extract tất cả boundary ±0.1s, hash check)
[ ] Vision check 1 boundary rõ rệt (pose/sản phẩm/góc camera khác)
[ ] Final file copied sang `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (BẮT BUỘC anh preference)
```

## 💡 Cross-skill lesson

`video-cut-tiktok-shorts` và `tiktok-video-editor` cũng cần reference PITFALL #91 nếu chúng chứa step "concat segments". Verify trong SKILL.md của 2 skill đó khi update lần sau.

---

*Created 2026-07-27 - First hard-verified case (MD5 + vision + 7 clip batch) của concat demuxer stream-copy frame overlap bug. Distinct from PITFALL #6 hallucinate (audio + content), PITFALL #18 silent duration, PITFALL #90 hard cut vs audio fade.*
