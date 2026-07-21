# Brecha Salarial de Género — SG Tech Pulse 2026 (Hallazgos Preliminares)

**Fecha:** 2026-07-21
**Datos:** Volcado de respuestas en vivo de SG Tech Pulse 2026 — 217 respuestas (165 completas, 52 parciales).
Género: 154 hombres, 60 mujeres, 2 personas no binarias, 1 sin especificar. Muestra para análisis salarial: **n=192** (136 hombres, 56 mujeres).
**Estado:** Preliminar. La encuesta sigue abierta; la muestra es autoseleccionada (no es una muestra probabilística del mercado).

---

## Resumen ejecutivo

1. **Las mujeres en tech ganan ~32% menos** de salario base mensual que los hombres ($55,000 vs $80,500 de mediana).
2. **~25% de esa brecha sobrevive a los controles** por experiencia, seniority, rol, industria, tamaño de empresa e inglés. La mayor parte de la brecha *no* se explica porque las mujeres sean más junior o estén en otros roles.
3. **La brecha es un fenómeno de la parte alta de la escalera:** casi nula en nivel medio, pero ~29% en Senior y ~38% en Gerente.
4. **Las mujeres son 28% de la muestra, pero se adelgazan por encima del nivel medio** (58% de Medio, ~20% de Senior en adelante), una fuga visible en la cima.
5. Las brechas de acceso de apoyo son **más moderadas de lo que sugerían las cifras iniciales de muestra pequeña**, pero las señales de experiencia vivida (aislamiento, acoso, ausencia de programas de liderazgo) son preocupantes.

---

## 1. La brecha (G1 cruda, G2 ajustada)

**Brecha cruda.** Salario base mensual, mediana: hombres **$80,500** vs mujeres **$55,000** → **−31.7%** (IC 95% [10%, 53%]; brecha por media 35%). El intervalo de confianza es amplio porque la muestra femenina aún es pequeña, pero excluye el cero.

**Brecha ajustada.** En una regresión de salario logarítmico controlando por experiencia tech, nivel de seniority, uso de inglés, rol, industria y tamaño de empresa, el coeficiente femenino corresponde a una brecha de **~25–26%** (IC 95% aproximadamente [10–12%, 38%]); las especificaciones simple y completa coinciden:

| Especificación | Brecha ajustada | IC 95% | R² | k |
|---|---|---|---|---|
| Simple (experiencia + seniority + inglés) | −26.3% | [12%, 38%] | 0.55 | 18 |
| Completa (+ rol + industria + tamaño) | −25.4% | [10%, 38%] | 0.77 | 73 |

**Interpretación:** la mayor parte de la brecha cruda no se explica por composición. El titular defendible es *"al mismo nivel, mismo rol y misma experiencia, las mujeres aún ganan cerca de una cuarta parte menos."*

---

## 2. Dónde se abre la brecha (G3)

La brecha es pequeña en nivel medio y se ensancha con la seniority (se suprimen los niveles con menos de 5 mujeres):

| Nivel | Hombres (mediana) | Mujeres (mediana) | Brecha | n (H / M) |
|---|---|---|---|---|
| Medio | $46,500 | $45,500 | −2% | 10 / 14 |
| Senior | $79,500 | $56,795 | **−29%** | 52 / 21 |
| Gerente | $96,500 | $60,000 | **−38%** | 30 / 7 (directivo) |
| Junior / Staff-Principal / Director | — | — | suprimido | mujeres <5 |

---

## 3. Representación y pipeline (G5)

- **Las mujeres son 27.8%** de la muestra en total.
- **La distribución se fuga en la cima.** Proporción femenina por nivel: Junior 19%, **Medio 58%**, Senior 28%, Staff-Principal 19%, Gerente 21%, Director 20%. Las mujeres se concentran en nivel medio y se adelgazan por encima.
- **Brecha de origen del pipeline:** las mujeres escribieron su primer programa más tarde (mediana **19 vs 17**) y tuvieron menos acceso a computadora en la infancia (**40% vs 51%**).

