# G4 · Rework de orquestador-seo — diseño

> Parte del rework del ecosistema SEO por cliente. Precedido por G1 (diseño-secciones→raíz),
> G2 (estrategia.yaml→sitio.yaml), G3 (master consume el árbol). Este documento cubre **G4**:
> reworkear el CONTENIDO de `orquestador-seo` (sigue siendo skill, no agente).
> Fuente de verdad del mapa producto/consumo: `docs/rework/contratos-conexiones.md`.

## Problema

`orquestador-seo` quedó desalineado del ecosistema real en tres ejes:

1. **Modelo de alta obsoleto.** Usa `~/seo-clientes/<slug>/`, `PROJECT.md`,
   `conexiones/conexiones.md`, `REGISTRO.md` y un repo git por cliente. La realidad es
   `Clientes\<slug>\`, `base\contexto-<slug>.md` (base-cliente), `conexiones\conexiones.json`
   + `data\seo.db` (seo-setup-cliente), **sin repo git por cliente** y **sin REGISTRO**.
   Sus `plantilla-cliente/`, `references/00-alta-cliente.md` y `references/01-credenciales-agencia.md`
   están superseded por seo-setup-cliente + base-cliente + la convención `Clientes\`.

2. **Routing ciego.** Solo enruta a refs internas de `seo-master-plan` + `claude-seo:*`.
   No conoce a las dueñas reales del trabajo: arquitectura-seo, base-cliente, seo-setup/sync,
   seo-analisis/gsc, schema-graph, interlinking, geo-audit, seo-vitals, linkbuilding,
   diseno-secciones, seo-cambios, seo-dashboard, content-engine.

3. **Modelo de fases desalineado.** Sus 6 fases genéricas se apoyan en la dualidad
   "master = QUÉ/POR QUÉ · claude-seo = QUÉ ES HOY". La realidad son las **dos secuencias A/B**
   ya especificadas en `contratos-conexiones §2/§3`, y el master ahora se parte en
   **FRAMING** (§0–§2 → `enfoque.md` ANTES de arquitectura-seo) y **ENSAMBLAJE**
   (§3–§14 → consume el árbol DESPUÉS) tras G3.

## Frontera (invariante — NO cambia en G4)

- `orquestador-seo` sigue **skill** (decidido con el usuario: orquestar = invocar/secuenciar
  otras skills, capacidad del loop principal; un subagente no despacha sub-subagentes fiablemente).
- `orquestador = runtime` (secuencia skills, gestiona estado/gates, aplica la arista de retorno).
  `master = artefacto` (spec §0–§14 + planes). El orquestador **no hace SEO: enruta**.

## Decisiones tomadas en el brainstorm (2026-07-14)

- **D1 · Rol de claude-seo = gap-filler explícito.** El flujo primario son las skills propias
  del ecosistema. `claude-seo:*` queda como complemento para lo que el ecosistema **no tiene
  dueño** (seo-content-brief, auditoría single-page ad-hoc, hreflang/i18n, fallback si falta
  una skill propia). Se reescribe la tabla de división de labor.
- **D2 · Alta = delegar + secuenciar.** El orquestador NO reimplementa alta. Borra
  `plantilla-cliente/`, `references/00-alta-cliente.md`, `references/01-credenciales-agencia.md`.
  En su lugar, un checklist delgado de bootstrap que secuencia
  `crear Clientes\<slug>\ → seo-setup-cliente → base-cliente` y verifica pre-requisitos.

## Diseño

### § A — Alta / bootstrap (Fase 0.0)

- **Borrados:** `plantilla-cliente/`, `references/00-alta-cliente.md`,
  `references/01-credenciales-agencia.md`.
- **Nuevo bootstrap delgado** (queda como sección corta del `SKILL.md`, no como plantilla):
  1. Crear `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\` (slug kebab-case, minúsculas,
     sin tildes/espacios).
  2. Correr **seo-setup-cliente** → `conexiones\conexiones.json` + `data\seo.db` (10 tablas).
  3. Correr **base-cliente** → `base\` + `base\contexto-<slug>.md`.
- **Gate de arranque del ciclo:** verificar que existan `conexiones\conexiones.json`,
  `data\seo.db` y `base\contexto-<slug>.md` antes de entrar a las fases.
- **Sin** repo git por cliente, **sin** `REGISTRO.md`, **sin** `PROJECT.md`.
  Working dir al trabajar un cliente = `Clientes\<slug>\` (mantiene el aislamiento de memoria
  nativa de Claude Code por ruta de proyecto).
- **Credenciales:** son de agencia y las gestiona seo-setup-cliente
  (`~/.config/claude-seo/google-api.json` con service account con acceso al GSC/GA4 del cliente,
  DinoRank/Clarity con scope local en `~/.claude.json`). El orquestador solo referencia ese
  requisito, no lo documenta de nuevo.

### § B — Tabla de división de labor (reescrita)

Sustituye la tabla de 2 filas (master/claude-seo) por el mapa del ecosistema real. Cada
capacidad tiene **una** skill dueña; `claude-seo:*` es gap-filler.

| Dominio | Skill dueña | Artefacto principal |
|---|---|---|
| Estrategia, spec §0–§14, planes, KPIs/gates, principios, migración | **seo-master-plan** (CONSUME) | `docs\superpowers\{specs,plans}\` |
| Árbol de URLs + estudio de kws | **arquitectura-seo** | `arquitectura\resultados\{arquitectura.csv, enlazado.csv, mapeo-301.csv, mapa-keywords.csv}` + `sitio.yaml` |
| Conocimiento de negocio | **base-cliente** | `base\contexto-<slug>.md` |
| Conexiones + poblar seo.db | **seo-setup-cliente** / **seo-sync** | `conexiones\conexiones.json`, `data\seo.db` |
| Diagnóstico de datos | **seo-analisis** / **seo-analisis-gsc** | tabla `hallazgos`, `url_status`, reportes |
| PageRank interno / enlazado real | **interlinking** | `resultados\` (métricas, grafos, tablero) |
| JSON-LD del dominio | **schema-graph** | `schema-graph\` (snippets, SCHEMA-REPORT.md) |
| Visibilidad/citability AI | **geo-audit** | hallazgos GEO + scores en seo.db, `geo\informes\` |
| Core Web Vitals | **seo-vitals** | `cwv\seo.db` + `informes\CWV-<fecha>.md` |
| Backlinks / off-page | **linkbuilding** | tabla `lb_backlinks` + `linkbuilding\informes\` |
| Secciones/layout/copy de UNA página | **diseno-secciones** | `secciones\<slug-pagina>\{01,02,03}` |
| Redacción informacional (silo aparte) | **content-engine** | `Herramientas\SEO Blogs\content-engine\proyectos\` |
| Veredicto antes/después | **seo-cambios** | tabla `changes_log` + veredictos |
| Reporte / dashboard | **seo-dashboard** | `reportes\dashboard.html` + `clusters.json` |
| **Gap-filler** (content-brief, single-page ad-hoc, hreflang, fallback) | **claude-seo:*** | — |

### § C — Modelo de fases → espejo de escenarios A/B

**Fase 0 · Bootstrap & determinación de escenario.** Correr § A. Determinar escenario:
¿hay sitio vivo con GSC/GA4 pobladas y contenido que crawlear? → **A (existente)**.
¿No hay sitio ni datos? → **B (greenfield)**.

**Espina común (corrige G3):** el master se parte en FRAMING y ENSAMBLAJE alrededor de
arquitectura-seo:
```
base-cliente → master FRAMING (§0–§2 → arquitectura\data\enfoque.md)
             → arquitectura-seo (árbol) → master ENSAMBLAJE (§3–§14 → spec+planes)
