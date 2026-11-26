# TASK-007

## Brief
Read `.team-board/01-blueprint.md` first. News photos are uploaded in **4:6 portrait** (2:3). Current layouts force landscape boxes (`h-64`, `h-80`, `400x300`) with `bg-cover`, so portrait photos get badly cropped and cards carry large empty areas. Fix the ratio, the card composition, and the pagination.

### A. Portrait ratio everywhere a news image appears
- Use `aspect-[2/3]` (same as 4:6) for news image boxes. No fixed `h-64`/`h-80`/`h-[400px]` news image bands.
- Keep `object-cover` / `bg-cover bg-center`. Never stretch (`object-fill`).
- Applies to: `berita/berita.html` (hero + featured + compact cards), `berita/detail_berita.html` (article image, related/trending thumbs), `index.html` (Berita & Prestasi cards + hero news panel), `search_results.html` (result thumbs).
- Compact thumbnails stay small but portrait: `w-20 aspect-[2/3]` instead of `size-20`.

### B. Card composition: no dead space
News text fields available: `title`, `content` (rich text), `category.name`, `created_at`, `view_count`, `image`, `video`.

- Featured card (first item, page 1 and every page): horizontal split on desktop, `md:grid-cols-5`. Image column `md:col-span-2` with `aspect-[2/3]`; content column `md:col-span-3` with category chip, title `line-clamp-3`, excerpt `line-clamp-4` (`{{ berita.content|default:""|striptags|truncatewords:40 }}`), meta row (date + views), CTA at the bottom. Content column must fill the image height (`flex flex-col`, CTA `mt-auto`) so no gap under the text.
- Remaining cards: vertical cards in `md:grid-cols-3`, image `aspect-[2/3]`, then category chip, title `line-clamp-3`, excerpt `line-clamp-2` (`truncatewords:18`), meta row. Equal heights via `h-full` + `flex flex-col`, CTA `mt-auto`.
- Never render an empty `<p>` when `content` is empty; use `{% if berita.content %}`.
- No leftover `image-zoom` hover class on containers that no longer hold an image.

### C. Server-side pagination (replace client-side JS)
`otak_aplikasi/views.py` `berita()` currently disables the Paginator and ships every row to the browser; `berita.html` then hides cards with JS and injects buttons via `innerHTML`. Replace with real pagination.

1. In `views.py` `berita()`:
   - Apply `kategori_filter` and `search_query` **before** selecting the featured item, so the featured article matches the filter.
   - `Paginator(berita_list, 7)` → `page_obj = paginator.get_page(page_number)`.
   - Featured = `page_obj.object_list[0]` when the page has items; remaining = `page_obj.object_list[1:]`.
   - Pass `page_obj`, `berita_utama`, `berita_lainnya`, keep `kategori_list`.
   - Keep the existing cache wrapper but include `page_number` in the key (already present).
   - Return 404 for out-of-range pages? No — `get_page()` already clamps. Keep that.
2. In `berita.html`:
   - Delete the whole inline pagination `<script>` block and the `id="pagination-nav"`/`pagination-container` JS targets.
   - Render Django pagination: previous/next + page numbers with ellipsis, `?page=N` links preserving `search` and `kategori` query params (`?search=...&kategori=...&page=N`).
   - Current page: `bg-primary text-surface` with `aria-current="page"`; others: `border border-line hover:bg-sand text-muted hover:text-primary`.
   - Wrap in `<nav aria-label="Navigasi Halaman">`; hide the whole nav when `page_obj.paginator.num_pages == 1`.
   - Pagination must work without JavaScript.
3. Empty state stays as is, but change `py-24` to `py-12`.

### D. Hero of berita page
Hero image panel (`berita.html:72`) uses `lg:h-[400px]` with a landscape band. Make it a portrait panel: `aspect-[2/3]` capped by `max-h-[420px]` with `object-cover`, so the 4:6 photo shows most of its frame. Keep the "BERITA UTAMA" overlay and title at the bottom over a dark gradient.

## Depends
TASK-005 (null-safe + placeholder), TASK-006 (index.html empty states).

## Files
- `otak_aplikasi/views.py` — `berita()` function only
- `otak_aplikasi/templates/berita/berita.html`
- `otak_aplikasi/templates/berita/detail_berita.html`
- `otak_aplikasi/templates/index.html`
- `otak_aplikasi/templates/search_results.html`

## Interfaces
View context for `berita.html`: `page_obj`, `berita_utama`, `berita_lainnya`, `kategori_list`. No other view changes. No model or migration changes.

## Test
- `manage.py check` exit 0 (known `ckeditor.W001` acceptable).
- Fresh-process Django Client: `/berita/` 200; `/berita/?page=1` 200; `/berita/?kategori=<existing slug>` 200 and the featured card matches that category; `/berita/?search=berita` 200.
- Rendered `/berita/` HTML contains no `pagination-container` id and no `<script>` pagination block, and contains `?page=` links when more than one page exists.
- Assert each news image container class list contains `aspect-[2/3]` and no `h-64`/`h-80`.
- Do not restart the running waitress.

## Status
[TASK: TASK-007 ready_for_review]

## Evidence

[EVIDENCE: RED] `env\Scripts\python.exe task007_verify.py` (fresh process, Django Client) → exit 1 → 4/13 pass: `page_obj` missing, `pagination-container` present, inline pagination JS present, no `aspect-[2/3]`, `h-64`/`h-80`/`h-[400px]` bands present.

