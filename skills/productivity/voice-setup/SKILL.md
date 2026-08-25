---
name: voice-setup
description: Configure voice STT/TTS for Hermes Agent — Telegram voice messages, Vietnamese TTS, Edge TTS, gateway voice integration, Vietnamese STT language pitfall (28/07).
version: 1.3.0
# v1.3.0 (28/07/2026): Added Vietnamese STT Pitfall — `language: ''` empty falls back to "en" → Vietnamese audio hallucinated as English. Added reference `references/stt-vietnamese-config-2026-07-28.md`.
# v1.2.0 (21/07/2026): Added content rules (no prices, no model codes), speed default 1.4x, edge-tts --rate pitfall, rate limit retry pattern
# v1.1.0 (21/07/2026): Switched default voice to NamMinh (male), added workflow for sending voice to Telegram
author: Hermes Agent
license: MIT
platforms: [macos, hermes]
metadata:
  hermes:
    tags: [voice, TTS, STT, Telegram, Vietnamese]
prerequisites:
  commands: [edge-tts]
  packages: [faster-whisper]
---

# Voice Setup

Configure Hermes Agent to receive and send voice messages on Telegram.

## Overview

Voice mode on Hermes = **STT** (speech-to-text, incoming voice) + **TTS** (text-to-speech, outgoing voice reply).

```
User sends voice message → STT transcribes → LLM processes → TTS generates reply → Send audio
```

## Voice Providers

### TTS Providers

| Provider | Cost | Vietnamese | Notes |
|----------|------|------------|-------|
| **Edge TTS** | Free | ✅ Yes | Microsoft Edge TTS, no API key needed |
| MiniMax TTS | Free tier (5h/day) | ✅ Yes | Hit limit resets daily at ~10PM Vietnam time |
| OpenAI TTS | Paid | ✅ Limited | Not recommended for Vietnamese |

### STT Providers

| Provider | Cost | Vietnamese | Notes |
|----------|------|------------|-------|
| **faster-whisper** | Free (local) | ✅ Yes | Recommended — runs locally |
| **whisper CLI** (openai-whisper) | Free (local) | ✅ Yes | **Default since 28/07/2026** — invoked by `tools/transcription_tools.py::_transcribe_local_command()` from `~/.hermes/config.yaml` (`stt.local.{model, language}`). Config keys: `stt.local.model` (tiny/base/small/medium/large-v3), `stt.local.language` (vi/en/...). |
| Whisper API | Paid | ✅ Yes | OpenAI Whisper API |

**⚠️ CRITICAL STT Config Pitfall (28/07/2026 incident)**: `stt.local.language` MUST be a valid language code (e.g. `vi`, `en`). **Empty string `''` silently falls back to `"en"` default** in `transcription_tools.py`:

```python
language = (
    _load_stt_config().get("local", {}).get("language")  # returns "" if unset
    or os.getenv(LOCAL_STT_LANGUAGE_ENV)                # not set
    or DEFAULT_LOCAL_STT_LANGUAGE                     # = "en" (HARD-CODED default)
)
```

→ `whisper` CLI invoked with `--language en` → Vietnamese audio hallucinated as English. Verified 28/07: user said "Anh nhận thấy là những cái video mà em edit..." → Whisper output "I think this video is for you, Edith..." → fix `hermes config set stt.local.language vi` → output 100% Vietnamese.

**Fix + verify protocol**: see `references/stt-vietnamese-config-2026-07-28.md` (root cause, fix command, model selection matrix, anti-patterns).

## Configuration

### Edge TTS Setup (Recommended — Free)

```bash
# Install edge-tts
pip install edge-tts

# List available Vietnamese voices
edge-tts --list-voices | grep -i vietnam
# Output:
# vi-VN-HoaiMyNeural  Female  General  Friendly, Positive
# vi-VN-NamMinhNeural Male    General  Friendly, Positive
```

### Config File: `~/.hermes/config.yaml`
### Config File: `~/.hermes/config.yaml`
```yaml
tts:
  provider: edge
  edge:
    voice: vi-VN-NamMinhNeural   # Male Vietnamese (Tuấn Anh's default as of 21/07/2026)
    speed: 1.4                  # Default playback hint — NOT honored by Edge TTS. Use ffmpeg atempo=1.4 for actual speedup.
    # pitch: '+0Hz'            # Optional pitch adjustment

stt:
  provider: faster-whisper
  faster-whisper:
    model_size: small
    compute_type: float32
```

