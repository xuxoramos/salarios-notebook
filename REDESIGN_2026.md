# Salary Survey Redesign 2026

## Context

Software Guru publishes two survey products aimed at the Mexican (and increasingly Latin American) IT labor market:

1. **Best Place to Code (BP2C):** An employer satisfaction survey that functions as a certification program. It asks employees about their *employer's behavior* — culture, benefits, enablement, fairness. In 2026 it is being relaunched with a redesigned 45-question instrument organized around six independent levers (Employer Fundamentals, AI Enablement, Techno-Anxiety Management, Algorithmic Justice, Employee Agency, Future Confidence).

2. **Salary Survey:** An individual-level survey of IT professionals capturing demographics, compensation, skills, and work arrangements. It has run since at least 2020, collecting ~5,798 usable responses across 2020–2022. The primary analytical output has been a causal model explaining monthly gross salary (salarymx) with 42 predictors at R²=38.74%.

Both surveys have historically been designed independently, leading to **topical overlap** (benefits, remote work, organizational type) and **ambiguous editorial boundaries**. The BP2C redesign creates an opportunity to also redesign the Salary Survey so the two instruments complement rather than compete.

This document details the rationale and implementation for three goals:

| # | Goal | What it means |
|---|---|---|
| 1 | **Product separation** | The Salary Survey and BP2C must be clearly distinct instruments with no structural duplication. |
| 2 | **Policy impact** | The Salary Survey must produce findings that governments, universities, and industry associations can act on. |
| 3 | **BP2C commercial hook** | The Salary Survey must create natural demand for BP2C certification without cannibalizing it. |

### Separation Principle

The governing design rule for all three goals:

```
Salary Survey = X-ray of the MARKET   (supply, structure, prices, risks)
BP2C          = X-ray of the EMPLOYER  (culture, enablement, justice, agency)
```

Any topic (AI, remote work, compensation) may appear in both surveys **only if the lens differs**: the Salary Survey asks the individual about their *market position*; BP2C asks the individual about their *employer's behavior*. The separation is by **unit of analysis and perspective**, not by topic.

---

## Goal 1: Product Separation

### 1.1 Rationale

When both surveys ask overlapping questions from the same perspective, they:
- Confuse respondents who take both ("Didn't I just answer this?")
- Dilute each product's brand ("What's the difference?")
- Create conflicting datasets that are hard to reconcile in published reports

The BP2C redesign already tightened its scope to six theory-grounded levers about employer behavior. The Salary Survey must now reciprocate by purging anything that measures employer quality and doubling down on market structure.

### 1.2 Questions to Remove from the Salary Survey

#### 1.2.1 Benefits Block (18 multi-select items)

**Current items:** Equity, car, family support, education, bonus, housing, parking, gas, gym, flex hours, home office, loans, health insurance (major/minor), life insurance, cafeteria, cellphone, vouchers.

**Why remove:** Every one of these describes an *employer-provided perk*. They are employer attributes, not labor market signals. BP2C's Employer Fundamentals lever (14 questions, Herzberg Two-Factor Theory) now covers this territory with psychometrically validated items designed for discriminant validity.

**What we lose:** Ability to correlate specific benefits with salary. This is an acceptable loss because:
- In the 2020–2022 causal analysis, individual benefits were not included as predictors (they were not in the 42-predictor model).
- Benefits correlate heavily with org type and seniority, making them confounded proxies rather than causal drivers.
- The cross-survey link (Goal 3) recovers this analysis: we can correlate BP2C employer scores with salary-survey compensation data by matching on employer identity.

**Implementation:**
- Drop all `ben_*` columns from the survey instrument.
- Archive the historical benefits data in the existing answer files (do not delete from 2020–2022 CSVs).
- In the published report, note: *"For employer-level benefits analysis, see the Best Place to Code certification report."*

#### 1.2.2 COVID Employer Support (`covid_apoyo`)

**Current items:** computadora, muebles, internet (multi-select asking whether the employer provided equipment/support during COVID).

**Why remove:** This asks "Did your employer do X?" — that is employer behavior, not market structure. Additionally, by 2026 the COVID-era framing is outdated.

**What to do with the underlying signal:** The *interesting* signal here is not "did your employer provide a desk" but "what is your work arrangement and who pays for the infrastructure?" This gets reframed as a market structure question (see Section 2.3 below).

**Implementation:**
- Drop `covid_apoyo` from the instrument.
- Retain `covid_remoto` (remote/onsite/hybrid) but rename it to a non-COVID framing — it becomes the standard `work_arrangement` question.
- Drop `covid_salario` and `covid_carga` (pandemic-specific, no longer relevant).

#### 1.2.3 Summary of Removals

| Block | Items removed | Replacement location |
|-------|--------------|---------------------|
| Benefits (`ben_*`) | 18 items | BP2C Employer Fundamentals |
| COVID employer support | 3 items | Reframed as market structure (Sec 2.3) |
| COVID salary impact | 1 item | Dropped (outdated) |
| COVID workload impact | 1 item | Dropped (outdated) |
| **Total** | **23 items removed** | |

### 1.3 Questions to Keep and Reframe

#### 1.3.1 Remote Work → Work Arrangement

**Current:** `remote` (Y/N binary), `covid_remoto` (remote/onsite/semipresencial)

**Problem:** The binary Y/N is too coarse, and `covid_remoto` frames this as a pandemic response rather than a structural market feature.

**Redesign:** Single question `work_arrangement` with options:
- Fully remote
- Hybrid (1–3 days in office/week)
- Fully on-site
- Nomadic / location-independent

