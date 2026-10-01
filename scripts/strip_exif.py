#!/usr/bin/env python3
"""Strip metadata segments (EXIF/XMP/IPTC/comments) from JPEG files in place."""
import sys

# Segments to drop: APP1-APP15 (EXIF, XMP, Photoshop/IPTC, etc.) and COM.
# Keep APP0 (JFIF) and all image-data segments.
DROP = {0xE0 + i for i in range(1, 16)} | {0xFE}


def strip(path: str) -> None:
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        raise ValueError(f"{path}: not a JPEG")
    out = bytearray(b"\xff\xd8")
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            # Entropy-coded data reached; copy the rest verbatim.
            out += data[i:]
            break
        marker = data[i + 1]
        if marker == 0xDA:  # SOS: copy the rest verbatim.
            out += data[i:]
            break
        seglen = int.from_bytes(data[i + 2 : i + 4], "big")
        if marker not in DROP:
            out += data[i : i + 2 + seglen]
        i += 2 + seglen
    with open(path, "wb") as f:
        f.write(out)
    print(f"{path}: {len(data)} -> {len(out)} bytes")


for p in sys.argv[1:]:
    strip(p)
