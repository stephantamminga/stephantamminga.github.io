#!/usr/bin/env python3
"""Prepend a new photo-highlight block to pages/foto-van-de-maand.md.

The new block is inserted immediately after the intro paragraph (the
body content before the first existing photo-highlight block), keeping
the newest-first ordering already used on the page. The caption text is
identical in the img alt and the .photo-caption div.

Requires no third-party packages.
"""
import argparse
import os
import sys

PAGE_PATH = os.path.join("pages", "foto-van-de-maand.md")
BLOCK_MARKER = '<div class="photo-highlight">'


def build_caption(maker: str, month: str, title: str | None) -> str:
    caption = f"\u00a9 {maker} - {month}"
    if title:
        caption += f", {title}"
    return caption


def build_block(number: str, caption: str) -> str:
    return (
        '<div class="photo-highlight">\n'
        f'  <img src="{{{{ \'/assets/images/content/foto-van-de-maand/{number}.jpg\' | relative_url }}}}" alt="{caption}">\n'
        f'  <div class="photo-caption">{caption}</div>\n'
        '</div>'
    )


def update_page(page_path: str, number: str, maker: str, month: str,
                title: str | None) -> str:
    with open(page_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.endswith("\n"):
        content += "\n"

    marker_index = content.find(BLOCK_MARKER)
    if marker_index == -1:
        raise SystemExit(
            f"error: no existing photo-highlight block found in {page_path}; "
            "refusing to insert into a page without the expected structure"
        )

    # Walk back from the marker to the start of that line.
    line_start = content.rfind("\n", 0, marker_index) + 1
    # The intro block is everything before line_start. Ensure it ends with
    # a blank line separating the intro text from the new block.
    head = content[:line_start]
    tail = content[line_start:]

    if not head.endswith("\n"):
        head += "\n"
    if not head.endswith("\n\n"):
        head += "\n"

    caption = build_caption(maker, month, title)
    block = build_block(number, caption)

    already = f"/foto-van-de-maand/{number}.jpg"
    if already in content:
        raise SystemExit(
            f"error: page already references {already}; "
            "refusing to add a duplicate block for the same number"
        )

    new_content = head + block + "\n\n" + tail

    with open(page_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return caption


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepend a new photo-highlight block to foto-van-de-maand.md"
    )
    parser.add_argument("--number", required=True,
                        help="zero-padded image number, e.g. 32")
    parser.add_argument("--maker", required=True, help="photographer name")
    parser.add_argument("--month", required=True, help="Dutch month + year, e.g. januari 2026")
    parser.add_argument("--title", default=None, help="optional photo title")
    parser.add_argument("--page", default=PAGE_PATH, help="page markdown path")
    args = parser.parse_args()

    caption = update_page(args.page, args.number, args.maker, args.month, args.title)
    print(f"added block for {args.number}.jpg: {caption}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
