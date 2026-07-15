# Contratos y conexiones entre skills — mapa para ensamblar el master

> Basado en lectura directa de las SKILL.md reales (2026-07-13). El sustrato de contratos
> es doble: (1) la **carpeta del cliente** en disco y (2) el **`seo.db`** SQLite. Las skills
> se comunican dejando/leyendo archivos y tablas en esos dos medios, no llamándose entre sí.

---

## 0. HALLAZGO QUE CONDICIONA TODO: hay 3 raíces de cliente incompatibles

| Convención | Skills que la usan | Raíz |
|---|---|---|
| **A. `Clientes\<slug>\`** (dominante) | base-cliente, extraccion, arquitectura-seo, interlinking, schema-graph, seo-analisis, linkbuilding, geo-audit | `C:\Users\Marke\Documents\Respaldo SEO\Clientes\<slug>\` |
| **B. Por marcador** (agnóstica) | seo-setup, seo-sync, seo-analisis-gsc, seo-cambios, seo-dashboard, seo-vitals | resuelve subiendo hasta `conexiones\conexiones.json` o `estrategia.yaml` |
| **C. `~/seo-clientes/<slug>/`** (POSIX) | orquestador-seo, diseno-secciones | `~/seo-clientes/<slug>/` |
| **D. Silo propio** | content-engine | `Herramientas\SEO Blogs\content-engine\proyectos\<empresa>\` |

**Las convenciones B y A convergen** si la carpeta-marcador ES `Clientes\<slug>\` (seo.db queda en
`Clientes\<slug>\data\seo.db`, que es justo lo que leen todas las de la B). **Las que están fuera
de línea son C (orquestador + diseno-secciones) y D (content-engine).**

**DECISIÓN FUNDACIONAL:** unificar todo en **`Clientes\<slug>\`** (raíz A). Es la mayoritaria y la
única que ya aloja el seo.db compartido. Hay que **migrar orquestador-seo y diseno-secciones** de
`~/seo-clientes/` a `Clientes\<slug>\`. content-engine se queda como silo por empresa (es informacional,
no por-cliente-SEO) pero se le puede dar un puente.

---

## 1. LA CARPETA-CONTRATO CANÓNICA (sustrato compartido)

```
Clientes\<slug>\
├─ conexiones\conexiones.json     ← seo-setup CREA (slug, domain, gsc/ga4 property, location/lang, brand_terms)
├─ sitio.yaml                     ← arquitectura-seo EMITE (sitio:, plantilla:, paginas_dinero:=URLs P1, clusters hub/spoke). Lo leen extraccion/interlinking/seo-vitals/geo-audit. [ex-"estrategia.yaml" — renombrado porque la ESTRATEGIA la hace master-plan]
├─ base\                          ← base-cliente CREA (fichas + contexto-<slug>.md)
│   └─ contexto-<slug>.md
├─ keywords\                      ← estudio de kws (manual o de arquitectura-seo)
├─ data\
│   ├─ seo.db                     ← seo-setup CREA · seo-sync PUEBLA · analisis/gsc/cambios/linkbuilding/geo ESCRIBEN
│   ├─ internal_html.csv          ← extraccion (crawl)
│   ├─ all_inlinks.csv            ← extraccion
│   ├─ page_source\*.html         ← extraccion (original_ / rendered_)
│   ├─ schemas.json, schemas_resumen.csv, structured_data_*.csv ← extraccion
│   ├─ issues_overview.csv, issues\*.csv ← extraccion
│   └─ clarity-heatmaps\*.csv     ← export manual (lo lee seo-sync)
├─ inventario\internal.csv|sitemap.xml ← solo sitio existente (input de arquitectura-seo)
├─ historico\<YYYY-MM-DD>\        ← extraccion archiva snapshots
├─ arquitectura\
│   ├─ data\{enfoque.md, semillas.csv, estudio-<fecha>\}
│   └─ resultados\{arquitectura.csv, enlazado.csv, mapeo-301.csv, mapa-keywords.csv, descartes.csv, cola-larga.csv, arbol.html, informe.md}
├─ schema-graph\                  ← schema-graph (workspace: content-inventory, client-profile, graph-model, snippets\, SCHEMA-REPORT.md)
├─ resultados\                    ← interlinking (resumen.md, informe.md, metricas_paginas.csv, tablero.html, grafo*.html)
├─ cwv\                           ← seo-vitals (⚠️ cwv\seo.db SEPARADA + evidencia por corrida)
├─ geo\{geo.yaml, informes\}      ← geo-audit
├─ linkbuilding\{gsc\, informes\, outreach\} ← linkbuilding
├─ secciones\<slug-pagina>\       ← diseno-secciones (01-disenador, 02-redactor, 03-final)
├─ analisis\<fecha>-<modulo>.md   ← seo-analisis (reportes)
├─ informes\CWV-<fecha>.md        ← seo-vitals
├─ reportes\dashboard.html        ← seo-dashboard
├─ clusters.json                  ← seo-dashboard escribe (editor) · analisis/linkbuilding leen
└─ docs\superpowers\{discovery,specs,plans}\ ← seo-master-plan (spec + planes)
```

### Tablas de seo.db (contrato de datos vivo)
- **seo-setup CREA:** gsc_daily, ga4_daily, rank_tracking, core_keywords, changes_log, page_content, index_status, url_status, clarity_daily, clarity_heatmap.
- **seo-sync PUEBLA:** gsc_daily, ga4_daily, clarity_daily, clarity_heatmap, index_status, rank_tracking, page_content.
- **seo-analisis ESCRIBE:** `hallazgos` (estado nuevo/persistente/resuelto, clave (modulo,clave)).
- **seo-analisis-gsc ESCRIBE:** `url_status` (301+destino, alias de cluster).
- **seo-cambios ESCRIBE:** `changes_log`.
- **linkbuilding ESCRIBE:** `lb_backlinks` + pipeline de prospectos/estados.
- **geo-audit ESCRIBE:** hallazgos GEO + scores por capa + menciones/share of voice + tráfico AI.
- **seo-vitals ESCRIBE:** en base APARTE `cwv\seo.db` (cwv_runs, cwv_metrics, cwv_findings).
- **seo-dashboard LEE** todo lo anterior; ESCRIBE `clusters.json`.

---

## 2. ESCENARIO A — Web existente con data / en producción

El diferenciador: **hay datos reales (GSC/GA4) y un sitio vivo que crawlear** → hay una fase de
DIAGNÓSTICO antes de diseñar. arquitectura-seo trabaja en modo migración (inventario + 301).

```
1. base-cliente        → base\ + contexto-<slug>.md          (conocimiento del negocio)
2. seo-setup-cliente   → conexiones.json + data\seo.db
3. seo-sync (BACKFILL) → puebla seo.db con histórico GSC/GA4/Clarity/ranks   ┐ en paralelo
   extraccion (crawl)  → data\*.csv + page_source\ + issues\                 ┘
