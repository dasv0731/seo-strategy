# G4 · Rework de orquestador-seo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reworkear el CONTENIDO de la skill `orquestador-seo` para que delegue el alta y enrute a las skills dueñas del ecosistema SEO por cliente (con `claude-seo:*` como gap-filler), sobre la raíz `Clientes\<slug>\`, con un modelo de fases espejo de los escenarios A/B.

**Architecture:** Es un rework de documentación/contenido de skill, sin código ejecutable. Los archivos viven en el repo git `~/.claude/skills/orquestador-seo/` (remote `dasv0731/orquestador-seo`). Se reescriben `SKILL.md`, `references/02-contratos.md`, `README.md`, `INSTALL.md`; se borran `plantilla-cliente/`, `references/00-alta-cliente.md`, `references/01-credenciales-agencia.md`. La verificación es por grep de sanidad + lectura de las dos secuencias A/B, no por pytest.

**Tech Stack:** Markdown. Git. `rg`/Grep para verificación.

## Global Constraints

- **Raíz de cliente única:** `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`. Prohibido `~/seo-clientes/`, `PROJECT.md`, `REGISTRO.md`, `conexiones.md` (sin `.json`), repo git por cliente.
- **orquestador = runtime, skill** (no agente). **master = artefacto.** El orquestador enruta, no hace SEO.
- **claude-seo:* = gap-filler explícito** (solo lo sin dueño: content-brief, single-page ad-hoc, hreflang, fallback). Nunca fuente primaria de datos cuando existe la skill dueña.
- **Alta = delegar + secuenciar:** crear `Clientes\<slug>\` → `seo-setup-cliente` → `base-cliente`. El orquestador NO reimplementa alta.
- **Espina del master (post-G3):** FRAMING (§0–§2 → `arquitectura\data\enfoque.md`) ANTES de arquitectura-seo; ENSAMBLAJE (§3–§14 → spec+planes) DESPUÉS de consumir el árbol.
- **Editar la ubicación instalada** `~/.claude/skills/orquestador-seo/` (es el propio repo con remote).
- Fuente de verdad del mapa: `Estrategia\docs\rework\contratos-conexiones.md` y el diseño `…-g4-orquestador-seo-rework-design.md`.

---

### Task 1: Rama limpia + commit del pendiente

**Files:**
- Modify: `~/.claude/skills/orquestador-seo/SKILL.md` (solo estado git; hay 1 línea sin commitear)

**Interfaces:**
- Consumes: nada.
- Produces: repo `orquestador-seo` en rama `g4-rework`, working tree limpio, listo para el rework.

- [ ] **Step 1: Ver el estado**

Run:
```bash
cd ~/.claude/skills/orquestador-seo && git status --short && git branch --show-current
```
Expected: `M SKILL.md`, branch `main`. (La línea pendiente añade la heurística de `diseno-secciones`, ya consistente con el rework.)

- [ ] **Step 2: Crear la rama y commitear el pendiente**

Run:
```bash
cd ~/.claude/skills/orquestador-seo
git checkout -b g4-rework
git add SKILL.md
git commit -m "chore: heurística diseno-secciones (pendiente pre-G4)"
```
Expected: nuevo commit; working tree limpio.

- [ ] **Step 3: Verificar árbol limpio**

Run: `cd ~/.claude/skills/orquestador-seo && git status --short`
Expected: sin salida (limpio).

---

### Task 2: Reescribir `references/02-contratos.md` (mapa canónico de routing)

**Files:**
- Modify (overwrite): `~/.claude/skills/orquestador-seo/references/02-contratos.md`

**Interfaces:**
- Consumes: la línea de estado limpia de Task 1.
- Produces: `02-contratos.md` con (a) raíz `Clientes\<slug>\`, (b) mapa I/O por skill, (c) secuencias A/B, (d) capas de frontera con dueñas del ecosistema, (e) experimento 3↔5 preservado. `SKILL.md` (Task 3) lo referenciará.

- [ ] **Step 1: Sobrescribir el archivo con este contenido exacto**

```markdown
# 02 · Contratos de estado y routing (mapa vivo, NO contrato congelado)

Este documento hace **legible** el estado compartido que las skills del ecosistema producen y
consumen de facto, y es el **mapa de routing** del orquestador. **No fija fronteras**: las describe
con un *estado* explícito. La frontera correcta solo se valida ejecutando.

> **Cómo leerlo.** El estado evita que esto osifique:
> - 🟢 **firme** — invariante o validada por ejecución; el corte no está en duda.
> - 🟡 **en prueba** — frontera bajo experimento activo; **no** tratar como cerrada.
> - 🔴 **de riesgo** — vigilar; primera candidata a re-cortar si la ejecución lo pide.

El estado compartido es la fuente única de verdad. Las skills de diseño lo escriben; las de
ejecución lo leen. El orquestador solo gestiona estado, gates de dependencia y la arista de retorno
(`SKILL.md` → *Regla de conflicto*). No toma decisiones de SEO.

---

## 0. Sustrato: la carpeta-contrato canónica

Raíz única por cliente: `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`. Las skills se
comunican dejando/leyendo archivos ahí y tablas en `data\seo.db` — **no se llaman entre sí**.
No hay repo git por cliente ni REGISTRO central: la carpeta + `seo.db` son la verdad.

