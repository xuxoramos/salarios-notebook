# Rediseño de la Encuesta de Salarios 2026

## Contexto

Software Guru publica dos productos de encuesta dirigidos al mercado laboral de TI en México (y cada vez más en América Latina):

1. **Best Place to Code (BP2C):** Encuesta de satisfacción del empleador que funciona como programa de certificación. Pregunta a los empleados sobre el *comportamiento de su empleador* — cultura, beneficios, habilitación, justicia. En 2026 se relanza con un instrumento rediseñado de 45 preguntas organizado alrededor de seis palancas independientes (Fundamentos del Empleador, Habilitación de IA, Gestión de Tecnoansiedad, Justicia Algorítmica, Agencia del Empleado, Confianza en el Futuro).

2. **Encuesta de Salarios:** Encuesta individual de profesionales de TI que captura demografía, compensación, habilidades y arreglos de trabajo. Ha operado al menos desde 2020, recolectando ~5,798 respuestas útiles entre 2020–2022. El producto analítico principal ha sido un modelo causal que explica el salario mensual bruto (salarymx) con 42 predictores, con R²=38.74%.

Ambas encuestas históricamente se han diseñado de forma independiente, lo que genera **traslapes temáticos** (beneficios, trabajo remoto, tipo de organización) y **límites editoriales ambiguos**. El rediseño de BP2C crea una oportunidad para rediseñar la Encuesta de Salarios de forma que ambos instrumentos se complementen en lugar de competir.

Este documento detalla la justificación y la implementación de tres objetivos:

| # | Objetivo | Qué significa |
|---|---|---|
| 1 | **Separación de producto** | La Encuesta de Salarios y BP2C deben ser instrumentos claramente distintos sin duplicación estructural. |
| 2 | **Impacto en política pública** | La Encuesta de Salarios debe producir hallazgos accionables para gobiernos, universidades y asociaciones de industria. |
| 3 | **Gancho comercial para BP2C** | La Encuesta de Salarios debe crear demanda natural de la certificación BP2C sin canibalizarla. |

### Principio de Separación

La regla de diseño que rige los tres objetivos:

```
Encuesta de Salarios = Radiografía del MERCADO   (oferta, estructura, precios, riesgos)
BP2C                = Radiografía del EMPLEADOR (cultura, habilitación, justicia, agencia)
```

Cualquier tema (IA, trabajo remoto, compensación) puede aparecer en ambas encuestas **solo si el lente es distinto**: la Encuesta de Salarios pregunta al individuo por su *posición en el mercado*; BP2C pregunta al individuo por el *comportamiento de su empleador*. La separación es por **unidad de análisis y perspectiva**, no por tema.

---

## Objetivo 1: Separación de Producto

### 1.1 Justificación

Cuando ambas encuestas preguntan lo mismo desde la misma perspectiva, se generan:
- Confusión en personas que contestan ambas ("¿No acabo de responder esto?")
- Dilución de la marca de cada producto ("¿Cuál es la diferencia?")
- Datos conflictivos difíciles de conciliar en reportes publicados

El rediseño de BP2C ya acotó su alcance a seis palancas sustentadas en teoría sobre el comportamiento del empleador. La Encuesta de Salarios debe ahora corresponder depurando todo lo que mide calidad del empleador y concentrándose en estructura de mercado.

### 1.2 Preguntas a Eliminar de la Encuesta de Salarios

#### 1.2.1 Bloque de Beneficios (18 ítems selección múltiple)

**Ítems actuales:** equity, auto, apoyo familiar, educación, bono, vivienda, estacionamiento, gasolina, gimnasio, horarios flexibles, home office, préstamos, seguros de salud (mayor/menor), seguro de vida, cafetería, celular, vales.

**Por qué eliminar:** Cada uno describe un *beneficio provisto por el empleador*. Son atributos del empleador, no señales del mercado laboral. La palanca de Fundamentos del Empleador de BP2C (14 preguntas, Teoría de Dos Factores de Herzberg) ya cubre este territorio con ítems psicométricamente validados diseñados para validez discriminante.

**Qué perdemos:** Capacidad de correlacionar beneficios específicos con salario. Es una pérdida aceptable porque:
- En el análisis causal 2020–2022, los beneficios individuales no se incluyeron como predictores (no estaban en el modelo de 42 predictores).
- Los beneficios se correlacionan fuertemente con tipo de organización y seniority, por lo que son proxies confundidos y no impulsores causales.
- El vínculo entre encuestas (Objetivo 3) recupera este análisis: podemos correlacionar los puntajes de BP2C por empleador con la compensación de la encuesta de salarios mediante la identidad del empleador.

**Implementación:**
- Eliminar todas las columnas `ben_*` del instrumento.
- Archivar los datos históricos de beneficios en los archivos de respuestas existentes (no borrar de los CSV 2020–2022).
- En el reporte publicado, indicar: *"Para análisis de beneficios a nivel empleador, ver el reporte de certificación Best Place to Code."*

#### 1.2.2 Apoyo del Empleador en COVID (`covid_apoyo`)

**Ítems actuales:** computadora, muebles, internet (selección múltiple sobre si el empleador proporcionó equipo/apoyo durante COVID).

**Por qué eliminar:** Pregunta "¿tu empleador hizo X?" — eso es comportamiento del empleador, no estructura de mercado. Además, en 2026 el encuadre COVID es obsoleto.

**Qué hacer con la señal subyacente:** La señal interesante no es "¿te dieron escritorio?" sino "¿cuál es tu arreglo de trabajo y quién paga la infraestructura?" Eso se reencuadra como pregunta de estructura de mercado (ver Sección 2.3 abajo).

**Implementación:**
- Eliminar `covid_apoyo` del instrumento.
- Conservar `covid_remoto` (remoto/onsite/híbrido) pero renombrarlo con un encuadre no-COVID — se convierte en la pregunta estándar `work_arrangement`.
- Eliminar `covid_salario` y `covid_carga` (específicas de pandemia, ya no relevantes).

#### 1.2.3 Resumen de Eliminaciones

| Bloque | Ítems eliminados | Ubicación de reemplazo |
|-------|--------------|---------------------|
| Beneficios (`ben_*`) | 18 ítems | Fundamentos del Empleador en BP2C |
| Apoyo COVID del empleador | 3 ítems | Reencuadrado como estructura de mercado (Sec 2.3) |
| Impacto COVID en salario | 1 ítem | Eliminado (obsoleto) |
| Impacto COVID en carga de trabajo | 1 ítem | Eliminado (obsoleto) |
| **Total** | **23 ítems eliminados** | |

### 1.3 Preguntas a Conservar y Reencuadrar

#### 1.3.1 Trabajo Remoto → Arreglo de Trabajo

**Actual:** `remote` (Y/N), `covid_remoto` (remoto/onsite/semipresencial)

**Problema:** El binario Y/N es demasiado grueso, y `covid_remoto` enmarca esto como respuesta a pandemia, no como rasgo estructural.

**Rediseño:** Una sola pregunta `work_arrangement` con opciones:
- Totalmente remoto
- Híbrido (1–3 días en oficina/semana)
- Totalmente presencial
- Nómada / independiente de ubicación

**Por qué este encuadre:** El trabajo remoto ya no es un beneficio del empleador (eso es BP2C) — es una *característica estructural del mercado* que afecta niveles salariales, arbitraje geográfico y dinámicas transfronterizas. El modelo causal encontró +$12,213 MXN/mes para quienes trabajan remoto; el rediseño preserva este análisis y actualiza el encuadre.

#### 1.3.2 Tipo de Empleo (`emptype`)

**Actual:** nómina, honorarios, freelance, híbrido, emprendedor, becario, estudiante

**Por qué conservar:** La formalidad laboral es una variable de *estructura de mercado*, no un atributo del empleador. Estar en nómina vs. honorarios determina acceso a seguridad social, tratamiento fiscal y protecciones legales. BP2C no preguntaría esto — certifica empleadores que (en teoría) ya son formales.

**Rediseño:** Conservar tal cual, pero enriquecer con dos preguntas complementarias (ver Sección 2.2).

#### 1.3.3 Tipo de Organización (`orgtype`)

**Actual:** corp, startup, isv, itservices, freelance, gobierno, uni

**Por qué conservar:** Describe el *tipo de mercado en el que opera la persona*, no la calidad del empleador. Es una variable de segmentación de mercado.

**Rediseño:** Actualizaciones menores para reflejar el mercado 2026:
- Agregar: `ai_native` (empresas cuyo producto principal es IA/ML)
- Renombrar: `isv` → `product_company` (etiqueta más clara)
- Mantener el resto.

### 1.4 Naming y Branding

