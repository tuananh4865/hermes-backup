---
title: "H.264"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [video, codec, compression, standard, multimedia]
---

# H.264 (AVC / MPEG-4 Part 10)

## Overview

H.264, formally known as Advanced Video Coding (AVC) and technically identical to MPEG-4 Part 10, is one of the most widely adopted video coding standards in the world. Developed jointly by ITU-T and MPEG (the same bodies behind JPEG and MPEG-1/2), H.264 was finalized in 2003 and has since become the dominant format for video recording, compression, streaming, and transmission. It powers Blu-ray discs, YouTube, Netflix, video conferencing (via H.264 SVC), telepresence, surveillance systems, and mobile video.

The standard achieves remarkable compression ratios—typically 3 to 10 times better than MPEG-2 for equivalent quality—by combining spatial prediction (within a frame), temporal prediction (between frames), transform coding, and entropy coding into an sophisticated hybrid codec. This compression efficiency made HD streaming practical at reasonable bandwidth and enabled mobile video when cellular networks were still early in their evolution.

## Key Concepts

**I-Frames (Intra-coded)** are complete images encoded independently, like a JPEG. They serve as reference points for other frames but contain the most data. I-frames are needed periodically to reset the decoding state and enable random access.

**P-Frames (Predicted)** encode only the differences from the preceding frame (I or P). They reference previously decoded frames to reconstruct the current frame, dramatically reducing data compared to I-frames when there is minor motion.

**B-Frames (Bi-predicted)** reference both preceding and subsequent frames to interpolate the current frame. This bidirectional prediction provides the best compression but requires more processing power and introduces latency, making B-frames unsuitable for real-time communication.

**Macroblocks** are 16x16 pixel grid units that form the basic processing unit in H.264. Each macroblock can be subdivided into smaller blocks (8x8, 4x4) for motion estimation. The encoder chooses the best subdivision per macroblock to balance quality and file size.

**CABAC (Context-Adaptive Binary Arithmetic Coding)** and **CAVLC (Context-Adaptive Variable Length Coding)** are the two entropy coding methods in H.264. CABAC provides ~10% better compression than CAVLC but is more computationally intensive, making it the default for most applications.

**Profiles** constrain which features a bitstream uses. Common profiles include:
- **Baseline**: Low complexity, for low-power devices (mobile, video conferencing)
- **Main**: Broadcast and storage applications
- **High**: Studio-quality compression with higher bit depths
- **Constrained Baseline**: Intersection of Baseline for interoperability

## How It Works

The H.264 encoding process follows a multi-step pipeline. First, the input video is partitioned into macroblocks. For each macroblock, the encoder searches reference frames for matching regions (motion estimation) and computes the residual (difference) between the predicted and actual pixels. This residual is transformed using a 4x4 or 8x8 DCT-like integer transform, quantized (dividing coefficients to reduce precision), and entropy-coded. Deblocking filtering is applied to reduce block artifacts, and the result is packed into a NAL unit for transmission or storage.

NAL (Network Abstraction Layer) units are the structural container format in H.264. Each NAL unit has a header indicating its type (SPS for sequence parameters, PPS for picture parameters, slice data for encoded video, etc.). This structure enables decoders to parse and skip parts of the bitstream gracefully—a feature used for adaptive streaming where quality layers can be dropped.

Decoding is the inverse: NAL units are parsed, entropy-coded coefficients are decoded, inverse quantization and inverse transform are applied, motion compensation reconstructs predicted blocks, and the deblocking filter smooths the result. The decoded frame is then stored as a reference for subsequent P and B frames.

## Practical Applications

- **Video Streaming**: H.264 is the dominant codec for streaming services, using adaptive bitrate streaming (HLS/DASH) to deliver the best quality for available bandwidth.
- **Video Conferencing**: Zoom, Skype, and WebRTC use H.264 (often SVC-annex G extension) for real-time communication. Hardware acceleration in CPUs and GPUs makes encoding efficient.
- **Broadcast Television**: ATSC, DVB, and digital cable all rely on H.264 for HD television transmission.
- **Blu-ray and Physical Media**: H.264 replaced MPEG-2 as the primary Blu-ray codec, enabling HD content on a disc at reasonable bitrates.
- **Mobile Video**: YouTube and social media video platforms default to H.264 for maximum device compatibility.
- **Surveillance**: IP cameras and NVR systems encode in H.264 to reduce storage and bandwidth requirements.

## Examples

Decoding a H.264 file with FFmpeg:

```bash
# Check codec info
ffprobe -v error -show_entries stream=codec_name,width,height,bit_rate -of default=noprint_wrappers=1 input.mp4

# Re-encode to a smaller file with CRF quality mode
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# Extract a specific time range
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy clip.mp4

# Hardware-accelerated encode on macOS
ffmpeg -i input.mp4 -c:v h264_videotoolbox -quality realtime -c:a aac output.mp4
```

## Related Concepts

- [[Video Codecs]] - The category H.264 belongs to
- [[FFmpeg]] - The Swiss-army tool for video processing
- [[WebRTC]] - Real-time communication that uses H.264
- [[MPEG]] - The moving picture experts group that co-developed H.264
- [[Compression]] - The underlying technology that makes H.264 valuable
- [[Self-Healing Wiki]] - The system that auto-created this page

## Further Reading

- [ITU-T H.264 Specification](https://www.itu.int/rec/T-REC-H.264) - The official standard
- [FFmpeg H.264 Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264) - Practical encoding guidance
- [H.264 Wikipedia](https://en.wikipedia.org/wiki/H.264/MPEG-4_AVC) - Accessible overview with profiles and levels

## Personal Notes

H.264 is a marvel of engineering that touches almost every aspect of modern digital life, yet few people know its name. Its combination of compression efficiency and hardware support (virtually every device made in the last 15 years has H.264 decode silicon) makes it the safest choice for any video application. That said, H.265/HEVC offers ~50% better compression for the same quality, and AV1 is emerging as a royalty-free alternative. For new greenfield projects, the codec choice depends heavily on licensing considerations and target device support.
