# Hallazgos Generales — SG Tech Pulse 2026 (Preliminar)

> 🔄 **Actualizado 2026-11-19** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 19 November 2026.csv`, 787 respuestas). Reemplaza las cifras del 12-oct-2026 (publicadas como 688 respuestas).

**Fecha:** 2026-11-19
**Datos:** Volcado en vivo de SG Tech Pulse 2026 — 787 respuestas (90% reside en México). Muestra para análisis salarial: n=689.
**Estado:** Preliminar. Respondientes autoseleccionados; se presenta como muestra de respondientes, no como estimación poblacional.

**Mediana general de salario base: $60,000 MXN/mes.**

---

## Resumen ejecutivo

- **La experiencia es ahora la mayor palanca salarial por sí sola**, seguida del seniority y del uso del inglés. El tamaño de empresa, la industria y el rol aportan menos. En conjunto explican ~54% de la varianza salarial (R² ajustada).
- **El inglés es un factor de ~2.1× en el salario**: quienes trabajan totalmente en inglés ganan ~$80k contra ~$37k de quienes nunca lo usan.
- **La prima transfronteriza es real**: el 15% que trabaja para un empleador extranjero gana ~36% más (mediana ~$81k vs ~$60k con empleador no extranjero).
- **La IA ya está reconfigurando cómo se escribe código**: entre quienes respondieron, **aproximadamente la mitad (117 de 232)** sobre todo instruye a agentes de IA y revisa, en lugar de programar a mano.
- **El sector es mayormente formal** (88% de quienes respondieron tiene seguridad social), y **el riesgo de rotación lo manda el salario** (la razón principal para irse es el sueldo, por amplio margen).

---

## 1. Qué determina el salario (B1)

R² ajustada incremental sobre log del salario base (bloques agregados en orden):

| Bloque agregado | R² ajustada | ΔR² |
|---|---|---|
| Experiencia (años en tech) | 0.17 | **+0.17** |
| + Uso de inglés | 0.28 | +0.11 |
| + **Nivel de seniority** | 0.42 | +0.14 |
| + Tamaño de empresa | 0.46 | +0.03 |
| + Industria | 0.52 | +0.06 |
| + Rol principal | 0.54 | +0.03 |

**La experiencia (+0.17) es ahora la mayor palanca por sí sola**, seguida del seniority (+0.14) y del inglés (+0.11). La industria (+0.06) suma un poco más, y el tamaño de empresa (+0.03) y el rol (+0.03) suman poco una vez que entra el seniority. En octubre la experiencia y el seniority estaban empatados (+0.16 cada uno). Ahora el seniority aporta un poco menos cuando la experiencia y el inglés ya están en el modelo. Sigue siendo la segunda palanca, así que la apuesta central del rediseño se mantiene: una escalera de seniority limpia es de las preguntas de mayor valor del instrumento.

## 2. Estructura de compensación — primas por rol (B2)

Mediana de salario base mensual (MXN) por rol principal (roles con n≥6):

| Rol | Mediana | n |
|---|---|---|
| Seguridad / InfoSec | $92,000 | 15 |
| Liderazgo ejecutivo | $92,000 | 53 |
| Arquitectura | $90,000 | 29 |
| Engineering management | $79,000 | 15 |
| Ciencia de datos / IA | $76,610 | 36 |
| Desarrollo de software (BE/FE/FS/Móvil) | $70,000 | 198 |
| DevOps / SRE / Infra | $70,000 | 26 |
| Ingeniería de datos / IA / ML | $65,000 | 37 |
| Product management | $65,000 | 30 |
| Project management | $52,000 | 37 |
| QA / Testing | $51,500 | 38 |
| Analista de software/datos | $50,000 | 32 |
| Diseño UX / UI | $45,500 | 22 |
| Soporte técnico | $35,000 | 17 |

Seguridad y liderazgo ejecutivo empatan arriba ($92,000), con arquitectura ($90,000) y engineering management ($79,000) muy cerca. Analista, diseño y soporte quedan abajo, y soporte técnico es el más bajo ($35,000).

## 3. Transfronterizo / el mercado global (B3)

- El **15%** de quienes respondieron (n=743) trabaja para un **empleador con sede en el extranjero**, y gana una **prima de ~36%** (mediana $81,400, n=97, vs $60,000 con empleador no extranjero).
- Esquema de contratación de los transfronterizos: representante local (38), contratista independiente (38), **intermediario / Employer-of-Record — Deel, Remote (20)**.
- 53 respondientes reportan pago en USD.

Es la "economía Deel" que anticipó el rediseño: cerca de un séptimo del mercado está enchufado a paga extranjera, con prima relevante y en buena medida fuera de la nómina local.

## 4. Prima del inglés (B4)

La mediana de salario base sube marcadamente con el *uso* del inglés:

| Uso de inglés en el trabajo | Mediana base | n |
|---|---|---|
| Nunca | $37,300 | 50 |
| Ocasionalmente (documentación) | $45,000 | 215 |
| Con regularidad (juntas, correo) | $74,000 | 103 |
| La mayoría del tiempo | $78,000 | 78 |
| Todo el tiempo | $80,000 | 176 |

Trabajar totalmente en inglés se asocia con **~2.1× el salario** de quien nunca lo usa, con el salto concentrado entre "ocasionalmente" y "con regularidad". El uso (no solo el nivel autoevaluado) es una señal salarial de primer orden.

## 5. Adopción de IA (B5)

- De los **232** que respondieron la pregunta de generación de código, **aproximadamente la mitad (117)** sobre todo *instruye a agentes de IA y revisa el resultado* en vez de programar a mano.
- **73 respondientes ya tienen un rol centrado en IA** — sobre todo GenAI/LLM/Agent Engineer (21), AI product manager (16), Prompt manager (9) y ML Engineer (8). Es un salto fuerte frente a julio (19) y ya es una categoría ocupacional real.
- La confianza en que las habilidades actuales sigan siendo relevantes en 3 años promedia **3.3 / 5** — y, notablemente, es **plana en todos los niveles de experiencia** (entre 3.25 y 3.44 según el tramo de experiencia, ver las historias para medios de género/IA).

## 6. Formalidad y protección social (B6)

- **12%** no tiene seguridad social — el sector tech es mucho más formal que la informalidad nacional (~55%).
- **26%** (uno de cada cuatro) no aporta a ningún fondo de retiro.
- **15%** carga deuda educativa.

*Corrección metodológica:* la versión de octubre reportó 10% / 21% / 12%. Esas proporciones se calcularon sobre todas las filas, así que las no respuestas contaban como si no tuvieran la condición, y eso las subestimaba. Las tres ahora se calculan sobre quienes respondieron cada pregunta (n=651 para seguridad social, n=642 para fondo de retiro y deuda educativa).

## 7. Resiliencia financiera (B7)

- **66%** de quienes respondieron califica su capacidad de cubrir necesidades básicas como cómoda (4–5 de 5). *Corrección metodológica:* la versión de octubre reportó 55%, calculado sobre todas las filas (las no respuestas contaban como "no cómoda"). Con la regla de quienes respondieron, octubre habría dado 68%, así que la proporción de fondo se mantiene estable.
- **La tasa de ahorro mediana es 10%** del ingreso mensual (media 18%): **69% ahorra al menos 10%**, ~13% ahorra más del 30%, y **16% no ahorra nada**.

## 8. Rutas de formación (B8)

- Proporciones sobre quienes respondieron: **57% aprendió en la escuela**, 15% en el trabajo, 9% vía cursos en línea, 12% no programa, y solo **5% por bootcamp** (1% principalmente por IA).
- La relevancia autoevaluada de la formación académica para el trabajo actual promedia **7.2 / 10**.

## 9. Retención y satisfacción (B9)

- **La calificación media de "recomendar a tu empleador" es 7.6 / 10** (n=611) — disposición amplia a recomendar.
- **La razón principal para irse es el salario** (284), luego desarrollo profesional (152), trabajo remoto (78) y cultura (42).
- **El vínculo con BP2C ya casi es analizable**: 103 respondientes reportan que su empleador está inscrito en Best Place to Code (291 No, 179 no sabe) — suficientes empleadores inscritos para empezar una comparación de prima de certificación en la próxima pasada.

## 10. Inclusión — discapacidad y neurodivergencia (B10)

- **~6%** reporta una discapacidad física (36 de 617 que responden).
- **~15%** reporta una neurodivergencia diagnosticada (92 de 617 que responden) — una proporción notable que merece un ángulo de inclusión propio.

---

## Metodología

- Salario base mensual normalizado a MXN (USD × TC 18.5; robusto entre TC 17–20); transformado a log para la regresión; se recortan valores atípicos fuera de ~$8k–$400k.
- El análisis de palancas usa R² ajustada incremental (ajustada por número de predictores, dado que el modelo completo tiene muchas dummies).
- Los descriptivos son medianas/proporciones sobre respuestas disponibles; se marcan subgrupos delgados.
- Los porcentajes se calculan sobre quienes respondieron cada pregunta.
- Tasas de ahorro normalizadas a una escala porcentual común (entradas decimales ×100); variantes de texto libre de ruta de aprendizaje consolidadas.
- Muestra autoseleccionada; sin ponderación poblacional.

## Advertencias de calidad de datos

- **53 reportes en USD** dependen de un único supuesto de tipo de cambio.
- Los valores de respuesta llegan en español canónico sin importar el idioma en que se contestó la encuesta.
- **Preliminar:** la encuesta sigue abierta; las cifras se moverán conforme se llene.

---

## Cambios vs la versión de octubre 2026

- **Datos:** 787 respuestas (octubre se publicó como 688). Muestra para análisis salarial n=689 (antes 601).
- **Mediana general de salario base:** $64,000 → **$60,000 MXN/mes**.
- **B1, orden de palancas:** la experiencia y el seniority estaban empatados (+0.16 cada uno). Ahora la experiencia es la mayor palanca por sí sola (+0.17), por delante del seniority (+0.14) y del inglés (+0.11). R² ajustada acumulada 0.53 → 0.54.
- **B4, prima del inglés:** ~2.4× → **~2.1×** (todo el tiempo vs nunca: $85,000 vs $35,800 → $80,000 vs $37,300).
- **B3, prima por empleador extranjero:** +31% → **+36%** (mediana $81,400 vs $62,000 → $81,400 vs $60,000).
- **Regla de denominador (corrección metodológica, B6 y B7):** las proporciones ahora se calculan sobre quienes respondieron cada pregunta. Las de octubre se dividían entre todas las filas, lo que contaba las no respuestas como "no" y las subestimaba: sin seguridad social 10% → 12%, sin fondo de retiro 21% → 26%, deuda educativa 12% → 15%, cómodo para cubrir necesidades básicas 55% → 66%.
