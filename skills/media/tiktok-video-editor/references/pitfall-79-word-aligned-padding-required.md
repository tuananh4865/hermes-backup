# PITFALL #79 — Audio fade đầu/cuối mỗi đoạn cắt (v0.01)

## User verbatim feedback (22/07)
> "Anh thấy vào đầu và cuối mỗi đoạn cắt audio bị fade out đúng không?"

## Root cause
Whisper segment timestamp rộng hơn word range thật:
- Source transcript segment ở [46.30-51.00] → từ thật "mà" ở 47.06s
- Head gap 0.76s → audio đầu câu "mà..." bị mất khi concat
- 4/9 KEEP ranges bị head gap 0.28-0.76s trong test clip 0036

### Reproducible diagnostic
```python
import json
from pathlib import Path

with open('work/audio.json') as f:
    d = json.load(f)

all_words = []
for s in d['segments']:
    for w in s.get('words', []):
        all_words.append(w)
all_words.sort(key=lambda x: x['start'])

# Check 4 critical ranges in test clip 0036
keep_ranges = [
    (46.30, 51.00, "Build quality + CNC"),
    (53.90, 57.50, "Hít pocket bar"),
    (67.40, 69.80, "Ống kính siêu cận"),
    (93.20, 98.20, "Key insight 3cm"),
]

for seg_start, seg_end, desc in keep_ranges:
    words_in_range = [w for w in all_words if seg_start <= w['start'] < seg_end]
    if words_in_range:
        head_gap = words_in_range[0]['start'] - seg_start
        if head_gap > 0.2:
            print(f"❌ [{seg_start}-{seg_end}] {desc}: head gap {head_gap:.2f}s")
```

Output:
```
❌ [46.30-51.00] Build quality + CNC: head gap 0.76s
❌ [53.90-57.50] Hít pocket bar: head gap 0.40s
❌ [67.40-69.80] Ống kính siêu cận: head gap 0.28s
❌ [93.20-98.20] Key insight 3cm: head gap 0.42s
```

## Fix (v0.01)
- `scripts/smart_pad.sh` chạy sau step 6 (viết keep_plan.json) và trước step 7a (build pre-speed)
- `scripts/smart_keep_plan.py` walk word_timestamps, tìm `first_word_start` và `last_word_end` trong mỗi KEEP range
- Pad ±0.05s: `new_start = first_word_start - 0.05`, `new_end = last_word_end + 0.05`
- Lưu vào `keep_plan.json` với field `start_padded` / `end_padded` + `padded_note`
- `scripts/build_concat_list.py` tự động prefer `start_padded` nếu có (không cần edit thủ công)

### Test result clip 0036
```
Plan: 9 KEEP ranges, expected=75.0s, actual=...
Padded: 9/9 ranges (avg gap 0.222s → 0.1s)
```

Saved 1.5s tổng cộng dead silence → audio output nghe liền mạch, không mất từ đầu/cuối.

## Bài học
Khi Whisper transcript có word-level timestamps, **LUÔN dùng word range** thay vì segment range. Segment timestamp của Whisper là approximation, có padding dư. Nếu bỏ qua bước pad, audio edit sẽ mất 0.2-0.8s đầu/cuối mỗi đoạn cắt.
