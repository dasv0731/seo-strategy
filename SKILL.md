---
name: seo-master-plan
description: Use when starting or scoping a full SEO strategy for any business (B2B, B2C, local, e-commerce, YMYL, SaaS). Guides the complete pipeline — discovery → design spec → phased implementation plans → content → KPIs — distilled from two real 12-month plans (B2B industrial cross-matrix and YMYL person-based health). Stack-agnostic. Triggers on "plan SEO", "SEO strategy", "estrategia SEO", "auditar y planear SEO", "arquitectura SEO", "content cluster plan", "GEO / AI Overviews plan".
---

# SEO Master Plan — punto de entrada

Codifica una metodología SEO integral a 12 meses, **probada dos veces** en proyectos reales:

- **AioTech** — ingeniería eléctrica/automatización, B2B industrial, multi-ubicación, arquitectura **matriz cruzada** (servicios × sectores × ubicaciones), marca anclada en `Organization`.
- **Inspira Bienestar** — psicóloga individual, **YMYL salud**, sede única, arquitectura **especialidad-first**, marca anclada en `Person`.

El mismo esqueleto produjo ambos. Tu trabajo con este skill es **parametrizar ese esqueleto** para el negocio que tienes enfrente, no re-inventarlo. Ver `references/case-studies.md` para ver lado a lado cómo se adapta.

Es **agnóstico al stack**: la metodología (arquitectura, clusters, schema, GEO, E-E-A-T, KPIs) no depende de ningún CMS ni framework. El stack se decide en discovery; el skill solo se enfoca en SEO.

---

## El pipeline (los 3 artefactos)

```
Cuestionario Discovery  →  Design Spec (§0–§14)  →  Planes por mes/trimestre  →  Contenido + KPIs
   (intake)                 (arquitectura)            (tareas ejecutables)
```

1. **Discovery** — entrevista/intake estructurado. Output: `docs/superpowers/discovery/YYYY-MM-DD-{cliente}-discovery.md`. Ver `references/01-discovery.md`.
2. **Design Spec** — el documento de diseño que gobierna todo, secciones §0–§14. Output: `docs/superpowers/specs/YYYY-MM-DD-{cliente}-seo-design.md`. Ver `references/02-spec-skeleton.md`.
3. **Planes de implementación** — derivados del spec, ejecutables tarea-por-tarea con checkboxes, uno por mes/trimestre. Cada plan termina con un **Self-Review** que mapea cada sección del spec a la(s) fase(s) que la cubren. Output: `docs/superpowers/plans/YYYY-MM-DD-{cliente}-seo-mesN-plan.md`. Ver `references/12-plan-phases.md`.

El spec se construye con el skill `superpowers:brainstorming`; los planes con `superpowers:writing-plans`; la ejecución con `superpowers:subagent-driven-development` o `executing-plans`.

---

## Cómo usar este skill

**Si empiezas un proyecto nuevo:** trabaja el pipeline en orden.
1. Corre discovery (`references/01-discovery.md`) — no avances sin los datos del Nivel 1 (bloqueantes).
2. **Identifica la restricción dominante** (ver principio 1 abajo) antes de decidir arquitectura.
3. Elige enfoque de arquitectura justificando descartados y trade-off (`references/03-architecture.md`).
4. Redacta el spec sección por sección (`references/02-spec-skeleton.md`), apoyándote en las referencias temáticas.
5. Deriva planes de implementación por fase (`references/12-plan-phases.md`).

**Si refinas un proyecto existente:** ve directo a la referencia temática relevante (schema, GEO, local, KPIs…).

**Si auditas/comparas:** usa `references/case-studies.md` + las referencias temáticas como checklist.

---

## Principios transversales (lo que más se repite en ambos planes)

Hazlos explícitos en cada spec. Son la diferencia entre un plan que funciona y uno genérico.

1. **Restricción dominante primero.** Antes de la arquitectura, identifica la fuerza que gobierna TODAS las decisiones siguientes y dedícale una sección (§0.1). En Inspira fue **YMYL / E-E-A-T en salud** (condiciona arquitectura, schema, contenido, conversión, off-site). En AioTech fue **cumplimiento normativo demostrable + ciclo de venta B2B largo**. Para e-commerce sería catálogo/inventario; para SaaS, product-led + ciclo de prueba. Sin esto, el plan es plantilla muerta.

2. **Honestidad estructural.** Nunca markup `Review`/`AggregateRating` falso. Nunca credenciales/certificaciones no verificables. Todo dato real pendiente va como placeholder explícito (`XXXX` / `// CONFIRMAR`) + entra en una **checklist de datos privada** que se mapea a las fases que lo consumen. En YMYL esto es regla de oro; en B2B también (registros, RUC, membresías).

3. **GEO/AI como ciudadano de primera clase.** robots.txt con allowlist de crawlers AI, `llms.txt` en raíz, citability passage-level (TL;DR 40-60 palabras, FAQ con respuesta directa en la 1ª oración, auto-suficiencia por párrafo), optimización por plataforma. No es un apéndice: va integrado al contenido. Ver `references/06-geo-eeat.md`.

4. **E-E-A-T basado en personas reales.** La autoridad se ancla en humanos verificables (bios, credenciales con `ImageObject`, `Person` schema con `knowsAbout`), no en una entidad anónima. En negocios persona-céntricos (`Person` es el núcleo); en corporativos, el equipo respalda a `Organization`.

