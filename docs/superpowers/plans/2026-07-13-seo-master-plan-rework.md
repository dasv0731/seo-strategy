# Rework de seo-master-plan — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reenfocar seo-master-plan para que **consuma** los artefactos de arquitectura-seo / schema-graph / base-cliente en vez de regenerarlos, partiéndose en framing (§0–§2) y ensamblaje (§3–§14).

**Architecture:** Skill de proceso (referencias Markdown + SKILL.md). Alcance quirúrgico: se redirigen las secciones delegadas de "genera" a "consume", se añade una referencia nueva de flujo/contratos, y se verifica con subagentes en escenario (baseline vs con-skill). No hay código; el "test" es el comportamiento de un subagente leyendo la skill.

**Tech Stack:** Markdown. Verificación con subagentes (Task tool). Git (repo `Estrategia`).

**Spec:** `docs/superpowers/specs/2026-07-13-seo-master-plan-rework-design.md` (leer antes de empezar).

## Global Constraints

- **Repo único:** `C:\Users\Marke\Documents\Respaldo SEO\Nuevas skills\Estrategia\` (rama `main`). `~/.claude/skills/seo-master-plan` es junction a esta carpeta — editar aquí basta. Skill files: `SKILL.md`, `references/`, `templates/`.
- **Regla dura — consumir, no regenerar:** donde la skill decía "diseña la arquitectura / haz el estudio de keywords / diseña el grafo de schema", ahora dice "consume el artefacto de la skill dueña y añade la capa estratégica". Nunca re-derivar el árbol de URLs, los volúmenes de keywords ni el JSON-LD dentro de master.
- **Consumo híbrido:** referenciar el artefacto canónico como fuente de verdad + embeber un resumen compacto marcado como *derivado*. No duplicar el árbol completo.
- **Dos fases:** el framing NO escribe el archivo del spec; deja §0–§2 en el discovery doc + `enfoque.md`. El ensamblaje escribe el spec §0–§14 completo.
- **Rutas de salida del spec:** `Clientes\<slug>\docs\superpowers\{discovery,specs,plans}\`.
- **Handoff a arquitectura-seo:** el framing escribe `Clientes\<slug>\arquitectura\data\enfoque.md`.
- **Config de sitio:** se llama `sitio.yaml` (ya renombrado en G2), la emite arquitectura-seo. Nunca `estrategia.yaml` en texto nuevo.
- **NO TOCAR (🟢 intactos):** `references/00-parametrizacion-vertical.md`, `05-local-gbp.md`, `06-geo-eeat.md`, `10-kpis.md`, `11-competitive-linkbuilding.md`, `case-studies.md`, `templates/team-bio.md`, `templates/competitive-audit.md`.

---

## File Structure

- **Crear:** `references/00b-flujo-y-contratos.md` — flujo de dos fases, contrato de inputs consumidos, degradación, formato de `enfoque.md`, rama de escenarios.
- **Modificar (reescribir, 🟡):** `references/01-discovery.md`, `03-architecture.md`, `04-schema.md`, `07-technical-seo.md`, `08-keywords-clusters.md`, `09-content-roadmap.md`, `12-plan-phases.md`, `13-migracion-sitio-existente.md`, `templates/page-brief.md`, `templates/content-brief.md`.
- **Modificar (anclar/marcar):** `SKILL.md`, `references/02-spec-skeleton.md`.
- **Verificación:** carpeta temporal con cliente sintético (fixtures) + subagentes.

---

## Task 1: Referencia nueva de flujo y contratos + gancho en SKILL.md

**Files:**
- Create: `references/00b-flujo-y-contratos.md`
- Modify: `SKILL.md` (sección "El pipeline", "Índice de referencias", "Anti-patrones", "Cómo usar")

**Interfaces:**
- Produces: la referencia canónica `00b-flujo-y-contratos.md` que las Tasks 2–6 citan (`Ver references/00b-flujo-y-contratos.md`).

- [ ] **Step 1: Crear `references/00b-flujo-y-contratos.md`** con este contenido:

```markdown
# 00b · Flujo de dos fases y contratos de consumo

