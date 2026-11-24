# Brecha Salarial de Género — SG Tech Pulse 2026 (Hallazgos Preliminares)

> 🔄 **Actualizado 2026-11-19** con el volcado vigente (`data/Responses - Encuesta de Salarios SG 2026 - 19 November 2026.csv`, 787 respuestas, 712 residentes en México). Reemplaza las cifras de octubre de 2026 (620 respuestas de México). Varias afirmaciones de octubre cambiaron con la muestra más grande, y algunas tasas se corrigieron con la regla de calcular sobre quienes respondieron. Ver el registro de cambios al final.

> **"En el tech mexicano las mujeres son mayoría en el medio, y se evaporan rumbo a la cima."**

**Fecha:** 2026-11-19
**Datos:** Volcado en vivo de SG Tech Pulse 2026, **restringido a residentes en México** (90% de la muestra). 712 respuestas de México. Género: 416 hombres, 287 mujeres, 5 no binarias. Muestra para análisis salarial: **n=642** (374 hombres, 262 mujeres).
**Estado:** Preliminar. La encuesta sigue abierta. La muestra es autoseleccionada (no probabilística del mercado).

---

## Resumen ejecutivo

**En el tech mexicano las mujeres son mayoría en la mitad de la escalera y se evaporan al subir, y la brecha salarial se profundiza conforme suben hacia los peldaños senior.** Cinco hallazgos:

1. **El costo que se acumula.** La brecha cruda de medianas es **39%** ($73,900 hombres vs $45,000 mujeres) y se ensancha hacia los peldaños senior: **Medio −10%, Senior −29%**, así que la brecha casi se triplica del nivel medio a Senior. El nivel Gerente marca **−22%** con apenas 22 mujeres (direccional), así que la brecha se ensancha hacia senior pero no crece en cada peldaño.
2. **La desaparición.** Las mujeres son el **59% de los puestos de nivel Medio pero solo el 33% de Senior en adelante.** Mayoría en el medio, una de cada tres en la cima. Las brechas de origen son chicas o nulas (edad mediana del primer programa 18 en mujeres vs 17 en hombres, y ellas reportan un poco *más* acceso temprano a computadora), así que es una historia de **paga y progresión**, no de entrada al pipeline.
3. **Sobre todo la escalera, más una multa chica.** Al emparejar experiencia, inglés, nivel y rol, la brecha cae de 39% a cerca de **10%** por etapas. Ese ~10% ya se distingue del cero, aunque por poco: **intervalo de confianza al 95% de 1% a 19% (p≈0.035)**. La estimación es la misma que en octubre. Lo que cambió es la precisión, porque hay más respuestas. Sí existe una multa por el mismo perfil, pero es chica e imprecisa, así que no la convertimos en pesos. El efecto queda **acotado entre ~10% y 39%**, y la parte grande y firme de la brecha sigue siendo la escalera: cerca de **82%** se explica por composición, sobre todo nivel y rol.
4. **La salida que no rescata.** Las mujeres llegan a empleadores extranjeros a la **misma tasa** que los hombres (13% vs 14%), pero ahí ganan **55% menos** (32 mujeres, direccional). La prima transfronteriza no cierra la brecha, la repite.
5. **La pausa de carrera (mecanismo).** Entre quienes respondieron, las mujeres interrumpen o reducen su carrera >10 meses por motivos familiares/personales **2.3× más** que los hombres (21% vs 9%). Es un motor plausible de la desaparición.

IC 95% de la brecha cruda [30%, 46%] (bootstrap). Muestra autoseleccionada, tratar como preliminar.

---

## Hallazgo 1 — El costo que se acumula: una brecha que se ensancha hacia los peldaños senior

**Brecha cruda.** Salario base mensual, mediana: hombres **$73,900** vs mujeres **$45,000** → **−39%** (IC 95% [30%, 46%], n=262 mujeres).

**Se ensancha hacia los peldaños senior:**

| Etapa de carrera | Hombres (mediana) | Mujeres (mediana) | Brecha | n (H / M) |
|---|---|---|---|---|
| Junior / Medio | $34,500 | $32,750 | **−5%** | 68 / 107 |
| Senior en adelante | $80,750 | $58,000 | **−28%** | 300 / 146 |

