---
name: badminton-highlight-editor
description: Cut highlight reels from badminton match videos using hybrid 3-layer audio detection (RMS energy + YAMNet applause + Whisper BLV cross-verify). INDEPENDENT from tiktok-video-editor — focus is on rally detection, not viral editing.
created: 2026-07-09
updated: 2026-07-12
version: 1.3.0
---

# 🏸 Badminton Highlight Editor

> **Độc lập với `tiktok-video-editor`.** Workflow này chuyên cắt highlight rally từ video trận đấu cầu lông dài (15-90 phút) → highlight reel 30-120s.

## 🎯 Khi nào dùng skill này

| Task | Dùng skill này? |
|---|---|
| Cut highlight rally từ video trận đấu cầu lông | ✅ CÓ |
| Edit video TikTok viral bán hàng Yonex | ❌ → dùng `tiktok-product-script` |
| Edit Vlog cầu lông cá nhân | ❌ → dùng `tiktok-video-editor` |
| Tổng hợp rally từ NHIỀU trận | ⚠️ Cần mở rộng (TODO) |

## 🔑 Nguyên tắc cốt lõi (Anh Tuấn Anh dạy 09/07/2026)

> **"Tiếng vỗ tay / hú hét của khán giả + tiếng BLV là cách trực quan nhất để biết một pha rally hay hoặc một điểm cầu hay."**

Hệ thống dựa trên **3 tín hiệu audio song song** để detect rally hay, KHÔNG chỉ dựa vào Whisper BLV (vì nhiều clip không có BLV — chỉ có tiếng cầu đập + crowd).

> **⚠️ WORKFLOW BOUNDARY (anh Tuấn Anh explicit 09/07/2026):** Skill này **ĐỘC LẬP** với `tiktok-video-editor`. Edit highlight cầu lông = class riêng (audio-driven rally detection), KHÔNG trộn với TikTok viral edit (narrative-driven framework).

---

## 📊 Workflow 6 bước (Hybrid 3-Layer Detection)

### Phase 0: Detect BLV presence (CRITICAL FIRST STEP)

**BẮT BUỘC chạy Phase 0 trước Phase 1.** Nếu clip KHÔNG có BLV → SKIP Phase 1, 3, 4 → chỉ dùng Phase 2 (RMS) + Phase 5 (render).

```bash
# Check transcript có BLV hay không — detect 2 hallucinate patterns (VN + EN)
total_lines=$(wc -l < audio.srt)
# VN pattern (verified 09/07): "Hãy đăng ký kênh" loop
hallucinate_vn=$(grep -c "Hãy đăng ký" audio.srt 2>/dev/null || echo 0)
# EN pattern (verified 12/07): "Wow", "That's the", "Long of" repeated on crowd audio
hallucinate_en=$(grep -icE "^Wow\.|^That's the\.$|^Long of" audio.srt 2>/dev/null || echo 0)
hallucinate_lines=$((hallucinate_vn + hallucinate_en))
real_lines=$((total_lines - hallucinate_lines))

if [ "$real_lines" -lt 5 ]; then
  echo "⚠️ No BLV detected → SKIP Whisper layer, use RMS-only workflow"
  HAS_BLV=false
else
  echo "✅ BLV present ($real_lines real lines)"
  HAS_BLV=true
fi
```

**Tại sao quan trọng:**
- Test case `n2884oDI824` (09/07/2026): 100% Whisper VN output là "Hãy đăng ký kênh" hallucinate (21/21 dòng) — VN pattern
- Test case `TCG9oKtmaQE` Indonesia Open Final (12/07/2026): Whisper EN hallucinate MASSIVELY — 1000+ dòng "Wow"/"That's the"/"Long of the back line" loops trên audio crowd. Transcript vẫn sinh ra nhưng text KHÔNG dùng được để BLV scoring → CHỈ dùng RMS làm ground truth.
- **Lesson 12/07 (NEW):** Whisper medium-mlx EN hallucinate KHÔNG fix được bằng anti-hallucinate flags. Ngay cả với `--condition-on-previous-text False --no-speech-threshold 0.6`, audio crowd vẫn bị loop "Wow"/"That's the"/"Long of the back line" hàng trăm lần. → Khi clip có crowd noise mạnh (BWF TV, giải đấu lớn), Phase 1 vẫn chạy được nhưng Phase 4 (BLV scoring) PHẢI skip.