El nombre "Encuesta de Salarios" es descriptivamente correcto pero posiciona el producto muy estrecho. Una encuesta de salarios sugiere que aprenderás cuánto ganan las personas. Un *reporte de inteligencia de mercado* sugiere que entenderás cómo funciona el mercado.

**Nombres candidatos:**
- **Radiografía del Talento Tech** — señala profundidad de análisis
- **Pulso Tech LATAM** — sugiere alcance regional y vigencia
- **Encuesta de Mercado Laboral Tech** — el más descriptivo

**Recomendación:** Elegir el nombre *después* de decidir el alcance geográfico (Sección 2.8), ya que el alcance afecta el branding. Por ahora, continuar con "Encuesta de Salarios" como título de trabajo.

### 1.5 Mejoras a Preguntas Retenidas

Varias preguntas retenidas tienen debilidades analíticas que se acumulan en ruido de medición y desperdicio de espacio. Estos cambios afectan campos existentes, no bloques nuevos.

#### 1.5.1 Compensación: Desambiguación

**Problema:** `salarymx` pregunta "salario mensual bruto" sin especificar si incluye bonos prorrateados, compensación variable o equity. Distintas personas lo interpretan de forma distinta, introduciendo ruido en la variable más importante.

**Campos actuales eliminados o reemplazados:**
- `salarymx` → reemplazado por `base_salary` + `total_cash_annual`
- `salaryusd` → eliminado (redundante con `payment_currency` de la Sección 2.3; todos reportan en moneda local, se normaliza en análisis)
- `extramx` / `extrausd` → eliminados (capturados por `total_cash_annual`)
- `variation` → reemplazado por `salary_change` + `salary_change_reason`

**Campos rediseñados:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `base_salary` | ¿Cuál es tu salario mensual bruto BASE (antes de impuestos, sin incluir bonos ni compensación variable)? | Numérico | (moneda local) |
| `total_cash_annual` | ¿Cuál fue tu compensación total en efectivo en los últimos 12 meses (incluyendo salario, bonos, aguinaldo, y cualquier otra compensación en efectivo)? | Numérico | (moneda local) |
| `has_equity` | ¿Recibes compensación en acciones, opciones o RSUs? | Selección única | Sí / No |
| `salary_change` | Comparado con hace 12 meses, tu compensación total... | Selección única | Aumentó >20% / Aumentó 10–20% / Aumentó 1–9% / Se mantuvo igual / Disminuyó |
| `salary_change_reason` | ¿A qué se debió el cambio principal? | Selección única | Promoción / Cambio de empresa / Ajuste anual / Cambio a moneda extranjera / Recorte / Otro / No cambió |

**Por qué:** `base_salary` es inequívoco y comparable. `total_cash_annual` captura la foto completa (lo que `salarymx + extramx + aguinaldo + bonos` aproximaba). `has_equity` identifica el nivel oculto de compensación cada vez más común en tech. `salary_change_reason` separa crecimiento por mercado vs. acciones individuales — AMITI puede decir si el crecimiento salarial es de mercado o de movilidad.

#### 1.5.2 Experiencia: Separar Tech vs. Total

**Problema:** `experience` no especifica experiencia en *qué*. Alguien que cambió de carrera con 3 años en tech pero 15 años totales tiene un perfil salarial distinto a alguien con 18 años continuos en software. El segmento de cambios de carrera es grande y creciente.

**Campos actuales eliminados o reemplazados:**
- `experience` → reemplazado por `experience_tech` + `experience_total`
- `seniority` (años en el rol actual) → reemplazado por `tenure_current` (años en la empresa actual)

**Campos rediseñados:**

| ID | Pregunta | Tipo |
|---|---|---|
| `experience_tech` | ¿Cuántos años llevas trabajando profesionalmente en el sector de tecnología? | Numérico |
| `experience_total` | ¿Cuántos años de experiencia laboral total tienes (en cualquier sector)? | Numérico |
| `tenure_current` | ¿Cuántos años llevas en tu empresa actual? | Numérico |

**Por qué:** La diferencia (`experience_total - experience_tech`) identifica a quienes cambiaron de carrera. `tenure_current` reemplaza `seniority` — la antigüedad en la empresa predice mejor compresión salarial y riesgo de rotación que la antigüedad en el rol. Si quienes cambiaron de carrera ganan menos que quienes han estado siempre en tech con la misma experiencia técnica, eso es un hallazgo de política de reskilling.

#### 1.5.3 `profile` → `seniority_level`

**Problema:** El campo `profile` (godín, independiente, emprendedor, directivo, docente, estudiante, otro) mezcla relación de empleo (ya cubierta por `emptype`) con nivel de seniority (no cubierto). "Godín" es slang mexicano — personas de Colombia o Argentina no lo reconocen.

**Campo rediseñado:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `seniority_level` | ¿Cuál es tu nivel dentro de tu organización? | Selección única | Junior / Mid / Senior / Staff-Principal / Lead-Manager / Director+ / Founder-C-Level / No aplica (freelance, estudiante) |

**Por qué:** El nivel de seniority es uno de los predictores salariales más fuertes en cualquier encuesta de desarrolladores, y el encuesta actual no lo captura. Un dev con 3 años en "Senior" gana distinto a uno con 3 años en "Mid". Este campo reemplaza `profile` con valor analítico mucho mayor.

#### 1.5.4 Agregar Tamaño de Empresa

**Problema:** Un backend en un startup de 15 personas y un backend en un banco de 10,000 personas tienen estructuras de compensación muy distintas. `orgtype` captura *tipo* pero no *escala*.

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `company_size` | ¿Cuántos empleados tiene tu empresa (aproximadamente)? | Selección única | 1–10 / 11–50 / 51–200 / 201–1000 / 1001–5000 / 5000+ |

**Por qué:** El tamaño de empresa es un predictor top-5 en cualquier estudio de compensación. Su ausencia es un hueco analítico importante.

#### 1.5.5 Agregar Vertical de Industria

**Problema:** Un dev Python en fintech, en hospital o en gaming está en mercados distintos con normas salariales distintas. El encuesta no lo capta.

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `industry` | ¿En qué industria opera tu empresa? | Selección única | Tecnología/Software / Finanzas/Fintech / Salud / E-commerce/Retail / Educación / Manufactura / Gobierno / Consultoría / Telecomunicaciones / Entretenimiento/Medios / Otro |

#### 1.5.6 Inglés: Agregar Ancla Conductual

**Problema:** La autoevaluación del inglés (ILR 0–5) suele inflarse por el efecto Dunning-Kruger. Personas en nivel 2 reportan 3–4.

**Conservar `english` (ILR 0–5) y agregar:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `english_use` | ¿Con qué frecuencia usas inglés en tu trabajo diario? | Selección única | Nunca / Ocasionalmente (documentación) / Regularmente (reuniones, emails) / La mayor parte del tiempo / Todo mi trabajo es en inglés |

**Por qué:** Los empleadores pagan por *uso*, no por *conocimiento*. `english_use` puede predecir salario mejor que el nivel autoevaluado, y la discrepancia entre ambos detecta autoevaluaciones poco confiables.

#### 1.5.7 `education`: Localizar para LatAm

**Problema:** "Prepa" es mexicano, "pasante" es un estatus académico específico de México, "posgrado" y "maestría" se traslapan. Personas de Colombia y Argentina no lo mapean bien.

**Opciones rediseñadas:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `education` | ¿Cuál es tu nivel máximo de estudios completado? | Selección única | Secundaria o equivalente / Preparatoria-Bachillerato o equivalente / Técnico superior / Licenciatura (en curso) / Licenciatura (titulado) / Maestría / Doctorado |

**Por qué:** "O equivalente" da compatibilidad regional. La distinción en curso vs. completado reemplaza "pasante" explícitamente. Posgrado se integra a maestría/doctorado.

### 1.6 Rediseño del Stack Tech: Arquitectura Rol-Primero

Los bloques de tecnología actuales son la parte más larga del encuesta (~100+ casillas entre lenguajes, frameworks, bases de datos, data science, data engineering, infraestructura, certificaciones y actividades) pero generan la señal analítica más débil. Esta sección los reemplaza por completo.

#### 1.6.1 El Problema de las Matrices de Casillas