---

## 4. Brechas de acceso de apoyo (G4)

Con la muestra más grande son reales pero moderadas (mujeres vs hombres, proporción y razón de riesgo):

| Acceso | Hombres | Mujeres | RR (M/H) |
|---|---|---|---|
| Equity (acciones/opciones/RSU) | 24% | 17% | 0.70 |
| Empleador extranjero | 20% | 14% | 0.70 |
| Totalmente remoto | 46% | 46% | 1.00 (sin brecha) |
| Roles centrados en IA (conteo) | 14 | 5 | — |

Nota: las cifras de la semana de lanzamiento salían de ~15 mujeres y sobreestimaban algunas de estas (p. ej. equity parecía 3×, remoto 2×, roles de IA 7 a 0). Con 60 mujeres, las brechas de equity y de empleador extranjero son ~0.70, la brecha de remoto desaparece, y sí aparecen mujeres en roles de IA. Citar los valores de esta tabla, no los del lanzamiento.

---

## 5. Experiencia vivida de las mujeres (G6)

Descriptivo, solo mujeres, n≈47, celdas por debajo del umbral suprimidas:

- **~30%** reporta haberse sentido insegura o haber sufrido acoso ("rara vez" 26% + "frecuentemente" 4%).
- **68%** dice que su empleador **no tiene un programa formal** para promover a mujeres hacia el liderazgo.
- **49%** es el 20% o menos de su grupo de pares (mediana 25% de pares mujeres): la mitad es una clara minoría en su propio equipo.

---

## Metodología

- **Salario:** base mensual, normalizado a MXN (reportes en USD × tipo de cambio 18.5; las conclusiones son estables entre TC 17 y 20). Transformado a logaritmo para la regresión; se recortan outliers fuera de ~$8k–$400k.
- **Brecha cruda:** mediana (robusta) con IC 95% por bootstrap de 3,000 muestras.
- **Brecha ajustada:** MCO sobre salario logarítmico; el coeficiente femenino se reporta como `1 − exp(β)` con IC por aproximación normal.
- **Supresión:** se retiene cualquier celda publicada con menos de 5 mujeres. Las personas no binarias (n=2) se excluyen de la inferencia.
- **Muestra:** respondientes autoseleccionados; se presenta como muestra de respondientes, no como estimación poblacional.

---

## Limitaciones

- **Muestra femenina pequeña** (56 con salario) → intervalos amplios, sobre todo por nivel.
- **Sin descomposición por mecanismo.** El instrumento desplegado eliminó los ítems de negociación / transparencia salarial / promoción / patrocinio del rediseño, por lo que G2 arroja un *residual no explicado*, no una atribución a canales específicos. Para explicar *por qué* persiste la brecha, esos ítems deben volver en la siguiente ola.
- **Mezcla de monedas** (16 reportes en USD) resuelta con un solo supuesto de tipo de cambio.
- **Preliminar:** las cifras se moverán conforme se llene la encuesta; tratar como direccionales.

---

## Implicaciones (para AMITI / advocacy)

- El mensaje a nivel de mercado ya es defendible: **una brecha ajustada de ~25% que se ensancha en niveles senior y gerenciales**, encuadrada como problema de oferta de talento (el sector pierde a las mujeres senior que menos puede darse el lujo de perder).
- Los hallazgos de origen del pipeline y de programas de liderazgo apuntan a peticiones concretas: acceso temprano a STEM para niñas (brechas de computadora en la infancia y edad del primer programa) y rendición de cuentas del empleador sobre programas formales de mujeres hacia el liderazgo.
- Antes de que esto salga al exterior, las dos prioridades son: (1) crecer más la muestra femenina, y (2) restaurar los ítems de mecanismo para poder descomponer el residual en canales de negociación, patrocinio y promoción.
