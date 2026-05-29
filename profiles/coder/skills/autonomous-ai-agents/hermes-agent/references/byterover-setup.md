# ByteRover Setup (No ByteRover Account Required)

> Created: 2026-05-06
> Source: Session verification of ByteRover CLI v3.10.3

## The Misleading Error

When you first run `brv curate` without connecting a provider:

```
Unexpected error: No provider connected.
Run "brv providers connect byterover" to use the free built-in provider,
or connect another provider.
```

**This error misleads you into thinking you need a ByteRover account.** You do NOT.

The actual fix: connect a third-party LLM provider (MiniMax, OpenRouter, Anthropic, etc.).

## Setup Steps (MiniMax — no new API key needed)

```bash
# 1. Ensure brv is in PATH (added by installer)
export PATH="$HOME/.brv-cli/bin:$PATH"

# 2. Load existing MiniMax API key from .env
export $(grep -v '^#' ~/.hermes/.env | xargs)

# 3. Connect MiniMax as ByteRover provider (NO ByteRover account needed)
brv providers connect minimax --api-key "$MINIMAX_API_KEY"
```

## Verified Working (2026-05-06)

- `brv providers connect minimax` → ✅ Connected to MiniMax (minimax)
- `brv curate "test entry"` → ✅ Curated successfully
- `brv query "test entry"` → ✅ Query returned result
- ByteRoverMemoryProvider in hermes-agent → ✅ `is_available: True`, `prefetch()` returns results

## Provider Options (all work without ByteRover account)

| Provider | Command |
|----------|---------|
| MiniMax | `brv providers connect minimax --api-key $MINIMAX_API_KEY` |
| OpenRouter | `brv providers connect openrouter --api-key $OPENROUTER_API_KEY` |
| Anthropic | `brv providers connect anthropic --api-key $ANTHROPIC_API_KEY` |
| OpenAI | `brv providers connect openai --api-key $OPENAI_API_KEY` |

## LM Studio Local Model (100% Offline)

ByteRover can use LM Studio local models — no API key, no internet needed.

### Available LM Studio Models (localhost:1234)
```
qwen3.5-0.8b, google/gemma-4-e2b, google/gemma-4-e4b, qwen3.6-35b-a3b
```

### Local Model Test Results (2026-05-06, verified)

| Model | Curate | Query | Status | Notes |
|-------|--------|-------|--------|-------|
| **qwen3.5-4b-awq-instruct** | **~44s** | **~46s** | **✅ BEST** | Fastest, stable (VRAM permitting) |
| google/gemma-4-e2b | ~76s | ~76s | ✅ Works | **Current active model** |
| google/gemma-4-e4b | ~87s | ~75s | ✅ Works | More VRAM |
| QuantTrio-Qwen3.5-4B-AWQ | ~85s | — | ⚠️ Slow | Occasional empty output |
| qwen3.5-0.8B | ❌ | — | ❌ | Too small for ByteRover |
| qwen3.6-35b-a3b | ❌ | — | ❌ | Too slow |

**Failed experiments (2026-05-06):**
- `Qwen3.5-2B-mxfp4` (MLX, 1.5GB) → appeared in `/v1/models` as `qwen3.5-2b@mxfp4` but `brv` → `Failed to load model` (MLX runtime not available via API)
- `Qwen3.5-2B-GGUF Q4_K_M` (1.2GB) → prompt template error (`"No user query found in messages"`)
- After loading 2B models, 4B AWQ model disappeared from `/v1/models` (VRAM full)

**Recommendation:** `gemma-4-e2b` is the reliable current choice. `qwen3.5-4b-awq-instruct` is faster but VRAM contention can cause model eviction.

**Recommendation: `qwen3.5-4b-awq-instruct`** — ~45s curate/query, 3× faster than gemma-4-e2b. Use `qwen3.5-4b-awq-instruct` in the brv connect command.

### Setup (LM Studio Local — recommended model)

```bash
export PATH="$HOME/.brv-cli/bin:$PATH"

brv providers connect openai-compatible \
  --base-url http://localhost:1234/v1 \
  --model qwen3.5-4b-awq-instruct \
  --api-key "no-key"

# Verify
brv status
# Output: Provider: OpenAI Compatible | Model: qwen3.5-4b-awq-instruct

# Test
brv curate "Test local model $(date)"
brv query "Test local"
```

### Speed Comparison

| Provider | Speed | API Key | Internet | Privacy |
|----------|-------|---------|----------|---------|
| MiniMax cloud | ~5s | Yes | Yes | No |
| google/gemma-4-e4b via LM Studio | 75-87s | No | No | ✅ 100% local |

For cron jobs: use MiniMax. For privacy-sensitive memory: use LM Studio.

## What Requires ByteRover Account (NOT local usage)

These cloud features require `brv login`:
- `brv vc push` / `brv vc pull` — cloud sync
- `brv vc clone` — clone remote space
- `brv space switch` — team spaces
- `brv providers connect byterover` — ByteRover built-in LLM (requires login, limited free usage)

Local-only features that NEVER need login:
- `brv status` — local project state
- `brv query` — search local context tree
- `brv curate` — add to local context tree (AFTER connecting a third-party provider)
- `brv providers connect <third-party>` — connect any external LLM provider
- `brv connectors` — manage agent connectors
- `brv hub` — browse skills/bundles

## Hermes Agent Integration

The ByteRoverMemoryProvider plugin is at:
```
~/.hermes/hermes-agent/plugins/memory/byterover/__init__.py
```

To use ByteRover as Hermes memory provider:
```bash
hermes config set memory.provider byterover
```

Or keep `wiki` as primary and run both:
- WikiMemoryProvider: checkpoints, wiki/log.md write
- ByteRoverMemoryProvider: long-term memory search + LLM categorization

MemoryManager supports multiple providers simultaneously.

## Quick Test

```bash
export PATH="$HOME/.brv-cli/bin:$PATH"
export $(grep -v '^#' ~/.hermes/.env | xargs)

# Option A: MiniMax cloud (fast ~5s)
brv providers connect minimax --api-key "$MINIMAX_API_KEY"

# Option B: LM Studio local (100% private, ~45s with qwen3.5-4b-awq)
brv providers connect openai-compatible \
  --base-url http://localhost:1234/v1 \
  --model qwen3.5-4b-awq-instruct \
  --api-key "no-key"

# Verify
brv status
brv curate "Test $(date)"
brv query "Test"
```

## Key Insight

**ByteRover is truly local-first.** The "No provider connected" error means "no LLM provider connected for the curate/query operations" — NOT "no ByteRover account." You only need a third-party API key, which you likely already have.
