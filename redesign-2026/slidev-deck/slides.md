---
theme: default
title: "Rediseño Encuesta de Salarios 2026"
info: Presentación para Product Owners — Software Guru, Equipo de Datos
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
---

# Rediseño de la Encuesta de Salarios 2026

**Presentación para Product Owners**

Software Guru — Equipo de Datos · Marzo 2026

<div class="abs-br m-6 text-sm opacity-50">
Branch: redesign-2026
</div>

---
transition: fade-out
---

# ¿Por qué rediseñar ahora?

<v-clicks>

- BP2C acaba de completar su rediseño (45 preguntas, Marco de 6 Palancas)
- Las dos encuestas **se traslapan**: beneficios, trabajo remoto, tipo de organización — misma perspectiva
- Los encuestados que contestan ambas: *"¿No ya contesté esto?"*
- El diseño de ~130 checkboxes produce **rendimientos analíticos decrecientes**
- **Ventana de oportunidad**: alinear ambos productos ahora

</v-clicks>

---

# Tres Objetivos

| # | Objetivo | En una línea |
|---|----------|--------------|
| 1 | **Separación de producto** | Cero duplicación estructural con BP2C |
| 2 | **Impacto en política pública** | Hallazgos que AMITI pueda llevar a tomadores de decisiones |
| 3 | **Gancho para BP2C** | Generar demanda por la certificación |

<br>

<v-click>

> **Encuesta de Salarios** = Radiografía del **MERCADO** *(oferta, estructura, precios)*
>
> **BP2C** = Radiografía del **EMPLEADOR** *(cultura, habilitación, justicia)*

</v-click>

---
layout: two-cols
layoutClass: gap-8
---

# Lo que quitamos

| Bloque | Ítems |
|--------|:-----:|
| Beneficios (`ben_*`) | 18 |
| COVID (`covid_*`) | 5 |
| Checkboxes de tech | ~133 |
| Compensación redundante | 5 |
| Remoto/perfil viejo | 4 |
| **Total** | **~165** |

::right::

# ¿Por qué?

<v-clicks>

- **Beneficios** → atributos del empleador, ahora en BP2C
- **COVID** → 6 años obsoleto
- **Checkboxes de tech** → 40% del tiempo, <5% de señal
- **Comp. redundante** → reemplazado por campos más claros
- **Perfil/remoto** → rediseñados, no eliminados

</v-clicks>

---

# Lo que agregamos

<v-clicks>

**12 campos rediseñados**
- Desambiguación de compensación (base vs. total)
- Nivel de seniority (Jr → C-Level)
- Tamaño de empresa, vertical de industria
- Ancla conductual de inglés

**13 campos de stack tecnológico**
- Arquitectura rol-primero que reemplaza ~100 checkboxes

**25 preguntas nuevas de política pública**
- 6 bloques para advocacy de AMITI + 3 gancho BP2C

</v-clicks>

<v-click>

<div class="mt-4 p-3 bg-blue-600 text-white rounded-lg text-center text-lg font-bold">
62 ítems totales (antes eran ~130)
</div>

</v-click>

---

# La brecha más grande: `seniority_level`

La encuesta anterior tenía `profile`: godín / independiente / emprendedor / directivo

<v-clicks>

**Problemas:**
- Mezcla tipo de empleo con nivel organizacional
- "Godín" es slang mexicano — no funciona para expansión a LatAm
- No hay forma de distinguir a un Junior de un Senior

**Nuevo campo:** Jr / Mid / Sr / Staff / Lead / Director+ / C-Level

</v-clicks>

<v-click>

<div class="mt-6 p-4 bg-amber-600 text-white rounded-lg text-center">
<div class="text-3xl font-bold">+12.4 puntos porcentuales de R²</div>
<div class="text-sm mt-1">con este solo campo — más que todas las preguntas de tecnología juntas</div>
</div>

</v-click>

---
layout: two-cols
layoutClass: gap-8
---

# Stack Tech: Diseño Anterior

- 20 checkboxes de lenguajes ☐
- 8+ checkboxes de frameworks ☐
- 15 checkboxes de bases de datos ☐
- 27 checkboxes de certificaciones ☐
- 26 checkboxes de actividades ☐

<br>

**~100 ítems binarios**

⏱️ 8–12 min para completar

::right::

# Stack Tech: Diseño Nuevo

- 1 rol principal
- 1 lenguaje principal
- 1 framework principal
- 1 base de datos principal
- 1 nube principal
- campos de profundidad (años, amplitud)
- 3 preguntas de certs (tiene/categoría/cuántas)

