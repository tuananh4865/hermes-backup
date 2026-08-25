# 01 — Python API Surface

Generated từ `omnivoice/models/omnivoice.py` (1727 LOC). Verified v0.2.1.

---

## Top-level imports

```python
from omnivoice import (
    OmniVoice,                  # Main model class
    OmniVoiceConfig,            # PretrainedConfig subclass
    OmniVoiceGenerationConfig,  # Generation params dataclass
    VoiceClonePrompt,           # Reusable voice prompt
)
```

---

## Class: `OmniVoice`

### Constructor

```python
OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",          # HF repo or local path
    device_map="mps",            # "cuda:0" | "mps" | "xpu" | "cpu"
    dtype=torch.float16,         # or torch.float32
    load_asr=False,              # True = auto-load Whisper for ref_text
    asr_model_name=None,         # Default: "openai/whisper-large-v3-turbo"
    asr_device=None,             # Default: same as main model
    train=False,                 # True for training mode (skips tokenizer)
)
```

### Method: `model.generate()`

```python
audio = model.generate(
    text="...",                    # str or List[str]
    language="vi",                 # ISO 639-3 code or name (600+ supported)
    ref_audio="ref.wav",           # path or List[str] for batch
    ref_text="...",                # transcript of ref_audio
    voice_clone_prompt=prompt,     # OR pass pre-saved prompt (skip encode!)
    instruct="female, british",    # voice design (no ref needed)
    duration=10.0,                 # fixed seconds (overrides speed)
    speed=1.0,                     # >1 faster, <1 slower
    num_step=32,                   # diffusion steps (16 for faster)
    guidance_scale=2.0,
    t_shift=0.1,
    denoise=True,
    preprocess_prompt=True,
    postprocess_output=True,
    layer_penalty_factor=5.0,
    position_temperature=5.0,
    class_temperature=0.0,
    pad_duration=0.1,
    fade_duration=0.1,
    audio_chunk_duration=15.0,
    audio_chunk_threshold=30.0,
    normalize_text=False,          # zh/en numbers via WeTextProcessing
)
# Returns: List[np.ndarray], shape (T,), sampling_rate = 24000
```

**3 modes auto-detect:**
- `ref_audio` provided → **Voice Cloning**
- `instruct` provided (no ref) → **Voice Design**
- Neither → **Auto Voice** (random)

### Method: `model.create_voice_clone_prompt()`

```python
prompt = model.create_voice_clone_prompt(
    ref_audio="ref.wav",
    ref_text="...",                # NGẮN: 1 câu ~100 chars
    preprocess_prompt=True,        # default
)
# Returns: VoiceClonePrompt
# Side effects: ref_text auto-uppercase first letter, add punctuation
```

---

## Class: `VoiceClonePrompt`

```python
@dataclass
class VoiceClonePrompt:
    ref_audio_tokens: torch.Tensor   # (C, T) = (8, ~200)
    ref_text: str
    ref_rms: float

    def save(self, path: str) -> None:
        """torch.save với weights_only=True (torch 2.6+)"""
        # Lưu CPU, load được mọi device

    @classmethod
    def load(cls, path: str, map_location: str = "cpu") -> "VoiceClonePrompt":
        """Load .pt file"""
        # Validate format_version == 1, raise nếu mismatch
```

**File format version: 1** (hard-coded in source)

**Disk size:** ~10-15KB per prompt

---

## Class: `OmniVoiceGenerationConfig`

```python
@dataclass
class OmniVoiceGenerationConfig:
    # Decoding
    num_step: int = 32
    guidance_scale: float = 2.0
    t_shift: float = 0.1
    denoise: bool = True

    # Sampling
    position_temperature: float = 5.0
    class_temperature: float = 0.0
    layer_penalty_factor: float = 5.0

    # Pre/Post
    preprocess_prompt: bool = True
    postprocess_output: bool = True
    pad_duration: float = 0.1
    fade_duration: float = 0.1

    # Long-form chunking
    audio_chunk_duration: float = 15.0
    audio_chunk_threshold: float = 30.0
```

---

## Class: `OmniVoiceConfig` (PretrainedConfig)

```python
@dataclass
class OmniVoiceConfig:
    model_type = "omnivoice"
    audio_vocab_size: int = 1025      # 1024 tokens + 1 mask
    audio_mask_id: int = 1024
    num_audio_codebook: int = 8
    audio_codebook_weights: list = [8, 8, 6, 6, 4, 4, 2, 2]  # default
    llm_config: dict | PretrainedConfig  # Qwen3 backbone
```

**8 codebooks, mỗi 1025 vocab → 8200 unique audio tokens**

---

## Internal classes (for advanced use)

```python
@dataclass
class GenerationTask:
    batch_size: int
    texts: List[str]
    target_lens: List[int]
    langs: List[Optional[str]]
    instructs: List[Optional[str]]
    ref_texts: List[Optional[str]]
    ref_audio_tokens: List[Optional[torch.Tensor]]
    ref_rms: List[Optional[float]]
    speed: Optional[List[float]] = None

    def get_indices(config, frame_rate) -> (short_idx, long_idx):
        # Split by audio_chunk_threshold for chunked generation

    def slice_task(indices) -> GenerationTask:
        # Sub-batch for chunked processing

@dataclass
class OmniVoiceModelOutput(ModelOutput):
    loss: Optional[torch.Tensor] = None
    logits: Optional[torch.Tensor] = None
```

---

## ASR support (optional)

```python
model.load_asr_model(
    model_name=None,      # Default: "openai/whisper-large-v3-turbo"
    device=None,           # Default: same as main model
)
# After this, can omit ref_text → auto-transcribe ref_audio

text = model.transcribe(("waveform_array", 24000))
# or
text = model.transcribe("path/to/audio.wav")
# Returns: str (transcript)
```

**Note:** `from_pretrained(load_asr=True)` loads ASR at startup (slower init).

---

## Method: `model.transcribe()`

```python
@torch.inference_mode()
def transcribe(self, audio: Union[str, tuple]) -> str:
    """
    Args:
        audio: File path OR (waveform, sample_rate) tuple
               Waveform = np.ndarray or torch.Tensor, shape (1, T) or (T,)
    Returns:
        Transcribed text (stripped)
    Raises:
        RuntimeError if ASR model not loaded
    """
```

---

## Architecture deep-dive (for nerds)

**Backbone:** Qwen3 LLM (8B params, from config)
**Audio codec:** HiggsAudioV2TokenizerModel (8 codebooks, 24kHz)
**Generation method:** Iterative unmasked diffusion (num_step rounds)
**Audio format:** 24kHz mono PCM (s16le)

**Token vocabulary:**
- 1024 audio tokens (0-1023) per codebook
- 1 mask token (1024) per codebook
- 8 codebooks × 1025 tokens = 8200 total audio token space

**Diffusion process:**
1. Start with all-mask tokens
2. Each step: predict top-k tokens, replace masks
3. After num_step steps: all tokens decided
4. Decode to audio via HiggsAudioV2 tokenizer
