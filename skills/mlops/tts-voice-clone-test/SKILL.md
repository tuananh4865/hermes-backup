---
name: tts-voice-clone-test
description: Test, benchmark, và so sánh 3rd-party TTS voice-clone models trên Mac M-series. Cover OmniVoice, CosyVoice, F5-TTS, ChatTTS, GPT-SoVITS, OpenVoice. Use khi user nói test model TTS mới, clone giọng bằng X, so sánh X với edge-tts, benchmark voice clone trên Mac, hoặc muốn evaluate pretrained voice-clone model chạy local. Workflow 6 bước pre-flight, ref audio prep, Whisper transcribe, install model, generate clone, compare baseline.
---

# TTS Voice-Clone Test

Class-level umbrella skill để **test và benchmark 3rd-party TTS/voice-clone models** chạy local trên Mac M-series (MPS) hoặc GPU NVIDIA (CUDA).

Distinct from `voice-setup` (production TTS cho Telegram = Edge TTS) và `third-party-tool-install` (install CLI). Skill này cover: **evaluating một pretrained voice-clone model** trước khi integrate vào workflow content.

## Khi nào dùng

- User hỏi test model TTS mới, clone giọng bằng X, so sánh OmniVoice/CosyVoice/F5-TTS với edge-tts
- User muốn evaluate: zero-shot voice cloning, voice design, multilingual TTS, RTF benchmark, chất lượng giọng
- User cần decision matrix: model nào phù hợp cho use case (TikTok voice, podcast, dubbing)

## Khi KHÔNG dùng

- User chỉ muốn generate voice bằng Edge TTS cho Telegram reply → dùng `voice-setup`
- User muốn fine-tune custom voice model từ scratch → dùng `fine-tuning-with-trl` hoặc `axolotl`
- User muốn research model architecture (paper, benchmarks) mà KHÔNG cần test trên Mac → dùng `ml-model-comparison-report`

## Workflow 6 bước (BẮT BUỘC theo thứ tự)

### Step 1 — Pre-flight check (5 phút)

Verify trước khi bắt đầu:
```bash
# Python
python3 --version  # ≥3.10 cho hầu hết TTS mới

# torch + device
python3 -c "import torch; print('torch', torch.__version__); print('mps:', torch.backends.mps.is_available()); print('cuda:', torch.cuda.is_available())"

# Disk space (model thường 1-3GB)
df -h / | tail -1

# Chưa có cài đặt model
python3 -c "import <package>" 2>&1 | head -1
```

**Output báo cáo:** torch version, MPS/CUDA available, disk free, model installed Y/N.

### Step 2 — Nhận ref audio từ user (CLARIFY)

**KHÔNG TỰ PICK** raw clip từ Footages/. **Hỏi user cung cấp** vì:
- TTS cần audio CLEAN (không nhạc nền, không风扇 noise, không echo)
- User biết file nào đủ clean
- Pocket 3 raw hay có风扇 noise → clone quality giảm
- iPhone MOV đôi khi không đúng speaker intent

**4 options đưa cho user (verified 23/07 — anh prefer option 4):**
1. User auto-pick từ Footages/ (nếu user OK với quality có thể thấp)
2. User chỉ định path raw cụ thể
3. User pick từ iPhone MOV (audio thường cleaner hơn DJI)
4. **User cung cấp file audio thu sẵn (RECOMMENDED)** — clean voice, no noise, đúng speaker intent

**Real case 23/07:** Anh chọn option 4 cho OmniVoice test, cung cấp 17.08s Opus 48kHz qua Telegram voice bubble. Kết quả: 3/3 clone tests PASS với chất lượng tốt.

**Ref audio requirements:**
- Format: wav/mp3/m4a/ogg/voice bubble (em convert được hết)
- Duration: **3-10s recommended** (dưới 3s reject, trên 10s degradation)
- Quality: clean voice, không nhạc nền, không tiếng ồn xung quanh
- Source: thu bằng mic (preferred) > voice memo > Pocket 3 (có风扇) > iPhone MOV

### Step 3 — Pre-process ref audio (ffmpeg 1 lệnh)

MỌI TTS model cần ref audio ở format chuẩn:
- **Sample rate:** 16kHz hoặc 24kHz (tùy model, check docs)
- **Channels:** mono
- **Format:** WAV PCM 16-bit

```bash
# Universal recipe (check docs trước cho sample rate chính xác)
ffmpeg -y -i <user_input> -ar 16000 -ac 1 -c:a pcm_s16le ref.wav

# Verify
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 ref.wav
```

**Pitfall:** Một số model (OmniVoice) auto-load bằng `soundfile` — sample rate khác 16kHz sẽ silent-fail hoặc resample sai. **LUÔN check model docs** trước khi assume 16kHz.

### Step 4 — Whisper transcribe ref audio

