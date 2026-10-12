# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

> 🔄 **Refreshed 2026-10-12** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 12 October 2026.csv`, 688 responses; 620 Mexico-resident). This supersedes the September-2026 figures (561 Mexico responses). Several September claims moved with the larger sample — see the change log at the bottom. **Downstream campaign assets** (gender-slides figures, Slidev decks, stat cards, `docs/ig_scripts/`) still hardcode the older numbers and must be regenerated from this version.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Date:** 2026-10-12
**Data:** SG Tech Pulse 2026 live dump, **restricted to Mexico-resident respondents** (90% of the sample). 620 Mexico responses. Gender: 382 men, 230 women, 5 non-binary. Base-salary analysis sample: **n=558** (341 men, 212 women).
**Status:** Preliminary. Survey still open; sample is self-selected (not a probability sample of the market).

---

## Executive summary

**In Mexican tech, women are the majority in the middle of the ladder and vanish on the way up — and the pay gap deepens as they climb toward the senior rungs.** Five findings:

1. **The compounding cost.** The raw median gap is **37%** ($75,000 men vs $47,250 women) and it deepens toward the senior rungs: **Medio −20%, Senior −25%** (the Gerente tier reads **−20%** but rests on just 15 women — directional).
2. **The vanishing.** Women are **61% of mid-level (Medio) roles but only ~30% of senior-and-above.** Majority in the middle, roughly one in three at the top — and the origin gaps (when they started, early computer access) have essentially closed, so this is a **pay-and-progression** story, not a pipeline-entry one.
3. **The residual.** Match a man and a woman on experience, seniority, role and English and about **four-fifths of the gap closes** — but a **~10% penalty survives** that nothing on paper explains. For a senior woman that is roughly **$6,800/month (~$82,000/year)**.
4. **The exit that doesn't rescue.** Women now reach foreign employers at the **same rate** as men (the July "male-only exit" is gone), yet at those employers they still earn **54% less** — the cross-border premium doesn't close the gap, it repeats it.
5. **The career pause (mechanism).** Women interrupt or scale back their careers >10 months for family/personal reasons **2.3× more** than men (16% vs 7%) — a plausible engine of the vanishing.

Raw gap 95% CI [29%, 46%] (bootstrap). Self-selected sample; treat as preliminary.

---

## Finding 1 — The compounding cost: a gap that widens with rank

**Raw gap.** Base monthly salary, median: men **$75,000** vs women **$47,250** → **−37%** (95% CI [29%, 46%], n=212 women).

**It widens toward the senior rungs:**

| Career stage | Men (median) | Women (median) | Gap | n (M / W) |
|---|---|---|---|---|
| Junior / Mid | $34,000 | $31,000 | **−9%** | 57 / 90 |
| Senior and above | $83,600 | $63,453 | **−24%** | 279 / 117 |

By individual tier: **Medio −20%, Senior −25%, Gerente −20%.** The gap deepens from Medio to Senior, but the Gerente tier now rests on only **15 women** — too thin to read as a trend (it was −32% in September), so treat it as directional; the clean monotonic "widens at every rung" pattern no longer holds. At the Junior tier alone women are nominally ahead, but that cell is small and volatile, so the early picture is anchored on the junior/mid band, where the gap is a modest −9%.

---

## Finding 2 — The vanishing: majority in the middle, one in three at the top

- Women are **38%** of Mexico respondents (of men+women), but the distribution thins with rank: **61% of both Junior and Medio roles are held by women, versus 32% of Senior, 20% of Staff/Principal and 25% of Gerente.** Majority in the base and the middle, roughly one in three at the top.
- The thinning lands exactly where the pay penalty (Finding 1) grows: fewer women *and* paid less, at the same rung.
- **The pipeline explanation is now dead.** With the larger sample the origin gaps have closed: median age at first program is **17 for both** genders, and childhood computer access is **51% (women) vs 48% (men)** — if anything women report slightly *more* early access. Women are not entering tech later or with less exposure; they are being held below the senior rungs.

---

## Finding 3 — The residual: the part no résumé explains

Line up a man and a woman with identical profiles — same experience, same seniority, same role, same English — and ask how much of the gap survives.

- **Oaxaca-Blinder** (Mexico, pooled reference) splits the **35% log gap** into **~82% explained** by composition (mostly seniority and role — i.e., the vanishing) and **~18% unexplained**.
- The single-equation adjusted gap — a woman identical on every measured control — is **~10%.**

Monetizing the ~10% residual:

| | Woman's median | Equivalent man | Monthly penalty | Annual penalty |
|---|---|---|---|---|
| Median woman | $47,250 | ~$52,500 | ~$5,250 | **~$63,000** |
| Senior woman | $60,000 | ~$66,800 | ~$6,800 | **~$82,000** |

For a senior woman, roughly **$6,800 a month — about $82,000 a year — is pay that nothing about her experience, level, role or English explains.**

> **Honest caveat:** this residual keeps *shrinking* — **~10%** now, versus ~12% in September and ~20% in July. More of the gap is now attributable to composition — which is not good news, because composition here means *the vanishing*: women are systematically kept off the senior, better-paid rungs. Closing the residual alone would barely move the 37%.

---

## Finding 4 — The exit that doesn't rescue

Working for a foreign employer is one of the biggest raises in the market. In July the concern was access — that the lane was essentially male. **That has flipped: women now reach foreign employers at the same rate as men.** But the rescue doesn't happen:

- Among foreign-employer workers, the gap is **54%** (men **$109,000** vs women **$50,000**, n=30 women) — *wider* than the 24% gap at senior levels domestically.

So the cross-border premium, held up as the escape hatch from low local pay, **reproduces the gap rather than closing it.**

Access ratios (Mexico residents, women vs men):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 16% | 17% | 1.06 (no gap) |
| Foreign employer | 14% | 14% | 1.00 (no gap) |
| Fully remote | 41% | 38% | 0.93 |
| AI-focused roles (count) | 37 | 17 | — |

Note: the July access gaps (equity, remote, foreign-employer) have essentially closed. The remaining access asymmetry is in **AI-focused roles** (men outnumber women ~2-to-1) — see the AI media stories.

---

## Finding 5 — The career pause (the mechanism)

The clearest candidate mechanism behind the vanishing shows up directly in the data: **women interrupt or scale back their careers for more than 10 months, for family or personal responsibilities, at 2.3× the male rate — 16% of women vs 7% of men.** In an industry that measures seniority by continuous years and visibility, a ten-month pause doesn't cost ten months of pay — it resets the promotion clock at exactly the life stage where the Medio→Senior jump is decided. Fewer women make that jump; the pyramid thins.

---

## Support — Women-only lived experience

Descriptive, women-only, Mexico residents; cells below threshold suppressed:

- **~25%** report having felt unsafe or experienced harassment at their current employer ("rara vez" 35 + "frecuentemente" 10, of 180 substantive answers) — roughly one in four, with 10 reporting it happens *frequently*.
- **65%** say their employer has **no formal program** to promote women into leadership (n=178).
- **55%** are 20% or less of their peer group (median 20% female peers) — a clear minority in their own team.

---

## Methodology

- **Geography:** restricted to **Mexico-resident respondents** (90% of the sample) so the "tech mexicano" framing matches the data.
- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Oaxaca-Blinder:** twofold decomposition with pooled reference coefficients over a parsimonious control set (experience, seniority rank, English use, role family). The single-equation adjusted gap is the coefficient on a female dummy in the same specification. The monetized penalty applies the ~10% residual to median salaries.
- **Suppression:** thin cells (e.g. Gerente n=15 women) flagged as directional. Non-binary respondents (n=5) excluded from inference.
- **Sample:** self-selected respondents; presented as a respondent sample, not a population estimate.

---

## Limitations

- **Tier cells still modest** (Gerente n=15 women; Staff/Principal still thin) → those tier gaps are directional.
- **No mechanism decomposition beyond the career-pause item.** The deployed instrument still lacks negotiation / pay-transparency / sponsorship items, so the ~10% residual is *unexplained*, not attributed to specific channels. To explain *why* the gap persists, those questions should return in the next wave.
- **Currency mix** (USD reporters) handled by a single FX assumption.
- **Preliminary:** figures will move as the survey fills.

---

## Change log vs the September 2026 version

- **Raw gap:** 38% → **37%** (n=212 women; CI tightened to [29%, 46%]).
- **Per-tier gaps:** Medio −22% → **−20%**, Senior −27% → **−25%**, Gerente −32% → **−20%**. The Gerente tier thinned to **15 women** and no longer extends the monotonic widening, so the framing moves from "widens at every rung" to **"widens toward senior,"** with Gerente flagged as directional.
- **Unexplained residual:** ~12% → **~10%**; Oaxaca "explained" share rose from ~80% to ~82%. The monetized senior-woman penalty fell from ~$7,700/mo (~$93,000/yr) to **~$6,800/mo (~$82,000/yr)**.
- **The exit that doesn't rescue:** the foreign-employer gap narrowed from 57% to **54%** (men $115,000 → $109,000; n women 27 → 30); access stays equal by gender (14%/14%).
- **The vanishing:** senior-and-above female share 31% → **30%**; total female participation 39% → **38%**; Staff/Principal share eased to 20%.

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
- Concrete asks: employer accountability on **pay-equity audits at every level** (not just the top); **formal women-to-leadership programs** (65% of women report none); and **structured career re-entry** so a family pause stops resetting the seniority clock.
- Before this goes external: (1) keep growing the tier-level female cells, and (2) restore the mechanism questions so the ~10% residual can be decomposed into negotiation, sponsorship, and promotion channels.
