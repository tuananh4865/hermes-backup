---
title: "Encoding"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [character-encoding, unicode, utf-8, text-processing, data-formats]
---

# Encoding

## Overview

Encoding refers to the process of converting data from one format into another, particularly when discussing how text characters are represented as bytes in computer systems. Character encoding is a fundamental concept in computing because computers store and manipulate text by representing characters as numerical codes. Without a shared understanding of which numerical code maps to which character, the same sequence of bytes could be interpreted completely differently by different systems.

The history of character encoding is long and fragmented. Early computing used proprietary encodings like EBCDIC on IBM mainframes. ASCII emerged in the 1960s as a 7-bit standard for English text, defining 128 characters including letters, digits, punctuation, and control codes. As computing spread globally, numerous country-specific encodings emerged (ISO-8859-1 for Western European languages, Shift-JIS for Japanese, GB2312 for Simplified Chinese), creating a chaotic landscape of incompatible character representations.

Unicode was created to unify these fragmented systems by assigning a unique code point to every character used in all known writing systems. Unicode can represent over 1 million characters, though current assignments cover about 150 scripts. However, Unicode itself is not a encoding—it defines code points but not how those code points are stored as bytes. This is where encoding schemes like UTF-8, UTF-16, and UTF-32 become essential.

## Key Concepts

**Code Point**: A unique number assigned to a character in the Unicode standard. Written in the form U+XXXX (e.g., U+0041 for the letter 'A'). Unicode defines over 1.4 million possible code points, though only about 150,000 are currently assigned.

**Character Set (Charset)**: A collection of characters that can be used for a particular purpose. A charset defines which characters exist but not how they are stored. Unicode is a character set; UTF-8 is an encoding.

**Encoding Scheme**: A mapping from code points to byte sequences. UTF-8, UTF-16LE, UTF-16BE, and UTF-32 are all encoding schemes for the Unicode character set.

**Byte Order Mark (BOM)**: A Unicode character (U+FEFF) placed at the beginning of a text stream to indicate the byte order of the data. UTF-16 and UTF-32 files often start with a BOM, though UTF-8 files rarely need one.

**Code Unit**: The minimal bit combination that can represent a character in a given encoding. UTF-8 uses 8-bit code units (bytes), UTF-16 uses 16-bit code units, and UTF-32 uses 32-bit code units.

## How It Works

UTF-8 is the most widely used encoding on the web and in modern software. It uses a variable-width encoding scheme where ASCII characters (U+0000 to U+007F) are encoded as single bytes, while characters outside the ASCII range require two to four bytes. This design makes UTF-8 backward-compatible with ASCII and space-efficient for English text while still supporting all Unicode characters.

The encoding algorithm is clever in its bit layout:
- Single-byte codes (0xxxxxxx) for ASCII
- Two-byte codes (110xxxxx 10xxxxxx) for characters needing up to 11 bits
- Three-byte codes (1110xxxx 10xxxxxx 10xxxxxx) for characters needing up to 16 bits
- Four-byte codes (11110xxx 10xxxxxx 10xxxxxx 10xxxxxx) for characters needing up to 21 bits

UTF-16 uses two or four bytes per character. Characters in the Basic Multilingual Plane (U+0000 to U+FFFF) are encoded as a single 16-bit code unit, while characters above U+FFFF require a surrogate pair of two code units. UTF-32 is fixed-width, always using exactly four bytes per character, which simplifies indexing but wastes significant space for common text.

```python
# Working with encodings in Python
text = "Hello, 世界! 🎉"

# Encode to UTF-8 bytes
utf8_bytes = text.encode('utf-8')
print(utf8_bytes)  # b'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x8e\x89'

# Decode bytes back to string
decoded = utf8_bytes.decode('utf-8')
print(decoded)  # Hello, 世界! 🎉

# Handling encoding errors
try:
    invalid_utf8 = b'\xff\xfe'
    decoded = invalid_utf8.decode('utf-8')
except UnicodeDecodeError as e:
    print(f"Encoding error: {e}")

# Replace errors with a placeholder
safe_decoded = invalid_utf8.decode('utf-8', errors='replace')
print(safe_decoded)  # ��
```

Character encoding issues commonly manifest as mojibake—garbled text where characters are displayed incorrectly. For example, the bytes for "café" encoded in UTF-8, then decoded as ISO-8859-1, produces "cafÃ©" or similar gibberish.

## Practical Applications

**Web Development**: All modern websites should use UTF-8. HTTP headers, HTML meta tags, and database connections should all specify UTF-8 encoding. The WHATWG encoding standard is the authoritative reference for web browsers.

**File Systems**: Different operating systems use different default encodings. Linux typically uses UTF-8 everywhere, macOS uses UTF-8, but Windows often uses locale-specific encodings, creating cross-platform file handling challenges.

**Network Protocols**: JSON and XML expect UTF-8 unless another encoding is explicitly declared. Email originally used 7-bit ASCII with extensions for other character sets, though UTF-8 email is now widely supported.

**APIs**: REST and GraphQL APIs should consistently use UTF-8 and declare it in the Content-Type header (application/json; charset=utf-8).

## Examples

Detecting and converting encodings is a common task:

```python
import chardet

# Detect the encoding of raw bytes
raw_data = b'\xe4\xb8\xad\xe6\x96\x87\xe5\xad\x97'
detected = chardet.detect(raw_data)
print(detected)  # {'encoding': 'utf-8', 'confidence': 0.99}

# Normalize text to NFC form for consistent comparison
from unicodedata import normalize
text1 = "café"  # é as single character
text2 = "cafe\u0301"  # é as e + combining acute accent
print(text1 == text2)  # False
print(normalize('NFC', text1) == normalize('NFC', text2))  # True
```

Unicode normalization is important because the same visual character can be represented multiple ways. NFC (Composition) combines characters where possible, while NFD (Decomposition) splits them.

## Related Concepts

- [[Unicode]] - The character set that many modern encodings implement
- [[UTF-8]] - The most common Unicode encoding
- [[ASCII]] - The ancestor of modern encodings
- [[Character Sets]] - Collections of characters
- [[Data Serialization]] - Encoding structured data
- [[Base64]] - Encoding binary data as ASCII text

## Further Reading

- The Unicode Standard - The definitive reference for Unicode
- UTF-8 Everywhere Manifesto - Arguments for UTF-8 as the default encoding
- Joel Spolsky's "The Absolute Minimum Every Software Developer Must Know About Unicode and Character Sets" - Excellent introduction
- WHATWG Encoding Standard - Web browser encoding behavior

## Personal Notes

The most important practical rule: always know what encoding you're working with. Default encodings vary by language, platform, and library. Python 3's default encoding is UTF-8 for text files opened in text mode, but reading files in binary mode gives you raw bytes—no encoding applied. Java's default encoding depends on the platform locale. JavaScript's string type is UTF-16. This inconsistency is a common source of bugs.

When handling text from unknown sources, always attempt to detect or validate the encoding rather than assuming UTF-8. Invalid byte sequences are common in real-world data and should be handled gracefully, either by rejecting the input or replacing invalid sequences with placeholders.
