---
title: Rework de seo-master-plan — estrategia + gobernanza + ensamblaje (consume, no regenera)
date: 2026-07-13
status: draft
owner: dasv0731
phase: design-spec
---

# Rework de seo-master-plan

## Objetivo

Reenfocar `seo-master-plan` de "hace todo" a **espina estratégica + gobernanza + ensamblaje**:
deja de regenerar internamente la arquitectura, las keywords y el schema, y en su lugar
**consume** los artefactos que ya producen las skills dedicadas del ecosistema (arquitectura-seo,
schema-graph, base-cliente, y el pipeline de diagnóstico). El valor que conserva —restricción
dominante, parametrización vertical, principios, gobernanza (KPIs/gates/runbook), estrategia de
migración, roadmap de contenido, línea estratégica de local/GEO/off-site, y el ensamblaje
spec↔plan— es lo que ninguna otra skill produce.

## Decisiones tomadas (brainstorm 2026-07-13)

- **Alcance = quirúrgico (A).** Conservar la metodología probada, el esqueleto §0–§14 y los case
  studies (AioTech/Inspira). Solo redirigir las secciones delegadas de "genera" a "consume" y
  añadir los contratos. No reescribir el skill desde cero.
- **Consumo = híbrido (c).** El spec **referencia** el artefacto canónico como fuente de verdad
  (sin duplicar el árbol completo → sin drift) **y** embebe un **resumen compacto** marcado como
  derivado (para que el spec se lea de corrido), + la capa estratégica encima.
- **Secuenciación = dos fases (a).** El framing estratégico de master corre ANTES de
  arquitectura-seo (para que la restricción dominante gobierne la arquitectura); el ensamblaje
  corre DESPUÉS (consumiendo el árbol).

## Fuera de alcance (tareas separadas)