seo-master-plan **consume** artefactos de otras skills; no los regenera. Corre en dos momentos,
con arquitectura-seo en medio.

## Las dos fases

**FRAMING** (antes de arquitectura-seo):
- Lee `Clientes\<slug>\base\contexto-<slug>.md` (base-cliente). Si falta → entrevista de discovery
  (fallback) y sugiere base-cliente. No bloquea.
- Razona §0 panorama · §0.1 restricción dominante · §1 decisiones estratégicas · §2 elección de
  enfoque de arquitectura. NO escribe el spec: deja este razonamiento en el discovery doc +
  `enfoque.md`.
- Escribe el handoff `Clientes\<slug>\arquitectura\data\enfoque.md` (formato abajo) y
  `Clientes\<slug>\docs\superpowers\discovery\<fecha>-<slug>-discovery.md`.

**arquitectura-seo** corre (consume `enfoque.md`) → `arquitectura\resultados\arquitectura.csv`,
`enlazado.csv`, `mapa-keywords.csv` + `sitio.yaml`.

**ENSAMBLAJE** (después):
- Lee (requerido) `arquitectura\resultados\arquitectura.csv`, `enlazado.csv`, `mapa-keywords.csv`.
- Lee (opcional, Escenario A) el bundle de diagnóstico.
- Escribe el spec §0–§14 completo en `Clientes\<slug>\docs\superpowers\specs\<fecha>-<slug>-seo-design.md`
  y los planes en `...\plans\`.

## Formato de `enfoque.md` (lo consume arquitectura-seo Fase 0)

```
# Enfoque — <cliente>

**Qué priorizar:** <líneas/servicios a potenciar, derivado de la restricción dominante>
**Dimensiones de arquitectura:** <servicios | sectores | ubicaciones | especialidades ...>
**País/idioma:** <location_code / language_code, confirmado contra conexiones.json>
**Modelo de conversión:** <compra | lead | whatsapp | llamada | booking>
**Competidores conocidos:** <lista o "ninguno declarado">
```

## Contrato de inputs que consumo

| Artefacto | De | Sección que lo consume | Requerido |
|---|---|---|---|
| `base\contexto-<slug>.md` | base-cliente | §0, §7 (framing) | no (fallback entrevista) |
| `arquitectura\resultados\arquitectura.csv` | arquitectura-seo | §3 | **sí** (duro) |
| `arquitectura\resultados\enlazado.csv` | arquitectura-seo | §4 | sí |
| `arquitectura\resultados\mapa-keywords.csv` | arquitectura-seo | §9 | sí |
| bundle diagnóstico (hallazgos, interlinking, geo, cwv, linkbuilding, SCHEMA-REPORT, mapeo-301) | pipeline | §13, baseline | no (Escenario A) |

## Reglas de degradación

- Falta `arquitectura.csv` al ensamblar → **DETENERSE** y derivar a correr arquitectura-seo. No
  generar el árbol.
- Falta `contexto-<slug>.md` en framing → entrevista propia (fallback), sugiere base-cliente.
- Falta el bundle de diagnóstico (Escenario A) → ensamblar con lo que haya y marcar huecos como
  checklist de datos privada en §13. No fabricar.
- Falta salida de schema-graph → §5 se queda en anclaje estratégico + "generación pendiente: schema-graph".

## Rama de escenarios (por `estado del sitio` del discovery)

- `greenfield` | `básico` → **Escenario B**: arquitectura-seo modo greenfield (sin inventario/301);
  spec sabor foundation (§13 N/A); planes = fases de build.
- `con-tráfico` → **Escenario A**: fase de diagnóstico previa (master la CONSUME, no la corre);
  arquitectura-seo modo migración (inventario + `mapeo-301.csv`); spec sabor migración (§13 activo,
  KPI retención); planes con M0-M2 antes del build.

master **consume, no orquesta**: en el Escenario A lee los outputs del diagnóstico si existen; no
invoca las skills. El runtime que las encadena es orquestador-seo.
```

