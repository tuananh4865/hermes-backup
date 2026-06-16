# Motion Analysis & AI Video Prompt Generation

This reference covers the advanced workflow when Tuấn Anh asks to "phân tích chuyển động" (analyze movement) or "tạo prompt video tương tự" (create similar video prompt) — added after the 2026-06-16 TikTok Shoppable OOTD session.

## When to use this workflow

**Trigger phrases:**
- "phân tích chuyển động của mẫu"
- "analyze movement / pose / camera angle"
- "góc máy", "camera movement"
- "tạo prompt video tương tự", "replicate this video"
- "bắt chước hành động chính xác từng frame"
- "Veo 3", "Kling", "Runway", "Sora" (AI video tools)

## The 4-Phase Workflow

### Phase 1: Dense Frame Extraction

For motion analysis, 1fps is too sparse. Use 2fps for short videos (<60s):

```bash
cd /tmp/frame-analysis
ffmpeg -i compressed.mp4 -vf "fps=2" -q:v 2 dense_frame_%03d.jpg -y
# 17s video → 34 frames
# 60s video → 120 frames
```

For long videos (>2min), use sparse sampling instead:
```bash
ffmpeg -i compressed.mp4 -vf "fps=1/2" -q:v 2 dense_frame_%03d.jpg -y  # 1 frame per 2s
```

### Phase 2: Motion Detection (ffmpeg scene_score)

**The key insight:** Vision models analyze one frame at a time. They CANNOT see motion. To know when the subject actually moves, use ffmpeg's scene detection:

```bash
ffmpeg -i compressed.mp4 -vf "select='gte(scene\,0)',metadata=print" -an -f null - 2>&1 | grep "scene_score"
```

**Output example (17s video, 1020 frames at 60fps):**
```
lavfi.scene_score=0.000000  (frame 0)
lavfi.scene_score=0.003593  (frame 1)
lavfi.scene_score=0.027820  (frame 2)  ← motion burst
lavfi.scene_score=0.002528  (frame 3)  ← static
lavfi.scene_score=0.026357  (frame 4)  ← motion burst
...
```

**Score interpretation:**
| Score | Meaning | Inference |
|-------|---------|-----------|
| 0.000-0.005 | Near-static | Pose hold, breathing only |
| 0.020-0.045 | Medium motion | Hand raise, body sway, weight shift |
| 0.060-0.080 | Peak motion | Key signature pose, turn, step |
| 0.100+ | Scene change | Cut, transition, large gesture |

**Pattern recognition:**
- **Alternating static (0.002) + burst (0.025-0.045)** = rhythmic posing every 0.25s
- **Single peak (0.07+)** = key signature pose
- **Decreasing scores near end** = "settle" pose with slow zoom in
- **Continuous low (0.005-0.010)** = natural breathing/micro-motion only

### Phase 3: Pose Analysis (Structured Prompt)

For each KEY frame (identified via scene_score peaks), use this prompt:

```
Phân tích motion frame này trong timeline. Tôi cần biết CHÍNH XÁC:
1. Body pose (đứng thẳng, nghiêng trái/phải, xoay bao nhiêu độ, weight trên chân nào)
2. Tay trái (vị trí: eo, bụng, đùi, buông thõng; ngón tay: duỗi/co; cầm gì)
3. Tay phải (cầm điện thoại che mặt ở vị trí nào, cao/thấp, xoay bao nhiêu)
4. Đầu & mặt (nghiêng, cúi, ngẩng; điệu bộ)
5. Vai & hông (thẳng hay lệch, mở rộng hay thu)
6. Chân (dáng đứng, bước rộng/hẹp)
7. Camera angle (góc từ dưới lên/ngang/từ trên; khoảng cách; zoom/dolly)
8. Lighting (ánh sáng từ hướng nào, shadow ở đâu)
9. Frame này khác frame trước ở điểm nào? (motion delta)

Trả lời cực ngắn: POSE: ... | TAY_T: ... | TAY_P: ... | ĐẦU: ... | VAI: ... | CHÂN: ... | CAM: ... | LIGHT: ... | DELTA: ...
```

