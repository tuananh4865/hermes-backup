---
name: pixar-3d-animation
description: Workflow cho creative animation project dùng Pixar-style 3D characters (giống Toy Story, Inside Out, Coco, Frozen, Zootopia) — smooth 24-30 FPS + character design chi tiết cao + cinematic 3-point lighting + subsurface scattering + depth of field. Class-level skill bao trùm character bible design, production pipeline (Blender manual V3 hoặc Google AI Gemini + Veo 3 V4), voice cho nhân vật, scene templates, batch rendering, pivot workflow khi anh đổi visual direction hoặc tool stack. Load khi user nói Pixar / Disney 3D / cinematic 3D animation / hoạt hình 3D Pixar / Toy Story style / Inside Out style / high-detail 3D animation / smooth 3D characters / banana pro / Veo 3 / Google AI / Nano Banana, hoặc pivot bất kỳ animation project từ style khác (voxel 3D pixel, anime 2D, 2.5D Pixar-like) sang Pixar 3D style, hoặc pivot tool stack từ manual (Blender) sang AI-generated (Google AI).
---

# Pixar 3D Animation — Class Skill

Workflow chuẩn cho creative animation project dùng **Pixar-style 3D characters** (smooth cinematic 3D + high detail + character-driven storytelling). Bao trùm từ character design → production pipeline (Blender manual V3 hoặc Google AI Gemini + Veo 3 V4) → final render.

## Khi nào dùng skill này

| Trigger | Ví dụ |
|---------|-------|
| User nói "Pixar" / "3D Pixar" / "hoạt hình 3D Pixar" | *"style hoạt hình 3D Pixar"*, *"Pixar style character"*, *"Disney 3D animation"* |
| User pivot animation project sang Pixar direction | *"đổi từ voxel 3D pixel sang Pixar 3D"*, *"đổi từ 2.5D Pixar-like sang Pixar 3D thật"* |
| User đã có project nhưng đổi visual style + nhân vật | *"đổi nhân vật + style Pixar"* (combo) |
| User yêu cầu cinematic 3D pipeline | *"Blender cinematic render"*, *"subsurface scattering character"*, *"depth of field animation"* |
| User yêu cầu character bible cho Pixar-style animation | *"character bible Pixar style"*, *"high-detail 3D character design"* |
| User chỉ định tool stack AI (Google AI Gemini/Veo 3) | *"banana pro"*, *"Veo 3"*, *"Nano Banana"*, *"dùng Gemini + Veo 3"*, *"tạo video bằng AI"* |
| User pivot tool stack từ manual sang AI-generated | *"đổi từ Blender sang Google AI"*, *"tạo bằng AI thôi"*, *"không cần manual nữa"* |

## 1. VISUAL DIRECTION CHUẨN (BẮT BUỘC mọi scene)

### Style "Hoạt hình 3D Pixar" là gì

**Pixar-style 3D animation** = phong cách hoạt hình 3D chuẩn Hollywood, giống các phim:

- **Toy Story** (1995) - character design iconic, biểu cảm phong phú
- **Inside Out** (2015) - màu sắc vibrant, lighting cinematic
- **Coco** (2017) - văn hóa sâu sắc, nhân vật relatable
- **Frozen** (2013) - detail cao, animation mượt mà
- **Zootopia** (2016) - city life, character diversity
- **Soul** (2020) - abstract concept visualization
- **Luca** (2021) - childhood nostalgia
- **Turning Red** (2022) - Gen Z emotion

### Spec cụ thể (áp dụng cho MỌI scene trong script + MỌI shot trong render)

| Element | Spec cụ thể |
|---------|-------------|
| **Geometry** | Smooth 3D mesh, organic shapes, KHÔNG block/voxel |
| **Chi tiết nhân vật** | Cao — tóc có sợi rõ ràng, mắt có iris + pupil + highlight, da có texture subtle |
| **Tỷ lệ** | Tự nhiên — người thật proportion (không chibi to đầu) |
| **Mắt** | To, biểu cảm, có iris chi tiết, highlight phản chiếu ánh sáng |
| **Màu sắc** | Rich palette 64-128+ màu mỗi scene, gradient mịn, vibrant |
| **Animation** | **24-30 FPS mượt mà** (không giật), squash & stretch, anticipation + follow-through |
| **Lighting** | **Cinematic** — 3-point lighting (key + fill + rim), soft shadows, global illumination, subsurface scattering cho da |
| **Camera** | Cinematic angles — close-up emotional, wide epic, dolly tracking, depth of field |
| **Render style** | Photorealistic cao + cartoon stylization (giống Pixar chứ không realistic 100%) |
| **Background** | Rich detail — mỗi location có architecture, props, atmosphere riêng |

### KHÔNG nhầm với

| Sai lầm | Đúng |
|---------|------|
| ❌ Voxel 3D pixel (Minecraft/Among Us) | ✅ Smooth 3D organic mesh |
| ❌ Anime 2D flat | ✅ 3D with cinematic depth of field |
| ❌ 2.5D low-poly Pixar-like | ✅ Full 3D with detailed characters + lighting |
| ❌ Realistic 3D (như The Last of Us) | ✅ Photorealistic + cartoon stylization hybrid |
| ❌ Flat shading 16-32 màu | ✅ Rich palette 64-128+ màu + gradient |
| ❌ Frame rate 12-24 FPS voxel giật | ✅ 24-30 FPS mượt mà |

### Khi nào CHỌN Pixar 3D vs Voxel 3D

| Tiêu chí | Pixar 3D | Voxel 3D |
|----------|----------|----------|
| **Audience** | Family + mainstream, emotional storytelling | Gen Z, retro pixel lovers, Minecraft community |
| **Tone** | Wholesome + emotional + inspirational | Retro + quirky + meme-able |
| **Complexity** | Cao (cần Blender expert + render time lâu) | Thấp (CapCut template nhanh) |
| **Cost** | Cao (render farm hoặc lâu) | Thấp (mobile-friendly) |
| **Virality** | Slow-burn emotional, rewatchable | Fast viral, meme-friendly |
| **Examples** | Pixar/Disney/DreamWorks films | CapCut "Voxel Character" TikTok templates |

## 2. CHARACTER BIBLE TEMPLATE (Blender-ready hoặc Gemini prompt-ready)

Mỗi nhân vật cần mô tả đủ 9 sections để 3D modeler HOẶC Gemini AI tạo character chi tiết:

