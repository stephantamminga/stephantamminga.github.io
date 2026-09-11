# Foto van de maand convention

Reference for the layout, numbering, and caption format used by the
"Foto van de maand" page. Load this when building or checking captions.

## Files

- Page: `pages/foto-van-de-maand.md`
- Images: `assets/images/content/foto-van-de-maand/<NN>.jpg`
- Nav entry: already present in `_includes/nav.html` as a single top-level
  `<li>` linking to `/pages/foto-van-de-maand`. Do not add another entry.

## Numbering

- Images are named with a zero-padded number: `01.jpg`, `02.jpg`, … `31.jpg`.
- The newest photo has the **highest** number; the oldest has `01.jpg`.
- The page lists photos newest-first (highest number at the top).
- A new entry gets `max(existing NN) + 1`. From 100 upward the number is no
  longer zero-padded to two digits (use `100.jpg`, `101.jpg`, …).
- Never reuse a number; never create gaps.

## Block structure

Each photo is a `photo-highlight` block. The image `src` uses the Liquid
`relative_url` filter; the `alt` and the `.photo-caption` text are identical.

```html
<div class="photo-highlight">
  <img src="{{ '/assets/images/content/foto-van-de-maand/31.jpg' | relative_url }}" alt="© André Krale - januari 2026, Thema: It's so good">
  <div class="photo-caption">© André Krale - januari 2026, Thema: It's so good</div>
</div>
```

The `photo-highlight` wrapper plus the sibling `.photo-caption` div is what
`js/main.js` uses for the lightbox caption and click-to-open behavior
(AGENTS.md §8.3.3, §7.2.2). Keep the structure intact.

## Caption format

Base form (no title):

```
© <Maker> - <month>
```

With a title:

```
© <Maker> - <month>, <Title>
```

- `©` is the literal copyright sign.
- Maker and month are separated by ` - ` (space, hyphen, space).
- Title, when present, is separated from the month by `, ` (comma, space).
- Preserve the maker's exact spelling, capitalization, and accents
  (e.g. `André`, not `Andre`).
- Do not add a trailing period or extra commentary.

### Real examples from the page

| File    | Caption                                                          |
|---------|------------------------------------------------------------------|
| 31.jpg  | © André Krale - januari 2026, Thema: It's so good                |
| 30.jpg  | © Liesbeth Timmermans - april 2026                               |
| 29.jpg  | © André Krale - januari 2026, Thema: Een nieuwe start            |
| 28.jpg  | © Rinske Hokwerda - november 2025, Thema: Fine art in architecture |
| 27.jpg  | © Guido Kamp - oktober 2025, ingang/uitgang                      |
| 26.jpg  | © Stephan Tamminga - september 2025, Queen II                    |
| 19.jpg  | © Brenda de Vries - oktober 2024                                 |
| 11.jpg  | © Stephan Tamminga - november 2023                               |

Note that some captions omit the title entirely (e.g. `30.jpg`, `19.jpg`,
`11.jpg`) and some include a "Thema:" prefix within the free-text title
(e.g. `31.jpg`, `29.jpg`). The title is free text supplied by the user;
do not reformat it.

## Dutch month names

januari, februari, maart, april, mei, juni, juli, augustus, september,
oktober, november, december.

The month in the caption is lowercase Dutch, followed by the four-digit
year, e.g. `november 2025`.
