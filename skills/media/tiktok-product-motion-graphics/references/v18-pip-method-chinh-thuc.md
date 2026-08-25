# V18 PIP Method → See canonical reference

**This file is superseded by the consolidated canonical reference.**

👉 **Read the canonical PIP method here:** `references/v13-pip-position-method.md`

It contains the V18/V13 pattern as a single source-of-truth, including:
- 1 video element + GSAP keyframe scale/position (NO wrapper, NO clipPath)
- Math: `scale: 0.42, x: ±222, y: -540` verified by pixel bbox
- Anti-patterns (V14/V15/V16/V17) marked FAILED
- Visual verification protocol (vision_analyze PNG, NOT std pixel)
- Ship-verify-or-lie rule (mandatory `ls -la` after ffmpeg)
- GSAP `tl.fromTo()` requires CSS `opacity:0` (V90 fix)
- Workspace convention (Storage-1, not /tmp)
- Timing rules (PIP at 30% / 60% / last 10% of duration)

**Why this file was kept:** Historical reference for the 19/07 conversation that produced V18. The actual production-ready pattern is now in `v13-pip-position-method.md`.
