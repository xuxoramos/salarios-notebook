# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

**Date:** 2026-07-21
**Data:** SG Tech Pulse 2026 live response dump — 217 responses (165 completed, 52 partial).
Gender: 154 men, 60 women, 2 non-binary, 1 unstated. Base-salary analysis sample: **n=192** (136 men, 56 women).
**Status:** Preliminary. Survey still open; sample is self-selected (not a probability sample of the market).

---

## Executive summary

1. **Women in tech earn a raw ~32% less** in base monthly salary than men ($55,000 vs $80,500 median).
2. **~25% of that gap survives full controls** for experience, seniority, role, industry, company size, and English. Most of the gap is *not* explained by women being more junior or in different roles.
3. **The gap is a top-of-the-ladder phenomenon:** near zero at mid-level, but ~29% at Senior and ~38% at Manager.
4. **Women are 28% of respondents but thin out above mid-level** (58% of Medio, ~20% of Senior+), a visible leak at the top.
5. Supporting gaps in access are **more modest than early small-sample figures suggested**, but the lived-experience signals (isolation, harassment, absent leadership programs) are concerning.

---

## 1. The gap (G1 raw, G2 adjusted)

**Raw gap.** Base monthly salary, median: men **$80,500** vs women **$55,000** → **−31.7%** (95% CI [10%, 53%]; mean gap 35%). The confidence interval is wide because the female sample is still small, but it excludes zero.

**Adjusted gap.** In a log-salary regression controlling for tech experience, seniority level, English use, role, industry, and company size, the female coefficient corresponds to a **~25–26% gap** (95% CI roughly [10–12%, 38%]); the lean and full specifications agree:

| Specification | Adjusted gap | 95% CI | R² | k |
|---|---|---|---|---|
| Lean (experience + seniority + English) | −26.3% | [12%, 38%] | 0.55 | 18 |
| Full (+ role + industry + company size) | −25.4% | [10%, 38%] | 0.77 | 73 |

**Interpretation:** most of the raw gap is unexplained by composition. The defensible headline is *"at the same level, role, and experience, women still earn about a quarter less."*

---

## 2. Where the gap opens (G3)

The gap is small at mid-level and widens sharply with seniority (tiers with fewer than 5 women suppressed):

| Tier | Men (median) | Women (median) | Gap | n (H / M) |
|---|---|---|---|---|
| Medio | $46,500 | $45,500 | −2% | 10 / 14 |
| Senior | $79,500 | $56,795 | **−29%** | 52 / 21 |
| Gerente | $96,500 | $60,000 | **−38%** | 30 / 7 (directional) |
| Junior / Staff-Principal / Director | — | — | suppressed | women <5 |

---

## 3. Representation and pipeline (G5)

- **Women are 27.8%** of respondents overall.
- **The distribution leaks at the top.** Female share by tier: Junior 19%, **Medio 58%**, Senior 28%, Staff-Principal 19%, Gerente 21%, Director 20%. Women concentrate at mid-level and thin out above it.
- **Pipeline origin gap:** women wrote their first program later (median **19 vs 17**) and had less childhood computer access (**40% vs 51%**).

---

## 4. Supporting access gaps (G4)

With the larger sample these are real but modest (women vs men, share and risk ratio):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 24% | 17% | 0.70 |
| Foreign employer | 20% | 14% | 0.70 |
| Fully remote | 46% | 46% | 1.00 (no gap) |
| AI-focused roles (count) | 14 | 5 | — |

Note: earlier launch-week figures were drawn from ~15 women and overstated some of these (e.g. equity looked like 3×, remote like 2×, AI roles 7-to-0). With 60 women the equity and foreign-employer gaps are ~0.70, the remote gap disappears, and women do appear in AI roles. Cite the values in this table, not the launch-week ones.

---

## 5. Women-only lived experience (G6)

Descriptive, women-only, n≈47, cells below threshold suppressed:

- **~30%** report having felt unsafe or experienced harassment ("rara vez" 26% + "frecuentemente" 4%).
- **68%** say their employer has **no formal program** to promote women into leadership.
- **49%** are 20% or less of their peer group (median 25% female peers) — half are a clear minority in their own team.

---

## Methodology

- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; conclusions are stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Adjusted gap:** OLS on log salary; female coefficient reported as `1 − exp(β)` with a normal-approximation CI.
- **Suppression:** any published cell with fewer than 5 women is withheld. Non-binary respondents (n=2) are excluded from inference.
- **Sample:** self-selected respondents; presented as a respondent sample, not a population estimate.

---

## Limitations

- **Small female sample** (56 with salary) → wide intervals, especially by tier.
- **No mechanism decomposition.** The deployed instrument dropped the negotiation / pay-transparency / promotion / sponsorship items from the redesign, so G2 yields an *unexplained residual*, not an attribution to specific channels. To explain *why* the gap persists, those questions need to return in the next wave.
- **Currency mix** (16 USD reporters) handled by a single FX assumption.
- **Preliminary:** figures will move as the survey fills; treat as directional.

---

## Implications (for AMITI / advocacy)

- The market-level message is defensible now: **an adjusted ~25% gap that widens at senior and management levels**, framed as a talent-supply problem (the sector loses senior women it can least afford to lose).
- The pipeline-origin and leadership-program findings point to concrete asks: early-STEM access for girls (childhood-computer and first-program-age gaps) and employer accountability on formal women-to-leadership programs.
- Before this goes external, the two priorities are: (1) grow the female sample further, and (2) restore the mechanism questions so the residual can be decomposed into negotiation, sponsorship, and promotion channels.
