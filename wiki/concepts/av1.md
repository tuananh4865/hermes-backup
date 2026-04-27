---
title: "Av1"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [video-codec, compression, open-source, video-streaming]
---

# AV1 (AOMedia Video 1)

## Overview

AV1 is an open-source, royalty-free video coding format designed for video transmissions over the Internet. It was developed by the Alliance for Open Media (AOMedia), a consortium including Google, Amazon, Netflix, Apple, Microsoft, Meta, and other major technology companies. AV1 succeeded VP9 as the next-generation open video codec and was officially finalized in 2018 as version 1.0.0 of the specification.

The primary goal of AV1 is to provide significantly better compression efficiency than existing formats like H.264/AVC, H.265/HEVC, and VP9, enabling higher quality video at lower bitrates. This directly benefits streaming services, video conferencing platforms, and any application where bandwidth costs and video quality matter. AV1 adoption has accelerated as hardware decoder support has become widespread in consumer devices.

## Key Concepts

### Compression Efficiency

AV1 achieves its efficiency gains through several advanced techniques:

- **Extended Transform Sizes**: Supports transforms from 4x4 to 64x64, allowing better adaptation to different video content
- **Warped Motion Compensation**: Uses learned rather than explicit motion models for smoother motion estimation
- **Advanced Intra Prediction**: 56 directional intra prediction modes (vs. 8 in VP9) for better prediction of spatial redundancy
- **Loop Filtering**: More sophisticated deblocking and constraint filtering that preserves detail while removing artifacts

### Bitstream Structure

AV1 organizes video data hierarchically:

- **Sequence Header**: Global parameters for the entire video
- **Temporal Units**: Complete frames for a given time instant
- **Frame Headers**: Per-frame metadata and coding decisions
- **Tile Groups**: Independently decodable portions enabling parallel processing

### Profiles and Levels

AV1 defines three profiles (Main, High, Professional) that indicate feature support, and levels that specify maximum resolution and bitrate capabilities. Streaming services typically target Main profile at various levels depending on desired maximum resolution.

## How It Works

AV1 uses a hybrid block-based codec architecture similar to its predecessors but with enhanced prediction and transform mechanisms:

1. **Partitioning**: Each frame is split into superblocks (128x128 in the largest case) that can be recursively partitioned
2. **Prediction**: Inter prediction (motion compensation from previous frames) or intra prediction (prediction from neighboring blocks)
3. **Transform**: Predicted residual is transformed using DCT or ADST into frequency domain
4. **Quantization**: Coefficients are quantized to reduce precision
5. **Entropy Coding**: CABAC-style encoding compresses symbols based on context
6. **Loop Filtering**: Reconstructed frame is filtered before being stored as reference

```bash
# Example: Encoding a video with FFmpeg using AV1 (libaom-av1)
ffmpeg -i input.mov -c:v libaom-av1 -crf 30 -cpu-used 4 \
    -pix_fmt yuv420p output.webm

# Key parameters:
# -crf 30: Quality target (lower = better quality, 0-63 range)
# -cpu-used 4: Speed/quality tradeoff (0=best quality, 8=fastest)
```

## Practical Applications

AV1 is rapidly becoming the preferred format for:

- **Video Streaming**: YouTube, Netflix, Amazon Prime Video all serve AV1 to supported devices
- **Video Conferencing**: WebRTC is adding AV1 support for better low-bitrate quality
- **User-Generated Content**: Platforms encoding uploads to AV1 for storage efficiency
- **Broadcast**: ATSC 3.0 standard includes AV1 as a required codec

## Examples

Netflix studies show AV1 typically achieves 30-50% bitrate reduction compared to H.264 at equivalent perceptual quality. For 4K HDR content, this translates to requiring half the bandwidth or delivering noticeably better quality at the same bitrate.

## Related Concepts

- [[Video Codec]] - The broader category of video compression technologies
- [[hevc-h265]] - Competing standard with licensing complexities
- [[VP9]] - Google's predecessor to AV1
- [[FFmpeg]] - Open-source tool for AV1 encoding
- [[WebM]] - Container format often used with AV1

## Further Reading

- AOMedia official specifications (aomediacodec.github.io)
- FFmpeg AV1 encoding documentation
- Alliance for Open Media website (aomedia.org)

## Personal Notes

AV1 encoding is computationally intensive—a significant barrier for real-time applications. Hardware acceleration is improving rapidly, with modern GPUs and mobile SoCs including AV1 decode support. The main remaining challenge is encoding speed for live applications; cloud encoding is currently the practical solution for live streaming at scale.