### Phase 1: Transcribe (Whisper) — CHỈ chạy nếu HAS_BLV=true
```bash
# Whisper medium-mlx (verified clean cho VN, không hallucinate khi dùng default)
mlx_whisper --model mlx-community/whisper-medium-mlx \
  --language vi \
  --output-format srt \
  --output-dir . audio.wav

# ⚠️ Anti-hallucinate flags (dùng khi clip có nhiều silence/crowd noise):
mlx_whisper --model mlx-community/whisper-medium-mlx \
  --language vi \
  --condition-on-previous-text False \
  --no-speech-threshold 0.6 \
  --output-format srt \
  --output-dir . audio.wav
```

**Pitfall #1:** Whisper hallucinate "Hãy đăng ký kênh" / "Subscribe to channel" khi audio silence/intro YouTube. → Phát hiện bằng `grep -c "Hãy đăng ký"` > 30% tổng dòng → dùng anti-hallucinate flags.

**Pitfall #2:** Whisper KHÔNG detect được applause/cheer (chỉ detect được BLV speech). Vì vậy Layer 2 (RMS) và Layer 3 (YAMNet) là BẮT BUỘC khi có BLV, hoặc chỉ RMS khi không có BLV.

### Phase 2: RMS Energy Analysis (Layer 1 - Fast Pre-filter)
```bash
# Extract audio 16kHz mono (cho YAMNet + librosa)
ffmpeg -i source.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav -y

# Get RMS per second
ffmpeg -i audio.wav -af "asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms_log.txt" -f null -
```

**Threshold khuyến nghị (verified 09/07 + 12/07/2026):**

| Loại clip | Spike threshold | Min duration | Verified test case |
|---|---|---|---|
| Clip không nhạc nền, chỉ crowd + cầu | `-25 dB` | 2s | n2884oDI824 (09/07) |
| Clip có nhạc nền nhỏ | `-22 dB` | 3s | — |
| Clip YouTube highlight (nhạc nền to) | `-18 dB` | 3s | — |
| **Clip BWF chính thức (có BLV EN, music bed nhẹ)** | **`-25 dB` conservative / `-27 dB` catch thêm rallies** | **2s** | **TCG9oKtmaQE Indonesia Open Final (12/07)** |
| Clip quay điện thoại (gần micro) | `-20 dB` | 2s | — |

**Threshold tuning rule (12/07 lesson):**
- BWF TV / giải chính thức → start `-25 dB` (conservative, catch 6-7 rallies chắc chắn)
- Nếu muốn nhiều rallies hơn (catch thêm middle-game) → giảm `-27 dB` (thêm 2-4 rallies, có thể false positive)
- KHÔNG giảm dưới `-30 dB` — quá nhiều noise từ serve sounds, BLV small speech
- **Empirical (12/07 test):** -25 dB → 6 rallies (93s). -27 dB ước tính → 9-10 rallies (~120-130s).

**Xem chi tiết:** `references/rms-threshold-tuning.md` (adaptive threshold + visualize).

**Pitfall #3:** `ffmpeg astats` returns `-inf` cho 1-channel audio → dùng `volumedetect` cho mean volume check, KHÔNG dùng cho spike detection.

```bash
# ✅ Đúng - reset mỗi 16000 samples = 1 giây
ffmpeg -i audio.wav -af "asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms_log.txt" -f null -

# ❌ Sai - không có reset, output về mean toàn file
ffmpeg -i audio.wav -af "astats=metadata=1:reset=0,..." -f null -
```

