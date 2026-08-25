# PITFALL #86 — smart_pad tự mở rộng range NUỐT câu lặp ở ranh giới

**Phát hiện:** 25/07/2026 — clip 0086 (Lenspen, 7-clip batch từ footages/)

## Symptom

`smart_pad` mặc định tìm `last_word_end` trong `[seg_start, seg_end]` rồi `+ 0.05s` pad. Khi 2 câu lặp nằm ở cuối range (ví dụ USP kết thúc nhưng câu "vừa nhanh sạch" lặp lại ngay sau đó và bị Whisper merge vào seg tiếp), `last_word_end` thuộc về câu lặp → range bị mở rộng và bao luôn cả câu lặp.

**Hit case (clip 0086 recheck):**
```
[37.30→39.72] "Điều này nó sẽ giúp cho các bạn lau ống kính mà vừa nhanh sạch"
[40.84→42.88] "Vừa nhanh sạch mà vừa an toàn"  ← LẶP "vừa nhanh sạch"
```
USP range gốc `[36.06, 49.80]`. Smart_pad mở rộng end thành `50.35` (do last word "vừa nhanh sạch" trong range 36.06→49.80 end tại 49.80, nhưng gap 0.04s khiến smart_pad mở rộng qua seg kế).

Verify bằng `scan_false_start.py` + scan lặp liền kề → FAIL: "vừa nhanh sạch" lặp.

## Root cause

`smart_keep_plan.py` tính `new_end = (lw["end"] if lw else k["end"]) + PAD` mà không cap tại `k["end"]`. Khi `lw.end ≈ k["end"] + small_offset` (do Whisper re-segmentation 1-2 frame), `new_end` vượt qua `k["end"]`.

## Fix

Set explicit `cap_end = min(new_end, k["end"] + PAD)` trong smart_pad loop. Nếu muốn giữ lại nội dung "vừa nhanh sạch" lặp, range tiếp theo (PAIN) phải start SAU đoạn lặp (`>50.30s` cho clip 0086).

## Recipe áp dụng cho mọi keep_plan có lặp ý ở giữa

```python
# In smart_pad loop:
new_end = (lw["end"] if lw else k["end"]) + PAD
new_end = min(new_end, k["end"] + PAD)  # ← cap
```

Hoặc nếu lặp ở cuối range và bạn MUỐN giữ, chuyển sang range kế với start > end_of_lặp, ví dụ:

| Range gốc | Range fix |
|---|---|
| USP `[36.06, 49.80]` | USP `[36.06, 49.80]` (cap end, KHÔNG mở rộng) |
| PAIN `[50.30, 71.16]` | PAIN `[53.76, 71.16]` (skip lặp "vừa nhanh sạch") |

## Verify

Re-transcript final.mp4 + scan lặp liền kề. Nếu cụm "vừa nhanh sạch" không còn xuất hiện 2 lần liền kề → PASS.

## Lesson

Smart_pad = pad CHỨA audio fade an toàn, KHÔNG PHẢI mở rộng range. Khi set `keep.end` cố ý (vì muốn cắt lặp/filler), KHÔNG để smart_pad ghi đè. Luôn cap tại `k["end"] + PAD` (max +0.05s).

## Cross-reference

- PITFALL #57 — TRANSCRIPT-FIRST VERIFY (lặp liền kề = cắt câu trước, giữ câu sau)
- PITFALL #79 — word-aligned padding (smart_pad gốc)
- PITFALL #85 — expected_duration PHẢI = SUM padded