4. DIAGNÓSTICO del sitio actual (todos leen lo de 3):
     seo-analisis      → hallazgos (huérfanas, index bloat, CTR roto, gap kws)
     seo-analisis-gsc  → quick wins (5-15), canibalización, marca, 404/redirects
     interlinking      → PageRank interno actual vs estrategia.yaml
     schema-graph      → schema actual del dominio
     geo-audit         → visibilidad/citability AI actual
     seo-vitals        → CWV actual
     linkbuilding      → perfil de backlinks actual + gaps
5. arquitectura-seo (modo existente) → LEE inventario\ (crawl/sitemap) + seo.db (qué rankea)
     → arquitectura.csv (árbol con accion: mantener/301/fusionar/eliminar) + mapeo-301.csv
6. seo-master-plan → CONSUME contexto + arquitectura.csv + mapa-keywords.csv + el bundle de
     diagnóstico → produce Design Spec (sabor MIGRACIÓN §13, KPI retención) + planes por fase
7. Ejecución de cambios → diseno-secciones / content-engine / schema-graph regeneran páginas
8. MONITOREO continuo → seo-cambios (logchange + veredicto antes/después) · seo-dashboard ·
     re-corridas de geo-audit / seo-vitals / linkbuilding · seo-sync diario
```

## 3. ESCENARIO B — Web desde 0 (greenfield)

El diferenciador: **no hay sitio que crawlear ni GSC que medir** → NO hay fase de diagnóstico;
arquitectura-seo trabaja desde el estudio de keywords puro (sin inventario, sin 301).

```
1. base-cliente        → base\ + contexto-<slug>.md
2. seo-setup-cliente   → conexiones.json + data\seo.db   (GSC/GA4 vacíos hasta el launch;
                          arquitectura necesita DinoRank o DataForSEO para el estudio de kws)
