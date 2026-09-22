# Hallazgos Generales — SG Tech Pulse 2026 (Preliminar)

> 🔄 **Actualizado 2026-09-21** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 21 September 2026.csv`, 622 respuestas). Reemplaza las cifras de julio de 2026 (217 respuestas). **Los materiales de campaña derivados** (figuras de gender-slides, decks de Slidev, tarjetas HTML, `docs/ig_scripts/`) todavía tienen fijas las cifras anteriores y deben regenerarse desde esta versión.

**Fecha:** 2026-09-21
**Datos:** Volcado en vivo de SG Tech Pulse 2026 — 622 respuestas (90% reside en México). Muestra para análisis salarial: n=544.
**Estado:** Preliminar. Respondientes autoseleccionados; se presenta como muestra de respondientes, no como estimación poblacional.

**Mediana general de salario base: $65,000 MXN/mes.**

---

## Resumen ejecutivo

- **La experiencia y el seniority son las dos mayores palancas salariales**, seguidas del uso del inglés; el tamaño de empresa, la industria y el rol aportan menos. Juntas explican ~55% de la varianza salarial (R² ajustada).
- **El inglés es casi un factor de 2× en el salario**: quienes trabajan totalmente en inglés ganan ~$80k contra $35k de quienes nunca lo usan.
- **La prima transfronteriza es real**: el 14% que trabaja para un empleador extranjero gana ~35% más (mediana $85k vs $63k local).
- **La IA ya está reconfigurando cómo se escribe código**: entre quienes respondieron, **exactamente la mitad (94 de 188)** sobre todo instruye a agentes de IA y revisa, en lugar de programar a mano.
- **El sector es mayormente formal** (91% tiene seguridad social), y **el riesgo de rotación lo manda el salario** (la razón principal para irse es el sueldo, por amplio margen).

---

## 1. Qué determina el salario (B1)

R² ajustada incremental sobre log del salario base (bloques agregados en orden):

| Bloque agregado | R² ajustada | ΔR² |
|---|---|---|
| Experiencia (años en tech) | 0.17 | +0.17 |
| + Uso de inglés | 0.28 | +0.11 |
| + **Nivel de seniority** | 0.44 | **+0.16** |
| + Tamaño de empresa | 0.48 | +0.04 |
| + Industria | 0.52 | +0.04 |
| + Rol principal | 0.55 | +0.03 |

**La experiencia (+0.17) y el seniority (+0.16) son las dos mayores palancas**, con el inglés (+0.11) muy cerca; tamaño, industria y rol suman poco una vez que entra el seniority. Confirma la apuesta central del rediseño: una escalera de seniority limpia es de las preguntas de mayor valor del instrumento.

## 2. Estructura de compensación — primas por rol (B2)

Mediana de salario base mensual (MXN) por rol principal (roles con n≥6):

| Rol | Mediana | n |
|---|---|---|
| Seguridad / InfoSec | $111,000 | 12 |
| Arquitectura | $95,000 | 24 |
| Liderazgo ejecutivo | $95,000 | 44 |
| Product management | $86,950 | 23 |
| Engineering management | $85,000 | 12 |
| Ciencia de datos / IA | $76,220 | 31 |
| DevOps / SRE / Infra | $74,675 | 20 |
| Desarrollo de software (BE/FE/FS/Móvil) | $70,800 | 168 |
| Ingeniería de datos / ML | $65,000 | 33 |
| Project management | $55,250 | 26 |
| QA / Testing | $53,070 | 33 |
| Analista de software/datos | $50,000 | 27 |
| Diseño UX / UI | $35,000 | 18 |
| Soporte técnico | $24,000 | 10 |

Seguridad, arquitectura, liderazgo, producto y ciencia de datos arriba; analista, diseño y soporte abajo.

## 3. Transfronterizo / el mercado global (B3)

- El **14%** trabaja para un **empleador con sede en el extranjero**, y gana una **prima de ~35%** (mediana $85k vs $63k local).
- Esquema de contratación de los transfronterizos: representante local (32), contratista independiente (29), **intermediario / Employer-of-Record — Deel, Remote (14)**.
- 43 respondientes reportan pago en USD.

Es la "economía Deel" que anticipó el rediseño: cerca de un séptimo del mercado está enchufado a paga extranjera, con prima relevante y en buena medida fuera de la nómina local.

## 4. Prima del inglés (B4)

La mediana de salario base sube marcadamente con el *uso* del inglés:

| Uso de inglés en el trabajo | Mediana base | n |
|---|---|---|
| Nunca | $35,000 | 37 |
| Ocasionalmente (documentación) | $49,580 | 148 |
| Con regularidad (juntas, correo) | $75,000 | 85 |
| La mayoría del tiempo | $79,500 | 64 |
| Todo el tiempo | $80,000 | 155 |

Trabajar totalmente en inglés se asocia con **~2.3× el salario** de quien nunca lo usa, con el salto concentrado entre "ocasionalmente" y "con regularidad". El uso (no solo el nivel autoevaluado) es una señal salarial de primer orden.

## 5. Adopción de IA (B5)

- De los **188** que respondieron la pregunta de generación de código, **exactamente la mitad (94)** sobre todo *instruye a agentes de IA y revisa el resultado* en vez de programar a mano.
- **56 respondientes ya tienen un rol centrado en IA** — sobre todo GenAI/LLM/Agent Engineer (17), AI product manager (11), ML Engineer (7) y Prompt manager (6). Es un salto fuerte frente a julio (19) y ya es una categoría ocupacional real.
- La confianza en que las habilidades actuales sigan siendo relevantes en 3 años promedia **3.4 / 5** — y, notablemente, es **plana en todos los niveles de experiencia** (ver las historias para medios de género/IA).

## 6. Formalidad y protección social (B6)

- **9%** no tiene seguridad social — el sector tech es mucho más formal que la informalidad nacional (~55%).
- **21%** no aporta a ningún fondo de retiro.
- **12%** carga deuda educativa.

## 7. Resiliencia financiera (B7)

- **56%** califica su capacidad de cubrir necesidades básicas como cómoda (4–5 de 5).
- **La tasa de ahorro mediana es 10%** del ingreso mensual (media 18%): **69% ahorra al menos 10%**, ~12% ahorra más del 30%, y **15% no ahorra nada**.

## 8. Rutas de formación (B8)

- **58% aprendió en la escuela**, 15% en el trabajo, 9% vía cursos en línea, 11% no programa, y solo **6% por bootcamp** (1% principalmente por IA).
- La relevancia autoevaluada de la formación académica para el trabajo actual promedia **7.3 / 10**.

## 9. Retención y satisfacción (B9)

- **La calificación media de "recomendar a tu empleador" es 7.6 / 10** (n=481) — disposición amplia a recomendar.
- **La razón principal para irse es el salario** (227), luego desarrollo profesional (115), trabajo remoto (64) y cultura (30).
- **El vínculo con BP2C ya casi es analizable**: 95 respondientes reportan que su empleador está inscrito en Best Place to Code (208 No, 138 no sabe) — suficientes empleadores inscritos para empezar una comparación de prima de certificación en la próxima pasada.

## 10. Inclusión — discapacidad y neurodivergencia (B10)

- **~5%** reporta una discapacidad física (25 de 484 que responden).
- **~15%** reporta una neurodivergencia diagnosticada (75 de 484 que responden) — una proporción notable que merece un ángulo de inclusión propio.

---

## Metodología

- Salario base mensual normalizado a MXN (USD × TC 18.5; robusto entre TC 17–20); transformado a log para la regresión; se recortan valores atípicos fuera de ~$8k–$400k.
- El análisis de palancas usa R² ajustada incremental (ajustada por número de predictores, dado que el modelo completo tiene muchas dummies).
- Los descriptivos son medianas/proporciones sobre respuestas disponibles; se marcan subgrupos delgados.
- Tasas de ahorro normalizadas a una escala porcentual común (entradas decimales ×100); variantes de texto libre de ruta de aprendizaje consolidadas.
- Muestra autoseleccionada; sin ponderación poblacional.

## Advertencias de calidad de datos

- **43 reportes en USD** dependen de un único supuesto de tipo de cambio.
- Los valores de respuesta llegan en español canónico sin importar el idioma en que se contestó la encuesta.
- **Preliminar:** la encuesta sigue abierta; las cifras se moverán conforme se llene.
