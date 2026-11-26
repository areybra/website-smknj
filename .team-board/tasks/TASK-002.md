# TASK-002

## Brief
Read `.team-board/01-blueprint.md` first. Redesign homepage and search results with the mixed grid vocabulary. Files:
- `otak_aplikasi/templates/index.html`
- `otak_aplikasi/templates/search_results.html`

Homepage requirements:
- Hero: asymmetric 8/4 split, warm `bg-page` with subtle pattern, right visual panel uses `bg-background-dark` or image, no empty grey gradient placeholder (use image when available, otherwise accent panel with copy).
- Statistik: bento 4-col: one big dark tile `col-span-2 row-span-2`, 2 small KPI tiles, 1 accent tile, 1 pengumuman tile. When data empty, show friendly empty state on `bg-sand`, not blank.
- "Pusat Keunggulan": bento 3-col with 2 wide cards + 2 small tiles; not 2 equal lists.
- Berita & Prestasi: editorial grid, first item featured `md:col-span-2`, remaining compact cards.
- Sections alternate `bg-page` / `bg-sand` / `bg-background-dark`. Vary `py-16/20/24`.
- Apply semantic class mapping from blueprint.

Search results: editorial grid, featured first card `md:col-span-2`, rest compact; warm palette.

## Depends
TASK-001 (token names; may edit in parallel using blueprint names, no file overlap).

## Files
- `otak_aplikasi/templates/index.html`
- `otak_aplikasi/templates/search_results.html`

## Interfaces
Consumes tokens from TASK-001. No backend changes.

## Test
`curl.exe` GET `/` and `/search/?q=berita` must return 200. Django check pass.

## Status
[TASK: TASK-002 ready]

## Evidence
[EVIDENCE: FULL] `python manage.py check` (deploy.bat env) → exit 0 → 1 pre-existing ckeditor.W001 warning, 0 errors.
[EVIDENCE: FULL] `curl.exe http://127.0.0.1:8000/` → 200.
[EVIDENCE: FULL] `curl.exe "http://127.0.0.1:8000/search/?q=berita"` → 200.
[EVIDENCE: FULL] fresh-process Django test Client `/` → 200, contains `bg-page`, `lg:grid-cols-12`, `lg:row-span-2`, `md:grid-cols-3`, `bg-background-dark`, `bg-sand`.
[EVIDENCE: FULL] fresh-process Django test Client `/search/?q=berita` → 200, contains `bg-page`, `bg-surface`, `md:col-span-2`, `border-line`, `bg-highlight`.

Note: running waitress process has index.html in Django's DEBUG=False template cache, so live `/` HTML still shows pre-edit markup until server restart. Fresh-process render confirms new markup. Search page was not cached and shows new markup live.

## Review
[REVIEW: spec PASS]
[REVIEW: quality PASS]

Spec check:
- Hero: `lg:grid-cols-12` with `lg:col-span-8` text + `lg:col-span-4` visual; `bg-page` + `bg-triangle-pattern`; panel `bg-background-dark`, image when present, copy fallback. No grey gradient placeholder. PASS.
- Statistik: `lg:grid-cols-4`; dark tile `lg:col-span-2 lg:row-span-2`, 2 KPI tiles, `bg-accent` tile, pengumuman tile; friendly empty state on `bg-sand`. PASS.
- Pusat Keunggulan: `md:grid-cols-3`; 2 `md:col-span-2` wide cards + 2 single-column tiles. Not two equal lists. PASS.
- Berita & Prestasi and search results: `md:grid-cols-3`, first card `md:col-span-2`, compact remainder. PASS.
- Section backgrounds alternate page/sand/page/sand/dark/page; `py-20`/`py-24` varied. PASS.
- Semantic mapping: only permitted translucent `bg-white/5|10|20|90` overlays remain. No `bg-gray`, `text-gray`, `border-gray`, `text-[#0A192F]` or `bg-[#F8FAFC]` in target files. PASS.
- Django tags balanced: index 60/60 `{%`/`%}`, 21 open/21 close; search 30/30, 9/9. No broken `{% url %}` (evidence: HTTP 200 on both routes). PASS.
- Scope: only the two owned templates carry task mtimes (10:22, 10:24); no backend/Python edits. PASS.

Evidence: five `[EVIDENCE: FULL]` entries match the task test — `manage.py check` exit 0 (known ckeditor.W001 only), `curl.exe` 200 on `/` and `/search/?q=berita`, plus fresh-process render assertions for the new grid classes. Protocol allows `[EVIDENCE: FULL]`; no RED/GREEN pair for this visual-only task.

[FINDING: Medium] `otak_aplikasi/templates/index.html` — hero loop renders all 3 news items as `absolute inset-0 z-20`, so only the last (oldest) article paints; "Berita Utama" shows the wrong item — change line 72 to `{% for news in berita_list|slice:":1" %}` or use `{% with news=berita_list.0 %}`.
[FINDING: Low] `otak_aplikasi/templates/index.html` — `data-dashboard-width="{{ school.width_dashboard }}"` (line 199) references `school`, absent from the home context in `views.py` (only `school_stats` exists); attribute renders empty — remove it or bind `school_stats`.
[FINDING: Low] `otak_aplikasi/templates/index.html` — jurusan empty state (line 400) puts `<p>` directly inside `<dl>`, invalid HTML — wrap it in `<div>`.
[FINDING: Low] `otak_aplikasi/templates/index.html` — Berita & Prestasi grid (lines 663-690) has no `{% empty %}`; an empty `berita_list` leaves a blank section — add a friendly empty state on `bg-sand`.

## Follow-up fix
[EVIDENCE: FULL] `otak_aplikasi/templates/index.html` — hero loop changed to `{% for news in berita_list|slice:":1" %}`, `{% empty %}` fallback kept.
[EVIDENCE: FULL] `otak_aplikasi/templates/index.html` — removed dead `data-dashboard-width="{{ school.width_dashboard }}"`.
[EVIDENCE: FULL] `otak_aplikasi/templates/index.html` — jurusan empty state `<p>` wrapped in `<div class="sm:col-span-2 ...">`.
[EVIDENCE: FULL] `otak_aplikasi/templates/index.html` — added `{% empty %}` berita empty state on `bg-sand`.
[EVIDENCE: FULL] `python manage.py check` (deploy.bat env) → exit 0 → 1 pre-existing ckeditor.W001 warning, 0 errors.
[EVIDENCE: FULL] fresh-process Django Client `/` → 200, hero article count 1, no `data-dashboard-width`.
[EVIDENCE: FULL] fresh-process Django Client `/search/?q=berita` → 200, contains `bg-surface`.
[EVIDENCE: FULL] fresh-process `render_to_string('index.html', {})` → jurusan div, berita empty state, hero fallback all present.
[EVIDENCE: FULL] `curl.exe` `/` → 200; `curl.exe` `/search/?q=berita` → 200.

[APPROVED-TASK]