1. **Datos dispersos:** La mayoría de celdas son NaN. Tecnologías niche (Elixir, Rust, COBOL) tienen <5% de penetración, requieren N enorme para detectar efectos salariales.
2. **Sin señal de profundidad:** Marcar "Python" significa lo mismo si hiciste un script o si eres senior ML. Binario Y/N destruye la información más valiosa: la pericia.
3. **Multicolinealidad masiva:** React implica JavaScript. Kubernetes implica Docker. PyTorch implica Python. Los coeficientes individuales en el modelo causal son inestables.
4. **Ruptura de series de tiempo:** Opciones cambian cada año (COBOL se eliminó, Julia se añadió, mobile_* apareció en 2022). No se pueden comparar tendencias.
5. **Baja señal salarial:** El análisis 2020–2022 mostró que los roles explican más varianza salarial que tecnologías específicas (Dirección +$16,553 vs. Groovy +$13,854, un outlier). La mayoría de efectos por lenguaje son pequeños y ruidosos. ~40% del encuesta aporta <5% de poder explicativo.
6. **Fatiga del encuestado:** Navegar 100+ casillas es donde la gente abandona o contesta al azar.

#### 1.6.2 Paso 1: Reemplazar Actividades por Rol Primario + Secundario

**Actual:** `act_*` — 26 casillas binarios. Una persona puede marcar Backend Dev, Arquitectura, DevOps y Data Engineering sin indicar cuál define su salario.

**Rediseñado:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `primary_role` | ¿Cuál es tu rol o actividad principal? | Selección única | Backend Dev / Frontend Dev / Fullstack Dev / Mobile Dev / Data Science-ML / Data Engineering / DevOps-Infra-SRE / InfoSec / Architecture / PM / QA-Testing / UXD / Direction-Strategy / AI-ML Engineering / Support / Other |
| `secondary_role` | ¿Tienes un rol secundario? | Selección única | Mismas opciones + "No tengo rol secundario" |

**Por qué:** El modelo causal necesita **un** rol por persona para estimar efectos limpios. Selección múltiple obliga a dummies traslapadas. 2 preguntas reemplazan 26 casillas.

#### 1.6.3 Paso 2: Reemplazar Listas por Stack Principal

En lugar de preguntar por cada tecnología, preguntar por lo que usan *principalmente*.

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `primary_language` | ¿Cuál es tu lenguaje de programación principal? | Selección única | JavaScript-TypeScript / Python / Java / C# / Go / Rust / PHP / Ruby / Kotlin / Swift / C-C++ / Scala / Elixir / Other |
| `primary_framework` | ¿Cuál es tu framework o plataforma principal? | Selección única | React / Angular / Vue / Next.js / Spring / Django-FastAPI / .NET / Rails / Flutter / Laravel / Node.js-Express / None / Other |
| `primary_database` | ¿Cuál es tu base de datos principal? | Selección única | PostgreSQL / MySQL / SQL Server / MongoDB / Redis / DynamoDB / Firebase / Oracle / Other |
| `primary_cloud` | ¿Cuál es tu plataforma de nube principal? | Selección única | AWS / Azure / GCP / On-premise / No uso nube / Other |

**Por qué:** Selección única produce grupos limpios y no traslapados para comparar salarios. "Los devs Python ganan X" es una afirmación real; "la gente que marcó Python entre otras cosas gana X" está confundida. 4 preguntas reemplazan ~60 casillas (`lang_*` + `front_*` + `mobile_*` + `db_*` + parte de `infra_*`).

#### 1.6.4 Paso 3: Agregar Profundidad (lo que los casillas no captan)

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `primary_lang_years` | ¿Cuántos años llevas usando tu lenguaje principal? | Numérico | (años) |
| `tech_breadth` | ¿En cuántas de las siguientes áreas trabajas regularmente? (Backend, Frontend, Mobile, Data, Infra/DevOps, Security, AI/ML) | Numérico | 1–7 conteo |
| `stack_change` | ¿Has cambiado significativamente tu stack tecnológico en los últimos 2 años? | Selección única | Sí, completamente / Sí, parcialmente / No |

**Por qué:** `primary_lang_years` aporta señal de profundidad que los binarios destruyen. `tech_breadth` captura el eje generalista vs. especialista. `stack_change` mide movilidad tecnológica — ¿quienes cambian stack ganan más o menos?

#### 1.6.5 Paso 4: Reducir Certificaciones

**Actual:** `cert_*` — 27 casillas. La mayoría con <10% de penetración.

**Rediseñado:**

| ID | Pregunta | Tipo | Opciones |
|---|---|---|---|
| `has_certs` | ¿Tienes alguna certificación técnica vigente? | Selección única | Sí / No |
| `cert_category` | ¿En qué categoría(s)? (selecciona las que apliquen, máx 3) | Selección múltiple | Cloud (AWS/Azure/GCP) / Agile-PM (Scrum/PMP) / Security (CISSP/CEH) / Kubernetes-DevOps / Data (Databricks/Snowflake) / Other |
| `cert_count` | ¿Cuántas certificaciones tienes? | Numérico | (conteo) |

**Por qué:** Las categorías son estables en el tiempo (a diferencia de nombres específicos). `cert_count` prueba si más certs = más salario o si se aplana. 3 preguntas reemplazan 27 casillas.


#### 1.6.6 Resumen de Impacto

| Métrica | Actual | Rediseñado |
|---|---|---|
| Ítems tech | ~100+ casillas | 13 preguntas estructuradas + 1 opcional |
| Tiempo de respuesta (sección tech) | 8–12 min | 2–3 min |
| Señal analítica por pregunta | Baja (binarios dispersos) | Alta (primario + profundidad) |
| Comparabilidad interanual | Se rompe frecuentemente | Estable (categorías, no productos) |
| Multicolinealidad en modelo causal | Severa | Mínima (grupos de selección única) |

**Lo que se pierde (y por qué es aceptable):**
- **Rankings de popularidad** ("React lo usa el 34%") → se reemplaza por "React es el framework principal del 22% y se asocia a $X". La segunda es más valiosa. El campo opcional `all_technologies` recupera la primera.
- **Efectos de tecnologías niche** ("premium Elixir = +$11,838") → esa estimación se basó en ~100 respuestas y era ruidosa. El enfoque de stack principal da estimaciones más limpias para tecnologías con N suficiente.

---

## Objetivo 2: Artefacto para Política Pública

### 2.1 Justificación

El encuesta actual produce hallazgos descriptivos y causales excelentes (premio por experiencia, premio por inglés, brecha de género, efectos por ciudad), pero se enmarcan como *insights para decisiones individuales* ("aprende inglés para ganar más"). Para impulsar política pública, los hallazgos deben reencuadrarse como *condiciones estructurales que instituciones pueden cambiar*.

**Audiencia principal: AMITI (Asociación Mexicana de la Industria de Tecnologías de Información).** Software Guru no tiene canal directo con STPS, SAT, SEP o CONEVAL. AMITI sí. El valor de política del encuesta se realiza *a través de AMITI* — los hallazgos deben empaquetarse como munición de advocacy que AMITI pueda llevar a tomadores de decisión, no como observaciones académicas neutrales.

Esto implica que cada hallazgo debe responder la pregunta de AMITI: **"¿Qué podemos proponer, y a quién?"**

| Enfoque individual (actual) | Enfoque AMITI advocacy (propuesto) | Acción AMITI |
|----|-----|-----|
| "Aprende inglés para ganar 12K más" | "La proficiencia en inglés explica 15% de la varianza salarial — la pipeline de inglés es un cuello de botella para el crecimiento del sector" | Proponer a SEP: certificación de inglés alineada a industria para programas CS |
| "Múdate a Hermosillo para ganar más" | "Ciudades tier-2 ofrecen 30% menor salario nominal con mayor poder adquisitivo — destinos ideales de nearshoring" | Presentación a inversionistas vía misiones de AMITI |
| "Las mujeres ganan 12K menos" | "El pool de talento está limitado a ~50% de su potencial por una composición 95% masculina" | Proponer a miembros: financiar programas de pipeline como estrategia de oferta de talento |

El rediseño agrega bloques de preguntas que generan hallazgos *que solo instituciones pueden accionar*, enmarcados como posiciones de advocacy pre-redactadas para que AMITI las lleve. Cada bloque concluye con recomendaciones accionables organizadas por institución objetivo:

- **"Proponemos a [dependencia] que..."** — AMITI haciendo cabildeo con STPS, SAT, SEP
- **"Recomendamos a nuestros miembros que..."** — AMITI estableciendo estándares internos de industria
- **"Presentamos a inversionistas que..."** — AMITI promoviendo México/LatAm como destino tech

### 2.2 Nuevo Bloque: Formalidad Laboral y Protección Social

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `formal_contract` | ¿Tienes un contrato laboral formal por escrito? | Selección única | Sí / No / No sé |
| `social_security` | ¿Estás inscrito en el IMSS, ISSSTE u otro sistema de seguridad social a través de tu empleo? | Selección única | Sí, por mi empleo / Sí, por cuenta propia / No |
| `retirement_saving` | ¿Realizas aportaciones a una Afore o fondo de retiro? | Selección única | Sí, mi empleador aporta / Sí, solo por mi cuenta / No |

