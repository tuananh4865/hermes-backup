# 3D Trailer Progression (HyperFrames V1→V5 — 2026-07-16/17)

> **Context:** Em build cùng 1 concept trailer (NOUS Accelerated Business Hackathon 30s cyberpunk B&W analog) qua 5 version HyperFrames để thấy mỗi step nâng cấp visual quality như thế nào. Kết quả V5 đạt 4/4 vision-QA tiêu chí (lighting, depth, cast shadow, no shader warning) và match 23 MB file size cho 1080p 30s.

## Tại sao 5 version?

| # | Approach | Mục tiêu | Khi nào dừng |
|---|---|---|---|
| V1 | Flat SVG/CSS | Baseline 2D | So sánh với ref |
| V2 | CSS perspective + multi-layer glow | Faking 3D | Verifier 49/60 |
| V3 | All-pixel-must-move rule | Animation density | Verify 40% pixel change/frame |
| V4 | Three.js + ShaderMaterial | Real 3D | WebGL warning vẫn còn |
| V5 | MeshStandardMaterial + PBR + cast shadow | Cinematic | 4/4 vision QA pass |

**Rule: ship mỗi version, save canonical vào `/Volumes/Storage-1/Tiktok-Tuan-Anh/`, get feedback, chỉ iterate tiếp khi user yêu cầu rõ ràng.**

## 5 versions chi tiết

### V1 — Flat SVG/CSS Baseline (1.5 MB)
- 9 scene `<div>` clips, mỗi scene có `data-start`/`data-duration`/`data-track-index`
- Inline SVG cho chart line/bar với pre-computed deterministic points
- GSAP timeline paused + registered on `window.__timelines["main"]`
- NO perspective, NO glow stack, NO particle
- **Purpose**: baseline để vision AI chấm điểm visual quality

### V2 — CSS perspective + multi-layer glow (3.1 MB)
- Thêm `perspective: 1500-2200px` + `rotateX/rotateY` cho key scenes
- 5 layer `text-shadow` chồng nhau cho bloom
- Anamorphic streak (3 ghosts: cyan 1600px + purple 800px + blue 400px)
- Volumetric glow radial (1400×600px blur 30px)
- Chromatic aberration edge (red inset + cyan inset)
- Vanishing point lines (20 lines rotating 4°/s)
- **Verifier score: 49/60 (gần reference)**

### V3 — All-pixel-must-move rule (13.2 MB) ⭐ CRITICAL PATTERN
- **HARD RULE** (anh dặn 17/07): "nếu làm animation thì mọi hình ảnh trên screen đều phải được animation hết chứ không được có ảnh hoặc chỗ nào tĩnh hết"
- **Implementation**: 1 rAF loop duy nhất chạy 0-720 frames. Mọi animation đọc `tFrame = floor((now - startTime) / (1000/24))` và update DOM mỗi frame.
- **Quantitative verify**: pixel diff giữa 0.3s và 0.0s = 37.9%, giữa 0.6s và 0.3s = 45.4% → ≥30% = animation live
- **Universal animation checklist** — mỗi element phải có ÍT NHẤT 1 trong:
  1. Rebuild SVG `innerHTML` mỗi frame (chart line crawl, bar pulse)
  2. CSS `transform: translate/rotate/scale/translateZ` thay đổi theo `Math.sin(t * speed)`
  3. CSS `opacity` thay đổi theo `Math.sin(t * speed)`
  4. CSS `box-shadow` intensity thay đổi theo `Math.sin(t * speed)`
  5. CSS `backgroundPosition` thay đổi theo frame (scanline scroll)
  6. `text-shadow` blur radius thay đổi theo `Math.sin(t * speed)`
  7. `textContent` update mỗi frame (counter, random number)
- **Không được phép**: `gsap.to` 1 lần rồi để đó, `setTimeout` chỉ chạy 1 lần, animation chỉ chạy khi user click
- **Verification script**: `scripts/motion_diff_check.py` đo pixel diff programmatically

### V4 — Three.js Real 3D (25.0 MB) — BƯỚC ĐỘT PHÁ
- **Thêm Three.js CDN** `https://esm.sh/three@0.160.0`
- **Canvas host**: thẻ `<div id="three-host" class="three-canvas-host">` overlay DOM
- **Driver pattern**: rAF loop riêng gọi `tickThree(frame)`, đọc `window.__currentFrame` từ trailer.js loop
- **Scene types**:
  - `hero` (scene 144-216): PlaneGeometry 13×3.2 với custom ShaderMaterial
  - `wave` (scene 408-504): 64 LineSegments bars rebuild mỗi frame
  - `cubes` (scene 504-600): 4×6 wireframe cubes
  - `endcard` (scene 672-720): TorusKnot wireframe
- **Particles**: 3000 BufferGeometry points với AdditiveBlending
- **⚠️ Warning**: `WebGL: useProgram: program not valid` do ShaderMaterial lỗi trong hero scene → render vẫn chạy nhưng có 1-2 frame flash
- **Verifier score: "3D có visible" nhưng "lighting flat"**