**Detect applause spikes (Python logic xem `scripts/detect_rallies.py`):**
```python
SPIKE_THRESHOLD = -25.0  # dB - tune per clip (xem references/rms-threshold-tuning.md)
MIN_DURATION = 2         # seconds

spikes = []
i = 0
while i < len(rms_data):
    if rms_data[i][1] > SPIKE_THRESHOLD:
        start_t = rms_data[i][0]
        peak = rms_data[i][1]
        while i < len(rms_data) and rms_data[i][1] > SPIKE_THRESHOLD:
            peak = max(peak, rms_data[i][1])
            i += 1
        end_t = rms_data[i-1][0]
        duration = end_t - start_t + 1
        if duration >= MIN_DURATION:
            spikes.append((start_t, end_t, peak, duration))
    i += 1
```

**Pitfall #4:** Parse `pts_time` và `RMS_level` ở 2 dòng RIÊNG BIỆT trong ffmpeg log → phải parse line-by-line, KHÔNG regex multi-line.

### Phase 3: YAMNet Applause Detection (Layer 2 - Precision)
*(Optional - requires `tensorflow_hub` install ~600MB)*

**Class IDs (verified từ official `yamnet_class_map.csv`):**
- `Applause` = **62**
- `Cheering` = **61**
- `Clapping` = **58**
- `Crowd` = **64**

**Logic:**
```python
# Threshold: YAMNet score ≥ 0.5 cho Applause hoặc Cheering
# Triple-gate: (Applause ≥ 0.5 OR Cheering ≥ 0.5) AND RMS > -25 dB AND Music < 0.4
```

**Speed:** Scan 60-min video trên M1 ~3-5 phút (TFLite) hoặc ~30s (nếu dùng TFLite model nhỏ 4MB).

**Xem chi tiết:** `references/yamnet-class-ids.md` (full class mapping + Python inference code).

### Phase 4: Whisper BLV Cross-Verify (Layer 3 - Bonus) — CHỈ nếu HAS_BLV=true
*(Optional - chỉ áp dụng khi clip CÓ BLV nói tiếng Việt)*

**BLV keyword list (tier-based scoring):**

| Tier | Keywords | Score boost |
|---|---|---|
| 🔥 Hot (BLV scream) | "vào", "đỉnh", "hay quá", "quá đỉnh", "tuyệt vời", "không thể tin", "ngoạn mục", "xuất sắc" | +3 |
| ⚡ Energetic | "đẹp", "nhanh", "mạnh", "hay", "giỏi", "wow", "ồ" | +1.5 |
| 🎯 Negative (BỎ) | "tiếc", "hỏng", "lỗi", "sai", "trượt", "out" | → None |
| 🎬 Setup (transitional) | "bây giờ", "tiếp theo", "xem", "đợi" | -1 |

**Xem chi tiết:** `references/blv-keyword-list.md` (full list + Python `rally_score()` function).

**Nếu clip KHÔNG có BLV** (chỉ có crowd + tiếng cầu) → BỎ QUA layer này, dùng RMS + YAMNet là đủ.

### 🎯 Phase 4.5: EXTEND HIGHLIGHT BOUNDARIES (CRITICAL - 09/07/2026)

**Anh's rule (verbatim 09/07):**
> *"Cố gắng lấy hết một điểm highlight luôn chứ không cắt giữa chừng nữa mà phân tích từ điểm có tiếng khán giả hú hét đến khi có khoảng lặng ở cả 2 phía... khoảng lặng là một khoảng lặng dài không nghe tiếng cầu lông chạm vợt ấy!"*

**Logic:** Mỗi highlight phải là **MỘT ĐIỂM TRỌN VẸN**:
- **START** = khoảng lặng TRƯỚC tiếng crowd hò hét (không có tiếng shuttle đập vợt)
- **END** = khoảng lặng SAU khi crowd im (không có tiếng shuttle đập vợt)