**Justificación de advocacy para AMITI:**

La informalidad laboral en México ronda 55%, pero *nadie la ha medido específicamente en el sector tech*. La evidencia anecdótica sugiere que una fracción significativa de trabajadores — especialmente juniors, freelancers y quienes están en outsourcing — trabajan por honorarios sin IMSS ni aportaciones de retiro.

El reencuadre crítico: **la informalidad no es solo un problema de cumplimiento — es un problema de competitividad.** Clientes internacionales (sobre todo empresas de EUA y la UE evaluando nearshoring) requieren cada vez más evidencia de cumplimiento laboral. Un sector tech con alta informalidad es un sector que pierde contratos. Esto convierte la formalización en un argumento de *crecimiento industrial*, no en una carga regulatoria — y así es como AMITI debe posicionarlo.

**Recomendaciones accionables para AMITI:**
- **Proponer a STPS:** Un camino simplificado de formalización para el sector digital — un régimen de nómina ligero diseñado para trabajo remoto y micro-empleadores tech. Los datos cuantifican a cuántos cubriría y el aumento estimado de IMSS/Infonavit.
- **Recomendar a miembros AMITI:** Autocertificación de empleo formal para todo personal tech. Posicionarlo como diferenciador competitivo: "Empresas AMITI garantizan empleo formal." Vincularlo a BP2C como mecanismo de verificación.
- **Presentar a inversionistas:** "X% de la fuerza laboral tech mexicana está formalmente empleada con protección social completa" — dato que apoya decisiones de nearshoring.

**Plan analítico:**
- Cruzar `emptype` × `social_security` para cuantificar informalidad por tipo de empleo
- Modelar `formal_contract` en función de `orgtype`, `city` y `seniority` para identificar concentraciones (si se concentra en outsourcing/itservices, AMITI puede focalizar)
- Calcular el *premium/penalidad por informalidad*: si informales ganan *más* (diferencial compensatorio), el argumento es "la formalidad es poco competitiva — simplifiquemos el régimen". Si ganan *menos* (explotación), el argumento es "la informalidad deprime salarios y reduce atractivo".

**Conexión con datos existentes:** Estas tres preguntas enriquecen `emptype`. Un persona que responde con `emptype=honorarios` y `social_security=No` está en una situación cualitativamente distinta a uno con `emptype=honorarios` y `social_security=Sí, por cuenta propia`.

### 2.3 Nuevo Bloque: Dinámicas Transfronterizas

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `employer_hq` | ¿En qué país tiene su sede principal la empresa para la que trabajas? | Selección única | México / Estados Unidos / Canadá / Europa / América Latina (otro) / Asia / Otro |
| `payment_currency` | ¿En qué moneda recibes tu compensación principal? | Selección única | MXN / USD / EUR / Otra |
| `cross_border_contract` | ¿Cuál es tu relación laboral con esta empresa extranjera? | Selección única | Contrato laboral local (a través de entidad mexicana) / Contractor independiente / A través de Employer of Record (Deel, Remote, etc.) / Otro |
| `cross_border_tax` | ¿Emites facturas (CFDI) a una empresa extranjera como persona física con actividad empresarial? | Selección única | Sí / No / No aplica |

**Justificación de advocacy para AMITI:**

La pandemia de 2020 abrió el mercado laboral mexicano a trabajo remoto con EUA. El análisis causal encontró un premium remoto de +$12,213 MXN/mes, pero no distinguía remoto para empleador mexicano vs. remoto para empleador extranjero. Son posiciones de mercado distintas — y los miembros de AMITI pierden talento en ambos sentidos.

El problema central para AMITI: **empleadores extranjeros reclutan talento mexicano a 2–3× salarios locales sin obligación con el ecosistema mexicano** — sin IMSS, Infonavit, Afore, oficina local ni presencia fiscal. Es fuga de talento sin emigración, e invisible en estadísticas oficiales porque nadie sale del país. Cuantificar esta fuga da números concretos para el gobierno.

**Recomendaciones accionables para AMITI:**
- **Proponer a SAT:** Un marco de registro de empleadores extranjeros que contratan 5+ trabajadores tech mexicanos, con contribuciones a seguridad social (modelado en Portugal/Estonia). Los datos cuantifican el tamaño del workforce sin registrar.
- **Proponer a STPS:** Aclarar el estatus regulatorio de Employer of Record (EoR) (Deel, Remote, Oyster). ¿Son empleados formales? La data muestra qué fracción usa cada arreglo.
- **Proponer a SE (Secretaría de Economía):** Incentivos fiscales para empleadores tech nacionales que reduzcan la brecha salarial con extranjeros. Enmarcar como retención: "Por cada $X MXN de incentivos, se retienen Y desarrolladores".
- **Presentar a inversionistas:** "México tiene N miles de devs ya trabajando para empresas de EUA de forma remota — el pool es probado, con inglés y alineación horaria. Una operación formal captura mejor retención".

**Plan analítico:**
- Descomponer el premium remoto: `salary ~ remote + employer_hq + payment_currency + controles`. El premium remoto puede ser en realidad un *premium transfronterizo*.
- Cuantificar la "economía Deel": ¿qué fracción usa EoR? Ese es el número que STPS necesita.
- Mapear patrones geográficos: ¿qué ciudades están más expuestas a fuga transfronteriza? AMITI puede priorizar programas ahí.
- Estimar el "gap de seguridad social": trabajadores transfronterizos × contribución promedio no pagada = pérdida anual IMSS/Infonavit.

**Conexión con datos existentes:** Este bloque explica una parte significativa de la varianza no explicada del modelo 2020–2022. El dummy remoto era un instrumento burdo; estas preguntas lo descomponen en categorías estructurales.

### 2.4 Nuevo Bloque: Poder Adquisitivo y Costo de Vida

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `purchasing_power` | ¿Cómo calificarías tu capacidad para cubrir tus necesidades básicas con tu salario actual? | Likert 1–5 | 1=Con mucha dificultad ... 5=Con mucha holgura |
| `housing_burden` | ¿Qué porcentaje aproximado de tu ingreso mensual destinas a renta o hipoteca? | Selección única | 0% (vivienda propia sin hipoteca) / 1–20% / 21–30% / 31–40% / 41–50% / Más del 50% |
| `financial_savings` | ¿Logras ahorrar al menos el 10% de tu ingreso mensual? | Selección única | Sí, regularmente / A veces / Rara vez o nunca |

**Justificación de advocacy para AMITI:**

El análisis actual encontró efectos por ciudad muy marcados (Hermosillo +$18,632 vs. León -$13,427 respecto a CDMX), pero el salario nóminal cuenta solo la mitad de la historia. Un dev con $35K MXN en Mérida puede tener mayor *poder adquisitivo real* que alguien con $50K MXN en CDMX tras vivienda.

Para AMITI, este bloque es principalmente una **herramienta de presentación de nearshoring y estrategia de distribución de talento**. AMITI puede decir a inversionistas: "La ciudad X ofrece seniors a 30% menos costo nóminal que CDMX, con *mayor* satisfacción y poder adquisitivo. Aquí está el índice." Esto reencuadra el análisis de costo de vida como artefacto de atracción de inversión.

**Recomendaciones accionables para AMITI:**
- **Presentar a inversionistas (vía misiones de AMITI):** Índice "Tech Talent Value" por ciudad combinando salario nóminal, poder adquisitivo y densidad de talento. Se convierte en una lámina estándar en cada presentación.
- **Recomendar a miembros AMITI:** Empresas que expanden deberían usar ranking ajustado por poder adquisitivo, no solo salarios nóminales. Un hub en Mérida o Aguascalientes puede atraer talento equivalente con menor costo y mayor bienestar.
- **Presentar a gobiernos estatales:** "Tu ciudad está #X en compensación tech ajustada por poder adquisitivo. Esto te movería: vivienda, transporte, coworking." Datos accionables ligados a decisiones de inversión de miembros AMITI.

Nadie en LatAm publica un **índice de salarios reales específico de tech**. La combinación de salario + ciudad + poder adquisitivo subjetivo + carga de vivienda permite construirlo — y AMITI sería quien lo distribuye.

**Plan analítico:**
- Construir índice de poder adquisitivo por ciudad: promedio de `purchasing_power` por ciudad, ponderado por banda salarial
- Comparar rankings de salario nóminal vs. rankings ajustados por poder adquisitivo — resaltar ciudades donde el orden se invierte (ciudades "valor oculto")
- Modelar `financial_savings` en función de salario, ciudad, carga de vivienda y estado familiar para identificar fragilidad financiera (ciudades con mayor riesgo de rotación)

