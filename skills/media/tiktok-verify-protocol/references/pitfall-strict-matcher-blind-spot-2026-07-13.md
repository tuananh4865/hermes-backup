# Pitfall #1 — strict 2-word-prefix matcher blind spot

**Captured:** 13/07/2026
**Clip:** 0740 "Body mist AMAP - tinh tế" (V1 114.8s, source WAV 262.7s)
**Skill version when pitfall emerged:** tiktok-verify-protocol v1.0.0 + verify_clip.py v3.21.4

## Tóm tắt

`verify_clip.py` v3.21.4 báo PASS cho V1 của clip 0740, nhưng parent user phát hiện 2 lap_nghia thực tế trong verify transcript:

1. **"nhãn hàng" lặp** — verify transcript seg[0] "nhãn hàng này làm ơn..." + seg[1] "nhãn hàng mà có xem được..." (anchor lặp back-to-back)
2. **"nhưng mà" lặp** — verify transcript seg[18] "nhưng mà có người..." + seg[23] "nhưng mà nếu mà trời mát..." (anchor lặp cách 5 seg)

## Tại sao strict script bỏ sót

### chosen_segs filter của verify_clip.py
```python
if seg['start'] >= s_start - 0.3 and seg['end'] <= s_end + 0.5:
    chosen_segs.append(seg)
```

Với V1 keeps clip 0740:
- keep[0] = `[5.40, 16.40]` chứa src[1] `[5.38, 16.42]` → src[1] được include (start 5.38 vừa < keep_start 5.40)
- keep[1] = `[23.10, 29.70]` chứa src[3] `[20.04, 23.14]` + src[4] `[23.14, 29.70]`
  - src[3] start=20.04 < 22.80 (keep_start - 0.3) → **bị loại**
  - src[3] chứa "nhãn hàng" → nếu include thì src[1] vs src[3] match first 2 words → flag được
  - Vì bị loại → chosen_segs chỉ còn src[1] (keep[0]) + src[4] (keep[1]) → strict matcher so `[nhãn, hàng]` vs `[Những, hàng]` (lowercase-strip) → match=1 (chỉ "hàng") → không flag

### "nhưng mà" lặp
- keep[2] src[8] "Nhưng mà cái mùi..." → keep[7] src[24] "nhưng mà không có phản ứng..." (cách nhau 5 keep trung gian)
- keep[12] src[46] "nhưng mà có người..." → keep[13] src[52] "Nhưng mà nếu mà trời..." (back-to-back)

Trong chosen_segs: các segs "nhưng mà" KHÔNG còn adjacent vì bị keeps trung gian chèn → strict matcher không so được.

## Whisper verify transcript thực tế (30 segs)

```
vseg[ 0] [  0.00->  8.72]  nhãn hàng này làm ơn có thể gửi cho mình...           [NHAN-HANG]
vseg[ 1] [  8.72-> 13.44]  nhãn hàng mà có xem được video này...                 [NHAN-HANG]
vseg[ 3] [ 16.26-> 24.22]  nhưng mà cái mùi của nó mỗi lần...                    [NHUNG-MA]
vseg[10] [ 50.98-> 53.02]  Nhưng mà không có phản ứng khó chịu                    [NHUNG-MA]
vseg[18] [ 87.48-> 89.66]  nhưng mà có người thì mùi hương...                     [NHUNG-MA]
vseg[23] [100.48->103.00]  nhưng mà nếu mà trời mát lạnh...                      [NHUNG-MA]
```

## Repro recipe

```bash
# 1. Verify V1 với strict script
python3 scripts/verify_clip.py \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/0740/audio.json \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/0740/keeps.json \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0740_V1_troncau_body-mist-amap-tinh-te.mp4

# Output: ✅ ĐẠT GOAL - file có thể public!   (FALSE NEGATIVE!)
# exit 0 — script pass, nhưng thực tế clip có 2 lap_nghia nghe rõ

# 2. Whisper lại file output (đã có sẵn)
# /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0740_V1_troncau_body-mist-amap-tinh-te_verify.json

# 3. Spot tay thấy nhãn hàng lặp vseg[0]+vseg[1], nhưng mà lặp vseg[3]+vseg[10]+vseg[18]+vseg[23]
```

## Action items

- Thêm snippet anchor-keyword check vào SKILL.md (Section "🚨 PITFALL #1")
- Sau clip 0740 V2, parent cần update verify_clip.py lên v3.22 với:
  - **Semantic lap detector**: list anchor keywords + check adjacent trong verify transcript (không phải chosen_segs)
  - **Wider chosen_segs tolerance**: ±1.0s thay vì ±0.3/0.5s
  - Đã đề xuất trong lesson này nhưng chưa implement (chờ parent confirm scope)
- Mọi clip WHISPER output PHẢI được spot-check thủ công sau khi strict script PASS

## Snippet anchor-keyword semantic check (ready-to-run)

```python
#!/usr/bin/env python3
"""check_anchor_lap.py - Bổ sung semantic layer cho verify_clip.py"""
import json, sys

ANCHORS = [
    'nhãn hàng', 'nhưng mà', 'tuy nhiên', 'cho nên', 'vì vậy',
    'do đó', 'bởi vì', 'nói chung', 'tóm lại', 'cuối cùng',
    'kết luận', 'nhà mình', 'bên mình', 'các bạn', 'mọi người',
]

verify = json.load(open(sys.argv[1]))
segs = verify['segments']

fails = []
for i in range(len(segs) - 1):
    t1 = segs[i]['text'].lower()
    t2 = segs[i+1]['text'].lower()
    gap = segs[i+1]['start'] - segs[i]['end']
    for kw in ANCHORS:
        if kw in t1 and kw in t2 and gap < 3.0:
            fails.append({
                'seg_pair': [segs[i]['id'], segs[i+1]['id']],
                'keyword': kw,
                'gap_s': round(gap, 2),
                'a': t1[:80], 'b': t2[:80],
            })

if fails:
    print(f"❌ ANCHOR-LAP: {len(fails)} pairs")
    for f in fails[:10]:
        print(f"  seg{f['seg_pair']} '{f['keyword']}' gap={f['gap_s']}s")
        print(f"    A: {f['a']}")
        print(f"    B: {f['b']}")
    sys.exit(1)
print(f"✅ No anchor-lap across {len(segs)} segments ({len(ANCHORS)} keywords checked)")
```

## Cấu trúc source keeps → keeps_v2 (13 keeps, fix cả 2 issue)

```python
# Drop:
# - keep[0]  [5.40, 16.40]  → ƯU TIÊN GIỮ keep[1] (transition "tại vì mình thích... nhãn hàng")
# - keep[12] [188.00, 196.80] → ƯU TIÊN GIỮ keep[13] (20.7s weather/longevity content)

v2 = [keeps[i] for i in range(15) if i not in {0, 12}]  # 13 keeps
# Total source ≈ 129.3s → at speed 1.3 = 99.5s (DƯỚI target 110-115s!)
# → Cần drop 1 keep HOẶC giảm speed còn 1.15x (149.1/1.15 ≈ 130s, vẫn cao)
```

## Lesson chính

1. **Layer độc lập là BẮT BUỘC** — strict tool chỉ check 1 chiều, cần ≥2 layer (strict + semantic + human spot).
2. **Window filter trong chosen_segs che giấu lỗi** — mỗi lần thấy script PASS mà parent flag issue → nghi ngờ filter quá chật.
3. **Whisper verify transcript là evidence độc lập** — LUÔN spot-check anchor keywords lặp sau khi script PASS.
