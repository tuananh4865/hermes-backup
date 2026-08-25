# Workspace Convention — /Volumes/Storage-1/Hermes/scratch/

**Added 19/07/2026 (V91)** — Anh explicit: *"Chuyển tmp vào storage-1"*

## Lý do KHÔNG dùng /tmp

- `/tmp` disk cap: **228GB**, đầy nhanh với `work-*/captured-frames/` của HyperFrames render
- 100s clip @ 1080×1920 → **2-3GB captured-frames** per render
- 50 versions → có thể ăn hết /tmp
- `/Volumes/Storage-1` disk cap: **475GB**, còn ~144GB free (19/07/2026)

## Path convention (mọi session phải tuân thủ)

| Loại | Path | Ghi chú |
|---|---|---|
| **Work project** | `/Volumes/Storage-1/Hermes/scratch/hf_<name>_v<n>/` | HyperFrames project gốc, có HTML + assets + render output |
| **Render output** | `/Volumes/Storage-1/Hermes/scratch/hf_<clip>_v<n>/output_silent.mp4` | Silent MP4 trước khi ghép audio |
| **Final ship** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<name>_v<n>_<descriptor>.mp4` | Sau khi ghép audio, copy file đây |
| **Source video** | `/Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4` | Raw HEVC từ Pocket3 |
| **Source cũ (shipped)** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/_archive/ungrouped/` | Bản ship trước đó |
| **Wiki + entity + log** | `/Volumes/Storage-1/Hermes/wiki/` | Knowledge base |
| **PNG samples** | `/Volumes/Storage-1/Hermes/scratch/<project>/samples/` | Verify bằng mắt |

## Hard rule

1. **Mỗi HyperFrames project = folder riêng** `/Volumes/Storage-1/Hermes/scratch/hf_<clip>_v<n>/`
2. **Render output** = `output_silent.mp4` trong folder project
3. **Ship** = copy `output_silent.mp4 + audio.aac` sang `/Volumes/Storage-1/Pocket3/Hermes-Edit/`
4. **Cleanup work-*/captured-frames/** sau mỗi render SUCCESS — giải phóng ~1.5GB
5. **KHÔNG tạo symlink vào /tmp** — sẽ bị confused path

## Migration guide (đã làm 19/07)

Em đã chuyển 52 `hf_*` projects từ `/tmp` → `/Volumes/Storage-1/Hermes/scratch/`:
- 23× `hf_sacduphong_*` (V2-V24)
- 19× `hf_clip0003_*` (V3, V71-V84)
- 9× `hf_clip0006_*` (V4-V12)
- 1× `hf_minimal_pip_test`

Sau migrate: `/tmp` giải phóng 11% disk.

## Disk monitoring

```bash
df -h /Volumes/Storage-1
du -sh /Volumes/Storage-1/Hermes/scratch/* | sort -h | tail -10
```

Khi disk > 80%: cleanup `captured-frames/` của versions cũ không cần.