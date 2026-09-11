# Navigation Entry Patterns

Reference for the active-state navigation patterns used in `_includes/nav.html`. The site uses a vertical sidebar with manual HTML and Liquid `page.url contains` matching (AGENTS.md §4.2, §4.4).

## Top-level entry

```html
<li><a href="{{ '/pages/pagename' | relative_url }}" class="{%- if page.url contains 'pagename' %}active{%- endif %}">Page Name</a></li>
```

## Nested entry under a parent

The parent `<li>` contains its own `<a>`, followed by a `<ul>` of children:

```html
<li>
  <a href="{{ '/pages/parent' | relative_url }}" class="{%- if page.url contains 'parent' %}active{%- endif %}">Parent Page</a>
  <ul>
    <li><a href="{{ '/pages/parent/child' | relative_url }}" class="{%- if page.url contains 'child' %}active{%- endif %}">Child Page</a></li>
  </ul>
</li>
```

## Active-state substring rules

- The substring passed to `page.url contains` must be unique among all nav entries to avoid cross-highlighting.
- Prefer the full filename stem (without extension) as the substring.
- For entries sharing a prefix (e.g. multiple `fotobespreking-*` pages), use enough of the stem to disambiguate: `'fotobespreking-8-oktober'` not `'fotobespreking-8'`.
- Nested children should use a substring that does not match the parent, otherwise both highlight simultaneously.

## Existing parents (subdirectories under pages/)

- `pages/fotobespreking-werkwijze/`
- `pages/fotos-actueel/`
- `pages/fotos-archief/`
- `pages/fotos-van-leden/`

When adding a page that belongs under one of these, place the file under the subdirectory and add a nested `<li>` to that parent's `<ul>`.

## Layout constraints

- Navigation depth must not exceed 2 levels (parent + children) per AGENTS.md §9.2.
- Do not introduce a third nesting level.
