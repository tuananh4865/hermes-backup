# LM Studio Vision Model Crash — Debugging Guide

**Date:** 2026-05-10
**Updated:** 2026-05-10 (triple-location env var precedence discovered)
**Issue:** Vision tool crashes with `OSError: broken data stream when reading image file` or `Error code: 400 — broken data stream`

## Quick Diagnosis

```bash
# Check what model the RUNNING gateway process sees
python3 -c "import os; print('AUXILIARY_VISION_MODEL:', os.environ.get('AUXILIARY_VISION_MODEL'))"

# All three locations MUST agree — check them all:
echo "=== config.yaml ===" && grep -A5 "vision:" ~/.hermes/config.yaml | head -10
echo "=== .env ===" && grep AUXILIARY_VISION ~/.hermes/.env
echo "=== plist ===" && grep AUXILIARY_VISION ~/Library/LaunchAgents/ai.hermes.gateway.plist
```

## Root Cause: Triple-Location Env Var Override

The AUXILIARY_VISION_MODEL env var is set in **THREE PLACES** and they must all agree:

1. **`~/.hermes/config.yaml`** — `auxiliary.vision.model: google/gemma-4-e2b`
2. **`~/.hermes/.env`** — `AUXILIARY_VISION_MODEL=google/gemma-4-e2b`
3. **`~/Library/LaunchAgents/ai.hermes.gateway.plist`** — `EnvironmentVariables.AUXILIARY_VISION_MODEL`

**Precedence (highest to lowest):**
1. `.env` (loaded with `override=True` at module import time in `cli.py:98`)
2. `config.yaml` written to env vars at startup (`run.py:512-527`)
3. plist `EnvironmentVariables` (inherited by gateway process from launchd)

**The .env file wins.** Even if config.yaml and plist both say `gemma-4-e2b`, if `.env` says `gemma-4-e4b`, the running gateway will use `gemma-4-e4b`.

**Why gateway keeps using old model after config changes:** The `.env` file has the wrong value. Restarting the gateway via launchctl doesn't help because launchd reads `.env` fresh on each start (via the gateway's env loader), and `.env` was the stale source.

## Verified Working Models

| Model | Vision? | Status |
|-------|---------|--------|
| `google/gemma-4-e2b` | ✅ Yes | Works with real PNG/JPEG images (verified 2026-05-10) |
| `zai-org/glm-4.6v-flash` | ✅ Yes | Reliable, "v" suffix guarantees multimodal |
| `google/gemma-4-e4b` | ❌ Text-only | Crashes on image input |
| `qwen3.5-0.8b` | ❌ Text-only | Crashes on image input |

**gemma-4-e2b caveat:** Requires valid image input — properly formatted PNG/JPEG at reasonable resolution. Tiny test images (1x1 pixel) or malformed base64 fail with "Invalid image detected". Test with a real image (e.g. download Google logo).

## Crash Signatures

### Text-only model on image input
```
openai.BadRequestError: Error code: 400 - {
  'error': 'Error in iterating prediction stream: OSError: broken data stream when reading image file'
}
```
→ Model cannot process images. Switch to a vision-capable model.

### Tiny/malformed test image
```
BadRequestError: Error code: 400 - {'error': 'Invalid image detected at index 0 '}
```
→ Image is too small or malformed. Use a real PNG/JPEG (e.g. download Google logo).

## Working Vision Configs (2026-05-10)

### Preferred: gemma-4-e2b (Tuấn Anh's choice)
```yaml
auxiliary:
  vision:
    provider: custom
    model: google/gemma-4-e2b
    base_url: http://localhost:1234/v1
    api_key: no-key      # NOT "none" — LM Studio rejects "none"
    timeout: 120
```

### Alternative: glm-4.6v-flash
```yaml
auxiliary:
  vision:
    provider: custom
    model: zai-org/glm-4.6v-flash
    base_url: http://localhost:1234/v1
    api_key: no-key
    timeout: 120
```

## Debugging Steps

```python
# 1. Check what's actually running in the gateway process
import os
print(os.environ.get('AUXILIARY_VISION_MODEL'))   # stale if gateway wasn't restarted
print(os.environ.get('AUXILIARY_VISION_API_KEY')) # must be 'no-key', not 'none'

# 2. Test a model directly with image input
from tools.vision_tools import vision_analyze_tool
import asyncio, tempfile, base64, uuid

png_b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=='
tmp = pathlib.Path(tempfile.gettempdir()) / f'test_{uuid.uuid4()}.png'
tmp.write_bytes(base64.b64decode(png_b64))

result = asyncio.run(vision_analyze_tool(str(tmp), 'What color is this pixel?'))
print(result)
tmp.unlink()

# 3. List available models on LM Studio
curl http://localhost:1234/v1/models
# Only models with "v" in name support vision: glm-4.6v-flash, qwen-vl, etc.
```

## Checking Active Vision Model at Runtime

```python
from agent.auxiliary_client import resolve_vision_provider_client
provider, client, model = resolve_vision_provider_client(async_mode=True)
print(f"Provider: {provider}, Model: {model}")
```

## MiniMax-M2.7 Is Text-Only

The main model `MiniMax-M2.7` does NOT support vision. Vision is handled by the `auxiliary.vision` config — it routes to a separate vision-capable model (OpenRouter, Nous, or custom LM Studio endpoint).