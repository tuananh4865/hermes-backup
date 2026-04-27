---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 whisper (extracted)
  - 🔗 local-model-transcription (extracted)
  - 🔗 knowledge-extraction (inferred)
last_updated: 2026-04-11
tags:
  - transcription
  - voice
  - conversations
  - processing
---

# Transcript System

> Systems for capturing, processing, and analyzing conversations and voice content.

## Overview

Transcript systems convert spoken content into written text for analysis, storage, and reference. Key applications:
- Meeting notes
- Interview recordings
- Voice memos
- Podcast transcription
- Conversation analysis

## Pipeline

```
Audio Input → Transcription → Processing → Storage → Analysis
     │              │              │           │         │
  Microphone    Whisper/        Segment     Search    Insights
  File upload   API           Clean up     Index     Summarize
```

## Transcription Tools

### Whisper (OpenAI)
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")

print(result["text"])
```

### Local Transcription
```python
from faster_whisper import FasterWhisper

model = FasterWhisper("medium")
segments, _ = model.transcribe("audio.mp3")

for segment in segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

### With Timestamps
```python
result = model.transcribe(
    "audio.mp3",
    word_timestamps=True,
    condition_on_previous_text=True
)

for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']}: {word['start']:.2f}s")
```

## Processing Pipeline

### 1. Segment by Speaker
```python
def segment_by_speaker(transcript, speaker_boundaries):
    """Split transcript into speaker segments."""
    segments = []
    current_pos = 0
    
    for boundary in speaker_boundaries:
        text = transcript[current_pos:boundary]
        segments.append({"speaker": boundary["speaker"], "text": text})
        current_pos = boundary
    
    return segments
```

### 2. Clean Up
```python
import re

def clean_transcript(text):
    # Remove filler words
    text = re.sub(r'\b(um|uh|ah|like)\b', '', text)
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)
    # Capitalize sentences
    text = '. '.join(s.capitalize() for s in text.split('.'))
    return text
```

### 3. Extract Key Information
```python
def extract_insights(transcript):
    """Extract key points from transcript."""
    prompt = f"""Extract key insights from this transcript:
    
    {transcript}
    
    Format as:
    - Main topics discussed
    - Key decisions made
    - Action items
    - Questions raised
    """
    return call_llm(prompt)
```

## Storage Format

### JSON with Timestamps
```json
{
  "id": "conv_001",
  "date": "2026-04-11",
  "duration": 3600,
  "speakers": ["Anh", "Em"],
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "speaker": "Anh",
      "text": "Hôm nay chúng ta bàn về wiki quality."
    }
  ]
}
```

### Markdown Format
```markdown
# Conversation: 2026-04-11

## Speakers
- Anh (Tuấn Anh)
- Em (Hermes Agent)

## Transcript

**Anh:** Hôm nay chúng ta bàn về gì?

**Em:** Chúng ta sẽ nâng cấp wiki quality.

---

## Action Items
- [ ] Expand Batch 3 stubs
- [ ] Fix orphan links
```

## Analysis

### Topic Detection
```python
def detect_topics(transcript, topics):
    """Check which predefined topics appear in transcript."""
    found = []
    for topic in topics:
        if topic.lower() in transcript.lower():
            found.append(topic)
    return found
```

### Sentiment Analysis
```python
def analyze_sentiment(transcript):
    """Analyze overall sentiment of conversation."""
    result = llm.predict(f"""
    Analyze the sentiment of this conversation:
    
    {transcript[:2000]}
    
    Return:
    - Overall sentiment: positive/neutral/negative
    - Key emotional moments
    - Tone assessment
    """)
    return result
```

### Action Item Extraction
```python
def extract_actions(transcript):
    """Find action items in transcript."""
    result = llm.predict(f"""
    Extract all action items from this transcript.
    Format as a list:
    
    {transcript}
    
    Format:
    - [ ] Action description (who: if mentioned)
    """)
    return result
```

## Integration with Wiki

Our transcript processing:
```python
async def process_transcript(audio_path):
    # 1. Transcribe
    transcript = await transcribe(audio_path, service="whisper")
    
    # 2. Process
    cleaned = clean_transcript(transcript["text"])
    insights = extract_insights(cleaned)
    actions = extract_actions(cleaned)
    
    # 3. Save to wiki
    save_to_wiki(transcript, insights, actions)
    
    # 4. Update index
    index_transcript(transcript)
    
    return {"transcript": cleaned, "insights": insights, "actions": actions}
```

## Related Concepts

- [[whisper]] — OpenAI Whisper transcription
- [[local-model-transcription]] — Local transcription setup
- [[knowledge-extraction]] — Extracting knowledge from content
- [[conversations]] — Conversation patterns

## External Resources

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [WhisperX](https://github.com/m-bain/whisperX) — With word timestamps