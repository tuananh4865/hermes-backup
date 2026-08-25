---
name: audio-highlight-detection
title: Detect Highlight Moments in Long Audio/Video via Energy-Based Audio Features
description: Class-level umbrella for finding crowd-cheer/applause/audio-event highlights in long-form audio/video (sports broadcasts, concerts, podcasts, talks). Covers RMS amplitude, spectral centroid, zero-crossing rate, spectral flux, onset detection, and hybrid fusion with ASR/OCR. Use when user says "detect highlights", "find cheer moments", "auto-extract rally moments", "energy-based detection", "audio event detection", "tìm khoảnh khắc đáng chú ý", "detect applause", or has a 30min+ sports/event recording and wants timestamped candidate moments for clipping.
created: 2026-07-09
updated: 2026-07-12
type: skill
tags: [audio, librosa, signal-processing, rms, spectral-centroid, zero-crossing-rate, spectral-flux, onset-detection, sports, highlight, cheer, applause, mfcc, hybrid-detection]
confidence: medium
related_skills:
  - video-cut-tiktok-shorts
  - tiktok-transcript-pipeline
  - whisper
---

# Detect Highlight Moments via Energy-Based Audio Features

Class-level skill for finding "exciting" audio events (applause, crowd cheer, loud reactions, sudden energy changes) in long-form audio/video recordings. Companion to video-cut workflows but focused on the **DETECTION** step, not the cut step.

## When to use

Trigger phrases:
- "Detect highlights" / "find cheer moments" / "auto-extract rally moments"
- "Energy-based detection" / "audio event detection"
- "Detect applause" / "tìm khoảnh khắc đáng chú ý"
- "Tìm rally" / "điểm hay" / "đoạn hấp dẫn" trong video thể thao
- User has 30min+ recording (sports broadcast, concert, podcast with audience) and wants timestamped candidate moments

**NOT for:** Cut 60s TikTok clips from review/podcast videos → use `video-cut-tiktok-shorts` instead. The cut skill assumes input is already segmented; this skill finds the segments.

## Why this skill exists

Existing video skills (`video-cut-tiktok-shorts`, `tiktok-video-editor`) are **post-segmentation** workflows — they assume you already know which segments to cut. For long-form content (60min+ sports matches, concerts), the user typically wants:

> "Find me the 10 most exciting moments in this 90-minute badminton match"

That requires **detection**, not cutting. This skill covers the detection half.

## Core Approach: 3-Layer Hybrid

Single-feature detection (RMS alone) is too noisy. Production-grade systems use 3 layers:

| Layer | Signal | Purpose |
|-------|--------|---------|
| **L1 (Filter)** | RMS + adaptive threshold | Pre-filter ~50% of audio to candidate regions |
| **L2 (Refine)** | Spectral centroid + ZCR + spectral flux | Filter music/speech/whistle false positives |
| **L3 (Confirm)** | ASR text (Whisper BLV) + OCR scoreboard | High-confidence final candidates |

**Score formula (recommended starting point):**

```
final_score = 0.60 * audio_score + 0.30 * text_score + 0.10 * scoreboard_score
highlight candidate iff final_score > 0.65
```

Where:
- `audio_score = 0.5 * rms_score + 0.3 * centroid_score + 0.2 * zcr_score`
- `text_score = 0.3` if Whisper transcript matches cheer keywords, else `0.0`
- `scoreboard_score = 0.1` if OCR detects score change, else `0.0`

## Key thresholds (energy-based features)

All values normalized for 16kHz mono audio. Tune per-domain.

| Feature | Silence/Speech | Music | Applause (light) | Cheer (heavy) | Peak roar |
|---------|----------------|-------|------------------|---------------|-----------|
| **RMS amplitude** (linear) | 0.001-0.05 | 0.05-0.20 | 0.10-0.25 | 0.25-0.55 | 0.40-0.70 |
| **Spectral centroid** (Hz) | 500-1500 | 1500-3500 | 2000-4500 | 1800-5000 | 2500-6000 |
| **Zero-crossing rate** | 0.05-0.15 | 0.10-0.30 | 0.20-0.50 | 0.25-0.60 | 0.30-0.65 |
| **Spectral flux** | low | medium | high (onset) | sustained high | peak |

