---
title: "HEVC / H.265"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [video, codec, compression]
confidence: medium
sources: []
---

# HEVC / H.265

## Overview

HEVC (High Efficiency Video Coding), also known as H.265, is a video compression standard that provides roughly 50% better compression efficiency compared to H.264 at the same visual quality. Developed by ITU-T and ISO/IEC, it is the successor to H.264/AVC.

## Why It Matters

- 4K and 8K streaming (Netflix, Apple TV 4K use HEVC)
- Bandwidth savings — half the bitrate for same quality
- Essential for streaming on limited bandwidth connections

## Trade-offs

- **Licensing**: HEVC patents are heavily licensed (unlike AV1 which is royalty-free)
- **Encoding cost**: HEVC encoding requires significantly more CPU than H.264
- **Hardware support**: Apple devices have native HEVC hardware decode

## Related Concepts

- [[video-codec]] — General video codec overview
- [[h264]] — H.264/AVC, the predecessor
- [[av1]] — Royalty-free codec, HEVC's main competitor
