# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

> **"En el tech mexicano, ser mujer cuesta desde el primer día, y cada ascenso lo encarece."**

**Date:** 2026-07-28
**Data:** SG Tech Pulse 2026 live response dump, **restricted to Mexico-resident respondents** (92% of the sample). 270 Mexico responses (212 completed). Gender: 170 men, 96 women, 4 non-binary. Base-salary analysis sample: **n=245** (154 men, 91 women).
**Status:** Preliminary. Survey still open; sample is self-selected (not a probability sample of the market).

---

## Executive summary

**In Mexican tech, being a woman costs from day one, and every promotion makes it more expensive.** The gap is already present in early career and compounds as women climb, reaching its widest at management. It is not only a pipeline problem; it is a penalty that grows with seniority. Four findings:

1. **The compounding cost.** A gap is present early (**~13% at junior/mid**) and grows with each step: **Medio −24%, Senior −28%, Gerente −42%**. Roughly **half the raw gap is unexplained** by any difference in experience, level, or role (Oaxaca-Blinder).
2. **The vanishing.** Women are **62% of mid-level roles but only 32% of senior-and-above** — the headcount thins exactly where the penalty grows.
3. **The unexplained pesos.** For a senior woman, roughly **$15,000/month (~$176,000/year)** is a pure penalty that nothing about her work explains.
4. **The male-only exit (directional).** The market's biggest raise — working for a foreign employer — carries a **58% gap** there; the escape hatch from low local pay is essentially male (small sample, n=12 women).

Raw gap: base monthly median **$79,500 (men) vs $48,000 (women), −40%** (95% CI [21%, 50%]). Self-selected sample; treat as preliminary.

---

## Finding 1 — The compounding cost: a gap from the start that grows with rank

**Raw gap.** Base monthly salary, median: men **$79,500** vs women **$48,000** → **−40%** (95% CI [21%, 50%]). The interval is now tighter (n=91 women) and firmly excludes zero.

**The gap is present early and compounds with seniority:**

| Career stage | Men (median) | Women (median) | Gap | n (H / M) |
|---|---|---|---|---|
| Junior / Mid | $34,500 | $30,000 | **−13%** | 30 / 34 |
| Senior and above | $90,300 | $70,000 | **−23%** | 124 / 57 |

By individual tier the widening is sharp: **Medio −24%, Senior −28%, Gerente −42%** (Gerente n=10 women, directional). At the very entry level (Junior alone) women are slightly ahead, but that cell is too small to be reliable (n=9 women), so the early gap is anchored on the junior/mid band.

**Half the gap is unexplained.** An Oaxaca-Blinder decomposition splits the raw gap into a part explained by measurable qualifications (experience, seniority, English, role) and a residual:

| Component | Share of raw gap |
|---|---|
| Explained by qualifications | ~48% |
| **Unexplained residual** | **~52% (a ~20% pure penalty)** |

*Unexplained is not the same as proven discrimination — it also holds factors we did not measure, including the mechanism questions dropped from the deployed form (see Limitations).*

---

## Finding 2 — The vanishing: majority in the middle, one in three at the top

- **Women are 36%** of respondents overall, but the distribution thins with seniority: **62% of mid-level (Medio) roles are held by women, versus 32% of senior-and-above.** Majority in the middle, roughly one in three at the top.
- The thinning lands exactly where the pay penalty (Finding 1) grows: fewer women *and* paid less, at the same rung.
- **Note on pipeline origin:** with the larger sample the origin gaps have nearly closed (first-program age 18 vs 17; childhood computer access 49% vs 51%), so the story is now clearly about *pay and progression*, not about women entering tech later or with less early access.

---

## Finding 3 — The unexplained pesos

**The intuition.** Line up a man and a woman with identical résumés on paper — same experience, same seniority, same role, same English. Oaxaca-Blinder asks how much of the pay gap survives that matching. About half of it closes (real differences in qualifications); the other half stays — two people who look the same on paper, still paid differently.

Half of the gap is a pure penalty. Applying the ~20% unexplained residual (Finding 1) to salaries:

| | Woman's median | Equivalent man | Monthly penalty | Annual penalty |
|---|---|---|---|---|
| Median woman | $48,000 | ~$59,700 | ~$11,700 | **~$141,000** |
| Senior woman | $60,000 | ~$74,600 | ~$14,600 | **~$176,000** |

For a senior woman, roughly **$15,000 a month, about $176,000 a year**, is money that nothing about her experience, level, or role explains.

---

## Finding 4 (directional) — The male-only exit

Working for a foreign employer is one of the biggest raises in the market. But that lane is not equally open: **among foreign-employer workers the gap is 58%** (men $115,000 vs women $48,500, n=12 women), versus 36% at domestic employers. Treat the 58% as directional (small female cell), but it is consistent with the broader pattern.

Supporting access ratios (Mexico residents, women vs men):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 22% | 19% | 0.85 |
| Foreign employer | 17% | 13% | 0.74 |
| Fully remote | 46% | 46% | 1.00 (no gap) |
| AI-focused roles (count) | 15 | 6 | — |

Note: the launch-week campaign figures (3× equity, 2× remote, 7-to-0 AI) were small-sample artifacts. With the current sample the equity gap is modest (RR 0.85), the remote gap is absent, and women appear in AI roles. Cite this table.

---

## Support — Women-only lived experience

Descriptive, women-only, n≈77, cells below threshold suppressed:

- **~33%** report having felt unsafe or experienced harassment ("rara vez" 27% + "frecuentemente" 6%).
- **69%** say their employer has **no formal program** to promote women into leadership.
- **54%** are 20% or less of their peer group (median 20% female peers) — over half are a clear minority in their own team.

---

## Methodology

- **Geography:** restricted to **Mexico-resident respondents** (92% of the sample) so the "tech mexicano" framing matches the data; the 23 non-Mexico responses (mostly US) are excluded.
- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; conclusions are stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Oaxaca-Blinder:** twofold decomposition with pooled reference coefficients over a parsimonious control set (experience, seniority rank, English use, role family) to keep it estimable on the female subsample. The monetized penalty applies the unexplained log-point residual to median salaries.
- **Suppression:** any published cell with fewer than 5 women is withheld. Non-binary respondents (n=4) are excluded from inference.
- **Sample:** self-selected respondents; presented as a respondent sample, not a population estimate.

---

## Limitations

- **Female sample still modest** (91 with salary) → intervals are tighter than before but tier-level cells (e.g. Gerente n=10, Junior n=9) remain thin; the Junior-alone result (women slightly ahead) is not reliable.
- **No mechanism decomposition.** The deployed instrument dropped the negotiation / pay-transparency / promotion / sponsorship items from the redesign, so the residual is *unexplained*, not attributed to specific channels. To explain *why* the gap persists, those questions need to return in the next wave.
- **Currency mix** (USD reporters) handled by a single FX assumption.
- **Preliminary:** figures will move as the survey fills; treat as directional.

---

## Implications (for AMITI / advocacy)

- The reframe is the message: **the penalty starts early and compounds with rank.** Women are already paid less in early career and the gap widens with every step to management. Half of it is unexplained by qualifications. This is a pay-and-progression problem, not a pipeline-entry one — especially now that the early-access gaps have essentially closed.
- Concrete asks: employer accountability on **pay-equity audits at every level** (not just the top) and on **formal women-to-leadership programs** (69% of women report none).
- Before this goes external: (1) keep growing the female sample, and (2) restore the mechanism questions so the ~52% unexplained residual can be decomposed into negotiation, sponsorship, and promotion channels.
