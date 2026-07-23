---
theme: default
title: "SG Tech Pulse 2026 — Brecha de género"
info: Hallazgos preliminares de brecha de género · Software Guru
class: text-center
transition: slide-left
mdc: true
---

# La brecha de género en el tech mexicano

**SG Tech Pulse 2026 · hallazgos preliminares**

<div class="mt-8 text-2xl italic text-rose-600 font-semibold">
"El tech mexicano les paga igual a las mujeres… hasta que valen más."
</div>

<div class="abs-br m-6 text-sm opacity-50">
Muestra autoseleccionada · n=192 (56 mujeres) · cifras direccionales
</div>

---
layout: center
class: text-center
---

# No es un problema de pipeline

<div class="text-2xl mt-4 mb-8">Es un techo que se enciende en la cima.</div>

<div class="grid grid-cols-2 gap-6 max-w-3xl mx-auto text-left">
<div class="p-4 bg-gray-100 rounded-lg"><div class="text-4xl font-bold">−32%</div><div class="text-sm">brecha cruda de salario base (mediana)</div></div>
<div class="p-4 bg-rose-100 rounded-lg"><div class="text-4xl font-bold text-rose-700">−37%</div><div class="text-sm">castigo en niveles senior y de liderazgo</div></div>
<div class="p-4 bg-rose-100 rounded-lg"><div class="text-4xl font-bold text-rose-700">50%</div><div class="text-sm">de la brecha no la explica nada del trabajo</div></div>
<div class="p-4 bg-gray-100 rounded-lg"><div class="text-4xl font-bold">62% → 27%</div><div class="text-sm">mujeres, de nivel medio a senior+</div></div>
</div>

---

# Hallazgo 1 — El peaje: iguales abajo, castigadas arriba

<div class="flex justify-center">
<img src="./figures/fig1_toll.png" class="h-96 rounded-lg shadow" />
</div>

<div class="text-center mt-2 text-lg">
En junior y medio las mujeres van igual o arriba. El castigo del <b class="text-rose-600">37%</b> aparece justo al ascender.
</div>

---

# Hallazgo 1 — La brecha se ensancha con el nivel

<div class="flex justify-center">
<img src="./figures/fig2_scissors.png" class="h-96 rounded-lg shadow" />
</div>

<div class="text-center mt-2 text-lg">
Medio <b>−2%</b> → Senior <b class="text-rose-600">−29%</b> → Gerente <b class="text-rose-600">−38%</b>. Entre más alto, más cuesta.
</div>

---

# Hallazgo 2 — La desaparición

<div class="flex justify-center">
<img src="./figures/fig3_vanishing.png" class="h-96 rounded-lg shadow" />
</div>

<div class="text-center mt-2 text-lg">
Mayoría en el nivel medio (<b>62%</b>), y apenas <b>~1 de cada 4</b> en senior o más. El conteo se colapsa justo donde aparece el castigo.
</div>

---
layout: center
---

# Hallazgo 3 — Los pesos sin explicación

<div class="flex justify-center">
<img src="./figures/fig4_oaxaca.png" class="w-full max-w-4xl rounded-lg shadow" />
</div>

---

# Hallazgo 4 — La salida solo para ellos

<div class="flex justify-center">
<img src="./figures/fig5_exit.png" class="h-96 rounded-lg shadow" />
</div>

<div class="text-center mt-2 text-lg">
El mayor aumento del mercado (trabajar para el extranjero) casi no llega a ellas.
<span class="text-sm opacity-70">(direccional, n=11 mujeres)</span>
</div>

---
layout: center
class: text-center
---

# Qué significa

<div class="text-xl mt-4 max-w-3xl mx-auto text-left space-y-3">

- **No es pipeline, es un techo de promoción y pago.** Las mujeres llegan con fuerza al nivel medio y ahí se les paga justo; el sector las pierde y subpaga a las que se quedan, justo en senior y liderazgo.
- **Peticiones:** auditorías de equidad salarial en niveles senior/liderazgo; programas formales de mujeres hacia el liderazgo (68% reporta que no hay ninguno); acceso temprano a STEM para niñas.

</div>

<div class="mt-8 text-2xl italic text-rose-600 font-semibold">
"El tech mexicano les paga igual a las mujeres… hasta que valen más."
</div>

---
layout: center
class: text-sm
---

# Nota metodológica

Salario base normalizado a MXN (USD × TC 18.5, robusto entre 17–20); log para regresión; outliers ~$8k–$400k recortados. Brecha cruda con IC bootstrap; brecha ajustada por MCO; descomposición Oaxaca-Blinder (controles: experiencia, seniority, inglés, familia de rol). Celdas con <5 mujeres suprimidas; personas no binarias (n=2) excluidas de la inferencia.

**Lo no explicado no equivale a discriminación probada:** también contiene factores no medidos, incluidos los ítems de mecanismo (negociación, patrocinio, promoción) eliminados del formulario desplegado. Muestra autoseleccionada y preliminar; el hallazgo 4 es direccional (n=11 mujeres).

Detalle completo: `docs/GENDER_FINDINGS_2026.md` / `_ES_MX.md`.
