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
- Con las **16 tarjetas de contenido** actuales (02 a 17) hay material para **16 semanas** (un trimestre completo y tres semanas más), una por semana.
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

### 2.5 Secuencia sugerida (16 semanas)

Arranca con los datos más sólidos para generar confianza; deja los de muestra chica (carnada pura) para cuando ya haya tracción. El bloque de IA (semanas 13-15) se agrupa a propósito, ya entrada la campaña, como un segundo arranque temático antes del cierre.

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
| 13 | 16 Vibe coding | novedoso, muy compartible, dato sólido (n=232) |
| 14 | 15 Rol en IA | prima de rol, refuerza el ángulo de carrera (n=36) |
| 15 | 17 Roles 100% IA | carnada pura, mercado emergente (n=73) |
| 16 | 06 Mapa de LATAM | cierre "llena el mapa" |

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
| `stat` | La cifra estrella (ej. `2.2×`, `+64%`). | 340 px | 900 |
| `stat.sm` | Variante para cifras/textos largos (ej. `90%`, `−25%`, `+11%`). | 210 px | 900 |
| `head` | Titular que explica la cifra. | 66 px | 800 |
| `sub` | Detalle o cifras de apoyo. | 40 px | 500 |
| `fine` | Letra chica: tamaño de muestra y advertencia metodológica. | 24 px | normal |
| `footer` | Barra inferior: cuenta (izq.) + CTA (der.). | 34 px | 700 |

### Temas de color (degradados)

| Tema | Colores | Usado en |
|---|---|---|
| `t-red` | #7f1d1d → #b91c1c | Lenguaje, Industria |
| `t-slate` | #0f172a → #1e3a8a | Intro, Mapa LATAM, Experiencia, Roles 100% IA |
| `t-violet` | #4c1d95 → #7c3aed | Empleador, Seguridad, Certificaciones, Rol en IA |
| `t-teal` | #134e4a → #0d9488 | Inglés, Mapa de México, Modalidad |
| `t-amber` | #78350f → #d97706 | Nube, Equity, Vibe coding |
| `t-cta` | #111827 → #2563eb | Diáspora, CTA final |

Regla de diseño: no repetir el mismo tema en tarjetas consecutivas del carrusel.

---

## 4. Fuente de datos y método

- **Fuente:** SG Tech Pulse 2026, corte de **787 respuestas** (19 de noviembre de 2026). 712 son de residentes en México (90%).
- **Población:** las tarjetas de segmento (02 a 05, 07 y 10 a 14) usan solo a **residentes en México** con salario reportado (n=642). La tarjeta 06 (Mapa de LATAM) cuenta respuestas de toda la muestra (712 de 787).
- **Métrica:** mediana del **salario base mensual**. Quien reportó en USD se convierte a MXN con tipo de cambio 18.5. La mediana en MXN se divide entre 18.5 para mostrarla en USD/mes. Se descartan salarios fuera de un rango aproximado de 8,000 a 400,000 pesos al mes.
- **Mediana de referencia:** $3,243 USD/mes ($60,000 MXN a TC 18.5, residentes en México con salario, n=642). La mediana de la muestra completa también es $60,000 MXN. En el corte anterior era ~$3,445.
- **Excepciones de población:**
  - Tarjetas 09 (Seguridad) y 15 (Rol en IA): mediana del rol en la **muestra completa**, comparada contra la mediana de México.
  - Tarjeta 08 (Diáspora): residentes en Estados Unidos (n=26, 16 con sueldo reportado). Mediana $11,500 USD/mes.
  - Tarjetas 16 y 17 (bloque de IA): **muestra completa** (`docs/GENERAL_FINDINGS_2026.md`, 2026-11-19).
- Los porcentajes se calculan sobre quienes respondieron cada pregunta. La adopción de agentes (tarjeta 16) se calcula sobre quienes respondieron la pregunta de generación de código (117 de 232), no sobre las 787. El equity (tarjeta 13) lo recibe 18% de los residentes en México que respondieron esa pregunta (n=623).
- Las cifras son **preliminares y de muestra autoseleccionada**. No representan al sector completo. Representan a quien ha respondido hasta hoy.

---

## 5. Inventario de tarjetas

Para cada tarjeta: tema de color, textos exactos y la copia lista para redes (con hashtags). Las tarjetas 01 y 18 son fijas; las 02 a 17 rotan.