```bash
# Default: large-v3 cho technical accuracy
whisper-transcribe ref.wav --output_dir . --output_format txt

# File output: ref.txt (chỉ text, không timestamp)
```

**Output:** `ref_text` (string) — chính xác transcript của ref audio. User cần raw output KHÔNG cleanup (theo RAW-OUTPUT-PREFERENCE).

**Edge case:** Whisper có thể sai với technical terms. Nếu model nói "Doroto" mà visual thấy "Dodoto" → cross-verify trước khi dùng.

### Step 5 — Install model (~5-15 phút)

**MẤT THỜI GIAN NHHẤT.** Bắt đầu install sớm nếu có thể parallel với step 3-4.

```bash
# General pattern (check model docs cho command chính xác)
pip install <package>                     # từ PyPI
# HOẶC
pip install git+https://github.com/<owner>/<repo>.git  # từ GitHub

# Verify import
python3 -c "import <package>; print('<package>', <package>.__version__)"
```

**Apple Silicon gotchas:**
- `pynini` no wheel → `conda install -c conda-forge pynini` (cho text normalization)
- `flash_attn` không có trên MPS → model auto-fallback SDPA (verify bằng test)
- `flex_attention` partial support trên MPS → single-GPU SDPA OK
- `tokenizers` Rust wheel OK cho M-series

**Disk watch:** Model download 1-3GB. Verify trước khi install:
```bash
df -h / | tail -1 | awk '{print $4}'  # phải còn ≥5GB
```

### Step 6 — Generate clone + verify (~2-5 phút)

```python
from <package> import <Model>
import soundfile as sf, torch

model = <Model>.from_pretrained(
    "<org>/<model>",
    device_map="mps",  # hoặc "cuda:0" / "xpu"
    dtype=torch.float16,
)

audio = model.generate(
    text="<test text 3-5s>",
    ref_audio="ref.wav",
    ref_text="<ref transcript>",
)

sf.write("out.wav", audio[0], model.sampling_rate)  # 24kHz cho OmniVoice
```

**Verify output:**
```bash
# File valid + đúng spec
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,duration -of csv=p=0 out.wav
# Expected: pcm_s16le, 24000, 1, ~3-5s

# Duration sanity
ffprobe -v error -show_entries format=duration -of csv=p=0 out.wav
```

### Step 7 — Compare với baseline (optional nhưng recommended)

So sánh với Edge TTS NamMinh (anh default):
```bash
# Generate baseline
edge-tts --voice vi-VN-NamMinhNeural --text "<same test text>" --write-media baseline.mp3
ffmpeg -y -i baseline.mp3 -ar 24000 -ac 1 baseline.wav  # same sample rate
```

**Decision matrix (cho anh review):**
| Aspect | Baseline (Edge TTS) | Model mới |
|---|---|---|
| Sample rate | 48kHz (24kHz sau resample) | 24kHz native |
| Voice quality | Robotic, clean | Clone giọng user? |
| Latency | 1-2s (API call) | Local inference |
| Multilingual | Limited (vi-VN only chính) | 600+ langs |
| Cost | Free | Free (chạy local) |
| Disk | 0 (API) | 1-3GB (model) |
| Setup | 1 pip install | 5-10 phút + 2GB download |

### Step 8 — Batch test (5+ texts cùng voice) — ⚠️ MANDATORY WORKAROUND

**⚠️ QUAN TRỌNG (verified 2026-07-23 17:00):** Dùng **IN-PROCESS SEQUENTIAL** 1-by-1, KHÔNG dùng `omnivoice-infer-batch` CLI cho batch 5+ texts dài khác nhau trên MPS. GitHub issue #8: padding rows trong `_generate_iterative` gây NaN attention trên MPS → 4/5 file output gần silent (peak -16.6dB thay vì 0dB). Chi tiết + 5-variant test matrix ở `references/omnivoice-recipe.md` § LESSON 2.

**Khi nào cần:** Content TikTok có cấu trúc HOOK→PROBLEM→SOLUTION→USP→CTA. Generate 5+ audio clips cùng voice, concat thành 1 clip hoàn chỉnh.

**⚠️ Pitfall `language_id` vs `--language`:** JSONL schema cần **ISO 639-3 code** (`"vi"`, `"en"`) — KHÔNG phải language name (`"Vietnamese"`, `"English"`). CLI `--language` thì accept cả name (auto-resolve) nhưng JSONL KHÔNG. Verify trước khi generate:
```python
from omnivoice.utils.lang_map import LANG_IDS
# LANG_IDS là set ISO codes — check "vi" in LANG_IDS (True)
# LANG_NAME_TO_ID dict — check "Vietnamese" → "vi"
```

**JSONL schema (1 line = 1 sample):**
```jsonl
{"id": "hook_01", "text": "...", "ref_audio": "ref_10s.wav", "ref_text": "...", "language_id": "vi"}
{"id": "problem_02", "text": "...", "ref_audio": "ref_10s.wav", "ref_text": "...", "language_id": "vi"}
```