```markdown
### [TÊN NHÂN VẬT] ([VAI TRÒ])

**Visual Pixar 3D style (high detail):**
- **Body:** [mô tả hình dáng — cao/thấp/mập/ốm + tỷ lệ tự nhiên]
- **Head:** [mô tả đầu — tóc (sợi rõ ràng Pixar) + mắt (to + iris + pupil + highlight) + da (subsurface scattering)]
- **Outfit:** [quần áo + texture chi tiết (vải, da, kim loại)]
- **Props:** [đồ vật cầm theo — texture Pixar (gỗ, sắt, vàng reflection)]
- **Face details:** [mắt to biểu cảm + miệng + lông mày + biểu cảm default]
- **Hair:** [mô tả chi tiết — sợi tóc, màu, highlight kim tuyến khi ánh sáng chiếu]
- **Skin:** [subsurface scattering effect + texture + màu da Pixar]
- **Distinguishing feature:** [1-2 điểm nhận diệt ngay lập tức]

**Voice:** [giọng + tone + catchphrase]

**Pixar color palette (64-128 màu rich + gradient):**
| Main | Accent 1 | Accent 2 | Mood |
|------|----------|----------|------|
| [hex] | [hex] | [hex] | [keyword] |
```

**Lưu ý khi viết character bible Pixar:**
- Mỗi nhân vật = 1 universe tag để khán giả nhận diệt ngay (Phở Phi = tím pastel, Ớt Hiểm = đỏ rực, Bánh Mì Bé = nâu vàng)
- Catchphrase ngắn ≤10 từ, memorable, viral-able
- Mô tả HAIR + SKIN + EYE chi tiết vì đây là 3 yếu tố Pixar signature

## 3. SCENE VISUAL DIRECTION TEMPLATE

Mỗi scene trong script phải có 8 hướng dẫn Pixar 3D:

```markdown
### SCENE [N] — [TÊN] ([time range])

**Visual Pixar 3D cinematic:**
- **Camera:** [Extreme close-up face / Wide establishing shot / Low angle / High angle / Dolly tracking / Depth of field]
- **Pixar [character]:** [pose + smooth animation + biểu cảm chi tiết]
- **Props:** [đồ vật với texture rõ ràng]
- **Animation:** [smooth 30 FPS + squash & stretch + anticipation + follow-through]
- **Lighting:** [3-point cinematic key+fill+rim / Subsurface scattering da / Golden hour / Dramatic dark / Warm sunset]
- **Color grading:** [warm cinematic LUT / desaturated cool / high contrast karma / golden hour ending]
- **Atmosphere:** [bụi bay trong nắng / mưa nhỏ cinematic / particle effects / god rays]
- **Frame rate:** [24 FPS cinematic / 30 FPS smooth]

**SFX:** [cinematic sound design Pixar-style]
**Music:** [orchestral Pixar-style emotional score]

> 🎤 **[Thoại]**
> (word count)

**Text overlay:** [cinematic font Pixar-style + color + content]
```

## 4. PRODUCTION PIPELINE — 2 OPTIONS (V3 Manual vs V4 AI)

### V3 — Manual Pipeline (Blender + Character Animator + DaVinci)

```
[1] CHARACTER BIBLE       [2] BLENDER MODEL+ANIM  [3] CHARACTER ANIMATOR  [4] DAVINCI RESOLVE
   Wiki .md docs       →    3D model + skeleton  →  Lip-sync + face anim   →  Edit + sound + color
   (9 sections/char)        (rigging + shading)     (Adobe Character Anim)    (cinematic grade)
```

**V3 timeline:** 3-5 ngày/clip | **Cost:** $50-200/clip | **Skill:** cần 3D modeler + animator

### V4 — AI-Generated Pipeline (Google AI Gemini + Veo 3) — RECOMMENDED FOR SOLO CREATOR

```
[1] CHARACTER DESIGN       [2] SCENE STILLS       [3] VIDEO CLIPS         [4] VOICE + CONCAT
   Gemini Nano Banana Pro → Gemini Nano Banana Pro → Veo 3 image-to-video → ElevenLabs VI + ffmpeg
   (1 prompt/character)     (8 stills/script)        (8 clips/script)        (concat + voice)
```

**V4 timeline:** 30-60 phút/clip | **Cost:** $50/clip API pure hoặc $19.99/mo Google AI Pro (unlimited Nano Banana + Veo 3 Fast ~3 video/day) | **Skill:** KHÔNG cần — AI tự generate

### Bước V3 #1 — Character Bible (wiki docs)

- Output: `research/T-XX-character-bible.md` hoặc file trong project folder
- Template: 9 sections như mục 2 ở trên
- Lưu ý: KHÔNG cần vẽ art — chỉ mô tả chi tiết để 3D modeler dựng

### Bước V3 #2 — Blender Model + Animate

