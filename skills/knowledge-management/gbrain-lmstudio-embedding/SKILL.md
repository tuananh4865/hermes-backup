---
name: gbrain-lmstudio-embedding
title: gbrain LM Studio Embedding Setup
description: Setup gbrain v0.27 with LM Studio embedding — create lmstudio recipe, configure env, fix PGLite WASM bug, use mxbai (1024 dims) for best quality
created: 2026-05-01
updated: 2026-05-01
type: skill
tags: [gbrain, lm-studio, embedding]
confidence: high
relationships: [lm-studio, gbrain]
---

# gbrain + LM Studio Embedding Setup

## Problem
gbrain defaults to OpenAI `text-embedding-3-large` (1536 dims) for embeddings. User wants local embedding via LM Studio instead of paying for OpenAI API.

## Architecture

```
gbrain → AI Gateway (Vercel SDK) → lmstudio recipe → LM Studio /v1/embeddings
```

LM Studio recipe uses `createOpenAICompatible()` with `baseURL=http://localhost:1234/v1`.

## Option A: PR #257 Branch — Pluggable Embedding Providers (RECOMMENDED)

PR #257 (`garrytan/embedding-providers`, v0.27) merges all community PRs into a unified pluggable system using Vercel AI SDK. Supports Ollama, LM Studio, Voyage, Google Gemini, and any OpenAI-compatible endpoint.

**CRITICAL LEARNING: lmstudio recipe must be CREATED** — v0.27.0 doesn't ship with it. Recipe `default_dims` is used when no dimensions env var is set. Must update recipe AND .env when switching models.

### 1. Checkout the embedding-providers branch
```bash
cd ~/gbrain
git fetch origin
git checkout garrytan/embedding-providers
bun install
```

### 2. Create lmstudio recipe (NOT included in v0.27.0!)
```bash
# Create file: ~/gbrain/src/core/ai/recipes/lmstudio.ts
cat > src/core/ai/recipes/lmstudio.ts << 'EOF'
import type { Recipe } from '../types.ts';

export const lmstudio: Recipe = {
  id: 'lmstudio',
  name: 'LM Studio (local)',
  tier: 'openai-compat',
  implementation: 'openai-compatible',
  base_url_default: 'http://localhost:1234/v1',
  auth_env: {
    required: [],
    optional: ['LMSTUDIO_BASE_URL'],
    setup_url: 'https://lmstudio.ai',
  },
  touchpoints: {
    embedding: {
      models: ['text-embedding-nomic-embed-text-v1.5', 'text-embedding-mxbai-embed-large-v1'],
      default_dims: 1024, // CHANGE THIS to match your model: 768 (nomic) or 1024 (mxbai)
      cost_per_1m_tokens_usd: 0,
      price_last_verified: '2026-04-30',
    },
  },
  setup_hint: 'Download LM Studio from https://lmstudio.ai, load a text embedding model, and start the local server.',
};
EOF
```

### 3. Add lmstudio to recipes index
```bash
# Edit src/core/ai/recipes/index.ts — add 'lmstudio' to the ALL array
```

### 4. Configure environment
```bash
# In ~/gbrain/.env:
OPENAI_API_KEY=sk-dummy
GBRAIN_EMBEDDING_MODEL=lmstudio:text-embedding-mxbai-embed-large-v1
GBRAIN_EMBEDDING_DIMENSIONS=1024
```

### 5. Build binary
```bash
cd ~/gbrain
bun build --compile --outfile bin/gbrain src/cli.ts
```

### 6. Test
```bash
./bin/gbrain providers test --model lmstudio:text-embedding-mxbai-embed-large-v1
./bin/gbrain query "test query"
```

## Option B: Fallback with openai-compatible baseURL Override (for v0.22.8)

If PR #257 branch is unavailable, use this workaround:

### 1. Download and load model in LM Studio
```bash
# mxbai-embed-large-v1 (1024 dims) — best GGUF option
"/Applications/LM Studio.app/Contents/Resources/app/.webpack/lms" get "https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1"
"/Applications/LM Studio.app/Contents/Resources/app/.webpack/lms" load "mixedbread-ai/mxbai-embed-large-v1"
```

### 2. Configure baseURL override
```bash
# In ~/gbrain/.env:
OPENAI_API_KEY=sk-dummy
OPENAI_BASE_URL=http://localhost:1234/v1
```

### 3. Patch DIMENSIONS in embedding.ts
Edit `src/core/embedding.ts`:
```typescript
const DIMENSIONS = 1024;  // mxbai = 1024, nomic = 768
```

### 4. Run (compiled binary may fail — use bun run instead)
```bash
# Binary compiled with bun may have PGLite WASM bug:
./bin/gbrain query "test"  # → "ENOENT: no such file or directory, open '/$bunfs/root/pglite.data'"

# Workaround — use bun run directly:
bun run src/cli.ts query "test"  # Works
```

## Troubleshooting

### PGLite Lock Timeout / "$bunfs/root/pglite.data" error
This is a macOS 26.3 WASM bug in compiled binaries. The `bun build --compile` binary tries to write to `/$bunfs/root/` which doesn't exist on macOS.

