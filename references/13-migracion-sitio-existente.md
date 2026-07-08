# 13 · Migración / sitio existente con tráfico

**Cuándo leer:** discovery Nivel 1 dice "estado del sitio = con tráfico". Este archivo **modifica el plan de Fase 1** de `12-plan-phases.md`: inserta las fases M0-M2 antes de la Fase 1 y amplía Pre-launch/Launch/Post-launch (13-15).

## Regla cero
El KPI de una migración es **retención, no crecimiento** (objetivo: ≥90-95% de clics a semana 6-8). **Declarar al cliente por escrito la fluctuación esperada**: 2-6 semanas de baile de rankings es normal, no un fracaso. Evitar combinar en un mismo release cambio de dominio + reestructura de URLs + rediseño + reescritura de contenido; si el negocio lo obliga, el benchmark debe ser más fino para poder aislar la causa de cualquier caída.

## M0 — Inventario + benchmark (ANTES de diseñar la arquitectura nueva)
- **Inventario por URL** con datos de 12-16 meses: clics/impresiones/posición (GSC), sesiones/conversiones por landing (GA4), backlinks y ref domains por URL, y crawl completo (status, titles, canonicals, schema, noindex).
- **Benchmark congelado pre-migración**: top 50-100 queries con posición, tráfico por sección, # de páginas indexadas, CWV. Sin benchmark no hay medición de retención — es bloqueante, como la Fase 0.
- La arquitectura nueva (§2-§3) se diseña **con el inventario a la vista**: lo que ya rankea pesa en las decisiones de URLs.

## Matriz keep / improve / consolidate / kill (por URL, con umbrales)
| Decisión | Criterio (datos 12m) | Acción |
|---|---|---|
| **Keep** | Tiene clics, conversiones o backlinks; contenido vigente | Migrar 1:1 tocando lo mínimo |
| **Improve** | Impresiones sin clics; **posición 5-15**; contenido flojo | Migrar + rewrite (ver quick wins) |
| **Consolidate** | Varias URLs thin sobre el mismo tema; canibalización | Fusionar en una; 301 de las demás |
| **Kill** | 0 clics + 0 backlinks + 0 valor de negocio en 12m | 410 (o 301 al padre temático si tiene algún backlink) |

Cada URL del inventario recibe exactamente una decisión. El % de kill/consolidate suele ser alto en sitios viejos (tags, archivos, páginas thin) — eso es salud, no pérdida.

## Quick wins M1-M2 (el ROI más rápido del año 1)
Con GSC histórico disponible, esto se hace **aunque la migración se retrase**:
1. **Striking distance**: queries en posición 5-15 → rewrite de title/meta (CTR), reforzar enlaces internos hacia esas páginas desde hubs y páginas fuertes, completar el contenido contra el top 3 actual del SERP.
2. Si la migración tarda >4-6 semanas, ejecutar sobre el sitio **viejo**: el equity mejorado se transfiere por los 301.

## Mapa 301 (reglas)
- **1:1** URL vieja → equivalente nuevo. **Nunca todo a Home** (Google lo trata como soft-404). Máximo 1 salto.
- Cubrir variantes: parámetros (`?p=123`), mayúsculas, con/sin trailing slash, http, www.
- Kill con backlinks → 301 al padre temático, no al vacío.
- El mapa vive en un archivo versionado y se mantiene ≥12 meses.

## Pre-switch — crawl diff staging vs producción (bloqueante de launch)
Crawl paralelo de staging y producción: URLs esperadas vs reales, titles, canonicals, robots/noindex, schema, status codes. **Cualquier diferencia no explicada bloquea el launch.** Validar el mapa 301 completo en staging (script o crawler en modo lista).

## Día del switch + ventana de monitoreo
| Cuándo | Qué |
|---|---|
| Día 0 | 301 activos → verificación inmediata · submit sitemap nuevo (mantener el viejo accesible 2-4 semanas) · IndexNow · solicitar indexación de top páginas en GSC |
| Días 1-14 (diario) | 404s en GSC/logs · cobertura de indexación · muestreo de redirects · top queries del benchmark |
| Semanas 2-8 (semanal) | Retención de clics vs benchmark · posiciones del top 50 · ref domains (pérdida de backlinks) |

**Criterio de alerta:** caída >20% sostenida 2+ semanas en una sección → auditar sus 301, indexación y render **antes** de tocar contenido. La causa de una caída post-migración casi siempre es técnica, no editorial.