- [ ] **Step 2: Actualizar `SKILL.md` — sección del pipeline.** Reemplazar la descripción de "los 3 artefactos" para reflejar framing→arquitectura-seo→ensamblaje. Insertar, tras la línea del pipeline actual, el puntero: `El flujo de dos fases, los contratos de consumo y la rama de escenarios están en references/00b-flujo-y-contratos.md (leer al empezar).`

- [ ] **Step 3: Actualizar `SKILL.md` — índice de referencias.** Añadir la fila: `| references/00b-flujo-y-contratos.md | Al empezar — dos fases, contratos de consumo, degradación, escenarios |`.

- [ ] **Step 4: Actualizar `SKILL.md` — anti-patrones.** Añadir el bullet: `- **Regenerar el árbol de URLs, el estudio de keywords o el grafo de schema que ya producen arquitectura-seo / schema-graph** → duplicación y drift. master CONSUME esos artefactos; si faltan, se detiene y deriva.`

- [ ] **Step 5: Verificar consistencia.** Leer `SKILL.md` completo y confirmar que: (a) las 4 ediciones están, (b) el índice enlaza `00b`, (c) no quedó ninguna afirmación de que master "diseña la arquitectura" o "corre el estudio de keywords" en el cuerpo del SKILL. Corregir las que queden.

Run: `grep -niE "dise(ñ|n)a la arquitectura|estudio de keywords|genera el (á|a)rbol" SKILL.md`
Expected: 0 coincidencias que impliquen que master lo hace (solo referencias a "consume").

- [ ] **Step 6: Commit**

```bash
cd "C:/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia"
git add references/00b-flujo-y-contratos.md SKILL.md
git commit -m "rework(master): referencia de flujo/contratos + gancho en SKILL.md"
```

---

## Task 2: Reescribir `01-discovery.md` (framing + rama de escenarios + handoff enfoque.md)

**Files:**
- Modify: `references/01-discovery.md`

**Interfaces:**
- Consumes: `references/00b-flujo-y-contratos.md` (formato de `enfoque.md`, rama de escenarios).
- Produces: la definición de la fase FRAMING que las Tasks 3–6 asumen.

- [ ] **Step 1: Leer el archivo actual** `references/01-discovery.md` para preservar las preguntas estratégicas de los Niveles 1–4.

- [ ] **Step 2: Editar — marcar el intake factual como consumido.** En el Nivel 1 y Nivel 3, donde se piden datos de empresa (nombre legal, fundación, productos/servicios, personas/credenciales, casos, certificaciones), añadir al inicio de esas preguntas: `> Estos datos NO se re-preguntan: se leen de base\contexto-<slug>.md (base-cliente). Solo confirmar/rellenar huecos.` Mantener las preguntas ESTRATÉGICAS (alcance, modelo de conversión, render mode, estado del sitio, decision gates) como intake directo.

- [ ] **Step 3: Editar — añadir la sección "Salida del framing".** Al final del archivo, insertar:

```markdown
## Salida del framing (qué produce el discovery)

El discovery es la fase FRAMING. Produce dos artefactos (NO el spec):
1. `Clientes\<slug>\docs\superpowers\discovery\<fecha>-<slug>-discovery.md` — el discovery narrado.
2. `Clientes\<slug>\arquitectura\data\enfoque.md` — el handoff a arquitectura-seo (formato en
   `references/00b-flujo-y-contratos.md`), derivado de la restricción dominante (§0.1) y del enfoque
   de arquitectura elegido (§2).

Tras escribir `enfoque.md`, se corre arquitectura-seo. El spec §0–§14 se ensambla DESPUÉS.
```

