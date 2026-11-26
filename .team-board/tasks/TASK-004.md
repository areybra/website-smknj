# TASK-004

## Brief
Read `.team-board/01-blueprint.md` first. Redesign profile, program, extracurricular, and contact pages. Files:
- `otak_aplikasi/templates/profil/profil_sekolah.html`
- `otak_aplikasi/templates/profil/guru-staff.html`
- `otak_aplikasi/templates/profil/fasilitas.html`
- `otak_aplikasi/templates/program/jurusan/jurusan.html`
- `otak_aplikasi/templates/program/jurusan/detail_jurusan.html`
- `otak_aplikasi/templates/program/ektrakurikuler/ektrakurikuler.html`
- `otak_aplikasi/templates/program/ektrakurikuler/detail_ektrakurikuler.html`
- `otak_aplikasi/templates/kontak/kontak.html`

Requirements:
- Profil sekolah & guru-staff: modular 12-col, compact cards, no giant white blocks.
- Fasilitas: mosaic image tiles with varied spans (`col-span-2 row-span-2` featured) using existing images only.
- Jurusan listing: bento 3-col with featured program card + compact program tiles.
- Detail jurusan: zigzag alternating image/text for fasilitas/karir/testimoni sections; asymmetrical split header.
- Ekstrakurikuler: mosaic for main cards + list/row for schedule.
- Detail ekstrakurikuler: modular with compact cards.
- Kontak: asymmetric split, warm form surface `bg-surface`, labels visible.
- All standalone templates listed above have their own `tailwind.config`; update tokens there too.
- Apply semantic class mapping. Keep all Django tags and data logic.

## Depends
TASK-001 token names (no file overlap).

## Files
See list above.

## Interfaces
Consumes tokens from TASK-001. No backend changes.

## Test
`curl.exe` GET `/profil-sekolah/`, `/guru-staff/`, `/fasilitas/`, `/program-studi/`, `/ektrakurikuler/`, `/kontak/` must be 200. Django check pass.

## Evidence
[EVIDENCE: RED] env\Scripts\python.exe C:\Users\445\AppData\Local\Temp\opencode\task004_check.py → exit 1 → 151 failures (no warm tokens, legacy classes, missing grid vocab, stale standalone configs).
[EVIDENCE: GREEN] env\Scripts\python.exe C:\Users\445\AppData\Local\Temp\opencode\task004_check.py → exit 0 → PASS: 8 templates warm tokens, mixed grids, configs, Django tags intact (535 tags unchanged).
[EVIDENCE: FULL]
- Design guard: `task004_check.py` → exit 0 → PASS (8/8 templates; 4 standalone tailwind configs carry exact blueprint tokens and radius).
- Fresh-process Django Client: `task004_fresh_render.py` → exit 0 → 8 routes 200 (6 listed + 1 jurusan detail + 1 ekskul detail), balanced markup, no legacy ink literal.
- Django check (env from deploy.bat): `manage.py check` → exit 0 → 1 pre-existing ckeditor.W001 warning only.
- Live routes (curl.exe, waitress cache): `/profil-sekolah/`, `/guru-staff/`, `/fasilitas/`, `/program-studi/`, `/ektrakurikuler/`, `/kontak/` → all 200.
- Scope: exactly 8 templates changed; no Python, no installs, no worktrees, no server restart.

## Review (2026-11-26)

Scope check: exactly the 8 owned templates were modified (mtimes 10:32–10:34). No Python, settings, or layout files touched. `static/images/placeholder/warm.svg` (10:35) belongs to TASK-005 and is not referenced by these templates.
Django tags: 535 tags, sequence identical to baseline in all 8 files. Forbidden classes: 0 non-overlay `bg-white`, 0 `text-gray-*`, 0 `border-gray-*`, 0 `text-[#0A192F]`; remaining `bg-white/10|20|90|95` are overlays on dark surfaces.
Warm tokens: present in all 8. Standalone configs (kontak, detail_jurusan, ektrakurikuler, detail_ektrakurikuler) carry the exact blueprint color map and radius. Evidence RED/GREEN/FULL matches the task commands.

