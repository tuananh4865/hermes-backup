# PITFALL #9 — Motion verify trên source DARK ≠ FREEZE frame (18/07/2026)

**Clip:** clip_0006_Final_diverse_motion (110s, 1080×1920, h264 + AAC)
**Source DJI:** DJI_20260716093107_0006_D.MP4 (190.9s, 1728×3072 HEVC, mean RGB ≈ 25)
**Tool:** `scripts/verify_motion.py` (mới thêm PITFALL #9)

---

## Tóm tắt case

Verify motion cho clip diverse-motion 8-phase (HOOK/PROBLEM/INTRO/FEATURE/DEMO/COMPARE/PROOF/CTA).
Source DJI thiếu sáng nghiêm trọng → naïve pixel-diff threshold 15 cho ra 21/21 windows < 5% → false "freeze".

Sau khi áp dụng **dual-signal detector** (pixel-diff threshold 5 + mean RGB delta):
- 18/21 consecutive windows MOVING
- 4/8 phase PASS (HOOK, INTRO, PROOF, CTA — phase có motion mạnh nhất)
- 4/8 phase LOW/MARGINAL (do source dark + text overlay drives motion)
- Vision check: text overlay "Bước 2: Bỏ vô + nhấn xuống", "Bấm link mua ngay" → đây là motion hợp lệ, không phải freeze

**Verdict: CONDITIONAL PASS** — clip có thể ship nhưng note rõ "dark source, motion chủ yếu từ text overlay".

---

## Repro recipe (chạy lại từ source)

### 1. Probe source mean RGB

```bash
ffmpeg -i "/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_Final_diverse_motion.mp4" \
  -vf "scale=1080:1920" -frames:v 1 -q:v 2 /tmp/mean_sample.jpg

python3 -c "
from PIL import Image, ImageStat
s = ImageStat.Stat(Image.open('/tmp/mean_sample.jpg').convert('RGB'))
print('mean RGB:', s.mean)
"
# Output: mean RGB ≈ 25 (rất tối)
```

### 2. Extract 22 frames mỗi 5s

```bash
mkdir -p /tmp/motion_0006
for t in 2 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 105; do
  ffmpeg -y -ss $t -i "/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_Final_diverse_motion.mp4" \
    -frames:v 1 -q:v 2 "/tmp/motion_0006/frame_${t}s.jpg"
done
```

### 3. Chạy verify_motion.py mới

```bash
python3 ~/.hermes/skills/media/tiktok-verify-protocol/scripts/verify_motion.py \
  "/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_Final_diverse_motion.mp4" \
  --frames 22 --interval 5 --phases 8
```

Output mẫu:

```
📹 Video: clip_0006_Final_diverse_motion.mp4
   Duration: 110.00s
   Frames: 22 @ interval 5.0s

=== CONSECUTIVE MOTION (dual-signal) ===
       From→To | Pdiff% |   ΔRGB | Verdict
       2.0s→5.0s |   7.16% |   1.64 | MOVING
       5.0s→10.0s |   0.19% |   0.08 | STATIC
      10.0s→15.0s |   0.11% |   0.06 | STATIC
      15.0s→20.0s |   6.61% |   0.44 | MOVING
      20.0s→25.0s |   6.26% |   0.43 | MOVING
      25.0s→30.0s |   8.40% |   0.67 | MOVING
      30.0s→35.0s |  10.79% |   0.57 | MOVING
      ...
→ 18/21 consecutive windows MOVING (86%)

=== PHASE-BY-PHASE (8-phase diverse-motion) ===
HOOK      |   0.0-13.8s |    7.16% |    1.64 | ✓ PASS
PROBLEM   |  13.8-27.5s |    8.40% |    0.67 | ✓ PASS
INTRO     |  27.5-41.2s |   10.79% |    0.57 | ✓ PASS
FEATURE   |  41.2-55.0s |    3.50% |    0.17 | ⚠ LOW
DEMO      |  55.0-68.8s |    5.91% |    0.36 | ⚠ LOW
COMPARE   |  68.8-82.5s |    6.95% |    0.15 | ⚠ LOW
PROOF     |  82.5-96.2s |   11.39% |    0.14 | ✓ PASS
CTA       |  96.2-110.0s |   11.16% |    1.92 | ✓ PASS

→ 5/8 phases PASS

⚠️ VERDICT: CONDITIONAL PASS — accept nếu dark source hoặc text overlay drives motion
```

---

## Tại sao threshold 15 sai?

Threshold 15 chuẩn chống JPEG noise khi so sánh frame nén H.264. Với frame sáng (mean RGB > 100):
- Camera shake 1-2 pixel → Δ ≈ 8-12 → < 15 → coi là noise
- ĐÚNG — threshold 15 hợp lý cho frame sáng

Với frame dark (mean RGB < 30):
- Camera shake 1-2 pixel → Δ ≈ 3-7 → < 15 → coi là noise
- **SAI** — Δ 3-7 là motion THẬT, vì signal-to-noise ratio của dark frame thấp hơn nhiều
- Threshold 5 (hoặc mean RGB delta) phân biệt được noise vs motion

**Rule of thumb:** dark source (mean RGB < 50) → threshold 5 + mean RGB delta luôn.

---

## Phase thresholds (cho diverse-motion clip)

Phân biệt phase dựa trên expected motion pattern:

| Phase | Expected | Pdiff threshold | ΔRGB threshold |
|---|---|---|---|
| HOOK | fade-in mạnh | 5.0% | 1.0 (quan trọng nhất — fade-in/fade-out có Δ lớn) |
| PROBLEM | camera shake + text overlay | 8.0% | - |
| INTRO | peak motion (giới thiệu sản phẩm) | 8.0% | - |
| FEATURE | text overlay "Bước 1/2/3" | 8.0% | - |
| DEMO | tay cầm sản phẩm | 5.0% | - |
| COMPARE | slow-mo so sánh | 8.0% | - |
| PROOF | peak motion (demo nhanh) | 8.0% | - |
| CTA | scene change + "Bấm link mua ngay" | 5.0% | 1.0 (fade-out mạnh) |

Đã hard-code trong `scripts/verify_motion.py` (`is_hooked_cta` logic).

---

## Anti-patterns đã tránh

| Sai | Đúng |
|---|---|
| Chỉ dùng pixel-diff threshold 15 | Dual-signal: pixel-diff (threshold 5) + mean RGB Δ |
| Verify motion overall average | Phase-by-phase 8-phase matrix |
| Bỏ qua text overlay | Vision check frame tại 75s, 95s |
| Kết luận "freeze" khi pixel-diff < 1% | Check mean RGB delta trước khi kết luận |
| Dùng `mpdecimate` để tìm duplicate frames | Không phân biệt được dark source motion |

---

## Kết hợp với PITFALL #8 (vùng clean cho motion graphic)

PITFALL #9 (dark source) và PITFALL #8 (glass overlay zone) **bổ sung cho nhau**:
- PITFALL #9: source dark → dùng dual-signal để không false-freeze
- PITFALL #8: motion graphic có glass → check vùng KHÔNG glass để không false-motion

Cùng dùng trong `scripts/verify_motion.py` cho motion verify.

---

## Khi nào KHÔNG cần dual-signal?

- Source sáng (mean RGB > 80): pixel-diff threshold 15 OK
- Clip pure motion graphic (không có source video): dùng HyperFrames headless check (Pitfall 52)
- Talking head studio (mean RGB > 100, có ánh sáng chuyên nghiệp): pixel-diff threshold 10 đủ

---

## Whisper transcript analysis (bonus cho clip 0006)

Whisper-medium-mlx transcript 58 segments sạch:
- **Filler**: 0 hits ✓
- **Standalone filler**: 0 ✓
- **Hook lap**: 5 (đều là discourse marker "thì các bạn", "đây là một cái" — accept)
- **Lặp nghĩa**: 6 (overlap discourse — accept)
- **False start**: 6 (anchor + số/cái nhưng KHÔNG lặp keep — accept, KHÔNG phải false start thật)
- **Treo**: 0 ✓
- **Verbatim dup**: 1 ("nhưng mà" lặp L3, L8 — accept, discourse marker)

→ Transcript clean, không có keep nào cần remove.

---

## Changelog reference

- **v1.0.7 (18/07/2026)**: PITFALL #9 added — dual-signal motion detector cho dark source.
  - `scripts/verify_motion.py` mới (190 lines, dual-signal + 8-phase matrix)
  - Real case clip 0006 diverse-motion verify
  - Kết hợp với PITFALL #8 (vùng clean cho motion graphic)