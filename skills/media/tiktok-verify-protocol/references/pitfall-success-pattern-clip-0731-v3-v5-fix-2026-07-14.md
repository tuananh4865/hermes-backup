# Pitfall SUCCESS PATTERN — Clip 0731 V3→V5 fix (14/07/2026)

> Real case where V4 FAILED Layer 1 + Layer 2 nhưng V5 đã PASS sạch cả 2 layers + transcript sạch sau khi áp dụng đúng 2-pattern-fix dưới đây.

## Background

- **Source:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/0731_v1/audio.json` — 72 segs, 333.8s
- **V3 keeps:** 17 segments, total 135.5s source → 104.2s sau 1.3x
- **V4 output:** ship FAIL với Layer 1 (1 treo) + Layer 2 ("các bạn" lặp seg[16-17] gap=0.0s)
- **V5 output:** 92.11s, PASS 0 issues cả 2 layers

## Pattern fix #1 — BỎ HẲN keep chứa anchor-lap liền kề (NOT just trim)

V3 keeps index[14]=[276.6, 279.0] chứa "Rất là mạnh luôn **các bạn**" + V3 keeps index[15]=[282.4, 297.7] chứa "**Các bạn** nào đang chật vật..." → Layer 2 báo anchor-lap "các bạn" với gap=0.0s giữa các seg.

**Fix không dùng:** chỉ trim 1 keep → vẫn còn nguy cơ lap ngầm vì giọng nói anh Tuấn Anh hay xuất hiện "các bạn" ~5-8 lần/clip.

**Fix ĐÃ dùng thành công:** bỏ HẲN keep index[15], giữ 1 anchor duy nhất ở keep[14]. Số keeps: 17 → 16. Sau render, Whisper verify transcript chỉ còn 1 instance "các bạn" cuối câu (seg[23] @ 85.68s), gap >5s với mọi instance khác → Layer 2 PASS.

## Pattern fix #2 — Trim keep dài giàu bridge words trước khi render

V3 keeps index[11]=[245.4, 251.1] chứa seg[45] "Và mục đích của nó để sinh ra là để hút bụi cho những góc nhỏ, bàn làm việc, góc nhỏ, phòng làm việc, những khu vực nhỏ thôi" (14.4s) — rất nhiều bridge words ("là", "của", "nó", "những", "thôi") dù KHÔNG trigger rule `duration > 5s AND bridge >= 50%` của `read_narrative_check.py` (vì predicate rõ ở cuối).

**Eyeball risk:** Whisper có thể hallucinate hoặc người nghe thấy "treo cảm xúc" dù không strict treo.

**Fix:** trim đầu keep từ [245.4, 251.1] → [246.0, 251.1] (cắt ~0.6s đầu câu dư). Keep mới 5.1s — trong ngưỡng an toàn cho TikTok vertical pace 1.3x.

## Pattern fix #3 — CTA hard-sell nằm cùng keep gây lặp thì PHẢI DROP

V3 keeps index[15]=[282.4, 297.7] chứa cả 2 câu:
- "Các bạn nào đang chật vật... thì các bạn có thể tham khảo..." (seg[57-58])
- source seg[71] "các bạn nào mà quan tâm thì có thể bấm vào link phía dưới để mua hàng nhé" (CTA hard-sell)

→ Khi fix pattern #1 bỏ keep này → MẤT luôn CTA cuối.

**Trade-off đã chấp nhận:** V5 chỉ kết thúc bằng "giá thành thì khoảng 300k-400k" (seg[26]) — KHÔNG có CTA "bấm vào link". Chấp nhận được vì:
- Giá đã rõ ràng
- TikTok review sản phẩm không ép CTA explicit
- Anchor-lap còn nguy hiểm hơn mất CTA

**Real case general rule:** Nếu phải chọn giữa CTA và anchor-free, **ƯU TIÊN anchor-free**. CTA có thể thêm ở overlay text/caption khi post lên TikTok.

## Whisper hallucination phenomenon @ speed 1.3x concat (PHÁT HIỆN MỚI)

V5 verify transcript seg[10] (52.36-55.34s): "Một cái xe hút bụi cầm tay nhỏ gọn như thế này các bạn" — whisper nghe source seg[19] "so với 1 máy hút bụi cầm tay nhỏ gọn như thế này" thành "Một cái xe hút bụi cầm tay" (chèn thừa từ). Nhưng đây là minor, ý nghĩa giữ được.

**Hơi nghiêm trọng hơn ở seg[10] keep index[7]**: source seg[17] "**và nó là 1 đầu hút và 1 đầu thổi**" → Whisper output "**Và nó là 1 đầu hút, 1 đầu hút và 1 đầu thổi**" (lặp "1 đầu hút"). Đây là **concat-induced hallucination**: khi speed 1.3x dồn các âm tiết từ 2 source seg liền kề thành 1 nhịp nhanh hơn, Whisper nghe thành "1 đầu hút, 1 đầu hút" thay vì "1 đầu hút và 1".

→ KHÔNG phải lỗi source/keep, KHÔNG phải anchor-lap. Chỉ là Whisper medium decode sai khi speed up.

**Rule tổng quát mới:** khi verify transcript thấy câu có 2 keyword liền kề nhau kiểu "X, X và Y" mà source chỉ có "X và Y" → check source audio.json gốc. Nếu source OK → đây là Whisper hallucination @ speed, KHÔNG TÁI EDIT.

## Checklist sau khi áp dụng 3-pattern

- [ ] Đã identify được anchor keyword nào xuất hiện ≥2 lần trong các keep LIỀN KỀ (Layer 2 gap<5s)
- [ ] Đã QUYẾT ĐỊNH trước: giữ 1 instance anchor duy nhất bằng cách BỎ HẲN keep lặp (không trim)
- [ ] Nếu keep dài >10s + nhiều bridge words → trim đầu/cuối keep để giảm rủi ro treo Whisper
- [ ] Nếu CTA nằm cùng keep với anchor-lap → chấp nhận drop CTA (ưu tiên anchor-free)
- [ ] Khi transcript verify thấy "X, X và Y" lặp từ → check source audio.json. Source không lặp → Whisper hallucination @ 1.3x speed, KHÔNG tái edit

## Câu anh dặn gối vào case này

> *"ĐỌC FULL TRANSCRIPT bằng mắt (BẮT BUỘC theo anh dặn 13/07)"* — đây là lý do phát hiện được câu seg[10] Whisper hallucination + kiểm chứng anchor-lap seg[14]→seg[15] đã fix.

## Kết quả cuối

| Layer | Trước (V4) | Sau (V5) |
|-------|-----------|----------|
| Layer 1 (verify_clip.py tương đương) | 1 treo | **0 issues** |
| Layer 2 (check_anchor_lap.py) | anchor-lap "các bạn" gap=0.0s | **✅ No anchor-lap** |
| Eyeball transcript | 1+ seg suspect | **Clean** |
| ffprobe spec | OK | **92.11s, 1080x1920@30fps, aac 44.1k** |
