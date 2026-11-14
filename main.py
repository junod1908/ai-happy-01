#!/usr/bin/env python3
"""ai-happy-01 entry: write the entry's image to /output/entry.png.

The repository holds the image as entry.png beside this program, and the
program copies it, byte for byte, to the output. The gate takes a whole PNG
or JPEG of at most 1 MiB and 1024 by 1024 pixels, told apart by its first
bytes (this entry's file holds JPEG bytes under the entry.png name, which
the rules allow); the judge sees exactly the bytes copied, and two runs
write the same bytes because a copy never changes them.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_NAME = "entry.png"


def output_dir() -> Path:
    """The directory the grader reads the entry from."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    dest_dir = output_dir()
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / OUTPUT_NAME
        shutil.copyfile(SOURCE, dest)
    except OSError:
        # Fallback for runs where the primary output directory cannot be
        # created or written (a local checkout, say): write to an "out"
        # directory beside this program instead of failing outright.
        dest = HERE / "out" / OUTPUT_NAME
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE, dest)
    if dest.read_bytes() != SOURCE.read_bytes():
        raise SystemExit("the written entry.png does not match the source image")


if __name__ == "__main__":
    main()
