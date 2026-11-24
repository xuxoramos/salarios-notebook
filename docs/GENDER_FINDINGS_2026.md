# Gender Pay Gap — SG Tech Pulse 2026 (Preliminary Findings)

> 🔄 **Refreshed 2026-11-19** from the current dump (`data/Responses - Encuesta de Salarios SG 2026 - 19 November 2026.csv`, 787 responses, 712 Mexico-resident). This supersedes the October-2026 figures (620 Mexico responses). Several October claims moved with the larger sample, and some prevalence rates were corrected to the answered-denominator rule. See the change log at the bottom.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Date:** 2026-11-19
**Data:** SG Tech Pulse 2026 live dump, **restricted to Mexico-resident respondents** (90% of the sample). 712 Mexico responses. Gender: 416 men, 287 women, 5 non-binary. Base-salary analysis sample: **n=642** (374 men, 262 women).
**Status:** Preliminary. Survey still open. The sample is self-selected (not a probability sample of the market).

---

## Executive summary

**In Mexican tech, women are the majority in the middle of the ladder and vanish on the way up, and the pay gap deepens as they climb toward the senior rungs.** Five findings:

1. **The compounding cost.** The raw median gap is **39%** ($73,900 men vs $45,000 women) and it widens toward the senior rungs: **Medio −10%, Senior −29%**, so the gap roughly triples from the middle tier to Senior. The Gerente tier reads **−22%** on just 22 women (directional), so the gap widens toward senior but does not grow at every rung.
2. **The vanishing.** Women are **59% of mid-level (Medio) roles but only 33% of Senior-and-above.** Majority in the middle, one in three at the top. The origin gaps are small or absent (median first-program age 18 for women vs 17 for men, and women report slightly *more* early computer access), so this is a **pay-and-progression** story, not a pipeline-entry one.
3. **Mostly the ladder, plus a small penalty.** Matching on experience, English, level and role, the gap falls from 39% to about **10%** in stages. That ~10% is now distinguishable from zero, but only just: **95% CI 1% to 19% (p≈0.035)**. The point estimate is unchanged from October. What changed is precision, with more responses. A same-profile penalty does exist, but it is small and imprecise, so we do not monetize it. The effect is **bounded between ~10% and 39%**, and the large, firm part of the gap is still the ladder: about **82%** is explained by composition, mostly level and role.
4. **The exit that doesn't rescue.** Women reach foreign employers at the **same rate** as men (13% vs 14%), yet at those employers they still earn **55% less** (32 women, directional). The cross-border premium doesn't close the gap, it repeats it.
5. **The career pause (mechanism).** Among those who answered, women interrupt or scale back their careers >10 months for family/personal reasons **2.3× more** than men (21% vs 9%). It is a plausible engine of the vanishing.

Raw gap 95% CI [30%, 46%] (bootstrap). Self-selected sample, treat as preliminary.

---

## Finding 1 — The compounding cost: a gap that widens toward the senior rungs

**Raw gap.** Base monthly salary, median: men **$73,900** vs women **$45,000** → **−39%** (95% CI [30%, 46%], n=262 women).

**It widens toward the senior rungs:**

| Career stage | Men (median) | Women (median) | Gap | n (M / W) |
|---|---|---|---|---|
| Junior / Mid | $34,500 | $32,750 | **−5%** | 68 / 107 |
| Senior and above | $80,750 | $58,000 | **−28%** | 300 / 146 |

By individual tier: **Medio −10%, Senior −29%, Gerente −22%.** The gap roughly triples from Medio to Senior. The Gerente tier reads lower than Senior and rests on only **22 women** (15 in October), still too thin to read as a trend, so treat it as directional. The pattern is "widens toward the senior rungs", not "widens at every rung". At the Junior tier alone women are nominally ahead, but that cell is thin and volatile (19 men), so the early picture is anchored on the junior/mid band, where the gap is a modest −5%.

---

## Finding 2 — The vanishing: majority in the middle, one in three at the top

