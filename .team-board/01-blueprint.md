# Blueprint: Warm Paper + Mixed Grid Redesign

Project: website-smknj (Django templates)
Domain: UI/UX visual redesign, no backend changes
Status: active

## Design direction: Warm Paper

Language: Indonesian. Keep brand blue, remove cold/sterile pure white feel.

### Tailwind token names (MUST use these exact names)

In every `tailwind.config` block (base + standalone templates), set:

```
colors: {
  "primary": "#0047AB",
  "brand": "#0047AB",
  "brand-dark": "#003380",
  "accent": "#00697A",
  "accent-bright": "#00B4D8",
  "page": "#F6F1E9",
  "background-light": "#F6F1E9",
  "surface": "#FFFDF8",
  "sand": "#EDE6D8",
  "line": "#DED5C6",
  "ink": "#0A192F",
  "muted": "#475569",
  "highlight": "#F2B84B",
  "background-dark": "#0A192F",
}
borderRadius: { "DEFAULT": "0.5rem", "lg": "0.75rem", "xl": "1rem", "2xl": "1.25rem", "3xl": "1.5rem", "full": "9999px" }
```

Semantic usage:
- Page background: `bg-page` (warm cream), never `bg-white`.
- Section background: `bg-page` or `bg-sand`; pure white only as card `bg-surface`.
- Card: `bg-surface border border-line shadow-sm`.
- Body text: `text-ink`; secondary: `text-muted`.
- Accent text/links: `text-accent` (6.26:1 on surface). `accent-bright` decorative only on dark surfaces.
- Highlight/CTA secondary: `bg-highlight` with `text-ink` (9.84:1).
- Primary CTA: `bg-primary text-surface` (8.44:1).

### Mechanical class replacements (apply only where semantic)

- `bg-white` -> `bg-surface` for sections/cards/inputs.
- `bg-white/5`, `bg-white/10`, `bg-white/20`, `bg-white/90` -> KEEP (translucent overlays on dark).
- `bg-gray-50`, `hover:bg-gray-50` -> `bg-sand`, `hover:bg-sand`.
- `bg-[#F8FAFC]` -> `bg-sand` or `bg-page`.
- `text-[#0A192F]` -> `text-ink`.
- `text-gray-400`, `text-gray-500` -> `text-muted` (for text).
- `border-gray-100`, `border-gray-200` -> `border-line`.
- Keep gradients, Material Symbols, Tailwind CDN.

### Grid vocabulary (mixed, not all cards)

1. Bento: 4-col grid with varied spans (2x2, 2x1, 1x1) for statistics and programs.
2. Editorial: featured item spans 2 cols + compact sidebar/list for news.
3. Modular 12-col: strict alignment for profile, facilities, staff.
4. Asymmetric split: 8/4 for hero, sambutan, detail headers.
5. List/row: compact rows for announcements and schedules.
6. Mosaic: varied image tiles for facilities/extracurricular galleries.
7. Zigzag: alternating image/text for program highlights.
8. Dashboard/KPI: stat tiles for school statistics.

Mobile rule: all grids collapse to 1 column; spans reset. Keep DOM order readable.

### Radius & spacing

- Cards: `rounded-2xl` (20px) default; small chips `rounded-xl`; hero panels `rounded-3xl`.
- Section rhythm: vary `py-16`, `py-20`, `py-24` by hierarchy; avoid identical everywhere.

### Accessibility

- 4.5:1 normal text, 3:1 UI boundaries.
- Focus rings visible (`focus:ring-2 focus:ring-primary`).
- Reduced motion respected; do not add new heavy animation.

### Verification (all tasks)

- `python D:\website-smknj\manage.py check` with env `DJANGO_SETTINGS_MODULE=web_smknj.production_settings` and required env vars from `deploy.bat`.
- `curl.exe` HTTP 200 on affected routes.
- Screenshot review by Conductor.
- No backend/Python changes.

## Ruling on worktrees

No `.git` repository exists. Conductor ruling: shared workspace, strictly non-overlapping file ownership per task. No worktree creation.
