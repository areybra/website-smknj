# TASK-001

## Brief
Read `.team-board/01-blueprint.md` first. Apply the Warm Paper token system and semantic class mapping to the shared shell only:
- `otak_aplikasi/templates/layouts/base.html`
- `otak_aplikasi/templates/layouts/navbar.html`
- `otak_aplikasi/templates/layouts/footer.html`

Define all token names exactly as in blueprint in `tailwind.config`. Replace hardcoded `bg-white`, `text-[#0A192F]`, `text-gray-400`, `border-gray-100`, `bg-gray-50` with semantic tokens. Keep translucent white overlays on dark surfaces. Keep fonts, icons, animations. Footer/nav must use `bg-background-dark`, `bg-surface`, `text-ink`, `text-muted`, `border-line` appropriately. Add consistent focus rings on nav links if missing. Do not touch other files.

## Depends
None.

## Files
- `otak_aplikasi/templates/layouts/base.html`
- `otak_aplikasi/templates/layouts/navbar.html`
- `otak_aplikasi/templates/layouts/footer.html`

## Interfaces
Exports classes: `bg-page`, `bg-surface`, `bg-sand`, `border-line`, `text-ink`, `text-muted`, `text-primary`, `text-accent`, `bg-highlight`, `bg-background-dark`. Other tasks consume these.

## Test
`curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8000/` must be 200. Django check must pass (see blueprint env).

## Status
[VERIFIED]
[NEXT: @auditor]

## Evidence
[EVIDENCE: RED] powershell token/legacy-class grep over the 3 target files → exit 1 → FAIL missing="brand","brand-dark","accent-bright","page","sand","line","ink","muted","highlight"; bad_matches=47
[EVIDENCE: GREEN] same grep after edits → exit 0 → PASS tokens+legacy classes; 0 legacy hardcodes remain
[EVIDENCE: VERIFY] token/ring grep → exit 0 → PASS; rings=10; no duplicate ring classes; Django tags and structure intact
[EVIDENCE: FULL] env DJANGO_SETTINGS_MODULE=web_smknj.production_settings + deploy.bat env values → `D:\website-smknj\env\Scripts\python.exe D:\website-smknj\manage.py check` → exit 0 → only known ckeditor.W001 warning; `curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8000/` → HTTP_CODE=200

[EVIDENCE: FULL] FRESH verifier run (no prior reports trusted). Command: PowerShell set env DJANGO_SETTINGS_MODULE=web_smknj.production_settings + all 10 deploy.bat env values, then `& 'D:\website-smknj\env\Scripts\python.exe' 'D:\website-smknj\manage.py' check 2>&1` → exit 0 → only ckeditor.W001 warning, 0 silenced, 0 errors (acceptable).
[EVIDENCE: FULL] FRESH verifier run. Command: `$code = & curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8000/` → exit 0 → HTTP_CODE=200.
[EVIDENCE: FULL] FRESH verifier run. Command: PowerShell regex grep over base.html/navbar.html/footer.html. Result: TOKENS_MISSING= (all 14 required token names present in base.html tailwind.config: primary, brand, brand-dark, accent, accent-bright, page, background-light, surface, sand, line, ink, muted, highlight, background-dark); FORBIDDEN_TOTAL=0 (no non-overlay bg-white, text-[#0A192F], text-gray-400/500, border-gray-100/200, bg-gray-50, bg-[#F8FAFC]); OVERLAYS_KEPT=3 (translucent bg-white/5 on dark kept per blueprint). All pass.

## Review
[REVIEW: spec PASS]
[REVIEW: quality PASS]

Verification notes:
- Token names in `base.html` `tailwind.config` match blueprint exactly: primary, brand, brand-dark, accent, accent-bright, page, background-light, surface, sand, line, ink, muted, highlight, background-dark. borderRadius matches. Extra `primary-dark` alias is intentional: grep found 37 legacy usages in TASK-004 templates; removing it would break those hover/gradient styles.
- Semantic mapping correct: body `bg-page text-ink`; navbar `bg-surface/95` + `border-line` + `text-ink`/`text-muted`; footer `bg-background-dark` + `text-surface` on dark. No non-overlay `bg-white`, `text-[#0A192F]`, `text-gray-400/500`, `border-gray-100/200`, `bg-gray-50`, or `bg-[#F8FAFC]` remains in the 3 files. The only `bg-white` hits are `bg-white/5` overlays on dark footer, as blueprint requires.
- Translucent overlays preserved: `bg-white/5`, `border-white/10`, `bg-primary/10`, `bg-accent-bright/10`, `bg-sand/50`, `bg-surface/95`.
- Django tags balanced and intact: base 12/12, navbar 31/31, footer 5/5 `{%`/`%}`; all `{% url %}`, `{% static %}`, `{% for %}`/`{% empty %}`/`{% endfor %}`, blocks and includes still present.
- Focus rings: 10 nav links/buttons carry `focus:ring-2 focus:ring-primary` (+ offset), matching evidence `rings=10`. Mobile search input uses `focus:ring-primary/20` plus `focus:border-primary`, still visibly focused.
- No unrelated files touched by this task: target-file mtimes 10:18-10:21; other recently modified templates map to TASK-002/003/004 ownership. No backend/Python edits in this task.
- Evidence RED/GREEN/VERIFY/FULL present and consistent with task test: Django check exit 0 (only known ckeditor.W001), curl HTTP 200.

[FINDING: Low] `navbar.html` — search-toggle, SPMB, mobile-menu-toggle and close-search buttons lack explicit `focus:ring-2 focus:ring-primary` while nav links have it — add the same ring classes to those four buttons for consistent keyboard focus styling.
[FINDING: Low] `base.html` — `fadeInUp` keyframes defined twice with different translateY values (20px in tailwind.config vs 30px in inline `<style>`) — consolidate to one definition; non-blocking, shell animation still works.

[APPROVED-TASK]
