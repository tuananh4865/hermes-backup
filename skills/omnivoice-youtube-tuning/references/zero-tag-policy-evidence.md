># Zero Emotion Tag Policy: Evidence 29/07

## Why ZERO emotion/non-verbal tags in input text

User tested every emotion tag in OmniVoice 29/07. Every single one (including `[question-ah]`, `[confirmation-en]`) produced filler vocalizations that Whisper transcription silently missed.

### Test grid (3-câu small sample, 001 + 027 + 080)

| Tag | Transcript start | Filler? |
|---|---|---|
| (none) | "Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ" | ✅ CLEAN |
| `[question-ah]` | "ờ… Hố đen có lẽ là..." | ⚠️ "ờ" filler |
| `[confirmation-en]` | "ờ… Hố đen..." | ⚠️ "ờ" filler |
| `[surprise-oh]` | "ô… Hố đen..." | ⚠️ "ô" filler |
| `[laughter]` | "ha… Hố đen..." | ⚠️ "ha" filler |
| `[sigh]` | "ừ… Hố đen..." | ⚠️ "ừ" filler |

User verbatim 29/07: *"Loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phép chèn các emotional tag có thể tạo ra các từ đó nữa"*.

## Why Whisper misses these fillers

Whisper transcription is text-to-text alignment. It maps audio frames to text tokens. Filler vocalizations are:

1. **Low-amplitude** — model adds them as prosody markers, not as distinct phonemes
2. **Between phoneme boundaries** — Whisper's alignment skips them
3. **Familiar sounds** — Whisper may transcribe "ờ" as silence or skip entirely

So even if the audio contains "ờ" at the start, Whisper transcript shows clean text. This is why:
- Whisper transcript PASS ≠ voice quality PASS
- User's ear is the only reliable verifier
- Auto-trim trailing silence does NOT remove leading filler (it only trims end)

## Why this matters more for YouTube than TikTok

- TikTok clips are 30-60s, mostly single-shot. A few "ờ" are tolerable.
- YouTube videos are 10-20min. Filler at the start of EVERY chapter compounds into "speaking style is too casual / unprepared" perception.

For YouTube, professional narration requires:
- ZERO filler at sentence/chapter boundaries
- Clean prosody that comes from punctuation + model natural flow
- Trust the model's default output, not emotion tag injection

## Production rule (vĩnh viễn)

**Default OmniVoice text input: ZERO emotion/non-verbal tags.**

Override only if:
1. User explicitly requests a specific tag.
2. A/B test on 3-câu sample proves it safe (no filler in transcript + no filler in ear test).
3. Document the tag + result in `references/zero-tag-policy-evidence.md`.

## Skill impact

This rule has been baked into the existing `omnivoice-voice-clone` skill SKILL.md (Rule section, 29/07 patch). The new class-level skill `omnivoive-youtube-tuning` carries the same rule + evidence.
