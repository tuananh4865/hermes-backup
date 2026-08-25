---
title: Voice Re-verify at Session Start
created: 2026-06-16
type: reference
applies_to: tiktok-viral-script
trigger: Session start, before writing any script
---

# Voice Re-verify Rule (CRITICAL)

**Rule:** At the START of every session where you will write or review a TikTok script, re-verify the current voice profile. **DO NOT rely on cached voice state from earlier sessions.**

## Why this rule exists

Tuấn Anh's voice has changed multiple times:

- **Original (2026-04):** "anh" + "mấy con vợ" (cố định)
- **2026-05-04:** content-director/SOUL.md locks in "anh" + "mấy con vợ"
- **2026-06-13:** voice đã đổi — bỏ "anh" + "mấy con vợ", dùng trung tính "mình"/"bạn"
- **2026-06-16:** voice cho SETUP/EDIT niche = "các bạn" (HỢP LỆ), cho GEAR REVIEW = "mọi người" hoặc trung tính

An agent that loaded `tiktok-viral-script` once on 2026-05-04 and trusted that voice profile would have written 1+ month of scripts in the WRONG voice (using "anh" + "mấy con vợ" after 13/06 when that voice was already rejected).

## How to re-verify (mandatory, 3 steps)

1. **Read the latest voice note** in `Operations/ho-so-giong-van-va-kich-ban-*.md` (or current voice profile file in the project hub)
2. **Check the frontmatter** — every Operations/* voice file should have a date in the filename showing when it was last updated
3. **Pick the voice by trụ** (not by default):
   - Trụ SETUP (ánh sáng, camera, mic) → "các bạn"
   - Trụ EDIT (CapCut, hiệu ứng) → "các bạn"
   - Trụ GEAR REVIEW → "mọi người" hoặc trung tính
   - Series "Xây kênh 0 đồng" → "các bạn"
   - Default fallback → trung tính ("mình"/"bạn"), NEVER "anh" + "mấy con vợ" unless user explicitly requests

## When voice is ambiguous → ASK

If the user has not specified voice AND the project file doesn't make it clear, use `clarify` with 3 options. Do NOT silently default to "các bạn" or "trung tính" — voice is a recurring complaint point and getting it wrong costs a full rewrite.

## Anti-pattern

❌ "I already know the voice from last session" — voice changes; cached memory is wrong by default
❌ "The skill says 'anh' + 'mấy con vợ'" — skill was last updated on a different date than the current voice profile
❌ "I'll just use the safer old voice" — the OLD voice is the one that was rejected, not the new one

## Real failure (2026-06-13)

User rejected scripts written with "anh" + "mấy con vợ" voice. The skill still had that voice in its own file (from 2026-05-04), so the agent kept recommending it. The fix was a skill file update to add "Voice đã đổi 13/06" — but that fix only works if the agent READS the skill fresh each session, which means re-verifying at session start, not relying on memory.

## Files to check (in order, freshest first)

1. `wiki/entities/learned-about-tuananh.md` → "Voice & Pronouns" section
2. `wiki/entities/content-creator-project.md` → "Voice & Pronouns" section
3. Project hub.md → "Content Creator" section
4. `Operations/ho-so-giong-van-va-kich-ban-*.md` (latest by date in filename)
5. THIS skill's "Voice & Pronouns" section (last updated 2026-06-16)

If file 1 and file 5 disagree, file 1 wins (user memory > skill cached content).
