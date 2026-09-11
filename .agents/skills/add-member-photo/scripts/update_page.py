#!/usr/bin/env python3
"""Add one or more images to a member photo page under pages/fotos-van-leden/.

If the member page does not yet exist, it is created from a template and a
new entry is added to the member index (pages/fotos-van-leden.md). Existing
pages are updated in place: the image markdown line for each new number is
appended after the last existing image line, keeping the existing order.

Image lines use the simple Markdown image syntax already used on existing
member pages:

    ![<caption>](/assets/images/content/<member-slug>/<NN>.jpg)

The caption is `© <Member display name>`, matching the convention of the
existing member pages (see references/convention.md).

Requires no third-party packages.
"""
import argparse
import os
import re
import sys
import unicodedata

PAGES_DIR = os.path.join("pages", "fotos-van-leden")
INDEX_PATH = os.path.join("pages", "fotos-van-leden.md")
ASSET_BASE = os.path.join("assets", "images", "content")

IMAGE_LINE_RE = re.compile(
    r"^!\[[^\]]*\]\(/assets/images/content/[^/]+/\d+\.jpg\)\s*$",
    re.MULTILINE,
)

NEW_PAGE_TEMPLATE = (
    "---\n"
    "layout: page\n"
    "title: {title}\n"
    "parent: Foto's van leden\n"
    "---\n"
    "\n"
    "# {title}\n"
    "\n"
    "(klik op de foto voor grote weergave)\n"
    "\n"
    "{images}\n"
)

PLACEHOLDER_RE = re.compile(
    r"\*Deze pagina heeft nog geen foto's[^\n]*\n"
)


def member_slug(member: str) -> str:
    """Lowercase kebab-case slug for a member display name.

    Accented characters are transliterated to their ASCII base (e.g.
    "André" -> "andre") so the slug matches the existing folder/file
    naming used on the site.
    """
    normalized = unicodedata.normalize("NFKD", member.strip())
    ascii_only = "".join(c for c in normalized if not unicodedata.combining(c))
    slug = ascii_only.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if not slug:
        raise SystemExit(f"error: cannot derive a slug from member name {member!r}")
    return slug


def caption_for(member: str) -> str:
    return f"\u00a9 {member}"


def image_line(member: str, slug: str, number: str) -> str:
    return (
        f"![{caption_for(member)}]"
        f"(/assets/images/content/{slug}/{number}.jpg)"
    )


def page_path(slug: str) -> str:
    return os.path.join(PAGES_DIR, f"{slug}.md")


def ensure_asset_dir(slug: str) -> str:
    d = os.path.join(ASSET_BASE, slug)
    os.makedirs(d, exist_ok=True)
    return d


def page_has_images(content: str) -> bool:
    return IMAGE_LINE_RE.search(content) is not None


