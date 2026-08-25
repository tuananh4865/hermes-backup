# STT Vietnamese Config — 28/07/2026 incident

## Triệu chứng

User gửi voice Telegram tiếng Việt (giọng nam miền Nam, code-switch Việt-Anh) → Hermes transcript SAI thành thuần tiếng Anh. Ví dụ thật 28/07:

Audio gốc (giọng user, ~24s): "Anh nhận thấy là những cái video mà em edit. Em chưa sắp xếp được nội dung. Vậy nên là em có thể thử lại với một cái clip nào đó khác được không."

Transcript SAI (BEFORE fix): "I think this video is for you, Edith. I haven't been able to use it for a long time. I think it's better to use it for a long time. So I can try it with a different clip."

Transcript ĐÚNG (AFTER fix): "Anh nhận thấy là những cái video mà em edit. Em chưa sắp xếp được nội dung. Thành theo kiểu hay giống như anh tưởng tượng. Vậy nên là em có thể thử lại với một cái clip nào đó khác được không."

## Root cause

`~/.hermes/config.yaml` STT config có `language: ''` (empty string) → code path trong `hermes-agent-self-learning/tools/transcription_tools.py`:

```python
language = (
    _load_stt_config().get("local", {}).get("language")  # returns ""
    or os.getenv(LOCAL_STT_LANGUAGE_ENV)                # not set
    or DEFAULT_LOCAL_STT_LANGUAGE                     # = "en" (default)
)
```

Empty string is falsy → fallback về `"en"` → `whisper` CLI invoked with `--language en` → Vietnamese audio hallucinated as English (Whisper không biết phải transcribe ngôn ngữ nào khi không có hint).

## Fix command (28/07/2026)

```bash
# CRITICAL: dùng 'hermes config' CLI, KHÔNG patch ~/.hermes/config.yaml trực tiếp
# (Hermes từ chối write trực tiếp vì security-sensitive)
hermes config set stt.local.language vi
hermes config set stt.local.model medium
```

Backup config cũ tự động: `~/.hermes/config.yaml.bak-YYYY-MM-DD-stt-vi`.

## Verify protocol (BẮT BUỘC sau khi config change)

### 1. Test whisper CLI thật với voice Telegram cached

```bash
# Lấy 1 voice gần đây (audio_*.ogg là từ gateway cache)
AUDIO=$(ls -t ~/.hermes/audio_cache/audio_*.ogg 2>/dev/null | head -1)
[ -z "$AUDIO" ] && { echo "❌ No voice cached"; exit 1; }

/Users/tuananh4865/Library/Python/3.9/bin/whisper "$AUDIO" \
  --model medium --language vi \
  --output_format txt --output_dir /tmp/stt_verify 2>&1 | tail -5
cat /tmp/stt_verify/*.txt
```

PASS criteria: transcript thuần tiếng Việt, có cấu trúc câu + dấu câu Việt, không có cụm từ tiếng Anh nào trừ khi user thật sự nói tiếng Anh.

### 2. Test code path load config

```bash
/opt/homebrew/bin/python3.11 -c "
import sys
sys.path.insert(0, '/Users/tuananh4865/hermes-agent-self-learning')
from tools.transcription_tools import _load_stt_config, _get_local_command_template
import json
print(json.dumps(_load_stt_config(), indent=2))
print(_get_local_command_template())
"
```

Expected output:
```
{
  "local": {
    "model": "medium",
    "language": "vi"
  }
}
/Users/tuananh4865/Library/Python/3.9/bin/whisper {input_path} --model {model} --output_format txt --output_dir {output_dir} --language {language}
```

### 3. Restart gateway nếu STT đang active

```bash
ps aux | grep -E "gateway|hermes" | grep -v grep
# Nếu gateway đang chạy với config cũ:
# ~/.hermes/hermes-agent/venv/bin/python3 -m hermes_cli.main gateway restart
```

## Model selection matrix

| Model | Size | Latency (24s audio, M-series CPU) | Vietnamese accuracy | Mix Việt-Anh |
|-------|------|------------------------------------|-------------------|--------------|
| `tiny` | 75MB | 5s | ❌ thấp | ❌ |
| `base` | 150MB | 8s | ⚠️ code-switch kém | ⚠️ |
| `small` | 500MB | 12s | ✅ tốt cho giọng thường | ✅ |
| `medium` | 1.5GB | 20s | ✅ tốt, hầu hết content creator | ✅ **DEFAULT choice** |
| `large-v3` | 3GB | 35s | ✅✅ best, catch technical terms | ✅✅ |

**Recommendation 28/07**:
- Default `medium` — balance speed/accuracy
- Upgrade `large-v3` khi user review TikTok clip có technical terms (CNC, focus, Pocket 3 — đã verify ở Pocket 3 task trước)
- KHÔNG dùng `base` cho Vietnamese — miss technical terms + hallucinate khi audio mờ

## Multi-language audio (Việt + Anh lẫn)

`--language vi` chỉ HINT Whisper ngôn ngữ chính. Whisper vẫn transcribe segment tiếng Anh ra tiếng Anh khi gặp. Verified 28/07:

User nói: "Anh muốn dùng Clip này cho video TikTok" → Whisper large-v3 output đúng cả "Clip" và "TikTok" (không transcribe thành "Klep" hay "Tích Tóc").

Để boost accuracy cho code-switch nặng, thêm `--initial-prompt` với câu Việt-Anh mix. WHISPER CLI support. Code chưa expose config này — patch sau nếu user yêu cầu.

## Related incident timeline

| Date | Whisper behavior | Fix |
|------|------------------|-----|
| 21/07 | Pocket 3 audio hallucinate "đặc thùng", "phó kết" thay vì "đặc biệt", "focus" | Switch large-v3 model |
| 22/07 | Whisper large-v3 verified chuẩn cho TikTok clip ("transcript chuẩn nhất") | Bake vào whisper-transcribe wrapper |
| 26/07 | Concat demuxer stream-copy gây frame overlap | filter_complex với hard cut |
| 28/07 | Voice Telegram Whisper hallucinate toàn tiếng Anh | `hermes config set stt.local.language vi` |

## Anti-patterns

❌ **Patch `~/.hermes/config.yaml` trực tiếp** — Hermes security rejects write, error: "Refusing to write to Hermes config file".
❌ **Để `language: ''` trong config** — silent fall về "en", hallucinate toàn bộ Vietnamese.
❌ **Dùng whisper model `base`** — miss technical terms Vietnamese + code-switch Việt-Anh.
❌ **Quên restart gateway sau config change** — gateway cache config, change không take effect.
❌ **Patch whisper config làm global** (env var `HERMES_LOCAL_STT_LANGUAGE`) — không survive session restart của một số platform.
✅ **Dùng `hermes config set` CLI** — atomic, audit trail, auto-backup.
✅ **Verify bằng whisper CLI thật sau mỗi config change** — transcript phải khớp audio gốc.

## Key files

- Config: `~/.hermes/config.yaml` → `stt.local.{model, language}`
- Code: `hermes-agent-self-learning/tools/transcription_tools.py` → `_load_stt_config()`, `_get_local_command_template()`, `_transcribe_local_command()`
- Gateway: `hermes-agent-self-learning/gateway/run.py` → `_enrich_message_with_transcription()` (gọi `transcribe_audio` cho mỗi voice message)
- Telegram adapter: `hermes-agent-self-learning/gateway/platforms/telegram.py` → cache .ogg từ `msg.voice` rồi pass cho STT
