---
name: voxel-3d-character-animation
description: Workflow cho creative animation project dùng voxel/3D pixel characters (Minecraft-style cube characters + 16-32 màu flat shading + isometric camera + 12-24 FPS giật nhẹ). Class-level skill bao trùm character bible design, MagicaVoxel → Blender → CapCut production pipeline, voice cho nhân vật, scene templates, batch rendering, pivot workflow khi anh đổi visual direction. Load khi user nói voxel / 3D pixel / Minecraft style character / low-poly cube characters / khối 3D / làm animation voxel / magicavoxel / Among Us style / Stardew Valley style, hoặc pivot bất kỳ animation project từ style khác (2.5D Pixar, anime 2D, etc.) sang 3D pixel voxel.
---

# Voxel 3D Character Animation — Class Skill

Workflow chuẩn cho creative animation project dùng **voxel/3D pixel characters** (Minecraft cube characters + flat shading + isometric camera). Bao trùm từ character design → MagicaVoxel export → Blender animation → CapCut edit → final render.

## Khi nào dùng skill này

| Trigger | Ví dụ |
|---------|-------|
| User nói "voxel" / "3D pixel" / "Minecraft style" | *"style hoạt hình 3D pixel"*, *"Minecraft style character"*, *"Among Us animation"* |
| User pivot animation project sang voxel direction | *"đổi từ 2.5D Pixar sang 3D pixel"* |
| User đã có project nhưng đổi tất cả nhân vật → người + đổi visual style | *"tất cả các nhân vật thay đổi lại thành con người"* + *"style 3D pixel"* (combo 2 câu liên tiếp = rapid pivot signal) |
| User yêu cầu MagicaVoxel export hoặc Blender render pipeline | *"tạo character bible voxel"*, *"render video voxel"*, *"MagicaVoxel → Blender"* |
| User yêu cầu character bible cho TikTok animation | *"character bible cho animation"*, *"voxel character design"* |

## 1. VISUAL DIRECTION CHUẨN (BẮT BUỘC mọi scene)

### Style "3D Pixel / Voxel" là gì

Kết hợp 2 yếu tố:
- **Pixel art aesthetic** (giống Minecraft / Stardew Valley / Among Us / Crossy Road) — block, chunky, retro, low-res nhưng có chi tiết
- **3D rendering** — chiều sâu, ánh sáng, perspective, camera angles đa dạng

### Spec cụ thể (áp dụng cho MỌI scene trong script + MỌI shot trong render)

| Element | Spec cụ thể |
|---------|-------------|
| **Geometry** | Voxel cube/block (64-128 cubes/nhân vật) |
| **Tỷ lệ nhân vật** | Chibi — đầu to ~40% thân, mắt 2-4 pixel vuông/tròn |
| **Palette** | 16-32 màu flat shading mỗi nhân vật (KHÔNG gradient mịn) |
| **Frame rate** | 12-24 FPS (giật nhẹ voxel feel — KHÔNG smooth 60 FPS) |
| **Camera default** | Isometric 30-45° (fixed) + close-up voxel khi thoại quan trọng |
| **Lighting** | Flat shading + warm ambient + ambient occlusion nhẹ (giống Among Us + Minecraft cinematic) |
| **Background** | Voxel pixel texture Việt Nam retro (nhà ống voxel, chợ voxel, quán cóc voxel) |
| **Style reference** | Minecraft character skin + Among Us + Stardew Valley + Crossy Road |

### KHÔNG nhầm với

| Sai lầm | Đúng |
|---------|------|
| ❌ 2.5D low-poly Pixar-like smooth | ✅ Voxel 3D pixel flat shading giật nhẹ |
| ❌ Anime 2D flat | ✅ Voxel 3D có chiều sâu |
| ❌ 3D realistic (chi tiết quá cao) | ✅ Voxel 64-128 cubes, chi tiết vừa đủ |
| ❌ Pixel art 2D thuần (no depth) | ✅ Voxel 3D có camera angle đa dạng |
| ❌ Gradient mịn 16M màu | ✅ Palette flat 16-32 màu/nhân vật |

## 2. CHARACTER BIBLE TEMPLATE (MagicaVoxel-ready)

Mỗi nhân vật cần mô tả đủ 8 sections để designer tạo voxel model:

