---
title: "Salary Survey Redesign 2026"
subtitle: "Product Owner Briefing"
author: "Software Guru — Data Team"
date: "March 2026"
theme: white
transition: slide
---

# Salary Survey Redesign 2026

**Product Owner Briefing**

Software Guru — Data Team | March 2026

::: notes
This presentation covers the rationale, structural changes, simulation evidence, and implementation roadmap for the 2026 Salary Survey redesign.
:::

---

## Why Redesign Now?

::: incremental

- BP2C just completed its redesign (45 Qs, Six-Lever Framework)
- The two surveys **overlap**: benefits, remote work, org type asked from the same perspective
- Respondents who take both: *"Didn't I already answer this?"*
- The Salary Survey's ~130-item checkbox design produces **diminishing analytical returns**

:::

::: notes
The BP2C redesign creates a natural window to also redesign the Salary Survey. The overlap problem is both a brand confusion issue and a data quality issue.
:::

---

## Three Goals

| # | Goal | One-liner |
|---|------|-----------|
| 1 | **Product separation** | No structural duplication with BP2C |
| 2 | **Policy impact** | Findings AMITI can carry to policymakers |
| 3 | **BP2C hook** | Create demand for certification without cannibalizing it |

. . .

### The governing rule

> **Salary Survey** = X-ray of the **MARKET** (supply, structure, prices)
>
> **BP2C** = X-ray of the **EMPLOYER** (culture, enablement, justice)

---

## What We're Removing

| Block | Items | Why |
|-------|-------|-----|
| Benefits (`ben_*`) | 18 | Employer attributes → BP2C |
| COVID-era (`covid_*`) | 5 | Outdated |
| Tech checkboxes (`lang_*`, `cert_*`, `act_*`, etc.) | ~133 | Sparse, low signal |
| Redundant compensation | 5 | Replaced by clearer fields |

. . .

**~165 items removed total**

::: notes
The benefits block was never in the causal model. COVID questions are 6 years old. The tech checkboxes consumed 40% of respondent time but contributed <5% of explanatory power.
:::

---

## What We're Adding

::: incremental

- **12 redesigned fields** — compensation disambiguation, seniority level, company size, industry, English behavioral anchor
- **13 tech stack fields** — role-first architecture replacing ~100 checkboxes
- **25 new policy questions** — 6 blocks for AMITI advocacy

:::

. . .

**62 total items** (down from ~130)

---

## The Biggest Gap: `seniority_level`

The old survey had `profile` (godin / independiente / emprendedor / directivo)

. . .

**Problems:**

::: incremental

- Mixes employment type with org level
- "Godin" is Mexican slang — won't work for LatAm
- No way to distinguish a Junior from a Senior developer

:::

. . .

**New:** Jr / Mid / Sr / Staff / Lead / Director+ / C-Level

. . .

**Simulation result:** This single field adds **+12.4 percentage points of R²**

::: notes
seniority_level is the single most impactful change in the entire redesign. Every compensation study in the world includes it. We didn't.
:::

---

## Tech Stack: From Checkboxes to Role-First

:::::::::::::: {.columns}
::: {.column width="45%"}

### Old Design

- 20 language checkboxes
- 8+ framework checkboxes
- 15 database checkboxes
- 27 certification checkboxes
- 26 activity checkboxes
- **~100 binary items**
- 8–12 min to complete

:::
::: {.column width="10%"}
→
:::
::: {.column width="45%"}

### New Design

- 1 primary role
- 1 primary language
- 1 primary framework
- 1 primary database
- 1 primary cloud
- **13 structured items**
- 2–3 min to complete

:::
::::::::::::::

::: notes
Single-select gives clean, non-overlapping groups. "Python developers earn X" is a real statement. "People who checked Python among other things earn X" is confounded.
:::

---

## New Policy Blocks (for AMITI)

| Block | Qs | What it enables |
|-------|:--:|-----------------|
| Labor Formality | 3 | First-ever tech-sector informality rate |
| Cross-Border Dynamics | 4 | Quantify the "Deel economy" and brain drain |
| Purchasing Power | 3 | City-by-city real wages index |
| Education ROI | 4 | Degree premium with modern controls |
| AI Impact | 4 | First LatAm AI adoption benchmark |
| Gender Pipeline | 4 | Diagnose pipeline vs. discrimination |

. . .

Each block → pre-drafted advocacy position for AMITI

::: notes
These blocks produce findings only institutions can act on. They are framed as AMITI advocacy ammunition, not neutral academic observations.
:::

---

## BP2C Hook: The Satisfaction Gap

Three outcome-only questions added to the Salary Survey:

::: incremental

- **eNPS** (0–10): "How likely to recommend your employer?"
- **leave_reason**: "Why would you leave?"
- **job_search**: "Are you actively looking?"

:::

. . .

### The narrative engine

> *"43% of tech professionals earning >$60K still report eNPS below 6.*
> *High salary alone does not predict satisfaction."*

