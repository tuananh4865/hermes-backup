# Mem0 OSS + Ollama Fully Local Setup

**Source:** Researched 2026-05-21 via Mem0 docs + GitHub + Codex verification

## Why This Matters

Mem0 has TWO products with similar names:
- **Mem0 Plugin** (Hermes bundled): Uses `MemoryClient` → cloud API → requires `MEM0_API_KEY`
- **Mem0 OSS** (`mem0ai` pip): Uses `Memory` class → local inference → free, no API key

## Compatible Ollama Models

| Model | Type | Size | Use |
|-------|------|------|-----|
| `llama3.1:8b` | LLM | 8B | ✅ Recommended — balanced performance |
| `llama3.2:3b` | LLM | 3B | Lighter, faster, less RAM |
| `mistral:7b` | LLM | 7B | Good for reasoning |
| `nomic-embed-text` | Embedder | 137M | ✅ Required for local embedding (768 dims) |

## Setup Commands

```bash
# 1. Install Ollama
brew install ollama

# 2. Start Ollama service
ollama serve  # background, or: brew services start ollama

# 3. Pull models
ollama pull llama3.1:8b
ollama pull nomic-embed-text:latest

# 4. Verify models
curl http://localhost:11434/api/tags

# 5. Install Mem0 OSS + ChromaDB
pip install mem0ai chromadb

# 6. Test
python3 -c "
from mem0 import Memory
m = Memory()
m.add('Test memory', user_id='test')
print(m.search('test', user_id='test'))
"
```

## ⚠️ Critical: Embedding Dimensions

`nomic-embed-text` produces **768-dimensional** vectors.

When using Chroma as vector store:
```python
vector_store={
    "provider": "chroma",
    "config": {
        "collection_name": "memories",
        "path": "~/.hermes/mem0/chroma_db",
        "embedding_model_dims": 768  # REQUIRED — nomic-embed-text is 768, NOT 1536
    }
}
```

If you forget this: `DataException: expected 1536 dimensions, not 768`

## Full Mem0 OSS Config

```python
from mem0 import Memory
from mem0.configs.base import MemoryConfig

config = MemoryConfig(
    llm={
        "provider": "ollama",
        "config": {
            "model": "llama3.1:8b",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434"
        }
    },
    embedder={
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://localhost:11434"
        }
    },
    vector_store={
        "provider": "chroma",
        "config": {
            "collection_name": "memories",
            "path": "~/.hermes/mem0/chroma_db",
            "embedding_model_dims": 768
        }
    }
)
memory = Memory(config)
```

## Known Issues

### Ollama LLM URL Bug (fixed in Mem0 PR #4320)
`OllamaLLM` constructor reads wrong config nesting (`config.config.url` instead of `config.url`), falling back to `localhost:11434` even when configured for remote Ollama. Fixed March 13, 2026 in PR #4320. Update mem0ai if you hit this.

### No Authentication on Ollama
Ollama has no auth by default. If exposed to network, anyone can access. For local-only this is fine.

## Integration with Hermes

Mem0 OSS is a Python library — NOT a Hermes plugin. Integration options:

| Option | Effort | Use Case |
|--------|--------|----------|
| Direct Python usage in scripts/cron | Low (30 min) | Standalone memory extraction from wiki/logs |
| Custom MemoryProvider wrapper | High (2-3h) | Full integration with Hermes agent loop |
| Keep wiki + improve retrieval | Minimal | If wiki is already working |

**Recommended for most cases:** Use direct Python + cron job for extraction, keep Hermes built-in memory as primary.