Artefactos clave: `conexiones\conexiones.json` (seo-setup), `data\seo.db` (setup crea, sync puebla),
`base\contexto-<slug>.md` (base-cliente), `sitio.yaml` (arquitectura-seo emite),
`arquitectura\resultados\*.csv` + `arquitectura\data\enfoque.md`, `schema-graph\`, `resultados\`
(interlinking), `cwv\` (seo-vitals), `geo\` (geo-audit), `linkbuilding\`, `secciones\<slug-pagina>\`,
`docs\superpowers\{discovery,specs,plans}\` (master).

---

## 1. Mapa producto/consumo por skill (normalizado a `Clientes\<slug>\`)

| Skill | LEE (input) | ESCRIBE (output) |
|---|---|---|
| **base-cliente** | docs/fuentes; opcional crawl de extraccion | `base\` + `base\contexto-<slug>.md` |
| **seo-setup-cliente** | credenciales (google-api.json, ~/.claude.json) | `conexiones\conexiones.json` + `data\seo.db` |
| **seo-sync** | conexiones.json + APIs (GSC/GA4/Clarity/DataForSEO) | puebla `seo.db` |
| **extraccion** | `sitio.yaml`, plantillas SF | `data\*.csv` + `page_source\` + `historico\<fecha>\` |
| **arquitectura-seo** | `base\`, `conexiones\`, `keywords\`, seo.db (GSC), `arquitectura\data\enfoque.md`, `inventario\` (si existe) | `arquitectura\resultados\{arquitectura.csv, enlazado.csv, mapeo-301.csv, mapa-keywords.csv}` + `sitio.yaml` |
| **seo-master-plan** | `contexto-<slug>.md`, `arquitectura.csv`, `enlazado.csv`, `mapa-keywords.csv`, bundle de diagnóstico | FRAMING: `arquitectura\data\enfoque.md`; ENSAMBLAJE: `docs\superpowers\{specs,plans}\` |
| **diseno-secciones** | `keywords\`, seo.db, `page_source\` | `secciones\<slug-pagina>\{01,02,03}` |
| **schema-graph** | `data\*.csv` + `page_source\` | `schema-graph\` (snippets, SCHEMA-REPORT.md) |
| **interlinking** | `data\all_inlinks.csv` + `internal_html.csv`, `sitio.yaml` | `resultados\` (métricas, grafos, tablero) |
| **html-semantico** | HTML/URL ad hoc | informe en chat |
| **content-engine** | tema/.docx, KB (silo aparte) | `Herramientas\SEO Blogs\content-engine\proyectos\<empresa>\` |
| **seo-vitals** | `conexiones`/`sitio.yaml`, `data\*.csv`, CrUX | `cwv\seo.db` + `informes\CWV-<fecha>.md` |
| **seo-analisis** | seo.db + crawl + DinoRank | tabla `hallazgos` + `analisis\*.md` |
| **seo-analisis-gsc** | seo.db (GSC) + HTTP propio | tabla `url_status` + reportes chat |
| **seo-cambios** | seo.db (GSC/GA4/Clarity/ranks) | tabla `changes_log` + veredictos |
| **seo-dashboard** | seo.db (hallazgos, url_status, GSC) + clusters.json | `reportes\dashboard.html` + `clusters.json` |
| **linkbuilding** | conexiones, GSC CSV, clusters.json, DinoRank/DataForSEO | tabla `lb_backlinks` + pipeline + `linkbuilding\informes\` |
| **geo-audit** | seo.db, `geo\geo.yaml`, `base\`, `sitio.yaml` | hallazgos GEO + scores en seo.db + `geo\informes\` |
| **claude-seo:*** (gap-filler) | ad hoc | content-brief, auditoría single-page, hreflang |

---

## 2. Secuencias por escenario

**Espina común** (master partido alrededor de arquitectura-seo):
`base-cliente → master FRAMING (§0–§2 → enfoque.md) → arquitectura-seo → master ENSAMBLAJE (§3–§14)`.

**Escenario A — existente** (diagnosticar → rediseñar → migrar → monitorear):
```
0. seo-setup-cliente + base-cliente
1. seo-sync BACKFILL ∥ extraccion crawl
2. DIAGNÓSTICO: seo-analisis · seo-analisis-gsc · interlinking · schema-graph · geo-audit · seo-vitals · linkbuilding
3. master FRAMING → enfoque.md
4. arquitectura-seo (migración → arquitectura.csv + mapeo-301.csv)
5. master ENSAMBLAJE → spec MIGRACIÓN + planes
6. Ejecución: diseno-secciones · content-engine · schema-graph
7. MONITOREO: seo-cambios · seo-dashboard · re-auditorías · seo-sync diario
```

**Escenario B — greenfield** (diseñar → construir → validar → lanzar → monitorear):
```
0. seo-setup-cliente + base-cliente
1. master FRAMING → enfoque.md
2. arquitectura-seo (greenfield: estudio de kws → árbol, sin inventario/301)
3. master ENSAMBLAJE → spec FOUNDATION + planes
4. BUILD: diseno-secciones · content-engine · schema-graph
5. VALIDACIÓN pre-launch: seo-vitals · geo-audit · interlinking · html-semantico
6. LAUNCH: sitemap + IndexNow
7. MONITOREO: seo-sync captura → converge con A
```
A y B convergen en el **monitoreo con seo.db poblado**.

---

## 3. Capas de frontera (dónde vive cada responsabilidad)

### Capa 1 — Diseño (gate secuencial)

| # | Responsabilidad | Dónde vive hoy | Entrega (clave) | Frontera |
|---|---|---|---|---|
| 1 | Mapeo negocio + intención | master FRAMING §0–§1 + base-cliente | `enfoque.md` + params de nicho | 🟢 firme |
| 2 | Dimensionamiento de demanda | arquitectura-seo (estudio de kws) | `mapa-keywords.csv` (volúmenes + veredicto) | 🟢 firme |
| 3 | Taxonomía / tipos de página | arquitectura-seo → `arquitectura.csv` | árbol de tipos de página | 🟡 **en prueba (3↔5)** |
| 4 | Convención de URLs | arquitectura-seo (plegada en 3) | patrón por clase de URL | 🟢 firme |
| 5 | Enlazado interno | arquitectura-seo `enlazado.csv` · interlinking (verificación) | reglas de enlace + flujo a money pages | 🟡 **en prueba (3↔5)** |

### Capa 3 — Medición como gate (antes de ejecutar)

| # | Responsabilidad | Dónde vive hoy | Hecho | Frontera |
|---|---|---|---|---|
| 10 | Medición e instrumentación | seo-setup-cliente (crea `changes_log`) · seo-sync (baseline) · seo-cambios (`report.py beforeafter`) · seo-dashboard | todo cambio rastreable a un veredicto | 🟢 firme (gate, no fase final) |

### Capa 2 — Ejecución (loops concurrentes)

| # | Responsabilidad | Dónde vive hoy | Frontera |
|---|---|---|---|
| 6 | Rastreo / indexabilidad | extraccion (crawl) · arquitectura-seo · seo-analisis-gsc + **modo de render** | 🔴 de riesgo (render enreda 6↔8) |
| 7 | Contenido + on-page (+schema) | diseno-secciones · content-engine · schema-graph · seo-analisis | 🟢 firme |
| 8 | Rendimiento | seo-vitals (CWV, CrUX) + **modo de render** | 🔴 de riesgo (render enreda 6↔8) |
| 9 | Off-page / autoridad | linkbuilding | 🟢 firme (track separado continuo) |

### Capa 3 — Gobierno continuo

| # | Responsabilidad | Dónde vive hoy | Frontera |
|---|---|---|---|
| 11 | Revisión de obsolescencia | decision gates del master + seo-cambios (regresión) + seo-dashboard | 🟡 mecanismo añadido, sin correr aún |

---

## 4. Costuras transversales (no son skills; varias las heredan)

- **Modo de render (CSR/SSR/estático)** → decisión de arquitectura que **6 y 8 heredan a la vez**.
  Se decide en discovery (master FRAMING) y se declara en `sitio.yaml`/spec. Por eso 6 y 8 están 🔴.
  Crítico en sitios programáticos: si las páginas a escala son CSR, la % de indexación se desploma.
- **i18n** → módulo condicional; único caso gap-filler estructural → `claude-seo:seo-hreflang`.

---

## 5. La frontera 🟡 en prueba: taxonomía (3) ↔ enlazado (5)

Frontera de **mayor riesgo**, **no se decide en escritorio**. Hoy `arquitectura.csv` (taxonomía) y
`enlazado.csv` los emite arquitectura-seo; interlinking verifica el enlazado real contra ellos.
Pregunta abierta: ¿taxonomía y enlazado son un corte o dos?

**Cómo se resuelve (instrumentado):** experimento en **metalectro** (6 clusters, baselines
congelados). Cada cambio se registra con seo-cambios (`logchange --area taxonomia|enlazado|ambos`);
el veredicto sale de `report.py --report covariacion`:
- ≥60% de cambios tocó `ambos` → **fusionar 3 y 5** (🟢).
- ≤30% → **mantener separadas** (🟢).
- zona gris → seguir 🟡, registrar más.

Cuando el veredicto llegue con alta confianza, **se actualiza este documento y el spec**.

---

## 6. Qué NO es este documento

- **No** es la re-arquitectura a contrato tipado de las skills (se difiere hasta que la ejecución
  valide las fronteras).
- **No** congela ningún corte: las filas 🟡/🔴 son provisionales.
- **No** reemplaza a los SKILL.md: los mapea, para que el orquestador valide handoffs.
```

