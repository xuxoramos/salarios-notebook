# Hallazgos Generales — SG Tech Pulse 2026 (Preliminar)

> 🔄 **Actualizado 2026-10-12** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 12 October 2026.csv`, 688 respuestas). Reemplaza las cifras del 21-sep-2026 (622 respuestas). **Los materiales de campaña derivados** (figuras de gender-slides, decks de Slidev, tarjetas HTML, `docs/ig_scripts/`) todavía tienen fijas las cifras anteriores y deben regenerarse desde esta versión.

**Fecha:** 2026-10-12
**Datos:** Volcado en vivo de SG Tech Pulse 2026 — 688 respuestas (90% reside en México). Muestra para análisis salarial: n=601.
**Estado:** Preliminar. Respondientes autoseleccionados; se presenta como muestra de respondientes, no como estimación poblacional.

**Mediana general de salario base: $64,000 MXN/mes.**

---

## Resumen ejecutivo

- **La experiencia y el seniority son las dos mayores palancas salariales**, seguidas del uso del inglés; el tamaño de empresa, la industria y el rol aportan menos. Juntas explican ~53% de la varianza salarial (R² ajustada).
- **El inglés es un factor de ~2.4× en el salario**: quienes trabajan totalmente en inglés ganan ~$85k contra ~$36k de quienes nunca lo usan.
- **La prima transfronteriza es real**: el 15% que trabaja para un empleador extranjero gana ~31% más (mediana ~$81k vs ~$62k local).
- **La IA ya está reconfigurando cómo se escribe código**: entre quienes respondieron, **aproximadamente la mitad (104 de 210)** sobre todo instruye a agentes de IA y revisa, en lugar de programar a mano.
- **El sector es mayormente formal** (90% tiene seguridad social), y **el riesgo de rotación lo manda el salario** (la razón principal para irse es el sueldo, por amplio margen).

---

## 1. Qué determina el salario (B1)

R² ajustada incremental sobre log del salario base (bloques agregados en orden):

| Bloque agregado | R² ajustada | ΔR² |
|---|---|---|
| Experiencia (años en tech) | 0.16 | +0.16 |
| + Uso de inglés | 0.26 | +0.10 |
| + **Nivel de seniority** | 0.42 | **+0.16** |
| + Tamaño de empresa | 0.46 | +0.04 |
| + Industria | 0.50 | +0.04 |
| + Rol principal | 0.53 | +0.02 |

**La experiencia (+0.16) y el seniority (+0.16) son las dos mayores palancas — ahora empatadas**, con el inglés (+0.10) muy cerca; tamaño, industria y rol suman poco una vez que entra el seniority. Confirma la apuesta central del rediseño: una escalera de seniority limpia es de las preguntas de mayor valor del instrumento.

## 2. Estructura de compensación — primas por rol (B2)

Mediana de salario base mensual (MXN) por rol principal (roles con n≥6):

| Rol | Mediana | n |
|---|---|---|
| Seguridad / InfoSec | $111,000 | 12 |
| Arquitectura | $100,000 | 27 |
| Liderazgo ejecutivo | $95,000 | 47 |
| Engineering management | $85,000 | 12 |
| Desarrollo de software (BE/FE/FS/Móvil) | $73,400 | 186 |
| Ciencia de datos / IA | $72,610 | 32 |
| Product management | $72,500 | 28 |
| DevOps / SRE / Infra | $72,175 | 22 |
| Ingeniería de datos / ML | $66,000 | 34 |
| Project management | $55,500 | 29 |
| QA / Testing | $51,500 | 36 |
| Analista de software/datos | $50,000 | 29 |
| Diseño UX / UI | $44,000 | 21 |
| Soporte técnico | $30,000 | 11 |

Seguridad, arquitectura, liderazgo y engineering management arriba; analista, diseño y soporte abajo.

## 3. Transfronterizo / el mercado global (B3)

- El **15%** trabaja para un **empleador con sede en el extranjero**, y gana una **prima de ~31%** (mediana $81,400 vs $62,000 local).
- Esquema de contratación de los transfronterizos: representante local (36), contratista independiente (35), **intermediario / Employer-of-Record — Deel, Remote (19)**.
- 48 respondientes reportan pago en USD.

Es la "economía Deel" que anticipó el rediseño: cerca de un séptimo del mercado está enchufado a paga extranjera, con prima relevante y en buena medida fuera de la nómina local.

## 4. Prima del inglés (B4)

La mediana de salario base sube marcadamente con el *uso* del inglés:

| Uso de inglés en el trabajo | Mediana base | n |
|---|---|---|
| Nunca | $35,800 | 44 |
| Ocasionalmente (documentación) | $50,000 | 169 |
| Con regularidad (juntas, correo) | $74,000 | 91 |
| La mayoría del tiempo | $79,000 | 69 |
| Todo el tiempo | $85,000 | 166 |

Trabajar totalmente en inglés se asocia con **~2.4× el salario** de quien nunca lo usa, con el salto concentrado entre "ocasionalmente" y "con regularidad". El uso (no solo el nivel autoevaluado) es una señal salarial de primer orden.

## 5. Adopción de IA (B5)

- De los **210** que respondieron la pregunta de generación de código, **aproximadamente la mitad (104)** sobre todo *instruye a agentes de IA y revisa el resultado* en vez de programar a mano.
- **61 respondientes ya tienen un rol centrado en IA** — sobre todo GenAI/LLM/Agent Engineer (18), AI product manager (13), Prompt manager (7) y ML Engineer (7). Es un salto fuerte frente a julio (19) y ya es una categoría ocupacional real.
- La confianza en que las habilidades actuales sigan siendo relevantes en 3 años promedia **3.4 / 5** — y, notablemente, es **plana en todos los niveles de experiencia** (ver las historias para medios de género/IA).

## 6. Formalidad y protección social (B6)

- **10%** no tiene seguridad social — el sector tech es mucho más formal que la informalidad nacional (~55%).
- **21%** no aporta a ningún fondo de retiro.
- **12%** carga deuda educativa.

## 7. Resiliencia financiera (B7)

- **55%** califica su capacidad de cubrir necesidades básicas como cómoda (4–5 de 5).
- **La tasa de ahorro mediana es 10%** del ingreso mensual (media 18%): **70% ahorra al menos 10%**, ~12% ahorra más del 30%, y **16% no ahorra nada**.

## 8. Rutas de formación (B8)

- **58% aprendió en la escuela**, 15% en el trabajo, 9% vía cursos en línea, 11% no programa, y solo **6% por bootcamp** (1% principalmente por IA).
- La relevancia autoevaluada de la formación académica para el trabajo actual promedia **7.3 / 10**.

## 9. Retención y satisfacción (B9)

- **La calificación media de "recomendar a tu empleador" es 7.6 / 10** (n=481) — disposición amplia a recomendar.
- **La razón principal para irse es el salario** (249), luego desarrollo profesional (127), trabajo remoto (69) y cultura (35).
- **El vínculo con BP2C ya casi es analizable**: 97 respondientes reportan que su empleador está inscrito en Best Place to Code (243 No, 152 no sabe) — suficientes empleadores inscritos para empezar una comparación de prima de certificación en la próxima pasada.

## 10. Inclusión — discapacidad y neurodivergencia (B10)

- **~6%** reporta una discapacidad física (31 de 535 que responden).
- **~15%** reporta una neurodivergencia diagnosticada (78 de 535 que responden) — una proporción notable que merece un ángulo de inclusión propio.

---

## Metodología

- Salario base mensual normalizado a MXN (USD × TC 18.5; robusto entre TC 17–20); transformado a log para la regresión; se recortan valores atípicos fuera de ~$8k–$400k.
- El análisis de palancas usa R² ajustada incremental (ajustada por número de predictores, dado que el modelo completo tiene muchas dummies).
- Los descriptivos son medianas/proporciones sobre respuestas disponibles; se marcan subgrupos delgados.
- Tasas de ahorro normalizadas a una escala porcentual común (entradas decimales ×100); variantes de texto libre de ruta de aprendizaje consolidadas.
- Muestra autoseleccionada; sin ponderación poblacional.

## Advertencias de calidad de datos

- **48 reportes en USD** dependen de un único supuesto de tipo de cambio.
- Los valores de respuesta llegan en español canónico sin importar el idioma en que se contestó la encuesta.
- **Preliminar:** la encuesta sigue abierta; las cifras se moverán conforme se llene.
