# Navigation Entry Patterns

Reference for the navigation data format used in `_data/navigation.yml`. The sidebar is rendered data-driven by `_includes/nav.html` from this file (AGENTS.md §4.2, §4.4).

## Top-level entry

```yaml
- title: Page Name
  url: "/pages/pagename"
  match: "pagename"
```

## Nested entry under a parent

Add the item under the parent's `children` list:

```yaml
- title: Parent Page
  url: "/pages/parent"
  match: "parent"
  children:
    - title: Child Page
      url: "/pages/parent/child"
      match: "child"
```

## Exact match (equality instead of substring)

Use `exact: true` when the `match` must compare with equality rather than `contains` (used by the homepage):

```yaml
- title: Homepage
  url: "/"
  match: "/"
  exact: true
```

## Match-string rules

- `match` is tested against `page.url` with `contains` by default; set `exact: true` for equality.
- The `match` substring must be unique among all nav entries to avoid cross-highlighting.
- Prefer the full filename stem (without extension) as the substring.
- For entries sharing a prefix (e.g. multiple `fotobespreking-*` pages), use enough of the stem to disambiguate: `fotobespreking-8-oktober` not `fotobespreking-8`.
- Nested children should use a `match` that does not match the parent, otherwise both highlight simultaneously.

## Existing parents (subdirectories under pages/)

- `pages/fotobespreking-werkwijze/`
- `pages/fotos-actueel/`
- `pages/fotos-archief/`
- `pages/fotos-van-leden/`

When adding a page that belongs under one of these, place the file under the subdirectory and add an item to that parent's `children` list.

## Order

The menu renders in YAML list order. To reorder, move entries within `_data/navigation.yml`.

## Layout constraints

- Navigation depth must not exceed 2 levels (parent + children) per AGENTS.md §9.2.
- Do not introduce a third nesting level.