**13 ítems estructurados**

⏱️ 2–3 min para completar

---

# Por qué selección única le gana a checkboxes

<v-clicks>

| Problema | Checkbox | Selección única |
|----------|----------|-----------------|
| **Dispersión** | 91.6% ceros | Grupos limpios |
| **Confusión** | React ∩ JS ∩ Frontend | Una categoría por persona |
| **Profundidad** | "Sabe Python" = ? | Años con lenguaje principal |
| **Estabilidad** | Coeficientes inestables | 87% más estables |
| **Serie de tiempo** | Opciones cambian cada año | Categorías son estables |

</v-clicks>

<v-click>

<br>

> *"Los desarrolladores de Python ganan $X"* es una afirmación real.
>
> *"La gente que marcó Python entre otras cosas gana $X"* está confundida.

</v-click>

---

# Nuevos Bloques de Política Pública (para AMITI)

| Bloque | Qs | Habilita |
|--------|:--:|----------|
| 🏛️ Formalidad Laboral | 3 | Primera tasa de informalidad en sector tech |
| 🌎 Cross-Border | 4 | Cuantificar "economía Deel" + fuga de talento |
| 💰 Poder Adquisitivo | 3 | Índice de salarios reales ciudad por ciudad |
| 🎓 ROI Educativo | 4 | Prima de título con controles modernos |
| 🤖 Impacto de IA | 4 | Primer benchmark de adopción IA en LatAm |
| ⚖️ Pipeline de Género | 4 | Diagnóstico: pipeline vs. discriminación |

<v-click>

<div class="mt-4 text-center text-sm">
Cada bloque → posición de advocacy pre-redactada para que AMITI lleve a STPS, SAT, SEP, ANUIES
</div>

</v-click>

---

# Gancho BP2C: La Brecha de Satisfacción

Tres preguntas **solo de resultado** agregadas:

<v-clicks>

- **eNPS** (0–10): "¿Qué tan probable es que recomiendes a tu empleador?"
- **leave_reason**: "¿Cuál sería la razón principal por la que te irías?"
- **job_search**: "¿Estás buscando trabajo activamente?"

</v-clicks>

<v-click>

<div class="mt-6 p-4 bg-gray-600 text-white rounded-lg">
<div class="text-lg italic">
"43% de los profesionales tech que ganan >$60K MXN reportan eNPS menor a 6.<br>
Un salario alto por sí solo no predice satisfacción."
</div>
</div>

</v-click>

<v-click>

<div class="mt-4 text-center">

**Encuesta de Salarios muestra el *qué*** → **BP2C explica el *por qué***

</div>

</v-click>

---

# Simulación: Resultados Principales

Monte Carlo · n=6,000 · Calibrado con tamaños de efecto reales 2020–2022

| Métrica | Anterior | Nuevo | Cambio |
|---------|--------:|------:|-------:|
| Ítems de encuesta | 130 | 62 | **−52%** |
| Tiempo de llenado | 30 min | 14 min | **−53%** |
| Predictores del modelo | 90 | 72 | −20% |
| Respuestas utilizables | 5,066 | 5,695 | +629 |
| **R²** | **0.340** | **0.490** | **+44%** |
| R² ajustada | 0.328 | 0.483 | +47% |

---

# Eficiencia de Información

| Métrica | Anterior | Nuevo | Mejora |
|---------|--------:|------:|:------:|
| R² por ítem | 0.003 | 0.008 | **+202%** |
| R² por minuto | 0.011 | 0.035 | **+208%** |
| Info efectiva (R² × N) | 1,724 | 2,788 | **+62%** |
| Estabilidad de coef. (CV) | 5.17 | 0.69 | **−87%** |

<v-click>

<div class="mt-6 p-4 bg-green-600 text-white rounded-lg text-center">
<div class="text-2xl font-bold">
Cada minuto del encuestado entrega 3× más señal analítica
</div>
</div>

</v-click>

---

# ¿De dónde viene la R²?

Partiendo de la línea base equivalente al diseño anterior (R² = 0.268):

| Bloque agregado | ΔR² | Notas |
|-----------------|-----:|-------|
| **seniority_level** | **+12.4 pp** | **> todas las Qs de tech juntas** |
| company_size | +2.4 pp | Ausente en encuesta anterior |
| english_use | +1.8 pp | 1 pregunta, alta señal |
| primary_role | +1.7 pp | Reemplaza 26 checkboxes |
| industry | +1.5 pp | Ausente en encuesta anterior |
| primary_language | +1.1 pp | Reemplaza 20 checkboxes |
| cert_depth | +0.9 pp | Reemplaza 27 checkboxes |
| Otros | +0.5 pp | experience_total, tenure, tech_depth |

