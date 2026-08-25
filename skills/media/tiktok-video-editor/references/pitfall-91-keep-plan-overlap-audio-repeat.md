# PITFALL #91 — KEEP_PLAN_OVERLAP: Audio + visual lặp khi 2 keep có vùng source chồng nhau

**Status:** FIRST-CLASS (v0.05.1 — 28/07/2026)
**Author:** Tuấn Anh + Hermes Agent
**Trigger:** Mọi keep_plan có 2 keep liên tiếp `next.start_padded < current.end_padded`

---

## Triệu chứng

User flag 28/07 lần 2: *"Vẫn bị lặp overlap"*. Em đã re-render 7 clip với `filter_complex` thay concat demuxer, subagent verify PASS (SSIM < 0.92 boundary), nhưng user VẪN thấy lặp. Root cause KHÔNG phải concat demuxer (đã fix) — mà là **keep_plan có vùng source bị overlap giữa 2 keep liên tiếp**.

Khi `filter_complex` trim từng keep `[start_padded, end_padded]` rồi concat:
- Keep N: source `[s_N, e_N]`
- Keep N+1: source `[s_{N+1}, e_{N+1}]` với `s_{N+1} < e_N` (overlap vùng `[s_{N+1}, e_N]`)
- Output: vùng `[s_{N+1}, e_N]` xuất hiện **2 LẦN** — frame + audio cùng content chồng lên nhau → user nghe "lặp", thấy "đè frame"

## Real case 28/07 (7 clip Pocket 3 ship 26/07)

| Clip | Tổng overlap | Worst transition |
|---|---|---|
| 0085 | 0.52s | HOOK→NEED 0.30s + PAIN_INSIGHT→GUIDE 0.22s |
| 0086 | 0.58s | HOOK→DESC 0.48s + DESC→USP 0.10s |
| **0088** | **2.22s** | RECAP→DETAIL 0.98s + DETAIL→CTA 0.88s |
| 0091 | 0.54s | SCENT→SCENT_DESC 0.44s + EFFECT→INSIGHT 0.10s |
| 0093 | 0.50s | HOOK→SCENT_DESC 0.50s |
| 0094 | 0.00s | sạch |
| 0095 | 0.00s | sạch |

Clip_0088 OLD duration 73.400s ≈ `sum(end_padded - start_padded) / 1.3 = 73.28s` (with overlap) → concat KHÔNG trim overlap.
Clip_0088 NEW duration 71.575s ≈ `sum_no_overlap / 1.3 = 71.57s` → đã trim đúng.

## Cách detect (BẮT BUỘC trước Step 7 render)

```python
# Quick overlap check — chạy 1 lần sau Step 6 build keep_plan.json
import json
d = json.load(open("keep_plan.json"))
keeps = d["keeps"]
overlaps = []
for i in range(len(keeps) - 1):
    cur, nxt = keeps[i], keeps[i+1]
    s, e = cur["start_padded"], cur["end_padded"]
    s_n = nxt["start_padded"]
    if s_n < e - 0.05:  # tolerance 0.05s cho word-boundary rounding
        overlaps.append((cur.get("name", i), nxt.get("name", i+1), round(e - s_n, 3)))
if overlaps:
    print(f"⚠️ KEEP_PLAN_OVERLAP detected ({len(overlaps)} pairs):")
    for a, b, sec in overlaps:
        print(f"   {a} → {b}: {sec}s overlap")
    print("FIX: trim end_padded của keep N = min(end_padded, next.start_padded)")
else:
    print("✓ no overlap")
```

Output phải là `✓ no overlap` TRƯỚC khi render. Nếu có overlap → **SỬA keep_plan TRƯỚC** không phải hack ở render.

## Fix (root cause — không workaround)

Trim `end` của mỗi keep (trừ keep cuối) bằng `min(end_padded, next.start_padded)`:

```python
def adjust_keeps(keeps):
    """Trim vùng overlap giữa 2 keep liên tiếp."""
    adj = []
    for i, k in enumerate(keeps):
        s = k["start_padded"]
        e = k["end_padded"]
        if i < len(keeps) - 1:
            e = min(e, keeps[i+1]["start_padded"])
        adj.append({**k, "end_padded": e})
    return adj
```

Áp dụng ngay sau Step 6 build keep_plan, TRƯỚC Step 6.5 SMART PAD:

```python
# In build keep_plan step
keeps = adjust_keeps(raw_keeps)  # ← thêm dòng này
keep_plan = {"keeps": keeps, "expected_duration": sum(k["end_padded"] - k["start_padded"] for k in keeps)}
```

Sau đó expected_duration = sum padded (PITFALL #85) vẫn đúng vì đã tính trên keeps đã trim.

## Verify (định lượng)

Sau khi re-render với keep đã trim:

```bash
# 1. Pre-speed duration khớp adjusted sum
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 tmp/clip_XXXX/v4_pre_speed.mp4

# 2. Final duration khớp expected / 1.3
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 Hermes-Edit/clip_XXXX_V2_NNs_FINAL_XXX.mp4

# 3. Audio MD5 0.3s chunks gần boundary — KHÔNG có duplicate
for t in 63.0 63.5 64.0 64.5 65.0 65.5; do
  ffmpeg -y -ss $t -t 0.3 -i final.mp4 -ac 1 -ar 8000 -f s16le - | md5
done
# Expect: 6 hash khác nhau, không trùng
```

## HARD RULE (FIRST-CLASS)

**Mọi keep_plan PHẢI pass overlap-check trước khi render.** Nếu fail → KHÔNG render, sửa keep_plan trước.

Anti-patterns:
- ❌ Render với keep_plan có overlap → user nghe lặp + thấy đè frame
- ❌ Hack bằng cách apply `-t` ở segment tiếp theo → mất word, mất nghĩa câu
- ❌ Hack bằng filter_complex `[0:v]overlay` để che overlap → thêm visual noise
- ❌ Tự tin "duration đúng" → duration có thể khớp với sum WITH overlap (concat demuxer) HOẶC NO overlap (filter_complex + trim) — phải check cả 2 cases

Real lesson: 28/07 subagent PASS verify SSIM boundary, nhưng MISS overlap vì SSIM chỉ check 1 frame, không check audio chunks hoặc tổng duration khớp expected.

## Cross-reference

- PITFALL #85 (expected_duration MUST = SUM padded) — liên quan: nếu overlap không trim, sum vẫn đúng nhưng audio bị lặp. PITFALL #91 phát hiện lỗi TRƯỚC khi PITFALL #85 check.
- PITFALL #90 (SMART PAD cap end) — cùng chủ đề "trim end_padded" nhưng PITFALL #90 trim về word boundary, PITFALL #91 trim về next.start_padded.
- `references/pattern-creative-arrange-not-just-cut.md` — nếu overlap phát sinh do keep_plan design sai (keep 2 câu liên tiếp mà không skip giữa), phải revisit Step 3-5.
