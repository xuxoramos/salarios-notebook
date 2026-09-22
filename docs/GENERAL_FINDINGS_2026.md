# General Findings — SG Tech Pulse 2026 (Preliminary)

> 🔄 **Refreshed 2026-09-21** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 21 September 2026.csv`, 622 responses). This supersedes the July-2026 figures (217 responses). **Downstream campaign assets** (gender-slides figures, Slidev decks, stat-card HTML, `docs/ig_scripts/`) still hardcode the older numbers and must be regenerated from this version.

**Date:** 2026-09-21
**Data:** SG Tech Pulse 2026 live dump — 622 responses (90% Mexico-resident). Base-salary analysis sample n=544.
**Status:** Preliminary. Self-selected respondents; presented as a respondent sample, not a population estimate.

**Overall median base salary: $65,000 MXN/month.**

---

## Executive summary

- **Experience and seniority are the two biggest salary levers**, followed by English usage; company size, industry, and role add less. Together they explain ~55% of salary variance (adjusted R²).
- **English is close to a 2× salary factor**: those who work fully in English earn ~$80k vs $35k for those who never use it.
- **A cross-border premium is real**: the 14% who work for a foreign employer earn ~35% more (median $85k vs $63k domestic).
- **AI is already reshaping how code gets written**: among those who answered, exactly **half (94 of 188)** mostly instruct AI agents and review, rather than writing code by hand.
- **The sector is largely formal** (91% have social security), and **retention risk is salary-led** (the top reason people would leave is pay, by a wide margin).

---

## 1. What drives salary (B1)

Incremental adjusted R² on log base salary (blocks added in order):

| Block added | Adjusted R² | ΔR² |
|---|---|---|
| Experience (tech years) | 0.17 | +0.17 |
| + English use | 0.28 | +0.11 |
| + **Seniority level** | 0.44 | **+0.16** |
| + Company size | 0.48 | +0.04 |
| + Industry | 0.52 | +0.04 |
| + Primary role | 0.55 | +0.03 |

**Experience (+0.17) and seniority (+0.16) are the two largest levers**, with English (+0.11) close behind; company size, industry, and role add little once seniority is in. This confirms the redesign's central bet: a clean seniority ladder is among the highest-value questions in the instrument.

## 2. Compensation structure — role premiums (B2)

Median base monthly MXN by primary role (roles with n≥6):

| Role | Median | n |
|---|---|---|
| Security / InfoSec | $111,000 | 12 |
| Architecture | $95,000 | 24 |
| Executive leadership | $95,000 | 44 |
| Product management | $86,950 | 23 |
| Engineering management | $85,000 | 12 |
| Data science / AI | $76,220 | 31 |
| DevOps / SRE / Infra | $74,675 | 20 |
| Software development (BE/FE/FS/Mobile) | $70,800 | 168 |
| Data engineering / ML | $65,000 | 33 |
| Project management | $55,250 | 26 |
| QA / Testing | $53,070 | 33 |
| Software/data analyst | $50,000 | 27 |
| UX / UI Design | $35,000 | 18 |
| Technical support | $24,000 | 10 |

Security, architecture, leadership, product, and data-science roles sit at the top; analyst, design, and support roles at the bottom.

## 3. Cross-border / the global market (B3)

- **14%** work for a **foreign-headquartered employer**, and they earn a **~35% premium** (median $85k vs $63k domestic).
- Engagement structure among cross-border workers: local-representative contract (32), independent contractor (29), **intermediary / Employer-of-Record — Deel, Remote (14)**.
- 43 respondents report pay in USD.

This is the "Deel economy" the redesign flagged: roughly a seventh of the market is plugged into foreign pay, at a meaningful premium, largely outside domestic payroll structures.

## 4. English premium (B4)

Median base salary rises steeply with English *usage*:

| English use at work | Median base | n |
|---|---|---|
| Never | $35,000 | 37 |
| Occasionally (docs) | $49,580 | 148 |
| Regularly (meetings, email) | $75,000 | 85 |
| Most of the time | $79,500 | 64 |
| All the time | $80,000 | 155 |

Working fully in English is associated with **~2.3× the salary** of never using it, with the jump concentrated between "occasionally" and "regularly." Usage (not just self-assessed level) is a first-order salary signal.

## 5. AI adoption (B5)

- Of the **188** who answered the code-generation question, **exactly half (94)** say they *mostly instruct AI agents and review the output* rather than writing code by hand.
- **56 respondents already hold an AI-focused role** — most commonly GenAI/LLM/Agent Engineer (17), AI product manager (11), ML Engineer (7), and Prompt manager (6). This is up sharply from the July sample (19) and is now a real occupational category.
- Confidence that current skills stay relevant in 3 years averages **3.4 / 5** — and, notably, is **flat across every experience level** (see the gender/AI media stories).

## 6. Formality & social protection (B6)

- **9%** have no social security — the tech sector is substantially more formal than the ~55% national informality rate.
- **21%** contribute to no retirement fund.
- **12%** carry education debt.

## 7. Financial resilience (B7)

- **56%** rate their ability to cover basic needs as comfortable (4–5 of 5).
- **Median savings rate is 10%** of monthly income (mean 18%): **69% save at least 10%**, ~12% save more than 30%, and **15% save nothing**.

## 8. Education pathways (B8)

- **58% learned in school**, 15% at work, 9% via online courses, 11% are non-developers, and only **6% via bootcamp** (1% primarily via AI).
- Self-rated relevance of formal education to current work averages **7.3 / 10**.

## 9. Retention & satisfaction (B9)

- **Mean "recommend your employer" score is 7.6 / 10** (n=481) — respondents are broadly willing to recommend their employer.
- **The top reason people would leave is salary** (227), then career development (115), then remote work (64) and culture (30).
- **BP2C linkage is now analyzable-adjacent**: 95 respondents report their employer is enrolled in Best Place to Code (208 No, 138 don't know) — enough enrolled employers to begin a certification-premium comparison in the next pass.

## 10. Inclusion — disability & neurodivergence (B10)

- **~5%** report a physical disability (25 of 484 answering).
- **~15%** report a diagnosed neurodivergence (75 of 484 answering) — a notable share worth a dedicated inclusion angle.

---

## Methodology

- Base monthly salary normalized to MXN (USD × FX 18.5; robust across FX 17–20); log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- Driver analysis uses incremental adjusted R² (adjusted for the number of predictors, since the full model has many dummies).
- Descriptive statistics are medians/shares on available responses; thin subgroups flagged.
- Savings-rate responses normalized to a common percentage scale (decimal entries ×100); learning-path free-text variants consolidated.
- Self-selected sample; no population weights.

## Data-quality caveats

- **43 USD reporters** depend on a single FX assumption.
- Answer values arrive in canonical Spanish regardless of the respondent's survey language.
- **Preliminary:** the survey is still open; figures will move as it fills.