**Code pattern (in-process sequential — bypass MPS bug):**
```python
import time, torch, soundfile as sf
from omnivoice.models.omnivoice import OmniVoice

print("Loading model..."); t0 = time.time()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
print(f"Loaded in {time.time()-t0:.1f}s")

# ref_text = 2 CÂU ĐẦU (sweet spot — đủ context, không leak)
ref_audio = "ref_10s.wav"
ref_text = "Xin chào đây là giọng đọc của Tuấn Anh. Tôi năm nay 30 tuổi đang thất nghiệp."

# Generate sequential 1-by-1
texts = [
    ("hook_01", "Các bạn ơi, hôm nay mình giới thiệu..."),
    ("problem_02", "Nhiều anh em phản hồi là..."),
    ("solution_03", "Chiếc máy hút bụi này..."),
    ("usp_04", "Điểm mình thích nhất là..."),
    ("cta_05", "Anh em nào thích thì bấm..."),
]
for sid, text in texts:
    audio = model.generate(text=text, language="vi",
                            ref_audio=ref_audio, ref_text=ref_text)[0]
    sf.write(f"output/{sid}.wav", audio, model.sampling_rate)
    print(f"  {sid}: dur={len(audio)/24000:.2f}s peak={float(abs(audio).max()):.4f}")
```

**Wall time:** 1:30 model load + N×18s generate. 5 file = 2:30 total.
**Output:** peak ~0.5 (gần baseline NamMinh -4.6dB), 24kHz mono, NO ref leak.

**RAM monitor pattern (BẮT BUỘC nếu user hỏi "RAM có tràn không?"):**
```bash
# Background monitor sample mỗi 2s
cat > /tmp/ram_monitor.sh <<'EOF'
#!/bin/bash
LOG=/tmp/batch_ram.log
echo "timestamp,free_gb,used_gb,active_gb" > $LOG
while true; do
  ts=$(date +%H:%M:%S)
  f=$(vm_stat | awk '/Pages free/ {print $3}' | tr -d '.')
  a=$(vm_stat | awk '/Pages active/ {print $3}' | tr -d '.')
  w=$(vm_stat | awk '/Pages wired down/ {print $4}' | tr -d '.')
  ps=16384
  printf "%s,%.2f,%.2f,%.2f\n" "$ts" "$(echo "$f*$ps/1024/1024/1024" | bc -l)" "$(echo "($a+$w)*$ps/1024/1024/1024" | bc -l)" "$(echo "$a*$ps/1024/1024/1024" | bc -l)" >> $LOG
  sleep 2
done
EOF
chmod +x /tmp/ram_monitor.sh
/tmp/ram_monitor.sh &
# Run batch...
# After done: pkill -f ram_monitor; sort -t, -k3 -n -r /tmp/batch_ram.log | head -5
```

**Real case 23/07 (OmniVoice batch 5):**
- Total audio 38.80s, synthesis 114.63s, **RTF 2.95x** (same as sequential — MPS single-process)
- **Peak RAM 12.68GB** (tăng 7GB so với baseline 19GB free) — model load ~3GB + 5 generations concurrent
- Mac 8GB RAM sẽ CRASH. Recommend ≥16GB cho batch 5+.
- `--nj_per_gpu 1` mandatory cho MPS (1 process, multi-GPU không áp dụng)

**Verify batch output:**
```bash
for f in batch_results/*.wav; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  sr=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$f")
  printf "%-30s %ss @ %sHz\n" "$(basename $f)" "$d" "$sr"
done
```

## Verification gates (BẮT BUỘC trước khi report)

**4-LAYER HARD RULE** (added 2026-07-23 sau session bug hunting, Layer 4 added 2026-07-24):

1. **Layer 1 — File valid:** ffprobe codec, sample_rate, channels, duration > 0
2. **Layer 2 — Amplitude:** `ffmpeg -af volumedetect` → peak > -10 dB, rms > -30 dB
3. **Layer 3 — Content:** `mlx_whisper --word-timestamps True` → transcript match expected text (NO ref leak, NO garbage)
4. **Layer 4 — Duration sanity** (NEW 2026-07-24): output duration ≤ 2× expected (chống hallucinate loop từ ref_text quá ngắn)

1. **Layer 1 — File valid:** ffprobe codec, sample_rate, channels, duration > 0
2. **Layer 2 — Amplitude:** `ffmpeg -af volumedetect` → peak > -10 dB, rms > -30 dB
3. **Layer 3 — Content:** `mlx_whisper --word-timestamps True` → transcript match expected text (NO ref leak, NO garbage)

