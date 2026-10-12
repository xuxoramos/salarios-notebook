# Findings site — "Cuánto vale programar en México"

A scrollytelling website plus a standalone print report for the SG Tech Pulse 2026
findings, told as a single salary-journey narrative. Mexican Spanish, doctrine style
(no intro phrases, no em dash, no semicolon). Matches the salarios.sg.com.mx look
(Bricolage Grotesque / Instrument Sans / IBM Plex Mono, bone/violet/lime/coral,
light-dark toggle).

## Files

- `index.html` — the scrollytelling site. Self-contained except for Google Fonts.
  Scroll-triggered reveal + animated SVG figures. Light/dark toggle.
- `report.html` — the standalone report, print-oriented layout (cover, acts,
  findings, methodology appendix). Figures static, forced light theme.
- `charts.js` — **the shared SVG chart engine.** Pure functions (barsH, compare,
  comparePct, pairBars, slope, shareBars, waterfall, waffle, donut) used by both
  `index.html` and `report.html`. Single source of truth for figure logic.
- `build_data.py` — recomputes **every number** from the current dump
  (Mexico-resident respondents, base monthly MXN, USD × 18.5, trimmed 8k–400k) and
  writes `data.js` (`window.SG_DATA`) + `data.json`. Documents the column mappings.
- `data.js` / `data.json` — generated. The pages read these; **nothing is hardcoded
  in the HTML.**
- `SG-Tech-Pulse-2026-Hallazgos.pdf` — the exported report (committed).

## Framing

The whole site is **Mexico-resident respondents only** (one coherent universe,
matching the gender findings doc and the media-stories). Every scene labels its `n`.
Gender findings mirror `docs/GENDER_FINDINGS_2026.md`.

## Rebuild (after a dump refresh)

```bash
source .venv/bin/activate
python campaign/findings-site/build_data.py           # regenerates data.js / data.json

# preview
python -m http.server 8099 --directory campaign/findings-site
# open http://localhost:8099/index.html  (site)  and  /report.html  (report)

# export the report PDF
chromium --headless --no-pdf-header-footer --virtual-time-budget=15000 \
  --print-to-pdf=campaign/findings-site/SG-Tech-Pulse-2026-Hallazgos.pdf \
  http://localhost:8099/report.html
```

The figures follow the data automatically — do not edit numbers by hand in the HTML.
Prose that cites a number pulls it from `window.SG_DATA`, so it never drifts.

## Deploy

Static files. Serve `index.html` (and `report.html`, `charts.js`, `data.js`) from any
static host, e.g. alongside `pulse-result` on thedata.pub. No build step, no backend.
