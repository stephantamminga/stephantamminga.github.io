---
name: add-sub-page
description: Create a new content sub-page for the Fotoclub Beeldspraak Jekyll site. Use when adding a new page under pages/, including updating the sidebar navigation and (optionally) adding content images. Activates on requests to "add a page", "new sub-page", "maak een pagina", or any task that produces a new route under /pages/.
---

# Add Sub-Page

Follow these instructions to add a new content page to the Jekyll site.

## Inputs

Confirm before starting:

- Page filename (lowercase kebab-case, `.md`), e.g. `nieuws-2026-herfst`.
- Page title (Dutch), shown as the `<h2>` heading.
- Target nav location: top-level entry, or nested under an existing parent `<li>`.
- Whether the page uses content images (determines whether image assets are needed).

## Procedure

1. Create the page file at `pages/<filename>.md`.
   - Use the template in [assets/page-template.md](assets/page-template.md).
   - Set `layout: page` and `title:` in front matter (both required by AGENTS.md §8.4).
   - Do not create a new layout; only `default` and `page` exist (AGENTS.md §3.3).
2. If the page has a parent (e.g. a fotobespreking under `fotos-actueel` or `fotos-archief`), place the file under the matching subdirectory: `pages/<parent>/<filename>.md`.
3. Add a navigation entry in `_data/navigation.yml` following the pattern in [references/nav-entry-patterns.md](references/nav-entry-patterns.md). The template `_includes/nav.html` renders the menu from this file; do not edit the template.
   - Top-level: append a new item to the top-level list.
   - Nested: add an item under the parent's `children` list.
   - Set `title`, `url`, and `match` (substring tested against `page.url`); use `exact: true` only when the match must be an exact equality (e.g. the homepage).
   - Choose a `match` substring unique to the new page (see references).
4. If the page references images:
   - Store web-optimized production images under `assets/images/content/` (AGENTS.md §9.3, §9.4).
   - Reference them with Liquid `relative_url`: `{{ '/assets/images/content/<file>.jpg' | relative_url }}`.
   - For lightbox-enabled images, use the image-with-caption pattern (img + sibling `.photo-caption` div) so `main.js` collects them (AGENTS.md §8.3.3, §7.2.2).
5. Add content below the front matter. Use `h3`+ for in-page headings; the `page` layout already emits the `h2` title (AGENTS.md §8.2).

## Validation

Before considering the page complete, verify:

- `pages/<filename>.md` exists with valid YAML front matter (`layout: page`, `title:`).
- The new item in `_data/navigation.yml` has `title`, `url`, and `match` (the template applies `relative_url`).
- The `match` substring is unique and does not accidentally match other nav entries.
- All image paths resolve under `assets/images/` and use `relative_url`.
- No new layout, plugin, or CSS file was introduced.
- Content images are web-optimized (≤1200px width, <500KB per file per AGENTS.md §9.3).

## Output

Report:

- The page path created (`pages/<filename>.md`).
- The navigation entry added and its active-state substring.
- Any images added and their paths.
- Confirmation that validation passed.

## Actions requiring approval

Do not, without explicit request:

- modify `_layouts/` or `_config.yml`;
- create new navigation top-level groups unrelated to the requested page;
- delete or reorder existing nav entries;
- push or merge to `main` (this skill creates local changes only unless told otherwise).

## Edge cases

- Duplicate substrings: if the chosen substring already appears in another nav entry, lengthen it (e.g. `'fotobespreking-8-oktober'` rather than `'fotobespreking-8'`).
- No parent: top-level pages go directly under `pages/` and get a standalone `<li>`.
- Homepage: do not use this skill for `index.md`, which uses `layout: default` (AGENTS.md §3.2).