- [ ] **Step 4: Editar — la pregunta "estado del sitio" ramifica el escenario.** Donde el Nivel 1 pregunta el estado del sitio, añadir: `Este campo ramifica todo (ver references/00b-flujo-y-contratos.md): greenfield/básico → Escenario B (foundation); con-tráfico → Escenario A (migración, con diagnóstico previo que master consume).`

- [ ] **Step 5: Verificar.** Confirmar que el archivo (a) conserva las preguntas estratégicas, (b) marca el intake factual como "de base-cliente", (c) define la salida `enfoque.md` + discovery doc, (d) enlaza la rama de escenarios.

Run: `grep -niE "enfoque.md|contexto-<slug>|estado del sitio|Escenario [AB]" references/01-discovery.md`
Expected: ≥4 coincidencias (las inserciones).

- [ ] **Step 6: Commit**

```bash
git add references/01-discovery.md
git commit -m "rework(master): 01-discovery = framing (consume contexto, escribe enfoque.md, rama escenarios)"
```

---

## Task 3: Reescribir `03-architecture.md` (consume el árbol — prohibición + recipe) [CRÍTICA]

**Files:**
- Modify: `references/03-architecture.md`
- Test: subagente en escenario (cliente sintético con `arquitectura.csv`)

**Interfaces:**
- Consumes: `arquitectura\resultados\arquitectura.csv` (14 columnas: url, nivel, padre, page_type, cluster_id, kw_principal, kw_secundarias, volumen_total, intencion, justificacion, prioridad, fase, accion, url_actual), `enlazado.csv`.

- [ ] **Step 1: RED baseline.** Dispatch un subagente con el prompt: *"Usando la skill seo-master-plan (lee su SKILL.md y references/03-architecture.md ACTUALES), y dado el cliente sintético en <carpeta> que YA tiene arquitectura\resultados\arquitectura.csv, produce la sección §3 (arquitectura de URLs) del spec."* Observar: ¿el agente re-diseña slugs/content-types desde cero (ignora el CSV)? Documentar el comportamiento verbatim. Esperado: REGENERA (confirma el problema).

- [ ] **Step 2: Leer** `references/03-architecture.md` actual. Identificar qué se queda (elección de enfoque = framing) y qué se redirige (diseño de URLs/slugs/content-types/internal-linking = consumir).

- [ ] **Step 3: Editar — mover la "elección de enfoque" al framing.** La tabla de enfoques (servicio/sector/matriz/especialidad-first) + el SERP reality check se marcan como **decisión del FRAMING (§2)** que alimenta `enfoque.md`. Encabezar esa parte con: `## §2 (FRAMING) — Elegir enfoque de arquitectura` y mantener su contenido.

- [ ] **Step 4: Editar — reemplazar el diseño de URLs por consumo (prohibición + recipe).** Sustituir las secciones de reglas de slug / content-types / anti-canibalización / internal-linking por:

```markdown
## §3 (ENSAMBLAJE) — Arquitectura de URLs: CONSUMIR el árbol

**NO diseñes el árbol de URLs aquí. Ya existe.** arquitectura-seo lo produjo en
`Clientes\<slug>\arquitectura\resultados\arquitectura.csv` (+ `arbol.html` visual, `enlazado.csv`).
Si te descubres escribiendo slugs, page-types o jerarquía desde cero, **DETENTE**: eso es
regenerar, no ensamblar.

**Si falta `arquitectura.csv`:** DETENERSE y derivar a correr arquitectura-seo. No lo generes tú.

**Recipe de consumo (híbrido):**
1. Lee `arquitectura.csv`. Es la fuente de verdad de §3 — referénciala como tal en el spec.
2. Embebe un **resumen compacto derivado**: el árbol de alto nivel (páginas core + hubs por
   dimensión + conteo de spokes por hub) y las páginas dinero (prioridad P1). Márcalo
   *"(derivado de arquitectura.csv; fuente de verdad ahí)"*.
3. Añade la **capa estratégica** que arquitectura-seo NO aporta: por qué esta arquitectura honra la
   restricción dominante (§0.1), qué page-types vigilar en los decision gates, y el racional de
   `accion` (keep/301/fusionar/eliminar) leído de la columna `accion` para sitio existente.
4. §4 internal linking: **consume `enlazado.csv`** igual (referencia + resumen del patrón
   hub-spoke + mix de anchor). No re-derives el enlazado.

**Reglas canónicas / anti-canibalización:** ya están resueltas en el árbol (columnas `page_type`,
`accion`, `intencion`). Aquí solo se **verifica** que el spec las refleja y se anota cualquier
conflicto de intención para los gates; no se re-deciden.
```

