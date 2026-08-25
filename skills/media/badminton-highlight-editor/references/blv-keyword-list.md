# BLV Keyword List (Tiếng Việt) cho Highlight Detection

> **Dùng cho Layer 3 — Whisper BLV cross-verify.** Chỉ apply khi clip CÓ BLV nói tiếng Việt. Skip hoàn toàn nếu clip chỉ có crowd + tiếng cầu.

## 🔥 Tier 1 — Hot keywords (score boost cao nhất)

Khi BLV nói 1 trong các từ này + RMS > -25 dB → RALLY ĐỈNH (score 9-10), KEEP bắt buộc.

```python
BLV_TIER1_HOT = [
    "vào",           # "VÀOOOOO!" — universal BLV scream
    "đỉnh",          # "ĐỈNH QUÁ!" — peak excitement
    "hay quá",       # "HAY QUÁ!" — reaction praise
    "quá đỉnh",      # intensified version
    "tuyệt vời",     # formal praise
    "không thể tin",  # disbelief
    "thật không thể", # disbelief variant
    "ngoạn mục",     # spectacular (formal)
    "xuất sắc",      # excellent
    "thần thánh",    # godly (informal)
    "cháy",          # fire (gen-z slang for "amazing")
    "xỉu",           # fainting (gen-z slang for "too good")
    "quá hay",       # alternative praise
    "đỉnh cao",      # peak performance
    "đỉnh thật",     # genuinely peak
]
```

## ⚡ Tier 2 — Energetic keywords (score boost trung bình)

Khi BLV nói 1 trong các từ này + RMS > -25 dB → RALLY HAY (score 7-8), KEEP.

```python
BLV_TIER2_ENERGETIC = [
    "đẹp",           # "ĐẸP QUÁ!" — beautiful
    "nhanh",         # "NHANH QUÁ!" — fast
    "mạnh",          # "MẠNH QUÁ!" — powerful
    "hay",           # general praise
    "tốt",           # good
    "giỏi",          # skilled
    "hay lắm",       # pretty good
    "được",          # "ĐƯỢC!" — approving
    "hay quá đi",    # intensifier
    "đỉnh thật",     # really peak
    "đỉnh cao",      # peak
    "phải",          # "PHẢI!" — must (in context of praise)
    "wow",           # English borrowing
    "oh",            # surprise exclamation
    "ồ",             # soft surprise
]
```

## 🎯 Tier 3 — Negative/sad keywords (BỎ nếu match)

Khi BLV nói 1 trong các từ này → rally không hay (lỗi, hỏng, etc.), BỎ.

```python
BLV_TIER3_NEGATIVE = [
    "tiếc",          # "TIẾC QUÁ!" — pity
    "hỏng",          # broken
    "lỗi",           # mistake
    "sai",           # wrong
    "trượt",         # miss
    "hụt",           # short
    "không được",    # not good
    "đáng tiếc",     # regret
    "tiếc nuối",     # full regret
    "out",           # out of bounds
    "việt vị",       # Vietnamese for "fault"
]
```

## 🎬 Tier 4 — Setup keywords (transitional, BỎ)

Khi BLV đang setup tình huống (không phải rally), BỎ.

```python
BLV_TIER4_SETUP = [
    "bây giờ",       # "now" (setup)
    "tiếp theo",     # "next" (transitional)
    "xem",           # "let's see" (setup)
    "đợi",           # "wait" (setup)
    "chuẩn bị",      # "prepare" (setup)
]
```

## 🎵 Cross-modality scoring formula

```python
def rally_score(rms_db, yamnet_applause, blv_text):
    """
    Score từ 0-10 dựa trên 3 signals.
    Trả về None nếu rally không đáng giữ.
    """
    # Base: RMS alone
    if rms_db < -25:
        return None  # Too quiet, skip

    base_score = min((rms_db - (-25)) / (-9 - (-25)) * 5, 5)  # 0-5 points
    # RMS -25dB = 0 pts, RMS -9dB = 5 pts

    # Layer 2: YAMNet applause
    if yamnet_applause >= 0.5:
        base_score += 2  # +2 for confirmed applause

    # Layer 3: BLV keyword
    blv_lower = blv_text.lower()
    if any(kw in blv_lower for kw in BLV_TIER1_HOT):
        base_score += 3  # +3 for hot BLV keyword
    elif any(kw in blv_lower for kw in BLV_TIER2_ENERGETIC):
        base_score += 1.5  # +1.5 for energetic BLV
    elif any(kw in blv_lower for kw in BLV_TIER3_NEGATIVE):
        return None  # Negative, skip
    elif any(kw in blv_lower for kw in BLV_TIER4_SETUP):
        base_score -= 1  # Setup, reduce

    return min(base_score, 10)
```

## 🚫 Pitfall #N: Whisper hallucinate BLV keywords

Whisper thỉnh thoảng hallucinate "BLV đang nói gì đó" trên audio silence → false positive.

**Fix:** Khi detect BLV keyword, **BẮT BUỘC verify RMS > -25 dB tại timestamp đó**. Nếu RMS thấp → BLV hallucinate → BỎ.

```python
# Anti-hallucinate check
if blv_keyword_detected and rms_at_that_time < -30:
    print(f"⚠️ BLV keyword at {t}s but RMS too low → hallucinate, skip")
    continue
```

## 📝 Notes từ session 2026-07-09

- **Test case:** `https://youtu.be/n2884oDI824` (635s clip) — **KHÔNG có BLV** → toàn bộ Whisper output là "Hãy đăng ký kênh" hallucinate
- Lesson: **Detect BLV presence first.** Nếu transcript có < 5 dòng non-hallucinate → skip Layer 3 hoàn toàn.
- Anti-hallucinate flags khi clip không BLV: `--condition-on-previous-text False --no-speech-threshold 0.6`