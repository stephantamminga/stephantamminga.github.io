#!/usr/bin/env python3
"""Resize an image to a maximum of 2048x2048 (longest side) and store it
as a baseline JPEG, honoring EXIF orientation.

Only shrinks; never upscales. Requires Pillow.
"""
import argparse
import sys
from PIL import Image, ImageOps

MAX_SIZE = 2048


def resize(input_path: str, output_path: str, max_size: int = MAX_SIZE) -> None:
    with Image.open(input_path) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        longest = max(im.size)
        if longest > max_size:
            scale = max_size / float(longest)
            new_size = (
                max(1, int(round(im.size[0] * scale))),
                max(1, int(round(im.size[1] * scale))),
            )
            im = im.resize(new_size, Image.LANCZOS)
        im.save(output_path, format="JPEG", quality=90, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resize an image to max 2048x2048 and store as JPEG."
    )
    parser.add_argument("--input", required=True, help="source image path")
    parser.add_argument("--output", required=True, help="destination .jpg path")
    parser.add_argument(
        "--max-size", type=int, default=MAX_SIZE,
        help="maximum length of the longest side in pixels (default 2048)",
    )
    args = parser.parse_args()
    try:
        resize(args.input, args.output, args.max_size)
    except FileNotFoundError:
        print(f"error: input not found: {args.input}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    with Image.open(args.output) as out:
        print(f"{args.output}: {out.format} {out.size[0]}x{out.size[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