- Women are **41%** of Mexico respondents (of men+women), but the distribution thins with rank: **women hold 66% of Junior and 59% of Medio roles, versus 34% of Senior, 23% of Staff/Principal and 32% of Gerente** (Senior-and-above combined: **33%**). Director reads 44%, but on a thin cell (n=32), so it is directional. Majority in the base and the middle, one in three at the top.
- The thinning lands exactly where the pay gap (Finding 1) grows: at Senior, women are 34% of the tier and earn 29% less. Fewer women *and* paid less, at the same rung.
- **The pipeline explanation does not hold.** The origin gaps are small or absent. Median age at first program is **18 for women vs 17 for men** (one year apart), and childhood computer access, among those who answered, is **61% (women) vs 58% (men)**. If anything, women report slightly *more* early access. Women are not entering tech with less exposure. They are being held below the senior rungs.

---

## Finding 3 — Where the gap comes from: the ladder

Line up a man and a woman and watch how much of the gap survives each control. It falls in an orderly way as you add them:

| Controls | Adjusted gap |
|---|---|
| None | **35%** |
| + experience | 24% |
| + English | 21% |
| + level (seniority) | 16% |
| + role | **10%** |

*The ladder is a regression on log salary, so its unadjusted row (35%) compares average log pay. It differs from the 39% raw gap, which compares medians. Both are correct; they measure the gap in different ways.*

- **Oaxaca-Blinder** (Mexico, pooled reference) splits the log gap into **~82% explained** by composition (mostly seniority and role, i.e., the vanishing) and **~18% unexplained**.
- The single-equation adjusted gap (a woman identical on every measured control) is **~10%** (10.2%, n=636). Its **95% CI runs from about 1% to 19%** (HC3 robust [0.7%, 18.7%], **p≈0.035**), and bootstrap intervals across five seeds agree (lower bounds 0.7% to 1.4%). The point estimate is the same as in October. What changed is precision: with more responses, the interval now clears zero, but only just. The residual is **robust to the FX assumption** (10% at FX 17, 18.5 and 20).
- So a same-profile penalty does exist, but it is small and imprecise. We **do not monetize it**, because an interval from 1% to 19% is too wide to turn into pesos. And unexplained is not proven discrimination: the residual also contains whatever the controls do not measure.

**Read it as bounds, not a point.** The gender effect is **bounded between ~10% (matching on everything) and 39% (unadjusted)**. And there is a statistical trap: controlling for level and role likely *understates* the effect, because level and role are themselves partly downstream of the same bias (women are held below the senior rungs). So the true value lives in that range, and even the low end (~10%) now sits above zero, if narrowly.

> **The firm message is still the ladder, not the penalty.** The large, statistically solid part of the gap is **progression**: women are kept on the lower-paid rungs (Finding 2). The slice that neither level nor role explains is real but small and imprecise. Closing that residual alone would leave most of the 39% in place. Do not call it proven discrimination.

---

## Finding 4 — The exit that doesn't rescue

Working for a foreign employer is one of the biggest raises in the market. In July the concern was access, that the lane was essentially male. **That has flipped: women now reach foreign employers at the same rate as men.** But the rescue doesn't happen:

- Among foreign-employer workers, the gap is **55%** (men **$110,000** vs women **$50,000**, n=32 women, directional). That is *wider* than the 28% gap across the Senior-and-above band.

So the cross-border premium, held up as the escape hatch from low local pay, **reproduces the gap rather than closing it.**

Access shares (Mexico residents, over those who answered each item):

| Access | Men | Women | RR (W/M) |
|---|---|---|---|
| Equity (stock/options/RSU) | 18% | 18% | ≈1.0 (no gap) |
| Foreign employer | 14% | 13% | ≈0.9 (no meaningful gap) |
| Fully remote | 45% | 37% | **0.82** |
| AI-focused roles (count) | 43 | 22 | — |

Note: equity and foreign-employer access are at parity, but the **fully remote gap has reopened** (RR 0.82, it read 0.93 in October), and **AI-focused roles** run nearly two to one (43 men vs 22 women). See the AI media stories.

