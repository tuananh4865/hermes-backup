# Session 2026-07-12: Independent Adversarial Verification → FAIL + Phase 4.7 added

**Date:** 2026-07-12
**Source clip:** `/tmp/badminton-highlight/indonesia-open-final/source.mp4` (58:05, BWF TV POLYTRON Indonesia Open 2026 Final, EN BLV)
**Output under verification:** `/tmp/badminton-highlight/indonesia-open-final/highlight_V1.mp4` (alleged 6-rally badminton highlight reel, 93s)
**Verifier role:** Independent adversarial checker (4 strict dimensions)
**Verdict:** **FAIL** (1 of 4 dimensions passes cleanly; 3 have serious defects)

---

## What the source agent claimed

- 6232-line EN Whisper transcript, 0 hallucination (false — see below)
- 6 rallies selected by RMS-based detection
- Output: 1280x720 H.264 30fps + AAC 44.1kHz
- Total 93s

## What the independent verifier actually found

### Dimension 1 — File integrity: ✅ PASS
- 28,110,331 bytes, decodes cleanly via `ffmpeg -f null` (exit 0)
- H.264 1280x720 @ 30fps, 2790 frames; AAC stereo 44.1kHz, 4007 frames
- Duration 93.000s, bitrate 2,418,092 bps

### Dimension 2 — Spec compliance: ✅ PASS
- H.264/AAC, 1280x720 (16:9 horizontal, NOT vertical TikTok)
- 44.1kHz stereo
- Total duration 93s matches 6 rallies concatenated (15+14+14+24+13+13)

### Dimension 3 — Source transcript cross-check: ❌ FAIL (CRITICAL)
- Whisper transcript has **massive hallucination**:
  - 1106 of 1558 unique subtitle entries are "That's the" hallucinate (= **71%** of all subtitle lines)
  - Single continuous hallucination run spans **1317s → 3499s** (~36 minutes)
  - Real BLV commentary stops at ~1317s (21:57 of match time)
- Source agent's "6232 lines valid, 0 hallucinate" claim is **false** (line count double-counts: each SRT entry = 4 lines: index, timestamp, text, blank)
- Of the 6 rally windows, **ZERO** contain any BLV reaction keywords ("amazing", "fantastic", "brilliant", "incredible", "long rally", "what a")

### Dimension 4 — Rally coverage (visual content check): ❌ FAIL (CRITICAL)

Sampled source.mp4 frames at each rally timestamp. Actual content:

| Rally window | Source time | What the frame shows |
|---|---|---|
| Rally 1 (193-208s) | t=200s | Canadian flag with "MOM'S SMILES" sponsor banner — **player introduction ceremony** |
| Rally 3 (112-136s) | t=124s | Red pyrotechnics, podium #1/#2 visible — **player introduction ceremony** |
| Rally 4 (2881-2895s) | t≈2885s | "WONDERFUL FINISH" countdown graphic — **post-match graphic** |
| Rally 6 (2988-3001s) | t≈2995s | Award podium ceremony (Christie on #1, opponent on #2) — **award ceremony** |
| Rally 2 (3097-3111s) | t≈3107s | Players applauding/farewelling in empty arena — **post-match** |
| Rally 5 (3114-3127s) | t≈3118s | Wide crowd shot in dark arena — **post-match warmdown / B-roll** |

**NO frame in any of the 6 rally windows shows active shuttle-in-play badminton.**

### Distribution check: ❌ FAIL
- 6 rallies clustered: 2 at opening (1:52, 3:13), 4 at end of game 2 (48:01-52:07)
- **44.5 minutes of match (208s → 2881s = 76% of match) has zero rally coverage**
- No early-game-2, no mid-game-1, no game-1 climax

---

## Root cause analysis

### Scoring formula inverted priority

`detect_rallies.py` scoring formula:
```python
score = (peak - SPIKE_DB) / 10.0 * 0.4 + min(1, duration / 15.0) * 0.6
```

This is a **weighted sum** where duration_norm dominates. A 76s ceremony at -22dB scores (0.3 × 0.4) + (1.0 × 0.6) = **0.720**. A 14s genuine rally at -22dB scores (0.3 × 0.4) + (0.93 × 0.6) = **0.678**. Ceremony outranks rally. Wrong.

In BWF TV broadcasts with music bed, anthem, and PA announcements, sustained loudness is the norm — so this formula **always** prefers ceremony/music over actual play.

### Why the rejected rally 0 was the best content

The top-1 RMS spike at t=1774-1881s (115s sustained, score 0.712) was manually filtered as "ceremony" because of Phase 4.6 (>60s = ceremony). But independent visual check at t=1774s shows **actual badminton play with scoreboard showing Christie 19 / Lai 20** — a game-deciding moment. The agent discarded the BEST content because the duration-based scoring couldn't distinguish "climactic 90s of crowd cheering during a 30-shot rally" from "ceremony is happening".

### Sharp transient peak count (shuttle hit signature)

A shuttle hit = sharp RMS peak with quiet immediately before AND after (>30dB swing in <2s).

Sharp transient count by rally window:
- Rally 1 (193-208s): 0  ← ceremony, no shuttle hits
- Rally 3 (112-136s): 0  ← ceremony
- Rally 4 (2881-2895s): 0  ← finish graphic
- Rally 6 (2988-3001s): 2 ← only one with hits
- Rally 2 (3097-3111s): 0  ← post-match
- Rally 5 (3114-3127s): 0  ← post-match

**5 of 6 windows have ZERO sharp transients.** This is conclusive evidence the algorithm picked ceremony/sustained-loud, not rallies.

---

## Real rallies that were missed

Random source sampling found actual play the algorithm discarded:
- **t=1774s**: score **Christie 19 / Lai 20** (game-deciding pressure) — actual play, scored 0.712 by algorithm but filtered as ceremony by Phase 4.6
- **t=800s**: score **Christie 6 / Lai 5** (early game 1) — actual play
- **t=950s**: 11s sustained peak at -25dB — likely actual rally

The algorithm filters by duration, ignoring the actual match content.

---

## Phase 4.7 added

To prevent this from happening on the next run, the badminton-highlight-editor skill added **Phase 4.7 — MANDATORY VISUAL VERIFICATION GATE** before declaring any highlight reel done. See `SKILL.md` Phase 4.7 section for full spec.

Key sub-steps:
- **4.7.1** Extract 1 frame per rally from source.mp4 and visually verify active play (≥4 of 6 frames must show court+action)
- **4.7.2** Count sharp transient peaks per window (≥60% of windows must have ≥1 transient)
- **4.7.3** Cross-check BLV text in window if transcript is reliable
- **4.7.4** Write `highlight_<id>_ADVERSARIAL_VERDICT.md` next to output with verdict
- **4.7.5** Replace scoring formula with `peak × 0.7 + (1 / (1 + duration/5)) × 0.3` (+ transient bonus)

## Verdict on the existing Test Case 2 in SKILL.md

The Test Case 2 entry previously claimed "verified PASS" with metrics. Independent verification 12/07 proves this is incorrect. The skill now has honest result: **not shippable, needs Phase 4.7 + scoring fix**. Any future runs MUST pass Phase 4.7 before being claimed as done.

## Reproduction recipe (for future adversarial checks)

```bash
# 1. File integrity
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,codec_type,width,height,sample_rate,channels \
  -of default=noprint_wrappers=1 highlight_V1.mp4

# 2. SRT hallucinate count
SRT=audio.srt
TOTAL=$(grep -c '^[0-9]\+$' "$SRT")
HALL=$(grep -c "That's the" "$SRT")
echo "Real lines: $((TOTAL - HALL))  Hallucinate: $HALL  Ratio: $(echo "scale=2; $HALL * 100 / $TOTAL" | bc)%"

# 3. Visual content per rally
for t in 200 3100 124 2885 3118 2992; do
  ffmpeg -hide_banner -loglevel error -ss $t -i source.mp4 -frames:v 1 -y /tmp/v_$t.png
  echo "t=$t saved"
done
# Then use vision_analyze on each to ask "active play or ceremony?"

# 4. Sharp transient count
python3 -c "
import re
data = open('rms_log.txt').read()
times = [float(m.group(1)) for m in re.finditer(r'pts_time:([\d.]+)', data)]
levels = [float(m.group(1)) for m in re.finditer(r'RMS_level=(-?[\d.]+)', data)]
rallies = [(193,208), (3097,3111), (2881,2895), (112,136), (3114,3127), (2988,3001)]
for rs, re_ in rallies:
    sharps = sum(1 for i in range(len(times)-1) if rs <= times[i] <= re_
                 and levels[i] > -25 and (levels[i-1] < -30 or levels[i+1] < -30))
    print(f'  {rs}-{re_}: {sharps} sharp transients')
"
```

The verdict for any badminton highlight reel going forward should be:
- ✅ PASS only if ≥4/6 frames show active play AND ≥60% of windows have ≥1 transient
- ❌ FAIL if ≥3 frames are ceremony/post-match/sponsor OR ≥50% of windows have 0 transients