- [ ] **Step 5: GREEN — verificar consumo.** Dispatch un subagente con el mismo prompt del Step 1 pero contra la skill YA editada. Esperado: **referencia `arquitectura.csv`**, embebe un resumen marcado como derivado, añade capa estratégica, y NO re-deriva slugs. Si aún regenera → reforzar la prohibición (añadir a la lista de "DETENTE" el síntoma exacto observado) y re-testear.

- [ ] **Step 6: Commit**

```bash
git add references/03-architecture.md
git commit -m "rework(master): 03 consume arquitectura.csv (prohibicion + recipe), no regenera"
```

---

## Task 4: Reescribir `04-schema.md` y `08-keywords-clusters.md` (mismo patrón)

**Files:**
- Modify: `references/04-schema.md`, `references/08-keywords-clusters.md`

**Interfaces:**
- Consumes: `mapa-keywords.csv` (08); salida de schema-graph `SCHEMA-REPORT.md` (04).

- [ ] **Step 1: Editar `08-keywords-clusters.md`.** Reemplazar la metodología de estudio de keywords por consumo:

```markdown
# 09 · Keyword research y mapa por cluster — CONSUMIR

**NO corras el estudio de keywords aquí.** arquitectura-seo ya lo hizo:
`Clientes\<slug>\arquitectura\resultados\mapa-keywords.csv` (keyword, cluster_id, es_principal,
volumen, dificultad, cpc, tendencia, intencion, fuente). Si te descubres inventando volúmenes o
listas de keywords, **DETENTE**.

**Recipe:** referencia `mapa-keywords.csv` como fuente de verdad; embebe un resumen derivado (un
cluster por servicio flagship/secundario/sector/ubicación + tabla de total de páginas indexables
año 1, leída del árbol); añade la lectura estratégica (qué clusters son la apuesta del año 1 según
la restricción dominante). El análisis continuo (quick wins, canibalización) es de seo-analisis-gsc.
```

- [ ] **Step 2: Editar `04-schema.md`.** Recortar a anclaje + delegación:

```markdown
# 05 · Schemas y datos estructurados — ANCLAJE + delegación

master decide el **anclaje estratégico** del grafo: la entidad raíz (`Organization` | `Person` |
`LocalBusiness` | `OnlineStore` | `SoftwareApplication`…) según el rubro (00-parametrizacion) y la
restricción dominante, y qué entidades E-E-A-T la respaldan (§7).

**NO generes el JSON-LD aquí.** La generación del grafo conectado por @id para todo el dominio la
hace **schema-graph** (`Clientes\<slug>\schema-graph\` → `SCHEMA-REPORT.md`, snippets por página).

**Recipe:** en §5 del spec, declara el anclaje + la tabla schema/dónde/propósito a alto nivel +
"validación y generación → schema-graph". Si existe `SCHEMA-REPORT.md`, referéncialo; si no, anota
"generación pendiente: schema-graph".
```

