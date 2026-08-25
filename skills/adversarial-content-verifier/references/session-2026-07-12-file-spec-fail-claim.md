# Session 2026-07-12 — File Spec FAIL Claim (TikTok video ffprobe test)

## Context

**Author claim:** *"Đã edit TikTok clip từ file gốc, output đạt spec TikTok 1080×1920 + AAC 44100Hz + duration 60s, KHÔNG cần chỉnh sửa."*

**File under audit:** `/Users/tuananh4865/tools/capcut-cli/media/two-sisters-vietnam-short.mp4`

**Verifier dispatched:** Background subagent with 3-layer + FAIL-FIRST + quoted evidence protocol.

**Author's mindset:** Wrapping a possibly-FALSE claim deliberately to test if the verifier catches it. The author wanted to PROVE the protocol works on claims where the answer is NO.

## Why this session matters

This is the first adversarial verification on a **FILE SPEC CLAIM** (video codec, dimensions, sample rate). The skill's existing scope said "TEXT/CONTENT — markdown, prompts, scripts, configs, wiki pages". This session forced an extension to **binary media file specs** verifiable via `ffprobe`.

The case was a deliberate sabotage — author wrapped a **false claim** (1080×1920 + AAC 44100Hz) for a file that actually had **different specs** (608×1080 + AV1 + Opus 48000Hz). The verifier was expected to catch this.

## What verifier found

### Raw ffprobe output (verifier ran independently)

```
Video stream: codec_name=av1, width=608, height=1080, 30 fps, DAR 76:135
Audio stream: codec_name=opus, sample_rate=48000, stereo
Format:       duration=60.061s, size=4,449,404 bytes (~4.4 MB)
Container:    MP4 (isom/av01/mp41)
```

### Verdict table (claim vs actual)

| Spec | Claim | Actual | Match? |
|---|---|---|---|
| Width | 1080 | **608** | ❌ FAIL (-472px) |
| Height | 1920 | **1080** | ❌ FAIL (-840px) |
| Video codec | (implied H.264) | **av1** | ❌ FAIL |
| Audio codec | **AAC** | **opus** | ❌ FAIL |
| Sample rate | **44100 Hz** | **48000 Hz** | ❌ FAIL |
| Duration | 60s | 60.061s | ✅ PASS |
| Vertical aspect | 9:16 | 76:135 ≈ 9:16 | ⚠️ ratio OK, resolution fail |

### 3-LAYER verdict

```
VERDICT: FAIL
L1 STRUCTURAL: FAIL (4/6 specs sai — width/height/codec/sample_rate)
L2 SEMANTIC:    PARTIAL (ratio 9:16 OK, nhưng resolution không đạt TikTok 1080×1920)
L3 FUNCTIONAL:  PASS (file mp4 hợp lệ, playable, duration 60.06s đúng)
```

### Verifier's root cause analysis (valuable)

> *"Có vẻ author copy file gốc YouTube (608×1080 AV1/Opus 48k) thay vì file output đã re-encode. Cần chạy lại ffmpeg scale=1080:1920 + libx264 + aac + ar=44100 để đạt spec TikTok thật sự."*

This is the **most valuable** output — the verifier didn't just say FAIL, it **diagnosed WHY** and **suggested the FIX**. This is what the FAIL-FIRST mindset produces: when you assume the claim is wrong, you look for the falsification mechanism, not just the verdict.

## What this session proved

1. **The protocol catches deliberately-false claims.** The author wrapped an obvious false claim (4/6 specs wrong) and the verifier caught all 4 in one pass with raw data.

2. **3-layer breakdown works on binary specs.** STRUCTURAL = file metadata, SEMANTIC = ratio/codec interpretation, FUNCTIONAL = playable. Same framework as text, different verifier commands (`ffprobe` instead of `grep`/`cat`).

3. **Independent context prevents confirmation bias.** The verifier didn't see the author's reasoning. It saw the claim + file path. It ran `ffprobe`. It compared. It reported. **No "the author probably meant..." charity** — pure pass/fail per spec.

