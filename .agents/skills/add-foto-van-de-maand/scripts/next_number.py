#!/usr/bin/env python3
"""Print the next incremental number for a Foto van de maand image.

Scans assets/images/content/foto-van-de-maand/ for files named <NN>.jpg,
finds the highest <NN>, and prints <NN>+1 (zero-padded to at least two
digits, three digits from 100 upward).
"""
import os
import re
import sys

IMAGE_DIR = os.path.join(
    "assets", "images", "content", "foto-van-de-maand"
)
PATTERN = re.compile(r"^(\d+)\.jpg$")


def next_number(image_dir: str = IMAGE_DIR) -> int:
    highest = 0
    if not os.path.isdir(image_dir):
        return 1
    for name in os.listdir(image_dir):
        m = PATTERN.match(name)
        if m:
            highest = max(highest, int(m.group(1)))
    return highest + 1


def format_number(n: int) -> str:
    return f"{n:02d}" if n < 100 else str(n)


def main() -> int:
    n = next_number()
    print(format_number(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