---

## Finding 5 — The career pause (the mechanism)

The clearest candidate mechanism behind the vanishing shows up directly in the data: **among those who answered, women interrupt or scale back their careers for more than 10 months, for family or personal responsibilities, at 2.3× the male rate: 21% of women (n=222) vs 9% of men (n=338).** (The rate is now reported over those who answered the item. This is a methodological correction: the previously published 16% vs 7% counted non-answers as "no". The 2.3× ratio is unchanged.) In an industry that measures seniority by continuous years and visibility, a ten-month pause doesn't cost ten months of pay — it resets the promotion clock at exactly the life stage where the Medio→Senior jump is decided. Fewer women make that jump; the pyramid thins.

---

## Support — Women-only lived experience

Descriptive, women-only, Mexico residents. Cells below threshold suppressed. Percentages are over those who answered each item:

- **~25%** report having felt unsafe or experienced harassment at their current employer ("rara vez" 42 + "frecuentemente" 12, of 217 substantive answers, 222 including "prefiero no responder"). Roughly one in four, with 12 reporting it happens *frequently*.
- **65%** say their employer has **no formal program** to promote women into leadership (n=220).
- **54%** are 20% or less of their peer group (median 20% female peers, n=196). A clear minority in their own team.

---

## Methodology

- **Geography:** restricted to **Mexico-resident respondents** (90% of the sample) so the "tech mexicano" framing matches the data.
- **Denominators:** percentages are computed over respondents who answered each question. Non-answers are excluded, not counted as "no".
- **Salary:** base monthly, normalized to MXN (USD reports × FX 18.5; stable across FX 17–20). Log-transformed for the regression; outliers outside ~$8k–$400k trimmed.
- **Raw gap:** median (robust) with a 3,000-sample bootstrap 95% CI.
- **Oaxaca-Blinder and control ladder:** twofold decomposition with pooled reference coefficients over a parsimonious control set (experience, seniority rank, English use, role family). The control ladder reports the gap as each block is added in turn (none → experience → English → level → role). The single-equation adjusted gap is the coefficient on a female dummy in the full specification (n=636). Its 95% CI and p-value come from an analytic test with HC3 heteroskedasticity-robust standard errors, cross-checked with a bootstrap (1,000 replicates, repeated over five seeds, with every interval clearing zero). The residual is not monetized: its interval now excludes zero, but it is too wide (≈1% to 19%) to support a peso figure.
- **Suppression:** thin cells (e.g. Gerente n=22 women, Junior n=19 men, foreign-employer n=32 women) flagged as directional. Non-binary respondents (n=5) excluded from inference.
- **Sample:** self-selected respondents, presented as a respondent sample, not a population estimate.

---

## Limitations

- **Tier cells still modest** (Gerente n=22 women; Staff/Principal and Director still thin) → those tier gaps are directional.
- **The adjusted residual is only marginally distinguishable from zero** (p≈0.035, 95% CI ≈1% to 19%). It is small and imprecise, so it is not monetized, and an unexplained residual is not proof of discrimination. The firm finding is the raw gap (39%) operating through progression (the vanishing), not the residual.
- **Potentially endogenous controls.** Controlling for level and role may *understate* the gender effect, since women are held down on those same variables. That is why we report bounds (~10% to 39%) rather than a single point.
- **No mechanism decomposition beyond the career-pause item.** The deployed instrument still lacks negotiation / pay-transparency / sponsorship items, so the residual is *unexplained*, not attributed to specific channels. To explain *why* the gap persists, those questions should return in the next wave.
- **Currency mix** (USD reporters) handled by a single FX assumption.
- **Preliminary:** figures will move as the survey fills.

---

## Change log vs the October 2026 version

