# Brecha Salarial de Género — SG Tech Pulse 2026 (Hallazgos Preliminares)

> 🔄 **Actualizado 2026-10-12** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 12 October 2026.csv`, 688 respuestas; 620 residentes en México). Reemplaza las cifras de septiembre de 2026 (561 respuestas de México). Varias afirmaciones de septiembre cambiaron con la muestra más grande — ver el registro de cambios al final. **Los materiales de campaña derivados** (figuras de gender-slides, decks de Slidev, tarjetas, `docs/ig_scripts/`) todavía tienen fijas las cifras anteriores y deben regenerarse desde esta versión.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Fecha:** 2026-10-12
**Datos:** Volcado en vivo de SG Tech Pulse 2026, **restringido a residentes en México** (90% de la muestra). 620 respuestas de México. Género: 382 hombres, 230 mujeres, 5 no binarias. Muestra para análisis salarial: **n=558** (341 hombres, 212 mujeres).
**Estado:** Preliminar. La encuesta sigue abierta; muestra autoseleccionada (no probabilística del mercado).

---

## Resumen ejecutivo

**En el tech mexicano las mujeres son mayoría en la mitad de la escalera y se evaporan al subir — y la brecha salarial se profundiza conforme suben hacia los peldaños senior.** Cinco hallazgos:

1. **El costo que se acumula.** La brecha cruda de medianas es **37%** ($75,000 hombres vs $47,250 mujeres) y se profundiza hacia los peldaños senior: **Medio −20%, Senior −25%** (el nivel Gerente marca **−20%** pero se apoya en apenas 15 mujeres — direccional).
2. **La desaparición.** Las mujeres son el **61% de los puestos de nivel Medio pero solo ~30% de Senior en adelante.** Mayoría en el medio, alrededor de una de cada tres en la cima — y las brechas de origen (cuándo empezaron, acceso temprano a computadora) prácticamente se cerraron, así que es una historia de **paga y progresión**, no de entrada al pipeline.
3. **El residuo.** Empareja a un hombre y una mujer en experiencia, seniority, rol e inglés y **cerca de cuatro quintas partes de la brecha se cierra** — pero sobrevive una **multa de ~10%** que nada en el papel explica. Para una mujer senior son aproximadamente **$6,800/mes (~$82,000/año)**.
4. **La salida que no rescata.** Hoy las mujeres llegan a empleadores extranjeros a la **misma tasa** que los hombres (la "salida solo para hombres" de julio ya no aplica), pero ahí ganan **54% menos** — la prima transfronteriza no cierra la brecha, la repite.
5. **La pausa de carrera (mecanismo).** Las mujeres interrumpen o reducen su carrera >10 meses por motivos familiares/personales **2.3× más** que los hombres (16% vs 7%) — un motor plausible de la desaparición.

IC 95% de la brecha cruda [29%, 46%] (bootstrap). Muestra autoseleccionada; tratar como preliminar.

---

## Hallazgo 1 — El costo que se acumula: una brecha que se ensancha con el rango

**Brecha cruda.** Salario base mensual, mediana: hombres **$75,000** vs mujeres **$47,250** → **−37%** (IC 95% [29%, 46%], n=212 mujeres).

**Se ensancha hacia los peldaños senior:**

| Etapa de carrera | Hombres (mediana) | Mujeres (mediana) | Brecha | n (H / M) |
|---|---|---|---|---|
| Junior / Medio | $34,000 | $31,000 | **−9%** | 57 / 90 |
| Senior en adelante | $83,600 | $63,453 | **−24%** | 279 / 117 |

Por nivel individual: **Medio −20%, Senior −25%, Gerente −20%.** La brecha se profundiza de Medio a Senior, pero el nivel Gerente ahora se apoya en apenas **15 mujeres** — demasiado delgado para leerse como tendencia (era −32% en septiembre), así que se trata como direccional; el patrón monótono de "se ensancha en cada peldaño" ya no se sostiene. En el nivel Junior aislado las mujeres van nominalmente arriba, pero esa celda es chica y volátil, así que el arranque se ancla en la banda junior/medio, donde la brecha es un modesto −9%.

---

## Hallazgo 2 — La desaparición: mayoría en el medio, una de cada tres en la cima

- Las mujeres son el **38%** de los respondientes de México (sobre hombres+mujeres), pero la distribución se adelgaza con el rango: **61% de Junior y de Medio son mujeres, contra 32% de Senior, 20% de Staff/Principal y 25% de Gerente.** Mayoría en la base y el medio, alrededor de una de cada tres en la cima.
- El adelgazamiento cae exactamente donde crece la multa salarial (Hallazgo 1): menos mujeres *y* peor pagadas, en el mismo peldaño.
- **La explicación del pipeline ya no se sostiene.** Con la muestra más grande, las brechas de origen se cerraron: la edad mediana del primer programa es **17 en ambos** géneros, y el acceso a computadora en la infancia es **51% (mujeres) vs 48% (hombres)** — si acaso, ellas reportan un poco *más* acceso temprano. No entran más tarde ni con menos exposición; se les detiene por debajo de los niveles senior.

---

## Hallazgo 3 — El residuo: la parte que ningún currículum explica

Pon lado a lado a un hombre y una mujer con perfiles idénticos —misma experiencia, mismo seniority, mismo rol, mismo inglés— y pregunta cuánto de la brecha sobrevive.

- **Oaxaca-Blinder** (México, referencia agrupada) parte la **brecha log de 35%** en **~82% explicado** por composición (sobre todo seniority y rol — es decir, la desaparición) y **~18% no explicado**.
- La brecha ajustada de ecuación única —una mujer idéntica en cada control medido— es de **~10%.**

Monetizando el residuo de ~10%:

| | Mediana de la mujer | Hombre equivalente | Multa mensual | Multa anual |
|---|---|---|---|---|
| Mujer mediana | $47,250 | ~$52,500 | ~$5,250 | **~$63,000** |
| Mujer senior | $60,000 | ~$66,800 | ~$6,800 | **~$82,000** |

Para una mujer senior, cerca de **$6,800 al mes —unos $82,000 al año— es paga que nada sobre su experiencia, nivel, rol o inglés explica.**

> **Matiz honesto:** este residuo sigue *encogiendo* — **~10%** ahora, frente a ~12% en septiembre y ~20% en julio. Ahora más de la brecha se atribuye a la composición — lo cual no es buena noticia, porque composición aquí significa *la desaparición*: se mantiene a las mujeres fuera de los peldaños senior mejor pagados. Cerrar solo el residuo apenas movería el 37%.

---

## Hallazgo 4 — La salida que no rescata

Trabajar para un empleador extranjero es uno de los mayores aumentos del mercado. En julio la preocupación era el acceso —que el carril fuera esencialmente masculino. **Eso se volteó: hoy las mujeres llegan a empleadores extranjeros a la misma tasa que los hombres.** Pero el rescate no ocurre:

- Entre quienes trabajan para empleador extranjero, la brecha es **54%** (hombres **$109,000** vs mujeres **$50,000**, n=30 mujeres) — *más ancha* que la brecha de 24% en niveles senior a nivel local.

Así que la prima transfronteriza, presentada como la puerta de escape del bajo sueldo local, **reproduce la brecha en vez de cerrarla.**

Razones de acceso (residentes en México, mujeres vs hombres):

| Acceso | Hombres | Mujeres | RR (M/H) |
|---|---|---|---|
| Equity (stock/opciones/RSU) | 16% | 17% | 1.06 (sin brecha) |
| Empleador extranjero | 14% | 14% | 1.00 (sin brecha) |
| Totalmente remoto | 41% | 38% | 0.93 |
| Roles centrados en IA (conteo) | 37 | 17 | — |

Nota: las brechas de acceso de julio (equity, remoto, empleador extranjero) prácticamente se cerraron. La asimetría de acceso que queda está en los **roles centrados en IA** (los hombres superan a las mujeres ~2 a 1) — ver las historias para medios de IA.

---

## Hallazgo 5 — La pausa de carrera (el mecanismo)

El candidato más claro a mecanismo detrás de la desaparición aparece directo en los datos: **las mujeres interrumpen o reducen su carrera por más de 10 meses, por responsabilidades familiares o personales, a 2.3× la tasa de los hombres — 16% de las mujeres vs 7% de los hombres.** En una industria que mide seniority por años continuos y por visibilidad, una pausa de diez meses no cuesta diez meses de sueldo —resetea el reloj del ascenso justo en la etapa de vida donde se decide el salto de Medio a Senior. Menos mujeres dan ese salto; la pirámide se adelgaza.

---

## Soporte — Experiencia vivida, solo mujeres

Descriptivo, solo mujeres, residentes en México; celdas bajo umbral suprimidas:

- **~25%** reporta haberse sentido insegura o haber sufrido acoso en su empleador actual ("rara vez" 35 + "frecuentemente" 10, de 180 respuestas sustantivas) — cerca de una de cada cuatro, con 10 que lo viven de forma *frecuente*.
- **65%** dice que su empleador **no tiene ningún programa formal** para promover mujeres a liderazgo (n=178).
- **55%** son 20% o menos de su grupo de pares (mediana 20% de pares mujeres) — una clara minoría en su propio equipo.

---

## Metodología

- **Geografía:** restringido a **residentes en México** (90% de la muestra) para que el marco "tech mexicano" cuadre con los datos.
- **Salario:** base mensual, normalizado a MXN (reportes en USD × TC 18.5; estable entre TC 17–20). Transformado a log para la regresión; atípicos fuera de ~$8k–$400k recortados.
- **Brecha cruda:** mediana (robusta) con IC 95% por bootstrap de 3,000 muestras.
- **Oaxaca-Blinder:** descomposición twofold con coeficientes de referencia agrupados sobre un set parsimonioso de controles (experiencia, rango de seniority, uso de inglés, familia de rol). La brecha ajustada de ecuación única es el coeficiente de una dummy femenina en la misma especificación. La multa monetizada aplica el residuo de ~10% a las medianas.
- **Supresión:** celdas delgadas (p. ej. Gerente n=15 mujeres) marcadas como direccionales. No binarias (n=5) excluidas de la inferencia.
- **Muestra:** autoseleccionada; se presenta como muestra de respondientes, no como estimación poblacional.

---

## Limitaciones

- **Celdas por nivel aún modestas** (Gerente n=15 mujeres; Staff/Principal todavía delgada) → esas brechas por nivel son direccionales.
- **Sin descomposición de mecanismo más allá del ítem de pausa de carrera.** El instrumento desplegado todavía carece de ítems de negociación / transparencia salarial / sponsorship, así que el residuo de ~10% es *no explicado*, no atribuido a canales específicos. Para explicar *por qué* persiste, esas preguntas deberían volver en la próxima ola.
- **Mezcla de monedas** (reportes en USD) manejada con un único supuesto de tipo de cambio.
- **Preliminar:** las cifras se moverán conforme se llene la encuesta.

---

## Registro de cambios vs la versión de septiembre 2026

- **Brecha cruda:** 38% → **37%** (n=212 mujeres; IC más ajustado [29%, 46%]).
- **Brechas por nivel:** Medio −22% → **−20%**, Senior −27% → **−25%**, Gerente −32% → **−20%**. El nivel Gerente adelgazó a **15 mujeres** y ya no extiende el ensanchamiento monótono, así que el encuadre pasa de "se ensancha en cada peldaño" a **"se ensancha hacia senior"**, con Gerente marcado como direccional.
- **Residuo no explicado:** ~12% → **~10%**; la parte "explicada" del Oaxaca subió de ~80% a ~82%. La multa monetizada de la mujer senior bajó de ~$7,700/mes (~$93,000/año) a **~$6,800/mes (~$82,000/año)**.
- **La salida que no rescata:** la brecha en empleador extranjero se estrechó de 57% a **54%** (hombres $115,000 → $109,000; n mujeres 27 → 30); el acceso sigue parejo por género (14%/14%).
- **La desaparición:** la participación femenina de Senior en adelante 31% → **30%**; participación total 39% → **38%**; Staff/Principal bajó a 20%.

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
- Peticiones concretas: rendición de cuentas de empleadores en **auditorías de equidad salarial en cada nivel** (no solo la cima); **programas formales de mujeres a liderazgo** (65% de las mujeres reporta ninguno); y **reincorporación de carrera estructurada** para que una pausa familiar deje de resetear el reloj del seniority.
- Antes de que esto salga al exterior: (1) seguir creciendo las celdas femeninas por nivel, y (2) restaurar las preguntas de mecanismo para poder descomponer el residuo de ~10% en canales de negociación, sponsorship y ascenso.
