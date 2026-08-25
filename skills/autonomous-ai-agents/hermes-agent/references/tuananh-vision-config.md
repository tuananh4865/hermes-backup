# Tuấn Anh's Vision Configuration

## Current Working Setup

Vision tool is configured to use **LM Studio local server** with a multimodal model:

```yaml
auxiliary:
  vision:
    provider: custom
    model: zai-org/glm-4.6v-flash
    base_url: http://localhost:1234/v1
    api_key: no-key
    timeout: 120
    download_timeout: 30
```

## Critical: Not All Models Support Vision

LM Studio serves multiple models — most are TEXT-ONLY and will crash on image input.
The error: `BadRequestError: The model has crashed without additional information.`

**Model compatibility (LM Studio, tested 2026-05-10):**
| Model | Vision | Status |
|-------|--------|--------|
| `zai-org/glm-4.6v-flash` | ✅ | Working — "The pixel is red" |
| `google/gemma-4-e4b` | ❌ | Crashes on image input |
| `google/gemma-4-e2b` | ❌ | Crashes on image input |
| `qwen3.5-0.8b` | ❌ | Crashes on image input |
| `qwen/qwen3.5-9b` | ❌ | Text-only |

**Rule:** Model name must contain "v" (e.g., `glm-4.6v`, `qwen-vl`, `llava`, `pixtral`) to indicate vision capability.

## How to Verify

```bash
# Check which model is actually being used
grep "Auxiliary vision" ~/.hermes/logs/agent.log | tail -3
```

## Related

- [[hermes-agent]] skill — Troubleshooting section has detailed vision fix documentation