### 01 · Intro (fija) — `t-slate`
- **Kicker:** SG Tech Pulse 2026
- **Head:** ¿Cuánto vale tu _____?
- **Sub:** Tu lenguaje, tu nube, tu inglés, tu país. No dejes que el promedio hable por ti.
- **CTA:** El número lo pones tú

> **Copy para redes:** ¿Cuánto vale tu inglés, tu stack, tu ciudad? Estamos midiendo el sueldo tech de LATAM, y el promedio no te representa hasta que respondes. Cada semana soltamos un número nuevo. ¿Te atreves a comparar el tuyo? Responde SG Tech Pulse 2026.
> `#SGTechPulse #SoftwareGuru #SalariosTech #TechLATAM`

### 02 · Inglés — `t-teal`
- **Kicker:** ¿Cuánto vale tu inglés?
- **Cifra:** 2.2×
- **Head:** Quien usa inglés todo el día gana 2.2× lo de quien no lo usa.
- **Sub:** Mediana: $4,324 vs $1,978 USD al mes.
- **Letra chica:** Mediana bruta USD/mes, residentes en México, sin ajustar por experiencia. Todo el tiempo n=160, nunca n=47. Muestra autoseleccionada.
- **CTA:** Que tu inglés cuente

> **Copy para redes:** Quien usa inglés todo el día reporta 2.2× lo de quien no lo usa: $4,324 vs $1,978 al mes (mediana, residentes en México). ¿Tu inglés se está pagando o te lo estás regalando? Pon tu número.
> `#SGTechPulse #Ingles #SalariosTech #TechLATAM`

### 03 · Empleador extranjero — `t-violet`
- **Kicker:** ¿Cuánto vale tu jefe extranjero?
- **Cifra:** +42%
- **Head:** Trabajar para una empresa de otro país paga ~42% más.
- **Sub:** Mediana $4,595 vs $3,243 USD al mes (empleador local).
- **Letra chica:** n=86 con empleador extranjero, residentes en México. Mediana bruta USD/mes. Muestra preliminar.
- **CTA:** Presume para quién trabajas

> **Copy para redes:** Trabajar para una empresa de fuera paga ~42% más: $4,595 vs $3,243 al mes. ¿Local o extranjero? Presume para quién trabajas.
> `#SGTechPulse #TrabajoRemoto #SalariosTech #TechLATAM`

### 04 · Nube — `t-amber`
- **Kicker:** ¿Cuánto vale tu nube?
- **Cifra:** +33%
- **Head:** Quien usa AWS reporta 33% más que la mediana.
- **Sub:** Google Cloud +25% · Azure +15%. AWS: $4,324 USD al mes.
- **Letra chica:** AWS n=95, Azure n=62. Google Cloud tiene solo 15 respuestas, muy pocas para ubicarlo bien. Ayúdanos a confirmarlo.
- **CTA:** Pon tu nube en el mapa

> **Copy para redes:** AWS lidera con +33% sobre la mediana: $4,324 al mes (n=95). Google Cloud marca +25%, pero solo 15 personas nos lo han dicho. Azure queda en +15%. ¿GCP paga más o menos de lo que parece? Ayúdanos a confirmarlo. ¿Cuál es tu nube?
> `#SGTechPulse #AWS #Azure #GoogleCloud #DevOps`

### 05 · Lenguaje — `t-red`
- **Kicker:** ¿Cuánto vale tu lenguaje?
- **Cifra:** +92%
- **Head:** El lenguaje que mejor paga en la muestra casi no tiene respuestas.
- **Sub:** Ruby lidera. Java +42%, Python +8%, JavaScript −17%.
- **Letra chica:** Solo 6 respuestas de Ruby: es un guiño, no un dato. ¿Programas en algo raro? Cuéntanos.
- **CTA:** Defiende tu lenguaje

> **Copy para redes:** El lenguaje que mejor paga en la muestra casi no tiene respuestas: Ruby +92% (n=6). Java +42%, Python +8%, y JavaScript... −17%. Sí, JS debajo de la mediana. ¿Nos vas a dejar así o defiendes tu lenguaje?
> `#SGTechPulse #JavaScript #Python #Ruby #DevLATAM`