**Algorithm:**
```python
APPLAUSE_DB = -25.0   # Crowd hò hét
QUIET_DB = -32.0      # Khoảng lặng (no shuttle)
MAX_EXTENSION = 5     # Giới hạn max extension mỗi side = 5s

# 1. Detect applause spikes (RMS > APPLAUSE_DB)
# 2. For each spike, walk BACKWARD until QUITE region (RMS < QUIET_DB)
#    hoặc MAX_EXTENSION giây trước spike
# 3. Walk FORWARD until next QUITE region
#    hoặc MAX_EXTENSION giây sau spike
# 4. Nếu giữa 2 spike không có quiet → midpoint
```

**Tại sao cần MAX_EXTENSION:**
- Clip highlight dày đặc → spikes liên tiếp nhau, không có quiet thật
- MAX_EXTENSION giới hạn an toàn, không cắt nguyên 1 rally khác

**Updated score formula:** Ưu tiên full duration (point trọn vẹn)
```python
score = peak_norm × 0.4 + full_duration_norm × 0.6
```

### 🎯 Phase 4.6: POST-MERGE CEREMONY FILTER (NEW - 12/07/2026)

**Vấn đề:** Sau Phase 4.5 extend boundaries, rally dài nhất thường là ENDING + ceremony (90s+ có music bed + crowd + interview + trophy lift), KHÔNG phải rally. Test case `TCG9oKtmaQE` Indonesia Open Final: spike 90s ở 1791-1881s là toàn bộ post-match ceremony, không có rally nào.

**Filter rule:**
```bash
# Filter rallies > 60s — likely ceremony, không phải rally
awk -F'\t' '$4 < 60 {print}' top_rallies.txt > keep_rallies_final.txt
```

**Tại sao 60s:** Rally cầu lông dài nhất thực tế hiếm khi > 60s (BLV thường đếm "31-shot rally" là max). 90s+ = ceremony chắc chắn. Threshold 60s là safe boundary.

**Edge case:** Nếu match đặc biệt dài (5-game thriller), có rally thật 50-60s → giữ lại bằng tay sau khi xem qua.

### 🛑 Phase 4.7: MANDATORY VISUAL VERIFICATION GATE (CRITICAL - 12/07/2026, added by adversarial verifier)

**Phát hiện 12/07/2026 bởi independent verifier:** Phase 4.6 filter KHÔNG đủ. Test case `TCG9oKtmaQE` Indonesia Open Final đã pass Phase 4.5 + 4.6 nhưng OUTPUT là 4 ceremony frames + 2 player-introduction frames trong 6 rally windows. **Không một frame nào cho thấy badminton play.** Lý do: `peak × 0.4 + duration × 0.6` scoring formula CHỌN ceremony/sustained-loud (76s sustained) thay vì rallies thật (5-15s transient) vì ceremony có peak_norm = 0.21 và dur_norm = 1.0 (=0.685 score) cao hơn rally 14s thật (score 0.65).

**BẮT BUỘC chạy Phase 4.7 sau Phase 5 (render) trước khi khai báo highlight reel đã xong:**

#### 4.7.1 Visual ground truth (1 frame per rally from source.mp4)

```bash
mkdir -p /tmp/verify-rallies
# Filter file thường có thứ tự: r1, r2, r3, r4, r5, r6 với offset từ sum prior durations
# Đơn giản hơn: render trực tiếp từ source.mp4 với cùng trim như filter.txt
ffmpeg -ss <rally1_src_t> -i source.mp4 -frames:v 1 -y /tmp/verify-rallies/rally1.png
ffmpeg -ss <rally2_src_t> -i source.mp4 -frames:v 1 -y /tmp/verify-rallies/rally2.png
# ... 6 lần, dùng vision_analyze tool để check mỗi frame
```

**Tiêu chí PASS (≥ 4 of 6 frames):**
- Frame HIỂN THỊ players trên court với action posture
- Court markings visible (lines, net)
- KHÔNG chỉ là podium, anthem, sponsor banner, "WONDERFUL FINISH" countdown, trophy lift, hoặc player waving

