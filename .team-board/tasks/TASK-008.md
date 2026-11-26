# TASK-008

## Brief
Read `.team-board/01-blueprint.md` first. Final layout polish from Conductor screenshot review of the running site. Every item below was observed on the live page, not guessed. Fix dead space and ragged grids; do not redesign.

1. `berita/berita.html` — featured card (`md:grid-cols-5`) is ~480px tall because the image column is `aspect-[2/3]` uncapped, so the text column shows a title, one line of excerpt, then ~250px of blank before the CTA. Cap the image column (`max-h-[320px]` with `aspect-[2/3]`) and vertically distribute the text column (`justify-center` on the content wrapper, CTA still `mt-auto` inside a `flex flex-col`). Target card height 300-340px at `md` and up.
2. `berita/berita.html` — hero H1 accent word "Informasi" uses `text-accent-bright`/`text-accent` on the blue band (fails contrast). Use `text-highlight` (#F2B84B) on the blue, same treatment already applied to the ekstrakurikuler H1.
3. `index.html` — "Berita & Prestasi" grid is ragged: featured `md:col-span-2` + 1 card + 1 card leaves two empty slots. Change to: featured card `md:col-span-3` as a horizontal split (image left `md:col-span-1` portrait, text `md:col-span-2`), then the remaining news in a `md:grid-cols-2` row below. No empty slots with 3 items.
4. `index.html` — "Pusat Keunggulan" right column: the Leadership card stretches to the height of the taller left card, leaving ~200px of blank inside. Add `items-start` to the grid and remove `h-full` from the right column cards so each card hugs its content.
5. `index.html` — statistics bento: the dark "Monitoring" tile contains a large inner empty-state panel. Make it compact (single line note, `py-6`, no nested card) so the tile does not dominate the grid.
6. `profil/fasilitas.html` — mosaic tiles are far too tall: the featured tile is ~900px and the "Perpustakaan Digital" card has ~200px of blank under its spec row. Cap image tiles at `max-h-[420px]` with `object-cover`, set `grid-auto-rows: minmax(180px, auto)`, and let the text cards hug content (no `h-full` stretch).
7. `program/jurusan/jurusan.html` — "Peluang Karir" blue panel still has a tall blank area under its note row. Remove the fixed height/min-height so it hugs content.

Rules:
- Warm tokens only; no new colors, no new fonts.
- Keep all Django tags, loops, URLs and context variables unchanged.
- No Python changes, no data seeding, do not restart waitress.
- Touch only the four files above.

## Depends
TASK-006, TASK-007.

## Files
- `otak_aplikasi/templates/index.html`
- `otak_aplikasi/templates/berita/berita.html`
- `otak_aplikasi/templates/profil/fasilitas.html`
- `otak_aplikasi/templates/program/jurusan/jurusan.html`

## Test
- `manage.py check` exit 0 (known `ckeditor.W001` acceptable).
- Fresh-process Django Client: `/`, `/berita/`, `/fasilitas/`, `/program-studi/` → 200, no literal `{{`.
- Assert rendered `/berita/` featured image wrapper contains `max-h-[320px]`, and `/` news grid contains `md:col-span-3`.
- Conductor re-screenshots all four pages and confirms no card with more than ~80px of blank space.

## Status
[TASK: TASK-008 READY_FOR_REVIEW]

## Evidence
[EVIDENCE: RED] env\Scripts\python.exe verify_task008.py → exit 1 → routes 200/no `{{`, but `/berita/` missing `max-h-[320px]` and `/` missing `md:col-span-3`
[EVIDENCE: GREEN] env\Scripts\python.exe manage.py check → exit 0 → System check identified 1 issue (ckeditor.W001 only)
[EVIDENCE: GREEN] env\Scripts\python.exe verify_task008.py → exit 0 → GET `/`, `/berita/`, `/fasilitas/`, `/program-studi/` → 200, no literal `{{`, `max-h-[320px]` present in `/berita/`, `md:col-span-3` present in `/`
[EVIDENCE: FULL] All 7 items applied to the four listed templates only. No Python, no new colors/fonts, Django tags/context unchanged, waitress not restarted.
[READY_FOR_REVIEW]

## Review
[REVIEW: spec FAIL]
[REVIEW: quality PASS]

Items 1, 2, 4, 6, 7 verified: featured `max-h-[320px]` + `justify-center` + CTA `mt-auto`, hero accent `text-highlight`, `items-start` with no `h-full` on Pusat Keunggulan right cards, fasilitas `max-h-[420px]` + `grid-auto-rows: minmax(180px,auto)` + `items-start`, jurusan Karir panel with no fixed height. Item 5 note is compact but the tile still spans 2x2. Item 3's `md:col-span-3` / `md:grid-cols-2` split is in place; the "portrait" part is not.

[FINDING: High] otak_aplikasi/templates/index.html:697 — item 3 requires the featured image column to be portrait; it is `md:col-span-1 h-56 md:h-auto md:min-h-[260px] max-h-[320px]` with no `aspect-[2/3]`, so the image renders landscape and crops the 4:6 photo. — Same fix as TASK-007: `aspect-[2/3]` plus a width cap (`md:max-w-[213px]`) under `max-h-[320px]`, drop `h-56`/`md:min-h-[260px]`.
[FINDING: Low] otak_aplikasi/templates/index.html:202 — item 5: the empty Monitoring state is compact (`py-6`, one line), but the article keeps `lg:row-span-2` (2x2), so the empty tile still dominates the bento. — Move `lg:row-span-2` inside `{% if school_stats %}` so the empty variant is a 2x1 tile.
[FINDING: Low] otak_aplikasi/templates/index.html:725-757 — with exactly 2 news items the featured card takes the full row and the nested `md:grid-cols-2` renders one half-width card, leaving an empty slot. — Render the remaining card `md:col-span-2` when `berita_list|length == 2`.

Evidence RED/GREEN present and consistent with the four listed files; scope check by mtime shows only `berita.html`, `index.html`, `fasilitas.html`, `jurusan.html` touched at 11:12-11:13.

## Fix round (review findings)
[EVIDENCE: RED] Reviewer High finding = failing state: `index.html:697` featured news image `md:col-span-1 h-56 md:h-auto md:min-h-[260px] max-h-[320px]` had no `aspect-[2/3]`, rendering a landscape band that crops 4:6 photos.
[EVIDENCE: GREEN] `env\Scripts\python.exe manage.py check` → exit 0 → System check identified 1 issue (ckeditor.W001 only).
[EVIDENCE: GREEN] `verify_task008_fix.py` (fresh process, Django Client) → exit 0 → GET `/` 200, no literal `{{`; featured news container class list = `relative md:col-span-1 aspect-[2/3] overflow-hidden` (no `h-56`, no `max-h-[320px]`); teaser `max-h-[380px]` removed and remaining cards moved to `md:grid-cols-3`; `/search/?q=berita` 200 with `aspect-[2/3]` and no clamping `max-h-*`; `berita.html` pagination links now have `focus:ring-2 focus:ring-primary focus:outline-none`.
[EVIDENCE: FULL] Scope = `index.html` featured portrait + teaser grid, `search_results.html` caps, `berita/berita.html` pagination focus rings. No Python, no other files, waitress not restarted.
[READY_FOR_REVIEW]
