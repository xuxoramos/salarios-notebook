# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Causal analysis of IT salary surveys for the Mexican market (Software Guru / SG), plus everything built on top of it: the 2026 survey redesign ("SG Tech Pulse 2026"), findings reports, slide decks, and social-media campaign assets. Most public-facing content is in Mexican Spanish; findings docs come in English/Spanish pairs (`X.md` / `X_ES_MX.md`).

## Commands

Python environment (venv already exists at `.venv`):

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

- Main analysis: `jupyter notebook notebooks/causal_analysis.ipynb` — writes figures to `output/figures/`. (`notebooks/salarios.ipynb` is the older exploratory notebook documenting what each survey field means.)
- Old-vs-new survey simulation: `python redesign-2026/simulation_old_vs_new.py` — writes to `output/simulation_results/`. Seeded (`np.random.seed(2026)`), so results are reproducible.
- Survey rehearsal form: `python redesign-2026/build_rehearsal_form.py` — regenerates `survey-rehearsal.html` from `salarios_question_inventory_2026.csv`. Re-run whenever the inventory CSV changes.
- Gender-slides figures: `python campaign/gender-slides/make_figures.py` — writes PNGs to `campaign/gender-slides/figures/`.
- Findings site data: `python campaign/findings-site/build_data.py` — recomputes `data.js`/`data.json` (Mexico-resident, from the current dump) for the scrollytelling site (`index.html`) and the report (`report.html`). Re-run after any dump refresh. Export the report PDF with headless Chrome: serve the folder (`python -m http.server --directory campaign/findings-site`) then `chromium --headless --no-pdf-header-footer --print-to-pdf=campaign/findings-site/SG-Tech-Pulse-2026-Hallazgos.pdf http://localhost:<port>/report.html`.

Slidev decks (in `redesign-2026/slidev-deck/` and `campaign/gender-slides/`; run `npm install` first in the deck directory):

```bash
npm run dev      # live preview
npm run export   # export to the committed PDF
```

There are no tests or linters.

## Data

- `data/answers-2020.csv` … `answers-2022.csv`: original survey answers. Values are coded keys; decode them with the lookup tables in `data/options/*_options.csv`.
- `data/Responses - Encuesta de Salarios SG 2026 - <date>.csv`: live response dump of the 2026 survey, latest by date (currently `12 October 2026.csv`, 688 responses; still collecting; treat findings as preliminary). Earlier dated dumps are superseded and removed.
- `data/ingles_gdl.csv`: per the spec, ignore this file.
- Analysis target is `salarymx`. Exclude other compensation fields (`salaryusd`, `extramx`, `extrausd`) as predictors.

## Methodology constraint (important)

This is a **causal inference** project, not a predictive-ML one — DAG-guided OLS with deliberately chosen controls, not R² maximization. Do not "improve" models by adding more features: mediators and colliders (e.g., `works_for_US_company` or current role when estimating the effect of English) invalidate the causal interpretation. The README explains the DAG, identification strategy, and why low R² is acceptable; `docs/SPECIFICATION.md` is the original project brief.

## How the pieces depend on each other

The pipeline is: raw survey CSVs → notebooks/scripts → findings docs → campaign assets. The **current live dump** is `data/Responses - Encuesta de Salarios SG 2026 - <date>.csv` (the latest by date); earlier dated dumps are superseded.

- **Numbers are not pinned — they are refreshed from the current dump.** `docs/GENDER_FINDINGS_2026.md` (Mexico-resident respondents only) and `docs/GENERAL_FINDINGS_2026.md` (full sample) (+ `_ES_MX` versions) are the **single source of truth** for the 2026 live findings, and are re-derived whenever a new dump lands — they are not frozen. `docs/media-stories/` (gender pieces Mexico-only, AI pieces full-sample) derive from them.
- **Refresh procedure when a new dump arrives** (do all, do not leave stale copies behind): (1) recompute and update both findings docs + their `_ES_MX` pairs from the new dump; (2) re-run `python campaign/gender-slides/make_figures.py` — it **computes every figure from the dump at runtime** (no hardcoded findings), so figures follow the data, then re-export the deck PDF (`npm run export` in `campaign/gender-slides/`); (3) refresh the prose assets that cite 2026 numbers — `campaign/gender-slides/slides.md`, `campaign/stat-cards-mujeres.html`, `campaign/stat-cards-cuanto-vale.html` + `blueprint-cuanto-vale.md`, and `docs/media-stories/` — sourcing every number from the findings docs, never from another asset; (4) re-run `python campaign/findings-site/build_data.py` — it **recomputes every number on the scrollytelling site + report from the dump at runtime** (Mexico-resident; nothing hardcoded in the HTML), so `index.html`/`report.html` follow the data, then re-export the report PDF (see Commands). Prefer **computing figures from the data** over hardcoding.
- **Not part of the 2026 refresh:** `docs/ig_scripts/` (the 10 Instagram reels + README) are built on the **older 2020–2022 causal study** (`notebooks/causal_analysis.ipynb`, n=5,798, regression coefficients like +$1,522/yr) — a different sample and a different quantity class (coefficients, not medians). Do **not** swap 2026 medians into them. `redesign-2026/slidev-deck/slides.md` is about the **survey redesign** (question inventory + Monte-Carlo simulation of the old-vs-new instrument), not live results — leave its design/simulation figures alone.
- `campaign/` pairs each asset with a blueprint doc for the comms team (e.g., `blueprint-cuanto-vale.md` documents strategy, copy, and design spec for `stat-cards-cuanto-vale.html`). Keep the HTML and its blueprint in sync when editing either. Stat-card HTML files are self-contained (no build step, no network).
- `campaign/findings-site/` is the **"Cuánto vale programar en México" scrollytelling site** (`index.html`, animated SVG, salary-journey narrative, Mexico-resident framing) and a **standalone print report** (`report.html` → committed `SG-Tech-Pulse-2026-Hallazgos.pdf`). Both load `charts.js` (the shared SVG chart engine, single source for figure logic) and `data.js` (computed by `build_data.py`). **Every number is computed from the dump — nothing is hardcoded in the HTML.** See `campaign/findings-site/README.md`.
- `redesign-2026/salarios_question_inventory_2026.csv` is the source of truth for the 2026 survey questions; `survey-rehearsal.html` is generated from it, never edited by hand.
- `pulse-result/` is a small FastAPI app deployed at `https://thedata.pub/pulse/mi-resultado` (Hetzner host `hetzner-web`, systemd unit `sg-pulse`, port 8020) that shows each new SurveySparrow respondent where their salary lands in the live distribution. See `pulse-result/README.md` for the webhook/redirect design and deploy commands.
- Everything in `output/` is generated but committed.
