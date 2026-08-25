---
name: concave-bang-bon-hang
description: 'Mode B clip bán hàng TikTok VN — calibration range 90-120s, sweet spot ~110s. KHÔNG "ngắn nhất có thể". Apply khi anh yêu cầu "ngắn hơn/dưới 2 phút/cô đọng/làm bản dài hơn". Save to Pocket3/Hermes-Edit/.'
version: 1.0.0
author: 'Tuấn Anh + Hermes Agent (04-05/07/2026 evidence — clip 0688 V4 110.5s ✓ + clip 0687 V4 109s ✓. Pitfall cũ: V2 0687 86s quá ngắn mất nội dung. Reference session-2026-07-04-mode-b-calibration.md)'
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [video, editing, tiktok, mode-b, ban-hang]
    related-skills: [tiktok-video-editor]
---

# Mode B — Clip Bán Hàng (04-05/07/2026)

## 🚨 SWEET SPOT MỚI: ~110s (KHÔNG PHẢI ≤120s TỐI ĐA)

**Anh preference (04/07 evidence, clip 0688):**
> *"Ngắn hơn đi dưới 2 phút cho 1 video thôi em video bán hàng mà cần cô đọng mà làm cho khách hàng thấy được mình ở trong đó là được"*

**Anh correction (04/07 evidence, clip 0687):**
> *"Hơi ngắn quá nội dung bị mất đi nhiều! Làm lại một bản dài hơn chút đi"*

→ **Calibration range = 90-120s, sweet spot = ~110s** (không phải 86s, cũng không phải 120s+).

## 🎯 5 Framework Bán Hàng (GIỮ đủ)

Khi edit Mode B clip bán hàng, GIỮ narrative đủ **5 cluster representative** (KHÔNG skip cả cluster):

1. **HOOK + PRICE** (5-8% duration): punchline viral + giá
2. **AUTHORITY + USP** (15-20%): thương hiệu, xuất xứ, đặc điểm chính
3. **★ TRANSFORMATION + PUNCHLINE behavior** (15-20%): "trước/sau" + cảm giác cụ thể
4. **PROOF + ANALOGY** (25-30%): social proof (người khác hỏi, đồng đội thích) + so sánh evocative (đi biển, mùa hè...)
5. **PROS+CONS+CTA** (20-25%): điểm mạnh/yếu + giá so sánh + CTA đầy đủ

**Skip những gì:**
- Filler đầu ("chán động quá ha ha", "à ờ", lặp giá)
- USP expand/liệt kê quá chi tiết (VD: "có mùi A, mùi B, mùi C..." — chỉ giữ 2-3 mùi chính)
- Personal context dài ("mình không phải dân chuyên nước hoa..." quá 3 câu)
- Loop pattern ("từ khi mình mua", "rồi mình thấy") — chỉ giữ 1 lần
- Self-correction lặp 3+ lần
- Transition filler ("nói sao ta", "thì cái này")

## ⚠️ Kỹ thuật "cô đọng" đúng nghĩa

**ĐÚNG** = GIỮ đủ 5 cluster representative, BỎ filler GIỮA các cluster
**SAI** = BỎ cả cluster (V2 clip 0687 đã fail: bỏ seg 74 "đi biển" + seg 80 "cảm giác" → 86s mất narrative evocative)

**Heuristic:** Khi skip 1 segment, hỏi "cluster này còn representative không?". Nếu cluster chỉ còn 0-1 keep → KHÔNG skip, hoặc thêm keep khác trong cluster đó.

## 🔧 Smart Padding Rule (FIX overlap bug)

Khi build ranges với consecutive keeps, bug overlap xảy ra khi seg sau start < seg trước end (Whisper transcripts hay có segment overlap 0.05-0.15s).

**Rule đúng:**
```python
if start - prev_end > 0.3:
    cur_start = max(0, start - 0.10)  # Padding gap lớn
else:
    cur_start = max(start, prev_end)  # KHÔNG pad back, prevent overlap

gap_to_next = next_start_raw - end
if gap_to_next > 0.3:
    cur_end = end + 0.15
elif gap_to_next < 0:
    cur_end = next_start_raw  # Overlap! Trim at next start
else:
    cur_end = end  # No padding, close keep
```

**Anti-pattern cũ:**
```python
# ❌ Fails với Whisper overlap
cur_start = max(0, start - 0.10)  # Always pad 0.10
```

## 🔍 Detect Concat-Induced Hallucinate (NEW 04/07)

Khi re-Whisper output có segment ngắn ≤3 từ với avg_prob < 0.5, đó là **concat-induced hallucinate** (Whisper invent từ audio boundary artifact), KHÔNG phải content thật.

**Detect rule:**
```python
for s in segs:
    text = s['text'].strip()
    avg_prob = sum(w.get('probability', 1) for w in s.get('words', [])) / max(len(s.get('words', [])), 1)
    if len(text.split()) <= 3 and avg_prob < 0.5:
        # Hallucinate! Bỏ segment này khỏi output
        # Verify audio RMS để confirm
```

**Real case 04/07 (clip 0687 V1 seg 14):**
- Text: "Cái thôi" (2 từ)
- Word prob: "Cái"=0.27, "thôi"=0.40
- Audio RMS: -20.9dB (audio có, không silence)
- Source thực sự: "phải nói là giống như các bạn đi biển á" (seg 74)
- **Root cause:** padding 0.15s tạo audio gap → Whisper sinh "Cái thôi"

**Fix:** Cut exactly tại source end, KHÔNG pad khi seg sau liền kề hoặc overlap.

## 📊 Verify checklist (BẮT BUỘC trước ship)

- [ ] Duration 90-120s, sweet spot ~110s
- [ ] 0 hallucinate (avg_prob check)
- [ ] 0 câu treo thật (predicate check)
- [ ] ≥15/20 punchline keywords present
- [ ] Audio RMS > -25dB (full audio)
- [ ] 5 cluster narrative đầy đủ
- [ ] Output path flat (no folder con)
- [ ] Filename: `{nội-dung-viet-tat}-{ddmmyyyy}.mp4`

## Reference

- `references/session-2026-07-04-mode-b-calibration.md` — full evidence 0688 V1→V4 + 0687 V2→V4 evolution
- `references/smart-padding-no-overlap.md` — implementation detail
- `references/concat-hallucinate-detection.md` — detection script

## Related

- `tiktok-video-editor` — full skill (Mode A + Mode B + workflow 7-step)
- `tiktok-transcript-pipeline` — Whisper MLX transcribe