#!/usr/bin/env python3
"""Entry for make.fun news-image-20261122.

Copies the pre-rendered front-page image (entry.png, in this same
directory) to the grader's output directory as /output/entry.png.

Standard library only: no network, no third-party packages.
"""
import hashlib
import os
import shutil
import struct
import sys


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_png(path):
    """Check the file is a 1024x1024 PNG before it is copied.

    Verifies the 8-byte PNG signature and reads the width/height from
    the first chunk (IHDR). Returns an error string, or None if valid.
    """
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        return f"{path} is too small to be a PNG ({len(header)} bytes)"
    if header[:8] != PNG_SIGNATURE:
        return f"{path} is not a PNG file (bad signature)"
    chunk_length = struct.unpack(">I", header[8:12])[0]
    chunk_type = header[12:16]
    if chunk_type != b"IHDR" or chunk_length != 13:
        return f"{path} has no valid IHDR chunk as its first chunk"
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return (
            f"{path} has wrong dimensions {width}x{height}, "
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1

    validation_error = validate_png(source)
    if validation_error is not None:
        print(f"error: {validation_error}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    shutil.copyfile(source, target)

    src_hash = sha256_of(source)
    dst_hash = sha256_of(target)
    if src_hash != dst_hash:
        print("error: copied file differs from entry.png", file=sys.stderr)
        return 1

    size = os.path.getsize(target)
    print(f"wrote {target} ({size} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
