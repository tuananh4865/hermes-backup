# Pitfall: Fade In/Out Rule — Voice vs Audio Gốc Video

**Discovered:** 2026-07-26 by Tuấn Anh feedback (verbatim, real use case VXgN3KtMt0M).

---

## 🚨 ROOT CAUSE: Hiểu nhầm "không fade in fade out audio"

### Anh dạy (verbatim 26/07/2026, 2 turn liên tiếp):

> **Turn 1:** *"Không được fade in fade out audio"*

> **Turn 2 (clarify):** *"Ý anh là không được fade in fade out voice thôi còn cách ghép voice vào video phải fade audio của video là đúng rồi"*

### Em hiểu nhầm

Lần đầu em đọc câu 1, em nghĩ **CẢ voice + audio gốc đều không fade** → dùng filter chain ghép voice + audio chạy đồng thời, không có `afade` nào.

Anh clarify ở turn 2: chỉ **VOICE mới không được fade**. **AUDIO GỐC của video PHẢI fade đúng cách** (mute khi voice chạy, fade in sau voice kết thúc).

→ **Đây là filter chain chuẩn**, đã được verify với clip VXgN3KtMt0M (audio gốc có nhạc nền + tiếng cầu lông).

---

## ✅ CORRECT PATTERN

### Voice: KHÔNG fade

```bash
[1:a]aresample=44100,apad=whole_dur=20.97,volume=1.4[voice];
```

- `apad` chỉ pad silence SAU voice (không phải trước)
- KHÔNG `afade` đầu/cuối voice
- Voice instant start (peak -7 to -10 dB ngay frame 0)
- Voice instant stop (peak -inf hoặc silent khi hết)

### Audio gốc video: FADE đúng

```bash
[2:a]aresample=44100,
     volume='if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,8.0),0,if(lt(t,10.0),(t-8.0)/2.0,1)))'
     :eval=frame[audio];
```

**Pattern piecewise volume (4 phase):**

| Phase | Time | Volume | Behavior |
|---|---|---|---|
| 1. Fade out đầu | 0 → 0.3s | `(0.3-t)/0.3` (1 → 0) | Audio gốc tắt dần để voice chiếm |
| 2. Mute (voice chạy) | 0.3 → 8.0s | `0` | Audio gốc im lặng — voice nổi trội |
| 3. Fade in sau voice | 8.0 → 10.0s | `(t-8.0)/2.0` (0 → 1) | Audio gốc dâng lại dần |
| 4. Full | 10.0s+ | `1` | Audio gốc full volume |

### Mix voice + audio

```bash
[voice][audio]amix=inputs=2:duration=longest:dropout_transition=0[mix];
[mix]aresample=44100,pan=stereo|c0=c0|c1=c0[out]
```

---

## ❌ ANTI-PATTERN

### Fade cả voice (sai)

```bash
# ❌ KHÔNG dùng — mất mở đầu/kết thúc câu voice
[1:a]aresample=44100,afade=t=in:st=0:d=0.03,apad=...,volume=1.4[voice];
[1:a]aresample=44100,afade=t=out:st=7.97:d=0.03,apad=...,volume=1.4[voice];
```

### Không fade audio gốc (sai — voice bị chìm)

```bash
# ❌ Voice bị overlap với audio gốc → voice khó nghe
[2:a]aresample=44100[audio];
```

---

## 📊 VERIFY BẰNG VOLUME SAMPLING

```bash
for t in 0.0 0.1 0.3 0.5 1.0 4.0 7.0 7.95 8.0 8.5 9.0 10.0 12.0; do
  ffmpeg -y -ss $t -i output.mp4 -t 0.3 -vn -f wav /tmp/check.wav
  ffmpeg -i /tmp/check.wav -af volumedetect -vn -f null - 2>&1 | grep -E "max_volume|mean_volume"
done
```

**Kết quả đúng:**
- t=0.0s: max=-7 to -10 dB (voice INSTANT, không fade in)
- t=0.3s: max=-7 to -10 dB (audio gốc đã mute = 0)
- t=7.95s: max=-15 dB (voice sắp hết)
- t=8.0s: max=-25 to -30 dB (voice stop, audio gốc vẫn mute)
- t=9.0s: max=-15 to -20 dB (audio gốc đang fade in)
- t=10.0s: max=-8 to -10 dB (audio gốc full)
- t=12.0s+: max=-8 to -10 dB (audio gốc full, FLAT — không gradient)

**Kết quả SAI (em đã làm ban đầu):**
- t=0.0s: max=-7 dB → voice + audio cùng lúc (voice bị chìm ❌)
- t=8.0s: max=-10 dB (audio gốc không mute ❌)

---

## 🎯 VERIFIED CASES (26/07)

### Clip VXgN3KtMt0M (Lin Đan 2008 vs Ly Chong Quây, 20.97s, 720×1280)

| Phase | Filter | Verify |
|---|---|---|
| Voice 0→8s | `aresample + apad + volume=1.4` (no afade) | RMS -7 to -10 dB INSTANT ✅ |
| Audio fade out 0→0.3s | `volume='(0.3-t)/0.3'` | Smooth 1 → 0 ✅ |
| Audio mute 0.3→8s | `volume='0'` | Silent (peak -inf) ✅ |
| Audio fade in 8→10s | `volume='(t-8)/2'` | Smooth 0 → 1 ✅ |
| Audio full 10s+ | `volume='1'` | Peak -8 to -10 dB ✅ |

---

## 📚 QUY TẮC ĐỌC YÊU CẦU CỦA ANH

Khi user nói "không fade in/out", LUÔN **clarify: voice hay audio gốc?** trước khi áp dụng filter chain.

Nếu KHÔNG chắc, hỏi ngắn 1 câu:
> *"Anh không fade voice (giữ nguyên instant) hay không fade cả audio gốc (giữ audio gốc chạy nền)?"*

**Default rule (nếu không hỏi được):** Audio gốc của video thường CẦN fade (mute khi voice chạy, fade in sau). Voice KHÔNG fade. Đây là pattern đã verify work với nhiều clip.

---

## Related

- Skill: `omnivoice-voice-clone` (PITFALL fade rule)
- Skill: `voice-overlay-clip-workflow` (full pipeline)
- Skill: `voice-hook-overlay` (variation với fade in/out audio gốc)
- Memory rule: "Concat Fade PHẢI NHẸ — 30ms" (đã verify 23/07)