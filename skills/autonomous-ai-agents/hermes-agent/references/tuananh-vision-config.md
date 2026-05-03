# Tuấn Anh's Vision Configuration

## Current Working Setup

Vision tool is configured to use **LM Studio local server** with a multimodal small model:

```yaml
auxiliary:
  vision:
    provider: custom
    model: qwen3.5-0.8b
    base_url: http://localhost:1234/v1
    api_key: none
    timeout: 120
    download_timeout: 30
```

## How to Verify Vision is Working

```bash
# Check logs for current vision provider
grep "Auxiliary vision" ~/.hermes/logs/agent.log | tail -5
```

Expected output when working:
```
Auxiliary vision: using custom (qwen3.5-0.8b) at http://localhost:1234/v1/
```

## Common Mistake: Over-diagnosing

**Symptom:** Agent spends too much time investigating vision when it's already working.

**Lesson:** Before digging into provider code, check the actual config and logs first:
1. `cat ~/.hermes/config.yaml | grep -A8 "auxiliary:"`
2. `grep "Auxiliary vision" ~/.hermes/logs/agent.log | tail -3`

**Tuấn Anh's environment specifics:**
- Main model: `MiniMax-M2.7` (text-only, no vision) — confirmed
- Vision backend: **LM Studio** (`qwen3.5-0.8b`) at `localhost:1234` — this is what actually handles vision
- No OpenRouter key needed for vision when using local backend

## Related

- [[hermes-agent]] skill — Troubleshooting section has detailed MiniMax vision fix documentation