**Tại sao 4 layer:** Layer 1-2 là CONTAINER check (file có valid không, có audio không). Layer 3 là CONTENT check (audio có đúng nội dung text cần synthesize không). Layer 4 là DURATION sanity (output không bị hallucinate loop do ref_text quá ngắn). Em đã fail cả 2 lần chỉ check layer 1-2 mà skip layer 3 → output bị REF LEAK (câu cuối ref audio inject vào) hoặc bị MPS batch bug (4/5 silent) mà không phát hiện. Lần 3 (24/07): chỉ check layer 1-3 mà skip layer 4 → không phát hiện hallucinate loop (output 76.96s thay vì ~13s, text lặp 8-10 lần). Layer 4 catch được case này.

```python
# Code recipe (adapt cho mọi TTS output)
import subprocess
# Layer 1
out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                "stream=codec_name,sample_rate,channels",
                                "-of", "csv=p=0", "out.wav"]).decode()
assert "pcm_s16le" in out and "24000" in out
# Layer 2
amp = subprocess.run(["ffmpeg", "-i", "out.wav", "-af", "volumedetect",
                       "-vn", "-f", "null", "-"], capture_output=True).stderr.decode()
peak_db = float(amp.split("max_volume: ")[1].split(" dB")[0])
assert peak_db > -10, f"audio too quiet: {peak_db} dB"
# Layer 3
subprocess.run(["mlx_whisper", "--model", "mlx-community/whisper-large-v3-mlx",
                "--language", "vi", "--output-format", "txt",
                "--word-timestamps", "True",
                "--output-dir", "/tmp/verify/", "out.wav"])
transcript = open("/tmp/verify/out.txt").read()
# Check NO ref leak (câu cuối ref_text KHÔNG xuất hiện trong output)
for ref_phrase in REF_PHRASES:  # list từ ref_text
    assert ref_phrase not in transcript.lower(), f"REF LEAK: '{ref_phrase}' found in output"
# Check expected text CÓ mặt
assert expected_phrase in transcript.lower(), f"missing expected content"
# Layer 4 — Duration sanity check (NEW 2026-07-24) — chống hallucinate loop
expected_dur = len(expected_text) / 4.0  # Vietnamese ≈ 4 chars/sec cho TTS natural
actual_dur = float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "csv=p=0", "out.wav"]).decode().strip())
assert actual_dur <= expected_dur * 2.0, \
    f"HALLUCINATE LOOP: output {actual_dur:.1f}s > 2× expected {expected_dur:.1f}s (ref_text quá ngắn?)"
```

**Nếu bất kỳ layer fail → KHÔNG báo xong. Fix hoặc escalate.**

## Output cho user

Save evidence ở `/Volumes/Storage-1/Hermes/scratch/<model>-test/`:
- `PLAN.md` — workflow + decisions
- `ref.wav` — ref audio preprocessed
- `ref.txt` — Whisper transcript
- `out.wav` — model output
- `baseline.wav` — Edge TTS NamMinh same text
- `compare.md` — verdict (PASS/FAIL/PARTIAL) + audio specs + decision matrix

**Báo cáo inline trong chat** (anh đọc Telegram):
- VERDICT: PASS/FAIL/PARTIAL
- 3 bằng chứng: file size, duration, sample rate (từ ffprobe raw)
- 1 decision matrix
- 1 recommendation: dùng tiếp / skip / thử model khác

## Common pitfalls

