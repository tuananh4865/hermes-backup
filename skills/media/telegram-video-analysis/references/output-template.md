# Output Template for Telegram Video Analysis

Use this structure when sending analysis back to Tuấn Anh via Telegram. Adapted from the 2026-06-16 case study.

## Message Structure (Standard Analysis)

```markdown
Anh ơi, em tải được video rồi! [One-line description of what the video is].

**📹 Video gốc (đã convert HEVC→H.264, X.XMB):**
MEDIA:/tmp/frame-analysis/compressed.mp4

**🎬 Summary N frames + audio:**
MEDIA:/tmp/frame-analysis/summary.mp4

---

## 🔍 PHÂN TÍCH CHI TIẾT

### [Section 1: What is this video?]
[2-3 sentences describing the type, source, creator]

### [Section 2: Format & Style]
| Element | Chi tiết |
|---------|----------|
| Format | [Mirror selfie / talking head / screen recording / etc.] |
| Thời lượng | [Xs] |
| Ánh sáng | [Natural / studio / etc.] |
| Âm thanh | [Voice / music / silent] |
| Caption | "[actual caption text]" |

### [Section 3: Engagement (if social media)]
| Metric | Value | Đánh giá |
|--------|-------|----------|
| ❤️ Like | X | [Bình thường/Cao/Thấp] |
| 💾 Save | X | [Tỷ lệ save/like = X% — flag if >30%] |
| 🔄 Share | X | [Ổn/Cao] |
| 🛒 Shop tag | ✅/❌ | [Conversion path rõ/không] |

### [Section 4: Tại sao đáng chú ý?]
**Điểm mạnh:**
- [Bullet 1]
- [Bullet 2]

**Điểm yếu:**
- [Bullet 1] (if any)

### [Section 5: Replicable Pattern] (optional)
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

**Full analysis file:** `/tmp/frame-analysis/analysis.md`
**N frames extracted:** `/tmp/frame-analysis/frame_001.jpg` → `frame_NNN.jpg
```

## Message Structure (Motion Analysis + AI Prompt)

When user asks "phân tích chuyển động" or "tạo prompt video tương tự", use this structure:

```markdown
Được chứ anh! 🎬 Em đã phân tích xong motion + góc máy từng frame, kèm prompt video AI sẵn.

**📊 MOTION TIMELINE (0-Xs)**

[Pose sequence table with Pose A, B, C, D, E states]

**Pose A** (0-Ys) — [Name]: [description]. Motion: [score/pattern]
**Pose B** (Y-Zs) — [Name] ⭐ [SIGNATURE?]: [description]. Motion: [peak]
[etc.]

**📷 CAMERA**
| Aspect | Value |
|--------|-------|
| Type | [Mirror selfie / etc.] |
| Angle | [Eye-level / etc.] |
| Distance | [Xm] |
| Zoom | [Static / push-in X% / etc.] |
| Movement | [No pan/tilt / etc.] |

**💡 LIGHTING**
- [Nguồn]: [description]
- [Hướng]: [description]
- [Tông]: [color temp]
- [Palette]: [colors]

**🎯 PROMPT CHO VEO 3 / KLING / RUNWAY**

```
[Full detailed prompt with pose sequence + camera + lighting + format]
```

**📋 CHECKLIST REPLICATE**
- [Background]
- [Lighting]
- [Camera]
- [Pose sequence]
- [Tempo]
- [Motion intensity]
- [Zoom]
- [Duration]
- [Audio]
- [Caption + Shop tag]

**Full analysis:** `/tmp/frame-analysis/motion-analysis.md
```

## Customization by video type

### TikTok/Social Media
- Always include engagement table
- Always note save ratio (most important metric for algorithm)
- Always check for Shop tag
- Caption transcription is critical

### Screen recording (tutorial/demo)
- Skip engagement table
- Focus on UI flow, steps shown
- Note any text/code visible
- Audio is critical (voice-over explains the screen action)

### Talking head / Vlog
- Frame analysis less important (face doesn't change much)
- Audio is the primary content — full transcript matters
- Note background, lighting, outfit

### Product review / Unboxing
- Note product details visible in frames
- Track reveal sequence (what's shown when)
- Final verdict / rating if present
- Pricing info if visible

### Motion analysis request (replicate video)
- Switch to Motion Analysis structure above
- Include 5 pose sequence map with timestamps
- Include camera + lighting analysis
- Include 3 AI video prompt templates
- Include replicate checklist
- Always combine frame analysis with ffmpeg scene_score (vision models can't see motion)

## Tone
- Vietnamese casual
- Short, dense bullets (not paragraphs)
- Use tables for structured data
- "Em" for self-reference (not "tôi")
- Always include actionable insights, not just description