[EVIDENCE: GREEN] `manage.py check` → exit 0 (only known `ckeditor.W001`).
[EVIDENCE: GREEN] `task007_verify.py` → exit 0 → 35/35 pass:
- `/berita/` 200, `page_obj` present, per_page 7, `berita_utama` = first of page, `berita_lainnya` = rest.
- `/berita/?page=1` 200; `/berita/?kategori=berita` 200 + featured and all page items match the category; `/berita/?search=berita` 200 + all page items match query.
- Rendered HTML: no `pagination-container`, no `id="pagination-nav"`, no `itemsPerPage`/`renderPagination`; every news `<figure>` carries `aspect-[2/3]`; no `h-64 md:h-80`, no `h-48`, no `h-[400px]`.
- Synthetic 10-page context: page numbers + ellipsis, `aria-current="page"`, `?search=...&kategori=...&page=N` preserved, prev/next links.
- `/` 200 + portrait cards; `/search/` 200; news detail 200 + `aspect-[2/3]` article image.
- Stale pre-deploy cache entry ignored (`'page_obj' in cached_data` guard).
- Running waitress not restarted; no model/migration changes.

[EVIDENCE: FULL] Scope = `berita()` in `otak_aplikasi/views.py` + `berita/berita.html`, `berita/detail_berita.html`, `index.html`, `search_results.html`. Nothing else touched.

[READY_FOR_REVIEW]

## Review
[REVIEW: spec FAIL]
[REVIEW: quality FAIL]

View (`berita()`), `berita.html` pagination, featured split, card composition and hero panel all match sections B/C/D: filters before featured, `Paginator(..., 7)`, `page_obj`/`berita_utama`/`berita_lainnya`, page in cache key, no inline pagination script, no `pagination-container`, `?page=` links preserve `search`/`kategori`, nav hidden at 1 page, `aria-current="page"`, `aspect-[2/3]` on every `berita.html` figure, no `h-64`/`h-80`/`h-[400px]` news bands. Section A is not met on `index.html` after the TASK-008 rewrite.

[FINDING: High] otak_aplikasi/templates/index.html:697 — featured "Berita & Prestasi" image wrapper has no `aspect-[2/3]`; it is a fixed `h-56` mobile band plus `md:h-auto md:min-h-[260px] max-h-[320px]`, so at md the ~405px-wide column renders ~405x320 landscape and the 4:6 photo is cropped. Section A names index.html news cards; TASK-008 item 3 also calls the column portrait. — Add `aspect-[2/3]` and a width cap so 2:3 holds under the height cap (e.g. `aspect-[2/3] max-h-[320px] md:max-w-[213px]`), remove `h-56`/`md:min-h-[260px]`, keep `object-cover`.
[FINDING: Medium] otak_aplikasi/templates/index.html:730 — remaining news cards use `aspect-[2/3] max-h-[380px]`; at md each card is ~590px wide, so the cap clamps the box to 590x380 (landscape) and re-crops the portrait photo. — Drop `max-h-[380px]`, or narrow the columns until width x 1.5 stays under the cap.
[FINDING: Low] otak_aplikasi/templates/search_results.html:40 — `aspect-[2/3]` combined with `max-h-[480px]` (first result, `md:col-span-2`) / `max-h-[420px]`: the featured result is ~810px wide, so the cap makes it landscape. — Remove the caps or apply them only at breakpoints where they do not bind.
[FINDING: Low] otak_aplikasi/templates/berita/berita.html:239-263 — the new pagination links have hover styles but no visible focus ring (blueprint requires `focus:ring-2 focus:ring-primary`). — Add `focus-visible:ring-2 focus-visible:ring-primary` to prev/next/number links.

Notes: the `[EVIDENCE: GREEN]` run (11:08) predates the TASK-008 rewrite of `index.html` (11:13), so its "portrait cards on `/`" claim no longer holds. The view change is confined to `berita()`.

## Fix round (review findings)
[EVIDENCE: RED] Reviewer findings = failing state: `index.html:697` featured image had no `aspect-[2/3]` (`h-56 md:h-auto md:min-h-[260px] max-h-[320px]`, landscape); `index.html:730` teaser `max-h-[380px]` clamped the portrait box; `search_results.html:40` `max-h-[480px]`/`max-h-[420px]` clamped `aspect-[2/3]`; `berita.html` pagination links had no focus ring.
[EVIDENCE: GREEN] `env\Scripts\python.exe manage.py check` → exit 0 → System check identified 1 issue (ckeditor.W001 only).
[EVIDENCE: GREEN] `verify_task008_fix.py` (fresh process, Django Client) → exit 0 → GET `/` 200 and `/search/?q=berita` 200, no literal `{{`; featured container class list = `relative md:col-span-1 aspect-[2/3] overflow-hidden` (no `h-56`, no `max-h-[320px]`); no `max-h-[380px]` on `/`; `/search/` keeps `aspect-[2/3]` with no `max-h-[480px]`/`max-h-[420px]`; pagination prev/number/next links carry `focus:ring-2 focus:ring-primary focus:outline-none`.
[EVIDENCE: FULL] Scope = `index.html` (featured portrait + teaser grid `md:grid-cols-3`, cap removed) and `search_results.html` (caps removed), plus `berita/berita.html` pagination focus rings. No Python, no other files, waitress not restarted.
[READY_FOR_REVIEW]
