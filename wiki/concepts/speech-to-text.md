---
title: "Speech-to-Text"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [speech-recognition, whisper, audio, transcription, stt]
confidence: medium
relationships:
  - 🔗 whisper
  - 🔗 voice-agents
  - 🔗 audio
---

# Speech-to-Text

## Overview

Speech-to-Text (STT) is the automated transcription of spoken language into written text. Also known as automatic speech recognition (ASR), STT systems convert audio waveforms into textual representations, enabling voice-controlled interfaces, transcription services, and accessibility tools.

Modern STT systems are powered by deep neural networks, with transformer-based architectures achieving near-human transcription accuracy in many conditions. Key players include OpenAI's Whisper for general-purpose transcription, Google Speech-to-Text for cloud APIs, and Whisper.cpp for efficient local inference.

## Key Concepts

### Whisper Architecture

OpenAI's Whisper is an encoder-decoder transformer trained on 680,000 hours of multilingual audio:

- **Encoder**: Processes raw mel-spectrogram features from audio
- **Decoder**: Generates text tokens autoregressively
- **Multilingual**: Supports 100+ languages including Vietnamese
- **Variants**: tiny (39M), base (74M), small (244M), medium (769M), large (1550M parameters)

### Audio Preprocessing

Before transcription, audio is typically transformed:

1. **Sampling**: Convert analog audio to digital (typically 16kHz for STT)
2. **Mel-Spectrogram**: Convert waveform to frequency-time representation
3. **Normalization**: Volume normalization, voice activity detection

```python
# Example: Using faster-whisper
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "audio.wav",
    language="vi",  # Vietnamese
    beam_size=5,
    vad_filter=True  # Voice activity detection
)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

### Streaming vs Batch Processing

**Batch processing**: Transcribe entire audio files, higher accuracy, no real-time requirement. Best for transcription services, podcast processing.

**Streaming**: Real-time transcription with partial results, latency-critical. Best for live captions, voice agents, accessibility tools.

## Practical Applications

### Local STT with faster-whisper

For private, offline transcription:

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

# Run on CPU with INT8 quantization
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# Transcribe with word-level timestamps
segments, words = model.transcribe(
    "meeting.wav",
    word_timestamps=True
)

for segment in segments:
    print(segment.text)
```

### Voice Agent Integration

Voice agents use STT as the first stage of a pipeline:

```
Microphone → VAD → STT → LLM → TTS → Speaker
```

The STT output flows into an LLM for intent recognition, enabling conversational AI interfaces.

### Streaming with websockets

For real-time applications:

```python
# Server-side streaming transcription
async def stream_transcribe(audio_stream):
    model = WhisperModel("base")
    
    # Process audio chunks as they arrive
    for chunk in audio_stream:
        result, _ = model.transcribe(
            chunk,
            language="en",
            task="transcribe"
        )
        yield result.text
```

## Whisper Model Sizes

| Model | Parameters | English-only | Required RAM |
|-------|------------|--------------|--------------|
| tiny | 39M | ~1GB | ~1GB |
| base | 74M | ~1GB | ~1GB |
| small | 244M | ~2GB | ~2GB |
| medium | 769M | ~5GB | ~5GB |
| large | 1550M | ~10GB | ~10GB |

For local inference on Apple Silicon with MLX, quantized versions enable running large model on limited RAM.

## Related

- [[whisper]] — OpenAI's Whisper implementation
- [[voice-agents]] — Voice AI systems architecture
- [[speech-to-text]] — Audio processing fundamentals
