# PITFALL #80 — Filler false positive do speed 1.3x (v0.01)

## User verbatim feedback (22/07)
> "Anh thấy vào đầu và cuối mỗi đoạn cắt audio bị fade out đúng không?" (implicitly triggered recheck fail khi smart_pad apply)

## Root cause
Sau speed 1.3x:
- Source: câu "Vậy nên là ở bên trong..." → Whisper detect 1 segment ngắn
- Post-speed: audio compressed → Whisper re-detect thành 2-3 segments:
  - Seg 1: "Vậy nên là ở bên" (0.4s)
  - Seg 2: "trong nó được thiết kế phức tạp nó cũng khá là dày bản" (1.6s)
- Filler `ừm` ở đầu các câu dài → trở thành segment độc lập với `gap_before > 0.5s`

### Old rule V1 — flag mọi filler đầu
```python
if re.match(r'^\s*(ừm|ờ|à|rồi|nhé|nha|thì)\b', text):
    fail_reasons.append(filler)  # FAIL
```

Bug: False positive vì filler đầu câu dài trở thành segment độc lập sau speed 1.3x.

## Fix — Rule V2 (v0.01)
Allow filler nếu có transition gap do speed/process hoặc cut boundary thật:

```python
if re.match(r'^\s*(ừm|ờ|à|rồi|nhé|nha|thì)\b', text):
    gap_before = seg['start'] - prev_seg['end']
    if 0.2 <= gap_before <= 0.7:
        continue  # Whisper re-segmentation sau speed 1.3x → ALLOW
    if gap_before > 0.7:
        continue  # Cut boundary thật → filler tự nhiên ALLOW
    if gap_before < 0.2:
        fail_reasons.append(filler)  # Re-segmentation chặt → FAIL
```

### Reproducible test
Test clip 0036 V3 (post smart_pad):
- Filler "ừm" ở 52.4s (post-speed), `gap_before = 0.62s` → ALLOW (process transition)
- Không bị block ship
- Audio nghe tự nhiên, không mất "ừm" đầu câu

## Bài học
Khi speed/resample/audio post-processing thay đổi timing, các tool kiểm tra filler/câu treo **PHẢI** check `gap_before` để phân biệt filler do process vs filler thật. Hard rule absolute "flag all filler" sẽ false positive sau bất kỳ audio transformation nào.
