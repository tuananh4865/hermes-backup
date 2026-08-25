---
title: BWF Indonesia Open Final 2026 - EN Whisper Hallucinate Test
created: 2026-07-12
type: session-test
tags: [bwf, en-hallucinate, ceremony-filter, rms-threshold-tuning]
---

# Session 2026-07-12 — POLYTRON Indonesia Open 2026 Final

> **Test case #2** cho skill `badminton-highlight-editor` v1.2.0.
> **Phát hiện chính:** Whisper EN hallucinate MASSIVELY trên BWF TV crowd audio — pattern MỚI không có trong skill cũ.

## 📋 Source Video

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=TCG9oKtmaQE |
| Channel | BWF TV (official) |
| Match | POLYTRON Indonesia Open 2026 - Men's Singles FINAL |
| Players | Jonatan Christie (INA) [5] vs Victor Lai (CAN) |
| Result | Victor Lai thắng 21-19, 21-8 (39 phút) |
| Duration | 58:05 (3485s) |
| File size | 257 MB |

## 🆕 Lessons captured (embedded in SKILL.md)

### Lesson #8 (NEW): EN Whisper Hallucinate "Wow"/"That's the"/"Long of the back line"

**Triệu chứng:** Whisper medium-mlx EN với `--language en` trên BWF TV clip:
- 1000+ dòng "Wow." repeated
- 800+ dòng "That's the." repeated
- 200+ dòng "Long of the back line." repeated
- Tất cả hallucinate ở audio có crowd noise (applause, cheer)

**Root cause:** Whisper model EN overfit pattern "Wow" / "That's the" / filler EN khi audio có crowd reaction. Cả với `--condition-on-previous-text False --no-speech-threshold 0.6` vẫn hallucinate.

**Fix:** Phase 0 detect `hallucinate_en` pattern:
```bash
hallucinate_en=$(grep -icE "^Wow\.|^That's the\.$|^Long of" audio.srt)
if [ "$hallucinate_en" -gt 100 ]; then
  echo "⚠️ Whisper EN heavily hallucinated — SKIP Phase 4 BLV scoring"
fi
```

→ Vẫn chạy Phase 1 (Whisper) nhưng KHÔNG dùng text cho Phase 4. Dùng RMS làm ground truth duy nhất.

### Lesson #9 (NEW): Post-Merge Ceremony Filter (Phase 4.6)

**Triệu chứng:** Rally 90s+ sau Phase 4.5 extend thường là ending + ceremony (music bed + interview + trophy lift), KHÔNG phải rally.

**Real case:** Indonesia Open Final, spike dài nhất = 90s ở 1791-1881s = toàn bộ post-match ceremony (Victor Lai trophy lift + interview + BWF official speech).

**Fix:** Phase 4.6 mới — filter `awk '$4 < 60'`:
```bash
awk -F'\t' '$4 < 60 {print}' top_rallies.txt > keep_rallies_final.txt
```

Threshold 60s an toàn: rally cầu lông thật hiếm khi > 60s (BLV "31-shot rally" là max historical).

## 📊 Tuning rule cho BWF TV clips (12/07 empirical)

| Threshold | Rallies detected | Use case |
|---|---|---|
| `-25 dB` | 6 rallies (93s) | Conservative — chắc chắn rally (recommended default) |
| `-27 dB` | 9-10 rallies (~120-130s) | Catch thêm middle-game (anh muốn nhiều hơn) |
| `-30 dB` | 15+ rallies | Quá nhiều false positive từ serve sounds + BLV small speech |

→ **Default `-25 dB`**, giảm `-27 dB` nếu anh muốn nhiều hơn.

## 🎯 Output

```
File: /Volumes/Storage-1/Tiktok-Tuan-Anh/badminton-highlights/TCG9oKtmaQE_V1_highlight_6rallies.mp4
Duration: 93.000s
Size: 28.1 MB
Spec: H.264 1280×720 + AAC 44100Hz stereo
Rallies: 6 (112-136s, 193-208s, 2881-2895s, 2988-3001s, 3097-3111s, 3114-3127s)
```

## 📂 Distribution (có thể improve lần sau)

| Phase | Time range | Rallies |
|---|---|---|
| Opening / intro | 0-300s | 2 |
| Game 1 mid | 300-1500s | 0 ⚠️ MISSING |
| Game 1-2 transition | 1500-2200s | 0 |
| Game 2 mid-late | 2200-3400s | 4 |
| Ending + ceremony | 3400-3485s | 0 (filtered) |

→ **Gap:** Game 1 mid (5-25 phút) không catch rally nào. Khả năng do threshold -25 dB quá conservative cho vùng này (có thể crowd yếu hơn giữa game). Fix: chạy lại với `-27 dB` để catch thêm middle-game rallies.

## 🔍 RMS evidence (anh có thể tự verify)

```python
# Tất cả 6 rallies đều có peak RMS -22 đến -24 dB (= crowd reaction đỉnh điểm)
# Rally 1 (90s, 1791-1881s): peak -22.2, avg -24.7 (quá đều → ceremony, đã filter)
# 6 rallies kept: peak -22.0 đến -24.1, avg -25.3 đến -27.6
```

## Related

- SKILL.md → Phase 4.6 (post-merge ceremony filter)
- SKILL.md → Pitfall #8 (EN hallucinate)
- SKILL.md → Pitfall #9 (ceremony filter)
- SKILL.md → Threshold table (BWF row updated with -25/-27 dB choice)
- [[wiki/raw/articles/badminton-indonesia-open-final-2026.md]] — Full session recap
