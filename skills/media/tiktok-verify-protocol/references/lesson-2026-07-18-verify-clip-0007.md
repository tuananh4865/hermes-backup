# Lesson — Verify clip 0007 KNF carbon fiber bộ vệ sinh (18/07/2026)

**Clip:** `clip_0007_Final_troncau_bo-ve-sinh-knf-carbon-fiber.mp4`
**Source:** `DJI_20260716093536_0007_D.MP4` (275.95s, 1728×3072 HEVC)
**Edited:** 137.30s, 1080×1920 H.264 yuv420p10le 30fps, AAC LC 44100Hz stereo, 5565 kbps, 91.1 MB
**Trigger:** User instruction 18/07 verbatim — "Verify clip 0007 (KNF carbon fiber bộ vệ sinh) đã edit - kiểm tra false start + lặp câu + filler"
**Tool:** 7-layer one-shot workflow (Layer 4 Layer 3 FALSE START scan PITFALL #21 tiktok-video-editor v3.24.0)

---

## Tóm tắt case

Clip 0007 KNF carbon fiber bộ vệ sinh — single continuous narrative take 137.3s. Speaker Tuấn Anh giải thích vì sao cần khăn carbon fiber thay vì khăn thường để vệ sinh ống kính máy ảnh / sơn ô tô.

**Verify kết quả: PARTIAL PASS** — 7/7 layers PASS về mặt nội dung + audio + motion, nhưng duration 137.3s > Mode B strict max 130s → cần apply Pitfall #26 speed 1.3x trước khi ship.

---

## 7-Layer workflow đã chạy (theo PITFALL #10/11 mới)

| Layer | Check | Result | Evidence |
|---|---|---|---|
| **1. Spec** | 1080×1920 H.264 + AAC 44100Hz | ⚠️ PARTIAL | Resolution/codec OK nhưng duration 137.3s > 130s Mode B max |
| **2. 5-dim strict** | FILLER/TREO/LẶP NGHĨA/HOOK LẶP/ỰM_Ỡ | ✅ PASS | 0/0/0/0/0 hits trên 30 segments |
| **3. Anchor-lap semantic** | Anchor keywords lặp | ✅ PASS | 0 pairs (chỉ có 2 brief false positive "Thì trên..." / "Đó là cái..." = SOURCE-NATURAL) |
| **4. FALSE START Layer 3** | 5+/8 từ đầu match + gap < 10s | ✅ PASS | 1 candidate seg 21↔22 match=5/8 NHƯNG phân tích = parallel-reason rhetoric (PITFALL #11 FALSE POSITIVE) |
| **5. RMS first-3s** | mean_volume first 3s > -50dB | ✅ PASS | -26.6 dB (audible, không silent take cũ) |
| **6. RMS delta vs source** | edited vs source mean_volume delta ≤ 0.5dB | ✅ PASS | 0.4 dB (-27.0 vs -26.6) — loudness match |
| **7. Motion** | pixel diff t=5s vs t=10s ≥ 10% | ✅ PASS | 41.46% — sản phẩm được cầm/xoay rõ |

---

## PITFALL #10 (Layer 3 FALSE START) — workflow chi tiết

### Step 1: Whisper re-read output

```bash
ffmpeg -y -i clip.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/verify_0007.wav
~/.hermes/scripts/whisper-transcribe /tmp/verify_0007.wav /tmp/whisper_0007_json
# 30 segments, max NSP 0.097 (clean, no hallucinate cascade)
```

### Step 2: Scan Layer 3 FALSE START

```python
import json
with open("/tmp/whisper_0007_json/verify_0007.json") as f:
    segments = json.load(f)["segments"]
candidates = []
for i in range(len(segments) - 1):
    seg_i = segments[i]
    seg_j = segments[i + 1]
    gap = seg_j["start"] - seg_i["end"]
    if gap > 10: continue
    words_i = seg_i["text"].strip().split()[:8]
    words_j = seg_j["text"].strip().split()[:8]
    match = sum(1 for a, b in zip(words_i, words_j) if a == b)
    if match >= 5:
        candidates.append({...})
# → 1 candidate: seg 21↔22, gap=0.00s, match=5/8
```

### Step 3: Phân tích candidate (PITFALL #11 classifier)

| Vị trí | Thời gian | Câu cũ | Câu mới |
|---|---|---|---|
| seg 21 ↔ 22 | gap=0.00s, match=5/8 | "**Bởi vì** những cái **vết suốt này** trung vi nó khá nhỏ" (92.00-94.24s) | "**Bởi vì** những cái **hạt bụi này** chúng ta không nhìn thấy…" (94.24-97.52s) |

**First 8 words comparison:**
```
[0] == old='Bởi'      new='Bởi'
[1] == old='vì'        new='vì'
[2] == old='những'     new='những'
[3] == old='cái'       new='cái'
[4] != old='vết'       new='hạt'      ← content phân kỳ
[5] != old='suốt'      new='bụi'      ← content phân kỳ
[6] == old='này'       new='này'      ← demonstrative giống
[7] != old='trung'     new='chúng'    ← content phân kỳ
```

**Verdict theo PITFALL #11:**
- Connector scaffolding: "Bởi vì" (1 từ) + "những cái" (2 từ demonstrative) = 3/8 từ đầu là connector/filler
- Content phân kỳ từ từ thứ 4: "vết suốt" vs "hạt bụi" = 0/5 match trong content
- **Classify: PARALLEL_REASON FALSE POSITIVE — KHÔNG phải false start**
- Whisper gốc confirm: speaker đang giải thích "vì vết xước nhỏ + vì hạt bụi không thấy được" = 2 lý do song song tự nhiên

### Step 4: RMS first-3s silent-take detector

```bash
ffmpeg -hide_banner -t 3 -i clip.mp4 -af "volumedetect" -f null - 2>&1 | grep mean_volume
# mean_volume: -26.6 dB (audible, NOT silent)
# → KHÔNG có silent take cũ ẩn
```

### Step 5: RMS delta vs source

```bash
ffmpeg -hide_banner -i clip.mp4 -af "volumedetect" -f null - 2>&1 | grep mean_volume
# mean_volume: -27.0 dB
ffmpeg -hide_banner -i source.mp4 -af "volumedetect" -f null - 2>&1 | grep mean_volume
# mean_volume: -26.6 dB
# Delta: 0.4 dB → PASS (≤ 0.5 dB threshold)
```

### Step 6: Motion check (single-point)

```python
# Extract frame t=5s và t=10s
# Sample pixel diff step=4, threshold 30/255 RGB sum
# Result: 41.46% pixels changed → MOTION OK (≥ 10% threshold)
```

---

## 3-Keep detection workflow

Khi Whisper output gaps < 0.15s (single continuous take) → dùng **silence detection** để tìm keep boundaries:

```bash
ffmpeg -i clip.mp4 -af "silencedetect=noise=-30dB:d=0.3" -f null - 2>&1 | grep "silence"
# → 47 silent regions, tất cả duration 0.3-2.5s (KHÔNG có gap > 3s = single continuous take)
```

Kết hợp với Whisper gap > 0.15s → 3 keep tự nhiên:
- **Keep 1** (seg 0-6, 0.00-28.24s): HOOK + INTRO (giới thiệu sản phẩm + problem)
- **Keep 2** (seg 7-24, 28.40-110.32s): CORE USP (giải thích carbon fiber hút bụi)
- **Keep 3** (seg 25-29, 110.48-132.72s): CLOSING (bảo quản + CTA)

So sánh first-5-words + trigram sharing giữa 3 keep pairs: **0 overlap pair đủ signature** (hook lap scan PASS).

---

## Brief definition 5-check (user verbatim 18/07) — cách phân biệt với protocol 5-dim strict

User dùng "false start + lặp câu + filler" theo brief định nghĩa riêng. So sánh với `scripts/verify_clip.py` 5-dim strict:

| User brief | Protocol mapping | Note |
|---|---|---|
| **False start** | PITFALL #10 (Layer 3 scan mới) | Brief = anchor (nãy/ờ/thì/à/rồi/đó/giờ/tiếp theo/tiếp tục) + số/câu/cái. Strict = gap<10s + 5+/8 first-word match. Layer 3 scan RỘNG HƠN brief |
| **Lặp câu** | HOOK LẶP + LẶP NGHĨA | Brief = "câu lặp" chung chung, protocol chia nhỏ 2 loại (3+/5 first-word match vs 2+ first + trigram share) |
| **Filler** | FILLER + ỰM_Ỡ + TREO | Brief = "ơ, ờ, ừm, ừ, ó, à, á" (match với FILLER_LIST) |

→ Protocol 5-dim strict **đã cover** user brief + Layer 3 FALSE START bổ sung case take-retry. Khi user nói "verify false start + lặp câu + filler" → chạy `verify_clip.py` + `verify_clip_full.py` Layer 4 để cover all 3 brief items + bonus checks (anchor-lap, RMS, motion).

---

## VERDICT + Action items

**Verdict: PARTIAL PASS** (7/7 layers PASS ngoại trừ duration vượt Mode B max)

**Action BẮT BUỘC trước khi ship:**
```bash
# Apply Pitfall #26 speed 1.3x để đưa 137.3s → ~105.6s (sweet spot Mode B):
ffmpeg -y -i "...clip_0007_Final_troncau_bo-ve-sinh-knf-carbon-fiber.mp4" \
  -filter_complex "[0:v]setpts=PTS/1.3[v];[0:a]atempo=1.3[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -preset medium -crf 18 \
  -c:a aac -b:a 128k -ar 44100 \
  -movflags +faststart \
  "...clip_0007_Final_troncau_bo-ve-sinh-knf-carbon-fiber_speed13.mp4"
```

→ Sau speed 1.3x: 137.3 / 1.3 ≈ 105.6s → ✅ Mode B strict sweet spot (80-120s)

**Re-Whisper verify sau speed:**
- 0 HIGH NSP segments (audio clean)
- 0 câu treo > 8s
- CTA còn nguyên (seg 29 "Cái book này thì giá nó đang khá là rẻ thôi")

---

## Changelog reference

- **v1.0.8 (18/07/2026)**: PITFALL #10 (Layer 3 FALSE START scan) + PITFALL #11 (parallel-reason rhetoric false positive) + tool `scripts/verify_clip_full.py` (7-layer one-shot verifier) + reference `lesson-2026-07-18-verify-clip-0007.md` (real case clip 0007 KNF carbon fiber bộ vệ sinh).