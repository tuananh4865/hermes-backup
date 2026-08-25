# PITFALL #95 — TTS/AI-generated audio: container valid ≠ content OK

**Ngày phát hiện:** 23/07/2026 (OmniVoice batch 5 — em report "PASS" vì file 24kHz/has size, user flag "Toàn bộ 5batch lỗi hết" → 4/5 file audio peak -20.8dB gần silent).

## Trigger

Khi verify output từ TTS/voice-clone (edge-tts, OmniVoice, ElevenLabs, F5-TTS, CosyVoice, ...) hoặc bất kỳ AI-generated audio nào. Em hay chỉ check:
- `ffprobe -show_entries format=duration` → 6.28s ✅
- `ffprobe -select_streams a:0 -show_entries stream=codec_name,sample_rate` → pcm_s16le 24kHz ✅
- `ls -la` → 300KB ✅

→ Report PASS → user nghe thấy audio gần silent → mất trust.

## Root cause

AI-generated audio có thể pass container check (valid encoding, non-zero size, correct sample rate) nhưng content bên trong:
- **Gần silent** — model output toàn zero hoặc gần zero (peak -20dB so với baseline -5dB)
- **Garbage noise** — model output noise không phải speech
- **Wrong content** — model output text khác (sai transcript, sai language)
- **Mismatched loudness** — peak OK nhưng average volume quá thấp (RMS < -30dB)

Container metadata chỉ describe "cái hộp" — KHÔNG describe "cái bên trong hộp".

## Recipe — BẮT BUỘC cho MỌI TTS output

### Single file quick check
```bash
ffmpeg -i out.wav -af "volumedetect" -vn -f null - 2>&1 | grep -E "max_volume|mean_volume"
```
Expected:
- `max_volume: -1.0 dB` → OK (full volume, có thể clip một chút)
- `max_volume: -5.0 dB` → OK (giọng nói bình thường)
- `max_volume: -10.0 dB` → ⚠️ yếu, có thể OK nếu cần mix với audio khác
- `max_volume: -20.0 dB` → ❌ **GẦN SILENT, FAIL**
- `max_volume: -inf dB` → ❌ **TOÀN ZERO, FAIL**

- `mean_volume: -20.0 dB` → OK
- `mean_volume: -25.0 dB` → OK
- `mean_volume: -30.0 dB` → ⚠️ yếu
- `mean_volume: -35.0 dB` → ❌ **FAIL**

### Batch check N files
```bash
for f in *.wav; do
  max=$(ffmpeg -i "$f" -af "volumedetect" -vn -f null - 2>&1 | grep "max_volume" | awk '{print $5}')
  rms=$(ffmpeg -i "$f" -af "volumedetect" -vn -f null - 2>&1 | grep "mean_volume" | awk '{print $5}')
  echo "$f: max=$max rms=$rms"
done
```

### Time-resolved analysis (khi cần debug "tại sao sai")
```bash
# Per-second RMS — phát hiện silent segment giữa audio
ffmpeg -i out.wav -af "astats=metadata=1:reset=2,ametadata=mode=print:key=lavfi.astats.Overall.RMS_level" -f null - 2>&1 | grep "RMS_level"
```
- Nếu RMS drop về `-inf` ở giữa → audio có silent gap
- Nếu RMS đều thấp (~-35dB) toàn bộ → model output gần silent uniformly

### Thresholds (cho voice content, không phải BGM/SFX)
| Metric | OK | Borderline | FAIL |
|---|---|---|---|
| `max_volume` | > -3 dB | -3 đến -10 dB | < -10 dB |
| `mean_volume` | > -20 dB | -20 đến -28 dB | < -28 dB |

## Verify checklist cho TTS pipeline

MỖI khi ship TTS output (single hoặc batch):

- [ ] `ffprobe` confirm encoding (24kHz hoặc đúng spec, mono/stereo) — **container check**
- [ ] `volumedetect` confirm amplitude (`max > -10dB`, `rms > -25dB`) — **content check**
- [ ] Nếu output là speech: confirm transcript match (whisper ASR re-transcribe → diff với text input)
- [ ] Sample listen 1 file đầu tiên (anh nghe) — **human sanity check**
- [ ] Nếu batch > 3 files: spot check 2-3 file, không phải chỉ file đầu

## PITFALL đừng quên

