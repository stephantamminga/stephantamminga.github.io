---
name: add-foto-van-de-maand
description: Add a new "Foto van de maand" entry to the Fotoclub Beeldspraak site. Resizes an image to max 2048x2048, stores it under assets/images/content/foto-van-de-maand/ with the next incremental number, and prepends a new photo-highlight block to pages/foto-van-de-maand.md with a credit caption. Use when asked to add, upload, or publish a new "foto van de maand", or when a user supplies a photo of the month. If the maker, month, or title are missing, ask the user before proceeding.
---

# Add Foto van de maand

Follow these instructions to add a new "Foto van de maand" entry.

## Required inputs

Collect all of the following before doing any file work. If any are missing, stop and ask the user (use the agent's interactive question mechanism):

- **Image file** — the new photo. Accept any common raster format (JPEG, PNG, TIFF, WebP). If the image is supplied as a path, use it directly; if supplied another way, write it to a temporary file first.
- **Maker** — the photographer's full name as it appears in existing captions (e.g. "André Krale", "Liesbeth Timmermans"). Preserve capitalization and accents exactly.
- **Month** — the Dutch month name + year, lowercase month, e.g. "januari 2026", "november 2025". Use the Dutch month names: januari, februari, maart, april, mei, juni, juli, augustus, september, oktober, november, december.
- **Title** — optional free-text description of the photo, e.g. "Thema: It's so good", "Queen II", "Geel". May be omitted; the caption then has no title suffix.

Do not guess the maker, month, or title. Only proceed once all required fields are confirmed.

## Caption format

The caption text is shared between the `<img alt>` and the `.photo-caption` div, and is identical in both. Build it exactly as:

```
© <Maker> - <month>
```

and, **only if a title is given**, append a comma and the title:

```
© <Maker> - <month>, <Title>
```

Rules (see [references/convention.md](references/convention.md) for examples and the full convention):

- Copyright sign is the literal `©`.
- Separator between maker and month is ` - ` (space hyphen space).
- Title, when present, is separated by `, ` (comma space) from the month.
- Preserve the maker's exact punctuation and accents.
- Do not add extra commentary, periods at the end, or reformat the title.

## Procedure

1. **Determine the next number.**
   - Images live in `assets/images/content/foto-van-de-maand/` and are named `<NN>.jpg` with zero-padded two-digit numbers (`01.jpg` … `31.jpg`).
   - The next number is the highest existing `<NN>` plus one, formatted as two digits. When the count reaches 100, keep three digits (`100.jpg`) and continue.
   - Use the helper:
     ```bash
     python3 .agents/skills/add-foto-van-de-maand/scripts/next_number.py
     ```
     It prints the next number (e.g. `32`). If it ever disagrees with a manual count, trust the script.

2. **Resize and store the image.**
   ```bash
   python3 .agents/skills/add-foto-van-de-maand/scripts/resize_image.py \
       --input <source-image> \
       --output assets/images/content/foto-van-de-maand/<NN>.jpg
   ```
   - The script downscales so the longest side is at most 2048px, preserving aspect ratio, and only shrinks (never upscales).
   - Output is baseline JPEG, and it rotates the image according to EXIF orientation so phone photos appear upright.
   - Requires Pillow (`pip3 install Pillow`). If Pillow is unavailable, report the blocker; do not store an un-resized image.

3. **Update `pages/foto-van-de-maand.md`.**
   ```bash
   python3 .agents/skills/add-foto-van-de-maand/scripts/update_page.py \
       --number <NN> \
       --maker "<Maker>" \
       --month "<month>" \
       [--title "<Title>"]
   ```
   - The script prepends a new `photo-highlight` block immediately after the intro paragraph (the first line(s) of body content before the first `<div class="photo-highlight">`), so the newest photo stays at the top of the page, matching the existing newest-first ordering.
   - It generates the block using the caption format above, with identical text in `alt` and `.photo-caption`.
   - It reuses the existing `{{ '/assets/images/content/foto-van-de-maand/<NN>.jpg' | relative_url }}` path convention.
   - Run a git diff after this step and confirm only one new block was added and nothing else changed.

4. **Do not edit** `_includes/nav.html`, `_layouts/`, `_config.yml`, or any data files. The "Foto van de maand" nav entry already exists; the page is a single growing list.

## Validation

Before considering the task complete, verify:

- `assets/images/content/foto-van-de-maand/<NN>.jpg` exists, is a JPEG, and its longest side is ≤ 2048px. Check with:
  ```bash
  python3 -c "from PIL import Image; im=Image.open('assets/images/content/foto-van-de-maand/<NN>.jpg'); print(im.format, im.size)"
  ```
- `pages/foto-van-de-maand.md` contains exactly one new `photo-highlight` block referencing `<NN>.jpg`, placed above all prior blocks and below the intro text.
- The `alt` attribute and the `.photo-caption` text are identical and match the caption format.
- The page still builds: if Jekyll is available, run `bundle exec jekyll build` and confirm no errors; otherwise confirm the markdown is well-formed by eye.
- No unrelated files were modified (`git status` shows only the new image and the page).

## Output

Report:

- The assigned number (`<NN>`).
- The stored image path and its final dimensions.
- The exact caption text used.
- Confirmation that the page was updated and validation passed.
- A short diff summary (one new block added).

## Actions requiring approval

Do not, without explicit request:

- overwrite or delete an existing `<NN>.jpg`;
- reorder, edit, or remove existing photo blocks on the page;
- modify `_includes/nav.html`, `_layouts/`, `_config.yml`, or data files;
- push, merge, or commit to `main` (this skill produces local changes only unless told otherwise).

## Edge cases

- **Missing caption inputs:** ask the user for maker, month, and (optionally) title before resizing or writing any file.
- **Gap in numbering:** `next_number.py` always returns max+1, so gaps are never created; do not reuse numbers from removed photos.
- **Image already ≤ 2048px:** the resize script keeps it as-is (only shrinks) but still re-encodes as JPEG and applies EXIF orientation.
- **Non-JPEG source:** accepted; output is always JPEG regardless of input format.
- **Animated/non-photographic content:** this page is for photos only; if the source is clearly not a photo, confirm with the user before proceeding.
- **Duplicate (maker, month) already on the page:** a month normally has one photo; if the same month already exists, confirm with the user before adding a second.
