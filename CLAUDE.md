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

Slidev decks (in `redesign-2026/slidev-deck/` and `campaign/gender-slides/`; run `npm install` first in the deck directory):

```bash
npm run dev      # live preview
npm run export   # export to the committed PDF
```

There are no tests or linters.

## Data

- `data/answers-2020.csv` … `answers-2022.csv`: original survey answers. Values are coded keys; decode them with the lookup tables in `data/options/*_options.csv`.
- `data/Salarios2026-Dump - Encuesta de Salarios SG 2026.csv`: live response dump of the 2026 survey (still collecting; treat findings as preliminary).
- `data/ingles_gdl.csv`: per the spec, ignore this file.
- Analysis target is `salarymx`. Exclude other compensation fields (`salaryusd`, `extramx`, `extrausd`) as predictors.

## Methodology constraint (important)

This is a **causal inference** project, not a predictive-ML one — DAG-guided OLS with deliberately chosen controls, not R² maximization. Do not "improve" models by adding more features: mediators and colliders (e.g., `works_for_US_company` or current role when estimating the effect of English) invalidate the causal interpretation. The README explains the DAG, identification strategy, and why low R² is acceptable; `docs/SPECIFICATION.md` is the original project brief.

## How the pieces depend on each other

The pipeline is: raw survey CSVs → notebooks/scripts → findings docs → campaign assets.

- `docs/GENDER_FINDINGS_2026.md` and `docs/GENERAL_FINDINGS_2026.md` (+ `_ES_MX` versions) hold the **locked numbers**. Downstream assets hardcode these numbers rather than recomputing them: `campaign/gender-slides/make_figures.py`, both Slidev `slides.md` decks, the stat-card HTML files, and `docs/ig_scripts/`. If the analysis changes, update the findings docs first, then propagate to every downstream asset and regenerate figures/PDFs.
- `campaign/` pairs each asset with a blueprint doc for the comms team (e.g., `blueprint-cuanto-vale.md` documents strategy, copy, and design spec for `stat-cards-cuanto-vale.html`). Keep the HTML and its blueprint in sync when editing either. Stat-card HTML files are self-contained (no build step, no network).
- `redesign-2026/salarios_question_inventory_2026.csv` is the source of truth for the 2026 survey questions; `survey-rehearsal.html` is generated from it, never edited by hand.
- `pulse-result/` is a small FastAPI app deployed at `https://thedata.pub/pulse/mi-resultado` (Hetzner host `hetzner-web`, systemd unit `sg-pulse`, port 8020) that shows each new SurveySparrow respondent where their salary lands in the live distribution. See `pulse-result/README.md` for the webhook/redirect design and deploy commands.
- Everything in `output/` is generated but committed.
