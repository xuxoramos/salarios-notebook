# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

> **"El tech mexicano les paga igual a las mujeres… hasta que valen más."**

**Date:** 2026-07-22
**Data:** SG Tech Pulse 2026 live response dump — 217 responses (165 completed, 52 partial).
Gender: 154 men, 60 women, 2 non-binary, 1 unstated. Base-salary analysis sample: **n=192** (136 men, 56 women).
**Status:** Preliminary. Survey still open; sample is self-selected (not a probability sample of the market).

---

## Executive summary

**Mexican tech pays women fairly, until they start to be worth more.** At junior and mid levels women earn as much as men or slightly more. Then, exactly at seniority and leadership, a penalty opens and never closes. This is not a pipeline problem; it is a ceiling that switches on at the top. Four findings:

1. **The toll.** Equal at junior/mid, but a **~37% penalty at senior and leadership** levels, and **half the raw gap is unexplained** by any difference in experience, level, or role (Oaxaca-Blinder).
2. **The vanishing.** Women are **62% of mid-level roles but only 27% of senior-and-above** — the headcount collapses exactly where the pay penalty appears.
3. **The unexplained pesos.** For a senior woman, roughly **$15,000/month (~$176,000/year)** is a pure penalty that nothing about her work explains.
4. **The male-only exit (directional).** The market's biggest raise — working for a foreign employer — carries a **63% gap** there; the escape hatch from low local pay is essentially male (small sample, n=11 women).

Raw gap: base monthly median **$80,500 (men) vs $55,000 (women), −32%**. Sample is self-selected and the female n is small; treat as preliminary and directional.

---

## Finding 1 — The toll: equal at the bottom, penalized at the top

**Raw gap.** Base monthly salary, median: men **$80,500** vs women **$55,000** → **−32%** (95% CI [10%, 53%]; mean gap 35%). Wide interval (small female sample), but it excludes zero.

**The gap is not flat — it switches on at the top.** Grouped by career stage:

| Career stage | Men (median) | Women (median) | Gap | n (H / M) |
|---|---|---|---|---|
| Junior / Mid | $32,000 | $37,623 | **women +18%** | 25 / 25 |
| Senior and above | $95,000 | $60,000 | **−37%** | 125 / 47 |

At junior and mid levels there is no male advantage (if anything women are slightly ahead, partly because women concentrate in the better-paid Medio tier). The penalty appears at senior and leadership levels and is large. By individual tier: Medio −2%, Senior **−29%**, Gerente **−38%** (n=7 women, directional).

**Half the gap is unexplained.** An Oaxaca-Blinder decomposition splits the raw gap into a part explained by measurable qualifications (experience, seniority, English, role) and a residual:

| Component | Share of raw gap |
|---|---|
| Explained by qualifications | ~50% |
| **Unexplained residual** | **~50% (a ~20% pure penalty)** |

An adjusted log-salary regression agrees: controlling for experience, seniority, role, industry, company size, and English, women still earn **~25% less** (95% CI ~[10%, 38%]). *Unexplained is not the same as proven discrimination — it also holds factors we did not measure, including the mechanism questions dropped from the deployed form (see Limitations).*

---

## Finding 2 — The vanishing: majority in the middle, one in four at the top

- **Women are 27.8%** of respondents overall, but the distribution collapses with seniority: **62% of mid-level (Medio) roles are held by women, versus only 27% of senior-and-above.** They are the majority in the middle and roughly one in four at the top.
- The collapse lands exactly where the pay penalty (Finding 1) appears: fewer women *and* paid less, at the same rung.
- **Pipeline origin gap (context):** women wrote their first program later (median **19 vs 17**) and had less childhood computer access (**40% vs 51%**).

---

## Finding 3 — The unexplained pesos

Half of the gap is a pure penalty. Applying the ~20% unexplained residual (Finding 1) to salaries:

| | Woman's median | Equivalent man | Monthly penalty | Annual penalty |
|---|---|---|---|---|
| Median woman | $55,000 | ~$68,500 | ~$13,500 | **~$162,000** |
| Senior woman | $60,000 | ~$74,700 | ~$14,700 | **~$176,000** |

For a senior woman, roughly **$15,000 a month, about $176,000 a year**, is money that nothing about her experience, level, or role explains.

---

## Finding 4 (directional) — The male-only exit

Working for a foreign employer is the single biggest raise in the market (+49% overall). But that lane is not equally open: **among foreign-employer workers the gap is 63%** (men $120,000 vs women $44,400, n=11 women). Every lever that raises pay — seniority, English, going global — *widens* the gap rather than closing it. Treat the 63% as directional (small female cell), but the pattern across all three levers is consistent.

Supporting access ratios (women vs men, share and risk ratio):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 24% | 17% | 0.70 |
| Foreign employer | 20% | 14% | 0.70 |
| Fully remote | 46% | 46% | 1.00 (no gap) |
| AI-focused roles (count) | 14 | 5 | — |

Note: earlier launch-week figures were drawn from ~15 women and overstated some of these (e.g. equity looked like 3×, remote like 2×, AI roles 7-to-0). With 60 women the equity and foreign-employer gaps are ~0.70, the remote gap disappears, and women do appear in AI roles. Cite the values in this table, not the launch-week ones.

---

## Support — Women-only lived experience

Descriptive, women-only, n≈47, cells below threshold suppressed:

- **~30%** report having felt unsafe or experienced harassment ("rara vez" 26% + "frecuentemente" 4%).
- **68%** say their employer has **no formal program** to promote women into leadership.
- **49%** are 20% or less of their peer group (median 25% female peers) — half are a clear minority in their own team.

---

## Methodology

- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; conclusions are stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Adjusted gap:** OLS on log salary; female coefficient reported as `1 − exp(β)` with a normal-approximation CI.
- **Oaxaca-Blinder:** twofold decomposition with pooled reference coefficients over a parsimonious control set (experience, seniority rank, English use, role family) to keep it estimable on the female subsample. The monetized penalty applies the unexplained log-point residual to median salaries.
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

- The reframe is the message: **it is not a pipeline problem, it is a promotion-and-pay ceiling.** Women reach mid-level in force and are paid fairly there; the sector then loses them, and underpays the ones who stay, exactly at senior and leadership. That is the talent the industry can least afford to lose.
- Concrete asks: employer accountability on **pay-equity audits at senior/leadership levels** and on **formal women-to-leadership programs** (68% of women report none); plus early-STEM access for girls (the first-program-age and childhood-computer gaps).
- Before this goes external: (1) grow the female sample, and (2) restore the mechanism questions so the ~50% unexplained residual can be decomposed into negotiation, sponsorship, and promotion channels.
