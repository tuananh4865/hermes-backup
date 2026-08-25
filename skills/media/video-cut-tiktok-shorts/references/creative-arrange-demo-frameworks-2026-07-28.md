# CREATIVE ARRANGE Demo Frameworks (28/07/2026 — 4 demos verified)

Tuấn Anh yêu cầu demo kỹ thuật sắp xếp lại nội dung video. Em đã demo 4 clip bằng 4 framework KHÁC nhau để cover breadth. Bài học: **mỗi demo phải apply framework MỚI**, không lặp demo trước.

## 4 Frameworks đã verify

### 1. Emotional HOOK (clip_0088 — Ốp Pocket 3 Full)

**Source narrative:** HOOK → PROTECT → SLOT → INTERIOR → RECAP → DETAIL → CTA (linear feature dump)

**Re-arrange:** HOOK_PAIN → SOLUTION → USP_SLOT → USP_PROOF → PROTECT → CTA

**Strategy:** Mở bằng PAIN emotional (túi nhỏ Pocket 3 quá bất tiện) → user đồng cảm → tiếp tục xem

**Emotional arc:** TENSION → RELIEF → VALUE → EMOTION → ACTION

**Final:** 34.3s (compact, gọn hơn 53% vs source 73.4s)

**When to use:** Khi source có PAIN tự nhiên (user kể về sự bất tiện, frustration), KHÔNG cần tạo pain mới.

### 2. Counter-intuitive HOOK (clip_0095 — Lenspen)

**Source narrative:** HOOK (lau bằng áo → chày xước) → INTRO (sắm bút) → USP (carbon fiber) → CTA (lâu ống kính sai)

**Re-arrange:** HOOK_INSIGHT (counter-intuitive) → PAIN → SOLUTION → USP_PROOF → USP_WRAP → CTA

**Strategy:** Lấy insight MẠNH từ CTA source ("điện thoại mới quay kém không phải do điện thoại mà do vệ sinh sai") → đưa lên đầu → thách thức belief → user tò mò

**Emotional arc:** CURIOSITY → EDUCATION → RELIEF → VALIDATION → VALUE → ACTION

**Final:** 113s (full Mode B+, giữ toàn bộ insight)

**When to use:** Khi source có INSIGHT counter-intuitive mạnh ở CTA → move lên đầu.

### 3. PROBLEM→SOLUTION + OmniVoice PAIN (clip_0697 — Bút cảm ứng iPad Gojodot Pro)

**Source narrative:** HOOK → INTRO (giá 1/5) → FEATURES → MISSING_FEATURE (KHÔNG có bấm 2 lần + cảm biến lực) → RECAP → DETAIL → CTA

**Re-arrange:** HOOK_PRICE → PAIN_OMNIVOICE → SOLUTION_FEATURES → PROOF_1 → PROOF_2 → PROOF_3 → CTA

**Strategy:** Source THIẾU PAIN rõ → dùng OmniVoice generate voice PAIN mới chèn vào đầu (emotion [sigh] + [question-ah]) overlay trên B-roll source. Voice clone từ `tuan_anh_session_2026-07-23.pt`.

**Emotional arc:** CURIOSITY → TENSION → RELIEF → VALIDATION → ACTION

**Final:** 99s

**When to use:** Khi source KHÔNG có PAIN setup rõ (user mới review sản phẩm chưa từng gặp vấn đề) → generate voice mới chèn vào.

### 4. PROBLEM→SOLUTION từ source (clip_0699 — Bút cảm ứng iPad giá rẻ)

**Source narrative:** HOOK (lặp 3 lần) → PRICE → DESIGN → FEATURES → SẠC_KHÔNG_DÂY → KẾT_NỐI_NHANH → THIẾT_KE → CTA

**Re-arrange:** HOOK_PRICE → SOLUTION_FEATURES → PROOF_USP → CTA (drop QUALITY_DESIGN)

**Strategy:** Source CÓ PAIN qua price-shock ("1/5 giá chính hãng") → KHÔNG cần OmniVoice. Drop QUALITY_DESIGN vì Whisper loop hallucinate.

**Emotional arc:** TENSION → RELIEF → VALIDATION → ACTION

**Final:** 90s

**When to use:** Khi source đã có PAIN qua PRICE-SHOCK (giá so với hàng chính hãng) → dùng trực tiếp.

## Decision matrix — chọn framework nào

| Source characteristic | Recommended framework |
|---|---|
| Source có PAIN tự nhiên (user kể frustration) | **Emotional HOOK** |
| Source có INSIGHT counter-intuitive mạnh ở CTA | **Counter-intuitive HOOK** |
| Source THIẾU PAIN setup rõ + bạn có file voice clone .pt | **PROBLEM→SOLUTION + OmniVoice PAIN** |
| Source có PAIN qua PRICE-SHOCK (so với hàng chính hãng) | **PROBLEM→SOLUTION từ source** |
| Source dài >300s, nhiều features (>20) | **TRỌN-CÂU selection** (mode B-strict 110-120s, accept 60-80% features) |

