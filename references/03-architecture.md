# 03 · Arquitectura: enfoque, URLs, content-types, internal linking

## Elegir enfoque (el más importante)

Documenta el elegido, los **descartados** y el **trade-off aceptado**.

| Enfoque | Dimensiones | Cuándo | Riesgo |
|---|---|---|---|
| **Servicio-first** | `/servicios/[slug]` hub→spokes | Negocio mono-audiencia, pocos servicios | Limitado si hay sectores/ubicaciones fuertes |
| **Sector-first** | `/sectores/[slug]` | La decisión la guía la industria del cliente | Diluye keywords de servicio |
| **Matriz cruzada** (AioTech) | servicios × sectores × ubicaciones + casos | Audiencia mixta + multi-ubicación + sectorial + horizonte 12m + **recursos para 2-3× contenido** | Canibalización si no hay disciplina de canonicales |
| **Especialidad-first** (Inspira) | hub-and-spoke por problemática, anclado en `Person` | Profesional/equipo pequeño, YMYL, sede única | — (el seguro por defecto) |

**Regla de oro:** elige por **tamaño y recursos reales**. Copiar la matriz cruzada a un negocio pequeño produce páginas thin y canibalización — **penalización grave en YMYL**. Una persona no sostiene decenas de páginas únicas.

---

## Reglas de slug
Minúsculas · sin diacríticos (`automatizacion`, no `automatización`) · guión separador · sin stopwords innecesarios · sin `.html` · trailing slash consistente forzado por 301 · forzar sin-www + HTTPS por 301.

## Content-types (CPT / colecciones)
Patrón universal, no específico de ningún CMS: cada dimensión es un content-type (colección) con **hub overview + jerarquía hub→spokes**: `/[tipo]/[hub-slug]/[spoke-slug]`.

Ejemplos de dimensiones canónicas:
- **Servicios** — canónico transaccional.
- **Sectores** — hub por audiencia / decision-stage.
- **Ubicaciones** — local SEO / service area.
- **Casos** — prueba E-E-A-T transversal.
- **Blog** — pillar + clusters (informacional).

## Reglas canónicas
- Canonical auto-referente por content-type.
- Taxonomías de filtro (tag/categoría) → `noindex` salvo que tengan copy curado único.
- Paginación de listings → canonical a sí misma (sin rel prev/next, deprecado).
- Trailing slash consistente.

---

## Anti-canibalización (tabla por conflicto típico)

| Conflicto | Página canónica | La otra enlaza con anchor |
|---|---|---|
| `[servicio] + [ciudad]` | `/ubicaciones/[ciudad]` | "cobertura en [ciudad]" |
| `[servicio] + [sector]` | `/sectores/[sector]` | "aplicaciones en [sector]" |
| `[servicio]` genérico | `/servicios/[slug]` (hub) | — |
| `[ciudad] + [servicio específico]` low-volume | `/servicios/[slug]` | mencionar ciudad sin H1 dedicado |

Resolución: por **mayor intent local/sectorial** + medición trimestral de impresiones en GSC. Si la página secundaria gana impresiones por la query → se redirige el canonical.

---

## Internal linking

- **Topología hub-and-spoke en capas**: Home → hubs de cada dimensión → spokes; casos cruzan transversalmente.
- Toda página crítica **≤ 3 clics desde Home**. El footer global expone los hubs principales (servicios + sectores + ubicaciones) para garantizarlo.
- **Breadcrumbs** en todas las páginas (excepto Home) con `BreadcrumbList` JSON-LD.

### Bloques de internal linking reutilizables (componentes)
1. "Servicios/áreas relacionados" — 3-4 cards.
2. "Sectores que atendemos" / "Para quién es".
3. "Cobertura" / "Atención local + online".
4. "Casos similares" — 3 cards.
5. "Recursos del blog" — 3-4 cards (blog → hub).
6. "Hablemos de tu proyecto" / "Agenda tu cita" — CTA (todas las páginas).
7. Bloque de **autoría** (`Person`) en contenido clínico/técnico — refuerza E-E-A-T.

### Mix de anchor text interno
| Tipo | % | Ejemplo |
|---|---|---|
| Exact-match | 10–15% | "automatización industrial" |
| Partial-match | 40–50% | "soluciones de automatización con PLC" |
| Branded | 15–20% | "los proyectos de {marca}" |
| Generic | 10–15% | "ver detalle", "más información" |
| Naked URL | 5–10% | "dominio.com/servicios/..." |

---

## Separación informacional ↔ transaccional
Las queries **informacionales viven en el blog** (pillar + clusters) y **enlazan obligatoriamente a su hub comercial**. Los hubs no se diluyen con contenido informacional. Así el blog alimenta conversión y construye topical authority sin canibalizar el intent transaccional.
