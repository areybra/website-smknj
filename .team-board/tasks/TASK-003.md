# TASK-003

## Brief
Read `.team-board/01-blueprint.md` first. Redesign news and announcement pages with mixed grid. Files:
- `otak_aplikasi/templates/berita/berita.html`
- `otak_aplikasi/templates/berita/detail_berita.html`
- `otak_aplikasi/templates/pengumuman/pengumuman.html`
- `otak_aplikasi/templates/pengumuman/detail_pengumuman.html`

Requirements:
- Berita listing: editorial grid. First item featured `md:col-span-2`, other items compact list/row cards. Warm page background, `bg-surface` cards with `border-line`.
- Detail berita: 12-col main/sidebar split already present; restyle with warm tokens, sidebar cards compact, related/trending as list rows.
- Pengumuman listing: list/row grid, not big cards. One featured "penting" row, others compact rows. Download panel uses `bg-sand`.
- Detail pengumuman: 3-col split kept but restyled; file download rows compact. This template has its own `tailwind.config` — update tokens there too.
- Apply semantic class mapping. Keep all Django template tags, URLs, filters and data logic unchanged.

## Depends
TASK-001 token names (no file overlap).

## Files
- `otak_aplikasi/templates/berita/berita.html`
- `otak_aplikasi/templates/berita/detail_berita.html`
- `otak_aplikasi/templates/pengumuman/pengumuman.html`
- `otak_aplikasi/templates/pengumuman/detail_pengumuman.html`

## Interfaces
Consumes tokens from TASK-001. No backend changes.

## Test
`curl.exe` GET `/berita/`, `/pengumuman/` must be 200. Detail routes with existing slugs must be 200. Django check pass.

## Evidence (coder)

[EVIDENCE: RED] env\Scripts\python.exe C:\Users\445\AppData\Local\Temp\opencode\task003_check.py → exit 1 → 9/58 passed, 49 failed
[EVIDENCE: GREEN] env\Scripts\python.exe C:\Users\445\AppData\Local\Temp\opencode\task003_check.py → exit 0 → 58/58 passed, 0 failed

[EVIDENCE: FULL]
- env\Scripts\python.exe manage.py check (env from deploy.bat) → exit 0 → 0 errors, 1 pre-existing ckeditor.W001 warning
- curl.exe GET /berita/ → 200
- curl.exe GET /berita/berita-sekolah-6/ → 200
- curl.exe GET /pengumuman/ → 200
- curl.exe GET /pengumuman/verify-003-temporary/ → 200 (temp record created, deleted in finally; DB back to 0 pengumuman, 0 temp category)
- Fresh-process Django render check: /berita/, /berita/berita-sekolah-6/, /pengumuman/ → 200, zero missing warm tokens
- Restarted waitress: in-memory template cache held pre-edit templates. Re-curl after restart → 200 + `md:col-span-2` present on berita, 28× `bg-sand` on pengumuman

Note: base layout `tailwind.config` still has old tokens (TASK-001 scope). `detail_pengumuman.html` standalone config updated here. Base-layout pages need TASK-001 before visual review.

## Status
[TASK: TASK-003 ready]
[READY_FOR_REVIEW]

## Review

[REVIEW: spec PASS]
[REVIEW: quality PASS]

Verified:
- Berita listing: featured-first editorial grid confirmed (`grid md:grid-cols-3`, first card `md:col-span-2`, later cards compact `p-4` rows with `size-20` thumb), warm `bg-page`/`bg-surface`/`border-line`/`text-ink`/`text-muted` present.
- Detail berita: `lg:grid-cols-12` with `lg:col-span-8` main + `lg:col-span-4` aside kept; trending/related/terbaru rendered as compact list rows.
- Pengumuman listing: `space-y-4` row list, one featured `bg-sand` "Penting" row, download panel `bg-sand`, no giant card grid.
- Detail pengumuman: `lg:grid-cols-3` kept; standalone `tailwind.config` carries all blueprint tokens (page/surface/sand/line/ink/muted/highlight/brand/brand-dark/accent/accent-bright/background-dark/background-light) and radius scale; compact file rows.
- Forbidden classes absent: only `bg-white/5`, `/10`, `/20` overlays remain (allowed by blueprint). No `text-gray-*`, `border-gray-*`, `text-[#0A192F]`.
- Django tags/URLs intact; context vars match `views.py` (`berita_utama`, `berita_trending`, `pengumuman_penting`, `pengumuman_file`, `total_files`, `total_downloads`, `most_downloaded_file`). `primary-dark` alias exists in `layouts/base.html:26`, so gradients resolve.
- Scope: only the four owned templates carry TASK-003 mtimes; other recent edits belong to TASK-002/TASK-004 files.
- Evidence: `task003_check.py` re-run now → 58/58 passed, 0 failed; RED count (58 total) matches the script. Placeholder images are accepted risk, not flagged.

[FINDING: Low] `otak_aplikasi/templates/pengumuman/pengumuman.html:327` — tooltip uses non-token `bg-gray-800` (no gray token in blueprint) — replace with `bg-background-dark` or `bg-ink`.
[FINDING: Low] `otak_aplikasi/templates/berita/detail_berita.html:183` — primary CTA search button uses `bg-primary text-white`; blueprint rule is `bg-primary text-surface` — swap for consistency (visual impact negligible).
[FINDING: Low] `otak_aplikasi/templates/pengumuman/pengumuman.html:78,204,215,222` — template reads `selected_category`, but `views.py:231-240` passes only `category_name`; active category chip never highlights and pagination links drop `category` — pre-existing, not introduced by this task; template-only fix is `request.GET.category` comparison if Architect wants it in scope.

[APPROVED-TASK]