Por nivel individual: **Medio −10%, Senior −29%, Gerente −22%.** La brecha casi se triplica de Medio a Senior. El nivel Gerente marca menos que Senior y se apoya en apenas **22 mujeres** (15 en octubre), todavía demasiado delgado para leerse como tendencia, así que se trata como direccional. El patrón es "se ensancha hacia los peldaños senior", no "se ensancha en cada peldaño". En el nivel Junior aislado las mujeres van nominalmente arriba, pero esa celda es delgada y volátil (19 hombres), así que el arranque se ancla en la banda junior/medio, donde la brecha es un modesto −5%.

---

## Hallazgo 2 — La desaparición: mayoría en el medio, una de cada tres en la cima

- Las mujeres son el **41%** de los respondientes de México (sobre hombres+mujeres), pero la distribución se adelgaza con el rango: **66% de Junior y 59% de Medio son mujeres, contra 34% de Senior, 23% de Staff/Principal y 32% de Gerente** (Senior en adelante combinado: **33%**). Director marca 44%, pero en una celda delgada (n=32), así que es direccional. Mayoría en la base y el medio, una de cada tres en la cima.
- El adelgazamiento cae exactamente donde crece la brecha salarial (Hallazgo 1): en Senior las mujeres son el 34% del nivel y ganan 29% menos. Menos mujeres *y* peor pagadas, en el mismo peldaño.
- **La explicación del pipeline no se sostiene.** Las brechas de origen son chicas o nulas. La edad mediana del primer programa es **18 en mujeres vs 17 en hombres** (un año de diferencia), y el acceso a computadora en la infancia, entre quienes respondieron, es **61% (mujeres) vs 58% (hombres)**. Si acaso, ellas reportan un poco *más* acceso temprano. No entran al tech con menos exposición. Se les detiene por debajo de los niveles senior.

---

## Hallazgo 3 — ¿De dónde viene la brecha? De la escalera

Pon lado a lado a un hombre y una mujer y mira cuánto de la brecha sobrevive a cada control. Cae de forma ordenada conforme se agregan:

| Controles | Brecha ajustada |
|---|---|
| Sin ajuste | **35%** |
| + experiencia | 24% |
| + inglés | 21% |
| + nivel (seniority) | 16% |
| + rol | **10%** |

*La escalera es una regresión sobre el logaritmo del salario, así que su fila sin ajuste (35%) compara el salario promedio en logaritmos. Difiere de la brecha cruda de 39%, que compara medianas. Las dos son correctas, miden la brecha de forma distinta.*

- La **descomposición Oaxaca-Blinder** (México, referencia agrupada) parte la brecha log en **~82% explicado** por composición (sobre todo seniority y rol, es decir, la desaparición) y **~18% no explicado**.
- La brecha ajustada de ecuación única (una mujer idéntica en cada control medido) es de **~10%** (10.2%, n=636). Su **intervalo de confianza al 95% va de cerca de 1% a 19%** (robusto HC3 [0.7%, 18.7%], **p≈0.035**), y los intervalos bootstrap con cinco semillas coinciden (límites inferiores de 0.7% a 1.4%). La estimación puntual es la misma que en octubre. Lo que cambió es la precisión: con más respuestas, el intervalo ya no toca el cero, aunque por poco. El residuo es **robusto al tipo de cambio** (10% con TC 17, 18.5 y 20).
- Así que sí existe una multa por el mismo perfil, pero es chica e imprecisa. **No la convertimos en pesos**, porque un intervalo de 1% a 19% es demasiado ancho. Y "no explicado" no es discriminación probada: el residuo también contiene lo que los controles no miden.

**Lectura honesta: cotas, no un punto.** El efecto del género queda **acotado entre ~10% (emparejando todo) y 39% (sin ajustar)**. Y hay una trampa estadística: controlar por nivel y rol probablemente *subestima* el efecto, porque el nivel y el rol son en parte consecuencia del mismo sesgo (a las mujeres se las mantiene abajo). Así que el valor real vive en ese rango, y hasta el extremo bajo (~10%) ya queda por encima del cero, aunque por poco.

> **El mensaje firme sigue siendo la escalera, no la multa.** La parte grande y estadísticamente sólida de la brecha es la **progresión**: a las mujeres se las mantiene en los peldaños peor pagados (Hallazgo 2). El pedazo que ni el nivel ni el rol explican es real, pero chico e impreciso. Cerrar solo ese residuo dejaría en pie la mayor parte del 39%. No lo llames discriminación probada.

