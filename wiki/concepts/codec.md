---
title: Codec
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [codec, video, audio, compression]
---

## Overview

A codec, short for coder-decoder, is a technology that compresses and decompresses digital media files, enabling efficient storage and transmission of audio and video content. The codec consists of two primary components: an encoder that takes raw media data and compresses it into a smaller format, and a decoder that reverses this process to reconstruct the original media for playback. This compression is essential because uncompressed media produces extremely large file sizes that would be impractical for storage and impossible to stream over networks with limited bandwidth.

Codecs work by exploiting redundancies in media data. Video codecs identify spatial redundancies within individual frames and temporal redundancies between consecutive frames, while audio codecs remove acoustic information that is imperceptible to human perception. The goal is to achieve the highest possible compression ratio while maintaining acceptable visual and auditory quality. Different codecs use varying mathematical algorithms and techniques to achieve this balance, resulting in significant differences in compression efficiency, computational complexity, and compatibility.

The choice of codec affects everything from the file size of a stored movie to the quality of a live video call. Codecs are fundamental to modern digital media infrastructure, powering streaming services, video conferencing, digital television, and mobile applications. Without codecs, distributing high-quality media over the internet would be prohibitively expensive in terms of bandwidth and storage costs.

## Video Codecs

Video codecs compress moving images by analyzing and encoding the differences between frames, rather than storing every single frame independently. Modern video codecs use block-based motion estimation and prediction techniques to achieve efficient compression.

**H.264 (AVC)** is the most widely adopted video codec in history, standardized by the ITU-T and MPEG. It provides excellent compression efficiency and broad compatibility across devices, browsers, and platforms. H.264 powers everything from Blu-ray discs and YouTube videos to Zoom calls and surveillance systems. Despite being over fifteen years old, it remains the default choice for many applications due to its mature ecosystem and hardware acceleration support in nearly all devices.

**VP9** is an open-source video codec developed by Google as a successor to VP8. It offers approximately 50% better compression efficiency than VP8 and competes directly with H.264 in quality-per-bit ratio. VP9 is particularly prominent on platforms like YouTube, where it serves as the primary codec for streaming. Its royalty-free licensing model makes it attractive for services seeking to avoid patent-related costs.

**AV1** represents the newest generation of video codecs, developed by the Alliance for Open Media (which includes Google, Amazon, Netflix, Apple, and others). AV1 provides 30-50% better compression efficiency than H.264 and is designed as a truly royalty-free format with no licensing fees. While encoding complexity was initially a barrier, hardware support for AV1 is rapidly expanding across devices and browsers. AV1 is increasingly becoming the codec of choice for next-generation streaming services and is expected to eventually replace H.264 as the dominant standard.

## Audio Codecs

Audio codecs compress sound data by removing information that falls outside the range of human hearing and exploiting patterns in audio signals. They are essential for digital music distribution, voice communication, and streaming.

**MP3** (MPEG-1 Audio Layer III) revolutionized digital audio when it emerged in the 1990s. It achieved dramatic file size reductions—typically 10:1 compared to CD audio—while retaining perceptually acceptable quality. MP3 became the de facto standard for digital music sharing and remains widely supported today, though it has been superseded by more efficient codecs in professional and streaming contexts.

**AAC (Advanced Audio Coding)** is the successor to MP3 and provides better quality at similar bitrates. AAC is the default audio format for YouTube, iTunes, and many streaming services. It supports multiple audio channels and advanced features like parametric stereo, making it suitable for everything from spoken word to high-fidelity music. Apple's adoption of AAC for the iTunes Store cemented its position as a major standard in digital audio.

**Opus** is a relatively recent codec developed by the Xiph.org Foundation and standardized by the IETF. It excels at both speech and music compression, using a flexible architecture that switches between different coding modes based on input type. Opus is particularly favored for real-time communication applications like VoIP calls, video conferencing, and gaming chat due to its low latency and excellent quality at moderate bitrates. It also powers much of the WebRTC ecosystem and is the default codec for many streaming platforms.

## Related

- [[Compression]] - The general technique of reducing data size that underlies all codecs
- [[H.264]] - The most widely deployed video codec standard
- [[AV1]] - The newest open and royalty-free video codec
- [[MP3]] - The pioneering digital audio codec that enabled music sharing
- [[Opus]] - The versatile audio codec designed for real-time communication
- [[Streaming]] - Media delivery that depends heavily on codec efficiency
- [[Digital Television]] - Broadcasting standard that relies on video codecs like H.264
