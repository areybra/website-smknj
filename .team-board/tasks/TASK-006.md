# TASK-006

## Brief
Read `.team-board/01-blueprint.md` first. Fix the empty-data layout holes found in Conductor screenshot review. Data is sparse in seed DB: several sections render a heading followed by a large blank area or a mostly empty white card. The fix is compact, friendly empty states and conditional section hiding. Do not invent data.

Targets (verify each against the current file before editing):

1. `program/ektrakurikuler/ektrakurikuler.html` — "Ekstrakurikuler Wajib" section renders heading + huge void when no `wajib` items. Render the grid only when items exist; otherwise a single compact `bg-sand border border-line` note row inside the same section (icon + "Belum ada ekstrakurikuler wajib" + link). No 300px gap.
2. `program/jurusan/jurusan.html` — "Program Unggulan" bento: the featured tile is a tall mostly empty white card. Give it a compact minimum height (`min-h-[180px]` not full-height stretch), keep description clamped (`line-clamp-3`), and let the grid not stretch empty space. Also the "Mitra Penyaluran Kerja" card: replace the centered blank block with a compact note row.
3. `program/jurusan/detail_jurusan.html` — "Peluang Karir" blue panel and "Galeri Kegiatan" tile are near-empty. Compact them: note row inside the panel, gallery falls back to the local placeholder already wired in TASK-005.
4. `index.html` — statistics bento: when `school_stats` values are empty the big dark tile shows a lone empty state. Keep the bento shape but add 2 static KPI tiles that always have content (e.g. jumlah jurusan and jumlah ekstrakurikuler from existing context, only if those variables already exist in the view — otherwise use the existing counts already printed elsewhere on the page; do not add view logic).
5. `program/jurusan/jurusan.html` hero program tiles — the 2x2 tiles have mismatched vertical offsets and a white gradient wash over the lower half of "Multimedia" and "Akuntansi". Normalize: equal tile heights inside one grid (`grid-rows-2`), remove the white gradient overlay so text sits on `bg-surface`.
6. `index.html` hero right panel — dark card with only a small news line. If `berita_list` first item has an image, show it; otherwise use `images/placeholder/warm.svg` as background with the news text over a dark gradient overlay so the panel reads as intentional.
7. `profil/profil_sekolah.html` — "Struktur Organisasi" renders a heading and nothing else. The view supplies `struktur_organisasi` (`views.py:60`). Wrap the section body in `{% if struktur_organisasi %}` and add an `{% else %}` compact note row ("Data struktur organisasi belum tersedia"). No empty 200px block.
8. `profil/guru-staff.html` — "Struktur Kepemimpinan Sekolah" (`leaders_list`) and "Guru Produktif & Instruktur" (`guru_staff_list`) render headings with no content. Same treatment: compact `{% empty %}` note row inside each list, or hide the section when empty. Also the KPI strip prints "0+ Guru & Instruktur" with no data — render `—` instead of `0+`. Do not invent counts.

Rules:
- Warm tokens only: `bg-sand`, `bg-surface`, `border-line`, `text-ink`, `text-muted`, `text-primary`.
- Every empty state: icon + one short Indonesian sentence, max 2 lines, `py-6` to `py-8`, no `py-20` voids.
- No new context variables, no Python changes, no data seeding.
- Keep all Django tags, loops and URLs intact.

## Depends
TASK-005 (placeholder asset wiring, null-safe text).

## Files
- `otak_aplikasi/templates/index.html`
- `otak_aplikasi/templates/program/jurusan/jurusan.html`
- `otak_aplikasi/templates/program/jurusan/detail_jurusan.html`
- `otak_aplikasi/templates/program/ektrakurikuler/ektrakurikuler.html`
- `otak_aplikasi/templates/profil/profil_sekolah.html`
- `otak_aplikasi/templates/profil/guru-staff.html`

## Interfaces
Consumes tokens from TASK-001 and the placeholder asset from TASK-005. No backend changes.

## Test
- Fresh-process Django Client render of `/`, `/program-studi/`, `/ektrakurikuler/`, and one detail jurusan URL returns 200.
- Screenshot review by Conductor: no section taller than ~120px with only a heading and empty space.
- `manage.py check` exit 0 (known `ckeditor.W001` acceptable).
- Do not restart the running waitress.

## Status
[TASK: TASK-006 done] [READY_FOR_REVIEW]