### 2.5 Nuevo Bloque: ROI Educativo y Trayectorias

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `edu_relevance` | ¿Qué tan relevante fue tu educación formal para tu trabajo actual? | Likert 1–5 | 1=Nada relevante ... 5=Totalmente relevante |
| `recent_training` | ¿Has completado alguna capacitación o curso en los últimos 12 meses? | Selección única | Sí, pagado por mi empleador / Sí, pagado por mí / Sí, gratuito / No |
| `first_job_degree` | ¿Tu primer empleo en tecnología requirió un título universitario? | Selección única | Sí, era requisito formal / No, pero lo tenía / No, y no lo tenía |
| `edu_debt` | ¿Tienes deuda educativa actualmente (crédito educativo, préstamo para estudios)? | Selección única | Sí / No / Prefiero no contestar |

**Justificación de advocacy para AMITI:**

AMITI ya corre programas de colaboración con ANUIES. Las variables `education` y `edutype` muestran que *cómo* aprendiste importa junto con *cuánto* estudiaste. Pero el encuesta actual no responde la pregunta clave del comité educativo de AMITI: **¿qué trayectorias educativas producen el talento más competitivo y cómo debe invertir la industria?**

- **¿Vale la pena un grado de CS?** `edu_relevance` + `first_job_degree` lo miden directamente. Si 60% de seniors dice que su educación fue "poco relevante" y su primer empleo no requirió título, AMITI puede ir a ANUIES con datos: "Los planes deben rediseñarse con industria".
- **¿Quién se reentrena y quién paga?** `recent_training` distingue capacitación pagada por empresa vs. autofinanciada vs. gratuita. Si la mayoría es autofinanciada, AMITI puede pedir deducción fiscal para capacitación de empleador (similar al incentivo STPS, ampliado para certs tech).
- **¿La deuda educativa es barrera para crecimiento del pipeline?** `edu_debt` es proxy de accesibilidad. Si egresados de bootcamp cargan menos deuda y ganan similar a licenciados, AMITI puede promover bootcamps como ruta más rápida y barata para ampliar talento.

**Recomendaciones accionables para AMITI:**
- **Proponer a ANUIES (vía comité educativo):** Reformas curriculares basadas en `edu_relevance` por área. "Programas con prácticas industriales alcanzan $50K MXN de mediana 2 años antes — aquí está el dato".
- **Proponer a STPS:** Expandir el incentivo fiscal de capacitación para cubrir certificaciones tech y reskilling en IA. `recent_training` cuantifica la brecha entre capacitación financiada por empresa y por persona.
- **Recomendar a miembros AMITI:** Financiar becas en bootcamps y vías alternativas, no solo universidades. Si `edutype=bootcamp` rinde comparable con menor deuda, el ROI es mejor.

**Plan analítico:**
- Calcular la "prima de título" con controles modernos: `salary ~ education + edutype + edu_relevance + first_job_degree + experience + english_num + ...`
- Si `edu_relevance` media la ruta educación→salario, la prima es de señalización, no capital humano — el argumento de AMITI hacia ANUIES cambia (reformar currículos vs. eliminar requisitos).
- Segmentar por `edutype`: ¿autodidactas ganan menos *porque* no tienen título o *a pesar* de alta relevancia? Esto distingue credencialismo de habilidad y guía a AMITI para argumentar contra requisitos de título.

### 2.6 Nuevo Bloque: Impacto de IA en el Individuo

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `ai_tools_use` | ¿Utilizas herramientas de IA (Copilot, ChatGPT, etc.) como parte regular de tu trabajo? | Selección única | Sí, diariamente / Sí, semanalmente / Ocasionalmente / No |
| `ai_task_change` | ¿Han cambiado las tareas que realizas debido a herramientas de IA? | Selección única | Sí, hago tareas de mayor nivel / Sí, hago las mismas tareas más rápido / Sí, algunas tareas ya no las hago / No ha cambiado |
| `ai_skill_confidence` | ¿Qué tan confiado/a estás en que tus habilidades actuales seguirán siendo relevantes en 3 años? | Likert 1–5 | 1=Nada confiado ... 5=Totalmente confiado |
| `ai_salary_impact` | ¿Consideras que tu uso de herramientas de IA ha contribuido a mejorar tu compensación? | Selección única | Sí, directamente / Probablemente sí / No creo / Definitivamente no |

**Separación de BP2C (cumplimiento Objetivo 1):**

| Aspecto | Encuesta de Salarios (estas preguntas) | BP2C |
|--------|------|------|
| Sujeto | Posición de mercado del individuo | Comportamiento organizacional del empleador |
| Qué mide | "¿Estoy en riesgo? ¿Estoy ganando?" | "¿Mi empleador me habilita?" |
| Palanca | Ninguna (nivel mercado) | Habilitación de IA (6 Qs), Tecnoansiedad (3 Qs) |

**Justificación de advocacy para AMITI:**

El impacto de la IA en el mercado laboral tech es la pregunta de política de la década, pero casi todos los datos vienen de encuestas de EUA/Europa (Stack Overflow, Dice, etc.). En LatAm hay muy poca data estructurada sobre patrones de adopción de IA entre devs. Para AMITI, este bloque produce el **primer benchmark de adopción de IA del workforce tech mexicano** — dato que posiciona a AMITI como voz autorizada en política de IA y talento.

El reencuadre clave: la adopción de IA no es una amenaza a gestionar — es una **ventaja competitiva que debe acelerarse**. Los miembros de AMITI que invierten en capacitación en IA retienen talento y aumentan productividad. La data debe demostrarlo para crear un business case que AMITI lleve a miembros y gobierno.

- **ROI de inversión del empleador:** Si los datos muestran que devs cuyos empleadores ofrecen capacitación en IA (detectable vía `recent_training` cruzado con `ai_tools_use`) tienen mayor `ai_skill_confidence` y menor intención de búsqueda (`job_search`), AMITI puede argumentar: "La capacitación en IA retiene desarrolladores X% más. Un crédito fiscal para reskilling en IA beneficia al sector".
- **Velocidad de adopción como métrica competitiva:** Cruzar `ai_tools_use` por `orgtype`, `city` y `employer_hq` para mapear dónde la adopción es rápida o lenta. AMITI puede presentar a SE: "La adopción de IA en México es X% vs. Y% en Brasil/India — esto se necesita para cerrar la brecha".
- **Captura de productividad:** `ai_salary_impact` mide si las ganancias de productividad se traducen en compensación o se quedan en el empleador. Si no se comparten, AMITI puede recomendar normas de profit-sharing antes de regulación externa.

**Recomendaciones accionables para AMITI:**
- **Proponer a STPS/SE:** Deducción fiscal para programas de reskilling en IA (basado en incentivo STPS, ampliado a contenido IA). La data cuantifica la brecha de capacitación y el ROI de retención.
- **Recomendar a miembros AMITI:** Benchmark de adopción de IA contra la mediana. Empresas debajo de la mediana se están rezagando — AMITI puede ofrecer assessment de readiness como servicio.
- **Presentar a socios internacionales:** "El workforce mexicano tiene X% de uso diario de IA — mayor que [comparativo]. La fuerza laboral está lista para operaciones de nearshoring con IA".

### 2.7 Nuevo Bloque: Pipeline de Género y Diversidad

**Preguntas:**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `first_code_age` | ¿A qué edad escribiste tu primera línea de código o programa? | Numérico | (años) |
| `childhood_computer` | ¿Tenías acceso a una computadora en casa durante tu infancia (antes de los 15 años)? | Selección única | Sí, propia / Sí, compartida / No |
| `discrimination_exp` | ¿Has experimentado discriminación en procesos de contratación o promoción en el sector tecnológico? | Selección única | Sí, frecuentemente / Sí, alguna vez / No / Prefiero no contestar |
| `identity_visibility` | ¿Te sientes cómodo/a siendo visible con tu identidad (género, orientación, etnia) en tu lugar de trabajo? | Likert 1–5 | 1=Nada cómodo ... 5=Totalmente cómodo |

**Justificación de advocacy para AMITI:**

El análisis 2020–2022 encontró una brecha ajustada de -$12,442, pero con solo 291 mujeres (5% de la muestra) el hallazgo es ruidoso y, más importante, *sin explicación*. La brecha persiste tras controlar experiencia, educación y rol, lo que implica discriminación o efectos de pipeline (o ambos). Sin datos de pipeline, no se pueden distinguir.

Para AMITI, el encuadre es **restricción de oferta de talento**, no solo justicia social (aunque se alinean). El sector tech mexicano está limitado artificialmente a la mitad de su potencial por una composición ~95% masculina. Cada mujer que no entra a tech es una dev menos que los miembros de AMITI pueden contratar. El diagnóstico importa porque la *intervención* depende de la causa:

