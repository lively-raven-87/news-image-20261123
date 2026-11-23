#!/usr/bin/env python3
"""Ship the pre-drawn 23 November 2026 front page.

Reads entry.png next to this file, checks it is a whole PNG inside the
competition gate (at most 1 MiB, at most 1024x1024), then copies it to the
output directory and re-checks the copy. Standard library only.
"""
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
BYTE_LIMIT = 1048576
SIDE_LIMIT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def iter_chunks(blob):
    """Yield (type, payload) for each chunk of a PNG byte string."""
    cursor = 8
    while cursor + 8 <= len(blob):
        size = struct.unpack(">I", blob[cursor:cursor + 4])[0]
        kind = blob[cursor + 4:cursor + 8]
        stop = cursor + 8 + size + 4
        if stop > len(blob):
            raise ValueError("chunk %r runs past end of file" % kind)
        payload = blob[cursor + 8:stop - 4]
        expect = struct.unpack(">I", blob[stop - 4:stop])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != expect:
            raise ValueError("CRC mismatch in chunk %r" % kind)
        yield kind, payload
        cursor = stop


def dimensions_of(blob):
    """Return (width, height) of a PNG, verifying its structure."""
    if blob[:8] != PNG_MAGIC:
        raise ValueError("missing PNG signature")
    width = height = None
    closed = False
    for kind, payload in iter_chunks(blob):
        if kind == b"IHDR":
            width, height = struct.unpack(">II", payload[:8])
        elif kind == b"IEND":
            closed = True
            break
    if width is None or not closed:
        raise ValueError("PNG has no IHDR or no IEND")
    return width, height


def load_entry():
    with open(SOURCE, "rb") as handle:
        blob = handle.read()
    width, height = dimensions_of(blob)
    if len(blob) > BYTE_LIMIT:
        raise ValueError("entry.png is %d bytes, over the 1 MiB gate"
                         % len(blob))
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 gate"
                         % (width, height))
    return blob, width, height


def main():
    blob, width, height = load_entry()
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    with open(target, "rb") as handle:
        copied = handle.read()
    if copied != blob:
        raise ValueError("output copy differs from source")
    print("entry.png: %d bytes, %dx%d, gate OK" % (len(blob), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
