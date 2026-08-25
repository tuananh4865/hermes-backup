# STORYBOARD.md Template for TikTok Product Motion Graphics

Write this file BEFORE authoring `index.html`. Counts visual elements. Tuấn Anh's standard: minimum 8 elements for a 30s clip.

```markdown
# Storyboard: <product-slug>-<style>-v<n>
# Source: <absolute path>
# Duration: <X>s
# Resolution: 1080×1920 (TikTok spec)
# Author: Hermes Agent
# Reference video: <URL if any>

## Time Segments (from Whisper transcript)
| Time | Transcript | Spoken word count | Visual element | Animation |
|---|---|---|---|---|
| 0.0-2.3 | "Các bạn ơi..." | 2 | HOOK big text | pop in scale |
| ... | ... | ... | ... | ... |

## Visual Element Count (PRE-FLIGHT CHECK)

Run this before writing code:

| Element | Present | Phase |
|---|---|---|
| HOOK (1) | YES | 0-2s |
| PROBLEM eyebrow (1) | YES | 2-7s |
| PROBLEM highlight big (1) | YES | 2-7s |
| PROBLEM sub (1) | YES | 2-7s |
| Bar chart container (1) | YES | 7-13s |
| Bar chart bar × 2 | YES | 7-13s |
| Bar chart value × 2 | YES | 7-13s |
| Coffee stamp emoji (1) | YES | 13-17s |
| Coffee label (1) | YES | 13-17s |
| Product brand (1) | YES | 17-19s |
| Product name (1) | YES | 17-19s |
| Product tagline (1) | YES | 17-19s |
| iPhone frame (1) | YES | 19-28s |
| iPhone label (1) | YES | 19-28s |
| iPhone sub label (1) | YES | 19-28s |
| USP bullet × 4 = 4 cards × 3 sub = 12 | YES | 28-30s |
| CTA button (1) | YES | 30-32s |
| CTA price old (1) | YES | 30-32s |
| CTA price new (1) | YES | 30-32s |

**Total elements: at minimum 25 DOM nodes (counted from real case 17/07/2026)**

If your element count is under 8 visible elements, STOP. The user standard requires more density. Re-look at the transcript, every fact/number/comparison deserves a graphic.

## Phase animation mapping

For each phase, specify:
- start time (s) — when this phase begins
- end time (s) — when this phase ends
- elements that appear (their entry animation)
- elements that exit (their exit animation)
- transitions between phases (cross-fade 0.5s? hard cut?)

## Audio sync map

For each segment in the Whisper transcript, mark:
- which visual element peaks when that segment ends
- ±300ms tolerance (loose) for pop-ins
- ±100ms tolerance (strict) for chart bars + typewriter

Example:
```
[ 8.94-9.22] "ra ngoài đường"  →  Bar chart phase starts at 7.3s, bars animate over 2.5s starting at 8.0s
                                       Audio word "ra" lands at 8.94s — bar chart at 35% of growth — sync OK
```

## Reference

See ../../concepts/sac-du-phong-infographic-v2.md for a full worked example.
