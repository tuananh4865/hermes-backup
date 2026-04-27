---
title: "Text-to-Speech"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [text-to-speech, voice-synthesis, tts, audio]
confidence: medium
relationships:
  - 🔗 voice-agents
  - 🔗 audio
  - 🔗 speech-to-text
---

# Text-to-Speech

## Overview

Text-to-Speech (TTS) is the artificial generation of spoken language from text. Also known as voice synthesis, TTS systems convert textual input into audible speech output, enabling applications from screen readers and accessibility tools to voice assistants and audiobook narration.

Modern TTS systems range from concatenative synthesis (stringing together recorded phonemes) to neural network-based approaches that generate natural-sounding speech. State-of-the-art systems like ElevenLabs, OpenAI's API, and Apple's VoiceOver use deep learning to produce human-like voices with proper prosody, emphasis, and emotional inflection.

## Key Concepts

### Neural TTS Architecture

Modern neural TTS typically uses a two-stage pipeline:

1. **Neural Vocoder**: Converts spectrograms to waveforms
   - WaveNet-style architectures
   - HiFi-GAN for real-time synthesis
   - Diffusion-based vocoders

2. **Duration/Prosody Model**: Predicts timing and emphasis
   - FastSpeech 2: Parallel generation with duration prediction
   - Glow-TTS: Flow-based duration modeling
   - VITS: End-to-end unified model

### Streaming TTS

For real-time applications, streaming TTS generates audio in chunks:

```
Text → Tokenize → Model → Spectrogram chunks → Vocoder → Audio chunks
```

Target latency for interactive applications: <300ms from text to first audio.

### Voice Cloning

Zero-shot voice cloning enables synthesizing speech in any voice from a short audio sample:

- **Speaker encoding**: Extract voice characteristics from reference audio
- **Cross-lingual**: Clone voice while generating in different languages
- **Use cases**: Personalized assistants, content localization, accessibility

## Practical Applications

### OpenAI TTS API

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input="Kubernetes automates deployment, scaling, and management of containerized applications."
)

response.stream_to_file("output.mp3")
```

### Coqui TTS (Open Source)

For self-hosted, private TTS:

```python
from TTS.api import TTS

# Initialize with HiFi-GAN vocoder
tts = TTS(model_name="tts_models/en/ljspeech/hifigan_v2")

# Generate speech
tts.tts(
    text="Hello, this is text to speech synthesis.",
    file_path="output.wav"
)
```

### ElevenLabs API

Commercial API with high-quality voices:

```python
import requests

response = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSAxNIp",
    headers={
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "YOUR_API_KEY"
    },
    json={
        "text": "Welcome to the future of voice synthesis.",
        "model_id": "eleven_monolingual_v1"
    }
)
```

## Voice Characteristics

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| Speaking rate | Words per minute | 100-200 WPM |
| Pitch | Voice fundamental frequency | 100-200 Hz |
| Volume | Loudness level | 0-100% |
| Pause | Inter-word and sentence breaks | 100-500ms |

## Related

- [[voice-agents]] — Voice AI system architecture
- [[text-to-speech]] — Audio processing and codecs
- [[speech-to-text]] — Speech recognition (inverse process)
