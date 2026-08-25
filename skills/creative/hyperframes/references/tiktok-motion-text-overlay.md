_content># TikTok Motion Text Overlay — Voice-Synced Kinetic Typography

> **Khi user yêu cầu:** "chèn hiệu ứng text theo voice" / "chữ chuyển động hiện ra theo lời thoại" / kinetic typography cho TikTok video.

## ⚠️ Critical User Preference (L22 2026-07-16)

**User đã explicit correct em:** Anh muốn **HIỆU ỨNG chữ chuyển động (motion graphics)** hiện ra theo voice — KHÔNG phải **subtitle tĩnh** (text fade in/out rồi biến mất).

| ❌ SAI (subtitle) | ✅ ĐÚNG (motion text) |
|---|---|
| Chữ fade in/out | **Chữ pop in bouncy** (scale 0.5 → 1.15) |
| Highlight màu vàng + scale | **Highlight vàng + scale + glow text-shadow** |
| Từ tĩnh | **Từng từ typewriter animation** |
| Container phẳng | **Box đen blur + shadow** |

Nếu user nói "chữ theo voice" / "text sync" → đây là **MOTION TEXT**, không phải subtitle. Hỏi lại nếu nghi ngờ.

## Pipeline (7 bước)

### 1. Setup project
```bash
npx hyperframes init <project> --non-interactive --example kinetic-type
cd <project>
mkdir assets
```

### 2. Whisper extract word-level timestamps
```python
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-format json --word-timestamps True \
  --condition-on-previous-text False \
  --output-dir <worktree>/audio.json <input>.mp4
```

### 3. Group words thành phrases (CRITICAL: ≤27 phrases!)
- **HyperFrames có limit DOM elements** — 80 phrases bị silent crash, chỉ load 1 phrase
- **30 phrases max** để safe
- Group bằng cách: merge 3 phrases nhỏ thành 1 phrase lớn (~5-7 từ)

```python
phrases = []
i = 0
while i < len(all_words):
    chunk = all_words[i:i+5]
    phrases.append({
        "start": chunk[0]["start"],
        "end": chunk[-1]["end"],
        "text": " ".join([w["word"] for w in chunk])
    })
    i += 5
```

### 4. Copy video vào project assets (BẮT BUỘC — không dùng file://)
```bash
cp <final_clip>.mp4 <project>/assets/clip.mp4
```

### 5. Create composition file (sub-composition pattern)
File: `<project>/compositions/tiktok-motion-text.html`

**QUAN TRỌNG — phải dùng sub-composition (`data-composition-src`), KHÔNG inline DOM ngoài root** vì HyperFrames render ẩn các DOM elements trong root, chỉ render sub-composition đúng cách.

### 6. Critical CSS pitfalls (L16 2026-07-16)

| Pitfall | Fix |
|---|---|
| Inline-block word + space character bị **CSS collapse** | Dùng **`&nbsp;&nbsp;`** trong `innerHTML` của `.word-space` span |
| Space span width 0.4em quá nhỏ | **0.6em** |
| Space span thiếu vertical-align | Thêm **`vertical-align: baseline`** |
| Google Fonts bị **ERR_BLOCKED_BY_ORB** trong headless Chrome | Dùng system font: `-apple-system, BlinkMacSystemFont, "SF Pro Display"` |
| Watermark `@tuancuaban` bị dính liền | Thêm space: `@ tuancuaban` |
| Font HyperFrames không render Vietnamese glyph đầy đủ | Test frame + dùng vision_analyze để verify |

**Template `.word-space` span BẮT BUỘC:**
```css
.word-space {
  display: inline-block;
  white-space: pre;
  width: 0.6em;
  opacity: 1 !important;
  transform: none !important;
  vertical-align: baseline;
}
```

**Template DOM build:**
```javascript
words.forEach((w, wIdx) => {
  const wordSpan = document.createElement('span');
  wordSpan.className = 'word';
  wordSpan.textContent = w;
  textDiv.appendChild(wordSpan);

  // Thêm space giữa các word (KHÔNG thêm sau word cuối)
  if (wIdx < words.length - 1) {
    const spaceSpan = document.createElement('span');
    spaceSpan.className = 'word-space';
    spaceSpan.innerHTML = '&nbsp;&nbsp;';  // CRITICAL: innerHTML not textContent
    textDiv.appendChild(spaceSpan);
  }
});
```