**Từ chối nếu:**
- ≥ 3 frames là crowd-only, sponsor-only, ceremony, post-match, hoặc player-portrait B-roll
- Có frame nào hiển thị "WONDERFUL FINISH" / "Please welcome ..." / country flag anthems

#### 4.7.2 Sharp transient peak count (shuttle hit signature)

Shuttle hit = sharp RMS peak với quiet immediately before AND after (>30dB swing trong <2s).

```python
# Trong window [rally_start, rally_end], đếm sharp transients:
sharp_count = 0
for i, (t, rms) in enumerate(rms_data):
    if rally_start <= t <= rally_end and rms > -25:
        prev_db = rms_data[max(0, i-1)][1]
        next_db = rms_data[min(len(rms_data)-1, i+1)][1]
        if (prev_db < -30 and rms - prev_db > 30) or \
           (next_db < -30 and rms - next_db > 30):
            sharp_count += 1
```

**Tiêu chí PASS:** ≥ 60% of rally windows contain ≥ 1 sharp transient.

Nếu fail → scoring formula picks ceremony/sustained-loud hơn rallies, scoring cần fix.

#### 4.7.3 BLV text-window cross-check (KHI transcript reliable)

Nếu transcript reliable (verified not hallucinate bằng Phase 0) → check xem rally window có chứa BLV reaction keywords không. Trong test case TCG9oKtmaQE transcript is 71% hallucinate nên keyword check unreliable, skip.

Reliable transcripts → keywords: "amazing", "fantastic", "brilliant", "incredible", "what a", "long rally", "extended rally", "winner", "smash", "kills it".

#### 4.7.4 Report & write verdict file

Sau verification, **BẮT BUỘC write** `highlight_<id>_ADVERSARIAL_VERDICT.md` cạnh output file với:
- ✅ File integrity check (ffprobe exit 0, codec/resolution/duration)
- ✅/❌ Visual frame count (≥4/6 active play)
- ✅/❌ Sharp transient count (≥60% windows with transients)
- ✅/❌ Distribution check (rally positions across match time, not clustered)
- **VERDICT: PASS / PARTIAL_PASS / FAIL**

#### 4.7.5 Fix scoring formula (chỉ khi Phase 4.7.2 FAIL)

```python
# ❌ OLD (inverts priority - prefers ceremony over real rallies)
def score_old(peak, duration):
    peak_norm = (peak - SPIKE_DB) / 10.0  # -25 → 0, -15 → 1.0
    dur_norm = min(1, duration / 15.0)
    return peak_norm * 0.4 + dur_norm * 0.6

# ✅ NEW (rewards brief-but-loud transients like shuttle hits + crowd peaks)
def score_new(peak, duration):
    peak_norm = (peak - SPIKE_DB) / 10.0  # -25 → 0, -15 → 1.0
    peak_norm = max(0, min(1, peak_norm))
    # Higher peak norm → HIGHER score, long duration → LOWER score
    # (rally should be 5-15s, >30s is suspect)
    dur_penalty = 1.0 / (1.0 + duration / 5.0)  # 5s → 0.5, 15s → 0.25, 60s → 0.077
    return peak_norm * 0.7 + dur_penalty * 0.3
```

**Empirical test (TCG9oKtmaQE @ 12/07):**
- 5s rally at -22dB: OLD = (0.3 × 0.4) + (0.33 × 0.6) = **0.318** ❌ ranked LOW
- 5s rally at -22dB: NEW = (0.3 × 0.7) + (0.5 × 0.3) = **0.360** ✓ but still modest
- 90s ceremony at -22dB: OLD = (0.3 × 0.4) + (1.0 × 0.6) = **0.720** ❌ ranked TOP
- 90s ceremony at -22dB: NEW = (0.3 × 0.7) + (0.052 × 0.3) = **0.226** ✓ ranked LOW
- 14s rally at -22dB: NEW = (0.3 × 0.7) + (0.263 × 0.3) = **0.289**
- 14s genuine peak at -22dB with 1 sharp transient: add bonus +0.2 for transient → 0.489