def append_images_to_page(path: str, member: str, slug: str, numbers: list[str]) -> None:
    """Append image lines for `numbers` to an existing member page."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_lines = [image_line(member, slug, n) for n in numbers]

    already = {n: False for n in numbers}
    for n in numbers:
        ref = f"/{slug}/{n}.jpg"
        if ref in content:
            already[n] = True

    if all(already.values()):
        raise SystemExit(
            "error: every supplied number is already referenced on the page; "
            "nothing to add"
        )

    if not content.endswith("\n"):
        content += "\n"

    if not page_has_images(content):
        # Page has no images yet (placeholder-only page): drop the placeholder
        # and insert the new images in its place.
        placeholder = PLACEHOLDER_RE.search(content)
        block = "\n".join(new_lines) + "\n"
        if placeholder:
            start, end = placeholder.span()
            new_content = content[:start] + block + content[end:]
        else:
            new_content = content + "\n" + block
    else:
        lines = content.splitlines(keepends=True)
        last_img_idx = None
        for i, line in enumerate(lines):
            if IMAGE_LINE_RE.match(line):
                last_img_idx = i
        if last_img_idx is None:
            # No image line matched but page_has_images returned True; fall back
            # to appending at the end.
            new_content = content
            if not new_content.endswith("\n"):
                new_content += "\n"
            new_content += "\n".join(new_lines) + "\n"
        else:
            to_insert = []
            for line in new_lines:
                if not already_relevant(line, content):
                    to_insert.append(line + "\n")
            insert_block = "".join(to_insert)
            if insert_block and not insert_block.startswith("\n"):
                insert_block = "\n" + insert_block
            new_content = (
                content[: sum(len(x) for x in lines[: last_img_idx + 1])]
                + insert_block
                + content[sum(len(x) for x in lines[: last_img_idx + 1]):]
            )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)


def already_relevant(line: str, content: str) -> bool:
    m = re.search(r"/(\d+)\.jpg\)", line)
    return bool(m and m.group(0) and m.group(0) in content)


def create_page(slug: str, member: str, numbers: list[str]) -> str:
    """Create a brand-new member page and return its path."""
    path = page_path(slug)
    if os.path.exists(path):
        raise SystemExit(
            f"error: {path} already exists; use the update path instead of create"
        )
    images = "\n".join(
        image_line(member, slug, n) for n in numbers
    )
    content = NEW_PAGE_TEMPLATE.format(title=member, images=images)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def add_member_to_index(slug: str, member: str) -> bool:
    """Add a new member entry to pages/fotos-van-leden.md if missing.

    Returns True when an entry was added, False when it already existed.
    """
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if f"/fotos-van-leden/{slug}" in content:
        return False
    line = f"- [{member}](fotos-van-leden/{slug}/)\n"
    # Insert before the closing "---" that precedes the "Voor de leden" note,
    # i.e. append after the last existing member bullet under "## Leden".
    marker = "\n---\n"
    idx = content.find(marker)
    if idx == -1:
        # Fall back: append at end of file.
        new_content = content
        if not new_content.endswith("\n"):
            new_content += "\n"
        new_content += line
    else:
        head = content[:idx]
        tail = content[idx:]
        if not head.endswith("\n"):
            head += "\n"
        head += line
        new_content = head + tail
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def add_nav_entry(slug: str, member: str) -> bool:
    """Add a nested nav entry under the Foto's van leden parent in _includes/nav.html.

    Returns True when an entry was added, False when it already existed.
    """
    nav_path = os.path.join("_includes", "nav.html")
    with open(nav_path, "r", encoding="utf-8") as f:
        content = f.read()
    if f"/pages/fotos-van-leden/{slug}" in content:
        return False
    entry = (
        "        <li><a href=\"{{ '/pages/fotos-van-leden/" + slug + "' | relative_url }}\""
        " class=\"{%- if page.url contains '" + slug + "' %}active{%- endif %}\">"
        + member + "</a></li>\n"
    )
    # Find the Fotos van leden parent block. The first <ul> after the
    # "fotos-van-leden" parent link is the children list.
    parent_idx = content.find("/pages/fotos-van-leden'")
    if parent_idx == -1:
        raise SystemExit(
            "error: could not locate the Foto's van leden parent entry in "
            "_includes/nav.html; refusing to edit nav"
        )
    ul_open = content.find("      <ul>\n", parent_idx)
    if ul_open == -1:
        raise SystemExit(
            "error: could not locate the children <ul> for Foto's van leden in "
            "_includes/nav.html"
        )
    # Append at the end of the children list: insert just before the
    # matching </ul>. Match the first </ul> after the opening <ul>.
    ul_close = content.find("      </ul>", ul_open)
    if ul_close == -1:
        raise SystemExit(
            "error: could not locate the closing </ul> for Foto's van leden in "
            "_includes/nav.html"
        )
    new_content = content[:ul_close] + entry + content[ul_close:]
    with open(nav_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add images to a member photo page (creating it if needed)."
    )
    parser.add_argument("--member", required=True,
                        help="member display name, e.g. \"André Krale\"")
    parser.add_argument("--slug",
                        help="member slug; defaults to the kebab-case of --member")
    parser.add_argument("--numbers", required=True, nargs="+",
                        help="zero-padded image numbers to add, e.g. 01 02 03")
    args = parser.parse_args()

    slug = args.slug or member_slug(args.member)
    path = page_path(slug)

    if os.path.exists(path):
        append_images_to_page(path, args.member, slug, args.numbers)
        created = False
    else:
        create_page(slug, args.member, args.numbers)
        created = True
        add_member_to_index(slug, args.member)
        add_nav_entry(slug, args.member)

    print(f"member: {args.member} (slug: {slug})")
    print(f"page: {path} ({'created' if created else 'updated'})")
    print(f"numbers added: {', '.join(args.numbers)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