---

## Hallazgo 4 — La salida que no rescata

Trabajar para un empleador extranjero es uno de los mayores aumentos del mercado. En julio la preocupación era el acceso, que el carril fuera esencialmente masculino. **Eso se volteó: hoy las mujeres llegan a empleadores extranjeros a la misma tasa que los hombres.** Pero el rescate no ocurre:

- Entre quienes trabajan para empleador extranjero, la brecha es **55%** (hombres **$110,000** vs mujeres **$50,000**, n=32 mujeres, direccional). Es *más ancha* que la brecha de 28% en toda la banda de Senior en adelante.

Así que la prima transfronteriza, presentada como la puerta de escape del bajo sueldo local, **reproduce la brecha en vez de cerrarla.**

Tasas de acceso (residentes en México, sobre quienes respondieron cada pregunta):

| Acceso | Hombres | Mujeres | RR (M/H) |
|---|---|---|---|
| Equity (stock/opciones/RSU) | 18% | 18% | ≈1.0 (sin brecha) |
| Empleador extranjero | 14% | 13% | ≈0.9 (sin brecha relevante) |
| Totalmente remoto | 45% | 37% | **0.82** |
| Roles centrados en IA (conteo) | 43 | 22 | — |

Nota: el acceso a equity y a empleador extranjero está parejo, pero **la brecha en trabajo totalmente remoto se volvió a abrir** (RR 0.82, era 0.93 en octubre), y los **roles centrados en IA** van casi dos a uno (43 hombres vs 22 mujeres). Ver las historias para medios de IA.

---

## Hallazgo 5 — La pausa de carrera (el mecanismo)

El candidato más claro a mecanismo detrás de la desaparición aparece directo en los datos: **entre quienes respondieron, las mujeres interrumpen o reducen su carrera por más de 10 meses, por responsabilidades familiares o personales, a 2.3× la tasa de los hombres: 21% de las mujeres (n=222) vs 9% de los hombres (n=338).** (La tasa ahora se reporta sobre quienes respondieron el ítem. Es una corrección metodológica: el 16% vs 7% publicado antes contaba las no respuestas como "no". La razón 2.3× no cambia.) En una industria que mide seniority por años continuos y por visibilidad, una pausa de diez meses no cuesta diez meses de sueldo —resetea el reloj del ascenso justo en la etapa de vida donde se decide el salto de Medio a Senior. Menos mujeres dan ese salto; la pirámide se adelgaza.

---

## Soporte — Experiencia vivida, solo mujeres

Descriptivo, solo mujeres, residentes en México. Celdas bajo umbral suprimidas. Porcentajes sobre quienes respondieron cada pregunta:

- **~25%** reporta haberse sentido insegura o haber sufrido acoso en su empleador actual ("rara vez" 42 + "frecuentemente" 12, de 217 respuestas sustantivas, 222 si se incluye "prefiero no responder"). Cerca de una de cada cuatro, con 12 que lo viven de forma *frecuente*.
- **65%** dice que su empleador **no tiene ningún programa formal** para promover mujeres a liderazgo (n=220).
- **54%** son 20% o menos de su grupo de pares (mediana 20% de pares mujeres, n=196). Una clara minoría entre sus pares de puesto.

---

## Metodología

- **Geografía:** restringido a **residentes en México** (90% de la muestra) para que el marco "tech mexicano" cuadre con los datos.
- **Denominadores:** los porcentajes se calculan sobre quienes respondieron cada pregunta. Las no respuestas se excluyen, no se cuentan como "no".
- **Salario:** base mensual, normalizado a MXN (reportes en USD × TC 18.5; estable entre TC 17–20). Transformado a log para la regresión; atípicos fuera de ~$8k–$400k recortados.
- **Brecha cruda:** mediana (robusta) con IC 95% por bootstrap de 3,000 muestras.
- **Oaxaca-Blinder y escalera de controles:** descomposición twofold con coeficientes de referencia agrupados sobre un set parsimonioso de controles (experiencia, rango de seniority, uso de inglés, familia de rol). La escalera de controles reporta la brecha al agregar cada bloque en orden (sin ajuste → experiencia → inglés → nivel → rol). La brecha ajustada de ecuación única es el coeficiente de una dummy femenina en la especificación completa (n=636). Su IC 95% y su valor p salen de una prueba analítica con errores estándar robustos a heterocedasticidad (HC3), contrastada con un bootstrap (1,000 réplicas, repetido con cinco semillas, y todos los intervalos excluyen el cero). No se monetiza el residuo: su intervalo ya excluye el cero, pero es demasiado ancho (≈1% a 19%) para sostener una cifra en pesos.
- **Supresión:** celdas delgadas (p. ej. Gerente n=22 mujeres, Junior n=19 hombres, empleador extranjero n=32 mujeres) marcadas como direccionales. No binarias (n=5) excluidas de la inferencia.
- **Muestra:** autoseleccionada. Se presenta como muestra de respondientes, no como estimación poblacional.