- [ ] **Step 3: Verificar.** `grep -niE "DETENTE|CONSUMIR|schema-graph|mapa-keywords" references/04-schema.md references/08-keywords-clusters.md` → confirma el patrón en ambos.

- [ ] **Step 4: Commit**

```bash
git add references/04-schema.md references/08-keywords-clusters.md
git commit -m "rework(master): 04 (anclaje+schema-graph) y 08 (consume mapa-keywords)"
```

---

## Task 5: Recortar `07-technical-seo.md` a targets + anotar `09`, `13`, `12-plan-phases`

**Files:**
- Modify: `references/07-technical-seo.md`, `references/09-content-roadmap.md`, `references/13-migracion-sitio-existente.md`, `references/12-plan-phases.md`

- [ ] **Step 1: `07-technical-seo.md` — recortar a targets/requisitos.** Encabezar con: `master fija los OBJETIVOS técnicos (no los mide). Medición y crawl → extraccion / seo-vitals.` Conservar: render mode (decisión de discovery), CWV targets (passing 80% mobile, schema 100%, HTTPS 100%), IndexNow + Bing Webmaster (M1), foundation files (robots/llms/sitemap), regla de escala >~1.000 URLs. Recortar cualquier instrucción de CÓMO medir CWV o correr Lighthouse (eso es seo-vitals) → sustituir por "→ seo-vitals".

- [ ] **Step 2: `09-content-roadmap.md` — anotar delegación.** Insertar al inicio: `master planifica QUÉ y CUÁNDO (roadmap, cadencia, roles, longitudes). La REDACCIÓN de cada pieza → content-engine. La ESTRUCTURA de secciones de cada página → diseño-secciones.` No cambiar la metodología del roadmap.

- [ ] **Step 3: `13-migracion-sitio-existente.md` — anotar quién produce el 301.** Insertar donde se habla del inventario y el mapa 301: `El inventario (keep/improve/consolidate/kill) y el mapeo-301.csv los produce arquitectura-seo (modo migración, columna accion + mapeo-301.csv). master CONSUME esos artefactos y aporta la ESTRATEGIA de migración (KPI retención, ventanas de monitoreo, declarar la fluctuación, no combinar cambios).` Mantener el resto de la estrategia intacta.

- [ ] **Step 4: `12-plan-phases.md` — redirigir las fases de arquitectura/schema/keywords.** En las fases que generaban arquitectura/schema/keywords, sustituir "diseña/genera X" por "consume X de <skill> (ya producido)". Confirmar que las fases M0-M2 de migración referencian arquitectura-seo para inventario/301.

- [ ] **Step 5: Verificar.** Leer los 4 archivos y confirmar que ninguno instruye a master a medir CWV, redactar contenido, o generar el 301/keyword-study por su cuenta.

- [ ] **Step 6: Commit**

```bash
git add references/07-technical-seo.md references/09-content-roadmap.md references/13-migracion-sitio-existente.md references/12-plan-phases.md
git commit -m "rework(master): 07 targets, 09/13 delegacion, 12 consume artefactos"
```

---

## Task 6: Marcar `02-spec-skeleton.md` + anotar templates

**Files:**
- Modify: `references/02-spec-skeleton.md`, `templates/page-brief.md`, `templates/content-brief.md`

- [ ] **Step 1: `02-spec-skeleton.md` — etiquetar cada §.** En la lista de secciones §0–§14, añadir a cada una una etiqueta `[FRAMING]`, `[ENSAMBLAJE]` o `[CONSUME: <artefacto>]`:
  - §0, §0.1, §1, §2 → `[FRAMING]`
  - §3 → `[ENSAMBLAJE · CONSUME arquitectura.csv]` · §4 → `[ENSAMBLAJE · CONSUME enlazado.csv]`
  - §5 → `[ENSAMBLAJE · anclaje; genera schema-graph]` · §9 → `[ENSAMBLAJE · CONSUME mapa-keywords.csv]`
  - §6,§7,§8,§10,§11,§12,§13,§14 → `[ENSAMBLAJE]`