```

**Escenario A (existente) — diagnosticar → rediseñar → migrar → monitorear:**
```
0. seo-setup-cliente + base-cliente                              (bootstrap)
1. seo-sync BACKFILL  ∥  extraccion crawl                        (paralelo)
2. DIAGNÓSTICO (leen lo de 1):
     seo-analisis · seo-analisis-gsc · interlinking ·
     schema-graph · geo-audit · seo-vitals · linkbuilding
3. master FRAMING (§0–§2 → enfoque.md)
4. arquitectura-seo (modo migración → arquitectura.csv + mapeo-301.csv)
5. master ENSAMBLAJE (§3–§14 → spec sabor MIGRACIÓN + planes)
6. Ejecución: diseno-secciones · content-engine · schema-graph
7. MONITOREO: seo-cambios (logchange + veredicto) · seo-dashboard ·
     re-corridas geo-audit/seo-vitals/linkbuilding · seo-sync diario
```

**Escenario B (greenfield) — diseñar → construir → validar → lanzar → monitorear:**
```
0. seo-setup-cliente + base-cliente                              (bootstrap)
1. master FRAMING (§0–§2 → enfoque.md)
2. arquitectura-seo (modo greenfield: estudio de kws → árbol nuevo, sin inventario/301)
3. master ENSAMBLAJE (§3–§14 → spec sabor FOUNDATION + planes)
4. BUILD: diseno-secciones (modo propuesta) · content-engine · schema-graph
5. VALIDACIÓN pre-launch (sobre staging):
     seo-vitals · geo-audit · interlinking · html-semantico