- [ ] **Step 2: Verificar que no queden dueñas viejas ni rutas prohibidas**

Run: `rg -n "seo-clientes|PROJECT\.md|REGISTRO|claude-seo:seo-technical|claude-seo:seo-performance|claude-seo:seo-backlinks" ~/.claude/skills/orquestador-seo/references/02-contratos.md`
Expected: sin salida (ninguna dueña vieja ni ruta prohibida).

- [ ] **Step 3: Commit**

```bash
cd ~/.claude/skills/orquestador-seo
git add references/02-contratos.md
git commit -m "ref(02-contratos): mapa producto/consumo del ecosistema + secuencias A/B (raíz Clientes\\)"
```

---

### Task 3: Reescribir `SKILL.md`

**Files:**
- Modify (overwrite): `~/.claude/skills/orquestador-seo/SKILL.md`

**Interfaces:**
- Consumes: `references/02-contratos.md` (Task 2, referenciado desde el cuerpo).
- Produces: `SKILL.md` con bootstrap delegado, tabla de división de labor del ecosistema, ciclo A/B, gate de medición y regla de conflicto re-anclada a seo-cambios. No referencia `references/00`/`01` (se borran en Task 4).

- [ ] **Step 1: Sobrescribir el archivo con este contenido exacto**

````markdown
---
name: orquestador-seo
description: Use as the single entry point for a complete SEO engagement. Conducts the full lifecycle (bootstrap → diagnosis/framing → architecture → spec/plans → build/validation → monitor) by routing each phase to the OWNING skill of the ecosystem (base-cliente, seo-setup-cliente, seo-sync, extraccion, arquitectura-seo, seo-master-plan, diseno-secciones, schema-graph, interlinking, geo-audit, seo-vitals, linkbuilding, seo-analisis, seo-analisis-gsc, seo-cambios, seo-dashboard, content-engine); claude-seo:* only fills gaps. Triggers on "proyecto SEO completo", "orquestar SEO", "estrategia + auditoría SEO", "plan SEO con datos en vivo", "llevar un cliente SEO de principio a fin".
---

