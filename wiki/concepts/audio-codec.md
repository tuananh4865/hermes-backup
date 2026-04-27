---
title: "Audio Codec"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [audio, codec, compression, encoding, decoding, mp3, aac, opus]
---

# Audio Codec

## Overview

An audio codec is an algorithm or hardware component that compresses and decompresses digital audio data. The term "codec" derives from "coder-decoder"—software or hardware that encodes audio into a compressed format for storage or transmission, then decodes it back to playable audio. Codecs are essential because raw PCM audio data consumes enormous bandwidth and storage; a single minute of CD-quality stereo audio (44.1kHz, 16-bit) requires approximately 10MB, making uncompressed audio impractical for streaming, mobile devices, and most storage scenarios.

Audio codecs achieve compression by exploiting properties of human hearing. The most common approach is perceptual coding, which removes or reduces audio information that is perceptually irrelevant—sounds the human ear cannot easily detect due to masking effects, frequency limitations, or temporal constraints. Lossy codecs like MP3, AAC, and Opus discard some audio information permanently, while lossless codecs like FLAC and ALAC preserve all original data. The choice between lossy and lossless involves trade-offs in quality, file size, and use case.

## Key Concepts

### Sampling Rate and Bit Depth

Digital audio represents sound as discrete samples taken at regular intervals. The sampling rate (measured in Hz) determines how many samples are captured per second—CD audio uses 44,100 Hz (44.1kHz), meaning more than 44 thousand samples per second per channel. Higher sampling rates capture higher frequencies; the Nyquist theorem states you need at least twice the highest frequency you want to capture. Common rates include 44.1kHz (CD), 48kHz (video standard), 96kHz, and 192kHz for high-resolution audio.

Bit depth (typically 16-bit or 24-bit for consumer audio) determines the precision of each sample. Higher bit depth provides greater dynamic range and lower quantization noise. A 16-bit sample can represent 65,536 possible amplitude values, while 24-bit offers over 16 million—far beyond what most listening conditions can exploit.

### Perceptual Coding and Masking

Human hearing has limitations that codecs exploit. Frequency masking occurs when a loud sound makes simultaneous quieter sounds in nearby frequencies inaudible. Temporal masking works similarly over time—a loud sound can mask immediately preceding or following quieter sounds. By analyzing audio in frequency bands and removing masked components, perceptual codecs achieve dramatic size reductions with minimal perceptible quality loss.

### Bitrate

Bitrate measures how much data per second the encoded audio consumes, typically expressed in kilobits per second (kbps). Higher bitrates generally mean better quality but larger files. Variable bitrate (VBR) encoding adjusts bitrate dynamically based on the complexity of the audio, allocating more bits to complex passages and fewer to simple ones. Constant bitrate (CBR) uses the same rate throughout, useful for streaming with fixed bandwidth constraints.

### Latency

Codec latency is the delay between audio input and output. This matters critically for real-time communication where conversation flow depends on minimal delay. Some codecs are designed for low latency—Opus can operate at 5-10ms latency for speech, while others may introduce 100ms or more. Low-latency codecs use shorter analysis windows, trading compression efficiency for responsiveness.

## How It Works

Most modern audio codecs work by transforming audio into a frequency-domain representation, manipulating that representation to remove perceptually irrelevant information, and then encoding the result efficiently.

The encoding process typically involves: windowing the input audio into overlapping frames, applying a time-to-frequency transform (often MDCT—Modified Discrete Cosine Transform), analyzing the resulting spectral data to determine perceptually optimal quantization, encoding quantized spectral data along with side information (gain, stereo coupling details), and packaging everything into a bitstream with appropriate framing and error correction.

Decoding reverses this: the bitstream is parsed, spectral data is decoded, inverse quantization is applied, the inverse transform produces time-domain samples, and overlapping-add reconstruction yields the output audio. Each step must be precisely synchronized with its corresponding encoder step to produce accurate output.

