---
name: add-member-photo
description: Add one or more photos to a member's photo page on the Fotoclub Beeldspraak site (pages/fotos-van-leden/). Resizes each image to max 2048x2048, stores it under assets/images/content/<member-slug>/ with the next incremental number, and appends the image to the member page. Creates the page, image folder, nav entry, and index link when the member does not yet have a page. Use when asked to add, upload, or publish photos for a member ("voeg foto's toe voor <lid>", "upload foto's voor <lid>", "nieuwe foto's voor <lid>"), or when a user supplies member photos. If the member name or images are missing, ask the user before proceeding.
---

# Add member photo

Follow these instructions to add one or more photos to a member's photo
page, creating the page if it does not yet exist.

## Required inputs

Collect all of the following before doing any file work. If any are
missing, stop and ask the user (use the agent's interactive question
mechanism):

- **Member display name** — the member's full name as it appears in the
  member index and nav, e.g. "André Krale", "Jan Albert Bleeker". Preserve
  capitalization and accents exactly. Do not guess; ask if unsure.
- **One or more image files** — the photos to add. Accept any common raster
  format (JPEG, PNG, TIFF, WebP). If supplied as paths, use them directly;
  otherwise write each to a temporary file first.

Optionally confirm:

- **Member slug** — if the member wants a slug different from the
  kebab-case of their display name, supply it explicitly via
  `update_page.py --slug`. Otherwise the slug is derived automatically.

## Convention

See [references/convention.md](references/convention.md) for the page
layout, slug, numbering, and image syntax. The member pages use plain
Markdown image syntax (one `![© <Member>](...)` line per photo); do not
use the `photo-highlight` block here.

## Procedure

Run all commands from the repository root.

1. **Derive the member slug and image directory.**

   The slug is the lowercase kebab-case of the member display name unless
   overridden. The image directory is
   `assets/images/content/<member-slug>/`.

2. **For each supplied image, determine the next number and resize it.**

   Process the images one at a time so each gets a unique incremental
   number. For each image:

   ```bash
   NN=$(python3 .agents/skills/add-member-photo/scripts/next_number.py \
       --dir assets/images/content/<member-slug>)
   mkdir -p assets/images/content/<member-slug>
   python3 .agents/skills/add-member-photo/scripts/resize_image.py \
       --input <source-image> \
       --output assets/images/content/<member-slug>/$NN.jpg
   ```

   - `next_number.py` prints the highest existing `<NN>` plus one,
     zero-padded to two digits (three from 100 up). Between calls the new
     file is on disk, so the next call sees the incremented count.
   - The resize script downscales so the longest side is at most 2048px,
     preserving aspect ratio, only shrinks (never upscales), outputs
     baseline JPEG, and applies EXIF orientation so phone photos appear
     upright.
   - Requires Pillow (`pip3 install Pillow`). If Pillow is unavailable,
     report the blocker; do not store an un-resized image.
   - Collect every assigned `NN` for the next step.

3. **Update (or create) the member page.**

   ```bash
   python3 .agents/skills/add-member-photo/scripts/update_page.py \
       --member "<Member display name>" \
       --numbers <NN1> <NN2> ...
   ```

   - If the member page `pages/fotos-van-leden/<member-slug>.md` already
     exists, the script appends the new image lines after the last existing
     image line, preserving the page's order. For a placeholder-only page
     (`*Deze pagina heeft nog geen foto's…*`) it replaces the placeholder
     with the new images.
   - If the member page does not exist, the script:
     - creates `pages/fotos-van-leden/<member-slug>.md` from the template
       (front matter `layout: page`, `title`, `parent: Foto's van leden`,
       plus a `# <Member>` heading and the image lines);
     - adds a Markdown link entry to the member index
       `pages/fotos-van-leden.md` under `## Leden`;
     - adds a nested item to the "Foto's van leden" parent's `children` in
       `_data/navigation.yml` using the existing active-state pattern (the
       template `_includes/nav.html` renders the menu from this file).
   - Pass `--slug <member-slug>` only when overriding the derived slug.
   - Run a `git diff` after this step and confirm only the expected files
     changed (the image(s), the member page, and — for new members — the
     index and `nav entry in _data/navigation.yml`).

4. **Do not edit** `_layouts/`, `_config.yml`, `js/main.js`, or `css/`.
   The lightbox already handles plain `<img>` elements in the content area, so
   no JS or layout change is needed. (`_data/navigation.yml` is edited only to
   add a new member's nav entry, per step 3.)

## Validation

Before considering the task complete, verify:

- Each `assets/images/content/<member-slug>/<NN>.jpg` exists, is a JPEG,
  and its longest side is ≤ 2048px. Check with:
  ```bash
  python3 -c "from PIL import Image; im=Image.open('assets/images/content/<member-slug>/<NN>.jpg'); print(im.format, im.size)"
  ```
- `pages/fotos-van-leden/<member-slug>.md` contains exactly one new
  `![© <Member>](/assets/images/content/<member-slug>/<NN>.jpg)` line per
  added image, and no existing lines were altered.
- For a new member: the index `pages/fotos-van-leden.md` has a new
  `- [<Member>](fotos-van-leden/<member-slug>/)` entry, and
  `_data/navigation.yml` has a new nested item under the "Foto's van leden"
  parent with `match: <member-slug>` (a unique substring).
- The page still builds: if Jekyll is available, run
  `bundle exec jekyll build` and confirm no errors; otherwise confirm the
  markdown is well-formed by eye.
- No unrelated files were modified (`git status` shows only the new
  image(s), the member page, and — for new members — the index and nav).

## Output

Report:

- The member display name and slug.
- The stored image path(s) and final dimension(s).
- The exact `alt` text used (always `© <Member display name>`).
- Whether the page was created or updated.
- For a new member: confirmation that the index and nav entries were
  added.
- A short diff summary (which files changed).

## Actions requiring approval

Do not, without explicit request:

- overwrite or delete an existing `<NN>.jpg`;
- reorder, edit, or remove existing image lines on the page;
- modify the member's `title` or slug of an existing page;
- modify `_layouts/`, `_config.yml`, `js/main.js`, `css/`, or data files;
- push, merge, or commit to `main` (this skill produces local changes only
  unless told otherwise).

## Edge cases

- **First photos for an existing placeholder page:** the script removes
  the `*Deze pagina heeft nog geen foto's…*` line and inserts the images.
- **Duplicate number:** `next_number.py` always returns max+1, so
  duplicates are never created; do not reuse numbers from removed photos.
- **Image already ≤ 2048px:** the resize script keeps it as-is (only
  shrinks) but still re-encodes as JPEG and applies EXIF orientation.
- **Non-JPEG source:** accepted; output is always JPEG regardless of
  input format.
- **Many images at once:** process them sequentially so each
  `next_number.py` call reflects the previously stored file; record every
  assigned `NN` and pass them all to `update_page.py --numbers` in one call.
- **Slug collision:** if the derived slug already belongs to a different
  member, ask the user for an explicit `--slug` before proceeding.
