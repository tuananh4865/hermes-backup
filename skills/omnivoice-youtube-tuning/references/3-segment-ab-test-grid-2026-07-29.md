>---
title: 3-Segment A/B Test Grid — Black Hole Pilot
created: 2026-07-29
type: reference
tags: [voice, omnivoice, ab-test, youtube]
---

# 3-Segment A/B Test Grid (2026-07-29)

8 config variants tested on the same 3 fixed segments (001, 027, 080 of the black-hole pilot). User's audio verdict recorded for each.

## Test segments

- **001:** Hook (Hồ đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ)
- **027:** Mid-script descriptive (Đây là nghịch lý nhìn rất đẹp trên phim)
- **080:** Late-script (Khoảng trống bằng chứng là nơi khoa học bắt đầu làm việc)

Each variant generated → WAV → concat → MP3 192k → user listened.

## A/B grid

| # | layer_penalty | position_temp | pad_duration | fade_duration | speed | Verdict (audio) |
|---|---|---|---|---|---|---|
| A | 5.0 (default) | 5.0 (default) | 0.1 | 0.1 | 0.95 | ngắt quãng, đầu câu cắt "ờ" |
| B | 1.0 | 3.0 | 0.1 | 0.1 | 0.90 | mượt hơn, vẫn cắt head/tail |
| C | 2.0 | 3.5 | 0.1 | 0.1 | 0.90 | OK, vẫn hơi ngắt |
| D | 1.5 | 3.5 | 0.1 | 0.0 | 0.90 | mượt hơn, head/tail đầy đủ |
| E | 1.5 | 3.5 | 0.2 | 0.0 | 0.90 | nghỉ rõ giữa câu |
| F | 1.5 | 3.5 | 0.15 | 0.0 | 0.90 | cân bằng nhất ← **WINNER** |
| G | 1.5 | 3.7 | 0.2 | 0.0 | 0.90 | vẫn OK, F tốt hơn |
| H | 2.0 | 3.5 | 0.2 | 0.1 | 0.90 | ngắt lại |

## Winner: Variant F

**Final config used for the 12:24 full take:**

```python
OmniVoiceGenerationConfig(
    pad_duration=0.15,
    fade_duration=0.0,
    denoise=True,
    layer_penalty_factor=1.5,
    position_temperature=3.5,
)
# call site
model.generate(text=full_script, language="vi", voice_clone_prompt=prompt,
               generation_config=gc, speed=0.90)
```

**User verdict:** "Bản số 3 oke" (referring to the 0.90 speed take).

## Why this config works (post-hoc analysis)

- **`layer_penalty=1.5`** — middle ground between 1.0 (over-merging, jerky in some cases) and 2.0+ (more segmentation). 1.5 keeps multi-syllable words flowing without over-smoothing.
- **`position_temperature=3.5`** — slightly above 3.0 to add enough prosody variation for long narration. 3.7 also OK but 3.5 was user's pick.
- **`pad=0.15`** — covers the model's warmup trim (~10s envelope) without sounding robotic. 0.1 left some head/tail bite; 0.2 added dead pause.
- **`fade=0`** — voice has no fade; only video audio should fade.
- **`speed=0.90`** — Vietnamese natural pace; 0.95 felt "hơi nhanh" to user.

## Negative results worth remembering

1. **A (default all):** FAIL — confirms why we're here.
2. **B (low layer, 0.1 pad):** partial — prosody OK but head/tail bite.
3. **E (pad 0.2):** acceptable but 0.15 was tighter.
4. **G (position 3.7):** tied with F; user picked F.
5. **H (fade 0.1):** re-introduces the "mờ" head/tail; F wins.

## Why 3-segment sample matters

- 1 segment: can't tell if it's representative.
- 3 segments (early / mid / late script): catches warmup bias at start, end-of-chunk break, and narrative pacing.
- >5 segments: wastes time; user hasn't approved the config yet.

## Speed sensitivity

- `speed=0.95` default: too fast for Vietnamese narration (user verdict 29/07).
- `speed=0.90`: just right.
- `speed=0.85`: a bit too slow, but if 0.90 still feels fast to user, drop to 0.85.

## When to redo this grid

- New voice clone (different `.pt`).
- New content type (e.g. dialogue vs narration).
- Model upgrade.
- User flags prosody regression in a future session.
