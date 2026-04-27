---
title: "llama.cpp Metal Backend"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [llm, llama-cpp, apple-silicon, local-llm, inference, metal]
related:
  - [[local-llm-agents]]
  - [[mlx-apple-silicon]]
  - [[llama-cpp]]
---

# llama.cpp Metal Backend

## Overview

The Metal backend in llama.cpp enables GPU-accelerated inference on Apple Silicon chips (M1, M2, M3, M4) through Apple's Metal framework. This brings high-performance LLM inference to Mac hardware, leveraging the unified memory architecture for efficient processing of large language models without requiring cloud services.

Metal is Apple's low-level graphics and compute API, similar to Vulkan on other platforms. The llama.cpp Metal backend compiles quantized neural network layers as Metal shaders, executing matrix operations on the GPU with significantly higher throughput than CPU-only inference.

## Why Metal for Apple Silicon

### Unified Memory Architecture

Apple Silicon chips share memory between CPU and GPU (called the "unified memory" or "shared memory" architecture). This eliminates the primary bottleneck in traditional GPU computing—the PCIe bus connecting discrete GPUs to CPU memory.

For LLM inference, this means:
- **No memory copying**: Model weights stay in unified memory, accessible by both CPU and GPU
- **Lower latency**: Direct memory access without bus transfer overhead
- **Efficient small batches**: Individual token generation doesn't suffer from GPU batch inefficiency

### Performance Characteristics

On M-series chips, Metal backend typically delivers:
- **2-4x throughput** compared to CPU-only inference
- **20-40 tokens/second** for 7B parameter models on M4
- **30+ tokens/second** for quantized 7B models on M4 Pro/Max

The actual performance depends on:
- Model size (7B, 13B, 33B, 65B)
- Quantization level (FP16, Q8, Q6, Q5, Q4, Q3)
- Context length in use
- Specific chip model (M1 vs M4, standard vs Pro vs Max)

## Compilation

### Basic Metal Build

```bash
# Clone llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# Build with Metal support
mkdir build && cd build
cmake .. -DLLAMA_METAL=ON -DLLAMA_METAL_EMBED_LIBRARY=ON
cmake --build . --config Release
```

The `-DLLAMA_METAL_EMBED_LIBRARY=ON` flag embeds the Metal library shaders directly in the binary, eliminating runtime shader compilation.

### Build Options

| Option | Description |
|--------|-------------|
| `DLLAMA_METAL=ON` | Enable Metal support |
| `DLLAMA_METAL_EMBED_LIBRARY=ON` | Embed shaders in binary |
| `DLLAMA_METAL_JNI=ON` | Enable Metal for Android on M-series |
| `DLLAMA_METAL_V1=OFF` | Use newer Metal API version (default ON) |

### Verification

After building, verify Metal is available:

```bash
./llama-cli -m your-model.gguf --verbose 2>&1 | grep -i metal
# Should output: "Metal device: Apple M4 Pro"
```

## Model Preparation

### Quantization

Quantization reduces model size by using lower-precision weights. The standard workflow:

```bash
# Convert model to GGUF format
python3 convert.py models/your-model/

# Quantize to Q4_K_M (good balance of size/quality)
./llama-quantize models/your-model/ggml-model-f16.gguf models/your-model/ggml-model-q4_k_m.gguf Q4_K_M
```

### Recommended Quantizations

| Name | Size vs FP16 | Quality | Recommended Use |
|------|-------------|---------|-----------------|
| Q8_0 | ~50% | 99% of FP16 | Best quality, larger files |
| Q6_K | ~40% | ~97% of FP16 | Good balance |
| Q5_K_M | ~33% | ~95% of FP16 | Smaller files, minimal quality loss |
| Q4_K_M | ~27% | ~93% of FP16 | **Recommended default** |
| Q3_K_M | ~22% | ~90% of FP16 | For larger models on limited RAM |

### Model Sources

- **TheBloke** on Hugging Face: Pre-quantized GGUF models in all sizes
- **lmstudio-community** on Hugging Face: Optimized variants for LM Studio
- Official model pages: LLaMA, Mistral, Phi, Qwen in GGUF format

