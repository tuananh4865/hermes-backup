# MiniMax + Droid Configuration (Verified 2026-05-29)

## Anthropic-Compatible Path (RECOMMENDED)

Works for: M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2

```json
// ~/.factory/config.json
{
  "custom_models": [
    {
      "model_display_name": "MiniMax-M2.7",
      "model": "MiniMax-M2.7",
      "base_url": "https://api.minimax.io/anthropic",
      "api_key": "<MINIMAX_API_KEY>",
      "provider": "anthropic",
      "max_tokens": 64000
    }
  ]
}
```

**Env setup:**
```bash
# Clear old env vars (CRITICAL — these override config.json)
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_BASE_URL

# Launch Droid and pick model
droid
# → /model → select MiniMax-M2.7
```

## OpenAI-Compatible Path

Works for: M2.7, M2.7-highspeed only

```json
// ~/.factory/config.json
{
  "custom_models": [
    {
      "model_display_name": "MiniMax-M2.7",
      "model": "MiniMax-M2.7",
      "base_url": "https://api.minimax.io/v1",
      "api_key": "<MINIMAX_API_KEY>",
      "provider": "generic-chat-completion-api",
      "max_tokens": 64000
    }
  ]
}
```

## Key Differences

| Path | Base URL | Provider | Supports M2.7? | Features |
|------|----------|----------|----------------|----------|
| Anthropic-compatible | `api.minimax.io/anthropic` | `anthropic` | ✅ Yes | Thinking blocks, prompt caching, interleaved thinking |
| OpenAI-compatible | `api.minimax.io/v1` | `generic-chat-completion-api` | ✅ Yes | Standard chat completions |

## China Users

Replace `api.minimax.io` with `api.minimaxi.com`:
- International: `https://api.minimax.io/anthropic`
- China: `https://api.minimaxi.com/anthropic`

## Verified Sources

- [MiniMax Droid Guide](https://platform.minimax.io/docs/token-plan/droid)
- [Compatible Anthropic API](https://platform.minimax.io/docs/api-reference/text-anthropic-api)
- [M2.7 for AI Coding Tools](https://platform.minimax.io/docs/guides/text-ai-coding-tools)
