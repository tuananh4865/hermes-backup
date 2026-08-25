---
name: omnivoice-youtube-concat-recipe
title: OmniVoice YouTube Concat Recipe
created: 2026-07-29
description: Ship multi-segment OmniVoice with silence pads.
type: recipe
tags: [voice, tts, omnivoice, video, qa]
confidence: high
---

# OmniVoice YouTube Concat Recipe

Use when shipping multi-segment OmniVoice narration (YouTube, audiobook, podcast).

## Hard rules (Tuấn Anh preferences, 2026-07-29)

1. **Default ZERO emotion tags.** Any tag can inject filler audio (`ựm, ờ, à, ồ, ờm, ừm`) that Whisper silently drops.
2. **NEVER post-speed-up YouTube voiceovers.** `atempo=1.2` etc. compresses speech so adjacent segments butt into each other.
3. **Per-segment WAV padded head + tail with silence** so bursts don't clip at concat boundaries:
   - `head_padding_ms = 400`
   - `tail_padding_ms = 400` in-chapter / `600` chapter-end
   - `inter_segment_gap_ms = 280`
4. **Verify with audio tools, not Whisper alone.** Whisper hallucinates text continuations.
5. **Background jobs always expose `process_id` + `notify_on_complete=true`.**

## Confirmed silent-safe voice prompt

`/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt` — ref_rms 0.1100, ref_text ngắn 1 câu, 0 tags verified.

## Concat recipe (verified 29/07 on black-hole pilot)

```bash
# 1) silence padding files
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.40 -c:a pcm_s16le silence-400ms.wav
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.60 -c:a pcm_s16le silence-600ms.wav

# 2) pad each segment
ffmpeg -y -i silence-400ms.wav -i 001.wav -i silence-400ms.wav \
  -filter_complex '[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]' \
  -map '[out]' -ar 24000 -ac 1 -c:a pcm_s16le 001.wav
# chapter-end files: substitute silence-600ms.wav as [2:a]

# 3) concat in numeric order
cat > concat.txt <<EOF
file '001.wav'
file '002.wav'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -ar 44100 -ac 1 \
  -c:a libmp3lame -b:a 192k final.mp3

# 4) verify (NO atempo step)
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,sample_rate,channels -of json final.mp3
ffmpeg -hide_banner -i final.mp3 -af silencedetect=noise=-40dB:d=0.2 -f null - 2>&1 \
  | grep -c silence_end     # expect > 60 for 85 segments
```

## History

- **29/07 18:00 — black-hole pilot**: `tuan_anh_5s_1sent_amp.pt`, 85 segments, 0 tags, head=400ms, tail=400/600ms. Output `HO_DEN_YOUTUBE_ORIGINAL_SPEED_NATURAL_PAUSES_192K.mp3` (12:45, 192kbps mono). Verified 98 silence events, peak -1.3dB, no filler. **Shipped.**
- **29/07 evening — second pass with single-prompt render**: user noted prosody was OK but speed was "hơi nhanh". A/B iterated on `layer_penalty_factor`, `position_temperature`, `pad_duration`, `fade_duration`, `speed`. Final config `layer=1.5, position=3.5, pad=0.15, fade=0, denoise=True, speed=0.90` rendered as a single `model.generate()` over the full 13655-char / 3032-word script. Output `HO_DEN_OMNI_FULL_0.90_192K.mp3` (13:05, 192kbps mono, peak -0.7dB, mean -19.3dB). User accepted. See `references/verify-and-prosody-tuning.md` for the full A/B grid and the "why padded silence fails at boundaries" lesson.

→ For per-segment concat, prefer the head/tail pad recipe above. For scripts that fit in a single prompt (~10–15k chars), prefer the single-shot render (verified clean, no clipped heads, no filler).