- Tool: **Blender 4.x** (free + open-source, https://blender.org)
- Workflow:
  1. Model nhân vật từ character bible (organic mesh, smooth)
  2. Rig skeleton (armature cho animation)
  3. Shading với subsurface scattering cho da (Pixar signature)
  4. Lighting setup 3-point cinematic
  5. Animate scenes 24-30 FPS (smooth, KHÔNG voxel giật)
  6. Render PNG sequence 1080×1920 cho TikTok (hoặc 1920×1080 cho YouTube)
- Pitfall: Phải set frame rate 24 hoặc 30 (KHÔNG 12 FPS voxel)
- Reference: https://docs.blender.org/manual/en/latest/animation/keyframes/

### Bước V3 #3 — Adobe Character Animator

- Tool: **Adobe Character Animator** ($20/tháng)
- Workflow: Import rigged character → Setup puppet → Lip-sync tự động với audio → Facial animation (mắt, miệng, lông mày) → Record performance → Export
- Alternative: **Reallusion iClone** ($200 1 lần) - Character animation nhanh với motion library
- Pitfall: Character phải được rigged CHUẨN với blend shapes cho face

### Bước V3 #4 — DaVinci Resolve Edit

- Tool: **DaVinci Resolve** (free, https://blackmagicdesign.com)
- Workflow: Import PNG sequence + audio → Color grading cinematic (LUT) → Add text overlay cinematic → Sound design + music → Export MP4
- Alternative: **CapCut desktop** (free) cho edit nhanh
- Pitfall: PHẢI dùng color grading cinematic LUT để có "Pixar feel" — KHÔNG skip bước này

### Bước V4 #1 — Gemini Nano Banana Pro Character Sheet

- Tool: **Google AI Studio** → Gemini Nano Banana Pro model (https://aistudio.google.com)
- Subscription: Google AI Pro $19.99/mo (unlimited) hoặc API $0.134-0.24/image
- Workflow:
  1. Mở Google AI Studio → chọn Nano Banana Pro model
  2. Paste prompt character bible vào (Xem mục 5 cho template)
  3. Generate 16:9, 4096×4096 ultra high detail
  4. Lưu ảnh làm reference
- **Format prompt cụ thể:** Xem `references/karmavid-pivot-v4-google-ai-case-study.md`

### Bước V4 #2 — Gemini Nano Banana Pro Scene Stills

- Tool: Gemini Nano Banana Pro
- Workflow:
  1. Với mỗi scene (8 scenes/script), paste Gemini prompt scene
  2. Reference character sheet từ Bước V4 #1 (giữ character consistent)
  3. Generate 8 stills Pixar-style (16:9, 4096×4096)
  4. Lưu 8 stills để dùng làm input cho Veo 3

### Bước V4 #3 — Veo 3 Video Clips

- Tool: **Veo 3 / Veo 3.1** (Google AI Studio hoặc API $0.75/second)
- Subscription: Google AI Pro $19.99/mo (Veo 3 Fast ~3 video/day) hoặc Google AI Ultra $249.99/mo (Veo 3 full ~10+ video/day)
- Workflow:
  1. Mở Google AI Studio → chọn Veo 3 model
  2. **OPTION A (image-to-video):** Upload scene still từ Bước V4 #2 + paste Veo 3 prompt → generate 8s clip 1080p 24fps native audio
  3. **OPTION B (text-to-video):** Chỉ paste Veo 3 prompt (kèm character description) → generate
  4. Lưu 8 video clips
- Pitfall: Ảnh input càng chi tiết → video output càng consistent

### Bước V4 #4 — Voice Vietnamese + Concat

- Tool: **ElevenLabs VI** / **Voqul AI** ($0.05/scene) + **ffmpeg** (free)
- Workflow:
  1. Generate voice tiếng Việt với ElevenLabs cho 8 scenes (≤20 từ/scene)
  2. Concat 8 video clips thành 64s bằng ffmpeg
  3. Add voice track
  4. Export 1080×1920 TikTok spec

## 5. RAPID PIVOT WORKFLOW — VERIFIED CASES (V1 → V2 → V3 → V4 KarmaVid)

### CASE A: V3 pivot (visual style typo correction) — 16:32 + 16:38 + 16:55 11/07

**Signal:** Anh ra 3 lệnh liên tiếp trong 30 phút:
1. *"đổi nhân vật → CON NGƯỜI"* (16:32)
2. *"style hoạt hình 3D pixal"* (16:38 — em SAI hiểu thành "3D pixel" thay vì "3D Pixar")
3. *"style hoạt hình 3D Pixar, ban nãy anh ghi nhầm đó phải là 3D pixar mới đúng"* (16:55 — sửa lại)

**Pivot history:**
- V1 (26/06): Đồ ăn biến hình + 2.5D low-poly Pixar-like
- V2 (16:38 lần 1): CON NGƯỜI + Voxel 3D pixel (EM SAI — hiểu "pixal" = "pixel")
- **V3 (16:55 lần 2): CON NGƯỀI + Hoạt hình 3D Pixar (ĐÚNG — "pixal" = "Pixar" thiếu "r")**

**Workflow khi pivot visual style:**
```
[1] ĐỌC NHANH V2 files (5 min) - hub.md + T-02.1 + T-03.1 + T-03.2
[2] IDENTIFY GIỮ NGUYÊN (nhân vật CON NGƯỜI đã đúng) + ĐỔI (voxel → Pixar)
[3] RE-DESIGN từng file với Pixar specs:
    - Geometry: voxel cube → smooth 3D organic mesh
    - Frame rate: 12-24 FPS → 24-30 FPS
    - Palette: 16-32 màu flat → 64-128 màu rich gradient
    - Camera: isometric 30-45° → cinematic angles
    - Lighting: flat shading → 3-point cinematic + subsurface scattering
[4] UPDATE hub.md với PIVOT HISTORY (V1→V2→V3 comparison table)
[5] LOG pivot event vào logs/2026-07-11-pivot-v3-pixar-session.md
[6] EMBED SUMMARY Telegram (V2 vs V3 table + sample script demo)
```

**Timeline:** 1 lệnh sửa typo → em đọc + re-design 4 file (69.6 KB) trong ~17 phút → embed summary = DONE.

### CASE B: V4 pivot (tool stack change) — 17:15 11/07

**Signal:** Anh chỉ định tool stack cụ thể:

> *"anh làm trên nền tảng tạo hình ảnh và video AI của google gồm banana pro và Veo3 cho kênh này"* (17:15)

**Pivot:** V3 (Blender manual) → **V4 (Google AI Gemini + Veo 3)**

**Workflow khi pivot tool stack:**
```
[1] ĐỌC NHANH V3 files (5 min)
[2] IDENTIFY GIỮ NGUYÊN: visual style Pixar 3D, nhân vật CON NGƯỜI, 8-scene formula, voice
[3] IDENTIFY ĐỔI: tool stack từ Blender manual → Google AI
[4] RE-DESIGN mỗi file thêm 2 layers:
    - Layer A: visual style (giữ Pixar 3D specs)
    - Layer B: tool stack (thêm Gemini + Veo 3 prompts ready-to-use)
[5] UPDATE hub.md với tool stack pivot + cost comparison
[6] LOG pivot event trong logs/2026-07-11-pivot-v4-googleai-session.md
[7] EMBED SUMMARY cho anh (tool stack comparison + cost estimate)
```

**Timeline:** 1 lệnh tool stack pivot → 4 file updated (~17 phút) → embed summary.

### Critical Lesson: Informal Name Decoding

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

### Critical Lesson: API Key Absent in Session

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

### Critical Workflow: Write READY-TO-USE Prompts

**Lesson quan trọng nhất V4:** Mỗi scene PHẢI có 2 prompts cụ thể (Gemini + Veo 3) để anh paste vào Google AI Studio thủ công.

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

**Sample prompt (Phở Phi - Scene 1 HOOK):** Xem `references/karmavid-pivot-v4-google-ai-case-study.md` cho full prompts.

## 6. TOOLS & RESOURCES

### Tools V3 — Manual Pipeline

| Tool | Vai trò | Platform | License |
|------|---------|----------|---------|
| **Blender 4.x** | Model + animate + render Pixar-style 3D | macOS/Win/Linux | Free |
| **Blender Eevee / Cycles** | Render engine cinematic | Built-in | Free |
| **Adobe Character Animator** | Lip-sync + facial animation | macOS/Win | $20/tháng |
| **Reallusion iClone** | Character animation nhanh với motion library | macOS/Win | $200 1 lần |
| **Voicelead AI / ElevenLabs VI** | Voice tiếng Việt cho nhân vật | Web | Free tier |
| **DaVinci Resolve** | Edit + color grading cinematic | macOS/Win/Linux | Free |
| **CapCut desktop** | Edit nhanh (alternative cho DaVinci) | macOS/Win | Free |

### Tools V4 — AI Pipeline (Recommended for solo creator)

| Tool | Vai trò | Platform | License |
|------|---------|----------|---------|
| **Google Gemini Nano Banana Pro** | Image generation (character sheet + scene stills) | https://aistudio.google.com | Free tier / Pro $19.99/mo |
| **Google Veo 3 / Veo 3.1** | Video generation (1080p, 24fps, 8s, native audio) | https://aistudio.google.com | Pro $19.99/mo (Fast) / Ultra $249.99/mo (full) |
| **ElevenLabs VI / Voqul AI** | Voice tiếng Việt | Web | Free tier / $0.05/scene |
| **ffmpeg** | Concat + format convert | CLI | Free |
| **DaVinci Resolve** | Edit + color grading cinematic | macOS/Win/Linux | Free |
| **CapCut desktop** | Edit nhanh | macOS/Win | Free |

### Reference visual (paste vào brief cho designer hoặc Gemini prompt)

- **Toy Story** (Pixar 1995) - character design iconic, biểu cảm phong phú
- **Inside Out** (Pixar 2015) - màu sắc vibrant, lighting cinematic
- **Coco** (Pixar 2017) - văn hóa sâu sắc, nhân vật relatable
- **Frozen** (Disney 2013) - detail cao, animation mượt mà
- **Zootopia** (Disney 2016) - city life, character diversity
- **Kung Fu Panda** (DreamWorks 2008) - hero character design
- **How to Train Your Dragon** (DreamWorks 2010) - character + creature design
- **Despicable Me / Minions** (Illumination 2010) - stylized character
- **Spider-Verse** (Sony 2018) - kết hợp 3D + 2D style (advanced)

## 7. PITFALLS — Lessons learned

### Pitfall #1 (NEW 11/07/2026): Nhầm "3D pixal" = "3D pixel" thay vì "3D Pixar"

**Triệu chứng:** Em default theo trend TikTok → re-design sang voxel → 17 phút sau phải sửa.

**Fix:** Khi phrase AMBIGUOUS (pixel vs Pixar) → PHẢI confirm trước khi re-design. Style guide phải có reference film cụ thể.

### Pitfall #2 (NEW 11/07/2026): Pixar character design thiếu hair/skin/eye detail

**Triệu chứng:** Em describe nhân vật chung chung ("cô gái đầu bếp") → 3D modeler tạo character giống low-poly, KHÔNG có Pixar signature (tóc sợi rõ, da subsurface scattering, mắt iris + highlight).

**Fix:** Character bible PHẢI có 3 sections riêng: Hair (sợi + màu + highlight) + Skin (subsurface scattering effect + màu da Pixar) + Eyes (to + iris + pupil + highlight + reflection).

### Pitfall #3 (NEW 11/07/2026): Frame rate 12 FPS = mất Pixar feel

**Triệu chứng:** Em giữ frame rate voxel (12 FPS) → animation giật → KHÔNG còn là Pixar cinematic smooth.

**Fix:** Set frame rate 24-30 FPS trong Blender render settings. 24 FPS = cinematic (giống phim Pixar chiếu rạp). 30 FPS = smooth cho action scenes.

### Pitfall #4 (NEW 11/07/2026): Flat shading = KHÔNG phải Pixar

**Triệu chứng:** Em giữ flat shading từ voxel → render giống low-poly → KHÔNG có subsurface scattering cinematic.

**Fix:** PHẢI dùng subsurface scattering cho da (Pixar signature). Kết hợp 3-point lighting (key + fill + rim) + soft shadows + global illumination.

### Pitfall #5 (NEW 11/07/2026): Palette 16-32 màu flat = KHÔNG phải Pixar

**Triệu chứng:** Em giữ palette voxel (16-32 màu flat) → render giống Minecraft → KHÔNG có rich gradient Pixar.

**Fix:** Mở rộng palette 64-128 màu/nhân vật + gradient mịn + vibrant. Đây là điểm khác biệt lớn nhất giữa voxel vs Pixar.

### Pitfall #6 (NEW 11/07/2026): Bỏ qua color grading cinematic

**Triệu chứng:** Em edit DaVinci Resolve mà KHÔNG apply color grading LUT → render flat, KHÔNG có "Pixar feel" cinematic.

**Fix:** PHẢI apply color grading cinematic LUT (warm/cool/desaturated/high contrast/golden hour) theo mood từng scene.

### Pitfall #7 (NEW 11/07/2026): Default AI tool assumption without checking API access

**Triệu chứng:** Em mặc định "Google AI" = có sẵn API key trong session → viết prompts assuming direct call → không có API key = không thể test.

**Fix:** LUÔN check `os.environ.get("GEMINI_API_KEY")` + `os.environ.get("GOOGLE_API_KEY")` TRƯỚC khi viết prompts call Gemini/Veo 3 trực tiếp. Nếu missing → viết READY-TO-USE prompts + offer 2 options (subscribe / provide API key).

### Pitfall #8 (NEW 11/07/2026): Tool stack pivot mà không giữ visual style

**Triệu chứng:** Khi pivot tool stack (Blender → Google AI), em có thể vô tình thay đổi visual style (ví dụ: chuyển từ Pixar 3D → anime style vì "Google AI dễ làm anime hơn").

**Fix:** Khi pivot tool stack, **visual style PHẢI giữ nguyên**. Chỉ đổi CÁCH SẢN XUẤT (tool), không đổi KẾT QUẢ VISUAL. Apply matrix:
- Visual style = GIỮ NGUYÊN (Pixar 3D)
- Tool stack = ĐỔI (Blender → Google AI)
- Output quality = GIỮ NGUYÊN (cinematic Pixar)
- Workflow = ĐỔI (manual → AI-generated)

### Pitfall #9 (NEW 11/07/2026): Informational name decoding without research

**Triệu chứng:** User dùng informal name ("banana pro") → em default to common interpretation ("banana" = Midjourney Niji hoặc similar) → chọn sai vendor.

**Fix:** Khi user dùng informal name → research chính thức vendor docs (Google Blog, OpenAI docs) để decode CHÍNH XÁC. Build lookup table (banana pro → Nano Banana Pro → Gemini 3 Pro Image) trước khi viết prompts.

### Pitfall #10 (NEW 11/07/2026): Rapid pivot without focus dimension identification

**Triệu chứng:** Khi user pivot (đặc biệt pivot nhanh 5 lần trong 1 ngày), em có thể vô tình đổi toàn bộ layers thay vì chỉ focus dimension mới.

**Real case (11/07):** Anh pivot 5 lần trong 1 ngày:
- V1→V2: visual (đồ ăn → người)
- V2→V3: visual style (voxel → Pixar)
- V3→V4: tool stack (Blender → Google AI)
- V4→V5: narrative depth (visual+tool → +depth)

Nếu em đổi toàn bộ mỗi pivot → lose context, mất 2 giờ chỉnh lại. Nếu em focus 1 dimension + giữ layers trước → 5 pivots × ~17 phút mỗi pivot = ~85 phút = DONE.

**Fix:** Mỗi pivot phải pass qua decision tree:
1. FOCUS DIMENSION là gì? (visual / tool / narrative / voice / character / marketing)
2. Layers GIỮ NGUYÊN? (liệt kê cụ thể)
3. Layers CẦN UPDATE? (liệt kê cụ thể)
4. Matrix so sánh old vs new (cột: layer | old state | new state | reason)

**Pivot matrix template:**
| Layer | Old state | New state | Reason |
|-------|-----------|-----------|--------|
| Visual style | Pixar 3D | Pixar 3D | GIỮ NGUYÊN (focus này pivot tool) |
| Tool stack | Blender manual | Google AI (Gemini + Veo 3) | ĐỔI (focus dimension) |
| Character visual | 6 CON NGƯỜI | 6 CON NGƯỜI | GIỮ NGUYÊN |
| 8-scene formula | 8 scenes × 8s | 8 scenes × 8s | GIỮ NGUYÊN |
| Voice Vi | Tiếng Việt | Tiếng Việt | GIỮ NGUYÊN |
| Narrative depth | Visual only | + Character Bible 12 fields | ĐỔI (focus dimension V5) |

### Pitfall #11 (NEW 11/07/2026): Default to trend TikTok when phrase ambiguous

**Triệu chứng:** User dùng phrase ambiguous ("3D pixal" = "Pixar" thiếu "r" OR "pixel"?) → em default theo trend TikTok hiện tại (CapCut "Voxel Character" template đang viral) → re-design sang voxel → 17 phút sau user phải sửa.

**Real failure case (11/07 16:38 → 16:55):**
- 16:38: *"style hoạt hình 3D pixal"* → em default sang voxel 3D pixel (Minecraft + Among Us hybrid)
- 16:55: *"phong cách hoạt hình 3D Pixar, ban nãy anh ghi nhầm đó phải là 3D pixar mới đúng"* → phải re-design sang Pixar 3D cinematic

**Fix:** Khi phrase AMBIGUOUS (có thể hiểu 2+ cách) → confirm với user trước khi re-design. Đặc biệt với:
- Tên informal AI tool ("banana pro" / "Veo3" / "DALL-E" / "Sora")
- Visual style ambiguous ("3D pixal" / "3D p*" / "phong cách 3D [X]")
- Genre ambiguous ("horror" / "thriller" / "drama")

**Confirmation pattern (template message):**
```
Anh ơi, em hiểu "[phrase]" có thể là:
- Option A: [interpretation 1 — thường phổ biến nhất]
- Option B: [interpretation 2 — alternative]
- Option C: [interpretation 3 — niche]

Em chọn A vì [lý do]. Nếu anh muốn B hoặc C, anh nói rõ em re-design ngay.
```

**Anti-pattern:** Default without confirmation khi phrase ambiguous.

**Correct pattern:**
- ✅ Confirm khi phrase ambiguous (visual style, tool name, genre)
- ✅ Reference film cụ thể trong style guide (Toy Story, Inside Out, Coco) để tránh hiểu sai
- ✅ Build lookup table cho AI tool informal names (banana pro → Nano Banana Pro → Gemini 3 Pro Image)

## 8. RELATED SKILLS

- **`voxel-3d-character-animation`** (creative/) — Voxel 3D pixel character animation (Minecraft/Among Us style). Sibling skill, dùng cho retro pixel aesthetic. Pivot giữa 2 skill này rất phổ biến.
- **`pixel-art`** (creative/) — 2D pixel art conversion (image→PNG). Distinct từ voxel 3D + Pixar 3D character animation. Load nếu user cần STATIC pixel art.
- **`tiktok-viral-script`** (social-media/) — TikTok script structure (hook + body + CTA). Dùng KẾT HỢP với skill này khi viết script cho TikTok animation.
- **`tiktok-product-script`** (content/) — Generate TikTok sales script từ product info. KHÔNG liên quan trực tiếp.
- **`tiktok-video-editor`** (media/) — TikTok raw clip editing workflow. Dùng SAU khi render Pixar animation xong, để edit cuối + add sound + text.
- **`clone-and-adapt-competitor`** — Clone competitor channel style. Dùng KẾT HỢP khi muốn clone 1 channel Pixar animation nào đó.
- **`ideation`** (creative/) — Brainstorm project ideas qua creative constraints. Dùng TRƯỚC khi bắt đầu project Pixar animation để có concept chắc chắn.

## 9. CHECKLIST (áp dụng trước khi ship)

### V3 Manual Pipeline Checklist
- [ ] Character bible có 9 sections (Body, Head, Outfit, Props, Face, Hair, Skin, Distinguishing feature, Voice + Palette)
- [ ] Hair detail: sợi rõ ràng + màu + highlight kim tuyến khi ánh sáng chiếu
- [ ] Skin detail: subsurface scattering effect (Pixar signature)
- [ ] Eyes detail: to + iris + pupil + highlight + reflection ánh sáng
- [ ] Pixar color palette 64-128 màu rich gradient (KHÔNG flat shading)
- [ ] Frame rate 24-30 FPS (KHÔNG 12 voxel)
- [ ] Camera cinematic angles (close-up emotional + wide epic + dolly + depth of field)
- [ ] Lighting 3-point cinematic (key + fill + rim) + soft shadows + global illumination
- [ ] Mỗi scene có visual direction Pixar 3D cinematic đầy đủ 8 fields
- [ ] Blender render output là PNG sequence (KHÔNG video trực tiếp — để DaVinci edit + color grade sau)
- [ ] DaVinci Resolve color grading cinematic LUT applied
- [ ] Voice tiếng Việt rõ ràng, đúng tone nhân vật
- [ ] Test render 1 scene đầu tiên + verify visual style TRƯỚC khi batch render toàn bộ

### V4 AI Pipeline Checklist
- [ ] API key check: `GEMINI_API_KEY` available OR user prepared to use Google AI Studio manually
- [ ] Character prompts (Gemini Nano Banana Pro): 6 characters × 1 prompt each, Pixar 3D style anchor + 16:9 + 4096×4096
- [ ] Scene stills (Gemini): 8 scenes × 1 prompt each, character consistent
- [ ] Video clips (Veo 3): 8 scenes × 1 prompt each, 8s, 1080p, 24fps, native audio
- [ ] Voice lines (ElevenLabs VI): 8 voice lines, ≤20 từ/scene, tiếng Việt
- [ ] Concat 8 clips → 64s video bằng ffmpeg
- [ ] Export 1080×1920 TikTok spec
- [ ] Text overlay "LÀM ÁC THÌ PHẢI CHỊU — KARMA KHÔNG BỎ SÓT AI!" ở scene 8
- [ ] End card + subscribe button

## 12. NARRATIVE BIBLE PATTERN (NEW 11/07 — V5 case study)

**Khi user yêu cầu "thiết kế hệ thống nhân vật + câu chuyện + chiều sâu thế giới"** sau khi đã có visual style + tool stack, đây là pivot thứ 3 (focus shift từ visual → tool → narrative).

### Pattern: Character Bible 12 Fields (per character)

Mỗi nhân vật cần đủ 12 sections để có CHIỀU SÂU NARRATIVE (KHÔNG chỉ visual):

| Field | Mục đích |
|-------|----------|
| **1. Thông tin cơ bản** | Tên + biệt danh + tuổi + giới tính + chiều cao + nghề + quê quán + trình độ học vấn |
| **2. Visual Pixar 3D** | Da + tóc + mắt + áo quần + props + biểu cảm + tỷ lệ (giữ nguyên từ v4) |
| **3. Backstory chi tiết** | Sinh ra ở đâu + gia đình + mối quan hệ + sự kiện lớn (lifecycle) |
| **4. Karma Score Life Timeline** | Bảng tuổi → sự kiện → K thay đổi (tracked từ nhỏ đến lớn) |
| **5. Tính cách 4 chiều** | **Strength / Flaw / Want / Need** — đặc biệt **Need** là điều nhân vật CHƯA BIẾT mình cần → tạo arc growth |
| **6. Dark Secret** | 1-2 bí mật mà nhân vật chưa tiết lộ → reveal dần qua arc → cliffhanger |
| **7. Character Arc** | Từng part + Karma shift + visual highlight + Karma Effect |
| **8. Dialogue Style** | Tone + cách nói + ẩn dụ đặc trưng + hành vi khi buồn/giận/vui |
| **9. Về các nhân vật khác** | Quotes về từng NPC khác (giúp cross-character consistency) |
| **10. TikTok Content Hook** | Hook gợi ý cho mỗi part (template cho scriptwriter) |
| **11. NO REDEMPTION Arc** (cho villain) | Hard rule: phản diện KHÔNG BAO GIỜ có arc chuộc lỗi |
| **12. Karmic Crystallization** | Hình thức biến hình khi K < -10 (cụ thể cho từng villain) |

### Pattern: World Rules + Lore

Khi user yêu cầu "thế giới có chiều sâu", thiết kế:

| Layer | Component |
|-------|-----------|
| **World Physics** | Quy luật vật lý (Karma Physics: K = Σ(thiện) - Σ(ác), thresholds, hard rules) |
| **World Rules** | 5 Hard Rules (cân bằng, tỉ lệ nghịch đảo, no redemption, etc.) |
| **Hierarchy** | Power structure (Karma Council invisible + quận dân + quận quyền lực + vùng thiêng liêng) |
| **Locations (5+)** | Mỗi location có tuổi + lore + visual + nhân vật qua lại + dark secret |
| **Timeline** | 500+ năm lịch sử với các mốc quan trọng |
| **Themes + Anti-themes** | 5 themes chính + 5 anti-themes (triết lý sâu) |
| **Economy** | Karma Manipulation Rules + Karmic Crystallization mechanic |

### Workflow: Pivot to Narrative Depth

```
[1] GIỮ NGUYÊN: visual style (Pixar 3D) + tool stack (Google AI) + character visual specs
[2] THÊM LAYER: narrative depth (Character Bible 12 fields + World Rules + Locations + Timeline + Themes)
[3] RE-DESIGN: T-02.1 universe file thêm 8 phần narrative (KHÔNG đổi phần visual)
[4] UPDATE hub.md: pivot history V1→V2→V3→V4→V5
[5] LOG V5 pivot event
[6] EMBED SUMMARY cho user
```

**Timeline:** 1 lệnh "thiết kế hệ thống nhân vật + chiều sâu" → 50KB narrative bible → embed summary = DONE.

### CASE C: V5 pivot (narrative depth) — 18:25 11/07

**Signal:** Anh yêu cầu chiều sâu narrative:
> *"thiết kế hệ thống nhân vật, câu chuyện cho từng nhân vật để nhân vật có chiều sâu. thế giới và chiều sâu cho thế giới đó"* (18:25)

**Pivot:** V4 (visual + tool) → **V5 (visual + tool + narrative depth)**

**Workflow khi pivot to narrative:**
```
[1] ĐỌC NHANH V4 files (5 min) - confirm visual + tool giữ nguyên
[2] IDENTIFY GIỮ NGUYÊN: visual Pixar 3D, tool Gemini + Veo 3, 8-scene formula, voice Vi
[3] THÊM 8 phần narrative vào T-02.1:
    - Karma Physics (công thức K = Σ thiện - Σ ác)
    - 5 Hard Rules (cân bằng tức thì, tỉ lệ nghịch đảo, NO REDEMPTION, etc.)
    - 5 Locations với lore riêng
    - 6 nhân vật × 12 fields Character Bible
    - 5 Series + 25 episodes breakdown
    - Timeline 500 năm
    - 5 Themes + 5 Anti-themes
    - Karmic Crystallization (hình phạt biến hình)
[4] UPDATE hub.md với V5 pivot history
[5] LOG V5 pivot event
[6] EMBED SUMMARY: highlight 12 fields + 8 phần + sample Character Bible Phở Phi
```

**Kết quả V5:** 50.3 KB narrative bible, 9,102 từ, 8 sections, 6 nhân vật với backstory + dark secret + character arc + karma timeline.

### Critical Lesson: Pivot Focus Shift (visual → tool → narrative)

**Pattern quan trọng nhất V5:** Mỗi pivot có FOCUS DIMENSION khác nhau — KHÔNG thay đổi toàn bộ:

| Pivot | Focus dimension | Giữ nguyên |
|-------|-----------------|-------------|
| V1 → V2 | Visual (đồ ăn → người) | Karma concept, Việt Nam retro |
| V2 → V3 | Visual style (voxel → Pixar) | Nhân vật CON NGƯỜI |
| V3 → V4 | Tool stack (Blender → Google AI) | Visual Pixar 3D, nhân vật CON NGƯỜI |
| V4 → V5 | Narrative depth (visual+tool → +depth) | Visual Pixar 3D, tool Gemini/Veo 3, character visual |

**Rule:** Khi pivot, identify FOCUS DIMENSION mới + giữ nguyên TẤT CẢ layers trước + thêm layer mới. KHÔNG đổi toàn bộ.

**Anti-pattern (real failure 11/07):** Em đã default theo trend TikTok khi anh nói "3D pixal" → re-design sang voxel → 17 phút sau phải sửa. **Lesson:** Khi phrase AMBIGUOUS → PHẢI confirm với user trước khi re-design.

**Confirmed workflow for any pivot:**
1. Đọc file cũ
2. Phân loại dimension: visual / tool / narrative / voice / character / marketing
3. Confirm dimension mới = pivot focus
4. Identify layers giữ nguyên + layers cần update
5. Re-design chỉ layers cần update
6. Update pivot history table
7. Log + embed summary

### Critical Lesson: Character Bible Depth = 12 Fields (KHÔNG chỉ Visual)

**Lesson từ V5:** Khi user yêu cầu "nhân vật có chiều sâu", visual spec + 1-2 thuộc tính KHÔNG ĐỦ. Cần đủ 12 fields:

**Visual fields (giữ nguyên):**
1. Thông tin cơ bản (Identity)
2. Visual Pixar 3D (Body, Head, Outfit, Props, Hair, Skin, Eyes)

**Narrative fields (NEW cho V5):**
3. Backstory chi tiết (gia đình, quan hệ, sự kiện lớn)
4. Karma Score Life Timeline (track qua từng tuổi)
5. Tính cách 4 chiều (Strength / Flaw / Want / **Need** — điều nhân vật CHƯA BIẾT mình cần)
6. Dark Secret (1-2 bí mật reveal dần qua arc)
7. Character Arc (timeline + Karma shift + visual highlight)
8. Dialogue Style (tone + ẩn dụ + behavior patterns)
9. Về các nhân vật khác (quotes về NPC khác)
10. TikTok Content Hook (gợi ý hook cho mỗi part)

**Villain-specific fields:**
11. NO REDEMPTION Arc (hard rule)
12. Karmic Crystallization form (hình phạt biến hình cụ thể)

**Anti-pattern (avoid):**
- ❌ Visual spec + 1-2 personality traits → "depth" giả
- ❌ Lore dump 10 trang không có structure → reader overwhelmed
- ❌ Dark secret ở đầu series → mất cliffhanger

**Correct pattern:**
- ✅ Đủ 12 fields mỗi nhân vật
- ✅ Lore được structured theo 8 phần (Physics → Rules → Locations → Characters → Series → Timeline → Themes → Economy)
- ✅ Dark secret reveal dần qua arc (Part 3, Part 5, Part 7 tùy series)

## 13. PIVOT SUMMARY MATRIX (Updated 11/07 — 5 versions trong 1 ngày)

| Pivot | Trigger | Focus Dimension | Old | New | Status |
|-------|---------|-----------------|-----|-----|--------|
| V1→V2 | 16:32 "đổi nhân vật → CON NGƯỜI" | Visual (character form) | Đồ ăn biến hình | CON NGƯỜI | OK |
| V2→V3 | 16:38 "3D pixal" → 16:55 "3D Pixar" (typo) | Visual (style) | Voxel 3D pixel | Pixar 3D cinematic | ✅ Fix typo |
| V3→V4 | 17:15 "banana pro + Veo 3" | Tool stack | Blender manual | Google AI (Gemini + Veo 3) | ✅ Pivot tool |
| **V4→V5** | **18:25 "thiết kế nhân vật + chiều sâu"** | **Narrative depth** | **Visual+tool** | **+12 fields character bible + 8 phần narrative** | ✅ **NEW** |

**Lesson master:** Mỗi pivot có 1 FOCUS DIMENSION duy nhất. Khi user pivot, identify dimension đó + giữ nguyên các dimensions khác + thêm layer mới.

## 14. RELATED SKILLS (UPDATED)

- **`voxel-3d-character-animation`** (creative/) — Voxel 3D pixel animation (Minecraft/Among Us style). Sibling skill, dùng cho retro pixel aesthetic. Pivot giữa 2 skill này rất phổ phổ biến — pattern đã được verify trong V2 pivot.
- **`pixel-art`** (creative/) — 2D pixel art conversion (image→PNG). Distinct từ voxel 3D + Pixar 3D character animation.
- **`tiktok-viral-script`** (social-media/) — TikTok script structure (hook + body + CTA). Kết hợp với skill này khi viết script cho TikTok animation.
- **`tiktok-video-editor`** (media/) — TikTok raw clip editing. Dùng SAU khi render Pixar animation xong.
- **`clone-and-adapt-competitor`** — Clone competitor channel style. Đã có KarmaVid case study (clone + adapt @herocat2309 onion girl universe thành Pixar 3D Pixar Vietnamese characters).
- **`ideation`** (creative/) — Brainstorm project ideas TRƯỚC khi bắt đầu project Pixar animation.

## 15. CHECKLIST (UPDATED 11/07 — V5 narrative)

### V5 Narrative Checklist (NEW)
- [ ] 6 nhân vật × 12 fields Character Bible (mỗi nhân vật đủ 12 sections)
- [ ] Karma Score Life Timeline cho mỗi nhân vật (track K qua từng tuổi)
- [ ] 4-chiều tính cách: Strength / Flaw / Want / **Need** (Need là điều CHƯA BIẾT)
- [ ] Dark Secret cho mỗi nhân vật (1-2 bí mật reveal dần qua arc)
- [ ] NO REDEMPTION Arc cho villain (hard rule R3)
- [ ] Karmic Crystallization form cho từng villain (hình phạt cụ thể)
- [ ] 5+ Locations với lore riêng + visual + dark secrets
- [ ] World Rules: Karma Physics + 5 Hard Rules + Action Weights
- [ ] Hierarchy: Karma Council + 3 quận dân + 3 quận quyền lực + 2 vùng thiêng liêng
- [ ] Timeline 500+ năm với mốc quan trọng
- [ ] 5 Themes chính + 5 Anti-themes
- [ ] Karma Economy + Manipulation Rules
- [ ] 5 Series + 25 episodes breakdown (mỗi episode có Karma Score + visual highlight)

## 10. TRIGGER EXAMPLES (để nhận biết khi nào load skill này)

```
# Direct trigger — Pixar 3D
"hoạt hình 3D Pixar"
"Pixar style character"
"Toy Story style animation"
"Inside Out style"
"Disney 3D cinematic"
"smooth 3D animation"

# Direct trigger — Google AI tools (NEW 11/07)
"banana pro"
"Nano Banana"
"Gemini 3 Pro Image"
"Veo 3" / "Veo3"
"Google AI"
"AI-generated animation"
"tạo video bằng AI"
"dùng AI làm animation"

# Pivot trigger — visual style
"đổi từ voxel sang Pixar 3D"
"đổi từ 2.5D Pixar-like sang Pixar 3D thật"
"đổi từ anime 2D sang Pixar 3D"
"đổi từ low-poly sang Pixar cinematic"

# Pivot trigger — tool stack
"đổi từ Blender sang Google AI"
"tạo bằng AI thôi"
"không cần manual nữa"
"dùng AI tạo character"
"dùng AI tạo video"

# Ambiguous phrase trigger (CẦN confirm)
"3D pixal" (typo - có thể Pixar hoặc pixel)
"3D p*" (cần confirm)
"phong cách 3D [X]" (cần confirm X là gì)
"banana pro" (cần decode: Nano Banana Pro = Gemini 3 Pro Image)

# Production pipeline — V3 manual
"Blender Pixar render"
"subsurface scattering character"
"depth of field animation"
"cinematic 3-point lighting"
"DaVinci Resolve color grading"
"Adobe Character Animator lip-sync"

# Production pipeline — V4 AI (NEW 11/07)
"Gemini character sheet"
"Veo 3 video clip 8s"
"image-to-video animation"
"AI character bible"
"prompt for Nano Banana Pro"
```

## 11. VERIFIED CASE STUDIES (KarmaVid project 11/07/2026 — 4 versions trong 1 ngày)

### V1 → V2 → V3 → V4 Pivot Timeline

| Pivot | Trigger | New Style + Tool | Status |
|-------|---------|-------------------|--------|
| V1 → V2 | 16:32: *"đổi nhân vật → CON NGƯỜI"* | Đồ ăn biến hình → CON NGƯỜI voxel | OK |
| V2 → V3 | 16:38 + 16:55: *"3D pixal"* (typo) → *"3D Pixar"* | voxel → Pixar 3D | ✅ Fix typo |
| V3 → V4 | 17:15: *"banana pro + Veo 3"* | Pixar manual → Pixar + Google AI | ✅ Pivot tool |

**Common workflow across all pivots:**
1. Đọc nhanh file cũ (5 min)
2. Identify GIỮ NGUYÊN + ĐỔI
3. Re-design từng file với matrix
4. Update hub.md với pivot history table
5. Log pivot event
6. Embed summary Telegram

**Total timeline:** 4 pivots trong ~1 giờ (16:32 → 17:15) = very rapid iteration workflow.

### Output Files Updated (4 versions)

| Version | hub.md | T-02.1 universe | T-03.1 template | T-03.2 samples | Total |
|---------|--------|----------------|------------------|----------------|-------|
| V1 (26/06) | 5.1 KB | 14.1 KB | 12.8 KB | 11.8 KB | 43.8 KB |
| V2 (11/07 lần 1) | 10.8 KB | 19.7 KB | 13.6 KB | 17.3 KB | 61.4 KB |
| V3 (11/07 lần 2) | 11.5 KB | 22.0 KB | 17.3 KB | 18.8 KB | 69.6 KB |
| V4 (11/07 lần 3) | 15.8 KB | 17.5 KB | 18.0 KB | 18.1 KB | 69.4 KB |

**Trend:** File size tăng đều qua 4 versions do thêm pivot history + visual specs + tool stack details.

**References:**
- V3 case study: `references/karmavid-pivot-v3-pixar-case-study.md`
- V4 case study: `references/karmavid-pivot-v4-google-ai-case-study.md` (FULL DETAILS)
- **V5 case study: `references/karmavid-pivot-v5-narrative-bible-case-study.md`** (NEW 11/07 — Narrative Bible 12 fields + 8 phần world-building + 5-pivot matrix)

## Related

- [[voxel-3d-character-animation]] (skill) — Voxel 3D pixel animation (sibling skill, khi nào dùng voxel vs Pixar xem mục 1)
- [[pixel-art]] (skill) — 2D pixel art conversion (companion skill, KHÔNG overlap)
- [[tiktok-viral-script]] (skill) — TikTok script structure (kết hợp)
- [[tiktok-video-editor]] (skill) — Final edit (sau khi render Pixar xong)
- KarmaVid project: `/Volumes/Storage-1/Hermes/wiki/projects/karmavid/`