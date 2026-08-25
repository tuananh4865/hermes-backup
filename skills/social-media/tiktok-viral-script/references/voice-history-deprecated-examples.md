---
title: Voice History — Deprecated Examples Reference
created: 2026-07-02
type: reference
applies_to: tiktok-viral-script
trigger: Historical reference ONLY — DO NOT use these as voice model for new content
---

# Voice History — Deprecated Examples

> **⚠️ CRITICAL WARNING (2026-07-02):** Examples trong file này dùng voice "anh + mấy con vợ" CŨ, đã bị user LOẠI BỎ HOÀN TOÀN từ 13/06/2026. File này chỉ lưu giữ để tham khảo CẤU TRÚC script (hook → body → CTA flow, Gen Z slang patterns, intensity levels), KHÔNG PHẢI voice model cho content mới.

**Voice đã đổi từ 13/06/2026:**
- ❌ KHÔNG dùng: "anh + mấy con vợ", "mấy đứa", "mấy chị", "các bạn ơi", "các mom ơi"
- ✅ Voice MỚI: Trung tính, chuyên nghiệp — "mình"/"bạn" hoặc neutral
- ⚠️ Default = trung tính, KHÔNG tự động dùng voice cũ

**Wiki ground truth:** `wiki/entities/learned-about-tuananh.md` → "Voice & Pronouns" section

**Runtime enforcement:** `scripts/voice-scan.sh` — scan output TRƯỚC khi gửi user

---

## Ví dụ 1: Product Discovery Hook (Kẹp Tóc Nơ Bong Bóng)

**Mục đích tham khảo:** Cấu trúc hook → body → CTA, Gen Z slang density, social proof pattern

**Voice CŨ (KHÔNG DÙNG LÀM MODEL):**
```
[HOOK — 0-3s]
"Anh nhìn thấy cái này trên TikTok lúc 2h sáng và không ngủ được luôn"

[BODY — 3-20s]
"Mấy con vợ ơi, anh thề luôn, cái nơ bong bóng này nó cute vãi.
Anh mua cho em gái, xem review 1星 → 5星 hết luôn.
Mà giá chỉ 36K thôi, vừa túi học sinh.
Cái này bán 19K đơn trong 7 ngày — nghe có vẻ nhiều nhưng mà ạ,
ai bán được cái này commission nó ngon lắm luôn."

[CTA — 20-25s]
"Link in bio đó mấy con vợ ơi, mua ủng hộ anh đi chứ"
```

**Cấu trúc để HỌC (không phải để copy voice):**
- Hook: Pattern disrupt + curiosity ("nhìn thấy lúc 2h sáng")
- Body: Social proof (review rating) + price comparison + volume metrics
- CTA: Casual + specific action ("link in bio", "ủng hộ anh")

---

## Ví dụ 2: Warning Hook (Nam Thư Parody)

**Mục đích tham khảo:** Hook contrarian, warning style, drama opening

**Voice CŨ (KHÔNG DÙNG LÀM MODEL):**
```
[HOOK — 0-3s]
"⚠️ CẢNH BÁO CÓ NAM THƯ — mấy con vợ né gấp"

[BODY — 3-20s]
"Không phải dating nam thư đâu, là cái kẹp tóc nam thư này
nó toxic cho ví tiền của mấy con vợ luôn.
Mấy ơi, 32K thôi mà ai cũng mua, hàng 32K đơn trong tuần.
Anh tính nhẩm xong hoảng luôn — sản phẩm này ai bán cũng ăn commission."

[CTA — 20-25s]
"Nhé, mua ủng hộ anh đi mấy con vợ chứ"
```

**Cấu trúc để HỌC:**
- Hook: Warning icon + contrarian open + urgency
- Body: Pivot (không phải X, là Y) + price anchor + volume proof
- CTA: Soft imperative + "ủng hộ"

---

## Ví dụ 3: Transformation Hook (Charm Chữ Mini)

**Mục đích tham khảo:** Social proof + curiosity + volume metric

**Voice CŨ (KHÔNG DÙNG LÀM MODEL):**
```
[HOOK — 0-3s]
"Ngay cả nhân viên ngân hàng cūng hỏi anh mua ở đâu"

[BODY — 3-20s]
"Không phải anh khoe đâu, charm mini này nó làm cả phòng đều hỏi.
21K một cái, 164K đơn trong 7 ngày — mấy con vợ biết cái gì hot chưa?
Anh thì biết rồi, vì anh đã bán được 2 tuần nay."

[CTA — 20-25s]
"Mua link in bio đi, giao nhanh lắm luôn"
```

**Cấu trúc để HỌC:**
- Hook: Authority figure reaction (bank teller) — high social proof
- Body: Volume metric (164K orders) + FOMO angle
- CTA: Specific action (link in bio) + speed promise

---

## Voice MỚI — Sample cho reference (2026-06-13+)

**Cùng pattern (transformation hook) nhưng dùng voice trung tính:**
```
[HOOK — 0-3s]
"Ngay cả nhân viên ngân hàng cũng hỏi mua ở đâu"

[BODY — 3-20s]
"Không phải khoe đâu, charm mini này làm cả phòng đều hỏi.
21K một cái, 164K đơn trong 7 ngày — biết cái gì hot chưa?
Đã bán được 2 tuần nay rồi."

[CTA — 20-25s]
"Link in bio đó, giao nhanh lắm"
```

**Note:** Giữ nguyên cấu trúc hook → body → CTA, chỉ đổi voice xưng hô.

---

## Lý do file này tồn tại

1. **Lịch sử:** Skill cũ có 3 examples voice "anh + mấy con vợ" ở cuối SKILL.md (trước 13/06/2026). Sau pivot 13/06, examples vẫn nằm trong SKILL.md → LLM contamination.
2. **Ngày 02/07/2026:** Em viết content Facebook (KHÔNG phải TikTok script) nhưng LLM vẫn dùng "mấy con vợ" 3 LẦN trong cùng 1 reply → user flag → lesson mới.
3. **Fix:** Tách examples ra reference file này + thêm runtime gate `scripts/voice-scan.sh` để enforce voice rule ở generation time, không chỉ documentation.

## Bài học vĩnh viễn

**Documentation ≠ enforcement.** Khi LLM đọc skill, nó tune theo examples gần nhất. Voice rule ở đầu SKILL.md KHÔNG đủ mạnh nếu examples ở cuối file vẫn chứa voice cũ. CẦN:
1. Examples cũ → reference file (KHÔNG nằm trong SKILL.md)
2. Runtime gate → `scripts/voice-scan.sh` scan output trước khi gửi
3. Wiki là ground truth → check `learned-about-tuananh.md` voice rule

**Pattern recognition:** Bất kỳ preference nào user thay đổi MÀ skill cũ vẫn còn examples cũ → sẽ có contamination. Fix: tách examples + enforcement script.