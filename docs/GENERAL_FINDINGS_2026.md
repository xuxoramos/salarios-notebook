# General Findings — SG Tech Pulse 2026 (Preliminary)

> 🔄 **Refreshed 2026-10-12** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 12 October 2026.csv`, 688 responses). This supersedes the 21-Sep-2026 figures (622 responses). **Downstream campaign assets** (gender-slides figures, Slidev decks, stat-card HTML, `docs/ig_scripts/`) still hardcode the older numbers and must be regenerated from this version.

**Date:** 2026-10-12
**Data:** SG Tech Pulse 2026 live dump — 688 responses (90% Mexico-resident). Base-salary analysis sample n=601.
**Status:** Preliminary. Self-selected respondents; presented as a respondent sample, not a population estimate.

**Overall median base salary: $64,000 MXN/month.**

---

## Executive summary

- **Experience and seniority are the two biggest salary levers**, followed by English usage; company size, industry, and role add less. Together they explain ~53% of salary variance (adjusted R²).
- **English is roughly a 2.4× salary factor**: those who work fully in English earn ~$85k vs ~$36k for those who never use it.
- **A cross-border premium is real**: the 15% who work for a foreign employer earn ~31% more (median ~$81k vs ~$62k domestic).
- **AI is already reshaping how code gets written**: among those who answered, roughly **half (104 of 210)** mostly instruct AI agents and review, rather than writing code by hand.
- **The sector is largely formal** (90% have social security), and **retention risk is salary-led** (the top reason people would leave is pay, by a wide margin).

---

## 1. What drives salary (B1)

Incremental adjusted R² on log base salary (blocks added in order):

| Block added | Adjusted R² | ΔR² |
|---|---|---|
| Experience (tech years) | 0.16 | +0.16 |
| + English use | 0.26 | +0.10 |
| + **Seniority level** | 0.42 | **+0.16** |
| + Company size | 0.46 | +0.04 |
| + Industry | 0.50 | +0.04 |
| + Primary role | 0.53 | +0.02 |

**Experience (+0.16) and seniority (+0.16) are the two largest levers — now tied**, with English (+0.10) close behind; company size, industry, and role add little once seniority is in. This confirms the redesign's central bet: a clean seniority ladder is among the highest-value questions in the instrument.

## 2. Compensation structure — role premiums (B2)

Median base monthly MXN by primary role (roles with n≥6):

| Role | Median | n |
|---|---|---|
| Security / InfoSec | $111,000 | 12 |
| Architecture | $100,000 | 27 |
| Executive leadership | $95,000 | 47 |
| Engineering management | $85,000 | 12 |
| Software development (BE/FE/FS/Mobile) | $73,400 | 186 |
| Data science / AI | $72,610 | 32 |
| Product management | $72,500 | 28 |
| DevOps / SRE / Infra | $72,175 | 22 |
| Data engineering / ML | $66,000 | 34 |
| Project management | $55,500 | 29 |
| QA / Testing | $51,500 | 36 |
| Software/data analyst | $50,000 | 29 |
| UX / UI Design | $44,000 | 21 |
| Technical support | $30,000 | 11 |

Security, architecture, leadership, and engineering-management roles sit at the top; analyst, design, and support roles at the bottom.

## 3. Cross-border / the global market (B3)

- **15%** work for a **foreign-headquartered employer**, and they earn a **~31% premium** (median $81,400 vs $62,000 domestic).
- Engagement structure among cross-border workers: local-representative contract (36), independent contractor (35), **intermediary / Employer-of-Record — Deel, Remote (19)**.
- 48 respondents report pay in USD.

This is the "Deel economy" the redesign flagged: roughly a seventh of the market is plugged into foreign pay, at a meaningful premium, largely outside domestic payroll structures.

## 4. English premium (B4)

Median base salary rises steeply with English *usage*:

| English use at work | Median base | n |
|---|---|---|
| Never | $35,800 | 44 |
| Occasionally (docs) | $50,000 | 169 |
| Regularly (meetings, email) | $74,000 | 91 |
| Most of the time | $79,000 | 69 |
| All the time | $85,000 | 166 |

Working fully in English is associated with **~2.4× the salary** of never using it, with the jump concentrated between "occasionally" and "regularly." Usage (not just self-assessed level) is a first-order salary signal.

## 5. AI adoption (B5)

- Of the **210** who answered the code-generation question, **roughly half (104)** say they *mostly instruct AI agents and review the output* rather than writing code by hand.
- **61 respondents already hold an AI-focused role** — most commonly GenAI/LLM/Agent Engineer (18), AI product manager (13), Prompt manager (7), and ML Engineer (7). This is up sharply from the July sample (19) and is now a real occupational category.
- Confidence that current skills stay relevant in 3 years averages **3.4 / 5** — and, notably, is **flat across every experience level** (see the gender/AI media stories).

## 6. Formality & social protection (B6)

- **10%** have no social security — the tech sector is substantially more formal than the ~55% national informality rate.
- **21%** contribute to no retirement fund.
- **12%** carry education debt.

## 7. Financial resilience (B7)

- **55%** rate their ability to cover basic needs as comfortable (4–5 of 5).
- **Median savings rate is 10%** of monthly income (mean 18%): **70% save at least 10%**, ~12% save more than 30%, and **16% save nothing**.

## 8. Education pathways (B8)

- **58% learned in school**, 15% at work, 9% via online courses, 11% are non-developers, and only **6% via bootcamp** (1% primarily via AI).
- Self-rated relevance of formal education to current work averages **7.3 / 10**.

## 9. Retention & satisfaction (B9)

- **Mean "recommend your employer" score is 7.6 / 10** (n=481) — respondents are broadly willing to recommend their employer.
- **The top reason people would leave is salary** (249), then career development (127), then remote work (69) and culture (35).
- **BP2C linkage is now analyzable-adjacent**: 97 respondents report their employer is enrolled in Best Place to Code (243 No, 152 don't know) — enough enrolled employers to begin a certification-premium comparison in the next pass.

## 10. Inclusion — disability & neurodivergence (B10)

- **~6%** report a physical disability (31 of 535 answering).
- **~15%** report a diagnosed neurodivergence (78 of 535 answering) — a notable share worth a dedicated inclusion angle.

---

## Methodology

- Base monthly salary normalized to MXN (USD × FX 18.5; robust across FX 17–20); log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- Driver analysis uses incremental adjusted R² (adjusted for the number of predictors, since the full model has many dummies).
- Descriptive statistics are medians/shares on available responses; thin subgroups flagged.
- Savings-rate responses normalized to a common percentage scale (decimal entries ×100); learning-path free-text variants consolidated.
- Self-selected sample; no population weights.

## Data-quality caveats

- **48 USD reporters** depend on a single FX assumption.
- Answer values arrive in canonical Spanish regardless of the respondent's survey language.
- **Preliminary:** the survey is still open; figures will move as it fills.
