# General Findings — SG Tech Pulse 2026 (Preliminary)

> 🔄 **Refreshed 2026-11-19** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 19 November 2026.csv`, 787 responses). This supersedes the 12-Oct-2026 figures (published as 688 responses).

**Date:** 2026-11-19
**Data:** SG Tech Pulse 2026 live dump — 787 responses (90% Mexico-resident). Base-salary analysis sample n=689.
**Status:** Preliminary. Self-selected respondents; presented as a respondent sample, not a population estimate.

**Overall median base salary: $60,000 MXN/month.**

---

## Executive summary

- **Experience is now the single biggest salary lever**, followed by seniority and English usage; company size, industry, and role add less. Together they explain ~54% of salary variance (adjusted R²).
- **English is roughly a 2.1× salary factor**: those who work fully in English earn ~$80k vs ~$37k for those who never use it.
- **A cross-border premium is real**: the 15% who work for a foreign employer earn ~36% more (median ~$81k vs ~$60k at non-foreign employers).
- **AI is already reshaping how code gets written**: among those who answered, roughly **half (117 of 232)** mostly instruct AI agents and review, rather than writing code by hand.
- **The sector is largely formal** (88% of those who answered have social security), and **retention risk is salary-led** (the top reason people would leave is pay, by a wide margin).

---

## 1. What drives salary (B1)

Incremental adjusted R² on log base salary (blocks added in order):

| Block added | Adjusted R² | ΔR² |
|---|---|---|
| Experience (tech years) | 0.17 | **+0.17** |
| + English use | 0.28 | +0.11 |
| + **Seniority level** | 0.42 | +0.14 |
| + Company size | 0.46 | +0.03 |
| + Industry | 0.52 | +0.06 |
| + Primary role | 0.54 | +0.03 |

**Experience (+0.17) is now the single largest lever**, followed by seniority (+0.14) and English (+0.11); industry (+0.06) adds a little more, and company size (+0.03) and role (+0.03) add little once seniority is in. In October experience and seniority were tied (+0.16 each); seniority now adds slightly less once experience and English are already in the model. It remains the second-largest lever, so the redesign's central bet holds: a clean seniority ladder is among the highest-value questions in the instrument.

## 2. Compensation structure — role premiums (B2)

Median base monthly MXN by primary role (roles with n≥6):

| Role | Median | n |
|---|---|---|
| Security / InfoSec | $92,000 | 15 |
| Executive leadership | $92,000 | 53 |
| Architecture | $90,000 | 29 |
| Engineering management | $79,000 | 15 |
| Data science / AI | $76,610 | 36 |
| Software development (BE/FE/FS/Mobile) | $70,000 | 198 |
| DevOps / SRE / Infra | $70,000 | 26 |
| Data engineering / AI / ML | $65,000 | 37 |
| Product management | $65,000 | 30 |
| Project management | $52,000 | 37 |
| QA / Testing | $51,500 | 38 |
| Software/data analyst | $50,000 | 32 |
| UX / UI Design | $45,500 | 22 |
| Technical support | $35,000 | 17 |

Security and executive leadership tie at the top ($92,000), with architecture ($90,000) and engineering management ($79,000) close behind; analyst, design, and support roles sit at the bottom, with technical support lowest ($35,000).

## 3. Cross-border / the global market (B3)

- **15%** of those who answered (n=743) work for a **foreign-headquartered employer**, and they earn a **~36% premium** (median $81,400, n=97, vs $60,000 at non-foreign employers).
- Engagement structure among cross-border workers: local-representative contract (38), independent contractor (38), **intermediary / Employer-of-Record — Deel, Remote (20)**.
- 53 respondents report pay in USD.

This is the "Deel economy" the redesign flagged: roughly a seventh of the market is plugged into foreign pay, at a meaningful premium, largely outside domestic payroll structures.

## 4. English premium (B4)

Median base salary rises steeply with English *usage*:

| English use at work | Median base | n |
|---|---|---|
| Never | $37,300 | 50 |
| Occasionally (docs) | $45,000 | 215 |
| Regularly (meetings, email) | $74,000 | 103 |
| Most of the time | $78,000 | 78 |
| All the time | $80,000 | 176 |

Working fully in English is associated with **~2.1× the salary** of never using it, with the jump concentrated between "occasionally" and "regularly." Usage (not just self-assessed level) is a first-order salary signal.

## 5. AI adoption (B5)

- Of the **232** who answered the code-generation question, **roughly half (117)** say they *mostly instruct AI agents and review the output* rather than writing code by hand.
- **73 respondents already hold an AI-focused role** — most commonly GenAI/LLM/Agent Engineer (21), AI product manager (16), Prompt manager (9), and ML Engineer (8). This is up sharply from the July sample (19) and is now a real occupational category.
- Confidence that current skills stay relevant in 3 years averages **3.3 / 5** — and, notably, is **flat across every experience level** (3.25 to 3.44 across experience bands; see the gender/AI media stories).

## 6. Formality & social protection (B6)

- **12%** have no social security — the tech sector is substantially more formal than the ~55% national informality rate.
- **26%** (about one in four) contribute to no retirement fund.
- **15%** carry education debt.

*Methodological correction:* the October version reported 10% / 21% / 12%. Those shares divided by all rows, so non-answers were counted as not reporting the condition, which deflated them. All three are now computed over respondents who answered each question (n=651 for social security; n=642 for retirement fund and education debt).

## 7. Financial resilience (B7)

- **66%** of those who answered rate their ability to cover basic needs as comfortable (4–5 of 5). *Methodological correction:* the October version reported 55%, computed over all rows (non-answers counted as not comfortable). On the answered basis October was 68%, so the underlying share is broadly stable.
- **Median savings rate is 10%** of monthly income (mean 18%): **69% save at least 10%**, ~13% save more than 30%, and **16% save nothing**.

## 8. Education pathways (B8)

- Shares of those who answered: **57% learned in school**, 15% at work, 9% via online courses, 12% are non-developers, and only **5% via bootcamp** (1% primarily via AI).
- Self-rated relevance of formal education to current work averages **7.2 / 10**.

## 9. Retention & satisfaction (B9)

- **Mean "recommend your employer" score is 7.6 / 10** (n=611) — respondents are broadly willing to recommend their employer.
- **The top reason people would leave is salary** (284), then career development (152), then remote work (78) and culture (42).
- **BP2C linkage is now analyzable-adjacent**: 103 respondents report their employer is enrolled in Best Place to Code (291 No, 179 don't know) — enough enrolled employers to begin a certification-premium comparison in the next pass.

## 10. Inclusion — disability & neurodivergence (B10)

- **~6%** report a physical disability (36 of 617 answering).
- **~15%** report a diagnosed neurodivergence (92 of 617 answering) — a notable share worth a dedicated inclusion angle.

---

## Methodology

- Base monthly salary normalized to MXN (USD × FX 18.5; robust across FX 17–20); log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- Driver analysis uses incremental adjusted R² (adjusted for the number of predictors, since the full model has many dummies).
- Descriptive statistics are medians/shares on available responses; thin subgroups flagged.
- Percentages are computed over respondents who answered each question.
- Savings-rate responses normalized to a common percentage scale (decimal entries ×100); learning-path free-text variants consolidated.
- Self-selected sample; no population weights.

## Data-quality caveats

- **53 USD reporters** depend on a single FX assumption.
- Answer values arrive in canonical Spanish regardless of the respondent's survey language.
- **Preliminary:** the survey is still open; figures will move as it fills.

---

## Changes vs the October 2026 version

- **Data:** 787 responses (October was published as 688); base-salary analysis sample n=689 (was 601).
- **Overall median base salary:** $64,000 → **$60,000 MXN/month**.
- **B1 lever ranking:** experience and seniority were tied (+0.16 each); experience is now the single largest lever (+0.17), ahead of seniority (+0.14) and English (+0.11). Cumulative adjusted R² 0.53 → 0.54.
- **B4 English premium:** ~2.4× → **~2.1×** (all the time vs never: $85,000 vs $35,800 → $80,000 vs $37,300).
- **B3 foreign-employer premium:** +31% → **+36%** (median $81,400 vs $62,000 → $81,400 vs $60,000).
- **Denominator rule (methodological correction, B6 and B7):** prevalence shares are now computed over respondents who answered each question. The October shares divided by all rows, which counted non-answers as "no" and deflated them: no social security 10% → 12%, no retirement fund 21% → 26%, education debt 12% → 15%, comfortable covering basic needs 55% → 66%.
