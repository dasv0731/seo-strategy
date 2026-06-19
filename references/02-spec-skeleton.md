# 02 · Esqueleto del Design Spec (§0–§14)

El spec es el documento de diseño que gobierna todo. Estable y estratégico (los planes son lo operativo). Se construye con `superpowers:brainstorming`.

Output: `docs/superpowers/specs/YYYY-MM-DD-{cliente}-seo-design.md`

**Frontmatter YAML:**
```yaml
---
title: {Cliente} — Estrategia SEO Integral 12 meses
date: YYYY-MM-DD
status: draft
owner: {responsable}
phase: design-spec
---
```

---

## Las secciones

### §0 — Panorama del negocio
Narrativa: qué hace, equipo, diferenciadores, audiencias. 3-5 párrafos. Es el contexto del que se derivan todas las decisiones.

### §0.1 — Restricción dominante ⚠️
**La sección más importante.** Identifica la fuerza que gobierna TODAS las decisiones siguientes y explica cómo condiciona arquitectura, schema, contenido, conversión y off-site.
- Inspira → YMYL / E-E-A-T en salud mental.
- AioTech → cumplimiento normativo demostrable + ciclo de venta B2B largo.
- (e-commerce → catálogo/inventario; SaaS → product-led + ciclo de prueba; legal/finanzas → YMYL.)

### §1 — Decisiones estratégicas
Tabla **decisión | valor**: audiencia primaria, alcance geográfico, idioma, servicios flagship/secundarios, modelo de conversión, stack, estado del sitio, scope del spec, dominio asumido.

### §2 — Enfoque de arquitectura
Elegir **un** enfoque entre alternativas (servicio-first / sector-first / matriz cruzada / especialidad-first), **justificarlo**, listar los **descartados** y el **trade-off aceptado**. Ver `03-architecture.md`.

### §3 — Arquitectura de URLs y content-types
3.1 páginas core estáticas · 3.2+ cada content-type (CPT) con jerarquía hub→spokes · reglas de slug · reglas canónicas · archivos en raíz (robots/sitemap/llms.txt).

### §4 — Clusters e internal linking
4.1 topología hub-and-spoke (capas) · 4.2 reglas anti-canibalización (tabla por conflicto) · 4.3 mix de anchor text interno (%) · 4.4 profundidad de clic + bloques de linking reutilizables.

### §5 — Schemas y datos estructurados
5.1 estrategia de grafo JSON-LD con `@id` · 5.2 tabla schema/dónde/propósito · 5.3 esqueleto del grafo en Home · 5.4 validación obligatoria pre-deploy. Ver `04-schema.md`.

### §6 — Local SEO y GBP
Principio rector (1 sede vs service-area) · config GBP · estructura de página por ciudad · NAP consistency · estrategia de reviews. Ver `05-local-gbp.md`. (Omitir/reducir si no hay componente local.)

### §7 — GEO, AI Overviews, llms.txt y E-E-A-T
robots.txt crawlers AI · llms.txt · citability passage-level · E-E-A-T concreto · brand mentions off-site · optimización por plataforma · (YMYL: ética/seguridad de contenido). Ver `06-geo-eeat.md`.

### §8 — Technical SEO foundation
Hosting · criterios de stack (+ qué evitar) · CWV targets · optimizaciones · sitemap · headers · mobile-first · IndexNow · setup de medición · mantenimiento cron. Ver `07-technical-seo.md`.

### §9 — Keyword research y mapa por cluster
Metodología 4 pasos · un cluster por servicio flagship + secundarios + sectores + ubicaciones · tabla de total de páginas indexables año 1. Ver `08-keywords-clusters.md`.

### §10 — Plan de contenido 12 meses
Modelo de producción · roles+horas · plantilla de brief · roadmap trimestral · cadencia · plantillas de longitud · promoción cross-channel. Ver `09-content-roadmap.md`.

### §11 — Análisis competitivo y link building
Tipología de competidores por tier · auditoría competitiva · gaps · estrategia link building 12m · anchor externo · outreach. Ver `11-competitive-linkbuilding.md`. *(En Inspira esto es más ligero: off-site = autoridad de la persona.)*

### §12 — KPIs, dashboard y tooling
Jerarquía 3 tiers · proyección Q1-Q4 · tooling · reporting · atribución · alertas. Ver `10-kpis.md`.

### §13 — Roadmap consolidado, riesgos y supuestos
Recursos (hrs/semana) · presupuesto año 1 · supuestos críticos · riesgos + mitigaciones · out of scope · definition of success · decision gates.

### §14 — Briefs de página (con copy)
Convenciones globales (header/footer/CTA/breadcrumbs/mobile/tono) + un brief detallado por página del **primer hito**. Ver `templates/page-brief.md`.

### Apéndices
- **A** — Páginas fuera del primer hito (fases posteriores).
- **B** — Glosario de términos.

---

## Numeración flexible
La numeración varía según el negocio (Inspira usó §0–§13 sin dimensión de sectores; AioTech §0–§14 con matriz completa). Adapta: **omite secciones que no apliquen y registra por qué**. El orden conceptual (panorama → restricción → decisiones → arquitectura → schema → local → GEO → técnico → keywords → contenido → competencia → KPIs → roadmap → briefs) se mantiene.

## Spec self-review (antes de pasar a planes)
1. **Placeholders** — ¿quedan TBD/TODO/datos vagos? Conviértelos en `// CONFIRMAR` + checklist de datos.
2. **Consistencia interna** — ¿alguna sección contradice a otra? ¿arquitectura ↔ features?
3. **Scope** — ¿enfocado para un set de planes, o necesita descomposición?
4. **Ambigüedad** — ¿algún requisito interpretable de dos formas? Elige una y hazla explícita.
