---
name: ml-model-comparison-report
description: Research and comparison report for picking between pretrained ML models (audio, vision, NLP) for a specific use case. Use when user asks "research X vs Y", "compare A and B", "chọn model nào cho task Z", "phân tích toàn diện model X", "đánh giá model X có gì mới", or wants benchmarks plus decision matrix plus code snippets plus deployment gotchas. Produces a structured markdown report saved to file, bilingual Vietnamese/English following the user's reading language. Covers arxiv papers, GitHub repos, pretrained checkpoints, benchmark numbers on target hardware, multi-label vs softmax tradeoffs, ONNX/CoreML/quantization paths for Mac M1/M2.
---

# ML Model Comparison Report

Class-level umbrella for comparing pretrained ML models end-to-end. Triggered by any "compare A vs B for task Z" research request — especially when the user is at a model-selection fork for a production pipeline.

## When to load

- User says "research X so sánh với Y", "compare A and B", "nên chọn model nào", "đánh giá model"
- User says "phân tích toàn diện model X", "X có gì mới", "đọc hiểu model X" → still load this skill; treat the model family as the comparison axis
- User is building a pipeline (audio tagger, vision classifier, etc.) and needs to pick a backbone
- User mentions hardware constraints (M1/M2, CPU only, real-time, edge device)
- User asks for benchmarks, inference speed, or model size tradeoffs

## What to deliver

A markdown report saved to file (NOT just in-chat output) with these sections:

1. **Architecture overview** — table comparing model variants, layers, params, input shapes
2. **Benchmark numbers** — mAP / accuracy from original paper plus independent reproductions; be explicit which eval set
3. **Output format** — softmax vs sigmoid (multi-label); single-frame vs sliding window; frame-level vs clip-level
4. **Implementation repos and install** — GitHub URLs, PyPI packages, pretrained checkpoint locations
5. **Inference speed** — RTF (real-time factor), wall-clock for typical workload, with hardware breakdown (CPU / MPS / CoreML EP for Mac)
6. **Use-case mapping** — specific class indices, threshold recommendations, false-positive pitfalls for the target domain
7. **Decision matrix** — table with speed/quality/simplicity/dimensions, ending in "khi nào dùng cái nào"
8. **References** — numbered list with paper URLs plus repo URLs plus benchmark sources
9. **TL;DR** — 5-8 bullets maximum

## Workflow

### Step 1: Parallel research sprint (5-7 web searches fired together)

Do NOT serialize search calls. Fan out:

```
[arxiv paper for model X architecture]
[GitHub repo for X + pretrained checkpoints]
[tutorial OR inference example for X]
[paper OR blog comparing X vs Y directly]
[benchmark on target hardware (Apple Silicon / CPU / edge)]
[model Y original repo + class names]
[independent benchmark OR third-party comparison]
```

Cover 5+ sources minimum. Quoted mAP numbers must come from the original paper, not secondary summaries.

### Step 2: Verify class indices and labels from canonical files

Don't trust index numbers from summaries. Fetch the canonical label file directly. A class index mismatch silently breaks downstream threshold logic.

### Step 3: Hardware-specific inference gotchas

Always include these Mac M1/M2 warnings when relevant:

- **PyTorch MPS is often SLOWER than CPU** for non-CNN-shaped models (RNN, attention, custom ops); see pytorch issue #77799
- **ONNX Runtime plus CoreMLExecutionProvider** unlocks Apple Neural Engine (ANE) for CNN models
- **TFLite quantized** is fastest path for models with TFLite export (YAMNet, MobileNet) on Mac
- **Laptop thermal throttling**: on Raspberry Pi inference latency rises 25% after 8 min continuous run; mention this for edge-deploy scenarios

### Step 4: Domain mapping

For the target use case, list:

- Which class indices map to the positive signal (cheering, applause, etc.)
- Threshold recommendations per signal
- False-positive hazards (background music, ambient noise, irrelevant chatter)
- Multi-label consensus logic when >1 class must vote

### Step 5: Decision matrix and pipeline recommendation

End with a per-scenario table:

| Scenario | Recommendation | Why |
| Real-time / live stream | Model A (faster) | RTF << 0.1 |
| Offline batch, high quality | Model B (more accurate) | mAP gap |
| Production at scale | Hybrid: pre-filter + confirm | cost x10 reduction |

Plus 2-3 concrete pipeline snippets (Pipeline A, B, C) the user can drop in.

## Output conventions

- **Bilingual lead**: short Vietnamese section for narrative plus English table headers / code / metric names
- **Code snippets ready to copy**: bash install + Python inference for each candidate model
- **Save to file**: `/Users/tuananh4865/<topic>_research.md` or `~/...md` — never just paste in chat
- **Length target**: 6-15 KB markdown (deep enough to be a reference, short enough to actually read)