### 7. GSAP Timeline Animation (motion graphics)
```javascript
const tl = gsap.timeline({ paused: true });
window.__timelines["tiktok-motion-text"] = tl;

phrasesData.forEach((phrase, pIdx) => {
  const phraseEl = phraseEls[pIdx];
  const words = phraseEl.querySelectorAll('.word');
  const phraseDur = phrase.end - phrase.start;

  // Initial state
  gsap.set(phraseEl, { opacity: 0 });
  gsap.set(words, { opacity: 0, y: 40, scale: 0.5 });

  // Phrase fade in
  tl.to(phraseEl, { opacity: 1, duration: 0.15 }, phrase.start);

  // Words stagger animation
  words.forEach((wordEl, wIdx) => {
    const wordDur = phraseDur / words.length;
    const wordStart = phrase.start + (wIdx * wordDur);

    // Pop in (slide + scale + bounce)
    tl.to(wordEl, {
      opacity: 1, y: 0, scale: 1,
      duration: 0.15, ease: "back.out(2)"
    }, wordStart);

    // Mark active (highlight vàng)
    tl.call(() => {
      words.forEach(w => w.classList.add('spoken'));
      wordEl.classList.add('active');
    }, [], wordStart + 0.001);
  });

  // Phrase fade out
  tl.to(phraseEl, { opacity: 0, y: -20, duration: 0.2 }, phrase.end);
});
```

### 8. Render
```bash
npx hyperframes render --quality draft --output /path/output.mp4
```

## Validation Checklist (BẮT BUỘC)

Sau render, **phải verify bằng vision_analyze** trên 2-3 frames:

```python
# Extract frames
subprocess.run(["ffmpeg", "-y", "-ss", "5", "-i", output, "-frames:v", "1", "/tmp/check.jpg"])

# Vision check
vision_analyze(image, "Text Tiếng Việt có space giữa các từ không? Hiển thị 'cái công đoạn' hay 'cáicôngđoạn' (dính liền)?")
```

**Nếu fail (text dính liền / mất chữ):**
- Check word-space span có width 0.6em chưa
- Check innerHTML dùng `&nbsp;&nbsp;` chưa  
- Check fonts không phải Google Fonts
- Check phrases count ≤ 27

## Common Issues & Fixes

| Issue | Fix |
|---|---|
| Only 1 phrase loaded (console `phrases: 1`) | Merge phrases thành ≤27 |
| `TypeError: Cannot read properties of undefined (reading 'split')` | Thêm safe check: `const textStr = (phrase && phrase.text) ? String(phrase.text) : ''` |
| `net::ERR_BLOCKED_BY_ORB` cho Google Fonts | Dùng system font fallback |
| Sub-composition không render | Dùng `data-composition-src`, KHÔNG inline DOM |
| Watermark mất chữ Vietnamese | Thêm space + font fallback |
| Video HTML5 không load từ `file://` | Copy file vào `assets/` folder |

## Render Time
- Clip 110s → ~3.5 phút draft
- 3300 frames = 30 FPS × 110s
- Production (`--quality high`) ~10-12 phút

## Tools

| Tool | Use |
|---|---|
| `@tiktok-product-script` | Research products for script |
| `tiktok-video-editor` | Edit clip raw thành Final |
| `hyperframes` (skill này) | Motion text overlay theo voice |

## Related Files

- `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_Final_motion_text.mp4` — Demo output (clip ngàm thao tác nhanh với motion text)
- `/Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/hf_demo/` — Project workspace template
- `/Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/hf_demo/compositions/tiktok-motion-text.html` — Working composition file

## Lessons Learned (L22 2026-07-16)

1. **User correction #1:** "motion text ≠ subtitle" — distinguish rõ ràng trong mind ngay từ đầu
2. **HyperFrames limit DOM elements:** 80 phrases → silent crash → merge to 27
3. **CSS space collapse:** `inline-block` + space character → dùng `&nbsp;&nbsp;`
4. **Google Fonts blocked:** Headless Chrome blocks `fonts.googleapis.com` qua ORB
5. **Sub-composition pattern:** `data-composition-src` là cách DUY NHẤT để render dynamic DOM
6. **Font Vietnamese rendering:** Test frame bằng vision_analyze sớm, đừng tin console log
