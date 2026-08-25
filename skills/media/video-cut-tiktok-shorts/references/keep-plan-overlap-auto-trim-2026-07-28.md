# Keep-Plan Overlap Auto-Trim (2026-07-28)

## Problem
When `keep_plan.json` has overlapping ranges between consecutive keeps in source, `ffmpeg filter_complex` trim+concat renders the overlap region **twice** — both audio and video frames. User reports: "vẫn bị lặp overlap" or "xếp chồng audio + hình ảnh".

**Why easy to miss:** Adversarial verify chỉ check 1-2 boundary frames via vision/SSIM. Overlap nằm GIỮA 2 keeps chứ không tại boundary → visual diff vẫn "OK" nhưng audio bị loop ngầm.

## Detection (run BEFORE render)
```python
import json
kp = json.load(open("tmp/clip_XXXX/keep_plan.json"))
keeps = kp["keeps"]
overlap_total = 0
for i in range(len(keeps) - 1):
    s, e = keeps[i]["start_padded"], keeps[i]["end_padded"]
    ns = keeps[i+1]["start_padded"]
    overlap = max(0, e - ns)
    overlap_total += overlap
    if overlap > 0.05:
        print(f"  ⚠️ {keeps[i]['name']} → {keeps[i+1]['name']}: overlap={overlap:.2f}s")
print(f"Total source overlap: {overlap_total:.2f}s")
```

## Auto-trim in filter_complex
For each keep (except last), set `end = min(end_padded, next.start_padded)`:
```python
for i, k in enumerate(keeps):
    s = k["start_padded"]
    e = k["end_padded"]
    if i < len(keeps) - 1:
        e = min(e, keeps[i+1]["start_padded"])
    # ... build trim filter
```

## Verify (duration match)
- Expected pre-speed WITHOUT overlap = `sum(end_adjusted - start)` for all keeps
- Actual pre-speed duration khớp expected → đã trim đúng
- Actual > expected → còn overlap chưa trim

```bash
# Compute expected
python3 -c "
import json
k = json.load(open('tmp/clip_XXXX/keep_plan.json'))['keeps']
t = 0
for i, x in enumerate(k):
    s = x['start_padded']
    e = min(x['end_padded'], k[i+1]['start_padded'] if i+1 < len(k) else x['end_padded'])
    t += e - s
print(f'{t:.3f}')"
# Compare with ffprobe
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 tmp/clip_XXXX/v4_pre_speed.mp4
```

## Real case 2026-07-28
7 clip Pocket 3 (0085/0086/0088/0091/0093/0094/0095), keep_plan có overlap:

| Clip | Total overlap (s) | Worst overlap |
|---|---|---|
| 0085 | 0.52 | HOOK→NEED 0.30s + PAIN_INSIGHT→GUIDE 0.22s |
| 0086 | 0.58 | HOOK→DESC 0.48s + DESC→USP 0.10s |
| **0088** | **2.22** | RECAP→DETAIL 0.98s + DETAIL→CTA 0.88s |
| 0091 | 0.54 | SCENT→SCENT_DESC 0.44s + EFFECT→INSIGHT 0.10s |
| 0093 | 0.50 | HOOK→SCENT_DESC 0.50s |
| 0094, 0095 | 0.00 | clean |

Adversarial subagent verify (PASS) chỉ check boundary frames MD5/SSIM → không thấy overlap vì overlap nằm bên trong keep, không tại boundary. Duration check (`old_dur × 1.3 ≈ sum_with_overlap`, `new_dur × 1.3 ≈ sum_no_overlap`) mới phát hiện được.

## Anti-patterns
- ❌ Trust `keep_plan.json` field `expected_duration` — tính theo sum(end_padded - start_padded) CÓ overlap, không phản ánh output thực tế
- ❌ Adversarial verify chỉ check 1 boundary frame — overlap có thể ở giữa keep
- ❌ Render filter_complex không auto-trim → audio + frame lặp tại vùng overlap, user nghe "delay/echo"

## Storage
- Backup V2 (concat demuxer cũ): `/Volumes/Storage-1/Pocket3/Hermes-Edit/_archive/v2_overlapped/`
- Backup V4 (fixed no-overlap): `/Volumes/Storage-1/Pocket3/Hermes-Edit/_archive/v3_fixed_noOverlap/`
- Script template: `/tmp/render_7clips_v4_noOverlap.sh`
