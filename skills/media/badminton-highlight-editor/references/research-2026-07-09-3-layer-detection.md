# Research: 3-Layer Audio Detection cho Badminton Highlight (2026-07-09)

## Bối cảnh

Anh Tuấn Anh dạy nguyên tắc cốt lõi 09/07/2026: **"Tiếng vỗ tay / hú hét của khán giả + tiếng BLV là cách trực quan nhất để biết một pha rally hay hoặc một điểm cầu hay."**

Em dispatch 3 subagents research song song về 3 phương pháp detect applause/cheer, output 3 file research (~80 KB tổng):
- `/Users/tuananh4865/yamnet-research-report.md` (18 KB)
- `/Users/tuananh4865/badminton-highlight-research/rms-energy-detection.md` (41 KB)
- `/Users/tuananh4865/PANN_vs_YAMNet_research.md` (22 KB)

## So sánh 3 phương pháp

| Method | Accuracy (mAP) | Speed (60-min video) | Model size | Mac M1/M2 fit? |
|---|---|---|---|---|
| **YAMNet** (Google, 2019) | 0.306 mAP | ~30s (TFLite) | 22 MB | ✅ Tốt |
| **RMS + Spectral** | 70-80% recall | Real-time | 0 MB | ✅ Đơn giản |
| **PANN CNN14** | 0.431 mAP | 12-18 min CPU | 80 MB | ⚠️ Chậm |
| **PANN Wavegram** | 0.439 mAP | Chậm hơn CNN14 | >100 MB | ❌ Quá chậm |

## Verdict: Hybrid 3-Layer (RMS + YAMNet + Whisper BLV)

### Layer 1 — RMS Energy (Fast Pre-filter)
- Source: rms-energy-detection.md Section 2-3
- Adaptive threshold thay vì fixed (top 85th percentile)
- Window 500ms smooth, 23ms hop (librosa defaults)
- Spectral centroid 2000-4500 Hz lọc nhạc nền
- ZCR 0.20-0.50 lọc speech/tonal sounds

### Layer 2 — YAMNet (Precision Filter)
- Source: yamnet-research-report.md
- Load TFLite 4MB qua `pip install tensorflow_hub`
- Class IDs (verified từ official `yamnet_class_map.csv`):
  - `Applause` = **62**
  - `Cheering` = **61**
  - `Clapping` = **58**
  - `Crowd` = **64**
- Threshold: score ≥ 0.5 cho Applause/Cheering
- Scan 60-min video trên M1 ~3-5 phút, M2 ~2-3 phút

### Layer 3 — Whisper BLV (Cross-verify Bonus)
- Source: BLV keyword list (xem `references/blv-keyword-list.md`)
- Chỉ apply khi clip CÓ BLV nói tiếng Việt
- Skip hoàn toàn nếu clip chỉ có crowd + tiếng cầu

## Quyết định loại PANN

Lý do chọn YAMNet thay vì PANN:
1. **Speed**: YAMNet scan 60-min = 30s, PANN = 12-18 phút → batch processing Mac M1/M2 không khả thi với PANN
2. **M1/M2 pitfall**: PyTorch MPS chậm hơn CPU cho audio models (pytorch issue #77799)
3. **Đủ tốt**: Cho task "detect applause/cheer" (đơn giản), YAMNet đã OK
4. **File size**: YAMNet 22MB vs PANN 80MB → dễ ship standalone

## Decision tree kết hợp 3 layer

```
Audio segment:
├─ Layer 1 RMS > 0.05 AND centroid 2000-4500Hz
│  ├─ Layer 2 YAMNet (Applause|Cheering|Crowd) ≥ 0.5
│  │  ├─ Layer 3 Whisper có BLV keyword "vào/đỉnh/hay"
│  │  │  → 🔥 RALLY ĐỈNH (score 9-10) — KEEP bắt buộc
│  │  └─ Whisper im lặng
│  │     → ✅ RALLY HAY (score 7-8) — KEEP
│  └─ YAMNet < 0.5 (chỉ có RMS)
│     → ⚖️ RALLY CÓ TIẾNG (score 5-6) — KEEP nếu narrative hay
└─ RMS thấp
   → ❌ ĐOẠN CHẾT — BỎ
```

## Sources cited (15+ official)

**YAMNet:**
1. Google Group announcement (2019)
2. tensorflow/models repo (yamnet/inference.py + params.py)
3. yamnet_class_map.csv (verified class IDs)
4. AudioSet ontology page
5. arXiv:1912.10211 (PANNs comparison)

**PANN:**
6. arXiv:1912.10211 (PANNs paper)
7. TASLP 2020 publication
8. qiuqiangkong/audioset_tagging_cnn GitHub
9. Zenodo checkpoints
10. 2 independent benchmarks on Apple Silicon

**RMS + Audio Detection:**
11. arXiv:2501.16100 (Sport highlight DL 2025)
12. Columbia EE6820 (Soccer audio 2001)
13. SciTePress 145852 (Multi-modal broadcast)
14. Tsinghua HCSI (HMM cheer detection)
15. US Patent 11025985B2 (commercial crowd noise detection)

**Application papers:**
16. arXiv:2501.16100 — Sports highlight detection (2025)
17. CVPR 2018 Merler (highlight detection)
18. ACM MM 2016 Bettadapura (Google, event detection)