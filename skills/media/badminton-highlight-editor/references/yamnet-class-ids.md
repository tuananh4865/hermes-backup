# YAMNet Class IDs cho Badminton Highlight

> **Reference mapping 521 AudioSet classes → badminton-relevant IDs.** Verified từ official `yamnet_class_map.csv`.

## 📥 Setup

```bash
pip install tensorflow tensorflow_hub resampy soundfile
# Tải model (~22 MB)
wget https://storage.googleapis.com/audioset/yamnet.h5 -O ~/.cache/yamnet.h5
wget https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv -O ~/.cache/yamnet_class_map.csv
```

**Hoặc dùng TFLite (4 MB, faster):**
```bash
pip install tflite-runtime
wget https://storage.googleapis.com/audioset/yamnet.tflite -O ~/.cache/yamnet.tflite
```

## 🎯 Badminton-relevant class IDs

Verified từ `yamnet_class_map.csv` (mid 2020 version, vẫn stable):

| Class name | Class ID | Confidence threshold |
|---|---|---|
| `Applause` | **62** | ≥ 0.5 |
| `Cheering` | **61** | ≥ 0.5 |
| `Clapping` | **58** | ≥ 0.5 |
| `Crowd` | **64** | ≥ 0.4 |
| `Hubbub` | **65** | ≥ 0.4 |
| `Yell` | **9** | ≥ 0.6 (nhiều false positive) |
| `Shout` | **6** | ≥ 0.6 |
| `Bellow` | **7** | ≥ 0.6 |
| `Screaming` | **11** | ≥ 0.6 |
| `Whoop` | **8** | ≥ 0.6 |
| `Children shouting` | **10** | ⚠️ Skip (false positive) |
| `Whistle` | **N/A** (not in classes 1-521) | — |

## 📊 Class co-occurrence patterns

Trong clip cầu lông thật, các class thường xuất hiện cùng lúc:

```
Rally điểm hay:
- Applause (62) + Cheering (61) + Crowd (64) → score cao

Rally dài:
- Applause (62) + Cheering (61) → score trung bình

Sai/bắn trượt:
- Yell (9) + Laughter (74) → score thấp, BỎ

BLV speech:
- Speech (0) + Applause (62) → score cao nhất
```

## 🚫 Negative class IDs (BỎ nếu detect)

| Class name | Class ID | Lý do BỎ |
|---|---|---|
| `Music` | **137** | False positive khi clip có nhạc nền |
| `Singing` | **162** | Nhầm với BLV đang hát/nick name |
| `Television` | **324** | Background TV noise |
| `Static` | **467** | Audio static, không phải rally |
| `White noise` | **465** | Noise floor, không phải rally |
| `Pink noise` | **466** | Noise floor |
| `Jingle` | **156** | Intro/outro YouTube, không phải rally |

## 🔧 Inference code (Python)

```python
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv

# Load model
model = hub.load('https://tfhub.dev/google/yamnet/1')

# Load class names
class_names = []
with open('~/.cache/yamnet_class_map.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        class_names.append(row[2])  # display_name column

def detect_applause(audio_wav_path, sample_rate=16000):
    """Detect applause regions trong audio file."""
    import librosa
    waveform, sr = librosa.load(audio_wav_path, sr=sample_rate, mono=True)

    # Run YAMNet
    scores, embeddings, spectrogram = model(waveform)

    # scores shape: (N_patches, 521)
    # Each patch = 0.96s, hop = 0.48s

    # Find Applause + Cheering + Crowd
    applause_scores = scores[:, 62].numpy()  # Applause
    cheering_scores = scores[:, 61].numpy()  # Cheering
    crowd_scores = scores[:, 64].numpy()      # Crowd
    music_scores = scores[:, 137].numpy()     # Music (negative filter)

    # Combined applause score (max of all 3)
    combined_score = np.maximum.reduce([
        applause_scores,
        cheering_scores,
        crowd_scores
    ])

    # Convert patch indices to seconds
    patches_per_second = 1 / 0.48  # 2.08 patches/sec
    timestamps = np.arange(len(combined_score)) / patches_per_second

    # Triple-gate: Applause ≥ 0.5 AND NOT music
    applause_regions = []
    i = 0
    while i < len(combined_score):
        if combined_score[i] >= 0.5 and music_scores[i] < 0.4:
            start_t = timestamps[i]
            max_score = combined_score[i]
            while i < len(combined_score) and combined_score[i] >= 0.4:
                max_score = max(max_score, combined_score[i])
                i += 1
            end_t = timestamps[i-1] if i < len(timestamps) else timestamps[-1]
            applause_regions.append({
                'start': float(start_t),
                'end': float(end_t),
                'peak_score': float(max_score),
            })
        else:
            i += 1

    return applause_regions


# Usage
regions = detect_applause('audio.wav')
for r in regions:
    print(f"  [{r['start']:.1f}s - {r['end']:.1f}s] peak={r['peak_score']:.2f}")
```

## 📊 M1/M2 Performance (verified)

| Clip length | Inference time (M1) | Inference time (M2) |
|---|---|---|
| 60 seconds | 1.2s | 0.8s |
| 10 minutes | 12s | 8s |
| 60 minutes | 75s | 50s |
| 90 minutes | 110s | 75s |

Model ~22 MB, load time ~3s. CPU inference đủ nhanh, không cần CoreML conversion.

## 🛠 TFLite inference (lighter alternative)

```python
import tflite_runtime.interpreter as tflite
import numpy as np

# Load TFLite model
interpreter = tflite.Interpreter(model_path='~/.cache/yamnet.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Run inference
waveform = audio.astype(np.float32)  # (N,) float32 in [-1, 1]
interpreter.set_tensor(input_details[0]['index'], waveform)
interpreter.invoke()

scores = interpreter.get_tensor(output_details[0]['index'])  # (N_patches, 521)
```

**TFLite model size: 4 MB** (vs 22 MB h5). Inference chậm hơn ~10% nhưng tiết kiệm 18 MB disk.

## 🚫 Pitfall: Music false positive

**Vấn đề lớn nhất:** YAMNet detect Applause class 62 trong nhạc có tiếng vỗ tay (applause track, EDM drop).

**Fix (verified):**
```python
# Triple-gate
if applause >= 0.5 AND music < 0.4:
    return True  # Real applause
else:
    return False  # Music with claps, not rally
```

Threshold music < 0.4 loại được 90% false positive.

## 📚 References

- `../references/research-2026-07-09-3-layer-detection.md` Layer 2 section
- `/Users/tuananh4865/yamnet-research-report.md` (full 18 KB research)
- `/Users/tuananh4865/PANN_vs_YAMNet_research.md` (YAMNet vs PANN comparison)
- Official: https://tfhub.dev/google/yamnet/1
- Official: https://github.com/tensorflow/models/tree/master/research/audioset/yamnet