# Review Log

[Init] No reviews yet.

## Accessibility audit

Target: http://127.0.0.1:8000 — 9 pages (`/`, `/berita/`, `/pengumuman/`, `/program-studi/`,
`/ektrakurikuler/`, `/profil-sekolah/`, `/guru-staff/`, `/fasilitas/`, `/kontak/`).
Standard: WCAG 2.2 AA. Method: Chrome DevTools MCP (live DOM, computed styles, keyboard walk,
screenshots) + template source.
Palette measured as-shipped: page `#F6F1E9`, surface `#FFFDF8`, ink `#0A192F`, primary `#0047AB`,
accent `#00697A`, accent-bright `#00B4D8`, highlight `#F2B84B`, sand `#EDE6D8`, line `#DED5C6`.

### Verdict: FAIL — 6 blocker groups, 12 major, 4 minor

Palette itself is sound. `#0047AB` on cream = 7.5:1, `#00697A` on sand = 5.12:1,
`#475569` muted on surface = 7.45:1, white on `#0047AB` = 8.3:1, `#F2B84B` on `#0047AB` = 4.64:1.
Contrast failures come from **accent-on-dark** and **accent-on-primary** combinations, not from the
cream redesign.

---

### Blockers

**B1 — Desktop nav dropdowns unreachable by keyboard** · `1.2.1`→`2.1.1` Keyboard · BLOCKER
`templates/layouts/navbar.html:33-102` (panels 41, 60, 90)
Submenus open only via `group-hover:opacity-100 group-hover:visible`; the panels also carry
`invisible`, so the links are removed from the tab order. The trigger `<button>` has no
`aria-expanded` / `aria-controls` and no click handler.
Evidence: Tab sequence on `/fasilitas/` = Beranda → Tentang Kami → Program → Informasi → Kontak;
submenu links never focused. `button.click()` on "Tentang Kami" leaves `visibility:hidden`.
Fix: toggle with `aria-expanded="false"` + `aria-controls`, open on click **and** `:focus-within`
(drop `group-hover` as the only trigger), close on `Escape` and on focus-out. Keep `hidden`/
`invisible` only while closed.

**B2 — Icon-only controls have no accessible name** · `4.1.2` Name, Role, Value · BLOCKER
`navbar.html:113-116` (search toggle), `:128-131` (mobile menu), `:146-149` (close search),
`footer.html:23-28` and `navbar.html:244-252` (social links).
Names resolve to the ligature text or nothing: `search`, `menu`, `close`, `public`, `photo_camera`,
`smart_display`. Social links are additionally `href="#"` (also `2.4.4` Link Purpose).
Fix: `aria-label="Buka pencarian"`, `aria-label="Menu utama"` + `aria-expanded`, `aria-label="Tutup pencarian"`,
`aria-label="Instagram"` etc., and real URLs.

**B3 — Accent text/icons on dark and on primary fail contrast** · `1.4.3` Contrast (Minimum) · BLOCKER
| Location | Pair | Ratio | Need |
|---|---|---|---|
| `templates/index.html:217` "Live Update" chip | `#00697A` on `#162539` | **2.44** | 4.5 |
| `templates/index.html:210` analytics icon | `#00697A` on `#082240` | **2.47** | 3.0 |
| `templates/program/ektrakurikuler/ektrakurikuler.html` hero stat icons (`groups`, `emoji_events`, `schedule`, `text-accent` on gradient) | `#00697A` on `#0047AB` | **1.33** | 3.0 |
Fix: on dark surfaces use `#00B4D8` (accent-bright, 7.14:1 on `#0A192F`); on primary use
`text-surface` or `text-highlight`. Do not use `text-accent` on `bg-background-dark`/`bg-primary`.

**B4 — Search inputs have no accessible name** · `3.3.2` Labels or Instructions · BLOCKER
`navbar.html:143` (`#desktop-search-input`), `navbar.html:159` (mobile `q`), and
`ektrakurikuler.html:262` (`name="search"`). Placeholder only; `/berita/` and `/pengumuman/`
do this correctly with a `<label>` — copy that pattern.
Fix: `<label for="…" class="sr-only">Cari …</label>` or `aria-label="Cari di situs"`.

**B5 — Search overlay input has no visible focus indicator** · `2.4.7` Focus Visible · BLOCKER
`navbar.html:143` — `focus:ring-0 focus:outline-none` yields
`outline: 2px solid transparent; box-shadow: 0 0 0 0`.
Fix: `focus:ring-2 focus:ring-primary focus:ring-offset-2` and remove `focus:outline-none`,
or add `.focus-ring` utility used sitewide.

**B6 — `/kontak/` and `/ektrakurikuler/` are not built on `base.html`** · `1.3.1` Info and
Relationships + `3.3.1` Error Identification · BLOCKER
`templates/kontak/kontak.html:1` and `templates/program/ektrakurikuler/ektrakurikuler.html:1`
start with `<!DOCTYPE html>` instead of `{% extends 'layouts/base.html' %}`.
Consequences: no `<main>` landmark (0 found), a duplicated navbar/footer that will drift from
`layouts/`, and the form error path below.
Fix: extend `base.html`, move page body into `{% block content %}`.

