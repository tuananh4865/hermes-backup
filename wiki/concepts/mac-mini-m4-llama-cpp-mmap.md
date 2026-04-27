---
title: "Mac Mini M4 chạy Model 35B với llama.cpp --mmap"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [apple-silicon, llama.cpp, local-ai, mac-mini, inference]
description: "Cách Ben Badejo chạy model 35B trên Mac Mini M4 16GB với llama.cpp --mmap flag"
sources: [raw/transcripts/2026-04-15-tun-https-leopardracer.md]
---

# Mac Mini M4 chạy Model 35B với llama.cpp --mmap

## Tóm tắt

Ben Badejo (leopardracer) đã chạy thành công model AI 35 tỷ tham số trên Mac Mini M4 bản base $599 với 16GB RAM bằng cách sử dụng **llama.cpp** với flag **`--mmap`** duy nhất.

## Vấn đề ban đầu

- Mọi người đều bảo 16GB RAM không đủ để chạy model 35B
- Thử dùng Ollama hoặc LM Studio → **thất bại**: model không generate được token nào, coi như dead

## Giải pháp

Dùng **llama.cpp** với flag duy nhất: **`--mmap`**

> Kết quả: Same model, same hardware → chạy mượt

## Kỹ thuật --mmap

`--mmap` bật **memory-mapped file access**:

- Thay vì nạp toàn bộ model vào RAM, llama.cpp memory-map file model vào RAM
- Chỉ đọc phần cần thiết từ disk
- macOS tự động quản lý phần nào được cache trong RAM, phần nào giữ trên disk
- Zero swap (không dùng disk làm virtual RAM)

## Kết quả thực tế

| Spec | Value |
|------|-------|
| Hardware | Mac Mini M4 base ($599, 16GB RAM) |
| Tool | llama.cpp + `--mmap` |
| Model size | 35B parameters |
| Swap used | 0 |

## Ý nghĩa

1. **Phá vỡ lầm tưởng**: Nhiều người nghĩ 16GB RAM không thể chạy model > 7B
2. **Local AI không cần phần cứng đắt tiền**: $600 Mac Mini có thể thay thế nhiều use case của cloud API
3. **llama.cpp tận dụng tốt unified memory architecture** của Apple Silicon M4

## Liên quan

- [[llama.cpp]]
- [[Apple Silicon]]
- [[local-ai]]
- Ben Badejo (leopardracer)
