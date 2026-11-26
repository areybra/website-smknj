# TASK-005

## Brief
Read `.team-board/01-blueprint.md` first. Two mechanical fixes across all frontend templates. No layout redesign, no backend changes.

### A. Null-safe text (kill literal "None")
Django renders `None` for null model fields. Apply `|default:""` to these fields wherever they are printed, or wrap the block in `{% if %}` and skip the label:

- `newsCategory.description`, `news.content`
- `ektraCategory.description`, `ektra.content`, `ektra.pembina`, `ektra.hari`, `ektra.jadwal`
- `jurusan.deskripsi_singkat`, `jurusan.deskripsi_lengkap`, `jurusan.kaprodi_nama`, `jurusan.kaprodi_email`, `jurusan.kontak`, `jurusan.gedung`
- `Pengumuman.deskripsi`
- `guru_staff.deskripsi`
- `lab.deskripsi`
- `ProspekKarir.rata_gaji`
- `SchoolStatistics` text fields

Rules:
- Never print a bare label with an empty value. `Pembina: {{ ektra.pembina }}` must become conditional: show the row only when the value exists.
- Filter order matters: `{{ x.content|default:""|striptags|truncatewords:30 }}`, and wrap the `<p>` in `{% if x.content %}` so an empty paragraph is not rendered.
- Do not change any other filter, URL, loop or context variable.

### B. Local placeholder image
External `https://via.placeholder.com/...` is slow and shows cold grey boxes. A local warm asset already exists: `static/images/placeholder/warm.svg` (1200x800, warm sand + school icon, safe for `cover` cropping).

Replace every `https://via.placeholder.com/<any>` fallback with `{% static 'images/placeholder/warm.svg' %}`. Known locations:
- `index.html:669`
- `berita/berita.html:77,150,195`
- `berita/detail_berita.html:200`
- `program/jurusan/jurusan.html:253`
- `program/jurusan/detail_jurusan.html:230,631`
- `program/ektrakurikuler/ektrakurikuler.html:213,294`
- `program/ektrakurikuler/detail_ektrakurikuler.html:186,356`

For inline `style="background-image: url('...')"` the `{% static %}` tag works directly. Confirm each edited template has `{% load static %}` (add it right after `{% extends %}` if missing). Keep `object-cover` / `background-size` behaviour unchanged.

## Depends
TASK-003, TASK-004 approved (same files).

## Files
All `otak_aplikasi/templates/**/*.html` that print the nullable fields above or contain `via.placeholder.com`.

## Interfaces
No new template variables. Consumes tokens and markup from TASK-001..004. New static asset path: `images/placeholder/warm.svg`.

## Test
- `grep -r "via.placeholder.com" otak_aplikasi/templates` returns 0 hits.
- Fresh-process Django Client render of `/`, `/berita/`, `/pengumuman/`, `/program-studi/`, `/ektrakurikuler/`, `/profil-sekolah/`, `/guru-staff/`, `/fasilitas/`, `/kontak/` returns 200 and the HTML contains no `>None<`.
- `manage.py check` exit 0 (known `ckeditor.W001` acceptable).
- Do not restart the running waitress; verification uses a fresh process.

## Evidence

[EVIDENCE: RED] `env\Scripts\python.exe task005_check.py` → exit 1 → 12 `via.placeholder.com` hits; all 9 routes status 200 but `>None<` x6 on `/`, x6 on `/program-studi/`, x13 on `/ektrakurikuler/`.
[EVIDENCE: GREEN] `env\Scripts\python.exe task005_check.py` → exit 0 → 0 placeholder hits; 9 routes 200; 0 `>None<`, 0 bare `None`.

[EVIDENCE: FULL]
- `env\Scripts\python.exe task005_check.py` → exit 0 → 0 hits, 9/9 routes 200, 0 `None`.
- `task005_detail.py` (fresh process, DB-driven slugs) → exit 0 → `/berita/berita-sekolah-1/`, `/program-studi/rekayasa-perangkat-lunak/`, `/ektrakurikuler/futsal/` all 200, no `None`; `{% static %}` resolves to `/static/images/placeholder/warm.svg` on `/ektrakurikuler/`.
- Template compile pass: `get_template()` on all 12 edited templates → exit 0 → "compiled 12 templates OK".
- `env\Scripts\python.exe manage.py check` with deploy.bat env → exit 0 → only known `ckeditor.W001`.
- `grep -r "via.placeholder.com" otak_aplikasi/templates` → 0 hits.
- No Python/model/view/context changes, no data seeding, waitress untouched, no files outside `otak_aplikasi/templates/` edited.

### Changed files (12)
- `index.html` — content guards (news, berita), `jurusan.deskripsi_singkat` guard, 1 placeholder → static.
- `berita/berita.html` — 3 placeholders → static, 2 content guards.
- `berita/detail_berita.html` — meta description/og default, content guard, 1 placeholder.
- `pengumuman/pengumuman.html` — 3 `deskripsi` guards.
- `pengumuman/detail_pengumuman.html` — `deskripsi` guard.
- `program/jurusan/jurusan.html` — `deskripsi_singkat` guard, 1 placeholder.
- `program/jurusan/detail_jurusan.html` — 2 placeholders, `deskripsi_lengkap` if/else keeps fallback copy.
- `program/ektrakurikuler/ektrakurikuler.html` — 2 placeholders, content guards (3 spots), `default:""` on pembina/hari/jadwal, conditional `Pembina:` label.
- `program/ektrakurikuler/detail_ektrakurikuler.html` — 2 placeholders, excerpt guard, conditional Pembina/Jadwal info cards, content guard.
- `profil/fasilitas.html` — `lab.deskripsi` guard.
- `profil/guru-staff.html` — 2 `guru_staff.deskripsi` guards.
- `profil/profil_sekolah.html` — 1 `guru_staff.deskripsi` guard.