## Pitfalls

- **DO NOT trust paper-only mAP for production**: paper eval uses balanced subset, user data may differ wildly. Always include a "fine-tune on your data" callout
- **Softmax models lose multi-label info**: if 2+ positive classes co-occur (Cheering + Applause), softmax forces them to compete. Use sigmoid models (PANN, AST, BEATs) when multi-label is needed
- **Speed claims are hardware-dependent**: "real-time factor 0.05x" on RTX 3090 is meaningless on M1. Always give wall-clock plus CPU/GPU explicitly
- **Class index drift across libraries**: YAMNet has 521 classes, PANN has 527, both based on AudioSet but index assignments differ for the 6 dropped classes. Check class_name not [62] when comparing
- **Don't fabricate model numbers** if not in sources — say "not benchmarked in this session" rather than inventing
- **Reference quality matters more than count**: 10-15 high-quality cited sources beat 50 Wikipedia links

### Pitfall #N+1 — Official docs vs Hugging Face docs vs arXiv disagree on modality/variant support (codified 2026-07-22 from Gemma 4 case)

When researching any multimodal AI model (vision/audio/video support), the three canonical sources often disagree on WHICH VARIANT supports WHICH MODALITY:

- **Vendor official docs** (ai.google.dev, anthropic.com, openai.com) — usually most current on what was released
- **Hugging Face Transformers docs / model card** — usually lag behind, but tells you what the `transformers` library actually exposes today
- **arXiv technical report** — describes the trained model, frozen at paper publication date

**Real case (2026-07-22, Gemma 4 audio support):**
- Hugging Face Transformers v5.14.0 page: explicitly says **"Audio (E2B and E4B Only)"**.
- Google AI audio guide sample code lists `["gemma-4-E2B-it", "gemma-4-E4B-it", "gemma-4-12B-it"]` — includes 12B.
- Google model card: says "audio supported on E2B, E4B, and 12B models".

These don't agree. The correct move when the agent catches this:

1. **DO NOT pick silently** which side is "right" and report only that.
2. **Quote both sides verbatim** with their source URLs in the report.
3. **Tell the user which source to trust for which purpose** — "can I load it with `transformers.AutoProcessor` right now" → trust HF; "what did the vendor actually ship" → trust vendor docs.
4. **Recommend empirical check**: load the checkpoint and see if `processor.feature_extractor` accepts audio. Print the result.

This pitfall applies to every multimodal model released in the last 2 years (Gemma 3n, Gemma 4, Qwen2-Audio, Llama 3.2 Vision, Pixtral, etc.) because HF docs lag the model release by weeks-to-months. Always state the source date when quoting.

### Pitfall #N+2 — Single-model research is also in scope (not just "X vs Y")

Trigger phrases that should activate this skill even when there's no A-vs-B comparison:

- "phân tích toàn diện model X"
- "research model X capabilities"
- "X có gì mới"
- "đánh giá model X"
- "đọc hiểu model X"

In these cases, treat the model FAMILY itself as a 5-way comparison across its variants (E2B vs E4B vs 12B vs 26B-A4B vs 31B for Gemma 4). Same deliverable shape — architecture table, decision matrix, code snippets, deployment gotchas — but the comparison axis is "model size within the family" rather than "different model families".

## Verification before claiming done

1. File actually exists at `~/<topic>_research.md` (use ls -la or read_file to confirm)
2. File size > 5 KB
3. Every mAP number has a source URL
4. Decision matrix has at least 4 rows × 4 columns
5. At least 1 code snippet per model candidate
6. Vietnamese narrative plus English technical terms

## Reference files

- `references/audio-tagging-models-pann-vs-yamnet.md` — PANN vs YAMNet comparison (audio tagging case study)
- `references/gemma-4-multimodal-2026-07-22.md` — Gemma 4 condensed research notes (vision/audio/video/token budget/workflow recipe); full synthesis at `/Volumes/Storage-1/Hermes/wiki/concepts/gemma-4-toan-dien-2026-07-22.md`
- `references/gemma-4-e2b-mlx-test-methodology-2026-07-22.md` — Real MLX Apple Silicon test results for `mlx-community/gemma-4-e2b-it-4bit` (peak RAM 4.2-5.3 GB, speed 56-62 gen-tps), mlx-vlm CLI entry gotcha (`mlx_vlm.generate` binary ≠ `python -m mlx_vlm.generate`), `apply_chat_template(num_videos=1)` silent failure, video pre-flight recipe, ground-truth verification workflow with vision tool. Use this when next session asks to test any Gemma 4 variant locally on Mac.
