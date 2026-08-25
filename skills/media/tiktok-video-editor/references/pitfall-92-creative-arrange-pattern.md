# PITFALL #92 — Creative Arrange Pattern (Linear → Emotional Arc)

**Status:** FIRST-CLASS (v0.06.0 — 28/07/2026)
**Author:** Tuấn Anh + Hermes Agent (from 28/07 demos clip_0088 + clip_0095)
**Trigger:** Mọi keep_plan đã chọn xong content → trước khi render, ASK: "Sắp xếp này có phải linear feature dump không? Có thể sắp lại theo emotional arc để lôi cuốn hơn không?"

---

## Triệu chứng (problem)

Source transcript thường là **linear feature dump**: người nói tự nhiên đi từ A → B → C → D theo thứ tự họ nghĩ ra, KHÔNG phải thứ tự emotional tốt nhất cho viewer. Khi em cut giữ nguyên source order:
- Pain quan trọng nằm giữa clip → user đã lướt mất
- Solution xuất hiện sớm quá → không có tension để release
- USP punch technical đến cuối → user chưa thấy lý do nên tin
- ARC thiếu **TENSION → RELIEF → VALUE → ACTION** — chỉ là liệt kê USP

## Real case 28/07 (verified ship)

| Clip | Source length | V2 final | V3 creative | Δ |
|---|---|---|---|---|
| clip_0088 (Ốp Pocket 3) | 103.7s | 73.4s (linear dump) | **34.3s** (compact emotional arc) | -53% |
| clip_0095 (Lenspen) | 182s | 81.2s (linear dump) | **112.5s** (counter-intuitive insight HOOK) | +39% |

---

## 2 verified recipes

### Recipe A — Emotional HOOK (clip_0088 demo)

**Khi nào dùng:** Source có pain cụ thể, rõ ràng, relatable. Viewer dễ đồng cảm.

```
V2 source: HOOK feature → feature → feature → PAIN (giữa) → RECAP → CTA
V3:        HOOK_PAIN → SOLUTION → USP_punch → USP_proof → EMOTION → CTA
```

**Arc:** TENSION → RELIEF → VALUE → EMOTION → ACTION

**Demo clip_0088 (Ốp Pocket 3 Full):**
- HOOK_PAIN (7s): "Túi nhỏ đi kèm Pocket 3 quá nhỏ, bỏ vô bất tiện lắm" — emotional hook đầu
- SOLUTION (3s): "Bọc Pocket 3 vô rồi quăng vô bất cứ túi nào cũng được" — relief ngay
- USP_SLOT (5s): "4 slot len/filter tùy ý" — punch early
- USP_PROOF (15s): "Ron cao su ép thân hình, gimbal không nhúc nhích" — technical evidence
- PROTECT (7s): "Bảo vệ toàn diện cho chiếc Pocket 3 yêu quý" — chuyển emotional
- CTA (6s): "Bấm link mua"

### Recipe B — Counter-intuitive HOOK (clip_0095 demo)

**Khi nào dùng:** Source có 1 insight đảo ngược belief mạnh nằm CUỐI source (thường là CTA cuối). Insight này nên lên đầu để challenge belief + tò mò.

```
V2 source: HOOK pain (instructional) → INTRO → USP (dài) → CTA insight (cuối)
V3:        HOOK_INSIGHT (counter) → PAIN (deep) → SOLUTION → USP_PROOF → USP_WRAP → CTA
```

**Arc:** CURIOSITY → EDUCATION → RELIEF → VALIDATION → VALUE → ACTION

**Demo clip_0095 (Lenspen):**
- HOOK_INSIGHT (15s): "Điện thoại mới ra quay kém / không phải do điện thoại / do vệ sinh sai / sắm Lenspen đổi cách vệ sinh" — counter-intuitive đầu
- PAIN (29s): "Xài áo lau ống kính → chày xước → thay kính mới → tốn tiền oan" — education
- SOLUTION (21s): "Sắm bút này nhỏ gọn, 2 đầu lông + carbon fiber"
- USP_PROOF (54s): "Carbon fiber hàng tỷ sợi nhỏ → lực hút → hút bụi sâu → lau sạch + không gây hại" — validation
- USP_WRAP (23s): "Nhỏ gọn mà bảo vệ tuổi thọ ống kính"
- CTA (3s): "Đó là lý do tại sao" — loop insight

---

## Khi nào KHÔNG nên Creative Arrange

- **SP quá mới, audience chưa biết** → giữ linear feature dump để educate trước
- **Source < 30s** → không đủ material để rearrange
- **Tutorial / how-to clip** → giữ source order (steps logical)
- **User explicit "giữ nguyên thứ tự"** → respect

## Workflow áp dụng

```python
# Step 1: Đọc source transcript + keep_plan V2/V4 (current source order)
# Step 2: Đánh dấu segment theo archetype:
#   - HOOK_PAIN: pain cụ thể, relatable
#   - HOOK_INSIGHT: counter-intuitive belief challenge
#   - SOLUTION: 1 câu punch reveal giải quyết pain
#   - USP_PUNCH: tính năng đặc biệt KHÔNG có ở standard
#   - USP_PROOF: technical evidence (số liệu, demo, so sánh)
#   - USP_WRAP: giá trị thực tế (nhỏ gọn, bền, tiện)
#   - PAIN: giải thích tại sao problem tồn tại
#   - CTA: call-to-action cụt gọn

# Step 3: Map archetype → Recipe A hoặc Recipe B
# Step 4: Build keep_plan_v3 (jumps around source timestamps, NO overlap)
# Step 5: Render filter_complex (each keep = separate -ss -t -i input)
# Step 6: Apply speed 1.3x
# Step 7: Verify
```

## Verify (định lượng)

1. **100% boundary MD5 unique** — no overlap, no stuck frame (PITFALL #91)
2. **Whisper transcript readable** — chạy `whisper-transcribe` rồi đọc output, đảm bảo:
   - Đúng thứ tự emotional arc
   - Không bị cắt câu giữa chừng (mỗi keep phải có câu hoàn chỉnh)
   - CTA rõ ràng cuối clip
3. **Spec TikTok** — 1080×1920, 30fps, h264+aac 44.1kHz (PITFALL #83)

## Source overlap check (BẮT BUỘC)

Vì creative arrange jumps around source timestamps, em KHÔNG dùng source-order check overlap nữa. Thay vào đó: **MỖI KEEP phải là source range ĐỘC LẬP** (không 2 keep nào share source range):

```python
for i in range(len(keeps)):
    for j in range(i+1, len(keeps)):
        a, b = keeps[i], keeps[j]
        if a["start"] < b["end"] and b["start"] < a["end"]:
            raise ValueError(f"Source overlap: {a['name']} and {b['name']}")
```

## Hard rule (FIRST-CLASS)

**Mọi keep_plan mới BẮT BUỘC apply Creative Arrange check trước khi render.** Nếu không thể rearrange (vì SP/tutorial/insight yếu), giữ source order nhưng document lý do trong keep_plan.

## Cross-reference

- **PITFALL #89** (CREATIVE ARRANGE original rule): "Arrange lại transcript theo narrative arc thu hút, KHÔNG giữ source order cứng nhắc"
- **PITFALL #91** (KEEP_PLAN_OVERLAP): defensive auto-trim in build_pre_speed.sh — works for both source-order và creative-order
- **Recipe 12** (HOOK→PAIN→SOLUTION→USP→CTA): framework gốc
- **skill tiktok-product-script** (v0.9.2): mỗi version anchor 1 NHU CẦU duy nhất — Creative Arrange giúp find anchor tự nhiên hơn