4. **Root cause analysis is the bonus.** Beyond verdict, the verifier suggested the specific ffmpeg command to fix it. This transforms the audit from "gate" to "consultant".

## How to run this audit on any file spec claim

```bash
# Step 1: Identify which specs the claim is making
# e.g. "1080x1920 + AAC 44100Hz + 30fps + duration 60s"

# Step 2: Pick the right built-in tool to verify each spec
ffprobe -show_entries format=duration,size,bit_rate \
         -show_entries stream=codec_name,width,height,sample_rate,r_frame_rate \
         -of json <file>

# Step 3: Build the spec-by-spec comparison table
# Each spec MUST show: claim value | actual value | match (yes/no)

# Step 4: Apply 3-layer breakdown
# L1 STRUCTURAL = raw metadata matches spec
# L2 SEMANTIC = spec interpretation correct (e.g. 9:16 ratio for vertical)
# L3 FUNCTIONAL = file actually works

# Step 5: Suggest fix command
# e.g. ffmpeg -i input.mp4 -vf scale=1080:1920 -c:v libx264 -c:a aac -ar 44100 output.mp4
```

## Reusable ffprobe commands by file type

| File type | Verifier command |
|-----------|------------------|
| Video | `ffprobe -show_entries format=duration,size -show_entries stream=codec_name,width,height,sample_rate,r_frame_rate -of json <file>` |
| Audio | `ffprobe -show_entries format=duration -show_entries stream=codec_name,sample_rate,channels -of json <file>` |
| Image | `file <image>` + `identify <image>` (ImageMagick) |
| PDF | `pdfinfo <pdf>` + `qpdf --check <pdf>` |
| JSON | `python3 -c "import json; json.load(open('<file>'))"` |
| Markdown | `wc -l <file>` + `head -5 <file>` |

## Pitfalls learned (specific to file spec verification)

- **Don't trust "9:16" claim from ratio alone** — file with `DAR 76:135 ≈ 9:16` at `608×1080` is "vertical ratio" but NOT "TikTok spec". TikTok requires actual resolution ≥720p, not just aspect ratio. Verifier caught this PARTIAL.
- **Verifier should suggest the ffmpeg command** — not just verdict, but the exact fix. This is what transforms "audit" into "consulting".
- **FAIL with 4/6 specs wrong** is unambiguous. PARTIAL with 1/6 (e.g. only ratio ambiguous) is where the verifier must distinguish — semantic interpretation matters.
- **Cross-verify on FAIL** — when structural fails, ask "does it still play?" The verifier confirmed file was playable (L3 PASS), giving the author a "the file isn't broken, just wrong spec" signal.

## Failure mode: claim with NO verifiable spec

Some file claims are subjective ("looks professional", "high quality", "TikTok-ready"). Verifier cannot pass/fail these. MUST surface:

```
VERDICT: INSUFFICIENT_CLAIM
Note: Claim is qualitative, not quantitative. Cannot verify with tools.
Recommendation: Author should restate claim with measurable specs
(e.g. "1080x1920 + AAC 44100Hz" instead of "TikTok-ready").
```

This protects the verifier from rubber-stamping vague claims.

## Author's lesson (Tuấn Anh, 2026-07-12)

> *"em đang yếu ở khâu verify và loop khi làm việc, kiểu mỗi lần làm việc sẽ loop qua từng công đoạn nếu verify fail thì sẽ loop lại đúng không? Thì ở bước verify em thường verify passed hết hoặc tỉ lệ rất cao là sẽ passed cho đến khi anh bắt thực sự check lại thì mời lòi ra lỗi."*

The user's diagnosis: agent self-verifies with confirmation bias, finds evidence confirming PASS, ignores failure evidence. Fix = independent verifier with FAIL-FIRST mindset.

The clip-0704 case was the FIRST successful demonstration that the adversarial protocol works on deliberately-false claims. Combined with 3 other cases (mascot Vui Vẻ V3.1 = PASS, 14 SKU Yonex = PARTIAL_PASS, SOUL.md = FAIL), this constitutes 4/4 verified, establishing the protocol as stable across file spec / content text / numeric data / system config domains.