- [ ] **Step 2: `templates/page-brief.md` y `content-brief.md` — anotar delegación.** Insertar al inicio de cada uno: `Este brief = lista de páginas del árbol (arquitectura.csv) + notas estratégicas. La ESTRUCTURA de secciones la produce diseño-secciones; el COPY informacional largo, content-engine. No re-diseñes secciones ni redactes el cuerpo aquí.`

- [ ] **Step 3: Verificar.** `grep -c "\[FRAMING\]\|\[ENSAMBLAJE" references/02-spec-skeleton.md` → ≥14 etiquetas.

- [ ] **Step 4: Commit**

```bash
git add references/02-spec-skeleton.md templates/page-brief.md templates/content-brief.md
git commit -m "rework(master): etiqueta secciones del spec + delega estructura/copy en templates"
```

---

## Task 7: Verificación end-to-end por escenario

**Files:**
- Test: cliente sintético en carpeta temporal (fixtures)

- [ ] **Step 1: Construir fixtures.** Crear una carpeta temporal `Clientes-test\acme\` con: `base\contexto-acme.md` (negocio mínimo), `conexiones\conexiones.json` (slug/domain/location/language), y `arquitectura\resultados\arquitectura.csv` (5-8 filas con las 14 columnas: home, 2 hubs, 3 spokes, page_types y prioridades variadas), `enlazado.csv`, `mapa-keywords.csv`. Para Escenario A añadir `mapeo-301.csv` + un `hallazgos` mínimo.

- [ ] **Step 2: Test Escenario B (greenfield).** Subagente: *"Con seo-master-plan, cliente acme, estado=greenfield: corre el framing y luego el ensamblaje."* Verificar: escribe `enfoque.md` (con los 5 campos), luego el spec §0–§14 que **referencia arquitectura.csv** con resumen derivado, §13 marcado N/A, sin re-derivar el árbol.

- [ ] **Step 3: Test Escenario A (existente).** Subagente con `estado=con-tráfico` + bundle presente. Verificar: spec sabor migración (§13 activo, KPI retención), consume `mapeo-301.csv` y el bundle, planes con M0-M2.

- [ ] **Step 4: Test degradación.** Subagente con `arquitectura.csv` AUSENTE. Verificar: **se detiene y deriva a arquitectura-seo**; NO genera el árbol.

- [ ] **Step 5: Registrar resultados.** Escribir `tests/resultados-rework-<fecha>.md` con el veredicto de cada test (PASS/FAIL + evidencia). Si algún test falla → volver a la Task correspondiente, reforzar prohibición/recipe, re-testear.

- [ ] **Step 6: Commit**

```bash
git add tests/resultados-rework-*.md
git commit -m "rework(master): verificacion end-to-end por escenario (greenfield/existente/degradacion)"
```

---

## Self-Review (del plan contra el spec)

- **Cobertura:** §1 spec (dos fases) → Task 1,2. §2 (contratos/degradación) → Task 1. §3 (escenarios) → Task 1,7. §4 (alcance quirúrgico archivo-por-archivo) → Tasks 2–6 (cada 🟡 tiene su task; 🟢 en Global Constraints "NO TOCAR"; 🔵 en Task 1). §5 (verificación, riesgo #1 prohibición+recipe) → Task 3 (RED/GREEN) + Task 7.
- **Sin placeholders:** el contenido nuevo (00b, prohibición+recipe de 03, formato enfoque.md, recipes de 04/08) va verbatim; los recortes/anotaciones dan la frase exacta a insertar.
- **Consistencia de nombres:** `arquitectura.csv`, `enlazado.csv`, `mapa-keywords.csv`, `enfoque.md`, `sitio.yaml`, `mapeo-301.csv`, `SCHEMA-REPORT.md`, `contexto-<slug>.md` — usados igual en todas las tasks.
```