```markdown
### [TÊN NHÂN VẬT] ([VAI TRÒ])

**Visual voxel 3D pixel:**
- **Body:** [mô tả hình dáng — cao/thấp/mập/ốm + voxel cube count ước tính]
- **Head:** [mô tả đầu — tóc/mũ/mặt]
- **Outfit:** [quần áo + màu voxel palette cụ thể]
- **Props:** [đồ vật cầm theo — voxel]
- **Face:** [mắt 2-4 pixel + miệng + biểu cảm default]
- **Chiều cao:** [X voxel cubes tổng]
- **Distinguishing feature:** [1-2 điểm nhận diện ngay lập tức]

**Voice:** [giọng + tone + catchphrase]

**Voxel color palette (16-32 màu):**
| Main | Accent 1 | Accent 2 | Mood |
|------|----------|----------|------|
| [hex] | [hex] | [hex] | [keyword] |
```

**Lưu ý khi viết character bible:**
- Mỗi nhân vật = 1 universe tag để khán giả nhận diệt ngay (Phở Phi = tím pastel, Ớt Hiểm = đỏ rực, Bánh Mì Bé = nâu vàng)
- Catchphrase ngắn ≤10 từ, memorable, viral-able
- Voxel palette PHẢI được define cụ thể (hex codes) để MagicaVoxel render chính xác

## 3. SCENE VISUAL DIRECTION TEMPLATE

Mỗi scene trong script phải có 6 hướng dẫn voxel 3D pixel:

```markdown
### SCENE [N] — [TÊN] ([time range])

**Visual 3D PIXEL voxel:**
- **Camera:** [Isometric 30-45° / Close-up voxel / Wide shot voxel / Top-down voxel]
- **Voxel [character]:** [pose + animation + expression]
- **Voxel props:** [đồ vật trong scene]
- **Animation:** [walk cycle 12fps / squash pixel / impact frame / transformation]
- **Lighting:** [warm ambient voxel / dramatic shadow voxel / flash pixel / sunset voxel]
- **Frame rate:** [12 FPS cho voxel retro / 24 FPS cho montage cần mượt]

**SFX:** [pixel sound effects]
**Music:** [voxel music style]

> 🎤 **[Thoại]**
> (word count)

**Text overlay:** [pixel font + color + content]
```

## 4. PRODUCTION PIPELINE (4 bước)

```
[1] CHARACTER BIBLE       [2] MAGICA VOXEL      [3] BLENDER RENDER     [4] CAPCUT EDIT
   Wiki .md docs      →     .vox file export  →    Animation 12-24 FPS →  Edit + sound + text
   (8 sections/char)        (cube assembly)        (render to PNG seq)    (export MP4)
```

### Bước 1 — Character Bible (wiki docs)

- Output: `research/T-XX-character-bible.md` hoặc file trong project folder
- Template: 8 sections như mục 2 ở trên
- Lưu ý: KHÔNG cần vẽ art — chỉ mô tả voxel để designer (human hoặc AI) dựng

### Bước 2 — MagicaVoxel Export

