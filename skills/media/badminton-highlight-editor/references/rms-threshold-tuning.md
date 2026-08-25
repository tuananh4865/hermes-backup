# RMS Threshold Tuning Guide

> **Hướng dẫn chọn ngưỡng RMS phù hợp theo từng loại clip cầu lông.** Threshold sai = miss rally hay hoặc pick nhầm đoạn nhạc nền.

## 📊 Ngưỡng RMS đề xuất theo loại clip

| Loại clip | Threshold | Min duration | Lý do |
|---|---|---|---|
| **Clip không nhạc nền, chỉ crowd + cầu** | `-25 dB` | 2s | Background noise thấp, applause/cầu đập rõ rệt |
| **Clip có nhạc nền nhỏ** | `-22 dB` | 3s | Nhạc nền ~-28dB, applause >-22dB |
| **Clip YouTube highlight (nhạc nền to)** | `-18 dB` | 3s | Nhạc nền loud, cần threshold cao |
| **Clip BWF chính thức (có BLV)** | `-25 dB` | 2s | BLV tạo spike đều, crowd reaction rõ |
| **Clip quay điện thoại (gần micro)** | `-20 dB` | 2s | Micro gần → RMS overall cao hơn |

## 🔍 Cách tune threshold cho clip mới

### Step 1: Lấy baseline RMS distribution

```bash
# Get all RMS values
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav -y
ffmpeg -i audio.wav -af "asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms_log.txt" -f null -

python3 << 'EOF'
import re
rms_vals = []
with open('rms_log.txt') as f:
    for line in f:
        m = re.search(r'RMS_level=([-\d.]+)', line)
        if m:
            try:
                rms_vals.append(float(m.group(1)))
            except ValueError:
                continue

print(f"Min: {min(rms_vals):.1f} dB")
print(f"Max: {max(rms_vals):.1f} dB")
print(f"Mean: {sum(rms_vals)/len(rms_vals):.1f} dB")
print(f"Median: {sorted(rms_vals)[len(rms_vals)//2]:.1f} dB")
print(f"75th percentile: {sorted(rms_vals)[len(rms_vals)*3//4]:.1f} dB")
print(f"90th percentile: {sorted(rms_vals)[len(rms_vals)*9//10]:.1f} dB")
EOF
```

### Step 2: Visualize (optional, matplotlib)

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(20, 5))
plt.plot(rms_vals, linewidth=0.5)
plt.axhline(y=-25, color='r', linestyle='--', label='Default -25 dB')
plt.axhline(y=-22, color='orange', linestyle='--', label='Music -22 dB')
plt.axhline(y=-18, color='purple', linestyle='--', label='Loud music -18 dB')
plt.xlabel('Second')
plt.ylabel('RMS (dB)')
plt.title('Audio Energy Timeline')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('rms_timeline.png', dpi=100)
```

### Step 3: Manual tune

- Nếu **mean RMS** < -25 → clip rất yên → threshold quá cao, GIẢM xuống -28 hoặc -30
- Nếu **90th percentile** > -20 → clip ồn ào → threshold cao hơn (e.g., -22 hoặc -18)
- Nếu **detect quá nhiều spikes** (>30% thời lượng) → tăng threshold lên -22 hoặc tăng min duration lên 4s
- Nếu **detect quá ít spikes** (<5 spikes trong 10 phút) → giảm threshold xuống -28

## 🎯 Adaptive threshold (auto-tune)

```python
def adaptive_threshold(rms_vals, percentile=85):
    """Pick threshold tại Nth percentile (mặc định 85th)."""
    sorted_rms = sorted(rms_vals)
    threshold = sorted_rms[len(sorted_rms) * percentile // 100]
    return threshold

# Usage
rms_data = parse_rms_log('rms_log.txt')
rms_vals = [r for _, r in rms_data]
threshold = adaptive_threshold(rms_vals, percentile=85)
print(f"Adaptive threshold (85th percentile): {threshold:.1f} dB")
```

**Khi nào dùng adaptive:**
- ✅ Clip có mix nhạc nền không đồng đều (ví dụ: 30s đầu không nhạc, 30s sau có nhạc)
- ✅ Clip dài (>30 phút) có nhiều đoạn khác nhau
- ❌ Clip ngắn (<10 phút) — adaptive threshold kém ổn định, dùng fixed

## 🛠 Combined approach: Adaptive + Fixed fallback

```python
def smart_threshold(rms_vals):
    """Adaptive threshold với fallback fixed."""
    sorted_rms = sorted(rms_vals)
    adaptive = sorted_rms[len(sorted_rms) * 85 // 100]
    # Clamp giữa -30 và -18
    smart = max(min(adaptive, -18), -30)
    return smart
```

## 🧪 Real cases (verified 2026-07-09)

| Clip | Threshold | Spike count | Top peak | Top duration |
|---|---|---|---|---|
| `n2884oDI824` (635s, no music) | -25 dB | 75 spikes | -9.7 dB | 19s |
| _TODO: test clip có nhạc nền_ | -22 dB | ? | ? | ? |
| _TODO: test BWF chính thức_ | -25 dB | ? | ? | ? |

## 🚫 Pitfall: Mean volume vs RMS per second

**`ffmpeg volumedetect`** trả mean volume cho toàn clip → KHÔNG dùng để detect spike.

**`ffmpeg astats`** trả RMS per frame → cần `asetnsamples=16000` để 1 sample = 1 giây.

```bash
# ❌ Sai - không có reset, output về mean
ffmpeg -i audio.wav -af astats=metadata=1:reset=0,ametadata=print:key=lavfi.astats.Overall.RMS_level -f null -

# ✅ Đúng - reset mỗi 16000 samples = 1 giây
ffmpeg -i audio.wav -af "asetnsamples=16000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms_log.txt" -f null -
```

## 📚 References

- `../references/research-2026-07-09-3-layer-detection.md` Section 2-3 (RMS analysis)
- `../../scripts/detect_rallies.py` (CLI tool đã implement adaptive threshold)
- `/Users/tuananh4865/badminton-highlight-research/rms-energy-detection.md` Section 5 (limitations + hybrid approach)