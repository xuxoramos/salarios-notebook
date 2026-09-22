# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

> 🔄 **Refreshed 2026-09-21** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 21 September 2026.csv`, 622 responses; 561 Mexico-resident). This supersedes the July-2026 figures (270 Mexico responses). Several July claims moved with the larger sample — see the change log at the bottom. **Downstream campaign assets** (gender-slides figures, Slidev decks, stat cards, `docs/ig_scripts/`) still hardcode the older numbers and must be regenerated from this version.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Date:** 2026-09-21
**Data:** SG Tech Pulse 2026 live dump, **restricted to Mexico-resident respondents** (90% of the sample). 561 Mexico responses. Gender: 340 men, 213 women, 5 non-binary. Base-salary analysis sample: **n=500** (303 men, 197 women).
**Status:** Preliminary. Survey still open; sample is self-selected (not a probability sample of the market).

---

## Executive summary

**In Mexican tech, women are the majority in the middle of the ladder and vanish on the way up — and the pay gap widens at every rung they do climb.** Five findings:

1. **The compounding cost.** The raw median gap is **38%** ($76,000 men vs $47,000 women) and it widens with rank: **Medio −22%, Senior −27%, Gerente −32%.**
2. **The vanishing.** Women are **62% of mid-level (Medio) roles but only ~31% of senior-and-above.** Majority in the middle, roughly one in three at the top — and the origin gaps (when they started, early computer access) have essentially closed, so this is a **pay-and-progression** story, not a pipeline-entry one.
3. **The residual.** Match a man and a woman on experience, seniority, role and English and about **four-fifths of the gap closes** — but a **~12% penalty survives** that nothing on paper explains. For a senior woman that is roughly **$7,700/month (~$93,000/year)**.
4. **The exit that doesn't rescue.** Women now reach foreign employers at the **same rate** as men (the July "male-only exit" is gone), yet at those employers they still earn **57% less** — the cross-border premium doesn't close the gap, it repeats it.
5. **The career pause (mechanism).** Women interrupt or scale back their careers >10 months for family/personal reasons **2.3× more** than men (16% vs 7%) — a plausible engine of the vanishing.

Raw gap 95% CI [29%, 48%] (bootstrap). Self-selected sample; treat as preliminary.

---

## Finding 1 — The compounding cost: a gap that widens with rank

**Raw gap.** Base monthly salary, median: men **$76,000** vs women **$47,000** → **−38%** (95% CI [29%, 48%], n=197 women).

**It widens with seniority:**

| Career stage | Men (median) | Women (median) | Gap | n (M / W) |
|---|---|---|---|---|
| Junior / Mid | $35,000 | $32,000 | **−9%** | 53 / 84 |
| Senior and above | $85,000 | $63,453 | **−25%** | 247 / 109 |

By individual tier: **Medio −22%, Senior −27%, Gerente −32%** (Gerente n=14 women, directional). At the Junior tier alone women are nominally ahead, but that cell is small and volatile (n=26 women), so the early picture is anchored on the junior/mid band, where the gap is a modest −9%.

---

## Finding 2 — The vanishing: majority in the middle, one in three at the top

- Women are **39%** of Mexico respondents (of men+women), but the distribution thins with rank: **59% of Junior and 62% of Medio roles are held by women, versus 32% of Senior and 24–25% of Staff/Principal and Gerente.** Majority in the base and the middle, roughly one in three at the top.
- The thinning lands exactly where the pay penalty (Finding 1) grows: fewer women *and* paid less, at the same rung.
- **The pipeline explanation is now dead.** With the larger sample the origin gaps have closed: median age at first program is **17 for both** genders, and childhood computer access is **53% (women) vs 49% (men)** — if anything women report slightly *more* early access. Women are not entering tech later or with less exposure; they are being held below the senior rungs.

---

## Finding 3 — The residual: the part no résumé explains

Line up a man and a woman with identical profiles — same experience, same seniority, same role, same English — and ask how much of the gap survives.

- **Oaxaca-Blinder** (Mexico, pooled reference) splits the **36% log gap** into **~80% explained** by composition (mostly seniority and role — i.e., the vanishing) and **~20% unexplained**.
- The single-equation adjusted gap — a woman identical on every measured control — is **~12%.**

Monetizing the ~12% residual:

| | Woman's median | Equivalent man | Monthly penalty | Annual penalty |
|---|---|---|---|---|
| Median woman | $47,000 | ~$53,200 | ~$6,200 | **~$75,000** |
| Senior woman | $58,300 | ~$66,000 | ~$7,700 | **~$93,000** |

For a senior woman, roughly **$7,700 a month — about $93,000 a year — is pay that nothing about her experience, level, role or English explains.**

> **Honest caveat:** this residual is *smaller* than the July estimate (~12% vs the earlier ~20%). More of the gap is now attributable to composition — which is not good news, because composition here means *the vanishing*: women are systematically kept off the senior, better-paid rungs. Closing the residual alone would barely move the 38%.

---

## Finding 4 — The exit that doesn't rescue

Working for a foreign employer is one of the biggest raises in the market. In July the concern was access — that the lane was essentially male. **That has flipped: women now reach foreign employers at the same rate as men.** But the rescue doesn't happen:

- Among foreign-employer workers, the gap is **57%** (men **$115,000** vs women **$50,000**, n=27 women) — *wider* than the 25% gap at senior levels domestically.

So the cross-border premium, held up as the escape hatch from low local pay, **reproduces the gap rather than closing it.**

Access ratios (Mexico residents, women vs men):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 17% | 17% | 1.02 (no gap) |
| Foreign employer | 12% | 13% | 1.09 (no gap) |
| Fully remote | 40% | 37% | 0.91 |
| AI-focused roles (count) | 34 | 17 | — |

Note: the July access gaps (equity, remote, foreign-employer) have essentially closed. The remaining access asymmetry is in **AI-focused roles** (men outnumber women ~2-to-1) — see the AI media stories.

---

## Finding 5 — The career pause (the mechanism)

The clearest candidate mechanism behind the vanishing shows up directly in the data: **women interrupt or scale back their careers for more than 10 months, for family or personal responsibilities, at 2.3× the male rate — 16% of women vs 7% of men.** In an industry that measures seniority by continuous years and visibility, a ten-month pause doesn't cost ten months of pay — it resets the promotion clock at exactly the life stage where the Medio→Senior jump is decided. Fewer women make that jump; the pyramid thins.

---

## Support — Women-only lived experience

Descriptive, women-only, Mexico residents; cells below threshold suppressed:

- **~25%** report having felt unsafe or experienced harassment at their current employer ("rara vez" 34 + "frecuentemente" 8, of 166 substantive answers) — roughly one in four, with 8 reporting it happens *frequently*.
- **63%** say their employer has **no formal program** to promote women into leadership (n=167).
- **40%** are 20% or less of their peer group (median 20% female peers) — a clear minority in their own team.

---

## Methodology

- **Geography:** restricted to **Mexico-resident respondents** (90% of the sample) so the "tech mexicano" framing matches the data.
- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Oaxaca-Blinder:** twofold decomposition with pooled reference coefficients over a parsimonious control set (experience, seniority rank, English use, role family). The single-equation adjusted gap is the coefficient on a female dummy in the same specification. The monetized penalty applies the ~12% residual to median salaries.
- **Suppression:** thin cells (e.g. Gerente n=14, Junior n=26 women) flagged as directional. Non-binary respondents (n=5) excluded from inference.
- **Sample:** self-selected respondents; presented as a respondent sample, not a population estimate.

---

## Limitations

- **Tier cells still modest** (Gerente n=14, Staff/Principal n=8 women) → those tier gaps are directional.
- **No mechanism decomposition beyond the career-pause item.** The deployed instrument still lacks negotiation / pay-transparency / sponsorship items, so the ~12% residual is *unexplained*, not attributed to specific channels. To explain *why* the gap persists, those questions should return in the next wave.
- **Currency mix** (USD reporters) handled by a single FX assumption.
- **Preliminary:** figures will move as the survey fills.

---

## Change log vs the July 2026 version

- **Raw gap:** 40% → **38%** (tighter CI, n=197 women).
- **Unexplained residual:** ~20% → **~12%**; Oaxaca "explained" share rose from ~48% to ~80%. The gap is now more clearly a composition (vanishing) story than a pure-penalty one.
- **"Male-only exit" retired:** foreign-employer *access* is now equal by gender (RR 1.09); the story is the **57% pay gap at foreign employers**, not access.
- **Equity and remote access gaps:** essentially closed (RR 1.02 and 0.91).
- **New finding:** the **career-pause** item (16% women vs 7% men) is now surfaced as the leading candidate mechanism.
- **Origin gaps** (first-program age, childhood computer access): confirmed closed.

---

## Implications (for AMITI / advocacy)

- The reframe is the message: **women are the majority in the middle and vanish at the top.** This is a pay-and-progression problem, not a pipeline-entry one — the origin gaps have closed. Fix the promotion step, not just the intake.
- Concrete asks: employer accountability on **pay-equity audits at every level** (not just the top); **formal women-to-leadership programs** (63% of women report none); and **structured career re-entry** so a family pause stops resetting the seniority clock.
- Before this goes external: (1) keep growing the tier-level female cells, and (2) restore the mechanism questions so the ~12% residual can be decomposed into negotiation, sponsorship, and promotion channels.
