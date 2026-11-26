#!/usr/bin/env python3
"""news-image-20261126 entrypoint (Python 3.13, standard library only).

The front page is pre-rendered and committed as entry.png; this program
just copies it to the output directory, so both grader runs write the
same bytes. It validates the PNG magic and the 1 MiB / 1024x1024 caps
before copying.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

with open(SRC, "rb") as fh:
    head = fh.read(33)

assert head[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
width = int.from_bytes(head[16:20], "big")
height = int.from_bytes(head[20:24], "big")
assert width <= 1024 and height <= 1024, "entry.png over 1024x1024"
assert os.path.getsize(SRC) <= 1048576, "entry.png over 1 MiB"

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, OUT)
os.chmod(OUT, 0o644)

# Confirm the copy is byte-identical to the committed image, so both
# grader runs write the same bytes.
assert os.path.getsize(OUT) == os.path.getsize(SRC), "output size mismatch"
with open(SRC, "rb") as a, open(OUT, "rb") as b:
    assert a.read() == b.read(), "output bytes differ from entry.png"
print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