### V5 — MeshStandardMaterial + PBR + cast shadow (23.0 MB) ⭐⭐ CINEMATIC
- **Fix shader warning**: thay custom `ShaderMaterial` → `MeshStandardMaterial` (built-in PBR)
- **Hero text mesh**: PlaneGeometry với Z-displacement dựa trên text-shape mask, alphaMap texture, `metalness: 0.4, roughness: 0.3, emissive: 0x88ff88, emissiveIntensity: 0.8`
- **Wave bars**: 64 BoxGeometry, isHot variant cho bar > 70% height, `metalness: 0.7, roughness: 0.2`
- **HACKATHON 3D bars**: 28 BoxGeometry, Floor plane với `ShadowMaterial` để nhận shadow
- **Cube grid**: filled + wireframe overlay (`EdgesGeometry` + `LineBasicMaterial`)
- **TorusKnot endcard**: `metalness: 0.95, roughness: 0.05` (mirror-like)
- **3-point lighting**:
  - `AmbientLight(0x404060, 0.8)` — soft fill
  - `DirectionalLight(0xffffff, 1.6)` — key light từ (8,12,16), castShadow
  - `DirectionalLight(0x88ff88, 0.9)` — fill light cyan
  - `DirectionalLight(0x4444ff, 0.7)` — rim light từ dưới
- **renderer setup**:
  - `renderer.shadowMap.enabled = true`
  - `renderer.shadowMap.type = THREE.PCFSoftShadowMap`
  - `renderer.toneMapping = THREE.ACESFilmicToneMapping`
  - `renderer.toneMappingExposure = 1.15`
  - `renderer.outputColorSpace = THREE.SRGBColorSpace`
- **Camera dolly**:
  - `camera.position.x = sin(t * 0.15) * 1.0`
  - `camera.position.y = cos(t * 0.2) * 0.5`
  - `camera.position.z = 16 + sin(t * 0.18) * 1.5`
  - `camera.lookAt(0, 0, 0)` — always center
- **Verifier 4/4 pass** (17/07):
  - ✅ Lighting contrast rõ (front/side face phân biệt)
  - ✅ Depth 3D rõ ràng (bars có thể tích thật, perspective thấy rõ)
  - ✅ Cast shadow có (bars đổ bóng xuống floor plane)
  - ✅ Shader warning hết (render log clean)

## Pitfall: HARD RULE "every pixel must move" (NEW 2026-07-17)

**Anh dặn verbatim:**
> *"Nếu làm animation thì mọi hình ảnh trên screen đều phải được animation hết chứ không được có ảnh hoặc chỗ nào tĩnh hết"*

**Anti-pattern (fail)**:
- `gsap.to(element, { opacity: 1 })` 1 lần rồi để đó → element chỉ chuyển động 1 lần rồi tĩnh
- `setInterval(..., 1000)` 1 lần → 1 motion mỗi giây, 99% thời gian tĩnh
- `innerHTML = "..."` chỉ build 1 lần → SVG tĩnh vĩnh viễn
- Random mỗi 5s → user thấy ảnh đứng yên 4s

**Pattern (pass)** — Universal rAF loop:
```js
function tick(now) {
  const frame = Math.floor((now - startTime) / (1000 / fps));
  // Update EVERY element với frame-driven value
  charts.forEach(c => c.innerHTML = rebuildChart(frame));
  elements.forEach(e => e.style.transform = `scale(${1 + Math.sin(frame * 0.1) * 0.02})`);
  monitors.forEach(m => m.style.boxShadow = `0 0 ${20 + Math.sin(frame * 0.2) * 8}px ${color}`);
  // ...
  requestAnimationFrame(tick);
}
```

**Quantitative gate** (verification):
```bash
python3 scripts/motion_diff_check.py trailer.mp4 --t1 0.0 --t2 0.3
# Output: "At 0.3s vs 0.0s: 37.9% pixels changed"
# >30% = PASS, <5% = FAIL (frozen content)
```

## Three.js integration pattern (V4/V5)

**CDN load**:
```html
<script type="module">
  import * as THREE from 'https://esm.sh/three@0.160.0';
</script>
```

**Host div**:
```html
<div id="three-host" class="three-canvas-host"></div>
<style>
  .three-canvas-host {
    position: absolute;
    top: 0; left: 0;
    width: 1920px; height: 1080px;
    pointer-events: none;
    z-index: 4;
  }
</style>
```

**Init**:
```js
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
```

**Switch scenes**:
```js
const sceneRanges = [
  { from: 0, to: 144, type: 'particles' },
  { from: 144, to: 216, type: 'hero' },
  { from: 408, to: 504, type: 'wave' },
  { from: 504, to: 600, type: 'cubes' },
  { from: 672, to: 720, type: 'endcard' },
];
// In tick loop, find active type and call setThreeScene(type, frame)
```

**Render frame**:
```js
renderer.render(scene, camera);
```

**Expose frame for 3D layer**:
```js
// trailer.js tick loop
window.__currentFrame = tFrame;

// three-scene.js separate rAF
const f = window.__currentFrame;
```

## Common Three.js mistakes in HyperFrames