---
layout: two-cols
layoutClass: gap-8
---

# Encuestado: Antes (25–35 min)

1. Demográficos *(2 min)*
2. Profesionales *(3 min)*
3. Compensación *(2 min)*
4. **100+ checkboxes** *(8–12 min)*
   <br>← 🔴 zona de fatiga
5. Beneficios *(3 min)*
6. COVID *(2 min)*

<br>

**85% de completitud** (estimado)

::right::

# Encuestado: Nuevo (12–15 min)

1. Demográficos *(2 min)*
2. Profesional + seniority *(3 min)*
3. Compensación *(2 min)*
4. **13 Qs de tech** *(2–3 min)*
5. Bloques de política *(4–5 min)*
6. Gancho BP2C *(1 min)*

<br>

**95% de completitud** (estimado)

<div class="mt-2 text-sm text-green-400 font-bold">
+629 respuestas utilizables más
</div>

---

# Hoja de Ruta de Implementación

| Fase | Qué | Cuándo |
|:----:|-----|--------|
| **1** | Finalizar redacción · Prueba con 10–15 profesionales TI | Pre-lanzamiento |
| **2** | Recolección de datos · Meta: 5,000+ MX | 4–6 semanas |
| **3** | Reproducir modelo 2020–2022 + bloques nuevos | Post-recolección |
| **4** | Reporte público + Brief privado AMITI | — |

<v-click>

<div class="mt-6 p-3 bg-yellow-600 text-white rounded-lg">

**Decisión pendiente:** Alcance geográfico — ¿solo México o expandir a Colombia, Argentina, Brasil?

</div>

</v-click>

---

# Decisiones que Necesitamos de los Product Owners

<v-clicks>

1. **Alcance geográfico** — ¿Solo México o expansión a LatAm?
2. **Etiquetado de empresas** — ¿nombre de empresa opt-in para cruce entre encuestas?
3. **Canales de distribución** — ¿qué alianzas con comunidades?
4. **Brief AMITI** — ¿aprueban el concepto de entregable privado?
5. **Naming** — ¿"Encuesta de Salarios" o rebrand? *(Radiografía del Talento Tech)*

</v-clicks>

---
layout: center
class: text-center
---

# Resumen

<div class="grid grid-cols-3 gap-6 mt-8 text-left">
<div class="p-4 bg-blue-600 text-white rounded-lg">
<div class="text-2xl font-bold">−52%</div>
<div class="text-sm">menos preguntas</div>
</div>
<div class="p-4 bg-green-600 text-white rounded-lg">
<div class="text-2xl font-bold">+44%</div>
<div class="text-sm">más poder explicativo</div>
</div>
<div class="p-4 bg-amber-600 text-white rounded-lg">
<div class="text-2xl font-bold">3×</div>
<div class="text-sm">info por minuto</div>
</div>
<div class="p-4 bg-purple-600 text-white rounded-lg">
<div class="text-2xl font-bold">+12.4pp</div>
<div class="text-sm">solo de seniority_level</div>
</div>
<div class="p-4 bg-red-600 text-white rounded-lg">
<div class="text-2xl font-bold">25</div>
<div class="text-sm">preguntas de política nueva</div>
</div>
<div class="p-4 bg-teal-600 text-white rounded-lg">
<div class="text-2xl font-bold">14 min</div>
<div class="text-sm">tiempo de llenado</div>
</div>
</div>

<div class="mt-8 text-lg">
Siguiente paso: revisar <code>question_inventory_2026.csv</code> y agendar pruebas con usuarios
</div>

---
layout: center
class: text-center
---

# Recursos

<div class="text-left inline-block">

| Archivo | Propósito |
|---------|-----------|
| `REDESIGN_2026.md` | Justificación completa (3 objetivos) |
| `question_inventory_2026.csv` | 62 ítems bilingüe |
| `SIMULATION_FINDINGS.md` | Análisis detallado de simulación |
| `simulation_old_vs_new.py` | Script de simulación reproducible |
| `simulation_results/` | CSVs de resultados crudos |

</div>

<div class="mt-6 text-sm opacity-60">
Todo en el branch <code>redesign-2026</code>
</div>