## HARD RULES (FIRST-CLASS)

### 1. Mỗi demo phải apply framework MỚI

Anh sẽ không thấy demo thứ 2 với cùng strategy. Khi demo "sắp xếp lại nội dung", mỗi clip phải dùng 1 framework KHÁC để show breadth.

### 2. Mode B target 75-110s

| Range | Status |
|---|---|
| 75-110s | Hoàn hảo Mode B |
| 111-130s | Accept, gần Mode B |
| > 130s | Phải cut gọn thêm |

Nếu tổng pre-speed × 1.3 > 130s → cut SOLUTION/PROOF (giữ HOOK + PAIN + CTA).

### 3. Whisper loop hallucinate anti-pattern

**Triệu chứng:** Audio source có 1 mention "X" (vd "hỗ trợ nghiêng bút") nhưng tại boundary giữa QUALITY_DESIGN và CTA có audio silence ngắn → Whisper large-v3 hallucinate lặp 50+ lần "X" trong output.

**Fix:**
1. Detect loop bằng cách đếm X trong Whisper transcript của final file
2. Nếu loop > 5 lần trong 2s window → DROP segment gây ra
3. Verify bằng cách check `[segment_count] × [mean_phrase_count]` — nếu vượt expected thì có loop

**Real case 28/07 clip_0699:** "Hỗ trợ nghiêng bút" xuất hiện 1 lần trong source segment 43, nhưng Whisper hallucinate lặp 50+ lần trong final file. Fix: drop QUALITY_DESIGN keep (source 221-252) → 4 keeps thay vì 5.

### 4. Verify định lượng bắt buộc

Mỗi demo phải pass:
- 100% boundary MD5 unique (no stuck frame at segment cuts)
- Whisper large-v3-mlx transcript SẠCH (NO loop hallucinate, NO missing content)
- Final duration khớp `sum(keep_padded_duration) / 1.3` ±0.1s

Nếu final duration ≠ expected → check overlap hoặc trim issue.

### 5. PAIN placement

**Nếu có sẵn PAIN trong source:** đặt PAIN ở keep 2 (ngay sau HOOK)
**Nếu KHÔNG có PAIN trong source:** generate PAIN bằng OmniVoice chèn ở keep 2
**Nếu source có PRICE-SHOCK:** dùng PRICE-SHOCK luôn làm PAIN (1/5 giá chính hãng = PAIN cho Apple Pencil)

PAIN đặt SAU HOOK_PRICE (price shock) → relief ở keep 3 (SOLUTION).

### 6. PROOF giữ gọn

Không cần demo full PROOF (sạc không dây 3 phút, kết nối nhanh 5 phút). Mỗi PROOF chỉ cần 1 punch ngắn 5-10s:
- "Sạc không dây / hit là sạc" (8s)
- "Kết nối nhanh / hít lại là sáng" (10s)
- "Nghiêng bút / viết vẽ" (4s)

3 PROOF × 10s = 30s punch thay vì 90s demo chi tiết.

## Workflow 5 bước (CREATIVE ARRANGE demo)

```
1. Source transcript + keep_plan (initial)
   ↓
2. Phân tích narrative → identify framework phù hợp từ decision matrix
   ↓
3. Build re-arranged keep_plan (apply framework)
   ↓
4. Render pre-speed (filter_complex + auto-trim overlap)
   ↓
5. Apply speed 1.3x → Whisper transcript verify → boundary MD5 verify
```

## Common pitfalls

- ❌ Trust subagent SSIM PASS boundary → MISS overlap trong source giữa các keep
- ❌ Drop source segment có PAIN nhẹ → user không cảm thấy tension
- ❌ Add 3+ PROOF demo dài → final > 130s, không kịp CTA
- ❌ PAIN do AI generate không khớp voice clone hiện có → nghe lạ
- ❌ Counter-intuitive HOOK cường điệu → user thấy clickbait, bỏ qua
- ❌ Re-arrange KHÔNG theo framework rõ ràng → random shuffle, không có arc

## References

- Skill `tiktok-video-editor` v0.05.1: PITFALL #91 KEEP_PLAN_OVERLAP (auto-trim pattern)
- Skill `video-cut-tiktok-shorts`: 8-step workflow + 3-LAYER REASONING FRAMEWORK
- Wiki demo files:
  - `/Volumes/Storage-1/Hermes/wiki/queries/clip_0088_creative_arrange_demo_2026-07-28.md`
  - `/Volumes/Storage-1/Hermes/wiki/queries/clip_0095_creative_arrange_demo_2026-07-28.md`
  - `/Volumes/Storage-1/Hermes/wiki/queries/clip_0697_problem_solution_omnivoice_demo_2026-07-28.md`
  - `/Volumes/Storage-1/Hermes/wiki/queries/clip_0699_problem_solution_demo_2026-07-28.md`