---

### Major

**M1 — No skip link** · `2.4.1` Bypass Blocks
`templates/layouts/base.html:107-113`. Keyboard users must tab through 9+ nav items on every page.
Fix: first focusable element `<a href="#main" class="sr-only focus:not-sr-only …">Lewati ke konten</a>`
and `<main id="main" tabindex="-1">`.

**M2 — Nav landmark unlabeled** · `1.3.1` / `2.4.1`
`navbar.html:1` `<nav id="main-navbar">` has no `aria-label`. On `/` there are two `nav` elements
(`#main-navbar` + `#jurusan-dots`), so the landmark list is ambiguous.
Fix: `aria-label="Navigasi utama"`. `#jurusan-dots` (`index.html:434`) already does this correctly —
`/pengumuman/` "Kategori Pengumuman" too. Use those as the pattern.

**M3 — Heading order broken** · `1.3.1` / `2.4.6`
- `jurusan.html:57` — four visible `<h3>` (jurusan strip) render **before** the `<h1>` at `:72`.
- `index.html:84` — `<h3>` news title inside hero, before `<h2>` at `:93`.
- `kontak.html:151` — `h1` → `h3` "Kirim Pesan" (skip).
- `ektrakurikuler.html:259` — `h1` → `h3` "Filter & Cari:", and `:327` `h2` → `h4` (card titles).
- `navbar.html:16` — logo text is `<h2>` on every page, before the page `<h1>`.
Fix: logo text → `<span>`/`<p>`; jurusan strip + filter label → `<p>`/`<span>`; card titles
`h4` → `h3` under their `h2`.

**M4 — Form errors are not identified or announced** · `3.3.1` Error Identification
`kontak.html:156-167` and `:169-214`.
- Server error path (`views.py` contact view) renders `messages.error` into a plain `div` with no
  `role="alert"`/`aria-live`; success and error share identical classes (`:159`).
- `#form-feedback` is `role="status"` (polite) only — wrong politeness for failures.
- No field gets `aria-invalid="true"` or `aria-describedby` pointing at its error text.
Fix: `role="alert"` on the messages block, per-field `<p id="nama-error">` + `aria-describedby`,
`aria-invalid` on failure, and a visual (not icon-only) error marker.

**M5 — Missing `autocomplete` on identity fields** · `1.3.5` Identify Input Purpose
`kontak.html:174` (nama), `:179` (email), `:187` (telepon).
Fix: `autocomplete="name"`, `autocomplete="email"`, `autocomplete="tel"`.

**M6 — Decorative Material Symbols exposed to assistive tech** · `1.3.1` / `4.1.2`
46/46 icons on `/kontak/`, 90/92 on `/ektrakurikuler/`, 71/78 on `/program-studi/` lack
`aria-hidden="true"`. Announced names become "Tentang Kami expand_more", "chevron_right Profil Sekolah",
and headings read as "contact_page Informasi Kontak", "stars Alumni Sukses".
`index.html` is inconsistent: `:57,62,66` are hidden correctly, `:210,340` are not.
Fix: `aria-hidden="true"` on every icon-only `<span class="material-symbols-outlined">`; keep the
visible text as the name.

**M7 — Map iframe has no title** · `4.1.2` Name, Role, Value
`footer.html:87` — `<iframe src="https://www.google.com/maps/embed…">` with no `title`.
Fix: `title="Peta lokasi SMK Nurul Jadid"`.

**M8 — Pagination controls do not exist** · `2.4.1` Bypass Blocks / navigation semantics
`views.py:95,131,228` paginate (staff 6, berita 7, pengumuman 6) but no template renders controls;
0 `?page=` links found on any page. Today the data fits one page, so no user is blocked yet — but
page 2 is unreachable the moment content grows.
Fix when adding: `<nav aria-label="Paginasi">` + `<a aria-current="page">` for the active number,
`rel="prev"`/`rel="next"`, and text labels on the arrow controls (not `‹`/`›` alone).

**M9 — No `aria-current` on the active nav item** · `2.4.8` Location (advisory at AA)
0 `[aria-current]` nodes sitewide; the current section is only implied by hover decoration.
Fix: `aria-current="page"` on the matching top-level link.

**M10 — `prefers-reduced-motion` ignored** · `2.3.3` Animation from Interactions (AAA) / vestibular risk
`base.html:86` `scroll-behavior: smooth`; `animate-fade-in-up` (0.8s), `animate-float` (6s infinite),
`animate-pulse`, plus 300–500 ms `transition-all` everywhere. Under
`emulate prefersReducedMotion: reduce`, `animationName: fadeInUp` still runs and
`scrollBehavior: smooth` — 0 matching media rules.
Fix:
```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
```