6. LAUNCH: sitemap + IndexNow + solicitar indexación
7. MONITOREO: seo-sync empieza a capturar → converge con Escenario A
```

Punto de convergencia de A y B: el **monitoreo con seo.db poblado**.

### § D — Gate de medición + Regla de conflicto (conservar, re-anclar)

Se conservan tal cual el **Gate de medición** (baseline + `changes_log` activo antes de abrir
loops de ejecución) y la **Regla de conflicto de 3 ramas**
(mejora/regresión propaga · `no_determinable` ignora · `sin_efecto` nulo confiable), pero
**re-ancladas al ecosistema**: el veredicto sale de **seo-cambios** (`changes_log` →
`report.py --report beforeafter`), no de claude-seo/pipeline `_tooling`.

**Costuras transversales** (no pertenecen a una sola skill, se conservan):
- **Modo de render (CSR/SSR/estático):** se decide en discovery (master FRAMING) y lo heredan
  a la vez la indexabilidad (crawl de extraccion + arquitectura-seo) y el rendimiento (seo-vitals).
- **i18n:** módulo condicional; único caso gap-filler estructural → `claude-seo:seo-hreflang`.

### § E — `references/02-contratos.md` (formalizar el mapa producto/consumo)

Se reescribe para ser el mapa canónico de routing del orquestador:
- I/O por skill anclado a `Clientes\<slug>\` + tablas de `seo.db`
  (tomado de `contratos-conexiones §4`).
- Las dos secuencias A/B (de `contratos-conexiones §2/§3`).
- Se **preserva** el concepto de estado de frontera (🟢/🟡/🔴) y el experimento vivo **3↔5**
  (taxonomía↔enlazado en metalectro) — sigue abierto.

### § F — Dependencias, README, INSTALL, plantilla-cliente

- **Dependencias:** ampliar la lista (hoy solo master + claude-seo) para declarar las skills del
  ecosistema esperadas instaladas; el orquestador se detiene y avisa si falta una crítica.
- **Rutas:** todas a `Clientes\<slug>\`.
- **Borrar** `plantilla-cliente/`.
- **README.md / INSTALL.md:** ajustar al modelo de delegación y a la raíz `Clientes\`.

## Cierre del programa de rework

Al terminar G4, actualizar en `contratos-conexiones.md §5` el gap **G4** a ✅ DECIDIDO/HECHO.
Queda pendiente solo **G5** (menor): decidir si seo-vitals unifica su `cwv\seo.db` en
`data\seo.db` o el dashboard lee ambas.

## Verificación (cómo sabremos que quedó bien)

- Test de escenario A: dado un cliente con `Clientes\<slug>\` poblado (conexiones+seo.db+base),
  el orquestador enruta a la secuencia A completa sin mencionar `~/seo-clientes/`, `PROJECT.md`
  ni claude-seo como fuente primaria de datos.
- Test de escenario B: greenfield sin datos → secuencia B, master FRAMING antes de arquitectura-seo.
- Grep de sanidad: `SKILL.md` + `references/` sin ocurrencias de `~/seo-clientes`, `PROJECT.md`,
  `REGISTRO.md`, `conexiones.md` (sin `.json`), ni `git init` por cliente.
- La tabla § B no deja ninguna capacidad del ecosistema sin dueña, y claude-seo aparece solo
  como gap-filler.
