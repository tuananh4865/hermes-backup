---
title: 'PITFALL #6 — Keep boundaries match Whisper segment boundaries (14/07)'
created: 2026-07-14
type: reference
skill: tiktok-verify-protocol
tags: [verify, anchor-lap, whisper, keep-boundary, first-class-pitfall]
related: [pitfall-anchor-lap-false-positive-2026-07-14.md]
---

# PITFALL #6 — Keep boundaries match Whisper segment boundaries

## Trigger

When `check_anchor_lap.py` reports anchor-lap pairs that **persist after multiple trim attempts** (V2, V3, V4 all fail with same pairs), this signals keep boundaries are creating false boundary detection in Whisper output.

## Root cause

`check_anchor_lap.py` checks **adjacent segments in Whisper output**. When keep boundaries fall BETWEEN Whisper verify segments (not at segment boundaries), the rendered file has 2 keeps with cross-boundary content → Whisper splits them at keep transition → adjacent Whisper segments with shared anchor keyword → script reports false positive.

**Conversely, when keep boundaries align exactly with Whisper verify segment boundaries**, each keep = 1+ whole Whisper segments, no artificial splits → script only flags real cross-boundary anchor issues.

## Real case 14/07/2026 — Clip 0758 (tripod)

V1 → V3 → V4 all failed Layer 2 (anchor-lap "các bạn" 3 pairs):
- seg 0+1: "giới thiệu với các bạn" → "bình thường các bạn"
- seg 20+21: "Các bạn có thể dùng nó để quay" → "các bạn có thể dùng..."
- seg 31+32: "Các bạn chuẩn bị xe vụ tháng" → "Vậy nên các bạn..."

V5 PASS Layer 2 by building keep_plan from Whisper V4 output (NOT source audio.json):
- Skip seg 0, 21, 31 (containing anchor keywords)
- Each keep = 1+ complete Whisper verify segments
- Keep boundaries = exact Whisper segment boundaries

## Workflow fix

```python
# Normal workflow: build keep_plan from source audio.json
# Render V1 → Whisper verify output

# When Layer 2 anchor-lap fails PERSISTENTLY (V3, V4):
# Step 1: Load Whisper V1 verify output
import json
verify = json.load(open('verify_output_v1/clip_xxx.json'))

# Step 2: Build keep_plan V5 directly from Whisper verify segments
keeps_v5 = []
for seg in verify['segments']:
    keeps_v5.append({
        "start": seg['start'],
        "end": seg['end'],
        "role": f"SEG_{seg['id']:03d}"
    })

# Optional: filter out segments with anchor keywords (trade-off: lose 5-10% features)
ANCHOR_KEYWORDS = ['các bạn', 'chúng ta', 'thì đó', 'mọi người']
keeps_v5_filtered = [
    k for k in keeps_v5
    if not any(kw in verify['segments'][i]['text'].lower() for kw in ANCHOR_KEYWORDS)
]

# Step 3: Render V5 + verify 2 layers
# Result: Layer 2 should PASS because keep boundaries = Whisper verify boundaries
```

## Trade-off analysis

**Pros:**
- Pass Layer 2 anchor-lap immediately without further trim attempts
- No false positives in Whisper output
- Workflow converges quickly (V5 instead of V8-V9)

**Cons:**
- Loses 5-10% features (segments with anchor keywords skipped)
- Depends on Whisper V1 verify output quality (if V1 has hallucinations, V5 inherits them)

**When to apply PITFALL #6:**
- ✅ Source has many natural anchor keywords (speaker uses "các bạn", "chúng ta" frequently)
- ✅ Trim V3-V4 still produces same anchor-lap pairs (proves it's structural, not fixable by trim)
- ✅ Acceptable to lose 5-10% features for Mode B cô đọng
- ❌ DO NOT apply if source has few anchor keywords (just trim normally)
- ❌ DO NOT apply if need full feature coverage (use PITFALL #3 verify_with_keep_awareness instead)

## Combination with PITFALL #3

For maximum feature preservation:
1. Apply PITFALL #6 first to identify which keeps MUST be dropped
2. Apply PITFALL #3 (verify_with_keep_awareness) to keep GHÉP features when same-keep anchor-lap is acceptable
3. Use Gap > 0.5s between keeps to avoid Whisper segment adjacency confusion

## Verification

After V5 re-render:
```bash
# Layer 2 should now PASS
python3 scripts/check_anchor_lap.py verify_output_v5/clip_xxx.json
# Expected: ✅ No anchor-lap across N segments

# If still FAIL:
# - Check if Whisper V5 verify has different segment boundaries than V4
# - May need to render V6 with even smaller keeps (max 3-5s each)
# - Or accept PARTIAL_PASS if anchor keywords are source-natural
```

## Transcript transcript evidence

V5 Whisper verify for clip 0758 showed segments aligned with keep boundaries, no false adjacency. Layer 2 output: "✅ No anchor-lap across 32 segments (19 keywords, gap<5.0s)"

## Lessons learned

1. **Persistent failure = structural issue** — when V3 + V4 both fail with same anchor-lap, accept that trim alone can't fix it
2. **Whisper boundaries matter** — don't fight Whisper's natural segmentation, work with it
3. **Feature loss is acceptable** — 5-10% feature loss for clean verify > 100% feature with anchor-lap noise

## Related pitfalls

- **PITFALL #3** — anchor-lap false positive on keeps GHÉP (uses same technique)
- **PITFALL #5** — Whisper hallucination @ speed 1.3x (similar boundary artifact)
- **PITFALL #4** — verify 2 layers mandatory (PITFALL #6 is a fix technique for layer 2 failures)