- **Si es pipeline:** Las mujeres entran más tarde, con menos exposición en infancia y acumulan menos experiencia. Acción AMITI → financiar acceso temprano STEM como inversión de oferta, no CSR. Cabildear SEP para computadoras en escuelas públicas con metas de participación femenina.
- **Si es discriminación:** Mujeres con mismas credenciales ganan menos. Acción AMITI → promover normas de transparencia salarial entre miembros (voluntarias antes de regulación). Vincular a BP2C: empresas con auditorías de equidad reciben badge.

La interacción `first_code_age` × `gender` es el diagnóstico clave. Si las mujeres inician a codificar 5+ años después, la penalidad salarial por experiencia es un problema de pipeline en la infancia, no de mercado laboral.

`childhood_computer` prueba la hipótesis de acceso: ¿el problema es oportunidad o interés? Si mujeres sin acceso están subrepresentadas incluso frente a hombres sin acceso, el obstáculo es distinto al equipo.

**Recomendaciones accionables para AMITI:**
- **Proponer a SEP:** "Solo X% de mujeres tuvo acceso a computadora antes de los 15 vs. Y% de hombres. El acceso a equipo es cuello de botella del pipeline — financiar programa tech-para-niñas".
- **Recomendar a miembros AMITI:** Financiar programas de coding para mujeres (Laboratoria, iniciativas tipo Hackbright) con ROI de pipeline, no CSR. La data da línea base: por cada 100 mujeres que entran al pipeline, miembros AMITI ganan X devs mid-level en 5 años.
- **Presentar a inversionistas:** "Empresas con diversidad de género arriba de la mediana (medible vía BP2C) tienen X% menor rotación y Y% más pool de candidatos" — dato ESG para inversión.

**Nota de tamaño de muestra:** Con 5% de participación femenina, el poder estadístico es limitado. El rediseño debe incluir canales de distribución específicos (Women Who Code México, redes de egresadas Laboratoria, etc.) para elevar la tasa femenina a 15–20%.

### 2.8 Expansión Geográfica a América Latina

**Alcance actual:** México (con respuestas incidentales de 26 países en 2020, mayormente ruido).

**Alcance propuesto:** México + Colombia + Argentina + Brasil como objetivos principales, con recolección LatAm-wide como secundaria.

**Implementación:**

| Cambio | Detalle |
|--------|--------|
| Idioma | Agregar versión en portugués para Brasil |
| Moneda | Normalizar salarios a USD-PPP para comparación; recolectar en moneda local |
| Seguridad social | Localizar: IMSS (MX), EPS/AFP (CO), ANSES/OSDE (AR), INSS (BR) |
| Opciones de ciudad | Expandir a Bogotá, Medellín, Buenos Aires, Córdoba, São Paulo, Belo Horizonte, etc. |
| Distribución | Alianzas con comunidades tech locales (Colombia: BogotáJS, Argentina: Meetup.js, Brasil: DevParaná, etc.) |

**Justificación de advocacy para AMITI:**

No existe una encuesta comparable de mercado laboral tech en América Latina. Las más cercanas son:
- Stack Overflow Developer Survey (global, mínima cobertura LatAm)
- Glassdoor/Levels.fyi (centradas en EUA, auto-selección, sin framing de política)
- Datos OCDE (no específicos de tech)

Para AMITI, la expansión geográfica convierte el encuesta de **reporte nacional** a **benchmark regional** — y AMITI se vuelve el custodio de ese benchmark. Implica tres efectos estratégicos:

1. **Posicionamiento competitivo:** AMITI puede mostrar dónde México se ubica frente a Colombia, Argentina y Brasil en cada métrica (formalidad, compensación, adopción IA, diversidad). Donde México lidera, es argumento para inversión. Donde rezaga, es argumento para apoyo gubernamental.
2. **Alianzas pan-LatAm:** Datos cross-country generan alianzas con asociaciones equivalentes (FEDESOFT en Colombia, CESSI en Argentina, Brasscom en Brasil). AMITI se posiciona como convocante de una red regional de inteligencia laboral tech.
3. **Visibilidad internacional:** Un reporte regional puede ser citado por BID, Banco Mundial y OCDE — elevando el perfil de AMITI más allá de México.

**Recomendaciones accionables para AMITI:**
- **Presentar a BID/Banco Mundial:** "Primera comparación cross-country del mercado laboral tech en LatAm. México tiene formalidad X% vs. Colombia Y% — estas son barreras estructurales." Organismos de desarrollo financian este tipo de comparativos.
- **Proponer a SE (vía AMITI):** "La fuerza laboral tech mexicana es Z% más productiva por dólar que Brasil — aquí está el argumento de nearshoring por ciudad." 
- **Construir alianzas con FEDESOFT, CESSI, Brasscom:** Reportes regionales co-marcados multiplican distribución y credibilidad. Cada asociación lleva hallazgos a su gobierno.

**Riesgos:**
- Dilución de muestra: si N total se mantiene ~5,000, dividir en 4 países da ~1,250 por país, limitando análisis por subgrupo. Meta: 3,000+ por país.
- Costo de localización: traducción a portugués, normalización de moneda, localización de seguridad social requieren inversión.
- Pérdida de comparabilidad temporal: agregar países en 2026 rompe la serie 2020–2022 México-only. Mitigación: mantener México como cohorte continua.

### 2.9 Entregable: Brief de Advocacy AMITI

Además del reporte público, el análisis debe producir un **brief separado de 4–6 páginas para AMITI** — no publicado, entregado a liderazgo AMITI — que empaquete los hallazgos clave como posiciones de advocacy pre-redactadas. Este es el entregable que hace a AMITI un socio recurrente.

**Estructura del Brief AMITI:**

| Sección | Contenido | Institución objetivo |
|---------|---------|-------------------|
| 1. Resumen ejecutivo | Top 5 hallazgos con cifras | Consejo AMITI |
| 2. Propuesta de formalización | Tasa de informalidad + propuesta de régimen simplificado | STPS |
| 3. Regulación transfronteriza | Prevalencia EoR + propuesta de registro de empleadores extranjeros | SAT, STPS |
| 4. Presentación de inversión | Índice de poder adquisitivo + perfiles por ciudad | Inversionistas (vía misiones AMITI) |
| 5. Pipeline educativo | ROI de títulos + prioridades de reforma curricular | ANUIES (vía comité educativo AMITI) |
| 6. Benchmark de IA | Adopción + propuesta de crédito fiscal de capacitación | SE, STPS |

Cada sección sigue un formato estándar:
1. **Hallazgo** (1 párrafo + 1 gráfica)
2. **Por qué importa al sector** (1 párrafo)
3. **Acción propuesta** (bullets: quién, qué, impacto esperado)
4. **Exhibición de soporte** (tabla o figura del encuesta)

**Por qué un brief separado importa:** El reporte público debe ser periodístico y servir a la comunidad — no puede leer como documento de lobby. El Brief AMITI puede ser explícitamente de advocacy por ser privado y para una audiencia con intereses institucionales. Esta separación protege credibilidad y maximiza utilidad de política.

**Valor de Software Guru para AMITI:** Software Guru se convierte en *socio de datos* de AMITI — la organización que provee la base empírica para las posiciones de advocacy. Es una relación duradera que justifica co-patrocinio, distribución por miembros y potencial financiamiento de expansión LatAm.

---

## Objetivo 3: Gancho Comercial para BP2C

### 3.1 Justificación

La Encuesta de Salarios es un activo comunitario gratuito con alto alcance. BP2C es una certificación pagada con alcance limitado (26–51 empresas, participación decreciente). El objetivo estratégico es usar la audiencia de la Encuesta de Salarios para crear demanda de BP2C, sin:

- Convertir la encuesta en anuncio (mata credibilidad)
- Duplicar contenido de BP2C en la Encuesta de Salarios (canibaliza)
- Hacer que la encuesta se sienta incompleta sin BP2C (frustra)

La solución es diseñar la Encuesta de Salarios para que sus *hallazgos apunten naturalmente a preguntas que solo BP2C puede contestar*.

### 3.2 El Teaser de Brecha de Satisfacción

**Preguntas (agregar — máximo 3):**

| ID | Pregunta | Tipo | Opciones |
|----|----------|------|---------|
| `enps` | Del 0 al 10, ¿qué tan probable es que recomiendes a tu empleador a un amigo? | Escala NPS | 0–10 |
| `leave_reason` | ¿Cuál sería la razón principal por la que dejarías tu empleo actual? | Selección única | Salario / Crecimiento profesional / Cultura organizacional / Liderazgo / Flexibilidad / Otro |
| `job_search` | ¿Estás buscando activamente otro empleo? | Selección única | Sí / No, pero estoy abierto/a / No |