**Workaround — use bun run instead of compiled binary:**
```bash
# DON'T:
./bin/gbrain query "test"  # → ENOENT error

# DO:
bun run src/cli.ts query "test"  # Works

# Or create alias:
alias gbrain='cd ~/gbrain && ~/.bun/bin/bun run src/cli.ts'
```

**Alternative fix (may work):**
```bash
rm -rf ~/.gbrain/.gbrain-lock ~/.gbrain/postmaster.pid
pkill -f bun
```

### `gbrain init` does NOT read .env file
**CRITICAL**: When initializing a fresh brain with `gbrain init`, you MUST pass embedding model and dimensions as CLI flags. The `.env` file is ignored during init.

```bash
# WRONG — .env is NOT read by init:
bun run src/cli.ts init --pglite  # → uses 1536 dims from recipe default

# CORRECT — pass as CLI flags:
bun run src/cli.ts init --pglite --embedding-model lmstudio:text-embedding-mxbai-embed-large-v1 --embedding-dimensions 1024
```

This means if you reset the database (delete brain.pglite), you must re-init with flags:
```bash
rm -rf ~/.gbrain/brain.pglite ~/.gbrain/import-checkpoint.json
bun run src/cli.ts init --pglite --embedding-model lmstudio:text-embedding-mxbai-embed-large-v1 --embedding-dimensions 1024
```

### Wiki source shows 0 pages but sync completes successfully
The `gbrain sources list` may show "0 pages" for a newly-added source even after successful sync. This is a display bug. The actual data is imported correctly — test with `gbrain query` to verify.

To force a clean re-import:
```bash
rm -rf ~/.gbrain/brain.pglite ~/.gbrain/import-checkpoint.json
bun run src/cli.ts init --pglite --embedding-model lmstudio:text-embedding-mxbai-embed-large-v1 --embedding-dimensions 1024
bun run src/cli.ts sources add wiki --path /Volumes/Storage-1/Hermes/wiki
# Run sync with nohup to avoid PGLite lock conflicts:
cd ~/gbrain && nohup bash -c 'PATH="$HOME/.bun/bin:$PATH" ~/.bun/bin/bun run src/cli.ts sync --source wiki --full > ~/.gbrain/sync.log 2>&1' &
```

### Model dimension mismatch
If you see "Embedding dim mismatch: model returned X but schema expects Y":

**CRITICAL: Three places must agree on dims AND model:**
1. `.env` file: `GBRAIN_EMBEDDING_DIMENSIONS=1024`
2. `gbrain config set` (stored in brain): `bun run src/cli.ts config set embedding_dimensions 1024`
3. Recipe `default_dims` in `src/core/ai/recipes/lmstudio.ts`

If any one disagrees → "Embedding dim mismatch" error.

**To change models:**
```bash
# 1. Update .env
sed -i '' 's/GBRAIN_EMBEDDING_MODEL=lmstudio:.*/GBRAIN_EMBEDDING_MODEL=lmstudio:text-embedding-mxbai-embed-large-v1/' .env
sed -i '' 's/GBRAIN_EMBEDDING_DIMENSIONS=.*/GBRAIN_EMBEDDING_DIMENSIONS=1024/' .env

# 2. Update config in brain
bun run src/cli.ts config set embedding_model lmstudio:text-embedding-mxbai-embed-large-v1
bun run src/cli.ts config set embedding_dimensions 1024

# 3. Update recipe default_dims
# Edit src/core/ai/recipes/lmstudio.ts → default_dims: 1024

# 4. Rebuild binary
bun build --compile --outfile bin/gbrain src/cli.ts
```

## Tested Model Results
| Model | Dims | Speed | Status |
|-------|------|-------|--------|
| nomic-embed-text-v1.5 | 768 | ~185ms | ✓ Works |
| mxbai-embed-large-v1 | 1024 | ~55ms | ✓ Better (faster + more dims) |

## Model ID Format
LM Studio embedding model IDs use format: `text-embedding-{model-name}`
- `text-embedding-nomic-embed-text-v1.5`
- `text-embedding-mxbai-embed-large-v1`

Not the HuggingFace model ID — these are LM Studio's internal embedding model IDs.

## Verified Working Setup (2026-05-01)
- **Wiki source**: /Volumes/Storage-1/Hermes/wiki — 3673 files, 14175 chunks imported
- **Model**: mxbai-embed-large-v1 (1024 dims) — fast ~55ms per embedding
- **LM Studio**: localhost:1234, model loaded as `text-embedding-mxbai-embed-large-v1`
- **Query results**: 20 results returned with relevance scores 0.9+ for top matches

## Quick Reference (verified working alias)
```bash
# Add to ~/.zshrc or ~/.bashrc:
alias gbrain='cd ~/gbrain && PATH="$HOME/.bun/bin:$PATH" ~/.bun/bin/bun run src/cli.ts'

# Usage:
gbrain sources list
gbrain query "your question"
gbrain providers list
```

### LM Studio not responding
- LM Studio runs on `localhost:1234` (not `192.168.0.187`)
- Verify: `curl http://localhost:1234/v1/models`

## Verification
```bash
curl -s http://localhost:1234/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"text-embedding-nomic-embed-text-v1.5","input":"test"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('dims:', len(d['data'][0]['embedding']))"
```
