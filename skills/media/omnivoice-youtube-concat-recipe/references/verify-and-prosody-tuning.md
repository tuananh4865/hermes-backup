# Verify and prosody tuning — 2026-07-29 session lessons

## Verify tools (do NOT trust Whisper transcript alone)

Whisper hallucinates continuations across padded silence, so a transcript
that looks "clean" can hide a clipped head/tail or duplicated sentence. Always
verify with built-in audio tools:

```bash
# 1) ffprobe: format + stream sanity
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,sample_rate,channels -of json out.mp3

# 2) volume: peak + mean (catches silent-output regressions)
ffmpeg -i out.mp3 -af volumedetect -vn -f null - 2>&1 | egrep 'mean_volume|max_volume'

# 3) silence count (catches missing padding or total gap-out)
ffmpeg -hide_banner -i out.mp3 -af silencedetect=noise=-40dB:d=0.2 -f null - 2>&1 \
  | grep -c silence_end     # expect N-1 for N segments + chapter ends
```

Manual: play back the first 2 s and the last 2 s of every segment. Catches
"`hay` → `ay`" head-clipping that Whisper silently drops.

## Why padded-silence concat fails at segment boundaries

Empirically each Omni segment opens with the model mid-phoneme because there
is no leading audio context for the warm-up. Padded silence added **outside**
the segment cannot fix this — the model has already started the segment
without a leading phoneme.

Symptoms:
- Whisper transcript starts mid-word: "ay", "ờm", "à" instead of the first
  real word.
- Worse for short segments (<10 s).

Two real fixes (verified end-to-end 2026-07-29):

1. **Pad inside the text with `…` at the end of each chunk** so Omni sees a
   natural continuation instead of a hard cut. Loses one phoneme at the
   chunk boundary but keeps the head intact.
2. **Render the full script in ONE `model.generate()` call** when the
   script fits in a single prompt (~10–15k chars). This is the
   cleanest fix and is what the user ultimately chose for the
   black-hole pilot.

## Prosody param reference (OmniVoice 0.2.1)

| Param | Default | Verified 22-min YouTube | Effect |
|---|---|---|---|
| `layer_penalty_factor` | 5.0 | 1.5 | Lower → layer decoder disagreement allowed → smoother prosody. 5.0 = clipped, jerky. |
| `position_temperature` | 5.0 | 3.5 | Lower → less random variation. 3.0–3.5 is the sweet spot for natural narration. |
| `pad_duration` | 0.1 | 0.15 | Silence added by model at both ends of every generated segment. |
| `fade_duration` | 0.1 | 0.0 | No fade in/out (fade adds audible click artifacts). |
| `denoise` | True | True | Prepends `<|denoise|>` token to block ref-text echo. Never disable. |
| `speed` | 1.0 | 0.90 | Pass via `model.generate(speed=0.90)`. Slows speech without changing pitch. |

A/B test grid the user actually iterated through (in order):

1. L1.0/P3.0/pad0/fade0/speed0.90 — clean prosody but "hơi nhanh"
2. Same with **speed=0.90** — clean
3. L1.0/P3.0/speed0.90/one-shot full script 12:24 — clean
4. L1.0/P3.0/speed0.90/one-shot full script at speed 0.90 — 13:04 — clean
5. L2.0/P3.5/pad0.1/fade0.1/speed0.90 — slight feel change
6. L1.5/P3.5/pad0.1/fade0/speed0.90 — better
7. L1.5/P3.5/pad0.2/fade0/speed0.90 — even better
8. L1.5/P3.5/pad0.15/fade0/speed0.90 — **final chosen**

## Hard rule: "1 prompt when it fits"

If the full script is ≤ ~15k characters and ≤ ~20 minutes, render it as a
single `model.generate()` call. Multi-segment concat is acceptable only when
the script exceeds the model's prompt window.

`generate_voice.py` is the canonical entry point:

```bash
python3 ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt \
  --text "$(cat full-script.jsonl | python3 -c 'import sys,json; print(json.load(sys.stdin)["text"])')" \
  --output full_voice.wav
```

## Why Whisper can disagree on identical text

Cross-segment with padded silence, Whisper sometimes "merges" two segments
("...Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ. **và** nghịch
lý nhìn rất đẹp trên phim") even though the actual audio has silence. The
model hallucinates a conjunctive. Always verify with `silencedetect` count,
not transcript.

## What to never try again

- **atempo 1.2 on YouTube voice** — compresses speech so segments butt into
  each other; user explicitly rejected. ANH's verbatim: "Voice youtube
  không cần tăng speed! Giữa các câu không có ngắt nghỉ mà nói liền cảm giác
  rất khó chịu!"
- **External silence pad via ffmpeg concat** — does NOT recover clipped heads.
  Use single-prompt render or `…` in text.
- **Surprise/amazement/laughter/confirmation/question tags for fill-in
  emotion** — they introduce filler vocalizations Whisper can't hear.
  Default to zero tags unless the user explicitly requests a tested-safe one.