---

## Limitaciones

- **Celdas por nivel aún modestas** (Gerente n=22 mujeres; Staff/Principal y Director todavía delgadas) → esas brechas por nivel son direccionales.
- **El residuo ajustado apenas se distingue de cero** (p≈0.035, IC 95% ≈1% a 19%). Es chico e impreciso, así que no se monetiza, y un residuo no explicado no es prueba de discriminación. El hallazgo firme es la brecha cruda (39%) operando por la progresión (la desaparición), no el residuo.
- **Controles potencialmente endógenos.** Controlar por nivel y rol puede *subestimar* el efecto del género, porque a las mujeres se las mantiene abajo en esas mismas variables. Por eso presentamos cotas (~10% a 39%) en lugar de un único punto.
- **Sin descomposición de mecanismo más allá del ítem de pausa de carrera.** El instrumento desplegado todavía carece de ítems de negociación / transparencia salarial / sponsorship, así que el residuo es *no explicado*, no atribuido a canales específicos. Para explicar *por qué* persiste, esas preguntas deberían volver en la próxima ola.
- **Mezcla de monedas** (reportes en USD) manejada con un único supuesto de tipo de cambio.
- **Preliminar:** las cifras se moverán conforme se llene la encuesta.

---

## Registro de cambios vs la versión de octubre 2026

- **Brecha cruda:** 37% → **39%** (hombres $75,000 → $73,900, mujeres $47,250 → $45,000, n mujeres 212 → 262, IC 95% [29%, 46%] → [30%, 46%]).
- **Brechas por nivel:** Medio −20% → **−10%**, Senior −25% → **−29%**, Gerente −20% → **−22%** (n mujeres 15 → 22, sigue direccional). Bandas: Junior/Medio −9% → **−5%**, Senior en adelante −24% → **−28%**. La brecha ahora casi se triplica de Medio a Senior. El encuadre sigue siendo **"se ensancha hacia senior"**, no "en cada peldaño" (Gerente queda por debajo de Senior).
- **Residuo ajustado:** misma estimación puntual (**10.2%**), pero ahora ya no toca el cero. El IC 95% de octubre, [0%, 20%] (HC3 [−0.2%, 19.5%], p=0.054), tocaba el cero. El de noviembre es **[0.7%, 18.7%], p=0.035**. El cambio viene de más precisión, no de un efecto más grande. La escalera pasó de 35 → 25 → 22 → 15 → 10 a **35 → 24 → 21 → 16 → 10**. El reparto Oaxaca no cambia (~82% explicado, ~18% no explicado). Nueva lectura: una multa por el mismo perfil, chica e imprecisa. Sigue sin monetizarse, sigue sin ser discriminación probada y se sigue reportando como cotas (~10% a 39%).
- **La desaparición:** participación femenina por nivel Junior 61% → **66%**, Medio 61% → **59%**, Senior 32% → **34%**, Staff/Principal 20% → **23%**, Gerente 25% → **32%**, Director 41% → **44%**. Senior en adelante 30% → **33%**. Participación femenina total 38% → **41%**.
- **La salida que no rescata:** la brecha en empleador extranjero pasó de 54% a **55%** (hombres $109,000 → $110,000, mujeres sin cambio en $50,000, n mujeres 30 → 32).
- **Acceso (ahora sobre quienes respondieron):** **la brecha en trabajo totalmente remoto se volvió a abrir**, RR 0.93 → **0.82** (hombres 45% vs mujeres 37%). Equity 16%/17% → **18%/18%** y empleador extranjero 14%/14% → **14%/13%** (hombres/mujeres), ambos siguen parejos. Roles centrados en IA 37/17 → **43/22** (hombres/mujeres), casi dos a uno.
- **Origen:** la edad mediana del primer programa pasó de 17 en ambos a **18 (mujeres) vs 17 (hombres)**. Sigue siendo una brecha chica.
- **Regla de denominador (corrección metodológica):** las tasas de prevalencia ahora se calculan sobre quienes respondieron cada pregunta, no sobre todas las filas (lo que contaba las no respuestas como "no"). Pausa de carrera 16% vs 7% → **21% vs 9%** (misma razón 2.3×, denominador corregido). Acceso a computadora en la infancia 51% vs 48% → **61% vs 58%** (ellas siguen un poco arriba).
- **Soporte:** acoso sigue en ~25% (ahora 42 + 12 de 217 respuestas sustantivas). Sin programa formal de liderazgo sigue en 65% (n=220). Quienes son ≤20% de su grupo de pares 55% → **54%** (n=196).