### 06 · Mapa de LATAM — `t-slate`
- **Kicker:** ¿Cuánto se gana en tu país?
- **Cifra:** 90% (`stat.sm`)
- **Head:** 90% de las respuestas son de México. El resto de LATAM casi no aparece.
- **Sub:** Colombia −7% y Argentina −20%, con apenas 9 y 8 salarios reportados. No alcanza para saberlo.
- **Letra chica:** 712 de 787 respuestas son de México. Tu país está en blanco hasta que respondas.
- **CTA:** Tu país te necesita

> **Copy para redes:** 90% de las respuestas son de México. Colombia y Argentina: 12 y 11 respuestas. El resto, un puñado. No alcanza para saber cuánto se gana en tu país. El mapa de sueldos de LATAM lo está dibujando México solo. Tu país está en blanco.
> `#SGTechPulse #TechLATAM #Colombia #Peru #Chile #Argentina`

### 07 · Mapa de México — `t-teal`
- **Kicker:** ¿Cuánto se gana en tu región?
- **Cifra:** −25% (`stat.sm`)
- **Head:** Monterrey, la meca del norte, reporta 25% menos que la mediana.
- **Sub:** CDMX manda (+26%). Aguascalientes sorprende (+12%). Monterrey se queda atrás (−25%). El mapa no es el que crees.
- **Letra chica:** CDMX n=224, Monterrey n=95, Aguascalientes n=22: direccional. Tu ciudad casi no aparece hasta que respondas.
- **CTA:** Pon tu ciudad en el mapa

> **Copy para redes:** Sorpresa: Monterrey reporta 25% menos que la mediana, mientras CDMX manda con +26% y Aguascalientes sorprende con +12%. ¿De verdad tu ciudad gana eso? Ponla en el mapa.
> `#SGTechPulse #Monterrey #CDMX #Guadalajara #SalariosTech`

**Nota de regiones:** los sueldos se agruparon por ciudad en seis regiones. Noroeste (Tijuana, Culiacán, Hermosillo, Durango), Noreste (Monterrey, Saltillo, Torreón), Bajío (Guadalajara, Querétaro, León, Aguascalientes, SLP), Centro (CDMX, Edomex, Puebla, Toluca), Sur (Guerrero, Oaxaca, Chiapas), Sureste (Veracruz, Mérida, Cancún). "Sureste" cubre lo que a veces se llama sur/sureste.

### 08 · Diáspora en EE.UU. — `t-cta`
- **Kicker:** ¿Y los que ya cruzaron?
- **Cifra:** 3.5×
- **Head:** Los que trabajan desde Estados Unidos reportan 3.5× la mediana. Pero solo 26 nos han contado.
- **Sub:** ¿Estás en la bahía o en un tech gringo? Tu número es la brújula de quien sueña con llegar.
- **Letra chica:** n=26 residentes en EE.UU., 16 con sueldo reportado. Mediana $11,500/mes vs $3,243 en México. Muy pocos para un dato. Preséntate.
- **CTA:** Ilumina el camino

> **Copy para redes:** Los que ya cruzaron reportan 3.5× la mediana de México: $11,500 al mes contra $3,243. Pero solo 26 nos han contado. Si estás en la bahía o en un tech gringo, tu número es la brújula de quien sueña con llegar. Preséntate.
> `#SGTechPulse #LatinosInTech #SiliconValley #TechLATAM`

**Nota de distribución:** esta tarjeta está pensada para compartirse en redes de diáspora (Latinx in Tech, Techqueria, grupos de empresa), no solo en el feed de Software Guru.

### 09 · Seguridad — `t-violet`
- **Kicker:** ¿Cuánto vale tu rol?
- **Cifra:** 1.5×
- **Head:** Seguridad/InfoSec reporta 1.5× la mediana. Empata con liderazgo ejecutivo.
- **Sub:** $4,973 USD al mes vs $3,243 de la mediana general.
- **Letra chica:** Solo 15 respuestas en seguridad: muy pocas para asegurarlo. ¿Trabajas en seguridad? Cuéntanos.
- **CTA:** Demuéstralo

> **Copy para redes:** Seguridad/InfoSec reporta 1.5× la mediana: $4,973 al mes. Es lo mismo que reporta liderazgo ejecutivo. Con 15 respuestas es un indicio, no un veredicto. ¿Trabajas en seguridad? Demuéstralo.
> `#SGTechPulse #InfoSec #Ciberseguridad #SalariosTech`

