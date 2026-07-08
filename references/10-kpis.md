# 10 · KPIs, dashboard y tooling

## Jerarquía en 3 tiers
```
Tier 1 — Business outcomes    ← lo que importa al cliente
  leads, leads calificados, distribución por audiencia/segmento, revenue atribuido
Tier 2 — SEO outcomes         ← lo que mueve el negocio
  tráfico orgánico, rankings, visibility GSC (impresiones/clicks/CTR/posición)
  Tier 2.5 — Local SEO: ranking en map pack, acciones GBP, reviews
Tier 3 — Leading indicators   ← lo que controlas hoy
  contenido publicado, backlinks/ref domains, salud técnica (CWV/schema/HTTPS), GEO/AI
```
Cada KPI con **proyección Q1→Q2→Q3→Q4** y método de medición. Targets técnicos permanentes: CWV passing 80%+, schema válido 100%, HTTPS 100%.

## GEO/AI como KPI propio
- **Segmento GA4 de referrals AI** (setup 20 min, hacerlo en M1): `chatgpt.com`, `perplexity.ai`, `gemini.google.com`, `copilot.microsoft.com` → canal "AI" en el dashboard. **Ojo:** esto mide chatbots; los clics desde **AI Overviews llegan como Google orgánico normal y NO son segmentables** — no prometer su medición al cliente.
- **Búsqueda branded en GSC** (impresiones/clics de queries con la marca, tendencia trimestral) como proxy de autoridad: si el GEO funciona, la gente busca la marca después de verla citada.
- Brand mentions en respuestas de AI (sample fijo de queries, check mensual).
- llms.txt devuelve 200 OK (check mensual) · citaciones en Perplexity / aparición en AI Overviews para queries objetivo.

## Tooling stack
| Categoría | Free obligatorio | De pago (escalonado) |
|---|---|---|
| Search data | GSC, Bing Webmaster | Ahrefs / Semrush |
| Analytics | GA4, Cloudflare Analytics | — |
| Local | GBP Insights | BrightLocal |
| Performance | PageSpeed Insights, Lighthouse | Sitebulb |
| Dashboard | Looker Studio | — |
| Tag mgmt | GTM | — |
| Keyword/SERP | (manual) | DataForSEO |

## Cadencia de reporting
| Frecuencia | Esfuerzo | Output |
|---|---|---|
| Semanal | 15 min | check de anomalías |
| Mensual | 1 h | reporte 2 págs |
| Trimestral | 1 día | ejecutivo 5-7 págs + decision gate |
| Anual | — | plan año 2 |

## Atribución de leads (estructural)
UTMs en todo link · GA4 custom dimensions · hidden fields en formularios · WhatsApp con UTM en la query · CRM con pipeline definido. Sin esto, los KPIs Tier 1 no se pueden medir.

## Alertas automáticas (desde M2)
GSC anomaly · Lighthouse-CI cron · UptimeRobot · schema validation cron · backlink loss · Google Alerts de marca.

## Runbook ante caída (ANTES de "optimizar" nada)
Orden de diagnóstico — la causa casi siempre está arriba de la lista:
1. **Técnico**: ¿noindex/robots accidental? ¿caída de cobertura en GSC? ¿404s? ¿deploy/migración reciente? (GSC Cobertura + crawl rápido)
2. **Acción manual / seguridad**: GSC → Manual actions / Security issues.
3. **Core update**: comparar la fecha de la caída con updates confirmados de Google. Si coincide → **no tocar nada reactivamente**; auditar calidad con calma.
4. **Cambio de layout del SERP**: ¿apareció AI Overview / local pack / shopping en tus queries? Impresiones estables + clics abajo = pérdida de CTR, no de ranking.
5. **Estacionalidad**: comparar YoY, no MoM.
6. **Competencia**: ¿entró alguien nuevo al top 3?

Regla: una caída sin causa identificada **no se "optimiza" reescribiendo contenido** — se diagnostica.

## Decision gates (umbral → acción; un gate sin umbral es una reunión)
- **M3** — fijar baseline (no exigir resultados). Umbrales técnicos: indexación = exactamente el árbol designado, CWV passing ≥80%, schema válido 100%. **Si falla → congelar contenido nuevo hasta resolver.**
- **M6** — ¿≥50% de los hubs con impresiones crecientes (GSC, tendencia 3 meses)? **Sí** → abrir los spokes/facetas planificados. **No** → congelar spokes y auditar indexación/calidad/tipo-de-SERP antes de producir más. Canibalización: página secundaria ganando impresiones por la query → redirigir canonical.
- **M9** — ¿ref domains y búsqueda branded creciendo vs M6? **Sí** → duplicar lo que funciona (outreach sobre las piezas top). **No** → reasignar horas de producción a promoción/refresh; elegir qué refrescar con los criterios de pruning (`09`).
- **M12** — reporte de cierre + plan año 2. **Kill criteria honesto**: cluster sin impresiones tras 9 meses con técnica sana → replantear la apuesta (¿SERP hostil? ¿keyword muerta?), no insistir.

En cada gate, re-revisar ≥1 criterio SERP-dependiente (principio 10).
