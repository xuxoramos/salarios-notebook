# Blueprint de campaña · "¿Cuánto vale tu ___?"

**SG Tech Pulse 2026 · Software Guru**
Documento guía para el equipo de comunicación. Acompaña al archivo `stat-cards-cuanto-vale.html`.

Este documento describe la estrategia, las copias listas para publicar y la especificación de diseño de cada tarjeta, para que puedan reproducir, rediseñar o extender la campaña sin depender del archivo HTML.

---

## 1. Propósito

Convertir la Encuesta de Salarios de Software Guru en una campaña de captación de respuestas. Cada pieza muestra un número llamativo del sondeo y, cuando la muestra de ese segmento es pequeña, usa esa misma debilidad como gancho: "todavía no lo sabemos con certeza, ayúdanos a confirmarlo respondiendo".

El objetivo no es solo informar, es **provocar que la gente responda la encuesta** para sentirse representada y para mover el número.

---

## 2. Concepto y estrategia

### 2.1 La técnica: dato + brecha como llamado a la acción

Cada tarjeta parte de un segmento (idioma, nube, país, región, rol, etc.) y muestra la **diferencia de sueldo** de ese segmento contra la mediana general. La gracia del método:

- Cuando el segmento tiene **muchas respuestas**, el dato es defendible y se presenta con confianza.
- Cuando el segmento tiene **pocas respuestas**, no se afirma como verdad. Se muestra el número como carnada y se pide ayuda: *"solo N personas nos lo han dicho, muy pocas para confirmarlo"*. La celda chica es justo la comunidad que queremos reclutar.

El hilo conductor es la pregunta **"¿Cuánto vale tu ___?"** (tu inglés, tu nube, tu lenguaje, tu país, tu región, tu experiencia).

### 2.2 Modelo de publicación semanal

Cada semana se publica un carrusel de **3 tarjetas**:

1. **Tarjeta 1 (fija):** Intro. Presenta la pregunta "¿Cuánto vale tu ___?".
2. **Tarjeta 2 (rotativa):** el dato de la semana. Rota entre las tarjetas de contenido.
3. **Tarjeta 3 (fija):** CTA. Invita a responder la encuesta.

Las tarjetas 1 y 3 son las mismas cada semana (se producen una sola vez). La del centro cambia. Por lo tanto:

- **Cada tarjeta de contenido nueva = una semana más de campaña.** El modelo no limita el número de tarjetas, lo amplía.
- Con las **13 tarjetas de contenido** actuales (02 a 14) hay material para **13 semanas** (un trimestre completo), una por semana.
- Recomendación opcional: dejar la tarjeta 3 (CTA) idéntica siempre, y cambiar solo la primera línea de la Intro para nombrar el tema de esa semana y evitar que se sienta repetitivo.

### 2.3 Voz y tono

- **Orgullo y reto.** El CTA es una provocación ("Demuéstralo", "Defiende tu lenguaje", "Pon tu número sobre la mesa"), no una súplica.
- **Directo y candente**, en segunda persona.
- **Español de México**, cercano pero sin caer en relleno.
- **Sin emojis** en las tarjetas. En las copias de redes son opcionales (el equipo decide).
- La honestidad convive con el orgullo: el reto va arriba, el "letra chica" con el tamaño de muestra se mantiene siempre.

### 2.4 Reglas de honestidad (obligatorias)

1. **Nunca afirmar como dato una celda con muestra chica.** Siempre acompañar de "solo N respuestas", "direccional", "muy pocas para confirmarlo" o "preséntate".
2. **Todo en dólares mensuales** (mediana), para poder comparar entre países. No mezclar monedas en una misma cifra.
3. **La cifra es carnada, no conclusión.** Si el número resulta falso cuando llegue más gente, mejor: eso es justo lo que la campaña busca corregir.
4. **Temas sensibles** (por ejemplo diáspora) se tratan con respeto y sentido de comunidad, nunca con culpa ni tono de "fuga de cerebros".

### 2.5 Secuencia sugerida (13 semanas)

Arranca con los datos más sólidos para generar confianza; deja los de muestra chica (carnada pura) para cuando ya haya tracción.