## Evidence
- `[EVIDENCE: RED] env\Scripts\python.exe %TEMP%\opencode\task006_check.py → exit 1 → 9 FAIL (hero image fallback, 2 static KPI tiles, grid-rows-2, row-span-2, min-h-[180px], wajib empty state, struktur empty state, KPI dash, leaders/guru empty lists)`
- `[EVIDENCE: GREEN] env\Scripts\python.exe %TEMP%\opencode\task006_check.py → exit 0 → 17/17 PASS; fresh Client render 200 on /, /program-studi/, /program-studi/rekayasa-perangkat-lunak/, /ektrakurikuler/, /profil-sekolah/, /guru-staff/`
- `[EVIDENCE: FULL] env\Scripts\python.exe manage.py check → exit 0 → 1 warning ckeditor.W001 (known/accepted)`

## Notes
- Item 3: "Peluang Karir" blue panel and "Galeri Kegiatan" exist only in `jurusan.html` (grep: lines 250, 275). Compacted there. `detail_jurusan.html` has no such sections, so it is unchanged.
- Item 5: hero program tiles had no white gradient element; they were rebuilt as one `grid-rows-2` grid (equal `min-h-[180px]`, `bg-surface`, `text-ink`), removing the `pt-8` column offset.
- Item 4: static KPI tiles use existing `jurusan_list|length` and `berita_list|length`; accent CTA tile moved outside `{% if school_stats %}` so the bento fills when stats are absent.
- Wajib empty state detects absence via `{% with last_ektra=ektra_list|dictsort:"type_ektra"|last %}` (Wajib sorts last; no Python change).

## Review
[REVIEW: spec PASS]
[REVIEW: quality FAIL]

Items 1, 2, 5, 6, 7, 8 verified in the files (compact `py-6`/`py-8` notes, warm tokens, `grid-rows-2` hero tiles, `min-h-[180px]`, KPI `—`, no new context vars, no Python change). Item 3 named sections live in `jurusan.html` and are compacted there; `detail_jurusan.html` is unchanged. Item 4 tiles exist but one prints a false total. Evidence RED/GREEN present, but the GREEN run (11:02) predates the TASK-007/TASK-008 rewrites of `index.html` and `jurusan.html`, so it no longer describes the current files.

[FINDING: Medium] otak_aplikasi/templates/index.html:280 — "Publikasi / Berita Terbit" prints `{{ berita_list|length }}`, but `beranda()` slices `berita_list[:3]` (views.py:32), so the KPI can never exceed 3 and is not the publication count. Misleading number, against "do not invent data". — Replace that tile with a non-numeric "Semua Berita" CTA, or another count already in context; a true total needs a view change (out of scope).
[FINDING: Medium] otak_aplikasi/templates/program/ektrakurikuler/ektrakurikuler.html:392-430 — "Ekstrakurikuler Pilihan" only has `{% empty %}` on the loop, which fires only when `ektra_list` is empty. With only `Wajib` items the section renders a heading plus an empty grid (same void class this task targets). — Mirror the Wajib detection: `{% with first_ektra=ektra_list|dictsort:"type_ektra"|first %}{% if not first_ektra or first_ektra.type_ektra != 'Pilihan' %}` compact note `{% endif %}{% endwith %}`.
[FINDING: Medium] otak_aplikasi/templates/program/jurusan/detail_jurusan.html:274-292,413-491,550,591-612 — empty states invent data: stat defaults `120`/`8`/`3`/`96%`, facilities "Lab Komputer Modern"/"Server Room"/"Studio Multimedia", careers "Network Administrator"/"Software Developer", certifications "Cisco Certified Network Associate"/"MTCNA", kaprodi "Dr. Ir. Budi Santoso". Brief forbids invented data and this file is listed. — Replace each `{% empty %}` with the compact note row (`bg-sand border border-line rounded-xl px-4 py-6`, icon + "Belum ada ... terdaftar"); drop the numeric `|default:` fabrications in favour of `—`.
[FINDING: Low] otak_aplikasi/templates/program/ektrakurikuler/ektrakurikuler.html:365-380 — the Wajib-empty check runs on the filtered `ektra_list` (views.py:278-282), so `?kategori=`/`?search=` that hides all Wajib items shows "Belum ada ekstrakurikuler wajib pada periode ini" while wajib items exist. — Gate the note on `{% if not request.GET.kategori and not request.GET.search %}` or reword to "Tidak ada ekstrakurikuler wajib pada filter ini".
[FINDING: Low] otak_aplikasi/templates/index.html:85 — hero excerpt uses `{{ news.content|default:""|safe|truncatewords:10 }}`; `truncatewords` is not HTML-aware, so rich-text tags can be cut mid-tag. — Use the news-card pattern `striptags|truncatewords:10|safe`.