- **❌ Tự pick raw clip** — Pocket 3 audio có风扇 noise → clone quality giảm. LUÔN hỏi user cung cấp file clean.
- **❌ Skip pre-flight** — torch version mismatch, MPS not available, disk full → fail silently ở step 5. Check trước.
- **❌ Skip baseline comparison** — không biết model mới tốt hơn/xấu hơn edge-tts bao nhiêu. LUÔN generate baseline cùng text.
- **❌ Trust model success exit code** — một số model tạo file 0KB hoặc silent. LUÔN ffprobe verify.
- **❌ Skip edge cases** — ref audio <3s (reject), >10s (degradation), có nhạc nền (clone noise). Test edge cases khi có thể.
- **❌ Save output ở `/tmp/`** — KHÔNG survive backup. Save ở `/Volumes/Storage-1/Hermes/scratch/<model>-test/`.
- **❌ Trust user caption text thay vì Whisper transcript** — Khi user gõ text trong chat (có thể sai chính tả do gõ thoải mái) + Whisper transcribe audio, **LUÔN dùng Whisper output làm ref_text** (audio = source of truth). Real case 23/07: user gõ "dọng độc của Tung Anh... 30 tụi đang thức nghiệp" (sai chính tả) nhưng audio nói đúng "giọng đọc của Tuấn Anh... 30 tuổi đang thất nghiệp". Whisper transcript mới là ref_text chính xác.
- **❌ Trust TikTok link content mà không verify audio trước (NEW 2026-07-23 17:30, from @tuan_anh.review clip "Bài đăng 19").** Khi user gửi link TikTok/YouTube để extract ref audio, **LUÔN verify nội dung audio trước khi dùng làm ref** — TikTok CDN có thể trả về: (a) audio watermark track thay vì audio gốc, (b) voice hook outro (subscribe CTA) thay vì voice content, (c) chỉ nhạc nền không voice. Real case 23/07 17:30: link `vt.tiktok.com/ZSXGsWrMr` (video 7658580075805297938) → yt-dlp tải về 192s audio → Whisper transcribe 6 segments 30s đều chỉ là 1 câu "Hãy subscribe cho kênh La La School" lặp 7 lần → VAD detect peak level -0.02 dB (music) → user copy nhầm link clip outro hook. **Verify recipe (2 min, mandatory trước khi dùng làm ref):**
  ```bash
  # 1. Download audio
  yt-dlp -f audio_best --output "ref_check.%(ext)s" "<tiktok-url>"
  
  # 2. Whisper word-level detect voice segments (NO language hint — let model auto-detect)
  mlx_whisper --model mlx-community/whisper-large-v3-mlx \
    --output-format json --word-timestamps True \
    --output-dir /tmp/ref_check/ ref_check.m4a
  
  # 3. VAD check: voice speech thường peak -3 to -10 dB, music peak gần 0 dB
  ffmpeg -i ref_check.m4a -af "astats=metadata=1:reset=1,ametadata=mode=print:key=lavfi.astats.Overall.Peak_level" -f null - 2>&1 | grep "Peak_level"
  
  # 4. CHECK unique phrases ≥ 3 (nếu 1-2 phrases lặp → outro hook, KHÔNG dùng)
  python3 -c "
  import json
  d = json.load(open('/tmp/ref_check/ref_check.json'))
  texts = list({s.get('text','').strip() for s in d.get('segments', []) if s.get('text','').strip()})
  print(f'Unique phrases: {len(texts)}')
  if len(texts) < 3: print('⚠️ LIKELY OUTRO HOOK — DO NOT USE AS REF')
  "
  ```
  **Pass criteria:** ≥3 unique phrases, detected language = expected (vi), peak level < -3 dB. **Fail criteria:** <3 unique phrases hoặc detected language = en (mismatch) hoặc peak > -2 dB (music). Nếu fail → hỏi user "Clip này chỉ có voice outro/sound effect, không phải voice review. Anh có link clip khác không?" thay vì assume.
- **❌ JSONL `language_id` dùng language name** — `language_id` field trong JSONL BẮT BUỘC là ISO 639-3 code (`"vi"`, `"en"`), KHÔNG phải `"Vietnamese"` / `"English"`. CLI `--language` accept cả name (auto-resolve) nhưng batch parser KHÔNG. Verify: `from omnivoice.utils.lang_map import LANG_IDS; "vi" in LANG_IDS` (True). Nếu sai → silent skip sample hoặc fallback language mặc định.
- **❌ Skip RAM monitor khi batch** — Model load ~3GB + N generations concurrent có thể peak 12GB+ trên MPS. Mac 8GB sẽ swap hoặc crash. **LUÔN chạy RAM monitor background** khi batch ≥3 texts. Pattern xem Step 8.
- **❌ Set `--nj_per_gpu >1` trên Mac** — MPS = 1 process, multi-process gây contention + crash. Force `--nj_per_gpu 1`.
- **❌ Assume batch nhanh hơn sequential** — Trên MPS, batch RTF SAME như sequential (~2.5-3.5x) vì 1 process. Batch chỉ save cold-start overhead. Multi-GPU benefit KHÔNG apply cho Mac.
- **❌ Dùng `ref_text` full transcript (17s/3 câu)** — gây REF LEAK, model inject câu cuối vào output đầu/giữa. Sweet spot = **2 câu đầu** (~10s đầu ref audio). Chi tiết + 4-variant test matrix ở `references/omnivoice-recipe.md` § LESSON 1.
- **❌ Verify TTS output chỉ bằng file size/duration/sample_rate** — đó là container check, KHÔNG phải content check. 3-layer HARD RULE: (1) ffprobe valid, (2) volumedetect peak > -10dB, (3) Whisper word-level transcript match expected. Bắt buộc. Chi tiết ở `references/omnivoice-recipe.md` § LESSON 3.
- **❌ Blame "model bug" trước khi test prompt variants** — ref_text/temperature/num_step variants cheap (5 phút) → có thể fix ngay không cần workaround. Khi user flag issue → check 4 variants TRƯỚC. Chi tiết + anti-pattern ở `references/omnivoice-recipe.md` § LESSON 4.
- **❌ Skip A/B/C/D variant test trước khi conclude "model bug"** (NEW 2026-07-23, from anh direct feedback) — Real case: em đoán "model luôn leak ref text" → spent 30 min investigate amplitude bug, MPS bug, v.v. User correct: "test variants đi, đâu cần lần nào cũng import lại". Test 4 variants trong 5 phút → root cause = `ref_text` length (sweet spot 2 câu = no leak). **Lesson:** khi user flag issue với model behavior, KHÔNG default "model bug" → test 4 variants A/B/C/D trước. Variant matrix = cheap, immediate, often reveals prompt/config issue. See `diagnose` skill § "Common Pitfalls #6" for full anti-pattern.
- **❌ Dùng `ref_text` quá NGẮN (<60 chars)** (NEW 2026-07-24, from voice-clone session) — Khi ref_text quá ngắn (vd 1 câu ngắn 26 chars như "Xin chào tôi là Tuấn Anh đây."), OmniVoice KHÔNG có đủ context để anchor voice → model hallucinate LOOP: output kéo dài 5-6× bình thường (13s expected → 76.96s actual), text bị lặp 8-10 lần. Real case 24/07: ref audio 12.9s voice message, ref_text 26 chars → output 76.96s, Whisper: "Tôi là Tùng anh này" × 8-10 lần. **Sweet spot: ref_text ≥ 60 chars (1 câu dài hoặc 2 câu ngắn) AND ≤ 100 chars.** Verify protocol: check `ffprobe -show_entries format=duration` → nếu output > 2× expected duration → hallucinate loop → ref_text quá ngắn, re-save với ref_text dài hơn (≥ 60 chars).\n- **❌ Dùng CLI `omnivoice-infer-batch` cho batch 5+ texts dài khác nhau trên MPS** — bug GitHub issue #8 (peak -16.6dB trên 4/5 file). Workaround: in-process sequential 1-by-1, model load 1 lần. Chi tiết + test matrix ở `references/omnivoice-recipe.md` § LESSON 2.