# Orquestador SEO

Punto de entrada único de un proyecto SEO completo. **No hace el trabajo: lo enruta** a la skill dueña de cada capacidad y resuelve los conflictos entre la estrategia y los datos reales.

## Frontera (invariante)

- El orquestador es **skill** y es **runtime**: secuencia skills, gestiona estado/gates y aplica la arista de retorno. No toma decisiones de SEO.
- `seo-master-plan` = **artefacto** (spec §0–§14 + planes). El orquestador lo invoca; no lo suplanta.
- **Sustrato de comunicación:** las skills no se llaman entre sí; dejan/leen archivos en la carpeta del cliente `Clientes\<slug>\` y tablas en `data\seo.db`. El mapa producto/consumo vive en `references/02-contratos.md`.

## División de labor (la regla mental)

Cada capacidad tiene UNA skill dueña. `claude-seo:*` es **gap-filler**: solo para lo que el ecosistema no cubre.

| Dominio | Skill dueña |
|---|---|
| Estrategia, spec §0–§14, planes, KPIs/gates, principios, migración | **seo-master-plan** (CONSUME artefactos) |
| Árbol de URLs + estudio de keywords | **arquitectura-seo** (`arquitectura.csv`, `enlazado.csv`, `mapeo-301.csv`, `mapa-keywords.csv`, `sitio.yaml`) |
| Conocimiento de negocio | **base-cliente** (`base\contexto-<slug>.md`) |
| Conexiones + poblar/actualizar seo.db | **seo-setup-cliente** (alta) · **seo-sync** (ingesta) |
| Crawl del sitio (HTML, schemas, issues, inlinks) | **extraccion** |
| Diagnóstico de datos (huérfanas, index bloat, CTR, quick wins, canibalización, 404) | **seo-analisis** · **seo-analisis-gsc** |
| PageRank interno / enlazado real | **interlinking** |
| JSON-LD conectado del dominio | **schema-graph** |
| Visibilidad/citability AI | **geo-audit** |
| Core Web Vitals | **seo-vitals** |
| Backlinks / off-page | **linkbuilding** |
| Secciones/layout/copy de UNA página | **diseno-secciones** |
| Redacción informacional (silo aparte) | **content-engine** |
| Veredicto antes/después de un cambio | **seo-cambios** |
| Reporte / dashboard | **seo-dashboard** |
| **Gap-filler** (content-brief competitivo, auditoría single-page ad-hoc, hreflang/i18n, fallback si falta una skill propia) | **claude-seo:*** |

El orquestador nunca duplica: si una capacidad existe en una skill, se delega.

## Dependencias (verificar antes de empezar)

Skills del ecosistema esperadas en `~/.claude/skills/` (repos privados en `dasv0731`): `seo-master-plan`, `arquitectura-seo`, `base-cliente`, `seo-setup-cliente`, `seo-sync`, `extraccion`, `seo-analisis`, `seo-analisis-gsc`, `interlinking`, `schema-graph`, `geo-audit`, `seo-vitals`, `linkbuilding`, `diseno-secciones`, `seo-cambios`, `seo-dashboard`, `content-engine`. Gap-filler: `claude-seo` (se auto-carga como `claude-seo@skills-dir`).

Si falta una skill crítica para la fase en curso, detente y avisa. Comprueba con `claude plugin list` y `ls ~/.claude/skills/`.

## Multi-cliente (agencia)

Cada cuenta es un **proyecto aislado** con su carpeta canónica `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\`. El working dir al trabajar un cliente es esa carpeta → la **memoria nativa de Claude Code queda aislada por cliente** (se indexa por ruta de proyecto). **No hay repo git por cliente ni REGISTRO central**: la carpeta + `data\seo.db` son la fuente de verdad.

Credenciales = **agencia, una sola vez**: service account de Google en `~/.config/claude-seo/google-api.json` (con acceso al GSC/GA4 de cada cliente), login DataForSEO, tokens DinoRank/Clarity con scope local en `~/.claude.json`. Las gestiona **seo-setup-cliente**; el orquestador no las documenta de nuevo. Nunca hay secretos en `Clientes\`.

### Fase 0.0 · Bootstrap de cliente (delegado)
Da de alta una cuenta nueva secuenciando skills dueñas — **no reimplementa alta**:
1. Crear `Clientes\<slug>\` (slug kebab-case, minúsculas, sin tildes/espacios).
2. **seo-setup-cliente** → `conexiones\conexiones.json` + `data\seo.db`.
3. **base-cliente** → `base\` + `base\contexto-<slug>.md`.

**Gate de arranque:** no entrar al ciclo sin `conexiones\conexiones.json`, `data\seo.db` y `base\contexto-<slug>.md`.

## El ciclo (por escenario)

**Fase 0 · Determinar el escenario.** ¿Hay sitio vivo con GSC/GA4 pobladas y contenido que crawlear? → **A (existente)**. ¿No hay sitio ni datos? → **B (greenfield)**.

**Espina común** (el master se parte en FRAMING y ENSAMBLAJE alrededor de arquitectura-seo):
`base-cliente → master FRAMING (§0–§2 → arquitectura\data\enfoque.md) → arquitectura-seo (árbol) → master ENSAMBLAJE (§3–§14 → spec+planes)`.

Crea un todo por paso y vuelve a pasos anteriores cuando los datos lo exijan (Regla de conflicto).

### Escenario A — existente (diagnosticar → rediseñar → migrar → monitorear)
```
0. seo-setup-cliente + base-cliente                          (Fase 0.0)
1. seo-sync BACKFILL  ∥  extraccion crawl                    (paralelo)
2. DIAGNÓSTICO (leen lo de 1):
     seo-analisis · seo-analisis-gsc · interlinking ·
     schema-graph · geo-audit · seo-vitals · linkbuilding