**Key frame selection for short videos (17s, 34 frames @ 2fps):**
- Frame 1, 3 (intro)
- Frame 8, 12 (early motion)
- Frame 15, 18, 22 (mid motion, peak)
- Frame 28, 32, 34 (settle)

**For medium videos (60s, 120 frames @ 2fps):**
- Sample every 10th frame = 12 key frames
- Always include first/last + peak motion frames

### Phase 4: Build Pose Sequence Map

Group similar poses into named states:

```markdown
## 5 Pose Chính

### Pose A — Front Stance (Frames 1-12, 0-3s)
- Đứng thẳng, hông đánh trái, tay phải cầm iPhone che mặt
- Tay trái buông thõng sát thân
- Scene score: 0.020-0.035 (medium motion)

### Pose B — "Tay Chạm Ngực" ⭐ SIGNATURE (Frames 13-22, 3-5s)
- Tay trái đưa lên chạm ngực/xương quai xanh
- Hông đảo phải
- Scene score: 0.074 (PEAK)

### Pose C — Body Sway (Frames 23-28, 5-7s)
- Tay trái buông lại, hông lắc nhịp nhàng
- Scene score: 0.040-0.044

### Pose D — Đồng Hồ Cát (Frames 29-31, 7-8s)
- Tay trái đặt eo, hông S-line mạnh

### Pose E — Settle (Frames 32-34, 8-17s)
- Pose ổn định + camera zoom in 5-10%
- Scene score: 0.025 → 0.001 (decreasing)
```

## AI Video Prompt Generation

### Three-Template System

Always generate 3 versions for different tools/contexts:

#### Template 1: Full Detailed (Veo 3 / Kling 2.0+ / Runway Gen-3)

```python
full_prompt = f"""A young Asian woman, 20-25 years old, [SCENE] in [LOCATION].

OUTFIT: [Top + bottom + accessories with colors]

CAMERA: [Angle] shot, [distance] through [mirror/tripod/etc.].
[Static/Locked-off/Handheld] with [micro-shake level].
[Movement: e.g., Slow push-in zoom 5-10% over final 3s].

POSE SEQUENCE (0-{duration}s):
- 0-Xs: [Pose A full description]
- X-Ys: [Pose B full description]
- Y-Zs: [Pose C full description]
- Z-Ws: [Pose D full description]
- W-{duration}s: [Pose E - settle]

MOTION: [Speed descriptor], [style descriptor].
[Micro-motion % vs static %].
No [prohibited motion type].

LIGHTING: [Color temp]K, [direction] lighting,
[shadow map]. [Palette description].

AUDIO: [Music genre] + [voice overlay if any].

STYLE: [Aesthetic], [target platform], [save-worthy/emotional/etc.].

FORMAT: {duration}s, {fps}fps, {aspect_ratio} vertical.
"""
```

**Real example (TikTok Shoppable OOTD):**
```
A young Asian woman, 20-25, mirror selfie OOTD video in wooden-walled 
room. Brown polka-dot top with white square neckline, white mini skirt, 
brown cap, white shoulder bag.

CAMERA: Eye-level shot, 1.2-1.5m through mirror. Locked-off with 
slight handheld micro-shake. Slow push-in zoom 5-10% over final 3s.

POSE SEQUENCE (0-17s):
- 0-3s: Stands facing mirror, weight on right leg, left hand at side, 
  right hand holds iPhone covering face
- 3-5s: Raises left hand gracefully to chest/collarbone, fingers touch 
  fabric. Weight shifts to left leg, hip sways right
- 5-12s: Hand returns to side, slow rhythmic hip sway (L-R-L)
- 12-15s: Left hand moves to waist, creates S-curve silhouette
- 15-17s: Settles into final pose, camera pushes in

MOTION: Slow, graceful, fashion-catalog pace. Mostly micro-motion 
(2-3 inch movements), no large gestures.

LIGHTING: Warm overhead diffuse (3000K), soft shadows under chin.
Tone-on-tone palette: brown, white, beige.

FORMAT: 17s, 60fps, 9:16 vertical, TikTok Shoppable aesthetic.
```

