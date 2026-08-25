---
name: omnivoice-youtube-tuning
description: "YouTube voiceover tuning for OmniVoice, 5min+ videos."
---

# OmniVoice YouTube Tuning (class-level)

**Verified:** 29/07/2026, hố đen pilot 3032 words / 12:24 audio, single take, user-approved "Bản số 3 oke".
**Hardware:** Mac M-series (MPS), Python 3.11, torch 2.8.0.
**Ref voice:** `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt` (ref_rms=0.1100).

---

## 1. Hard Rules (FIRST-CLASS, vĩnh viễn)

1. **ZERO emotion/non-verbal tags** in input text. Tags (`[surprise-*]`, `[amazement-*]`, `[question-*]`, `[confirmation-*]`, `[laughter]`, `[sigh]`) can produce filler vocalizations "ựm, ờ, à, ồ, ờm, ừm" that Whisper transcription silently misses. User verbatim 29/07: *"Loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phèn các emotional tag có thể tạo ra các từ đó nữa"*.
2. **No post-speed-up.** Speed control goes through `model.generate(speed=...)` only. Never apply `ffmpeg atempo > 1.0` after generate.
3. **Single-prompt full take** for any YouTube voiceover >5 minutes. Generate the whole script in one `model.generate()` call. Chunking always produces seam clipping.
4. **3-câu small-sample A/B test before scaling** any config change. Pick 3 fixed sample segments (e.g. 001, 027, 080). Send MP3 to user. Wait for explicit approval. Then full render.
5. **Background job** must use `notify_on_complete=True`. User expects auto ping on completion, not silent.
6. **Always explain each param the user asks about** (position_temperature, layer_penalty_factor, pad_duration, fade_duration, speed, denoise). User asks conceptual questions; answer with 1 paragraph + impact table.

---

## 2. Verified Config (29/07, single 12:24 take)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.15,         # 150ms — covers head/tail trim without sounding dead
    fade_duration=0.0,         # NO fade on voice
    denoise=True,              # MANDATORY — prevents ref text leak
    layer_penalty_factor=1.5,  # 1.0-2.0 sweet spot
    position_temperature=3.5,  # 3.5-3.7 sweet spot
)
# Plus at call site:
model.generate(text=full_script, language="vi", voice_clone_prompt=prompt,
               generation_config=gc, speed=0.90)
```

### Config parameters explained (for user Q&A)

| Param | Default | Verified | Effect (user-friendly) |
|---|---|---|---|
| `pad_duration` | 0.1 | 0.15-0.20 | Khoảng silence model chèn ở đầu/cuối từng đoạn. Che chỗ model nuốt phoneme đầu/cuối. >0.3 nghe robotic. |
| `fade_duration` | 0.1 | 0.0 | Fade in/out mượt ở 2 mép. Voice KHÔNG cần, set 0. Audio gốc của video thì vẫn fade được. |
| `layer_penalty_factor` | 5.0 | 1.0-2.0 | Cao = model phạt khác biệt giữa layer → ngắt quãng. Thấp = layer nối mượt. 1.5 sweet spot cho narration. |
| `position_temperature` | 5.0 | 3.0-3.7 | Nhiệt độ sampling. Cao = lên xuống thái quá. Thấp = phẳng. 3.5 tự nhiên cho Việt. |
| `denoise` | True | True | Prepend `<\|denoise\|>` token; chặn ref text leak. **Always True.** |
| `speed` | 1.0 | 0.85-0.90 | 0.90 = tiếng Việt đời thường. 0.85 nếu 0.90 vẫn nhanh. |

### A/B grid tested 29/07 (3-segment tests on 001/027/080)

| Variant | L | P | pad | fade | speed | User verdict (audio) |
|---|---|---|---|---|---|---|
| Default (5/5) | 5.0 | 5.0 | 0.1 | 0.1 | 0.95 | ngắt quãng, đầu câu cắt "ờ" |
| Test 1 | 1.0 | 3.0 | 0.1 | 0.1 | 0.90 | vẫn ngắt nhẹ, head/tail cắt |
| Test 2 (2.0/3.5/0.1/0.1/0.90) | 2.0 | 3.5 | 0.1 | 0.1 | 0.90 | OK, vẫn hơi ngắt |
| Test 3 (1.5/3.5/0.1/0/0.90) | 1.5 | 3.5 | 0.1 | 0.0 | 0.90 | mượt hơn |
| Test 4 (1.5/3.5/0.2/0/0.90) | 1.5 | 3.5 | 0.2 | 0.0 | 0.90 | nghỉ rõ giữa câu |
| Test 5 (1.5/3.5/0.15/0/0.90) | 1.5 | 3.5 | 0.15 | 0.0 | 0.90 | cân bằng nhất |
| Test 6 (1.5/3.7/0.2/0/0.90) | 1.5 | 3.7 | 0.2 | 0.0 | 0.90 | vẫn OK |
| **FINAL (Test 5)** | **1.5** | **3.5** | **0.15** | **0** | **0.90** | **"Bản số 3 oke"** |

→ Sweet spot cho Vietnamese narration dài: **layer 1.5, position 3.5, pad 0.15, fade 0, speed 0.90**.

---

## 3. Why Single-Prompt Works (root cause: model warmup)

**OmniVoice has a ~10s warmup that trims edge phonemes.** If each chunk is shorter than the warmup, first and last phonemes vanish. A 12-minute single take has warmup, body, and tail all inside one model run → no edge truncation.

**Pad-after fails:** `ffmpeg anullsrc concat` adds silence BETWEEN chunks but cannot restore phonemes the model already trimmed. User verdict 29/07: *"Pad làm khoảng lặng bị im lặng hoàn toàn! Câu đầu và câu cuối vẫn bị khuyết mất một phần của câu!!!"*.

**Chunk-and-join with longer segments:** A/B tested 29/07 with 5-sentence chunks (~40s each). Chunk 2 and 3 still had head/tail bite because OmniVoice warmup runs on every call.

---

## 4. Workflow: 3-câu small test → full render

```bash
# 1. Build 3-line JSONL with fixed sample segments
cat > /tmp/test-3short.jsonl <<'EOF'
{"id":"001","language":"vi","text":"<segment-1-text>"}
{"id":"027","language":"vi","text":"<segment-2-text>"}
{"id":"080","language":"vi","text":"<segment-3-text>"}
EOF