| Semana | Tarjeta central | Por qué ahí |
|---|---|---|
| 1 | 02 Inglés | dato fuerte y universal |
| 2 | 03 Empleador extranjero | fuerte, aspiracional |
| 3 | 11 Experiencia | fuerte, todos se ubican |
| 4 | 12 Modalidad (remoto) | fuerte |
| 5 | 04 Nube | tribal (AWS/Azure/GCP) |
| 6 | 05 Lenguaje | tribal, polémico |
| 7 | 13 Equity | "más allá del sueldo" |
| 8 | 07 Mapa de México | regional, sorpresa Monterrey |
| 9 | 09 Seguridad | tribal, carnada |
| 10 | 14 Certificaciones | rompe mitos |
| 11 | 10 Industria | identidad de sector |
| 12 | 08 Diáspora EE.UU. | carnada, para compartir en redes de diáspora |
| 13 | 06 Mapa de LATAM | cierre "llena el mapa" |

---

## 3. Especificación de la tarjeta (layout)

Formato base para rediseño. Las tarjetas actuales siguen esta estructura.

- **Lienzo:** 1080 × 1080 px (cuadrado de Instagram). Esquinas redondeadas 36 px.
- **Márgenes internos:** 80 px arriba/abajo, 84 px a los lados.
- **Fondo:** degradado a 150° según el tema de color.
- **Color de texto:** blanco. Cifras con tipografía de números tabulares.
- **Tipografía:** `system-ui` (San Francisco / Segoe UI / Roboto).

### Campos (de arriba hacia abajo)

| Campo | Uso | Tamaño | Peso |
|---|---|---|---|
| `kicker` | Etiqueta superior (la pregunta "¿Cuánto vale tu ___?" o "SG Tech Pulse 2026"). Mayúsculas. | 30 px | 700 |
| `stat` | La cifra estrella (ej. `2.5×`, `+77%`). | 340 px | 900 |
| `stat.sm` | Variante para cifras/textos largos (ej. `85%`, `−8%`, `≈ 0%`). | 210 px | 900 |
| `head` | Titular que explica la cifra. | 66 px | 800 |
| `sub` | Detalle o cifras de apoyo. | 40 px | 500 |
| `fine` | Letra chica: tamaño de muestra y advertencia metodológica. | 24 px | normal |
| `footer` | Barra inferior: cuenta (izq.) + CTA (der.). | 34 px | 700 |

### Temas de color (degradados)

| Tema | Colores | Usado en |
|---|---|---|
| `t-red` | #7f1d1d → #b91c1c | Lenguaje, Industria |
| `t-slate` | #0f172a → #1e3a8a | Intro, Mapa LATAM, Experiencia |
| `t-violet` | #4c1d95 → #7c3aed | Empleador, Seguridad, Certificaciones |
| `t-teal` | #134e4a → #0d9488 | Inglés, Mapa de México, Modalidad |
| `t-amber` | #78350f → #d97706 | Nube, Equity |
| `t-cta` | #111827 → #2563eb | Diáspora, CTA final |

Regla de diseño: no repetir el mismo tema en tarjetas consecutivas del carrusel.

---

## 4. Fuente de datos y método

- **Fuente:** SG Tech Pulse 2026, corte de **323 respuestas** (2026-08-04).
- **Métrica:** mediana del **salario base mensual en USD**. Si la persona reportó en USD se usa ese valor; si reportó en MXN se convierte con tipo de cambio 18.5. Se recortan valores fuera de 400 a 25,000 USD/mes.
- **Mediana general de referencia:** ~$3,514 USD/mes (n=293 con salario).
- Las cifras son **preliminares y de muestra autoseleccionada**. No representan al sector completo; representan a quien ha respondido hasta hoy.

---

## 5. Inventario de tarjetas

Para cada tarjeta: tema de color, textos exactos y la copia lista para redes (con hashtags). Las tarjetas 01 y 15 son fijas; las 02 a 14 rotan.

### 01 · Intro (fija) — `t-slate`
- **Kicker:** SG Tech Pulse 2026
- **Head:** ¿Cuánto vale tu _____?
- **Sub:** Tu lenguaje, tu nube, tu inglés, tu país. No dejes que el promedio hable por ti.
- **CTA:** El número lo pones tú

> **Copy para redes:** ¿Cuánto vale tu inglés, tu stack, tu ciudad? Estamos midiendo el sueldo tech de LATAM, y el promedio no te representa hasta que respondes. Cada semana soltamos un número nuevo. ¿Te atreves a comparar el tuyo? Responde SG Tech Pulse 2026.
> `#SGTechPulse #SoftwareGuru #SalariosTech #TechLATAM`

