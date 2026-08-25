# YouTube Long-Form Narration — Config Grid (29/07)

**Source:** black-hole pilot session, voice clone `tuan_anh_5s_1sent_amp.pt` (5s ref, ref_rms=0.1100).
**Goal:** find voice config dễ chịu nhất cho narration 10–25 phút tiếng Việt, single voice clone, native speed.

## A/B matrix (đã test 29/07, voice `tuan_anh_5s_1sent_amp.pt`, 3 câu short test)

| L (layer_penalty) | P (position_temp) | pad | fade | speed | Nhận xét ngắn | Verdict |
|---|---|---|---|---|---|---|
| 5.0 (default) | 5.0 (default) | 0.1 | 0.1 | 0.95 | Whisper miss vài từ đầu, filler phụ thuộc tag | ❌ |
| 2.0 | 3.5 | 0.1 | 0.1 | 0.90 | Hơi nặng ở câu 1, mid rõ | ⚠️ |
| 1.5 | 3.5 | 0.1 | 0.0 | 0.90 | Tốt ổn, câu 1 ổn định | ✅ |
| 1.5 | 3.7 | 0.2 | 0.0 | 0.90 | Tốt nhất "đầu-cuối" cảm giác rõ, mid ổn | ✅+ |
| 1.5 | 3.5 | 0.2 | 0.1 | 0.90 | Tốt ổn, mid ổn | ✅ |
| 1.0 | 3.0 | 0.0 | 0.0 | 0.95 | Smooth nhưng hơi nhanh | ⚠️ |
| 4.0 | 3.5 | 0.05 | 0.1 | 0.90 | Ổn, mid ổn | ✅ |
| 4.0 | 2.5 | 0.05 | 0.1 | 0.90 | Ổn định hơn nữa, filler ít | ✅ |
| 3.0 | 2.0 | 0.05 | 0.0 | 0.90 | Rất phẳng, có thể hơi tẻ | ⚠️ |
| 3.0 | 2.5 | 0.1 | 0.05 | 0.90 | Cân bằng mid | ✅ |

## Quyết định cuối (verified 12:24 take 1 call full script)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.1,             # small padding at boundaries
    fade_duration=0.0,            # NO FADE
    denoise=True,                 # blocks ref-text echo
    layer_penalty_factor=1.5,     # smooth without over-merging
    position_temperature=3.5,     # natural prosody for narration
)
# Plus: model.generate(..., speed=0.90)
```

Kết quả: Whisper coverage 98.7%, 0 filler, peak -1.4dB, 85 sentences preserved.

## Tuning rules (nếu cần điều chỉnh)

| Mục tiêu | Tăng/giảm | Ghi chú |
|---|---|---|
| Voice "ấm" hơn | Tăng `layer_penalty_factor` +0.5 | 1.5 → 2.0 |
| Voice "phẳng" quá | Tăng `position_temperature` +0.5 | 3.0 → 3.5 |
| Nói nhanh hơn | Tăng `speed` +0.05 | 0.85 → 0.90 |
| Tránh filler đầu câu | Tăng `pad_duration` +0.05 | 0.10 → 0.15 |
| Câu nối mượt hơn | Tăng `fade_duration` +0.05 | 0.00 → 0.05 |

## Anti-patterns (NEVER)

- `layer_penalty_factor=5.0` (default) — Whisper miss từ + ngắt quãng.
- `position_temperature=5.0` (default) — filler "ờ/ựm" đầu câu.
- `pad_duration=0.2, fade_duration=0.1` (mặc định cũ) — gap lớn giữa chunk 60–200ms.
- Áp `atempo=1.2` cho YouTube — phá tốc độ tự nhiên.
- Tự chèn emotion tag `[question-ah]/[confirmation-en]` — gây filler đầu câu.

## Bước QA bắt buộc sau mỗi config A/B

```bash
# 1. Generate test 3 câu ngắn (3 short paragraphs đầu file script)
python3 scripts/generate_voice.py --prompt <pt> --text "..." --output smoke.wav

# 2. Concat + encode
ffmpeg -y -ar 44100 -ac 1 -c:a libmp3lame -b:a 192k smoke.mp3

# 3. Whisper transcript (xem coverage, có filler không)
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir qa/ smoke.mp3

# 4. Search filler bằng regex
grep -E '\b(ờ|ựm|ừm|ồ|à)\b' qa/smoke.txt
# Expect: 0 match (zero filler)
```

## Workflow tổng cho 1 video YouTube 15–25 phút

1. Đọc script, strip heading/timestamps, tách thành paragraphs.
2. Smoke test 3 paragraphs đầu với config trên, nghe + check filler.
3. OK → gộp TOÀN BỘ paragraphs thành 1 string duy nhất.
4. Generate 1 call duy nhất với `--text <full_text> --output full.wav`.
5. Encode MP3 192k 44.1kHz.
6. Whisper transcript, check 0 filler, check coverage ≥ 95%.
7. OK → ship.

## Nếu model OOM (RAM > peak)

- Fall back sang merge chunks 25–40s theo Pitfall #22.
- KHÔNG thử merge chunks 5–10s (Plan C) — sẽ drop âm đầu/cuối.
- Khi dùng fallback, vẫn giữ config L1.5/P3.5/pad 0.1/fade 0/speed 0.90.