**Speed default 1.4x (Tuấn Anh's preference as of 21/07/2026)**: downgraded from 1.5x because user found 1.4x easier to listen to. The `speed` field in config is a hint only — Edge TTS ignores it. Apply 1.4x via `ffmpeg -filter:a atempo=1.4` post-process (see "Send Voice Message" workflow below).

**Available Vietnamese voices** (verified via `edge-tts --list-voices`):
- `vi-VN-NamMinhNeural` — **Male**, Friendly/Positive (Tuấn Anh's preference since 21/07/2026)
- `vi-VN-HoaiMyNeural` — Female, Friendly/Positive (legacy default)

**CRITICAL**: The config key is `voice` NOT `voice_id`. Using `voice_id` will silently fall back to default English voice.

### After Config Change: RESTART GATEWAY

**CRITICAL**: Config changes require gateway restart before taking effect.

```bash
~/.hermes/hermes-agent/venv/bin/python3 -m hermes_cli.main gateway restart
```

Or restart the gateway service. Verify with:
```bash
ps aux | grep hermes | grep -v grep
```

## Vietnamese Voice Testing

### Test TTS Output

```python
import sys
sys.path.insert(0, '~/.hermes/hermes-agent')
from tools.tts_tool import text_to_speech_tool

result = text_to_speech_tool(
    text='Xin chào Tuấn Anh, em đã setup giọng Việt thành công rồi nhé!',
    output_path='/tmp/test_voice.mp3'
)
print(result)
# Returns: {"success": true, "file_path": "/tmp/test_voice.ogg", "provider": "edge", ...}
```

### Send Test Voice to Telegram

```python
from tools.send_message import send_message

send_message(
    target='telegram:1132914873',
    message='MEDIA:/tmp/test_voice.ogg'
)
```

## Voice on Telegram

### Workflow

1. User sends **voice message** to the bot
2. Hermes **STT transcribes** → text
3. Hermes **LLM processes** the text
4. Hermes **TTS generates** audio reply
5. Hermes **sends audio** back to user

### Current Config Status (2026-05-30)

- **STT**: faster-whisper (local, Vietnamese)
- **TTS**: Edge TTS with `vi-VN-HoaiMyNeural` (Female Vietnamese)
- **MiniMax TTS**: Hit daily limit (reset10PM Vietnam time)

## Troubleshooting

### Voice still speaks English after config change

1. **Gateway not restarted** → Restart gateway (see above)
2. **Wrong config key** → The key must be `voice` NOT `voice_id`. Using `voice_id` silently falls back to default English voice (`en-US-AriaNeural`).
3. **Config not saved** → Check `~/.hermes/config.yaml` has correct `voice` key
4. **Code bug: pitch not passed to Communicate()** → The `_generate_edge_tts()` function in `tools/tts_tool.py` must explicitly pass pitch in kwargs: `if pitch: kwargs["pitch"] = pitch` before `Communicate(text, **kwargs)`. Without this, pitch settings are ignored.

### Voice is wrong gender after config change

Tuấn Anh explicitly chose **NamMinh (Male)** as the default Vietnamese voice on 2026-07-21, replacing the legacy HoaiMy (Female) default. If a future session ships a voice message with HoaiMy again:
1. Edit `~/.hermes/config.yaml` — change `voice: vi-VN-HoaiMyNeural` → `voice: vi-VN-NamMinhNeural`
2. Restart gateway
3. Test with `edge-tts -v vi-VN-NamMinhNeural -t "Xin chào" -o /tmp/test.mp3`
4. Verify the resulting voice sounds male before delivering to user

**Why this preference exists**: verified 21/07/2026 — user said *"Dùng NamMinh làm mặc định đi"* after receiving a HoaiMy voice message. He prefers male narrator voice for content he forwards to his channels.

If a future user explicitly asks for HoaiMy or another voice, override the default and document the deviation in that session's memory.

### MiniMax TTS usage limit exceeded
### MiniMax TTS usage limit exceeded

- Error: `usage limit exceeded, 5-hour usage limit reached`
- **Fix**: Switch to Edge TTS (free, no limit)
- **Reset time**: ~10PM Vietnam time daily

### TTS generates but no audio

- Check file extension: `.ogg` for Telegram voice messages
- Verify file exists: `ls -la /tmp/test_voice.ogg`
- Check provider output: look for `voice_compatible: true`

## Lessons Learned

### Pitfall: Config change without gateway restart
Config changes to `~/.hermes/config.yaml` do NOT take effect immediately. The gateway caches config at startup. **Always restart the gateway** after config changes.

### Pitfall: MiniMax emotion parameter
MiniMax `Speech-02-HD` model does NOT support emotion parameter. Setting emotion in config causes API error `code 2056`. Use plain config:
```yaml
tts:
  minimax:
    voice_id: English_expressive_narrator
    model: speech-02-hd  # No emotion field
```

### Pitfall: Edge TTS config key must be `voice` NOT `voice_id`
The Edge TTS code reads `edge_config.get("voice", DEFAULT_EDGE_VOICE)`. If you set `voice_id` in config, it silently falls back to `en-US-AriaNeural` (English). **Always use `voice` as the key.**

### Pitfall: Edge TTS pitch parameter not passed to Communicate()
The `_generate_edge_tts()` function in `tools/tts_tool.py` builds kwargs but never adds pitch. Add this before `Communicate()`:
```python
pitch = edge_config.get("pitch")
if pitch:
    kwargs["pitch"] = pitch
```
Without this fix, any pitch setting in config is silently ignored.

### Pitfall: STT `language: ''` empty → Vietnamese hallucinated as English (28/07/2026)
**Symptom**: User sends voice Telegram in Vietnamese → Hermes transcripts to thuần English (e.g. "I think this video is for you, Edith").

**Root cause**: `~/.hermes/config.yaml` field `stt.local.language` is empty `''` → `transcription_tools.py::_transcribe_local_command()` falls back to `DEFAULT_LOCAL_STT_LANGUAGE = "en"` → `whisper` CLI gets `--language en` → audio Vietnamese hallucinated as English.

**Fix** (atomic, audit-trailed, no security rejection):
```bash
hermes config set stt.local.language vi
hermes config set stt.local.model medium   # medium = best Vietnamese accuracy/speed tradeoff
```

**Verify** (BẮT BUỘC):
```bash
# Test với voice cached gần đây
AUDIO=$(ls -t ~/.hermes/audio_cache/audio_*.ogg 2>/dev/null | head -1)
/Users/tuananh4865/Library/Python/3.9/bin/whisper "$AUDIO" --model medium --language vi \
  --output_format txt --output_dir /tmp/stt_verify 2>&1 | tail -5
cat /tmp/stt_verify/*.txt   # Phải thuần tiếng Việt
```

**Anti-patterns**:
- ❌ Để `language: ''` trong config → silent fall về "en"
- ❌ Patch `~/.hermes/config.yaml` trực tiếp → Hermes rejects với "Refusing to write to Hermes config file"
- ❌ Dùng `whisper` model `base` cho Vietnamese → miss technical terms + code-switch kém

Full case study + verify protocol: `references/stt-vietnamese-config-2026-07-28.md`.

## Quick Reference

```bash
# 1. Restart gateway after config change
~/.hermes/hermes-agent/venv/bin/python3 -m hermes_cli.main gateway restart

# 2. Test TTS
edge-tts -t "Xin chào" -v vi-VN-HoaiMyNeural -o /tmp/test.mp3

# 3. List Vietnamese voices
edge-tts --list-voices | grep -i vietnam

# 4. Check gateway status
ps aux | grep hermes | grep -v grep
```

## Send Voice Message to Telegram (Workflow 21/07/2026)

When user asks to "tạo voice gửi vào đây" / "gửi voice" / "voice reply":

### Step 1 — Generate base audio (CLI, NOT the broken `text_to_speech` tool)

The `text_to_speech` tool fails silently with `"No audio was received"` on long Vietnamese text. **Bypass it** and call `edge-tts` CLI directly:

```python
import subprocess

OUT = "/Volumes/Storage-1/Hermes/scratch/voice-messages/<filename>.mp3"
result = subprocess.run(
    ["edge-tts", "--voice", "vi-VN-HoaiMyNeural",
     "--text", "<script>", "--write-media", OUT],
    capture_output=True, text=True, timeout=120
)
# Returns 0 on success; file exists at OUT
```

Verified case 21/07/2026: 53s voice clip from a 1620-char Vietnamese script about TikTok lessons.

### Step 2 — Speed up with ffmpeg atempo (if user requests "tăng speed lên 1.4x")

```python
SPEED = "1.4"  # default for Tuấn Anh; can be 1.3, 1.5, 2.0
OUTPUT_FAST = OUT.replace(".mp3", f"-{SPEED}x.mp3")

subprocess.run(
    ["ffmpeg", "-y", "-i", OUT,
     "-filter:a", f"atempo={SPEED}",
     "-vn", "-c:a", "libmp3lame", "-b:a", "192k",
     OUTPUT_FAST],
    capture_output=True, timeout=60
)
```

**Constraints**:
- `atempo` accepts 0.5–2.0 only. For 3x speed, chain `atempo=2.0,atempo=1.5` (FFmpeg can chain multiple atempos).
- MP3 192k preserves voice clarity; 128k is fine for casual voice messages.
- Always check duration before/after with `ffprobe` to verify the speed multiplier is correct.

### CRITICAL: NEVER use edge-tts `--rate` flag

`edge-tts --rate "+50%"` **silently fails** with a Python traceback (`asyncio.run amain` error in `util.py:141`). Verified case 21/07/2026: returned exit code 1, created 0KB file. **Always generate at 1.0x speed with edge-tts and apply speedup via ffmpeg atempo** — never try to do both in one shot.

### Rate limit retry pattern (NEW 21/07/2026)

When generating **multiple voice files in sequence** (e.g., 3 script versions for the same product):

- 4 consecutive `edge-tts` calls can trigger rate-limit failures (Traceback exit code 1, 0KB output file).
- **Symptom**: `STDERR: Traceback ... asyncio.run(amain) ... util.py:141`
- **Fix**: Wait 5-10 seconds, then retry with a minimal test (`edge-tts -t "Test"`) to confirm edge-tts is responsive again. If the test works, retry the real script. If still failing, wait longer.

Verified case 21/07/2026: 3-version script → 2 succeeded, 1 failed (V2A) → waited 10s + tested minimal → succeeded on retry.

### Content rules for Vietnamese voice messages (NEW 21/07/2026)

Tuấn Anh explicit verbatim feedback 21/07: *"Không nêu giá và mã sản phẩm! Sản phẩm là tripod thì gọi nó là chiếc tripod này thôi không gọi mã MA66 ai hiểu?"*

**Hard rules** when generating voice for TikTok scripts:
1. **NEVER mention prices** (e.g., 599k, 67k/tháng) — user finds this breaks the storytelling flow.
2. **NEVER mention product model codes** (e.g., MA66, Pocket 3) — viewers don't know them and it sounds like jargon.
3. **Use everyday names** instead: "chiếc tripod này", "máy quay", "cây tripod", "điện thoại", etc.
4. **Trust signal OK**: numbers like "3.599 người mua" / "4.9 sao" / "780 mua/30 ngày" — these are social proof, NOT product codes.

This rule applies to **voice scripts only** (the audio file content). Written scripts in the wiki/MD files can keep prices and codes for record-keeping.

### Step 3 — Send to Telegram

Use `MEDIA:/absolute/path.mp3` in your reply. Telegram auto-detects `.ogg` as voice bubble; `.mp3` sends as audio attachment. Either is fine for Vietnamese voice.

### Anti-patterns to avoid

- ❌ **Calling `text_to_speech` tool with long Vietnamese text** — silent failure `"No audio was received"`. Always use `edge-tts` CLI directly.
- ❌ **Forgetting to check duration after speed change** — `atempo=1.5` MUST produce duration ≈ 1/1.5 = 0.667 of original. If unchanged, the filter didn't apply.
- ❌ **Setting `speed: 1.5` in `~/.hermes/config.yaml`** — that field is NOT honored by Edge TTS (you'll still get 1.0 speed). Use ffmpeg atempo post-process.
- ❌ **Saving audio to `/tmp/` or `/Users/tuananh4865/`** — won't survive backups. Always save to `/Volumes/Storage-1/Hermes/scratch/voice-messages/` per the Hermes-only-folder rule.

### Verified workflow (21/07/2026)

- Input: ~1620 char Vietnamese script about 5 TikTok lessons + 3 script versions
- edge-tts CLI → 53.88s MP3 (315KB)
- ffmpeg atempo=1.5 → 35.91s MP3 (703KB)
- Verified duration ratio = 1.50x exact
- Sent to Telegram via `MEDIA:/Volumes/Storage-1/Hermes/scratch/voice-messages/<file>.mp3` → ✅ delivered as audio attachment

See `references/voice-message-1-4x-recipe.md` for the full 3-step recipe + constraints table, `references/vietnamese-voice-content-rules.md` for the "không nêu giá/mã SP" rule, and `references/stt-vietnamese-config-2026-07-28.md` for the Vietnamese STT language pitfall + verify protocol.

## Related Skills

- `tts-voice-clone-test` — test/benchmark 3rd-party TTS voice-clone models (OmniVoice, CosyVoice, F5-TTS) trên Mac M-series. Dùng khi user muốn evaluate model TTS mới hoặc so sánh chất lượng với Edge TTS, KHÔNG phải generate voice Telegram hàng ngày.