3. seo-master-plan FRAMING (§0–§2 → enfoque.md; restricción dominante)
4. arquitectura-seo (modo migración → arquitectura.csv + mapeo-301.csv)
5. seo-master-plan ENSAMBLAJE (§3–§14 → spec sabor MIGRACIÓN + planes)
6. Ejecución: diseno-secciones · content-engine · schema-graph
7. MONITOREO: seo-cambios (logchange + veredicto) · seo-dashboard ·
     re-corridas geo-audit/seo-vitals/linkbuilding · seo-sync diario
```

### Escenario B — greenfield (diseñar → construir → validar → lanzar → monitorear)
```
0. seo-setup-cliente + base-cliente                          (Fase 0.0)
1. seo-master-plan FRAMING (§0–§2 → enfoque.md)
2. arquitectura-seo (modo greenfield: estudio de kws → árbol nuevo, sin inventario/301)
3. seo-master-plan ENSAMBLAJE (§3–§14 → spec sabor FOUNDATION + planes)
4. BUILD: diseno-secciones (modo propuesta) · content-engine · schema-graph
5. VALIDACIÓN pre-launch (staging): seo-vitals · geo-audit · interlinking · html-semantico
6. LAUNCH: sitemap + IndexNow + solicitar indexación
7. MONITOREO: seo-sync empieza a capturar GSC/GA4 → converge con Escenario A
```
A y B convergen en el **monitoreo con seo.db poblado**.

## Gate de medición (antes de abrir cualquier loop de ejecución)

La medición es **pre-requisito, no fase final**. Antes de tocar contenido/técnico/enlazado (ejecución) debe existir: **baseline** registrado (crawl + `seo.db` con GSC/GA4 vía seo-sync) y **`changes_log` activo** para marcar el antes/después. Sin esto, los loops corren a ciegas. Lo instala **seo-setup-cliente** (crea `changes_log`) + **seo-sync** (puebla el baseline); cada cambio se registra con **seo-cambios** (`logchange`).

## Regla de conflicto + arista de retorno (el corazón del orquestador)

Cuando los **datos contradicen un supuesto del spec**, ganan los datos — pero **no todo dato es señal**. Clasifica el veredicto (lo emite **seo-cambios**: `changes_log` → `report.py --report beforeafter`) en 3 ramas:

1. **Alta confianza (`mejora` / `regresion`)** → propaga. Si confirma el supuesto, refuerza el criterio; si lo **invalida**, reabre el gate de diseño (FRAMING/arquitectura-seo).
2. **`no_determinable`** (muestra o madurez insuficiente) → **NO propaga.** El ruido no reescribe criterios ("aprender de fantasmas"). Espera más datos.
3. **`sin_efecto`** (datos suficientes, sin movimiento) → nulo confiable; registra que no movió la aguja, no reabras diseño.

Ejemplos de conflicto que (con veredicto de alta confianza) ajustan la estrategia:
- Volumen real insuficiente para un spoke planeado → **no abrir el spoke** (anti-thin; arquitectura-seo / master §9).
- Una página secundaria gana impresiones por la query objetivo → **redirigir el canonical** (anti-canibalización; seo-analisis-gsc + arquitectura-seo).
- Auditoría revela deuda técnica que mata CWV (seo-vitals) → **priorizar lo técnico** antes de escalar contenido.
- Competidor domina un cluster con autoridad inalcanzable → **re-priorizar clusters** hacia gaps reales (linkbuilding).

Nunca forzar el plan contra la evidencia, **pero tampoco dejar que el ruido lo reescriba**.

## Estado compartido y costuras transversales

El estado compartido (`Clientes\<slug>\` + `seo.db`) es la **fuente única de verdad**: las skills de diseño escriben, las de ejecución leen. El mapa producto/consumo por skill, con su estado de frontera (🟢 firme / 🟡 en prueba / 🔴 de riesgo) y el experimento vivo 3↔5, está en `references/02-contratos.md`. Consúltalo ante cualquier duda de "a quién le toca".

Algunas decisiones **no pertenecen a una sola skill** (costuras que varias heredan):
- **Modo de render (CSR/SSR/estático)** — se decide una vez en discovery (master FRAMING) y lo heredan a la vez la **indexabilidad** (crawl de extraccion + arquitectura-seo) y el **rendimiento** (seo-vitals). Crítico en sitios programáticos: si las páginas a escala son CSR, la % de indexación se desploma; verificar el render **antes** de escalar contenido.
- **i18n** — módulo condicional; único caso gap-filler estructural → `claude-seo:seo-hreflang`. Solo si el negocio es multi-región.

## Cómo decidir qué invocar (heurística rápida)

- ¿Estructura, arquitectura, árbol de URLs o estudio de kws? → **arquitectura-seo** (y el master lo consume).
- ¿Estrategia, spec, planes, principios o KPIs? → **seo-master-plan**.
- ¿Un número real, un estado actual o validar en vivo? → la skill dueña del dominio (seo-vitals CWV, geo-audit AI, linkbuilding backlinks, interlinking enlazado, seo-analisis/gsc datos).
- ¿Secciones/layout/copy de UNA página? → **diseno-secciones**.
- ¿Una pieza de contenido informacional? → **content-engine** (brief competitivo con `claude-seo:seo-content-brief` si aplica).
- ¿Algo sin dueño en el ecosistema (hreflang, auditoría single-page ad-hoc)? → **claude-seo:*** (gap-filler).

## Anti-patrones

- **Saltarse Fase 0 / la restricción dominante** → plan sin ancla.
- **Construir el spec con volúmenes estimados** cuando arquitectura-seo da reales → decisiones sobre arena.
- **Duplicar trabajo** (rehacer a mano lo que una skill ya hace) → enruta, no reimplementes.
- **Usar claude-seo como fuente primaria** cuando existe la skill dueña → rompe el modelo gap-filler.
- **Ignorar la Regla de conflicto** o dejar que el ruido reescriba el plan → spec bonito que no rankea, o aprender de fantasmas.
- **Ejecutar sin el Gate de medición** (baseline + changes_log) → cambios sin veredicto defendible.
````

- [ ] **Step 2: Verificar sanidad (rutas viejas, dualidad vieja, refs muertas)**

Run: `rg -n "seo-clientes|PROJECT\.md|REGISTRO|conexiones\.md|references/00|references/01|QUÉ ES HOY" ~/.claude/skills/orquestador-seo/SKILL.md`
Expected: sin salida.

- [ ] **Step 3: Verificar que enruta al ecosistema y a 02-contratos**

Run: `rg -n "arquitectura-seo|base-cliente|seo-cambios|seo-vitals|linkbuilding|geo-audit|references/02-contratos" ~/.claude/skills/orquestador-seo/SKILL.md | wc -l`
Expected: número ≥ 6 (varias menciones a skills del ecosistema + la ref a 02-contratos).

- [ ] **Step 4: Commit**

```bash
cd ~/.claude/skills/orquestador-seo
git add SKILL.md
git commit -m "SKILL: rework G4 — routing al ecosistema, bootstrap delegado, ciclo A/B, gap-filler claude-seo"
```

---

### Task 4: Borrar artefactos de alta obsoletos

**Files:**
- Delete: `~/.claude/skills/orquestador-seo/plantilla-cliente/` (árbol completo)
- Delete: `~/.claude/skills/orquestador-seo/references/00-alta-cliente.md`
- Delete: `~/.claude/skills/orquestador-seo/references/01-credenciales-agencia.md`

**Interfaces:**
- Consumes: `SKILL.md` (Task 3) ya no referencia estos archivos.
- Produces: repo sin scaffolding de alta superseded.

- [ ] **Step 1: Confirmar que nada los referencia**

Run: `rg -n "plantilla-cliente|00-alta-cliente|01-credenciales" ~/.claude/skills/orquestador-seo/SKILL.md ~/.claude/skills/orquestador-seo/references/02-contratos.md`
Expected: sin salida. (Si aparece algo, corregir la referencia ANTES de borrar.)

- [ ] **Step 2: Borrar con git**

Run:
```bash
cd ~/.claude/skills/orquestador-seo
git rm -r plantilla-cliente references/00-alta-cliente.md references/01-credenciales-agencia.md
```
Expected: git lista los archivos como eliminados.

- [ ] **Step 3: Verificar que solo queda 02-contratos en references**

Run: `ls ~/.claude/skills/orquestador-seo/references/`
Expected: solo `02-contratos.md`.

- [ ] **Step 4: Commit**

```bash
cd ~/.claude/skills/orquestador-seo
git commit -m "chore: borrar alta obsoleta (plantilla-cliente, refs 00/01) — superseded por seo-setup-cliente + base-cliente"
```

---

### Task 5: Reescribir `README.md` e `INSTALL.md`

**Files:**
- Modify (overwrite): `~/.claude/skills/orquestador-seo/README.md`
- Modify (overwrite): `~/.claude/skills/orquestador-seo/INSTALL.md`

**Interfaces:**
- Consumes: el modelo de delegación de `SKILL.md` (Task 3).
- Produces: onboarding docs alineados a la raíz `Clientes\` y al ecosistema.

- [ ] **Step 1: Sobrescribir `README.md` con este contenido exacto**

````markdown
# orquestador-seo

Skill **conductor** de Claude Code: el punto de entrada único de un proyecto SEO completo. No hace el trabajo — lo **enruta** a la skill dueña de cada capacidad del ecosistema SEO por cliente.

## Qué hace

Conduce el ciclo de vida completo delegando cada fase a su skill dueña y resolviendo los conflictos entre la estrategia y los datos reales. Es **runtime**; el artefacto (spec+planes) lo produce `seo-master-plan`.

Cada capacidad tiene una dueña — estrategia (`seo-master-plan`), árbol de URLs + keywords (`arquitectura-seo`), negocio (`base-cliente`), datos (`seo-setup-cliente`/`seo-sync`/`seo-analisis`/`seo-analisis-gsc`), crawl (`extraccion`), enlazado (`interlinking`), schema (`schema-graph`), AI (`geo-audit`), CWV (`seo-vitals`), backlinks (`linkbuilding`), secciones de página (`diseno-secciones`), contenido (`content-engine`), veredicto de cambios (`seo-cambios`), reporte (`seo-dashboard`). `claude-seo:*` es **gap-filler** (content-brief, single-page ad-hoc, hreflang).

### El ciclo (por escenario)

Fase 0 determina el escenario:
```
A · existente   diagnóstico → arquitectura (migración) → spec → ejecución → monitoreo
B · greenfield  arquitectura (nueva) → spec → build → validación → launch → monitoreo
```
Espina común: `base-cliente → master FRAMING (enfoque.md) → arquitectura-seo → master ENSAMBLAJE (spec+planes)`.

El núcleo es la **regla de conflicto**: cuando los datos (veredicto de `seo-cambios`) contradicen un supuesto del spec con alta confianza, ganan los datos y se reabre el diseño; el ruido (`no_determinable`) se ignora.

## Raíz por cliente

Cada cliente es un proyecto aislado en `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\` (sin repo git por cliente). La memoria nativa de Claude Code queda aislada por ruta. Credenciales = agencia (`~/.config/claude-seo/google-api.json` + DataForSEO/DinoRank), gestionadas por `seo-setup-cliente`.

Alta de cliente (Fase 0.0): crear la carpeta → `seo-setup-cliente` → `base-cliente`. El orquestador delega; no reimplementa alta. Detalle en `SKILL.md`.

## Dependencias

Skills del ecosistema en `~/.claude/skills/` (repos privados `dasv0731`): seo-master-plan, arquitectura-seo, base-cliente, seo-setup-cliente, seo-sync, extraccion, seo-analisis, seo-analisis-gsc, interlinking, schema-graph, geo-audit, seo-vitals, linkbuilding, diseno-secciones, seo-cambios, seo-dashboard, content-engine. Gap-filler: `claude-seo` (`claude-seo@skills-dir`).

## Uso

Se activa ante *"proyecto SEO completo"*, *"orquestar SEO"*, *"estrategia + auditoría SEO"*, *"llevar un cliente SEO de principio a fin"*.
````

- [ ] **Step 2: Sobrescribir `INSTALL.md` con este contenido exacto**

````markdown
# Instalación en una máquina nueva

`orquestador-seo` es el **conductor** del ecosistema SEO por cliente. Depende de las skills dueñas del ecosistema, cada una en su propio repo bajo `~/.claude/skills/`.

## Requisitos
- Claude Code instalado.
- `git` y `gh` (GitHub CLI) autenticado (`gh auth login`).
- `python3` + `pip` (scripts de Google API de `claude-seo` y del pipeline seo-*).

## 1. Clonar el orquestador
```bash
git clone https://github.com/dasv0731/orquestador-seo.git ~/.claude/skills/orquestador-seo
```
(PowerShell: reemplaza `~/.claude` por `"$env:USERPROFILE\.claude"`.)

## 2. Instalar las skills del ecosistema
Cada capacidad la aporta su skill dueña; instálalas en `~/.claude/skills/` desde sus repos privados (`dasv0731`) y sigue el INSTALL de cada una para sus dependencias:

`seo-master-plan` (repo seo-strategy), `arquitectura-seo`, `base-cliente`, `seo-setup-cliente`, `seo-sync`, `extraccion`, `seo-analisis`, `seo-analisis-gsc`, `interlinking`, `schema-graph`, `geo-audit`, `seo-vitals`, `linkbuilding`, `diseno-secciones`, `seo-cambios`, `seo-dashboard`, `content-engine`.

Gap-filler:
```bash
git clone https://github.com/AgriciDaniel/claude-seo.git ~/.claude/skills/claude-seo
cd ~/.claude/skills/claude-seo && ./install.sh   # Windows: .\install.ps1
```
`claude-seo` carga como `claude-seo@skills-dir` (tiene `.claude-plugin/plugin.json`).

## 3. Recargar y verificar
En Claude Code: `/reload-plugins` (o reiniciar). Verifica:
```bash
claude plugin list      # claude-seo@skills-dir: loaded
ls ~/.claude/skills/    # deben verse las skills del ecosistema
```

## 4. Credenciales de agencia (una sola vez)
Configurar `~/.config/claude-seo/google-api.json` (service account con acceso al GSC/GA4 de cada cliente + API key) y el login de DataForSEO. Tokens de DinoRank/Clarity con scope local en `~/.claude.json`. Las gestiona `seo-setup-cliente`. **Nunca en repos.**

## Listo
Da de alta clientes con la **Fase 0.0** del orquestador (crear `Clientes\<slug>\` → `seo-setup-cliente` → `base-cliente`). Cada cliente es su propia carpeta bajo `Clientes\` (sin repo por cliente), con memoria aislada por ruta.

---

### Notas
- Para actualizar `claude-seo`: `cd ~/.claude/skills/claude-seo && git pull` + `/reload-plugins`.
- Las credenciales (`~/.config/claude-seo/`) no están en ningún repo — se configuran a mano por seguridad.
````

- [ ] **Step 3: Verificar sanidad de ambos**

Run: `rg -n "seo-clientes|REGISTRO|references/00|references/01|repo privado|6 fases" ~/.claude/skills/orquestador-seo/README.md ~/.claude/skills/orquestador-seo/INSTALL.md`
Expected: sin salida.

- [ ] **Step 4: Commit**

```bash
cd ~/.claude/skills/orquestador-seo
git add README.md INSTALL.md
git commit -m "docs: README + INSTALL al modelo de delegación (raíz Clientes\\, ecosistema, sin workspace ~/seo-clientes)"
```

---

### Task 6: Verificación final + cierre del programa

**Files:**
- Modify: `Nuevas skills\Estrategia\docs\rework\contratos-conexiones.md` (marcar G4 hecho)

**Interfaces:**
- Consumes: Tasks 1–5 commiteadas en `orquestador-seo`.
- Produces: suite de grep en verde, escenarios A/B legibles, G4 marcado ✅ en el mapa del programa.

- [ ] **Step 1: Suite de sanidad global sobre el repo del orquestador**

Run: `rg -n "seo-clientes|PROJECT\.md|REGISTRO|conexiones\.md[^a-z]|git init" ~/.claude/skills/orquestador-seo/ || echo "LIMPIO"`
Expected: `LIMPIO` (ninguna ruta/convención vieja en todo el repo).

- [ ] **Step 2: Confirmar que no quedan refs a archivos borrados**

Run: `rg -n "plantilla-cliente|00-alta-cliente|01-credenciales" ~/.claude/skills/orquestador-seo/ || echo "SIN REFS MUERTAS"`
Expected: `SIN REFS MUERTAS`.

- [ ] **Step 3: Lectura de escenarios (verificación manual)**

Abrir `~/.claude/skills/orquestador-seo/SKILL.md` y confirmar a ojo:
- La tabla de división de labor no deja ninguna capacidad del ecosistema sin dueña, y `claude-seo:*` aparece solo como gap-filler.
- El Escenario A empieza en setup+base y pasa por diagnóstico → FRAMING → arquitectura-seo (migración) → ENSAMBLAJE → ejecución → monitoreo.
- El Escenario B es greenfield (FRAMING → arquitectura-seo sin 301 → ENSAMBLAJE → build → validación → launch → monitoreo).
- La Regla de conflicto ancla el veredicto en `seo-cambios` (`report.py beforeafter`), no en claude-seo.

- [ ] **Step 4: Marcar G4 hecho en el mapa del programa**

En `Nuevas skills\Estrategia\docs\rework\contratos-conexiones.md`, en la sección **§5 GAPS**, reemplazar el bloque **G4** por:
```markdown
**G4 · orquestador-seo ciego al ecosistema. ✅ HECHO (2026-07-14):** se reworkeó el CONTENIDO de
orquestador-seo — routing a las skills dueñas del ecosistema (claude-seo = gap-filler), alta delegada
a seo-setup-cliente + base-cliente sobre `Clientes\<slug>\` (sin repo por cliente ni REGISTRO),
modelo de fases espejo de los escenarios A/B con la espina FRAMING→arquitectura-seo→ENSAMBLAJE.
`references/02-contratos.md` reescrito como mapa producto/consumo. Diseño y plan en
`docs/rework/2026-07-14-g4-orquestador-seo-rework-{design,plan}.md`.
```