[REVIEW: spec FAIL]
[REVIEW: quality FAIL]

[FINDING: High] program/jurusan/detail_jurusan.html:106-114 — `.zigzag-grid > *` forces `display:flex` on every child, so the Kompetensi, Fasilitas, Karir and Alumni cards render as horizontal rows (icon, heading and body side by side) and even children are reversed and right-aligned; the previous 2-column grid is lost. — Remove the `> *` flex rule. Build zigzag from two halves: `md:grid-cols-2` with `md:order-1`/`md:order-2` on image and text blocks, or `even:md:flex-row-reverse` on the inner row of testimonial cards only.
[FINDING: High] program/jurusan/detail_jurusan.html:186,406,513,515,517,552,663 — 7 `{{ ... }}` tags contain a newline, so Django's tag regex does not match them and the page prints the raw text `{{ jurusan.kode_jurusan }}` (also alumni name/jabatan/perusahaan, kaprodi, fasilitas icon, CTA label). Pre-existing and unchanged by this task, but it ships broken from an owned file. — Join each variable tag onto one line; add a guard that greps `\{\{[^}]*\n` and `\{%[^%]*\n` over the 8 files.
[FINDING: High] program/jurusan/detail_jurusan.html:242 — caption changed from `text-gray-200` to `text-muted`; #475569 on the dark image gradient is about 2.5:1 and nearly invisible. — Use `text-surface/90` or `text-white/90`.
[FINDING: Medium] profil/fasilitas.html:182-284 — the varied-span grid (`col-span-2 row-span-2`) holds icon cards only, while the cards that carry images are uniform `lg:col-span-12`; the required "mosaic image tiles with varied spans using existing images" is not implemented. — Turn the lab grid into a 4-col mosaic: first lab `lg:col-span-2 lg:row-span-2` with `lab.gambar`, remaining labs `1x1`/`2x1`.
[FINDING: Medium] program/ektrakurikuler/ektrakurikuler.html:291 — every Wajib card is `col-span-2 row-span-2`, so the grid is a uniform 2-up, not a varied mosaic. — Vary spans by `forloop.counter`: featured `col-span-2 row-span-2`, others `col-span-1` or `col-span-2 row-span-1`.
[FINDING: Medium] program/jurusan/jurusan.html:437-444 — `{% cycle %}` still emits cold pastels `bg-blue-100`, `bg-orange-100`, `bg-purple-100`, `bg-green-100` and `text-*-600` on the warm page. — Drop the color cycles; use `bg-sand` with `text-accent` and keep only the icon cycle.
[FINDING: Medium] kontak/kontak.html:174-205 — `focus:outline-none` plus `focus:ring-primary/20` and the `.contact-form` CSS shadow `rgba(0,71,171,0.1)` give a 10–20% focus indicator, below the blueprint 3:1 rule. — Use `focus:ring-2 focus:ring-primary` without `outline-none`, and raise the CSS focus shadow to a solid 2px ring.
[FINDING: Medium] program/ektrakurikuler/ektrakurikuler.html:168 — `text-accent` (#00697A) on the `from-primary` gradient is about 1.6:1 for the H1 words "& Kegiatan". — Use `text-accent-bright` (decorative on dark) or `text-surface`.
[FINDING: Medium] profil/fasilitas.html:117 — `md:flex-row-reverse` is applied to a `grid` container, so even labs never reverse; the class is dead (pre-existing). — For `forloop.counter|divisibleby:2` put `md:order-2` on the figure and `md:order-1` on the body.
[FINDING: Medium] program/ektrakurikuler/detail_ektrakurikuler.html:193 — `grid-cols-2 md:grid-cols-6` with three `col-span-3` cards leaves the third card alone at half width on md+. — Use `md:grid-cols-3` with `md:col-span-1`.
[FINDING: Low] program/jurusan/jurusan.html:434, program/jurusan/detail_jurusan.html:584, kontak/kontak.html:231,243,254,265, program/ektrakurikuler/ektrakurikuler.html:421 — `hover:bg-sand` on an element that is already `bg-sand` does nothing. — Remove the hover class.
[FINDING: Low] program/ektrakurikuler/detail_ektrakurikuler.html:166, kontak/kontak.html:159, kontak/kontak.html:299 — `{% if %}` branches and a JS ternary produce identical output for every case. — Collapse each to one branch, or give success and error distinct styles.
[FINDING: Low] program/jurusan/detail_jurusan.html:394,449,496 — section headings mix `md:flex-row` and `md:flex-row-reverse` (two reversed, one not). — Pick one heading alignment.
[FINDING: Low] program/ektrakurikuler/ektrakurikuler.html:420 — `{% for day in days %}` has no provider: `days` is absent from `views.py` and `web_smknj/context_processors.py`, so the day filter renders zero buttons (pre-existing). — Hardcode Senin–Sabtu, or add `days` to the view (backend change, needs its own task).
[FINDING: Low] program/jurusan/detail_jurusan.html:233, profil/fasilitas.html:121 — `from-[#0A192F]/80` and `/60` bypass the token map. — Use `from-ink/80` and `from-ink/60`.

## Fix Evidence (review round 1)

[EVIDENCE: RED] `task004_review_check.py` → exit 1 → 33 failures; fresh Django Client render → literal `{{ }}` on `/program-studi/rekayasa-perangkat-lunak/`.

[EVIDENCE: FULL]
- `task004_review_check.py` → exit 0 → all 7 MUST fixes pass: 7 multiline tags joined, zigzag rebuilt on row axis (`md:grid-cols-2` + `direction: rtl/ltr`, mobile 1 col), dark-gradient caption `text-surface/90`, real image mosaics in fasilitas/ekstrakurikuler, warm `{% cycle %}` removed, kontak focus ring `focus:ring-2 focus:ring-primary focus:border-primary`, H1 `text-surface` + `text-highlight`.
- `task004_check.py` → exit 0 → 8 templates still carry warm tokens, mixed grids, exact standalone configs; Django tag set intact except the two explicitly removed color cycles.
- `task004_fresh_render.py` → exit 0 → fresh-process Django Client: 8 routes 200 including `/program-studi/rekayasa-perangkat-lunak/`, `/fasilitas/`, `/ektrakurikuler/`, `/kontak/`; no literal `{{`/`}}`, no `text-gray-200`, balanced markup.
- `manage.py check` (env from deploy.bat) → exit 0 → known ckeditor.W001 only.
- Scope: same 8 owned templates only; no Python, no new data, no waitress restart. Placeholder URLs untouched.

## Review round 2 (2026-11-26)

Verified fixed:
- 7 multiline tags: `grep '{{[^}]*$'` and `'{%[^%]*$'` over the whole `otak_aplikasi/templates` tree return 0 hits, so no tag can print literally. Line 189/408/514-516/550/660 are single-line.
- `text-gray-200` gone repo-wide; caption is `text-surface/90`.
- kontak focus: `focus:ring-2 focus:ring-primary focus:border-primary` on all 5 controls, `.contact-form` CSS shadow now `0 0 0 2px #0047AB` (solid, 3:1). `focus:outline-none` gone.
- ekskul H1: `text-surface` + `text-highlight` (#F2B84B on #0047AB = 4.75:1).
- fasilitas lab mosaic: real `lab.gambar` tiles, spans vary via `.lab-even` (2x1) and `:nth-child(3n)` (1xN); mobile 1 col.
- ekskul mosaic: first card 2x2, `:not(:first-child)` 1x1, `3n` 2x1 — varied.
- `{% cycle %}` colour pastels gone from `jurusan.html` (icon-only cycle kept); no `bg-*-100`/`text-*-600` left.
- detail_ektrakurikuler info grid is `grid-cols-1 sm:grid-cols-3`; fasilitas `md:flex-row-reverse` on a grid container removed.
- Evidence RED/GREEN/FULL present and match the task commands.

[REVIEW: spec FAIL]
[REVIEW: quality PASS]

[FINDING: Medium] program/jurusan/detail_jurusan.html:107-112,507 — testimoni zigzag is dead: `.zigzag-grid > :nth-child(even) > * { direction: ltr }` resets the inner `flex items-center gap-4` row, so the avatar stays left on every card. Only the Karir rows alternate. The task names testimoni explicitly. — Put `even:md:flex-row-reverse` (or `md:[direction:rtl]` on the row plus `direction:ltr` on its two children) on the flex row at line 507 and drop the alumni block from `.zigzag-grid`.
[FINDING: Medium] program/jurusan/detail_jurusan.html:402-445 — Fasilitas section sits inside `.zigzag-grid` but each card is a vertical icon-over-text block, so nothing alternates left/right; `FasilitasJurusan` has no image field, so "image/text zigzag" is not buildable here without a backend change. — Either make each row a 2-col grid (icon block + text) and alternate with `md:order-*`, or remove `.zigzag-grid` from this section and record the deviation in the task note.
[FINDING: Medium] profil/fasilitas.html:71,127 and profil/guru-staff.html:63 — image fallbacks still hotlink `https://lh3.googleusercontent.com/aida-public/...`, not a local asset. These URLs expire, so the hero and lab tiles will break. — Use `{% static 'images/placeholder/warm.svg' %}` for `lab.gambar` and a local hero image; nothing else in the brief blocks it.
[FINDING: Low] program/ektrakurikuler/ektrakurikuler.html:300 — mosaic base is `grid-cols-2`; the blueprint mobile rule says every grid collapses to 1 column. — `grid-cols-1 sm:grid-cols-2 md:grid-cols-4`.
[FINDING: Low] kontak/kontak.html:231,243,254,265 — `group-hover:bg-sand` on an element already `bg-sand` (round-1 finding, untouched). — Remove the hover class.
[FINDING: Low] kontak/kontak.html:159 and program/ektrakurikuler/detail_ektrakurikuler.html:166 — `{% if %}` branches still produce identical classes for every case (round-1 finding, untouched). — Collapse each to one branch.
[FINDING: Low] program/jurusan/jurusan.html:394 — `transition-colors` is now dead after the `hover:bg-sand` removal. — Drop it or add a real hover.

## Fix Evidence (review round 2)

[EVIDENCE: RED] `task004_round2_check.py` → exit 1 → 11 failures (old direction trick, no `md:order-*`, 3 remote hotlinks); fresh Django Client render → `googleusercontent.com` on `/guru-staff/` and `/fasilitas/`.

[EVIDENCE: FULL]
- `task004_round2_check.py` → exit 0 → testimoni and fasilitas rows carry `md:order-1`/`md:order-2` with even-row CSS overrides; old `direction: rtl/ltr` trick removed; mobile stays 1 column in DOM order; Karir alternation preserved via `.karir-row`.
- `profil/fasilitas.html` (hero + lab fallback) and `profil/guru-staff.html` (hero) now use `{% static 'images/placeholder/warm.svg' %}`; both have `{% load static %}`; zero `googleusercontent.com` in the template tree.
- `task004_check.py` → exit 0, `task004_review_check.py` → exit 0 (earlier rounds still green).
- Fresh-process Django Client (`task004_fresh_render.py`) → exit 0 → `/program-studi/rekayasa-perangkat-lunak/`, `/fasilitas/`, `/guru-staff/` all 200 (plus 5 other routes); no literal `{{`/`}}`, no `googleusercontent.com`, `md:order-` present on detail page, balanced markup.
- `manage.py check` (env from deploy.bat) → exit 0 → known ckeditor.W001 only.
- Scope: only the three owned templates changed in this round; no Python, no new context variables, no waitress restart.
- Note: shared workspace showed concurrent edits by other owners inside owned files; those edits were left intact.

## Status
[READY_FOR_REVIEW]