## Step 9 — Production: Save/Load VoiceClonePrompt (cache 1 lần, dùng mãi) ⭐

**Tuấn Anh feedback 23/07 (verbatim):** *"Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu"*. **Lesson: KHI user muốn generate N file TikTok cùng voice, encode ref audio 1 LẦN → save `.pt` → load mãi mãi.** Skip Whisper + audio encoding mỗi lần → nhanh hơn 40% (11s/file vs 18s/file).

**Code recipe:**

```python
import torch
from omnivoice.models.omnivoice import OmniVoice, VoiceClonePrompt

# ONE-TIME setup (sau khi đã verify ref audio + ref_text đúng)
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
prompt = model.create_voice_clone_prompt(
    ref_audio="ref_5s_amp.wav",   # ⚠️ amp để ref_rms > 0.1 (xem Step 10)
    ref_text="<2 câu đầu ref audio>",  # ⚠️ NGẮN — xem Step 11
    preprocess_prompt=True,
)
prompt.save("/Volumes/Storage-1/Hermes/voice-prompts/<name>.pt")  # HERMES-ONLY-FOLDER

# MỖI LẦN DÙNG (load instant — 0.00s)
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/<name>.pt")
audio = model.generate(text="<target>", language="vi", voice_clone_prompt=prompt)
```

**HERMES-ONLY-FOLDER:** prompts lưu ở `/Volumes/Storage-1/Hermes/voice-prompts/` (~10-15KB each, KHÔNG ở `/Users/tuananh4865/.hermes/`).

**Speed comparison (5 file TikTok, Mac M-series):**

| Workflow | Time/file | Cache benefit |
|---|---|---|
| `ref_audio` + `ref_text` mỗi lần (Step 6) | ~18s | None |
| `voice_clone_prompt` load (Step 9) | **~11s** | **-40%** |
| Skip model load (already cached) | ~11s | -1:30 cold start |

**Anti-pattern (em đã làm session này, user correct):** ban đầu em không tìm `VoiceClonePrompt` API mà chạy thẳng `ref_audio + ref_text` cho 5 file. User nhắc "tạo template voice clone thôi" → mới tìm được. **Lesson: KHI user yêu cầu "dùng voice này cho nhiều file", PHẢI check xem model có `voice_clone_prompt`/cache API không TRƯỚC khi bắt đầu.**

## Step 10 — `ref_rms > 0.1` workaround (CRITICAL bypass)

**Bug OmniVoice 0.2.1 (line 898-903 `models/omnivoice.py`):**
```python
if ref_rms is not None and ref_rms < 0.1:
    generated_audio = generated_audio * ref_rms / 0.1   # ← scale DOWN output
```
Nếu ref_rms < 0.1 → output bị divide theo `ref_rms/0.1` = mất 4-16 dB amplitude (peak ~-20dB thay vì 0dB).

**Test 4 ref audio variants (verified 23/07):**
| ref_rms | Output peak | Status |
|---|---|---|
| 0.0614 (gốc) | -20.8 dB | ❌ **BUG TRIGGER** |
| 0.0951 | -20.8 dB | ❌ vẫn < 0.1 |
| 0.1100 (amp) | **-1.2 dB** | ✅ **BYPASS** |
| 0.1185 (amp nhẹ) | -1.2 dB | ✅ bypass |