5. **Validar antes de avanzar.** Decision gates a M3/M6/M9. Validación de schema pre-deploy (Rich Results Test + Schema Validator + revisión manual). Checklist pre-launch sin bloqueantes. Anti-canibalización resuelta por **intención** + medición trimestral en GSC (si la página secundaria gana impresiones por la query, se redirige el canonical).

6. **Spec primero, planes ejecutables después.** El spec es estratégico y estable; los planes son operativos (tareas con comandos, snippets, validación + commit por tarea). El plan cierra con Self-Review que traza spec↔plan para garantizar cobertura.

7. **Separar informacional (blog) de transaccional (hubs).** Las queries informacionales viven en el blog y enlazan obligatoriamente a su hub comercial; los hubs no se diluyen con contenido informacional. El blog alimenta conversión y construye topical authority.

8. **Un predicado de cierre por fase.** Cada fase del plan declara **un** criterio "Hecho" inspeccionable (un sustantivo verificable, no "trabajo a medias"). Si para decir que una fase terminó necesitas dos respuestas independientes e inconexas, la fase está mal fusionada: pártela. El Self-Review verifica cobertura spec↔plan; este principio verifica que cada fase tenga *una* condición de salida clara — no una lista difusa. Ej.: "el buscador indexa exactamente lo que el árbol designa como indexable" (uno), no "indexabilidad + schema + CWV ok" (tres cosas en una caja).

9. **Modo de renderizado = costura transversal, no tema técnico.** Cómo llega el HTML al buscador (SSR / estático / CSR / híbrido) **no es un punto más de §8**: es una decisión de arquitectura que **indexabilidad (§8 crawl) y rendimiento (§8 CWV) heredan a la vez**. Decídela en discovery (`references/01-discovery.md`: ¿el contenido crítico se ve sin ejecutar JS?) y declárala explícita en el spec, porque afecta a dos frentes que en lo demás son independientes. Si el contenido depende de JS (CSR), "estar indexable" deja de ser trivial y el costo de rendimiento se mueve al cliente. **Letal en arquitecturas a escala** (programático): verifica el modo de render *antes* de escalar contenido, o el % de indexación se cae sin aviso.

10. **Criterios con fecha de caducidad (anti-osificación).** Todo juicio que dependa del **SERP de hoy** (intención de una keyword, qué premia Google para un page-type, si un término es trampa/commodity) se marca con una **condición de re-revisión** — no se trata como verdad permanente. Sin esto, el plan te empuja a ejecutar con disciplina lo correcto-de-hace-dos-años. Versión mínima: en cada decision gate (M3/M6/M9) revisa al menos un criterio SERP-dependiente y pregunta "¿sigue vigente?". No es una skill aparte todavía; es un hábito que se activa cuando hay datos post-ejecución que lo alimenten.

---

## Índice de referencias

| Archivo | Cuándo leerlo |
|---|---|
| `references/01-discovery.md` | Al iniciar — cuestionario de 4 niveles para el intake |
| `references/02-spec-skeleton.md` | Para redactar el spec — esqueleto §0–§14 |
| `references/03-architecture.md` | Decidir enfoque, URLs, content-types, internal linking, anti-canibalización |
| `references/04-schema.md` | Diseñar el grafo JSON-LD y schema por página |
| `references/05-local-gbp.md` | Local SEO, GBP, NAP, reviews (1 sede vs multi) |
| `references/06-geo-eeat.md` | GEO/AI Overviews, llms.txt, citability, E-E-A-T |
| `references/07-technical-seo.md` | CWV, optimizaciones, sitemap, headers, IndexNow, medición, mantenimiento |
| `references/08-keywords-clusters.md` | Keyword research + clustering + conteo de páginas |
| `references/09-content-roadmap.md` | Modelo de producción, roadmap 12m, longitudes, cadencia |
| `references/10-kpis.md` | Jerarquía KPI 3 tiers, reporting, atribución |
| `references/11-competitive-linkbuilding.md` | Tiers de competidores, auditoría, outreach |
| `references/12-plan-phases.md` | Las ~15 fases de un plan de implementación |
| `references/case-studies.md` | Cómo el mismo esqueleto se adapta: AioTech vs Inspira |
| `templates/content-brief.md` | Brief de 1 página por pieza de contenido |
| `templates/page-brief.md` | Brief de página con copy completo |
| `templates/competitive-audit.md` | Ficha por competidor |
| `templates/team-bio.md` | Bio E-E-A-T de equipo/persona |

---

## Anti-patrones

- **Saltarse discovery / la restricción dominante** → plan genérico que no rankea.
- **Copiar la arquitectura matriz cruzada de AioTech a un negocio pequeño** → páginas thin, canibalización, penalización (especialmente grave en YMYL). Elige el enfoque por el tamaño/recursos reales.
- **Markup falso o credenciales inventadas** → violación de guidelines de Google. Innegociable.
- **GEO como apéndice** → AI Overviews ya se come tráfico; va integrado al contenido desde el día 1.
- **Spec sin planes ejecutables** → nada se implementa. Spec sin Self-Review → cobertura sin verificar.
- **Abrir spokes sin volumen/contenido único que los justifique** → thin content. Valida con GSC trimestral.
