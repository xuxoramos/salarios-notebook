# Hallazgos Generales — SG Tech Pulse 2026 (Preliminar)

**Fecha:** 2026-07-21
**Datos:** Volcado en vivo de SG Tech Pulse 2026 — 217 respuestas (165 completas). Muestra para análisis salarial: n=193.
**Estado:** Preliminar. Respondientes autoseleccionados; se presenta como muestra de respondientes, no como estimación poblacional.

**Mediana de salario base general: $75,000 MXN/mes.**

---

## Resumen ejecutivo

- **La seniority es, por mucho, la mayor palanca salarial**, seguida por el uso de inglés, la industria y el rol. En conjunto explican ~61% de la varianza salarial (R² ajustada).
- **El inglés es casi un factor de 2×**: quienes trabajan totalmente en inglés ganan ~$100k vs ~$48.5k de quienes nunca lo usan.
- **La prima transfronteriza es real**: el 18% que trabaja para un empleador extranjero gana ~49% más (mediana $104.5k vs $70k).
- **La IA ya está cambiando cómo se escribe el código**: entre quienes respondieron, cerca de la mitad más bien instruye a agentes de IA y revisa, en lugar de escribir el código a mano.
- **El sector es mayormente formal** (91% tiene seguridad social), y **el riesgo de rotación lo encabeza el salario** (la razón principal para irse es el sueldo).

---

## 1. Qué determina el salario (B1)

R² ajustada incremental sobre salario base logarítmico (bloques agregados en orden):

| Bloque agregado | R² ajustada | ΔR² |
|---|---|---|
| Experiencia (años tech) | 0.14 | +0.14 |
| + Uso de inglés | 0.28 | +0.16 |
| + **Nivel de seniority** | 0.49 | **+0.23** |
| + Tamaño de empresa | 0.50 | +0.03 |
| + Industria | 0.55 | +0.10 |
| + Rol principal | 0.61 | +0.09 |

**La seniority es la palanca individual más grande** (+0.23), más que el inglés, la industria y el rol. Esto confirma la apuesta central del rediseño: una escalera de seniority limpia es la pregunta de mayor valor del instrumento.

## 2. Estructura de compensación — primas por rol (B2)

Mediana de salario base mensual MXN por rol principal (roles con n≥6):

| Rol | Mediana | n |
|---|---|---|
| Engineering management | $120,000 | 7 |
| Arquitectura | $110,000 | 6 |
| Product management | $99,000 | 12 |
| Liderazgo ejecutivo | $95,000 | 27 |
| Ciencia de datos / IA | $94,150 | 18 |
| DevOps / SRE / Infra | $72,500 | 8 |
| Desarrollo de software (BE/FE/FS/Móvil) | $65,000 | 41 |
| Ingeniería de datos / ML | $65,000 | 13 |
| Analista de software/datos | $55,000 | 15 |
| Project management | $52,500 | 8 |

Los roles de gestión, arquitectura, producto y ciencia de datos están arriba; analista y project management, abajo.

## 3. Transfronterizo / el mercado global (B3)

- **18%** trabaja para un **empleador con sede en el extranjero**, y gana una **prima de ~49%** (mediana $104.5k vs $70k nacional).
- Estructura de vínculo entre quienes trabajan transfronterizo: contrato vía representante local (15), contratista independiente (14), **Employer-of-Record / tipo Deel (7)**, directo/otro (2).
- 16 respondientes reciben pago en USD.

Es la "economía Deel" que señaló el rediseño: una quinta parte del mercado está conectada a pago extranjero, con una prima grande, en gran medida fuera de las estructuras de nómina nacionales.

## 4. Prima del inglés (B4)

La mediana salarial sube de forma monótona con el *uso* del inglés:

| Uso de inglés en el trabajo | Mediana base |
|---|---|
| Nunca | $48,500 |
| Ocasionalmente (documentación) | $50,500 |
| Con regularidad (juntas, emails) | $86,000 |
| La mayoría del tiempo | $91,000 |
| Todo el tiempo | $100,000 |

Trabajar totalmente en inglés se asocia con **~2× el salario** de quien nunca lo usa. El uso (no solo el nivel autoevaluado) es una señal salarial de primer orden.

## 5. Adopción de IA (B5)

- De quienes respondieron la pregunta de generación de código, cerca de **la mitad (24 de ~49)** dice que *más bien instruye a agentes de IA y revisa la salida* en lugar de escribir el código a mano; otros ~14 programan manual con IA como soporte.
- **19 respondientes ya tienen un rol centrado en IA.**
- La confianza en que sus habilidades sigan siendo relevantes en 3 años promedia **3.4 / 5** (moderada, sin alarma).

## 6. Formalidad y protección social (B6)

- **9%** no tiene seguridad social — el sector tech es sustancialmente más formal que la informalidad nacional de ~55%.
- **20%** no aporta a ningún fondo de retiro.
- **14%** carga deuda educativa.

## 7. Resiliencia financiera (B7)

- **58%** califica su capacidad de cubrir necesidades básicas como holgada (4–5 de 5).
- **La tasa de ahorro mediana es 12%** del ingreso mensual (media 20%): **58% ahorra al menos 10%**, ~17% ahorra más del 30%, y **12% no ahorra nada**.

## 8. Trayectorias educativas (B8)

- **57% aprendió en la escuela**, 17% en el trabajo, 11% con cursos en línea, 9% no son desarrolladores, y solo **5% en bootcamp** (1% principalmente mediante IA).
- La relevancia autoevaluada de la educación formal para el trabajo actual promedia **7.1 / 10**.

## 9. Retención y satisfacción (B9)

- **El eNPS promedia 7.7 / 10** (n=165) — los respondientes están en general dispuestos a recomendar a su empleador.
- **La razón principal para irse es el salario** (81), luego desarrollo profesional (41), trabajo remoto (18) y cultura (10).
- **El vínculo con BP2C es muy delgado para analizar**: solo ~14 respondientes reportan que su empleador está inscrito en Best Place to Code (109 No, 41 No sé). La comparación de prima por certificación necesita más empleadores inscritos.

## 10. Inclusión — discapacidad y neurodivergencia (B10)

- **~7%** reporta una discapacidad física (12 de 168 que respondieron).
- **~18%** reporta una neurodivergencia diagnosticada (30 de 167 que respondieron) — una proporción notable que amerita un ángulo de inclusión dedicado.

---

## Metodología

- Salario base mensual normalizado a MXN (USD × tipo de cambio 18.5; robusto entre TC 17 y 20); transformado a logaritmo para la regresión; se recortan outliers fuera de ~$8k–$400k.
- El análisis de determinantes usa R² ajustada incremental (ajustada por el número de predictores, ya que el modelo completo tiene muchas dummies con n≈193).
- Las estadísticas descriptivas son medianas/proporciones sobre las respuestas disponibles; se señalan los subgrupos delgados.
- Las respuestas de tasa de ahorro se normalizaron a una escala porcentual común (entradas decimales ×100); las variantes de texto libre de trayectoria de aprendizaje se consolidaron.
- Muestra autoseleccionada; sin ponderadores poblacionales.

## Salvedades de calidad de datos

- **La inscripción a BP2C** tiene muy pocas respuestas "sí" para la comparación de prima entre encuestas.
- **16 reportes en USD** dependen de un solo supuesto de tipo de cambio.

*(Corregido en esta versión: se normalizó la codificación de tasa de ahorro y se consolidaron los duplicados de trayectoria de aprendizaje.)*