**Fix recipe:** Amplify ref audio trước khi save prompt:
```python
import soundfile as sf, numpy as np
audio, sr = sf.read("ref_5s.wav")
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
amp_factor = 0.11 / ref_rms  # target = 0.11 (just above threshold)
audio_amp = audio * amp_factor
sf.write("ref_5s_amp.wav", audio_amp, sr)
print(f"amp: {amp_factor:.3f}, peak: {np.abs(audio_amp).max():.4f}")
# Kết quả: ref_rms = 0.11, peak < 1.0 (no clipping)
```

**Anti-pattern:** KHÔNG amp quá cao (ref_rms > 0.3) → output peak > 1.0 → clipping. Sweet spot = 0.11-0.15.

**Verify ref_rms after amp:**
```python
import torchaudio
wav, _ = torchaudio.load("ref_5s_amp.wav")
rms = torch.sqrt(torch.mean(wav.float() ** 2)).item()
assert 0.10 < rms < 0.20, f"ref_rms out of sweet spot: {rms}"
```

## Step 11 — `ref_text` ≤ 2 câu (~100 chars) — bypass REF LEAK

**Bug:** OmniVoice luôn inject câu cuối của `ref_text` vào đầu/giữa output (model dùng ref_text cuối làm prompt anchor). Real case 23/07: ref_text full 17s/3 câu → output 5/5 file đều có "Và bây giờ đang nhờ AI làm kịch bản cho tôi" ở đầu.

**Test 4 variants (verified 23/07):**

| ref_text length | Whisper output | Verdict |
|---|---|---|
| Full 17s (3 câu, 122 chars) | "...Và bây giờ đang nhờ AI + target text" | ❌ LEAK |
| 1 câu (39 chars) | "Target text lặp 2 lần" | ⚠️ lặp text target |
| **2 câu đầu (77-99 chars)** | **"Target text sạch"** | ✅ **BEST** |
| Quá ngắn (9 chars "Xin chào.") | Output rác 71s | ❌ model broken |

**Sweet spot: ref_text = 2 câu đầu của ref audio (~10s đầu, ~100 chars).**

**Verify no leak bằng Whisper word-level:**
```python
import subprocess, json
subprocess.run(["mlx_whisper", "--model", "mlx-community/whisper-large-v3-mlx",
                "--language", "vi", "--output-format", "json",
                "--word-timestamps", "True",
                "--output-dir", "/tmp/check/", "out.wav"])
data = json.load(open("/tmp/check/out.json"))
ref_words = set("và bây giờ đang nhờ ai làm kịch bản cho tôi".split())
for seg in data.get("segments", []):
    for w in seg.get("words", []):
        wt = w.get("word", "").lower().strip(".,!?")
        assert wt not in ref_words, f"REF LEAK detected: '{wt}'"
print("✅ No ref leak")
```

## Step 12 — `pad_duration=0` để concat thẳng (NEW 2026-07-23, anh feedback) ⭐

**Tuấn Anh feedback (verbatim):** *"Không fade không trim luôn audio bỏ padding 100ms luôn"*.

**Problem (em đã miss):** OmniVoice default config thêm `pad_duration=0.1` (100ms silence đầu) + `fade_duration=0.1` (100ms silence cuối) vào MỖI output audio. Khi concat N file thẳng → mỗi boundary có 100+100 = **200ms silent gap**. Whisper hallucinate câu ngay sau gap lớn (vd "tuần" → "tuổi").

**Fix sai #1 (em đã làm):** Dùng `afade=t=in:out:0.03` → tạo 60ms silent gap, peak audio boundary = 0.

**Fix sai #2 (em đã làm):** Trim 100ms padding + apply 30ms fade out → workaround work nhưng còn 30ms fade → voice bị cụt.

**✅ Fix đúng (anh correct):** Disable padding NGAY TỪ GENERATE, concat thẳng KHÔNG cần filter:

```python
from omnivoice import OmniVoiceGenerationConfig

# Disable pad/fade mặc định
gc = OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)

# Generate
audio = model.generate(text=text, language="vi", voice_clone_prompt=prompt, generation_config=gc)[0]
# Audio bắt đầu ngay sample 0, KHÔNG có lead/trail silence

# Concat thẳng — chỉ 1 dòng filter
ffmpeg -y \
  -i file1.wav -i file2.wav -i file3.wav \
  -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" \
  -map "[out]" -ar 24000 -ac 1 final.wav
```

**Verified (Mac M-series, 5 segments TikTok):**

| Method | Boundary peak | First audio | Whisper hallucinate |
|---|---|---|---|
| afade in+out (sai) | 0.00 | 104ms | "tuần" → "tuổi" |
| trim + fade out | 0.03-0.11 | 0ms (sau trim) | OK |
| **NO PADDING (đúng)** | **0.65-0.77** | **0ms** | **OK + clean** |

