---
name: omnivoice-voice-clone
description: "Voice clone + TTS generation với OmniVoice 0.2.1 trên Mac M-series MPS. Trigger khi anh nói clone giọng anh, OmniVoice TTS, tạo voice prompt, tạo audio TikTok từ text, hoặc cần synthetic voice cho content video. Skill đã verify end-to-end: prompt save/load, batch generate, MPS workarounds, ref leak fix, amplitude bug fix, 13 non-verbal emotion tags."
---

# OmniVoice Voice Clone — Hermes Skill

**Use when:** anh cần clone giọng thật của mình (hoặc người khác) từ audio 5-10s → tạo audio mới từ text bất kỳ. Đặc biệt phù hợp content TikTok Việt cần authentic voice.

**Repo:** https://github.com/k2-fsa/OmniVoice
**Version verified:** 0.2.1 (master, 2026-07)
**Verified hardware:** Mac M-series (MPS), Python 3.11, torch 2.8.0
**Verified by:** Tuấn Anh Review channel, 2026-07-23

---

## Quick Start (3 phút)

```bash
# 1. Setup (one-time)
cd /Volumes/Storage-1/Hermes/scratch/omnivoice-test
source .venv/bin/activate   # uv venv đã có sẵn từ session trước

# 2. Save voice prompt (one-time, 5-10s ref audio)
python3 scripts/save_voice_prompt.py save <ref_audio.wav> "<ref text 1 câu ngắn>" \
  /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt

# 3. Generate (mỗi lần dùng — instant, không cần re-encode)
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt \
  --text "Câu tiếng Việt cần synthesize" \
  --output out.wav
```

**Kết quả:** 24kHz mono WAV, 4-15s duration tùy text, voice giống ref audio.

---

## When to use this skill

| Scenario | Use this skill? |
|---|---|
| TikTok content cần voice thật (không phải Microsoft TTS) | ✅ **YES** |
| Generate voice multilingual (Anh, Trung, Tây Ban Nha) với giọng Việt làm anchor | ✅ **YES** |
| Voice design (không cần ref audio, describe attributes) | ✅ YES (xem Section 5) |
| Auto voice (không cần ref, không design) | ✅ YES (đơn giản nhất) |
| **TikTok content cần emotion/cảm xúc** (laugh, surprise, question) | ✅ **YES** — 13 non-verbal tags, xem Recipe 11 |
| 1 clip TikTok tiếng Việt bình thường, không cần authentic | ❌ Dùng `edge-tts NamMinh` thay (nhanh hơn 50x) |
| Realtime streaming TTS | ❌ OmniVoice không support |
| Production scale 1000+ file/giờ | ❌ Tốc độ MPS không đủ |

---

## 📚 LESSONS EMBEDDED FROM SESSION 2026-07-23

### L1: VoiceClonePrompt = Save Once, Reuse Forever (USER CORRECTION)

**Push-back:** "Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu"

**Rule:** Luôn dùng `model.create_voice_clone_prompt()` → `prompt.save()` → `VoiceClonePrompt.load()` thay vì pass `ref_audio`/`ref_text` mỗi lần.

```python
# ❌ SAI (re-encode mỗi lần - chậm)
audio = model.generate(text="...", ref_audio="ref.wav", ref_text="...")

# ✅ ĐÚNG (save 1 lần, load mãi)
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt")
audio = model.generate(text="...", voice_clone_prompt=prompt)
# → 5x speedup: 11s/file vs 18s/file
```

### L2: Test Variants Trước Khi Conclude (USER CORRECTION)

**Push-back:** "Tốt rồi! Nhưng Lúc em prompt omnivoice có vấn đề gì đó... chỉ cần fix prompt lại không inject câu đó vào nữa thôi!"

**Context:** Em default vào "Whisper post-trim" hack (workaround) thay vì test 4 variants ref_text để tìm prompt-level fix.

**Rule:** Khi user nói "fix prompt/input, không workaround output" → test A/B/C/D variants of input trước khi conclude. 4 phút test saves hours debugging.

