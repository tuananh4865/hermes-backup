# ML Model Research — `curl` raw GitHub Source Files (Tier 5)

**Captured:** 2026-07-09 (YAMNet research session)
**Skill:** `mcp-search-workarounds`
**Lesson type:** Reusable research pattern + concrete escape hatch

## The Lesson

When researching an ML model (architecture, class IDs, hyperparameters, inference code), the authoritative answer lives in the **repo's source files**, not in blog posts or search snippets. `raw.githubusercontent.com` is a raw CDN with no JS, no auth, no rate limits, returns exact file bytes. It beats every extraction backend for code/CSV/Python files.

## When to Use

- You need **exact** class indices, hyperparameters, or input/output shapes (not paraphrases)
- The model has a public repo on GitHub with `params.py` / `config.yaml` / `class_map.csv` / `inference.py`
- Web search returns blog posts that quote the docs but drift (out of date, truncated)
- `web_extract` returns "search-only backend" error
- `mcp__exa__web_fetch_exa` returns only file previews (CSVs > 200 rows, code > 1000 lines)

## The 5-File Priority List

For ANY ML model repo, `curl` these in order:

1. **Hyperparameters** — `params.py` / `config.py` / `config.yaml`
   - sample rate, image size, sequence length, mel bands, num classes
2. **Class/label maps** — `class_map.csv` / `labels.json` / `vocab.txt`
   - ground-truth mapping from class index → human label
3. **Inference example** — `inference.py` / `predict.py` / `demo.py`
   - shows intended input/output shape and preprocessing
4. **Model definition** — `model.py` / `architecture.py` / `network.py`
   - exact layer spec (only if you need to retrain or fine-tune)
5. **README.md** (raw) — official usage instructions

## Recipe

```bash
# 1. Discover file structure (if you don't know exact paths)
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents/<dir>" 
# Returns JSON listing of files in <dir>

# 2. Fetch raw files (no auth, no rate limit on public repos)
curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>/<filename>" -o /tmp/<filename>

# 3. Combine with grep to find exactly what you need
grep -i "applause\|cheer" /tmp/yamnet_class_map.csv
grep -i "sample_rate\|patch_window" /tmp/yamnet_params.py

# 4. Read full file (read_file tool, not cat)
read_file(path="/tmp/yamnet_class_map.csv")
```

## Real Example: YAMNet Research (2026-07-09)

**Goal:** find exact class index for "Applause" / "Cheering" in YAMNet (521-class AudioSet model from Google).

**Tried and failed:**
- `mcp__MiniMax__web_search` → returned blog posts saying "Applause is one of the 521 classes" but no exact index
- `web_extract` on official repo → Tier 1 fail (DuckDuckGo "search-only backend")
- `mcp__exa__web_fetch_exa` on `yamnet_class_map.csv` → file too large to render in Exa (CSV preview only)
- `mcp__exa__web_fetch_exa` on `yamnet.py` source file → got source code (worked), but not the class map

**Winning move (2 seconds):**
```bash
curl -sL "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv" -o /tmp/yamnet_class_map.csv
grep -i "applause\|cheer\|crowd\|yell" /tmp/yamnet_class_map.csv
# → 6,Shout
# → 9,Yell
# → 58,Clapping
# → 61,Cheering
# → 62,Applause
# → 64,Crowd
```

**Bonus — got hyperparameters + inference code in same session:**
```bash
curl -sL "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/params.py" -o /tmp/yamnet_params.py
# → sample_rate=16000, patch_window_seconds=0.96, mel_bands=64, num_classes=521

curl -sL "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/inference.py" -o /tmp/yamnet_inference.py
# → shows scores, embeddings, spectrogram return tuple shape
```

**Saved:** ~6 web search queries + 3 page extraction attempts that would have all been approximations.

## Comparison: When to Use Each Tier

| Need | Best Tier | Why |
|------|-----------|-----|
| "What is X?" (definition, current state) | Tier 3 (search snippets) | Fast, 1 query |
| "What does the community think of X?" | Tier 4 (multiple searches) | Breadth over depth |
| "What is the exact class index / param / shape?" | **Tier 5 (curl raw GitHub)** | Authoritative, no drift |
| "Read the full paper / docs page" | Tier 1 (web_extract) if backend ≠ DuckDuckGo | Full prose |
| "Compare 2-3 ML models on benchmarks" | Tier 5 + Tier 3 (curl + search) | Numbers from papers, quotes from blogs |

## Key Insights

1. **Search snippets drift.** Blog posts paraphrasing official docs lose precision over time. The repo's source is always canonical.
2. **`raw.githubusercontent.com` is the most reliable URL pattern in MCP work** — no JS, no auth, no rate limits on public repos.
3. **For ML models, `params.py` and `class_map.csv` are 90% of the answer.** Pull those first, only dig into `model.py` if you need to retrain.
4. **Combine `curl` + `grep` + `read_file`** — fastest research loop, no LLM cost until synthesis.
5. **Always `curl -sL` (silent + follow redirects)** — GitHub sometimes redirects to codeload.github.com for tagged releases.
6. **For very large repos:** start with the `tree/<branch>` view via `mcp__exa__web_fetch_exa` (Exa renders file trees well) to discover paths, then `curl` each raw file.

## Anti-Pattern (don't do this)

❌ **5 web searches + 3 page extractions** to find an exact class index that lives in a 22KB CSV in the repo.

✅ **1 `curl` + 1 `grep`** → 2 seconds, authoritative.

## Related

- `SKILL.md` §"Page Extraction Failures — The 4-Tier Fallback Chain" — Tier 5 added below Tier 4
- `mcp-search-workarounds` is the umbrella for ALL MCP search/extract workarounds
- `source-driven-development` — general principle: ground every decision in official docs
