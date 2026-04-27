---
title: "Whisper"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, speech-recognition, openai, audio, nlp]
---

# Whisper

## Overview

Whisper is an open-source automatic speech recognition (ASR) system developed by OpenAI, released in 2022. It is designed to transcribe speech to text in multiple languages and can also perform translation from various languages into English. Whisper is built on a Transformer-based encoder-decoder architecture and was trained on a diverse dataset of 680,000 hours of multilingual and multitask audio data, giving it remarkable robustness to accents, background noise, and technical terminology.

Unlike cloud-based speech recognition services that require internet connectivity and pose privacy concerns, Whisper can run locally on consumer hardware. This makes it attractive for applications requiring offline transcription, data sovereignty, or cost-effective processing of large audio volumes. The model is available in multiple sizes, from the tiny 39M parameter version to the large 1550M parameter variant, balancing speed and accuracy.

## Key Concepts

**Transformer Architecture**: Whisper uses a standard Transformer encoder-decoder model. The encoder processes log-mel spectrogram features extracted from audio, and the decoder generates text tokens autoregressively.

**Multilingual Training**: The model was trained on data spanning 99 languages, making it one of the most versatile open-source ASR systems. It handles code-switching (mixing languages) reasonably well.

**Task Types**: Whisper supports multiple tasks—transcription (speech to text), translation (to English), language identification, and voice activity detection.

**Timestamped Output**: The model can provide word-level or segment-level timestamps, enabling synchronization with audio for subtitling and video editing applications.

**Forced Decoding**: Allows specifying the output language or task to improve accuracy and consistency for known use cases.

## How It Works

1. **Audio Preprocessing**: Raw audio is converted to a log-mel spectrogram—a 2D representation of audio frequency content over time.

2. **Encoding**: The Transformer encoder processes the spectrogram, extracting hierarchical features and building a contextual representation.

3. **Decoding**: The decoder generates text autoregressively, starting with a special start-of-sequence token and conditioning on both the encoder output and previously generated tokens.

4. **Post-processing**: Special tokens indicate language, transcription vs. translation, and end of sentence. Timestamps are extracted from segment boundaries.

```text
Audio Input (WAV/MP3/FLAC)
    │
    ▼
Log-Mel Spectrogram Extraction
    │
    ▼
Transformer Encoder
    │
    ▼
Text Tokens ( autoregressive decoding)
    │
    ▼
Transcribed/Translated Text Output
```

## Practical Applications

- **Subtitle Generation**: Creating subtitles for videos, podcasts, and lectures automatically
- **Meeting Transcription**: Converting recorded meetings, calls, and interviews to searchable text
- **Voice Assistant Privacy**: Running speech recognition locally instead of sending audio to cloud services
- **Content Indexing**: Making audio content searchable for podcasts, YouTube videos, and audiobooks
- **Accessibility Tools**: Providing real-time captions for deaf and hard-of-hearing users

## Examples

Using the Whisper CLI for transcription:

```bash
whisper audio_recording.mp3 --model medium --language en --output_dir ./transcripts
```

Python usage with the Hugging Face Transformers library:

```python
from transformers import pipeline
import torch

# Load Whisper model
transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-medium",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

# Transcribe audio file
result = transcriber("meeting_recording.mp3")
print(result["text"])

# Force specific language and task
result = transcriber(
    "french_audio.mp3",
    language="french",
    task="translate"
)
print(result["text"])  # Outputs English translation
```

## Related Concepts

- [[Speech Recognition]] - The broader field of converting speech to text
- [[Transformer]] - Neural network architecture underlying Whisper
- [[OpenAI]] - Organization that developed Whisper
- [[Audio Processing]] - Manipulation and analysis of audio signals
- [[Natural Language Processing]] - Computational handling of human language

## Further Reading

- [Whisper Paper: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)
- [OpenAI Whisper GitHub Repository](https://github.com/openai/whisper)
- [Hugging Face Whisper Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/whisper)

## Personal Notes

Whisper changed the game for local speech recognition. I run the medium model on my desktop for meeting notes and it's surprisingly accurate even with technical jargon. The key is choosing the right model size—small models are fast but struggle with accents, while large models are accurate but need GPU acceleration. I also learned that providing language hints significantly improves results for non-English audio.