# 2. Generate
python3 ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt \
  --jsonl /tmp/test-3short.jsonl --output-dir /tmp/test-X

# 3. Concat + encode to 192k MP3
ffmpeg -y -f concat -safe 0 -i <(for f in /tmp/test-X/0*.wav; do printf "file '%s'\n" "$f"; done) \
  -ar 44100 -ac 1 -c:a libmp3lame -b:a 192k /tmp/test-X.mp3

# 4. Run Whisper for sanity
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/test-X-qa /tmp/test-X.mp3

# 5. Send MP3 to user. WAIT for explicit approval. Then full render.
```

For full render, use `--text "$(cat full.jsonl | python3 -c 'import sys,json; print(json.load(sys.stdin)["text"])')\"` to avoid shell quoting issues.

---

## 5. Background job pattern

```bash
terminal(background=True, notify_on_complete=True, command="<long render>")
```

User expects auto ping on completion. When async event arrives, do QA + deliver.

---

## 6. Verification (Whisper is NOT a verifier)

1. **ffprobe:** check codec, sample rate, duration.
2. **volumedetect:** check max (>-10dB), mean.
3. **silencedetect:** check for unexpected silence >10s between chunks (single-take case = no gap).
4. **Whisper transcript:** sanity check for ref-leak ("hãy subscribe", "đăng ký kênh", "Tuấn Anh đây"). **NOT** a verifier for prosody/quality.
5. **Always verify by ear** on the final MP3 before declaring done.

---

## 7. Anti-Patterns

1. Chèn emotion tag vào input — phải văng.
2. Scale config change lên full render — phải test 3 câu trước.
3. `ffmpeg anullsrc concat` cho YouTube voice — workaround, không fix.
4. `atempo > 1.0` sau khi generate.
5. Chunk script thành N đoạn nhỏ cho video >5 phút — single prompt mới clean.
6. Bỏ background `notify_on_complete=True` cho long render.
7. Chạy Whisper rồi tự báo OK — Whisper misses filler, cần verify bằng tai.
8. **Tự thông báo "xong" mà không gửi file MP3 vào Telegram** — user phải nghe được ngay. Luôn kèm `MEDIA:/path/to.mp3` ở turn báo xong.
9. **Đặt câu hỏi để biết test từ A/B nào khi user đã chỉ rõ config** — chạy luôn config đó, đừng hỏi lại. User trả lời rồi thì test thôi.

---

## 8. Reference Files

- `references/smooth-config-deep-dive.md` — prosody tuning details (when to bump layer vs position vs pad).
- `references/zero-tag-policy-evidence.md` — A/B test transcripts proving every tag risks filler.
- `references/single-prompt-evidence.md` — full 12:24 take transcript + duration math.
- `references/background-job-pattern.md` — notify_on_complete usage with process handles.
- `references/3-segment-ab-test-grid-2026-07-29.md` — full A/B table for 8 variants on 3 fixed segments with audio verify.