**Applied:** Tested 4 variants ref_text (full/1 sent/2 sent/minimal) → 2 câu = BEST, không cần trim hack.

### L3: 13 Non-Verbal Tags = Free Emotion (USER DISCOVERY)

**Insight:** "Anh thấy có phần Non-verbal & Pronunciation Control khá hay cộng thêm các key feature để thêm cảm xúc cho giọng đọc khiến cho giọng đọc giống người hơn!"

**Em đã verify:** 10/10 emotion variants PASS với prompt GOOJODOQ. Peak tăng rõ rệt (-2 to -3 dB vs -3.7 dB baseline).

**Rule:** Khi tạo TikTok content, LUÔN consider thêm 1-2 non-verbal tags:
- HOOK → `[surprise-oh]` (loudest, ngạc nhiên)
- PROBLEM → `[sigh]` (chạm pain point)
- SOLUTION → `[question-ah]` (kết thúc lên cao, engagement)
- CTA → `[confirmation-en]` (call action)

→ Xem `references/04-recipes.md` Recipe 11 cho full list 13 tags + TikTok emotion recipe.

### L4: PHẢI Đọc Hết README + Follow Tất Cả Links (USER CORRECTION)

**Push-back:** "Đọc hết phần readme của repo chưa?"

**Context:** Em fetch README.md + beyond, NHƯNG skip `docs/community-projects.md` vì em focus vào inference. User phát hiện và correct.

**Rule:** Khi build skill từ GitHub repo:
1. Phase 1.5: Enumerate TẤT CẢ links trong README
2. Skip = explicit decision (ghi lý do trong SKILL.md "Beyond" section)
3. KHÔNG silent skip — user luôn đánh giá completeness

**Anti-pattern:** "Em fetch README là đủ" — sai, README là gateway, mỗi link có thể chứa info quan trọng (community ecosystem, training pipeline, etc.).

### L5: Concat Fade PHẢI NHẸ — 30ms (USER PREFERENCE)

**Push-back:** "Khi em ghép batch lại với nhau thì để fadeout nhẹ thôi 30ms thôi"

**Context:** Em default dùng `afade=t=in:out:st=...:d=0.03` (fade cả in và out). User explicit: **fadeout nhẹ 30ms thôi**, không fade in/out đối xứng.

