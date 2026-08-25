---
title: KarmaVid V4 Pivot — Google AI Gemini + Veo 3 Pipeline (11/07/2026)
created: 2026-07-11
type: case-study
tags: [karmavid, google-ai, gemini, veo3, nano-banana-pro, pivot-v4, ai-generated]
confidence: high
sources: [karmavid-pivot-v3-pixar-case-study, google-gemini-nano-banana-pro-2026, google-veo-3-2026]
relationships: [karmavid, pixar-3d-animation, voxel-3d-character-animation, tiktok-viral-script]
---

# KarmaVid V4 — Google AI Pipeline (Gemini Nano Banana Pro + Veo 3)

Case study verified 11/07/2026 — anh pivot tool stack từ Blender manual (V3) → 100% AI-generated (V4).

## Context

**Project:** KarmaVid — TikTok animation channel
**Visual:** Hoạt hình 3D Pixar (giống Toy Story, Inside Out, Coco, Frozen)
**Universe:** 3 CON NGƯỜI Pixar 3D + 3 phản diện + 5 locations Việt Nam retro
**Pivot signal:** Anh request cụ thể tool stack

> *"anh làm trên nền tảng tạo hình ảnh và video AI của google gồm banana pro và Veo3 cho kênh này"* (11/07, ~17:15)

**Pivot history (4 lần trong 1 ngày):**

| Lần | Thời gian | Style + Tool | Status |
|-----|-----------|--------------|--------|
| V1 | 26/06 | Đồ ăn biến hình + 2.5D low-poly (manual) | Cũ |
| V2 | 11/07 lần 1 | CON NGƯỜI + voxel 3D pixel (manual) | ❌ SAI — em hiểu nhầm "pixal" = "pixel" |
| V3 | 11/07 lần 2 | CON NGƯỜI + Pixar 3D + **Blender manual** | ⚠️ OK nhưng pipeline phức tạp |
| **V4** | 11/07 lần 3 | **CON NGƯỜI + Pixar 3D + Google AI (Gemini + Veo 3)** | ✅ ĐÚNG — anh chỉ định dùng Google AI |

## Tool Stack V4 — Google AI

| Layer | Tool | Spec chính | Cost |
|-------|------|-----------|------|
| **Image generation** | Google Gemini **Nano Banana Pro** (Gemini 3 Pro Image) | 4096×4096 px, 16:9 | $0.134-0.24/image |
| **Video generation** | Google **Veo 3 / Veo 3.1** | 1080p, 24fps, 8s/clip, **native audio** | $0.75/second |
| **Audio (voice Vi)** | ElevenLabs VI / Voqul AI | Multi-language support | $0.05/scene |
| **Concat + edit** | ffmpeg + DaVinci Resolve + CapCut | Universal tools | Free |
| **Subscription khuyến nghị** | Google AI Pro | Unlimited Nano Banana + Veo 3 Fast | $19.99/tháng |

**Cost / 1 video (8 scenes × 8s):**
- API pure: ~$50/video (Gemini stills $1.60 + Veo 3 $48 + voice $0.40)
- Google AI Pro ($19.99/mo): Nano Banana Pro unlimited + Veo 3 Fast ~3 video/day

## Production Workflow V4 (6-step AI pipeline)

```
1. Character Design Sheet (Gemini Nano Banana Pro)
   → 6 character sheets (Phở Phi, Ớt Hiểm, Bánh Mì Bé, Bà Mụ, Nước Mắm Phú, Xúc Xích Xấu)
   ↓
2. Scene Stills (Gemini Nano Banana Pro)
   → 8 stills per script (16:9, 4096×4096) — Pixar 3D style
   ↓
3. Video Clips (Veo 3 image-to-video)
   → 8 video clips per script (8s each, 1080p, 24fps, native audio)
   ↓
4. Voice Vietnamese (ElevenLabs VI)
   → 8 voice lines per script (≤20 từ/scene)
   ↓
5. Concat + Post (ffmpeg + DaVinci Resolve)
   → 64s final video, 1080×1920 vertical, TikTok spec
   ↓
6. Upload TikTok + track metrics
```

## Critical Workflow: Write READY-TO-USE Prompts

**Lesson quan trọng nhất V4:** Mỗi scene PHẢI có 2 prompts cụ thể (Gemini + Veo 3) để anh paste vào Google AI Studio thủ công. KHÔNG assume có API key.

**Template (apply cho MỖI scene):**

