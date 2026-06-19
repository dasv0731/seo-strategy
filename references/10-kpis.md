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
- Brand mentions en respuestas de AI (sample fijo de queries, check mensual).
- llms.txt devuelve 200 OK (check mensual).
- Citaciones en Perplexity / aparición en AI Overviews para queries objetivo.

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

## Decision gates
- **M3** — fijar baseline (no esperar resultados aún). Validar indexación y CWV.
- **M6** — ¿clusters ganando impresiones? ¿abrir spokes? ¿redirigir canonicales?
- **M9** — ¿autoridad off-site creciendo? ¿qué refrescar?
- **M12** — reporte de cierre + plan año 2.