**Why this framing:** Remote work is no longer an employer perk (that's BP2C territory) — it is a *labor market structural feature* that affects salary levels, geographic arbitrage, and cross-border dynamics. The causal model found +$12,213 MXN/month for remote workers; the redesign preserves this analysis while updating the framing.

#### 1.3.2 Employment Type (`emptype`)

**Current:** nomina, honorarios, freelance, hibrido, emprendedor, becario, estudiante

**Why keep:** Employment formality is a labor *market structure* variable, not an employer quality attribute. Whether someone is on nómina vs. honorarios determines their access to social security, tax treatment, and legal protections. BP2C wouldn't ask this — it certifies employers who are (presumably) all formal.

**Redesign:** Keep as-is, but enrich with two companion questions (see Section 2.2).

#### 1.3.3 Organization Type (`orgtype`)

**Current:** corp, startup, isv, itservices, freelance, gobierno, uni

**Why keep:** This describes the *type of market the respondent operates in*, not the quality of their employer. It is a market segmentation variable.

**Redesign:** Minor updates to categories to reflect 2026 market reality:
- Add: `ai_native` (companies whose primary product is AI/ML)
- Rename: `isv` → `product_company` (clearer label)
- Keep the rest.

### 1.4 Naming and Branding

The name "Salary Survey" is descriptively accurate but positions the product too narrowly. A salary survey implies you'll learn what people earn. A *market intelligence report* implies you'll learn how the market works.

**Candidate names:**
- **Radiografía del Talento Tech** (X-Ray of Tech Talent) — signals depth of analysis
- **Pulso Tech LATAM** — signals regional scope and currency
- **Encuesta de Mercado Laboral Tech** — most descriptively accurate

**Recommendation:** Choose the name *after* the geographic expansion decision (Section 2.8) is made, since the scope affects the branding. For now, continue with "Salary Survey" as a working title.

### 1.5 Improvements to Retained Questions

Several retained questions have analytical weaknesses that accumulate into measurement noise and wasted survey space. These are changes to existing fields, not new blocks.

#### 1.5.1 Compensation: Disambiguation

**Problem:** `salarymx` asks "monthly gross salary" without specifying whether it includes prorated bonuses, variable compensation, or equity. Different respondents interpret it differently, introducing noise into the most important variable in the survey.

**Current fields removed or replaced:**
- `salarymx` → replaced by `base_salary` + `total_cash_annual`
- `salaryusd` → dropped (redundant with `payment_currency` from Section 2.3; all respondents report in local currency, normalize during analysis)
- `extramx` / `extrausd` → dropped (captured by `total_cash_annual`)
- `variation` → replaced by `salary_change` + `salary_change_reason`

**Redesigned fields:**

| ID | Question | Type | Options |
|---|---|---|---|
| `base_salary` | ¿Cuál es tu salario mensual bruto BASE (antes de impuestos, sin incluir bonos ni compensación variable)? | Numeric | (local currency) |
| `total_cash_annual` | ¿Cuál fue tu compensación total en efectivo en los últimos 12 meses (incluyendo salario, bonos, aguinaldo, y cualquier otra compensación en efectivo)? | Numeric | (local currency) |
| `has_equity` | ¿Recibes compensación en acciones, opciones, o RSUs? | Single | Sí / No |
| `salary_change` | Comparado con hace 12 meses, tu compensación total... | Single | Aumentó >20% / Aumentó 10–20% / Aumentó 1–9% / Se mantuvo igual / Disminuyó |
| `salary_change_reason` | ¿A qué se debió el cambio principal? | Single | Promoción / Cambio de empresa / Ajuste anual / Cambio a moneda extranjera / Recorte / Otro / No cambió |

**Why:** `base_salary` is unambiguous and comparable across respondents. `total_cash_annual` captures the full picture (what `salarymx + extramx + aguinaldo + bonos` approximated). `has_equity` identifies the hidden salary tier increasingly common in tech. `salary_change_reason` decomposes salary growth into market forces vs. individual actions — AMITI can tell whether salary growth is market-driven or mobility-driven.

#### 1.5.2 Experience: Disambiguate Tech vs. Total

**Problem:** `experience` doesn't specify experience doing *what*. A career-switcher with 3 years in tech but 15 years total has a different salary profile than someone with 18 continuous years in software. The career-switcher segment is large and growing.

**Current fields removed or replaced:**
- `experience` → replaced by `experience_tech` + `experience_total`
- `seniority` (years in current role) → replaced by `tenure_current` (years at current company)

**Redesigned fields:**

| ID | Question | Type |
|---|---|---|
| `experience_tech` | ¿Cuántos años llevas trabajando profesionalmente en el sector de tecnología? | Numeric |
| `experience_total` | ¿Cuántos años de experiencia laboral total tienes (en cualquier sector)? | Numeric |
| `tenure_current` | ¿Cuántos años llevas en tu empresa actual? | Numeric |

**Why:** The delta (`experience_total - experience_tech`) identifies career switchers. `tenure_current` replaces `seniority` — company tenure predicts salary compression and flight risk better than role tenure. If career switchers earn less than lifelong tech workers at equal tech-experience levels, that's a reskilling policy finding.

#### 1.5.3 `profile` → `seniority_level`

**Problem:** The current `profile` field (godin, independiente, emprendedor, directivo, docente, estudiante, otro) mixes employment relationship (already covered by `emptype`) with seniority level (covered by nothing). "Godin" is Mexican slang — Colombian and Argentine respondents won't recognize it.

**Redesigned field:**

| ID | Question | Type | Options |
|---|---|---|---|
| `seniority_level` | ¿Cuál es tu nivel dentro de tu organización? | Single | Junior / Mid / Senior / Staff-Principal / Lead-Manager / Director+ / Founder-C-Level / No aplica (freelance, estudiante) |

**Why:** Seniority level is one of the strongest salary predictors in every developer survey globally, and the current survey doesn't capture it. A 3-year developer at "Senior" level earns differently from a 3-year developer at "Mid" level. This single field replaces `profile` with vastly more analytical value.

#### 1.5.4 Add Company Size

**Problem:** A backend developer at a 15-person startup and a backend developer at a 10,000-person bank have vastly different compensation structures. `orgtype` captures *type* but not *scale*.

| ID | Question | Type | Options |
|---|---|---|---|
| `company_size` | ¿Cuántos empleados tiene tu empresa (aproximadamente)? | Single | 1–10 / 11–50 / 51–200 / 201–1000 / 1001–5000 / 5000+ |

**Why:** Company size is a top-5 salary predictor in every compensation study. Its absence from the current survey is a significant analytical gap.

#### 1.5.5 Add Industry Vertical

**Problem:** A Python developer at a fintech, a hospital, and a gaming studio are in different labor markets with different compensation norms. The survey has no way to see this.

| ID | Question | Type | Options |
|---|---|---|---|
| `industry` | ¿En qué industria opera tu empresa? | Single | Tecnología/Software / Finanzas/Fintech / Salud / E-commerce/Retail / Educación / Manufactura / Gobierno / Consultoría / Telecomunicaciones / Entretenimiento/Medios / Otro |

#### 1.5.6 English: Add Behavioral Anchor

**Problem:** Self-assessed English proficiency (ILR 0–5) is notoriously inflated due to the Dunning-Kruger effect. People at level 2 routinely report level 3–4.

**Keep `english` (ILR 0–5) and add:**

| ID | Question | Type | Options |
|---|---|---|---|
| `english_use` | ¿Con qué frecuencia usas inglés en tu trabajo diario? | Single | Nunca / Ocasionalmente (documentación) / Regularmente (reuniones, emails) / La mayor parte del tiempo / Todo mi trabajo es en inglés |

**Why:** Employers pay for *usage*, not *knowledge*. `english_use` may be a better salary predictor than self-assessed level, and the discrepancy between the two fields flags unreliable self-assessments.

#### 1.5.7 `education`: Localize for LatAm

**Problem:** "Prepa" is Mexican, "pasante" is a specifically Mexican academic status, "posgrado" and "maestria" overlap. Colombian and Argentine respondents won't map these to their systems.

**Redesigned options:**

| ID | Question | Type | Options |
|---|---|---|---|
| `education` | ¿Cuál es tu nivel máximo de estudios completado? | Single | Secundaria o equivalente / Preparatoria-Bachillerato o equivalente / Técnico superior / Licenciatura (en curso) / Licenciatura (titulado) / Maestría / Doctorado |

**Why:** "O equivalente" provides cross-country compatibility. The in-progress vs. completed distinction (replaces "pasante") is explicit. Posgrado is merged into maestría/doctorado.

### 1.6 Tech Stack Redesign: Role-First Architecture

The current tech blocks are the longest part of the survey (~100+ binary checkboxes across languages, frameworks, databases, data science, data engineering, infrastructure, certifications, and activities) but produce the weakest analytical signal. This section replaces them entirely.

#### 1.6.1 The Problem with Checkbox Matrices

1. **Sparse data:** Most cells are NaN. Niche technologies (Elixir, Rust, COBOL) have <5% penetration, requiring huge N for detectable salary effects.
2. **No depth signal:** Checking "Python" means the same whether you wrote one script or you're a senior ML engineer. Binary Y/N destroys the most valuable information — proficiency.
3. **Massive multicollinearity:** React implies JavaScript. Kubernetes implies Docker. PyTorch implies Python. Individual coefficients in the causal model are unstable.
4. **Time-series breakage:** Options change every year (COBOL dropped, Julia added, mobile_* appeared in 2022). Trends are impossible to track.
5. **Low salary signal:** The 2020–2022 causal analysis proved roles explain more salary variance than specific technologies (Direction +$16,553 vs. Groovy +$13,854, an outlier). Most individual language effects were small and noisy. ~40% of the survey contributes <5% of explanatory power.
6. **Respondent fatigue:** Scrolling through 100+ checkboxes is where people abandon the survey or click randomly.

#### 1.6.2 Step 1: Replace Activities with Primary + Secondary Role

**Current:** `act_*` — 26 binary checkboxes. A respondent might check Backend Dev, Architecture, DevOps, and Data Engineering without indicating which defines their salary.

**Redesigned:**

| ID | Question | Type | Options |
|---|---|---|---|
| `primary_role` | ¿Cuál es tu rol o actividad principal? | Single | Backend Dev / Frontend Dev / Fullstack Dev / Mobile Dev / Data Science-ML / Data Engineering / DevOps-Infra-SRE / InfoSec / Architecture / PM / QA-Testing / UXD / Direction-Strategy / AI-ML Engineering / Support / Other |
| `secondary_role` | ¿Tienes un rol secundario? | Single | Same options + "No tengo rol secundario" |

**Why:** The causal model needs **one** role per person to estimate role effects cleanly. Multi-select forces overlapping dummy variables. 2 questions replace 26 checkboxes.

#### 1.6.3 Step 2: Replace Individual Tech Lists with Primary Stack

Instead of asking everyone about every technology, ask what they *primarily* use.

| ID | Question | Type | Options |
|---|---|---|---|
| `primary_language` | ¿Cuál es tu lenguaje de programación principal? | Single | JavaScript-TypeScript / Python / Java / C# / Go / Rust / PHP / Ruby / Kotlin / Swift / C-C++ / Scala / Elixir / Other |
| `primary_framework` | ¿Cuál es tu framework o plataforma principal? | Single | React / Angular / Vue / Next.js / Spring / Django-FastAPI / .NET / Rails / Flutter / Laravel / Node.js-Express / None / Other |
| `primary_database` | ¿Cuál es tu base de datos principal? | Single | PostgreSQL / MySQL / SQL Server / MongoDB / Redis / DynamoDB / Firebase / Oracle / Other |
| `primary_cloud` | ¿Cuál es tu plataforma de nube principal? | Single | AWS / Azure / GCP / On-premise / No uso nube / Other |

**Why:** Single-select gives clean, non-overlapping groups for salary comparison. "Python developers earn X" is a real statement; "people who checked Python among other things earn X" is confounded by what else they checked. 4 questions replace ~60 checkboxes (`lang_*` + `front_*` + `mobile_*` + `db_*` + partial `infra_*`).

#### 1.6.4 Step 3: Add Depth (What Checkboxes Miss)

| ID | Question | Type | Options |
|---|---|---|---|
| `primary_lang_years` | ¿Cuántos años llevas usando tu lenguaje principal? | Numeric | (years) |
| `tech_breadth` | ¿En cuántas de las siguientes áreas trabajas regularmente? (Backend, Frontend, Mobile, Data, Infra/DevOps, Security, AI/ML) | Numeric | 1–7 count |
| `stack_change` | ¿Has cambiado significativamente tu stack tecnológico en los últimos 2 años? | Single | Sí, completamente / Sí, parcialmente / No |

**Why:** `primary_lang_years` provides depth signal destroyed by binary checkboxes. `tech_breadth` explicitly captures the generalist-vs-specialist axis. `stack_change` measures technology mobility — do people who switch stacks earn more or less?

#### 1.6.5 Step 4: Slim Down Certifications

**Current:** `cert_*` — 27 certification checkboxes. Most have <10% penetration.

**Redesigned:**

| ID | Question | Type | Options |
|---|---|---|---|
| `has_certs` | ¿Tienes alguna certificación técnica vigente? | Single | Sí / No |
| `cert_category` | ¿En qué categoría(s)? (selecciona las que apliquen, máx 3) | Multi-select | Cloud (AWS/Azure/GCP) / Agile-PM (Scrum/PMP) / Security (CISSP/CEH) / Kubernetes-DevOps / Data (Databricks/Snowflake) / Other |
| `cert_count` | ¿Cuántas certificaciones tienes? | Numeric | (count) |

**Why:** Categories are stable across years (unlike specific cert names). `cert_count` tests whether more certs = more salary or it plateaus. 3 questions replace 27 checkboxes.

#### 1.6.6 Step 5: Optional Granular Tech Detail

If Software Guru still wants the specific technology data for descriptive reports ("Top 10 languages in Mexico"), add an optional free-response at the end:

| ID | Question | Type | Options |
|---|---|---|---|
| `all_technologies` | (Opcional) Enlista todas las tecnologías que usas regularmente | Free text / tag input | Open |

This gives granular data for descriptive sections without burdening the analytical core. Parse post-hoc with text matching.

#### 1.6.7 Impact Summary

| Metric | Current | Redesigned |
|---|---|---|
| Tech-related items | ~100+ checkboxes | 13 structured questions + 1 optional |
| Response time (tech section) | 8–12 min | 2–3 min |
| Analytical signal per question | Low (sparse binary) | High (single primary + depth) |
| Year-over-year comparability | Breaks frequently | Stable (categories, not products) |
| Multicollinearity in causal model | Severe | Minimal (single-select groups) |

**What you lose (and why it's acceptable):**
- **Technology popularity rankings** ("React is used by 34%") → replaced by "React is the primary framework for 22% and is associated with $X salary." The second is more valuable. The optional `all_technologies` field recovers the first.
- **Niche technology effects** ("Elixir premium = +$11,838") → that estimate was based on ~100 respondents and was noisy. Primary stack approach gives cleaner estimates for technologies with sufficient sample.

---

## Goal 2: Policy-Driving Artifact

### 2.1 Rationale

The current survey produces excellent descriptive and causal findings (experience premium, English premium, gender gap, city effects), but they are framed as *insights for individual career decisions* ("learn English to earn more"). To drive policy, findings must be reframed as *structural conditions that institutions can change*.

**Primary audience: AMITI (Asociación Mexicana de la Industria de Tecnologías de Información).** Software Guru does not have a direct channel to STPS, SAT, SEP, or CONEVAL. AMITI does. The survey's policy value is therefore realized *through AMITI* — the findings must be packaged as advocacy ammunition that AMITI can carry to policymakers, not as neutral academic observations.

This means every finding needs to answer AMITI's question: **"What can we propose, and to whom?"**

| Individual framing (current) | AMITI advocacy framing (proposed) | AMITI action |
|----|-----|-----|
| "Learn English to earn 12K more" | "English proficiency explains 15% of salary variance — the national English-education pipeline is a bottleneck for sector growth" | Propose to SEP: industry-aligned English certification for CS programs |
| "Move to Hermosillo for higher pay" | "Tier-2 cities offer 30% lower nominal salary with higher purchasing power — ideal nearshoring destinations" | Pitch to foreign investors via AMITI's trade missions |
| "Women earn 12K less" | "The addressable talent pool is constrained to ~50% of its potential by a 95% male composition" | Propose to members: fund pipeline programs as a talent supply strategy |

The redesign adds question blocks that generate findings *only institutions can act on*, framed as pre-drafted advocacy positions for AMITI to carry forward. Each block concludes with specific AMITI-actionable recommendations organized by target institution:

- **"We propose to [government body] that..."** — AMITI lobbying federal agencies (STPS, SAT, SEP)
- **"We recommend to our members that..."** — AMITI setting internal industry standards
- **"We present to investors that..."** — AMITI promoting Mexico/LatAm as a tech destination

### 2.2 New Block: Labor Formality & Social Protection

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `formal_contract` | ¿Tienes un contrato laboral formal por escrito? | Single | Sí / No / No sé |
| `social_security` | ¿Estás inscrito en el IMSS, ISSSTE u otro sistema de seguridad social a través de tu empleo? | Single | Sí, por mi empleo / Sí, por cuenta propia / No |
| `retirement_saving` | ¿Realizas aportaciones a una Afore o fondo de retiro? | Single | Sí, mi empleador aporta / Sí, solo por mi cuenta / No |

**AMITI advocacy rationale:**

Mexico's labor informality rate is approximately 55% nationally, but *nobody has measured it specifically in the tech sector*. Anecdotal evidence suggests a significant fraction of tech workers — especially juniors, freelancers, and those in outsourcing arrangements — work on honorarios (fee-for-service contracts) without IMSS registration or retirement contributions.

The critical reframe: **informality is not a compliance problem — it is a competitiveness problem.** International clients (especially US and EU enterprises evaluating nearshoring partners) increasingly require vendors to demonstrate labor compliance. A tech sector with high informality rates is a sector that loses nearshoring contracts. This makes formalization an *industry growth* argument, not a regulatory burden argument — which is exactly how AMITI should position it.

**AMITI-actionable recommendations:**
- **Propose to STPS:** A simplified digital-sector formalization pathway — a lightweight nómina regime designed for remote workers and micro-employers in tech. The data will quantify how many workers would be covered and the estimated IMSS/Infonavit contribution increase.
- **Recommend to AMITI members:** Self-certification that all tech workers are formally employed. Position this as a competitive differentiator: "AMITI-member companies guarantee formal employment." Link to BP2C certification as the verification mechanism.
- **Present to investors:** "X% of the Mexican tech workforce is formally employed with full social protection" — a data point that supports nearshoring investment decisions.

**Analytical plan:**
- Cross-tabulate `emptype` × `social_security` to quantify the informality rate by employment type
- Model `formal_contract` as a function of `orgtype`, `city`, and `seniority` to identify where informality concentrates (if it's concentrated in outsourcing/itservices, AMITI can target those subsectors)
- Compute the *informality premium/penalty*: if informal workers earn *more* (compensating differential), the argument is "workers choose informality because formal employment is uncompetitive — simplify the regime." If they earn *less* (exploitation), the argument is "informality depresses wages and undermines the sector's attractiveness."

**Connection to existing data:** These three questions enrich the existing `emptype` field. A respondent who says `emptype=honorarios` and `social_security=No` is in a qualitatively different situation from one who says `emptype=honorarios` and `social_security=Sí, por cuenta propia`.

### 2.3 New Block: Cross-Border Work Dynamics

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `employer_hq` | ¿En qué país tiene su sede principal la empresa para la que trabajas? | Single | México / Estados Unidos / Canadá / Europa / América Latina (otro) / Asia / Otro |
| `payment_currency` | ¿En qué moneda recibes tu compensación principal? | Single | MXN / USD / EUR / Otra |
| `cross_border_contract` | ¿Cuál es tu relación laboral con esta empresa extranjera? | Single | Contrato laboral local (a través de entidad mexicana) / Contractor independiente / A través de Employer of Record (Deel, Remote, etc.) / Otro |
| `cross_border_tax` | ¿Emites facturas (CFDI) a una empresa extranjera como persona física con actividad empresarial? | Single | Sí / No / No aplica |

**AMITI advocacy rationale:**

The 2020 pandemic opened the Mexican IT labor market to US remote work. The causal analysis found a +$12,213 MXN/month remote premium, but it could not distinguish remote-for-Mexican-employer from remote-for-US-employer. These are fundamentally different market positions — and AMITI's domestic members are losing talent to both.

The core problem for AMITI members: **foreign employers recruit Mexican talent at 2–3× domestic salaries with zero obligation to the Mexican ecosystem** — no IMSS, no Infonavit, no Afore, no local office, no tax presence. This is brain drain without emigration, and it's invisible in official statistics because the workers never leave the country. Quantifying this bleed gives AMITI concrete numbers to take to government.

**AMITI-actionable recommendations:**
- **Propose to SAT:** A registered-foreign-employer framework requiring foreign companies that hire 5+ Mexican tech workers to register with SAT and contribute to social security (modeled on similar frameworks in Portugal and Estonia). The data will quantify the size of the unregistered foreign-employer workforce.
- **Propose to STPS:** Clarify the regulatory status of Employer of Record (EoR) services (Deel, Remote, Oyster). Are EoR-hired workers formal employees? The data will show what fraction of cross-border workers use each arrangement, giving STPS a basis for regulation.
- **Propose to SE (Secretaría de Economía):** Tax incentives for domestic tech employers to narrow the salary gap with foreign employers. Frame as talent retention: "For every $X MXN in tax incentives, domestic employers retain Y developers who would otherwise exit the domestic market."
- **Present to investors:** "Mexico has N thousand developers already working for US companies remotely — the talent pool is proven, English-proficient, and US-timezone-aligned. A formal nearshoring operation captures this talent with better retention."

**Analytical plan:**
- Decompose the remote premium: `salary ~ remote + employer_hq + payment_currency + controls`. The remote premium may largely be a *cross-border premium* — AMITI can use this to argue the gap is structural, not a quality difference.
- Quantify the "Deel economy": what fraction of tech workers use EoR services? This is the number STPS needs.
- Map geographic patterns: which cities are most exposed to cross-border talent drain? AMITI can prioritize retention programs in those cities.
- Estimate the "social security gap": cross-border workers × average missing employer contribution = total annual IMSS/Infonavit revenue not being collected.

**Connection to existing data:** This block explains a significant chunk of the unexplained variance from the 2020–2022 model. The remote dummy variable was a blunt instrument; these questions decompose it into meaningful structural categories.

### 2.4 New Block: Purchasing Power & Cost of Living

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `purchasing_power` | ¿Cómo calificarías tu capacidad para cubrir tus necesidades básicas con tu salario actual? | Likert 1–5 | 1=Con mucha dificultad ... 5=Con mucha holgura |
| `housing_burden` | ¿Qué porcentaje aproximado de tu ingreso mensual destinas a renta o hipoteca? | Single | 0% (vivienda propia sin hipoteca) / 1–20% / 21–30% / 31–40% / 41–50% / Más del 50% |
| `financial_savings` | ¿Logras ahorrar al menos el 10% de tu ingreso mensual? | Single | Sí, regularmente / A veces / Rara vez o nunca |

**AMITI advocacy rationale:**

The existing analysis found dramatic city effects (Hermosillo +$18,632 vs. León -$13,427 relative to CDMX), but nominal salary tells only half the story. A developer earning $35K MXN in Mérida may have higher *real purchasing power* than one earning $50K MXN in CDMX after housing costs.

For AMITI, this block is primarily a **nearshoring pitch tool and talent distribution strategy**. AMITI can tell foreign investors: "City X offers senior developers at 30% lower nominal cost than CDMX, with *higher* developer satisfaction and purchasing power. Here's the index." This reframes a cost-of-living analysis as an investment attraction artifact.

**AMITI-actionable recommendations:**
- **Present to investors (via AMITI trade missions):** A city-by-city "Tech Talent Value Index" combining nominal salary, purchasing power, and talent density. This becomes a standard slide in every AMITI nearshoring pitch deck.
- **Recommend to AMITI members:** Companies expanding domestically should consider the purchasing-power-adjusted ranking, not the nominal salary ranking, when choosing office locations. A Mérida or Aguascalientes office may attract equivalent talent at lower nominal cost with higher employee financial wellbeing.
- **Present to state governments:** "Your city ranks #X in purchasing-power-adjusted tech compensation. Here's what would move you up: housing programs, transit infrastructure, coworking spaces." This gives state-level economic development offices actionable data tied to AMITI member investment decisions.

No one in Latin America publishes a **tech-sector-specific real wages index**. The combination of salary + city + subjective purchasing power + housing burden allows Software Guru to construct one — and AMITI becomes the entity that distributes it to investors and state governments.

**Analytical plan:**
- Construct a city-level purchasing power index: mean `purchasing_power` score by city, weighted by salary band
- Compare nominal salary rankings vs. purchasing-power-adjusted rankings — highlight cities where the order flips (these are the "hidden value" cities AMITI pitches to investors)
- Model `financial_savings` as a function of salary, city, housing burden, and family status to identify where the tech middle class is financially fragile (these are the cities where retention risk is highest — AMITI can warn members)

### 2.5 New Block: Education ROI & Career Pathways

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `edu_relevance` | ¿Qué tan relevante fue tu educación formal para tu trabajo actual? | Likert 1–5 | 1=Nada relevante ... 5=Totalmente relevante |
| `recent_training` | ¿Has completado alguna capacitación o curso en los últimos 12 meses? | Single | Sí, pagado por mi empleador / Sí, pagado por mí / Sí, gratuito / No |
| `first_job_degree` | ¿Tu primer empleo en tecnología requirió un título universitario? | Single | Sí, era requisito formal / No, pero lo tenía / No, y no lo tenía |
| `edu_debt` | ¿Tienes deuda educativa actualmente (crédito educativo, préstamo para estudios)? | Single | Sí / No / Prefiero no contestar |

**AMITI advocacy rationale:**

AMITI already runs education partnership programs with ANUIES (the national university association). The existing `education` and `edutype` variables show that *how* you learned matters alongside *how much* you studied. But the survey currently cannot answer the question AMITI's education committee needs: **which educational pathways produce the most competitive talent, and how should industry invest in them?**

- **Is a CS degree worth it?** The `edu_relevance` + `first_job_degree` combination directly measures this. If 60% of senior developers say their formal education was "poco relevante" and their first job didn't require a degree, AMITI can take that finding to ANUIES and say: "Curricula need to be redesigned with industry input — here's the data."
- **Who is reskilling, and who pays?** The `recent_training` question distinguishes employer-funded from self-funded from free training. If most reskilling is self-funded, AMITI can argue for a tax deduction for employer-provided training (similar to the existing STPS training incentive but expanded for tech-specific certifications).
- **Is education debt a barrier to pipeline growth?** `edu_debt` is a proxy for financial accessibility. If bootcamp graduates carry less debt and earn comparably to CS degree holders, AMITI can promote bootcamp partnerships as a faster, cheaper path to expanding the talent pool.

**AMITI-actionable recommendations:**
- **Propose to ANUIES (via AMITI education committee):** Curriculum reform priorities based on `edu_relevance` scores by topic area. "Graduates from programs with industry internship components reach $50K MXN median salary 2 years faster — here's the data for your accreditation criteria."
- **Propose to STPS:** Expand the existing training tax incentive to cover tech-specific certifications and AI reskilling. The `recent_training` data quantifies the gap between employer-funded and self-funded training, demonstrating the need.
- **Recommend to AMITI members:** Fund scholarship programs at bootcamps and alternative pathways, not only universities. If `edutype=bootcamp` graduates perform comparably at lower debt, the ROI is better for both employer and worker.

**Analytical plan:**
- Compute the "degree premium" with modern controls: `salary ~ education + edutype + edu_relevance + first_job_degree + experience + english_num + ...`
- If `edu_relevance` mediates the education→salary path, the degree premium is about signaling, not human capital — AMITI's argument to ANUIES changes accordingly (reform curricula vs. drop degree requirements).
- Segment by `edutype`: do self-taught developers earn less *because* they lack a degree, or *despite* high relevance of their self-education? This distinguishes credentialism from skill and tells AMITI whether to lobby against degree requirements in job postings.

### 2.6 New Block: AI Impact on the Individual

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `ai_tools_use` | ¿Utilizas herramientas de IA (Copilot, ChatGPT, etc.) como parte regular de tu trabajo? | Single | Sí, diariamente / Sí, semanalmente / Ocasionalmente / No |
| `ai_task_change` | ¿Han cambiado las tareas que realizas debido a herramientas de IA? | Single | Sí, hago tareas de mayor nivel / Sí, hago las mismas tareas más rápido / Sí, algunas tareas ya no las hago / No ha cambiado |
| `ai_skill_confidence` | ¿Qué tan confiado/a estás en que tus habilidades actuales seguirán siendo relevantes en 3 años? | Likert 1–5 | 1=Nada confiado ... 5=Totalmente confiado |
| `ai_salary_impact` | ¿Consideras que tu uso de herramientas de IA ha contribuido a mejorar tu compensación? | Single | Sí, directamente / Probablemente sí / No creo / Definitivamente no |

**Separation from BP2C (Goal 1 compliance):**

| Aspect | Salary Survey (these questions) | BP2C |
|--------|------|------|
| Subject | The individual's market position | The employer's organizational behavior |
| What it measures | "Am I at risk? Am I gaining?" | "Is my employer equipping me?" |
| Lever | None (market-level) | AI Enablement (6 Qs), Techno-Anxiety (3 Qs) |

**AMITI advocacy rationale:**

The AI impact on tech labor markets is the policy question of the decade, but most data comes from US/European surveys (Stack Overflow, Dice, etc.). There is almost no structured data on AI adoption patterns among Latin American developers. For AMITI, this block produces the **first-ever AI adoption benchmark for the Mexican tech workforce** — a data point that positions AMITI as the authoritative voice on AI workforce policy in Mexico.

The key reframe: AI adoption is not a threat to be managed — it is a **competitive advantage to be accelerated**. AMITI's members who invest in AI training retain talent and increase productivity. The data should prove this, creating a business case for AI investment that AMITI can take to both its members and to government.

- **Employer investment ROI:** If the data shows that developers whose employers provide AI training (detectable via `recent_training` cross-tabulated with `ai_tools_use`) have higher `ai_skill_confidence` and lower `job_search` intent, AMITI can argue: "Companies investing in AI training retain developers X% longer. A tax credit for AI reskilling programs benefits the entire sector."
- **Adoption velocity as a competitiveness metric:** Cross-tabulate `ai_tools_use` by `orgtype`, `city`, and `employer_hq` to map where AI adoption is fastest and slowest. AMITI can present this to SE: "Mexico's AI adoption rate among developers is X% vs. Y% in Brazil/India — here's what's needed to close the gap."
- **Productivity gains and capture:** `ai_salary_impact` measures whether productivity gains from AI translate into worker compensation or are captured entirely by employers. If gains are not shared, AMITI can proactively recommend profit-sharing norms before regulation is imposed externally.

**AMITI-actionable recommendations:**
- **Propose to STPS/SE:** A tax deduction for AI reskilling programs (modeled on the existing STPS training incentive, expanded for AI-specific content). The data quantifies the training gap and the retention ROI.
- **Recommend to AMITI members:** Benchmark their AI adoption rate against the survey median. Companies below the median are falling behind — AMITI can offer a "readiness assessment" as a member service.
- **Present to international partners:** "Mexico's developer workforce has X% daily AI tool usage — higher than [comparison]. The workforce is AI-ready for nearshoring operations." This is an investment attraction data point.

### 2.7 New Block: Gender & Diversity Pipeline

**Questions:**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `first_code_age` | ¿A qué edad escribiste tu primera línea de código o programa? | Numeric | (years) |
| `childhood_computer` | ¿Tenías acceso a una computadora en casa durante tu infancia (antes de los 15 años)? | Single | Sí, propia / Sí, compartida / No |
| `discrimination_exp` | ¿Has experimentado discriminación en procesos de contratación o promoción en el sector tecnológico? | Single | Sí, frecuentemente / Sí, alguna vez / No / Prefiero no contestar |
| `identity_visibility` | ¿Te sientes cómodo/a siendo visible con tu identidad (género, orientación, etnia) en tu lugar de trabajo? | Likert 1–5 | 1=Nada cómodo ... 5=Totalmente cómodo |

**AMITI advocacy rationale:**

The 2020–2022 analysis found a -$12,442 adjusted gender gap, but with only 291 women (5% of respondents), the finding is noisy and, more importantly, *unexplained*. The gap persists after controlling for experience, education, and role, which means it's either discrimination or pipeline effects (or both). Without pipeline data, you cannot distinguish them.

For AMITI, the framing is **talent supply constraint**, not social justice (though the two are aligned). The Mexican tech sector's addressable talent pool is artificially constrained to roughly half its potential size by a ~95% male composition. Every woman who doesn't enter tech is a developer AMITI's members can't hire. The diagnostic matters because the *intervention* AMITI should lobby for depends on the cause:

- **If pipeline:** Women enter tech later, with less childhood exposure, and accumulate experience more slowly. AMITI action → fund and promote early STEM access programs as a *talent supply investment*, not CSR. Lobby SEP for computing equipment in public schools with measurable targets for girl participation.
- **If discrimination:** Women with identical qualifications are paid less. AMITI action → promote pay transparency norms among members (voluntarily, before regulation forces it). Link to BP2C certification: companies that pass pay-equity audits get a BP2C badge.

The `first_code_age` × `gender` interaction is the key diagnostic. If women systematically start coding 5+ years later than men, the experience gap (and its salary penalty) is a *pipeline* problem that begins in childhood, not a labor market problem.

`childhood_computer` tests the access hypothesis: is the pipeline problem about opportunity or interest? If women without childhood computer access are underrepresented even compared to men without access, the barrier is something other than equipment.

**AMITI-actionable recommendations:**
- **Propose to SEP:** "Only X% of female respondents had access to a computer before age 15, vs. Y% of males. Computing equipment access is a pipeline bottleneck — fund a tech-for-girls equipment program." The data makes the case quantitative.
- **Recommend to AMITI members:** Companies funding coding-for-girls programs (Laboratoria, Hackbright-style initiatives) should quantify the ROI as talent pipeline expansion, not CSR spending. The survey data provides the baseline: for every 100 women who enter the pipeline, AMITI members gain access to X additional mid-level developers within 5 years.
- **Present to investors:** "Companies with above-median gender diversity (measurable via BP2C) have X% lower attrition and Y% broader candidate pools" — an ESG-aligned investment data point.

**Note on sample size:** With 5% female representation, statistical power for subgroup analyses is limited. The survey redesign should include targeted distribution channels (Women Who Code Mexico, Laboratoria alumnae networks, etc.) to boost female response rates to at least 15–20%.

### 2.8 Geographic Expansion to Latin America

**Current scope:** Mexico (with incidental responses from 26 countries in 2020, mostly noise).

**Proposed scope:** Mexico + Colombia + Argentina + Brazil as primary targets, with LatAm-wide collection as secondary.

**Implementation:**

| Change | Detail |
|--------|--------|
| Language | Add Portuguese version for Brazil |
| Currency | Normalize all salaries to USD-PPP for cross-country comparison; collect in local currency |
| Social security questions | Localize: IMSS (MX), EPS/AFP (CO), ANSES/OSDE (AR), INSS (BR) |
| City options | Expand to include Bogotá, Medellín, Buenos Aires, Córdoba, São Paulo, Belo Horizonte, etc. |
| Distribution | Partner with local tech communities (Colombia: BogotáJS, Argentina: Meetup.js, Brazil: DevParaná, etc.) |

**AMITI advocacy rationale:**

There is no comparable cross-country tech labor market survey in Latin America. The closest equivalents are:
- Stack Overflow Developer Survey (global, minimal LatAm-specific analysis)
- Glassdoor/Levels.fyi (US-centric, self-selected, no policy framing)
- OECD employment data (not tech-specific)

For AMITI, geographic expansion transforms the survey from a **national report** into a **regional benchmark** — and AMITI becomes the steward of that benchmark. This has three strategic implications:

1. **Competitive positioning:** AMITI can show where Mexico stands relative to Colombia, Argentina, and Brazil on every metric (formality, compensation, AI adoption, gender diversity). Where Mexico leads, it's a selling point for investors. Where Mexico lags, it's a lobbying argument for government support.
2. **Pan-LatAm alliance building:** Cross-country data creates natural partnerships with equivalent associations (FEDESOFT in Colombia, CESSI in Argentina, Brasscom in Brazil). AMITI becomes the convener of a LatAm-wide tech labor intelligence network.
3. **International visibility:** A LatAm-scope report gets cited by IDB (Inter-American Development Bank), World Bank, and OECD — elevating AMITI's profile beyond Mexico.

**AMITI-actionable recommendations:**
- **Present to IDB/World Bank:** "Here is the first cross-country comparison of tech labor markets in Latin America. Mexico's formality rate is X% vs. Colombia's Y% — these are the structural barriers." International development organizations fund exactly this kind of comparative work.
- **Propose to SE (via AMITI):** "Mexico's tech workforce is Z% more productive-per-dollar than Brazil's — here's the nearshoring competitiveness argument, city by city."
- **Build alliances with FEDESOFT, CESSI, Brasscom:** Co-branded regional reports multiply distribution and credibility. Each national association carries the findings to their own government.

**Risks:**
- Sample size dilution: if total N stays at ~5,000, splitting across 4 countries yields ~1,250 per country, limiting subgroup analyses. Target 3,000+ per country.
- Localization cost: Portuguese translation, currency normalization, social security question localization all require investment.
- Loss of time-series comparability: adding countries in 2026 breaks the 2020–2022 Mexico-only time series. Mitigation: maintain Mexico as a continuous cohort within the expanded survey.

### 2.9 Deliverable: The AMITI Advocacy Brief

Beyond the public report, the analysis should produce a **separate 4–6 page AMITI Brief** — not published publicly, delivered directly to AMITI leadership — that packages the top findings as pre-drafted advocacy positions. This is the deliverable that makes AMITI a repeat partner for the survey.

**Structure of the AMITI Brief:**

| Section | Content | Target institution |
|---------|---------|-------------------|
| 1. Executive summary | Top 5 findings with headline numbers | AMITI board |
| 2. Formalization proposal | Informality rate + simplified regime proposal | STPS |
| 3. Cross-border regulation | EoR prevalence + foreign employer registration proposal | SAT, STPS |
| 4. Talent investment pitch | Purchasing power index + city-by-city talent profiles | Foreign investors (via AMITI trade missions) |
| 5. Education pipeline | Degree ROI data + curriculum reform priorities | ANUIES (via AMITI education committee) |
| 6. AI readiness benchmark | Adoption rates + training tax credit proposal | SE, STPS |

Each section follows a standard format:
1. **The finding** (1 paragraph + 1 chart)
2. **Why it matters for the sector** (1 paragraph)
3. **Proposed action** (bullet points: who, what, expected impact)
4. **Supporting data exhibit** (table or figure from the survey)

**Why a separate brief matters:** The public report must be journalistic and community-serving — it cannot read as an industry lobby document. The AMITI Brief can be explicitly advocacy-oriented because it is a private deliverable intended for a specific audience with specific institutional interests. This separation protects the survey's credibility while maximizing its policy utility.

**Software Guru's value to AMITI:** Software Guru becomes AMITI's *data partner* — the organization that provides the empirical foundation for AMITI's advocacy positions. This is a durable relationship that justifies AMITI co-sponsoring the survey, distributing it through member companies, and potentially funding the LatAm geographic expansion.

---

## Goal 3: BP2C Commercial Hook

### 3.1 Rationale

The Salary Survey is a free community asset with high reach. BP2C is a paid certification with limited reach (26–51 companies, declining participation). The strategic objective is to use the Salary Survey's audience to create demand for BP2C, without:

- Turning the Salary Survey into an advertisement (kills credibility)
- Duplicating BP2C's content in the Salary Survey (cannibalizes the paid product)
- Making the Salary Survey feel incomplete without BP2C (frustrates respondents)

The solution is to design the Salary Survey so that its *findings naturally point to questions only BP2C can answer*.

### 3.2 The Satisfaction Gap Teaser

**Questions (add to Salary Survey — maximum 3):**

| ID | Question | Type | Options |
|----|----------|------|---------|
| `enps` | Del 0 al 10, ¿qué tan probable es que recomiendes a tu empleador a un amigo? | NPS scale | 0–10 |
| `leave_reason` | ¿Cuál sería la razón principal por la que dejarías tu empleo actual? | Single | Salario / Crecimiento profesional / Cultura organizacional / Liderazgo / Flexibilidad / Otro |
| `job_search` | ¿Estás buscando activamente otro empleo? | Single | Sí / No, pero estoy abierto/a / No |

**Why only these three:**

These are *outcome variables*, not *diagnostic instruments*. They measure the *result* of employer quality without diagnosing *why*. BP2C's Six Levers are the diagnostic. This asymmetry is the commercial engine:

- The Salary Survey can publish: *"43% of tech professionals earning above $60K MXN still report an eNPS below 6. High salary alone does not predict employer satisfaction."*
- It **cannot** explain why, because it doesn't have the Six Lever measurements.
- The published report then notes: *"The BP2C certification framework measures the six independent dimensions of employer attractiveness that explain these satisfaction patterns. Companies interested in understanding their position can enroll at [link]."*

**Anonymity consideration:** eNPS is sensitive. Respondents may fear employer identification. The Salary Survey should **never** link eNPS to identifiable employers in public reports. This is both ethical and strategic: it makes BP2C (where employer identification is consensual) the only legitimate source of employer-level scores.

### 3.3 The Aggregated Cross-Survey Signal

If respondents can be linked across surveys (even loosely, by employer cluster), powerful narratives emerge:

| Published finding | Source | Drives demand for |
|---|---|---|
| "Employees at BP2C-certified companies earn 18% above market median" | Salary Survey × BP2C | Companies want the certification |
| "BP2C-certified companies have eNPS of 7.2 vs. 5.1 for non-certified" | Salary Survey (eNPS) × BP2C list | Companies want the score lift |
| "Certified employers report 40% lower voluntary attrition intent" | Salary Survey (`job_search`) × BP2C list | HR leaders want the retention data |

**Implementation:**

Linking requires knowing which company a respondent works for. The Salary Survey has historically **not** collected employer name (for anonymity). Options:

1. **Opt-in employer tagging:** "If you'd like your response to be included in employer-level benchmarking, enter your company name (optional)." This preserves anonymity as default.
2. **Domain-based clustering:** If collecting email addresses, cluster by email domain. This is implicit and less transparent — not recommended.
3. **BP2C participant matching:** Ask "Is your employer enrolled in BP2C?" (Y/N/Don't know). This is the lightest touch — it doesn't reveal the employer but enables the certified/non-certified comparison.

**Recommendation:** Option 3 (BP2C enrollment awareness) as the minimum viable implementation. Option 1 (opt-in employer tagging) as the aspirational target if response rates support it.

### 3.4 The "Missing Levers" Narrative

The causal model explains 38.74% of salary variance with 42 predictors. In the published report, explicitly frame the unexplained 61.26% as a feature, not a bug:

> *"Our model captures demographic, geographic, technical, and structural factors that explain 39% of salary variation. The remaining 61% reflects individual negotiation, employer-specific culture, career development opportunities, and organizational enablement — dimensions that the Best Place to Code certification is designed to measure."*

This narrative positions the two products as two halves of a complete picture:
- **Salary Survey:** What the market pays (structural, external)
- **BP2C:** Why people stay or leave (cultural, internal)

Neither is complete alone. Both are necessary for a full understanding of the tech labor market.

### 3.5 Report Structure for the Hook

In the annual published report, include a dedicated section (not more than 2 pages) titled something like:

> **"Más allá del salario: lo que el dinero no explica"**
> (Beyond salary: what money doesn't explain)

This section presents:
1. The eNPS distribution across salary bands (showing that high salary ≠ high satisfaction)
2. The top `leave_reason` responses (showing that salary is rarely #1)
3. The 61% unexplained variance finding
4. A non-promotional description of the BP2C framework as the complement

This section must be **journalistic, not commercial**. If it reads like an ad, it destroys the survey's credibility. The hook works precisely because the Salary Survey is a trusted, free community resource. That trust is the commercial asset.

---

## Implementation Roadmap

### Phase 1: Instrument Design (pre-launch)

- [ ] Finalize question wordings for all new blocks (Sections 2.2–2.7)
- [ ] User-test the instrument with 10–15 IT professionals for clarity and completion time
- [ ] Decide on geographic scope (Mexico-only vs. LatAm expansion)
- [ ] Design the sampling and distribution strategy (community partnerships, social media, employer channels)
- [ ] Implement the opt-in employer tagging mechanism (Section 3.3)
- [ ] Build the survey platform with proper skip logic (e.g., `cross_border_contract` only appears if `employer_hq` ≠ México)

### Phase 2: Data Collection

- [ ] Target sample size: 3,000+ per country (if LatAm expansion) or 5,000+ (if Mexico-only)
- [ ] Distribution window: 4–6 weeks
- [ ] Targeted outreach to underrepresented groups (women, non-binary, non-CDMX cities)
- [ ] BP2C participant notification: encourage employees of BP2C-enrolled companies to take the Salary Survey

### Phase 3: Analysis & Publication

- [ ] Reproduce the 2020–2022 causal model on new data for continuity
- [ ] Add new blocks to the causal framework (cross-border decomposition, formality premium, AI adoption effects)
- [ ] Construct the purchasing power index by city
- [ ] Compute the education ROI metrics
- [ ] Build the cross-survey link (Salary Survey × BP2C)
- [ ] Write the policy-oriented report with the "Beyond Salary" section
- [ ] Publish findings in both English and Spanish

### Phase 4: Feedback Loop

- [ ] Track BP2C enrollment inquiries that cite the Salary Survey report
- [ ] Measure respondent overlap between surveys
- [ ] Assess new question block completion rates — drop any with >30% non-response
- [ ] Plan 2027 iteration based on findings

---

## Question Inventory Summary

### Retained from Current Survey (with modifications)

| # | Field | Change |
|---|-------|--------|
| 1 | `age` | No change |
| 2 | `gender` | No change |
| 3 | `country` | Expand options for LatAm |
| 4 | `city` | Expand options for LatAm |
| 5 | `education` | Localized for LatAm; "o equivalente" added; pasante/posgrado replaced (Sec 1.5.7) |
| 6 | `edutype` | No change |
| 7 | `orgtype` | Add `ai_native`, rename `isv` → `product_company` |
| 8 | `emptype` | No change (enriched by formality block) |
| 9 | `work_arrangement` | Replaces `remote` (Y/N) and `covid_remoto`. 4 options. (Sec 1.3.1) |
| 10 | `english` | No change (ILR 0–5) |
| 11 | `vacaciones` | No change |
| 12 | `aguinaldo` | No change; localize for LatAm |

### Redesigned Existing Questions (Section 1.5)

| # | New Field | Replaces | Change |
|---|-----------|----------|--------|
| 13 | `base_salary` | `salarymx` | Unambiguous base salary; local currency only (Sec 1.5.1) |
| 14 | `total_cash_annual` | `salarymx` + `extramx` + `aguinaldo` + bonuses | Full annual compensation (Sec 1.5.1) |
| 15 | `has_equity` | (new) | Identifies equity compensation tier (Sec 1.5.1) |
| 16 | `salary_change` | `variation` | Categorical bands replace ambiguous % (Sec 1.5.1) |
| 17 | `salary_change_reason` | (new) | Decomposes growth cause — market vs. mobility (Sec 1.5.1) |
| 18 | `experience_tech` | `experience` | Explicit tech-sector years (Sec 1.5.2) |
| 19 | `experience_total` | (new) | Total career years; delta = career-switcher signal (Sec 1.5.2) |
| 20 | `tenure_current` | `seniority` | Company tenure replaces role tenure (Sec 1.5.2) |
| 21 | `seniority_level` | `profile` | Jr/Mid/Sr/Staff/Lead/Director/C-Level (Sec 1.5.3) |
| 22 | `company_size` | (new) | Top-5 salary predictor, previously missing (Sec 1.5.4) |
| 23 | `industry` | (new) | Labor market segmentation by vertical (Sec 1.5.5) |
| 24 | `english_use` | (new) | Behavioral anchor for English self-assessment (Sec 1.5.6) |

### Tech Stack Redesign (Section 1.6)

| # | New Field | Replaces | Change |
|---|-----------|----------|--------|
| 25 | `primary_role` | `act_*` (26 checkboxes) | Single primary role (Sec 1.6.2) |
| 26 | `secondary_role` | `act_*` (26 checkboxes) | Optional secondary role (Sec 1.6.2) |
| 27 | `primary_language` | `lang_*` (20 checkboxes) | Single primary language (Sec 1.6.3) |
| 28 | `primary_framework` | `front_*` + `mobile_*` | Single primary framework/platform (Sec 1.6.3) |
| 29 | `primary_database` | `db_*` (~15 checkboxes) | Single primary database (Sec 1.6.3) |
| 30 | `primary_cloud` | `infra_*` (partial) | Single primary cloud platform (Sec 1.6.3) |
| 31 | `primary_lang_years` | (new) | Depth signal for primary language (Sec 1.6.4) |
| 32 | `tech_breadth` | (new) | Generalist vs. specialist axis (Sec 1.6.4) |
| 33 | `stack_change` | (new) | Technology mobility in last 2 years (Sec 1.6.4) |
| 34 | `has_certs` | `cert_*` (27 checkboxes) | Binary: any cert? (Sec 1.6.5) |
| 35 | `cert_category` | `cert_*` (27 checkboxes) | Category-level multi-select, max 3 (Sec 1.6.5) |
| 36 | `cert_count` | (new) | Number of certifications (Sec 1.6.5) |
| 37 | `all_technologies` | `dsc_*` + `dataeng_*` + remaining | Optional free-text for granular data (Sec 1.6.6) |

### New Policy & Hook Questions (Sections 2.2–2.7, 3.2)

| Block | # Qs | IDs |
|-------|-------|-----|
| Labor formality (2.2) | 3 | `formal_contract`, `social_security`, `retirement_saving` |
| Cross-border dynamics (2.3) | 4 | `employer_hq`, `payment_currency`, `cross_border_contract`, `cross_border_tax` |
| Purchasing power (2.4) | 3 | `purchasing_power`, `housing_burden`, `financial_savings` |
| Education ROI (2.5) | 4 | `edu_relevance`, `recent_training`, `first_job_degree`, `edu_debt` |
| AI impact (2.6) | 4 | `ai_tools_use`, `ai_task_change`, `ai_skill_confidence`, `ai_salary_impact` |
| Gender & diversity pipeline (2.7) | 4 | `first_code_age`, `childhood_computer`, `discrimination_exp`, `identity_visibility` |
| BP2C hook (3.2) | 3 | `enps`, `leave_reason`, `job_search` |

### Removed Questions

| Block | Items removed |
|-------|-------------|
| Benefits (`ben_*`) | 18 items |
| COVID-era (`covid_*`) | 5 items |
| `salarymx`, `salaryusd`, `extramx`, `extrausd` | 4 items (replaced by `base_salary` + `total_cash_annual`) |
| `variation` | 1 item (replaced by `salary_change` + `salary_change_reason`) |
| `experience` | 1 item (replaced by `experience_tech` + `experience_total`) |
| `seniority` | 1 item (replaced by `tenure_current`) |
| `profile` | 1 item (replaced by `seniority_level`) |
| `lang_*` (20), `front_*`, `mobile_*`, `db_*`, `infra_*`, `dsc_*`, `dataeng_*` | ~80 checkboxes (replaced by primary stack, Sec 1.6) |
| `cert_*` (27) | 27 checkboxes (replaced by `has_certs` + `cert_category` + `cert_count`) |
| `act_*` (26) | 26 checkboxes (replaced by `primary_role` + `secondary_role`) |
| `remote`, `covid_remoto` | 2 items (replaced by `work_arrangement`) |

### Net Change

**Total final question count: 62 items**
- 12 retained (unchanged or minor option updates)
- 12 redesigned from existing fields (Sec 1.5)
- 13 tech stack redesign (Sec 1.6)
- 25 new policy & hook questions (Secs 2.2–2.7, 3.2)
- **~165 items removed** (checkboxes, COVID, benefits, redundant compensation fields)

The redesigned survey replaces a ~130-item instrument dominated by sparse checkboxes with 62 focused questions — each producing high analytical signal per response — while adding entirely new policy-relevant blocks. Estimated completion time drops from 25–35 minutes to 12–15 minutes.