**Rec:** combine NEW formula + sharp-transient bonus:
```python
def score_v3(peak, duration, sharp_count):
    base = score_new(peak, duration)
    transient_bonus = min(0.3, sharp_count * 0.05)  # each transient adds 0.05, capped 0.3
    return base + transient_bonus
```

#### 4.7.6 Honest Test Case 2 verdict (12/07 adversarial verdict)

PREVIOUSLY this skill claimed "verified Test Case 2 PASS". Independent adversarial verification 12/07/2026 found:

- **File integrity:** ✅ 28.1MB, H.264 1280x720@30fps, AAC 44.1kHz, decodes cleanly
- **Spec compliance:** ✅ H.264/AAC 1280x720 horizontal as spec'd
- **BLV transcript:** ❌ 1106/1558 entries (71%) hallucinate "That's the". Transcript KHÔNG dùng được cho verification.
- **Rally content:** ❌ **FAIL** — 0 of 6 windows show active play. 4 windows are post-match/finish graphic/ceremony, 2 are player introductions.
- **Distribution:** ❌ Thiếu 76% match (208s → 2881s = 44.5 phút = 76% match không có rally)
- **Real play missed:** t=1774s game-deciding moment (Christie 19-20) was scored 0.712 and filtered as ceremony bởi Phase 4.6

**Final VERDICT:** Old "verified Test Case 2" section is INCORRECT. Highlight reel not shippable. After implementing Phase 4.7 + scoring formula fix, redo Test Case 2.

### Phase 5: Render Highlight Reel (FFmpeg)
```bash
# Cut top-N rallies thành 60-120s highlight
# Score formula: peak_db_norm × 0.6 + duration_norm × 0.4

ffmpeg -y -i source.mp4 \
  -filter_complex_script filter.txt \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  highlight_v1.mp4
```

**filter.txt template:**
```
[0:v]trim=00:13.000:00:23.000,setpts=PTS-STARTPTS[v0];
[0:a]atrim=00:13.000:00:23.000,asetpts=PTS-STARTPTS[a0];
[0:v]trim=03:16.000:03:28.000,setpts=PTS-STARTPTS[v1];
[0:a]atrim=03:16.000:03:28.000,asetpts=PTS-STARTPTS[a1];
[0:v]concat=n=2:v=1:a=1[outv][outa]
```

**Pitfall #5:** Padding cuối mỗi rally dùng `atrim` chính xác (không thêm padding) — boundary effects có thể tạo 0.04s silence gap. Nếu cần padding thêm, dùng `apad` filter cuối cùng.

---

## 🛠 Scripts (xem `scripts/`)

| Script | Mục đích |
|---|---|
| `detect_rallies.py` | Full pipeline: extract audio → RMS → YAMNet (TODO) → BLV → render |

**CLI usage:**
```bash
python3 ~/.hermes/skills/media/badminton-highlight-editor/scripts/detect_rallies.py \
  /path/to/match.mp4 \
  --threshold -25 \
  --min-duration 2 \
  --top 6 \
  --output /path/to/highlight.mp4
```

## 📚 References (xem `references/`)

| File | Mục đích | Size |
|---|---|---|
| `research-2026-07-09-3-layer-detection.md` | Research 3-layer trade-offs (YAMNet vs PANN vs RMS) | ~12 KB |
| `yamnet-class-ids.md` | Mapping 521 AudioSet classes → badminton-relevant | ~5 KB |
| `blv-keyword-list.md` | BLV keywords VN theo tier + scoring formula | ~5 KB |
| `rms-threshold-tuning.md` | Hướng dẫn tune threshold theo từng loại clip | ~5 KB |
| `session-2026-07-12-bwf-indo-open-final-en-hallucinate.md` | Test case #2 (BWF Indonesia Open Final) — EN hallucinate pattern + ceremony filter | ~4 KB |
| `session-2026-07-12-adversarial-fail-and-phase-47-gate.md` | Independent adversarial verifier 12/07: scoring formula inverted, 4.7 visual gate added, full evidence log | ~6 KB |

