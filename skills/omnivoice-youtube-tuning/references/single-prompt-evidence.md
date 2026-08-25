# Single-Prompt vs Chunked: Evidence 29/07

## Why single-prompt is mandatory for >5min YouTube voiceover

User tested 4 approaches 29/07 on hố đen pilot (3032 words, 10 chapter). Only the **single-prompt full take** produced clean audio without head/tail bite.

### Test 1: 85 chunked segments → FAIL
- Generated 85 short chunks, concat with `ffmpeg -f concat`.
- Output: every segment dropped the first 100-300ms phoneme.
- Whisper transcript: "Hồ đen có lẽ là vật thể bị hiểu sai..." → "Hồ đen có lẽ..." (drop "H" first char in some).
- User verdict: *"Các đoạn chuyển bị cắt rất sát ở đầu câu và cuối câu"*.

### Test 2: 85 chunks + 400ms head + 600ms tail padding → FAIL
- Padded each chunk's head/tail with `ffmpeg anullsrc`.
- Output: model still trimmed edge phonemes, silence just replaced them.
- User verdict: *"Pad làm khoảng lặng bị im lặng hoàn toàn! Câu đầu và câu cuối vẫn bị khuyết mất một phần của câu!!!"*.
- Conclusion: padding cannot restore model-trimmed phonemes.

### Test 3: 17 chunks of 5 sentences each → FAIL
- Grouped 5 sentences per chunk (~40s each), concat with `ffmpeg -f concat`.
- Output: chunk 1 and chunk 17 clean, chunks 2-16 still had head bite.
- Reason: each `model.generate()` call has ~10s warmup that trims edges.

### Test 4: Single-prompt full take → PASS
- Generated entire 3032 words in ONE `model.generate()` call.
- Output: 12:24.32 audio, no head/tail bite, all 10 chapters intact.
- Whisper transcript: 182 lines, full content captured, only 1 hallucination ("tiỉnh" instead of "tỉ" — Whisper limit, not voice).
- User verdict: *"Bản số 3 oke đó"*.

## Why this happens (root cause)

OmniVoice generation has a model warmup phase at the START of every `model.generate()` call. During warmup (~10s), the model:
- Initializes decoder state
- Processes the prompt conditioning
- Aligns to ref voice characteristics

Phonemes generated during warmup get trimmed because the model is still settling. For chunks shorter than 10s, the ENTIRE chunk is consumed by warmup → 100% trimmed.

For a 12-minute single take, warmup happens ONCE at the very start, then the model runs continuously for the whole 12 minutes. Only the very first 1-2s gets trimmed (which is why we use `pad_duration=0.15-0.20` to cover it).

## Lesson

**For any YouTube voiceover >5min, ALWAYS use single-prompt full take.** The natural pause structure comes from:
- Punctuation in the input text (`,`, `.`, `;`, `?`).
- Trailing `…` for chapter-end pauses.
- The model's own prosody decisions.

**Do NOT chase gapless by removing pauses.** User explicitly rejected gapless narration: *"Giữa các câu không có ngắt nghỉ mà nói liền cảm giác rất khó chịu!"*.

## File outputs from this session

- `/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/HO_DEN_OMNI_FULL_192K.mp3` (12:24, full script, speed=0.95)
- `/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/HO_DEN_OMNI_FULL_0.90_192K.mp3` (13:04, full script, speed=0.90)
- `/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/HO_DEN_OMNI_NO_FILLER_1.2X_192K.mp3` (DEPRECATED — has filler + atempo)
