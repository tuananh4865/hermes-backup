# YouTube Long-Form Narration Smooth Config (2026-07-29)

## Session context

Anh asked for a 20-minute Vietnamese YouTube voiceover about black holes, originally using the existing `tuan_anh_5s_1sent_amp.pt` voice clone. Pilot produced:

- **Evidence dossier:** `wiki/projects/vuive-channel-research/research/black-holes-evidence-dossier-2026-07-29.md`
- **Script V1:** `wiki/projects/vuive-channel-research/scripts/pilot-01-tat-ca-dieu-ky-la-ve-ho-den-20-phut-v1.md` (3,082 spoken words, 18–22 min target)

After PATCH adversarial verify loop (PARTIAL_PASS → 2x FAIL → PASS), user asked to generate voice with OmniVoice. This file captures the actual OmniVoice config lessons learned.

## Progressive config iterations (what worked, what didn't)

| Iteration | Config | Result |
|---|---|---|
| v1 (default) | `pad=0`, `fade=0`, `denoise=True`, no layer/pos overrides, `speed=0.95` | Generated, but voice cut mid-word at start/end of each 85-segment chunk (head/tail clipping). |
| **Silence-padded concat** | head 400 ms + tail 600 ms silence per segment | Failed — Whisper transcript still missed chunk 1 first word (`Vì ồ` instead of `Video`) AND first words of chunks 2/3. Silencing outside the model cannot recover lost audio. |
| **Grouped chunks** | 5 paragraphs joined per chunk, `…` at end of each grouped chunk (except final) | Chunks 1 and 6 clean. Chunk 16 missing first word (`Châu` instead of `Câu`). Root cause: chunks too short at the seam. |
| **`A` — single-shot full script (one entry)** | Joined all 85 paragraphs into one JSONL entry, 3,032 words | BEST result so far. Whisper transcript 182/182 lines, all sentence heads/tails intact. Duration 12:24 at 24 kHz, peak −1.4 dB. |
| **`A` + `speed=0.90`** | Single-shot, but slowed from 0.95 → 0.90 | Accepted by anh (“đang rất tốt, chỉ hơi nhanh” became chậm lại). |
| **`A` + slow config test** | `layer_penalty=2.0`, `position_temperature=3.5`, `pad=0.1`, `fade=0.1`, `speed=0.90` | Final test pending user feedback at session close. |

## Verified recipe (2026-07-29 baseline)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.1,
    fade_duration=0.1,
    denoise=True,
    layer_penalty_factor=2.0,
    position_temperature=3.5,
)
```

And:

```python
audio = model.generate(
    text=full_script_concat_text,            # ONE entry, ≥3000 words OK
    language="vi",
    voice_clone_prompt=prompt,               # .pt file with ref_text set once
    generation_config=gc,
    speed=0.90,
)[0]
audio = trim_trailing_silence(audio, model.sampling_rate)
```

## Hard rules (do NOT regress)

1. **NEVER use atempo / post-speed-up** for YouTube narration. Anh explicitly rejected 1.2x: *"nói hơi nhanh thôi"*. Use OmniVoice `speed` parameter directly.
2. **NEVER split long script into many short chunks.** Each chunk boundary loses ~1 word from the head and tail. Either render the entire script as ONE entry, or group into ≥5 paragraphs/chunk with `…` at intermediate seams.
3. **NEVER pad external silence to fix head/tail clipping.** Padding out of ffmpeg cannot recover audio the model did not synthesize.
4. **NEVER insert emotion/non-verbal tags unless anh explicitly requests one and an A/B test proves it safe.** Tags like `[confirmation-en]`, `[question-ah]` inject filler (ờ/à/ồ) at chunk heads that Whisper may miss but anh's ear will hear.
5. **ALWAYS run 3-sample mini-test (`001`, a middle, near-end) before full render.** A/B prosody changes must be tested on small inputs; the difference is audible but rarely visible in transcript diff.
6. **ALWAYS verify with Whisper transcript + ffprobe duration + volumedetect peak before sending.** User’s ear is the final QA; transcript is the proxy.

## Why the slow config tested in this session

Anh asked what each prosody parameter does:

- `layer_penalty_factor` (default 5.0): controls layer agreement → high = jerky/segmented prosody, low = smooth link. **2.0** is a middle ground (was 1.0 before, anh said it was OK but trial 2.0 for variation).
- `position_temperature` (default 5.0): controls prosodic randomness → high = too varied, low = flat. **3.5** is mid-high (was 3.0 before).
- `pad_duration`/`fade_duration` (default 0.1): tails of model output. Was 0 before to avoid concat gaps; in this long-narration use case 0.1 was tested as the seed for natural sentence-ending breaths.

Anh’s verdict after speed=0.90 file (still on layer=1.0, position=3.0, pad=0): *"Mọi thứ đang rất tốt chỉ là nói hơi nhanh thôi"*. anh then directly asked for layer=2.0, position=3.5, pad=0.1, fade=0.1 as the next test variant. **Test result for this variant was not captured before session end.** → document and re-verify on next session.

## File version outputs available

- `HO_DEN_OMNI_FULL_RAW.wav` + `_192K.mp3` — speed=0.95, layer=1.0, pad=0, fade=0 (rejected as too fast)
- `HO_DEN_OMNI_FULL_0.90_RAW.wav` + `_192K.mp3` — speed=0.90, layer=1.0, pad=0, fade=0 (accepted baseline)
- `HO_DEN_TEST_L2P3.5_*` — speed=0.90, layer=2.0, position=3.5, pad=0.1, fade=0.1 (test result not captured this session — re-test first thing next session)

All files live at:
`/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/`
