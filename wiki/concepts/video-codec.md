---
title: "Video Codec"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [video-compression, multimedia, signal-processing, streaming]
---

# Video Codec

## Overview

A video codec (coder-decoder) is software or hardware that compresses and decompresses digital video data. The purpose of video coding is to reduce the massive amount of data required to represent video—uncompressed video at 1080p resolution at 60 frames per second can require over 1.5 Gbps (gigabits per second). Video codecs achieve compression by exploiting spatial redundancy (similarities within a frame), temporal redundancy (similarities between consecutive frames), and perceptual redundancy (details humans are unlikely to notice).

The field of video coding is governed by international standards developed by bodies such as ITU-T (H.261, H.263, H.264) and ISO/IEC MPEG (MPEG-1, MPEG-2, MPEG-4). The most widely deployed codec today is H.264/AVC (Advanced Video Coding), though newer codecs like H.265/HEVC (High Efficiency Video Coding), VP9, AV1, and VVC (H.266) offer significantly better compression efficiency. Understanding codecs is essential for anyone working in streaming, broadcasting, video conferencing, or multimedia applications.

## Key Concepts

**Bitrate** is the amount of data used to represent one second of video, typically measured in kilobits per second (kbps) or megabits per second (Mbps). Lower bitrate means smaller file sizes but reduced quality. Adaptive bitrate streaming systems dynamically adjust bitrate based on network conditions.

**Resolution** refers to the number of pixels in each frame, expressed as width × height. Common resolutions include 1280×720 (720p), 1920×1080 (1080p), 3840×2160 (4K), and 7680×4320 (8K). Higher resolution requires significantly more data to represent at the same quality level.

**Frame Rate** is the number of individual images (frames) displayed per second, measured in fps (frames per second). Common frame rates include 24 fps (cinematic), 30 fps (standard video), 60 fps (smooth motion), and 120 fps (high-speed capture). Frame rate and resolution together determine the total number of pixels processed per second.

**Keyframes (I-frames)** are complete frames that are encoded without reference to other frames. They serve as reference points for decoding subsequent predicted frames. Keyframes are larger but essential for random access and error recovery. **Predicted frames (P-frames)** are encoded relative to a previous frame, storing only the differences. **Bidirectional frames (B-frames)** reference both previous and future frames for even greater compression.

**Quantization** reduces the precision of transformed coefficients after the discrete cosine transform (DCT) step. Higher quantization values produce smaller files but introduce visible artifacts known as compression artifacts—blockiness, blurring, and ringing around edges.

**Codec Profiles and Levels** define subsets of a codec's features. A profile specifies which algorithmic features are available (e.g., specific entropy coding methods), while a level specifies constraints on bitrate, resolution, and buffer size. Compatibility between encoder settings and decoder capabilities is critical for interoperability.

## How It Works

Modern video codecs follow a common pipeline architecture:

1. **Frame Partitioning**: Each frame is divided into blocks (typically 16×16 pixel macroblocks in H.264, though newer codecs use flexible block sizes)
2. **Motion Estimation**: For each block, the encoder searches for similar regions in previously decoded frames to find motion vectors
3. **Motion Compensation**: The predicted block is formed by shifting the reference block by the motion vector
4. **Transformation**: The residual (difference between actual and predicted block) is transformed using DCT or integer transforms
5. **Quantization**: Transform coefficients are quantized to reduce precision
6. **Entropy Coding**: The quantized coefficients, motion vectors, and header information are compressed using statistical coding (CABAC or CAVLC in H.264)

```text
[Raw Video Frame]
       |
       v
[Block Partitioning] --> [Motion Estimation] --> [Motion Compensation]
       |                                                      |
       |                                                      v
       |                                           [Residual Computation]
       |                                                      |
       |                                                      v
       |                                           [DCT / Integer Transform]
       |                                                      |
       |                                                      v
       +---------------> [Intra Prediction] <-- [Quantization]
                                                      |
                                                      v
                                             [Entropy Coding]
                                                      |
                                                      v
                                             [Compressed Bitstream]
```

Decoding reverses this process: entropy decoding, dequantization, inverse transform, motion compensation, and frame reconstruction.

## Practical Applications

**Video Streaming** is the dominant application for video codecs. Services like YouTube, Netflix, and Vimeo rely heavily on codec efficiency to deliver high-quality video to viewers with varying bandwidth. Adaptive bitrate streaming (HLS, DASH) uses multiple quality levels encoded at different resolutions and bitrates, allowing players to switch seamlessly based on network conditions.

**Video Conferencing** places extreme demands on codecs due to real-time encoding/decoding requirements and the need for low latency. Codecs like H.264 SVC (Scalable Video Coding) and newer options like AV1 offer low-latency modes optimized for interactive communication. VP9 and AV1 are increasingly used in WebRTC-based applications.

**Broadcast Television** standards vary by region but historically relied on MPEG-2 for satellite and cable distribution. The transition to HD and 4K has driven adoption of H.264 and more recently H.265/HEVC, which offer approximately 50% better compression efficiency than H.264 at equivalent quality.

**Mobile Video** is constrained by device processing power and battery life. Hardware-accelerated codec support in mobile SoCs (system-on-chips) enables efficient real-time encoding and decoding. The most common codec for mobile video capture and sharing is H.264 due to universal hardware support and good compression efficiency.

## Examples

A concrete example of codec selection: Netflix produces content in 4K HDR at up to 15 Mbps using H.265/HEVC. On a 25 Mbps connection, a Netflix subscriber gets this maximum quality. On a 5 Mbps connection, Netflix might deliver 1080p at 5 Mbps instead—the same perceptual quality is maintained by using the codec's efficiency to match the available bandwidth. The Netflix encode at 5 Mbps looks roughly equivalent to a raw Blu-ray encode at 15-20 Mbps due to codec efficiency improvements.

Another example is YouTube's upload and transcoding pipeline. When a creator uploads a video, YouTube transcodes it into dozens of output formats and resolutions—144p through 8K, various frame rates, and both H.264 and AV1. This process, called [[Transcoding]], ensures every viewer gets the optimal format for their device and connection regardless of the original upload format.

## Related Concepts

- [[Transcoding]] - The process of converting video from one codec or format to another
- [[Adaptive Bitrate Streaming]] - Delivery technique that switches between quality levels based on network conditions
- [[H.264 AVC]] - The most widely deployed video codec standard
- [[hevc-h265]] - The successor to H.264 offering roughly 50% better compression
- [[AV1]] - Open, royalty-free codec developed by the Alliance for Open Media
- [[Video Compression]] - The broader discipline of reducing video data size
- [[Multimedia Streaming]] - Applications and protocols for delivering video over networks

## Further Reading

- "Video Coding: HDTV, 3D, and Beyond" by K.R. Rao et al. — technical introduction to video coding standards
- ITU-T H.264 and H.265 specifications — the official standard documents
- AOMedia AV1 specification — the open codec standard documentation
- Compression.app — practical resources comparing codec quality and efficiency

## Personal Notes

Choosing a video codec involves trade-offs between compression efficiency, computational cost, royalty status, and ecosystem support. H.264 remains the safest choice for broad compatibility—essentially all devices and browsers support it in hardware. AV1 is the future for efficiency-focused applications but requires more CPU for encoding and has limited hardware support. For new streaming projects, consider a codec ladder that includes AV1 for capable clients, H.264 as a fallback, and potentially HEVC for 4K content on Apple devices.