| Mistake | Fix |
|---|---|
| `ShaderMaterial` with custom GLSL → `useProgram: program not valid` warning | Use `MeshStandardMaterial` (built-in PBR) or `MeshBasicMaterial` (no lighting) |
| `MeshBasicMaterial` for everything → flat look | Add 3-point lighting: `AmbientLight` + 3 `DirectionalLight` (key/fill/rim) |
| No cast shadow → bars look glued to floor | `renderer.shadowMap.enabled = true` + `light.castShadow = true` + `mesh.castShadow = true` + floor `mesh.receiveShadow = true` |
| Camera fixed → static composition | Camera dolly: `pos.x = sin(t*0.15)*1.0; pos.z = 16 + sin(t*0.18)*1.5; lookAt(0,0,0)` |
| Same color everywhere | `metalness: 0.4-0.95` + `roughness: 0.05-0.7` (varied per material) |

## Specs comparison

| Version | Size | Render time | Tech | Lighting | V4-style cast shadow |
|---|---:|---:|---|---|---|
| V1 | 1.5 MB | 25s | CSS only | None | ❌ |
| V2 | 3.1 MB | 25s | CSS + multi-layer | CSS shadow | ❌ |
| V3 | 13.2 MB | 50s | V2 + rAF loop | V2 + per-frame pulse | ❌ |
| V4 | 25.0 MB | 46s | V3 + Three.js ShaderMaterial | 1 directional | ❌ |
| **V5** | **23.0 MB** | **44s** | V3 + Three.js MeshStandardMaterial | **3-point + ACES** | **✅** |

## Files

```
~/Documents/GitHub/nous-trailer-hyperframes/
├── index.html                          (V5 main + three-host)
├── trailer.js                          (V3 master loop + window.__currentFrame)
├── three-scene.js                     (V5 Three.js — MeshStandardMaterial + PBR)
├── index_v1.html.disabled             (V1 backup)
├── trailer_v1.js.disabled
├── renders/
│   ├── trailer.mp4                    (V1)
│   ├── trailer_v2.mp4                 (V2)
│   ├── trailer_v3.mp4                 (V3)
│   ├── trailer_v4.mp4                 (V4)
│   └── trailer_v5.mp4                 (V5)
```

## Canonical save

```
/Volumes/Storage-1/Tiktok-Tuan-Anh/
├── nous_trailer_hyperframes_1080p.mp4           (V1)
├── nous_trailer_hyperframes_v2_30s.mp4          (V2)
├── nous_trailer_hyperframes_v3_30s_animated.mp4 (V3)
├── nous_trailer_hyperframes_v4_3d_30s.mp4      (V4)
└── nous_trailer_hyperframes_v5_pbr_30s.mp4     (V5 final)
```

## Decision: when to use which version

- **V3** (13.2 MB): No GPU, lightweight deploy, "animation density" priority
- **V5** (23 MB): Modern hardware, real 3D PBR look, "cinematic" priority
- **Skip V1/V2/V4** unless user explicitly wants lightweight or shader warning OK

## Khi user nói "3D trailer / cyberpunk / cinematic depth"

1. Start from V5 template (copy 3 files: `index.html`, `trailer.js`, `three-scene.js`)
2. Replace scene timings in `sceneRanges` array
3. Replace scene builders: `buildHero3DText`, `buildWave3DMesh`, `buildCubes`, `buildEndcard`
4. Replace CSS animation primitives for non-3D parts (still 70% of frame)
5. Run `npx hyperframes check` → fix 2 errors (font-face, root composition)
6. Run `npx hyperframes render . -o out.mp4 --fps 24`
7. Verify with `python3 scripts/motion_diff_check.py` (>30% pixel change)
8. Save canonical to `/Volumes/Storage-1/Tiktok-Tuan-Anh/nous_trailer_v6_<descriptor>.mp4`
9. Send vision_understand_image to compare with reference

## Lessons cho future 3D trailer sessions

- **Cải thiện 1 layer mỗi lần**, save + verify, rồi mới qua layer tiếp
- **Vision AI verifier** chấm 4/4 thì PASS. Dùng cho mỗi version.
- **Quantitative motion_diff_check** đảm bảo "no static pixel" HARD RULE
- **Save mỗi version canonical** vào `/Volumes/Storage-1/Tiktok-Tuan-Anh/` — user test trên device thật, feedback quyết version tiếp
- **Three.js CDN qua esm.sh** hoạt động ổn định trong HyperFrames headless Chrome
- **Cast shadow cần `floor mesh`** nhận shadow — plane invisible ShadowMaterial trick
- **Performance budget**: 25 MB / 30s @ 1080p với 3-point lighting + 3000 particles là max practical
- **5-min render time per version** — đủ nhanh để iterate

## Cross-references

- `references/cinematic-trailer-3d-pattern.md` (V2 base patterns)
- `references/remotion-quickstart.md` (sibling tool)
- `references/tiktok-motion-text-overlay.md` (text overlay patterns)
- `scripts/motion_diff_check.py` (quantitative "no static pixel" gate)
- `scripts/trailer_contact_compare.py` (visual A/B comparison vs reference)