3. arquitectura-seo (modo greenfield) → LEE base\ + conexiones\ + keywords\ → corre el estudio
     de kws → arquitectura.csv (árbol nuevo, accion=nueva) + enlazado.csv + arbol.html
     (SIN inventario\, SIN mapeo-301)
4. seo-master-plan → CONSUME contexto + arquitectura.csv + enlazado.csv + mapa-keywords.csv →
     Design Spec (sabor FOUNDATION §0–§14) + planes por fase (las ~15 fases de build)
5. BUILD (dirigido por el spec/planes):
     diseno-secciones (modo B propuesta) → estructura de secciones por página del árbol
     content-engine   → redacta las piezas del roadmap
     schema-graph     → genera JSON-LD del árbol (crawl de staging o del build)
6. VALIDACIÓN pre-launch (sobre staging):
     seo-vitals (CWV) · geo-audit (allowlist/llms.txt/citability) · interlinking (enlazado real
     vs estrategia) · html-semantico (por página)
7. LAUNCH → sitemap + IndexNow + solicitar indexación
8. MONITOREO → seo-sync empieza a capturar GSC/GA4 → a partir de aquí converge con Escenario A
     (seo-analisis, seo-cambios, seo-dashboard, re-auditorías)
```

**Resumen de la diferencia:** A = *diagnosticar → rediseñar → migrar → monitorear*.
B = *diseñar → construir → validar → lanzar → (a partir del launch) monitorear como A*.
El punto donde ambos convergen es el **paso 8 (monitoreo con seo.db poblado)**.

---

## 4. CONTRATO POR SKILL (normalizado a raíz `Clientes\<slug>\`)

| Skill | LEE (input) | ESCRIBE (output) |
|---|---|---|
| **base-cliente** | docs/fuentes; opcional crawl de extraccion (internal_html + page_source) | `base\` + `contexto-<slug>.md` |
| **seo-setup-cliente** | credenciales (google-api.json, ~/.claude.json) | `conexiones\conexiones.json` + `data\seo.db` (10 tablas) |
| **seo-sync** | conexiones.json + APIs (GSC/GA4/Clarity/DataForSEO) | puebla seo.db |
| **extraccion** | sitio.yaml (`sitio:`), plantillas SF | `data\*.csv` + `page_source\` + `historico\<fecha>\` |
| **arquitectura-seo** | base\, conexiones\, keywords\, seo.db (GSC), inventario\ (si existe) | `arquitectura\resultados\{arquitectura.csv, enlazado.csv, mapeo-301.csv, mapa-keywords.csv}` **+ `sitio.yaml`** |
| **seo-master-plan** | contexto-<slug>.md, arquitectura.csv, enlazado.csv, mapa-keywords.csv, bundle de diagnóstico | `docs\superpowers\{discovery,specs,plans}\` |
| **diseno-secciones** | keywords\, seo.db, page_source\ (crawl) | `secciones\<slug-pagina>\{01,02,03}` |
| **schema-graph** | data\*.csv + page_source\ (crawl) | `schema-graph\` (snippets\, SCHEMA-REPORT.md) |
| **interlinking** | data\all_inlinks.csv + internal_html.csv, sitio.yaml | `resultados\` (metricas, grafos, tablero.html) |
| **html-semantico** | HTML/URL ad hoc | informe en chat (sin archivo) |
| **content-engine** | tema/.docx, KB de experiencia (silo aparte) | `proyectos\<empresa>\blogs\...` |
| **seo-vitals** | conexiones/sitio.yaml, data\*.csv (crawl), CrUX | `cwv\seo.db` + `informes\CWV-<fecha>.md` |
| **seo-analisis** | seo.db + crawl (Clientes\<slug>) + DinoRank | tabla `hallazgos` + `analisis\*.md` |
| **seo-analisis-gsc** | seo.db (GSC) + HTTP propio | tabla `url_status` + reportes chat |
| **seo-cambios** | seo.db (GSC/GA4/Clarity/ranks) | tabla `changes_log` + veredictos |
| **seo-dashboard** | seo.db (hallazgos, url_status, GSC) + clusters.json | `reportes\dashboard.html` + `clusters.json` |
| **linkbuilding** | conexiones, GSC CSV (linkbuilding\gsc\), clusters.json, DinoRank/DataForSEO | tabla `lb_backlinks` + pipeline + `linkbuilding\informes\` |
| **geo-audit** | seo.db, geo\geo.yaml, base\, sitio.yaml (paginas_dinero) | hallazgos GEO + scores en seo.db + `geo\informes\` |

---

## 5. GAPS DE CONTRATO A CERRAR (las 4 costuras rotas)

**G1 · Tres raíces de cliente. ✅ DECIDIDO (2026-07-13):** unificar en `Clientes\<slug>\`; migrar
orquestador-seo y diseno-secciones desde `~/seo-clientes/`. content-engine sigue como silo.

**G2 · `estrategia.yaml` es huérfano. ✅ DECIDIDO (2026-07-13):** se renombra a **`sitio.yaml`**
(el nombre "estrategia" queda reservado al master; esto es config de sitio, no estrategia).
Lo **EMITE arquitectura-seo** derivándolo del árbol: `sitio:` = domain de conexiones; `plantilla:`
= js/estatica del discovery; `paginas_dinero:` = URLs prioridad P1; `clusters:` = hub/spoke del
árbol. Lo consumen extraccion, interlinking, seo-vitals y geo-audit (se actualizan sus refs de
`estrategia.yaml` → `sitio.yaml`; interlinking mantiene su fallback por entrevista si falta).

**G3 · El árbol (`arquitectura.csv`) no lo consume nadie automáticamente. ✅ DECIDIDO (2026-07-13):**
el master **consume `arquitectura.csv` como su §2/§3** (deja de regenerar la arquitectura
internamente); en greenfield el árbol es la fuente de qué páginas construir (lo consumen
diseno-secciones + content-engine). Esto es el corazón del rework de master-plan.

**G4 · orquestador-seo ciego al ecosistema. ✅ HECHO (2026-07-14):** se reworkeó el CONTENIDO de
orquestador-seo — routing a las skills dueñas del ecosistema (claude-seo = gap-filler), alta delegada
a seo-setup-cliente + base-cliente sobre `Clientes\<slug>\` (sin repo por cliente ni registro central),
modelo de fases espejo de los escenarios A/B con la espina FRAMING→arquitectura-seo→ENSAMBLAJE.
`references/02-contratos.md` reescrito como mapa producto/consumo; `plantilla-cliente/` + refs 00/01
borradas; README/INSTALL alineados. 6 tasks vía subagent-driven (implementer+reviewer Opus por task).
Diseño y plan en `docs/rework/2026-07-14-g4-orquestador-seo-rework-{design,plan}.md`.

**G5 · Raíz única por cliente. ✅ HECHO (2026-07-15):** retirada la raíz vieja
`Herramientas\SEO Master\<slug>\`. extraccion blinda los durables de `data\` (contrato
`DURABLES` = seo.db, seo.db-wal, seo.db-shm, clarity-heatmaps\ en `crawlear-cliente.py` + SKILL.md);
`migrar_raiz.py` (`docs/rework/scripts/`, idempotente, TDD) migró metalectro a `Clientes\metalectro\`
(seo.db 40,5 MB con merge de las tablas `geo_*` del stub, conexiones, clusters.json, plans\,
reportes\, clarity-heatmaps) y neutralizó la raíz vieja (`conexiones.json.pre-merge`; queda como
backup, nada borrado). esacero/golgana/aiotech pendientes de correr el mismo script. La unificación
de `cwv\seo.db` en `data\seo.db` (texto original de este gap) queda DIFERIDA como decisión futura.
Diseño y plan en `docs/rework/2026-07-15-g5-raiz-unica-{design,plan}.md`.

---

## 6. QUÉ NECESITA EL MASTER DE LAS DEMÁS (para ensamblarlo)

**INPUT contract del master (target):**
- `base\contexto-<slug>.md` → §0 panorama, §7 E-E-A-T (personas reales).
- `arquitectura\resultados\arquitectura.csv` → §2 enfoque + §3 URLs/content-types (CONSUME, no regenera).
- `arquitectura\resultados\enlazado.csv` → §4 internal linking (diseño).
- `arquitectura\resultados\mapa-keywords.csv` → §9 keywords/clusters (volúmenes reales).
- **Solo Escenario A** — bundle de diagnóstico: `hallazgos` (seo-analisis), `resumen.md`
  (interlinking), scores GEO (geo-audit), CWV (seo-vitals), perfil (linkbuilding),
  SCHEMA-REPORT (schema-graph), inventario+mapeo-301 (arquitectura-seo §13).

**OUTPUT contract del master:** `docs\superpowers\specs\...seo-design.md` (§0–§14) +
`plans\...mesN-plan.md`. El master aporta lo que NINGUNA otra skill produce: restricción dominante,
parametrización vertical, principios, diseño de KPIs/gates/runbook, estrategia de migración,
roadmap de contenido, línea estratégica de local/off-site/GEO, y el ensamblaje spec↔plan.

**Lo que el master DEJA DE HACER** (vs versión actual): regenerar arquitectura/keywords/schema
internamente (§03/§08/§04). Ahora los consume de arquitectura-seo y schema-graph.

---

## 7. COMPETIDORES (diferida) — qué CONSUMIRÍA de las demás (nivel básico)

No se desarrolla aún, pero para no bloquear el diseño, esto es lo mínimo que necesitaría:
- **INPUT:** lista de competidores desde `base\` (o `geo\geo.yaml` / discovery); capacidad de crawl
  = **reutilizar el motor de `extraccion`** apuntado a dominios ajenos; SERP/keywords vía
  DataForSEO/DinoRank; perfil de backlinks del competidor (comparte lógica con `linkbuilding`).
- **OUTPUT:** fichas de competidor (schema, content-types, cadencia, gaps) que **consumen**:
  arquitectura-seo (señal SERP, ya prevista como opcional), linkbuilding (prospectos por gap),
  master §11 (auditoría competitiva).
- **Nivel básico factible sin la skill:** hoy la "señal de competidores" ya la aproxima
  arquitectura-seo desde las URLs del top-10 del SERP (Fase 4). Competidores formaliza y profundiza
  eso, pero no es bloqueante para el master.

---

## ORDEN DE TRABAJO PROPUESTO
1. **Decidir los gaps G1-G5** (sobre todo G1 raíz única, G2 productor de estrategia.yaml, G3 el
   master consume el árbol).
2. **Rework de master-plan** con el INPUT/OUTPUT contract de §6.
3. **Rework de orquestador-seo** (G4): enrutar a las skills propias por escenario (A vs B).
4. competidores (cuando toque) con el contrato de §7.
