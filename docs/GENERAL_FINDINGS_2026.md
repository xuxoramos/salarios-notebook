# General Findings — SG Tech Pulse 2026 (Preliminary)

**Date:** 2026-07-21
**Data:** SG Tech Pulse 2026 live dump — 217 responses (165 completed). Base-salary analysis sample n=193.
**Status:** Preliminary. Self-selected respondents; presented as a respondent sample, not a population estimate.

**Overall median base salary: $75,000 MXN/month.**

---

## Executive summary

- **Seniority is by far the biggest salary lever**, followed by English usage, industry, and role. Together they explain ~61% of salary variance (adjusted R²).
- **English is close to a 2× salary factor**: those who work fully in English earn ~$100k vs ~$48.5k for those who never use it.
- **A cross-border premium is real**: the 18% who work for a foreign employer earn ~49% more (median $104.5k vs $70k).
- **AI is already reshaping how code gets written**: among those who answered, roughly half mostly instruct AI agents and review, rather than writing code by hand.
- **The sector is largely formal** (91% have social security), and **retention risk is salary-led** (the top reason people would leave is pay).

---

## 1. What drives salary (B1)

Incremental adjusted R² on log base salary (blocks added in order):

| Block added | Adjusted R² | ΔR² |
|---|---|---|
| Experience (tech years) | 0.14 | +0.14 |
| + English use | 0.28 | +0.16 |
| + **Seniority level** | 0.49 | **+0.23** |
| + Company size | 0.50 | +0.03 |
| + Industry | 0.55 | +0.10 |
| + Primary role | 0.61 | +0.09 |

**Seniority is the single largest lever** (+0.23), more than English, industry, and role. This confirms the redesign's central bet: a clean seniority ladder is the highest-value question in the instrument.

## 2. Compensation structure — role premiums (B2)

Median base monthly MXN by primary role (roles with n≥6):

| Role | Median | n |
|---|---|---|
| Engineering management | $120,000 | 7 |
| Architecture | $110,000 | 6 |
| Product management | $99,000 | 12 |
| Executive leadership | $95,000 | 27 |
| Data science / AI | $94,150 | 18 |
| DevOps / SRE / Infra | $72,500 | 8 |
| Software development (BE/FE/FS/Mobile) | $65,000 | 41 |
| Data engineering / ML | $65,000 | 13 |
| Software/data analyst | $55,000 | 15 |
| Project management | $52,500 | 8 |

Management, architecture, product, and data-science roles sit at the top; analyst and project-management roles at the bottom.

## 3. Cross-border / the global market (B3)

- **18%** work for a **foreign-headquartered employer**, and they earn a **~49% premium** (median $104.5k vs $70k domestic).
- Engagement structure among cross-border workers: local-representative contract (15), independent contractor (14), **Employer-of-Record / Deel-type (7)**, direct/other (2).
- 16 respondents are paid in USD.

This is the "Deel economy" the redesign flagged: a fifth of the market is plugged into foreign pay, at a large premium, largely outside domestic payroll structures.

## 4. English premium (B4)

Median base salary rises monotonically with English *usage*:

| English use at work | Median base |
|---|---|
| Never | $48,500 |
| Occasionally (docs) | $50,500 |
| Regularly (meetings, email) | $86,000 |
| Most of the time | $91,000 |
| All the time | $100,000 |

Working fully in English is associated with **~2× the salary** of never using it. Usage (not just self-assessed level) is a first-order salary signal.

## 5. AI adoption (B5)

- Of those who answered the code-generation question, roughly **half (24 of ~49)** say they *mostly instruct AI agents and review the output* rather than writing code by hand; another ~14 code manually with AI as support.
- **19 respondents already hold an AI-focused role.**
- Confidence that current skills stay relevant in 3 years averages **3.4 / 5** (moderate, not alarmed).

## 6. Formality & social protection (B6)

- **9%** have no social security — the tech sector is substantially more formal than the ~55% national informality rate.
- **20%** contribute to no retirement fund.
- **14%** carry education debt.

## 7. Financial resilience (B7)

- **58%** rate their ability to cover basic needs as comfortable (4–5 of 5).
- **Median savings rate is 12%** of monthly income (mean 20%): **58% save at least 10%**, ~17% save more than 30%, and **12% save nothing**.

## 8. Education pathways (B8)

- **57% learned in school**, 17% at work, 11% via online courses, 9% are non-developers, and only **5% via bootcamp** (1% primarily via AI).
- Self-rated relevance of formal education to current work averages **7.1 / 10**.

## 9. Retention & satisfaction (B9)

- **eNPS averages 7.7 / 10** (n=165) — respondents are broadly willing to recommend their employer.
- **The top reason people would leave is salary** (81), then career development (41), then remote work (18) and culture (10).
- **BP2C linkage is too thin to analyze**: only ~14 respondents report their employer is enrolled in Best Place to Code (109 No, 41 don't know). The certification-premium comparison needs more enrolled employers.

## 10. Inclusion — disability & neurodivergence (B10)

- **~7%** report a physical disability (12 of 168 answering).
- **~18%** report a diagnosed neurodivergence (30 of 167 answering) — a notable share worth a dedicated inclusion angle.

---

## Methodology

- Base monthly salary normalized to MXN (USD × FX 18.5; robust across FX 17–20); log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- Driver analysis uses incremental adjusted R² (adjusted for the number of predictors, since the full model has many dummies at n≈193).
- Descriptive statistics are medians/shares on available responses; thin subgroups flagged.
- Savings-rate responses normalized to a common percentage scale (decimal entries ×100); learning-path free-text variants consolidated.
- Self-selected sample; no population weights.

## Data-quality caveats

- **BP2C enrollment** has too few "yes" responses for the cross-survey premium comparison.
- **16 USD reporters** depend on a single FX assumption.

*(Fixed in this version: savings-rate encoding normalized and learning-path duplicates consolidated.)*