**Critical insight — ADAPTIVE threshold wins:**

```python
# BAD — fixed threshold, fails when venue/volume varies
threshold = 0.22

# GOOD — adaptive per-video (top 85th percentile)
threshold = np.percentile(rms_db, 85)
```

Fixed thresholds break on quiet venues, distant mics, low-volume sports. Always calibrate to the file.

## 5-Step Detection Workflow

### Step 1: Extract audio (mono, 22050 Hz for librosa)

```bash
# Quick ffmpeg extraction
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 22050 -c:a pcm_s16le audio.wav
```

### Step 2: Pre-filter with RMS (L1)

```python
import librosa
import numpy as np
from scipy.ndimage import uniform_filter1d

y, sr = librosa.load("audio.wav", sr=22050, mono=True)
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
rms_db = librosa.amplitude_to_db(rms, ref=np.max)
rms_smooth = uniform_filter1d(rms_db, size=20)  # ~460ms smoothing

# Adaptive threshold — auto-calibrate to file
threshold = np.percentile(rms_db, 85)  # top 15% = "loud"
above_thr = rms_smooth > threshold
```

### Step 3: Filter with spectral features (L2)

```python
centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)[0]
zcr = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512)[0]

# Smooth
centroid_s = uniform_filter1d(centroid, size=20)
zcr_s = uniform_filter1d(zcr, size=20)

# Applause signature: high centroid + high ZCR
is_applause = above_thr & (centroid_s > 2000) & (zcr_s > 0.15)
```

### Step 4: Extract candidate segments (min duration ~2s)

```python
def extract_segments(mask, times, min_duration=2.0):
    segments = []
    in_seg = False
    start = 0
    for t, m in zip(times, mask):
        if m and not in_seg:
            start = t
            in_seg = True
        elif not m and in_seg:
            if t - start >= min_duration:
                segments.append((start, t))
            in_seg = False
    if in_seg and times[-1] - start >= min_duration:
        segments.append((start, times[-1]))
    return segments
```

### Step 5: Confirm with ASR/OCR (L3) — optional but recommended

- **Whisper BLV:** transcribe, match cheer keywords (see references/rms-energy-detection.md for sport-specific keyword lists)
- **OCR scoreboard:** detect score changes as anchor points

## Tool selection (3 options)

| Tool | Pros | Cons | Best for |
|------|------|------|----------|
| **ffmpeg `astats`** | Fast, no Python, streams | Returns dB only, no spectral info | Quick RMS scan |
| **librosa** | All features, clean API | Slower, RAM-heavy | Production analysis |
| **pydub** | Simplest, no numpy | Slower than librosa | Quick prototyping |

### ffmpeg astats one-liner

```bash
ffmpeg -i input.mp4 \
  -af "astats=metadata=1:reset=1:length=0.5,ametadata=print:key=lavfi.astats.Overall.RMS_level" \
  -f null - 2>&1 | grep "RMS_level"
```

Returns one line per 0.5s window — perfect for streaming into a processing pipeline.

### librosa complete snippet

See `references/rms-energy-detection.md` §3 — includes 5 ready-to-run snippets (basic RMS, centroid+cheer, onset detection, full pipeline, BadmintonAudioDetector class).

## Domain-specific considerations

Different content types need different tuning:

| Content | Typical loud mix | Threshold hint |
|---------|------------------|----------------|
| **Football/soccer broadcast** | Crowd + commentator | Centroid > 1800Hz, RMS > 0.20 |
| **Badminton indoor** | Quiet baseline, brief cheer | Lower RMS threshold (~0.15), trust duration |
| **Concert** | Music dominates | Need spectral gate to find applause BETWEEN songs |
| **Basketball** | Loud sustained crowd | Higher threshold, watch for whistle peaks |
| **Tennis** | Quiet between points | Use ZCR + spectral flux, not raw RMS |
| **Podcast with audience** | Speech + sparse laugh | ZCR-based laugh detection |