## Practical Applications

Audio codecs are everywhere in modern computing. Music streaming services (Spotify, Apple Music, Tidal) use codecs like Ogg Vorbis, AAC, or Opus to deliver music at manageable bandwidth. Video conferencing (Zoom, WebRTC) relies on low-latency speech codecs such as Opus or EVS. Video files embed audio tracks encoded with AAC (the standard for YouTube, broadcast TV, Blu-ray) or other codecs. Voice assistants and smart speakers use narrowband or wideband speech codecs optimized for voice reproduction. Game audio middleware often uses adaptive audio codecs to stream sound effects and music dynamically.

## Examples

MP3 (MPEG-1 Audio Layer III) remains the most recognizable audio codec despite being decades old. It uses perceptual coding with MDCT to achieve roughly 10:1 compression ratios at 128kbps, approaching CD quality for most listeners. While technically obsolete for new applications, MP3's universal compatibility means it persists in legacy hardware and archival contexts.

AAC (Advanced Audio Coding) succeeded MP3 as the successor standard, offering better quality at the same bitrate or similar quality at lower bitrates. It powers Apple's music ecosystem (iTunes, Apple Music), YouTube's primary audio codec, and broadcast standards. AAC-LC (Low Complexity) prioritizes decode simplicity, while HE-AAC and HE-AACv2 use bandwidth extension techniques for very low-bitrate applications.

Opus is a versatile codec standardized by the IETF, designed for both speech and general audio. It combines SILK (for speech) and CELT (for music) technologies, dynamically switching based on content. At 64kbps, Opus often exceeds MP3 quality at 128kbps. Its very low latency (as low as 5ms) makes it ideal for real-time communication, while higher bitrates excel for music streaming. WebRTC uses Opus as its primary audio codec.

```javascript
// Example: Basic audio context with Opus support (Web Audio API)
const audioContext = new AudioContext();

async function loadAndPlayAudio(url) {
  const response = await fetch(url);
  const arrayBuffer = await response.arrayBuffer();
  // The AudioContext will automatically decode using available codecs
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
  
  const source = audioContext.createBufferSource();
  source.buffer = audioBuffer;
  source.connect(audioContext.destination);
  source.start(0);
}

// MediaSource API example for streaming
const mediaSource = new MediaSource();
const sourceBuffer = mediaSource.addSourceBuffer('audio/webm; codecs=opus');
```

## Related Concepts

- [[MP3]] - Historical but still prevalent audio compression format
- [[AAC]] - Advanced Audio Coding, successor to MP3 and web video standard
- [[Opus]] - IETF standard codec for speech and general audio
- [[FLAC]] - Free Lossless Audio Codec, popular lossless format
- [[Compression Algorithms]] - General data compression theory applicable to audio
- [[Digital Signal Processing]] - Underlying signal processing fundamentals
- [[Web Audio API]] - Browser API for audio manipulation and codec access
- [[Media Source Extensions]] - Browser API for streaming encoded media

## Further Reading

- Mozilla's Web Audio API documentation - Practical codec usage in browsers
- Opus Codec RFC 6716 - The IETF specification for Opus
- Hydrogenaudio Knowledgebase - Deep technical resource on audio codecs and quality
- "Digital Audio Effects" by Udo Zölzer - Signal processing foundations for codec design
- ITUT Speech Coding Standards - Coverage of standardized speech codecs

## Personal Notes

The codec landscape has matured considerably— Opus represents an excellent general-purpose choice for most new applications, combining quality, latency, and versatility. The choice between lossy and lossless remains contextual: for casual listening and streaming, lossy codecs have reached transparency for most listeners at reasonable bitrates. For archival, production work, or critical listening, lossless formats like FLAC preserve full fidelity. One thing often overlooked is encoder quality—different implementations of the same codec can vary significantly in output quality, so using well-regarded encoders matters.
