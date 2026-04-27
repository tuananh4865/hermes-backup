---
title: Compression
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [compression, algorithms, data, optimization]
---

## Overview

Compression is the process of reducing the size of data to store or transmit it more efficiently. It works by identifying patterns, redundancy, and unnecessary information within the data, then encoding that data in a more compact representation. Compression is fundamental to modern computing, enabling faster data transfer over networks, reduced storage costs, and efficient resource utilization across everything from smartphones to data centers.

Data compression techniques have been developed and refined over decades, forming an essential part of many technologies people use daily. When you stream a video, download a file, or save a document, compression algorithms are working behind the scenes to reduce the amount of data that needs to be processed. The field draws heavily from information theory, mathematics, and computer science to develop algorithms that maximize compression ratios while minimizing the loss of information or quality.

Compression matters because bandwidth and storage are never infinite. Every byte saved through compression translates to faster downloads, lower storage costs, and reduced power consumption in data centers. As the volume of digital data continues to grow exponentially, compression remains one of the most practical and effective optimization techniques available.

## Types

Compression methods generally fall into two categories: lossless and lossy. Understanding the difference is crucial for selecting the right compression approach for any given use case.

**Lossless compression** reduces data size without losing any original information. When decompressed, the data is bit-for-bit identical to the original. This is essential for text documents, source code, databases, and any data where accuracy is critical. Lossless compression works by finding and eliminating statistical redundancy, typically using dictionary-based methods or statistical encoding schemes. Common lossless formats include ZIP, PNG for images, and FLAC for audio.

**Lossy compression** discards information deemed less important to achieve higher compression ratios. This approach is acceptable for media like images, audio, and video where some loss of fidelity may be imperceptible or acceptable to human senses. Lossy compression exploits limitations in human perception—for example, JPEG images discard color information the human eye is less sensitive to, and MP3 audio removes sounds outside typical human hearing ranges. While lossy compression can achieve dramatically smaller file sizes, the discarded information cannot be recovered.

The choice between lossless and lossy compression depends entirely on the use case. A text document requires perfect accuracy, making lossless compression mandatory. A photograph for a website might tolerate some quality loss for faster loading times. The best compression strategies often combine both approaches, using lossless compression where necessary and lossy compression where acceptable.

## Algorithms

Several algorithms form the foundation of modern compression technology, each with distinct approaches and strengths.

**Huffman coding** is a statistical compression algorithm that assigns variable-length codes to symbols based on their frequency of occurrence. More frequent symbols receive shorter codes, while less common symbols get longer codes. This approach was developed by David Huffman in 1952 and remains influential today. Huffman coding is often used as a component within larger compression systems, including DEFLATE. The elegance of Huffman coding lies in its guaranteed optimality for symbol-by-symbol encoding with known frequencies.

**LZ77** (Lempel-Ziv 1977) introduced the concept of dictionary-based compression using sliding windows. Instead of编码 each symbol individually, LZ77 finds repeated sequences in the data and replaces them with references to earlier occurrences. A reference consists of a distance (how far back in the window) and a length (how many characters to copy). This approach is particularly effective for data containing repeated patterns, such as text documents and source code. LZ77 forms the theoretical basis for many practical compression algorithms.

**DEFLATE** is a specific compression format that combines LZ77 with Huffman coding. Developed by Phil Katz for the original ZIP file format, DEFLATE remains one of the most widely used compression algorithms today. It uses LZ77 to identify repeated sequences and then applies Huffman coding to encode the resulting references and literal symbols. DEFLATE offers a good balance between compression ratio and computational complexity, making it suitable for a wide range of applications. The gzip format, PNG images, and ZIP archives all use DEFLATE internally.

Other notable compression algorithms include LZ78 (the basis for the LZW algorithm used in GIF images and UNIX compress), Burrows-Wheeler transform (used in bzip2), and more modern approaches like LZMA (used in 7-Zip) and Zstandard (used for fast real-time compression). Each algorithm makes different tradeoffs between compression ratio, speed, and memory requirements.

## Related

- [[Data Structures]] - How data is organized and stored, often interacting with compression
- [[Information Theory]] - The mathematical foundation of compression algorithms
- [[File Formats]] - Container formats that often incorporate compression like ZIP and PNG
- [[Network Protocols]] - Protocols that use compression to reduce transmission time
- [[Algorithm Complexity]] - The computational efficiency considerations in compression design
- [[Entropy Encoding]] - The category of encoding methods that includes Huffman coding