**Critical pitfall:** Don't assume football thresholds work for badminton. Badminton crowds are QUIETER — what counts as "loud" depends entirely on the sport/venue. Always start with adaptive threshold, then tune.

## Limitations to acknowledge

Energy-based detection **CANNOT**:

1. Distinguish two close rallies (back-to-back highlights merge into one segment)
2. Detect "silent highlights" (a beautiful shot with no crowd reaction)
3. Handle music masking (concert with loud backing track)
4. Adapt across venues without per-video calibration

**Solution:** Always fuse with non-audio signals. The 3-layer hybrid (audio + ASR + OCR) is the only way to reach production-grade accuracy.

## Reference files

- `references/rms-energy-detection.md` — **Full research dump** (41KB): threshold tables for 8 audio types, spectral feature explanations, 5 ready-to-run code snippets (librosa + ffmpeg + pydub), hybrid pipeline architecture, 19 cited sources (arXiv papers, code repos, librosa docs, patent US11025985B2). Load this when implementing or tuning a detector.

## Scripts (ready to run)

- `scripts/detect_highlights.py` — **Production CLI** with argparse. Takes any audio/video file, outputs timestamped JSON. Defaults tuned for sports broadcasts (badminton/football/basketball). Tunable via flags: `--percentile`, `--centroid-thr`, `--zcr-thr`, `--min-duration`, `--top`. Run when user says "find highlights in this video" and wants immediate output. Example: `python scripts/detect_highlights.py match.mp4 --top 10 --output highlights.json`

## Companion skills

- **`video-cut-tiktok-shorts`** — Once you have timestamps, use this to cut. It's a downstream consumer of detection output.
- **`whisper`** — Layer 3 text matching for hybrid confirmation.
- **`telegram-video-analysis`** — If user sends a video file expecting analysis, this is the entry point.

## Quick-start template

```python
from pathlib import Path
import librosa, numpy as np
from scipy.ndimage import uniform_filter1d

def quick_detect(audio_path: str, top_n: int = 10):
    """Quick 2-layer detector: RMS + spectral centroid. Returns top N segments by peak RMS."""
    y, sr = librosa.load(audio_path, sr=22050, mono=True)

    # L1: RMS
    rms_db = librosa.amplitude_to_db(
        librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0],
        ref=np.max
    )
    rms_smooth = uniform_filter1d(rms_db, size=20)

    # L2: Centroid
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=512)[0]
    cent_smooth = uniform_filter1d(centroid, size=20)

    # Adaptive threshold + gate
    thr = np.percentile(rms_db, 85)
    times = librosa.frames_to_time(np.arange(len(rms_smooth)), sr=sr, hop_length=512)
    mask = (rms_smooth > thr) & (cent_smooth > 2000)

    # Extract segments (≥2s)
    segs, in_seg, start = [], False, 0
    for t, m in zip(times, mask):
        if m and not in_seg:
            start, in_seg = t, True
        elif not m and in_seg:
            if t - start >= 2.0:
                peak = rms_smooth[(times >= start) & (times < t)].max()
                segs.append({"start": round(start, 2), "end": round(t, 2), "peak_db": round(peak, 1)})
            in_seg = False

    # Sort by peak
    segs.sort(key=lambda s: s["peak_db"], reverse=True)
    return segs[:top_n]

# Usage
hits = quick_detect("match_60min.wav")
print(f"Top {len(hits)} cheer candidates:")
for h in hits:
    print(f"  {h['start']}s - {h['end']}s (peak {h['peak_db']} dB)")
```

## Pitfalls (from real research)

### Pitfall 1: RMS alone is NOT enough
RMS = loudness. Music can be louder than applause. Always pair with spectral centroid or ZCR to filter music/speech.