**Por qué solo estas tres:**

Son *variables de resultado*, no *instrumentos diagnósticos*. Miden el *resultado* de la calidad del empleador sin explicar *por qué*. Las Seis Palancas de BP2C son el diagnóstico. Esa asimetría es el motor comercial:

- La Encuesta de Salarios puede publicar: *"43% de profesionales tech con salario >$60K MXN aún reportan eNPS <6. Un salario alto no predice satisfacción."*
- **No** puede explicar por qué, porque no tiene las Seis Palancas.
- El reporte entonces señala: *"El marco BP2C mide seis dimensiones independientes de atractivo del empleador que explican estos patrones. Empresas interesadas pueden inscribirse en [link]."*

**Consideración de anonimato:** eNPS es sensible. Los encuestados pueden temer identificación. La Encuesta de Salarios **nunca** debe vincular eNPS a empleadores identificables en reportes públicos. Esto es ético y estratégico: hace que BP2C (donde la identificación es consensual) sea la única fuente legítima de puntajes por empleador.

### 3.3 Señal Agregada Entre Encuestas

Si se puede vincular a personas entre encuestas (aunque sea débilmente, por cluster de empleador), emergen narrativas poderosas:

| Hallazgo publicado | Fuente | Impulsa demanda de |
|---|---|---|
| "Empleados en empresas BP2C certificadas ganan 18% arriba de la mediana" | Encuesta de Salarios × BP2C | Empresas quieren certificarse |
| "Empresas certificadas tienen eNPS 7.2 vs. 5.1 en no certificadas" | Encuesta de Salarios (eNPS) × lista BP2C | Empresas quieren subir su score |
| "Empleadores certificados reportan 40% menor intención de rotación" | Encuesta de Salarios (`job_search`) × lista BP2C | HR quiere la data de retención |

**Implementación:**

Vincular requiere saber en qué empresa trabaja la persona. La encuesta de salarios históricamente **no** recolecta nombre de empleador (por anonimato). Opciones:

1. **Etiquetado opt-in de empleador:** "Si deseas que tu respuesta se incluya en benchmarking por empresa, escribe el nombre de tu empresa (opcional)." Mantiene anonimato por default.
2. **Cluster por dominio:** Si se recolectan correos, agrupar por dominio. Es implícito y menos transparente — no recomendado.
3. **Matching BP2C:** Preguntar "¿Tu empleador está inscrito en BP2C?" (Sí/No/No sé). Es el enfoque más ligero — no revela empleador pero permite comparar certificados vs. no certificados.

**Recomendación:** Opción 3 (awareness de BP2C) como implementación mínima viable. Opción 1 (opt-in de empleador) como objetivo aspiracional si la tasa de respuesta lo permite.

### 3.4 La Narrativa de "Palancas Faltantes"

El modelo causal explica 38.74% de la varianza salarial con 42 predictores. En el reporte, enmarcar explícitamente el 61.26% no explicado como feature, no bug:

> *"Nuestro modelo captura factores demográficos, geográficos, técnicos y estructurales que explican 39% de la variación salarial. El 61% restante refleja negociación individual, cultura del empleador, oportunidades de desarrollo y habilitación organizacional — dimensiones que la certificación BP2C está diseñada para medir."*

Esto posiciona ambos productos como dos mitades de una visión completa:
- **Encuesta de Salarios:** Qué paga el mercado (estructural, externo)
- **BP2C:** Por qué la gente se queda o se va (cultural, interno)

Ninguno es completo solo. Ambos son necesarios para entender el mercado laboral tech.

### 3.5 Estructura de Reporte para el Gancho

En el reporte anual, incluir una sección dedicada (máx 2 páginas) con un título como:

> **"Más allá del salario: lo que el dinero no explica"**