**M11 — `role="alert"` on static content** · `4.1.2` / `2.2.2`
`index.html:34` — the "pengumuman penting" pill is a static `div` with `role="alert"`; it fires a
spurious announcement on every page load and is not a live region.
Fix: drop `role="alert"`; make it a link to the announcement.

**M12 — `aria-label` on a generic `span`** · `4.1.2`
`index.html:225` — `<span aria-label="… Siswa">{{ total }}</span>`. `aria-label` is prohibited on
`role=generic`; most screen readers ignore it.
Fix: `<span role="text">`/visible text, or `aria-hidden` the digits and put the label in adjacent
text.

---

### Minor

- `index.html:434` carousel dots: 8×8 px `<button>`s, 18 px apart → `2.5.8` Target Size fails even
  the spacing exception. Fix: 24×24 hit area with an 8 px visual dot (`p-2 -m-2`), keep
  `aria-label="Halaman n"`.
- `footer.html:47,51,55,102,103` — `href="#"` dead links (Info PPDB, BKK, Kemitraan, Privacy, Terms).
  `2.4.4`.
- `pengumuman.html:191,284` empty-state icons `#DED5C6` on sand/surface = 1.17/1.43. `aria-hidden`
  already set, so decorative → advisory only. If they carry meaning, use `text-muted` (6.1:1).
- `program/jurusan/jurusan.html` — `warm.svg` decorative pattern carries `alt="{{ jurusan.nama }}"`,
  duplicating the adjacent heading. Use `alt=""`.

### Passing checks (no action)

- Image alt text: 0 missing `alt` on all 9 pages; values are meaningful ("Logo SMK Nurul Jadid",
  "Laboratorium Lab Multimedia").
- `role="img"` + `aria-label`: 0 unlabeled instances (`index.html:75,699,732` correct).
- Reflow: no horizontal overflow at 640 px or 320 px effective width (`1.4.10` pass).
- Labels on `/berita/`, `/pengumuman/` search and all 5 `/kontak/` fields: `label[for]` present.
- `lang="id"` on `<html>`; single `<h1>` per page.
- Touch targets: 7–18 undersized per page, all pass the `2.5.8` spacing exception except the dots.

---

### Keyboard + focus order map

`/fasilitas/` (representative, 26 Tab presses):

```
1  a.logo "SMK NURUL JADID"        y=23   224x43   UA outline (ok)
2  a "Beranda"                     y=26    81x36   ring-2 primary (ok)
3  button "Tentang Kami"           y=26   138x36   ring ok — submenu NEVER opens
4  button "Program"                y=26   102x36   same
5  button "Informasi"              y=26   109x36   same
6  a "Kontak"                      y=26    72x36   ring ok
7  button#search-toggle "search"   y=24    40x40   UA 1px only, no name
8  button "SPMB"                   y=24   116x40   UA 1px only
9  a "Telusuri Laboratorium"       y=564  258x48   ok
10 a.footer logo                   —      268x44   ok
11-13 a social icons (3x)          —       40x40   no name, href="#"
14-18 a footer quick links (5x)    —      268x20   20px high, spacing ok, href="#" on 3
19-22 iframe (map)                 —      266x158  outline:none  ← no indicator
23-24 a Privacy / Terms            —       93x20   ok
25 a FAB (visibility icon)         —       56x56   no accessible name
```

Failures visible in this single walk: B1 (steps 3-5 dead-end), B2 (steps 7,8,11-13,25 unnamed),
M1 (no skip link, step 1 lands on logo), M7 (step 19-22), plus `#main-navbar` unlabeled.
`/kontak/` overlay search: `focus:ring-0 focus:outline-none` → `outline: 2px solid transparent`,
`box-shadow: 0 0 0 0` = invisible focus (B5).


## Final pass (Conductor)
- Fixed a11y blockers from audit: main landmarks on 5 standalone templates, skip link + id=main-content, nav ria-label, dropdown group-focus-within, aria-labels on icon-only controls, search input labels, kontak form ole=status + autocomplete, footer iframe title, prefers-reduced-motion, heading order (navbar logo, jurusan tiles, index hero, kontak), removed ole=alert from static pill.
- Removed invented data in detail_jurusan.html: stat defaults 120/8/3/96% -> em dash + serapan_kerja, fake skills/facilities/careers/certs/kaprodi/phone/gedung -> honest notes or conditional rows.
- Ekstrakurikuler: ektra_wajib_list/ektra_pilihan_list context, {% empty %} now fires per section, dangling {% endif %} removed.
- Homepage Publikasi KPI uses erita_total (real count).
- News images 4:6 everywhere; homepage featured/teaser cards horizontal portrait; berita featured image column 200px; search results horizontal portrait.
- Admin CSS 404 fixed: custom_css -> css/jazzmin-custom.css, /static/css/jazzmin-custom.css returns 200.
- Evidence: 9 routes 200, no literal {{, exactly 1 <main> per page, 0 googleusercontent/ia.placeholder hits.

