#!/usr/bin/env python3
"""Entry for make.fun news-image-20261122.

Copies the pre-rendered front-page image (entry.png, in this same
directory) to the grader's output directory as /output/entry.png.

Standard library only: no network, no third-party packages.
"""
import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("error: entry.png not found next to main.py", file=sys.stderr)
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
