# Smart Pad — Word-Aligned KEEP ranges

> Nguồn: phát minh 22/07 khi anh flag "audio đầu/cuối mỗi đoạn cắt bị fade out"

## Vấn đề

Khi AI agent quyết định KEEP range = `[start, end]` dựa trên Whisper **segment** timestamp, range sẽ rộng hơn **word** timestamps thực tế.

Ví dụ (clip 0036):
- Segment `[46.3s - 51.0s]` chứa phrase về build quality
- Word đầu thực tế: `"mà"` ở `47.06s`
- → Head gap = 47.06 - 46.30 = **0.76s** audio dead silence đầu câu
- Khi render × speed 1.3x → 0.76/1.3 = ~0.58s vẫn empty → listener nghe câu cụt

4/9 KEEP ranges trong clip 0036 có head gap 0.28-0.76s → audio fade cụt nặng.

## Fix algorithm

```python
# smart_keep_plan.py
def find_word_range(words, seg_start, seg_end):
    first_word_start = None
    last_word_end = None
    for w in words:
        ws, we = w['start'], w['end']
        # Word starts in range OR word overlapping with range
        if seg_start <= ws < seg_end:
            if first_word_start is None:
                first_word_start = ws
            last_word_end = we
    return first_word_start, last_word_end

# Pad 50ms each side for audio fade in/out + cleanup
new_start = max(0, first_word_start - 0.05)
new_end = last_word_end + 0.05
```

## Output keep_plan.json format (v0.01)

```json
{
  "ranges": [
    {
      "start": 46.30,
      "end": 51.00,
      "action": "KEEP",
      "start_padded": 47.01,
      "end_padded": 51.09,
      "orig_start": 46.30,
      "orig_end": 51.00,
      "padded_note": "word-aligned (saved 0.72s of head+tail silence)"
    }
  ],
  "padded_summary": {
    "ranges_padded": 9,
    "total_ranges": 9,
    "avg_gap_before_padding": 0.222,
    "avg_gap_after_padding": 0.1
  }
}
```

## build_concat_list.py integration

```python
# build_concat_list.py — tự động dùng padded boundaries
for r in plan.get('ranges', []):
    if r.get('action') == 'KEEP':
        start = r.get('start_padded', r.get('start'))  # prefer padded
        end = r.get('end_padded', r.get('end'))
        keep.append((float(start), float(end)))
```

## Kết quả clip 0036

| Range | Before | After (padded) | Saved |
|---|---|---|---|
| Build | 46.30-51.00 | 47.01-51.09 | **0.72s** |
| Hít | 53.90-57.50 | 54.25-57.51 | **0.44s** |
| Ống kính | 67.40-69.80 | 67.63-69.85 | **0.28s** |
| Key insight | 93.20-98.20 | 93.57-98.29 | **0.38s** |

**Total saved: 1.5s** dead silence across 9 ranges.

## Khi nào KHÔNG dùng smart_pad?

- Source không có word_timestamps (Whisper old version, ASR khác) → fallback dùng segment timestamps
- KEEP range quá ngắn (<0.5s) → smart_pad không hiệu quả
- Khi muốn giữ timing cut chính xác (ví dụ sync với visual cue)

## Usage

```bash
# Sau khi write keep_plan.json:
bash scripts/smart_pad.sh <clip_id>
# → Update keep_plan.json với start_padded/end_padded
# → Backup keep_plan.v1.json tự động
```

## References

- Source script: `/Users/tuananh4865/.hermes/skills/media/tiktok-video-editor/scripts/smart_pad.sh`
- Logic: `/Users/tuananh4865/.hermes/skills/media/tiktok-video-editor/scripts/smart_keep_plan.py`
- Test pilot: clip 0036 lens macro review NAMMINH (skipped: 23 → 9 KEEP ranges)
