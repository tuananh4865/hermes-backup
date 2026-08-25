# PITFALL #82 — `BASH_SOURCE` skill path resolution (v0.01)

## Vấn đề
Khi viết shell scripts có hard-code path:
```bash
python3 /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/smart_keep_plan.py ...
```
Script chỉ chạy đúng khi ở Hermes dev path. Khi apply skill vào `~/.hermes/skills/media/tiktok-video-editor/`, hard-code path SAI → fail.

## Fix (v0.01)
Dùng `BASH_SOURCE` để detect script location tự động:
```bash
#!/bin/bash
# Detect skill directory (works from Hermes or ~/.hermes)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CLIP_ID="${1:-}"
# ...

# Use SCRIPT_DIR để reference siblings
python3 "$SCRIPT_DIR/smart_keep_plan.py" \
    "$WHISPER" "$ORIG" --output "$OUTPUT"
```

## Apply vào scripts

Đã apply cho 2 scripts:
- `scripts/smart_pad.sh` — gọi `smart_keep_plan.py`
- `scripts/build_pre_speed.sh` — gọi `build_concat_list.py`

Template pattern:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/<helper>.py" <args>
```

## Test
```bash
# Test 1: from Hermes source (active development)
bash /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/smart_pad.sh 0036
# → expects: SCRIPT_DIR = /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/

# Test 2: from ~/.hermes (applied skill)
bash ~/.hermes/skills/media/tiktok-video-editor/scripts/smart_pad.sh 0036
# → expects: SCRIPT_DIR = ~/.hermes/skills/media/tiktok-video-editor/scripts/
```

Cả 2 paths work với cùng code (verified 22/07).

## Bài học
Khi viết shell scripts cho skill, LUÔN dùng `BASH_SOURCE` để detect script path → make skill **location-independent**. Khi user move/symlink skill tới nơi khác, scripts vẫn chạy.

Anti-pattern:
```bash
# ❌ Sai - hard-code absolute path
python3 /Volumes/Storage-1/Hermes/skills/<skill>/scripts/<helper>.py

# ❌ Sai - relative path (chỉ work khi cd to skill folder)
python3 scripts/<helper>.py

# ✅ Đúng - BASH_SOURCE detect
SCRIPT_DIR="$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)"
python3 "$SCRIPT_DIR/<helper>.py"
```