---

## Registro de cambios vs la versión de septiembre 2026

- **Brecha cruda:** 38% → **37%** (n=212 mujeres; IC más ajustado [29%, 46%]).
- **Brechas por nivel:** Medio −22% → **−20%**, Senior −27% → **−25%**, Gerente −32% → **−20%**. El nivel Gerente adelgazó a **15 mujeres** y ya no extiende el ensanchamiento monótono, así que el encuadre pasa de "se ensancha en cada peldaño" a **"se ensancha hacia senior"**, con Gerente marcado como direccional.
- **Residuo no explicado:** ~12% → **~10%**; la parte "explicada" del Oaxaca subió de ~80% a ~82%. **Endurecimiento metodológico:** ahora reportamos la escalera de controles (37% → 25% → 22% → 15% → 10%), el IC 95% del residuo ajustado (**[0%, 20%], toca el cero**) y su robustez al TC (10% con TC 17/18.5/20). Se retira la multa monetizada de la mujer senior (~$6,800/mes), porque el residuo no es distinguible de cero; el efecto se reporta como cotas (~10% a 37%).
- **La salida que no rescata:** la brecha en empleador extranjero se estrechó de 57% a **54%** (hombres $115,000 → $109,000; n mujeres 27 → 30); el acceso sigue parejo por género (14%/14%).
- **La desaparición:** la participación femenina de Senior en adelante 31% → **30%**; participación total 39% → **38%**; Staff/Principal bajó a 20%.

---

## Registro de cambios vs la versión de julio 2026

- **Brecha cruda:** 40% → **38%** (IC más ajustado, n=197 mujeres).
- **Residuo no explicado:** ~20% → **~12%**; la parte "explicada" del Oaxaca subió de ~48% a ~80%. La brecha es ahora más claramente una historia de composición (la desaparición) que de multa pura.
- **Se retira la "salida solo para hombres":** el *acceso* a empleador extranjero ya es igual por género (RR 1.09); la historia es la **brecha de paga de 57% en empleadores extranjeros**, no el acceso.
- **Brechas de acceso a equity y remoto:** prácticamente cerradas (RR 1.02 y 0.91).
- **Hallazgo nuevo:** el ítem de **pausa de carrera** (16% mujeres vs 7% hombres) se presenta como el principal candidato a mecanismo.
- **Brechas de origen** (edad del primer programa, acceso a computadora en la infancia): confirmadas cerradas.

---

## Implicaciones (para AMITI / incidencia)

- El reencuadre es el mensaje: **las mujeres son mayoría en el medio y se evaporan en la cima.** Es un problema de paga y progresión, no de entrada al pipeline, porque las brechas de origen son chicas o nulas. Arreglar el paso del ascenso, no solo la entrada.
- Peticiones concretas: rendición de cuentas de empleadores en **auditorías de equidad salarial en cada nivel** (no solo la cima); **programas formales de mujeres a liderazgo** (65% de las mujeres reporta ninguno); y **reincorporación de carrera estructurada** para que una pausa familiar (21% de las mujeres vs 9% de los hombres) deje de resetear el reloj del seniority.
- Antes de que esto salga al exterior: (1) seguir creciendo las celdas femeninas por nivel, y (2) restaurar las preguntas de mecanismo para poder descomponer el residuo de ~10%, que ya queda apenas por encima del cero, en canales de negociación, sponsorship y ascenso.
