# MiniMax 401 Auth Failure — 2026-06-07

## Error Observed
```
HTTP 401: login fail: Please carry the API secret key in the 'X-Api-Key' field of the request header
Authorization: Bearer *** ← API key missing (shows "Bearer None")
Status: non_retryable_client_error
```

## Sessions Affected
All 9 attempts on 2026-06-07 failed identically:
- Session `20260606_142557_c7a13bb5` — TikTok content research (23:53 → 00:17)
- Session `20260607_001949_bfbfbc` — "hi" greeting (00:20 → 07:23)
- Session `20260607_073641_742c12` — "hi" greeting (07:36 → 08:40)

## Root Cause
MiniMax API requires the secret key in the `X-Api-Key` request header, NOT in the standard `Authorization: Bearer` header. When the key is missing or misconfigured, the API returns 401 with the message "Please carry the API secret key in the 'X-Api-Key' field".

## Diagnostic Steps

```bash
# 1. Check if MINIMAX_API_KEY is set in .env
grep MINIMAX ~/.hermes/.env

# 2. Check what the gateway is actually sending (look at request dump)
cat ~/.hermes/sessions/request_dump_*.json | python3 -c "
import json,sys
for line in sys.stdin:
    try:
        d = json.loads(line)
        if d.get('reason') == 'non_retryable_client_error':
            headers = d['request']['headers']
            print(f\"Auth: {headers.get('Authorization', 'MISSING')}, X-Api-Key: {headers.get('X-Api-Key', 'MISSING')}\")
    except: pass
"

# 3. Test MiniMax API directly with curl
curl -X POST https://api.minimax.io/anthropic/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $MINIMAX_API_KEY" \
  -d '{"model":"MiniMax-M2.7","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

## Known Fix Patterns

### Pattern 1: Wrong env var name
**Symptom:** `.env` has `MINIMAX_API_KEY` but provider expects `ANTHROPIC_API_KEY` or vice versa.

**Fix:** Check the actual env var names expected:
```bash
# Check what Hermes config expects for MiniMax
grep -i minimax ~/.hermes/hermes-agent/hermes_cli/config.py | head -20
```

### Pattern 2: API key not set (empty or "None")
**Symptom:** `Authorization: Bearer None` in request dumps.

**Fix:**
```bash
# Set the key properly
hermes config set model.api_key YOUR_MINIMAX_API_KEY

# Or check .env has the right variable
echo "MINIMAX_API_KEY=your_actual_key" >> ~/.hermes/.env
```

### Pattern 3: Provider auth method mismatch
**Symptom:** MiniMax expects `X-Api-Key` but Hermes is sending `Authorization: Bearer`.

**Fix:** Check the provider configuration — MiniMax with Anthropic-compatible endpoint should use:
```yaml
model:
  provider: minimax
  base_url: https://api.minimax.io/anthropic
  api_key: YOUR_MINIMAX_API_KEY  # Must be set, not "None"
```

## Prevention
- If MiniMax auth fails with 401, always check:
  1. `MINIMAX_API_KEY` is set in `~/.hermes/.env`
  2. `model.api_key` in `config.yaml` is not empty
  3. Gateway has been restarted after config changes