### 02 · Inglés — `t-teal`
- **Kicker:** ¿Cuánto vale tu inglés?
- **Cifra:** 2.5×
- **Head:** Quien usa inglés todo el día gana 2.5× lo de quien no lo usa.
- **Sub:** Mediana: $5,405 vs $2,162 USD al mes.
- **Letra chica:** Mediana bruta USD/mes, sin ajustar por experiencia. Muestra autoseleccionada (n=323).
- **CTA:** Que tu inglés cuente

> **Copy para redes:** Quien usa inglés todo el día reporta 2.5× lo de quien no lo usa: $5,405 vs $2,162 al mes (mediana, n=323). ¿Tu inglés se está pagando o te lo estás regalando? Pon tu número.
> `#SGTechPulse #Ingles #SalariosTech #TechLATAM`

### 03 · Empleador extranjero — `t-violet`
- **Kicker:** ¿Cuánto vale tu jefe extranjero?
- **Cifra:** +40%
- **Head:** Trabajar para una empresa de otro país paga ~40% más.
- **Sub:** Mediana $4,865 vs $3,486 USD al mes (empleador local).
- **Letra chica:** n=49 con empleador extranjero. Mediana bruta USD/mes. Muestra preliminar.
- **CTA:** Presume para quién trabajas

> **Copy para redes:** Trabajar para una empresa de fuera paga ~40% más: $4,865 vs $3,486 al mes. ¿Local o extranjero? Presume para quién trabajas.
> `#SGTechPulse #TrabajoRemoto #SalariosTech #TechLATAM`

### 04 · Nube — `t-amber`
- **Kicker:** ¿Cuánto vale tu nube?
- **Cifra:** +77%
- **Head:** Quien usa Google Cloud reporta 77% más que la mediana.
- **Sub:** AWS +23% · Azure −23%. GCP: $6,216 USD al mes.
- **Letra chica:** Solo 6 respuestas de Google Cloud: muy pocas para confirmarlo. Ayúdanos a saber si es real.
- **CTA:** Pon tu nube en el mapa

> **Copy para redes:** Google Cloud lidera con +77% sobre la mediana... pero solo 6 personas nos lo han dicho. AWS +23%, Azure −23%. ¿GCP de verdad paga más o es puro ruido? Ayúdanos a confirmarlo. ¿Cuál es tu nube?
> `#SGTechPulse #AWS #Azure #GoogleCloud #DevOps`

### 05 · Lenguaje — `t-red`
- **Kicker:** ¿Cuánto vale tu lenguaje?
- **Cifra:** +131%
- **Head:** El lenguaje que mejor paga en la muestra casi no tiene respuestas.
- **Sub:** Clojure lidera; Java +38%, Python −25%, JavaScript −32%.
- **Letra chica:** Solo 2 respuestas de Clojure: es un guiño, no un dato. ¿Programas en algo raro? Cuéntanos.
- **CTA:** Defiende tu lenguaje

> **Copy para redes:** El lenguaje que mejor paga en la muestra casi no tiene respuestas: Clojure +131% (n=2). Java +38%, Python −25%, y JavaScript... −32%. Sí, JS debajo del promedio. ¿Nos vas a dejar así o defiendes tu lenguaje?
> `#SGTechPulse #JavaScript #Python #Clojure #DevLATAM`

### 06 · Mapa de LATAM — `t-slate`
- **Kicker:** ¿Cuánto se gana en tu país?
- **Cifra:** 85% (`stat.sm`)
- **Head:** 85% de las respuestas son de México. El resto de LATAM casi no aparece.
- **Sub:** Colombia −32%, Perú −28%... con 2 o 3 respuestas cada uno. No alcanza para saberlo.
- **Letra chica:** 273 de 323 respuestas son de México. Tu país está en blanco hasta que respondas.
- **CTA:** Tu país te necesita

> **Copy para redes:** 85% de las respuestas son de México. Colombia, Perú, Chile: 2 o 3 cada uno. No alcanza para saber cuánto se gana en tu país. El mapa de sueldos de LATAM lo está dibujando México solo. Tu país está en blanco.
> `#SGTechPulse #TechLATAM #Colombia #Peru #Chile #Argentina`