### 10 · Industria — `t-red`
- **Kicker:** ¿Cuánto vale tu industria?
- **Cifra:** −38%
- **Head:** Quien trabaja en gobierno reporta 38% menos que la mediana.
- **Sub:** $2,027 vs $3,243 USD al mes. Alimentos, en cambio, +36%.
- **Letra chica:** n=14 en gobierno y 14 en alimentos. Direccional. ¿Tú en qué industria estás?
- **CTA:** Suma tu industria

> **Copy para redes:** Gobierno reporta 38% menos que la mediana ($2,027). Alimentos, al revés, +36%. ¿Tu industria te paga lo que vales o te ancla? Suma la tuya.
> `#SGTechPulse #Fintech #Gobierno #SalariosTech`

### 11 · Experiencia — `t-slate`
- **Kicker:** ¿Cuánto vale tu experiencia?
- **Cifra:** 3.1×
- **Head:** Con 11+ años se reporta más de 3× lo del que empieza.
- **Sub:** 0-2 años $1,378 · 3-5 $2,162 · 6-10 $3,243 · 11+ $4,324 al mes.
- **Letra chica:** Mediana USD/mes, residentes en México (n=638). Los primeros años son los más baratos.
- **CTA:** Pon tus años sobre la mesa

> **Copy para redes:** Con 11+ años se reporta más de 3× lo del que empieza: $4,324 vs $1,378 al mes. Los primeros años son los más baratos, y nadie te lo dice. ¿En qué tramo vas? Pon tus años sobre la mesa.
> `#SGTechPulse #CarreraTech #SalariosTech #TechLATAM`

### 12 · Modalidad — `t-teal`
- **Kicker:** ¿Cuánto vale trabajar remoto?
- **Cifra:** +75%
- **Head:** El remoto total paga 75% más que el presencial.
- **Sub:** Remoto $3,784 vs presencial $2,162 al mes. El híbrido queda en medio.
- **Letra chica:** Mediana USD/mes, residentes en México. Remoto n=267, presencial n=110. Muestra preliminar.
- **CTA:** Presume tu modalidad

> **Copy para redes:** El remoto total paga 75% más que el presencial: $3,784 vs $2,162 al mes. ¿Te están pagando la oficina? Presume tu modalidad.
> `#SGTechPulse #TrabajoRemoto #RemoteWork #SalariosTech`

### 13 · Equity — `t-amber`
- **Kicker:** ¿Cuánto vale más allá del sueldo?
- **Cifra:** +64%
- **Head:** Quien recibe acciones reporta 64% más que quien no las recibe.
- **Sub:** Con equity $5,135 vs $3,135 sin equity. Casi 1 de cada 5 lo recibe.
- **Letra chica:** n=109 con acciones/RSU, residentes en México. Lo recibe 18% de quienes respondieron. Mediana de salario base USD/mes. El equity va aparte.
- **CTA:** ¿Te toca del pastel?

> **Copy para redes:** Quien recibe acciones reporta 64% más que quien no ($5,135 vs $3,135), y casi 1 de cada 5 lo recibe. El sueldo base es solo una parte. ¿A ti te toca del pastel?
> `#SGTechPulse #Equity #Startups #SalariosTech`

### 14 · Certificaciones — `t-violet`
- **Kicker:** ¿Tu certificación se paga sola?
- **Cifra:** +11% (`stat.sm`)
- **Head:** En la muestra, quien tiene certificación reporta 11% más.
- **Sub:** Con cert $3,486 vs sin cert $3,135 al mes. Una diferencia pequeña.
- **Letra chica:** n=324 vs 318, residentes en México. ¿Tu certificación te subió el sueldo? Demuéstranos que sí.
- **CTA:** Demuéstranos que sí

> **Copy para redes:** ¿La certificación se paga sola? En la muestra, un poco: con cert $3,486 vs sin cert $3,135 al mes, 11% más. ¿A ti la certificación te subió el sueldo? Demuéstranos que sí.
> `#SGTechPulse #Certificaciones #AWS #Scrum #SalariosTech`

### 15 · Rol en IA — `t-violet`
- **Kicker:** ¿Cuánto vale tu rol en IA?
- **Cifra:** +28%
- **Head:** Ciencia de datos / IA reporta 28% más que la mediana.
- **Sub:** Mediana $4,141 vs $3,243 USD al mes (mediana general).
- **Letra chica:** n=36 en ciencia de datos/IA. Cifra MXN convertida a USD (TC 18.5). Muestra preliminar.
- **CTA:** Defiende tu rol en IA