- **G1** (raíz única de cliente en `Clientes\<slug>\`; migrar orquestador-seo y diseño-secciones):
  este rework ya escribe a `Clientes\<slug>\docs\superpowers\`, compatible con G1, pero G1 en sí
  es aparte.
- **G4** (rework de orquestador-seo para enrutar a las skills propias): master **consume, no
  orquesta**; el runtime que corre las skills de diagnóstico y encadena las fases es el orquestador.
- **G5** (unificar `cwv\seo.db` de seo-vitals): sin relación con este rework.

---

## 1. Estructura de dos fases y reparto de secciones

Master se parte en dos momentos, con arquitectura-seo en medio:

```
base-cliente → [MASTER: FRAMING] → arquitectura-seo → [MASTER: ENSAMBLAJE] → planes
                    §0–§2                 (árbol)            §3–§14
                escribe enfoque.md    consume enfoque.md   consume el árbol
```

**Fase FRAMING** (antes de arquitectura-seo):
- Lee `base\contexto-<slug>.md`.
- Produce el cerebro estratégico: **§0** panorama · **§0.1** restricción dominante · **§1**
  decisiones estratégicas (audiencia, geo, modelo de conversión, render mode, estado del sitio,
  scope) · **§2** elección de enfoque de arquitectura (servicio/sector/matriz/especialidad-first,
  justificado por la restricción dominante + la tabla de parametrización vertical).
- Escribe el handoff `arquitectura\data\enfoque.md` + el discovery doc.
- Materializa el principio *"restricción dominante primero, antes de la arquitectura"*.

**arquitectura-seo** corre, consume `enfoque.md`, produce `arquitectura.csv` + `enlazado.csv` +
`sitio.yaml` + `mapa-keywords.csv`.

**Fase ENSAMBLAJE** (después):
- Lee los artefactos de arquitectura-seo + (solo Escenario A) el bundle de diagnóstico.
- Ensambla el Design Spec §0–§14 combinando el framing (§0–§2) con lo consumido:
  - **§3** URLs/content-types → consume `arquitectura.csv` (híbrido)
  - **§4** internal linking → consume `enlazado.csv` (híbrido)
  - **§5** schema → decide anclaje (Organization/Person/…) + delega generación a schema-graph
  - **§9** keywords → consume `mapa-keywords.csv`
  - **§6** local · **§7** GEO/E-E-A-T · **§8** targets técnicos · **§10** roadmap contenido ·
    **§11** competencia/linkbuilding · **§12** KPIs/gates · **§13** riesgos → estrategia propia
  - **§14** briefs → lista páginas del árbol; estructura/copy → diseño-secciones/content-engine
- Luego los planes (~15 fases): la fase de arquitectura dice *"el árbol ya lo produjo
  arquitectura-seo; se construye desde él"*.

**Dónde vive el §0–§2 entre fases:** el framing NO escribe el archivo del spec. Deja su
razonamiento §0–§2 en el **discovery doc** + `enfoque.md`. El **archivo del spec (§0–§14) lo
escribe el ensamblaje**, formalizando §0–§2 desde esos artefactos del framing y añadiendo §3–§14.
Así hay un único archivo-spec, producido al final, sin versiones parciales que se desincronicen.

---

## 2. Contratos y degradación

### Fase FRAMING
| | |
|---|---|
| Lee | `base\contexto-<slug>.md` (opcional) |
| Escribe | `docs\superpowers\discovery\<fecha>-<slug>-discovery.md` · `arquitectura\data\enfoque.md` |

**Formato de `enfoque.md`** (texto estructurado que arquitectura-seo Fase 0 espera):
- **Qué priorizar** — derivado de la restricción dominante (qué líneas/servicios potenciar).
- **Dimensiones de arquitectura** — del §2 (servicios / sectores / ubicaciones / especialidades…).
- **País e idioma** — confirmado contra `conexiones.json` (`location_code`/`language_code`).
- **Modelo de conversión** — compra / lead / WhatsApp / llamada / booking.
- **Competidores conocidos** — si los hay.

### Fase ENSAMBLAJE
| | |
|---|---|
| Lee (requerido) | `arquitectura\resultados\arquitectura.csv` · `enlazado.csv` · `mapa-keywords.csv` + artefactos del framing |
| Lee (opcional, Escenario A) | bundle de diagnóstico: tabla `hallazgos`, `resumen.md` (interlinking), scores geo, CWV, perfil linkbuilding, `SCHEMA-REPORT.md`, `mapeo-301.csv` |
| Escribe | `docs\superpowers\specs\<fecha>-<slug>-seo-design.md` (§0–§14) · `plans\<fecha>-<slug>-seo-mesN-plan.md` |

**Ubicación de salida:** todo bajo `Clientes\<slug>\docs\superpowers\` (alineado con la raíz única).

### Reglas de degradación
- **Falta `arquitectura.csv`** al ensamblar → master **se detiene** y deriva a correr
  arquitectura-seo. Dependencia dura: master **no** genera el árbol.
- **Falta `contexto-<slug>.md`** en framing → master hace su propia entrevista de discovery
  (fallback) y sugiere base-cliente. No bloquea.
- **Falta el bundle de diagnóstico** (Escenario A) → ensambla con lo que haya y marca los huecos
  como **checklist de datos privada** en §13. No fabrica.
- **Falta salida de schema-graph** → §5 se queda en anclaje estratégico + anota
  *"generación pendiente: schema-graph"*.

Regla de oro: **consumir, no regenerar**; insumo duro ausente → detenerse y derivar; insumo
blando ausente → degradar marcando el hueco.

---

## 3. Los dos escenarios

Master ramifica según **un solo campo del discovery: `estado del sitio`**.

**Escenario B — greenfield** (`estado = greenfield/básico`):
- Framing normal → `enfoque.md`.
- arquitectura-seo en modo greenfield (sin inventario, sin 301; árbol `accion=nueva`).
- Ensamblaje: spec **sabor FOUNDATION** (§13 migración = N/A; sin bundle); planes = ~15 fases de build.
- Validación post-build sobre staging (la orquesta el runtime, no master).

**Escenario A — existente con data** (`estado = con-tráfico`):
- **Fase de DIAGNÓSTICO** previa (sync + crawl + análisis) que master **NO corre**: consume el
  bundle **si existe** para informar la restricción dominante y el enfoque; si no, procede desde
  el contexto de negocio y **recomienda** el baseline (sin inventarlo).
- arquitectura-seo en modo migración (inventario + GSC → árbol con `accion` keep/301/fusionar/
  eliminar + `mapeo-301.csv`).
- Ensamblaje: spec **sabor MIGRACIÓN** (§13 activo, **KPI de retención**, consume el bundle +
  `mapeo-301.csv`); planes con fases **M0-M2 (inventario/benchmark)** antes del build.

**Consistencia:** master consume, no orquesta. En A no invoca las skills de diagnóstico; lee sus
outputs si están. Mantiene la frontera *master = artefacto / orquestador = runtime*.

---

## 4. Alcance quirúrgico (archivo por archivo)

**🟢 INTACTOS (cero cambio):** `00-parametrizacion-vertical.md` · `05-local-gbp.md` ·
`06-geo-eeat.md` · `10-kpis.md` · `11-competitive-linkbuilding.md` · `case-studies.md` ·
`templates/team-bio.md` · `templates/competitive-audit.md`.

**🟡 REESCRITOS (de "genera" a "consume"):**
- `03-architecture.md` — **cambio mayor.** La *elección de enfoque* (§2) se queda en el framing;
  el *diseño de URLs/slugs/content-types/internal-linking* pasa a **"consume `arquitectura.csv` +
  `enlazado.csv`"** (híbrido). Requiere **prohibición + recipe** (ver §5, riesgo #1).
- `04-schema.md` → recorte a **anclaje estratégico** + handoff a schema-graph.
- `08-keywords-clusters.md` → **"consume `mapa-keywords.csv`"**; la metodología de estudio vive en
  arquitectura-seo.
- `07-technical-seo.md` → recorte a **targets/requisitos** (render mode, CWV, IndexNow, foundation
  files); medición → extraccion/seo-vitals.
- `01-discovery.md` → conserva preguntas estratégicas; intake factual anota "tira de
  `contexto-<slug>.md`"; añade rama por `estado del sitio` y handoff a `enfoque.md`.
- `09-content-roadmap.md` → casi igual; anota producción→content-engine, estructura→diseño-secciones.
- `12-plan-phases.md` → fases de arquitectura/schema/keywords pasan a "consume el artefacto";
  inserta M0-M2 de migración.
- `13-migracion-sitio-existente.md` → estrategia intacta; anota que inventario/301 los produce
  arquitectura-seo.
- `templates/page-brief.md` + `content-brief.md` → briefs = lista de páginas del árbol + notas
  estratégicas; estructura/copy → diseño-secciones/content-engine.

**🔵 NUEVO:**
- `references/00b-flujo-y-contratos.md` (o sección en `SKILL.md`): estructura de dos fases,
  contrato de inputs que consumo, reglas de degradación, formato de `enfoque.md`, rama de escenarios.
- `SKILL.md`: actualizar el pipeline (3 artefactos → framing/ensamblaje con arquitectura-seo en
  medio), índice, anti-patrones (+*"regenerar el árbol que ya hizo arquitectura-seo"*), "cómo usar".
- `02-spec-skeleton.md`: marcar en cada § si es framing / ensamblaje / consumido.

Principio del cubo 🟡: no se borra la sabiduría, se **redirige** — donde decía "diseña X" ahora
dice "consume X de la skill Y y añade la capa estratégica".

---

## 5. Plan de verificación

Skill de proceso → se verifica con **subagentes en escenario** (baseline vs con-skill).

**Riesgo #1:** la metodología es tan rica en *diseñar arquitectura* que el agente, aun con el
skill reworked, podría **seguir diseñando el árbol** en vez de consumir `arquitectura.csv`. Es un
fallo de **disciplina** → la reescritura de `03/04/08` necesita **prohibición + recipe**
(writing-skills, "match the form to the failure"): *"NO diseñes el árbol de URLs aquí; ya existe
en `arquitectura.csv`. Si escribes slugs/page-types desde cero, DETENTE"* + receta positiva (lee
el CSV → resume → añade capa estratégica).

**Tests (subagente, cliente sintético):**
1. **RED baseline** — skill ACTUAL + cliente con `arquitectura.csv` + prompt "diseña la estrategia
   SEO" → confirmar que **regenera** la arquitectura (ignora el CSV). Documenta el fallo.
2. **GREEN consumo** — skill reworked, mismo input → **referencia `arquitectura.csv`** (resumen +
   overlay) y **no** re-deriva slugs. Test crítico.
3. **Escenario B** — `estado=greenfield` + árbol `accion=nueva` → spec foundation, §13 N/A.
4. **Escenario A** — `estado=con-tráfico` + bundle + `mapeo-301.csv` → spec migración, KPI retención.
5. **Degradación** — `arquitectura.csv` ausente → se detiene y deriva a arquitectura-seo.
6. **Contratos** — `enfoque.md` del framing tiene los campos que arquitectura-seo Fase 0 espera;
   rutas de I/O correctas.

**Orden:** probar `03` primero (mayor riesgo). Si "prohibición + recipe + consume" funciona ahí,
replicar en `04/08`.