- ❌ KHÔNG chỉ check `ffprobe` format + stream. Container valid ≠ audio content OK.
- ❌ KHÔNG check 1 file rồi assume cả batch OK. Real case 23/07: 1/5 file OK, 4/5 file fail.
- ❌ KHÔNG trust `Processing samples: 100%|██████████` progress bar. Cũng không trust CLI exit code 0. Verify bằng evidence tool.
- ❌ KHÔNG skip volumedetect vì "chắc chắn OK". 30s verify save hàng giờ debug.
- ❌ KHÔNG amplify output thay vì debug root cause (ref_rms < 0.1 có thể là root cause, không phải amp).
- ✅ LUÔN run volumedetect NGAY khi file TTS output xong, trước khi report done.
- ✅ LUÔN batch scan N file cùng lúc (loop volumedetect takes 1-2s per file, worth it).
- ✅ Nếu output fail threshold, check root cause TRƯỚC khi amp fix:
  - ref audio có hợp lệ không (duration 5-10s, sample rate ≥ 16kHz, không nhạc nền)?
  - model có support language này không?
  - MPS/CUDA có bug batch size không? (OmniVoice issue #8)
  - CLI flags có override model defaults không?
- ✅ Nếu amp fix cần thiết, amplify REF AUDIO chứ không phải output (vì output đã qua post-process).

## Repro recipe (OmniVoice batch 5 — 23/07)

Input: 5 text TikTok-style (HOOK→PROBLEM→SOLUTION→USP→CTA), ref audio 10s
Wrong verify (chỉ check container):
```bash
for f in batch_results/*.wav; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  sr=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$f")
  echo "$f: ${d}s @ ${sr}Hz"  # 6.28s @ 24000Hz ... ALL OK
done
# → Em report "5/5 PASS, 24kHz valid"
```

Right verify (check content):
```bash
for f in batch_results/*.wav; do
  max=$(ffmpeg -i "$f" -af volumedetect -vn -f null - 2>&1 | grep max_volume | awk '{print $5}')
  rms=$(ffmpeg -i "$f" -af volumedetect -vn -f null - 2>&1 | grep mean_volume | awk '{print $5}')
  echo "$f: max=$max rms=$rms"
done
# → batch_01_hook.wav: max=-20.8 rms=-35.5  ❌ FAIL
# → batch_02_problem.wav: max=-20.8 rms=-35.5  ❌ FAIL
# → batch_03_solution.wav: max=-20.8 rms=-35.4  ❌ FAIL
# → batch_04_usp.wav: max=-6.4 rms=-22.7  ✅ OK (anchor, longest text)
# → batch_05_cta.wav: max=-20.8 rms=-35.4  ❌ FAIL
# → 4/5 FAIL — em phải report 4/5 fail, không phải 5/5 PASS
```

Root cause: OmniVoice MPS backend bug với batch ≥ 5 texts có độ dài khác nhau (issue #8 vẫn còn trong v0.2.1). Workaround: sequential 1-by-1 hoặc batch với texts cùng độ dài.

## Cross-reference

- PITFALL #25 TECHNICAL SPEC VERIFY (encoding/integrity/pixel) — cover VIDEO 7-layer, focus codec/duration/visual
- PITFALL #43 FFPROBE-AUDIO-SILENT-DROP — `-select_streams v:0` MISS audio info; LUÔN probe audio RIÊNG
- PITFALL #57 TRANSCRIPT-FIRST VERIFY — verify clip = transcript analysis FIRST (narrative bugs, không phải amplitude)

PITFALL #95 này COMPLEMENT #25 (cover audio amplitude — chỗ #25 miss vì focus video pixel). PITFALL #95 cũng khác #43: #43 là "ffprobe MISS audio info", #95 là "ffprobe OK nhưng audio content bad".

## Quick decision tree

```
Có file audio cần verify không?
├─ AI-generated TTS / voice clone / synthesis?
│  └─ YES → volumedetect (this PITFALL)
├─ Edited/mixed audio trong TikTok clip?
│  └─ YES → PITFALL #25 L5 audio integrity (codec/bitrate, không cần volumedetect)
├─ Captured raw audio (mic/Pocket 3)?
│  └─ YES → volumedetect (luôn — nếu fail kiểm tra thiết bị)
└─ Music/BGM download?
   └─ YES → volumedetect optional (chỉ check duration + format)
```