### Deliberately left alone
- `detail_jurusan.html:200` `deskripsi_singkat|default:"<long copy>"` and `:318` fallback copy kept as `{% else %}` (intentional editorial text, no `None`).
- `detail_jurusan.html:547,550,563,567` `kaprodi_nama/kontak/gedung` already had `{% if %}`+fallback.
- `profil_sekolah.html:215`, `guru-staff.html:133` `deskripsi` already had non-empty `default:` fallback.
- `fasilitas.html:127` external `lh3.googleusercontent.com` image fallback — not `via.placeholder.com`, outside brief B.
- `search_results.html:76` `result.description` is a computed search field, not a model field in the brief; no `None` observed.
- `{{ day }}` loop and `pengumuman_penting.tanggal` known pre-existing issues untouched.
- NOTE for Conductor: `staticfiles/images/placeholder/warm.svg` is not yet collected; WhiteNoise serves `STATIC_ROOT`, so `collectstatic` (already part of `deploy.bat`) is required for the asset to resolve on the live server. Not run here to respect scope.

## Review (2026-11-26)

Spec check, all four points verified by read/grep:
- `grep -r "via.placeholder.com" otak_aplikasi/templates` → 0 hits. No `dummyimage`/`picsum` either.
- 12 `{% static 'images/placeholder/warm.svg' %}` fallbacks, exactly the 12 locations in the brief (`index.html:76,700,733`, `berita.html:77,149,196`, `detail_berita.html:200`, `jurusan.html:210`, `detail_jurusan.html:232,628`, `ektrakurikuler.html:225,306`, `detail_ektrakurikuler.html:186,356`). `static/images/placeholder/warm.svg` exists and is 1200x800 warm sand.
- Every edited template that uses `{% static %}` has `{% load static %}` (all 12, plus the 3 layouts).
- Nullable fields: `news.content` (index 85, 712, 745; berita 87, 173, 219), `jurusan.deskripsi_singkat` (index 424, jurusan 153), `jurusan.deskripsi_lengkap` (318 if/else), `kaprodi_nama/email/kontak/gedung` (547-567), `Pengumuman.deskripsi` (pengumuman 108/135/173, detail 113), `guru_staff.deskripsi` (profil_sekolah 216/240, guru-staff 134/158/201), `lab.deskripsi` (fasilitas 141), `rata_gaji` (jurusan 237), `ektra.content` (3 spots) all guarded with `|default:""` and/or `{% if %}`.
- `Pembina:` label rows are conditional: `ektrakurikuler.html:328` `{% if ektra.pembina %}`, `detail_ektrakurikuler.html:194-200` and `202-209` card-level `{% if %}`.
- `newsCategory.description`, `ektraCategory.description`, `SchoolStatistics` text fields are not printed by any template, so nothing to guard.
- Fields I checked that are *not* nullable in `models.py` (`FasilitasJurusan.deskripsi`, `ProspekKarir.deskripsi`, `Sertifikasi.penyelenggara`, `TestimoniAlumni.*`, `StaffDanGuru.deskripsi`) are left bare, correctly.
- Evidence RED/GREEN/FULL present, commands match the task test block.

[REVIEW: spec PASS]
[REVIEW: quality PASS]

[FINDING: Low] program/ektrakurikuler/ektrakurikuler.html:239,243 — the hero meta row prints `{{ hari|default:"" }} | {{ jadwal|default:"" }}`, so an empty pair renders a lone `|`; the pembina row leaves a person icon with no text. `pembina/hari/jadwal` are non-nullable and not `blank=True`, so this needs `''` data, hence Low. — Wrap the schedule span in `{% if ektra_utama.hari or ektra_utama.jadwal %}` and the pembina span in `{% if ektra_utama.pembina %}`.
[FINDING: Low] program/ektrakurikuler/ektrakurikuler.html:408-415 — the Pilihan card renders a person-icon row and a schedule-icon row with empty spans when the value is `''`. — Same `{% if %}` guard on both rows.
[FINDING: Low] program/ektrakurikuler/detail_ektrakurikuler.html:207-208 — inside the Jadwal card, `hari` and `jadwal` are two separate `<p>`, so one empty paragraph still renders when only the other is set. — Split into two `{% if %}` blocks.
[FINDING: Low] program/ektrakurikuler/detail_ektrakurikuler.html:166 — `{% if ektra.type_ektra == 'Wajib' %}bg-sand text-accent{% else %}bg-sand text-accent{% endif %}`: both branches identical. — Collapse to `bg-sand text-accent`.
[FINDING: Low] pengumuman/pengumuman.html:115,142 — `{{ pengumuman.tanggal|date:"d M Y" }}`: `Pengumuman` has no `tanggal` field, so the date slot renders empty (pre-existing, documented). — Track in a backend task or drop the slot.

Scope note for the Conductor: three external image fallbacks remain, all in TASK-004-owned files — `profil/fasilitas.html:71,127` and `profil/guru-staff.html:63` hotlink `lh3.googleusercontent.com`. They are outside brief B (`via.placeholder.com` only) and are tracked as a Medium finding in TASK-004.

## Status
[APPROVED-TASK]

