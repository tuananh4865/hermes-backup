#!/usr/bin/env python3
"""Fix broken string escapes in skills_tool.py"""
import re

with open('/Users/tuananh4865/.hermes/hermes-agent/tools/skills_tool.py', 'rb') as f:
    content = f.read()

# The bad pattern is: QUOTE + BACKSLASH + QUOTE + APOSTROPHE (0x22 0x5c 0x22 0x27)
# This appears inside t.strip().strip("\' --- a broken escape sequence
# The fix is: OPEN_SINGLE + DOUBLE_QUOTE + CLOSE_SINGLE + CLOSE_SINGLE
# i.e., 0x27 0x22 0x27 0x27 → t.strip().strip('"')

bad_seq = b'"\x5c\x22\x27'  # the broken escape: " \' "
good_seq = b"'\x22\x27\x27"  # the correct: ' " ' '

# Count occurrences
count = content.count(bad_seq)
print(f"Found {count} occurrences of bad escape sequence")

# Replace
fixed = content.replace(bad_seq, good_seq)
print(f"Replaced")

# Write
with open('/Users/tuananh4865/.hermes/hermes-agent/tools/skills_tool.py', 'wb') as f:
    f.write(fixed)

# Verify syntax
import ast
try:
    with open('/Users/tuananh4865/.hermes/hermes-agent/tools/skills_tool.py', 'r') as f:
        ast.parse(f.read())
    print("Syntax OK")
except SyntaxError as e:
    print(f"Still broken at line {e.lineno}: {e.msg}")
    # Show the context
    with open('/Users/tuananh4865/.hermes/hermes-agent/tools/skills_tool.py', 'r') as f:
        lines = f.readlines()
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
        marker = ">>>" if i+1 == e.lineno else "   "
        print(f"{marker} {i+1}: {repr(lines[i][:80])}")