### Pitfall 2: Fixed threshold fails on quiet venues
Badminton indoor, women's sports, small venues — all have lower baseline RMS. Use adaptive percentile (top 85th) not fixed value.

### Pitfall 3: Whistle ≠ cheer
Whistle: narrow-band sustained tone. Cheer: broadband transient. Filter via spectral flatness or duration (<1s = likely whistle).

### Pitfall 4: Whisper ASR can confirm cheer in 80% of cases
Add Layer 3 (Whisper BLV text matching) to boost precision from ~65% → ~88%. Best bang-for-buck fusion.

### Pitfall 5: Window size 23ms = too granular
Use `hop_length=512` (23ms) but smooth with `uniform_filter1d(size=20)` (~460ms) to avoid noise spikes being treated as events.

### Pitfall 6 (CRITICAL — 12/07/2026): Duration-weighted scoring inverts priority
Scoring formulas like `peak × 0.4 + duration_norm × 0.6` systematically prefer LONG-SUSTAINED-LOUD segments (ceremony, music bed, anthem, post-match speeches, applause loops) over BRIEF-LOUD TRANSIENTS (shuttle hits, whistles, actual applause bursts, action peaks).

**Why this happens:** Broadcast audio (sports, concerts, podcasts with audience) has sustained loudness as the norm during ceremony/music/anthem. Only actual content events (rally, song chorus, applause burst, slam dunk) are brief-and-loud transients. Duration-based weighting is essentially "reward sustained loudness" — which is exactly what ceremony is.

**Verified adversarial test 12/07 (badminton-highlight-editor):** a 76s ceremony at -22dB scored 0.720; a 14s genuine rally at same peak scored 0.678 — ceremony outranks rally. Result: 4 of 6 output clips were ceremony/post-match instead of rallies. **Discovered by independent adversarial verifier.**

**Fix (any of these):**
1. Replace `peak × 0.4 + duration × 0.6` with `peak × 0.7 + (1 / (1 + duration/5)) × 0.3` (rewards brief-but-loud over long-but-moderate).
2. Add sharp transient bonus: each peak with >30dB swing in <2s adds +0.05 to score.
3. Mandatory visual verification gate — sample 1 frame per detected segment, check the moment is actual content not ceremony.

### Pitfall 7: "Loud" ≠ "Content" — purely loud regions can be ceremony/music
A region peaking at -22dB RMS could be (a) genuine applause at game point, (b) music bed during intro, (c) PA announcement with crowd cheering, (d) anthem with crowd singing. All four peak at the same dB. Always ground-truth with a visual frame or external signal (BLV text, scoreboard change, lyrics in chorus window) before accepting a segment. **Strong signal of actual content (not ceremony): sharp transient peaks (>30dB swing in <2s) inside the window — shuttle hit, whistle, applause burst, shot clock.**

### Pitfall 8: Whisper EN transcripts hallucinate massively on crowd-only audio
Whisper medium-mlx EN hallucinates "Wow"/"That's the"/"Long of the back line" loops hundreds of times on BWF TV crowd-audio-only segments. Verified 1106/1558 entries (71%) hallucinate in one test. NOT fixable with anti-hallucinate flags (`--condition-on-previous-text False --no-speech-threshold 0.6`). → Detect via `grep -c "That's the"` count; skip text-scoring layer if hallucinate ratio > 50%; use audio-only as ground truth.

## When NOT to use this skill

- Audio is mostly speech with no crowd/audience (just an interview) → use `whisper` + `video-cut-tiktok-shorts` directly
- Source is < 5 minutes → manual annotation is faster than any detection
- Target is word-level transcription → use `whisper` directly
- User wants frame-by-frame visual analysis → use `telegram-video-analysis`

## Future extensions (not yet implemented)

- YAMNet / PANN embeddings as Layer 2 (better than hand-crafted features)
- Real-time streaming mode (process audio as it arrives)
- Per-broadcaster calibration (cache baseline stats from first 5 minutes)
- Whisper-small for fast Layer 3 (instead of full Whisper-large)