```markdown
### SCENE N — [TÊN] ([time range])

**🎨 Gemini Nano Banana Pro prompt (Scene still - copy-paste):**
```
[PROMPT - EXTREME CLOSE-UP / WIDE / MEDIUM shot...]
[Specify: 16:9 cinematic aspect ratio, 4096x4096 high detail]
[Style anchor: Pixar 3D animation style, Pixar Inside Out + Toy Story aesthetic]
[Lighting: 3-point cinematic / warm golden hour / rim light...]
[Character details: hair / skin / eye Pixar signature]
```

**🎬 Veo 3 prompt (Video clip 8s - copy-paste):**
```
[PROMPT - same scene but motion + audio]
[Specify: 1080p, 24fps, 8 seconds]
[Motion: camera movement, character animation]
[Audio: native audio - SFX + music + voice lines in Vietnamese]
```
```

**Sample prompt (Phở Phi - Scene 1 HOOK):**

```
🎨 Gemini Nano Banana Pro prompt:

EXTREME CLOSE-UP shot of Vietnamese female chef Phở Phi face 
in Pixar 3D animation style. Age 22, long black hair tied in 
high ponytail with subtle gold highlights catching light. Mouth 
wide open screaming, eyes very wide with detailed brown iris 
and white highlight reflections showing extreme fear and pain. 
Hair blowing in wind with motion blur. Background cinematic 
blur with white flash and lens flare burst effect. Pixar 
subsurface scattering on warm skin. Expressive Pixar facial 
features. Cinematic 3-point lighting with high-intensity 
rim light (red-yellow flash). Slow motion 0.5x feel for 
dramatic effect. 16:9 cinematic aspect ratio. Pixar Inside 
Out + Toy Story aesthetic. 4096x4096 ultra high detail.
```

```
🎬 Veo 3 prompt:

Pixar 3D animation cinematic extreme close-up. Vietnamese 
female chef Phở Phi (age 22, black ponytail) screaming 
"Aaaaaaaaa!" with extreme emotion. Mouth wide open, eyes 
showing intense fear and pain with detailed iris reflections. 
Hair blowing in wind. Background cinematic blur with white 
flash and lens flare. Slow motion 0.5x for first 1 second, 
then speeds up to 2x for remaining 7 seconds. Pixar 
subsurface scattering skin, expressive Pixar facial 
features, cinematic 3-point lighting with red-yellow rim 
light flash. 1080p, 24fps, 8 seconds. Native audio: female 
scream + dramatic orchestral strings cinematic build-up.
```

## Critical Lesson: Informal Name Decoding

**Anh dùng tên informal:** "banana pro"