- **Raw gap:** 37% → **39%** (men $75,000 → $73,900, women $47,250 → $45,000, n women 212 → 262, 95% CI [29%, 46%] → [30%, 46%]).
- **Per-tier gaps:** Medio −20% → **−10%**, Senior −25% → **−29%**, Gerente −20% → **−22%** (n women 15 → 22, still directional). Bands: Junior/Mid −9% → **−5%**, Senior-and-above −24% → **−28%**. The gap now roughly triples from Medio to Senior. The framing stays **"widens toward senior"**, not "at every rung" (Gerente reads below Senior).
- **Adjusted residual:** same point estimate (**10.2%**), but it now clears zero. October's 95% CI [0%, 20%] (HC3 [−0.2%, 19.5%], p=0.054) touched zero. November's is **[0.7%, 18.7%], p=0.035**. The change comes from more precision, not a larger effect. The ladder moved from 35 → 25 → 22 → 15 → 10 to **35 → 24 → 21 → 16 → 10**. The Oaxaca split is unchanged (~82% explained, ~18% unexplained). New reading: a small, imprecise same-profile penalty. It is still not monetized, still not proven discrimination, and still reported as bounds (~10% to 39%).
- **The vanishing:** female share by tier Junior 61% → **66%**, Medio 61% → **59%**, Senior 32% → **34%**, Staff/Principal 20% → **23%**, Gerente 25% → **32%**, Director 41% → **44%**. Senior-and-above 30% → **33%**. Total female participation 38% → **41%**.
- **The exit that doesn't rescue:** the foreign-employer gap moved from 54% to **55%** (men $109,000 → $110,000, women unchanged at $50,000, n women 30 → 32).
- **Access (now over those who answered):** the **fully remote gap has reopened**, RR 0.93 → **0.82** (men 45% vs women 37%). Equity 16%/17% → **18%/18%** and foreign employer 14%/14% → **14%/13%** (men/women), both still at parity. AI-focused roles 37/17 → **43/22** (men/women), nearly two to one.
- **Origin:** median first-program age moved from 17 for both to **18 (women) vs 17 (men)**. Still a small gap.
- **Denominator rule (methodological correction):** prevalence rates are now computed over those who answered each item, not over all rows (which counted non-answers as "no"). Career pause 16% vs 7% → **21% vs 9%** (same 2.3× ratio, corrected denominator). Childhood computer access 51% vs 48% → **61% vs 58%** (women still slightly ahead).
- **Support:** harassment still ~25% (now 42 + 12 of 217 substantive answers). No formal leadership program still 65% (n=220). Share who are ≤20% of their peer group 55% → **54%** (n=196).

---

## Change log vs the September 2026 version

- **Raw gap:** 38% → **37%** (n=212 women; CI tightened to [29%, 46%]).
- **Per-tier gaps:** Medio −22% → **−20%**, Senior −27% → **−25%**, Gerente −32% → **−20%**. The Gerente tier thinned to **15 women** and no longer extends the monotonic widening, so the framing moves from "widens at every rung" to **"widens toward senior,"** with Gerente flagged as directional.
- **Unexplained residual:** ~12% → **~10%**; Oaxaca "explained" share rose from ~80% to ~82%. **Methodological hardening:** we now report the control ladder (37% → 25% → 22% → 15% → 10%), the bootstrap 95% CI on the adjusted residual (**[0%, 20%], touches zero**), and its FX robustness (10% at FX 17/18.5/20). The monetized senior-woman penalty (~$6,800/mo) is retired, because the residual is not distinguishable from zero; the effect is reported as bounds (~10% to 37%).
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

- The reframe is the message: **women are the majority in the middle and vanish at the top.** This is a pay-and-progression problem, not a pipeline-entry one, because the origin gaps are small or absent. Fix the promotion step, not just the intake.
- Concrete asks: employer accountability on **pay-equity audits at every level** (not just the top); **formal women-to-leadership programs** (65% of women report none); and **structured career re-entry** so a family pause (21% of women vs 9% of men) stops resetting the seniority clock.
- Before this goes external: (1) keep growing the tier-level female cells, and (2) restore the mechanism questions so the ~10% residual, now narrowly above zero, can be decomposed into negotiation, sponsorship, and promotion channels.