- Tool: **MagicaVoxel** (free, open-source, https://ephtracy.github.io)
- Input: Character bible description + voxel color palette hex
- Output: 1 file `.vox` cho mỗi nhân vật
- Workflow: Open MagicaVoxel → Load palette → Build voxel model theo bible → Export .vox + .png render
- Pitfall: KHÔNG dùng gradient/anti-aliasing — phải flat shading
- Reference: https://ephtracy.github.io/tutorials.html

### Bước 3 — Blender Render + Animate

- Tool: **Blender + Voxel plugin** (import .vox → animate)
- Alternative: **Blender 4.x** built-in voxel import (Python script)
- Workflow: Import .vox → Setup scene lighting → Animate walk cycle 12-24 FPS → Render PNG sequence (1080×1920 cho TikTok)
- Pitfall: Phải set frame rate 12 hoặc 24 (KHÔNG 30/60 FPS — sẽ mất voxel feel)
- Reference: https://docs.blender.org/manual/en/latest/animation/keyframes/

### Bước 4 — CapCut Edit

- Tool: **CapCut** (mobile hoặc desktop) + "Voxel Character" template trending 2026
- Workflow: Import PNG sequence → Add scene transitions voxel-style → Add text overlay (pixel font) → Add SFX + music → Export MP4
- Pitfall: KHÔNG dùng CapCut smooth transitions — dùng hard cuts pixel-style
- Template search: "voxel", "3D pixel", "Minecraft style"

## 5. RAPID PIVOT WORKFLOW (Quan trọng - 11/07/2026 lesson)

**Signal:** Anh ra 2 lệnh liên tiếp trong <10 phút:
1. *"đổi nhân vật từ A → B"* (thường là CON NGƯỜI từ đồ ăn/biến hình)
2. *"đổi visual style từ X → Y"* (thường là voxel 3D từ 2.5D Pixar/anime 2D)

**Workflow khi gặp rapid pivot:**

```
[1] ĐỌC NHANH 4 file cũ (5-10 min)
    - hub.md (project overview)
    - research/T-XX-universe.md (character design)
    - research/T-XX-template.md (script formula)
    - research/T-XX-samples.md (sample scripts)
    ↓
[2] IDENTIFY những gì GIỮ NGUYÊN (concept, story, voice, arcs)
    ↓
[3] IDENTIFY những gì ĐỔI (visual style + nhân vật form)
    ↓
[4] RE-DESIGN từng file cũ với "GIỮ NGUYÊN + ĐỔI" matrix
    - Mỗi file thêm 1 section "V1 vs V2" để track pivot
    - Mỗi file thêm frontmatter `pivot_date` + `pivot_reason`
    - Mỗi file thêm `supersedes` field trỏ về version cũ
    ↓
[5] UPDATE hub.md với PIVOT SUMMARY (table so sánh V1 vs V2)
    ↓
[6] LOG pivot event trong logs/YYYY-MM-DD-pivot-session.md
    ↓
[7] EMBED SUMMARY cho anh đọc Telegram (markdown table + checklist)
```

**Verified case 11/07/2026 (KarmaVid project):**

| Pivot | V1 → V2 |
|-------|---------|
| Nhân vật | Đồ ăn biến hình (Phở, Ớt, Bánh Mì, Nước Mắm, Xúc Xích) → CON NGƯỜI voxel 3D (Cô đầu bếp, Anh nông dân, Cậu bé, Bà chủ, Ông phản bội, Mẹ kế) |
| Visual style | 2.5D low-poly Pixar-like smooth → Voxel 3D pixel (Minecraft + Among Us hybrid) |
| Frame rate | 24-30 FPS mịn → 12-24 FPS voxel giật nhẹ (retro feel) |
| Camera | 3D free camera → Isometric 30-45° + close-up voxel |
| Palette | Vibrant smooth gradient → 16-32 màu flat shading retro pixel |
| GIỮ NGUYÊN | Concept "Karma là luật chơi" + 5 universe rules + bối cảnh Karmacity + Việt Nam retro + voice giọng Việt + series arcs |

**Timeline thực tế:** 2 lệnh pivot trong 6 phút → em đọc + re-design 4 file trong ~20 phút → embed summary trong 1 turn.

## 6. TOOLS & RESOURCES

### Tools sản xuất (theo thứ tự workflow)

| Tool | Vai trò | Platform | License |
|------|---------|----------|---------|
| **MagicaVoxel** | Tạo voxel character | macOS/Win/Linux | Free |
| **Blender 4.x** | Render + animate | macOS/Win/Linux | Free |
| **CapCut "Voxel Character" template** | Edit nhanh + text + sound | Mobile/Desktop | Free |
| **Voqul AI / ElevenLabs VI** | Voice tiếng Việt cho nhân vật | Web | Free tier |
| **PixelLab / PicsArt Pixel** | Backup nếu không có MagicaVoxel | Mobile | Free |

### Reference visual (paste vào brief cho designer)

- **Minecraft character skin** (Steve, Alex) — body proportion
- **Among Us crewmate** — lighting + shadow style
- **Stardew Valley villagers** — chibi face + pixel texture
- **Crossy Road** — 3D pixel depth + camera angle
- **Disney Crossy Road** — premium voxel quality

### TikTok trend 2026

CapCut "Voxel Character" template đang viral TikTok 2026 — em đã verify qua `social-media-trends` skill (NEW June 2026).

## 7. PITFALLS — Lessons learned

### Pitfall #1 (NEW 11/07/2026): Nhầm voxel 3D với pixel art 2D

**Triệu chứng:** Em viết "pixel style" trong script mà quên specify "3D voxel" → designer hiểu nhầm thành 2D pixel art phẳng.

**Fix:** MỖI scene PHẢI có:
- Camera angle (isometric 30-45° = voxel 3D, top-down = 2D pixel)
- Lighting (flat shading + ambient occlusion = voxel 3D, NO lighting = 2D pixel)
- Frame rate (12-24 FPS = voxel 3D, 60 FPS = smooth 3D)

### Pitfall #2 (NEW 11/07/2026): Nhân vật CON NGƯỜI bị render thành đồ ăn

**Triệu chứng:** Em describe "Cô gái đầu bếp" trong brief mà KHÔNG specify voxel body parts (đầu, tay, chân riêng biệt) → MagicaVoxel render thành 1 khối blob giống đồ ăn.

**Fix:** Character bible PHẢI có:
- Body parts tách rời (đầu / thân / 2 tay / 2 chân = 6 sections)
- Voxel cube count cụ thể cho mỗi part (đầu = 20 cubes, thân = 40 cubes, etc.)
- Distinguishing feature (1-2 điểm nhận diệt ngay)

### Pitfall #3 (NEW 11/07/2026): Frame rate 30/60 FPS = mất voxel feel

**Triệu chứng:** Designer render Blender ở 30 hoặc 60 FPS → animation mịn như Pixar → KHÔNG còn là voxel retro.

**Fix:** Set frame rate 12-24 FPS trong Blender render settings. 12 FPS = voxel retro giật nhẹ (khuyến nghị cho narrative scenes). 24 FPS = voxel mượt hơn (chỉ dùng cho montage/training scene).

### Pitfall #4 (NEW 11/07/2026): Palette gradient mịn = không phải voxel

**Triệu chứng:** Designer dùng 64+ màu với gradient mịn → render giống 3D smooth chứ KHÔNG phải voxel flat shading.

**Fix:** Limit 16-32 màu/nhân vật + flat shading (NO gradient). Palette phải được list cụ thể (hex codes) trong character bible.

### Pitfall #5 (CRITICAL 11/07/2026): Ambiguous phrase → confirm trước khi pivot

**Triệu chứng:** Anh gõ "3D pixal" → em default theo trend TikTok 2026 (CapCut "Voxel Character" template) → re-design 4 file sang voxel → 17 phút sau anh phải sửa thành "3D Pixar" (typo thiếu "r").

**Root cause:** Em KHÔNG confirm khi phrase AMBIGUOUS giữa 2 style rất khác nhau (voxel 3D pixel vs Pixar 3D cinematic). Em assume "pixal" = "pixel" dựa theo trend.

**HARD RULE (applies to ALL pivot decisions):**
1. **Khi anh dùng phrase ambiguous** (pixel vs Pixar, voxel vs smooth, 2D vs 3D, low-poly vs high-detail) → **PHẢI confirm trước khi re-design 4 files**
2. **Style guide PHẢI có reference film cụ thể** — voxel = "Minecraft, Among Us, Stardew Valley"; Pixar = "Toy Story, Inside Out, Coco, Frozen"
3. **KHÔNG default theo trend TikTok** khi phrase unclear — trend ≠ user's intent
4. **Khi anh sửa typo trong cùng session** → re-design ngay không argue, KHÔNG giữ pivot sai
5. **Cost of wrong pivot** = 30 phút wasted (17 phút re-design + 13 phút correct) — cao hơn cost of 1 câu confirm

**Anti-pattern (EM ĐÃ SAI lần này):**
- ❌ Assume em hiểu đúng dựa trên trend
- ❌ Re-design 4 files ngay khi phrase ambiguous
- ❌ Skip confirmation step "anh muốn Pixar hay voxel?"
- ❌ Default theo CapCut template trending 2026

**Correct pattern (HARD RULE):**
- ✅ Phrase ambiguous → Ask 1 câu confirm trước khi re-design (≤30 giây)
- ✅ Cite reference film: "Anh muốn style Minecraft/Among Us (voxel) hay Toy Story/Inside Out (Pixar)?"
- ✅ Nếu confirmed → re-design ngay với đúng style
- ✅ Khi pivot sang style khác (trong cùng session) → re-design toàn bộ, giữ nguyên nhân vật/câu chuyện

**Verified cost:** KarmaVid V3 case = 30 phút wasted vì không confirm → bài học: 1 câu confirm = tiết kiệm 30 phút.

## 12. RELATED SIBLING SKILL — Pixar 3D Animation

Khi anh pivot từ voxel sang Pixar (hoặc ngược lại), load **sibling skill** `pixar-3d-animation` (creative/) để có Pixar-specific workflow (Blender + Character Animator + DaVinci Resolve + cinematic lighting specs).

**Decision rule — voxel vs Pixar:**
- Voxel: Gen Z + retro pixel lovers + CapCut template nhanh + TikTok viral ngắn hạn
- Pixar: Family + emotional storytelling + render lâu + TikTok viral dài hạn (rewatchable)

Xem `pixar-3d-animation` skill mục 1 bảng so sánh chi tiết.

## 8. RELATED SKILLS

- **`pixel-art`** (creative/) — 2D pixel art conversion (image→PNG). Distinct từ voxel 3D character animation. Load nếu user cần STATIC pixel art, KHÔNG phải animated voxel characters.
- **`tiktok-viral-script`** (social-media/) — TikTok script structure (hook + body + CTA). Dùng KẾT HỢP với skill này khi viết script cho TikTok animation.
- **`tiktok-product-script`** (content/) — Generate TikTok sales script từ product info. KHÔNG liên quan trực tiếp, nhưng character animation project có thể dùng để research audience trước khi viết script.
- **`tiktok-video-editor`** (media/) — TikTok raw clip editing workflow. Dùng SAU khi render voxel animation xong, để edit cuối + add sound + text.
- **`clone-and-adapt-competitor`** — Clone competitor channel style. Dùng KẾT HỰỚC với skill này khi muốn clone 1 channel voxel animation nào đó (vd: Disney Crossy Road, Among Us animation).
- **`ideation`** (creative/) — Brainstorm project ideas qua creative constraints. Dùng TRƯỚC khi bắt đầu project voxel animation để có concept chắc chắn.

## 9. CHECKLIST (áp dụng trước khi ship)

- [ ] Character bible có 8 sections (Body, Head, Outfit, Props, Face, Chiều cao, Distinguishing feature, Voice + Palette)
- [ ] Voxel color palette 16-32 màu flat shading (NO gradient)
- [ ] Frame rate 12-24 FPS (KHÔNG 30/60)
- [ ] Camera isometric 30-45° default (KHÔNG flat 2D)
- [ ] Mỗi scene có visual direction 3D pixel voxel đầy đủ 6 fields
- [ ] MagicaVoxel export có .vox file cho mỗi nhân vật
- [ ] Blender render output là PNG sequence (KHÔNG video trực tiếp — để CapCut edit sau)
- [ ] CapCut edit dùng hard cuts pixel-style (KHÔNG smooth transitions)
- [ ] Voice tiếng Việt rõ ràng, đúng tone nhân vật
- [ ] Test render 1 scene đầu tiên + verify visual style trước khi batch render toàn bộ

## 10. TRIGGER EXAMPLES (để nhận biết khi nào load skill này)

```
# Rapid pivot signal (2 lệnh liên tiếp trong <10 phút)
"đổi nhân vật thành con người"
"style 3D pixel voxel"

# Direct trigger
"làm animation voxel cho TikTok"
"tạo character bible Minecraft style"
"Among Us style animation"
"Stardew Valley character cho video"

# Production pipeline
"MagicaVoxel export character"
"Blender render animation voxel"
"CapCut voxel template"

# Pivot trigger (existing animation project đổi style)
"đổi từ 2.5D Pixar sang voxel 3D"
"đổi từ anime 2D sang 3D pixel"
"đổi từ low-poly sang voxel"
```

## 11. VERIFIED CASE STUDY (KarmaVid project 11/07/2026)

**Project:** KarmaVid — TikTok animation channel
**Universe:** 3 CON NGƯỜI voxel 3D + 3 phản diện voxel + 5 locations Việt Nam retro
**Pivot signal:** Anh ra 2 lệnh liên tiếp trong 6 phút (16:32 + 16:38 ngày 11/07/2026)
**Workflow applied:**
1. Em đọc 4 file cũ (hub + T-02.1 universe + T-03.1 template + T-03.2 samples)
2. Em identify: GIỮ NGUYÊN (concept Karma + 5 universe rules + voice + arcs), ĐỔI (nhân vật + visual style)
3. Em re-design 4 file với pivot matrix (V1 vs V2)
4. Em update hub.md với pivot summary
5. Em log pivot event trong logs/2026-07-11-pivot-v2-session.md
6. Em embed summary cho anh đọc Telegram (table V1 vs V2 + sample script demo)

**Timeline:** 2 lệnh pivot → 4 file updated (~20 min) → embed summary (1 turn) = DONE.

**Output:**
- hub.md (10.8 KB) — pivot summary + visual style guide
- research/T-02.1-karmavid-universe.md (19.7 KB) — 3 CON NGƯỜI voxel + 3 phản diện voxel
- research/T-03.1-karmavid-script-template.md (13.6 KB) — visual direction 3D pixel cho MỖI scene
- research/T-03.2-karmavid-script-samples.md (17.3 KB) — 2 sample scripts với nhân vật người voxel

**Total content:** 61.4 KB across 4 files (đủ để anh đọc ngay trên Telegram qua embed summary).

## Related

- [[pixel-art]] (skill) — 2D pixel art conversion (companion skill, KHÔNG overlap)
- [[tiktok-viral-script]] (skill) — TikTok script structure (kết hợp)
- [[tiktok-video-editor]] (skill) — Final edit (sau khi render voxel xong)
- KarmaVid project: `/Volumes/Storage-1/Hermes/wiki/projects/karmavid/`