## 📝 Pitfalls (đã verified)

| # | Pitfall | Fix |
|---|---|---|
| 1 | Whisper hallucinate "Hãy đăng ký kênh" loop | `--condition-on-previous-text False --no-speech-threshold 0.6` |
| 2 | Whisper hallucinate "bắt đầu" x 100+ khi BLV silent | Same flags as #1 + verify RMS > -40 dB |
| 3 | `ffmpeg astats` returns `-inf` cho 1-channel audio | Dùng `volumedetect` cho mean check, KHÔNG dùng cho spike |
| 4 | RMS sample size sai khi dùng 44100 vs 16000 | `asetnsamples=16000` cho 16kHz audio |
| 5 | ffmpeg `astats` output pts_time và RMS trên 2 dòng riêng | Parse line-by-line, không regex multi-line |
| 6 | Clip không BLV → Whisper layer vô dụng | Phase 0 detection → skip Phase 1, 3, 4 nếu no BLV |
| 7 | Nhạc nền YouTube highlight tăng RMS giả | Tune threshold cao hơn (`-18 dB`) hoặc detect Music < 0.4 (YAMNet) |
| **8 (NEW 12/07)** | **Whisper EN hallucinate "Wow"/"That's the"/"Long of the back line" loop hàng trăm lần trên BWF TV crowd audio — KHÔNG fix được bằng anti-hallucinate flags** | **Phase 0 detect hallucinate_en pattern. Skip Phase 4 BLV scoring. Dùng RMS làm ground truth duy nhất. Accept ít rallies hơn thay vì dùng transcript text bị polluted.** |
| **9 (NEW 12/07)** | **Rally 90s+ sau Phase 4.5 extend thường là ENDING + ceremony, không phải rally** | **Phase 4.6 filter `awk '$4 < 60'`. Rally thật hiếm khi > 60s.** |
| **10 (CRITICAL — 12/07, found by independent adversarial verifier)** | **Scoring formula `peak × 0.4 + duration × 0.6` systematically ranks CEREMONY/MUSIC (long sustained loudness) ABOVE real rallies (brief transient peaks from shuttle hits). A 76s ceremony at -22.9dB scores 0.685; a 5-15s genuine rally at same peak scores 0.50-0.65. Algorithm INVERTS the priority.** | **Phase 4.7 mandatory verification gate — see below. NEVER trust the score alone. Always (a) extract 1 frame per rally from source.mp4 and visually confirm active play, (b) check `rms_log.txt` for sharp transient peaks (>30dB swing in <2s) inside each window, (c) replace the formula with `peak × 0.7 + (1 / (1 + duration/5)) × 0.3` if not already done.** |
| **11 (CRITICAL — 12/07)** | **"RMS peak -22 to -24 dB" is NOT sufficient evidence of a rally. Ceremony, music bed, anthem, and post-match speeches ALSO peak at -22 to -25 dB.** | **Phase 4.7.2: count sharp transient peaks (shuttle hits) per window. ≥60% of windows must contain ≥1 transient, else FAIL. Crowd cheering without shuttle hits = ceremony, not rally.** |
| **12 (CRITICAL — 12/07)** | **Player introduction ceremony has audio peaks that match rally peaks. PA announcer reading "Please welcome Jonathan Christie!" with crowd cheering scores IDENTICALLY to a 30-shot rally in `detect_rallies.py`.** | **Phase 4.7.1: sample frame MUST show court + active play. If frame shows podium, flag, anthem, sponsor, or B-roll player portrait → not a rally. Visual ground truth is final.** |

## 🎯 Verified workflows (09/07 + 12/07/2026)