**Apply:** MỌI concat pipeline N file OmniVoice → set `pad_duration=0, fade_duration=0` ở `OmniVoiceGenerationConfig`, concat thẳng với filter `[i:a]concat`. KHÔNG cần trim/fade post-process.

## Step 13 — 13 Non-Verbal Emotion Tags (NEW 2026-07-23) ⭐

**Khám phá:** OmniVoice hỗ trợ inline emotion tags `[laughter]`, `[sigh]`, `[question-ah]`, etc. giúp voice "thật hơn" cho TikTok content. 13 tags từ source `_NONVERBAL_PATTERN` (line 1651-1654):

| Tag | Emotion | Verified peak |
|---|---|---|
| `[laughter]` | Cười | -3.2 dB |
| `[sigh]` | Thở dài | -3.2 dB |
| `[question-ah]` | Câu hỏi kết thúc "à" | -3.1 dB |
| `[question-oh]` | "ô" | (chưa test) |
| `[question-ei]` | "êy" | (chưa test) |
| `[question-yi]` | "ỳ" | (chưa test) |
| `[surprise-ah]` | "á" | (chưa test) |
| `[surprise-oh]` | Wow, "ô" | **-2.6 dB** (loudest!) |
| `[surprise-wa]` | "wa" | (chưa test) |
| `[surprise-yo]` | "yo" | (chưa test) |
| `[dissatisfaction-hnn]` | "hừm", không hài lòng | -3.0 dB |
| `[confirmation-en]` | Xác nhận (English) | (chưa test) |
| `[question-en]` | Câu hỏi (English) | (chưa test) |

**Verified effect:** emotion tags TĂNG peak amplitude (-2 to -3 dB vs -3.7 baseline) → voice engaging hơn cho TikTok.

**Recipe TikTok với emotion:**

```python
gc = OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)

texts = [
    ("hook",    "[surprise-oh] Sale SỐC hôm nay! [laughter] Giảm 50% luôn các bạn ơi!"),
    ("problem", "[sigh] Bình thường máy hút bụi nặng lắm, pin yếu, lại còn ồn."),
    ("solution","Chiếc máy này thì sao[question-ah] Nhỏ gọn, êm, pin trâu, rẻ nữa!"),
    ("cta",     "Bấm giỏ hàng đi anh em[confirmation-en] Freeship toàn quốc nha!"),
]

prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/<name>.pt")
for sid, text in texts:
    audio = model.generate(text=text, language="vi",
                            voice_clone_prompt=prompt,
                            generation_config=gc)[0]
    sf.write(f"{sid}.wav", audio, model.sampling_rate)
```

**Pronunciation control (bonus):**
- English: `[B EY1 S]`, `[B AE1 S]` override CMU dict
- Chinese: uppercase pinyin + tone digit `ZHE2` override tone
- Inline preserved bởi `_apply_with_protection` trong normalize_text

**Anti-patterns:**
- ❌ Capitalize tag (`[Laughter]`) → không match regex
- ❌ Combine tags KHÔNG có space — `[laughter][sigh]` cần space để model parse
- ❌ Mix emotion tag + text without separator — `[laughter]cười` → model không detect tag

## Reference files

- `references/omnivoice-recipe.md` — OmniVoice install + clone recipe (Apple Silicon verified 2026-07-23, batch 5 verified 15:30, 23/07 production prompt verified 19:53, **pad_duration=0 verified 21:00**, **emotion tags verified 20:45**)
- `references/tiktok-link-verify.md` — verify recipe cho TikTok/YouTube link trước khi dùng làm ref audio (NEW 2026-07-23 17:30, từ case @tuan_anh.review clip outro hook)
- `references/omnivoice-production-prompt.md` — VoiceClonePrompt save/load pattern + 2 critical workarounds (ref_rms > 0.1, ref_text ≤ 2 câu) + pad_duration=0 + emotion tags — chính là workflow PRODUCTION cho TikTok voice clone từ session 23/07.
- (Thêm sau khi test thêm model: CosyVoice, F5-TTS, ChatTTS, vv.)

## Related skills

- `voice-setup` — production TTS cho Telegram (Edge TTS NamMinh)
- `third-party-tool-install` — install CLI lên Mac
- `ml-model-comparison-report` — research MODEL (weights/benchmarks) chưa cần test
- `github-repo-recon` — research repo structure (Khi em mới nhận link GitHub)
- `hermes-file-edit-logging` — mọi file edit phải log
- `evidence-first-delivery` — claim xong phải có evidence (ffprobe output, file path)
- `tiktok-pipeline-studio` — full TikTok video pipeline (motion graphic + edit + verify) — nếu anh muốn dùng OmniVoice cho TikTok narration thay edge-tts NamMinh, load cả 2 skills
- `tiktok-verify-protocol` — 3-layer verify pattern (file valid + amplitude + transcript) có thể adapt cho TTS output