> **Copy para redes:** Ciencia de datos / IA reporta 28% más que la mediana general: ~$4,141 vs ~$3,243 al mes. Todavía es muestra chica (n=36), pero apunta hacia dónde se mueve el dinero. ¿Ya trabajas en IA? Pon tu número.
> `#SGTechPulse #IA #DataScience #SalariosTech`

### 16 · Vibe coding — `t-amber`
- **Kicker:** ¿Todavía programas a mano?
- **Cifra:** 50%
- **Head:** Instruye a agentes de IA y ya casi no programa a mano.
- **Sub:** 29% programa a mano con apoyo de IA · 19% la usa solo de vez en cuando.
- **Letra chica:** 117 de 232 que respondieron la pregunta de generación de código. La encuesta sigue abierta.
- **CTA:** Cuéntanos cómo programas

> **Copy para redes:** La forma de programar ya cambió: la mitad de quienes nos contaron cómo programan ya casi no lo hace a mano. Instruye a agentes de IA y revisa el resultado (117 de 232). ¿Tú todavía picas código línea por línea o ya le hablas a la IA?
> `#SGTechPulse #VibeCoding #IA #DevLATAM`

### 17 · Roles 100% IA — `t-slate`
- **Kicker:** ¿Ya tienes un rol 100% IA?
- **Cifra:** 73 (`stat.sm`)
- **Head:** 73 personas ya tienen un puesto enfocado 100% en IA.
- **Sub:** GenAI/LLM engineer, AI product manager, prompt manager: los nuevos títulos del sector.
- **Letra chica:** 73 de 787 respuestas. Rol abierto, no una lista cerrada. Mercado apenas naciendo.
- **CTA:** Preséntate

> **Copy para redes:** Ya son 73 las personas con un puesto 100% enfocado en IA: GenAI/LLM engineer, AI product manager, prompt manager, ML engineer. El mercado apenas se está formando. Si tu rol ya es así, cuéntanos y ayúdanos a dibujar el mapa.
> `#SGTechPulse #IA #CarrerasIA #TechLATAM`

### 18 · Llamado a la acción (fija) — `t-cta`
- **Kicker:** SG Tech Pulse 2026
- **Head:** No dejes que el promedio hable por ti.
- **Sub:** Si trabajas en tecnología en cualquier país de LATAM, responde SG Tech Pulse 2026 y pon tu número sobre la mesa.
- **CTA:** Link en bio

> **Copy para redes:** No dejes que el promedio hable por ti. Si trabajas en tecnología en cualquier país de LATAM, tu respuesta mueve cada número que publicamos. 5 minutos, anónimo, el mapa lo armamos entre todos. Responde SG Tech Pulse 2026.
> `#SGTechPulse #SoftwareGuru #SalariosTech #TechLATAM`

---

## 6. Qué falta y cómo crece

- **Frameworks:** la encuesta 2026 no capturó el framework principal (solo si el stack cambió en 18 meses). Para tener una tarjeta de frameworks en la próxima ola, hay que **agregar la pregunta** al cuestionario.
- **Más ángulos disponibles** para extender la campaña más allá de 16 semanas: premium por rol (frontend/backend/data), remuneración total vs base, tasa de ahorro / costo de vida, neurodivergencia (con trato respetuoso), segundo idioma, y profundizar por país conforme lleguen respuestas.
- **IA todavía tiene tela de dónde cortar:** confianza en que las habilidades sigan siendo relevantes en 3 años (3.3/5 promedio, sin explotar en tarjeta), corte de vibe coding por seniority o rol, y seguir recalculando el bloque de IA (15-17) contra cada corte nuevo conforme siga creciendo la muestra (hoy 787 respuestas).
- **Cada corte nuevo de datos** actualiza las cifras. Antes de reusar una tarjeta en una ola posterior, recalcular su número.

---

## 7. Archivos

- `stat-cards-cuanto-vale.html`: las 18 tarjetas listas para capturar (1080×1080) o exportar a PDF. Debajo de cada tarjeta trae su copia de redes (se oculta al imprimir).
- `blueprint-cuanto-vale.md`: este documento.
