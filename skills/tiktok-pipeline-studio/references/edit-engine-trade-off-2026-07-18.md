# Edit Engine Trade-off — `video-use` vs `tiktok-video-editor`

> **TL;DR:** Default dùng `tiktok-video-editor` v3.29.0 cho mọi clip Tuấn Anh
> đang edit. Chỉ switch sang `video-use` khi anh explicit yêu cầu AI tự edit.

## Decision Matrix

| Dimension | `tiktok-video-editor` v3.29.0 (manual) | `video-use` (AI auto-edit) |
|---|---|---|
| **Customize 7 KEY INSIGHTS** | ✅ Manual rõ ràng từng keep | ❌ AI tự quyết dựa trên LLM reasoning |
| **26 Pitfall coverage** | ✅ Systematic apply (HOOK_LAP, SOURCE-LOOP, FALSE_START, etc.) | ❌ AI có thể miss Vietnamese filler patterns |
| **SPEED 1.3x MANDATORY** | ✅ Step bắt buộc cuối workflow (Pitfall #26) | ❌ Không enforce |
| **MODE B 95-120s sweet spot** | ✅ Verify gate tự động | ⚠ AI có thể ship 60s hoặc 200s tùy ý |
| **Vietnamese dialect accuracy** | ✅ medium-mlx verified ANH NỚI rõ ràng (loop detection) | ⚠ ElevenLabs trained multi-lang, có thể miss |
| **Cost** | Free (Whisper medium-mlx local) | $0.10-0.30/clip (ElevenLabs API) |
| **Time per clip** | 5-15 phút (manual review 5 nhóm lỗi) | 1-3 phút (AI tự làm) |
| **Self-eval tại cut boundary** | ✅ verify_clip.py + check_anchor_lap.py | ✅ Built-in (3 retries max) |
| **Idempotent re-runs** | ✅ Keep plan saved, rerun exact | ⚠ LLM decision non-deterministic |
| **Skill maturity in Hermes** | ✅ v3.29.0, 218 files, mature (Pitfall #20-#26) | ❌ CHƯA install (cần git clone + uv sync) |

## Khi Nào Dùng Cái Nào

### Use `tiktok-video-editor` (default) khi:
- Anh muốn giữ voice + style của kênh TikTok (@hi.imdung-style)
- Có 7 KEY INSIGHTS riêng (BRIDGE, USP riêng, USP_PROOF, LẶP CỐ Ý, etc.)
- Cần SHIP đúng 95-120s Mode B sweet spot
- Cần verify 2-layer (Layer 1 verify_clip.py + Layer 2 check_anchor_lap.py)
- Cần clip quality 100% (TikTok Shop affiliate bán hàng)

### Use `video-use` (AI) khi:
- Anh explicit nói "AI tự edit cho anh" hoặc "dùng video-use"
- A/B test xem AI edit có match với manual quality không
- Clip ngắn < 60s, không cần customize nhiều
- Anh muốn bulk edit N clips trong 1 session
- Cần ELEVENLABS_API_KEY đã setup

### Use BOTH (hybrid) khi:
- video-use làm V0 draft nhanh
- tiktok-video-editor polish V0 thành V1 (apply 7 KEY INSIGHTS + SPEED 1.3x)

## Setup `video-use` (1 lần)

```bash
# 1. Clone + symlink
git clone https://github.com/browser-use/video-use ~/Developer/video-use
ln -sfn ~/Developer/video-use ~/.claude/skills/video-use
cd ~/Developer/video-use
uv sync
brew install ffmpeg  # required
brew install yt-dlp  # optional

# 2. ELEVENLABS_API_KEY
cp .env.example .env
$EDITOR .env
# Paste: ELEVENLABS_API_KEY=sk-xxxxxxxxxxxx
# Grab key tại: https://elevenlabs.io/app/settings/api-keys

# 3. Daily workflow
cd /path/to/raw/videos/
# Paste vào Hermes:
# "Set up https://github.com/browser-use/video-use for me. Read install.md first
# to install this repo, wire up ffmpeg, register the skill with whichever agent
# you're running under, and set up the ElevenLabs API key. Then read SKILL.md for
# daily usage, and always read helpers/ because that's where the editing scripts
# live. After install, don't transcribe anything on your own — just tell me it's
# ready and wait for me to drop footage into a folder."
```

## Pipeline `video-use` (post-setup)

```bash
# 1. Drop raw clips vào folder
cp raw_*.mp4 /Volumes/Storage-1/Pocket3/raw/

# 2. Chat với agent
# > "edit these into a launch video"

# 3. Agent tự động:
#    - Inventory sources (ffprobe)
#    - Propose strategy (LLM reasoning)
#    - Wait for anh's OK
#    - Edit → render → self-eval (max 3 retries)
#    - Produce edit/final.mp4
```

## Pipeline `tiktok-video-editor` (default)

```bash
# 1. Transcribe với Whisper medium-mlx
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --word-timestamps True --output-dir ./whisper_out raw.mp4

# 2. Manual review (5 nhóm lỗi narrative)
# - HOOK lặp 3+ từ
# - SOURCE-LOOP
# - TREO >5s
# - ỰM Ỡ
# - FILLER dài nối

# 3. Apply 7 KEY INSIGHTS self-check per keep
# - BRIDGE 0.5-3s
# - USP riêng 1 keep
# - USP_PROOF
# - LẶP CỐ Ý emphasis
# - SILENT GAP 5-10s
# - HOOK take punchy nhất
# - SỐ LIỆU CỤ THỂ

# 4. Render + SPEED 1.3x
ffmpeg -y -i source.mp4 -filter_complex \
  "[0:v]setpts=PTS/1.3[v];[0:a]atempo=1.3[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 128k output_troncau_speed13.mp4

# 5. Verify 2 layers
python3 ~/.hermes/skills/media/tiktok-verify-protocol/scripts/check_anchor_lap.py
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/verify_clip.py
```

## Cost-Benefit Reality Check

**Tính theo 100 clips:**
- tiktok-video-editor: 100 × 10 min manual = ~16 giờ + 0đ cost
- video-use: 100 × 2 min AI = ~3.3 giờ + ~$20 cost

**Quality comparison (estimated, chưa thật test):**
- tiktok-video-editor: 100% pass verify gate, 95-120s Mode B sweet spot, 100% features covered
- video-use: 60-80% pass verify gate (tùy LLM reasoning), 60-180s duration range, 70-90% features covered

## Recommendation For Anh

**Phase 1 (this month):** Use `tiktok-video-editor` exclusive. Đã mature 18 ngày, đã verified bằng evidence gate mỗi ngày.

**Phase 2 (next month):** Test `video-use` trên 5 clips test → so sánh quality → decide có hybrid không.

**Phase 3 (optional):** Nếu video-use quality đủ tốt → bulk edit N clips trước (speed), polish bằng tiktok-video-editor sau (quality).

## See Also

- `~/.hermes/skills/media/tiktok-video-editor/SKILL.md` v3.29.0 (Stage 2-3)
- `wiki/projects/content-creator/references/7-key-insights-summary.md` (nếu có)
- `https://github.com/browser-use/video-use` (upstream README)
- `~/.hermes/scripts/adversarial_verify.py` (để verify output từ cả 2 edit engine)