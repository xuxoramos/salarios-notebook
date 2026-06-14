# BP2C 2026 — AI Roles & Role-Transition Additions (proposal)

> **Status:** Proposal for the BP2C repo. This file is self-contained so it can be
> moved out of the Salary Survey repo and into BP2C without external references.
>
> **Scope:** Sharpen the existing **AI Enablement** lever of the redesigned 45-question
> BP2C instrument so it captures (a) whether the employer has created or converted
> **formal AI roles**, and (b) whether it is **enabling the people actually doing the
> AI work**. Mirrors the Salary Survey's individual-lens AI block so the two surveys
> join cleanly.

## 1. Why now

Since BP2C and the Salary Survey were last applied, the AI boom created new roles and
quietly transformed traditional software roles into AI roles. The current BP2C AI
Enablement lever asks whether the employer provides AI tools and permission, but not
whether the employer has **staffed**, **converted**, or **reskilled** people into AI
roles. That is the gap this proposal closes.

The unit-of-analysis rule is unchanged: the **Salary Survey** asks the individual about
their *market position*; **BP2C** asks the individual about their *employer's behavior*.
Same topic, different lens. These additions stay strictly on the employer-behavior side.

## 2. Grounding (live 2025 industry data)

- **WEF, Future of Jobs Report 2025** (1,000+ employers, 14M workers, 55 economies):
  AI and machine-learning specialists are among the fastest-growing roles in
  percentage terms; AI and big data are the **No. 1 fastest-rising skill set** through
  2030; employers expect **39% of core skills to change** by 2030.
- **McKinsey, The State of AI** (Nov 2025, 1,993 respondents, 105 countries):
  **88%** of organizations now use AI in at least one function (up from 78%); **62%**
  are experimenting with or scaling AI agents; AI-related hiring concentrates in
  **existing software- and data-engineering roles** rather than exotic new titles
  (most AI roles are converted, not created); **redesigning workflows** around AI is a
  top differentiator of high performers.
- **Gartner** frameworks used for the role taxonomy: **AI Engineering** (ML/AI,
  GenAI/LLM, MLOps/AI Platform) and **AI TRiSM** (Responsible AI / governance).

Implication for BP2C: the employer behaviors worth certifying are **role creation /
conversion**, **reskilling**, and **workflow redesign**, not just tool access.

## 3. Proposed BP2C items (AI Enablement lever)

All items are employer-behavior, single-select, and include "No sé" to avoid forcing a
guess. Field IDs are namespaced `bp2c_ai_*` to keep them distinct from Salary Survey
fields.

| ID | Question (ES) | Type | Options |
|----|---------------|------|---------|
| `bp2c_ai_roles_formal` | ¿Tu empleador ha creado roles formales de IA (ML/AI Engineer, GenAI/LLM, MLOps, AI PM, Responsible AI) en los últimos 2 años? | Single | Sí, contratando externamente / Sí, reconvirtiendo personal interno / Sí, ambos / No / No sé |
| `bp2c_ai_reskilling` | ¿Tu empleador ofrece programas de reskilling o capacitación para transicionar hacia roles o tareas de IA? | Single | Sí, formal y pagado por la empresa / Sí, informal / No / No sé |
| `bp2c_ai_workflow_redesign` | ¿Tu empleador ha rediseñado procesos o flujos de trabajo para incorporar IA (no solo dar herramientas)? | Single | Sí, de forma sistemática / Parcialmente / No / No sé |
| `bp2c_ai_enablement` | ¿Tu empleador te provee herramientas de IA aprobadas y permiso explícito para usarlas en tu trabajo? | Single | Sí, herramientas y permiso / Solo permiso, sin herramientas / Ni herramientas ni permiso / No sé |
| `bp2c_ai_role_support` | Si tu rol se transformó hacia IA, ¿tu empleador ajustó tu compensación, título o nivel para reflejarlo? | Single | Sí / No / No aplica (mi rol no se transformó) / No sé |

**Notes**
- `bp2c_ai_enablement` may already exist in the current AI Enablement lever. If so,
  keep the existing field and adopt only the other four. Do not duplicate.
- `bp2c_ai_roles_formal` is the keystone: its **"reconvirtiendo personal interno"** vs.
  **"contratando externamente"** split is the employer-side mirror of the Salary
  Survey's conversion-vs-hiring finding.
- `bp2c_ai_role_support` ties role transformation to recognition (pay/title/level),
  which is a certification-relevant fairness signal.

## 4. Cross-survey mapping (Salary Survey ↔ BP2C)

Each AI item has a counterpart on the other side, enabling a population-level join
(no PII; matched on `bp2c_enrolled` + employer attributes, exactly like the existing
certification-premium comparison).

| Phenomenon | Salary Survey (individual lens) | BP2C (employer lens) |
|---|---|---|
| AI tool usage | `ai_tools_use` — do I use AI tools, how often | `bp2c_ai_enablement` — does my employer provide tools + permission |
| Task change / workflow | `ai_task_change` — have my tasks changed due to AI | `bp2c_ai_workflow_redesign` — has my employer redesigned workflows around AI |
| Role identity / transition | `ai_role_status` — is my role net-new AI / transformed / unchanged | `bp2c_ai_roles_formal` — has my employer created/converted formal AI roles |
| AI specialization | `ai_specialization` — my AI specialization (gated) | `bp2c_ai_roles_formal` — which AI functions the employer has staffed |
| Skill confidence / reskilling | `ai_skill_confidence` — will my skills stay relevant | `bp2c_ai_reskilling` — does my employer fund AI reskilling |
| Recognition of transition | (covered by `salary_change` + `seniority_level`) | `bp2c_ai_role_support` — did pay/title/level follow the role change |

### Joint findings this enables

- **Enablement gap:** AI-role individuals (`ai_role_status` ≠ No, or high `ai_tools_use`)
  whose employers score low on `bp2c_ai_enablement` reveal **bottom-up, unsupported AI
  adoption** — the people doing the AI work are not being enabled by their employer.
- **Conversion vs. hiring (two-sided):** `ai_role_status` (individual) cross-checked
  against `bp2c_ai_roles_formal` (employer) shows whether the AI workforce is grown
  internally or bought, and whether employees and employers report it consistently.
- **Reskilling ROI:** employers strong on `bp2c_ai_reskilling` should show higher
  `ai_skill_confidence` and lower `job_search` intent in their workforce — the
  certification's evidence that AI investment retains talent.
- **Fairness of transformation:** `bp2c_ai_role_support` flags employers who transform
  roles toward AI without adjusting pay/title — a negative certification signal.

## 5. Lever-fit and scoring

These five items extend the **AI Enablement** lever. `bp2c_ai_role_support` and
`bp2c_ai_reskilling` also feed the **Techno-Anxiety Management** lever (they reduce the
fear of obsolescence). Suggested scoring: reward internal reskilling/conversion and
workflow redesign over tool access alone, consistent with the McKinsey finding that
workflow redesign — not tool rollout — distinguishes high performers.

## 6. Item budget

Net add of up to **5** items to the AI Enablement lever (4 if `bp2c_ai_enablement`
already exists). If BP2C must hold its ~45-item total, candidates to merge are any
generic "does your employer use modern technology" items now subsumed by the sharper
AI-specific set above.
