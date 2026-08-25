---
title: Mascot from Photo — Generate Cartoon Mascot from Real Portrait
created: 2026-07-11
type: reference
tags: [mascot, image-generation, branding, chibi-cartoon, vuive-style]
confidence: medium
relationships: [clone-and-adapt-competitor]
---

# Mascot from Photo — Generate Cartoon Mascot from Real Portrait

> Reference for when user wants their YouTube channel mascot to be a 2D cartoon version of THEIR OWN FACE (not a generic mascot). Common request when cloning edutainment channels like @VuiVe that use signature mascots.

## When to use this reference

- User says "làm mascot từ ảnh tôi", "chuyển hình tôi thành cartoon", "chuyển hình của anh thành cách vẻ giống X"
- User sends a portrait photo AND wants it converted to cartoon mascot style
- User is building a YouTube channel clone and wants personal brand identity

**Distinct from:**
- Generic mascot creation (no source photo) — different workflow
- Logo design (no character needed) — use graphic designer
- Style transfer to video (not image) — different tool

## 4-Step Workflow

### Step 1 — Analyze portrait signature features

Before generating ANY image, extract the user's signature features from the photo:

| Feature | What to capture | Why it matters |
|---------|----------------|----------------|
| **Hair** | Color, length, style, texture (straight/curly/wavy), parting, fringe/bangs | Most distinctive visual token — biggest differentiation lever |
| **Face shape** | Oval, round, square, heart | Affects chibi proportions |
| **Eyes** | Size, shape, double-eyelid? | "Mischievous grin" needs slightly cross-eyed / side-eye |
| **Nose** | Bridge height, tip shape | Determines chibi nose simplification |
| **Mouth** | Lip thickness, smile style | Affects "smug smile" rendering |
| **Skin tone** | Light, medium, dark | Preserve in cartoon (don't whitewash) |
| **Clothing** | Color, style, fit | Maps to cartoon t-shirt color |
| **Tattoos / accessories** | Visible marks, glasses, piercings | Keep or simplify? Ask user |
| **Expression** | Neutral, smiling, talking, angry | Default to "mischievous grin" if cloning Vui Vẻ-style |

**Output:** Mental note of 4-5 strongest signature features to preserve in cartoon version.

### Step 2 — Determine style formula from target channel

If cloning a specific channel (e.g. Vui Vẻ), extract the mascot style formula from that channel's audit:

**@VuiVe formula (CORRECTED 2026-07-11 — verified via mascot image, NOT thumbnail inference)** |
|---------|----------------------------------------|
| **Art style** | **Western Cartoon Mỹ** (Adventure Time / Gumball / Regular Show style) — KHÔNG phải chibi Nhật, KHÔNG phải anime |
| **Body proportions** | **SQUARE head**, large head = 50-60% of total height, simple stick limbs |
| **Eyes** | **CLOSED/SQUINTING** (signature ^^_ style) — KHÔNG big round open eyes |
| **Eyes asymmetry** | **2 mắt LỆCH nhau** (1 to 1 nhỏ) — signature quirk |
| **Mouth** | Small OPEN O shape (surprised/talking) |
| **Hair** | Signature token (Vui Vẻ = PINK/MAGENTA, SQUARE/ANGULAR with 1 prominent spike) |
| **Clothing** | Mustard YELLOW t-shirt + DARK NAVY PURPLE tie (LOPSIDED, hanging down) |
| **Skin tone** | LIGHT PINKISH-WHITE (very pale) |
| **Line art** | **BLACK THICK outline** (~3-4px) with VARIABLE thickness (dày ở góc, mỏng ở cong) + natural wobble |
| **Palette** | Dark navy OR white/cream bg, vibrant character colors, no gradient, NO 3D effect |
| **Pose** | **3/4 VIEW** (NOT front-facing thẳng) — one hand at CHIN (thinking pose) |
| **Tool** | Hand-drawn Procreate/iPad — brush stroke tự nhiên, slight jaggedness on curves |
| **Drop shadow** | Subtle shadow under feet |
| **No big-font text** on character |
| **Pose signature** | One hand at chin (thinking/talking pose) |

**Adjust formula based on target** (if cloning another channel, replace formula).

### Step 3 — Generate 4 variations with differentiated tokens

The differentiation rule (from `clone-and-adapt-competitor` Pitfall #10): **keep FORMULA 100% same, swap COLOR PALETTE + signature tokens**.

Generate 4 variations, each with different hair color + shirt color combos:

```
Variation 1: Hair CYAN BLUE + Shirt ORANGE (signature "tech")
Variation 2: Hair MAGENTA-PINK + Shirt YELLOW (echo competitor but different palette)
Variation 3: Hair ELECTRIC PURPLE + Shirt RED (mystic)
Variation 4: Hair LIME GREEN + Shirt BLACK (dark/edgy)
```

**Image generation prompt template (CORRECTED for Vui Vẻ Western Cartoon Mỹ style):**

```
A 2D Western cartoon mascot portrait (NOT chibi, NOT anime) in style
of Vietnamese YouTube channel Vui Vẻ. Young Vietnamese male character
with messy [HAIR COLOR] spiky/angular hair with one prominent spike
pointing up-right, big SQUARE head = 50-60% of total height, 
CLOSED/SQUINTING eyes with slight asymmetric (1 eye slightly 
different from other) drawn as curved arcs like smiling eyes (^_^),
small OPEN O-shape mouth, light pinkish-white skin, SQUARE-JAWED 
face shape, wearing a bright [SHIRT COLOR] t-shirt with DARK NAVY 
PURPLE tie hanging lopsided, one hand at CHIN (thinking/talking pose), 
other arm relaxed, 3/4 VIEW standing pose (not perfectly front-facing), 
legs as 2 simple straight lines, small oval shoes. BLACK THICK 
outline (~3-4px) with VARIABLE thickness + natural brush wobble, 
slight jaggedness on curved lines. NO gradients, NO shading, 
NO 3D effect, NO watercolor. ALL FLAT COLOR FILLS. Subtle drop 
shadow under feet. Hand-drawn Procreate/iPad style. White or dark 
navy background.
```

**Style reference images** (for image_generate with `reference_image_urls`):
- User's actual portrait photo (preserves signature features)
- Reference: Adventure Time / Gumball character style (if user wants to preserve Western Cartoon Mỹ formula)

**CRITICAL:** DO NOT use "2D chibi" in the prompt — Vui Vẻ mascot is Western Cartoon Mỹ (Adventure Time style), not chibi. The corrected prompt above captures the actual style.

### Step 4 — Verify + iterate

After generating 4 variations:

1. **Show user** all 4 side-by-side with color palette breakdown
2. **Ask user to pick 1** OR request specific tweaks (e.g. "Variation 2 but lighter hair")
3. **Generate final version** with user's chosen palette + signature features preserved
4. **Deliver** as PNG/JPG at 1024x1024 (square for YouTube avatar) + 512x512 (compressed for thumbnails)

## Pitfalls

1. **Don't generate without analyzing photo first.** Skipping Step 1 → generic mascot that looks like every other creator. User explicitly wanted "chuyển hình của anh" — preserve HIS features.

2. **Don't copy competitor's mascot color verbatim.** Even if user says "giống Vui Vẻ" → swap the color tokens (tóc hồng → tóc xanh dương) to avoid copycat accusation. The FORMULA (chibi, dark bg, mischievous) is reusable; the COLORS are copyrighted identity.

3. **FAL/MiniMax image generation may fail with auth errors (2026-07-11).** If `image_generate` tool returns "Cannot access application fal-ai/flux-2-klein" → BLOCKER, do NOT fake output. Report blocker to user + provide prompt template for them to use in Midjourney/DALL-E/Leonardo AI/ComfyUI.

4. **Don't whitewash skin tone.** Preserve the user's actual skin color in cartoon version.

5. **Don't simplify away distinctive features.** If user has round face + small eyes + thick lips → preserve these in chibi version. The "chibi" style is about proportions (big head, small body) not feature elimination.

6. **Tattoos / glasses / accessories** — ASK user whether to keep or simplify. Don't assume.

7. **Show all 4 variations before picking** — let user decide, don't pre-select "best" one. Variation comparison builds trust.

8. **Generate at 1024x1024 minimum** for YouTube avatar quality. Lower resolution = pixelated when used in thumbnails.

## Real Case Reference (2026-07-11)

User: Tuấn Anh (Vietnamese content creator, 1998, Ngoại thương university)
Photo: Selfie in gaming setup, brown T-shirt, messy black hair with slight wave, round face, big eyes, thick lips, arm tattoo visible

Target: @VuiVe-style mascot for new YouTube channel "Mọi Thứ Cũng Đơn Giản Thôi"

Generated variations (all FAILED due to FAL auth error → reported blocker):

| Var | Hair | Shirt | Differentiation |
|-----|------|-------|-----------------|
| 1 | Cyan blue | Orange | "Tech" vibe |
| 2 | Magenta-pink | Yellow | Echo Vui Vẻ pink but different shirt |
| 3 | Electric purple | Red | Mystic |
| 4 | Lime green | Black | Dark/edgy |

**Lesson:** Always analyze signature features FIRST. Even though image generation failed, the 4-variation prompt set was ready for user to use in their own tools.