- [ ] **Step 5: Commit del cierre (repo Estrategia)**

```bash
cd "/c/Users/Marke/Documents/Respaldo SEO/Nuevas skills/Estrategia"
git add docs/rework/contratos-conexiones.md
git commit -m "docs(rework): G4 hecho — orquestador-seo reworkeado al ecosistema"
```

- [ ] **Step 6: Reportar estado de push**

El repo `orquestador-seo` queda en rama `g4-rework` con 5 commits; el repo `Estrategia` en rama `g4-orquestador-seo-rework`. Informar al usuario y **preguntar antes de pushear/mergear** (no pushear sin visto bueno).

## Self-Review (hecho al escribir el plan)

- **Cobertura del spec:** § A → Task 3 (Fase 0.0) + Task 4 (borrados). § B → Task 3 (tabla). § C → Task 3 (ciclo A/B) + Task 2 (§2 secuencias). § D → Task 3 (gate + regla). § E → Task 2. § F → Task 3 (dependencias) + Task 4 (plantilla) + Task 5 (README/INSTALL). Cierre → Task 6. Sin gaps.
- **Placeholders:** ninguno; el contenido final de los 4 archivos está embebido.
- **Consistencia de nombres:** raíz `Clientes\<slug>\`, `enfoque.md`, `report.py --report beforeafter`, `seo-cambios`, `claude-seo:*` gap-filler — idénticos en spec, Task 2 y Task 3.