. . .

The Salary Survey shows **what** → BP2C explains **why**

::: notes
These are outcome variables, not diagnostics. BP2C's Six Levers are the diagnostic. This asymmetry is the commercial engine.
:::

---

## Simulation Evidence

Monte Carlo simulation: n=6,000, calibrated to 2020–2022 real effect sizes

. . .

| Metric | Old | New | Change |
|--------|-----|-----|--------|
| Survey items | 130 | 62 | −52% |
| Completion time | 30 min | 14 min | −53% |
| **R²** | **0.340** | **0.490** | **+44%** |
| Usable responses | 5,066 | 5,695 | +629 |

::: notes
Both designs face the identical DGP. The R² improvement comes entirely from better question design, not more data.
:::

---

## Information Efficiency

| Metric | Old | New | Improvement |
|--------|-----|-----|:-----------:|
| R² per survey item | 0.003 | 0.008 | **+202%** |
| R² per minute | 0.011 | 0.035 | **+208%** |
| Effective info (R² × N) | 1,724 | 2,788 | **+62%** |
| Coeff. stability (bootstrap) | 5.17 | 0.69 | **−87%** |

. . .

**Every minute of respondent time delivers 3× more analytical signal**

::: notes
The coefficient stability improvement means our published findings will be more reproducible year over year. Less sampling noise in the estimates.
:::

---

## Where the R² Comes From

Starting from old-equivalent baseline (R² = 0.268):

| Block added | ΔR² |
|-------------|:----:|
| **seniority_level** | **+12.4 pp** |
| company_size | +2.4 pp |
| english_use | +1.8 pp |
| primary_role | +1.7 pp |
| industry | +1.5 pp |
| primary_language | +1.1 pp |
| cert_depth | +0.9 pp |
| Others | +0.5 pp |

. . .

**`seniority_level` > all tech questions combined**

---

## Respondent Experience

:::::::::::::: {.columns}
::: {.column width="50%"}

### Old (25–35 min)

1. Demographics *(2 min)*
2. Professional *(3 min)*
3. Compensation *(2 min)*
4. **100+ checkboxes** *(8–12 min)* ← fatigue zone
5. Benefits *(3 min)*
6. COVID *(2 min)*

**85% completion** (estimated)

:::
::: {.column width="50%"}

### New (12–15 min)

1. Demographics *(2 min)*
2. Professional + seniority *(3 min)*
3. Compensation *(2 min)*
4. **13 structured tech Qs** *(2–3 min)*
5. Policy blocks *(4–5 min)*
6. BP2C hook *(1 min)*

**95% completion** (estimated)

:::
::::::::::::::

---

## Implementation Roadmap

| Phase | What | When |
|-------|------|------|
| **1. Instrument design** | Finalize wording, user-test with 10–15 IT pros | Pre-launch |
| **2. Data collection** | Target 5,000+ MX (or 3,000+/country if LatAm) | 4–6 weeks |
| **3. Analysis** | Reproduce 2020–2022 model + new blocks | Post-collection |
| **4. Publication** | Public report + private AMITI Brief | — |

. . .

### Key decision pending

**Geographic scope:** Mexico-only or expand to Colombia, Argentina, Brazil?

::: notes
LatAm expansion transforms the product from a national report into a regional benchmark. But it requires 3,000+ per country and Portuguese localization for Brazil.
:::

---

## What Product Owners Need to Decide

::: incremental

1. **Geographic scope** — Mexico-only or LatAm expansion?
2. **Employer tagging** — opt-in company name field for cross-survey linking?
3. **Distribution channels** — which community partnerships to activate?
4. **AMITI Brief** — approve the private deliverable concept?
5. **Naming** — "Salary Survey" or rebrand (Radiografía del Talento Tech)?

:::

::: notes
These are the blocking decisions. The instrument design, question inventory CSV, and simulation evidence are ready. We need product direction on these five items.
:::

---

## Resources

- **REDESIGN_2026.md** — Full rationale (all 3 goals, all sections)
- **question_inventory_2026.csv** — 62-item question list (bilingual, with skip logic)
- **SIMULATION_FINDINGS.md** — Detailed simulation analysis
- **simulation_old_vs_new.py** — Reproducible simulation script
- **simulation_results/** — Raw CSV outputs

All on branch `redesign-2026`

---

## Summary

::: incremental

- **52% fewer questions**, **44% more explanatory power**
- One missing field (`seniority_level`) was costing us 12.4 pp of R²
- 3× information density per minute of respondent time
- 25 new policy questions enable AMITI advocacy — a new revenue channel
- 3 BP2C hook questions create commercial demand without cannibalizing
- Respondent experience improves from 30 min checkbox gauntlet to 14 min structured flow

:::

. . .

### Next step

Review the question inventory CSV and schedule the user-testing round

::: notes
The question inventory CSV is designed to be opened in Excel by product owners. Every row has bilingual wording, field type, options, skip logic, and a reference back to the rationale document.
:::