#### Template 2: Compact (for tools with token limits)

```python
compact_prompt = f"""[Subject] [action] in [location]. [Camera setup]. [Pose sequence A→B→C→D]. [Lighting]. {duration}s, {fps}fps, {aspect_ratio}."""
```

#### Template 3: Image-to-Video (with reference image)

```python
img2vid_prompt = f"""SUBJECT: [Upload reference image]
MOTION:
- 0-Xs: [Pose A]
- X-Ys: [Pose B]
- Y-Zs: [Pose C]
CAMERA: [Setup]
STYLE: [Aesthetic]
MOTION_INTENSITY: [Low/Medium/High]
"""
```

## Camera Analysis Template

Always include in the analysis output:

```markdown
| Aspect | Value | Detail |
|--------|-------|--------|
| Type | Mirror selfie | Qua gương, fixed position |
| Angle | Eye-level / ngang ngực | Không nghiêng lên/xuống |
| Distance | 1.2-1.5m | Trung cảnh (waist-up) |
| Zoom | Static → zoom nhẹ 5-10% cuối video | Slow push-in |
| Stability | Rung nhẹ tay | Natural handheld |
| Movement | KHÔNG pan/tilt | Camera cố định |
```

## Lighting Analysis Template

```markdown
- **Nguồn:** [Overhead diffuse / Ring light / Natural / etc.]
- **Hướng:** [Top-down / Front-fill / Side]
- **Shadow map:** [Chin shadow / Neck shadow / Sides]
- **Tông:** [Warm 2700-3000K / Cool 5000-6500K]
- **Contrast:** [Low / Medium / High]
- **Palette:** [Tone-on-tone colors]
```

## Motion Pattern Summary

Always include this metric in output:

```markdown
## Motion Pattern Tổng Kết

Cycle: [2-3s/pose]
Pattern: [STATIC (hold) → MICRO-MOTION → NEW POSE]
Tempo: [Slow, graceful / Fast, energetic]
Số pose trong 17s: [4-5 pose chính]
Tổng motion: [60% static + 40% micro-motion]
```

## Replicate Checklist

Send this checklist so the user can shoot the original:

```markdown
- [ ] Background: [Specific type — wooden wall, beige tone]
- [ ] Lighting: [Warm overhead diffuse, 2700-3000K]
- [ ] Camera: [Mirror selfie fixed, eye-level, tripod]
- [ ] Outfit: [Specific items]
- [ ] Pose sequence: [A → B → C → D → E with timings]
- [ ] Tempo: [2-3s/pose, slow graceful]
- [ ] Motion: [60% static + 40% micro-motion]
- [ ] Zoom: [Slow push-in 5-10% in final 2-3s]
- [ ] Duration: [15-20s sweet spot]
- [ ] Audio: [Music + brief voice overlay if any]
- [ ] Caption: [1-2 words, 3 hashtags]
- [ ] Shop tag: [TikTok Shop integration]
```

## Tips for Better AI Video Prompts

1. **Be specific about pose, not motion** — "Left hand on collarbone" works better than "move left hand"
2. **Include timing** — AI tools respect pose sequence with timestamps
3. **Describe micro-motion, not big gestures** — "Slow sway 2-3 inches" beats "sway back and forth"
4. **Always specify camera** — "Eye-level, locked-off" prevents random camera movement
5. **Lighting matters** — "Warm overhead" vs "natural light" produces very different results
6. **For TikTok aesthetic, mention "save-worthy" or "fashion catalog pace"** — guides the tool toward polished output

## Example Output Structure

When user asks for motion analysis + AI prompt, send:

```markdown
## 📊 MOTION TIMELINE (0-17s)

[5 Pose Chính table]

## 📷 CAMERA
[Camera analysis table]

## 💡 LIGHTING
[Lighting analysis bullets]

## 🎯 PROMPT CHO VEO 3 / KLING / RUNWAY

[Full prompt in code block]

## 📋 CHECKLIST REPLICATE
[Replicate checklist]

**Full analysis:** `/tmp/frame-analysis/motion-analysis.md`
```
