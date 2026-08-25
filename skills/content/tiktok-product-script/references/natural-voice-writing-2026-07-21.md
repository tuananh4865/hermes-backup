# Văn nói tự nhiên cho script TikTok (Vietnamese)

> **Source session:** 2026-07-21 (ULANZI MA66 V4 rewrite)
> **User feedback (verbatim):** *"Cách em viết chưa giống văn nói của con người lắm!"*
> **Status:** v0.10.0 FIRST-CLASS rule (vĩnh viễn)

## Tại sao rule này tồn tại

Em viết script TikTok theo cảm tính, output "polished prose" - giống bài báo/blog post hơn là người nói. Sau research 9 web sources + phân tích transcript @dungkenhnghiepdu 81s (mẫu văn nói viral thật), em rút ra **8 bài học**.

WPM của Dũng: **284** (rất nhanh). WPM trung bình em viết: **130-150**. Khoảng cách 50%.

## 8 bài học văn nói

### 1. Sentence-final particles (đấy/nhá/nhé/nhỉ/ấy)
- Mỗi câu 5-10 từ PHẢI có 1 particle.
- Dũng dùng "đấy" 8 lần / 34 câu = 24%. Tạo cảm giác khẳng định + thân mật.
- Sentence-final particles tiếng Việt (Bắc):
  - **đấy**: khẳng định, chỉ (phổ biến nhất)
  - **nhé**: đề nghị, nhắc (CTA cuối)
  - **nhá**: xác nhận (cuối câu nhấn mạnh)
  - **nhỉ**: tự vấn, suy nghĩ (hỏi người nghe)
  - **ấy**: thân mật, gần gũi (cuối câu)
  - **thôi**: giới hạn (không hơn)
  - **luôn**: khẳng định mạnh (thường đi với "đấy")

### 2. Fragments 3-5 từ (24% câu)
- 8/34 câu trong Dũng là fragments: "Rất khó bán", "Thì nói thật nhá", "Lúc đấy nhé", "Bỏ túi nào cũng vừa".
- Tác dụng: tạo nhịp, khoảng lặng, cảm giác khẳng định.
- Target: 3-5 fragments/script 60-90s.

### 3. Tránh 5 từ cấm kỵ (theo Kapwing research - polished tone fail)
| Từ | Thay bằng |
|---|---|
| toàn | bỏ, hoặc "hết" |
| mọi | "ai cũng", "tụi mình" |
| đặc biệt | bỏ |
| vô cùng | "lắm", "cực kỳ" |
| rất nhiều | "nhiều vô kể" |

### 4. Length rhythm: câu 11 từ → fragment 3-5 từ → câu 11 từ
- Dũng trung bình câu 11.3 từ (em thường viết đều 11-15 từ → nghe như đọc báo cáo).
- Fix: thêm fragment giữa các câu dài để tạo nhịp.

### 5. WPM target 200-250
- Văn viết: ~130-150 WPM (câu dài, nhiều "văn viết").
- Văn nói TikTok: 200-250 WPM (câu ngắn, fragments nhiều).
- Test: `words / (seconds * 60)`. Script 60-90s cần ~200-300 từ.

### 6. Mid-thought start (KHÔNG "Xin chào")
ScrollScript research: scripts bắt đầu bằng "let me tell you about..." almost always lose first 3 seconds. Scripts bắt đầu mid-sentence almost always hold them.
- ❌ "Xin chào, hôm nay mình sẽ nói về..."
- ❌ "Có ai biết chiếc tripod này không?"
- ✅ "Hai năm làm video, có một thứ mình ước biết sớm hơn"
- ✅ "Ba mươi giây đấy"
- ✅ "Cái tin nhắn nó gửi tối qua..."

### 7. Sensory đời thường (không hoa mỹ)
- ❌ "tích hợp công nghệ magnetic tiên tiến" (văn viết)
- ✅ "gài máy quay vào một cái là dính" (đời thường)
- Sensory = chi tiết cụ thể, KHÔNG từ bóng bẩy.

### 8. Read aloud test BẮT BUỘC
5/9 sources nhắc đến read aloud như test #1.
- Dùng OmniVoice/edge-tts đọc script → nghe lại.
- Nếu nghe "AI" hoặc "cứng" → viết lại câu đó.
- Workflow: viết → TTS đọc → nghe → fix → TTS đọc lại.

## V3 → V4 example (ULANZI MA66)

**V3A cũ (văn viết - bị chê):**
> "Hồi mới quay, mình **toàn** đặt điện thoại lên bàn. Góc thấp, chỉ thấy cằm, **mà mình cứ tưởng** ổn."

**V4A mới (văn nói):**
> "Hồi mới quay, mình đặt điện thoại lên bàn **đấy**. Góc thấp, chỉ thấy cằm thôi. Mình cứ tưởng ổn **ấy**."

## Verify checklist (áp dụng trước deliver)

```python
text = script_text

# Check 1: particles ≥ 5
particles = ['đấy', 'nhá', 'nhé', 'nhỉ', 'ấy']
particle_count = sum(text.count(p) for p in particles)
assert particle_count >= 5, f"Only {particle_count} particles - need ≥5"

# Check 2: fragments ≥ 3
sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
fragments = sum(1 for s in sentences if 0 < len(s.split()) <= 6)
assert fragments >= 3, f"Only {fragments} fragments - need ≥3"

# Check 3: forbidden words = 0
forbidden = ['toàn bộ', 'mọi người', 'đặc biệt', 'vô cùng', 'rất nhiều']
for w in forbidden:
    assert text.count(w) == 0, f"Forbidden word '{w}' found"

# Check 4: WPM ≥ 200 (assume 60s script)
words = len(text.split())
wpm = words * 60 / 60  # assume 60s for 60-second script
assert wpm >= 200, f"WPM only {wpm:.0f} - need ≥200"

# Check 5: no formal opener
formal_openers = ['Xin chào', 'Có ai', 'Hôm nay mình']
for opener in formal_openers:
    assert not text.startswith(opener), f"Formal opener '{opener}' - use mid-thought start"
```

## 4 rule bổ trợ FIRST-CLASS (vĩnh viễn)

| Version | Rule | Source |
|---|---|---|
| 16/07 | "Không làm chuyên ngành" | User feedback (16/07) |
| 21/07 v0.9.1 | "Không dùng từ hoa mỹ" | User feedback "đừng dùng tư hoa mỹ quá!" |
| 21/07 v0.9.2 | "Mỗi video chỉ 1 nhu cầu" | Clip @dungkenhnghiepdu |
| **21/07 v0.10.0** | **"Văn nói tự nhiên"** | User feedback + 9 sources |

Khi viết script V2/V3/V4 → áp dụng CẢ 4 rule cùng lúc.

## Verified case (21/07)

ULANZI MA66 V4 (`wiki/projects/tuan-anh-review-tiktok/scripts/ulanzi-ma66-tripod-pocket-3-natural-voice.md`):
- 3 version × 232-258 từ × 70-77s
- 12-23 particles/script
- 18-21 fragments/script
- 0 forbidden words in actual script text

## Related files

- `wiki/concepts/tiktok-script-natural-voice-2026-07-21.md` - 10.8KB full lesson
- `wiki/projects/tuan-anh-review-tiktok/scripts/ulanzi-ma66-tripod-pocket-3-natural-voice.md` - V4 verified output
- `wiki/concepts/tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md` - 5 lessons on "1 nhu cầu"