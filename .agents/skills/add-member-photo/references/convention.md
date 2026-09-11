# Member photo page convention

Reference for the layout, naming, and image syntax used by member photo
pages under `pages/fotos-van-leden/`. Load this when adding or checking a
member's page.

## Files

- Member pages: `pages/fotos-van-leden/<member-slug>.md`
- Member images: `assets/images/content/<member-slug>/<NN>.jpg`
- Member index: `pages/fotos-van-leden.md` (the "Foto's van leden" overview)
- Nav parent: the "Foto's van leden" item in `_data/navigation.yml`, whose
  `children` list every member as a nested entry. `_includes/nav.html` renders
  the menu from this file.

## Member slug

- Lowercase kebab-case derived from the member's display name, e.g.
  `André Krale` → `andre-krale`, `Stephan Tamminga` → `stephan-tamminga`,
  `Jan Albert Bleeker` → `jan-albert-bleeker`.
- The page file, image folder, and nav/index link all share this slug.
- If a member supplies a preferred slug explicitly, honor it via
  `update_page.py --slug`.

## Page front matter

```yaml
---
layout: page
title: <Member display name>
parent: Foto's van leden
---
```

- `layout: page` is required (AGENTS.md §8.4.1).
- `title` is the member's display name, preserving capitalization and
  accents exactly.
- `parent: Foto's van leden` matches the existing member pages so the
  breadcrumb / sidebar relationship stays consistent.

## Image lines

Member pages use plain Markdown image syntax (not the `photo-highlight`
block used on "Foto van de maand"). The page `<h1>` is followed by a
hint line, then one image line per photo:

```markdown
# <Member display name>

(klik op de foto voor grote weergave)

![© <Member display name>](/assets/images/content/<member-slug>/01.jpg)
![© <Member display name>](/assets/images/content/<member-slug>/02.jpg)
```

- The `alt` text is always `© <Member display name>` and is identical for
  every image on the page.
- `js/main.js` collects every `<img>` in the content area for the
  lightbox, so the Markdown image syntax alone is sufficient; no separate
  `.photo-caption` div is used on member pages.

## Numbering

- Images are named with a zero-padded number: `01.jpg`, `02.jpg`, …
- Numbers are assigned by `next_number.py` as `max(existing NN) + 1`.
- From 100 upward the number is no longer zero-padded to two digits
  (`100.jpg`, `101.jpg`, …).
- Never reuse a number; never create gaps.

## Placeholder pages

Some members have an empty page with a placeholder line instead of
images:

```markdown
*Deze pagina heeft nog geen foto's. Foto's kunnen door het lid worden aangeleverd aan de webmaster.*
```

When adding the first real images to such a page, `update_page.py`
removes the placeholder line and inserts the image lines in its place.

## Member index entry

The overview page `pages/fotos-van-leden.md` lists members under
`## Leden` as Markdown links:

```markdown
- [<Member display name>](fotos-van-leden/<member-slug>/)
```

The link target ends with a trailing slash so Jekyll renders the
`<member-slug>/index.html` generated from `<member-slug>.md`.

## Nav entry

New members get a nested item under the "Foto's van leden" parent's `children`
list in `_data/navigation.yml`, following the existing active-state pattern:

```yaml
- title: <Member display name>
  url: "/pages/fotos-van-leden/<member-slug>"
  match: "<member-slug>"
```

The `match` substring is the member slug, which is unique per member.

## Real examples

| Member            | Page                              | Slug                  |
|-------------------|-----------------------------------|-----------------------|
| Stephan Tamminga  | `pages/fotos-van-leden/stephan-tamminga.md` | `stephan-tamminga` |
| Gerrit Scheeres   | `pages/fotos-van-leden/gerrit-scheeres.md`  | `gerrit-scheeres`  |
| André Krale       | `pages/fotos-van-leden/andre-krale.md`      | `andre-krale`      |
