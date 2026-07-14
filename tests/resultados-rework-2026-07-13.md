# Resultados de verificación — rework de seo-master-plan (2026-07-13)

Rama `rework-consume-artefactos`. Plan: `docs/superpowers/plans/2026-07-13-seo-master-plan-rework.md`.
Verificación por subagente en escenario (skill de proceso, sin tests de código). Cliente sintético
`acme` + variantes (fixtures en scratchpad de la sesión).

## Tests de escenario

### Test 1 — GREEN consumo / greenfield (Escenario B) → PASS
Prompt neutral ("produce §3 siguiendo la skill") contra el `03` reworked, cliente con
`arquitectura.csv` presente (todo `accion=nueva`). El agente:
- Trató `arquitectura.csv` como **fuente de verdad** y embebió un resumen **marcado como derivado**;
  NO re-derivó slugs/page-types.
- Añadió la capa estratégica (restricción dominante, anti-canibalización *verificada* no re-decidida).
- Detectó greenfield por `accion=nueva` → §13 N/A.
- Delegó §4 a `enlazado.csv` y §9 a `mapa-keywords.csv`.
Evidencia: RED baseline (skill previa) regeneraba; con el rework consume. Riesgo #1 del spec neutralizado.

### Test 2 — Migración (Escenario A) → PASS
Cliente `con-tráfico` con `arquitectura.csv` (accion mantener/301/fusionar), `mapeo-301.csv` y bundle
de diagnóstico. El agente:
- Detectó Escenario A → spec **sabor migración**.
- **Consumió** `arquitectura.csv` + `mapeo-301.csv` (lo verificó contra las reglas de §13, NO lo reescribió).
- Fijó **KPI = retención ≥90-95% a semana 6-8** (no crecimiento) + declaración de fluctuación 2-6 semanas.
- Insertó **M0-M2** (inventario/benchmark + quick wins sobre el sitio viejo) y consumió el bundle
  (LCP 4.1s, orfandad del flagship, striking distance de `/plc.html`).
- Detectó gaps reales (301 del blog quick-win ausente; `/sectores/alimentaria/` enlazado pero ausente
  del árbol; doble URL de tableros) y los marcó como **bloqueantes para arquitectura-seo sin fabricarlos**.

### Test 3 — Degradación (sin `arquitectura.csv`) → PASS
Cliente sin `arquitectura.csv`. El agente **se DETUVO**, citó las reglas de degradación de
`00b`/`03`/`SKILL.md`, **no inventó el árbol**, y emitió el handoff a correr `arquitectura-seo`
(vía orquestador — "master consume, no orquesta").

## Revisión por task (SDD, dos veredictos por task)

| Task | Archivos | Spec | Calidad | Notas |
|---|---|---|---|---|
| 1 | 00b (nuevo) + SKILL.md | ✅ | Aprobado | 2 Minor (filas índice 03/08) resueltas en Tasks 3/4 |
| 2 | 01-discovery | ✅ | Aprobado | 1 Minor inocuo |
| 3 | 03-architecture | ✅ | Aprobado (tras fix) | 1 Important (bilingüe) → fix `1c2e61f`; GREEN ✅ |
| 4 | 04-schema + 08-keywords | ✅ | Aprobado | 2 Minor informativos |
| 5 | 07 + 09 + 12 + 13 | ✅ | Aprobado | 1 Minor (gates DoD sin puntero → final review) |
| 6 | 02-spec-skeleton + templates | ✅ | Aprobado | sin issues |

## Minor pendientes para el final review
- `12-plan-phases.md` L31/L41/L44: gates DoD/validación (PSI mobile, schema de todas las páginas)
  sin puntero al dueño → añadir `(→ seo-vitals)` / `(→ schema-graph)` para alinear con la cron de `07`.

## Veredicto
La skill reworked **consume, no regenera** en los tres escenarios; el patrón prohibición+recipe de
`03/04/08` steerea a un agente neutral hacia el consumo. Rework funcional.
