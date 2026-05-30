---
name: voice-setup
description: Configure voice STT/TTS for Hermes Agent — Telegram voice messages, Vietnamese TTS, Edge TTS, gateway voice integration.
version: 1.0.0
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
| Whisper API | Paid | ✅ Yes | OpenAI Whisper API |

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
    voice: vi-VN-HoaiMyNeural  # Female Vietnamese voice — KEY IS "voice" NOT "voice_id"
    speed: 1.0                 # 1.0 = normal speed
    # pitch: '+0Hz'           # Optional pitch adjustment

stt:
  provider: faster-whisper
  faster-whisper:
    model_size: small
    compute_type: float32
```

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
