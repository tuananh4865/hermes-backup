---
title: "Transcript Processing Guide"
confidence: high
last_verified: 2026-04-18
type: concept
tags: [transcripts, ai-pipeline, workflow]
related:
  - [[ai-agent-trends-2026-04-18]]
  - [[local-llm-agents]]
  - [[python-code-examples]]
sources:
  - Real Python (speech recognition)
  - Restack (AI pipelines)
---

# Transcript Processing Guide

## Overview

Transcript processing is the end-to-end pipeline for converting raw audio/video into structured, actionable text. This guide covers the full workflow from audio ingestion to cleaned, timestamped transcript ready for AI analysis.

## The Pipeline

```
Audio/Video Input
       │
       ▼
┌──────────────────┐
│  Audio Extraction │  (yt-dlp, ffmpeg)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Speech-to-Text  │  (Whisper, faster-whisper, WhisperX)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Diarization     │  (Who said what — optional)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Cleaning        │  Remove filler words, normalize
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Formatting      │  Timestamps, speaker labels, paragraphs
└────────┬─────────┘
         │
         ▼
  Structured Output
```

## Key Steps

### 1. Audio Extraction

For video sources (TikTok, YouTube), extract audio first:

```bash
# TikTok via yt-dlp
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"

# YouTube
yt-dlp -x -f bestaudio "URL"

# ffmpeg for local files
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3
```

### 2. Speech Recognition

**faster-whisper** is the recommended engine for local transcription:

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

**Key whisper model sizes:**
| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| base | ~74M | Very fast | Good |
| small | ~244M | Fast | Better |
| large-v3 | ~809M | Slow | Best |

### 3. Diarization (Who Spoke When)

Speaker diarization separates segments by speaker. Libraries:
- **pyannote.audio** — open-source, local
- **Rev AI** — API-based, high accuracy
- **AssemblyAI** — API with speaker labels

### 4. Cleaning & Normalization

Common cleaning steps:
- Remove filler words ("um", "uh", "like")
- Fix common ASR errors (homophones)
- Normalize whitespace and punctuation
- Convert timestamps to readable format

```python
import re

def clean_transcript(text: str) -> str:
    # Remove filler words
    text = re.sub(r'\b(um|uh|like)\b', '', text, flags=re.IGNORECASE)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
```

### 5. Formatting for AI Consumption

For LLM processing, structure as:

```markdown
# Video Title
**Source:** [URL]
**Duration:** X minutes
**Speakers:** Speaker A, Speaker B

## Transcript

**[00:01:23] Speaker A:**
[Transcript text here]

**[00:01:45] Speaker B:**
[Response text here]
```

## Vietnamese Transcript Processing

For Vietnamese content (TikTok, YouTube Vietnamese):

```python
# faster-whisper with Vietnamese language hint
segments, info = model.transcribe(
    "audio.mp3",
    language="vi",
    initial_prompt="Đây là nội dung tiếng Việt về công nghệ AI và lập trình."
)
```

Key Vietnamese-specific considerations:
- **Tone markers**: Not needed with modern Whisper
- **Vietnamese punctuation**: Follows standard rules
- **Proper noun handling**: May need custom dictionary

## Local LLM Analysis Pipeline

After transcription, use local LLM for analysis:

```python
# Example: Summarize transcript with local LLM
import subprocess

def summarize_with_local_llm(transcript: str, model: str = "qwen3-8b") -> str:
    prompt = f"""Bạn là một trợ lý AI phân tích nội dung video.
Hãy tóm tắt nội dung sau đây theo các điểm chính:

{transcript[:4000]}

Tóm tắt:"""
    
    result = subprocess.run(
        ["ollama", "generate", model, "-p", prompt],
        capture_output=True, text=True
    )
    return result.stdout
```

## Tools Reference

| Tool | Use Case | Platform |
|------|----------|----------|
| yt-dlp | Video/audio extraction | CLI |
| faster-whisper | STT transcription | Local GPU |
| whisperX | STT + alignment + diarization | Local |
| pyannote | Speaker diarization | Local |
| llama.cpp | Local LLM inference | Local CPU/GPU |
| Ollama | Local LLM management | Local |

## Related

- [[local-llm-agents]] — Running LLM agents locally
- [[python-code-examples]] — Code patterns for pipeline implementation
- [[vibe-coding]] — Using AI to build with transcripts