### 07 · Mapa de México — `t-teal`
- **Kicker:** ¿Cuánto se gana en tu región?
- **Cifra:** −8% (`stat.sm`)
- **Head:** Monterrey, la meca del norte, reporta menos que CDMX.
- **Sub:** El noroeste manda (+42%); el sur reporta la mitad (−54%). El mapa no es el que crees.
- **Letra chica:** Monterrey n=29; Sur n=5, Noroeste n=8: direccional. Tu región casi no aparece hasta que respondas.
- **CTA:** Pon tu región en el mapa

> **Copy para redes:** Sorpresa: Monterrey reporta menos que CDMX (−8%). El noroeste manda (+42%) y el sur reporta la mitad (−54%). Varias regiones con un puñado de respuestas. ¿De verdad tu región gana eso? Ponla en el mapa.
> `#SGTechPulse #Monterrey #CDMX #Guadalajara #SalariosTech`

**Nota de regiones:** los sueldos se agruparon por ciudad en seis regiones. Noroeste (Tijuana, Culiacán, Hermosillo, Durango), Noreste (Monterrey, Saltillo, Torreón), Bajío (Guadalajara, Querétaro, León, Aguascalientes, SLP), Centro (CDMX, Edomex, Puebla, Toluca), Sur (Guerrero, Oaxaca, Chiapas), Sureste (Veracruz, Mérida, Cancún). "Sureste" cubre lo que a veces se llama sur/sureste.

### 08 · Diáspora en EE.UU. — `t-cta`
- **Kicker:** ¿Y los que ya cruzaron?
- **Cifra:** 3×
- **Head:** Los que trabajan desde Estados Unidos reportan el triple. Pero solo 9 nos han contado.
- **Sub:** ¿Estás en la bahía o en un tech gringo? Tu número es la brújula de quien sueña con llegar.
- **Letra chica:** n=9 residentes en EE.UU. ($10,000/mes mediana). Muy pocos para un dato. Preséntate.
- **CTA:** Ilumina el camino

> **Copy para redes:** Los que ya cruzaron reportan 3×: $10,000 al mes de mediana. Pero solo 9 nos han contado. Si estás en la bahía o en un tech gringo, tu número es la brújula de quien sueña con llegar. Preséntate.
> `#SGTechPulse #LatinosInTech #SiliconValley #TechLATAM`

**Nota de distribución:** esta tarjeta está pensada para compartirse en redes de diáspora (Latinx in Tech, Techqueria, grupos de empresa), no solo en el feed de Software Guru.

### 09 · Seguridad — `t-violet`
- **Kicker:** ¿Cuánto vale tu rol?
- **Cifra:** 2×
- **Head:** Seguridad/InfoSec reporta el doble de la mediana.
- **Sub:** $7,027 USD al mes vs $3,514 de la mediana general.
- **Letra chica:** Solo 7 respuestas en seguridad: muy pocas para asegurarlo. ¿Trabajas en seguridad? Cuéntanos.
- **CTA:** Demuéstralo

> **Copy para redes:** Seguridad/InfoSec reporta el doble de la mediana: $7,027 al mes. Con 7 respuestas es un indicio, no un veredicto. ¿Trabajas en seguridad? Demuéstralo.
> `#SGTechPulse #InfoSec #Ciberseguridad #SalariosTech`

### 10 · Industria — `t-red`
- **Kicker:** ¿Cuánto vale tu industria?
- **Cifra:** −53%
- **Head:** Quien trabaja en gobierno reporta 53% menos que la mediana.
- **Sub:** $1,649 vs $3,514 USD al mes. Ecommerce, en cambio, +69%.
- **Letra chica:** n=8 en gobierno. Direccional. ¿Tú en qué industria estás?
- **CTA:** Suma tu industria

> **Copy para redes:** Gobierno reporta 53% menos que la mediana ($1,649). Ecommerce, al revés, +69%. ¿Tu industria te paga lo que vales o te ancla? Suma la tuya.
> `#SGTechPulse #Fintech #Gobierno #SalariosTech`

### 11 · Experiencia — `t-slate`
- **Kicker:** ¿Cuánto vale tu experiencia?
- **Cifra:** 4×
- **Head:** Con 11+ años se reporta casi 4× lo del que empieza.
- **Sub:** 0-2 años $1,135 · 3-5 $2,162 · 6-10 $3,649 · 11+ $4,432 al mes.
- **Letra chica:** Mediana USD/mes (n=290). Los primeros años son los más baratos.
- **CTA:** Pon tus años sobre la mesa