**Rule (BẮT BUỘC khi concat N file TTS):**
1. **KHÔNG dùng `afade` đối xứng** — tạo 60ms silent gap (Pitfall #6)
2. **Dùng `concat_segments.py` của skill** — đã verify trim 100ms lead/trail + 30ms fade out only
3. **Manual override chỉ khi cần**: dùng `atrim` để bỏ padding + `afade=t=out:st=X:d=0.03` (fade out only)

**Anti-pattern (đã catch trong session):** `ffmpeg afade=t=in:st=0:d=0.03,afade=t=out:st=...:d=0.03` → 60ms silent mỗi boundary → Whisper hallucinate từ.

**Verified output (Mac M-series, 5 segments GOOJODOQ):**
- Peak audio tại boundary: 0.03-0.11 (có voice chạy qua)
- Silent gap: 30ms (chỉ fade out, không có gap)
- vs `afade in+out` cũ: peak = 0.0000 (silent), gap = 60ms

### L6: Test Variants A/B/C/D Trước Khi Conclude (RECURRING PATTERN)

**Trigger:** Bất kỳ khi nào gặp vấn đề KHÔNG HIỂU root cause.

**Rule:** Test ≥3 variants trước khi conclude root cause. 4 phút test saves hours debugging.

**Applied 3 lần trong session:**
- ref_text: full/1-sent/2-sent/minimal → 2-sent = BEST (Pitfall #3)
- concat method: afade/acrossfade/fade-out-only/trim-first → trim+30ms-out = BEST (Pitfall #6)
- amplitude: raw/amp×2.5/amp×11 → amp×11 (ref_rms=0.11) = BEST (Pitfall #2)

---

## Production workflow (đã verify)

### Phase 1: Setup environment (one-time, ~5 phút)

```bash
# 1. Tạo venv Python 3.11+ (Python 3.9 system KO dùng được, PEP 668 block)
uv venv .venv --python python3.11
source .venv/bin/activate

# 2. Install torch + omnivoice
uv pip install torch==2.8.0 torchaudio==2.8.0
uv pip install git+https://github.com/k2-fsa/OmniVoice.git

# 3. Verify
.venv/bin/python -c "
import torch, omnivoice
from importlib.metadata import version
print('torch:', torch.__version__, 'mps:', torch.backends.mps.is_available())
print('omnivoice:', version('omnivoice'))
"
# Expect: torch 2.8.0 mps: True  omnivoice 0.2.1
```

**Apple Silicon setup cũng cần:**
- macOS 14+ (Sonoma) hoặc 15+ (Sequoia)
- Xcode Command Line Tools (`xcode-select --install`)
- ~5GB disk cho model + venv

### Phase 2: Prepare reference audio

**Requirements:**
- Format: WAV/MP3/M4A/OGG, bất kỳ sample rate nào
- Duration: **5-10 giây sweet spot** (3s tối thiểu, 20s degradation)
- Content: voice thật, **không nhạc nền**, **không tiếng ồn**
- **Critical: voice đó PHẢI LÀ VOICE NGƯỜI THẬT** — KHÔNG phải AI TTS outro hook

**Extract 5-10s từ raw video:**
```bash
# Từ DJI Pocket 3 hoặc iPhone
ffmpeg -y -ss 10 -i raw_video.mov -t 5 -ar 16000 -ac 1 -c:a pcm_s16le ref_5s.wav

# Từ voice message Telegram
ffmpeg -y -i voice.ogg -t 5 -ar 16000 -ac 1 -c:a pcm_s16le ref_5s.wav

# Test verify: Whisper transcribe
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir ./verify/ ref_5s.wav
cat verify/ref_5s.txt
```

**Nếu ref audio có ref_rms < 0.1 → amplify trước khi save prompt** (xem Pitfall #2):
```bash
.venv/bin/python -c "
import soundfile as sf, numpy as np
audio, sr = sf.read('ref_5s.wav')
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
print(f'Current ref_rms: {ref_rms:.4f}')
if ref_rms < 0.1:
    audio_amp = audio * (0.11 / ref_rms)
    sf.write('ref_5s_amp.wav', audio_amp, sr)
    print(f'Amplified → ref_5s_amp.wav (new ref_rms: 0.11)')
"
```

### Phase 3: Save voice prompt (one-time, 5s encode)

```bash
# QUAN TRỌNG: ref_text phải NGẮN (~100 chars, 1 câu đầu)
# KHÔNG dùng full transcript — sẽ leak câu cuối vào output (Pitfall #3)
python3 scripts/save_voice_prompt.py save \
  ref_5s_amp.wav \
  "Câu đầu tiên trong ref audio, khoảng 100 ký tự." \
  /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v1.pt
```

Output: file .pt ~10KB, chứa `ref_audio_tokens` + `ref_text` + `ref_rms`. **Save 1 lần, dùng mãi mãi.**

### Phase 4: Generate (instant, ~12s/file)

```bash
# Single text
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v1.pt \
  --text "Câu bất kỳ cần synthesize bằng giọng clone" \
  --output out.wav

# Batch từ JSONL
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v1.pt \
  --jsonl 5_texts.jsonl \
  --output-dir batch_results/
```

**Output:** 24kHz mono WAV, 4-15s duration, voice giống ref.

### Phase 5: Verify (bắt buộc — đã catch 3 bugs trong session này)

```bash
# Verify 1: volumedetect (peak > -10 dB = không silent)
ffmpeg -i out.wav -af "volumedetect" -vn -f null - 2>&1 | grep max_volume

# Verify 2: Whisper transcript (clean content, không ref leak)
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/verify/ out.wav
cat /tmp/verify/out.txt
# Phải chỉ chứa text đã generate, KHÔNG có câu ref audio
```

### Phase 6: Concat (nếu N file) — DÙNG `concat_segments.py` CÓ SẴN

**QUAN TRỌNG — anh yêu cầu fadeout 30ms nhẹ.** Skill đã verify tự động trim 100ms padding + apply đúng 30ms fade out only (xem Pitfall #6):

```bash
python3 scripts/concat_segments.py \
  --inputs-dir batch_results/ \
  --output tiktok_FINAL.wav
# Default: trim 100ms lead/trail + 30ms fade out only
```

**KHÔNG dùng `ffmpeg -filter_complex afade=t=in:out` thủ công** — sẽ tạo 60ms silent gap (vì `pad_duration=0.1` mặc định của OmniVoice). Xem `references/00-pitfalls.md` Pitfall #6.

---

## User preferences (Tuấn Anh — hard rules từ session 23/07)

| # | Rule | Source |
|---|---|---|
| 1 | **NO workaround, ROOT CAUSE fix** | Anh correct 3 lần trong 1 session (Whisper trim → prompt fix, re-import → save prompt, trim+afade → disable padding). KHI anh correct cách tiếp cận → KHÔNG defend current approach, chuyển sang fix từ gốc |
| 2 | **Concat fade CHỈ 30ms** (verbatim: "fadeout nhẹ thôi 30ms thôi") | Session 23/07 — không fade in, không workarounds |
| 3 | **Voice authentic** (giọng thật) khi content TikTok cần real human voice | Built skill này để thay edge-tts NamMinh |
| 4 | **HERMES-ONLY-FOLDER**: outputs ở `/Volumes/Storage-1/Hermes/voice-prompts/`, KHÔNG ở `~/.hermes/` | Existing Hermes rule |
| 5 | **Skip = explicit decision in SKILL.md** | Anh correct 23/07 khi em silent skip `docs/community-projects.md` |

Xem full chi tiết: `references/05-user-corrections-2026-07-23.md`

---

## Reference docs (linked)

- `references/00-pitfalls.md` — 5 bug đã catch (đọc TRƯỚC khi dùng)
- `references/01-api-surface.md` — Full Python API + dataclasses + parameters
- `references/02-cli-commands.md` — 3 CLI entry points với full flags
- `references/03-known-issues.md` — GitHub issues + workarounds
- `references/04-recipes.md` — Common tasks (concat, mix với Pocket 3, emotion, etc.)
- `references/05-user-corrections-2026-07-23.md` — 5 user push-backs trong session này + rule tổng quát

## Scripts (production-ready)

- `scripts/save_voice_prompt.py` — Encode ref audio → save .pt
- `scripts/generate_voice.py` — Load .pt → generate 1 hoặc N audio
- `scripts/verify_audio.py` — 3-layer verify (file valid + amplitude + content)
- `scripts/concat_segments.py` — Concat N file với 30ms afade (PITFALL #81)
- `scripts/test_emotion.py` — Test 10 emotion variants với 13 non-verbal tags
- `scripts/with_venv.sh` — Wrapper auto-activate OmniVoice venv

## CRITICAL PITFALLS (đã verify)

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 1 | **MPS batch bug** (GitHub issue #8) | Batch ≥5 text dài khác nhau → 4/5 file silent (-20 dB) | Sequential 1-by-1 trong cùng process |
| 2 | **ref_rms < 0.1 amplitude bug** | Output giảm 1/6 volume | Amplify ref audio trước khi save prompt |
| 3 | **ref_text quá dài → ref leak** | Output luôn leak câu cuối ref_text vào đầu/giữa | ref_text = 1 câu ngắn ~100 chars |
| 4 | **TikTok CDN có thể trả audio khác expected** | Download clip review → chỉ có voice outro "subscribe" | Verify Whisper transcript trước khi dùng |
| 5 | **HiggsAudioV2Tokenizer không support MPS** | Model crash khi load trên MPS | Code tự fallback `device_map="cpu"` cho tokenizer (verified trong code) |
| 6 | **Concat gap (100ms lead/trail silent)** | Clip TikTok có gap 100-200ms giữa các segment → Whisper hallucinate | Trim 100ms trước, rồi 30ms fade out only (xem PITFALL #6) |

**Xem full detail:** `references/00-pitfalls.md`

---

## Performance benchmarks (Mac M-series, ref 5-10s)

| Operation | Time | RAM peak |
|---|---|---|
| Setup venv + install | ~3 phút | - |
| Model load (cold, 1st time) | ~1:30 | 12GB |
| Model load (warm, 2nd+) | ~2-3s | 12GB |
| Save voice prompt (one-time) | ~5s | 12GB |
| Generate 1 file (~10s audio) | ~12-15s | 12GB |
| **Generate 5 files** (sequential, cùng prompt) | **~55-70s** | 12GB |
| Concat 5 files (ffmpeg filter_complex) | <1s | - |
| Whisper verify 1 file (large-v3) | ~20s | 4GB |

**So sánh edge-tts NamMinh:**
- 1 file: edge-tts ~1s vs OmniVoice ~12-15s (chậm hơn 12x)
- Voice quality: edge-tts Microsoft voice vs OmniVoice authentic voice
- Use case: edge-tts cho 90% content, OmniVoice cho clip hero/brand

---

## File organization (recommended)

```
/Volumes/Storage-1/Hermes/voice-prompts/    # ← voice prompts (.pt) lưu ở đây
  ├── tuan_anh_v1.pt
  ├── tuan_anh_v2_soft.pt
  └── reviewer_A.pt

/Volumes/Storage-1/Hermes/scratch/voice-clone/   # ← outputs, scripts, test
  ├── ref_audio/         # ref audio files
  ├── batch_results/      # generated batches
  ├── final_clips/       # concat clips TikTok
  └── logs/

~/.hermes/skills/multimedia/omnivoice-voice-clone/
  ├── SKILL.md           # this file
  ├── scripts/
  │   ├── save_voice_prompt.py
  │   ├── generate_voice.py
  │   ├── verify_audio.py
  │   ├── concat_segments.py
  │   ├── test_emotion.py
  │   └── with_venv.sh
  └── references/
      ├── 00-pitfalls.md
      ├── 01-api-surface.md
      ├── 02-cli-commands.md
      ├── 03-known-issues.md
      └── 04-recipes.md
```

**HERMES-ONLY-FOLDER rule (l19):** voice prompts ở `/Volumes/Storage-1/Hermes/voice-prompts/`, KHÔNG ở `~/.hermes/` hoặc `/Users/tuananh4865/`.

---

## Cross-references với skills khác

- `tiktok-voice-clone` workflow (TBD) — dùng output OmniVoice làm voice track TikTok
- `media/tiktok-video-editor` — concat voice với video Pocket 3 (ffmpeg)
- `pocket-3` workflow — extract ref audio từ raw clip

---

## Lessons saved (wiki)

- L29: Dùng voice gốc khi build motion graphic từ raw clip (extend: clone voice từ ref audio)
- L25-OMNIVOICE: VoiceClonePrompt save 1 lần, dùng mãi mãi (5x speedup vs re-encode)
- PITFALL-OMNIVOICE-MPS-BATCH: Sequential 1-by-1, KHÔNG dùng `omnivoice-infer-batch` trên MPS
- PITFALL-OMNIVOICE-REF-LEAK: ref_text ngắn = 1 câu, KHÔNG full transcript
- PITFALL-OMNIVOICE-AMPLITUDE: ref_rms >= 0.1 để bypass bug line 898-903

---

## Beyond inference (what's NOT in this skill)

Skill này focus vào **voice clone + inference**. Các phần khác của repo (training/eval) chưa cover:

### Training (`examples/`)
- `run_emilia.sh` (3.8KB) — Pre-train trên Emilia dataset (100k hours multilingual)
- `run_finetune.sh` (2.5KB) — Finetune trên custom data
- `run_eval.sh` (9.4KB) — WER/MOS/speaker-similarity evaluation

→ Skill này KHÔNG cover training. Nếu anh cần fine-tune model trên voice riêng, mở skill mới `omnivoice-finetune` (TODO).

### Docs chưa fetch (liên kết từ README)
- `docs/languages.md` — nhưng `omnivoice/utils/lang_map.py` đã có 600+ entries từ source
- `docs/data_preparation.md` — JSONL format cho training
- `docs/evaluation.md` — WER calculation
- `docs/training.md` — full training pipeline
- `docs/OmniVoice.ipynb` — Colab notebook

### Community projects (16 third-party)

| Project | Use case | Relevant cho anh? |
|---|---|---|
| [ComfyUI-OmniVoice-TTS](https://github.com/Saganaki22/ComfyUI-OmniVoice-TTS) | ComfyUI node | ❌ Em không dùng ComfyUI |
| [vLLM-Omni](https://github.com/vllm-project/vllm-omni) | Fast serving (omni-modal) | ⚠️ Có thể scale nếu cần > 10 clips/giờ |
| [MLX-Audio](https://github.com/Blaizzy/mlx-audio) | Apple Silicon MLX backend | ⚠️ Có thể nhanh hơn MPS |
| [OmniVoice-MLX](https://github.com/ailuntx/OmniVoice-MLX) | MLX backend (anh tuấn) | ✅ MLX inference — đáng test nếu MPS chậm |
| [pyVideoTrans](https://github.com/jianchang512/pyvideotrans) | Video translation tool | ✅ **Có thể dùng** cho TikTok Vi→En dubbing |
| [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS) | Realtime streaming | ❌ OmniVoice không support realtime |
| [TTS-WebUI](https://github.com/rsxdalv/TTS-WebUI) | Gradio web UI multi-model | ⚠️ Alternative cho omnivoice-demo |
| [omnivoice-server](https://github.com/maemreyo/omnivoice-server) | OpenAI-compatible HTTP API | ✅ **Quan tâm** — production serving |
| [omnivoice-rs](https://github.com/FerrisMind/omnivoice-rs) | Rust + Candle GPU | ❌ Không cần Rust |
| [LA Studio](https://github.com/dduongtrandai/LA-Studio) | Desktop AI audio workstation | ⚠️ Alternative UI cho voice clone |

**Top 3 đáng test:**
1. **OmniVoice-MLX** — Apple Silicon MLX có thể nhanh hơn MPS 2-3x (verify khi cần scale)
2. **omnivoice-server** — production serving qua HTTP API (cleaner integration cho pipeline)
3. **pyVideoTrans** — TikTok Vi→En dubbing pipeline (extends workflow hiện tại)

---

## Future enhancements (roadmap)

- [ ] Auto-detect ref audio từ Pocket 3 raw clip + auto-extract 5s sweet spot
- [ ] Concat multi-segment với 30ms afade helper
- [ ] Voice design mode (gender/age/pitch) without ref audio
- [ ] Cache model globally để skip load 1:30 mỗi session
- [ ] Cross-lingual clone test (ref Vi → text En)
- [ ] **Emotion tuning** — Test which non-verbal tag combination works best for TikTok engagement (A/B test với audience)
- [ ] **omnivoice-server** integration — Replace sequential generation với HTTP API khi scale > 10 clips/giờ
- [ ] **OmniVoice-MLX** benchmark — So sánh MPS vs MLX speed khi cần scale
- [ ] **pyVideoTrans** integration — TikTok Vi→En dubbing pipeline
- [ ] **Auto emotion injection** — Heuristic: HOOK auto-thêm `[surprise-oh]`, CTA auto-thêm `[confirmation-en]`
