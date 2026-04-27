---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[text-to-speech]]
  - [[speech-to-text]]
relationship_count: 3
---

# Voice Agents

> AI agents that interact with users through spoken language — combining speech recognition, conversation, and voice synthesis.

## Overview

A **voice agent** is an AI system that conducts conversations via spoken language. Unlike text-based chatbots, voice agents must handle the complexities of speech:

- **Speech recognition** (STT): Convert spoken words to text
- **Natural language understanding**: Understand intent from transcribed text
- **Conversation management**: Maintain context across turns
- **Voice synthesis** (TTS): Generate natural spoken responses

## Architecture

### Voice Agent Pipeline

```
┌──────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│  User    │───►│   STT   │───►│   LLM    │───►│   TTS   │───►│  User    │
│  speaks  │    │ (Speech │    │(Dialogue │    │ (Voice  │    │ hears    │
│          │    │to text) │    │ Engine)  │    │ Synth)  │    │ response │
└──────────┘    └─────────┘    └──────────┘    └─────────┘    └──────────┘
```

### Key Components

| Component | Purpose | Technologies |
|-----------|---------|--------------|
| **STT** | Speech → Text | Whisper, Google Speech-to-Text, Azure Speech |
| **NLU** | Intent detection | LLMs with function calling |
| **Dialogue Engine** | Context management | Turn tracking, memory |
| **TTS** | Text → Speech | ElevenLabs, OpenAI TTS, Coqui |
| **Audio Pipeline** | Stream management | WebRTC, audio buffering |

## Implementation Patterns

### Simple Voice Agent

```python
import asyncio
from openai import OpenAI

class VoiceAgent:
    def __init__(self):
        self.stt = WhisperSTT()
        self.tts = ElevenLabsTTS()
        self.llm = OpenAI()
    
    async def run(self, audio_stream):
        # 1. Speech to text
        user_input = await self.stt.transcribe(audio_stream)
        
        # 2. LLM conversation
        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )
        
        # 3. Text to speech
        audio_response = await self.tts.synthesize(response.content)
        
        return audio_response
```

### Streaming Voice Agent

For low-latency voice interaction, use streaming:

```python
async def streaming_voice_agent(audio_queue, response_queue):
    """Streaming voice agent for real-time interaction."""
    
    # Start STT streaming
    stt_stream = whisper_streaming.create_stream()
    
    async def audio_to_text():
        async for chunk in audio_queue:
            # Feed audio chunks to STT
            result = await stt_stream.process(chunk)
            if result.complete:
                yield result.text
    
    async def text_to_voice():
        async for text in audio_to_text():
            # Get LLM response
            response = await llm.generate StreamingResponse(text)
            
            # Stream TTS response
            async for audio_chunk in tts.stream(response):
                await response_queue.put(audio_chunk)
    
    await text_to_voice()
```

## Key Technologies

### Speech Recognition (STT)

| Provider | Model | Strengths |
|----------|-------|-----------|
| **OpenAI** | Whisper | Open-source, multilingual |
| **Google** | Cloud Speech-to-Text | High accuracy, streaming |
| **Microsoft** | Azure Speech | Real-time, diarization |
| **AssemblyAI** | AssemblyAI | Speaker separation |

### Voice Synthesis (TTS)

| Provider | Strengths |
|----------|-----------|
| **ElevenLabs** | Natural voices, emotional range |
| **OpenAI** | TTS API, high quality |
| **Coqui** | Open-source TTS |
| **Google** | WaveNet voices |

## Voice-Specific Considerations

### Latency

Voice conversation requires low latency:
- STT processing: 100-500ms per utterance
- LLM generation: 500ms-2s per response
- TTS synthesis: 100-300ms

**Target total latency: < 1 second for natural feel**

### Turn-Taking

Voice agents must handle:
- **Interruption**: User cuts off the agent mid-sentence
- **Barge-in**: User starts talking while agent is speaking
- **Backchannel**: "uh-huh", "yeah" acknowledgment

```python
async def handle_turn_taking(audio_stream, is_speaking):
    """Detect if user is trying to interrupt."""
    
    while is_speaking:
        # Monitor for user speech
        audio_level = await audio_stream.get_volume()
        
        if audio_level > INTERRUPT_THRESHOLD:
            # User is speaking — stop agent output
            is_speaking.set(False)
            return "interrupted"
        
        await asyncio.sleep(0.05)
    
    return "completed"
```

### Noise Handling

Microphone input often contains:
- Background noise
- Echo from TTS playback
- Multiple speakers

Solutions:
- Noise cancellation (WebRTC AEC)
- Speaker separation/diarization
- Wake word detection before processing

## Real-Time Communication

### WebRTC for Voice Agents

```javascript
// Browser-side WebRTC setup for voice
const pc = new RTCPeerConnection({
  iceServers: [{ urls: 'stun:stun.example.org' }]
});

// Connect microphone
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    stream.getTracks().forEach(track => pc.addTrack(track, stream));
  });

// Handle incoming audio (from TTS)
pc.ontrack = (event) => {
  audioElement.srcObject = event.streams[0];
  audioElement.play();
};
```

### Architecture for Production

```
┌─────────────────────────────────────────────────────────┐
│                    Media Server                         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐     │
│  │  WebRTC   │───►│  Audio    │───►│  Mix      │     │
│  │  Gateway  │    │  Buffer   │    │  Engine   │     │
│  └───────────┘    └───────────┘    └───────────┘     │
└─────────────────────────────────────────────────────────┘
              │                    │
              ▼                    ▼
┌───────────────────┐    ┌───────────────────┐
│  Voice Agent      │    │  Voice Agent      │
│  Instance 1       │    │  Instance 2       │
└───────────────────┘    └───────────────────┘
```

## Use Cases

| Use Case | Description | Example |
|----------|-------------|---------|
| **Customer support** | Handle calls, answer questions | Voice support bot |
| **Personal assistant** | Task execution via voice | "Schedule a meeting" |
| **Accessibility** | Voice interface for apps | Screen reader alternative |
| **Voice commerce** | Orders via voice | "Order more paper towels" |
| **Healthcare** | Patient intake, symptom check | Medical voice triage |

## Related Concepts

- [[text-to-speech]] — Text-to-speech synthesis
- [[speech-to-text]] — Speech-to-text recognition

## References

- [OpenAI Whisper](https://github.com/openai/whisper)
- [ElevenLabs API](https://elevenlabs.io/docs/api-reference/)
- [WebRTC Voice](https://webrtc.org/)
