# 02 — CLI Commands

3 CLI entry points (verified v0.2.1). All scripts auto-installed by `pip install omnivoice`.

---

## `omnivoice-infer` — Single item

```bash
omnivoice-infer --model k2-fsa/OmniVoice \
  --text "Hello world" \
  --output out.wav
```

### Full flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--model` | str | k2-fsa/OmniVoice | HF repo or local path |
| `--text` | str | **required** | Text to synthesize |
| `--output` | str | **required** | Output WAV path |
| `--ref_audio` | str | None | Ref audio path (voice clone) |
| `--ref_text` | str | None | Ref audio transcript |
| `--instruct` | str | None | Voice design attrs (no ref) |
| `--language` | str | None | Language code or name (600+) |
| `--num_step` | int | 32 | Diffusion steps (16 = fast) |
| `--guidance_scale` | float | 2.0 | CFG scale |
| `--speed` | float | 1.0 | >1 faster, <1 slower |
| `--duration` | float | None | Fixed seconds (overrides speed) |
| `--t_shift` | float | 0.1 | Time shift |
| `--denoise` | bool | true | Add `<\|denoise\|>` token |
| `--postprocess_output` | bool | true | Remove trailing silence |
| `--layer_penalty_factor` | float | 5.0 | Codebook layer penalty |
| `--position_temperature` | float | 5.0 | Position sampling T |
| `--class_temperature` | float | 0.0 | Class token sampling T (0=greedy) |
| `--device` | str | auto | cuda / mps / xpu / cpu |

### Examples

```bash
# Voice cloning
omnivoice-infer --text "Test" --ref_audio ref.wav --ref_text "Transcript" --output out.wav

# Voice design (no ref audio)
omnivoice-infer --text "Test" --instruct "female, british accent" --output out.wav

# Auto voice
omnivoice-infer --text "Test" --output out.wav
```

---

## `omnivoice-infer-batch` — JSONL multi-item

```bash
omnivoice-infer-batch --model k2-fsa/OmniVoice \
  --test_list inputs.jsonl \
  --res_dir outputs/
```

### JSONL schema (mỗi line 1 sample)

```json
{
  "id": "sample_001",          // required, output filename
  "text": "Hello world",       // required
  "ref_audio": "/path/ref.wav", // optional (clone mode)
  "ref_text": "Transcript",    // optional (omit → auto-ASR)
  "instruct": "male, british", // optional (design mode)
  "language_id": "en",         // optional ISO 639-3
  "duration": 10.0,            // optional seconds
  "speed": 1.0                 // optional
}
```

### Full flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--model` | str | k2-fsa/OmniVoice | HF repo or local path |
| `--test_list` | str | **required** | JSONL input file |
| `--res_dir` | str | **required** | Output directory |
| `--num_step` | int | 32 | |
| `--guidance_scale` | float | 2.0 | |
| `--t_shift` | float | 0.1 | |
| `--nj_per_gpu` | int | 1 | Workers per GPU |
| `--audio_chunk_duration` | float | 15.0 | Chunk duration (s) |
| `--audio_chunk_threshold` | float | 30.0 | Threshold to chunk |
| `--batch_duration` | float | 1000.0 | Max total duration per batch |
| `--batch_size` | int | 0 | Fixed batch size (0=auto) |
| `--warmup` | int | 0 | Warmup runs before real inference |
| `--preprocess_prompt` | bool | true | |
| `--postprocess_output` | bool | true | |
| `--layer_penalty_factor` | float | 5.0 | |
| `--position_temperature` | float | 5.0 | |
| `--class_temperature` | float | 0.0 | |
| `--denoise` | bool | true | |
| `--lang_id` | str | None | Default for missing fields |

### ⚠️ BUG (PITFALL #1)

**`omnivoice-infer-batch` với batch_size ≥5 + texts dài khác nhau** trên MPS sẽ cho output silent. Workaround: dùng `scripts/generate_voice.py` của skill này (sequential 1-by-1).

---

## `omnivoice-demo` — Gradio web UI

```bash
omnivoice-demo --model k2-fsa/OmniVoice --port 7860
```

| Flag | Type | Default | Description |
|---|---|---|---|
| `--model` | str | k2-fsa/OmniVoice | |
| `--device` | str | auto | |
| `--ip` | str | 0.0.0.0 | Server IP |
| `--port` | int | 7860 | Server port |
| `--root-path` | str | None | Reverse proxy path |
| `--share` | flag | false | Create public link |
| `--no-asr` | flag | false | Skip Whisper load (faster startup) |
| `--asr-model` | str | openai/whisper-large-v3-turbo | HF repo for ASR |

**UI features:**
- Voice Clone tab: upload ref audio + text + generate
- Voice Design tab: pick gender/age/pitch/accent/dialect
- Generation Settings accordion: speed, duration, num_step, etc.

**Best for:** Quick interactive testing, NOT production (CLI scripts faster).

---

## Decision matrix: CLI nào dùng khi nào?

| Use case | Tool |
|---|---|
| 1 file, có sẵn ref | `omnivoice-infer` |
| 1 file, muốn test design | `omnivoice-infer` (với --instruct) |
| 1 file, có prompt .pt saved | `python3 scripts/generate_voice.py` |
| N files, sequential, ổn định | `python3 scripts/generate_voice.py --jsonl` |
| N files, GPU multi-process (Linux only) | `omnivoice-infer-batch` (NOT on MPS) |
| Quick interactive test | `omnivoice-demo` |

**Recommendation cho Mac M-series:** LUÔN dùng `scripts/generate_voice.py` (sequential 1-by-1) thay vì `omnivoice-infer-batch`.