**Decode:** "banana pro" = **Nano Banana Pro** = **Gemini 3 Pro Image** (Google's official image generation model)

**Rule (apply cho tất cả AI tool references từ user):**

| User informal name | Official name | Vendor |
|--------------------|---------------|--------|
| banana pro | Nano Banana Pro = Gemini 3 Pro Image | Google |
| Veo3 / Veo 3 | Veo 3 / Veo 3.1 | Google |
| DALL-E | DALL-E 3 | OpenAI |
| Midjourney | Midjourney v6 | Midjourney |
| Suno | Suno AI v3.5 | Suno |
| Claude | Claude 3.5/4 | Anthropic |
| Sora | Sora | OpenAI |

**Anti-pattern:** Default to common interpretation without research. "banana pro" ≠ "banana" (which could be Midjourney Niji) — phải research Google docs để decode chính xác.

## Critical Lesson: API Key Absent in Session

**Situation:** Em đang trong Hermes session nhưng KHÔNG có GEMINI_API_KEY trong env config.

**Workflow khi thiếu API key:**

1. **CHECK env vars first** — `os.environ.get("GEMINI_API_KEY")`
2. **IF missing → viết READY-TO-USE PROMPTS** để user paste vào Google AI Studio thủ công
3. **KHÔNG pretend test generation** — không có API key = không thể call trực tiếp
4. **OFFER 2 OPTIONS** cho user:
   - Option A: User subscribe Google AI Pro ($19.99/mo) → dùng Google AI Studio thủ công
   - Option B: User cung cấp API key → em setup pipeline tự động

**Anti-pattern (real failure risk):**
- ❌ Pretend "đã test" character generation khi không có API key
- ❌ Generate bằng FAL (FLUX) thay thế mà không nói rõ "đây không phải Gemini"
- ❌ Skip Google AI prompts vì "không có API key"

**Correct pattern:**
- ✅ Verify env vars trước
- ✅ Viết READY-TO-USE prompts ngay cả khi không test được
- ✅ Explain rõ "em không có API key, nhưng đã viết prompts để anh copy-paste"
- ✅ Offer 3 options: subscribe / API key / dùng tool khác (FAL)

## Cost Optimization Decision Tree

```
Q1: User cần bao nhiêu video / tháng?
├── 1-3 video / tháng → Google AI Pro $19.99/mo (Veo 3 Fast ~3/day)
├── 4-10 video / tháng → Google AI Pro $19.99/mo + API top-up
└── 10+ video / tháng → Google AI Ultra $249.99/mo (Veo 3 full quality)

Q2: User có cần full control (API)?
├── Có (custom workflow) → API pure ($50/video)
└── Không (manual OK) → Google AI Pro subscription

Q3: User ưu tiên speed hay quality?
├── Speed (Veo 3 Fast) → $19.99/mo
└── Quality (Veo 3 full) → $249.99/mo hoặc API pure
```

## Pivot History Lessons (4 lần trong 1 ngày)

**Lesson quan trọng:** Rapid iteration workflow khi anh pivot liên tục.

**Workflow khi pivot V3 → V4 (tool stack change):**

```
1. ĐỌC NHANH V3 files (5 min) — hub + T-02.1 + T-03.1 + T-03.2
2. IDENTIFY GIỮ NGUYÊN: visual style Pixar 3D, nhân vật CON NGƯỜI, 8-scene formula
3. IDENTIFY ĐỔI: tool stack từ Blender manual → Google AI
4. RE-DESIGN mỗi file thêm 2 layers:
   - Layer A: visual style (giữ Pixar 3D specs)
   - Layer B: tool stack (thêm Gemini + Veo 3 prompts ready-to-use)
5. UPDATE hub.md với tool stack pivot
6. LOG pivot event trong logs/2026-07-11-pivot-v4-googleai-session.md
7. EMBED SUMMARY cho anh (tool stack comparison + cost estimate)
```

**Timeline:** 1 lệnh tool stack pivot → 4 file updated (~17 phút) → embed summary (1 turn).

## Decision: V4 vs V3 vs V2 vs V1

| Tiêu chí | V1 (đồ ăn) | V2 (voxel) | V3 (Pixar manual) | **V4 (Google AI)** |
|----------|------------|------------|-------------------|---------------------|
| Speed/video | 1-2 tuần | 1-2 tuần | 3-5 ngày | **30-60 phút** |
| Cost/video | Rẻ | Rẻ | $50-200 | **~$50 API / $0 Pro sub** |
| Skill yêu cầu | Designer | Designer | 3D modeler + animator | **KHÔNG cần — AI tự generate** |
| Scalability | Thấp | Thấp | Trung bình | **Cao** |
| Visual quality | Medium | Low | High | **High (consistent với reference image)** |
| Anph test pilot | OK | OK | OK | **✅ Best for solo creator** |

## Reference Files Updated V4

| File | Size | Nội dung |
|------|------|----------|
| `hub.md` | 15.8 KB | Pivot history 4 lần + Tool stack Google AI |
| `research/T-02.1-karmavid-universe.md` | 17.5 KB | 6 CON NGƯỜI Pixar 3D + **Gemini character prompts** ready-to-use |
| `research/T-03.1-karmavid-script-template.md` | 18.0 KB | 8-scene + **Gemini + Veo 3 prompts** cho MỖI scene |
| `research/T-03.2-karmavid-script-samples.md` | 18.1 KB | Sample #1 Phở Phi - **prompts cụ thể copy-paste** vào Google AI Studio |

**Total V4:** 67.8 KB across 4 files.

## Final Pitfall #7 (NEW 11/07/2026): Default AI tool assumption without checking API access

**Triệu chứng:** Em mặc định "Google AI" = có sẵn API key trong session.

**Fix:** LUÔN check `os.environ.get("GEMINI_API_KEY")` + `os.environ.get("GOOGLE_API_KEY")` TRƯỚC khi viết prompts call Gemini/Veo 3 trực tiếp. Nếu missing → viết READY-TO-USE prompts + offer 2 options (subscribe / provide API key).

## Final Pitfall #8 (NEW 11/07/2026): Tool stack pivot mà không giữ visual style

**Triệu chứng:** Khi pivot tool stack, em có thể vô tình thay đổi visual style (ví dụ: pivot từ Blender → Google AI mà chuyển từ Pixar 3D → anime style).

**Fix:** Khi pivot tool stack, **visual style PHẢI giữ nguyên**. Chỉ đổi CÁCH SẢN XUẤT (tool), không đổi KẾT QUẢ VISUAL. Apply matrix:
- Visual style = GIỮ NGUYÊN (Pixar 3D)
- Tool stack = ĐỔI (Blender → Google AI)
- Output quality = GIỮ NGUYÊN (cinematic Pixar)
- Workflow = ĐỔI (manual → AI-generated)

## Related

- [[pixar-3d-animation]] — Parent skill (visual direction Pixar 3D)
- [[voxel-3d-character-animation]] — Sibling skill (Voxel V2 case study, historical)
- [[tiktok-viral-script]] — TikTok script structure (kết hợp)
- KarmaVid project: `/Volumes/Storage-1/Hermes/wiki/projects/karmavid/`