Esta sección presenta:
1. Distribución de eNPS por banda salarial (mostrar que salario alto ≠ satisfacción alta)
2. Principales respuestas de `leave_reason` (mostrar que salario rara vez es #1)
3. El 61% de varianza no explicada
4. Descripción no promocional del marco BP2C como complemento

Debe ser **periodística, no comercial**. Si suena a anuncio, se pierde credibilidad. El gancho funciona porque la encuesta es un recurso comunitario gratuito y confiable. Esa confianza es el activo comercial.

---

## Hoja de Ruta de Implementación

### Fase 1: Diseño del Instrumento (pre-lanzamiento)

- [ ] Finalizar redacción de preguntas para todos los nuevos bloques (Secciones 2.2–2.7)
- [ ] Probar el instrumento con 10–15 profesionales TI para claridad y tiempo
- [ ] Decidir el alcance geográfico (México vs. expansión LatAm)
- [ ] Diseñar estrategia de muestreo y distribución (alianzas, redes, empresas)
- [ ] Implementar mecanismo de etiquetado opt-in de empleador (Sección 3.3)
- [ ] Construir el instrumento con lógica de salto (ej. `cross_border_contract` solo si `employer_hq` ≠ México)

### Fase 2: Recolección de Datos

- [ ] Meta de muestra: 3,000+ por país (si expansión) o 5,000+ (si México)
- [ ] Ventana de distribución: 4–6 semanas
- [ ] Outreach dirigido a grupos subrepresentados (mujeres, no binario, ciudades no-CDMX)
- [ ] Notificación a participantes BP2C: invitar a empleados de empresas BP2C a responder

### Fase 3: Análisis y Publicación

- [ ] Reproducir el modelo causal 2020–2022 con datos nuevos
- [ ] Agregar nuevos bloques al marco causal (descomposición transfronteriza, premium de formalidad, efectos de adopción IA)
- [ ] Construir el índice de poder adquisitivo por ciudad
- [ ] Calcular métricas de ROI educativo
- [ ] Construir vínculo entre encuestas (Encuesta de Salarios × BP2C)
- [ ] Redactar reporte orientado a política con sección "Más allá del salario"
- [ ] Publicar hallazgos en inglés y español

### Fase 4: Ciclo de Retroalimentación

- [ ] Medir consultas de BP2C que citen el reporte de la Encuesta de Salarios
- [ ] Medir overlap de personas encuestadas entre encuestas
- [ ] Evaluar tasas de respuesta por bloque — eliminar cualquier bloque con >30% de no respuesta
- [ ] Planear iteración 2027 con base en hallazgos

---

## Resumen de Inventario de Preguntas

### Retenidas de la Encuesta Actual (con modificaciones)

| # | Campo | Cambio |
|---|-------|--------|
| 1 | `age` | Sin cambios |
| 2 | `gender` | Sin cambios |
| 3 | `country` | Expandir opciones LatAm |
| 4 | `city` | Expandir opciones LatAm |
| 5 | `education` | Localizada LatAm; "o equivalente" agregado; pasante/posgrado reemplazados (Sec 1.5.7) |
| 6 | `edutype` | Sin cambios |
| 7 | `orgtype` | Agregar `ai_native`, renombrar `isv` → `product_company` |
| 8 | `emptype` | Sin cambios (enriquecido por bloque de formalidad) |
| 9 | `work_arrangement` | Reemplaza `remote` (Y/N) y `covid_remoto`. 4 opciones. (Sec 1.3.1) |
| 10 | `english` | Sin cambios (ILR 0–5) |
| 11 | `vacaciones` | Sin cambios |
| 12 | `aguinaldo` | Sin cambios; localizable para LatAm |

### Preguntas Existentes Rediseñadas (Sección 1.5)

| # | Campo Nuevo | Reemplaza | Cambio |
|---|-----------|----------|--------|
| 13 | `base_salary` | `salarymx` | Salario base inequívoco; solo moneda local (Sec 1.5.1) |
| 14 | `total_cash_annual` | `salarymx` + `extramx` + `aguinaldo` + bonos | Compensación anual total (Sec 1.5.1) |
| 15 | `has_equity` | (nuevo) | Identifica compensación en equity (Sec 1.5.1) |
| 16 | `salary_change` | `variation` | Bandas categóricas vs. % ambiguo (Sec 1.5.1) |
| 17 | `salary_change_reason` | (nuevo) | Descompone causa del crecimiento (Sec 1.5.1) |
| 18 | `experience_tech` | `experience` | Años explícitos en tech (Sec 1.5.2) |
| 19 | `experience_total` | (nuevo) | Años totales; delta = señal de cambio de carrera (Sec 1.5.2) |
| 20 | `tenure_current` | `seniority` | Antigüedad en empresa reemplaza antigüedad en rol (Sec 1.5.2) |
| 21 | `seniority_level` | `profile` | Jr/Mid/Sr/Staff/Lead/Director/C-Level (Sec 1.5.3) |
| 22 | `company_size` | (nuevo) | Predictor top-5 ausente (Sec 1.5.4) |
| 23 | `industry` | (nuevo) | Segmentación por vertical (Sec 1.5.5) |
| 24 | `english_use` | (nuevo) | Ancla conductual del inglés (Sec 1.5.6) |

### Rediseño de Stack Tech (Sección 1.6)

| # | Campo Nuevo | Reemplaza | Cambio |
|---|-----------|----------|--------|
| 25 | `primary_role` | `act_*` (26 casillas) | Rol principal único (Sec 1.6.2) |
| 26 | `secondary_role` | `act_*` (26 casillas) | Rol secundario opcional (Sec 1.6.2) |
| 27 | `primary_language` | `lang_*` (20 casillas) | Lenguaje principal único (Sec 1.6.3) |
| 28 | `primary_framework` | `front_*` + `mobile_*` | Framework/plataforma principal (Sec 1.6.3) |
| 29 | `primary_database` | `db_*` (~15 casillas) | Base de datos principal (Sec 1.6.3) |
| 30 | `primary_cloud` | `infra_*` (parcial) | Plataforma de nube principal (Sec 1.6.3) |
| 31 | `primary_lang_years` | (nuevo) | Señal de profundidad (Sec 1.6.4) |
| 32 | `tech_breadth` | (nuevo) | Eje generalista vs. especialista (Sec 1.6.4) |
| 33 | `stack_change` | (nuevo) | Movilidad tecnológica 2 años (Sec 1.6.4) |
| 34 | `has_certs` | `cert_*` (27 casillas) | Binario: ¿alguna cert? (Sec 1.6.5) |
| 35 | `cert_category` | `cert_*` (27 casillas) | Categorías, máx 3 (Sec 1.6.5) |
| 36 | `cert_count` | (nuevo) | Número de certificaciones (Sec 1.6.5) |
| 37 | `all_technologies` | `dsc_*` + `dataeng_*` + restantes | Texto libre opcional (Sec 1.6.6) |

### Preguntas Nuevas de Política y Gancho (Secciones 2.2–2.7, 3.2)

| Bloque | # Qs | IDs |
|-------|-------|-----|
| Formalidad laboral (2.2) | 3 | `formal_contract`, `social_security`, `retirement_saving` |
| Dinámicas transfronterizas (2.3) | 4 | `employer_hq`, `payment_currency`, `cross_border_contract`, `cross_border_tax` |
| Poder adquisitivo (2.4) | 3 | `purchasing_power`, `housing_burden`, `financial_savings` |
| ROI educativo (2.5) | 4 | `edu_relevance`, `recent_training`, `first_job_degree`, `edu_debt` |
| Impacto IA (2.6) | 4 | `ai_tools_use`, `ai_task_change`, `ai_skill_confidence`, `ai_salary_impact` |
| Pipeline género y diversidad (2.7) | 4 | `first_code_age`, `childhood_computer`, `discrimination_exp`, `identity_visibility` |
| Gancho BP2C (3.2) | 3 | `enps`, `leave_reason`, `job_search` |

### Preguntas Eliminadas

| Bloque | Ítems eliminados |
|-------|-------------|
| Beneficios (`ben_*`) | 18 ítems |
| COVID-era (`covid_*`) | 5 ítems |
| `salarymx`, `salaryusd`, `extramx`, `extrausd` | 4 ítems (reemplazados por `base_salary` + `total_cash_annual`) |
| `variation` | 1 ítem (reemplazado por `salary_change` + `salary_change_reason`) |
| `experience` | 1 ítem (reemplazado por `experience_tech` + `experience_total`) |
| `seniority` | 1 ítem (reemplazado por `tenure_current`) |
| `profile` | 1 ítem (reemplazado por `seniority_level`) |
| `lang_*` (20), `front_*`, `mobile_*`, `db_*`, `infra_*`, `dsc_*`, `dataeng_*` | ~80 casillas (reemplazados por stack principal, Sec 1.6) |
| `cert_*` (27) | 27 casillas (reemplazados por `has_certs` + `cert_category` + `cert_count`) |
| `act_*` (26) | 26 casillas (reemplazados por `primary_role` + `secondary_role`) |
| `remote`, `covid_remoto` | 2 ítems (reemplazados por `work_arrangement`) |

### Cambio Neto

**Total final: 62 ítems**
- 12 retenidos (sin cambios o ajustes menores)
- 12 rediseñados desde campos existentes (Sec 1.5)
- 13 del rediseño de stack tecnológico (Sec 1.6)
- 25 nuevas preguntas de política y gancho (Secs 2.2–2.7, 3.2)
- **~165 ítems eliminados** (casillas, COVID, beneficios, campos redundantes)

La encuesta rediseñada reemplaza un instrumento de ~130 ítems dominado por casillas dispersos con 62 preguntas enfocadas — cada una con alta señal analítica por respuesta — mientras agrega bloques nuevos relevantes para política. El tiempo estimado baja de 25–35 minutos a 12–15 minutos.

---

## Evidencia de Simulación

Se ejecutó una simulación Monte Carlo (n=6,000 personas encuestadas sintéticos, seed=2026) para comparar el diseño viejo y el nuevo bajo condiciones idénticas de generación de datos. La DGP salarial usa tamaños de efecto calibrados del modelo real 2020–2022. Detalles completos: `SIMULATION_FINDINGS.md`; script reproducible: `simulation_old_vs_new.py`.

### Comparativo Principal

| Métrica | Diseño Antiguo | Diseño Nuevo | Cambio |
|--------|-----------|-----------|--------|
| Ítems de encuesta | 130 | 62 | −52% |
| Tiempo estimado de llenado | 30 min | 14 min | −53% |
| Predictores del modelo (k) | 90 | 72 | −20% |
| Respuestas útiles (post abandono) | 5,066 | 5,695 | +629 |
| **R²** | **0.340** | **0.490** | **+0.149** |
| R² ajustada | 0.328 | 0.483 | +0.155 |
| Error estándar de estimación | $22,928 | $20,158 | −$2,770 |
| R² por ítem | 0.0026 | 0.0079 | +202% |
| R² por minuto del encuestado | 0.011 | 0.035 | +208% |
| Información efectiva (R² × N) | 1,724 | 2,788 | +62% |
| CV medio bootstrap (estabilidad coef.) | 5.17 | 0.69 | −87% |

### De Dónde Viene la Nueva R²

Partiendo de los predictores equivalentes al diseño anterior (R² = 0.268), cada bloque nuevo agrega:

| Bloque | ΔR² | R² acumulada |
|-------|-----|---------------|
| `seniority_level` | **+0.124** | 0.392 |
| `company_size` | +0.024 | 0.416 |
| `english_use` | +0.018 | 0.449 |
| `primary_role` | +0.017 | 0.469 |
| `industry` | +0.015 | 0.431 |
| `primary_language` | +0.011 | 0.479 |
| `cert_depth` | +0.009 | 0.488 |
| `experience_total + tenure` | +0.003 | 0.452 |
| `tech_depth` | +0.002 | 0.490 |

**`seniority_level` por sí solo suma +12.4 pp** — más que todas las preguntas de stack tecnológico juntas. Este campo, ausente en el encuesta vieja, es el mayor hueco analítico que cierra el rediseño.

### Hallazgos Clave

1. **3× densidad de información por minuto.** Las personas entregan 3× más valor analítico por minuto. La eliminación de casillas es la principal responsable.
2. **87% más estabilidad de coeficientes.** Eliminar predictores binarios dispersos reduce los swings de coeficientes que hacían poco confiables los efectos por tecnología.
3. **+629 respuestas útiles.** El encuesta más corto retiene personas que antes abandonaban a mitad de la sección de casillas, reduciendo sesgo de selección hacia senior, hombres, CDMX.
4. **Las 25 preguntas de política no se modelan.** Los nuevos bloques (formalidad, transfronterizo, poder adquisitivo, ROI educativo, IA, pipeline de género) están diseñados para hallazgos propios, no predictores salariales. Su valor no se refleja en R² sino en los artefactos de advocacy que habilitan.

### Caveats

- Los resultados son de datos sintéticos calibrados a efectos 2020–2022. Los valores absolutos de R² (0.49) no deben citarse como predicción; lo importante es la comparación relativa entre diseños.
- Las tasas de completitud (85% viejo, 95% nuevo) son estimaciones de literatura de metodología de encuestas, no mediciones del instrumento real.
- El VIF es mayor en el diseño nuevo (media 2.58 vs 1.35) porque predictores relevantes se correlacionan entre sí. Ninguna variable supera VIF=10. El VIF bajo del diseño viejo refleja ruido disperso casi ortogonal, no mejor condicionamiento.