## Inference

### Basic CLI Usage

```bash
./llama-cli \
  -m models/llama-7b-q4_k_m.gguf \
  -p "### Instruction: Write a haiku about coding\n### Response:" \
  -n 100 \
  -t 8 \
  --m金属 1
```

Key flags:
- `-m`: Model path
- `-p`: Prompt (with optional chat template)
- `-n`: Number of tokens to generate
- `-t`: Thread count (set to CPU core count)
- `--m金属 1`: Enable Metal (use 0 for CPU-only)

### GPU Layer Configuration

For systems with large unified memory, increasing GPU layers can improve throughput:

```bash
./llama-cli -m models/llama-7b-q4_k_m.gguf -p "Your prompt" -n 50 -ngl 32
```

`-ngl 32` offloads 32 layers to GPU. Set to the number of layers in your model (7B = 32 layers, 13B = 40 layers, 33B = 60 layers).

### Memory Requirements

| Model Size | Layers | FP16 RAM | Q4_K_M RAM | Recommended GPU Layers |
|-----------|--------|----------|-----------|------------------------|
| 7B | 32 | ~14GB | ~4.5GB | 32 |
| 13B | 40 | ~26GB | ~8GB | 40 |
| 33B | 60 | ~66GB | ~20GB | 60 (M3 Max, M4 Max) |
| 65B | 80 | ~130GB | ~40GB | 80 (M3 Ultra, workstation) |

## Metal vs CPU Performance

### Token Generation Speed (tokens/second)

| Chip | Q4_K_M 7B | Q4_K_M 13B |
|------|-----------|------------|
| M1 | ~15-18 | ~8-10 |
| M2 | ~18-22 | ~10-12 |
| M3 | ~22-28 | ~12-16 |
| M4 | ~30-40 | ~16-22 |
| M4 Pro | ~35-45 | ~20-26 |
| M4 Max | ~40-55 | ~24-32 |

*Numbers are approximate; actual performance varies by model and context.*

### Memory Bandwidth

Apple Silicon M-series chips have exceptional memory bandwidth:

| Chip | Bandwidth |
|------|-----------|
| M4 | 100 GB/s |
| M4 Pro | 273 GB/s |
| M4 Max | 410 GB/s |
| M3 Ultra | 819 GB/s |

LLM inference is heavily bandwidth-bound, making Apple Silicon particularly well-suited for this workload despite having less raw compute than high-end NVIDIA GPUs.

## Integration with Local LLM Tools

### LM Studio

LM Studio provides a GUI wrapper around llama.cpp with Metal support:

- Model download and management
- Chat interface with customizable parameters
- Local API server compatible with OpenAI API
- Built-in Metal acceleration

### Ollama

Ollama uses llama.cpp internally for Apple Silicon Metal:

```bash
# Ollama auto-detects Metal
ollama run llama3
```

### Homebrew

For quick command-line access:

```bash
brew install llama.cpp
llama-cli -m model.gguf -p "prompt"
```

## Troubleshooting

### Metal Not Available

```bash
# Verify Metal device detection
./llama-cli --verbose 2>&1 | grep -E "(Metal|GPU)"
```

If no Metal device appears:
1. Verify macOS is 12.3+ (Metal required)
2. Check system preferences → Privacy & Security → Metal is not blocked
3. Try rebuilding with `-DLLAMA_METAL_EMBED_LIBRARY=ON`

### Out of Memory

Reduce GPU layers or use stronger quantization:

```bash
# Reduce GPU layers
./llama-cli -m model.gguf -ngl 16

# Or use Q3_K_M (smaller)
./llama-quantize model.gguf model-q3.gguf Q3_K_M
```

### Slow Inference

If Metal is enabled but slow:
- Increase `-ngl` to offload more layers
- Reduce context length (`-c` flag)
- Use a smaller or more quantized model
- Check for thermal throttling

## See Also

- [[local-llm-agents]] — Running agents on local models
- [[mlx-apple-silicon]] — Apple's official MLX framework
- [[llama-cpp]] — Core llama.cpp project
