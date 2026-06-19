# 08 · Keyword research y clustering

## Metodología (4 pasos)
1. **Seed expansion** — cada servicio/área flagship genera ~80-150 keywords (DataForSEO Labs, Keyword Planner, SERP scraping manual, "People Also Ask").
2. **Filtrado por intent** — informacional / navegacional / comercial / transaccional.
3. **Mapeo 1 keyword principal + 3-5 secundarias por página** — evita canibalización (una página, una intención dominante).
4. **Local modifier strategy** — `[servicio] + [ciudad]` se sirve desde `/ubicaciones/[ciudad]`; `[servicio] + [sector]` desde `/sectores/[sector]`.

## Estructura de una tabla de cluster
Una por servicio flagship + secundarios + por sector + por ubicación:

| Keyword | Intent | Página canónica | Vol. estimado |
|---|---|---|---|
| automatización industrial | comercial | hub | 200-500 |
| programación PLC Siemens | comercial | spoke PLC | 30-100 |
| empresa automatización Quito | transaccional | `/ubicaciones/quito` | 30-100 |
| permisos ARCERNNR | informacional | blog | — |

Cada cluster de servicio define su **pillar de blog** + N posts cluster (cola larga). Las queries informacionales → blog, enlazando al hub comercial.

## Disciplina anti-thin (clave en YMYL y negocios pequeños)
**Abrir un spoke solo cuando haya volumen Y contenido único** que lo justifique. Validar con data GSC trimestral antes de expandir. En negocios pequeños, empezar con hubs y dejar spokes para fase 2.

## Total de páginas indexables esperadas (año 1)
Tabla de planificación — ejemplos de los dos casos:

| Tipo | AioTech (matriz) | Inspira (especialidad) |
|---|---|---|
| Core estáticas | 5 | 9 |
| Hubs de servicio/área | 5 | 6 |
| Spokes | 19 | 0-6 (fase 2) |
| Sectores | 4 | — |
| Ubicaciones / modalidad | 7 | 2 |
| Casos | 8-15 | — |
| Pillar pages | 5 | 4-5 |
| Cluster posts | 30-40 | 20-30 |
| **Total año 1** | **~80-95** | **~45-60** |

El tamaño del inventario debe ser **sostenible con los recursos reales** de producción de contenido (ver `09-content-roadmap.md`).