**Test case 1:** `https://youtu.be/n2884oDI824` (635s clip, NO BLV) — 09/07/2026
- ✅ Phase 0: BLV detection → no BLV → skip Phase 1, 3, 4
- ⏭️ Phase 1: Whisper default → 21 dòng "Hãy đăng ký" hallucinate (would have been skipped if Phase 0 ran first)
- ✅ Phase 2: RMS analysis → 75 spikes detected, top 15 ranked
- ⏭️ Phase 3: YAMNet (skipped, no model install in test env)
- ⏭️ Phase 4: BLV cross-verify (skipped, no BLV in clip)
- ✅ Phase 5: Top 4 rallies → 71s highlight reel (3.8 MB)

**Output:** `~/Movies/badminton-highlights/n2884oDI824_V1_highlight_4rallies.mp4`

**Audio quality check:** mean volume -20.4 dB (source) → -18.1 dB (highlight), delta 2.3 dB ⚠️ (acceptable - do top rallies lọc từ loud regions).

---

**Test case 2:** `https://youtu.be/TCG9oKtmaQE` POLYTRON Indonesia Open 2026 FINAL (58:05 clip, BWF TV with EN BLV) — 12/07/2026
- ✅ Phase 0: BLV detection → detected BLV (6232 lines) BUT `hallucinate_en` pattern detected (1000+ "Wow"/"That's the"/"Long of" loops) → SKIP Phase 4 BLV scoring
- ⚠️ Phase 1: Whisper EN → 6232 lines, MASSIVE hallucinate pollution (chỉ dùng để confirm match intro/outro context, KHÔNG dùng text scoring)
- ✅ Phase 2: RMS analysis (-25 dB conservative) → 15 spike candidates
- ⏭️ Phase 3: YAMNet (skipped, no model install in test env)
- ⏭️ Phase 4: BLV scoring SKIPPED do hallucinate_en detected
- ✅ Phase 4.5: Extend boundaries → 7 rallies after merge
- ✅ Phase 4.6: Filter > 60s → 6 rallies (93s) — ceremony 90s loại bỏ
- ❌ Phase 4.7 (added retroactively by adversarial verifier): **FAILED**
  - 4.7.1 visual frames: 0 of 6 windows show active play. t=200s = Canadian flag ceremony, t=124s = player-intro pyrotechnics, t=35s = "WONDERFUL FINISH" countdown, t=63s = award podium, t=78s = player waving, t=86s = broadcast B-roll player portrait.
  - 4.7.2 sharp transients: only 1 of 6 windows contains a sharp transient peak. Other 5 are sustained-loud (ceremony signature).
  - 4.7.4 verdict: **FAIL** — output is not a badminton highlight reel.
- Root cause: scoring formula `peak × 0.4 + duration × 0.6` overweights ceremony/sustained-loud; missed real rallies (t=1774s score 19-20 game-deciding moment was scored 0.712 and incorrectly classified as ceremony by Phase 4.6)

**Output:** `/Volumes/Storage-1/Tiktok-Tuan-Anh/badminton-highlights/TCG9oKtmaQE_V1_highlight_6rallies.mp4` ❌ **NOT SHIPPABLE** — needs Phase 4.7 gate + scoring formula fix before re-rendering.

**Adversarial verdict file:** `ADVERSARIAL_VERDICT.md` (full evidence log written next to output).

## 🔗 Related

- **Sister skill:** `~/.hermes/skills/media/tiktok-video-editor/SKILL.md` (general TikTok editing — KHÔNG dùng cho highlight cầu lông)
- **Sister skill:** `~/.hermes/skills/media/tiktok-product-script/SKILL.md` (TikTok bán hàng Yonex — KHÔNG dùng cho highlight cầu lông)
- **Research files:**
  - `/Users/tuananh4865/yamnet-research-report.md` (18 KB, 9 sources)
  - `/Users/tuananh4865/badminton-highlight-research/rms-energy-detection.md` (41 KB, 19 sources)
  - `/Users/tuananh4865/PANN_vs_YAMNet_research.md` (22 KB, 8 sources)