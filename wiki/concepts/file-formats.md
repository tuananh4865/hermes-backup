---
title: "File Formats"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [data, serialization, formats, interchange, standards]
---

# File Formats

## Overview

A file format is a standardized way of encoding information so that it can be stored in a file and later reconstructed by appropriate software. Formats define the structure, data types, encoding rules, and organizational schema that transform abstract data — numbers, text, images, audio, documents — into a sequence of bytes that persists across program executions, system reboots, and hardware changes.

File formats sit at the boundary between human intent and machine storage. They are contracts: an agreement between the writer of data and any future reader about what bytes mean. When that contract is public, documented, and widely adopted, we call it an open standard. When it is proprietary and unpublished, it creates vendor lock-in and data longevity risk — formats like early Word `.doc` files demonstrate how proprietary formats can become liabilities as software evolves.

Understanding file formats is essential for data engineering, interoperability, archival, and debugging. Every programmer encounters the consequences of format choice early: the moment a text file you edited looks like hieroglyphics because it was saved as UTF-16 instead of UTF-8, or a spreadsheet shows dates as numbers because the parser didn't know the epoch offset.

## Key Concepts

**Text vs. Binary Formats**: Text formats encode data as human-readable character sequences — JSON, CSV, XML, Markdown. Binary formats encode data as raw machine-readable bytes — PNG, MP4, AVRO, Parquet. Text formats are debuggable with a text editor; binary formats are denser and faster to parse but require a specification to decode.

**Schema-ful vs. Schema-less**: Some formats embed their schema (field names, types, structure) in every file — JSON and XML are self-describing. Others store only data, relying on an external schema at read time — Avro and Parquet are schema-evolution-aware binary formats used heavily in [[Big Data]] pipelines.

**Serialization and Deserialization**: The process of turning an in-memory object or data structure into a byte stream (serialization) and reconstructing it (deserialization). Different formats optimize for different properties: human readability, speed, size, or schema evolution safety.

**Endianness and Encoding**: Binary formats must specify byte order (little-endian vs. big-endian) for multi-byte numbers. Text formats must specify character encoding — ASCII, UTF-8, UTF-16, Latin-1. Misunderstanding either renders data unreadable. The "BOM" (byte order mark) in UTF-8/UTF-16 files is a small marker that tells parsers how to interpret the following bytes.

**Compression**: Many formats pair with compression algorithms — `.gz` for gzip, `.bz2` for bzip2, `.xz` for LZMA. Columnar formats like Parquet and ORC achieve compression by storing data column-by-column, allowing aggressive type-specific encoding (dictionary encoding, run-length encoding, delta encoding).

## How It Works

Most file formats begin with a magic number — a short byte sequence that identifies the format before any parsing begins. PNG files always start with bytes `89 50 4E 47 0D 0A 1A 0A`. PDF files start with `%PDF`. This allows file utility programs and browsers to route data to the correct parser.

```bash
# Inspect magic numbers to identify formats
file document.png     # PNG image data, ASCII, 800 x 600
file data.csv         # CSV text
file archive.gz       # gzip compressed data
file binary.dat        # data

# View hex dump of a file's header
xxd -l 32 document.png
# 00000000: 8950 4e47 0d0a 1a0a 0000 0d00 4849 5254  .PNG........HIRT
```

Text-based formats can often be parsed with standard library functions:

```python
import json
import csv
import xml.etree.ElementTree as ET

# JSON — parse a configuration or API response
config = json.loads('{"theme": "dark", "font_size": 14}')

# CSV — tabular data, common for exports and datasets
with open('users.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['email'])

# XML — structured hierarchical data
tree = ET.parse('config.xml')
root = tree.getroot()
for child in root:
    print(child.tag, child.attrib)
```

## Practical Applications

Data interchange formats like JSON and XML power web APIs. REST APIs overwhelmingly use JSON; SOAP APIs use XML. Choosing the right format affects not just your code but every client that integrates with your API — JSON's lightweight readability has made it the default for public APIs, while XML remains important in enterprise and government systems.

Archive and preservation formats prioritize longevity over performance. The Library of Congress recommends TIFF for image preservation (lossless, well-documented) and PDF/A for documents (self-contained, ISO-standardized). The cost of format obsolescence is data loss — migration between formats is expensive and lossy if done carelessly.

In software development, configuration files use JSON (Node.js `package.json`), YAML (Docker Compose, Ansible), TOML (Rust `Cargo.toml`), and ENV files (environment variables) — each with tradeoffs in readability, schema support, and tooling ecosystem.

In [[Big Data]] and analytics, columnar formats (Parquet, ORC) replaced row-oriented formats for analytical queries because they allow queries to read only the columns needed, dramatically reducing I/O for wide tables with billions of rows.

## Examples

The same data — say, a list of users — can be represented across formats:

```json
// JSON — human-readable, self-describing, ubiquitous
[
  {"id": 1, "name": "Amara Osei", "email": "amara@example.com", "active": true},
  {"id": 2, "name": "Luca Ferretti", "email": "luca@example.com", "active": false}
]
```

```csv
# CSV — minimal, tabular, every tool reads it
id,name,email,active
1,Amara Osei,amara@example.com,true
2,Luca Ferretti,luca@example.com,false
```

```xml
<!-- XML — verbose, self-describing, schema-validatable -->
<users>
  <user id="1">
    <name>Amara Osei</name>
    <email>amara@example.com</email>
    <active>true</active>
  </user>
</users>
```

Each format serves the same conceptual data but with different tradeoffs in size, tooling, and human vs. machine orientation.

## Related Concepts

- [[JSON]] — The dominant text format for web APIs and configuration
- [[XML]] — Structured markup format, still prevalent in enterprise
- [[CSV]] — Simple tabular interchange format
- [[Binary Data]] — Formats that encode at the byte level for efficiency
- [[Big Data]] — Domain where columnar formats like Parquet are essential
- [[Serialization]] — The process underlying file format operations

## Further Reading

- [File Format Encyclopedia — Gary Kessler's site](https://www.garykessler.net/library/file_sigs.html)
- [RFC 8259 — The JSON Spec](https://datatracker.ietf.org/doc/html/rfc8259)
- *Designing Data-Intensive Applications* by Martin Kleppmann — Chapter 4 covers data formats and encodings in depth

## Personal Notes

I once spent three days debugging a data pipeline failure that turned out to be an encoding mismatch: the upstream system was writing UTF-16 CSV files, and my Python script was opening them with the default UTF-8. The resulting decode errors were opaque until I hex-dumped the file and saw the zero-width bytes that are telltale signatures of UTF-16. Now, whenever I encounter a file that "looks wrong," the first thing I check is `file` or `xxd` before assuming anything about the content. Format identification is a prerequisite to format parsing.
