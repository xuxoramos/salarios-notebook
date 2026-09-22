# Brecha Salarial de Género — SG Tech Pulse 2026 (Hallazgos Preliminares)

> 🔄 **Actualizado 2026-09-21** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 21 September 2026.csv`, 622 respuestas; 561 residentes en México). Reemplaza las cifras de julio de 2026 (270 respuestas de México). Varias afirmaciones de julio cambiaron con la muestra más grande — ver el registro de cambios al final. **Los materiales de campaña derivados** (figuras de gender-slides, decks de Slidev, tarjetas, `docs/ig_scripts/`) todavía tienen fijas las cifras anteriores y deben regenerarse desde esta versión.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Fecha:** 2026-09-21
**Datos:** Volcado en vivo de SG Tech Pulse 2026, **restringido a residentes en México** (90% de la muestra). 561 respuestas de México. Género: 340 hombres, 213 mujeres, 5 no binarias. Muestra para análisis salarial: **n=500** (303 hombres, 197 mujeres).
**Estado:** Preliminar. La encuesta sigue abierta; muestra autoseleccionada (no probabilística del mercado).

---

## Resumen ejecutivo

**En el tech mexicano las mujeres son mayoría en la mitad de la escalera y se evaporan al subir — y la brecha salarial se ensancha en cada peldaño que sí logran subir.** Cinco hallazgos:

1. **El costo que se acumula.** La brecha cruda de medianas es **38%** ($76,000 hombres vs $47,000 mujeres) y se ensancha con el rango: **Medio −22%, Senior −27%, Gerente −32%.**
2. **La desaparición.** Las mujeres son el **62% de los puestos de nivel Medio pero solo ~31% de Senior en adelante.** Mayoría en el medio, alrededor de una de cada tres en la cima — y las brechas de origen (cuándo empezaron, acceso temprano a computadora) prácticamente se cerraron, así que es una historia de **paga y progresión**, no de entrada al pipeline.
3. **El residuo.** Empareja a un hombre y una mujer en experiencia, seniority, rol e inglés y **cerca de cuatro quintas partes de la brecha se cierra** — pero sobrevive una **multa de ~12%** que nada en el papel explica. Para una mujer senior son aproximadamente **$7,700/mes (~$93,000/año)**.
4. **La salida que no rescata.** Hoy las mujeres llegan a empleadores extranjeros a la **misma tasa** que los hombres (la "salida solo para hombres" de julio ya no aplica), pero ahí ganan **57% menos** — la prima transfronteriza no cierra la brecha, la repite.
5. **La pausa de carrera (mecanismo).** Las mujeres interrumpen o reducen su carrera >10 meses por motivos familiares/personales **2.3× más** que los hombres (16% vs 7%) — un motor plausible de la desaparición.

IC 95% de la brecha cruda [29%, 48%] (bootstrap). Muestra autoseleccionada; tratar como preliminar.

---

## Hallazgo 1 — El costo que se acumula: una brecha que se ensancha con el rango

**Brecha cruda.** Salario base mensual, mediana: hombres **$76,000** vs mujeres **$47,000** → **−38%** (IC 95% [29%, 48%], n=197 mujeres).

**Se ensancha con el seniority:**

| Etapa de carrera | Hombres (mediana) | Mujeres (mediana) | Brecha | n (H / M) |
|---|---|---|---|---|
| Junior / Medio | $35,000 | $32,000 | **−9%** | 53 / 84 |
| Senior en adelante | $85,000 | $63,453 | **−25%** | 247 / 109 |

Por nivel individual: **Medio −22%, Senior −27%, Gerente −32%** (Gerente n=14 mujeres, direccional). En el nivel Junior aislado las mujeres van nominalmente arriba, pero esa celda es chica y volátil (n=26 mujeres), así que el arranque se ancla en la banda junior/medio, donde la brecha es un modesto −9%.

---

## Hallazgo 2 — La desaparición: mayoría en el medio, una de cada tres en la cima

- Las mujeres son el **39%** de los respondientes de México (sobre hombres+mujeres), pero la distribución se adelgaza con el rango: **59% de Junior y 62% de Medio son mujeres, contra 32% de Senior y 24–25% de Staff/Principal y Gerente.** Mayoría en la base y el medio, alrededor de una de cada tres en la cima.
- El adelgazamiento cae exactamente donde crece la multa salarial (Hallazgo 1): menos mujeres *y* peor pagadas, en el mismo peldaño.
- **La explicación del pipeline ya no se sostiene.** Con la muestra más grande, las brechas de origen se cerraron: la edad mediana del primer programa es **17 en ambos** géneros, y el acceso a computadora en la infancia es **53% (mujeres) vs 49% (hombres)** — si acaso, ellas reportan un poco *más* acceso temprano. No entran más tarde ni con menos exposición; se les detiene por debajo de los niveles senior.

---

## Hallazgo 3 — El residuo: la parte que ningún currículum explica

Pon lado a lado a un hombre y una mujer con perfiles idénticos —misma experiencia, mismo seniority, mismo rol, mismo inglés— y pregunta cuánto de la brecha sobrevive.

- **Oaxaca-Blinder** (México, referencia agrupada) parte la **brecha log de 36%** en **~80% explicado** por composición (sobre todo seniority y rol — es decir, la desaparición) y **~20% no explicado**.
- La brecha ajustada de ecuación única —una mujer idéntica en cada control medido— es de **~12%.**

Monetizando el residuo de ~12%:

| | Mediana de la mujer | Hombre equivalente | Multa mensual | Multa anual |
|---|---|---|---|---|
| Mujer mediana | $47,000 | ~$53,200 | ~$6,200 | **~$75,000** |
| Mujer senior | $58,300 | ~$66,000 | ~$7,700 | **~$93,000** |

Para una mujer senior, cerca de **$7,700 al mes —unos $93,000 al año— es paga que nada sobre su experiencia, nivel, rol o inglés explica.**

> **Matiz honesto:** este residuo es *menor* que la estimación de julio (~12% vs el ~20% anterior). Ahora más de la brecha se atribuye a la composición — lo cual no es buena noticia, porque composición aquí significa *la desaparición*: se mantiene a las mujeres fuera de los peldaños senior mejor pagados. Cerrar solo el residuo apenas movería el 38%.

---

## Hallazgo 4 — La salida que no rescata

Trabajar para un empleador extranjero es uno de los mayores aumentos del mercado. En julio la preocupación era el acceso —que el carril fuera esencialmente masculino. **Eso se volteó: hoy las mujeres llegan a empleadores extranjeros a la misma tasa que los hombres.** Pero el rescate no ocurre:

- Entre quienes trabajan para empleador extranjero, la brecha es **57%** (hombres **$115,000** vs mujeres **$50,000**, n=27 mujeres) — *más ancha* que la brecha de 25% en niveles senior a nivel local.

Así que la prima transfronteriza, presentada como la puerta de escape del bajo sueldo local, **reproduce la brecha en vez de cerrarla.**

Razones de acceso (residentes en México, mujeres vs hombres):

| Acceso | Hombres | Mujeres | RR (M/H) |
|---|---|---|---|
| Equity (stock/opciones/RSU) | 17% | 17% | 1.02 (sin brecha) |
| Empleador extranjero | 12% | 13% | 1.09 (sin brecha) |
| Totalmente remoto | 40% | 37% | 0.91 |
| Roles centrados en IA (conteo) | 34 | 17 | — |

Nota: las brechas de acceso de julio (equity, remoto, empleador extranjero) prácticamente se cerraron. La asimetría de acceso que queda está en los **roles centrados en IA** (los hombres superan a las mujeres ~2 a 1) — ver las historias para medios de IA.

---

## Hallazgo 5 — La pausa de carrera (el mecanismo)

El candidato más claro a mecanismo detrás de la desaparición aparece directo en los datos: **las mujeres interrumpen o reducen su carrera por más de 10 meses, por responsabilidades familiares o personales, a 2.3× la tasa de los hombres — 16% de las mujeres vs 7% de los hombres.** En una industria que mide seniority por años continuos y por visibilidad, una pausa de diez meses no cuesta diez meses de sueldo —resetea el reloj del ascenso justo en la etapa de vida donde se decide el salto de Medio a Senior. Menos mujeres dan ese salto; la pirámide se adelgaza.

---

## Soporte — Experiencia vivida, solo mujeres

Descriptivo, solo mujeres, residentes en México; celdas bajo umbral suprimidas:

- **~25%** reporta haberse sentido insegura o haber sufrido acoso en su empleador actual ("rara vez" 34 + "frecuentemente" 8, de 166 respuestas sustantivas) — cerca de una de cada cuatro, con 8 que lo viven de forma *frecuente*.
- **63%** dice que su empleador **no tiene ningún programa formal** para promover mujeres a liderazgo (n=167).
- **40%** son 20% o menos de su grupo de pares (mediana 20% de pares mujeres) — una clara minoría en su propio equipo.

---

## Metodología

- **Geografía:** restringido a **residentes en México** (90% de la muestra) para que el marco "tech mexicano" cuadre con los datos.
- **Salario:** base mensual, normalizado a MXN (reportes en USD × TC 18.5; estable entre TC 17–20). Transformado a log para la regresión; atípicos fuera de ~$8k–$400k recortados.
- **Brecha cruda:** mediana (robusta) con IC 95% por bootstrap de 3,000 muestras.
- **Oaxaca-Blinder:** descomposición twofold con coeficientes de referencia agrupados sobre un set parsimonioso de controles (experiencia, rango de seniority, uso de inglés, familia de rol). La brecha ajustada de ecuación única es el coeficiente de una dummy femenina en la misma especificación. La multa monetizada aplica el residuo de ~12% a las medianas.
- **Supresión:** celdas delgadas (p. ej. Gerente n=14, Junior n=26 mujeres) marcadas como direccionales. No binarias (n=5) excluidas de la inferencia.
- **Muestra:** autoseleccionada; se presenta como muestra de respondientes, no como estimación poblacional.

---

## Limitaciones

- **Celdas por nivel aún modestas** (Gerente n=14, Staff/Principal n=8 mujeres) → esas brechas por nivel son direccionales.
- **Sin descomposición de mecanismo más allá del ítem de pausa de carrera.** El instrumento desplegado todavía carece de ítems de negociación / transparencia salarial / sponsorship, así que el residuo de ~12% es *no explicado*, no atribuido a canales específicos. Para explicar *por qué* persiste, esas preguntas deberían volver en la próxima ola.
- **Mezcla de monedas** (reportes en USD) manejada con un único supuesto de tipo de cambio.
- **Preliminar:** las cifras se moverán conforme se llene la encuesta.

---

## Registro de cambios vs la versión de julio 2026

- **Brecha cruda:** 40% → **38%** (IC más ajustado, n=197 mujeres).
- **Residuo no explicado:** ~20% → **~12%**; la parte "explicada" del Oaxaca subió de ~48% a ~80%. La brecha es ahora más claramente una historia de composición (la desaparición) que de multa pura.
- **Se retira la "salida solo para hombres":** el *acceso* a empleador extranjero ya es igual por género (RR 1.09); la historia es la **brecha de paga de 57% en empleadores extranjeros**, no el acceso.
- **Brechas de acceso a equity y remoto:** prácticamente cerradas (RR 1.02 y 0.91).
- **Hallazgo nuevo:** el ítem de **pausa de carrera** (16% mujeres vs 7% hombres) se surface como el principal candidato a mecanismo.
- **Brechas de origen** (edad del primer programa, acceso a computadora en la infancia): confirmadas cerradas.

---

## Implicaciones (para AMITI / incidencia)

- El reencuadre es el mensaje: **las mujeres son mayoría en el medio y se evaporan en la cima.** Es un problema de paga y progresión, no de entrada al pipeline — las brechas de origen se cerraron. Arreglar el paso del ascenso, no solo la entrada.
- Peticiones concretas: rendición de cuentas de empleadores en **auditorías de equidad salarial en cada nivel** (no solo la cima); **programas formales de mujeres a liderazgo** (63% de las mujeres reporta ninguno); y **reincorporación de carrera estructurada** para que una pausa familiar deje de resetear el reloj del seniority.
- Antes de que esto salga al exterior: (1) seguir creciendo las celdas femeninas por nivel, y (2) restaurar las preguntas de mecanismo para poder descomponer el residuo de ~12% en canales de negociación, sponsorship y ascenso.