> **Copy para redes:** Con 11+ años se reporta casi 4× lo del que empieza: $4,432 vs $1,135 al mes. Los primeros años son los más baratos, y nadie te lo dice. ¿En qué tramo vas? Pon tus años sobre la mesa.
> `#SGTechPulse #CarreraTech #SalariosTech #TechLATAM`

### 12 · Modalidad — `t-teal`
- **Kicker:** ¿Cuánto vale trabajar remoto?
- **Cifra:** +56%
- **Head:** El remoto total paga 56% más que el presencial.
- **Sub:** Remoto $3,784 vs presencial $2,432 al mes. El híbrido queda en medio.
- **Letra chica:** Mediana USD/mes. Remoto n=133, presencial n=43. Muestra preliminar.
- **CTA:** Presume tu modalidad

> **Copy para redes:** El remoto total paga 56% más que el presencial: $3,784 vs $2,432 al mes. ¿Te están pagando la oficina? Presume tu modalidad.
> `#SGTechPulse #TrabajoRemoto #RemoteWork #SalariosTech`

### 13 · Equity — `t-amber`
- **Kicker:** ¿Cuánto vale más allá del sueldo?
- **Cifra:** +68%
- **Head:** Quien recibe acciones reporta 68% más que la mediana.
- **Sub:** Con equity $5,892 vs $3,243 sin equity. Solo 1 de cada 5 lo recibe.
- **Letra chica:** n=61 con acciones/RSU. Mediana de salario base USD/mes; el equity va aparte.
- **CTA:** ¿Te toca del pastel?

> **Copy para redes:** Quien recibe acciones reporta 68% más que la mediana ($5,892 vs $3,243), y solo 1 de cada 5 lo recibe. El sueldo base es solo una parte. ¿A ti te toca del pastel?
> `#SGTechPulse #Equity #Startups #SalariosTech`

### 14 · Certificaciones — `t-violet`
- **Kicker:** ¿Tu certificación se paga sola?
- **Cifra:** ≈ 0% (`stat.sm`)
- **Head:** En la muestra, tener certificación no mueve la aguja.
- **Sub:** Con cert $3,459 vs sin cert $3,674 al mes. Casi lo mismo.
- **Letra chica:** n=147 vs 146. ¿Tu certificación te subió el sueldo? Demuéstranos que sí.
- **CTA:** Demuéstranos que sí

> **Copy para redes:** ¿La certificación se paga sola? En la muestra, no: con cert $3,459 vs sin cert $3,674 al mes, casi lo mismo. ¿A ti la certificación te subió el sueldo? Demuéstranos que sí.
> `#SGTechPulse #Certificaciones #AWS #Scrum #SalariosTech`

### 15 · Llamado a la acción (fija) — `t-cta`
- **Kicker:** SG Tech Pulse 2026
- **Head:** No dejes que el promedio hable por ti.
- **Sub:** Si trabajas en tecnología en cualquier país de LATAM, responde SG Tech Pulse 2026 y pon tu número sobre la mesa.
- **CTA:** Link en bio

> **Copy para redes:** No dejes que el promedio hable por ti. Si trabajas en tecnología en cualquier país de LATAM, tu respuesta mueve cada número que publicamos. 5 minutos, anónimo, el mapa lo armamos entre todos. Responde SG Tech Pulse 2026.
> `#SGTechPulse #SoftwareGuru #SalariosTech #TechLATAM`

---

## 6. Qué falta y cómo crece

- **Frameworks:** la encuesta 2026 no capturó el framework principal (solo si el stack cambió en 18 meses). Para tener una tarjeta de frameworks en la próxima ola, hay que **agregar la pregunta** al cuestionario.
- **Más ángulos disponibles** para extender la campaña más allá de 13 semanas: premium por rol (frontend/backend/data), remuneración total vs base, tasa de ahorro / costo de vida, neurodivergencia (con trato respetuoso), segundo idioma, y profundizar por país conforme lleguen respuestas.
- **Cada corte nuevo de datos** actualiza las cifras. Antes de reusar una tarjeta en una ola posterior, recalcular su número.

---

## 7. Archivos

- `stat-cards-cuanto-vale.html`: las 15 tarjetas listas para capturar (1080×1080) o exportar a PDF. Debajo de cada tarjeta trae su copia de redes (se oculta al imprimir).
- `blueprint-cuanto-vale.md`: este documento.
